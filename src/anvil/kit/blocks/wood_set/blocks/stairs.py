from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockFlammable,
    BlockGeometry,
    BlockItemVisual,
    BlockLightDampening,
    BlockLiquidDetection,
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
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
    ItemTagFilter,
    MaterialParams,
)
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.core.core import CONFIG
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.jsonmodel.enums import (
    BlockCornerState,
    BlockCornerValues,
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
    CardinalDirectionsValues,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
    PlacementPositionTrait,
    RecipeUnlockContext,
    VerticalHalfValues,
)
from anvil.lib.jsonmodel.types import Color

from . import MAP_COLOR, MODEL

AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 1.5,
    MinecraftItemTags.StoneTier: 0.75,
    MinecraftItemTags.CopperTier: 0.6,
    MinecraftItemTags.IronTier: 0.5,
    MinecraftItemTags.DiamondTier: 0.4,
    MinecraftItemTags.NetheriteTier: 0.35,
    MinecraftItemTags.GoldenTier: 0.25,
}

CARDINAL_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}

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


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_stairs")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Stairs"

    block.server.description.traits.set_placement_direction(
        traits=[PlacementDirectionTrait.CornerAndCardinalDirection],
        blocks_to_corner_with=[
            BlockDescriptor(tags=Query.AllTags([MinecraftBlockTags.CornerableStairs]))
        ],
    )
    block.server.description.traits.set_placement_position(
        [PlacementPositionTrait.VerticalHalf]
    )

    half = Query.BlockState(PlacementPositionTrait.VerticalHalf)
    corner = Query.BlockState(BlockCornerState.Corner)
    bottom = half == VerticalHalfValues.BOTTOM
    top = half == VerticalHalfValues.TOP

    geometry = BlockGeometry(
        blockbench=MODEL,
        collection="stairs",
        uv_lock=True,
    ).add_bone_visibility(
        **{
            name: (bottom & (corner == b_value if b_equal else corner != b_value))
            | (top & (corner == t_value if t_equal else corner != t_value))
            for name, (_, ((b_equal, b_value), (t_equal, t_value))) in QUADRANTS.items()
        }
    )

    for h, rule_index in (
        (VerticalHalfValues.BOTTOM, 0),
        (VerticalHalfValues.TOP, 1),
    ):
        for value in BlockCornerValues:
            collision = BlockCollisionBox(origin=(-8, 0, -8), size=(16, 8, 16))
            for origin, rules in QUADRANTS.values():
                equal, rule_value = rules[rule_index]
                if (value == rule_value) == equal:
                    x, y, z = origin
                    collision.add_box(origin=(-x - 8, y, z), size=(8, 8, 8))
            block.server.permutation((half == h) & (corner == value)).add(collision)

    for direction, (x, y, z) in CARDINAL_ROTATIONS.items():
        facing = (
            Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        )
        block.server.permutation(facing & bottom).add(
            BlockTransformation(rotation=(x, (y + 180) % 360, z))
        )
        block.server.permutation(facing & top).add(
            BlockTransformation(rotation=((x + 180) % 360, y, z))
        )

    mining = BlockDestructibleByMining(seconds_to_destroy=3)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    item_visual = BlockItemVisual(blockbench=MODEL, collection="stairs")
    item_visual.add_material_instance(blockbench=MODEL, texture=f"{wood}_planks")
    item_visual.item_display_transforms(
        merge=False,
        gui=ItemDisplayGuiTransform(
            rotation=[30, -135, 0], scale=[0.625, 0.625, 0.625], fit_to_frame=False
        ),
        firstperson_righthand=ItemDisplayTransform(
            rotation=[0, 135, 0], scale=[0.4, 0.4, 0.4]
        ),
        thirdperson_righthand=ItemDisplayTransform(
            rotation=[70, -45, 0], scale=[0.375, 0.375, 0.375]
        ),
        fixed=ItemDisplayTransform(rotation=[0, 90, 0]),
    )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        geometry,
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockMovable(movement_type="push_pull"),
        BlockFlammable(),
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
        ),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockTagComponent(
            value=[
                MinecraftBlockTags.Wood,
                MinecraftBlockTags.IsAxeItemDestructible,
                MinecraftBlockTags.CornerableStairs,
            ]
        ),
        BlockConnectionRule(accepts_connections_from="all"),
        BlockDestructibleByExplosion(explosion_resistance=15),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=True, redstone_conductor=False
        ),
        BlockSupport(shape="stair"),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=15),
    )
    block.item.server.description.set_menu_category(
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
