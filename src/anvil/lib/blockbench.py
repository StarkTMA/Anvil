import base64
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Dict, List, Optional, Union

import click
from packaging.version import Version

from anvil.api.core.enums import BlockFaces
from anvil.api.core.types import Vector2D
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.lib import FileExists
from anvil.lib.schemas import AddonObject, JsonSchemes


class BlockBenchSource(StrEnum):
    ACTOR = "actors"
    BLOCK = "blocks"
    ITEM = "items"


def adjust_value(
    val: Union[str, float, int], negate: bool = False
) -> Union[float, str]:
    is_num = isinstance(val, (int, float)) or (
        isinstance(val, str) and re.match(r"^-?\d+\.?\d*$", val)
    )
    if is_num:
        num = float(val)
        if negate:
            num = -num
        return round(num, 4) + 0.0
    else:
        if isinstance(val, str) and len(val) == 0:
            raise ValueError("Empty string found in keyframe value.")
        if negate:
            return f"-({val})"
        return str(val)


def process_vector(
    values: List[Any], negate_indices: List[int]
) -> List[Union[float, str]]:
    return [adjust_value(v, i in negate_indices) for i, v in enumerate(values)]


class _BlockCulling(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "block_culling")

    def _build_bones_dict(self, tree: dict) -> None:
        for bone in tree:
            if isinstance(bone, dict):
                bone_group = self._groups[bone["uuid"]]
                bone_name = bone_group["name"]
                self.bones[bone_name] = len(bone.get("children", []))
                if bone.get("children"):
                    self._build_bones_dict(bone.get("children"))

    def __init__(self, name: str, bbmodel: dict) -> None:
        super().__init__(name)
        self._bbmodel = bbmodel
        self._groups = {g["uuid"]: g for g in self._bbmodel["groups"]}
        # self._elements = {e["uuid"]: e for e in self._bbmodel["elements"]}

        self.bones = {}
        self._build_bones_dict(self._bbmodel["outliner"])

        self.content(JsonSchemes.block_culling_rules(self.identifier))

    def add_rule(
        self,
        direction: BlockFaces,
        bone: str,
        face: BlockFaces = None,
        cube_index: int = None,
        # condition: Literal["same_block", "same_block_permutation", "same_culling_layer"] = "",
        # cull_against_full_and_opaque: bool = False,
    ) -> None:
        if bone not in list(map(lambda g: g["name"], self._groups.values())):
            raise ValueError(
                f"Bone '{bone}' not found in blockbench model '{self._bbmodel['model_identifier']}'."
            )
        if cube_index is not None and (
            cube_index < 0 or cube_index >= self.bones[bone]
        ):
            raise ValueError(
                f"Cube index '{cube_index}' out of range for bone '{bone}' in blockbench model '{self._bbmodel['model_identifier']}'."
            )

        if direction == BlockFaces.All or direction == BlockFaces.Side:
            raise ValueError(
                "Direction cannot be 'all' or 'side'. Please specify a single direction."
            )
        if face == BlockFaces.All or face == BlockFaces.Side:
            raise ValueError(
                "Face cannot be 'all' or 'side'. Please specify a single face."
            )
        if face is not None and cube_index is None:
            raise ValueError(
                "Face specified without cube_index. Please specify cube_index when using face."
            )

        rule = {
            "direction": direction.value,
            "geometry_part": {
                "bone": bone,
            },
        }
        if face:
            rule["geometry_part"]["face"] = face.value
        if cube_index is not None:
            rule["geometry_part"]["cube"] = cube_index
        # if condition:
        #    rule["condition"] = condition
        # if cull_against_full_and_opaque:
        #    rule["cull_against_full_and_opaque"] = cull_against_full_and_opaque
        self._content["minecraft:block_culling_rules"]["rules"].append(rule)


class _Geometry(AddonObject):
    _extension = ".geo.json"
    _path = os.path.join(CONFIG.RP_PATH, "models", "entity")

    def __init__(self, name: str, content: dict) -> None:
        super().__init__(name)
        self.content(content)


class _Animation(AddonObject):
    _extension = ".animations.json"
    _path = os.path.join(CONFIG.RP_PATH, "animations")

    def __init__(self, name: str, content: dict) -> None:
        super().__init__(name)
        self.content(content)


