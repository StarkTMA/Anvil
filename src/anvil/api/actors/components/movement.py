from typing import Annotated, Literal

from anvil.api.core.components import EventTrigger
from anvil.api.core.enums import (
    LeashSpringType,
    RideableDismountMode,
)
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.lib.jsonmodel import (
    AtLeastOne,
    Chance,
    InRange,
    JsonComponent,
    JsonObject,
    MetersPerSecond,
    NonNegative,
    RangeMinMax,
    Trigger,
    json_field,
)
from anvil.lib.schemas import (
    MinecraftBlockDescriptor,
    MinecraftEntityDescriptor,
    MinecraftItemDescriptor,
)
from anvil.lib.translator import AnvilTranslator

# region Parts: objects nested inside components


class BoostItem(JsonObject):
    """An item that boosts a ridden entity.

    Args:
        item (str | MinecraftItemDescriptor): The item that can be used to boost.
        damage (int, optional): The damage the item takes each time it is used.
        replace_item (str | MinecraftItemDescriptor, optional): The item the boost item becomes once it is used up.
    """

    item: str | MinecraftItemDescriptor = json_field()
    damage: int | None = json_field(default=None)
    replace_item: str | MinecraftItemDescriptor | None = json_field(default=None)


class JumpData(JsonObject):
    """Jump data of `minecraft:jump.dynamic`.

    Args:
        animation_duration (int, optional): Duration of the jump animation. Game default 1.
        distance_scale (float, optional): The multiplier applied to horizontal velocity when jumping. Game default 1.
        height (float, optional): The force applied vertically when jumping. Game default 0.1.
        jump_delay (int, optional): Ticks between sequential jumps. Game default 30.
    """

    animation_duration: int | None = json_field(default=None)
    distance_scale: float | None = json_field(default=None)
    height: float | None = json_field(default=None)
    jump_delay: int | None = json_field(default=None)


class PreferredPathBlocks(JsonObject):
    """Blocks a mob prefers to walk on, and their pathfinding cost.

    Args:
        cost (float): Cost of walking on these blocks.
        blocks (list[str | MinecraftBlockDescriptor]): The blocks.
    """

    cost: float = json_field()
    blocks: list[str | MinecraftBlockDescriptor] = json_field()


class Rider(JsonObject):
    """A rider `minecraft:addrider` adds.

    Args:
        entity_type (MinecraftEntityDescriptor | str): The entity type that rides this entity.
        spawn_event (str, optional): The spawn event used when the rider is created.
    """

    entity_type: MinecraftEntityDescriptor | str = json_field()
    spawn_event: str | None = json_field(default=None)


class EntityMovementControl(JsonComponent, abstract=True):
    """Base of the move controls (`minecraft:movement.*`).

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.
    """

    max_turn: Annotated[float, NonNegative] | None = json_field(default=None)


class EntityNavigation(JsonComponent, abstract=True):
    """Base of the navigation components (`minecraft:navigation.*`): how the pathfinder plans paths.

    Args:
        avoid_damage_blocks (bool, optional): Avoids blocks that cause damage. Game default false.
        avoid_portals (bool, optional): Avoids portals. Game default false.
        avoid_sun (bool, optional): Avoids blocks exposed to the sun. Game default false.
        avoid_water (bool, optional): Avoids water. Game default false.
        blocks_to_avoid (list[str | MinecraftBlockDescriptor], optional): Blocks the pathfinder avoids.
        can_breach (bool, optional): Can jump out of water, like a dolphin. Game default false.
        can_break_doors (bool, optional): Can path through a closed door, breaking it. Game default false.
        can_float (bool, optional): Can float in water.
        can_jump (bool, optional): Can jump up blocks. Game default true.
        can_open_doors (bool, optional): Can path through a closed door, opening it. Game default false.
        can_open_iron_doors (bool, optional): Can path through a closed iron door, opening it. Game default false.
        can_pass_doors (bool, optional): Can path through doors. Game default true.
        can_path_from_air (bool, optional): Can start pathing while in the air. Game default false.
        can_path_over_lava (bool, optional): Can travel on the surface of lava. Game default false.
        can_path_over_water (bool, optional): Can travel on the surface of water. Game default false.
        can_sink (bool, optional): Is pulled down by gravity in water. Game default true.
        can_swim (bool, optional): Can path anywhere through water, with the swimming animation. Game default false.
        can_walk (bool, optional): Can walk on the ground outside water. Game default true.
        can_walk_in_lava (bool, optional): Can travel in lava like on ground. Game default false.
        is_amphibious (bool, optional): Can walk on the ground under water. Game default false.
    """

    avoid_damage_blocks: bool | None = json_field(default=None)
    avoid_portals: bool | None = json_field(default=None)
    avoid_sun: bool | None = json_field(default=None)
    avoid_water: bool | None = json_field(default=None)
    blocks_to_avoid: list[str | MinecraftBlockDescriptor] | None = json_field(
        default=None
    )
    can_breach: bool | None = json_field(default=None)
    can_break_doors: bool | None = json_field(default=None)
    can_float: bool | None = json_field(default=None)
    can_jump: bool | None = json_field(default=None)
    can_open_doors: bool | None = json_field(default=None)
    can_open_iron_doors: bool | None = json_field(default=None)
    can_pass_doors: bool | None = json_field(default=None)
    can_path_from_air: bool | None = json_field(default=None)
    can_path_over_lava: bool | None = json_field(default=None)
    can_path_over_water: bool | None = json_field(default=None)
    can_sink: bool | None = json_field(default=None)
    can_swim: bool | None = json_field(default=None)
    can_walk: bool | None = json_field(default=None)
    can_walk_in_lava: bool | None = json_field(default=None)
    is_amphibious: bool | None = json_field(default=None)


