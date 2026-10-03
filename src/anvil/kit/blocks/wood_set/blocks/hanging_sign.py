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
    PlacementPositionTrait,
    RecipeUnlockContext,
)
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemDisplayName,
    ItemFuel,
    ItemIcon,
)
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags, MinecraftItemTypes

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


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_hanging_sign")
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
        ).add(BlockTransformation().rotation(rotation))
    for side, rotation in SIDE_ROTATIONS.items():
        block.server.permutation(face == side).add(
            BlockTransformation().rotation(rotation)
        )

    # Selectable: the board and its chains, plus the bar across the block on a wall
    block.server.permutation(hung_under).add(
        BlockSelectionBox((14, 16, 2), (-7, 0, -1))
    )
    block.server.permutation(~hung_under).add(
        BlockSelectionBox((16, 16, 4), (-8, 0, -2))
    )

    mining = BlockDestructibleByMining(1)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(f"{wood}_planks", collection="hanging_sign").bone_visibility(
            **{SIDE_BONE: ~hung_under, BOTTOM_BONE: hung_under}
        ),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_hanging_sign")],
                # The chains are flat cut-outs seen from both sides
                params=MaterialParams(render_method=BlockMaterial.AlphaTest),
            )
        ),
        # Walked through like a vanilla sign
        BlockCollisionBox((0, 0, 0), (0, 0, 0)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(5),
        BlockRedstoneConductivity(False, False),
        BlockPlacementFilter().add_condition(
            [BlockFaceValues.Down, BlockFaceValues.Side]
        ),
        BlockTick((1, 1), True),
        # The text lives in the block entity's dynamic properties
        BlockEntity(dynamic_properties=True),
        # Script: asks for the text when placed, and again when interacted with; shown on
        # both sides of the board (14 x 10, 2 thick, centred), in the middle of its height
        BlockWoodSetSign(
            (8, 3.2, 9.1), text_scale=0.53, line_length=9, double_sided=False
        ),
        # Breaks with the block its block face was placed on
        BlockWoodSetSupport(SupportedBy.BlockFace),
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemIcon(TextureComponents(color=f"{wood}_hanging_sign")),
        ItemFuel(10),
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