@dataclass
class AnimBone:
    name: str
    position: Dict[float, Any] = field(default_factory=dict)
    rotation: Dict[float, Any] = field(default_factory=dict)
    scale: Dict[float, Any] = field(default_factory=dict)
    relative_to_rotation: Optional[str] = None

    def is_empty(self) -> bool:
        return not (self.position or self.rotation or self.scale)


@dataclass
class Animation:
    name: str
    length: float = 0.0
    loop: Union[bool, str] = False
    anim_time_update: Optional[str] = None
    override_previous_animation: bool = False
    bones: Dict[str, AnimBone] = field(default_factory=dict)
    particles: Dict[float, Any] = field(default_factory=dict)
    sounds: Dict[float, Any] = field(default_factory=dict)
    timeline: Dict[float, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict, model_name: str) -> "Animation":
        loop_map = {
            "once": False,
            "loop": True,
            "hold": "hold_on_last_frame",
        }

        anim = cls(
            name=data.get("name", "animation"),
            length=round(data.get("length", 0.0), 4),
            loop=loop_map.get(data.get("loop", "once"), False),
            anim_time_update=data.get("anim_time_update"),
            override_previous_animation=data.get("override", None),
        )
        # Fix override being strictly boolean or None? Original code checked logic.

        # Process animators
        for animator in data.get("animators", {}).values():
            bone_name = animator.get("name")
            if not bone_name:
                continue

            bone = AnimBone(name=bone_name)
            if animator.get("rotation_global", False):
                bone.relative_to_rotation = "entity"

            keyframes_raw = animator.get("keyframes", [])

            # Sort raw keyframes by channel
            channels = defaultdict(list)
            for kf in keyframes_raw:
                channels[kf.get("channel")].append(kf)

            for channel_name, kfs in channels.items():
                kfs.sort(key=lambda k: float(k.get("time")))

                if channel_name == "position":
                    cls._process_vector_channel(
                        bone.position, kfs, [0]
                    )  # Negate X. Verify indices?
                    # Original code: adjust_keyframe_sign(..., num=1) => indices < 1 => index 0. Correct.
                elif channel_name == "rotation":
                    cls._process_vector_channel(
                        bone.rotation, kfs, [0, 1]
                    )  # Negate X, Y.
                    # Original code: adjust_keyframe_sign(..., num=2) => indices < 2 => 0, 1. Correct.
                elif channel_name == "scale":
                    cls._process_vector_channel(bone.scale, kfs, [])
                    # Original: adjust_keyframe_type => no negation. Correct.
                elif channel_name == "particle":
                    cls._process_particle_channel(anim.particles, kfs)
                elif channel_name == "sound":
                    cls._process_sound_channel(anim.sounds, kfs)
                elif channel_name == "timeline":
                    cls._process_timeline_channel(anim.timeline, kfs)

            if not bone.is_empty():
                anim.bones[bone_name] = bone

        return anim

    @staticmethod
    def _process_vector_channel(
        target_dict: Dict, keyframes: List[dict], negate_indices: List[int]
    ):
        is_step = False
        parsed_kfs = []

        # Pre-parse all keyframes for this channel
        for kf in keyframes:
            time = round(float(kf.get("time")), 4)
            interp = kf.get("interpolation", "linear")
            pts = [list(pt.values()) for pt in kf.get("data_points")]
            parsed_kfs.append((time, interp, pts))  # pts is list of lists

        for i, (time, interp, pts) in enumerate(parsed_kfs):
            points_processed = [process_vector(pt, negate_indices) for pt in pts]
            prev_points_processed = []
            if i > 0:
                # Get previous keyframe's points
                prev_points_processed = [
                    process_vector(pt, negate_indices) for pt in parsed_kfs[i - 1][2]
                ]

            # Logic from original _process_..._channel
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
                # Catmullrom usually has 1 point but needs specific object structure
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

    @staticmethod
    def _process_particle_channel(target_dict: Dict, keyframes: List[dict]):
        for kf in keyframes:
            time = round(float(kf.get("time")), 4)
            data = kf.get("data_points")[0]
            effect = data.get("effect", "")
            locator = data.get("locator", "")
            script = data.get("script", "")

            if "\n" in effect or "\n" in locator or "\n" in script:
                raise ValueError(f"Newline in particle keyframe at {time}")

            val = {"effect": effect, "locator": locator}
            if script:
                val["pre_effect_script"] = (script + ";").replace(";;", ";")
            target_dict[time] = val

    @staticmethod
    def _process_sound_channel(target_dict: Dict, keyframes: List[dict]):
        for kf in keyframes:
            time = round(float(kf.get("time")), 4)
            effect = kf.get("data_points")[0].get("effect", "")
            if "\n" in effect:
                raise ValueError(f"Newline in sound at {time}")
            target_dict[time] = {"effect": effect}

    @staticmethod
    def _process_timeline_channel(target_dict: Dict, keyframes: List[dict]):
        for kf in keyframes:
            time = round(float(kf.get("time")), 4)
            val = kf.get("data_points")[0]
            if isinstance(val, str) and "\n" in val:
                raise ValueError(f"Newline in timeline at {time}")
            target_dict[time] = val

    def compile(self, full_name: str) -> dict:
        anim_data = {}
        if self.length:
            anim_data["animation_length"] = self.length
        if self.loop is not False:
            anim_data["loop"] = self.loop
        if self.anim_time_update:
            anim_data["anim_time_update"] = self.anim_time_update
        if self.override_previous_animation:
            anim_data["override_previous_animation"] = self.override_previous_animation

        bones_data = {}
        for bname, bone in self.bones.items():
            b_data = {}
            if bone.relative_to_rotation:
                b_data["relative_to"] = {"rotation": bone.relative_to_rotation}

            # Clean up single value channels? Old code did this.
            # "If len(keys) == 1: ... = list(...)[0]" - wait, that removed the time key?
            # Old code:
            # if len(keys) == 1:
            #      bones[bone_name][channel] = list(bones[bone_name][channel].values())[0]
            # Yes, if only one keyframe, it becomes a static value (no time key).
            # But only if it's not a complex object? Bedrock allows static value.

            for kv_name, kv_dict in [
                ("position", bone.position),
                ("rotation", bone.rotation),
                ("scale", bone.scale),
            ]:
                if not kv_dict:
                    continue
                if len(kv_dict) == 1:
                    # Static value optimization
                    val = list(kv_dict.values())[0]
                    # Check if val is dict (complex keyframe) -> then we might need to keep it as time?
                    # Bedrock allows "rotation": [x,y,z] or "rotation": { "0.0": ... }
                    # If the value is a complex keyframe (step/lerp), it must be in a timeline map?
                    # The old code just took the value. If the value is a list, it's fine. If it's a dict (pre/post), it might not work as static value?
                    # Actually standard bedrock format: "rotation": [0,0,0] is valid. "rotation": { "0.0": ... } is valid.
                    # If we have { "0.0": { "pre":..., "post":... } } -> extracting value makes it object.
                    # Bedrock might not support object as static value (it expects array).
                    # I'll stick to old code behavior: extract it.
                    b_data[kv_name] = val
                else:
                    b_data[kv_name] = kv_dict

                # Special scale check from old code
                if kv_name == "scale" and isinstance(b_data[kv_name], list):
                    # Unique scale check?
                    # if len(set(bones[bone_name]["scale"])) == 1: ...
                    # This checked if all components are same? i.e. uniform scale?
                    # Old code: if len(set(bones[bone_name]["scale"])) == 1: bones[bone_name]["scale"] = bones[bone_name]["scale"][0]
                    # This converts [1, 1, 1] to 1.
                    scale_val = b_data["scale"]
                    if (
                        isinstance(scale_val, list)
                        and len(scale_val) == 3
                        and scale_val[0] == scale_val[1] == scale_val[2]
                    ):
                        b_data["scale"] = scale_val[0]

            if b_data:
                bones_data[bname] = b_data

        if bones_data:
            anim_data["bones"] = bones_data
        if self.particles:
            anim_data["particle_effects"] = self.particles
        if self.sounds:
            anim_data["sound_effects"] = self.sounds
        if self.timeline:
            anim_data["timeline"] = self.timeline

        return {full_name: anim_data}


