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
    BlockPlacementFilter,
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
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockMovementType,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
    RecipeUnlockContext,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags

from ..components import BlockWoodSetSupport, BlockWoodSetTogglable, SupportedBy
from . import MODEL

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


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_pressure_plate")
    display_name = f"{wood.replace('_', ' ').title()} Pressure Plate"

    block.server.description.traits.placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    block.server.description.add_state("powered", (False, True))
    block.server.permutation(Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=15, strongly_powered_face=BlockFaceValues.Up),
        BlockTransformation().translation((0, -0.5 / 16, 0)),
        # Ticks only while pressed, to release; idle plates don't tick
        BlockTick((20, 20), True),
    )
    block.server.permutation(~Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.Down),
        BlockTransformation().translation((0, 0, 0)),
    )

    mining = BlockDestructibleByMining(2.5)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    geometry = BlockGeometry(MODEL, collection="pressure_plate")
    geometry.block_culling("custom").add_rule(
        BlockFaceValues.Down, "pressure_plate", BlockFaceValues.Down, 0
    )

    item_visual = BlockItemVisual(MODEL, collection="pressure_plate")
    item_visual.material_instance(MODEL, f"{wood}_planks")
    item_visual.item_display_transforms(
        False,
        gui={
            "rotation": [30, 45, 0],
            "scale": [0.625, 0.625, 0.625],
            "fit_to_frame": False,
        },
        fixed={"translation": [0, 3.5, 0], "rotation": [0, 180, 0]},
        firstperson_righthand={
            "translation": [0, 3, 0],
            "scale": [0.4, 0.4, 0.4],
        },
        thirdperson_righthand={"translation": [0, 3, 2.5]},
    )
    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        geometry,
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockCollisionBox((14, 3.3, 14), (-7, 0, -7)),
        BlockSelectionBox((14, 1, 14), (-7, 0, -7)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent(
            [MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(7),
        BlockRedstoneConductivity(True, True),
        # Format 1.26.20+ wants it in the base components too when a permutation sets it
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.Down),
        BlockPlacementFilter().add_condition(
            [BlockFaceValues.Up, BlockFaceValues.Side]
        ),
        BlockLiquidDetection().add_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
            use_liquid_clipping=True,
        ),
        # Scripts: pressed when stepped on and released on tick, broken with its support.
        # The script's onTick needs a tick in the base components: it ticks once and stops,
        # and only the powered permutation above keeps ticking
        BlockTick((20, 20), False),
        BlockWoodSetTogglable(),
        BlockWoodSetSupport(SupportedBy.BlockFace),
        item_visual,
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(15),
    )
    block.item.server.description.menu_category(
        ItemCategory.Items, ItemGroups.PressurePlate
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_pressure_plate")
        recipe.ingredients([[planks, planks]])
        recipe.result(block.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
