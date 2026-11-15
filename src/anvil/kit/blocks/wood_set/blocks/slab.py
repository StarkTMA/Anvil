from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockFlammable,
    BlockGeometry,
    BlockItemVisual,
    BlockLightDampening,
    BlockLiquidDetection,
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockTagComponent,
    InstanceSpec,
    InstanceVariant,
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
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
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
    RecipeUnlockContext,
    VerticalHalfValues,
)
from anvil.lib.jsonmodel.types import Color

from ..components import BlockWoodSetSlab
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
    block = Block(f"{wood}_slab")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Slab"

    block.server.description.traits.set_placement_position(
        [PlacementPositionTrait.VerticalHalf]
    )

    block.server.description.add_state("double", (False, True))

    half = Query.BlockState(PlacementPositionTrait.VerticalHalf)
    double = Query.BlockState("double")
    bottom = half == VerticalHalfValues.BOTTOM
    top = half == VerticalHalfValues.TOP

    block.server.permutation(bottom & ~double).add(
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 8, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 8, 16)),
    )
    block.server.permutation(top & ~double).add(
        BlockCollisionBox(origin=(-8, 8, -8), size=(16, 8, 16)),
        BlockSelectionBox(origin=(-8, 8, -8), size=(16, 8, 16)),
    )
    block.server.permutation(double).add(
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 16, 16)),
    )

    mining = BlockDestructibleByMining(seconds_to_destroy=3)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    item_visual = BlockItemVisual(
        blockbench=MODEL,
        collection="slab",
    ).add_bone_visibility(slab_top="0")
    item_visual.add_material_instance(
        blockbench=MODEL,
        texture=f"{wood}_planks",
    )
    item_visual.item_display_transforms(
        merge=False,
        gui=ItemDisplayGuiTransform(translation=[0, 0, 0], fit_to_frame=False),
        fixed=ItemDisplayTransform(translation=[0, 2, 0]),
        firstperson_righthand=ItemDisplayTransform(translation=[0, 1.5, 0]),
        thirdperson_righthand=ItemDisplayTransform(translation=[0, 3, 1.5]),
    )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(
            blockbench=MODEL,
            collection="slab",
        ).add_bone_visibility(slab_bottom=bottom | double, slab_top=top | double),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockMovable(movement_type="push_pull"),
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
        BlockConnectionRule(accepts_connections_from="all"),
        BlockDestructibleByExplosion(explosion_resistance=15),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=True, redstone_conductor=False
        ),
        BlockWoodSetSlab(),
        item_visual,
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=7.5),
        ItemTags(tags=[MinecraftItemTags.WoodenSlabs]),
    )
    block.item.server.description.set_menu_category(
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
