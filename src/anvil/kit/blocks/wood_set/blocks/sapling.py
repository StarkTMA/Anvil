from collections.abc import Sequence

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
    BlockPlacementFilter,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.features import Feature
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemIcon
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.world.loot_tables import LootTable
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
    ItemCategory,
    ItemGroups,
    SupportedBy,
)
from anvil.lib.jsonmodel.types import Color

from ..components import BlockWoodSetSapling, BlockWoodSetSupport
from . import MAP_COLOR, MODEL

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
    tree: Feature | str,
    soil: Sequence[str] = DEFAULT_SOIL,
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Grass,
) -> Block:
    """The sapling, which grows into `tree`: the feature `/place feature` builds at its position.

    It can only be planted on the `soil` blocks.
    """
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_sapling")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Sapling"

    drop = LootTable(f"{wood}_sapling")
    drop.pool().entry(f"{namespace}:{wood}_sapling")
    drop.queue()

    block.server.description.add_state("stage", (False, True))

    block.server.components.add(
        BlockDisplayName(value=display_name),
        BlockDestructibleByMining(seconds_to_destroy=0),
        BlockGeometry(blockbench="minecraft:geometry.cross"),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_sapling")],
                params=MaterialParams(render_method=BlockMaterial.AlphaTestSingleSided),
            )
        ),
        BlockCollisionBox(enabled=False),
        BlockSelectionBox(origin=(-6, 0, -6), size=(12, 12, 12)),
        BlockFlammable(),
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.Popped,
        ),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockConnectionRule(accepts_connections_from="none"),
        BlockDestructibleByExplosion(explosion_resistance=0),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=False, redstone_conductor=False
        ),
        BlockPlacementFilter().add_condition(
            allowed_faces=[BlockFaceValues.Up], block_filter=list(soil)
        ),
        BlockLootTable(value=drop),
        BlockWoodSetSapling(tree_feature=str(tree)),
        BlockWoodSetSupport(supported_by=SupportedBy.Below),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemIcon(textures=TextureComponents(color=f"{wood}_sapling")),
    )
    block.item.server.description.set_menu_category(
        ItemCategory.Nature, ItemGroups.Sapling
    )

    block.queue()
    return block
