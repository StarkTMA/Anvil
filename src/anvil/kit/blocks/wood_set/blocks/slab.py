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
    InstanceSpec,
    InstanceVariant,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockMaterial,
    BlockMovementType,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
    RecipeUnlockContext,
    VerticalHalfValues,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel, ItemTags
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags

from ..components import BlockWoodSetSlab

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


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_slab")
    display_name = f"{wood.replace('_', ' ').title()} Slab"

    block.server.description.traits.placement_position(
        [PlacementPositionTrait.VerticalHalf]
    )

    # A second slab placed on the open half sets `double`, making it a full block (script).
    block.server.description.add_state("double", (False, True))

    half = Query.BlockState(PlacementPositionTrait.VerticalHalf)
    double = Query.BlockState("double")
    bottom = half == VerticalHalfValues.BOTTOM
    top = half == VerticalHalfValues.TOP

    block.server.permutation(bottom & ~double).add(
        BlockCollisionBox((16, 8, 16), (-8, 0, -8)),
        BlockSelectionBox((16, 8, 16), (-8, 0, -8)),
    )
    block.server.permutation(top & ~double).add(
        BlockCollisionBox((16, 8, 16), (-8, 8, -8)),
        BlockSelectionBox((16, 8, 16), (-8, 8, -8)),
    )
    block.server.permutation(double).add(
        BlockCollisionBox((16, 16, 16), (-8, 0, -8)),
        BlockSelectionBox((16, 16, 16), (-8, 0, -8)),
    )

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(f"{wood}_planks", collection="slab").bone_visibility(
            slab_bottom=bottom | double,
            slab_top=top | double,
        ),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockMovable(BlockMovementType.PushPull),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("all"),
        BlockDestructibleByExplosion(15),
        BlockRedstoneConductivity(True, False),
        BlockWoodSetSlab(),
    )

    # Its item: shown in the creative inventory, burns in a furnace, and its vanilla tag lets every vanilla wood recipe use it
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(7.5),
        ItemTags([MinecraftItemTags.WoodenSlabs]),
    )
    block.item.server.description.menu_category(
        ItemCategory.Construction, ItemGroups.Slab
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_slab")
        recipe.ingredients([[planks, planks, planks]])
        recipe.result(block.identifier, 6)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
