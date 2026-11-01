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
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockTagComponent,
    BlockTransformation,
    InstanceSpec,
    InstanceVariant,
    ItemTagFilter,
    MaterialParams,
)
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockMaterial,
    BlockSoundGroup,
    FacingDirectionValues,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
)
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemDisplayName,
    ItemFuel,
    ItemTags,
)
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.lib import Color
from . import MAP_COLOR, MODEL

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 3,
    MinecraftItemTags.StoneTier: 1.5,
    MinecraftItemTags.CopperTier: 0.75,
    MinecraftItemTags.IronTier: 0.6,
    MinecraftItemTags.DiamondTier: 0.5,
    MinecraftItemTags.NetheriteTier: 0.4,
    MinecraftItemTags.GoldenTier: 0.35,
}

# Rotation (x, y, z) per face the log was placed against
FACE_ROTATIONS = {
    FacingDirectionValues.NORTH: (270, 0, 0),
    FacingDirectionValues.SOUTH: (90, 0, 0),
    FacingDirectionValues.WEST: (0, 270, 90),
    FacingDirectionValues.EAST: (0, 90, 270),
    FacingDirectionValues.Down: (180, 0, 0),
    FacingDirectionValues.Up: (0, 0, 0),
}


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
) -> Block:
    block = Block(f"{wood}_log_stripped")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Log Stripped"

    block.server.description.traits.placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    for direction, rotation in FACE_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementPositionTrait.BlockFace) == direction
        ).add(BlockTransformation(rotation=rotation))

    mining = BlockDestructibleByMining(seconds_to_destroy=3)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    # Stripped wood all round, rings on the ends
    materials = BlockMaterialInstance()
    for face, texture in (
        (BlockFaceValues.All, f"{wood}_log_stripped"),
        (BlockFaceValues.Up, f"{wood}_log_stripped_top"),
        (BlockFaceValues.Down, f"{wood}_log_stripped_top"),
    ):
        materials.add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=face,
                variations=[InstanceVariant(color=texture)],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(),
        materials,
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockMovable(movement_type="push_pull"),
        BlockFlammable(),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockTagComponent(
            value=[
                MinecraftBlockTags.Wood,
                MinecraftBlockTags.IsAxeItemDestructible,
                MinecraftBlockTags.Log,
            ]
        ),
        BlockConnectionRule(accepts_connections_from="all"),
        BlockDestructibleByExplosion(explosion_resistance=15),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=True, redstone_conductor=True
        ),
    )

    block.descriptor()

    # Its item: shown in the creative inventory, burns in a furnace, and its vanilla tag lets every vanilla wood recipe use it
    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=15),
        ItemTags(tags=[MinecraftItemTags.Logs, MinecraftItemTags.LogsThatBurn]),
    )
    block.item.server.description.menu_category(ItemCategory.Nature, ItemGroups.Log)

    block.queue()

    return block
