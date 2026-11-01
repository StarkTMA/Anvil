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
from anvil.api.core.enums import (
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

# The two exclusive bones of the `hanging_sign` collection: the bar across the top that
# hangs it on a wall, and the chains up to the block above
SIDE_BONE = "top_bit"
BOTTOM_BONE = "top_chain"

# Hung under a block: rotation (x, y, z) per direction the player faced when placing it.
# The `hanging_sign` collection is modelled with its board facing north and south.
BOTTOM_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}

# Hung on the side of a block: rotation per face it was placed on. The side bone's bar
# runs west to east, so at rotation 0 it hangs from the block to the west (placed on its
# east face).
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

    # Which way the player faced, and which face it was placed on: under a block it hangs
    # facing the player, on the side of a block it hangs from that block
    block.server.description.traits.placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    block.server.description.traits.placement_position(
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

    # Selectable: the board and its chains, plus the bar across the block on a wall
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
                # The chains are flat cut-outs seen from both sides
                params=MaterialParams(render_method=BlockMaterial.AlphaTest),
            )
        ),
        # Walked through like a vanilla sign
        BlockCollisionBox(enabled=False),
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
            allowed_faces=[BlockFaceValues.Down, BlockFaceValues.Side]
        ),
        BlockTick(interval_range=(1, 1), looping=True),
        # The text lives in the block entity's dynamic properties
        BlockEntity(dynamic_properties=True),
        # Script: asks for the text when placed, and again when interacted with; shown on
        # both sides of the board (14 x 10, 2 thick, centred), in the middle of its height
        BlockWoodSetSign(
            text_offset=(8, 3.2, 9.1),
            text_scale=0.53,
            line_length=9,
            double_sided=False,
        ),
        # Breaks with the block its block face was placed on
        BlockWoodSetSupport(supported_by=SupportedBy.BlockFace),
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemIcon(textures=TextureComponents(color=f"{wood}_hanging_sign")),
        ItemFuel(duration=10),
        # Vanilla signs stack to 16
        ItemMaxStackSize(value=16),
    )
    block.item.server.description.menu_category(
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