class _AnimationsManager:
    def __init__(self, name: str, source: str, bbmodel: dict) -> None:
        self._name = name
        self._content = JsonSchemes.animations_rp()
        self._queued = False
        self._source = "actors"  # Original hardcoded? "actors". Defaults to "actors" in signature but overwritten?
        # Original: self._source = "actors" (Line 489)

        self.animations: Dict[str, Animation] = {}

        # Parse all animations immediately
        for anim_dict in bbmodel.get("animations", []):
            anim = Animation.from_dict(anim_dict, name)
            self.animations[anim.name] = anim

    def queue_animation(self, animation_name: str):
        anim = self.animations.get(animation_name)
        if not anim:
            raise ValueError(
                f"Animation '{animation_name}' not found in blockbench model '{self._name}'."
            )

        full_name = f"animation.{CONFIG.NAMESPACE}.{self._name}.{anim.name}"
        if full_name not in self._content["animations"]:
            self._content["animations"].update(anim.compile(full_name))
            self._queued = True

    def _export(self) -> None:
        if self._queued:
            _Animation(self._name, self._content).queue(self._source)


class _TexturesManager:
    def __init__(self, filename: str, source: str, bbmodel: dict) -> None:
        config = CONFIG
        self._name = filename
        self._bbmodel = bbmodel

        self._path = os.path.join(
            config.RP_PATH,
            "textures",
            config.NAMESPACE,
            config.PROJECT_NAME,
            source,
            self._name,
        )
        self._textures = {
            texture.get("name").split(".")[0]: texture
            for texture in self._bbmodel["textures"]
        }
        self._queued_textures: set[str] = set()

    def queue_texture(self, texture: str) -> None:
        if texture in self._textures:
            self._queued_textures.add(texture)
        else:
            raise ValueError(
                f"Texture '{texture}' not found in blockbench model '{self._bbmodel['model_identifier']}'."
            )

    def _export(self) -> None:
        os.makedirs(self._path, exist_ok=True)
        for texture in self._queued_textures:
            image_data = base64.b64decode(
                self._textures[texture]
                .get("source")
                .replace("data:image/png;base64,", "")
            )
            with open(os.path.join(self._path, f"{texture}.png"), "wb") as file:
                file.write(image_data)


