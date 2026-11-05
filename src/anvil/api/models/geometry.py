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
    arm.locator("hand", offset=(6, 12, 0))

    geo.queue()
    ```

## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/schemasreference/schemas/minecraftschema_geometry_1.21.0)
"""

from collections.abc import Iterator, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Annotated, Any, ClassVar, Literal

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import GEOMETRY_VERSION
from anvil.lib.jsonmodel import (
    FitToFrame,
    JsonFile,
    JsonObject,
    Keyed,
    Length,
    NonNegative,
    json_field,
)


def _vec(value: Sequence[float], length: int) -> tuple[float, ...]:
    if isinstance(value, (str, bytes)):
        raise ValueError(f"Expected a vector of {length} values, got {value!r}.")
    values = tuple(value)
    if len(values) != length:
        raise ValueError(f"Expected a vector of {length} values, got {values}.")
    return values


def _number(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(
            f"Cannot transform non-numeric value {value!r}. Transforms only work on numbers."
        )
    return value


# region Cubes


class _CubeFace(JsonObject):
    """The UV of one face of a cube.

    Args:
        uv (tuple[float, float]): The corner of the face on the texture.
        uv_size (tuple[float, float], optional): How many texels the face maps. Game
            default: the cube's size.
        uv_rotation (Literal[0, 90, 180, 270], optional): Turns the UV clockwise before it
            is applied.
        material_instance (str, optional): The material instance of the face.
    """

    uv: tuple[float, float] = json_field()
    uv_size: tuple[float, float] | None = None
    uv_rotation: Literal[0, 90, 180, 270] | None = None
    material_instance: str | None = None

    def set_uv(self, u: float, v: float) -> "_CubeFace":
        """Sets the corner of the face on the texture."""
        self.uv = (u, v)
        return self

    def set_uv_size(self, width: float, height: float) -> "_CubeFace":
        """Sets how many texels the face maps."""
        self.uv_size = (width, height)
        return self

    def set_uv_rotation(self, uv_rotation: Literal[0, 90, 180, 270]) -> "_CubeFace":
        """Turns the UV clockwise before it is applied."""
        self.uv_rotation = uv_rotation
        return self

    def set_material_instance(self, material_instance: str) -> "_CubeFace":
        """Sets the material instance of the face."""
        self.material_instance = material_instance
        return self


class _CubeFaces(JsonObject):
    """Per-face UVs of a cube. A face left out is not drawn."""

    north: _CubeFace | None = None
    east: _CubeFace | None = None
    south: _CubeFace | None = None
    west: _CubeFace | None = None
    up: _CubeFace | None = None
    down: _CubeFace | None = None

    def _copy(self) -> "_CubeFaces":
        return replace(
            self,
            **{
                face: replace(value)
                for face in ("north", "east", "south", "west", "up", "down")
                if (value := getattr(self, face)) is not None
            },
        )


class _Cube(JsonObject):
    """A single cuboid. Created through :meth:`_Bone.cube`.

    Args:
        origin (tuple[float, float, float]): The unrotated lower corner.
        size (tuple[float, float, float]): How far the cube extends from its origin.
        uv (tuple[float, float] | _CubeFaces, optional): Box UV, or per-face UVs.
        pivot (tuple[float, float, float], optional): The point the cube rotates around.
        rotation (tuple[float, float, float], optional): The rotation, in degrees.
        inflate (float, optional): Grows the cube in every direction.
        mirror (bool, optional): Mirrors the cube's UV along the x axis.
    """

    origin: tuple[float, float, float] = json_field()
    size: tuple[float, float, float] = json_field()
    uv: tuple[float, float] | _CubeFaces = json_field(default=(0, 0))
    pivot: tuple[float, float, float] = json_field(default=(0, 0, 0), omit_default=True)
    rotation: tuple[float, float, float] = json_field(
        default=(0, 0, 0), omit_default=True
    )
    inflate: float = json_field(default=0, omit_default=True)
    mirror: bool = json_field(default=False, omit_default=True)

    @property
    def is_rotated(self) -> bool:
        return self.rotation != (0, 0, 0)

    def set_origin(self, x: float, y: float, z: float) -> "_Cube":
        """Sets the unrotated lower corner."""
        self.origin = (x, y, z)
        return self

    def set_size(self, x: float, y: float, z: float) -> "_Cube":
        """Sets how far the cube extends from its origin."""
        self.size = (x, y, z)
        return self

    def set_uv(self, uv: tuple[float, float] | _CubeFaces) -> "_Cube":
        """Sets box UV, `(u, v)`, or per-face UVs."""
        self.uv = uv
        return self

    def set_pivot(self, x: float, y: float, z: float) -> "_Cube":
        """Sets the point the cube rotates around."""
        self.pivot = (x, y, z)
        return self

    def set_rotation(self, x: float, y: float, z: float) -> "_Cube":
        """Sets the rotation, in degrees."""
        self.rotation = (x, y, z)
        return self

    def set_inflate(self, inflate: float) -> "_Cube":
        """Grows the cube in every direction."""
        self.inflate = inflate
        return self

    def set_mirror(self, mirror: bool = True) -> "_Cube":
        """Mirrors the cube's UV along the x axis."""
        self.mirror = mirror
        return self

    def _copy(self) -> "_Cube":
        uv = self.uv._copy() if isinstance(self.uv, _CubeFaces) else self.uv
        return replace(self, uv=uv)


def _face_uv(face: str, value: Sequence[Any] | _CubeFace) -> _CubeFace:
    """One face of `Bone.cube`: `(uv, uv_size)`, `(uv, uv_size, rotation)` or a `_CubeFace`."""
    if isinstance(value, _CubeFace):
        return value
    values = list(value) if not isinstance(value, (str, bytes)) else []
    if len(values) not in (2, 3):
        raise ValueError(
            f"Face '{face}' takes (uv, uv_size) or (uv, uv_size, rotation), got {value!r}."
        )
    return _CubeFace(
        uv=_vec(values[0], 2),
        uv_size=_vec(values[1], 2),
        uv_rotation=values[2] if len(values) == 3 and values[2] else None,
    )


# endregion

# region Bones


class _Locator(JsonObject):
    """A named attachment point. Created through :meth:`_Bone.locator`.

    Written as its offset alone when it has no rotation and keeps the inherited scale.

    Args:
        name (str): The locator name.
        offset (tuple[float, float, float]): The position, in model space.
        rotation (tuple[float, float, float], optional): The rotation, in model space.
        ignore_inherited_scale (bool, optional): Discards the scale inherited from the bone.
    """

    name: str = json_field(exclude=True, positional=True)
    offset: tuple[float, float, float] = json_field()
    rotation: tuple[float, float, float] | None = None
    ignore_inherited_scale: bool = json_field(default=False, omit_default=True)

    def set_offset(self, x: float, y: float, z: float) -> "_Locator":
        """Sets the position, in model space."""
        self.offset = (x, y, z)
        return self

    def set_rotation(self, x: float, y: float, z: float) -> "_Locator":
        """Sets the rotation, in model space."""
        self.rotation = (x, y, z)
        return self

    def set_ignore_inherited_scale(
        self, ignore_inherited_scale: bool = True
    ) -> "_Locator":
        """Discards the scale inherited from the bone."""
        self.ignore_inherited_scale = ignore_inherited_scale
        return self

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        return payload["offset"] if list(payload) == ["offset"] else payload

    @classmethod
    def __schema_body__(cls, definitions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return {"anyOf": [schema["properties"]["offset"], schema]}


class _Bone(JsonObject):
    """A bone in a :class:`Geometry`.

    Do not instantiate directly: use :meth:`Geometry.bone` for a root bone or
    :meth:`_Bone.bone` for a child bone.
    """

    name: str = json_field(positional=True)
    parent: str | None = json_field(default=None, init=False)
    pivot: tuple[float, float, float] = json_field(default=(0, 0, 0))
    rotation: tuple[float, float, float] = json_field(
        default=(0, 0, 0), omit_default=True
    )
    mirror: bool = json_field(default=False, omit_default=True)
    inflate: float | None = None
    debug: bool | None = None
    render_group_id: Annotated[int, NonNegative] | None = None
    binding: str | None = None
    cubes: list[_Cube] = json_field(default_factory=list, omit_default=True)
    locators: Annotated[list[_Locator], Keyed("name")] = json_field(
        default_factory=list, omit_default=True
    )
    _geometry: Any = json_field(default=None, init=False, exclude=True)
    _parent: Any = json_field(default=None, init=False, exclude=True)
    _children: list[Any] = json_field(default_factory=list, init=False, exclude=True)

    def __validate__(self) -> None:
        if not self.name:
            raise ValueError("Bone names cannot be empty.")

    @property
    def children(self) -> list["_Bone"]:
        return list(self._children)

    def _attach(self, geometry: "Geometry", parent: "_Bone | None") -> None:
        if not self.name:
            raise ValueError("Bone names cannot be empty.")
        self._geometry = geometry
        self._parent = parent
        self.parent = parent.name if parent is not None else None

    def _detach(self) -> None:
        self._geometry = None
        self._parent = None
        self.parent = None

    def _add_child(self, child: "_Bone") -> None:
        self._children.append(child)

    def _remove_child(self, child: "_Bone") -> None:
        self._children.remove(child)

    def _alive(self) -> "Geometry":
        if self._geometry is None:
            raise ValueError(f"Bone '{self.name}' was removed from its geometry.")
        return self._geometry

    def bone(
        self,
        name: str,
        pivot: Sequence[float] = (0, 0, 0),
        *,
        rotation: Sequence[float] = (0, 0, 0),
        mirror: bool = False,
        inflate: float | None = None,
        binding: str | None = None,
        render_group_id: int | None = None,
        debug: bool | None = None,
    ) -> "_Bone":
        """Creates a child bone of this bone and returns the **child**. See
        :meth:`Geometry.bone` for the arguments."""
        return self._alive()._add_bone(
            self,
            _Bone(
                name,
                pivot=_vec(pivot, 3),
                rotation=_vec(rotation, 3),
                mirror=mirror,
                inflate=inflate,
                binding=binding,
                render_group_id=render_group_id,
                debug=debug,
            ),
        )

    def remove(self) -> None:
        """Removes this bone and all of its descendants from the geometry."""
        self._alive()._remove_bone(self)

    def set_pivot(self, x: float, y: float, z: float) -> "_Bone":
        """Sets the point the bone rotates around."""
        self.pivot = (x, y, z)
        return self

    def set_rotation(self, x: float, y: float, z: float) -> "_Bone":
        """Sets the rotation before animation, in degrees."""
        self.rotation = (x, y, z)
        return self

    def set_mirror(self, mirror: bool = True) -> "_Bone":
        """Mirrors the UV of the bone's unrotated cubes along the x axis."""
        self.mirror = mirror
        return self

    def set_inflate(self, inflate: float) -> "_Bone":
        """Grows every cube of the bone in every direction."""
        self.inflate = inflate
        return self

    def set_binding(self, binding: str) -> "_Bone":
        """Sets the Molang naming the parent skeleton's bone this bone follows."""
        self.binding = binding
        return self

    def set_render_group_id(self, render_group_id: int) -> "_Bone":
        """Sets the render group of the bone."""
        self.render_group_id = render_group_id
        return self

    def set_debug(self, debug: bool = True) -> "_Bone":
        """Sets the bone's `debug` flag."""
        self.debug = debug
        return self

    def cube(
        self,
        origin: Sequence[float],
        size: Sequence[float],
        uv: Sequence[float] | None = None,
        *,
        north: Sequence[Any] | _CubeFace | None = None,
        east: Sequence[Any] | _CubeFace | None = None,
        south: Sequence[Any] | _CubeFace | None = None,
        west: Sequence[Any] | _CubeFace | None = None,
        up: Sequence[Any] | _CubeFace | None = None,
        down: Sequence[Any] | _CubeFace | None = None,
        pivot: Sequence[float] = (0, 0, 0),
        rotation: Sequence[float] = (0, 0, 0),
        inflate: float = 0.0,
        mirror: bool = False,
    ) -> "_Bone":
        """Adds a cube to this bone. Returns this bone so calls can be chained.

        UVs are either box UV, `uv=(u, v)`, or per face: any of `north`, `east`,
        `south`, `west`, `up` and `down`, each `(uv, uv_size)`,
        `(uv, uv_size, rotation)`, or a `_CubeFace`. Faces left out are not rendered.
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
            cube_uv: tuple[float, ...] | _CubeFaces = _CubeFaces(
                **{face: _face_uv(face, value) for face, value in faces.items()}
            )
        else:
            cube_uv = _vec(uv if uv is not None else (0, 0), 2)

        return self._add_cube(
            _Cube(
                origin=_vec(origin, 3),
                size=_vec(size, 3),
                uv=cube_uv,
                pivot=_vec(pivot, 3),
                rotation=_vec(rotation, 3),
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
        offset: Sequence[float],
        *,
        rotation: Sequence[float] | None = None,
        ignore_inherited_scale: bool = False,
    ) -> "_Bone":
        """Adds a locator to this bone. Returns this bone so calls can be chained.

        Args:
            name (str): The locator name.
            offset (Sequence[float]): The position, in model space.
            rotation (Sequence[float], optional): The rotation, in model space.
            ignore_inherited_scale (bool, optional): Discards the scale inherited from the
                bone.
        """
        geometry = self._alive()
        if any(existing.name == name for existing in self.locators):
            raise ValueError(
                f"Duplicate locator '{name}' in bone '{self.name}' of geometry '{geometry.name}'."
            )
        self.locators.append(
            _Locator(
                name,
                offset=_vec(offset, 3),
                rotation=None if rotation is None else _vec(rotation, 3),
                ignore_inherited_scale=ignore_inherited_scale,
            )
        )
        return self

    def _add_mesh(self, mesh: Any) -> "_Bone":
        """Adds the cubes of a Blockbench mesh (anything with `compile() -> list[_Cube]`)."""
        self._alive()
        self.cubes.extend(mesh.compile())
        return self

    def walk(self) -> Iterator["_Bone"]:
        """Yields this bone followed by all of its descendants (depth-first)."""
        yield self
        for child in self._children:
            yield from child.walk()

    def _copy_into(self, owner: "Geometry | _Bone", prefix: str) -> "_Bone":
        clone = owner.bone(
            prefix + self.name,
            self.pivot,
            rotation=self.rotation,
            mirror=self.mirror,
            inflate=self.inflate,
            binding=self.binding,
            render_group_id=self.render_group_id,
            debug=self.debug,
        )
        for cube in self.cubes:
            clone._add_cube(cube._copy())
        for locator in self.locators:
            clone._add_locator(replace(locator))
        for child in self._children:
            child._copy_into(clone, prefix)
        return clone

    def _add_locator(self, locator: _Locator) -> None:
        self.locators.append(locator)


# endregion

# region File


class _GeometryDescription(JsonObject):
    """The `description` of a geometry."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: str | None = None
    visible_bounds_width: float | None = None
    visible_bounds_height: float | None = None
    visible_bounds_offset: tuple[float, float, float] | None = None
    texture_width: int | None = None
    texture_height: int | None = None

    def set_identifier(self, identifier: str) -> None:
        """Sets the identifier entities and blocks reference the geometry by."""
        self.identifier = identifier

    def set_visible_bounds(self, width: float, height: float) -> None:
        """Sets the size of the visibility box, in blocks."""
        self.visible_bounds_width = width
        self.visible_bounds_height = height

    def set_visible_bounds_offset(self, x: float, y: float, z: float) -> None:
        """Sets the offset of the visibility box from the entity, in blocks."""
        self.visible_bounds_offset = (x, y, z)

    def set_texture_size(self, width: int, height: int) -> None:
        """Sets the size of the texture, in texels."""
        self.texture_width = width
        self.texture_height = height

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("A geometry needs an identifier.")


class _GeometryModel(JsonObject):
    """One geometry of a `minecraft:geometry` list."""

    description: _GeometryDescription = json_field(default_factory=_GeometryDescription)
    item_display_transforms: ItemDisplayTransforms | None = None
    cape: str | None = None
    bones: list[_Bone] = json_field(default_factory=list, omit_default=True)

    def set_item_display_transforms(
        self, item_display_transforms: ItemDisplayTransforms | None
    ) -> None:
        """Sets how the geometry is shown as an item, or None to remove it."""
        self.item_display_transforms = item_display_transforms

    def set_cape(self, cape: str) -> None:
        """Sets the cape texture of the geometry."""
        self.cape = cape

    def set_bones(self, bones: Sequence[_Bone]) -> None:
        """Sets every bone, parents before their children."""
        self.bones = list(bones)


class _GeometryFile(JsonObject):
    """The content of `models/entity/<name>.geo.json`."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:geometry")

    format_version: str = json_field(default=GEOMETRY_VERSION, init=False)
    geometry: Annotated[list[_GeometryModel], Length(1, 1)] = json_field(
        key="minecraft:geometry", default_factory=lambda: [_GeometryModel()]
    )


class Geometry(JsonFile[_GeometryFile]):
    """A Bedrock geometry file (``*.geo.json``) built from a tree of bones.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/schemasreference/schemas/minecraftschema_geometry_1.21.0)
    """

    _extension = ".geo.json"
    _pack = Pack.RP
    _folder = Path("models", "entity")
    _object_type = "Geometry"

    def __init__(
        self,
        name: str,
        texture_size: tuple[int, int] = (64, 64),
        visible_bounds: tuple[float, float] = (1, 1),
        visible_offset: tuple[float, float, float] = (0, 0, 0),
    ) -> None:
        super().__init__(name)
        self._roots: list[_Bone] = []
        self._by_name: dict[str, _Bone] = {}
        self._description.set_identifier(self.geometry_identifier)
        self.set_texture_size(*texture_size)
        self.set_visible_bounds(*visible_bounds)
        self.set_visible_offset(*visible_offset)

    @property
    def _model(self) -> _GeometryModel:
        return self._document.geometry[0]

    @property
    def _description(self) -> _GeometryDescription:
        return self._model.description

    @property
    def texture_size(self) -> tuple[int, int]:
        return (self._description.texture_width, self._description.texture_height)

    @property
    def visible_bounds(self) -> tuple[float, float]:
        return (
            self._description.visible_bounds_width,
            self._description.visible_bounds_height,
        )

    @property
    def visible_offset(self) -> tuple[float, float, float]:
        return self._description.visible_bounds_offset

    @property
    def item_display_transforms(self) -> "ItemDisplayTransforms | None":
        """How a block geometry is shown as an item."""
        return self._model.item_display_transforms

    def set_texture_size(self, width: int, height: int) -> "Geometry":
        """Sets the size of the texture, in texels."""
        self._description.set_texture_size(width, height)
        return self

    def set_visible_bounds(self, width: float, height: float) -> "Geometry":
        """Sets the size of the visibility box, in blocks."""
        self._description.set_visible_bounds(width, height)
        return self

    def set_visible_offset(self, x: float, y: float, z: float) -> "Geometry":
        """Sets the offset of the visibility box from the entity, in blocks."""
        self._description.set_visible_bounds_offset(x, y, z)
        return self

    def set_item_display_transforms(
        self, item_display_transforms: "ItemDisplayTransforms | None"
    ) -> "Geometry":
        """Sets how a block geometry is shown as an item, or None to remove it."""
        self._model.set_item_display_transforms(item_display_transforms)
        return self

    def set_cape(self, cape: str) -> "Geometry":
        """Sets the cape texture of the geometry."""
        self._model.set_cape(cape)
        return self

    def _sync(self) -> None:
        self._model.set_bones(self.bones)

    def _add_bone(self, parent: _Bone | None, bone: _Bone) -> _Bone:
        bone._attach(self, parent)
        if bone.name in self._by_name:
            raise ValueError(
                f"Duplicate bone '{bone.name}' in geometry '{self.identifier.name}'. Bone names must be unique."
            )
        self._by_name[bone.name] = bone
        if parent is None:
            self._roots.append(bone)
        else:
            parent._add_child(bone)
        self._sync()
        return bone

    def _remove_bone(self, bone: _Bone) -> None:
        if bone._parent is None:
            self._roots.remove(bone)
        else:
            bone._parent._remove_child(bone)
        for removed in list(bone.walk()):
            self._by_name.pop(removed.name, None)
            removed._detach()
        self._sync()

    def bone(
        self,
        name: str,
        pivot: Sequence[float] = (0, 0, 0),
        *,
        rotation: Sequence[float] = (0, 0, 0),
        mirror: bool = False,
        inflate: float | None = None,
        binding: str | None = None,
        render_group_id: int | None = None,
        debug: bool | None = None,
    ) -> _Bone:
        """Creates a root bone (no parent) and returns it.

        Args:
            name (str): The bone name, unique in the geometry.
            pivot (Sequence[float], optional): The point the bone rotates around.
            rotation (Sequence[float], optional): The rotation before animation, in degrees.
            mirror (bool, optional): Mirrors the UV of the bone's unrotated cubes.
            inflate (float, optional): Grows every cube of the bone.
            binding (str, optional): Molang naming the parent skeleton's bone to follow.
            render_group_id (int, optional): The render group of the bone.
            debug (bool, optional): The bone's `debug` flag.
        """
        return self._add_bone(
            None,
            _Bone(
                name,
                pivot=_vec(pivot, 3),
                rotation=_vec(rotation, 3),
                mirror=mirror,
                inflate=inflate,
                binding=binding,
                render_group_id=render_group_id,
                debug=debug,
            ),
        )

    def find(self, name: str) -> _Bone | None:
        return self._by_name.get(name)

    @property
    def geometry_identifier(self) -> str:
        """How entities and blocks reference this geometry: ``geometry.<namespace>.<name>``."""
        return f"geometry.{CONFIG.NAMESPACE}.{self.identifier.name}"

    @property
    def bones(self) -> list[_Bone]:
        """All bones, parents always before their children."""
        return [bone for root in self._roots for bone in root.walk()]

    @property
    def locator_names(self) -> set[str]:
        return {loc.name for bone in self.bones for loc in bone.locators}

    def clone(self, name: str | None = None) -> "Geometry":
        """Returns an independent copy, optionally under a new name."""
        clone = Geometry(
            name or self.identifier.name,
            self.texture_size,
            self.visible_bounds,
            self.visible_offset,
        )
        transforms = self.item_display_transforms
        if transforms is not None:
            clone.set_item_display_transforms(transforms._copy())
        if self._model.cape is not None:
            clone.set_cape(self._model.cape)
        for root in self._roots:
            root._copy_into(clone, "")
        return clone

    def merge(
        self,
        other: "Geometry",
        *,
        parent: _Bone | None = None,
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

    def translate(self, offset: Sequence[float]) -> "Geometry":
        """Moves the whole model by `offset`. Pivots, cube origins and locator offsets are
        model-space positions, so they all move together."""
        dx, dy, dz = (_number(v) for v in _vec(offset, 3))

        def move(vec: Sequence[float]) -> tuple[float, float, float]:
            return (
                _number(vec[0]) + dx,
                _number(vec[1]) + dy,
                _number(vec[2]) + dz,
            )

        for bone in self.bones:
            bone.set_pivot(*move(bone.pivot))
            for cube in bone.cubes:
                cube.set_origin(*move(cube.origin))
                if cube.is_rotated or cube.pivot != (0, 0, 0):
                    cube.set_pivot(*move(cube.pivot))
            for locator in bone.locators:
                locator.set_offset(*move(locator.offset))
        return self

    def scale(self, factor: float, origin: Sequence[float] = (0, 0, 0)) -> "Geometry":
        """Scales the whole model by `factor` around `origin`."""
        _number(factor)
        ox, oy, oz = (_number(v) for v in _vec(origin, 3))

        def grow(vec: Sequence[float]) -> tuple[float, float, float]:
            return (
                ox + (_number(vec[0]) - ox) * factor,
                oy + (_number(vec[1]) - oy) * factor,
                oz + (_number(vec[2]) - oz) * factor,
            )

        for bone in self.bones:
            bone.set_pivot(*grow(bone.pivot))
            if bone.inflate:
                bone.set_inflate(_number(bone.inflate) * factor)
            for cube in bone.cubes:
                cube.set_origin(*grow(cube.origin))
                cube.set_size(*(_number(v) * factor for v in cube.size))
                if cube.inflate:
                    cube.set_inflate(_number(cube.inflate) * factor)
                if cube.is_rotated or cube.pivot != (0, 0, 0):
                    cube.set_pivot(*grow(cube.pivot))
            for locator in bone.locators:
                locator.set_offset(*grow(locator.offset))
        return self


# endregion

# region Item display transforms


class ItemDisplayTransform(JsonObject):
    """How a block's item is shown in one display slot. Vectors are (x, y, z).

    Args:
        rotation (tuple[float, float, float], optional): The rotation, in degrees.
        translation (tuple[float, float, float], optional): The offset.
        scale (tuple[float, float, float], optional): The scale.
        rotation_pivot (tuple[float, float, float], optional): The point the rotation turns around.
        scale_pivot (tuple[float, float, float], optional): The point the scale grows from.
    """

    rotation: tuple[float, float, float] | None = json_field(default=None)
    translation: tuple[float, float, float] | None = json_field(default=None)
    scale: tuple[float, float, float] | None = json_field(default=None)
    rotation_pivot: tuple[float, float, float] | None = json_field(default=None)
    scale_pivot: tuple[float, float, float] | None = json_field(default=None)


class ItemDisplayGuiTransform(ItemDisplayTransform):
    """The `gui` display slot, the only one that accepts `fit_to_frame`. It also takes every
    option of `ItemDisplayTransform`.

    Args:
        fit_to_frame (bool, optional): True is written as `{}`, which is how Blockbench exports it; False as `false`, which Minecraft may reject from 1.21.130.
    """

    fit_to_frame: Annotated[bool, FitToFrame] | None = json_field(default=None)


class ItemDisplayTransforms(JsonObject):
    """How a block's item is shown in each display slot.

    Args:
        thirdperson_righthand (ItemDisplayTransform, optional): The transform of the `thirdperson_righthand` slot.
        thirdperson_lefthand (ItemDisplayTransform, optional): The transform of the `thirdperson_lefthand` slot.
        firstperson_righthand (ItemDisplayTransform, optional): The transform of the `firstperson_righthand` slot.
        firstperson_lefthand (ItemDisplayTransform, optional): The transform of the `firstperson_lefthand` slot.
        head (ItemDisplayTransform, optional): The transform of the `head` slot.
        ground (ItemDisplayTransform, optional): The transform of the `ground` slot.
        fixed (ItemDisplayTransform, optional): The transform of the `fixed` slot.
        gui (ItemDisplayGuiTransform, optional): The transform of the `gui` slot.
    """

    thirdperson_righthand: ItemDisplayTransform | None = json_field(default=None)
    thirdperson_lefthand: ItemDisplayTransform | None = json_field(default=None)
    firstperson_righthand: ItemDisplayTransform | None = json_field(default=None)
    firstperson_lefthand: ItemDisplayTransform | None = json_field(default=None)
    gui: ItemDisplayGuiTransform | None = json_field(default=None)
    head: ItemDisplayTransform | None = json_field(default=None)
    ground: ItemDisplayTransform | None = json_field(default=None)
    fixed: ItemDisplayTransform | None = json_field(default=None)

    def _copy(self) -> "ItemDisplayTransforms":
        return replace(
            self,
            **{
                spec.name: replace(value)
                for spec in self.__json_fields__()
                if (value := getattr(self, spec.name)) is not None
            },
        )


# endregion