class LeashPreset(JsonObject):
    """How an entity behaves while leashed, when the preset's filter matches.

    Args:
        filter (Filter, optional): Conditions for this preset to apply.
        hard_distance (float, optional): Distance in blocks beyond which the entity is pulled towards the holder. Game default 7.
        max_distance (float, optional): Distance in blocks at which the leash breaks. Game default 12.
        rotation_adjustment (float, optional): Adjusts the rotation at which a dampened spring reaches equilibrium. Game default 0.
        soft_distance (float, optional): Distance in blocks beyond which the entity pathfinds towards the holder. Game default 4.
        spring_type (LeashSpringType, optional): The spring force pulling the entity to its holder. Game default dampened.
    """

    filter: Filter | None = json_field(default=None)
    hard_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    max_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    rotation_adjustment: float | None = json_field(default=None)
    soft_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    spring_type: LeashSpringType | None = json_field(default=None)


class Seat(JsonObject):
    """A seat of `minecraft:rideable`.

    Args:
        position (tuple[float, float, float]): Position of the seat relative to the entity.
        max_rider_count (int): The seat is used while the rider count is at most this.
        min_rider_count (int, optional): The seat is used once the rider count is at least this. Game default 0.
        lock_rider_rotation (float, optional): Angle in degrees a rider can turn. Without it, riders turn freely.
        rotate_rider_by (float | Molang | str, optional): Offset to rotate riders by. Game default 0.
        third_person_camera_radius (float, optional): Radius of the third person cameras for a player in this seat, from 1 to 64.
        camera_relax_distance_smoothing (float, optional): Smoothing of the camera returning to its full distance after an obstacle.
    """

    position: tuple[float, float, float] = json_field()
    max_rider_count: Annotated[int, NonNegative] = json_field()
    min_rider_count: Annotated[int, NonNegative] | None = json_field(default=None)
    lock_rider_rotation: float | None = json_field(default=None)
    rotate_rider_by: float | Molang | str | None = json_field(default=None)
    third_person_camera_radius: Annotated[float, InRange(1, 64)] | None = json_field(
        default=None
    )
    camera_relax_distance_smoothing: float | None = json_field(default=None)


# endregion

# region Components


class EntityAddRider(JsonComponent):
    """Adds riders to the entity. Requires `minecraft:rideable`.

    Args:
        riders (list[Rider], optional): The riders to add. Can only spawn as many riders as `minecraft:rideable` has seats. Add more with `add_rider`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_addrider)
    """

    identifier = "minecraft:addrider"

    riders: list[Rider] = json_field(default_factory=list, omit_default=True)

    def add_rider(
        self,
        *,
        entity_type: MinecraftEntityDescriptor | str,
        spawn_event: str | None = None,
    ) -> "EntityAddRider":
        """Adds a rider.

        Args:
            entity_type (MinecraftEntityDescriptor | str): The entity type that rides this entity.
            spawn_event (str, optional): The spawn event used when the rider is created.
        """
        self.riders.append(Rider(entity_type=entity_type, spawn_event=spawn_event))
        return self


class EntityBalloonable(JsonComponent):
    """Allows this entity to have a balloon attached, and defines what happens when it is ballooned.

    Args:
        mass (float, optional): Mass used when computing balloon pull forces. Game default 1.
        max_distance (float, optional): Distance in blocks at which the balloon breaks. Game default 10.
        soft_distance (float, optional): Distance in blocks at which the 'spring' effect lifts it. Game default 2.
        on_balloon (EventTrigger | str, optional): Event to run when this entity is ballooned.
        on_unballoon (EventTrigger | str, optional): Event to run when this entity is unballooned.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_balloonable)
    """

    identifier = "minecraft:balloonable"

    mass: Annotated[float, NonNegative] | None = json_field(default=None)
    max_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    soft_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    on_balloon: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    on_unballoon: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )


class EntityBlockClimber(JsonComponent):
    """Allows the player to detect and manuever on the scaffolding block.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_block_climber)
    """

    identifier = "minecraft:block_climber"


class EntityBodyRotationAlwaysFollowsHead(JsonComponent):
    """Causes the entity's body rotation to match the one of their head. Does not override the "minecraft:body_rotation_blocked" component.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_always_follows_head)
    """

    identifier = "minecraft:body_rotation_always_follows_head"


class EntityBodyRotationBlocked(JsonComponent):
    """When set, the entity will no longer visually rotate their body to match their facing direction.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_blocked)
    """

    identifier = "minecraft:body_rotation_blocked"