@dataclass
class Cube:
    name: str
    origin: List[float]
    size: List[float]
    rotation: List[float] = field(default_factory=lambda: [0, 0, 0])
    pivot: List[float] = field(default_factory=lambda: [0, 0, 0])
    inflate: float = 0.0
    mirror: bool = False
    uv: Union[List[float], Dict[str, Any]] = field(default_factory=dict)
    box_uv: bool = False

    @staticmethod
    def _process_uv(data: dict, box_uv: bool) -> Union[List[float], Dict[str, Any]]:
        if box_uv:
            return data.get("uv_offset", [0, 0])

        uvs = {}
        for face, face_data in data.get("faces", {}).items():
            if face_data.get("texture") is None:
                continue

            uv_map = face_data.get("uv", [])
            rotation = face_data.get("rotation", 0)
            material_instance = face_data.get("material_name", {})

            if face in ("up", "down"):
                uv_map = [uv_map[2], uv_map[3], uv_map[0], uv_map[1]]

            uv_size = [
                round(uv_map[2] - uv_map[0], 2),
                round(uv_map[3] - uv_map[1], 2),
            ]

            if uv_size[0] != 0 and uv_size[1] != 0:
                face_uv = {
                    "uv": [uv_map[0], uv_map[1]],
                    "uv_size": uv_size,
                    "material_instance": material_instance,
                }
                if rotation != 0:
                    face_uv["uv_rotation"] = rotation
                uvs[face] = face_uv
        return uvs

    @classmethod
    def from_dict(cls, data: dict) -> "Cube":
        name = data["name"]

        # Rotation
        rot = [-x for x in data.get("rotation", [0, 0, 0])]
        rot[2] = -rot[2]

        # Pivot
        pivot = data.get("origin", [0, 0, 0])
        pivot = [-pivot[0], pivot[1], pivot[2]]

        # Origin & Size
        original_origin = data["from"]
        size = [round(j - i, 2) for i, j in zip(original_origin, data["to"])]

        # Origin adjustment
        origin = list(original_origin)
        origin[0] = round(-(origin[0] + size[0]), 2)

        inflate = data.get("inflate", 0)
        mirror = data.get("mirror_uv", False)
        box_uv = data.get("box_uv", False)

        uv = cls._process_uv(data, box_uv)

        return cls(
            name=name,
            origin=origin,
            size=size,
            rotation=rot,
            pivot=pivot,
            inflate=inflate,
            mirror=mirror,
            uv=uv,
            box_uv=box_uv,
        )

    def compile(self) -> dict:
        cube = {
            "origin": self.origin,
            "size": self.size,
            "uv": self.uv,
        }
        if self.pivot != [0, 0, 0]:
            cube["pivot"] = self.pivot
        if self.rotation != [0, 0, 0]:
            cube["rotation"] = self.rotation
        if self.inflate != 0:
            cube["inflate"] = self.inflate
        if self.mirror:
            cube["mirror"] = True
        return cube


