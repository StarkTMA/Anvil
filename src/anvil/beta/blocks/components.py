"""Experimental block components. They need `features.experimental` in anvilconfig.json."""

from typing import TYPE_CHECKING, Annotated, Any, Literal

from anvil.api.blocks.components import (
    BlockCollisionBox,
)
from anvil.api.blocks.components import BlockEntity as _BlockEntity
from anvil.api.blocks.components import ItemSpecificSpeed, ItemTagFilter, _Switchable
from anvil.api.items.items import Item
from anvil.api.models.voxel_shape import VoxelShape
from anvil.lib.blockbench import _Blockbench, _BlockBenchSource
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import (
    InRange,
    JsonComponent,
    JsonObject,
    JsonValueComponent,
    Length,
    json_field,
)
from anvil.lib.translator import AnvilTranslator

if TYPE_CHECKING:
    from anvil.api.blocks.server import BlockServer

__all__ = [
    "BlockCollisionBoxMinMax",
    "BlockEnchantmentPowerTransmitter",
    "BlockEntity",
    "BlockEntityContainer",
    "BlockMinMaxBox",
    "BlockNeighborChange",
    "BlockVibrationProperties",
]


def _require_experimental(component: str) -> None:
    if not CONFIG._EXPERIMENTAL:
        raise ValueError(
            f"{component} is experimental: turn on features.experimental in anvilconfig.json."
        )


class BlockMinMaxBox(JsonObject):
    """A box inside the block, in pixels, by its two corners. (0, 0, 0) is the bottom-left
    corner of the block and (16, 16, 16) the top-right.

    Args:
        min (tuple[float, float, float]): The minimal corner.
        max (tuple[float, float, float]): The maximal corner.
    """

    min: tuple[float, float, float] = json_field()
    max: tuple[float, float, float] = json_field()


class BlockEntityContainer(JsonObject):
    """The inventory of a block entity.

    Args:
        slot_count (int): The number of slots, from 1 to 54.
        show_ui_on_interaction (bool, optional): Determines whether interacting with this block opens its container UI. Defaults to true. When false, normal block interaction events can run instead.
        title (str, optional): The title shown on the container, 1 to 256 characters. Anvil adds it to the language file under a key made from the block identifier. Leaving it out leaves the heading blank.
    """

    slot_count: Annotated[int, InRange(1, 54)] = json_field()
    show_ui_on_interaction: bool | None = json_field(default=None)
    title: Annotated[str, Length(1, 256)] | None = json_field(default=None)


