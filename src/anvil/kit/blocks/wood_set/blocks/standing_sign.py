from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockConnectionRule,
    BlockDestructibleByExplosion,
    BlockDestructibleByMining,
    BlockDisplayName,
    BlockEntity,
    BlockFlammable,
    BlockGeometry,
    BlockLightDampening,
    BlockLootTable,
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockPlacementFilter,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockTagComponent,
    BlockTick,
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
    PlacementDirectionTrait,
    RecipeUnlockContext,
)
from anvil.api.items.components import (
    ItemBlockPlacer,
    ItemDisplayName,
    ItemFuel,
    ItemIcon,
)
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.items.items import Item
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags, MinecraftItemTypes
from anvil.api.world.loot_tables import LootTable

from ..components import BlockWoodSetSign, BlockWoodSetSupport

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 0.5,
    MinecraftItemTags.StoneTier: 0.25,
    MinecraftItemTags.CopperTier: 0.2,
    MinecraftItemTags.IronTier: 0.15,
    MinecraftItemTags.DiamondTier: 0.15,
    MinecraftItemTags.NetheriteTier: 0.1,
    MinecraftItemTags.GoldenTier: 0.1,
}


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_standing_sign")
    # The sign item: placed on the side of a block it becomes the wall sign
    display_name = f"{wood.replace('_', ' ').title()} Sign"
    wall_sign = f"{namespace}:{wood}_wall_sign" if "wall_sign" in selected else None

    # Turns in 16 steps with the player, rendered by the geometry itself
    block.server.description.traits.placement_direction(
        y_rotation_offset=180, traits=[PlacementDirectionTrait.SixteenWayRotation]
    )

    mining = BlockDestructibleByMining(1)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(
            f"{wood}_planks", collection="standing_sign"
        ).n_way_visual_rotation(y=PlacementDirectionTrait.SixteenWayRotation),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=f"{wood}_planks",
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_standing_sign")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        # Walked through like a vanilla sign; boxes don't turn with the geometry, so the
        # selection is a centred post
        BlockCollisionBox((0, 0, 0), (0, 0, 0)),
        BlockSelectionBox((8, 16, 8), (-4, 0, -4)),
        BlockMovable(BlockMovementType.Popped),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockLightDampening(0),
        BlockTagComponent([MinecraftBlockTags.Wood]),
        BlockConnectionRule("none"),
        BlockDestructibleByExplosion(5),
        BlockRedstoneConductivity(False, False),
        BlockPlacementFilter().add_condition(
            [BlockFaceValues.Up, BlockFaceValues.Side]
            if wall_sign
            else [BlockFaceValues.Up]
        ),
        BlockTick((1, 1), True),
        # The text lives in the block entity's dynamic properties
        BlockEntity(dynamic_properties=True),
        # Script: asks for the text when placed, and again when interacted with
        BlockWoodSetSign((8, 9.5, 8.75), text_scale=0.46, wall_sign=wall_sign),
        # Breaks with the block below
        BlockWoodSetSupport(),
    )

    # Its own item stays out of the inventory: the sign item below places it
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
    )

    # Broken, it drops the sign item
    drop = LootTable(f"{wood}_standing_sign")
    drop.pool().entry(f"{namespace}:{wood}_sign")
    drop.queue()
    block.server.components.add(BlockLootTable(drop))

    block.queue()

    # The sign item: places the standing sign, which becomes the wall sign on the side of
    # a block
    sign = Item(f"{wood}_sign")
    sign.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=False),
        ItemDisplayName(display_name),
        ItemIcon(TextureComponents(color=f"{wood}_sign")),
        ItemFuel(10),
    )
    sign.server.description.menu_category(ItemCategory.Items, ItemGroups.Sign)
    sign.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        stick = MinecraftItemTypes.Stick()
        recipe = ShapedCraftingRecipe(f"{wood}_sign")
        recipe.ingredients(
            [[planks, planks, planks], [planks, planks, planks], [None, stick, None]]
        )
        recipe.result(sign.identifier, 3)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
