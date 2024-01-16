import json
import os

import commentjson

from anvil import CONFIG
from anvil.api.types import Molang
from anvil.lib.lib import FileExists
from anvil.lib.schemas import AddonObject, JsonSchemes


class _Bone:
    """
    The _Bone class represents a bone in the geometric model.

    Attributes:
        _bone (dict): The dictionary representation of a bone.
    """

    def __init__(self, name, pivot, parent) -> None:
        """
        Initializes the _Bone instance.

        Args:
            name (str): The name of the bone.
            pivot (list): The pivot coordinates of the bone.
            parent (str): The parent bone's name.
        """
        self._bone = {
            "name": name,
            "pivot": pivot,
            "parent": parent if not parent is None else {},
            "cubes": [],
        }

    def add_cube(
        self,
        origin: list[float, float, float],
        size: list[float, float, float],
        uv: list[int, int],
        pivot: list[float, float, float] = (0, 0, 0),
        rotation: list[float, float, float] = (0, 0, 0),
        inflate: float = 0,
        mirror: bool = False,
        reset: bool = False,
        uv_face: list[str, list[int, int], list[int, int]] = None,
    ):
        """
        Adds a cube to the _Bone instance.

        Args:
            origin (list): The origin coordinates of the cube.
            size (list): The size of the cube.
            uv (list): The UV coordinates of the cube.
            pivot (list, optional): The pivot coordinates of the cube. Defaults to (0,0,0).
            rotation (list, optional): The rotation of the cube. Defaults to (0,0,0).
            inflate (float, optional): The inflation level of the cube. Defaults to 0.
            mirror (bool, optional): If the cube should be mirrored. Defaults to False.
            reset (bool, optional): If the cube should be reset. Defaults to False.
            uv_face (list, optional): The UV face of the cube. Defaults to None.

        Returns:
            _Bone: The instance of the _Bone class.
        """
        self._bone["cubes"].append(
            {
                "origin": origin,
                "size": size,
                "uv": uv if uv_face is None else {uv_face[0]: {"uv": uv_face[1], "uv_size": uv_face[2]}},
                "pivot": pivot if not pivot == (0, 0, 0) else {},
                "rotation": rotation if not rotation == (0, 0, 0) else {},
                "inflate": inflate if not inflate == 0 else {},
                "mirror": mirror if mirror else {},
                "reset": reset if reset else {},
            }
        )
        return self

    @property
    def _queue(self):
        """
        Getter for the _queue property of _Bone instance.

        Returns:
            dict: The dictionary representation of a bone.
        """
        return self._bone


class _Geo:
    """
    The _Geo class represents the geometry of a model.

    Attributes:
        _geo_name (str): The name of the geometry.
        _geo (dict): The dictionary representation of the geometry.
        _bones (list): A list of bones in the geometry.
    """

    def __init__(self, geometry_name: str, texture_size: list[int, int] = (16, 16)) -> None:
        self._geo_name = geometry_name
        self._geo = {
            "description": {
                "identifier": f"geometry.{CONFIG.NAMESPACE}.{geometry_name}",
                "texture_width": texture_size[0],
                "texture_height": texture_size[1],
            },
            "bones": [],
        }
        self._bones: list[_Bone] = []

    def set_visible_bounds(
        self,
        visible_bounds_wh: list[float, float],
        visible_bounds_offset: list[float, float, float],
    ):
        self._geo["description"]["visible_bounds_width"] = visible_bounds_wh[0]
        self._geo["description"]["visible_bounds_height"] = visible_bounds_wh[1]
        self._geo["description"]["visible_bounds_offset"] = visible_bounds_offset
        return self

    def add_bone(self, name: str, pivot: list[int, int, int], parent: str = None) -> _Bone:
        bone = _Bone(name, pivot, parent)
        self._bones.append(bone)
        return bone

    @property
    def _queue(self):
        for bone in self._bones:
            self._geo["bones"].append(bone._queue)
        return self._geo


class _Anim_Bone:
    """
    The _Anim_Bone class represents a bone in the animation.

    Attributes:
        _name (str): The name of the bone.
        _bone (dict): The dictionary representation of the bone in the animation.
    """

    def __init__(self, name) -> None:
        self._name = name
        self._bone = {
            self._name: {
                "rotation": {},
                "position": {},
                "scale": {},
            }
        }

    def rotation(self, rotation: list[float, float, float] = (0, 0, 0), keyframe: float = 0.0):
        self._bone[self._name]["rotation"].update({keyframe: rotation})
        return self

    def position(self, position: list[float, float, float] = (0, 0, 0), keyframe: float = 0.0):
        self._bone[self._name]["position"].update({keyframe: position})
        return self

    def scale(
        self,
        scale: list[float, float, float] | float | Molang = 1,
        keyframe: float = 0.0,
    ):
        self._bone[self._name]["scale"].update({keyframe: scale if scale != 1 else {}})
        return self

    @property
    def _queue(self):
        if len(self._bone[self._name]["rotation"]) == 1 and list(self._bone[self._name]["rotation"].keys())[0] == 0:
            self._bone[self._name]["rotation"] = self._bone[self._name]["rotation"][0]

        if len(self._bone[self._name]["position"]) == 1 and list(self._bone[self._name]["position"].keys())[0] == 0:
            self._bone[self._name]["position"] = self._bone[self._name]["position"][0]

        if len(self._bone[self._name]["scale"]) == 1 and list(self._bone[self._name]["scale"].keys())[0] == 0:
            self._bone[self._name]["scale"] = self._bone[self._name]["scale"][0]
        return self._bone


