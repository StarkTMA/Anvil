"""Builders for Bedrock animation files (``*.animations.json``).

An :class:`Animations` is one animations file holding any number of
:class:`_Animation` objects. An animation hands out :class:`_AnimBone` objects
by bone name, and each channel call returns the same bone so keyframes chain.

Example:
    ```python
    anims = Animations("my_mob")

    walk = anims.animation("walk", length=1.0, loop=True)
    walk.bone("arm").rotation(0.0, [0, 0, 0]).rotation(0.5, [0, 30, 0]).rotation(
        1.0, [0, 0, 0]
    )
    walk.bone("body").position(0.5, [0, 1, 0], pre=[0, 0, 0])
    walk.particle(0.25, "minecraft:dust", locator="foot")
    walk.sound(0.25, "step")
    walk.timeline(0.5, "v.step = 1;")

    anims.queue()
    ```
"""

import os
from typing import Any, Dict, List, Optional, Sequence, Union

from anvil.api.models.geometry import Geometry
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes

_Value = Sequence[Union[float, int, str]]

_CHANNELS = ("position", "rotation", "scale")


def _time(value: Union[float, int, str]) -> float:
    return round(float(value), 4)


def _no_newline(value: str, what: str, time: float) -> None:
    if "\n" in value:
        raise ValueError(f"Newline in {what} at {time}")


class _AnimBone:
    """Keyframes for one bone. Created through :meth:`_Animation.bone`."""

    def __init__(self, name: str, relative_to_rotation: Optional[str] = None) -> None:
        self.name = name
        self.relative_to_rotation = relative_to_rotation
        self._channels: Dict[str, Dict[float, Any]] = {c: {} for c in _CHANNELS}

    def _set_keyframe(self, channel: str, time: float, value: Any) -> "_AnimBone":
        """Stores a keyframe whose value is already in Bedrock form.

        `value` is a vector, or a dict such as ``{"pre": ..., "post": ...}``.
        """
        if channel not in self._channels:
            raise ValueError(
                f"Unknown animation channel '{channel}'. Expected one of {_CHANNELS}."
            )
        self._channels[channel][_time(time)] = value
        return self

    def _keyframe(
        self,
        channel: str,
        time: float,
        value: _Value,
        pre: Optional[_Value],
        lerp_mode: Optional[str],
    ) -> "_AnimBone":
        if pre is not None and lerp_mode is not None:
            raise ValueError("A keyframe cannot use both 'pre' and 'lerp_mode'.")
        if pre is not None:
            keyframe: Any = {"pre": list(pre), "post": list(value)}
        elif lerp_mode is not None:
            keyframe = {"post": list(value), "lerp_mode": lerp_mode}
        else:
            keyframe = list(value)
        return self._set_keyframe(channel, time, keyframe)

    def position(
        self,
        time: float,
        value: _Value,
        *,
        pre: Optional[_Value] = None,
        lerp_mode: Optional[str] = None,
    ) -> "_AnimBone":
        """Adds a position keyframe. `pre` makes a step, `lerp_mode` e.g. 'catmullrom'."""
        return self._keyframe("position", time, value, pre, lerp_mode)

    def rotation(
        self,
        time: float,
        value: _Value,
        *,
        pre: Optional[_Value] = None,
        lerp_mode: Optional[str] = None,
    ) -> "_AnimBone":
        """Adds a rotation keyframe. `pre` makes a step, `lerp_mode` e.g. 'catmullrom'."""
        return self._keyframe("rotation", time, value, pre, lerp_mode)

    def scale(
        self,
        time: float,
        value: _Value,
        *,
        pre: Optional[_Value] = None,
        lerp_mode: Optional[str] = None,
    ) -> "_AnimBone":
        """Adds a scale keyframe. `pre` makes a step, `lerp_mode` e.g. 'catmullrom'."""
        return self._keyframe("scale", time, value, pre, lerp_mode)

    def is_empty(self) -> bool:
        return not any(self._channels.values())

    def compile(self) -> dict:
        data: Dict[str, Any] = {}
        if self.relative_to_rotation:
            data["relative_to"] = {"rotation": self.relative_to_rotation}
        for channel in _CHANNELS:
            keyframes = self._channels[channel]
            if keyframes:
                data[channel] = dict(sorted(keyframes.items()))
        return data