@dataclass
class Locator:
    name: str
    position: List[float]
    rotation: List[float] = field(default_factory=lambda: [0, 0, 0])

    @classmethod
    def from_dict(cls, data: dict) -> "Locator":
        name = data["name"]
        rot = [-x for x in data.get("rotation", [0, 0, 0])]
        pos = list(data["position"])
        pos[0] *= -1
        return cls(name=name, position=pos, rotation=rot)

    def compile(self) -> dict:
        return {self.name: self.position}


@dataclass
class Mesh:
    name: str
    vertices: Dict[str, List[float]]
    faces: Dict[str, Any]
    model_center_offset: List[float] = field(default_factory=lambda: [0, 0, 0])
    parent: str = "root"

    mesh_texture_multiplier: int = 64

    @classmethod
    def from_dict(
        cls, data: dict, parent: str = "root", model_center_offset: List[float] = None
    ) -> "Mesh":
        return cls(
            name=data.get("name", "mesh"),
            vertices=data.get("vertices", {}),
            faces=data.get("faces", {}),
            model_center_offset=model_center_offset or [0, 0, 0],
            parent=parent,
        )

    def extract_cuboids(self):
        # Re-implementation of extract_cuboids using internal data
        face_verts = {fid: set(face["vertices"]) for fid, face in self.faces.items()}

        vertex_to_faces = defaultdict(list)
        for fid, face in self.faces.items():
            for vid in face["vertices"]:
                vertex_to_faces[vid].append(fid)

        shared_counts = defaultdict(int)
        for face_list in vertex_to_faces.values():
            for i in range(len(face_list)):
                for j in range(i + 1, len(face_list)):
                    f1, f2 = face_list[i], face_list[j]
                    if f1 > f2:
                        f1, f2 = f2, f1
                    shared_counts[(f1, f2)] += 1

        face_neighbors = {fid: set() for fid in self.faces}
        for (f1, f2), count in shared_counts.items():
            if count >= 2:
                face_neighbors[f1].add(f2)
                face_neighbors[f2].add(f1)

        all_visited = set()
        cuboids = []
        cuboid_id = 0

        for fid in self.faces:
            if fid in all_visited:
                continue

            # Extract a connected component of faces
            original_component = set()
            stack = [fid]
            while stack:
                current = stack.pop()
                if current not in original_component:
                    original_component.add(current)
                    stack.extend(face_neighbors[current] - original_component)

            unvisited = original_component - all_visited
            while unvisited:
                seed = next(iter(unvisited))
                working_faces = set()
                working_verts = set()
                working_stack = [seed]

                while working_stack:
                    current = working_stack.pop()
                    if current in working_faces:
                        continue

                    current_verts = face_verts[current]
                    new_verts = working_verts.union(current_verts)
                    if len(new_verts) > 8:
                        continue

                    coords = [self.vertices[vid] for vid in new_verts]
                    xs, ys, zs = zip(*coords)
                    if (
                        max(xs) - min(xs) > 24
                        or max(ys) - min(ys) > 24
                        or max(zs) - min(zs) > 24
                    ):
                        continue

                    working_faces.add(current)
                    working_verts = new_verts
                    neighbors = face_neighbors[current] & unvisited
                    working_stack.extend(neighbors - working_faces)

                if working_faces:
                    cuboid = {
                        "name": f"{self.name}_{cuboid_id}",
                        "type": "mesh",
                        "faces": {cfid: self.faces[cfid] for cfid in working_faces},
                        "vertices": {vid: self.vertices[vid] for vid in working_verts},
                    }
                    cuboids.append(cuboid)
                    cuboid_id += 1
                    all_visited.update(working_faces)
                    unvisited.difference_update(working_faces)
                else:
                    all_visited.add(seed)
                    unvisited.discard(seed)

        return cuboids

    def map_vertices(self, cube_origin: List[float], vertices: List[float]) -> str:
        x_min = min(v[0] for v in vertices)
        y_min = min(v[1] for v in vertices)
        z_min = min(v[2] for v in vertices)

        x_max = max(v[0] for v in vertices)
        y_max = max(v[1] for v in vertices)
        z_max = max(v[2] for v in vertices)

        vertices_size = [
            round(x_max - x_min, 4),
            round(y_max - y_min, 4),
            round(z_max - z_min, 4),
        ]

        if vertices_size[0] == 0:
            return "west" if x_max > cube_origin[0] else "east"
        elif vertices_size[1] == 0:
            return "up" if y_max > cube_origin[1] else "down"
        elif vertices_size[2] == 0:
            return "south" if z_max > cube_origin[2] else "north"
        else:
            return "east"

    def process_cubes(self):
        vertices_values = list(self.vertices.values())

        origin = [
            min(x[0] for x in vertices_values),
            min(x[1] for x in vertices_values),
            min(x[2] for x in vertices_values),
        ]
        size = [
            max(x[0] for x in vertices_values) - origin[0],
            max(x[1] for x in vertices_values) - origin[1],
            max(x[2] for x in vertices_values) - origin[2],
        ]

        if self.model_center_offset != [0, 0, 0]:
            origin[0] -= self.model_center_offset[0]
            origin[1] -= self.model_center_offset[1]
            origin[2] -= self.model_center_offset[2]

        uv = {}
        for face_id, face_data in self.faces.items():
            uv_values = list(face_data["uv"].values())
            x_min = min(i[0] for i in uv_values) * self.mesh_texture_multiplier
            y_min = min(i[1] for i in uv_values) * self.mesh_texture_multiplier

            x_max = max(i[0] for i in uv_values) * self.mesh_texture_multiplier
            y_max = max(i[1] for i in uv_values) * self.mesh_texture_multiplier

            face_vertices = face_data["vertices"]
            vertices = []

            for v in face_vertices:
                vertices.append(self.vertices[v])

            original_origin = [
                origin[0] + self.model_center_offset[0],
                origin[1] + self.model_center_offset[1],
                origin[2] + self.model_center_offset[2],
            ]

            # Note: map_vertices expects specific args.
            direction = self.map_vertices(original_origin, vertices)

            uv[direction] = {
                "uv": [x_min, y_min],
                "uv_size": [round(x_max - x_min, 4), round(y_max - y_min, 4)],
            }

        return [{"origin": origin, "size": size, "uv": uv}]

    def compile(self):
        vertices_count = len(self.vertices.keys())
        if vertices_count > 0 and vertices_count <= 8:
            return self.process_cubes()
        else:
            meshes = []
            cuboids = self.extract_cuboids()

            for cube_data in cuboids:
                # Recursively create Mesh objects for sub-cuboids and compile them
                m = Mesh.from_dict(cube_data, self.parent, self.model_center_offset)
                meshes.extend(m.compile())
            return meshes


