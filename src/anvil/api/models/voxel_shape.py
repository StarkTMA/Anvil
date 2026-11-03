"""Builder for Bedrock voxel shape files (``*.shape.json``).

Built like a :class:`~anvil.api.models.geometry.Geometry`: a :class:`VoxelShape` only
creates root groups, and a :class:`_VoxelGroup` creates boxes and child groups.
Groups organise the shape and can be found again by name; the file itself is a
flat list of every box, in the order they were added.

Example:
    ```python
    shape = VoxelShape("table")
    shape.group("top").box(min=(0, 12, 0), max=(16, 16, 16))

    legs = shape.group("legs")
    legs.box(min=(0, 0, 0), max=(2, 12, 2)).box(min=(14, 0, 14), max=(16, 12, 16))

    BlockGeometry(table).block_culling(shape)
    ```

## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/voxelshapes)
"""

from typing import Annotated, ClassVar, Iterator, Sequence

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import VOXEL_SHAPE_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, Length, json_field


class _Box(JsonObject):
    """An axis-aligned box, in pixels from the block's corner. Created through
    :meth:`_VoxelGroup.box`.

    Args:
        min (tuple[float, float, float]): The corner with the smallest coordinates.
        max (tuple[float, float, float]): The opposite corner.
    """

    min: tuple[float, float, float] = json_field()
    max: tuple[float, float, float] = json_field()

    def set_min(self, x: float, y: float, z: float) -> "_Box":
        """Sets the corner with the smallest coordinates."""
        self.min = (x, y, z)
        return self

    def set_max(self, x: float, y: float, z: float) -> "_Box":
        """Sets the corner with the largest coordinates."""
        self.max = (x, y, z)
        return self

    def __validate__(self) -> None:
        if any(low >= high for low, high in zip(self.min, self.max)):
            raise ValueError(
                f"Box min {self.min} must be smaller than max {self.max} on every axis."
            )
        if any(not -30 <= value <= 30 for value in (*self.min, *self.max)):
            raise ValueError(
                f"Box {self.min} to {self.max} must stay within -30 and 30 pixels."
            )
        if any(
            min(high, 16) - max(low, 0) < 1 for low, high in zip(self.min, self.max)
        ):
            raise ValueError(
                f"Box {self.min} to {self.max} must overlap the block by at least one pixel."
            )


class _VoxelShapeDescription(JsonObject):
    """The `description` of a voxel shape."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: str | None = None

    def set_identifier(self, identifier: str) -> None:
        """Sets the `namespace:name` blocks reference the shape by."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("A voxel shape needs an identifier.")


class _VoxelShapeBoxes(JsonObject):
    """The `shape` of a voxel shape: up to 32 boxes."""

    boxes: Annotated[list[_Box], Length(1, 32)] = json_field(default_factory=list)

    def set_boxes(self, boxes: Sequence[_Box]) -> None:
        """Sets every box of the shape."""
        self.boxes = list(boxes)


class _VoxelShapeDefinition(JsonObject):
    """The `minecraft:voxel_shape` object."""

    description: _VoxelShapeDescription = json_field(
        default_factory=_VoxelShapeDescription
    )
    shape: _VoxelShapeBoxes = json_field(default_factory=_VoxelShapeBoxes)