class BlockCollisionBoxMinMax(JsonComponent):
    """[EXPERIMENTAL] The area of the block that collides with entities, as boxes given by their two corners.
    It writes `minecraft:collision_box` like `BlockCollisionBox`, and clashes with it: a block
    cannot use both, in its components or in a permutation.
    Experimental: needs `features.experimental` in anvilconfig.json.

    Args:
        min (tuple[float, float, float], optional): The minimal corner of the box, in pixels from the bottom-left corner of the block.
        max (tuple[float, float, float], optional): The maximal corner of the box. Boxes must stay within (0, 0, 0) and (16, 24, 16).

    Give either `min` and `max`, or a voxel shape with `set_voxel_shape`. Add more boxes with
    `add_box`, up to 32. Boxes are always written as a list.
    """

    identifier = "minecraft:collision_box"
    _clashes = (BlockCollisionBox,)

    min: tuple[float, float, float] | None = json_field(default=None)
    max: tuple[float, float, float] | None = json_field(default=None)
    _voxel_shape: str | None = json_field(default=None, init=False, exclude=True)
    _boxes: list[BlockMinMaxBox] = json_field(
        default_factory=list, init=False, exclude=True
    )

    def add_box(
        self, *, min: tuple[float, float, float], max: tuple[float, float, float]
    ) -> "BlockCollisionBoxMinMax":
        """Adds another collision box, for more complex shapes.

        Args:
            min (tuple[float, float, float]): The minimal corner of the box.
            max (tuple[float, float, float]): The maximal corner of the box.
        """
        self._boxes.append(BlockMinMaxBox(min=min, max=max))
        return self

    def set_voxel_shape(
        self,
        voxel_shape: VoxelShape | None = None,
        *,
        blockbench: str | None = None,
        collection: str | None = None,
    ) -> "BlockCollisionBoxMinMax":
        """Uses a voxel shape as the collision shape instead of boxes.

        Example:
            >>> BlockCollisionBoxMinMax().set_voxel_shape(blockbench="lantern")

        Args:
            voxel_shape (VoxelShape, optional): A voxel shape built in code, queued for export.
            blockbench (str, optional): The Blockbench model whose bounding boxes build the shape, the same shape `block_culling(culling_shape="custom")` uses.
            collection (str, optional): The collection of the Blockbench model to build the shape from.

        Give either `voxel_shape` or `blockbench`.
        """
        if (voxel_shape is None) == (blockbench is None):
            raise ValueError(
                "BlockCollisionBoxMinMax.set_voxel_shape takes either voxel_shape or blockbench."
            )
        if blockbench is not None:
            model = _Blockbench(blockbench, _BlockBenchSource.BLOCK)
            voxel_shape = model.model.queue_voxel_shape(collection)
        elif collection is not None:
            raise ValueError(
                "BlockCollisionBoxMinMax.set_voxel_shape: collection only applies to Blockbench models."
            )
        else:
            voxel_shape.queue()
        self._voxel_shape = voxel_shape.shape_identifier
        return self

    def __validate__(self) -> None:
        _require_experimental("BlockCollisionBoxMinMax")
        has_box = self.min is not None or self.max is not None
        if self._voxel_shape is not None:
            if has_box or self._boxes:
                raise ValueError(
                    "BlockCollisionBoxMinMax takes either boxes or a voxel shape, not both."
                )
            return
        if self.min is None or self.max is None:
            raise ValueError(
                "BlockCollisionBoxMinMax needs both min and max, or a voxel shape."
            )
        boxes = [(self.min, self.max), *((box.min, box.max) for box in self._boxes)]
        if len(boxes) > 32:
            raise ValueError(
                f"BlockCollisionBoxMinMax takes at most 32 boxes, got {len(boxes)}."
            )
        high = (16, 24, 16)
        for low_corner, high_corner in boxes:
            if any(lo > hi for lo, hi in zip(low_corner, high_corner)):
                raise ValueError(
                    f"BlockCollisionBoxMinMax: min {tuple(low_corner)} must not be above "
                    f"max {tuple(high_corner)}."
                )
            if any(v < 0 for v in low_corner) or any(
                v > limit for v, limit in zip(high_corner, high)
            ):
                raise ValueError(
                    f"BlockCollisionBoxMinMax: the box from {tuple(low_corner)} to "
                    f"{tuple(high_corner)} must stay within (0, 0, 0) and {high}."
                )

    def __json__(self) -> Any:
        box = JsonObject.__json__(self)
        if self._voxel_shape is not None:
            return {self.identifier: self._voxel_shape}
        return {self.identifier: [box, *(extra.__json__() for extra in self._boxes)]}


class BlockEnchantmentPowerTransmitter(JsonValueComponent):
    """[EXPERIMENTAL] Whether the block transmits enchantment power. When true and the block sits
    in the 1 block gap between an enchanting table and a bookshelf, the table stays powered by
    the bookshelf.
    Experimental: needs `features.experimental` in anvilconfig.json.

    Args:
        value (bool, optional): Whether the block transmits enchantment power. Defaults to True.
    """

    identifier = "minecraft:enchantment_power_transmitter"

    value: bool = json_field(default=True)

    def __validate__(self) -> None:
        _require_experimental("BlockEnchantmentPowerTransmitter")


class BlockEntity(_BlockEntity):
    """[EXPERIMENTAL] Gives each placed block its own data, with an inventory and entity storage.
    It writes `minecraft:block_entity` like the public `BlockEntity`, which only has
    `dynamic_properties`. Experimental: needs `features.experimental` in anvilconfig.json.

    Args:
        container (BlockEntityContainer, optional): An inventory. Set it with `set_container`.
        dynamic_properties (bool, optional): Whether scripts can store dynamic properties on the block. Game default false.
        entity_storage (bool, optional): Whether scripts can store serialized entities in the block. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_block_entity)
    """

    container: BlockEntityContainer | None = json_field(default=None)
    entity_storage: bool | None = json_field(default=None)

    def set_container(
        self,
        *,
        slot_count: int,
        title: str | None = None,
        show_ui_on_interaction: bool | None = None,
    ) -> "BlockEntity":
        """Gives the block an inventory.

        Args:
            slot_count (int): The number of slots, from 1 to 54.
            title (str, optional): The title shown on the container, 1 to 256 characters. Anvil adds it to the language file under a key made from the block identifier. Leaving it out leaves the heading blank.
            show_ui_on_interaction (bool, optional): Whether interacting with the block opens its container UI. When false, normal block interaction events run instead. Game default true.
        """
        self.container = BlockEntityContainer(
            slot_count=slot_count,
            title=title,
            show_ui_on_interaction=show_ui_on_interaction,
        )
        return self

    def __validate__(self) -> None:
        _require_experimental("BlockEntity")

    def __prepare_export__(self, owner: "BlockServer", *, root: bool = True) -> None:
        """Adds the container title to the language file under
        `tile.<identifier>.container_title` for the root, and
        `tile.<identifier>.<name>.container_title` for a permutation, then writes the key.
        """
        if self.container is None or self.container.title is None:
            return
        prefix = f"tile.{owner.identifier}"
        if self.container.title.startswith(f"{prefix}."):
            return
        if root:
            key = f"{prefix}.container_title"
            AnvilTranslator().add_localization_entry(key, self.container.title)
        else:
            key = AnvilTranslator().localize(
                self.container.title, prefix=prefix, suffix="container_title"
            )
        self.container = BlockEntityContainer(
            slot_count=self.container.slot_count,
            title=key,
            show_ui_on_interaction=self.container.show_ui_on_interaction,
        )


