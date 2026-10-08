"""A complete wood set from one call: `create_wood_set("rotten")`.

    WoodSet("rotten").tree(my_tree).leaf_drop(coconut, 0.02).build()   # tree and drops
    WoodSet("rotten", [WoodBlock.DOOR, WoodBlock.BOAT]).tree(my_tree).build()   # all but these
    WoodSet("rotten", WoodBlock.SAPLING | WoodBlock.DOOR).build()      # no saplings: no tree
    create_wood_set("rotten", tree=my_tree)                            # a one-call shortcut

Every block and boat is its own file in `blocks/`: its `create(wood, selected)` builds it,
names it, queues it and registers the recipes that make it. The custom components the
blocks share their scripts through are in `components.py`. The TypeScript the
blocks use is then written to `scripts/javascript/blocks/wood_set`; register it from
`main.ts` with `registerWoodSet(init)`. The signs' script uses `@minecraft/server-ui`,
so it needs `scriptui` enabled in `anvilconfig.json`.

Expected textures: `<name>_planks`, `<name>_log`, `<name>_log_top`, `<name>_log_stripped`,
`<name>_log_stripped_top`, `<name>_door_bottom`, `<name>_door_top`, `<name>_trapdoor`,
`<name>_hanging_sign`, `<name>_standing_sign`, `<name>_boat`, `<name>_leaves`,
`<name>_sapling`, and the item icons `<name>_sign`,
`<name>_hanging_sign`, `<name>_boat` and `<name>_chest_boat` in `assets/textures/items/`.

Every wood set shares the same two blockbench models, so only the names differ between
sets. Each model holds the textures of every set, named as above:

- `wood_set` (`assets/bbmodels/wood_set.bbmodel`): the block collections. `hanging_sign`
  has a `top_bit` bone (on a wall) and a `top_chain` bone (under a block).
  It also needs a `sapling` collection (a crossed pair of planes) for the saplings.
- `wood_set_boat` (`assets/bbmodels/wood_set_boat.bbmodel`): both boats, facing north,
  with a `chest` bone and the `paddle`, `paddle_left`, `paddle_right` and `shake`
  animations.

Their names are `MODEL` and `BOAT_MODEL` in `blocks/__init__.py`. When one is missing
from `assets/bbmodels`, building a set offers to copy Anvil's base model there (the files in
`models/`), and never overwrites an existing one.

Leaves and saplings: a leaves block's `natural` state is off for leaves a player placed,
which stay forever. Whatever generates leaves sets it on, and they then decay when no log of
the set is within `leaf_distance` blocks through leaves. A sapling grows into the `tree`
feature, which `/place feature` builds at its position. See docs/kit for the details.
"""

import shutil
import sys
from enum import Flag, auto
from pathlib import Path
from typing import Callable, Iterable, NamedTuple

from anvil.api.actors.actors import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.core.enums import ItemCategory
from anvil.api.core.types import Identifier
from anvil.api.features import Feature
from anvil.api.items.crafting import CraftingItemCatalog
from anvil.api.items.items import Item

from .blocks import (
    BOAT_MODEL,
    MODEL,
    boat,
    button,
    chest_boat,
    door,
    fence,
    fence_gate,
    hanging_sign,
    leaves,
    log,
    log_stripped,
    planks,
    pressure_plate,
    sapling,
    sign,
    slab,
    stairs,
    trapdoor,
    wood,
    wood_stripped,
)
from .blocks.leaves import LeafDrop
from .typescript import generate_typescript

__all__ = [
    "LeafDrop",
    "WoodBlock",
    "WoodSet",
    "WoodSetPart",
    "create_wood_set",
]


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
    SIGN = auto()
    HANGING_SIGN = auto()
    BOAT = auto()
    CHEST_BOAT = auto()
    LEAVES = auto()
    SAPLING = auto()

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
        | SIGN
        | HANGING_SIGN
        | BOAT
        | CHEST_BOAT
        | LEAVES
        | SAPLING
    )


