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
    BlockSupport,
    BlockTagComponent,
    BlockTransformation,
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockCornerState,
    BlockCornerValues,
    BlockFaceValues,
    BlockMaterial,
    BlockMovementType,
    CardinalDirectionsValues,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
    PlacementPositionTrait,
    RecipeUnlockContext,
    VerticalHalfValues,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.schemas import MinecraftBlockDescriptor

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 1.5,
    MinecraftItemTags.StoneTier: 0.75,
    MinecraftItemTags.CopperTier: 0.6,
    MinecraftItemTags.IronTier: 0.5,
    MinecraftItemTags.DiamondTier: 0.4,
    MinecraftItemTags.NetheriteTier: 0.35,
    MinecraftItemTags.GoldenTier: 0.25,
}

# Rotation (x, y, z) per direction the player is facing
CARDINAL_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}

# Upper quadrants: origin, then the (equal, corner) visibility rule for bottom and top stairs
QUADRANTS = {
    "outer_right": (
        (-8, 8, 0),
        ((False, BlockCornerValues.OuterLeft), (False, BlockCornerValues.OuterRight)),
    ),
    "outer_left": (
        (0, 8, 0),
        ((False, BlockCornerValues.OuterRight), (False, BlockCornerValues.OuterLeft)),
    ),
    "inner_right": (
        (-8, 8, -8),
        ((True, BlockCornerValues.InnerRight), (True, BlockCornerValues.InnerLeft)),
    ),
    "inner_left": (
        (0, 8, -8),
        ((True, BlockCornerValues.InnerLeft), (True, BlockCornerValues.InnerRight)),
    ),
}


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_stairs")
    display_name = f"{wood.replace('_', ' ').title()} Stairs"

    block.server.description.traits.placement_direction(
        traits=[PlacementDirectionTrait.CornerAndCardinalDirection],
        blocks_to_corner_with=[
            MinecraftBlockDescriptor(
                tags=Query.AllTags([MinecraftBlockTags.CornerableStairs])
            )
        ],
    )
    block.server.description.traits.placement_position(
        [PlacementPositionTrait.VerticalHalf]
    )

    half = Query.BlockState(PlacementPositionTrait.VerticalHalf)
    corner = Query.BlockState(BlockCornerState.Corner)
    bottom = half == VerticalHalfValues.BOTTOM
    top = half == VerticalHalfValues.TOP

    # Each upper quadrant is a bone, visible when `(corner == value) == equal`.
    geometry = BlockGeometry(f"{wood}_planks", collection="stairs", uv_lock=True)
    geometry.bone_visibility(
        **{
            name: (bottom & (corner == b_value if b_equal else corner != b_value))
            | (top & (corner == t_value if t_equal else corner != t_value))
            for name, (_, ((b_equal, b_value), (t_equal, t_value))) in QUADRANTS.items()
        }
    )

    # Collision: the lower slab plus the upper quadrants visible for each half/corner.
    for h, rule_index in (
        (VerticalHalfValues.BOTTOM, 0),
        (VerticalHalfValues.TOP, 1),
    ):
        for value in BlockCornerValues:
            collision = BlockCollisionBox((16, 8, 16), (-8, 0, -8))
            for origin, rules in QUADRANTS.values():
                equal, rule_value = rules[rule_index]
                if (value == rule_value) == equal:
                    x, y, z = origin
                    # Collision x is mirrored relative to the geometry's x.
                    collision.add_box((8, 8, 8), (-x - 8, y, z))
            block.server.permutation((half == h) & (corner == value)).add(collision)

    # Rotation: towards the player, y+180 on the bottom half, flipped upside down on the top
    for direction, (x, y, z) in CARDINAL_ROTATIONS.items():
        facing = Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        block.server.permutation(facing & bottom).add(
            BlockTransformation().rotation((x, (y + 180) % 360, z))
        )
        block.server.permutation(facing & top).add(
            BlockTransformation().rotation(((x + 180) % 360, y, z))
        )

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        geometry,
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockSelectionBox((16, 16, 16), (-8, 0, -8)),
        BlockMovable(BlockMovementType.PushPull),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent(
            [MinecraftBlockTags.Wood, MinecraftBlockTags.CornerableStairs]
        ),
        BlockConnectionRule("all"),
        BlockDestructibleByExplosion(15),
        BlockRedstoneConductivity(True, False),
        BlockSupport("stair"),
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(15),
    )
    block.item.server.description.menu_category(
        ItemCategory.Construction, ItemGroups.Stairs
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_stairs")
        recipe.ingredients([[planks], [planks, planks], [planks, planks, planks]])
        recipe.result(block.identifier, 4)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
