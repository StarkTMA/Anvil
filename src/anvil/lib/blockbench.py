import base64
import json
import os
from collections import defaultdict
from typing import Dict, List, Union
from warnings import warn

import click
from packaging.version import Version

from anvil.lib.config import CONFIG
from anvil.lib.enums import BlockFaces
from anvil.lib.lib import FileExists
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import Vector2D


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


class _AnimationsManager:
    _loop_map = {
        "once": False,
        "loop": True,
        "hold": "hold_on_last_frame",
    }

    def adjust_keyframe_sign(self, points: List[Dict[str, str]]) -> List[str]:
        return [
            (
                (-float(x) + 0.0 if i < 2 else float(x))
                if x.replace("-", "").replace(".", "").isnumeric()
                else (f"-({x})" if i < 2 else x)
            )
            for i, x in enumerate(points)
        ]

    def adjust_keyframe_type(self, points: List[Dict[str, str]]) -> List[str]:
        return [
            (float(x) if x.replace("-", "").replace(".", "").isnumeric() else str(x))
            for x in points
        ]

    def _keyframes_mapper(self, keyframes: List[dict]) -> dict:
        keyframes_dict = {}
        for keyframe in keyframes:
            time = float(keyframe.get("time"))
            data_points = keyframe.get("data_points")
            interpolation = keyframe.get("interpolation", "linear")
            channel = keyframe.get("channel")

            keyframes_dict.setdefault(channel, {})[time] = {
                "data_points": list(data_points),
                "interpolation": interpolation,
            }

        return keyframes_dict

    def _process_position_channel(
        self, bone_name: str, channel: dict, bones: dict
    ) -> None:
        """Process position keyframes for a bone."""
        is_step = False
        channel_points = list(channel.values())

        for keyframe_index, (time, value) in enumerate(list(channel.items())):
            interpolation = value["interpolation"]
            points: list[Dict[str, str]] = value["data_points"]
            previous_points = channel_points[keyframe_index - 1]["data_points"]

            if len(points) == 1:
                points = self.adjust_keyframe_type(points[0].values())
                # Check for newline characters in keyframe values
                for point in points:
                    if isinstance(point, str) and "\n" in point:
                        raise ValueError(
                            f"Newline character found in position keyframe for bone '{bone_name}' at time {time}. "
                            f"Keyframe values cannot contain newlines."
                        )

            if interpolation == "linear" or interpolation == "bezier":
                if is_step:
                    bones[bone_name]["position"][time] = {
                        "pre": self.adjust_keyframe_type(previous_points[0].values()),
                        "post": points,
                    }
                    is_step = False
                elif len(points) == 2:
                    bones[bone_name]["position"][time] = {
                        "pre": self.adjust_keyframe_type(points[0].values()),
                        "post": self.adjust_keyframe_type(points[1].values()),
                    }
                else:
                    bones[bone_name]["position"][time] = points

            elif interpolation == "catmullrom":
                bones[bone_name]["position"][time] = {
                    "post": points,
                    "lerp_mode": interpolation,
                }
                is_step = False

            elif interpolation == "step":
                if is_step:
                    bones[bone_name]["position"][time] = {
                        "pre": self.adjust_keyframe_type(previous_points[0].values()),
                        "post": self.adjust_keyframe_type(
                            value["data_points"][0].values()
                        ),
                    }
                else:
                    bones[bone_name]["position"][time] = points
                is_step = True

    def _process_rotation_channel(
        self, bone_name: str, channel: dict, bones: dict
    ) -> None:
        """Process rotation keyframes for a bone."""
        is_step = False
        channel_points = list(channel.values())

        for keyframe_index, (time, value) in enumerate(list(channel.items())):
            interpolation = value["interpolation"]
            points: list[Dict[str, str]] = value["data_points"]
            previous_points = channel_points[keyframe_index - 1]["data_points"]

            if len(points) == 1:
                points = self.adjust_keyframe_sign(points[0].values())
                # Check for newline characters in keyframe values
                for point in points:
                    if isinstance(point, str) and "\n" in point:
                        raise ValueError(
                            f"Newline character found in rotation keyframe for bone '{bone_name}' at time {time}. "
                            f"Keyframe values cannot contain newlines."
                        )

            if interpolation == "linear" or interpolation == "bezier":
                if is_step:
                    bones[bone_name]["rotation"][time] = {
                        "pre": self.adjust_keyframe_type(previous_points[0].values()),
                        "post": points,
                    }
                    is_step = False
                elif len(points) == 2:
                    bones[bone_name]["rotation"][time] = {
                        "pre": self.adjust_keyframe_type(points[0].values()),
                        "post": self.adjust_keyframe_type(points[1].values()),
                    }
                else:
                    bones[bone_name]["rotation"][time] = points

            elif interpolation == "catmullrom":
                bones[bone_name]["rotation"][time] = {
                    "post": points,
                    "lerp_mode": interpolation,
                }
                is_step = False

            elif interpolation == "step":
                if is_step:
                    bones[bone_name]["rotation"][time] = {
                        "pre": self.adjust_keyframe_type(previous_points[0].values()),
                        "post": self.adjust_keyframe_type(
                            value["data_points"][0].values()
                        ),
                    }
                else:
                    bones[bone_name]["rotation"][time] = points
                is_step = True

    def _process_scale_channel(
        self, bone_name: str, channel: dict, bones: dict
    ) -> None:
        """Process scale keyframes for a bone."""
        is_step = False
        channel_points = list(channel.values())

        for keyframe_index, (time, value) in enumerate(list(channel.items())):
            interpolation = value["interpolation"]
            points: list[Dict[str, str]] = value["data_points"]
            previous_points = channel_points[keyframe_index - 1]["data_points"]

            if len(points) == 1:
                points = self.adjust_keyframe_type(points[0].values())
                # Check for newline characters in keyframe values
                for point in points:
                    if isinstance(point, str) and "\n" in point:
                        raise ValueError(
                            f"Newline character found in scale keyframe for bone '{bone_name}' at time {time}. "
                            f"Keyframe values cannot contain newlines."
                        )

            if interpolation == "linear" or interpolation == "bezier":
                if is_step:
                    bones[bone_name]["scale"][time] = {
                        "pre": self.adjust_keyframe_type(previous_points[0].values()),
                        "post": points,
                    }
                    is_step = False
                elif len(points) == 2:
                    bones[bone_name]["scale"][time] = {
                        "pre": self.adjust_keyframe_type(points[0].values()),
                        "post": self.adjust_keyframe_type(points[1].values()),
                    }
                else:
                    bones[bone_name]["scale"][time] = points

            elif interpolation == "catmullrom":
                bones[bone_name]["scale"][time] = {
                    "post": points,
                    "lerp_mode": interpolation,
                }
                is_step = False

            elif interpolation == "step":
                if is_step:
                    bones[bone_name]["scale"][time] = {
                        "pre": self.adjust_keyframe_type(previous_points[0].values()),
                        "post": self.adjust_keyframe_type(
                            value["data_points"][0].values()
                        ),
                    }
                else:
                    bones[bone_name]["scale"][time] = points
                is_step = True

    def _process_particle_channel(self, channel: dict, particles: dict) -> None:
        """Process particle effect keyframes."""
        for time, value in channel.items():
            effect = value["data_points"][0]["effect"]
            locator = value["data_points"][0]["locator"]
            script = value["data_points"][0]["script"]

            # Check for newline characters
            if "\n" in effect:
                raise ValueError(
                    f"Newline character found in particle effect keyframe at time {time}. "
                    f"Keyframe values cannot contain newlines."
                )
            if "\n" in locator:
                raise ValueError(
                    f"Newline character found in particle locator keyframe at time {time}. "
                    f"Keyframe values cannot contain newlines."
                )
            if "\n" in script:
                raise ValueError(
                    f"Newline character found in particle script keyframe at time {time}. "
                    f"Keyframe values cannot contain newlines."
                )

            particles[time] = {
                "effect": effect,
                "locator": locator,
            }
            if script != "":
                particles[time]["pre_effect_script"] = (script + ";").replace(";;", ";")

    def _process_sound_channel(self, channel: dict, sounds: dict) -> None:
        """Process sound effect keyframes."""
        for time, value in channel.items():
            effect = value["data_points"][0]["effect"]

            # Check for newline characters
            if "\n" in effect:
                raise ValueError(
                    f"Newline character found in sound effect keyframe at time {time}. "
                    f"Keyframe values cannot contain newlines."
                )

            sounds[time] = {"effect": effect}

    def _process_timeline_channel(self, channel: dict, timeline: dict) -> None:
        """Process timeline keyframes."""
        for time, value in channel.items():
            data_point = value["data_points"][0]

            # Check for newline characters
            if isinstance(data_point, str) and "\n" in data_point:
                raise ValueError(
                    f"Newline character found in timeline keyframe at time {time}. "
                    f"Keyframe values cannot contain newlines."
                )

            timeline[time] = data_point

    def _cleanup_bone_channels(self, bone_name: str, bones: dict) -> None:
        """Clean up empty or single-value bone channels."""
        for channel in ["position", "rotation", "scale"]:
            keys = bones[bone_name][channel].keys()
            if len(keys) == 0:
                del bones[bone_name][channel]
            elif len(keys) == 1:
                bones[bone_name][channel] = list(bones[bone_name][channel].values())[0]

            if (
                channel == "scale"
                and isinstance(bones[bone_name].get("scale"), list)
                and len(set(bones[bone_name]["scale"])) == 1
            ):
                bones[bone_name]["scale"] = bones[bone_name]["scale"][0]

    def _process_animation(self, animation_dict: dict) -> dict:
        animation = {}
        animation_length = animation_dict.get("length")
        anim_time_update = animation_dict.get("anim_time_update")
        override = animation_dict.get("override")
        loop = self._loop_map.get(animation_dict.get("loop", "once"))

        if animation_length:
            animation["animation_length"] = animation_length

        if anim_time_update:
            animation["anim_time_update"] = anim_time_update

        if override:
            animation["override_previous_animation"] = override

        if loop:
            animation["loop"] = loop

        if animation_dict.get("animators"):
            bones = {}
            particles = {}
            sounds = {}
            timeline = {}

            for animator in animation_dict.get("animators", {}).values():
                bone_name = animator.get("name")

                bones[bone_name] = {
                    "position": {},
                    "rotation": {},
                    "scale": {},
                }

                keyframes = self._keyframes_mapper(animator.get("keyframes", []))

                for channel_name, channel in keyframes.items():
                    if channel_name == "position":
                        self._process_position_channel(bone_name, channel, bones)
                    elif channel_name == "rotation":
                        self._process_rotation_channel(bone_name, channel, bones)
                    elif channel_name == "scale":
                        self._process_scale_channel(bone_name, channel, bones)
                    elif channel_name == "particle":
                        self._process_particle_channel(channel, particles)
                    elif channel_name == "sound":
                        self._process_sound_channel(channel, sounds)
                    elif channel_name == "timeline":
                        self._process_timeline_channel(channel, timeline)

                self._cleanup_bone_channels(bone_name, bones)

                if animator.get("rotation_global", False):
                    bones[bone_name]["relative_to"] = {"rotation": "entity"}

            if bones != {}:
                animation["bones"] = bones
            if particles != {}:
                animation["particle_effects"] = particles
            if sounds != {}:
                animation["sound_effects"] = sounds
            if timeline != {}:
                animation["timeline"] = timeline

        return {
            f"animation.{CONFIG.NAMESPACE}.{self._name}.{animation_dict.get('name')}": animation
        }

    def __init__(self, name: str, source: str, bbmodel: dict) -> None:
        self._name = name
        self._bbanimations = bbmodel.get("animations", [])
        self._content = JsonSchemes.animations_rp()
        self._queued = False
        self._source = "actors"

    def queue_animation(self, animation_name: str):
        animation_dict = next(
            (anim for anim in self._bbanimations if anim.get("name") == animation_name),
            None,
        )
        if animation_dict:
            if (
                not f"animation.{CONFIG.NAMESPACE}.{self._name}.{animation_dict.get('name')}"
                in self._content["animations"]
            ):
                self._content["animations"].update(
                    self._process_animation(animation_dict)
                )
                self._queued = True
        else:
            raise ValueError(
                f"Animation '{animation_name}' not found in blockbench model '{self._name}'."
            )

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
            filename,
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


