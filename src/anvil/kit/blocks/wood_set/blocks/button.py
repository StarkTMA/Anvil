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
    BlockRedstoneProducer,
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
    FacingDirectionValues,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
    RecipeUnlockContext,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapelessRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags

from ..components import BlockWoodSetSupport, BlockWoodSetTogglable, SupportedBy

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 0.4,
    MinecraftItemTags.StoneTier: 0.2,
    MinecraftItemTags.CopperTier: 0.15,
    MinecraftItemTags.IronTier: 0.15,
    MinecraftItemTags.DiamondTier: 0.1,
    MinecraftItemTags.NetheriteTier: 0.1,
    MinecraftItemTags.GoldenTier: 0.1,
}

# Rotation (x, y, z) per face the button was placed against
FACE_ROTATIONS = {
    FacingDirectionValues.NORTH: (270, 0, 0),
    FacingDirectionValues.SOUTH: (90, 0, 0),
    FacingDirectionValues.WEST: (0, 270, 90),
    FacingDirectionValues.EAST: (0, 90, 270),
    FacingDirectionValues.Down: (180, 0, 0),
    FacingDirectionValues.Up: (0, 0, 0),
}


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_button")
    display_name = f"{wood.replace('_', ' ').title()} Button"

    block.server.description.traits.placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    for direction, rotation in FACE_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementPositionTrait.BlockFace) == direction
        ).add(BlockTransformation().rotation(rotation))

    block.server.description.add_state("powered", (False, True))
    block.server.permutation(Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=15, strongly_powered_face=BlockFaceValues.South),
        BlockSelectionBox((6, 1, 4), (-3, 0, -2)),
    )
    block.server.permutation(~Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.South),
        BlockSelectionBox((6, 2, 4), (-3, 0, -2)),
    )

    mining = BlockDestructibleByMining(0.75)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(f"{wood}_planks", collection="button").bone_visibility(
            button_full=~Query.BlockState("powered"),
            button_pressed=Query.BlockState("powered"),
        ),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockCollisionBox((6, 2, 4), (-3, 0, -2)),
        BlockSelectionBox((6, 2, 4), (-3, 0, -2)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(0, 0, "never"),
        BlockMapColor("#19381F"),
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(7),
        BlockRedstoneConductivity(False, False),
        # Scripts: pressed on interact and released on tick, broken with its support
        BlockTick((20, 20), True),
        BlockWoodSetTogglable(),
        BlockWoodSetSupport(SupportedBy.BlockFace),
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(5),
    )
    block.item.server.description.menu_category(ItemCategory.Items, ItemGroups.Buttons)

    block.queue()

    if "planks" in selected:
        recipe = ShapelessRecipe(f"{wood}_button")
        recipe.ingredients([f"{namespace}:{wood}_planks"])
        recipe.result(block.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