class EntityBoostable(JsonComponent):
    """Defines the conditions and behavior of a rideable entity's boost.

    Args:
        boost_items (list[BoostItem], optional): Items that boost while riding this entity. Add more with `add_boost_item`.
        duration (float, optional): Seconds the boost lasts. Game default 3.
        speed_multiplier (float, optional): Factor by which the entity's speed increases. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boostable)
    """

    identifier = "minecraft:boostable"

    boost_items: list[BoostItem] = json_field(default_factory=list, omit_default=True)
    duration: Annotated[float, NonNegative] | None = json_field(default=None)
    speed_multiplier: Annotated[float, NonNegative] | None = json_field(default=None)

    def add_boost_item(
        self,
        *,
        item: str | MinecraftItemDescriptor,
        damage: int | None = None,
        replace_item: str | MinecraftItemDescriptor | None = None,
    ) -> "EntityBoostable":
        """Adds an item that boosts the entity. See `BoostItem` for the parameters."""
        self.boost_items.append(
            BoostItem(item=item, damage=damage, replace_item=replace_item)
        )
        return self


class EntityBuoyant(JsonComponent):
    """Enables an entity to float on the given liquid blocks.

    Args:
        liquid_blocks (list[str | MinecraftBlockDescriptor]): Blocks this entity can float on. Must be liquid blocks.
        apply_gravity (bool, optional): Applies gravity each tick. Game default true.
        base_buoyancy (float, optional): Base buoyancy used to calculate how much the entity floats. Game default 1.
        big_wave_probability (float, optional): Probability of a big wave hitting the entity, with `movement_type` waves. Game default 0.03.
        big_wave_speed (float, optional): Speed multiplier of a big wave. Game default 10.
        can_auto_step_from_liquid (bool, optional): Whether the entity can step out of a liquid onto a solid block. Game default false.
        drag_down_on_buoyancy_removed (float, optional): How much the entity is dragged down when the component is removed. Game default 0.
        movement_type (Literal["waves", "bobbing", "none"], optional): Type of vertical movement applied to the entity. Game default waves.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_buoyant)
    """

    identifier = "minecraft:buoyant"

    liquid_blocks: list[str | MinecraftBlockDescriptor] = json_field()
    apply_gravity: bool | None = json_field(default=None)
    base_buoyancy: float | None = json_field(default=None)
    big_wave_probability: Annotated[float, Chance] | None = json_field(default=None)
    big_wave_speed: float | None = json_field(default=None)
    can_auto_step_from_liquid: bool | None = json_field(default=None)
    drag_down_on_buoyancy_removed: float | None = json_field(default=None)
    movement_type: Literal["waves", "bobbing", "none"] | None = json_field(default=None)


class EntityCanClimb(JsonComponent):
    """Allows an entity to climb ladders.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_climb)
    """

    identifier = "minecraft:can_climb"


class EntityCanFly(JsonComponent):
    """Marks the entity as being able to fly, the pathfinder won't be restricted to paths where a solid block is required underneath it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_fly)
    """

    identifier = "minecraft:can_fly"


class EntityCanPowerJump(JsonComponent):
    """Allows the entity to power jump like the Horse does in Vanilla.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_power_jump)
    """

    identifier = "minecraft:can_power_jump"


class EntityCanStandOnPowderSnow(JsonComponent):
    """Allows this entity to stand on powder snow without sinking. Not in the Microsoft reference."""

    identifier = "minecraft:can_stand_on_powder_snow"


class EntityDash(JsonComponent):
    """Ability for a rideable entity to dash.

    Args:
        cooldown_time (float, optional): The dash cooldown in seconds. Default value is 1.000000. Game default 1.
        horizontal_momentum (float, optional): Horizontal momentum of the dash. Game default 1.
        vertical_momentum (float, optional): Vertical momentum of the dash. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash)
    """

    identifier = "minecraft:dash"

    cooldown_time: float | None = json_field(default=None)
    horizontal_momentum: float | None = json_field(default=None)
    vertical_momentum: float | None = json_field(default=None)


class EntityDashAction(JsonComponent):
    """Ability for a rideable entity to dash.

    Args:
        can_dash_underwater (bool, optional): Whether the entity can dash underwater. Game default false.
        cooldown_time (float, optional): The dash cooldown in seconds. Game default 1.
        direction (Literal['entity', 'passenger'], optional): Should the momentum be applied in the direction of the 'entity' or 'passenger'. Game default entity.
        horizontal_momentum (float, optional): Horizontal momentum of the dash. Game default 1.
        vertical_momentum (float, optional): Vertical momentum of the dash. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash_action)
    """

    identifier = "minecraft:dash_action"

    can_dash_underwater: bool | None = json_field(default=None)
    cooldown_time: float | None = json_field(default=None)
    direction: Literal["entity", "passenger"] | None = json_field(default=None)
    horizontal_momentum: float | None = json_field(default=None)
    vertical_momentum: float | None = json_field(default=None)


class EntityDefaultLookAngle(JsonComponent):
    """Sets this entity's default head rotation angle.

    Args:
        value (float, optional): Angle in degrees. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_default_look_angle)
    """

    identifier = "minecraft:default_look_angle"

    value: float | None = json_field(default=None)


