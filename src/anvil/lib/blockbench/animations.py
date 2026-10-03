"""Converts Blockbench animations into `anvil.api.models.animations.Animations`."""

import re
from collections import defaultdict
from enum import StrEnum
from typing import Any, Dict, List, Optional, Union

from anvil.api.models.animations import _Animation, Animations


class _ChannelType(StrEnum):
    """Blockbench animation channel names used in keyframe data."""

    POSITION = "position"
    ROTATION = "rotation"
    SCALE = "scale"
    PARTICLE = "particle"
    SOUND = "sound"
    TIMELINE = "timeline"


def _adjust_value(
    val: Union[str, float, int], negate: bool = False
) -> Union[float, str]:
    if isinstance(val, str):
        # Blockbench reads blank values as 0
        val = val.strip() or 0
    is_num = isinstance(val, (int, float)) or (
        isinstance(val, str) and re.match(r"^-?\d+\.?\d*$", val)
    )
    if is_num:
        num = float(val)
        if negate:
            num = -num
        return round(num, 4) + 0.0
    else:
        if negate:
            return f"-({val})"
        return str(val)


def _process_vector(
    values: List[Any], negate_indices: List[int]
) -> List[Union[float, str]]:
    return [_adjust_value(v, i in negate_indices) for i, v in enumerate(values)]


def _point_values(point: Dict[str, Any]) -> List[Any]:
    """Keyframe point as [x, y, z], not relying on dict ordering."""
    if all(axis in point for axis in ("x", "y", "z")):
        return [point["x"], point["y"], point["z"]]
    return list(point.values())


def _process_vector_channel(
    keyframes: List[dict], negate_indices: List[int]
) -> Dict[float, Any]:
    """Converts Blockbench position/rotation/scale keyframes to Bedrock values."""
    target_dict: Dict[float, Any] = {}
    is_step = False
    parsed_kfs = []

    for kf in keyframes:
        time = round(float(kf.get("time")), 4)
        interp = kf.get("interpolation", "linear")
        pts = [_point_values(pt) for pt in kf.get("data_points")]
        parsed_kfs.append((time, interp, pts))

    for i, (time, interp, pts) in enumerate(parsed_kfs):
        points_processed = [_process_vector(pt, negate_indices) for pt in pts]
        prev_points_processed = []
        if i > 0:
            prev_points_processed = [
                _process_vector(pt, negate_indices) for pt in parsed_kfs[i - 1][2]
            ]

        final_val = None

        if interp in ("linear", "bezier"):
            if is_step:
                if prev_points_processed:
                    final_val = {
                        "pre": prev_points_processed[0],
                        "post": points_processed[0],
                    }
                is_step = False
            elif len(points_processed) == 2:
                final_val = {
                    "pre": points_processed[0],
                    "post": points_processed[1],
                }
            elif len(points_processed) == 1:
                final_val = points_processed[0]

        elif interp == "catmullrom":
            final_val = {
                "post": points_processed[0] if points_processed else [],
                "lerp_mode": interp,
            }
            is_step = False

        elif interp == "step":
            if is_step and prev_points_processed:
                final_val = {
                    "pre": prev_points_processed[0],
                    "post": points_processed[0],
                }
            else:
                final_val = points_processed[0]
            is_step = True

        if final_val is not None:
            target_dict[time] = final_val

    return target_dict


def _animation_args(data: Dict[str, Any]) -> Dict[str, Any]:
    """Arguments for `Animations.animation` from a Blockbench animation."""
    loop_map = {
        "once": False,
        "loop": True,
        "hold": "hold_on_last_frame",
    }
    return {
        "name": data.get("name", "animation"),
        "length": round(data.get("length", 0.0), 4),
        "loop": loop_map.get(data.get("loop", "once"), False),
        "anim_time_update": data.get("anim_time_update"),
        "override_previous_animation": data.get("override", False),
    }


def _populate_animation(anim: _Animation, data: Dict[str, Any]) -> None:
    vector_channels = {
        _ChannelType.POSITION: [0],
        _ChannelType.ROTATION: [0, 1],
        _ChannelType.SCALE: [],
    }

    for animator in data.get("animators", {}).values():
        bone_name = animator.get("name")
        if not bone_name:
            continue

        channels = defaultdict(list)
        for kf in animator.get("keyframes", []):
            channels[kf.get("channel")].append(kf)
        for kfs in channels.values():
            kfs.sort(key=lambda k: float(k.get("time")))

        # Bones with no keyframes are not created, so they are never emitted.
        has_vectors = any(channels.get(c) for c in vector_channels)
        if has_vectors:
            bone = anim.bone(
                bone_name,
                relative_to_rotation=(
                    "entity" if animator.get("rotation_global", False) else None
                ),
            )
            for channel, negate in vector_channels.items():
                for time, value in _process_vector_channel(
                    channels.get(channel, []), negate
                ).items():
                    bone._set_keyframe(str(channel), time, value)

        for kf in channels.get(_ChannelType.PARTICLE, []):
            time = round(float(kf.get("time")), 4)
            for particle in kf.get("data_points"):
                if not particle.get("effect", "").strip():
                    continue
                anim.particle(
                    time,
                    particle.get("effect", "").replace("\n", ""),
                    particle.get("locator", "").replace("\n", ""),
                    particle.get("script", "").replace("\n", ""),
                )

        for kf in channels.get(_ChannelType.SOUND, []):
            time = round(float(kf.get("time")), 4)
            for effect in kf.get("data_points"):
                if not effect.get("effect"):
                    continue
                anim.sound(time, effect["effect"], effect.get("locator") or "")

        for kf in channels.get(_ChannelType.TIMELINE, []):
            time = round(float(kf.get("time")), 4)
            anim.timeline(time, kf.get("data_points")[0]["script"])


class _AnimationsManager:
    def __init__(self, name: str, source: str, bbmodel: dict) -> None:
        self._name = name
        self._source = source

        self._file: Optional[Animations] = None
        self._bb_animations: Dict[str, dict] = {}

        for anim_dict in bbmodel.get("animations", []):
            self._bb_animations[_animation_args(anim_dict)["name"]] = anim_dict

    def queue_animation(self, animation_name: str) -> _Animation:
        """Adds the animation to this model's set (once) and returns it.

        The returned animation can be edited further before export.
        """
        if self._file is not None:
            existing = self._file.get(animation_name)
            if existing is not None:
                return existing

        anim_dict = self._bb_animations.get(animation_name)
        if anim_dict is None:
            raise ValueError(
                f"Animation '{animation_name}' not found in blockbench model '{self._name}'."
            )

        if self._file is None:
            self._file = Animations(self._name)
        anim = self._file.animation(**_animation_args(anim_dict))
        _populate_animation(anim, anim_dict)
        return anim

    def __export__(self) -> None:
        if self._file is not None and self._file.has_animations:
            self._file.queue(self._source)
