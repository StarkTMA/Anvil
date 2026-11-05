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
    BlockMapColor,
    BlockMaterialInstance,
    BlockMovable,
    BlockRedstoneConductivity,
    BlockRedstoneProducer,
    BlockSelectionBox,
    BlockTagComponent,
    BlockTick,
    BlockTransformation,
    InstanceSpec,
    InstanceVariant,
    ItemDisplayGuiTransform,
    ItemDisplayTransform,
    ItemTagFilter,
    MaterialParams,
)
from anvil.api.core.core import CONFIG
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemFuel
from anvil.api.items.crafting import ShapelessRecipe
from anvil.api.logic.molang import Query
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.api.vanilla.items import MinecraftItemTags
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockMaterial,
    BlockSoundGroup,
    FacingDirectionValues,
    ItemCategory,
    ItemGroups,
    PlacementPositionTrait,
    RecipeUnlockContext,
    SupportedBy,
)
from anvil.lib.jsonmodel.types import Color

from ..components import (
    BlockWoodSetSupport,
    BlockWoodSetTogglable,
)
from . import MAP_COLOR, MODEL

AXE_SPEEDS = {
    MinecraftItemTags.WoodenTier: 0.4,
    MinecraftItemTags.StoneTier: 0.2,
    MinecraftItemTags.CopperTier: 0.15,
    MinecraftItemTags.IronTier: 0.15,
    MinecraftItemTags.DiamondTier: 0.1,
    MinecraftItemTags.NetheriteTier: 0.1,
    MinecraftItemTags.GoldenTier: 0.1,
}

FACE_ROTATIONS = {
    FacingDirectionValues.NORTH: (270, 0, 0),
    FacingDirectionValues.SOUTH: (90, 0, 0),
    FacingDirectionValues.WEST: (0, 270, 90),
    FacingDirectionValues.EAST: (0, 90, 270),
    FacingDirectionValues.Down: (180, 0, 0),
    FacingDirectionValues.Up: (0, 0, 0),
}


ON_SOUND = "random.wood_click"
OFF_SOUND = "random.wood_click"


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
    block = Block(f"{wood}_button")
    block.client.sound_group(sound_group)
    display_name = f"{wood.replace('_', ' ').title()} Button"

    block.server.description.traits.set_placement_position(
        [PlacementPositionTrait.BlockFace]
    )
    for direction, rotation in FACE_ROTATIONS.items():
        block.server.permutation(
            Query.BlockState(PlacementPositionTrait.BlockFace) == direction
        ).add(BlockTransformation(rotation=rotation))

    block.server.description.add_state("powered", (False, True))
    block.server.permutation(Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=15, strongly_powered_face=BlockFaceValues.South),
        BlockSelectionBox(origin=(-3, 0, -2), size=(6, 1, 4)),
        BlockTick(interval_range=(20, 20), looping=True),
    )
    block.server.permutation(~Query.BlockState("powered")).add(
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.South),
        BlockSelectionBox(origin=(-3, 0, -2), size=(6, 2, 4)),
    )

    mining = BlockDestructibleByMining(seconds_to_destroy=0.75)
    for tier, speed in AXE_SPEEDS.items():
        mining.add_item_specific_speed(
            item=ItemTagFilter(tags=Query.AllTags([MinecraftItemTags.IsAxe, tier])),
            destroy_speed=speed,
        )

    item_visual = BlockItemVisual(
        blockbench=MODEL,
        collection="button",
    ).add_bone_visibility(button_pressed="0")
    item_visual.add_material_instance(blockbench=MODEL, texture=f"{wood}_planks")
    item_visual.item_display_transforms(
        merge=False,
        gui=ItemDisplayGuiTransform(
            rotation=[110, 0, -135],
            scale=[0.75, 0.75, 0.75],
            fit_to_frame=False,
            translation=[3.5, 1.5, 0],
        ),
        fixed=ItemDisplayTransform(translation=[0, 3.5, 0], rotation=[0, 90, 0]),
        firstperson_righthand=ItemDisplayTransform(
            rotation=[0, 45, 0], translation=[0, 4, 0], scale=[0.4, 0.4, 0.4]
        ),
    )

    block.server.components.add(
        BlockDisplayName(value=display_name),
        mining,
        BlockGeometry(
            blockbench=MODEL,
            collection="button",
        ).add_bone_visibility(
            button_full=~Query.BlockState("powered"),
            button_pressed=Query.BlockState("powered"),
        ),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench=MODEL,
                face=BlockFaceValues.All,
                variations=[InstanceVariant(color=f"{wood}_planks")],
                params=MaterialParams(render_method=BlockMaterial.Opaque),
            )
        ),
        BlockCollisionBox(origin=(-3, 0, -2), size=(6, 2, 4)),
        BlockSelectionBox(origin=(-3, 0, -2), size=(6, 2, 4)),
        BlockMovable(movement_type="popped"),
        BlockFlammable(
            catch_chance_modifier=0, destroy_chance_modifier=0, lava_flammable="never"
        ),
        BlockMapColor(color=map_color),
        BlockTagComponent(
            value=[MinecraftBlockTags.Wood, MinecraftBlockTags.IsAxeItemDestructible]
        ),
        BlockConnectionRule(accepts_connections_from="none"),
        BlockDestructibleByExplosion(explosion_resistance=7),
        BlockRedstoneConductivity(
            allows_wire_to_step_down=False, redstone_conductor=False
        ),
        BlockRedstoneProducer(power=0, strongly_powered_face=BlockFaceValues.South),
        BlockTick(interval_range=(20, 20), looping=False),
        BlockWoodSetTogglable(
            on_interact=True,
            on_sound=on_sound,
            off_sound=off_sound,
        ),
        BlockWoodSetSupport(supported_by=SupportedBy.BlockFace),
        item_visual,
    )

    block.item.server.components.add(
        ItemBlockPlacer(block=block.identifier, replace_block_item=True),
        ItemDisplayName(value=display_name),
        ItemFuel(duration=5),
    )
    block.item.server.description.set_menu_category(ItemCategory.Items, ItemGroups.Buttons)

    block.queue()

    if "planks" in selected:
        recipe = ShapelessRecipe(f"{wood}_button")
        recipe.ingredients([f"{namespace}:{wood}_planks"])
        recipe.result(block.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return block
