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
    BlockPlacementFilter,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockMaterial,
    ItemCategory,
    ItemGroups,
)
from anvil.api.core.types import Identifier
from anvil.api.features import Feature
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemIcon
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.world.loot_tables import LootTable

from ..components import BlockWoodSetSapling, BlockWoodSetSupport, SupportedBy
from . import MODEL

# What a sapling can be planted on, unless the set says otherwise
DEFAULT_SOIL = (
    "minecraft:dirt",
    "minecraft:grass_block",
    "minecraft:coarse_dirt",
    "minecraft:sand",
    "minecraft:red_sand",
)


def create(
    wood: str,
    selected: set[str],
    tree: Feature | Identifier,
    soil: Sequence[Identifier] = DEFAULT_SOIL,
) -> Block:
    """The sapling, which grows into `tree`: the feature `/place feature` builds at its position.

    It can only be planted on the `soil` blocks.
    """
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_sapling")
    display_name = f"{wood.replace('_', ' ').title()} Sapling"

    # It drops itself
    drop = LootTable(f"{wood}_sapling")
    drop.pool().entry(f"{namespace}:{wood}_sapling")
    drop.queue()

    # Like vanilla, it has two stages: the first growth sets this, the second grows the tree
    block.server.description.add_state("stage", (False, True))

    block.server.components.add(
        BlockDisplayName(display_name),
        BlockDestructibleByMining(0),
        BlockGeometry("minecraft:geometry.cross"),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_sapling")],
                params=MaterialParams(render_method=BlockMaterial.AlphaTestSingleSided),
            )
        ),
        BlockCollisionBox((0, 0, 0), (0, 0, 0)),
        BlockSelectionBox((12, 12, 12), (-6, 0, -6)),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(0),
        BlockRedstoneConductivity(False, False),
        BlockPlacementFilter().add_condition([BlockFaceValues.Up], list(soil)),
        BlockLootTable(drop),
        BlockWoodSetSapling(str(tree)),
        BlockWoodSetSupport(SupportedBy.Below),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemIcon(TextureComponents(color=f"{wood}_sapling")),
    )
    block.item.server.description.menu_category(ItemCategory.Nature, ItemGroups.Sapling)

    block.queue()
    return block