class _VoxelShapeFile(JsonObject):
    """The content of `shapes/<name>.shape.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:voxel_shape",
    )

    format_version: str = json_field(default=VOXEL_SHAPE_VERSION, init=False)
    voxel_shape: _VoxelShapeDefinition = json_field(
        key="minecraft:voxel_shape", default_factory=_VoxelShapeDefinition
    )


class _VoxelGroup:
    """A named group of boxes in a :class:`VoxelShape`.

    Do not instantiate directly: use :meth:`VoxelShape.group` for a root group or
    :meth:`_VoxelGroup.group` for a child group.
    """

    def __init__(
        self, shape: "VoxelShape", name: str, parent: "_VoxelGroup | None" = None
    ) -> None:
        if not name:
            raise ValueError("Group names cannot be empty.")
        self._shape: "VoxelShape | None" = shape
        self._parent = parent
        self._name = name
        self._items: list["_Box | _VoxelGroup"] = []

    @property
    def name(self) -> str:
        """Read-only: groups are indexed by name, so they cannot be renamed."""
        return self._name

    @property
    def parent(self) -> "_VoxelGroup | None":
        return self._parent

    @property
    def children(self) -> list["_VoxelGroup"]:
        return [item for item in self._items if isinstance(item, _VoxelGroup)]

    @property
    def boxes(self) -> list[_Box]:
        """The boxes directly in this group (not in its child groups)."""
        return [item for item in self._items if isinstance(item, _Box)]

    def _alive(self) -> "VoxelShape":
        if self._shape is None:
            raise ValueError(f"Group '{self._name}' was removed from its shape.")
        return self._shape

    def group(self, name: str) -> "_VoxelGroup":
        """Creates a child group of this group and returns the **child**."""
        shape = self._alive()
        child = _VoxelGroup(shape, name, self)
        shape._register(child)
        self._items.append(child)
        return child

    def box(self, min: Sequence[float], max: Sequence[float]) -> "_VoxelGroup":
        """Adds a box to this group. Returns this group so calls can be chained.

        Args:
            min (Sequence[float]): The corner with the smallest coordinates, in pixels from
                the block's corner.
            max (Sequence[float]): The opposite corner.
        """
        shape = self._alive()
        self._items.append(_Box(min=tuple(min), max=tuple(max)))
        shape._sync()
        return self

    def remove(self) -> None:
        """Removes this group, its boxes and all of its descendants from the shape."""
        shape = self._alive()
        siblings = self._parent._items if self._parent else shape._roots
        siblings.remove(self)
        for group in self.walk():
            shape._by_name.pop(group._name, None)
            group._shape = None
        self._parent = None
        shape._sync()

    def walk(self) -> Iterator["_VoxelGroup"]:
        """Yields this group followed by all of its descendants (depth-first)."""
        yield self
        for child in self.children:
            yield from child.walk()

    def _all_boxes(self) -> Iterator[_Box]:
        for item in self._items:
            if isinstance(item, _VoxelGroup):
                yield from item._all_boxes()
            else:
                yield item


class VoxelShape(JsonFile):
    """A voxel shape file (``<name>.shape.json``) built from a tree of groups.

    The file is named after `name`. The shape identifier is
    ``<namespace>:<identifier_name>`` and defaults to `name`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/voxelshapes)
    """

    _document = _VoxelShapeFile
    _extension = ".shape.json"
    _pack = Pack.BP
    _folder = "shapes"
    _object_type = "Voxel Shape"

    def __init__(self, name: str, identifier_name: str | None = None) -> None:
        super().__init__(name)
        self._identifier_name = identifier_name or name
        self._roots: list[_VoxelGroup] = []
        self._by_name: dict[str, _VoxelGroup] = {}
        self._content.voxel_shape.description.set_identifier(self.shape_identifier)

    @property
    def identifier_name(self) -> str:
        """The name in the shape identifier."""
        return self._identifier_name

    def _register(self, group: _VoxelGroup) -> None:
        if group._name in self._by_name:
            raise ValueError(
                f"Duplicate group '{group._name}' in voxel shape '{self.identifier.name}'. Group names must be unique."
            )
        self._by_name[group._name] = group

    def _sync(self) -> None:
        self._content.voxel_shape.shape.set_boxes(self.boxes)

    def group(self, name: str) -> _VoxelGroup:
        """Creates a root group and returns it."""
        group = _VoxelGroup(self, name)
        self._register(group)
        self._roots.append(group)
        return group

    def find(self, name: str) -> _VoxelGroup | None:
        return self._by_name.get(name)

    @property
    def groups(self) -> list[_VoxelGroup]:
        """All groups, parents always before their children."""
        return [group for root in self._roots for group in root.walk()]

    @property
    def boxes(self) -> list[_Box]:
        """Every box of the shape, in the order they were added."""
        return [box for root in self._roots for box in root._all_boxes()]

    @property
    def shape_identifier(self) -> str:
        """How a block's geometry references this shape: ``<namespace>:<identifier_name>``."""
        return f"{CONFIG.NAMESPACE}:{self._identifier_name}"
