from anvil.api.actors.actors import Entity
from anvil.api.actors.components import (
    DamageSensor,
    EntityBodyRotationAlwaysFollowsHead,
    EntityAIRiseToLiquidLevel,
    EntityCollisionBox,
    EntityDamageSensor,
    EntityInventory,
    EntityIsCollidable,
    EntityLeashable,
    EntityMovementType,
    EntityNavigationType,
    EntityPhysics,
    EntityPushableByBlock,
    EntityPushableByEntity,
    EntityRideable,
    EntityTypeFamily,
)
from anvil.api.core.core import CONFIG
from anvil.api.core.enums import (
    ContainerType,
    DamageCause,
    ItemCategory,
    ItemGroups,
    RecipeUnlockContext,
)
from anvil.api.items.components import (
    ItemDisplayName,
    ItemEntityPlacer,
    ItemFuel,
    ItemIcon,
    ItemLiquidClipped,
    ItemMaxStackSize,
)
from anvil.api.items.crafting import ShapelessRecipe
from anvil.api.items.items import Item
from anvil.api.logic.molang import Math, Molang, Query, Variable
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.items import MinecraftItemTypes
from . import BOAT_MODEL

# boat.ts steers, faces and breaks this family
BOAT_FAMILY = "wood_set_boat"
RIDER_ROTATION = 90
SEAT = (0, 0.2, 0.2)
# Degrees per second
TURNING = 20
SHAKE_PER_HIT = 0.25
SHAKE_DECAY = 1
# Must match boat.ts
HITS_WRAP = 16


def create(wood: str, selected: set[str]) -> tuple[Entity, Item]:
    namespace = CONFIG.NAMESPACE
    entity = Entity(f"{wood}_chest_boat")
    display_name = f"{wood.replace('_', ' ').title()} Boat with Chest"

    entity.client.description.geometry(BOAT_MODEL)
    entity.client.description.texture(
        BOAT_MODEL, TextureComponents(color=f"{wood}_boat")
    )
    entity.client.description.material("blend", "entity_alphablend")
    entity.client.description.material("alpha", "entity_alphatest")
    render = entity.client.description.render_controller("default")
    render.geometry(BOAT_MODEL)
    render.textures(f"{wood}_boat")
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
            BOAT_MODEL, animation, True, Query.HasRider() & condition
        )

    # The client can't tell who hit it, so boat.ts counts hits in a synced property
    entity.server.description.add_property.int(
        "hits", (0, HITS_WRAP - 1), client_sync=True
    )
    hits = Query.Property("hits")
    entity.client.description.init_vars(shake_strength=0, last_hits=hits)
    entity.client.description.script(
        Variable.shake_strength,
        Math.clamp(
            Variable.shake_strength
            - Query.DeltaTime() * SHAKE_DECAY
            + (Molang.condition(hits != Variable.last_hits, SHAKE_PER_HIT, 0)),
            0,
            1,
        ),
    )
    entity.client.description.script(Variable.last_hits, hits)
    entity.client.description.animation(
        BOAT_MODEL, "shake", True, Variable.shake_strength > 0
    )

    # Sneaking skips the seat and opens the chest
    rideable = EntityRideable(interact_text="Board")
    rideable.add_seat(SEAT, 1, lock_rider_rotation=RIDER_ROTATION)
    rideable.family_types(["player"])

    entity.server.description.config(summonable=True, spawnable=False)
    entity.server.components.add(
        EntityTypeFamily([BOAT_FAMILY, "boat", "inanimate"]),
        EntityCollisionBox(0.455, 1.4),
        EntityPhysics(True, True),
        EntityAIRiseToLiquidLevel(0, 0.005, 0.005).priority(0),
        EntityNavigationType.Generic(can_sink=False, can_walk=False, can_jump=False),
        EntityMovementType.Basic(),
        # boat.ts turns the head; without this the body lags and snaps on the spot
        EntityBodyRotationAlwaysFollowsHead(),
        rideable,
        EntityInventory(container_type=ContainerType.ChestBoat, inventory_size=27),
        EntityLeashable(),
        EntityDamageSensor().add_trigger(DamageCause.All, DamageSensor.No),
        EntityIsCollidable(),
        EntityPushableByEntity(),
        EntityPushableByBlock(),
    )
    entity.queue(display_name=display_name)

    item = Item(f"{wood}_chest_boat")
    item.server.components.add(
        ItemDisplayName(display_name),
        ItemIcon(TextureComponents(color=f"{wood}_chest_boat")),
        ItemEntityPlacer(entity),
        ItemLiquidClipped(True),
        ItemMaxStackSize(1),
        ItemFuel(60),
    )
    item.server.description.menu_category(ItemCategory.Items, ItemGroups.ChestBoat)
    item.queue()

    if "boat" in selected:
        recipe = ShapelessRecipe(f"{wood}_chest_boat")
        recipe.ingredients([f"{namespace}:{wood}_boat", MinecraftItemTypes.Chest()])
        recipe.result(item.identifier, 1)
        recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
        recipe.queue()

    return entity, item
