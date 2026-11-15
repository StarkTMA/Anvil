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
)
from anvil.api.core.core import CONFIG
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
from anvil.lib.jsonmodel.enums import (
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
    SupportedBy,
)
from anvil.lib.jsonmodel.types import Color

from ..components import BlockWoodSetSign, BlockWoodSetSupport
from . import MAP_COLOR, MODEL

AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 0.5,
    MinecraftItemTags.StoneTier: 0.25,
    MinecraftItemTags.CopperTier: 0.2,
    MinecraftItemTags.IronTier: 0.15,
    MinecraftItemTags.DiamondTier: 0.15,
    MinecraftItemTags.NetheriteTier: 0.1,
    MinecraftItemTags.GoldenTier: 0.1,
}

SIDE_BONE = "top_bit"
BOTTOM_BONE = "top_chain"

BOTTOM_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}

SIDE_ROTATIONS = {
    BlockFaceValues.East: (0, 0, 0),
    BlockFaceValues.North: (0, 90, 0),
    BlockFaceValues.West: (0, 180, 0),
    BlockFaceValues.South: (0, 270, 0),
}


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.HangingSign,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_hanging_sign")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Hanging Sign"

    block.server.description.traits.set_placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    block.server.description.traits.set_placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    face = Query.BlockState(PlacementPositionTrait.BlockFace)
    hung_under = face == BlockFaceValues.Down
    for direction, rotation in BOTTOM_ROTATIONS.items():
        block.server.permutation(
            hung_under
            & (Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction)
        ).add(BlockTransformation(rotation=rotation))
    for side, rotation in SIDE_ROTATIONS.items():
        block.server.permutation(face == side).add(
            BlockTransformation(rotation=rotation)
        )

    block.server.permutation(hung_under).add(
        BlockSelectionBox(origin=(-7, 0, -1), size=(14, 16, 2))
    )
    block.server.permutation(~hung_under).add(
        BlockSelectionBox(origin=(-8, 0, -2), size=(16, 16, 4))
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
            collection="hanging_sign",
        ).add_bone_visibility(**{SIDE_BONE: ~hung_under, BOTTOM_BONE: hung_under}),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_hanging_sign")],
                params=MaterialParams(render_method=BlockMaterial.AlphaTest),
            )
        ),
        BlockCollisionBox(enabled=False),
        BlockMovable(movement_type="popped"),
        BlockFlammable(),
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
            allowed_faces=[BlockFaceValues.Down, BlockFaceValues.Side]
        ),
        BlockTick(interval_range=(1, 1), looping=True),
        BlockEntity(dynamic_properties=True),
        BlockWoodSetSign(
            text_offset=(8, 3.2, 9.1),
            text_scale=0.53,
            line_length=9,
            double_sided=False,
        ),
        BlockWoodSetSupport(supported_by=SupportedBy.BlockFace),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemIcon(textures=TextureComponents(color=f"{wood}_hanging_sign")),
        ItemFuel(duration=10),
        ItemMaxStackSize(value=16),
    )
    block.item.server.description.set_menu_category(
        ItemCategory.Items, ItemGroups.HangingSign
    )

    block.queue()

    if "log_stripped" in selected:
        log = f"{namespace}:{wood}_log_stripped"
        chain = MinecraftItemTypes.IronChain()
        recipe = ShapedCraftingRecipe(f"{wood}_hanging_sign")
        recipe.ingredients([[chain, None, chain], [log, log, log], [log, log, log]])
        recipe.result(block.identifier, 6)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
