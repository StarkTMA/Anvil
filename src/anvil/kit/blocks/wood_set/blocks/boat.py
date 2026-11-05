from anvil.api.actors.components import (
    EntityAIRiseToLiquidLevel,
    EntityBodyRotationAlwaysFollowsHead,
    EntityCollisionBox,
    EntityDamageSensor,
    EntityIsCollidable,
    EntityLeashable,
    EntityMovementBasic,
    EntityNavigationGeneric,
    EntityPhysics,
    EntityPushableByBlock,
    EntityPushableByEntity,
    EntityRideable,
    EntityTypeFamily,
)
from anvil.api.actors.entity import Entity
from anvil.api.core.core import CONFIG
from anvil.api.items.components import (
    ItemDisplayName,
    ItemEntityPlacer,
    ItemFuel,
    ItemIcon,
    ItemLiquidClipped,
    ItemMaxStackSize,
)
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.items.items import Item
from anvil.api.logic.molang import Math, Molang, Query, Variable
from anvil.api.pbr.texture_set import TextureComponents
from anvil.lib.jsonmodel.enums import (
    DamageSensor,
    ItemCategory,
    ItemGroups,
    RecipeUnlockContext,
)

from . import BOAT_MODEL

BOAT_FAMILY = "wood_set_boat"
RIDER_ROTATION = 90
SEATS = [(0, 0.2, 0.2), (0, 0.2, -0.6)]
TURNING = 20
SHAKE_PER_HIT = 0.25
SHAKE_DECAY = 1
HITS_WRAP = 16


def create(wood: str, selected: set[str]) -> tuple[Entity, Item]:
    namespace = CONFIG.NAMESPACE
    entity = Entity(f"{wood}_boat")
    display_name = f"{wood.replace('_', ' ').title()} Boat"

    entity.client.description.add_geometry(BOAT_MODEL)
    entity.client.description.add_texture(
        blockbench=BOAT_MODEL, component=TextureComponents(color=f"{wood}_boat")
    )
    entity.client.description.add_material("blend", "entity_alphablend")
    entity.client.description.add_material("alpha", "entity_alphatest")
    render = entity.client.description.render_controller("default")
    render.set_geometry(BOAT_MODEL)
    render.add_texture(f"{wood}_boat")
    render.add_part_visibility("chest", False)
    render.material("*", "alpha")
    render.material("water_clip", "blend")

    yaw_speed = Query.YawSpeed()
    straight = (Math.abs(yaw_speed) <= TURNING) & (Query.GroundSpeed() > 0.5)
    for animation, condition in (
        ("paddle_right", yaw_speed > TURNING),
        ("paddle_left", yaw_speed < -TURNING),
        ("paddle", straight),
    ):
        entity.client.description.animation(
            blockbench=BOAT_MODEL,
            animation_name=animation,
            animate=True,
            condition=Query.HasRider() & condition,
        )

    entity.server.description.add_int_property(
        "hits", (0, HITS_WRAP - 1), client_sync=True
    )
    hits = Query.Property("hits")
    entity.client.description.init_vars(shake_strength=0, last_hits=hits)
    entity.client.description.add_script(
        Variable.shake_strength,
        Math.clamp(
            Variable.shake_strength
            - Query.DeltaTime() * SHAKE_DECAY
            + (Molang.condition(hits != Variable.last_hits, SHAKE_PER_HIT, 0)),
            0,
            1,
        ),
    )
    entity.client.description.add_script(Variable.last_hits, hits)
    entity.client.description.animation(
        blockbench=BOAT_MODEL,
        animation_name="shake",
        animate=True,
        condition=Variable.shake_strength > 0,
    )

    rideable = EntityRideable(
        interact_text="Board", family_types=["player"], seat_count=len(SEATS)
    )
    for min_riders, position in enumerate(SEATS):
        rideable.add_seat(
            position=position,
            max_rider_count=len(SEATS),
            min_rider_count=min_riders,
            lock_rider_rotation=RIDER_ROTATION,
        )

    entity.server.description.config(is_summonable=True, is_spawnable=False)
    entity.server.components.add(
        EntityTypeFamily(family=[BOAT_FAMILY, "boat", "inanimate"]),
        EntityCollisionBox(height=0.455, width=1.4),
        EntityPhysics(push_towards_closest_space=True),
        EntityAIRiseToLiquidLevel(
            priority=0, liquid_y_offset=0, rise_delta=0.005, sink_delta=0.005
        ),
        EntityNavigationGeneric(can_sink=False, can_walk=False, can_jump=False),
        EntityMovementBasic(),
        EntityBodyRotationAlwaysFollowsHead(),
        rideable,
        EntityLeashable(),
        EntityDamageSensor().add_trigger(deals_damage=DamageSensor.No),
        EntityIsCollidable(),
        EntityPushableByEntity(),
        EntityPushableByBlock(),
    )
    entity.set_display_name(display_name).queue()

    item = Item(f"{wood}_boat")
    item.server.components.add(
        ItemDisplayName(value=display_name),
        ItemIcon(textures=TextureComponents(color=f"{wood}_boat")),
        ItemEntityPlacer(entity=entity),
        ItemLiquidClipped(),
        ItemMaxStackSize(value=1),
        ItemFuel(duration=60),
    )
    item.server.description.set_menu_category(ItemCategory.Items, ItemGroups.Boat)
    item.queue()

    if "planks" in selected:
        planks = f"{namespace}:{wood}_planks"
        recipe = ShapedCraftingRecipe(f"{wood}_boat")
        recipe.ingredients([[planks, None, planks], [planks, planks, planks]])
        recipe.result(item.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return entity, item