class _Cube:
    def __init__(self, cube_dict: dict, parent: str = "root") -> None:
        self.cube = cube_dict
        self.parent = parent
        self.name = self.cube["name"]
        self.rotation = [0, 0, 0]
        self.origin = [0, 0, 0]
        self.pivot = [0, 0, 0]
        self.size = [0, 0, 0]
        self.box_uv = False
        self.inflate = 0
        self.mirror = False
        self.faces = {}
        self.uv = []
        self.process_cube()

    def process_cube(self):
        self.rotation = [-x for x in self.cube.get("rotation", [0, 0, 0])]
        self.rotation[2] = -self.rotation[2]
        self.pivot = self.cube.get("origin", [0, 0, 0])
        self.pivot[0] = -self.pivot[0]
        self.origin = self.cube["from"]
        self.size = [round(j - i, 2) for i, j in zip(self.origin, self.cube["to"])]
        self.origin[0] = round(-(self.origin[0] + self.size[0]), 2)
        self.inflate = self.cube.get("inflate", 0)
        self.mirror = self.cube.get("mirror_uv", False)
        self.box_uv = self.cube.get("box_uv", False)
        self.process_uv()

    def process_uv(self):
        if self.box_uv:
            self.uv = self.cube.get("uv_offset", [0, 0])
        else:
            self.uv = {}
            for face, face_data in self.cube.get("faces", {}).items():
                if face_data.get("texture") is not None:
                    uv_map = face_data.get("uv", [])
                    rotation = face_data.get("rotation", 0)
                    material_instance = face_data.get("material_name", {})
                    if face == "up" or face == "down":
                        uv_map = [uv_map[2], uv_map[3], uv_map[0], uv_map[1]]

                    uv_size = [
                        round(uv_map[2] - uv_map[0], 2),
                        round(uv_map[3] - uv_map[1], 2),
                    ]
                    if uv_size[0] != 0 and uv_size[1] != 0:
                        self.uv[face] = {
                            "uv": [uv_map[0], uv_map[1]],
                            "uv_size": uv_size,
                            "material_instance": material_instance,
                        }
                        if rotation != 0:
                            self.uv[face]["uv_rotation"] = rotation

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


