"""A complete wood set from one call: `create_wood_set("rotten")`.

    create_wood_set("rotten")                                    # everything
    create_wood_set("rotten", WoodBlock.PLANKS | WoodBlock.SLAB)  # only these
    create_wood_set("rotten", WoodBlock.ALL & ~WoodBlock.DOOR)    # everything but these
    create_wood_set("rotten", own_creative_group=True)           # in a "Rotten Wood" group

Every block and boat is its own file in `blocks/`: its `create(wood, selected)` builds it,
names it, queues it and registers the recipes that make it. The custom components the
blocks share their scripts through are in `components.py`. The TypeScript the
blocks use is then written to `scripts/javascript/blocks/wood_set`; register it from
`main.ts` with `registerWoodSet(init)`. The signs' script uses `@minecraft/server-ui`,
so it needs `scriptui` enabled in `anvilconfig.json`.

Expected textures: `<name>_planks`, `<name>_log`, `<name>_log_top`, `<name>_log_stripped`,
`<name>_log_stripped_top`, `<name>_door_bottom`, `<name>_door_top`, `<name>_trapdoor`,
`<name>_hanging_sign`, the item icons `<name>_sign`, `<name>_hanging_sign`, `<name>_boat`
and `<name>_chest_boat` in `assets/textures/items/`, and two blockbench models:

- `<name>_planks`: the block collections. `hanging_sign` has a `top_bit` bone (on a
  wall) and a `top_chain` bone (under a block).
- `<name>_boat`: both boats, facing north, with a `chest` bone and the `paddle`,
  `paddle_left`, `paddle_right` and `shake` animations.
"""

from enum import Flag, auto

from anvil.api.actors.actors import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.core.enums import ItemCategory
from anvil.api.items.crafting import CraftingItemCatalog
from anvil.api.items.items import Item

from .blocks import (
    boat,
    button,
    chest_boat,
    door,
    fence,
    fence_gate,
    hanging_sign,
    log,
    log_stripped,
    planks,
    pressure_plate,
    slab,
    stairs,
    standing_sign,
    trapdoor,
    wall_sign,
    wood,
    wood_stripped,
)
from .typescript import generate_typescript

__all__ = ["WoodBlock", "create_wood_set"]


class WoodBlock(Flag):
    """The blocks a wood set can contain. Combine them with `|` and remove them with `& ~`."""

    PLANKS = auto()
    BUTTON = auto()
    PRESSURE_PLATE = auto()
    FENCE = auto()
    FENCE_GATE = auto()
    STAIRS = auto()
    DOOR = auto()
    TRAPDOOR = auto()
    SLAB = auto()
    LOG = auto()
    LOG_STRIPPED = auto()
    WOOD = auto()
    WOOD_STRIPPED = auto()
    WALL_SIGN = auto()
    STANDING_SIGN = auto()
    HANGING_SIGN = auto()
    BOAT = auto()
    CHEST_BOAT = auto()

    ALL = (
        PLANKS
        | BUTTON
        | PRESSURE_PLATE
        | FENCE
        | FENCE_GATE
        | STAIRS
        | DOOR
        | TRAPDOOR
        | SLAB
        | LOG
        | LOG_STRIPPED
        | WOOD
        | WOOD_STRIPPED
        | WALL_SIGN
        | STANDING_SIGN
        | HANGING_SIGN
        | BOAT
        | CHEST_BOAT
    )


BLOCKS = {
    WoodBlock.PLANKS: planks.create,
    WoodBlock.BUTTON: button.create,
    WoodBlock.PRESSURE_PLATE: pressure_plate.create,
    WoodBlock.FENCE: fence.create,
    WoodBlock.FENCE_GATE: fence_gate.create,
    WoodBlock.STAIRS: stairs.create,
    WoodBlock.DOOR: door.create,
    WoodBlock.TRAPDOOR: trapdoor.create,
    WoodBlock.SLAB: slab.create,
    WoodBlock.LOG: log.create,
    WoodBlock.LOG_STRIPPED: log_stripped.create,
    WoodBlock.WOOD: wood.create,
    WoodBlock.WOOD_STRIPPED: wood_stripped.create,
    WoodBlock.WALL_SIGN: wall_sign.create,
    WoodBlock.STANDING_SIGN: standing_sign.create,
    WoodBlock.HANGING_SIGN: hanging_sign.create,
    WoodBlock.BOAT: boat.create,
    WoodBlock.CHEST_BOAT: chest_boat.create,
}


def create_wood_set(
    name: str,
    blocks: WoodBlock = WoodBlock.ALL,
    *,
    own_creative_group: bool = False,
) -> None:
    """Create the selected `blocks` of the `name` wood set.

    In the creative inventory each block sits next to its vanilla counterparts, or with
    `own_creative_group`, all of them in one "<Name> Wood" group under Construction.
    """
    # Block names like "log_stripped", so each block knows what else is in the set
    selected = {kind.name.lower() for kind in BLOCKS if kind in blocks}

    # Boats return their entity and item
    created = []
    for kind, create in BLOCKS.items():
        if kind in blocks:
            made = create(name, selected)
            created.extend(made if isinstance(made, tuple) else [made])

    if own_creative_group and created:
        _add_creative_group(name, created)

    generate_typescript(created)


def _add_creative_group(name: str, created: list[Block | Entity | Item]) -> None:
    """Move the items out of their vanilla groups into a group of their own."""
    items = [made.item if isinstance(made, Block) else made for made in created]
    items = [item for item in items if isinstance(item, Item)]
    # The first block is the planks when selected, which makes the group's icon
    CraftingItemCatalog().add_group(
        ItemCategory.Construction,
        f"{name.replace('_', ' ').title()} Wood",
        items[0],
        items,
    ).queue()
