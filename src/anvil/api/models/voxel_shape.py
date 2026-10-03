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
"""

import os
from typing import Any, Dict, Iterator, List, Optional, Sequence, Union

from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes


def _vec3(value: Sequence[float]) -> List[float]:
    values = list(value)
    if len(values) != 3:
        raise ValueError(f"Expected a vector of 3 values, got {values}.")
    return values


class _Box:
    """An axis-aligned box. Created through :meth:`_VoxelGroup.box`."""

    def __init__(self, min: Sequence[float], max: Sequence[float]) -> None:
        self.min = _vec3(min)
        self.max = _vec3(max)
        if any(lo > hi for lo, hi in zip(self.min, self.max)):
            raise ValueError(
                f"Box min {self.min} must not be greater than max {self.max} on any axis."
            )

    def compile(self) -> Dict[str, Any]:
        return {"min": self.min, "max": self.max}


class _VoxelGroup:
    """A named group of boxes in a :class:`VoxelShape`.

    Do not instantiate directly: use :meth:`VoxelShape.group` for a root group or
    :meth:`_VoxelGroup.group` for a child group.
    """

    def __init__(
        self, shape: "VoxelShape", name: str, parent: Optional["_VoxelGroup"] = None
    ) -> None:
        if not name:
            raise ValueError("Group names cannot be empty.")
        self._shape: Optional["VoxelShape"] = shape
        self._parent = parent
        self._name = name
        # Boxes and child groups, in the order they were added
        self._items: List[Union[_Box, "_VoxelGroup"]] = []

    # -- structure -----------------------------------------------------------

    @property
    def name(self) -> str:
        """Read-only: groups are indexed by name, so they cannot be renamed."""
        return self._name

    @property
    def parent(self) -> Optional["_VoxelGroup"]:
        return self._parent

    @property
    def children(self) -> List["_VoxelGroup"]:
        return [item for item in self._items if isinstance(item, _VoxelGroup)]

    @property
    def boxes(self) -> List[_Box]:
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
        """Adds a box to this group. Returns this group so calls can be chained."""
        self._alive()
        self._items.append(_Box(min, max))
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


class VoxelShape(AddonObject):
    """A voxel shape file (``<name>.shape.json``) built from a tree of groups.

    The file is named after `name`. The shape identifier is
    ``<namespace>:<identifier_name>`` and defaults to `name`.
    """

    _extension = ".shape.json"
    _path = os.path.join(CONFIG.BP_PATH, "shapes")

    def __init__(self, name: str, identifier_name: Optional[str] = None) -> None:
        super().__init__(name)
        self.identifier_name = identifier_name or name
        self._roots: List[_VoxelGroup] = []
        self._by_name: Dict[str, _VoxelGroup] = {}

    def _register(self, group: _VoxelGroup) -> None:
        if group._name in self._by_name:
            raise ValueError(
                f"Duplicate group '{group._name}' in voxel shape '{self._name}'. Group names must be unique."
            )
        self._by_name[group._name] = group

    def group(self, name: str) -> _VoxelGroup:
        """Creates a root group and returns it."""
        group = _VoxelGroup(self, name)
        self._register(group)
        self._roots.append(group)
        return group

    def find(self, name: str) -> Optional[_VoxelGroup]:
        return self._by_name.get(name)

    @property
    def groups(self) -> List[_VoxelGroup]:
        """All groups, parents always before their children."""
        return [group for root in self._roots for group in root.walk()]

    @property
    def boxes(self) -> List[_Box]:
        """Every box of the shape, in the order they were added."""
        return [box for root in self._roots for box in root._all_boxes()]

    @property
    def shape_identifier(self) -> str:
        """How a block's geometry references this shape: ``<namespace>:<identifier_name>``."""
        return f"{CONFIG.NAMESPACE}:{self.identifier_name}"

    def compile(self) -> dict:
        boxes = self.boxes
        if not boxes:
            raise ValueError(f"Voxel shape '{self._name}' has no boxes.")
        content = JsonSchemes.voxel_shape(self.identifier_name)
        content["minecraft:voxel_shape"]["shape"]["boxes"] = [
            box.compile() for box in boxes
        ]
        return content

    def __export__(self) -> None:
        self.content(self.compile())
        super().__export__()
