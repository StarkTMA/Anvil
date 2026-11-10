from collections.abc import Sequence
from dataclasses import dataclass

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
    BlockLiquidDetection,
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
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
    ItemCategory,
    ItemGroups,
)
from anvil.lib.jsonmodel.types import Color

from ..components import BlockWoodSetLeaves
from . import MAP_COLOR, MODEL


@dataclass(frozen=True)
class LeafDrop:
    """An extra item leaves drop, like the apple of oak leaves.

    It drops by chance when the leaves are broken without shears or silk touch, and when they
    decay: the same loot table serves both. `item` can be an `Item` or an identifier (a
    vanilla item like `minecraft:apple`).
    """

    item: Item | str
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
    def identifier(self) -> str:
        return self.item.identifier if isinstance(self.item, Item) else self.item


TRUNKS = ("log", "log_stripped", "wood", "wood_stripped")


def create(
    wood: str,
    selected: set[str],
    drops: Sequence[LeafDrop] = (),
    distance: int = 4,
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Grass,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_leaves")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Leaves"

    block.server.description.add_state("natural", (False, True))

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
        BlockDisplayName(value=display_name),
        BlockDestructibleByMining(seconds_to_destroy=0.2),
        BlockGeometry(),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_leaves")],
                params=MaterialParams(
                    render_method=BlockMaterial.AlphaTestSingleSidedToOpaque
                ),
            )
        ),
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockMovable(movement_type="push_pull"),
        BlockFlammable(catch_chance_modifier=60, destroy_chance_modifier=30),
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
        ),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=1),
        BlockTagComponent(
            value=[
                MinecraftBlockTags.Leaves,
                MinecraftBlockTags.IsShearsItemDestructible,
            ]
        ),
        BlockConnectionRule(accepts_connections_from="none"),
        BlockDestructibleByExplosion(explosion_resistance=0.2),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=False, redstone_conductor=False
        ),
        BlockLootTable(value=loot),
        BlockWoodSetLeaves(trunks=trunks, sapling=sapling, distance=distance),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemTags(tags=[MinecraftItemTags.Leaves]),
        ItemCompostable(composting_chance=30),
    )
    block.item.server.description.set_menu_category(
        ItemCategory.Nature, ItemGroups.Leaves
    )

    block.queue()
    return block