class _Locator:
    def __init__(self, _Locator_dict: dict, parent: str = "root") -> None:
        self._Locator = _Locator_dict
        self.parent = parent
        self.name = self._Locator["name"]
        self.rotation = [-x for x in self._Locator.get("rotation", [0, 0, 0])]
        self.position = self._Locator["position"]
        self.position[0] *= -1

    def compile(self) -> dict:
        return {self.name: self.position}


class _Mesh:
    mesh_texture_multiplier = 64

    def __init__(
        self,
        mesh_dict: dict,
        parent: str = "root",
        model_center_offset: List[float] = None,
    ) -> None:
        self.mesh = mesh_dict
        self.parent = parent
        self.vertices = self.mesh.get("vertices", [])
        self.faces = self.mesh.get("faces", [])
        self.model_center_offset = model_center_offset or [0, 0, 0]

    def extract_cuboids(self):
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
                # Start a new sub-cuboid from a seed in the remaining set
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

                    # All constraints passed, add face
                    working_faces.add(current)
                    working_verts = new_verts
                    neighbors = face_neighbors[current] & unvisited
                    working_stack.extend(neighbors - working_faces)

                if working_faces:
                    cuboid = {
                        "name": f"{self.mesh.get('name')}_{cuboid_id}",
                        "type": "mesh",
                        "faces": {cfid: self.faces[cfid] for cfid in working_faces},
                        "vertices": {vid: self.vertices[vid] for vid in working_verts},
                    }
                    cuboids.append(cuboid)
                    cuboid_id += 1
                    all_visited.update(working_faces)
                    unvisited.difference_update(working_faces)
                else:
                    # Couldn’t grow anything from this seed? Mark it visited anyway
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
        # else:
        #    raise ValueError(f"Face is not planar or not axis-aligned. Cannot determine direction. {self.mesh.get('name')} {vertices_size}")

    def process_cubes(self):
        vertices_values = self.vertices.values()

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

        # Apply model center offset to center the entire model
        if self.model_center_offset != [0, 0, 0]:
            origin[0] -= self.model_center_offset[0]
            origin[1] -= self.model_center_offset[1]
            origin[2] -= self.model_center_offset[2]

        uv = {}
        for face_id, face_data in self.faces.items():
            uv_values = list(face_data["uv"].values())
            x_min = min(i[0] for i in uv_values) * _Mesh.mesh_texture_multiplier
            y_min = min(i[1] for i in uv_values) * _Mesh.mesh_texture_multiplier

            x_max = max(i[0] for i in uv_values) * _Mesh.mesh_texture_multiplier
            y_max = max(i[1] for i in uv_values) * _Mesh.mesh_texture_multiplier

            face_vertices = face_data["vertices"]
            vertices = []

            for v in face_vertices:
                vertices.append(self.vertices[v])

            original_origin = [
                origin[0] + self.model_center_offset[0],
                origin[1] + self.model_center_offset[1],
                origin[2] + self.model_center_offset[2],
            ]
            uv[self.map_vertices(original_origin, vertices)] = {
                "uv": [x_min, y_min],
                "uv_size": [round(x_max - x_min, 4), round(y_max - y_min, 4)],
            }

        return [{"origin": origin, "size": size, "uv": uv}]

    def compile(self):
        vertices = len(self.vertices.keys())
        if vertices > 0 and vertices <= 8:  # A cube or a face
            return self.process_cubes()
        else:
            meshes = []
            cuboids = self.extract_cuboids()

            for cube in cuboids:
                meshes.append(
                    _Mesh(cube, self.parent, self.model_center_offset).compile()[0]
                )
            return meshes