class EntityFloatsInLiquid(JsonComponent):
    """Sets that this entity can float in liquid blocks.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_floats_in_liquid)
    """

    identifier = "minecraft:floats_in_liquid"


class EntityFlocking(JsonComponent):
    """Allows entities to flock in groups in water or not.

    Args:
        block_distance (float, optional): The amount of blocks away the entity will look at to push away from. Game default 0.
        block_weight (float, optional): The weight of the push back away from blocks. Game default 0.
        breach_influence (float, optional): The amount of push back given to a flocker that breaches out of the water. Game default 0.
        cohesion_threshold (float, optional): The threshold in which to start applying cohesion. Game default 1.
        cohesion_weight (float, optional): The weight applied for the cohesion steering of the flock. Game default 1.
        goal_weight (float, optional): The weight on which to apply on the goal output. Game default 0.
        high_flock_limit (int, optional): Determines the high bound amount of entities that can be allowed in the flock. Game default 0.
        in_water (bool, optional): Tells the Flocking Component if the entity exists in water. Game default false.
        influence_radius (float, optional): The area around the entity that allows others to be added to the flock. Game default 0.
        innner_cohesion_threshold (float, optional): The distance in which the flocker will stop applying cohesion. Game default 0.
        loner_chance (float, optional): The percentage chance between 0-1 that a fish will spawn and not want to join flocks. Invalid values will be capped at the end points. Game default 0.
        low_flock_limit (int, optional): Determines the low bound amount of entities that can be allowed in the flock. Game default 0.
        match_variants (bool, optional): Tells the flockers that they can only match similar entities that also match the variant, mark variants, and color data of the other potential flockers. Game default false.
        max_height (float, optional): The max height allowable in the air or water. Game default 0.
        min_height (float, optional): The min height allowable in the air or water. Game default 0.
        separation_threshold (float, optional): The distance that is determined to be to close to another flocking and to start applying separation. Game default 2.
        separation_weight (float, optional): The weight applied to the separation of the flock. Game default 1.
        use_center_of_mass (bool, optional): Tells the flockers that they will follow flocks based on the center of mass. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flocking)
    """

    identifier = "minecraft:flocking"

    block_distance: float | None = json_field(default=None)
    block_weight: float | None = json_field(default=None)
    breach_influence: float | None = json_field(default=None)
    cohesion_threshold: float | None = json_field(default=None)
    cohesion_weight: float | None = json_field(default=None)
    goal_weight: float | None = json_field(default=None)
    high_flock_limit: int | None = json_field(default=None)
    in_water: bool | None = json_field(default=None)
    influence_radius: float | None = json_field(default=None)
    innner_cohesion_threshold: float | None = json_field(default=None)
    loner_chance: float | None = json_field(default=None)
    low_flock_limit: int | None = json_field(default=None)
    match_variants: bool | None = json_field(default=None)
    max_height: float | None = json_field(default=None)
    min_height: float | None = json_field(default=None)
    separation_threshold: float | None = json_field(default=None)
    separation_weight: float | None = json_field(default=None)
    use_center_of_mass: bool | None = json_field(default=None)


class EntityFlyingSpeed(JsonComponent):
    """Speed in Blocks that this entity flies at.

    Args:
        value (float): Flying speed in blocks per tick. Game default 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flying_speed)
    """

    identifier = "minecraft:flying_speed"

    value: float = json_field()


class EntityFlyingSpeedMeters(EntityFlyingSpeed):
    """`minecraft:flying_speed` with the speed given in blocks per second, converted to the game's flying speed value.

    Args:
        value (float): Flying speed in blocks per second.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flying_speed)
    """

    value: Annotated[float, MetersPerSecond(2)] = json_field()


class EntityFreeCameraControlled(JsonComponent):
    """When configured as a rideable entity, the entity will be controlled using WASD controls and mouse to move in three dimensions.

    Args:
        backwards_movement_modifier (float, optional): Modifies speed going backwards. Game default 0.5.
        strafe_speed_modifier (float, optional): Modifies the strafe speed. Game default 0.4.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_free_camera_controlled)
    """

    identifier = "minecraft:free_camera_controlled"

    backwards_movement_modifier: float | None = json_field(default=None)
    strafe_speed_modifier: float | None = json_field(default=None)


class EntityGroundOffset(JsonComponent):
    """Sets the offset from the ground that the entity is actually at.

    Args:
        value (float, optional): The value of the entity's offset from the terrain, in blocks. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ground_offset)
    """

    identifier = "minecraft:ground_offset"

    value: float | None = json_field(default=None)


class EntityHide(JsonComponent):
    """Moves to and hides at their owned POI or the closest nearby.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_hide)
    """

    identifier = "minecraft:hide"


class EntityHome(JsonComponent):
    """Saves a home position for when the entity is spawned.

    Args:
        home_block_list (list[str | MinecraftBlockDescriptor], optional): Blocks that can be a valid home.
        restriction_radius (int, optional): Radius the entity is restricted to around its home. Game default 0.
        restriction_type (Literal["none", "random_movement", "all_movement"], optional): How the entity is restricted to its home. Game default none.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_home)
    """

    identifier = "minecraft:home"

    home_block_list: list[str | MinecraftBlockDescriptor] | None = json_field(
        default=None
    )
    restriction_radius: Annotated[int, NonNegative] | None = json_field(default=None)
    restriction_type: Literal["none", "random_movement", "all_movement"] | None = (
        json_field(default=None)
    )


