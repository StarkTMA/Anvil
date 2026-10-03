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
    BlockRedstoneConsumer,
    BlockSelectionBox,
    BlockTagComponent,
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
    VerticalHalfValues,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags

from ..components import BlockWoodSetInteractable, BlockWoodSetRedstoneConsumer

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


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_trapdoor")
    display_name = f"{wood.replace('_', ' ').title()} Trapdoor"

    # Rotation: towards the player, y+180 on the bottom half, flipped upside down on the top
    block.server.description.traits.placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    block.server.description.traits.placement_position(
        [PlacementPositionTrait.VerticalHalf]
    )
    half = Query.BlockState(PlacementPositionTrait.VerticalHalf)
    for direction, (x, y, z) in CARDINAL_ROTATIONS.items():
        facing = Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        block.server.permutation(facing & (half == VerticalHalfValues.BOTTOM)).add(
            BlockTransformation().rotation((x, (y + 180) % 360, z))
        )
        block.server.permutation(facing & (half == VerticalHalfValues.TOP)).add(
            BlockTransformation().rotation(((x + 180) % 360, y, z))
        )

    block.server.description.add_state("open", (False, True))
    block.server.permutation(~Query.BlockState("open")).add(
        BlockCollisionBox((16, 3, 16), (-8, 0, -8)),
        BlockSelectionBox((16, 3, 16), (-8, 0, -8)),
    )
    block.server.permutation(Query.BlockState("open")).add(
        BlockCollisionBox((16, 16, 3), (-8, 0, 5)),
        BlockSelectionBox((16, 16, 3), (-8, 0, 5)),
    )

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )


    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(f"{wood}_planks", collection="trapdoor").bone_visibility(
            trapdoor_closed=~Query.BlockState("open"),
            trapdoor_open=Query.BlockState("open"),
        ),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_trapdoor")],
                params=MaterialParams(render_method=BlockMaterial.AlphaTestSingleSided),
            )
        ),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("all"),
        BlockDestructibleByExplosion(7),
        BlockRedstoneConductivity(False, False),
        BlockRedstoneConsumer(0, True),
        # Scripts: opened by players and by redstone
        BlockWoodSetInteractable(),
        BlockWoodSetRedstoneConsumer(),
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(15),
    )
    block.item.server.description.menu_category(
        ItemCategory.Construction, ItemGroups.Trapdoor
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_trapdoor")
        recipe.ingredients([[planks, planks, planks], [planks, planks, planks]])
        recipe.result(block.identifier, 2)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
