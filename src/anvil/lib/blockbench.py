import base64
import json
import os
import uuid
from collections import defaultdict
from copy import deepcopy
from csv import Error
from typing import Dict, List, Tuple, Union
from warnings import warn

from anvil import CONFIG
from anvil.lib.lib import FileExists
from anvil.lib.schemas import AddonObject, JsonSchemes


def _keyframes_mapper(keyframes: List[dict]) -> dict:
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

    def _process_animation(self, animation_dict: dict) -> dict:
        animation = {}
        animation_length = animation_dict.get("length")
        loop = self._loop_map.get(animation_dict.get("loop", "once"))

        if animation_length:
            animation["animation_length"] = animation_length
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
                for channel_name, channel in _keyframes_mapper(animator.get("keyframes", [])).items():
                    if channel_name not in ["particle", "sound", "timeline"]:
                        is_step = False
                        for keyframe_index, (time, value) in enumerate(list(channel.items())):
                            interpolation = value["interpolation"]
                            points = value["data_points"]
                            if len(points) == 1:
                                points = list(points[0].values())

                            if interpolation == "linear" or interpolation == "bezier":
                                if is_step:
                                    bones[bone_name][channel_name][time] = {
                                        "pre": list(list(channel.values())[keyframe_index - 1]["data_points"][0].values()),
                                        "post": points,
                                    }
                                    is_step = False
                                elif len(points) == 2:
                                    bones[bone_name][channel_name][time] = {
                                        "pre": [float(x) for x in list(points[0].values())],
                                        "post": [float(x) for x in list(points[1].values())],
                                    }
                                    is_step = False
                                else:
                                    bones[bone_name][channel_name][time] = points
                                    is_step = False
                            elif interpolation == "catmullrom":
                                bones[bone_name][channel_name][time] = {
                                    "post": points,
                                    "lerp_mode": interpolation,
                                }
                                is_step = False
                            elif interpolation == "step":
                                if is_step:
                                    bones[bone_name][channel_name][time] = {
                                        "pre": list(list(channel.values())[keyframe_index - 1]["data_points"][0].values()),
                                        "post": points,
                                    }
                                else:
                                    bones[bone_name][channel_name][time] = points
                                is_step = True
                    elif channel_name == "particle":
                        for time, value in channel.items():
                            particles[time] = {
                                "effect": value["data_points"][0]["effect"],
                                "locator": value["data_points"][0]["locator"],
                            }
                            if value["data_points"][0]["script"] != "":
                                particles[time]["pre_effect_script"] = value["data_points"][0]["script"]
                    elif channel_name == "sound":
                        for keyframe in list(channel.items()):
                            time, value = keyframe
                            sounds[time] = {"effect": value["data_points"][0]["effect"]}
                    elif channel_name == "timeline":
                        for keyframe in list(channel.items()):
                            time, value = keyframe
                            timeline[time] = value["data_points"][0]

                for channel in ["position", "rotation", "scale"]:
                    keys = bones[bone_name][channel].keys()
                    if len(keys) == 0:
                        del bones[bone_name][channel]
                    elif len(keys) == 1:
                        bones[bone_name][channel] = list(bones[bone_name][channel].values())[0]

                    if channel == "scale" and isinstance(bones[bone_name].get("scale"), list) and len(set(bones[bone_name]["scale"])) == 1:
                        bones[bone_name]["scale"] = bones[bone_name]["scale"][0]

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

        return {f"animation.{CONFIG.NAMESPACE}.{self._name}.{animation_dict.get("name")}": animation}
        # return { animation_dict.get("name"): animation}

    def __init__(self, name: str, source: str, bbmodel: dict) -> None:
        self._name = name
        self._bbanimations = bbmodel.get("animations", [])
        self._content = JsonSchemes.rp_animations()
        self._queued = False
        self._source = "actors"

    def queue_animation(self, animation_name: str):
        animation_dict = next((anim for anim in self._bbanimations if anim.get("name") == animation_name), None)
        if animation_dict:
            if not f"animation.{CONFIG.NAMESPACE}.{self._name}.{animation_dict.get('name')}" in self._content["animations"]:
                self._content["animations"].update(self._process_animation(animation_dict))
                self._queued = True
        else:
            raise ValueError(f"Animation '{animation_name}' not found in blockbench model '{self._name}'.")

    def _export(self) -> None:
        if self._queued:
            _Animation(self._name, self._content).queue(self._source)