class BlockVibrationProperties(JsonComponent):
    """[EXPERIMENTAL] How the block affects vibrations.
    Experimental: needs `features.experimental` in anvilconfig.json.

    Args:
        dampen_vibrations (bool, optional): Whether the block dampens vibrations. The game defaults to False.
        occlude_vibrations (bool, optional): Whether the block occludes vibrations. The game defaults to False.
    """

    identifier = "minecraft:vibration_properties"

    dampen_vibrations: bool | None = json_field(default=None)
    occlude_vibrations: bool | None = json_field(default=None)

    def __validate__(self) -> None:
        _require_experimental("BlockVibrationProperties")


class BlockNeighborChange(JsonComponent):
    """[EXPERIMENTAL] Which neighbouring block changes trigger the neighbor change after event of
    the block's custom components.
    Experimental: needs `features.experimental` in anvilconfig.json.

    Args:
        neighbor_directions (list["all" | "up" | "down" | "north" | "south" | "west" | "east"]): The directions to observe, 1 to 6 of them, no repeats. "all" must be used alone.
    """

    identifier = "minecraft:neighbor_change"

    neighbor_directions: Annotated[
        list[Literal["all", "up", "down", "north", "south", "west", "east"]],
        Length(1, 6),
    ] = json_field()

    def __validate__(self) -> None:
        _require_experimental("BlockNeighborChange")
        directions = self.neighbor_directions
        if len(set(directions)) != len(directions):
            raise ValueError(
                f"BlockNeighborChange: neighbor_directions {directions} repeats a direction."
            )
        if "all" in directions and len(directions) > 1:
            raise ValueError(
                "BlockNeighborChange: 'all' must be used alone in neighbor_directions."
            )


class BlockJukeBoxPlaylistSource(JsonComponent):
    """[EXPERIMENTAL] Allows a jukebox directly below this block to use its existing container
    as a playlist source. This component is an empty object. It does not create a container
    and has no effect without one.

    Experimental: needs `features.experimental` in anvilconfig.json.

    """

    identifier = "minecraft:jukebox_playlist_source"

    def __validate__(self) -> None:
        _require_experimental("BlockJukeBoxPlaylistSource")


class BlockDestructibleByMining(_Switchable):
    """Describes how long the block takes to mine.

    Args:
        base_time_to_destroy (int, optional): Sets the number of server simulation ticks it takes to mine the block with base equipment. Greater numbers result in greater mining times. A negative number means the block can't be mined.
        item_specific_speeds (list[ItemSpecificSpeed], optional): The seconds to mine it with specific items. Set them directly or add them with `add_item_specific_speed`.
        enabled (bool, optional): False makes the block indestructible by mining, written as `false`. Defaults to True.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockcomponents/minecraftblock_destructible_by_mining)
    """

    identifier = "minecraft:destructible_by_mining"

    base_time_to_destroy: int | None = json_field(default=None)
    item_specific_speeds: list[ItemSpecificSpeed] = json_field(
        default_factory=list, omit_default=True
    )

    def add_item_specific_speed(
        self,
        *,
        item: str | Item | ItemTagFilter,
        destroy_speed: float,
    ) -> "BlockDestructibleByMining":
        """Adds the seconds to mine the block with an item, or items with tags.

        Example:
            >>> mining.add_item_specific_speed(
            ...     item=ItemTagFilter(tags=Query.AllTags(["minecraft:is_axe"])), destroy_speed=1.5
            ... )
        """
        self.item_specific_speeds.append(
            ItemSpecificSpeed(item=item, destroy_speed=destroy_speed)
        )
        return self
