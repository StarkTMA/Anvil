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

from ..components import BlockWoodSetSign, BlockWoodSetSupport, SupportedBy
from . import MODEL

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
        InstanceSpec(
            blockbench_name=MODEL,
            face=BlockFaceValues.All,
            variations=[InstanceVariant(color=color)],
            params=MaterialParams(render_method=BlockMaterial.Opaque),
        )
    )


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_sign")
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
        ).add(BlockTransformation().rotation(rotation))
    block.server.permutation(~standing).add(
        BlockGeometry(MODEL, collection="wall_sign"),
        _material(wood, f"{wood}_planks"),
        BlockSelectionBox((16, 8, 1), (-8, 4, -8)),
    )

    mining = BlockDestructibleByMining(1)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(MODEL, collection="standing_sign").n_way_visual_rotation(
            y=PlacementDirectionTrait.SixteenWayRotation
        ),
        _material(wood, f"{wood}_standing_sign"),
        BlockCollisionBox((0, 0, 0), (0, 0, 0)),
        BlockSelectionBox((8, 16, 8), (-4, 0, -4)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent(
            [MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(5),
        BlockRedstoneConductivity(False, False),
        BlockPlacementFilter().add_condition(
            [BlockFaceValues.Up, BlockFaceValues.Side]
        ),
        BlockTick((1, 1), True),
        BlockEntity(dynamic_properties=True),
        BlockWoodSetSign(
            (8, 9.5, 8.75), text_scale=0.46, wall_text_offset=(8, 5.5, 1.1)
        ),
        BlockWoodSetSupport(SupportedBy.Sign),
    )

    drop = LootTable(f"{wood}_sign")
    drop.pool().entry(f"{namespace}:{wood}_sign")
    drop.queue()
    block.server.components.add(BlockLootTable(drop))

    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemIcon(TextureComponents(color=f"{wood}_sign")),
        ItemFuel(10),
        # Vanilla signs stack to 16
        ItemMaxStackSize(16),
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
