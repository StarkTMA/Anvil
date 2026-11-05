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
    ItemTagFilter,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
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
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockMaterial,
    BlockSoundGroup,
    ItemCategory,
    ItemGroups,
    RecipeUnlockContext,
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


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_planks")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Planks"

    mining = BlockDestructibleByMining(seconds_to_destroy=3)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockMovable(movement_type="push_pull"),
        BlockFlammable(),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockTagComponent(
            value=[MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule(accepts_connections_from="all"),
        BlockDestructibleByExplosion(explosion_resistance=15),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=True, redstone_conductor=True
        ),
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=15),
        ItemTags(tags=[MinecraftItemTags.Planks]),
    )
    block.item.server.description.set_menu_category(
        ItemCategory.Construction, ItemGroups.Planks
    )

    block.queue()

    for trunk in ("log", "log_stripped", "wood", "wood_stripped"):
        if trunk in selected:
            recipe = ShapelessRecipe(f"{wood}_planks_from_{trunk}")
            recipe.ingredients([f"{namespace}:{wood}_{trunk}"])
            recipe.result(block.identifier, 4)
            recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
            recipe.queue()

    if "slab" in selected:
        slab = f"{namespace}:{wood}_slab"
        recipe = ShapedCraftingRecipe(f"{wood}_planks_from_slab")
        recipe.ingredients([[slab], [slab]])
        recipe.result(block.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
