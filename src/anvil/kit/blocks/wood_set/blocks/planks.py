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
    RecipeUnlockContext,
)
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemDisplayName,
    ItemFuel,
    ItemTags,
)
from anvil.api.items.crafting import ShapedCraftingRecipe, ShapelessRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from . import MODEL

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
    block = Block(f"{wood}_planks")
    display_name = f"{wood.replace('_', ' ').title()} Planks"

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
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
            [MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
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
        ItemTags([MinecraftItemTags.Planks]),
    )
    block.item.server.description.menu_category(
        ItemCategory.Construction, ItemGroups.Planks
    )

    block.queue()

    # 4 planks from any trunk block
    for trunk in ("log", "log_stripped", "wood", "wood_stripped"):
        if trunk in selected:
            recipe = ShapelessRecipe(f"{wood}_planks_from_{trunk}")
            recipe.ingredients([f"{namespace}:{wood}_{trunk}"])
            recipe.result(block.identifier, 4)
            recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
            recipe.queue()

    # 1 plank from 2 slabs
    if "slab" in selected:
        slab = f"{namespace}:{wood}_slab"
        recipe = ShapedCraftingRecipe(f"{wood}_planks_from_slab")
        recipe.ingredients([[slab], [slab]])
        recipe.result(block.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