class _Anims:
    """
    The _Anims class represents the animations of a model.

    Attributes:
        _name (str): The name of the model.
        _anim_name (str): The name of the animation.
        _loop (bool): If the animation should loop.
        _override_previous_animation (bool): If the animation should override the previous animation.
        _anim (dict): The dictionary representation of the animation.
        _bones (list): A list of bones in the animation.
    """

    def __init__(
        self,
        name,
        animation_name: str,
        loop: bool = False,
        override_previous_animation: bool = False,
    ) -> None:
        self._name = name
        self._anim_name = animation_name
        self._loop = loop
        self._override_previous_animation = override_previous_animation
        self._anim = {
            f"animation.{CONFIG.NAMESPACE}.{self._name}.{self._anim_name}": {
                "loop": self._loop,
                "override_previous_animation": self._override_previous_animation,
                "bones": {},
            }
        }
        self._bones: list[_Anim_Bone] = []

    def add_bone(self, name: str):
        self._bones.append(_Anim_Bone(name))
        return self._bones[-1]

    @property
    def _queue(self):
        for bone in self._bones:
            self._anim[f"animation.{CONFIG.NAMESPACE}.{self._name}.{self._anim_name}"]["bones"].update(bone._queue)
        return self._anim


class Geometry(AddonObject):
    """
    The Geometry class represents the geometric model.

    Attributes:
        _geos (list): A list of geometries in the model.
    """

    _extension = ".geo.json"
    _path = os.path.join("assets", "models")

    def __init__(self, name: str) -> None:
        super().__init__(
            name,
        )
        self._geos: list[_Geo] = []

    def add_geo(self, geometry_name: str, texture_size: tuple[int, int] = (16, 16)):
        geo = _Geo(geometry_name, texture_size)
        self._geos.append(geo)
        return geo

    def queue(self, type: str):
        if not type in ["actors", "blocks"]:
            CONFIG.Logger.unsupported_model_type(type)

        if len(self._geos) == 0:
            CONFIG.Logger.no_geo_found(self._name)

        if FileExists(os.path.join("assets", "models", type, f"{self._name}.geo.json")):
            with open(os.path.join("assets", "models", type, f"{self._name}.geo.json"), "r") as file:
                self.content(commentjson.load(file))
        else:
            self.content(JsonSchemes.geometry())

        for g in self._geos:
            for geo in self._content["minecraft:geometry"]:
                if f"geometry.{CONFIG.NAMESPACE}.{g._geo_name}" == geo["description"]["identifier"]:
                    self._content["minecraft:geometry"].remove(geo)

            self._content["minecraft:geometry"].append(g._queue)
        super().queue(type)
        super()._export()


class Animation(AddonObject):
    """
    A class used to represent an Animation.

    Attributes
    ----------
    _extension(dict) : A dictionary to map the animation extension types.
    _name (str) : The name of the animation.
    _anims (list) : A list of animation instances.
    """

    _extension = ".animation.json"
    _path = os.path.join("assets", "animations")

    def __init__(self, name: str) -> None:
        """
        Constructs all the necessary attributes for the Animation object.

        Parameters
        ----------
        name : str
            The name of the animation.
        """
        super().__init__(name)

        self._name = name
        self._anims: list[_Anims] = []

    def add_animation(
        self,
        animation_name: str,
        loop: bool = False,
        override_previous_animation: bool = False,
    ):
        """
        Adds an animation instance to the list of animations.

        Parameters
        ----------
        animation_name : str
            The name of the animation to be added.
        loop : bool, optional
            Whether the animation should loop (default is False).
        override_previous_animation : bool, optional
            Whether the new animation should override the previous one (default is False).

        Returns
        -------
        _Anims
            The newly created animation instance.
        """
        geo = _Anims(self._name, animation_name, loop, override_previous_animation)
        self._anims.append(geo)
        return geo

    @property
    def queue(self):
        """
        Gets the current state of the animation queue. If no animations are found, logs
        an error. Also, updates the content with existing or new animation schemes.

        Raises
        ------
        FileNotFoundError
            If the specified path does not exist.
        """
        if len(self._anims) == 0:
            CONFIG.Logger.no_anim_found(self._name)
        path = os.path.join("assets", "animations", f"{self._name}{self._extension}")
        if FileExists(path):
            with open(path, "r") as file:
                self.content(commentjson.load(file))
        else:
            self.content(JsonSchemes.rp_animations())

        for a in self._anims:
            self._content["animations"].update(a._queue)

        super().queue()
        self._export()
