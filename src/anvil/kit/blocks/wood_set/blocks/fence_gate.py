from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockFlammable,
    BlockGeometry,
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
    RecipeUnlockContext,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags, MinecraftItemTypes

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
    block = Block(f"{wood}_fence_gate")
    display_name = f"{wood.replace('_', ' ').title()} Fence Gate"

    block.server.description.traits.placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    for direction, rotation in CARDINAL_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        ).add(BlockTransformation().rotation(rotation))

    block.server.description.add_state("open", (False, True))

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.permutation(~Query.BlockState("open")).add(
        BlockCollisionBox((16, 24, 4), (-8, 0, -2))
    )
    block.server.permutation(Query.BlockState("open")).add(
        BlockCollisionBox((0, 0, 0), (0, 0, 0))
    )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(f"{wood}_planks", collection="fence_gate").bone_visibility(
            fence_gate_closed=~Query.BlockState("open"),
            fence_gate_open=Query.BlockState("open"),
        ),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockSelectionBox((16, 16, 4), (-8, 0, -2)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
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
        ItemCategory.Construction, ItemGroups.FenceGate
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        stick = MinecraftItemTypes.Stick()
        recipe = ShapedCraftingRecipe(f"{wood}_fence_gate")
        recipe.ingredients([[stick, planks, stick], [stick, planks, stick]])
        recipe.result(block.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