class EntityHorseJumpStrength(JsonComponent):
    """Determines the jump height for a horse or similar entity, like a donkey.

    Args:
        value (float | tuple[float, float]): Jump strength the entity has when spawned, or a `(min, max)` range to pick it from.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_horse.jump_strength)
    """

    identifier = "minecraft:horse.jump_strength"

    value: Annotated[float | tuple[float, float], RangeMinMax] = json_field()


class EntityInputAirControlled(JsonComponent):
    """When configured as a rideable entity, the entity will be controlled using WASD controls and mouse to move in three dimensions.

    Args:
        backwards_movement_modifier (float, optional): Modifies speed going backwards. Game default 0.5.
        strafe_speed_modifier (float, optional): Modifies the strafe speed. Game default 0.4.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_input_air_controlled)
    """

    identifier = "minecraft:input_air_controlled"

    backwards_movement_modifier: float | None = json_field(default=None)
    strafe_speed_modifier: float | None = json_field(default=None)


class EntityInputGroundControlled(JsonComponent):
    """When configured as a rideable entity, the entity will be controlled using WASD controls. Beginning with 1.19.50 the default auto step height for rideable entities is half a block. Consider adding the "minecraft:variable_max_auto_step" component to increase it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_input_ground_controlled)
    """

    identifier = "minecraft:input_ground_controlled"


class EntityItemControllable(JsonComponent):
    """Defines what items can be used to control this entity while ridden.

    Args:
        control_items (list[str | MinecraftItemDescriptor], optional): The items that can be used to control this entity while ridden. Add more with `add_control_items`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_controllable)
    """

    identifier = "minecraft:item_controllable"

    control_items: list[str | MinecraftItemDescriptor] = json_field(
        default_factory=list, omit_default=True
    )

    def add_control_items(
        self, *items: str | MinecraftItemDescriptor
    ) -> "EntityItemControllable":
        """Adds items that control the entity."""
        self.control_items.extend(items)
        return self


class EntityJumpDynamic(JsonComponent):
    """A jump control that changes jump properties with the speed modifier of the mob. Requires `minecraft:movement.skip`.

    Args:
        regular_skip_data (JumpData, optional): Jump data used during normal skip movement. Set it with `set_regular_skip_data`.
        fast_skip_data (JumpData, optional): Jump data used while traveling quickly with skip movement. Set it with `set_fast_skip_data`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_jump.dynamic)
    """

    identifier = "minecraft:jump.dynamic"

    regular_skip_data: JumpData | None = json_field(default=None)
    fast_skip_data: JumpData | None = json_field(default=None)

    def set_fast_skip_data(
        self,
        *,
        animation_duration: int | None = None,
        distance_scale: float | None = None,
        height: float | None = None,
        jump_delay: int | None = None,
    ) -> "EntityJumpDynamic":
        """Sets the jump data used while traveling quickly with skip movement. See `JumpData` for the parameters."""
        self.fast_skip_data = JumpData(
            animation_duration=animation_duration,
            distance_scale=distance_scale,
            height=height,
            jump_delay=jump_delay,
        )
        return self

    def set_regular_skip_data(
        self,
        *,
        animation_duration: int | None = None,
        distance_scale: float | None = None,
        height: float | None = None,
        jump_delay: int | None = None,
    ) -> "EntityJumpDynamic":
        """Sets the jump data used during normal skip movement. See `JumpData` for the parameters."""
        self.regular_skip_data = JumpData(
            animation_duration=animation_duration,
            distance_scale=distance_scale,
            height=height,
            jump_delay=jump_delay,
        )
        return self


class EntityJumpStatic(JsonComponent):
    """Gives the entity the ability to jump.

    Args:
        jump_power (float, optional): The initial vertical velocity for the jump. Game default 0.42.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_jump.static)
    """

    identifier = "minecraft:jump.static"

    jump_power: float | None = json_field(default=None)


class EntityLavaMovement(JsonComponent):
    """Allows a custom movement speed across lava blocks.

    Args:
        value (float): The speed the mob moves over a lava block.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_lava_movement)
    """

    identifier = "minecraft:lava_movement"

    value: float = json_field()


