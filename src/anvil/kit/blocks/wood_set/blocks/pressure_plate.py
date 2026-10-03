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

    geometry = BlockGeometry(f"{wood}_planks", collection="pressure_plate")
    geometry.block_culling("custom").add_rule(
        BlockFaceValues.Down, "pressure_plate", BlockFaceValues.Down, 0
    )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        geometry,
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
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
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(7),
        BlockRedstoneConductivity(True, True),
        BlockPlacementFilter().add_condition(
            [BlockFaceValues.Up, BlockFaceValues.Side]
        ),
        BlockLiquidDetection().add_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
            use_liquid_clipping=True,
        ),
        # Scripts: pressed when stepped on and released on tick, broken with its support
        BlockTick((20, 20), True),
        BlockWoodSetTogglable(),
        BlockWoodSetSupport(SupportedBy.BlockFace),
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
