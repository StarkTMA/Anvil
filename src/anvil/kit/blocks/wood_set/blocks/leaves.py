from dataclasses import dataclass
from typing import Sequence

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockFlammable,
    BlockGeometry,
    BlockLightDampening,
    BlockLootTable,
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockTagComponent,
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockMaterial,
    BlockMovementType,
    ItemCategory,
    ItemGroups,
)
from anvil.api.core.types import Identifier
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemCompostable,
    ItemDisplayName,
    ItemTags,
)
from anvil.api.items.items import Item
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.api.world.loot_tables import LootTable

from ..components import BlockWoodSetLeaves
from . import MODEL


@dataclass(frozen=True)
class LeafDrop:
    """An extra item leaves drop, like the apple of oak leaves.

    It drops by chance when the leaves are broken without shears or silk touch, and when they
    decay: the same loot table serves both. `item` can be an `Item` or an identifier (a
    vanilla item like `minecraft:apple`).
    """

    item: Item | Identifier
    chance: float
    """The chance of the drop, from 0 to 1: `0.005` for the apple's 0.5%."""
    count: int | tuple[int, int] = 1
    """How many drop, or the range they are picked from."""

    def __post_init__(self) -> None:
        if not 0 <= self.chance <= 1:
            raise ValueError(
                f"A leaf drop's chance must be between 0 and 1, not {self.chance}."
            )
        if isinstance(self.count, tuple) and not 0 < self.count[0] <= self.count[1]:
            raise ValueError(f"A leaf drop's count range is invalid: {self.count}.")

    @property
    def identifier(self) -> Identifier:
        return self.item.identifier if isinstance(self.item, Item) else self.item


# Blocks that hold natural leaves up, from the kit's own blocks
TRUNKS = ("log", "log_stripped", "wood", "wood_stripped")


def create(
    wood: str,
    selected: set[str],
    drops: Sequence[LeafDrop] = (),
    distance: int = 4,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_leaves")
    display_name = f"{wood.replace('_', ' ').title()} Leaves"

    # Off for leaves a player placed, which never decay. Whatever generates leaves (a feature,
    # a jigsaw structure, a script) turns it on: only those leaves decay without a trunk.
    block.server.description.add_state("natural", (False, True))

    # The loot table defines leaf drops with conditions:
    # - Breaking with shears or silk touch drops the leaves block itself
    # - Breaking without shears/silk touch (or decaying) drops saplings or sticks by chance
    loot = LootTable(f"{wood}_leaves")

    shears_pool = loot.pool()
    shears_pool.conditions.match_tool(item="minecraft:shears")
    shears_pool.entry(f"{namespace}:{wood}_leaves")

    silk_pool = loot.pool()
    silk_pool.conditions.match_tool(enchantments="silk_touch")
    silk_pool.entry(f"{namespace}:{wood}_leaves")

    if "sapling" in selected:
        sapling_pool = loot.pool()
        sapling_pool.conditions.random_chance(0.05)
        sapling_pool.entry(f"{namespace}:{wood}_sapling")

    stick_pool = loot.pool()
    stick_pool.conditions.random_chance(0.02)
    stick_entry = stick_pool.entry("minecraft:stick")
    stick_entry.functions.SetCount((1, 2))

    for drop in drops:
        pool = loot.pool()
        pool.conditions.random_chance(drop.chance)
        entry = pool.entry(drop.identifier)
        if drop.count != 1:
            entry.functions.SetCount(drop.count)

    loot.queue()

    trunks = [f"{namespace}:{wood}_{trunk}" for trunk in TRUNKS if trunk in selected]
    sapling = f"{namespace}:{wood}_sapling" if "sapling" in selected else None

    block.server.components.add(
        BlockDisplayName(display_name),
        BlockDestructibleByMining(0.2),
        BlockGeometry(),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_leaves")],
                params=MaterialParams(
                    render_method=BlockMaterial.AlphaTestSingleSidedToOpaque
                ),
            )
        ),
        BlockCollisionBox((16, 16, 16), (-8, 0, -8)),
        BlockSelectionBox((16, 16, 16), (-8, 0, -8)),
        BlockMovable(BlockMovementType.PushPull),
        BlockFlammable(60, 30),
        BlockMapColor("#19381F"),
        BlockLightDampening(1),
        BlockTagComponent(
            [MinecraftBlockTags.Leaves, MinecraftBlockTags.IsShearsItemDestructible]
        ),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(0.2),
        BlockRedstoneConductivity(False, False),
        BlockLootTable(loot),
        BlockWoodSetLeaves(trunks, sapling, distance),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        # Vanilla recipes take leaves by this tag, like smelting them into leaf litter
        ItemTags([MinecraftItemTags.Leaves]),
        ItemCompostable(30),
    )
    block.item.server.description.menu_category(ItemCategory.Nature, ItemGroups.Leaves)

    block.queue()
    return block