@dataclass
class Bone:
    name: str
    pivot: List[float] = field(default_factory=lambda: [0, 0, 0])
    rotation: List[float] = field(default_factory=lambda: [0, 0, 0])
    mirror: bool = False
    parent: Optional[str] = None
    binding: Optional[str] = None
    cubes: List[Cube] = field(default_factory=list)
    locators: List[Locator] = field(default_factory=list)
    meshes: List[Mesh] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, parent: str = "root") -> "Bone":
        name = data.get("name", parent)
        binding = data.get("bedrock_binding", None)

        pivot = data.get("origin", [0, 0, 0])[:]
        pivot[0] = -pivot[0]

        rot = data.get("rotation", [0, 0, 0])
        rot = [-x if i != 2 else x for i, x in enumerate(rot)]

        mirror = data.get("mirror_uv", False)

        return cls(
            name=name,
            pivot=pivot,
            rotation=rot,
            mirror=mirror,
            parent=parent,
            binding=binding,
        )

    def add_cube(self, cube: Cube):
        self.cubes.append(cube)

    def add_locator(self, locator: Locator):
        self.locators.append(locator)

    def add_mesh(self, mesh: Mesh):
        self.meshes.append(mesh)

    def compile(self) -> dict:
        bone = {"name": self.name, "pivot": self.pivot, "cubes": []}
        if self.rotation != [0, 0, 0]:
            bone["rotation"] = self.rotation
        if self.mirror:
            bone["mirror"] = self.mirror
        if self.parent:
            bone["parent"] = self.parent
        if self.binding:
            bone["binding"] = self.binding

        if self.cubes:
            bone["cubes"] = [cube.compile() for cube in self.cubes]

        if self.locators:
            bone["locators"] = {
                k: v for loc in self.locators for k, v in loc.compile().items()
            }

        if self.meshes:
            for mesh in self.meshes:
                bone["cubes"].extend(mesh.compile())

        return bone


