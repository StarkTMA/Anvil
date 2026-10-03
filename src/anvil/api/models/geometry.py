"""Builders for Bedrock geometry files (``*.geo.json``).

The tree structure is enforced by the API itself: a :class:`Geometry` only
creates root bones, and a :class:`_Bone` creates child bones, cubes and
locators. A child bone always knows its parent, so the ``parent`` field of the
compiled output is never written by hand.

Example:
    ```python
    geo = Geometry("my_mob", texture_size=(64, 64))

    body = geo.bone("body", pivot=(0, 12, 0))
    body.cube(origin=(-4, 12, -2), size=(8, 12, 4), uv=(16, 16))

    arm = body.bone("arm", pivot=(5, 22, 0))  # parent is "body"
    arm.cube(origin=(4, 12, -2), size=(4, 12, 4), uv=(40, 16))
    arm.locator("hand", position=(6, 12, 0))

    geo.queue()
    ```
"""

import copy
import os
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    TypedDict,
    Union,
    Unpack,
)

from anvil.api.core.types import Vector2D, Vector3D
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes

_FACES = ("north", "east", "south", "west", "up", "down")
_FACE_KEYS = {"uv", "uv_size", "uv_rotation", "material_instance"}

_UV = Union[Sequence[float], Dict[str, Any]]
# One face of Bone.cube: (uv, uv_size), (uv, uv_size, rotation) or a dict
_FaceUV = Union[Sequence[Any], Dict[str, Any]]


def _vec(value: Sequence[float], length: int) -> List[float]:
    if isinstance(value, (str, bytes)):
        raise ValueError(f"Expected a vector of {length} values, got {value!r}.")
    values = list(value)
    if len(values) != length:
        raise ValueError(f"Expected a vector of {length} values, got {values}.")
    return values


def _vec3(value: Sequence[float]) -> List[float]:
    return _vec(value, 3)


def _number(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            f"Cannot transform non-numeric value {value!r}. Transforms only work on numbers."
        )
    return value


def _face_uv(face: str, value: Any) -> Dict[str, Any]:
    """One face of `Bone.cube`: `(uv, uv_size)`, `(uv, uv_size, rotation)` or a dict."""
    if isinstance(value, dict):
        unknown = set(value) - _FACE_KEYS
        if unknown or "uv" not in value:
            raise ValueError(
                f"Face '{face}' dict needs 'uv' and accepts only {sorted(_FACE_KEYS)}, got {sorted(value)}."
            )
        data = dict(value)
        data["uv"] = _vec(value["uv"], 2)
        if "uv_size" in value:
            data["uv_size"] = _vec(value["uv_size"], 2)
    else:
        values = list(value) if not isinstance(value, (str, bytes)) else []
        if len(values) not in (2, 3):
            raise ValueError(
                f"Face '{face}' takes (uv, uv_size) or (uv, uv_size, rotation), got {value!r}."
            )
        data = {"uv": _vec(values[0], 2), "uv_size": _vec(values[1], 2)}
        if len(values) == 3 and values[2]:
            data["uv_rotation"] = values[2]

    if data.get("uv_rotation", 0) not in (0, 90, 180, 270):
        raise ValueError(f"Face '{face}' UV rotation must be 0, 90, 180 or 270.")
    return data


def _check_uv(uv: _UV) -> Union[List[float], Dict[str, Any]]:
    if isinstance(uv, dict):
        for face, data in uv.items():
            if face not in _FACES:
                raise ValueError(
                    f"Unknown cube face '{face}'. Expected one of {_FACES}."
                )
            if not isinstance(data, dict) or "uv" not in data:
                raise ValueError(
                    f"Face '{face}' needs a dict with at least a 'uv' entry."
                )
        return copy.deepcopy(uv)
    return _vec(uv, 2)