class _Animation:
    """A single animation. Only create it through :meth:`Animations.animation`."""

    def __init__(
        self,
        name: str,
        length: Optional[float] = None,
        loop: Union[bool, str] = False,
        anim_time_update: Optional[str] = None,
        override_previous_animation: bool = False,
    ) -> None:
        """`length=None` uses the time of the last keyframe/event."""
        self.name = name
        self.length = length
        self.loop = loop
        self.anim_time_update = anim_time_update
        self.override_previous_animation = override_previous_animation
        self._bones: Dict[str, _AnimBone] = {}
        self._particles: Dict[float, List[dict]] = {}
        self._sounds: Dict[float, List[dict]] = {}
        self._timeline: Dict[float, List[str]] = {}
        # Set by Animations.animation
        self._file: Optional["Animations"] = None

    @property
    def file(self) -> "Animations":
        """The animations file this animation belongs to."""
        if self._file is None:
            raise ValueError(
                f"Animation '{self.name}' does not belong to an animations file. Create it with Animations.animation()."
            )
        return self._file

    @property
    def identifier(self) -> str:
        """How entities reference this animation: ``animation.<namespace>.<file>.<name>``."""
        return self.file._full_name(self)

    @property
    def loop(self) -> Union[bool, str]:
        return self._loop

    @loop.setter
    def loop(self, value: Union[bool, str]) -> None:
        if value is not True and value is not False and value != "hold_on_last_frame":
            raise ValueError(
                f"Animation '{self.name}' loop must be True, False or 'hold_on_last_frame', got {value!r}."
            )
        self._loop = value

    def _last_time(self) -> float:
        times: List[float] = [0.0]
        for bone in self._bones.values():
            for keyframes in bone._channels.values():
                times.extend(keyframes)
        times.extend(self._particles)
        times.extend(self._sounds)
        times.extend(self._timeline)
        return max(times)

    def bone(
        self, name: str, *, relative_to_rotation: Optional[str] = None
    ) -> _AnimBone:
        """Returns the keyframes of `name`, creating them on first use."""
        bone = self._bones.get(name)
        if bone is None:
            bone = self._bones[name] = _AnimBone(name, relative_to_rotation)
        elif relative_to_rotation is not None:
            bone.relative_to_rotation = relative_to_rotation
        return bone

    def particle(
        self,
        time: float,
        effect: str,
        locator: str = "",
        script: Optional[str] = None,
    ) -> "_Animation":
        t = _time(time)
        _no_newline(effect, "particle effect", t)
        _no_newline(locator, "particle locator", t)
        value = {"effect": effect, "locator": locator}
        if script:
            _no_newline(script, "particle script", t)
            value["pre_effect_script"] = (script + ";").replace(";;", ";")
        self._particles.setdefault(t, []).append(value)
        return self

    def sound(self, time: float, effect: str, locator: str = "") -> "_Animation":
        t = _time(time)
        _no_newline(effect, "sound", t)
        value = {"effect": effect}
        if locator != "":
            value["locator"] = locator
        self._sounds.setdefault(t, []).append(value)
        return self

    def timeline(self, time: float, script: str) -> "_Animation":
        t = _time(time)
        value = (script + ";").replace(";;", ";")
        _no_newline(value, "timeline", t)
        self._timeline.setdefault(t, []).append(value)
        return self

    def compile(self, full_name: str) -> dict:
        data: Dict[str, Any] = {}
        length = self.length if self.length is not None else self._last_time()
        if length:
            data["animation_length"] = length
        if self.loop is not False:
            data["loop"] = self.loop
        if self.anim_time_update:
            data["anim_time_update"] = self.anim_time_update
        if self.override_previous_animation:
            data["override_previous_animation"] = self.override_previous_animation

        bones = {
            name: bone.compile()
            for name, bone in self._bones.items()
            if not bone.is_empty()
        }
        if bones:
            data["bones"] = bones

        if self._particles:
            data["particle_effects"] = {
                t: v[0] if len(v) == 1 else v
                for t, v in sorted(self._particles.items())
            }
        if self._sounds:
            # Sounds are always a list, even with a single entry.
            data["sound_effects"] = dict(sorted(self._sounds.items()))
        if self._timeline:
            data["timeline"] = {
                t: v[0] if len(v) == 1 else v for t, v in sorted(self._timeline.items())
            }
        return {full_name: data}


class Animations(AddonObject):
    """An animations file (``<name>.animations.json``) holding many animations."""

    _extension = ".animations.json"
    _path = os.path.join(CONFIG.RP_PATH, "animations")

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._animations: Dict[str, _Animation] = {}

    def animation(
        self,
        name: str,
        length: Optional[float] = None,
        loop: Union[bool, str] = False,
        anim_time_update: Optional[str] = None,
        override_previous_animation: bool = False,
    ) -> _Animation:
        """Creates an animation in this file and returns it.

        This is the only way to add an animation to a set.
        """
        if name in self._animations:
            raise ValueError(f"Duplicate animation '{name}' in '{self._name}'.")
        animation = _Animation(
            name,
            length,
            loop,
            anim_time_update,
            override_previous_animation,
        )
        animation._file = self
        self._animations[name] = animation
        return animation

    @property
    def has_animations(self) -> bool:
        return bool(self._animations)

    def get(self, name: str) -> Optional[_Animation]:
        return self._animations.get(name)

    def validate(self, geometry: Geometry) -> "Animations":
        """Checks that every animated bone and locator exists in `geometry`.

        Raises a single ValueError listing all problems.
        """
        locators = geometry.locator_names
        problems: List[str] = []
        for animation in self._animations.values():
            for name, bone in animation._bones.items():
                if not bone.is_empty() and geometry.find(name) is None:
                    problems.append(f"'{animation.name}': bone '{name}' not found")
            events = [
                *(e for es in animation._particles.values() for e in es),
                *(e for es in animation._sounds.values() for e in es),
            ]
            for event in events:
                locator = event.get("locator")
                if locator and locator not in locators:
                    problems.append(
                        f"'{animation.name}': locator '{locator}' not found"
                    )
        if problems:
            details = "\n  - ".join(sorted(set(problems)))
            raise ValueError(
                f"Animations in '{self._name}' do not match geometry '{geometry.name}':\n  - {details}"
            )
        return self

    def _full_name(self, animation: _Animation) -> str:
        return f"animation.{CONFIG.NAMESPACE}.{self._name}.{animation.name}"

    def compile(self) -> dict:
        content = JsonSchemes.animations_rp()
        for animation in self._animations.values():
            content["animations"].update(animation.compile(self._full_name(animation)))
        return content

    def __export__(self) -> None:
        self.content(self.compile())
        super().__export__()