class EntityLeashable(JsonComponent):
    """Allows the entity to be leashed.

    Args:
        can_be_cut (bool, optional): Players can cut the entity's leashes with shears. Game default true.
        can_be_stolen (bool, optional): Players can leash the entity while it is leashed to another. Game default false.
        hard_distance (int, optional): Distance in blocks at which the leash stiffens. Game default 6.
        max_distance (int, optional): Distance in blocks at which the leash breaks.
        on_leash (EventTrigger | str, optional): Event to run when the entity is leashed.
        on_unleash (EventTrigger | str, optional): Event to run when the entity is unleashed.
        on_unleash_interact_only (bool, optional): `on_unleash` runs only when a player unleashes the entity. Game default false.
        presets (list[LeashPreset], optional): How the entity behaves while leashed; the first matching preset applies. Add more with `add_preset`.
        soft_distance (int, optional): Distance in blocks at which the spring starts pulling the entity. Game default 4.
        unleash_on_removal (bool, optional): The entity is unleashed when this component is removed. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable)
    """

    identifier = "minecraft:leashable"

    can_be_cut: bool | None = json_field(default=None)
    can_be_stolen: bool | None = json_field(default=None)
    hard_distance: Annotated[int, NonNegative] | None = json_field(default=None)
    max_distance: Annotated[int, NonNegative] | None = json_field(default=None)
    on_leash: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    on_unleash: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    on_unleash_interact_only: bool | None = json_field(default=None)
    presets: list[LeashPreset] = json_field(default_factory=list, omit_default=True)
    soft_distance: Annotated[int, NonNegative] | None = json_field(default=None)
    unleash_on_removal: bool | None = json_field(default=None)

    def add_preset(
        self,
        *,
        filter: Filter | None = None,
        hard_distance: float | None = None,
        max_distance: float | None = None,
        rotation_adjustment: float | None = None,
        soft_distance: float | None = None,
        spring_type: LeashSpringType | None = None,
    ) -> "EntityLeashable":
        """Adds a preset. See `LeashPreset` for the parameters."""
        self.presets.append(
            LeashPreset(
                filter=filter,
                hard_distance=hard_distance,
                max_distance=max_distance,
                rotation_adjustment=rotation_adjustment,
                soft_distance=soft_distance,
                spring_type=spring_type,
            )
        )
        return self


class EntityLeashableTo(JsonComponent):
    """Allows players to leash entities to this entity, retrieve entities already leashed to it, or free them using shears. For the last interaction to work, the leashed entities must have "can_be_cut" set to true in their "minecraft:leashable" component.

    Args:
        can_retrieve_from (bool, optional): Allows players to retrieve entities that are leashed to this entity. Game default false.
        unleash_on_removal (bool, optional): If true, all entities leashed to this entity are automatically unleashed when this component is removed. Defaults to true. This item requires a format version of at least 1.26.30. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable_to)
    """

    identifier = "minecraft:leashable_to"

    can_retrieve_from: bool | None = json_field(default=None)
    unleash_on_removal: bool | None = json_field(default=None)


class EntityMovement(JsonComponent):
    """Defines the base movement speed of an entity. Typical values: creeper (0.2), cow (0.25), zombie baby (0.35).

    Args:
        value (float | tuple[float, float]): The base movement speed, or a `(min, max)` range to pick it from. Higher values result in faster movement.
        max (float, optional): Maximum movement speed this entity can have.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement)
    """

    identifier = "minecraft:movement"

    value: Annotated[float | tuple[float, float], RangeMinMax] = json_field()
    max: float | None = json_field(default=None)


class EntityMovementAmphibious(EntityMovementControl):
    """Move control that lets the mob swim in water and walk on land.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.amphibious)
    """

    identifier = "minecraft:movement.amphibious"


class EntityMovementBasic(EntityMovementControl):
    """Basic move control.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.basic)
    """

    identifier = "minecraft:movement.basic"


class EntityMovementDolphin(JsonComponent):
    """Move control in a dolphin-like style. Not used by the game at the moment.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.dolphin)
    """

    identifier = "minecraft:movement.dolphin"


class EntityMovementFly(EntityMovementControl):
    """Move control that makes the mob fly.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.
        speed_when_turning (float, optional): Speed the mob slows to when it turns sharply. Game default 0.2.
        start_speed (float, optional): Initial speed of the mob. Game default 0.1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.fly)
    """

    identifier = "minecraft:movement.fly"

    speed_when_turning: float | None = json_field(default=None)
    start_speed: float | None = json_field(default=None)


class EntityMovementGeneric(EntityMovementControl):
    """Move control that lets the mob fly, swim, climb and so on.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.generic)
    """

    identifier = "minecraft:movement.generic"


class EntityMovementGlide(EntityMovementControl):
    """Move control of a flying mob that glides.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.
        speed_when_turning (float, optional): Speed the mob slows to when it turns sharply. Game default 0.2.
        start_speed (float, optional): Initial speed of the mob when it starts gliding. Game default 0.1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.glide)
    """

    identifier = "minecraft:movement.glide"

    speed_when_turning: float | None = json_field(default=None)
    start_speed: float | None = json_field(default=None)


class EntityMovementHover(EntityMovementControl):
    """Move control that makes the mob hover.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.hover)
    """

    identifier = "minecraft:movement.hover"


class EntityMovementJump(EntityMovementControl):
    """Move control that makes the mob jump as it moves, with a delay between jumps.

    To follow targets, the entity also needs `minecraft:behavior.slime_attack`.

    Args:
        jump_delay (float | tuple[float, float], optional): Seconds after landing before the next jump, or a `(min, max)` range. Game default 0.
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.jump)
    """

    identifier = "minecraft:movement.jump"

    jump_delay: Annotated[float | tuple[float, float], RangeMinMax] | None = json_field(
        default=None
    )