class _Cube:
    """A single cuboid. Created through :meth:`_Bone.cube`."""

    def __init__(
        self,
        origin: Sequence[float],
        size: Sequence[float],
        uv: _UV = (0, 0),
        *,
        pivot: Sequence[float] = (0, 0, 0),
        rotation: Sequence[float] = (0, 0, 0),
        inflate: float = 0.0,
        mirror: bool = False,
    ) -> None:
        self.origin = _vec3(origin)
        self.size = _vec3(size)
        self.uv = _check_uv(uv)
        self.pivot = _vec3(pivot)
        self.rotation = _vec3(rotation)
        self.inflate = inflate
        self.mirror = mirror

    @property
    def is_rotated(self) -> bool:
        return self.rotation != [0, 0, 0]

    def compile(self) -> dict:
        cube: Dict[str, Any] = {
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
    """A named attachment point. Created through :meth:`_Bone.locator`."""

    def __init__(
        self,
        name: str,
        position: Sequence[float],
        *,
        rotation: Sequence[float] = (0, 0, 0),
        ignore_inherited_scale: bool = False,
    ) -> None:
        self.name = name
        self.position = _vec3(position)
        self.rotation = _vec3(rotation)
        self.ignore_inherited_scale = ignore_inherited_scale

    def compile(self) -> dict:
        data: Dict[str, Any] = {"offset": self.position}
        if self.rotation != [0, 0, 0] or self.ignore_inherited_scale:
            data["rotation"] = self.rotation
        if self.ignore_inherited_scale:
            data["ignore_inherited_scale"] = True

        if list(data.keys()) == ["offset"]:
            return {self.name: self.position}
        return {self.name: data}


class _BoneOptions(TypedDict, total=False):
    """Optional bone properties accepted by `Geometry.bone` and `_Bone.bone`."""

    rotation: Sequence[float]
    bind_pose_rotation: Sequence[float]
    mirror: bool
    inflate: float
    binding: str
    material: str
    never_render: bool
    reset: bool
    render_group_id: int


class _Bone:
    """A bone in a :class:`Geometry`.

    Do not instantiate directly: use :meth:`Geometry.bone` for a root bone or
    :meth:`_Bone.bone` for a child bone.
    """

    def __init__(
        self,
        geometry: "Geometry",
        name: str,
        parent: Optional["_Bone"] = None,
        pivot: Sequence[float] = (0, 0, 0),
        **options: Unpack[_BoneOptions],
    ) -> None:
        if not name:
            raise ValueError("Bone names cannot be empty.")
        unknown = set(options) - set(_BoneOptions.__annotations__)
        if unknown:
            raise TypeError(f"Unknown bone option(s): {', '.join(sorted(unknown))}.")

        self._geometry: Optional["Geometry"] = geometry
        self._parent = parent
        self._children: List["_Bone"] = []
        self._name = name
        self.pivot = _vec3(pivot)
        self.rotation = _vec3(options.get("rotation", (0, 0, 0)))
        bind_pose = options.get("bind_pose_rotation")
        self.bind_pose_rotation: Optional[List[float]] = (
            _vec3(bind_pose) if bind_pose is not None else None
        )
        self.mirror = options.get("mirror", False)
        self.inflate: Optional[float] = options.get("inflate")
        self.binding: Optional[str] = options.get("binding")
        self.material: Optional[str] = options.get("material")
        self.never_render = options.get("never_render", False)
        self.reset = options.get("reset", False)
        self.render_group_id: Optional[int] = options.get("render_group_id")
        self.cubes: List[_Cube] = []
        self.locators: List[_Locator] = []
        # Anything exposing ``compile() -> list[dict]`` that yields cubes
        # (used by the Blockbench Wavefront importer).
        self._meshes: List[Any] = []

    # -- structure -----------------------------------------------------------

    @property
    def name(self) -> str:
        """Read-only: bones are indexed by name, so they cannot be renamed."""
        return self._name

    @property
    def parent(self) -> Optional["_Bone"]:
        return self._parent

    @property
    def children(self) -> List["_Bone"]:
        return list(self._children)

    def _alive(self) -> "Geometry":
        if self._geometry is None:
            raise ValueError(f"Bone '{self._name}' was removed from its geometry.")
        return self._geometry

    def bone(
        self,
        name: str,
        pivot: Sequence[float] = (0, 0, 0),
        **options: Unpack[_BoneOptions],
    ) -> "_Bone":
        """Creates a child bone of this bone and returns the **child**."""
        geometry = self._alive()
        child = _Bone(geometry, name, self, pivot, **options)
        geometry._register(child)
        self._children.append(child)
        return child

    def remove(self) -> None:
        """Removes this bone and all of its descendants from the geometry."""
        geometry = self._alive()
        siblings = self._parent._children if self._parent else geometry._roots
        siblings.remove(self)
        for bone in self.walk():
            geometry._by_name.pop(bone._name, None)
            bone._geometry = None
        self._parent = None

    def cube(
        self,
        origin: Sequence[float],
        size: Sequence[float],
        uv: Optional[Sequence[float]] = None,
        *,
        north: Optional[_FaceUV] = None,
        east: Optional[_FaceUV] = None,
        south: Optional[_FaceUV] = None,
        west: Optional[_FaceUV] = None,
        up: Optional[_FaceUV] = None,
        down: Optional[_FaceUV] = None,
        pivot: Sequence[float] = (0, 0, 0),
        rotation: Sequence[float] = (0, 0, 0),
        inflate: float = 0.0,
        mirror: bool = False,
    ) -> "_Bone":
        """Adds a cube to this bone. Returns this bone so calls can be chained.

        UVs are either box UV, `uv=(u, v)`, or per face: any of `north`, `east`,
        `south`, `west`, `up` and `down`, each `(uv, uv_size)`,
        `(uv, uv_size, rotation)`, or a dict with `uv`, `uv_size` and optionally
        `uv_rotation` and `material_instance`. Faces left out are not rendered.
        Without either, the cube uses box UV `(0, 0)`.

        Example:
            ```python
            bone.cube(origin=(0, 0, 0), size=(4, 4, 4), uv=(16, 16))
            bone.cube(
                origin=(0, 0, 0),
                size=(4, 4, 4),
                north=((0, 0), (4, 4)),
                up=((4, 0), (4, 4), 90),
            )
            ```
        """
        given = dict(north=north, east=east, south=south, west=west, up=up, down=down)
        faces = {face: value for face, value in given.items() if value is not None}
        if faces and uv is not None:
            raise ValueError(
                "A cube uses either box UV (uv=(u, v)) or per-face UVs (north=..., up=...), not both."
            )
        if faces:
            cube_uv: _UV = {
                face: _face_uv(face, value) for face, value in faces.items()
            }
        else:
            cube_uv = uv if uv is not None else (0, 0)

        return self._add_cube(
            _Cube(
                origin,
                size,
                cube_uv,
                pivot=pivot,
                rotation=rotation,
                inflate=inflate,
                mirror=mirror,
            )
        )

    def _add_cube(self, cube: _Cube) -> "_Bone":
        self._alive()
        self.cubes.append(cube)
        return self

    def locator(
        self,
        name: str,
        position: Sequence[float],
        *,
        rotation: Sequence[float] = (0, 0, 0),
        ignore_inherited_scale: bool = False,
    ) -> "_Bone":
        """Adds a locator to this bone. Returns this bone so calls can be chained."""
        geometry = self._alive()
        if any(existing.name == name for existing in self.locators):
            raise ValueError(
                f"Duplicate locator '{name}' in bone '{self._name}' of geometry '{geometry._name}'."
            )
        self.locators.append(
            _Locator(
                name,
                position,
                rotation=rotation,
                ignore_inherited_scale=ignore_inherited_scale,
            )
        )
        return self

    def _add_mesh(self, mesh: Any) -> "_Bone":
        self._alive()
        self._meshes.append(mesh)
        return self

    def walk(self) -> Iterator["_Bone"]:
        """Yields this bone followed by all of its descendants (depth-first)."""
        yield self
        for child in self._children:
            yield from child.walk()

    # -- copying -------------------------------------------------------------

    def _options(self) -> Dict[str, Any]:
        options: Dict[str, Any] = {
            "pivot": list(self.pivot),
            "rotation": list(self.rotation),
            "mirror": self.mirror,
            "never_render": self.never_render,
            "reset": self.reset,
        }
        if self.bind_pose_rotation is not None:
            options["bind_pose_rotation"] = list(self.bind_pose_rotation)
        for key in ("inflate", "binding", "material", "render_group_id"):
            value = getattr(self, key)
            if value is not None:
                options[key] = value
        return options

    def _copy_into(self, owner: Union["Geometry", "_Bone"], prefix: str) -> "_Bone":
        clone = owner.bone(prefix + self._name, **self._options())
        clone.cubes = copy.deepcopy(self.cubes)
        clone.locators = copy.deepcopy(self.locators)
        clone._meshes = copy.copy(self._meshes)
        for child in self._children:
            child._copy_into(clone, prefix)
        return clone

    # -- output --------------------------------------------------------------

    def compile(self) -> dict:
        bone: Dict[str, Any] = {"name": self._name, "pivot": self.pivot, "cubes": []}
        if self.rotation != [0, 0, 0]:
            bone["rotation"] = self.rotation
        if self.bind_pose_rotation is not None:
            bone["bind_pose_rotation"] = self.bind_pose_rotation
        if self.mirror:
            bone["mirror"] = self.mirror
        if self.inflate:
            bone["inflate"] = self.inflate
        if self._parent is not None:
            bone["parent"] = self._parent._name
        if self.binding:
            bone["binding"] = self.binding
        if self.material:
            bone["material"] = self.material
        if self.never_render:
            bone["neverRender"] = True
        if self.reset:
            bone["reset"] = True
        if self.render_group_id is not None:
            bone["render_group_id"] = self.render_group_id

        if self.cubes:
            bone["cubes"] = [cube.compile() for cube in self.cubes]

        if self.locators:
            bone["locators"] = {
                k: v for loc in self.locators for k, v in loc.compile().items()
            }

        for mesh in self._meshes:
            bone["cubes"].extend(mesh.compile())

        return bone


class Geometry(AddonObject):
    """A Bedrock geometry file (``*.geo.json``) built from a tree of bones."""

    _extension = ".geo.json"
    _path = os.path.join(CONFIG.RP_PATH, "models", "entity")

    def __init__(
        self,
        name: str,
        texture_size: Vector2D = (64, 64),
        visible_bounds: Vector2D = (1, 1),
        visible_offset: Vector3D = (0, 0, 0),
    ) -> None:
        super().__init__(name)
        self.texture_size = list(texture_size)
        self.visible_bounds = list(visible_bounds)
        self.visible_offset = list(visible_offset)
        # Only set for block geometries.
        self.item_display_transforms: Optional[Dict[str, Any]] = None
        self._roots: List[_Bone] = []
        self._by_name: Dict[str, _Bone] = {}

    def _register(self, bone: _Bone) -> None:
        if bone._name in self._by_name:
            raise ValueError(
                f"Duplicate bone '{bone._name}' in geometry '{self._name}'. Bone names must be unique."
            )
        self._by_name[bone._name] = bone

    def bone(
        self,
        name: str,
        pivot: Sequence[float] = (0, 0, 0),
        **options: Unpack[_BoneOptions],
    ) -> _Bone:
        """Creates a root bone (no parent) and returns it."""
        bone = _Bone(self, name, None, pivot, **options)
        self._register(bone)
        self._roots.append(bone)
        return bone

    def find(self, name: str) -> Optional[_Bone]:
        return self._by_name.get(name)

    @property
    def geometry_identifier(self) -> str:
        """How entities and blocks reference this geometry: ``geometry.<namespace>.<name>``."""
        return f"geometry.{CONFIG.NAMESPACE}.{self._name}"

    @property
    def bones(self) -> List[_Bone]:
        """All bones, parents always before their children."""
        return [bone for root in self._roots for bone in root.walk()]

    @property
    def locator_names(self) -> set[str]:
        return {loc.name for bone in self.bones for loc in bone.locators}

    # -- copying and combining ----------------------------------------------

    def clone(self, name: Optional[str] = None) -> "Geometry":
        """Returns an independent copy, optionally under a new name."""
        clone = Geometry(
            name or self._name,
            self.texture_size,
            self.visible_bounds,
            self.visible_offset,
        )
        clone.item_display_transforms = copy.deepcopy(self.item_display_transforms)
        for root in self._roots:
            root._copy_into(clone, "")
        return clone

    def merge(
        self,
        other: "Geometry",
        *,
        parent: Optional[_Bone] = None,
        prefix: str = "",
    ) -> "Geometry":
        """Copies the bones of `other` into this geometry.

        They become root bones, or children of `parent`. `prefix` is added to
        every copied bone name to avoid clashes. Texture size and bounds of this
        geometry are kept.
        """
        if other is self:
            raise ValueError("Cannot merge a geometry into itself. Use clone().")
        if parent is not None and parent._geometry is not self:
            raise ValueError(f"Bone '{parent.name}' does not belong to this geometry.")
        for root in other._roots:
            root._copy_into(parent if parent is not None else self, prefix)
        return self

    # -- transforms ----------------------------------------------------------
    # Pivots, cube origins and locator offsets are absolute model-space
    # positions in Bedrock geometry, so they all move together.

    def translate(self, offset: Sequence[float]) -> "Geometry":
        """Moves the whole model by `offset`."""
        dx, dy, dz = (_number(v) for v in _vec3(offset))

        def move(vec: List[float]) -> List[float]:
            return [
                _number(vec[0]) + dx,
                _number(vec[1]) + dy,
                _number(vec[2]) + dz,
            ]

        for bone in self.bones:
            bone.pivot = move(bone.pivot)
            for cube in bone.cubes:
                cube.origin = move(cube.origin)
                if cube.is_rotated or cube.pivot != [0, 0, 0]:
                    cube.pivot = move(cube.pivot)
            for locator in bone.locators:
                locator.position = move(locator.position)
        return self

    def scale(self, factor: float, origin: Sequence[float] = (0, 0, 0)) -> "Geometry":
        """Scales the whole model by `factor` around `origin`."""
        _number(factor)
        ox, oy, oz = (_number(v) for v in _vec3(origin))

        def grow(vec: List[float]) -> List[float]:
            return [
                ox + (_number(vec[0]) - ox) * factor,
                oy + (_number(vec[1]) - oy) * factor,
                oz + (_number(vec[2]) - oz) * factor,
            ]

        for bone in self.bones:
            bone.pivot = grow(bone.pivot)
            if bone.inflate:
                bone.inflate = _number(bone.inflate) * factor
            for cube in bone.cubes:
                cube.origin = grow(cube.origin)
                cube.size = [_number(v) * factor for v in cube.size]
                if cube.inflate:
                    cube.inflate = _number(cube.inflate) * factor
                if cube.is_rotated or cube.pivot != [0, 0, 0]:
                    cube.pivot = grow(cube.pivot)
            for locator in bone.locators:
                locator.position = grow(locator.position)
        return self

    # -- output --------------------------------------------------------------

    def compile(self) -> dict:
        content = JsonSchemes.geometry(
            self._name,
            self.texture_size,
            self.visible_bounds,
            self.visible_offset,
        )
        description = content["minecraft:geometry"][0]
        description["bones"] = [bone.compile() for bone in self.bones]
        if self.item_display_transforms is not None:
            description["item_display_transforms"] = self.item_display_transforms
        return content

    def __export__(self) -> None:
        self.content(self.compile())
        super().__export__()
