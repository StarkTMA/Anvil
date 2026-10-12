from anvil.api.blocks.blocks import Block, TextureComponents
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
    BlockRedstoneConsumer,
    BlockReplaceable,
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
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockMovementType,
    BlockSoundGroup,
    CardinalDirectionsValues,
    ItemCategory,
    ItemGroups,
    MultiblockPartState,
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
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.lib import Color

from ..components import (
    BlockWoodSetInteractable,
    BlockWoodSetRedstoneConsumer,
    BlockWoodSetSupport,
)
from . import MAP_COLOR, MODEL

# Mining time per axe tier
AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 2.25,
    MinecraftItemTags.StoneTier: 1.15,
    MinecraftItemTags.CopperTier: 0.9,
    MinecraftItemTags.IronTier: 0.75,
    MinecraftItemTags.DiamondTier: 0.6,
    MinecraftItemTags.NetheriteTier: 0.5,
    MinecraftItemTags.GoldenTier: 0.4,
}

# Rotation (x, y, z) per direction the player is facing
CARDINAL_ROTATIONS = {
    CardinalDirectionsValues.NORTH: (0, 0, 0),
    CardinalDirectionsValues.WEST: (0, 90, 0),
    CardinalDirectionsValues.SOUTH: (0, 180, 0),
    CardinalDirectionsValues.EAST: (0, 270, 0),
}


def _material(wood: str, texture: str) -> BlockMaterialInstance:
    return BlockMaterialInstance().add_instance(
        InstanceSpec(
            blockbench_name=MODEL,
            face=BlockFaceValues.All,
            variations=[InstanceVariant(color=texture)],
            params=MaterialParams(render_method=BlockMaterial.AlphaTestSingleSided),
        )
    )


# Vanilla's sounds for it, which the scripts play when it opens and closes
OPEN_SOUND = "open.wooden_door"
CLOSE_SOUND = "close.wooden_door"


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
    block = Block(f"{wood}_door")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Door"

    block.server.description.traits.placement_direction(
        y_rotation_offset=0, traits=[PlacementDirectionTrait.CardinalDirection]
    )
    for direction, rotation in CARDINAL_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementDirectionTrait.CardinalDirection) == direction
        ).add(BlockTransformation().rotation(rotation))

    block.server.description.traits.multi_block("up", 2)
    block.server.description.add_state("open", (False, True))
    block.server.description.add_state("powered", (False, True))

    # Part 0 is the lower half (base texture), part 1 the upper half.
    block.server.permutation(Query.BlockState(MultiblockPartState.Part) == 1).add(
        _material(wood, f"{wood}_door_top")
    )
    block.server.permutation(~Query.BlockState("open")).add(
        BlockCollisionBox((16, 16, 3), (-8, 0, 5)),
        BlockSelectionBox((16, 16, 3), (-8, 0, 5)),
    )
    block.server.permutation(Query.BlockState("open")).add(
        BlockCollisionBox((3, 16, 16), (5, 0, -8)),
        BlockSelectionBox((3, 16, 16), (5, 0, -8)),
    )

    mining = BlockDestructibleByMining(4.5)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(MODEL, collection="door").bone_visibility(
            door_open=Query.BlockState("open"),
            door_closed=~Query.BlockState("open"),
        ),
        _material(wood, f"{wood}_door_bottom"),
        BlockFlammable(),
        # Waterloggable like vanilla Bedrock: water flows into it and stays
        BlockLiquidDetection().add_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
        ),
        BlockMapColor(map_color),
        BlockLightDampening(0),
        BlockTagComponent(
            [MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule("all"),
        BlockMovable(BlockMovementType.Immovable),
        BlockPlacementFilter().add_condition([BlockFaceValues.Up]),
        BlockDestructibleByExplosion(15),
        BlockRedstoneConductivity(False, False),
        BlockRedstoneConsumer(0),
        BlockReplaceable(),
        # Scripts: both halves open together, by players and by redstone; broken with
        # the block below
        BlockWoodSetInteractable(
            multi_part=True,
            open_sound=open_sound,
            close_sound=close_sound,
        ),
        BlockWoodSetRedstoneConsumer(
            multi_part=True,
            open_sound=open_sound,
            close_sound=close_sound,
        ),
        BlockWoodSetSupport(),
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(10),
        ItemIcon(TextureComponents(color=f"{wood}_door")),
    )
    block.item.server.description.menu_category(
        ItemCategory.Construction, ItemGroups.Door
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_door")
        recipe.ingredients([[planks, planks], [planks, planks], [planks, planks]])
        recipe.result(block.identifier, 3)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