class WoodSetPart(NamedTuple):
    """A part of a wood set: what it places and the item that places it."""

    block: Block | Entity
    """The block, or the entity for boats and chest boats."""
    item: Item
    """The item in the inventory. For a block it is `block.item`."""


class WoodSet(dict[str, WoodSetPart]):
    """A wood set: configure it, then `build()` it. Once built it maps each part's name (the
    lowercase `WoodBlock` member, like "planks") to its `WoodSetPart`, and a part left out
    with `exclude` is missing.

        palm = (
            WoodSet("palm", exclude=WoodBlock.CHEST_BOAT)
            .tree(lambda wood: make_palm(wood["log"].block, wood["leaves"].block))
            .leaf_drop(coconut, 0.02)
            .build()
        )
        block, item = palm["planks"]

    The methods that configure the set return it, so they chain; all of them must come
    before `build()`.
    """

    def __init__(
        self,
        name: str,
        exclude: WoodBlock | Iterable[WoodBlock] = (),
        *,
        own_creative_group: bool = False,
    ) -> None:
        """
        Parameters:
            name (str): The name of the wood, which prefixes every block.
            exclude (WoodBlock | Iterable[WoodBlock]): The parts to leave out. Blocks that depend
                on an excluded one lose that part (a sign without planks has no recipe).
            own_creative_group (bool): Put the whole set in one "<Name> Wood" group under
                Construction, instead of next to the vanilla counterparts of each block.
        """
        super().__init__()
        self.name = name
        self.own_creative_group = own_creative_group
        self._tree = None
        self.tree_feature: Feature | Identifier | None = None
        """The feature the saplings grow into, once the set is built."""
        self._drops: list[LeafDrop] = []
        self._leaf_distance = 4
        self._soil = list(sapling.DEFAULT_SOIL)
        self._built = False

        # `exclude` is one WoodBlock (they combine with `|`) or a list of them
        excluded = WoodBlock(0)
        for kind in [exclude] if isinstance(exclude, WoodBlock) else exclude:
            excluded |= kind
        self.blocks = WoodBlock.ALL & ~excluded

    def tree(
        self, tree: Feature | Identifier | Callable[["WoodSet"], Feature | Identifier]
    ) -> "WoodSet":
        """Sets the feature the saplings grow into: a `Feature`, its identifier, or a function
        that builds it from the set once its blocks exist (so the tree can use them). The
        caller queues the feature. It is required unless `WoodBlock.SAPLING` is excluded.
        """
        self._tree = tree
        return self

    def leaf_drop(
        self, item: Item | Identifier, chance: float, count: int | tuple[int, int] = 1
    ) -> "WoodSet":
        """Adds an item the leaves drop by chance, like the apple of oak (`LeafDrop`)."""
        self._drops.append(LeafDrop(item, chance, count))
        return self

    def sapling_on(self, blocks: Iterable[Identifier | object]) -> "WoodSet":
        """Sets the blocks the sapling can be planted on (by default dirt, grass, sand...).
        Accepts identifiers and block descriptors like `MinecraftBlockTypes.Sand()`."""
        self._soil = [str(block) for block in blocks]
        return self

    def leaf_distance(self, blocks: int) -> "WoodSet":
        """Sets how far a log can be from the leaves holding on to it (4 like vanilla), going
        through leaves. Set it to the distance of the farthest leaf of your trees."""
        self._leaf_distance = blocks
        return self

    def build(self) -> "WoodSet":
        """Creates and queues every block, and writes their scripts. Returns the set."""
        if self._built:
            return self
        if WoodBlock.SAPLING in self.blocks and self._tree is None:
            raise ValueError(
                f"The '{self.name}' wood set has saplings, so it needs the feature they grow "
                "into: call `.tree(...)`, or exclude WoodBlock.SAPLING."
            )

        _offer_base_models()

        # Block names like "log_stripped", so each block knows what else is in the set
        selected = {kind.name.lower() for kind in BLOCKS if kind in self.blocks}

        # What the blocks that need more than their name are given. The sapling comes last
        # in `BLOCKS`: the tree it grows can then be built from the other blocks.
        extra_arguments = {
            WoodBlock.LEAVES: lambda: (self._drops, self._leaf_distance),
            WoodBlock.SAPLING: lambda: (self._resolve_tree(), self._soil),
        }
        for kind, create in BLOCKS.items():
            if kind in self.blocks:
                arguments = extra_arguments.get(kind, lambda: ())()
                self._add_part(kind, create(self.name, selected, *arguments))

        if self.own_creative_group and self:
            _add_creative_group(self.name, [part.item for part in self.values()])
        generate_typescript([part.block for part in self.values()])
        self._built = True
        return self

    def _resolve_tree(self) -> Feature | Identifier:
        """The tree feature, built now if it was given as a function."""
        self.tree_feature = self._tree(self) if callable(self._tree) else self._tree
        return self.tree_feature

    def _add_part(self, kind: WoodBlock, made: Block | tuple[Entity, Item]) -> None:
        """Stores what a `create` function made under the part's name: a block (its item is
        `block.item`), or an (entity, item) pair for boats."""
        block, item = made if isinstance(made, tuple) else (made, made.item)
        self[kind.name.lower()] = WoodSetPart(block, item)