class _TexturesManager:
    def __init__(self, filename: str, source: str, bbmodel: dict) -> None:
        self._name = filename
        self._bbmodel = bbmodel
        self._path = os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, source, filename)
        self._textures = {texture.get("name").split(".")[0]: texture for texture in self._bbmodel["textures"]}
        self._queued_textures: set[str] = set()

    def queue_texture(self, texture: str) -> None:
        if texture in self._textures:
            self._queued_textures.add(texture)
        else:
            raise ValueError(f"Texture '{texture}' not found in blockbench model '{self._bbmodel['model_identifier']}'.")

    def _export(self) -> None:
        os.makedirs(self._path, exist_ok=True)
        for texture in self._queued_textures:
            image_data = base64.b64decode(self._textures[texture].get("source").replace("data:image/png;base64,", ""))
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
                    uv_map = face_data["uv"]
                    rotation = face_data.get("rotation", 0)
                    if face == "up" or face == "down":
                        uv_map = [uv_map[2], uv_map[3], uv_map[0], uv_map[1]]

                    uv_size = [round(uv_map[2] - uv_map[0], 2), round(uv_map[3] - uv_map[1], 2)]
                    if uv_size[0] != 0 and uv_size[1] != 0:
                        self.uv[face] = {
                            "uv": [uv_map[0], uv_map[1]],
                            "uv_size": uv_size,
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

    def __init__(self, mesh_dict: dict, parent: str = "root") -> None:
        self.mesh = mesh_dict
        self.parent = parent
        self.vertices = self.mesh.get("vertices", [])
        self.faces = self.mesh.get("faces", [])

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
                    if max(xs) - min(xs) > 24 or max(ys) - min(ys) > 24 or max(zs) - min(zs) > 24:
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
            raise ValueError("Face is not planar or not axis-aligned. Cannot determine direction.")

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

            uv[self.map_vertices(origin, vertices)] = {
                "uv": [x_min, y_min],
                "uv_size": [round(x_max - x_min, 4), round(y_max - y_min, 4)],
            }

        return [{"origin": origin, "size": size, "uv": uv}]

    def compile(self):
        vertices = len(self.vertices.keys())
        if vertices <= 8:  # A cube or a face
            return self.process_cubes()
        else:
            meshes = []
            cuboids = self.extract_cuboids()

            for cube in cuboids:
                meshes.append(_Mesh(cube).compile()[0])
            return meshes


class _Bone:
    def __init__(self, bone_dict: dict, parent: str = "root") -> None:
        self.bone = bone_dict
        self.parent = parent
        self.name = self.bone.get("name", self.parent)
        self.binding = self.bone.get("bedrock_binding", None)
        self.pivot = self.bone.get("origin", [0, 0, 0])
        self.pivot[0] = -self.pivot[0]
        self.rotation = [-x if i != 2 else x for i, x in enumerate(self.bone.get("rotation", [0, 0, 0]))]
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
            bone["locators"] = {k: v for _Locator in self.locators for k, v in _Locator.compile().items()}
        if self.meshes:
            for mesh in self.meshes:
                bone["cubes"].extend(mesh.compile())
        return bone


class _ModelManager:
    def __init__(self, filename, source: str, bbmodel: dict) -> None:
        self._name = filename
        self._bbmodel = bbmodel
        self._queued = False
        self._source = source
        self._is_wavefront = self._bbmodel["meta"]["model_format"] == "free"

        if self._is_wavefront:
            warn(
                f"You are using a Blockbench model with a Wavefront format. This is not fully supported and it may not work correctly. Blockbench model [{self._name}]",
                UserWarning,
            )

    def process_bones(self, bones: List[Union[str, dict]], parent: str = "root") -> None:
        for bone in bones:
            if isinstance(bone, str):
                bone_dict = self._cubes[bone]
                if bone_dict["type"] == "cube":
                    self._bones[parent].add_cube(_Cube(bone_dict, parent))
                elif bone_dict["type"] == "locator":
                    self._bones[parent].add_locator(_Locator(bone_dict, parent))
                elif bone_dict["type"] == "mesh" and self._is_wavefront:
                    self._bones[parent].add_mesh(_Mesh(bone_dict, parent))
            elif isinstance(bone, dict):
                bone_name = bone["name"]
                self._bones[bone_name] = _Bone(bone, parent if self._bones else None)
                self.process_bones(bone["children"], bone_name)

    def queue_model(self) -> None:
        if not self._queued:
            self._cubes = {d["uuid"]: d for d in self._bbmodel["elements"]}
            self._bones: Dict[str, _Bone] = {}
            self.process_bones(self._bbmodel["outliner"], "root")

            texture_multiplier = 64 if self._is_wavefront else 1

            self._content = JsonSchemes.geometry(
                self._bbmodel["model_identifier"],
                [
                    self._bbmodel["resolution"]["width"] * texture_multiplier,
                    self._bbmodel["resolution"]["height"] * texture_multiplier,
                ],
                [
                    self._bbmodel["visible_box"][0] if not self._is_wavefront else 1024,
                    self._bbmodel["visible_box"][1] if not self._is_wavefront else 1024,
                ],
                [0, self._bbmodel["visible_box"][2], 0],
            )
            self._content["minecraft:geometry"][0]["bones"] = [bone.compile() for bone in self._bones.values()]
            if self._source == "block":
                self._content["minecraft:geometry"][0]["item_display_transforms"] = self._bbmodel["display"]
            self._queued = True

    def _export(self) -> None:
        if self._queued:
            _Geometry(self._bbmodel["model_identifier"], self._content).queue(self._source)


class _Blockbench:
    _loaded_blockbench_models: dict[str, "_Blockbench"] = {}

    def __new__(cls, filename, source: str = "actors"):
        if filename not in _Blockbench._loaded_blockbench_models:
            _Blockbench._loaded_blockbench_models[filename] = super(_Blockbench, cls).__new__(cls)
        return _Blockbench._loaded_blockbench_models[filename]

    def __init__(self, filename: str, source: str = "actors") -> None:
        if hasattr(self, "_path"):
            return

        self._path = os.path.join("assets", "bbmodels", f"{filename}.bbmodel")

        if FileExists(self._path):
            with open(self._path, "r") as model:
                self.bbmodel = json.load(model)
                if self.bbmodel["model_identifier"] != filename:
                    raise ValueError(f"Blockbench model identifier mismatch: expected '{filename}', found '{self.bbmodel['model_identifier']}'.")
        else:
            raise FileNotFoundError(f"{filename}.bbmodel not found in {os.path.join('assets', 'bbmodels')}. Please ensure the file exists.")

        self.model = _ModelManager(filename, source, self.bbmodel)
        self.animations = _AnimationsManager(filename, source, self.bbmodel)
        self.textures = _TexturesManager(filename, source, self.bbmodel)

    def _export():
        for bb in _Blockbench._loaded_blockbench_models.values():
            bb.model._export()
            bb.animations._export()
            bb.textures._export()