class _ModelManager:
    def __init__(self, filename, source: str, bbmodel: dict) -> None:
        """Handles loading and managing Blockbench models.

        Parameters:
            filename (str): The name of the model file (without extension).
            source (str): The source of the model. Defaults to "actors".
            bbmodel (dict): The Blockbench model data.
        """

        self._name = filename
        self._bbmodel = bbmodel
        self._queued = False
        self._source = source
        self._is_wavefront = self._bbmodel["meta"]["model_format"] == "free"
        self._bounding_box = None
        self._model_center_offset = None
        self._culling = None
        self._cubes = {}
        self._groups = {}
        self._bones: Dict[str, Bone] = {}

    def _calculate_model_center_offset(self) -> None:
        """Calculate the offset needed to center the entire model around the origin."""
        if not self._is_wavefront:
            return

        all_vertices = []

        # Collect all vertices from all mesh elements
        for element in self._bbmodel["elements"]:
            if element["type"] == "mesh":
                vertices = element.get("vertices", {})
                for vertex in vertices.values():
                    all_vertices.append(vertex)

        if not all_vertices:
            return

        # Calculate overall bounding box
        min_x = min(v[0] for v in all_vertices)
        min_y = min(v[1] for v in all_vertices)
        min_z = min(v[2] for v in all_vertices)

        max_x = max(v[0] for v in all_vertices)
        max_y = max(v[1] for v in all_vertices)
        max_z = max(v[2] for v in all_vertices)

        # Calculate center offset - center X and Z, but put bottom at Y=0
        center_x = (min_x + max_x) / 2
        center_z = (min_z + max_z) / 2

        self._model_center_offset = [center_x, min_y, center_z]

    def process_bones(
        self, bones: List[Union[str, dict]], parent: str = "root"
    ) -> None:
        for bone in bones:
            if isinstance(bone, str):
                bone_dict = self._cubes[bone]
                if bone_dict["type"] == "cube":
                    self._bones[parent].add_cube(Cube.from_dict(bone_dict))
                elif bone_dict["type"] == "locator":
                    self._bones[parent].add_locator(Locator.from_dict(bone_dict))
                elif bone_dict["type"] == "mesh" and self._is_wavefront:
                    self._bones[parent].add_mesh(
                        Mesh.from_dict(bone_dict, parent, self._model_center_offset)
                    )
            elif isinstance(bone, dict):
                bone_group = self._groups[bone["uuid"]]
                self._bones[bone_group["name"]] = Bone.from_dict(
                    bone_group, parent if self._bones else None
                )
                self.process_bones(bone["children"], bone_group["name"])

    def process_block_display(self) -> None:
        unit = [1, 1, 1]
        zero = [0, 0, 0]
        display_data: dict[str, dict[str, list[str | float | Molang]]] = (
            self._bbmodel.get("display", {})
        )
        transforms = self._content["minecraft:geometry"][0]["item_display_transforms"]
        if display_data:
            for display, transform in display_data.items():
                if any(
                    [
                        transform.get("rotation") != zero,
                        transform.get("translation") != zero,
                        transform.get("scale") != unit,
                        transform.get("rotation_pivot") != zero,
                        transform.get("scale_pivot") != zero,
                    ]
                ):
                    # Minecraft will not accept fit_to_frame=False from "1.21.130" onwards
                    transform["fit_to_frame"] = True
                    transforms[display] = transform

    def process_geometry_scheme(self) -> None:
        width = self._bbmodel["resolution"]["width"]
        height = self._bbmodel["resolution"]["height"]

        size = [
            width * (64 if self._is_wavefront else 1),
            height * (64 if self._is_wavefront else 1),
        ]
        bounding_box = (
            self._bounding_box
            if self._bounding_box
            else (
                self._bbmodel["visible_box"] if not self._is_wavefront else [1024, 1024]
            )
        )
        offset = [0, self._bbmodel["visible_box"][2], 0]

        self._content = JsonSchemes.geometry(
            self._bbmodel["model_identifier"],
            size,
            bounding_box,
            offset,
        )

        self._content["minecraft:geometry"][0]["bones"] = [
            bone.compile() for bone in self._bones.values()
        ]

        if self._source == BlockBenchSource.BLOCK:
            self._content["minecraft:geometry"][0]["item_display_transforms"] = {}

    def queue_model(self) -> None:
        if not self._queued:
            if self._is_wavefront:
                self._calculate_model_center_offset()

            self._cubes = {d["uuid"]: d for d in self._bbmodel["elements"]}
            self._groups = {d["uuid"]: d for d in self._bbmodel["groups"]}
            self.process_bones(self._bbmodel["outliner"], "root")
            self.process_geometry_scheme()

            if self._source == BlockBenchSource.BLOCK:
                self.process_block_display()
            self._queued = True

    def block_culling(self) -> _BlockCulling:
        if not self._culling:
            self._culling = _BlockCulling(self._name, self._bbmodel)
        return self._culling

    def _export(self) -> None:
        if self._queued:
            _Geometry(self._bbmodel["model_identifier"], self._content).queue(
                self._source
            )
            if self._culling:
                self._culling.queue()