# The base models shipped with Anvil, which `_offer_base_models` copies on request
BASE_MODELS = Path(__file__).parent / "models"

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
    WoodBlock.SIGN: sign.create,
    WoodBlock.HANGING_SIGN: hanging_sign.create,
    WoodBlock.BOAT: boat.create,
    WoodBlock.CHEST_BOAT: chest_boat.create,
    WoodBlock.LEAVES: leaves.create,
    WoodBlock.SAPLING: sapling.create,
}


def create_wood_set(
    name: str,
    exclude: WoodBlock | Iterable[WoodBlock] = (),
    *,
    tree: (
        Feature | Identifier | Callable[[WoodSet], Feature | Identifier] | None
    ) = None,
    leaf_drops: Iterable[LeafDrop] = (),
    own_creative_group: bool = False,
) -> WoodSet:
    """Create every block of the `name` wood set except `exclude`, in one call.

    A shortcut for `WoodSet(name, exclude, ...)` with its `tree` and `leaf_drops`, built right
    away. Use the `WoodSet` class to add leaf drops step by step.

        block, item = create_wood_set("rotten", tree=my_tree)["planks"]
    """
    wood = WoodSet(name, exclude, own_creative_group=own_creative_group)
    if tree is not None:
        wood.tree(tree)
    for drop in leaf_drops:
        wood.leaf_drop(drop.item, drop.chance, drop.count)
    return wood.build()


def _offer_base_models() -> None:
    """Offers to copy the base Blockbench models into the project when they aren't there.

    Nothing is ever overwritten: a model that exists is the user's. Without a terminal to
    ask on, nothing is copied and the missing model is reported when the blocks load it.
    """
    models = Path("assets") / "bbmodels"
    missing = [
        name for name in (MODEL, BOAT_MODEL) if not (models / f"{name}.bbmodel").exists()
    ]
    if not missing or not sys.stdin.isatty():
        return

    files = " and ".join(f"{name}.bbmodel" for name in missing)
    answer = input(f"Wood sets need {files} in {models}. Copy the base to work with? [Y/n] ")
    if answer.strip().lower() in ("", "y", "yes"):
        models.mkdir(parents=True, exist_ok=True)
        for name in missing:
            shutil.copy(BASE_MODELS / f"{name}.bbmodel", models)


def _add_creative_group(name: str, items: list[Item]) -> None:
    """Move the items out of their vanilla groups into a group of their own."""
    # The first item is the planks when selected, which makes the group's icon
    CraftingItemCatalog().add_group(
        ItemCategory.Construction,
        f"{name.replace('_', ' ').title()} Wood",
        items[0],
        items,
    ).queue()
