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
    BlockRedstoneConductivity,
    BlockRedstoneConsumer,
    BlockSelectionBox,
    BlockTagComponent,
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
    CardinalDirectionsValues,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
    PlacementPositionTrait,
    RecipeUnlockContext,
    VerticalHalfValues,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.lib import Color

from ..components import (
    BlockWoodSetInteractable,
    BlockWoodSetRedstoneConsumer,
)
from . import MAP_COLOR, MODEL

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

# Rotation (x, y, z) per direction the player is facing
CARDINAL_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}


# Vanilla's sounds for it, which the scripts play when it opens and closes
OPEN_SOUND = "open.wooden_trapdoor"
CLOSE_SOUND = "close.wooden_trapdoor"


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
    open_sound: str = OPEN_SOUND,
    close_sound: str = CLOSE_SOUND,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_trapdoor")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Trapdoor"

    # Rotation: towards the player, y+180 on the bottom half, flipped upside down on the top
    block.server.description.traits.placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    block.server.description.traits.placement_position(
        [PlacementPositionTrait.VerticalHalf]
    )
    half = Query.BlockState(PlacementPositionTrait.VerticalHalf)
    for direction, (x, y, z) in CARDINAL_ROTATIONS.items():
        facing = (
            Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        )
        block.server.permutation(facing & (half == VerticalHalfValues.BOTTOM)).add(
            BlockTransformation(rotation=(x, (y + 180) % 360, z))
        )
        block.server.permutation(facing & (half == VerticalHalfValues.TOP)).add(
            BlockTransformation(rotation=((x + 180) % 360, y, z))
        )

    block.server.description.add_state("open", (False, True))
    block.server.description.add_state("powered", (False, True))
    block.server.permutation(~Query.BlockState("open")).add(
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 3, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 3, 16)),
    )
    block.server.permutation(Query.BlockState("open")).add(
        BlockCollisionBox(origin=(-8, 0, 5), size=(16, 16, 3)),
        BlockSelectionBox(origin=(-8, 0, 5), size=(16, 16, 3)),
    )

    mining = BlockDestructibleByMining(seconds_to_destroy=3)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    item_visual = BlockItemVisual(
        blockbench=MODEL,
        collection="trapdoor",
    ).add_bone_visibility(trapdoor_open="0")
    item_visual.add_material_instance(
        blockbench=MODEL,
        texture=f"{wood}_trapdoor",
        render_method=BlockMaterial.AlphaTestSingleSided,
    )
    item_visual.item_display_transforms(
        merge=False,
        gui=ItemDisplayGuiTransform(translation=[0, 0, 0], fit_to_frame=False),
        fixed=ItemDisplayTransform(translation=[0, 3.5, 0]),
        firstperson_righthand=ItemDisplayTransform(translation=[0, 3, 0]),
        thirdperson_righthand=ItemDisplayTransform(translation=[0, 3.5, 2.2]),
    )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(
            blockbench=MODEL,
            collection="trapdoor",
        ).add_bone_visibility(
            trapdoor_closed=~Query.BlockState("open"),
            trapdoor_open=Query.BlockState("open"),
        ),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_trapdoor")],
                params=MaterialParams(render_method=BlockMaterial.AlphaTestSingleSided),
            )
        ),
        BlockMovable(movement_type="popped"),
        BlockFlammable(),
        # Waterloggable like vanilla Bedrock: water flows into it and stays
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
        ),
        BlockMapColor(color=map_color),
        BlockLightDampening(value=0),
        BlockTagComponent(
            value=[
                MinecraftBlockTags.Wood,
                MinecraftBlockTags.IsAxeItemDestructible,
                MinecraftBlockTags.Trapdoors,
            ]
        ),
        BlockConnectionRule(accepts_connections_from="all"),
        BlockDestructibleByExplosion(explosion_resistance=7),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=False, redstone_conductor=False
        ),
        BlockRedstoneConsumer(min_power=0, propagates_power=True),
        # Scripts: opened by players and by redstone
        BlockWoodSetInteractable(
            open_sound=open_sound,
            close_sound=close_sound,
        ),
        BlockWoodSetRedstoneConsumer(
            open_sound=open_sound,
            close_sound=close_sound,
        ),
        item_visual,
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=15),
    )
    block.item.server.description.menu_category(
        ItemCategory.Construction, ItemGroups.Trapdoor
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_trapdoor")
        recipe.ingredients([[planks, planks, planks], [planks, planks, planks]])
        recipe.result(block.identifier, 2)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