class _Blockbench:
    _loaded_blockbench_models: dict[str, "_Blockbench"] = {}

    def __new__(cls, filename, source: str = "actors"):
        if filename not in _Blockbench._loaded_blockbench_models:
            _Blockbench._loaded_blockbench_models[filename] = super(
                _Blockbench, cls
            ).__new__(cls)
        return _Blockbench._loaded_blockbench_models[filename]

    def __init__(self, filename: str, source: str = "actors") -> None:
        """Handles loading and managing Blockbench models.

        Parameters:
            filename (str): The name of the model file (without extension).
            source (str, optional): The source of the model. Defaults to "actors".

        Raises:
            ValueError: If the model identifier does not match the filename.
            FileNotFoundError: If the model file is not found.
        """
        if hasattr(self, "_path"):
            return

        self._path = os.path.join("assets", "bbmodels", f"{filename}.bbmodel")

        if FileExists(self._path):
            with open(self._path, "r") as model:
                self.bbmodel = json.load(model)
                if self.bbmodel["model_identifier"] != filename:
                    raise ValueError(
                        f"Blockbench model identifier mismatch: expected '{filename}', found '{self.bbmodel['model_identifier']}'."
                    )

                if Version(self.bbmodel["meta"]["format_version"]) < Version("5.0"):
                    raise ValueError(
                        f"'{filename}.bbmodel' Blockbench model format version '{self.bbmodel['meta']['format_version']}' is not supported. Please update your models with Blockbench 5.0 or higher to export the model."
                    )
        else:
            raise FileNotFoundError(
                f"{filename}.bbmodel not found in {os.path.join('assets', 'bbmodels')}. Please ensure the file exists."
            )

        self.model = _ModelManager(filename, source, self.bbmodel)
        self.animations = _AnimationsManager(filename, source, self.bbmodel)
        self.textures = _TexturesManager(filename, source, self.bbmodel)

    def override_bounding_box(self, bounding_box: Vector2D) -> None:
        self.model._bounding_box = bounding_box

    @classmethod
    def _export(cls):
        meshes = []
        for bb in _Blockbench._loaded_blockbench_models.values():
            bb.model._export()
            bb.animations._export()
            bb.textures._export()
            if bb.model._is_wavefront:
                meshes.append(bb.model._name)
        if len(meshes) > 0:
            click.echo(
                click.style(
                    f"\r[INFO]: Some Blockbench models are using a Wavefront format. This is not fully supported and it may not work correctly.",
                    fg="yellow",
                )
            )