class _Bone:
    def __init__(self, bone_dict: dict, parent: str = "root") -> None:
        self.bone = bone_dict
        self.parent = parent
        self.name = self.bone.get("name", self.parent)
        self.binding = self.bone.get("bedrock_binding", None)
        self.pivot = self.bone.get("origin", [0, 0, 0])
        self.pivot[0] = -self.pivot[0]
        self.rotation = [
            -x if i != 2 else x
            for i, x in enumerate(self.bone.get("rotation", [0, 0, 0]))
        ]
        self.mirror = self.bone.get("mirror_uv", False)
        self.cubes: List[_Cube] = []
        self.locators: List[_Locator] = []
        self.meshes: List[_Mesh] = []

    def add_cube(self, _Cube: _Cube):
        self.cubes.append(_Cube)

    def add_locator(self, _Locator: _Locator):
        self.locators.append(_Locator)

    def add_mesh(self, _Mesh: _Mesh):
        self.meshes.append(_Mesh)

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
                k: v
                for _Locator in self.locators
                for k, v in _Locator.compile().items()
            }
        if self.meshes:
            for mesh in self.meshes:
                bone["cubes"].extend(mesh.compile())
        return bone


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
                    self._bones[parent].add_cube(_Cube(bone_dict, parent))
                elif bone_dict["type"] == "locator":
                    self._bones[parent].add_locator(_Locator(bone_dict, parent))
                elif bone_dict["type"] == "mesh" and self._is_wavefront:
                    self._bones[parent].add_mesh(
                        _Mesh(bone_dict, parent, self._model_center_offset)
                    )
            elif isinstance(bone, dict):
                bone_group = self._groups[bone["uuid"]]
                self._bones[bone_group["name"]] = _Bone(
                    bone_group, parent if self._bones else None
                )
                self.process_bones(bone["children"], bone_group["name"])

    def queue_model(self) -> None:
        if not self._queued:
            self._cubes = {d["uuid"]: d for d in self._bbmodel["elements"]}
            self._groups = {d["uuid"]: d for d in self._bbmodel["groups"]}
            self._bones: Dict[str, _Bone] = {}

            # Calculate model center offset for mesh models
            if self._is_wavefront:
                self._calculate_model_center_offset()

            self.process_bones(self._bbmodel["outliner"], "root")

            texture_multiplier = 64 if self._is_wavefront else 1

            self._content = JsonSchemes.geometry(
                self._bbmodel["model_identifier"],
                [
                    self._bbmodel["resolution"]["width"] * texture_multiplier,
                    self._bbmodel["resolution"]["height"] * texture_multiplier,
                ],
                [
                    (
                        self._bounding_box[0]
                        if self._bounding_box
                        else (
                            self._bbmodel["visible_box"][0]
                            if not self._is_wavefront
                            else 1024
                        )
                    ),
                    (
                        self._bounding_box[1]
                        if self._bounding_box
                        else (
                            self._bbmodel["visible_box"][1]
                            if not self._is_wavefront
                            else 1024
                        )
                    ),
                ],
                [0, self._bbmodel["visible_box"][2], 0],
            )
            self._content["minecraft:geometry"][0]["bones"] = [
                bone.compile() for bone in self._bones.values()
            ]
            if self._source == "block":
                self._content["minecraft:geometry"][0]["item_display_transforms"] = (
                    self._bbmodel["display"]
                )
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
