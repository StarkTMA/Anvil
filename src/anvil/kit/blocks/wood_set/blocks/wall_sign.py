from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockEntity,
    BlockFlammable,
    BlockGeometry,
    BlockLightDampening,
    BlockLootTable,
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockPlacementFilter,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockTagComponent,
    BlockTick,
    BlockTransformation,
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockMaterial,
    BlockMovementType,
    CardinalDirectionsValues,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.api.world.loot_tables import LootTable

from ..components import BlockWoodSetSign, BlockWoodSetSupport, SupportedBy

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 0.5,
    MinecraftItemTags.StoneTier: 0.25,
    MinecraftItemTags.CopperTier: 0.2,
    MinecraftItemTags.IronTier: 0.15,
    MinecraftItemTags.DiamondTier: 0.15,
    MinecraftItemTags.NetheriteTier: 0.1,
    MinecraftItemTags.GoldenTier: 0.1,
}

# Rotation (x, y, z) per direction the player faced when placing it, i.e. towards the
# wall. The `wall_sign` collection is modelled against the north wall of the block.
CARDINAL_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_wall_sign")
    display_name = f"{wood.replace('_', ' ').title()} Sign"

    # North, east, south or west only
    block.server.description.traits.placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    for direction, rotation in CARDINAL_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        ).add(BlockTransformation().rotation(rotation))

    mining = BlockDestructibleByMining(1)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(f"{wood}_planks", collection="wall_sign"),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        # Walked through like a vanilla sign; the board is selectable against the wall
        BlockCollisionBox((0, 0, 0), (0, 0, 0)),
        BlockSelectionBox((16, 8, 1), (-8, 4, -8)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(5),
        BlockRedstoneConductivity(False, False),
        BlockPlacementFilter().add_condition([BlockFaceValues.Side]),
        BlockTick((1, 1), True),
        # The text lives in the block entity's dynamic properties
        BlockEntity(dynamic_properties=True),
        # Script: asks for the text when placed, and again when interacted with
        BlockWoodSetSign((8, 5.5, 1.1), text_scale=0.46),
        # Breaks with the wall it hangs on, which its cardinal direction points at
        BlockWoodSetSupport(SupportedBy.Facing),
    )

    # With a standing sign, the sign item places this block on walls (standing_sign.py):
    # it drops the sign item, and its own item stays out of the inventory.
    if "standing_sign" in selected:
        drop = LootTable(f"{wood}_wall_sign")
        drop.pool().entry(f"{namespace}:{wood}_sign")
        drop.queue()
        block.server.components.add(BlockLootTable(drop))

    # Its item: burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(10),
    )
    if "standing_sign" not in selected:
        block.item.server.description.menu_category(ItemCategory.Items, ItemGroups.Sign)

    block.queue()

    return block
