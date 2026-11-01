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
    BlockLiquidDetection,
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
    ItemTagFilter,
    MaterialParams,
    NWayVisualRotation,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
    CardinalDirectionsValues,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
    RecipeUnlockContext,
)
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemDisplayName,
    ItemFuel,
    ItemIcon,
    ItemMaxStackSize,
)
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags, MinecraftItemTypes
from anvil.api.world.loot_tables import LootTable
from anvil.lib.lib import Color

from ..components import BlockWoodSetSign, BlockWoodSetSupport, SupportedBy
from . import MAP_COLOR, MODEL

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

# Rotation (x, y, z) per direction the wall sign points at, i.e. towards the wall. The
# `wall_sign` collection is modelled against the north wall of the block.
WALL_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}


def _material(wood: str, color: str) -> BlockMaterialInstance:
    return BlockMaterialInstance().add_instance(
        spec=InstanceSpec(
            blockbench=MODEL,
            face=BlockFaceValues.All,
            variations=[InstanceVariant(color=color)],
            params=MaterialParams(render_method=BlockMaterial.Opaque),
        )
    )


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_sign")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Sign"

    block.server.description.traits.placement_direction(
        y_rotation_offset=180,
        traits=[
            PlacementDirectionTrait.SixteenWayRotation,
            PlacementDirectionTrait.CardinalDirection,
        ],
    )
    block.server.description.add_state("standing", (True, False))
    standing = Query.BlockState("standing")

    for direction, rotation in WALL_ROTATIONS.items():
        block.server.permutation(
            ~standing
            & (Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction)
        ).add(BlockTransformation(rotation=rotation))
    block.server.permutation(~standing).add(
        BlockGeometry(blockbench=MODEL, collection="wall_sign"),
        _material(wood, f"{wood}_planks"),
        BlockSelectionBox(origin=(-8, 4, -8), size=(16, 8, 1)),
    )

    mining = BlockDestructibleByMining(seconds_to_destroy=1)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(
            blockbench=MODEL,
            collection="standing_sign",
            n_way_visual_rotation=NWayVisualRotation(
                y=PlacementDirectionTrait.SixteenWayRotation
            ),
        ),
        _material(wood, f"{wood}_standing_sign"),
        BlockCollisionBox(enabled=False),
        BlockSelectionBox(origin=(-4, 0, -4), size=(8, 16, 8)),
        BlockMovable(movement_type="popped"),
        BlockFlammable(),
        # Waterloggable like vanilla Bedrock: water flows into it and stays
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
        ),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockTagComponent(
            value=[MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule(accepts_connections_from="none"),
        BlockDestructibleByExplosion(explosion_resistance=5),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=False, redstone_conductor=False
        ),
        BlockPlacementFilter().add_condition(
            allowed_faces=[BlockFaceValues.Up, BlockFaceValues.Side]
        ),
        BlockTick(interval_range=(1, 1), looping=True),
        BlockEntity(dynamic_properties=True),
        BlockWoodSetSign(
            text_offset=(8, 9.5, 8.75), text_scale=0.46, wall_text_offset=(8, 5.5, 1.1)
        ),
        BlockWoodSetSupport(supported_by=SupportedBy.Sign),
    )

    drop = LootTable(f"{wood}_sign")
    drop.pool().entry(f"{namespace}:{wood}_sign")
    drop.queue()
    block.server.components.add(BlockLootTable(value=drop))

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemIcon(textures=TextureComponents(color=f"{wood}_sign")),
        ItemFuel(duration=10),
        # Vanilla signs stack to 16
        ItemMaxStackSize(value=16),
    )
    block.item.server.description.menu_category(ItemCategory.Items, ItemGroups.Sign)

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        stick = MinecraftItemTypes.Stick()
        recipe = ShapedCraftingRecipe(f"{wood}_sign")
        recipe.ingredients(
            [[planks, planks, planks], [planks, planks, planks], [None, stick, None]]
        )
        recipe.result(block.identifier, 3)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
