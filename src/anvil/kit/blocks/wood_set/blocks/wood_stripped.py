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
    FacingDirectionValues,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
    RecipeUnlockContext,
)
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemDisplayName,
    ItemFuel,
    ItemTags,
)
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from . import MODEL

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 3,
    MinecraftItemTags.StoneTier: 1.5,
    MinecraftItemTags.CopperTier: 0.75,
    MinecraftItemTags.IronTier: 0.6,
    MinecraftItemTags.DiamondTier: 0.5,
    MinecraftItemTags.NetheriteTier: 0.4,
    MinecraftItemTags.GoldenTier: 0.35,
}

# Rotation (x, y, z) per face the block was placed against
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
    block = Block(f"{wood}_wood_stripped")
    display_name = f"{wood.replace('_', ' ').title()} Wood Stripped"

    block.server.description.traits.placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    for direction, rotation in FACE_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementPositionTrait.BlockFace) == direction
        ).add(BlockTransformation().rotation(rotation))

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(),
        # Stripped wood on every face
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_log_stripped")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockCollisionBox((16, 16, 16), (-8, 0, -8)),
        BlockSelectionBox((16, 16, 16), (-8, 0, -8)),
        BlockMovable(BlockMovementType.PushPull),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent(
            [
                MinecraftBlockTags.Wood,
                MinecraftBlockTags.IsAxeItemDestructible,
                MinecraftBlockTags.Log,
            ]
        ),
        BlockConnectionRule("all"),
        BlockDestructibleByExplosion(15),
        BlockRedstoneConductivity(True, True),
    )

    # Its item: shown in the creative inventory, burns in a furnace, and its vanilla tag lets every vanilla wood recipe use it
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(15),
        ItemTags([MinecraftItemTags.Logs, MinecraftItemTags.LogsThatBurn]),
    )
    block.item.server.description.menu_category(ItemCategory.Nature, ItemGroups.Wood)

    block.queue()

    if "log_stripped" in selected:
        log = f"{namespace}:{wood}_log_stripped"
        recipe = ShapedCraftingRecipe(f"{wood}_wood_stripped")
        recipe.ingredients([[log, log], [log, log]])
        recipe.result(block.identifier, 3)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
