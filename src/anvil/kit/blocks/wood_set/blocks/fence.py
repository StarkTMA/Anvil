from itertools import product

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
    BlockLeashable,
    BlockLiquidDetection,
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockSupport,
    BlockTagComponent,
    InstanceSpec,
    InstanceVariant,
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
    ItemTagFilter,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags, MinecraftItemTypes
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockLiquidDetectionTouching,
    BlockMaterial,
    BlockSoundGroup,
    CardinalConnectionStates,
    ConnectionTrait,
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

POST = ([4, 24, 4], [-2, 0, -2])
ARMS = {
    CardinalConnectionStates.North: ([2, 24, 6], [-1, 0, -8]),
    CardinalConnectionStates.South: ([2, 24, 6], [-1, 0, 2]),
    CardinalConnectionStates.East: ([6, 24, 2], [-8, 0, -1]),
    CardinalConnectionStates.West: ([6, 24, 2], [2, 0, -1]),
}


def create(
    wood: str,
    selected: set[str],
    *,
    map_color: Color = MAP_COLOR,
    sound_group: BlockSoundGroup | str = BlockSoundGroup.Wood,
) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_fence")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Fence"

    block.server.description.traits.set_connection(
        [ConnectionTrait.CardinalConnections]
    )

    for combo in product([False, True], repeat=len(ARMS)):
        boxes = [POST]
        terms = []
        for direction, connected in zip(ARMS, combo):
            state = Query.BlockState(direction)
            terms.append(state if connected else ~state)
            if connected:
                boxes.append(ARMS[direction])

        size, origin = boxes[0]
        collision = BlockCollisionBox(origin=origin, size=size)
        for size, origin in boxes[1:]:
            collision.add_box(origin=origin, size=size)

        min_x = min(origin[0] for _, origin in boxes)
        min_z = min(origin[2] for _, origin in boxes)
        max_x = max(origin[0] + size[0] for size, origin in boxes)
        max_z = max(origin[2] + size[2] for size, origin in boxes)

        block.server.permutation(" && ".join(terms)).add(
            collision,
            BlockSelectionBox(
                origin=[min_x, 0, min_z], size=[max_x - min_x, 16, max_z - min_z]
            ),
        )

    mining = BlockDestructibleByMining(seconds_to_destroy=3)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    item_visual = BlockItemVisual(blockbench=MODEL, collection="fence_item_visual")
    item_visual.add_material_instance(blockbench=MODEL, texture=f"{wood}_planks")
    item_visual.item_display_transforms(
        merge=False,
        gui=ItemDisplayGuiTransform(
            rotation=[30, -45, 0], scale=[0.625, 0.625, 0.625], fit_to_frame=False
        ),
        firstperson_righthand=ItemDisplayTransform(
            rotation=[0, -45, 0], scale=[0.375, 0.375, 0.375]
        ),
        thirdperson_righthand=ItemDisplayTransform(
            rotation=[70, -45, 0], scale=[0.375, 0.375, 0.375]
        ),
    )
    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(
            blockbench=MODEL,
            collection="fence",
        ).add_bone_visibility(
            fence_north=Query.BlockState(CardinalConnectionStates.North),
            fence_south=Query.BlockState(CardinalConnectionStates.South),
            fence_east=Query.BlockState(CardinalConnectionStates.East),
            fence_west=Query.BlockState(CardinalConnectionStates.West),
        ),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockMovable(movement_type="push"),
        BlockFlammable(),
        BlockLiquidDetection().add_detection_rule(
            on_liquid_touches=BlockLiquidDetectionTouching.NoReaction,
            can_contain_liquid=True,
        ),
        BlockMapColor(color=map_color),
        BlockTagComponent(
            value=[
                MinecraftBlockTags.Wood,
                MinecraftBlockTags.IsAxeItemDestructible,
                MinecraftBlockTags.HasFenceConnections,
            ]
        ),
        BlockConnectionRule(accepts_connections_from="all"),
        BlockDestructibleByExplosion(explosion_resistance=7),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=False, redstone_conductor=False
        ),
        BlockSupport(shape="fence"),
        BlockLeashable(offset=(0, 12, 0)),
        item_visual,
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=15),
    )
    block.item.server.description.set_menu_category(
        ItemCategory.Construction, ItemGroups.Fence
    )

    block.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        stick = MinecraftItemTypes.Stick()
        recipe = ShapedCraftingRecipe(f"{wood}_fence")
        recipe.ingredients([[planks, stick, planks], [planks, stick, planks]])
        recipe.result(block.identifier, 3)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
