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
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockRedstoneConductivity,
    BlockSelectionBox,
    BlockSupport,
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
    CardinalConnectionStates,
    ConnectionTrait,
    ItemCategory,
    ItemGroups,
    RecipeUnlockContext,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags, MinecraftItemTypes
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

# (size, origin) for the central post and each connected arm
POST = ([4, 24, 4], [-2, 0, -2])
ARMS = {
    CardinalConnectionStates.North: ([2, 24, 6], [-1, 0, -8]),
    CardinalConnectionStates.South: ([2, 24, 6], [-1, 0, 2]),
    CardinalConnectionStates.East: ([6, 24, 2], [-8, 0, -1]),
    CardinalConnectionStates.West: ([6, 24, 2], [2, 0, -1]),
}


def create(wood: str, selected: set[str]) -> Block:
    namespace = CONFIG.NAMESPACE
    block = Block(f"{wood}_fence")
    display_name = f"{wood.replace('_', ' ').title()} Fence"

    # Connects to its neighbours, with a collision and selection box per combination
    block.server.description.traits.connection([ConnectionTrait.CardinalConnections])

    for combo in product([False, True], repeat=len(ARMS)):
        boxes = [POST]
        terms = []
        for direction, connected in zip(ARMS, combo):
            state = Query.BlockState(direction)
            terms.append(state if connected else ~state)
            if connected:
                boxes.append(ARMS[direction])

        collision = BlockCollisionBox(*boxes[0])
        for box in boxes[1:]:
            collision.add_box(*box)

        # Selection box: the bounding envelope of the active boxes
        min_x = min(origin[0] for _, origin in boxes)
        min_z = min(origin[2] for _, origin in boxes)
        max_x = max(origin[0] + size[0] for size, origin in boxes)
        max_z = max(origin[2] + size[2] for size, origin in boxes)

        block.server.permutation(" && ".join(terms)).add(
            collision,
            BlockSelectionBox([max_x - min_x, 16, max_z - min_z], [min_x, 0, min_z]),
        )

    mining = BlockDestructibleByMining(3)
    for tier, speed in AXE_SPEEDS.items():
        mining.item_specific_speeds_tag(
            speed, Query.AllTags([MinecraftItemTags.IsAxe, tier])
        )

    item_visual = BlockItemVisual(MODEL, collection="fence_item_visual")
    item_visual.material_instance(MODEL, f"{wood}_planks")
    item_visual.item_display_transforms(
        False,
        gui={
            "rotation": [30, -45, 0],
            "scale": [0.625, 0.625, 0.625],
            "fit_to_frame": False,
        },
        firstperson_righthand={
            "rotation": [0, -45, 0],
            "scale": [0.375, 0.375, 0.375],
        },
        thirdperson_righthand={
            "rotation": [70, -45, 0],
            "scale": [0.375, 0.375, 0.375],
        },
    )
    block.server.components.add(
        BlockDisplayName(display_name),
        mining,
        BlockGeometry(MODEL, collection="fence").bone_visibility(
            fence_north=Query.BlockState(CardinalConnectionStates.North),
            fence_south=Query.BlockState(CardinalConnectionStates.South),
            fence_east=Query.BlockState(CardinalConnectionStates.East),
            fence_west=Query.BlockState(CardinalConnectionStates.West),
        ),
        BlockMaterialInstance().add_instance(
            InstanceSpec(
                blockbench_name=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockMovable(BlockMovementType.Push),
        BlockFlammable(),
        BlockMapColor("#19381F"),
        BlockTagComponent(
            [
                MinecraftBlockTags.Wood,
                MinecraftBlockTags.IsAxeItemDestructible,
                MinecraftBlockTags.HasFenceConnections,
            ]
        ),
        BlockConnectionRule("all"),
        BlockDestructibleByExplosion(7),
        BlockRedstoneConductivity(False, False),
        BlockSupport("fence"),
        BlockLeashable((0, 12, 0)),
        item_visual,
    )

    # Its item: shown in the creative inventory, burns in a furnace
    block.item.server.components.add(
        ItemBlockPlacer(block.identifier, replace_block_item=True),
        ItemDisplayName(display_name),
        ItemFuel(15),
    )
    block.item.server.description.menu_category(
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