class EntityMovementMeters(EntityMovement):
    """`minecraft:movement` with the speed given in blocks per second, converted to the game's movement value.

    Args:
        value (float | tuple[float, float]): The base movement speed in blocks per second, or a `(min, max)` range to pick it from.
        max (float, optional): Maximum movement speed in blocks per second.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement)
    """

    value: Annotated[float | tuple[float, float], MetersPerSecond(4), RangeMinMax] = (
        json_field()
    )
    max: Annotated[float, MetersPerSecond(4), RangeMinMax] | None = json_field(
        default=None
    )


class EntityMovementSkip(EntityMovementControl):
    """Move control that makes the mob hop as it moves.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.skip)
    """

    identifier = "minecraft:movement.skip"


class EntityMovementSoundDistanceOffset(JsonComponent):
    """Sets the offset used to determine the next step distance for playing a movement sound.

    Args:
        value (float): The higher the number, the less often the movement sound will be played. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.sound_distance_offset)
    """

    identifier = "minecraft:movement_sound_distance_offset"

    value: float = json_field()


class EntityMovementSway(EntityMovementControl):
    """Move control that makes the mob sway side to side, as if swimming.

    Args:
        max_turn (float, optional): Maximum degrees the mob can turn per tick. Game default 30.
        sway_amplitude (float, optional): Strength of the sway. Game default 0.05.
        sway_frequency (float, optional): Multiplier of the sway frequency. Game default 0.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.sway)
    """

    identifier = "minecraft:movement.sway"

    sway_amplitude: float | None = json_field(default=None)
    sway_frequency: float | None = json_field(default=None)


class EntityNavigationClimb(EntityNavigation):
    """Generates paths that include vertical walls, like spiders.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.climb)
    """

    identifier = "minecraft:navigation.climb"


class EntityNavigationFloat(EntityNavigation):
    """Generates paths by flying around in the air, like ghasts.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.float)
    """

    identifier = "minecraft:navigation.float"


class EntityNavigationFly(EntityNavigation):
    """Generates paths in the air, like parrots.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.fly)
    """

    identifier = "minecraft:navigation.fly"


class EntityNavigationGeneric(EntityNavigation):
    """Generates paths by walking, swimming, flying and climbing, and jumping up and down a block.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.generic)
    """

    identifier = "minecraft:navigation.generic"


class EntityNavigationHover(EntityNavigation):
    """Generates paths in the air with predictive movement, like bees.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.hover)
    """

    identifier = "minecraft:navigation.hover"


class EntityNavigationSwim(EntityNavigation):
    """Generates paths that include water.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.swim)
    """

    identifier = "minecraft:navigation.swim"


class EntityNavigationWalk(EntityNavigation):
    """Generates paths by walking.

    Args:
        See `EntityNavigation`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_navigation.walk)
    """

    identifier = "minecraft:navigation.walk"


class EntityPreferredPath(JsonComponent):
    """Specifies costing information for mobs that prefer to walk on preferred paths.

    Args:
        default_block_cost (float, optional): Cost for non-preferred blocks. Game default 0.
        jump_cost (float, optional): Added cost for jumping up a node. Game default 0.
        max_fall_blocks (int, optional): Distance the mob can fall without taking damage. Game default 3.
        preferred_path_blocks (list[PreferredPathBlocks], optional): Blocks and their costs. Add more with `add_preferred_path_blocks`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_preferred_path)
    """

    identifier = "minecraft:preferred_path"

    default_block_cost: float | None = json_field(default=None)
    jump_cost: float | None = json_field(default=None)
    max_fall_blocks: int | None = json_field(default=None)
    preferred_path_blocks: list[PreferredPathBlocks] = json_field(
        default_factory=list, omit_default=True
    )

    def add_preferred_path_blocks(
        self, *, cost: float, blocks: list[str | MinecraftBlockDescriptor]
    ) -> "EntityPreferredPath":
        """Adds blocks and their cost. See `PreferredPathBlocks`."""
        self.preferred_path_blocks.append(PreferredPathBlocks(cost=cost, blocks=blocks))
        return self


class EntityRailMovement(JsonComponent):
    """Defines the entity's movement on the rails. An entity with this component is only allowed to move on the rail.

    Args:
        max_speed (float, optional): Maximum speed that this entity will move at when on the rail. Game default 0.4.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rail_movement)
    """

    identifier = "minecraft:rail_movement"

    max_speed: float | None = json_field(default=None)


