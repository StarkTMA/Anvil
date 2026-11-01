from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
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
    ItemTagFilter,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
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
from anvil.lib.lib import Color

from ..components import (
    BlockWoodSetSupport,
    BlockWoodSetTogglable,
    SupportedBy,
)
from . import MAP_COLOR, MODEL

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


# Vanilla's sounds for it, which the script plays when it is stepped on and released
ON_SOUND = "click_on.wooden_pressure_plate"
OFF_SOUND = "click_off.wooden_pressure_plate"


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
    on_sound: str = ON_SOUND,
    off_sound: str = OFF_SOUND,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_pressure_plate")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Pressure Plate"

    block.server.description.traits.placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    block.server.description.add_state("powered", (False, True))
    block.server.permutation(Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=15, strongly_powered_face=BlockFaceValues.Up),
        BlockTransformation(translation=(0, -0.5 / 16, 0)),
        # Ticks only while pressed, to release; idle plates don't tick
        BlockTick(interval_range=(20, 20), looping=True),
    )
    block.server.permutation(~Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.Down),
        BlockTransformation(translation=(0, 0, 0)),
    )

    mining = BlockDestructibleByMining(seconds_to_destroy=2.5)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    geometry = BlockGeometry(blockbench=MODEL, collection="pressure_plate")
    geometry.block_culling(culling_shape="custom").add_rule(
        direction=BlockFaceValues.Down,
        bone="pressure_plate",
        face=BlockFaceValues.Down,
        cube_index=0,
    )

    item_visual = BlockItemVisual(blockbench=MODEL, collection="pressure_plate")
    item_visual.add_material_instance(blockbench=MODEL, texture=f"{wood}_planks")
    item_visual.item_display_transforms(
        merge=False,
        gui=ItemDisplayGuiTransform(
            rotation=[30, 45, 0], scale=[0.625, 0.625, 0.625], fit_to_frame=False
        ),
        fixed=ItemDisplayTransform(translation=[0, 3.5, 0], rotation=[0, 180, 0]),
        firstperson_righthand=ItemDisplayTransform(
            translation=[0, 3, 0], scale=[0.4, 0.4, 0.4]
        ),
        thirdperson_righthand=ItemDisplayTransform(translation=[0, 3, 2.5]),
    )
    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        geometry,
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockCollisionBox(origin=(-7, 0, -7), size=(14, 3.3, 14)),
        BlockSelectionBox(origin=(-7, 0, -7), size=(14, 1, 14)),
        BlockMovable(movement_type="popped"),
        BlockFlammable(),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockTagComponent(
            value=[MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule(accepts_connections_from="none"),
        BlockDestructibleByExplosion(explosion_resistance=7),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=True, redstone_conductor=True
        ),
        # Format 1.26.20+ wants it in the base components too when a permutation sets it
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.Down),
        BlockPlacementFilter().add_condition(
            allowed_faces=[BlockFaceValues.Up, BlockFaceValues.Side]
        ),
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
            use_liquid_clipping=True,
        ),
        # and only the powered permutation above keeps ticking
        # The script's onTick needs a tick in the base components: it ticks once and stops,
        # Scripts: pressed when stepped on and released on tick, broken with its support.
        BlockTick(interval_range=(20, 20), looping=False),
        BlockWoodSetTogglable(
            on_interact=False,
            on_sound=on_sound,
            off_sound=off_sound,
        ),
        BlockWoodSetSupport(supported_by=SupportedBy.BlockFace),
        item_visual,
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=15),
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