class EntityRideable(JsonComponent):
    """Allows the entity to be ridden.

    Args:
        controlling_seat (int, optional): The seat of the driver. Game default 0.
        crouching_skip_interact (bool, optional): A crouching entity cannot interact with this one. Game default true.
        dismount_mode (RideableDismountMode, optional): Where riders are placed when they dismount. Game default default.
        family_types (list[str], optional): Families of the entities that can ride this entity.
        interact_text (str, optional): Text shown on the interact button with touch controls. It is added to the language file.
        on_rider_enter_event (str, optional): Event to run when an entity starts riding this one.
        on_rider_exit_event (str, optional): Event to run when an entity stops riding this one.
        passenger_max_width (float, optional): Maximum width of a rider; 0 ignores it. Game default 0.
        pull_in_entities (bool, optional): Pulls entities of `family_types` into free seats. Game default false.
        rider_can_interact (bool, optional): The rider can pick this entity when looking at it. Game default false.
        seat_count (int, optional): How many entities can ride at the same time. Game default 1.
        seats (list[Seat], optional): The seats. Add more with `add_seat`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rideable)
    """

    identifier = "minecraft:rideable"

    controlling_seat: Annotated[int, NonNegative] | None = json_field(default=None)
    crouching_skip_interact: bool | None = json_field(default=None)
    dismount_mode: RideableDismountMode | None = json_field(default=None)
    family_types: list[str] | None = json_field(default=None)
    interact_text: str | None = json_field(default=None)
    on_rider_enter_event: str | None = json_field(default=None)
    on_rider_exit_event: str | None = json_field(default=None)
    passenger_max_width: Annotated[float, NonNegative] | None = json_field(default=None)
    pull_in_entities: bool | None = json_field(default=None)
    rider_can_interact: bool | None = json_field(default=False)
    seat_count: Annotated[int, AtLeastOne] | None = json_field(default=None)
    seats: list[Seat] = json_field(default_factory=list, omit_default=True)

    def __post_init__(self) -> None:
        if self.interact_text is not None:
            self.interact_text = AnvilTranslator().localize(
                self.interact_text, prefix="action.interact"
            )

    def add_seat(
        self,
        *,
        position: tuple[float, float, float],
        max_rider_count: int,
        min_rider_count: int | None = None,
        lock_rider_rotation: float | None = None,
        rotate_rider_by: float | Molang | str | None = None,
        third_person_camera_radius: float | None = None,
        camera_relax_distance_smoothing: float | None = None,
    ) -> "EntityRideable":
        """Adds a seat. See `Seat` for the parameters. Set `seat_count` for how many can ride."""
        self.seats.append(
            Seat(
                position=position,
                max_rider_count=max_rider_count,
                min_rider_count=min_rider_count,
                lock_rider_rotation=lock_rider_rotation,
                rotate_rider_by=rotate_rider_by,
                third_person_camera_radius=third_person_camera_radius,
                camera_relax_distance_smoothing=camera_relax_distance_smoothing,
            )
        )
        return self


class EntityRotationAxisAligned(JsonComponent):
    """Causes the entity to automatically rotate to align with the nearest cardinal direction based on its current facing direction. Combining this with the "minecraft:body_rotation_blocked" component will cause the entity's body to align with the nearest cardinal direction and remain fixed in that orientation, regardless of changes in its facing direction.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rotation_axis_aligned)
    """

    identifier = "minecraft:rotation_axis_aligned"


class EntityRotationLockedToVehicle(JsonComponent):
    """Causes the entity's rotation to match their vehicle's facing direction. Introduced in 1.21.130 as a rename of `minecraft:body_rotation_locked_to_vehicle`. Locks both the entity's body rotation and overall rotation to its mounted vehicle's facing direction.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rotation_locked_to_vehicle)
    """

    identifier = "minecraft:rotation_locked_to_vehicle"


class EntityUnderwaterMovement(JsonComponent):
    """Defines the speed with which an entity can move through water.

    Args:
        value (float): Movement speed of the entity under water.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_underwater_movement)
    """

    identifier = "minecraft:underwater_movement"

    value: float = json_field()


class EntityVariableMaxAutoStep(JsonComponent):
    """Entities with this component will have a maximum auto step height that is different depending on whether they are on a block that prevents jumping. Incompatible with "runtime_identifier": "minecraft:horse".

    Args:
        base_value (float, optional): The maximum auto step height when on any other block. Game default 0.5625.
        controlled_value (float, optional): The maximum auto step height when on any other block and controlled by the player. Game default 0.5625.
        jump_prevented_value (float, optional): The maximum auto step height when on a block that prevents jumping. Game default 0.5625.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variable_max_auto_step)
    """

    identifier = "minecraft:variable_max_auto_step"

    base_value: float | None = json_field(default=None)
    controlled_value: float | None = json_field(default=None)
    jump_prevented_value: float | None = json_field(default=None)


class EntityVerticalMovementAction(JsonComponent):
    """When configured as a rideable entity, the entity will move upwards or downwards when the player uses the jump action.

    Args:
        vertical_velocity (float, optional): Vertical velocity to apply when jump action is issued. Game default 0.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vertical_movement.action)
    """

    identifier = "minecraft:vertical_movement_action"

    vertical_velocity: float | None = json_field(default=None)


class EntityWalkAnimationSpeed(JsonComponent):
    """Sets the speed multiplier for this entity's walk animation speed.

    Args:
        value (float, optional): The higher the number, the faster the animation for walking plays. A value of 1.0 means normal speed, while 2.0 means twice as fast. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_walk_animation_speed)
    """

    identifier = "minecraft:walk_animation_speed"

    value: float | None = json_field(default=None)


class EntityWaterMovement(JsonComponent):
    """Customizes how the entity moves through water by adjusting drag coefficient. Lower values let entities glide through water easily like fish, while higher values create resistance for entities that struggle in water. Essential for aquatic mobs, boats, and any entity needing custom underwater physics.

    Args:
        drag_factor (float, optional): Drag factor to determine movement speed when in water. Game default 0.8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_water_movement)
    """

    identifier = "minecraft:water_movement"
    drag_factor: float | None = json_field(default=None)


# endregion
