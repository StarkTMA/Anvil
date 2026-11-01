from typing import (
    Literal,
    Self,
)

from anvil.api.actors.components._validators import (
    _block,
    _blocks,
    _boolean,
    _chance,
    _damage_cause,
    _entity,
    _event,
    _events,
    _filter,
    _integer,
    _items,
    _molang,
    _number,
    _positive,
    _string,
)
from anvil.api.core.components import (
    AIGoal,
    EventTrigger,
)
from anvil.api.core.enums import (
    DamageCause,
    FilterSubject,
)
from anvil.api.core.filters import Filter
from anvil.api.core.types import (
    RGBA255,
    BlockReference,
    ItemReference,
    NumberRange,
    Vector3D,
)
from anvil.api.logic.molang import Molang
from anvil.api.world.loot_tables import LootTable
from anvil.lib.jsonmodel import (
    JsonObject,
    encoders,
    json_field,
)
from anvil.lib.jsonmodel.validators import (
    each,
    in_range,
    instance_of,
    integer_pair,
    number_or_range,
    one_of,
    rgba_or_hex,
    vector3,
)
from anvil.lib.schemas import MinecraftEntityDescriptor

# region Parts: objects nested inside components


class EatBlockPair(JsonObject):
    """A block an entity eats, and the block that replaces it.

    Args:
        eat_block (BlockReference): The block the entity eats.
        replace_block (BlockReference): The block that replaces the eaten block.
    """

    eat_block: BlockReference = json_field(validators=[_block])
    replace_block: BlockReference = json_field(validators=[_block])


class GoalEntityType(JsonObject):
    """An entity type an AI goal reacts to, and how it reacts.

    Args:
        filters (Filter, optional): Conditions an entity must meet to match this entry.
        check_if_outnumbered (bool, optional): The mob checks whether it is outnumbered. Game default false.
        cooldown (float, optional): Seconds the mob waits before selecting an entity of this type again. Game default 0.
        max_dist (float, optional): Maximum distance in blocks to the entity. Game default 16.
        max_flee (float, optional): Distance in blocks from the entity at which the mob stops fleeing. Game default 10.
        max_height (float, optional): Maximum height difference in blocks to the entity. Game default -1.
        must_see (bool, optional): The entity must be visible. Game default false.
        must_see_forget_duration (float, optional): Seconds the mob keeps looking for an entity it cannot see before it forgets it. Game default 3.
        priority (int, optional): Priority of this entry. Game default 0.
        reevaluate_description (bool, optional): The mob stops reacting to the entity once it no longer matches the filters. Game default false.
        sprint_speed_multiplier (float, optional): Multiplier for the sprinting speed. Game default 1.
        walk_speed_multiplier (float, optional): Multiplier for the walking speed. Game default 1.
    """

    filters: Filter | None = json_field(default=None, validators=[_filter])
    check_if_outnumbered: bool | None = json_field(default=None, validators=[_boolean])
    cooldown: float | None = json_field(default=None, validators=[_positive])
    max_dist: float | None = json_field(default=None, validators=[_number])
    max_flee: float | None = json_field(default=None, validators=[_number])
    max_height: float | None = json_field(default=None, validators=[_number])
    must_see: bool | None = json_field(default=None, validators=[_boolean])
    must_see_forget_duration: float | None = json_field(
        default=None, validators=[_positive]
    )
    priority: int | None = json_field(default=None, validators=[_integer])
    reevaluate_description: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    sprint_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    walk_speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityTypesAIGoal(AIGoal, abstract=True):
    """Base of the AI goals that react to a list of entity types.

    Args:
        entity_types (list[GoalEntityType], optional): The entity types the goal reacts to. Add entries with `add_entity_type`.
    """

    entity_types: list[GoalEntityType] = json_field(
        default_factory=list,
        validators=[each(instance_of(GoalEntityType))],
        omit_default=True,
    )

    def add_entity_type(
        self,
        *,
        filters: Filter | None = None,
        check_if_outnumbered: bool | None = None,
        cooldown: float | None = None,
        max_dist: float | None = None,
        max_flee: float | None = None,
        max_height: float | None = None,
        must_see: bool | None = None,
        must_see_forget_duration: float | None = None,
        priority: int | None = None,
        reevaluate_description: bool | None = None,
        sprint_speed_multiplier: float | None = None,
        walk_speed_multiplier: float | None = None,
    ) -> Self:
        """Adds an entity type. See `GoalEntityType` for the parameters."""
        self.entity_types.append(
            GoalEntityType(
                filters=filters,
                check_if_outnumbered=check_if_outnumbered,
                cooldown=cooldown,
                max_dist=max_dist,
                max_flee=max_flee,
                max_height=max_height,
                must_see=must_see,
                must_see_forget_duration=must_see_forget_duration,
                priority=priority,
                reevaluate_description=reevaluate_description,
                sprint_speed_multiplier=sprint_speed_multiplier,
                walk_speed_multiplier=walk_speed_multiplier,
            )
        )
        return self


class PlaceableBlock(JsonObject):
    """A block an entity places at random, with its weight.

    Args:
        block (BlockReference): The block to place.
        filter (Filter, optional): Conditions for this entry to be picked. Self, Target and Block are set.
        weight (int, optional): Weight of this entry. Game default 1.
    """

    block: BlockReference = json_field(
        validators=[_block], encoder=encoders.block_object
    )
    filter: Filter | None = json_field(default=None, validators=[_filter])
    weight: int | None = json_field(default=None, validators=[_integer, _positive])


class PotionChoice(JsonObject):
    """A potion an entity can drink.

    Args:
        id (int): The registry ID of the potion.
        chance (float, optional): Chance from 0 to 1 that this potion is picked. Game default 1.
        filters (Filter, optional): Conditions for this potion to be picked.
    """

    id: int = json_field(validators=[_integer])
    chance: float | None = json_field(default=None, validators=[_number, _chance])
    filters: Filter | None = json_field(default=None, validators=[_filter])


class SendEventStep(JsonObject):
    """A step of a `minecraft:behavior.send_event` sequence.

    Args:
        event (str): The event to send to the entity.
        base_delay (float, optional): Seconds before this step starts. Game default 0.
        sound_event (str, optional): The sound event to play when this step happens.
    """

    event: str = json_field(validators=[_string])
    base_delay: float | None = json_field(default=None, validators=[_positive])
    sound_event: str | None = json_field(default=None, validators=[_string])


class SendEventChoice(JsonObject):
    """An event an entity can send, with its conditions, weight and steps.

    Args:
        cast_duration (float, optional): Seconds the whole event sending takes. Game default 0.
        cooldown_time (float, optional): Seconds before this choice can be used again. Game default 0.
        do_casting (bool, optional): The mob shows a casting animation while sending the event. Game default true.
        filters (Filter, optional): Conditions the target must meet to receive the event.
        look_at_target (bool, optional): The mob faces the entity it sends the event to. Game default true.
        max_activation_range (float, optional): Maximum distance in blocks to the target. Game default 32.
        min_activation_range (float, optional): Minimum distance in blocks to the target. Game default 1.
        particle_color (str | RGBA255, optional): Color of the particles spawned while casting.
        sequence (list[SendEventStep], optional): The events to send. Add more with `add_step`.
        start_sound_event (str, optional): The sound event to play when this choice starts.
        weight (float, optional): Weight of this choice when one is picked at random. Game default 0.
    """

    cast_duration: float | None = json_field(default=None, validators=[_positive])
    cooldown_time: float | None = json_field(default=None, validators=[_positive])
    do_casting: bool | None = json_field(default=None, validators=[_boolean])
    filters: Filter | None = json_field(default=None, validators=[_filter])
    look_at_target: bool | None = json_field(default=None, validators=[_boolean])
    max_activation_range: float | None = json_field(
        default=None, validators=[_positive]
    )
    min_activation_range: float | None = json_field(
        default=None, validators=[_positive]
    )
    particle_color: str | RGBA255 | None = json_field(
        default=None, validators=[rgba_or_hex]
    )
    sequence: list[SendEventStep] = json_field(
        default_factory=list,
        validators=[each(instance_of(SendEventStep))],
        omit_default=True,
    )
    start_sound_event: str | None = json_field(default=None, validators=[_string])
    weight: float | None = json_field(default=None, validators=[_positive])

    def add_step(
        self,
        *,
        event: str,
        base_delay: float | None = None,
        sound_event: str | None = None,
    ) -> "SendEventChoice":
        """Adds a step. See `SendEventStep` for the parameters."""
        self.sequence.append(
            SendEventStep(event=event, base_delay=base_delay, sound_event=sound_event)
        )
        return self


class SummonStep(JsonObject):
    """A step of a summon spell.

    Args:
        entity_type (MinecraftEntityDescriptor | str): The entity to summon.
        base_delay (float, optional): Seconds before this step starts. Game default 0.
        delay_per_summon (float, optional): Seconds between each summoned entity. Game default 0.
        entity_lifespan (float, optional): Seconds the summoned entity lives; -1 keeps it alive. Game default -1.
        num_entities_spawned (int, optional): Number of entities summoned in this step. Game default 1.
        shape (Literal["circle", "line"], optional): The shape the entities are summoned in. Game default line.
        size (float, optional): The base size of the shape. Game default 1.
        sound_event (str, optional): The sound event to play for this step.
        summon_cap (int, optional): Maximum number of summoned entities at a time. Game default 0.
        summon_cap_radius (float, optional): Radius in blocks the summon cap counts entities in. Game default 0.
        summon_event (str, optional): Event run on each summoned entity when it spawns.
        target (FilterSubject, optional): Where the spell starts: a line starts there, a circle is centered there. Game default self.
    """

    entity_type: MinecraftEntityDescriptor | str = json_field(validators=[_entity])
    base_delay: float | None = json_field(default=None, validators=[_positive])
    delay_per_summon: float | None = json_field(default=None, validators=[_positive])
    entity_lifespan: float | None = json_field(default=None, validators=[_number])
    num_entities_spawned: int | None = json_field(
        default=None, validators=[_integer, _positive]
    )
    shape: Literal["circle", "line"] | None = json_field(
        default=None, validators=[one_of("circle", "line")]
    )
    size: float | None = json_field(default=None, validators=[_number])
    sound_event: str | None = json_field(default=None, validators=[_string])
    summon_cap: int | None = json_field(default=None, validators=[_integer, _positive])
    summon_cap_radius: float | None = json_field(default=None, validators=[_positive])
    summon_event: str | None = json_field(default=None, validators=[_string])
    target: FilterSubject | None = json_field(
        default=None, validators=[one_of(*FilterSubject)]
    )


class SummonChoice(JsonObject):
    """A summon spell: when the entity casts it, and the steps it runs.

    Args:
        cast_duration (float, optional): Seconds the casting takes. Game default -1.
        cooldown_time (float, optional): Seconds before the spell can be used again. Game default 0.
        do_casting (bool, optional): The mob plays the casting animations and particles. Game default true.
        filters (Filter, optional): Conditions for the spell to be used.
        max_activation_range (float, optional): Maximum distance in blocks to the target. Game default 32.
        min_activation_range (float, optional): Minimum distance in blocks to the target. Game default 1.
        particle_color (str | RGBA255, optional): Color of the spell particles.
        sequence (list[SummonStep], optional): The steps of the spell. Add more with `add_step`.
        start_sound_event (str, optional): The sound event to play when the spell starts.
        weight (float, optional): Weight of this spell when one is picked at random. Game default 0.
    """

    cast_duration: float | None = json_field(default=None, validators=[_number])
    cooldown_time: float | None = json_field(default=None, validators=[_positive])
    do_casting: bool | None = json_field(default=None, validators=[_boolean])
    filters: Filter | None = json_field(default=None, validators=[_filter])
    max_activation_range: float | None = json_field(
        default=None, validators=[_positive]
    )
    min_activation_range: float | None = json_field(
        default=None, validators=[_positive]
    )
    particle_color: str | RGBA255 | None = json_field(
        default=None, validators=[rgba_or_hex]
    )
    sequence: list[SummonStep] = json_field(
        default_factory=list,
        validators=[each(instance_of(SummonStep))],
        omit_default=True,
    )
    start_sound_event: str | None = json_field(default=None, validators=[_string])
    weight: float | None = json_field(default=None, validators=[_positive])

    def add_step(
        self,
        *,
        entity_type: MinecraftEntityDescriptor | str,
        base_delay: float | None = None,
        delay_per_summon: float | None = None,
        entity_lifespan: float | None = None,
        num_entities_spawned: int | None = None,
        shape: Literal["circle", "line"] | None = None,
        size: float | None = None,
        sound_event: str | None = None,
        summon_cap: int | None = None,
        summon_cap_radius: float | None = None,
        summon_event: str | None = None,
        target: FilterSubject | None = None,
    ) -> "SummonChoice":
        """Adds a step. See `SummonStep` for the parameters."""
        self.sequence.append(
            SummonStep(
                entity_type=entity_type,
                base_delay=base_delay,
                delay_per_summon=delay_per_summon,
                entity_lifespan=entity_lifespan,
                num_entities_spawned=num_entities_spawned,
                shape=shape,
                size=size,
                sound_event=sound_event,
                summon_cap=summon_cap,
                summon_cap_radius=summon_cap_radius,
                summon_event=summon_event,
                target=target,
            )
        )
        return self


# endregion

# region Components


class EntityAIAdmireItem(AIGoal):
    """Enables the mob to admire items that have been configured as admirable.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        admire_item_sound (str, optional): The sound event to play when admiring the item.
        on_admire_item_start (EventTrigger | str, optional): Event to run when the mob starts admiring an item.
        on_admire_item_stop (EventTrigger | str, optional): Event to run when the mob stops admiring an item.
        sound_interval (float | NumberRange, optional): The range of time in seconds to randomly wait before playing the sound again. Can be a number, an array [min, max], or an object with range_min and range_max. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_admire_item)
    """

    identifier = "minecraft:behavior.admire_item"

    admire_item_sound: str | None = json_field(default=None, validators=[_string])
    on_admire_item_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_admire_item_stop: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )


class EntityAIAquaticChargeAttack(AIGoal):
    """Enables an aquatic mob to dash at its target with knockback; includes overshoot and cooldown settings.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_reach (float, optional): Horizontal reach grown around the mob's AABB to register a hit. Game default 0.05.
        charge_cooldown_time (float | NumberRange, optional): Range of time in seconds to wait before starting another charge. Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected.
        charge_overshoot_distance (float, optional): Distance beyond the target the mob aims during a charge. Game default 1.5.
        charge_speed (float, optional): Absolute speed used during the charge attack. Game default 0.06.
        knockback_force (float, optional): Knockback force applied to the target on hit. Game default 2.
        max_charge_distance (float, optional): Maximum distance at which the mob attempts a charge. Game default 16.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_aquatic_charge_attack)
    """

    identifier = "minecraft:behavior.aquatic_charge_attack"

    attack_reach: float | None = json_field(default=None, validators=[_number])
    charge_cooldown_time: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    charge_overshoot_distance: float | None = json_field(
        default=None, validators=[_number]
    )
    charge_speed: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0.05000000074505806)]
    )
    knockback_force: float | None = json_field(default=None, validators=[_number])
    max_charge_distance: float | None = json_field(default=None, validators=[_number])


class EntityAIAvoidBlock(AIGoal):
    """Allows this entity to avoid certain blocks.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        avoid_block_sound (str, optional): The sound event to play when the mob is avoiding a block.
        on_escape (EventTrigger | str, optional): Event triggers that fire when the entity escapes from the avoided block. Can be a single trigger or an array of triggers.
        search_height (int, optional): Maximum distance to look for a block in y. Game default 0.
        search_range (int, optional): Maximum distance to look for a block in xz. Game default 0.
        sound_interval (float | NumberRange, optional): The range of time in seconds to randomly wait before playing the sound again.
        sprint_speed_modifier (float, optional): Modifier for sprint speed. 1.0 means keep the regular speed, while higher numbers make the sprint speed faster. Game default 1.
        target_blocks (list[BlockReference], optional): List of block types this mob avoids.
        target_selection_method (str, optional): Block search method. Game default nearest.
        tick_interval (int, optional): Should start tick interval. Game default 1.
        walk_speed_modifier (float, optional): Modifier for walking speed. 1.0 means keep the regular speed, while higher numbers make the walking speed faster. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_block)
    """

    identifier = "minecraft:behavior.avoid_block"

    avoid_block_sound: str | None = json_field(default=None, validators=[_string])
    on_escape: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    search_height: int | None = json_field(default=None, validators=[_integer])
    search_range: int | None = json_field(default=None, validators=[_integer])
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    sprint_speed_modifier: float | None = json_field(default=None, validators=[_number])
    target_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks]
    )
    target_selection_method: str | None = json_field(default=None, validators=[_string])
    tick_interval: int | None = json_field(default=None, validators=[_integer])
    walk_speed_modifier: float | None = json_field(default=None, validators=[_number])


class EntityAIAvoidMobType(EntityTypesAIGoal):
    """Allows the entity to run away from other entities that meet the criteria specified.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        avoid_mob_sound (str, optional): The sound event to play when the mob is avoiding another mob.
        avoid_target_xz (int, optional): The next target position the entity chooses to avoid another entity will be chosen within this XZ Distance. Game default 16.
        avoid_target_y (int, optional): The next target position the entity chooses to avoid another entity will be chosen within this Y Distance. Game default 7.
        entity_types (list[GoalEntityType], optional): The list of conditions another entity must meet to be a valid target to avoid. Add entries with `add_entity_type`.
        ignore_visibility (bool, optional): Whether or not to ignore direct line of sight while this entity is running away from other specified entities. Game default false.
        max_dist (float, optional): Maximum distance to look for an avoid target for the entity. Game default 3.
        max_flee (float, optional): How many blocks away from its avoid target the entity must be for it to stop fleeing from the avoid target. Game default 10.
        on_escape_event (EventTrigger | str, optional): Event that is triggered when escaping from a mob.
        probability_per_strength (float, optional): Percent chance this entity will stop avoiding another entity based on that entity's strength, where 1.0 = 100%. Game default 1.
        remove_target (bool, optional): Determine if we should remove target when fleeing or not. Game default false.
        river_speed_multiplier (float, optional): Multiplier for speed when following river. 1.0 means keep the regular speed, while higher numbers make the speed faster. Game default 0.75.
        sound_interval (float | NumberRange, optional): The range of time in seconds to randomly wait before playing the sound again.
        sprint_distance (float, optional): How many blocks within range of its avoid target the entity must be for it to begin sprinting away from the avoid target. Game default 7.
        sprint_speed_multiplier (float, optional): Multiplier for sprint speed. 1.0 means keep the regular speed, while higher numbers make the sprint speed faster. Game default 1.
        walk_speed_multiplier (float, optional): Multiplier for walking speed. 1.0 means keep the regular speed, while higher numbers make the walking speed faster. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_mob_type)
    """

    identifier = "minecraft:behavior.avoid_mob_type"

    avoid_mob_sound: str | None = json_field(default=None, validators=[_string])
    avoid_target_xz: int | None = json_field(default=None, validators=[_integer])
    avoid_target_y: int | None = json_field(default=None, validators=[_integer])
    ignore_visibility: bool | None = json_field(default=None, validators=[_boolean])
    max_dist: float | None = json_field(default=None, validators=[_number])
    max_flee: float | None = json_field(default=None, validators=[_number])
    on_escape_event: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    probability_per_strength: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    remove_target: bool | None = json_field(default=None, validators=[_boolean])
    river_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    sprint_distance: float | None = json_field(default=None, validators=[_number])
    sprint_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    walk_speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIBarter(AIGoal):
    """Enables the mob to barter for items that have been configured as barter currency. Must be used in combination with the barter component.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_barter)
    """

    identifier = "minecraft:behavior.barter"


class EntityAIBeg(AIGoal):
    """Allows this mob to look at and follow the player that holds food they like.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        items (list[ItemReference], optional): List of items that this mob likes.
        look_distance (float, optional): Distance in blocks the mob will beg from. Game default 8.
        look_time (tuple[int, int], optional): The range of time in seconds this mob will stare at the player holding a food they like, begging for it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_beg)
    """

    identifier = "minecraft:behavior.beg"

    items: list[ItemReference] | None = json_field(default=None, validators=[_items])
    look_distance: float | None = json_field(default=None, validators=[_number])
    look_time: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )


class EntityAIBreakDoor(AIGoal):
    """Allows this mob to break doors.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_break_door)
    """

    identifier = "minecraft:behavior.break_door"


class EntityAIBreed(AIGoal):
    """Allows this mob to breed with other mobs.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier applied to the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_breed)
    """

    identifier = "minecraft:behavior.breed"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAICelebrate(AIGoal):
    """Allows this entity to celebrate surviving a raid by making celebration sounds and jumping.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        celebration_sound (str, optional): The sound event to trigger during the celebration. Game default celebrate.
        duration (float, optional): The duration in seconds that the celebration lasts for. Game default 30.
        jump_interval (float | NumberRange, optional): Minimum and maximum time between jumping (positive, in seconds). Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected.
        on_celebration_end_event (EventTrigger | str, optional): The event to trigger when the goal's duration expires.
        sound_interval (float | NumberRange, optional): Minimum and maximum time between sound events (positive, in seconds). Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_celebrate)
    """

    identifier = "minecraft:behavior.celebrate"

    celebration_sound: str | None = json_field(default=None, validators=[_string])
    duration: float | None = json_field(default=None, validators=[_number])
    jump_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    on_celebration_end_event: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )


class EntityAICelebrateSurvive(AIGoal):
    """Allows the player to trade with this mob. When the goal starts, it will stop the mob's navigation.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        duration (float, optional): The duration in seconds that the celebration lasts for. Game default 30.
        fireworks_interval (float | NumberRange, optional): Minimum and maximum time between firework (positive, in seconds).
        on_celebration_end_event (EventTrigger | str, optional): The event to trigger when the goal's duration expires.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_celebrate_survive)
    """

    identifier = "minecraft:behavior.celebrate_survive"

    duration: float | None = json_field(default=None, validators=[_number])
    fireworks_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    on_celebration_end_event: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAIChargeAttack(AIGoal):
    """Allows this entity to damage a target by using a running attack.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        max_distance (float, optional): A charge attack cannot start if the entity is farther than this distance to the target. Game default 3.
        min_distance (float, optional): A charge attack cannot start if the entity is closer than this distance to the target. Game default 2.
        sound_event (str, optional):  Game default charge.
        speed_multiplier (float, optional): Modifies the entity's speed when charging toward the target. Game default 1.
        success_rate (float, optional): Percent chance this entity will start a charge attack, if not already attacking (1.0 = 100%). Game default 0.1428.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_attack)
    """

    identifier = "minecraft:behavior.charge_attack"

    max_distance: float | None = json_field(default=None, validators=[_number])
    min_distance: float | None = json_field(default=None, validators=[_number])
    sound_event: str | None = json_field(default=None, validators=[_string])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    success_rate: float | None = json_field(default=None, validators=[_number])


class EntityAIChargeHeldItem(AIGoal):
    """Allows an entity to charge and use their held item.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        items (list[ItemReference], optional): The list of items that can be used to charge the held item. This list is required and must have at least one item in it. Value must have at least 1 items.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_held_item)
    """

    identifier = "minecraft:behavior.charge_held_item"

    items: list[ItemReference] | None = json_field(default=None, validators=[_items])


class EntityAICircleAroundAnchor(AIGoal):
    """Causes an entity to circle around an anchor point placed near a point or target.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        angle_change (float, optional): Number of degrees to change this entity's facing by, when the entity selects its next anchor point. Game default 15.
        goal_radius (float, optional): Maximum distance from the anchor-point in which this entity considers itself to have reached the anchor point. Game default 0.5.
        height_above_target_range (float | NumberRange, optional): The number of blocks above the target that the next anchor point can be set.
        height_adjustment_chance (float, optional): Percent chance to determine how often to increase or decrease the current height around the anchor point. Game default 0.0029.
        height_offset_range (float | NumberRange, optional): Vertical distance from the anchor point this entity must stay within, upon a successful height adjustment.
        radius_adjustment_chance (float, optional): Percent chance to determine how often to increase the size of the current movement radius around the anchor point. Game default 0.004.
        radius_change (float, optional): The number of blocks to increase the current movement radius by, upon successful "radius_adjustment_chance". Game default 1.
        radius_range (float | NumberRange, optional): Horizontal distance from the anchor point this entity must stay within upon a successful radius adjustment.
        speed_multiplier (float, optional): Multiplies the speed at which this entity travels to its next desired position. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_circle_around_anchor)
    """

    identifier = "minecraft:behavior.circle_around_anchor"

    angle_change: float | None = json_field(default=None, validators=[_number])
    goal_radius: float | None = json_field(default=None, validators=[_number])
    height_above_target_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    height_adjustment_chance: float | None = json_field(
        default=None, validators=[_number]
    )
    height_offset_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    radius_adjustment_chance: float | None = json_field(
        default=None, validators=[_number]
    )
    radius_change: float | None = json_field(default=None, validators=[_number])
    radius_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIControlledByPlayer(AIGoal):
    """Allows the entity to be controlled by the player using an item in the item_controllable property (required). On every tick, the entity will attempt to rotate towards where the player is facing with the control item whilst simultaneously moving forward.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        fractional_rotation (float, optional): The entity will attempt to rotate to face where the player is facing each tick. Game default 0.5.
        fractional_rotation_limit (float, optional): Limits the total degrees the entity can rotate to face where the player is facing on each tick. Game default 5.
        mount_speed_multiplier (float, optional): Speed multiplier of mount when controlled by player. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_controlled_by_player)
    """

    identifier = "minecraft:behavior.controlled_by_player"

    fractional_rotation: float | None = json_field(default=None, validators=[_number])
    fractional_rotation_limit: float | None = json_field(
        default=None, validators=[_number]
    )
    mount_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )


class EntityAICroak(AIGoal):
    """Allows the entity to croak at a random time interval with configurable conditions.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        duration (float | NumberRange, optional): Random range in seconds after which the croaking stops. Can also be a constant. Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected.
        filters (Filter, optional): Conditions for the behavior to start and keep running. The interval between runs only starts after passing the filters.
        interval (float | NumberRange, optional): Random range in seconds between runs of this behavior. Can also be a constant. Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_croak)
    """

    identifier = "minecraft:behavior.croak"

    duration: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    filters: Filter | None = json_field(default=None, validators=[_filter])
    interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )


class EntityAIDefendTrustedTarget(EntityTypesAIGoal):
    """Allows the mob to target another mob that hurts an entity it trusts.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        aggro_sound (str, optional): Sound to occasionally play while defending.
        attack_interval (int, optional): Time in seconds between attacks. Game default 0.
        entity_types (list[GoalEntityType], optional): List of entity types that this mob considers valid targets. Add entries with `add_entity_type`.
        must_see (bool, optional): If true, only entities in this mob's viewing range can be selected as targets. Game default false.
        must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Game default 3.
        on_defend_start (EventTrigger | str, optional): Trigger to be executed when defending begins.
        within_radius (float, optional): Distance in blocks that the target can be within to launch an attack. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_defend_trusted_target)
    """

    identifier = "minecraft:behavior.defend_trusted_target"

    aggro_sound: str | None = json_field(default=None, validators=[_string])
    attack_interval: int | None = json_field(default=None, validators=[_integer])
    must_see: bool | None = json_field(default=None, validators=[_boolean])
    must_see_forget_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    on_defend_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAIDefendVillageTarget(EntityTypesAIGoal):
    """Allows the entity to stay in a village and defend the village from aggressors. If a player is in bad standing with the village this goal will cause the entity to attack the player regardless of filter conditions.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_chance (float, optional): The percentage chance that the entity has to attack aggressors of its village, where 1.0 = 100%. Game default 0.05.
        attack_owner (bool, optional): If true, this entity can attack its owner. Game default false.
        entity_types (list[GoalEntityType], optional): Filters which types of targets are valid for this entity. Add entries with `add_entity_type`.
        must_reach (bool, optional): If true, this entity requires a path to the target. Game default false.
        must_see (bool, optional): Determines if target-validity requires this entity to be in range only, or both in range and in sight. Game default false.
        must_see_forget_duration (float, optional): Time (in seconds) the target must not be seen by this entity to become invalid. Used only if "must_see" is true. Game default 3.
        persist_time (float, optional): Time (in seconds) this entity can continue attacking the target after the target is no longer valid. Game default 0.
        within_radius (float, optional): Maximum distance this entity can be from the target when following it, otherwise the target becomes invalid. This value is only used if the entity doesn't declare "minecraft:follow_range". Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_defend_village_target)
    """

    identifier = "minecraft:behavior.defend_village_target"

    attack_chance: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    attack_owner: bool | None = json_field(default=None, validators=[_boolean])
    must_reach: bool | None = json_field(default=None, validators=[_boolean])
    must_see: bool | None = json_field(default=None, validators=[_boolean])
    must_see_forget_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    persist_time: float | None = json_field(default=None, validators=[_number])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAIDelayedAttack(AIGoal):
    """Allows an entity to attack, while also delaying the damage-dealt until a specific time in the attack animation.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_duration (float, optional): The entity's attack animation will play out over this duration (in seconds). Also controls attack cooldown. Game default 0.75.
        attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Game default false.
        attack_types (str, optional): Defines the entity types this entity will attack.
        can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Game default false.
        hit_delay_pct (float, optional): The percentage into the attack animation to apply the damage of the attack (1.0 = 100%). Game default 0.5.
        inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Game default 0.25.
        max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.55.
        melee_fov (float, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Game default 90.
        min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.2.
        on_attack (EventTrigger | str, optional): Defines the event to trigger when this entity successfully attacks.
        on_kill (EventTrigger | str, optional): Defines the event to trigger when this entity kills the target.
        outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Game default 0.5.
        path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Game default 0.75.
        path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Game default 16.
        path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Game default 32.
        random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Game default 0.
        reach_multiplier (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Game default 1.5.
        require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Game default false.
        sound_event (str, optional):  Game default attack.strong.
        speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Game default 1.
        track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Game default true.
        x_max_rotation (float, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_delayed_attack)
    """

    identifier = "minecraft:behavior.delayed_attack"

    attack_duration: float | None = json_field(default=None, validators=[_number])
    attack_once: bool | None = json_field(default=None, validators=[_boolean])
    attack_types: str | None = json_field(default=None, validators=[_string])
    can_spread_on_fire: bool | None = json_field(default=None, validators=[_boolean])
    hit_delay_pct: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    inner_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    max_path_time: float | None = json_field(default=None, validators=[_number])
    melee_fov: float | None = json_field(default=None, validators=[_number])
    min_path_time: float | None = json_field(default=None, validators=[_number])
    on_attack: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_kill: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    outer_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_fail_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_inner_boundary: float | None = json_field(default=None, validators=[_number])
    path_outer_boundary: float | None = json_field(default=None, validators=[_number])
    random_stop_interval: int | None = json_field(default=None, validators=[_integer])
    reach_multiplier: float | None = json_field(default=None, validators=[_number])
    require_complete_path: bool | None = json_field(default=None, validators=[_boolean])
    sound_event: str | None = json_field(default=None, validators=[_string])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    track_target: bool | None = json_field(default=None, validators=[_boolean])
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_head_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAIDig(AIGoal):
    """Allows this entity to dig into the ground before despawning.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        allow_dig_when_named (bool, optional): If true, this behavior can run when this entity is named. Otherwise not. Game default false.
        digs_in_daylight (bool, optional): Indicates that the actor should start digging when it sees daylight. Game default false.
        duration (float, optional): Goal duration in seconds. Game default 0.
        idle_time (float, optional): The minimum idle time in seconds between the last detected disturbance to the start of digging. Game default 0.
        on_start (EventTrigger | str, optional): Event(s) to run when the goal starts.
        suspicion_is_disturbance (bool, optional): If true, finding new suspicious locations count as disturbances that may delay the start of this goal. Game default false.
        vibration_is_disturbance (bool, optional): If true, vibrations count as disturbances that may delay the start of this goal. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dig)
    """

    identifier = "minecraft:behavior.dig"

    allow_dig_when_named: bool | None = json_field(default=None, validators=[_boolean])
    digs_in_daylight: bool | None = json_field(default=None, validators=[_boolean])
    duration: float | None = json_field(default=None, validators=[_number])
    idle_time: float | None = json_field(default=None, validators=[_number])
    on_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    suspicion_is_disturbance: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    vibration_is_disturbance: bool | None = json_field(
        default=None, validators=[_boolean]
    )


class EntityAIDoorInteract(AIGoal):
    """Allows the mob to open and close doors.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_door_interact)
    """

    identifier = "minecraft:behavior.door_interact"


class EntityAIDrinkMilk(AIGoal):
    """Allows the mob to drink milk based on specified environment conditions.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_seconds (float, optional): Time (in seconds) that the goal is on cooldown before it can be used again. Game default 5.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drink_milk)
    """

    identifier = "minecraft:behavior.drink_milk"

    cooldown_seconds: float | None = json_field(default=None, validators=[_number])
    filters: Filter | None = json_field(default=None, validators=[_filter])


class EntityAIDrinkPotion(AIGoal):
    """Allows the mob to drink potions based on specified environment conditions.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        potions (list[PotionChoice], optional): A list of potions that this entity can drink. Each potion entry has the following parameters:. Add more with `add_potion`.
        speed_modifier (float, optional): The movement speed modifier to apply to the entity while it is drinking a potion. A value of 0 represents no change in speed. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drink_potion)
    """

    identifier = "minecraft:behavior.drink_potion"

    potions: list[PotionChoice] = json_field(
        default_factory=list,
        validators=[each(instance_of(PotionChoice))],
        omit_default=True,
    )
    speed_modifier: float | None = json_field(default=None, validators=[_number])

    def add_potion(
        self,
        *,
        id: int,
        chance: float | None = None,
        filters: Filter | None = None,
    ) -> "EntityAIDrinkPotion":
        """Adds a potion. See `PotionChoice` for the parameters."""
        self.potions.append(PotionChoice(id=id, chance=chance, filters=filters))
        return self


class EntityAIDropItemFor(EntityTypesAIGoal):
    """Allows the entity to move toward a target, and drop an item near the target.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown (float, optional): Total time that the goal is on cooldown before it can be used again. Game default 0.25.
        drop_item_chance (float, optional): The percent chance the entity will drop an item when using this goal. Game default 1.
        entity_types (list[GoalEntityType], optional): The list of conditions another entity must meet to be a valid target to drop an item for. Add entries with `add_entity_type`.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        loot_table (LootTable | str, optional): The loot table that contains the possible loot the entity can drop with this goal.
        max_head_look_at_height (float, optional): The maximum height the entities head will look at when dropping the item. The entity will always be looking at its target. Game default 10.
        minimum_teleport_distance (float, optional): If the target position is farther away than this distance on any tick, the entity will teleport to the target position. Game default 2.
        offering_distance (float, optional): The preferred distance the entity tries to be from the target it is dropping an item for. Game default 1.
        on_drop_attempt (EventTrigger | str, optional): The event to trigger when the entity attempts to drop an item.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 0.
        search_height (int, optional): The height in blocks the entity will search within to find a valid target position. Game default 1.
        search_range (int, optional): The distance in blocks the entity will search within to find a valid target position. Game default 0.
        seconds_before_pickup (float, optional): The numbers of seconds that will pass before the dropped entity can be picked up from the ground. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.
        target_range (Vector3D, optional): The range in blocks within which the entity searches to find a target to drop an item for.
        teleport_offset (Vector3D, optional): When the entity teleports, offset the teleport position by this many blocks in the X, Y, and Z coordinate.
        time_of_day_range (float | NumberRange, optional): The valid times of day that this goal can be used. For reference: noon is 0.0, sunset is 0.25, midnight is 0.5, and sunrise is 0.75, and back to noon for 1.0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drop_item_for)
    """

    identifier = "minecraft:behavior.drop_item_for"

    cooldown: float | None = json_field(default=None, validators=[_number])
    drop_item_chance: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    loot_table: LootTable | str | None = json_field(
        default=None, validators=[instance_of(LootTable, str)]
    )
    max_head_look_at_height: float | None = json_field(
        default=None, validators=[_number]
    )
    minimum_teleport_distance: float | None = json_field(
        default=None, validators=[_number]
    )
    offering_distance: float | None = json_field(default=None, validators=[_number])
    on_drop_attempt: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    seconds_before_pickup: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    target_range: Vector3D | None = json_field(default=None, validators=[vector3])
    teleport_offset: Vector3D | None = json_field(default=None, validators=[vector3])
    time_of_day_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )


class EntityAIEatBlock(AIGoal):
    """Allows the entity to consume a block, replace the eaten block with another block, and trigger an event as a result.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        eat_and_replace_block_pairs (list[EatBlockPair], optional): A collection of pairs of blocks; the first ("eat_block") is the block the entity should eat, the second ("replace_block") is the block that should replace the eaten block. Add more with `add_block_pair`.
        on_eat (EventTrigger | str, optional): The event to trigger when the block eating animation has completed.
        success_chance (Molang | str | float, optional): A molang expression defining the success chance the entity has to consume a block. Game default 0.02.
        time_until_eat (float, optional): The amount of time (in seconds) it takes for the block to be eaten upon a successful eat attempt. Game default 1.8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_block)
    """

    identifier = "minecraft:behavior.eat_block"

    eat_and_replace_block_pairs: list[EatBlockPair] = json_field(
        default_factory=list,
        validators=[each(instance_of(EatBlockPair))],
        omit_default=True,
    )
    on_eat: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    success_chance: Molang | str | float | None = json_field(
        default=None, validators=[_molang]
    )
    time_until_eat: float | None = json_field(default=None, validators=[_number])

    def add_block_pair(
        self, *, eat_block: BlockReference, replace_block: BlockReference
    ) -> "EntityAIEatBlock":
        """Adds a block to eat and the block that replaces it."""
        self.eat_and_replace_block_pairs.append(
            EatBlockPair(eat_block=eat_block, replace_block=replace_block)
        )
        return self


class EntityAIEatCarriedItem(AIGoal):
    """If the mob is carrying a food item, the mob will eat it and the effects will be applied to the mob.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        delay_before_eating (float, optional): Time in seconds the mob should wait before eating the item. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_carried_item)
    """

    identifier = "minecraft:behavior.eat_carried_item"

    delay_before_eating: float | None = json_field(default=None, validators=[_number])


class EntityAIEatMob(AIGoal):
    """Allows the entity to eat a specified Mob.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        eat_animation_time (float, optional): Sets the time in seconds the eat animation should play for. Game default 1.
        eat_mob_sound (str, optional): Sets the sound that should play when eating a mob.
        loot_table (LootTable | str, optional): The loot table for loot to be dropped when eating a mob.
        pull_in_force (float, optional): Sets the force which the mob-to-be-eaten is pulled towards the eating mob. Game default 1.
        reach_mob_distance (float, optional): Sets the desired distance to be reached before eating the mob. Game default 1.
        run_speed (float, optional): Sets the entity's speed when running toward the target. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_mob)
    """

    identifier = "minecraft:behavior.eat_mob"

    eat_animation_time: float | None = json_field(default=None, validators=[_number])
    eat_mob_sound: str | None = json_field(default=None, validators=[_string])
    loot_table: LootTable | str | None = json_field(
        default=None, validators=[instance_of(LootTable, str)]
    )
    pull_in_force: float | None = json_field(default=None, validators=[_number])
    reach_mob_distance: float | None = json_field(default=None, validators=[_number])
    run_speed: float | None = json_field(default=None, validators=[_number])


class EntityAIEmerge(AIGoal):
    """Allows this entity to emerge from the ground.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.5.
        duration (float, optional): Goal duration in seconds. Game default 5.
        on_done (EventTrigger | str, optional): Trigger to be executed when the goal execution is about to end.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_emerge)
    """

    identifier = "minecraft:behavior.emerge"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    duration: float | None = json_field(default=None, validators=[_number])
    on_done: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAIEndermanLeaveBlock(AIGoal):
    """Allows the enderman to drop a block they are carrying.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_enderman_leave_block)
    """

    identifier = "minecraft:behavior.enderman_leave_block"


class EntityAIEndermanTakeBlock(AIGoal):
    """Allows the enderman to take a block and carry it around.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_enderman_take_block)
    """

    identifier = "minecraft:behavior.enderman_take_block"


class EntityAIEquipItem(AIGoal):
    """The entity puts on the desired equipment.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_equip_item)
    """

    identifier = "minecraft:behavior.equip_item"


class EntityAIExploreOutskirts(AIGoal):
    """Allows the entity to first travel to a random point on the outskirts of the village, and then explore random points within a small distance.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        dist_from_boundary (Vector3D, optional): The distance from the boundary the villager must be within in to explore the outskirts.
        explore_dist (float, optional): Total distance in blocks the the entity will explore beyond the village bounds when choosing its travel point. Game default 5.
        max_travel_time (float, optional): This is the maximum amount of time an entity will attempt to reach it's travel point on the outskirts of the village before the goal exits. Game default 60.
        max_wait_time (float, optional): The wait time in seconds between choosing new explore points will be chosen on a random interval between this value and the minimum wait time. Game default 0.
        min_dist_from_target (float, optional): The entity must be within this distance for it to consider it has successfully reached its target. Game default 2.25.
        min_perimeter (float, optional): The minimum perimeter of the village required to run this goal. Game default 1.
        min_wait_time (float, optional): The wait time in seconds between choosing new explore points will be chosen on a random interval between this value and the maximum wait time. Game default 3.
        next_xz (int, optional): A new explore point will randomly be chosen within this XZ distance of the current target position when navigation has finished and the wait timer has elapsed. Game default 5.
        next_y (int, optional): A new explore point will randomly be chosen within this Y distance of the current target position when navigation has finished and the wait timer has elapsed. Game default 3.
        speed_multiplier (float, optional): The multiplier for speed while using this goal. 1.0 maintains the speed. Game default 1.
        timer_ratio (float, optional): Each new explore point will be chosen on a random interval between the minimum and the maximum wait time, divided by this value. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_explore_outskirts)
    """

    identifier = "minecraft:behavior.explore_outskirts"

    dist_from_boundary: Vector3D | None = json_field(default=None, validators=[vector3])
    explore_dist: float | None = json_field(default=None, validators=[_number])
    max_travel_time: float | None = json_field(default=None, validators=[_number])
    max_wait_time: float | None = json_field(default=None, validators=[_number])
    min_dist_from_target: float | None = json_field(default=None, validators=[_number])
    min_perimeter: float | None = json_field(default=None, validators=[_number])
    min_wait_time: float | None = json_field(default=None, validators=[_number])
    next_xz: int | None = json_field(default=None, validators=[_integer])
    next_y: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    timer_ratio: float | None = json_field(default=None, validators=[_number])


class EntityAIFertilizeFarmBlock(AIGoal):
    """Allows the mob to search within an area for a growable crop block. If found, the mob will use any available fertilizer in their inventory on the crop. This goal will not execute if the mob does not have a fertilizer item in its inventory.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached it's target position. Game default 1.5.
        max_fertilizer_usage (int, optional): The maximum number of times the mob will use fertilzer on the target block. Game default 1.
        search_cooldown_max_seconds (float, optional): The maximum amount of time in seconds that the goal can take before searching again. The time is chosen between 0 and this number. Game default 8.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 9.
        search_height (int, optional): The height in blocks the mob will search within to find a valid target position. Game default 1.
        search_range (int, optional): The distance in blocks the mob will search within to find a valid target position. Game default 1.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 0.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_fertilize_farm_block)
    """

    identifier = "minecraft:behavior.fertilize_farm_block"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_fertilizer_usage: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_cooldown_max_seconds: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIFindCover(AIGoal):
    """Allows the mob to seek shade.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_cover)
    """

    identifier = "minecraft:behavior.find_cover"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIFindMount(AIGoal):
    """Allows the mob to look around for another mob to ride atop it.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        avoid_water (bool, optional): If true, the mob will not go into water blocks when going towards a mount. Game default false.
        max_failed_attempts (int, optional): Number of attempts to find mount. Game default 20.
        mount_distance (float, optional): This is the distance the mob needs to be, in blocks, from the desired mount to mount it. If the value is below 0, the mob will use its default attack distance. Game default -1.
        start_delay (int, optional): Time the mob will wait before starting to move towards the mount. Game default 0.
        target_needed (bool, optional): If true, the mob will only look for a mount if it has a target. Game default false.
        within_radius (float, optional): Distance in blocks within which the mob will look for a mount. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_mount)
    """

    identifier = "minecraft:behavior.find_mount"

    avoid_water: bool | None = json_field(default=None, validators=[_boolean])
    max_failed_attempts: int | None = json_field(default=None, validators=[_integer])
    mount_distance: float | None = json_field(default=None, validators=[_number])
    start_delay: int | None = json_field(default=None, validators=[_integer])
    target_needed: bool | None = json_field(default=None, validators=[_boolean])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAIFindUnderwaterTreasure(AIGoal):
    """Allows the mob to move towards the nearest underwater ruin or shipwreck.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        search_range (int, optional): The range that the mob will search for a treasure chest within a ruin or shipwreck to move towards. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        stop_distance (float, optional): The distance the mob will move before stopping. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_underwater_treasure)
    """

    identifier = "minecraft:behavior.find_underwater_treasure"

    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])


class EntityAIFireAtTarget(AIGoal):
    """Allows an entity to attack by firing a shot with a delay. Anchor and offset parameters of this component overrides the anchor and offset from projectile component.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_cooldown (float, optional): The cooldown time in seconds before this goal can be used again. Game default 0.5.
        attack_range (float | NumberRange, optional): Target needs to be within this range for the attack to happen.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.
        max_head_rotation_x (float, optional): Maximum head rotation (in degrees), on the X-axis, that this entity can apply while trying to look at the target. Game default 30.
        max_head_rotation_y (float, optional): Maximum head rotation (in degrees), on the Y-axis, that this entity can apply while trying to look at the target. Game default 30.
        owner_anchor (int, optional): Entity anchor for the projectile spawn location. Game default 2.
        owner_offset (Vector3D, optional): Offset vector from the owner_anchor.
        post_shoot_delay (float, optional): Time in seconds between firing the projectile and ending the goal. Game default 0.2.
        pre_shoot_delay (float, optional): Time in seconds before firing the projectile. Game default 0.75.
        projectile_def (MinecraftEntityDescriptor | str, optional): Actor definition to use as projectile for the ranged attack. The actor must be a projectile. This field is required for the goal to be usable.
        ranged_fov (float, optional): Field of view (in degrees) when using sensing to detect a target for attack. Game default 90.
        target_anchor (int, optional): Entity anchor for projectile target. Game default 2.
        target_offset (Vector3D, optional): Offset vector from the target_anchor.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_fire_at_target)
    """

    identifier = "minecraft:behavior.fire_at_target"

    attack_cooldown: float | None = json_field(default=None, validators=[_number])
    attack_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    filters: Filter | None = json_field(default=None, validators=[_filter])
    max_head_rotation_x: float | None = json_field(default=None, validators=[_number])
    max_head_rotation_y: float | None = json_field(default=None, validators=[_number])
    owner_anchor: int | None = json_field(default=None, validators=[_integer])
    owner_offset: Vector3D | None = json_field(default=None, validators=[vector3])
    post_shoot_delay: float | None = json_field(default=None, validators=[_number])
    pre_shoot_delay: float | None = json_field(default=None, validators=[_number])
    projectile_def: MinecraftEntityDescriptor | str | None = json_field(
        default=None, validators=[_entity]
    )
    ranged_fov: float | None = json_field(default=None, validators=[_number])
    target_anchor: int | None = json_field(default=None, validators=[_integer])
    target_offset: Vector3D | None = json_field(default=None, validators=[vector3])


class EntityAIFleeSun(AIGoal):
    """Allows the mob to run away from direct sunlight and seek shade.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_flee_sun)
    """

    identifier = "minecraft:behavior.flee_sun"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIFloat(AIGoal):
    """Allows the mob to stay afloat while swimming. Passengers will be kicked out the moment the mob's head goes underwater, which may not happen for tall mobs.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        chance_per_tick_to_float (float, optional): Probability per tick (0-1) that the entity will attempt to float when in water. Game default 0.8.
        sink_with_passengers (bool, optional): If true, the mob will keep sinking as long as it has passengers. Game default false.
        time_under_water_to_dismount_passengers (float, optional): Time in seconds the entity must spend with its head underwater before any passengers are dismounted. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float)
    """

    identifier = "minecraft:behavior.float"

    chance_per_tick_to_float: float | None = json_field(
        default=None, validators=[_number]
    )
    sink_with_passengers: bool | None = json_field(default=None, validators=[_boolean])
    time_under_water_to_dismount_passengers: float | None = json_field(
        default=None, validators=[_number]
    )


class EntityAIFloatTempt(AIGoal):
    """Allows a mob to be tempted by a player holding a specific item. Uses point-to-point movement. Designed for mobs that are floating (e.g. use the "minecraft:navigation.float" component).

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        can_get_scared (bool, optional): If true, the mob can stop being tempted if the player moves too fast while close to this mob. Game default false.
        can_tempt_vertically (bool, optional): If true, vertical distance to the player will be considered when tempting. Game default false.
        can_tempt_while_ridden (bool, optional): If true, the mob can be tempted even if it has a passenger (i.e. if being ridden). Game default false.
        items (list[ItemReference], optional): List of items that can tempt the mob.
        on_tempt_end (EventTrigger | str, optional): Event to trigger when this mob stops being tempted.
        on_tempt_start (EventTrigger | str, optional): Event to trigger when this mob starts being tempted.
        sound_interval (float | NumberRange, optional): Range of random ticks to wait between tempt sounds.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        stop_distance (float, optional): The distance at which the mob will stop following the player. Game default 1.5.
        tempt_sound (str, optional): Sound to play while the mob is being tempted.
        within_radius (float, optional): Distance in blocks this mob can get tempted by a player holding an item they like. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_tempt)
    """

    identifier = "minecraft:behavior.float_tempt"

    can_get_scared: bool | None = json_field(default=None, validators=[_boolean])
    can_tempt_vertically: bool | None = json_field(default=None, validators=[_boolean])
    can_tempt_while_ridden: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    items: list[ItemReference] | None = json_field(default=None, validators=[_items])
    on_tempt_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_tempt_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])
    tempt_sound: str | None = json_field(default=None, validators=[_string])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAIFloatWander(AIGoal):
    """Allows the mob to float around like the Ghast.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        additional_collision_buffer (bool, optional): If true, the mob will have an additional buffer zone around it to avoid collisions with blocks when picking a position to wander to. Game default false.
        allow_navigating_through_liquids (bool, optional): If true allows the mob to navigate through liquids on its way to the target position. Game default false.
        float_duration (float | NumberRange, optional): Range of time in seconds the mob will float around before landing and choosing to do something else.
        float_wander_has_move_control (bool, optional): If true, the MoveControl flag will be added to the behavior which means that it can no longer be active at the same time as other behaviors with MoveControl. Game default true.
        must_reach (bool, optional): If true, the point has to be reachable to be a valid target. Game default false.
        navigate_around_surface (bool, optional): If true, will prioritize finding random positions in the vicinity of surfaces, i.e. blocks that are not Air or Liquid. Game default false.
        random_reselect (bool, optional): If true, the mob will randomly pick a new point while moving to the previously selected one. Game default false.
        surface_xz_dist (int, optional): The horizontal distance in blocks that the goal will check for a surface from a candidate position. Only valid when `navigate_around_surface` is true. Game default 8.
        surface_y_dist (int, optional): The vertical distance in blocks that the goal will check for a surface from a candidate position. Only valid when `navigate_around_surface` is true. Game default 8.
        use_home_position_restriction (bool, optional): If true, the mob will respect home position restrictions when choosing new target positions. If false, it will choose target position without considering home restrictions. Game default true.
        xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Game default 10.
        y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Game default 7.
        y_offset (float, optional): Height in blocks to add to the selected target position. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_wander)
    """

    identifier = "minecraft:behavior.float_wander"

    additional_collision_buffer: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    allow_navigating_through_liquids: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    float_duration: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    float_wander_has_move_control: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    must_reach: bool | None = json_field(default=None, validators=[_boolean])
    navigate_around_surface: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    random_reselect: bool | None = json_field(default=None, validators=[_boolean])
    surface_xz_dist: int | None = json_field(default=None, validators=[_integer])
    surface_y_dist: int | None = json_field(default=None, validators=[_integer])
    use_home_position_restriction: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    xz_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_offset: float | None = json_field(default=None, validators=[_number])


class EntityAIFollowCaravan(EntityTypesAIGoal):
    """Allows the mob to follow mobs that are in a caravan.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        entity_count (int, optional): Number of entities that can be in the caravan. Game default 1.
        entity_types (list[GoalEntityType], optional): List of entity types that this mob can follow in a caravan. Can be a single filter object or an array of filter objects. Add entries with `add_entity_type`.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_caravan)
    """

    identifier = "minecraft:behavior.follow_caravan"

    entity_count: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIFollowMob(AIGoal):
    """Allows the mob to follow other mobs.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        filters (Filter, optional): If non-empty, provides criteria for filtering which nearby Mobs can be followed.
        preferred_actor_type (MinecraftEntityDescriptor | str, optional): The type of actor to prefer following. If left unspecified, a random actor among those in range will be chosen.
        search_range (int, optional): The distance in blocks it will look for a mob to follow. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        stop_distance (float, optional): The distance in blocks this mob stops from the mob it is following. Game default 2.
        use_home_position_restriction (bool, optional): If true, the mob will respect the 'minecraft:home' component's 'restriction_radius' field when choosing a target to follow. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_mob)
    """

    identifier = "minecraft:behavior.follow_mob"

    filters: Filter | None = json_field(default=None, validators=[_filter])
    preferred_actor_type: MinecraftEntityDescriptor | str | None = json_field(
        default=None, validators=[_entity]
    )
    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])
    use_home_position_restriction: bool | None = json_field(
        default=None, validators=[_boolean]
    )


class EntityAIFollowOwner(AIGoal):
    """Allows a mob to follow the player that owns it.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        can_teleport (bool, optional): Defines if the mob will teleport to its owner when too far away. Game default true.
        ignore_vibration (bool, optional): Defines if the mob should disregard following its owner after detecting a recent vibration. Game default false.
        max_distance (float, optional): The maximum distance the mob can be from its owner to start following it. Applicable only when "can_teleport" is set to false. Game default 60.
        post_teleport_distance (int, optional): Defines how far (in blocks) the entity will be from its owner after teleporting. If not specified, it defaults to "stop_distance" + 1, allowing the entity to seamlessly resume navigation. Game default 3.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        start_distance (float, optional): The minimum distance the mob must be from its owner to start following it. Game default 10.
        stop_distance (float, optional): The distance at which the mob will stop following its owner. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_owner)
    """

    identifier = "minecraft:behavior.follow_owner"

    can_teleport: bool | None = json_field(default=None, validators=[_boolean])
    ignore_vibration: bool | None = json_field(default=None, validators=[_boolean])
    max_distance: float | None = json_field(default=None, validators=[_number])
    post_teleport_distance: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    start_distance: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])


class EntityAIFollowParent(AIGoal):
    """Allows the mob to follow their parent around.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_parent)
    """

    identifier = "minecraft:behavior.follow_parent"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIFollowTargetLead(AIGoal):
    """Allows the mob to move towards its target lead. Not in the Microsoft reference.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        always_look_for_leader (bool, optional): The mob keeps searching for a valid leader when it has none. Game default false.
        follow_distance (float, optional): Distance in blocks the mob stays from its leader. Game default 0.
        leader_filters (Filter, optional): Conditions a leader must meet.
        search_cooldown (float, optional): Ticks before a new search after the leader is not found, lost or invalid. Game default 20.
        within_radius (float, optional): Maximum distance in blocks to the leader before the mob stops following it. Game default 0.
    """

    identifier = "minecraft:behavior.follow_target_lead"

    always_look_for_leader: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    follow_distance: float | None = json_field(default=None, validators=[_positive])
    leader_filters: Filter | None = json_field(default=None, validators=[_filter])
    search_cooldown: float | None = json_field(default=None, validators=[_positive])
    within_radius: float | None = json_field(default=None, validators=[_positive])


class EntityAIGoAndGiveItemsToNoteblock(AIGoal):
    """The entity will attempt to toss the items from its inventory to a nearby recently played noteblock.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        listen_time (int, optional): Sets the time an entity should continue delivering items to a noteblock after hearing it. Game default 30.
        on_item_throw (EventTrigger | str | list[EventTrigger | str], optional): Event(s) to run when this mob throws items.
        reach_block_distance (float, optional): Sets the desired distance to be reached before throwing the items towards the block. Game default 3.
        run_speed (float, optional): Sets the entity's speed when running toward the block. Game default 1.
        throw_force (float, optional): Sets the throw force. Game default 0.2.
        throw_sound (str, optional): Sound to play when this mob throws an item. Game default charge.
        vertical_throw_mul (float, optional): Sets the vertical throw multiplier that is applied on top of the throw force in the vertical direction. Game default 1.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_and_give_items_to_noteblock)
    """

    identifier = "minecraft:behavior.go_and_give_items_to_noteblock"

    listen_time: int | None = json_field(default=None, validators=[_integer])
    on_item_throw: EventTrigger | str | list[EventTrigger | str] | None = json_field(
        default=None, validators=[_events], encoder=encoders.trigger
    )
    reach_block_distance: float | None = json_field(default=None, validators=[_number])
    run_speed: float | None = json_field(default=None, validators=[_number])
    throw_force: float | None = json_field(default=None, validators=[_number])
    throw_sound: str | None = json_field(default=None, validators=[_string])
    vertical_throw_mul: float | None = json_field(default=None, validators=[_number])


class EntityAIGoAndGiveItemsToOwner(AIGoal):
    """The entity will attempt to toss the items from its inventory to its owner.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        on_item_throw (EventTrigger | str | list[EventTrigger | str], optional): Event(s) to run when this mob throws items.
        reach_mob_distance (float, optional): Sets the desired distance to be reached before giving items to owner. Game default 3.
        run_speed (float, optional): Sets the entity's speed when running toward the owner. Game default 1.
        throw_force (float, optional): Sets the throw force. Game default 0.2.
        throw_sound (str, optional): Sound to play when this mob throws an item. Game default charge.
        vertical_throw_mul (float, optional): Sets the vertical throw multiplier that is applied on top of the throw force in the vertical direction. Game default 1.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_and_give_items_to_owner)
    """

    identifier = "minecraft:behavior.go_and_give_items_to_owner"

    on_item_throw: EventTrigger | str | list[EventTrigger | str] | None = json_field(
        default=None, validators=[_events], encoder=encoders.trigger
    )
    reach_mob_distance: float | None = json_field(default=None, validators=[_number])
    run_speed: float | None = json_field(default=None, validators=[_number])
    throw_force: float | None = json_field(default=None, validators=[_number])
    throw_sound: str | None = json_field(default=None, validators=[_string])
    vertical_throw_mul: float | None = json_field(default=None, validators=[_number])


class EntityAIGoHome(AIGoal):
    """Allows the mob to move back to the position they were spawned.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        calculate_new_path_radius (float, optional): Distance in blocks that the mob is considered close enough to the end of the current path. A new path will then be calculated to continue toward home. Game default 2.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Game default 120.
        on_failed (EventTrigger | str | list[EventTrigger | str], optional): Event(s) to run when this goal fails.
        on_home (EventTrigger | str | list[EventTrigger | str], optional): Event(s) to run when this mob gets home.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_home)
    """

    identifier = "minecraft:behavior.go_home"

    calculate_new_path_radius: float | None = json_field(
        default=None, validators=[_number]
    )
    goal_radius: float | None = json_field(default=None, validators=[_number])
    interval: int | None = json_field(default=None, validators=[_integer])
    on_failed: EventTrigger | str | list[EventTrigger | str] | None = json_field(
        default=None, validators=[_events], encoder=encoders.trigger
    )
    on_home: EventTrigger | str | list[EventTrigger | str] | None = json_field(
        default=None, validators=[_events], encoder=encoders.trigger
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIGuardianAttack(AIGoal):
    """Allows this entity to use a laser beam attack. Can only be used by Guardians and Elder Guardians.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        elder_extra_magic_damage (int, optional): Amount of additional damage dealt from an elder guardian's magic attack. Game default 2.
        hard_mode_extra_magic_damage (int, optional): In hard difficulty, amount of additional damage dealt from a guardian's magic attack. Game default 2.
        magic_damage (int, optional): Amount of damage dealt from a guardian's magic attack. Magic attack damage is added to the guardian's base attack damage. Game default 1.
        min_distance (float, optional): Guardian attack behavior stops if the target is closer than this distance (doesn't apply to elders). Game default 3.
        sound_delay_time (float, optional): Time (in seconds) to wait after starting an attack before playing the guardian attack sound. Game default 0.5.
        x_max_rotation (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Game default 90.
        y_max_head_rotation (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Game default 90.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_guardian_attack)
    """

    identifier = "minecraft:behavior.guardian_attack"

    elder_extra_magic_damage: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    hard_mode_extra_magic_damage: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    magic_damage: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    min_distance: float | None = json_field(default=None, validators=[_number])
    sound_delay_time: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    x_max_rotation: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    y_max_head_rotation: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )


class EntityAIHarvestFarmBlock(AIGoal):
    """Allows the entity to search within an area for farmland with air above it. If found, the entity will replace the air block by planting a seed item from its inventory on the farmland block. This goal will not execute if the entity does not have an item in its inventory.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the entity considers it has reached it's target position. Game default 1.5.
        max_seconds_before_search (float, optional): The maximum amount of time in seconds that the goal can take before searching for the first harvest block. The time is chosen between 0 and this number. Game default 1.
        search_cooldown_max_seconds (float, optional): The maximum amount of time in seconds that the goal can take before searching again, after failing to find a a harvest block already. The time is chosen between 0 and this number. Game default 8.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 0.
        search_height (int, optional): The height in blocks the entity will search within to find a valid target position. Game default 1.
        search_range (int, optional): The distance in blocks the entity will search within to find a valid target position. Game default 16.
        seconds_until_new_task (float, optional): The amount of time in seconds that the goal will cooldown after a successful reap/sow, before it can start again. Game default 0.5.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 0.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_harvest_farm_block)
    """

    identifier = "minecraft:behavior.harvest_farm_block"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_seconds_before_search: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_cooldown_max_seconds: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    seconds_until_new_task: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIHide(AIGoal):
    """Allows a mob with the hide component to attempt to move to - and hide at - an owned or nearby POI.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        duration (float, optional): Amount of time in seconds that the mob reacts. Game default 1.
        poi_type (Literal["bed", "jobsite", "meeting_area"], optional): Tells the goal what POI type it should be looking for. Game default null.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.
        timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after a internal failure or timeout condition. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hide)
    """

    identifier = "minecraft:behavior.hide"

    duration: float | None = json_field(default=None, validators=[_number])
    poi_type: Literal["bed", "jobsite", "meeting_area"] | None = json_field(
        default=None, validators=[one_of("bed", "jobsite", "meeting_area")]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    timeout_cooldown: float | None = json_field(default=None, validators=[_number])


class EntityAIHoldGround(AIGoal):
    """Compels an entity to stop at their current location, turn to face a mob they are targeting, and react with an event.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        broadcast (bool, optional): Whether to broadcast out the mob's target to other mobs of the same type. Game default false.
        broadcast_range (float, optional): Range in blocks for how far to broadcast. Game default 0.
        min_radius (float, optional): Minimum distance the target must be for the mob to run this goal. Game default 10.
        within_radius_event (EventTrigger | str, optional): Event to run when target is within the radius. This event is broadcasted if broadcast is true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hold_ground)
    """

    identifier = "minecraft:behavior.hold_ground"

    broadcast: bool | None = json_field(default=None, validators=[_boolean])
    broadcast_range: float | None = json_field(default=None, validators=[_number])
    min_radius: float | None = json_field(default=None, validators=[_number])
    within_radius_event: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAIHurtByTarget(EntityTypesAIGoal):
    """Allows the mob to target another mob that hurts them.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        alert_same_type (bool, optional): If true, nearby mobs of the same type will be alerted about the damage. Game default false.
        entity_types (list[GoalEntityType], optional): List of entity types that this mob can target when hurt by them. Add entries with `add_entity_type`.
        hurt_owner (bool, optional): If true, the mob will hurt its owner and other mobs with the same owner as itself. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hurt_by_target)
    """

    identifier = "minecraft:behavior.hurt_by_target"

    alert_same_type: bool | None = json_field(default=None, validators=[_boolean])
    hurt_owner: bool | None = json_field(default=None, validators=[_boolean])


class EntityAIInspectBookshelf(AIGoal):
    """Allows the mob to inspect bookshelves.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 10.
        search_height (int, optional): The height that the mob will search for bookshelves. Game default 1.
        search_range (int, optional): The distance in blocks the mob will look for books to inspect. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_inspect_bookshelf)
    """

    identifier = "minecraft:behavior.inspect_bookshelf"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIInvestigateSuspiciousLocation(AIGoal):
    """Allows this entity to move towards a "suspicious" position based on data gathered in `minecraft:suspect_tracking`.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the entity considers it has reached it's target position. Game default 1.5.
        speed_multiplier (float, optional): Movement speed multiplier. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_investigate_suspicious_location)
    """

    identifier = "minecraft:behavior.investigate_suspicious_location"

    goal_radius: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIJumpAroundTarget(AIGoal):
    """Allows an entity to jump around a target.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        check_collision (bool, optional): Enables collision checks when calculating the jump. Setting check_collision to true may affect performance and should be used with care. Game default false.
        entity_bounding_box_scale (float, optional): Scaling temporarily applied to the entity's AABB bounds when jumping. Game default 0.7.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.
        jump_angles (list[float], optional): The jump angles in float degrees that are allowed when performing the jump. The order in which the angles are chosen is randomized.
        jump_cooldown_duration (float, optional): The time in seconds to spend in cooldown before this goal can be used again. Game default 0.5.
        jump_cooldown_when_hurt_duration (float, optional): The time in seconds to spend in cooldown after being hurt before this goal can be used again. Game default 0.1.
        landing_distance_from_target (float | NumberRange, optional): The range deciding how close to and how far away from the target the landing position can be when jumping.
        landing_position_spread_degrees (int, optional): This angle (in degrees) is used for controlling the spread when picking a landing position behind the target. Game default 90.
        last_hurt_duration (float, optional): If the entity was hurt within these last seconds, the jump_cooldown_when_hurt_duration will be used instead of jump_cooldown_duration. Game default 2.
        line_of_sight_obstruction_height_ignore (int, optional): If the entity's line of sight towards its target is obstructed by an obstacle with a height below this number, the obstacle will be ignored, and the goal will try to find a valid landing position. Game default 4.
        max_jump_velocity (float, optional): Maximum velocity a jump can be performed at. Game default 1.4.
        prepare_jump_duration (float, optional): The time in seconds to spend preparing for the jump. Game default 0.5.
        required_vertical_space (int, optional): The number of blocks above the entity's head that has to be air for this goal to be usable. Game default 4.
        snap_to_surface_block_range (int, optional): The number of blocks above and below from the jump target position that will be checked to find a surface to land on. Game default 10.
        valid_distance_to_target (float | NumberRange, optional): Target needs to be within this range for the jump to happen.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_jump.around_target)
    """

    identifier = "minecraft:behavior.jump_around_target"

    check_collision: bool | None = json_field(default=None, validators=[_boolean])
    entity_bounding_box_scale: float | None = json_field(
        default=None, validators=[_number]
    )
    filters: Filter | None = json_field(default=None, validators=[_filter])
    jump_angles: list[float] | None = json_field(
        default=None, validators=[each(_number)]
    )
    jump_cooldown_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    jump_cooldown_when_hurt_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    landing_distance_from_target: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    landing_position_spread_degrees: int | None = json_field(
        default=None, validators=[_integer]
    )
    last_hurt_duration: float | None = json_field(default=None, validators=[_number])
    line_of_sight_obstruction_height_ignore: int | None = json_field(
        default=None, validators=[_integer]
    )
    max_jump_velocity: float | None = json_field(default=None, validators=[_number])
    prepare_jump_duration: float | None = json_field(default=None, validators=[_number])
    required_vertical_space: int | None = json_field(
        default=None, validators=[_integer]
    )
    snap_to_surface_block_range: int | None = json_field(
        default=None, validators=[_integer]
    )
    valid_distance_to_target: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )


class EntityAIJumpToBlock(AIGoal):
    """Allows an entity to jump to another random block.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_range (float | NumberRange, optional): Minimum and maximum cooldown time-range (positive, in seconds) between each attempted jump.
        forbidden_blocks (list[BlockReference], optional): Blocks that the mob can't jump to.
        max_velocity (float, optional): The maximum velocity with which the mob can jump. Game default 1.5.
        minimum_distance (int, optional): The minimum distance (in blocks) from the mob to a block, in order to consider jumping to it. Game default 2.
        minimum_path_length (int, optional): The minimum length (in blocks) of the mobs path to a block, in order to consider jumping to it. Game default 5.
        preferred_blocks (list[BlockReference], optional): Blocks that the mob prefers jumping to.
        preferred_blocks_chance (float, optional): Chance (between 0.0 and 1.0) that the mob will jump to a preferred block, if in range. Only matters if preferred blocks are defined. Game default 1.
        scale_factor (float, optional): The scalefactor of the bounding box of the mob while it is jumping. Game default 0.7.
        search_height (int, optional): The height (in blocks, in range [1, 15]) of the search box, centered around the mob. Game default 10.
        search_width (int, optional): The width (in blocks, in range [1, 15]) of the search box, centered around the mob. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_jump.to_block)
    """

    identifier = "minecraft:behavior.jump_to_block"

    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    forbidden_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks]
    )
    max_velocity: float | None = json_field(default=None, validators=[_number])
    minimum_distance: int | None = json_field(default=None, validators=[_integer])
    minimum_path_length: int | None = json_field(default=None, validators=[_integer])
    preferred_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks]
    )
    preferred_blocks_chance: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    scale_factor: float | None = json_field(default=None, validators=[_number])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1, maximum=15)]
    )
    search_width: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1, maximum=15)]
    )


class EntityAIKnockbackRoar(AIGoal):
    """Allows the mob to perform a damaging knockback that affects all nearby entities.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_time (float, optional): The delay after which the knockback occurs (in seconds). Game default 0.5.
        cooldown_time (float, optional): Time (in seconds) the mob has to wait before using the goal again. Game default 0.1.
        damage_filters (Filter, optional): The list of conditions another entity must meet to be a valid target to apply damage to.
        duration (float, optional): The max duration of the roar (in seconds). Game default 1.
        knockback_damage (int, optional): The damage dealt by the knockback roar. Game default 6.
        knockback_filters (Filter, optional): The list of conditions another entity must meet to be a valid target to apply knockback to.
        knockback_height_cap (float, optional): The maximum height for vertical knockback. Game default 0.4.
        knockback_horizontal_strength (int, optional): The strength of the horizontal knockback. Game default 4.
        knockback_range (int, optional): The radius (in blocks) of the knockback effect. Game default 4.
        knockback_vertical_strength (int, optional): The strength of the vertical knockback. Game default 4.
        on_roar_end (EventTrigger | str, optional): Event that is triggered when the roar ends. Can be an object with event and target properties, or a simple event string.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_knockback_roar)
    """

    identifier = "minecraft:behavior.knockback_roar"

    attack_time: float | None = json_field(default=None, validators=[_number])
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    damage_filters: Filter | None = json_field(default=None, validators=[_filter])
    duration: float | None = json_field(default=None, validators=[_number])
    knockback_damage: int | None = json_field(default=None, validators=[_integer])
    knockback_filters: Filter | None = json_field(default=None, validators=[_filter])
    knockback_height_cap: float | None = json_field(default=None, validators=[_number])
    knockback_horizontal_strength: int | None = json_field(
        default=None, validators=[_integer]
    )
    knockback_range: int | None = json_field(default=None, validators=[_integer])
    knockback_vertical_strength: int | None = json_field(
        default=None, validators=[_integer]
    )
    on_roar_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAILayDown(AIGoal):
    """Allows mobs to lay down at times.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        interval (int, optional): A random value to determine at what intervals something can occur. This has a 1/interval chance to choose this goal. Game default 120.
        random_stop_interval (int, optional): A random value in which the goal can use to pull out of the behavior. This is a 1/interval chance to stop laying down. Game default 120.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_down)
    """

    identifier = "minecraft:behavior.lay_down"

    interval: int | None = json_field(default=None, validators=[_integer])
    random_stop_interval: int | None = json_field(default=None, validators=[_integer])


class EntityAILayEgg(AIGoal):
    """Allows the mob to lay an egg block on certain types of blocks if the mob is pregnant.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        allow_laying_from_below (bool, optional): Allows the mob to lay its eggs from below the target if it can't get there. This is useful if the target block is water with air above, since mobs may not be able to get to the air block above water. Game default false.
        egg_type (BlockReference, optional): Block type for the egg to lay. If this is a turtle egg, the number of eggs in the block is randomly set. Game default minecraft:turtle_egg.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        lay_egg_sound (str, optional): Name of the sound event played when laying the egg. Defaults to lay_egg, which is used for Turtles. Game default lay_egg.
        lay_seconds (float, optional): Duration of the laying egg process in seconds. From 1.26.10 onward, `lay_seconds` only accepts values greater than or equal to 0; entity JSON with negative values will fail to load. Game default 10.
        on_lay (EventTrigger | str, optional): Event to run when this mob lays the egg.
        search_height (int, optional): The height in blocks the mob will look for the block to move towards. Game default 1.
        search_range (int, optional): The distance in blocks it will look for the block to move towards. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.
        target_blocks (list[BlockReference], optional): Blocks that the mob can lay its eggs on top of.
        target_materials_above_block (list[Literal["Air", "Lava", "Water"]], optional): Types of materials that can exist above the target block. Valid types are Air, Water, and Lava.
        use_default_animation (bool, optional): Specifies if the default lay-egg animation should be played when the egg is placed or not. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_egg)
    """

    identifier = "minecraft:behavior.lay_egg"

    allow_laying_from_below: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    egg_type: BlockReference | None = json_field(default=None, validators=[_block])
    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    lay_egg_sound: str | None = json_field(default=None, validators=[_string])
    lay_seconds: float | None = json_field(default=None, validators=[_number])
    on_lay: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    target_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks]
    )
    target_materials_above_block: list[Literal["Air", "Lava", "Water"]] | None = (
        json_field(default=None, validators=[each(one_of("Air", "Lava", "Water"))])
    )
    use_default_animation: bool | None = json_field(default=None, validators=[_boolean])


class EntityAILeapAtTarget(AIGoal):
    """Allows monsters to jump at and attack their target. Can only be used by hostile mobs.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        must_be_on_ground (bool, optional): If true, the mob will only jump at its target if its on the ground. Setting it to false will allow it to jump even if its already in the air. Game default true.
        set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Game default false.
        yd (float, optional): The height in blocks the mob jumps when leaping at its target. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_leap_at_target)
    """

    identifier = "minecraft:behavior.leap_at_target"

    must_be_on_ground: bool | None = json_field(default=None, validators=[_boolean])
    set_persistent: bool | None = json_field(default=None, validators=[_boolean])
    yd: float | None = json_field(default=None, validators=[_number])


class EntityAILookAtEntity(AIGoal):
    """Compels an entity to look at a specific entity by rotating the `head` bone pose within a set limit.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Game default 360.
        angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Game default 360.
        filters (Filter, optional): Filter to determine the conditions for this mob to look at the entity.
        look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Game default 8.
        look_time (float | NumberRange, optional): Time range to look at the nearest entity.
        probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Game default 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_entity)
    """

    identifier = "minecraft:behavior.look_at_entity"

    angle_of_view_horizontal: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    angle_of_view_vertical: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    filters: Filter | None = json_field(default=None, validators=[_filter])
    look_distance: float | None = json_field(default=None, validators=[_number])
    look_time: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    probability: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )


class EntityAILookAtPlayer(AIGoal):
    """Compels an entity to look at the player by rotating the `head` bone pose within a set limit.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Game default 360.
        angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Game default 360.
        look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Game default 8.
        look_time (float | NumberRange, optional): Time range to look at the nearest entity.
        max_look_time (float, optional):
        min_look_time (float, optional):
        probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Game default 0.02.
        target_distance (float, optional):

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_player)
    """

    identifier = "minecraft:behavior.look_at_player"

    angle_of_view_horizontal: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    angle_of_view_vertical: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    look_distance: float | None = json_field(default=None, validators=[_number])
    look_time: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    max_look_time: float | None = json_field(default=None, validators=[_number])
    min_look_time: float | None = json_field(default=None, validators=[_number])
    probability: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    target_distance: float | None = json_field(default=None, validators=[_number])


class EntityAILookAtTarget(AIGoal):
    """Compels an entity to look at the target by rotating the head bone pose within a set limit.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Game default 360.
        angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Game default 360.
        look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Game default 8.
        look_time (float | NumberRange, optional): Time range to look at the nearest entity.
        probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Game default 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_target)
    """

    identifier = "minecraft:behavior.look_at_target"

    angle_of_view_horizontal: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    angle_of_view_vertical: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    look_distance: float | None = json_field(default=None, validators=[_number])
    look_time: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    probability: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )


class EntityAILookAtTradingPlayer(AIGoal):
    """Compels an entity to look at the player that is currently trading with the entity.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Game default 360.
        angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Game default 360.
        look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Game default 8.
        look_time (float | NumberRange, optional): Time range to look at the nearest entity.
        probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Game default 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_trading_player)
    """

    identifier = "minecraft:behavior.look_at_trading_player"

    angle_of_view_horizontal: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    angle_of_view_vertical: int | None = json_field(
        default=None, validators=[_integer, in_range(maximum=360)]
    )
    look_distance: float | None = json_field(default=None, validators=[_number])
    look_time: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    probability: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )


class EntityAIMakeLove(AIGoal):
    """Allows the villager to look for a mate to spawn other villagers with.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_make_love)
    """

    identifier = "minecraft:behavior.make_love"


class EntityAIMeleeAttack(AIGoal):
    """Allows an entity to deal damage through a melee attack.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Game default false.
        attack_types (str, optional): Defines the entity types this entity will attack.
        can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Game default false.
        cooldown_time (float, optional): Cooldown time, in seconds, between consecutive attacks. Game default 1.
        inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Game default 0.25.
        max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.55.
        melee_fov (float, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Game default 90.
        min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.2.
        on_attack (EventTrigger | str, optional): Defines the event to trigger when this entity successfully attacks.
        on_kill (EventTrigger | str, optional): Defines the event to trigger when this entity kills the target.
        outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Game default 0.5.
        path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Game default 0.75.
        path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Game default 16.
        path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Game default 32.
        random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Game default 0.
        reach_multiplier (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Game default 2.
        require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Game default false.
        speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Game default 1.
        track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Game default false.
        x_max_rotation (float, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_melee_attack)
    """

    identifier = "minecraft:behavior.melee_attack"

    attack_once: bool | None = json_field(default=None, validators=[_boolean])
    attack_types: str | None = json_field(default=None, validators=[_string])
    can_spread_on_fire: bool | None = json_field(default=None, validators=[_boolean])
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    inner_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    max_path_time: float | None = json_field(default=None, validators=[_number])
    melee_fov: float | None = json_field(default=None, validators=[_number])
    min_path_time: float | None = json_field(default=None, validators=[_number])
    on_attack: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_kill: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    outer_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_fail_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_inner_boundary: float | None = json_field(default=None, validators=[_number])
    path_outer_boundary: float | None = json_field(default=None, validators=[_number])
    random_stop_interval: int | None = json_field(default=None, validators=[_integer])
    reach_multiplier: float | None = json_field(default=None, validators=[_number])
    require_complete_path: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    track_target: bool | None = json_field(default=None, validators=[_boolean])
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_head_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAIMeleeBoxAttack(AIGoal):
    """Allows an entity to deal damage through a melee attack with reach calculations based on bounding boxes.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Game default false.
        attack_types (str, optional): Defines the entity types this entity will attack.
        can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Game default false.
        cooldown_time (float, optional): Cooldown time, in seconds, between consecutive attacks. Game default 1.
        horizontal_reach (float, optional): The attack reach of the mob will be a box with the size of the mobs bounds increased by this value in all horizontal directions. Game default 0.8.
        inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Game default 0.25.
        max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.55.
        melee_fov (float, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Game default 90.
        min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.2.
        on_attack (EventTrigger | str, optional): Defines the event to trigger when this entity successfully attacks.
        on_kill (EventTrigger | str, optional): Defines the event to trigger when this entity kills the target.
        outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Game default 0.5.
        path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Game default 0.75.
        path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Game default 16.
        path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Game default 32.
        random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Game default 0.
        require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Game default false.
        speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Game default 1.
        track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Game default false.
        x_max_rotation (float, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_melee_box_attack)
    """

    identifier = "minecraft:behavior.melee_box_attack"

    attack_once: bool | None = json_field(default=None, validators=[_boolean])
    attack_types: str | None = json_field(default=None, validators=[_string])
    can_spread_on_fire: bool | None = json_field(default=None, validators=[_boolean])
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    horizontal_reach: float | None = json_field(default=None, validators=[_number])
    inner_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    max_path_time: float | None = json_field(default=None, validators=[_number])
    melee_fov: float | None = json_field(default=None, validators=[_number])
    min_path_time: float | None = json_field(default=None, validators=[_number])
    on_attack: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_kill: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    outer_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_fail_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_inner_boundary: float | None = json_field(default=None, validators=[_number])
    path_outer_boundary: float | None = json_field(default=None, validators=[_number])
    random_stop_interval: int | None = json_field(default=None, validators=[_integer])
    require_complete_path: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    track_target: bool | None = json_field(default=None, validators=[_boolean])
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_head_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAIMingle(AIGoal):
    """Allows an entity to go to the village bell and mingle with other entities.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.
        duration (float, optional): Amount of time in seconds that the entity will chat with another entity. Game default 1.
        mingle_distance (float, optional): The distance from its partner that this entity will mingle. If the entity type is not the same as the entity, this value needs to be identical on both entities. Game default 2.
        mingle_partner_type (MinecraftEntityDescriptor | str, optional): The entity type that this entity is allowed to mingle with.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_mingle)
    """

    identifier = "minecraft:behavior.mingle"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    duration: float | None = json_field(default=None, validators=[_number])
    mingle_distance: float | None = json_field(default=None, validators=[_number])
    mingle_partner_type: MinecraftEntityDescriptor | str | None = json_field(
        default=None, validators=[_entity]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMountPathing(AIGoal):
    """Allows the mob to move around on its own while mounted seeking a target to attack. Also will allow an entity to target another entity for an attack.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        target_dist (float, optional): The distance at which this mob wants to be away from its target. Game default 0.
        track_target (bool, optional): If true, this mob will chase after the target as long as it's a valid target. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_mount_pathing)
    """

    identifier = "minecraft:behavior.mount_pathing"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    target_dist: float | None = json_field(default=None, validators=[_number])
    track_target: bool | None = json_field(default=None, validators=[_boolean])


class EntityAIMoveAroundTarget(AIGoal):
    """Allows an entity to move around a target.If the entity is too close(i.e.closer than destination range min and height difference limit) it will try to move away from its target.If the entity is too far away from its target it will try to move closer to a random position within the destination range.A randomized amount of those positions will be behind the target, and the spread can be tweaked with 'destination_pos_spread_degrees'.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        destination_pos_spread_degrees (float, optional): This angle (in degrees) is used for controlling the spread when picking a destination position behind the target. Game default 90.
        destination_position_range (float | NumberRange, optional): The range of distances from the target entity within which the goal should look for a position to move the owner entity to.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.
        height_difference_limit (float, optional): Distance in height (in blocks) between the owner entity and the target has to be less than this value when owner checks if it is too close and should move away from the target. Game default 10.
        horizontal_search_distance (int, optional): Horizontal search distance (in blocks) when searching for a position to move away from target. Game default 5.
        movement_speed (float, optional): The speed with which the entity should move to its target position. Game default 0.6.
        vertical_search_distance (int, optional): Vertical search distance (in blocks) when searching for a position to move away from target. Game default 5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_around_target)
    """

    identifier = "minecraft:behavior.move_around_target"

    destination_pos_spread_degrees: float | None = json_field(
        default=None, validators=[_number]
    )
    destination_position_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    filters: Filter | None = json_field(default=None, validators=[_filter])
    height_difference_limit: float | None = json_field(
        default=None, validators=[_number]
    )
    horizontal_search_distance: int | None = json_field(
        default=None, validators=[_integer]
    )
    movement_speed: float | None = json_field(default=None, validators=[_number])
    vertical_search_distance: int | None = json_field(
        default=None, validators=[_integer]
    )


class EntityAIMoveIndoors(AIGoal):
    """Allows this entity to move indoors.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): The movement speed modifier to apply to the entity while it is moving indoors. Game default 0.8.
        timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after pathfinding fails. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_indoors)
    """

    identifier = "minecraft:behavior.move_indoors"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    timeout_cooldown: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveOutdoors(AIGoal):
    """Allows this entity to move outdoors.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): The radius away from the target block to count as reaching the goal. Game default 2.
        search_count (int, optional): The amount of times to try finding a random outdoors position before failing. Game default 10.
        search_height (int, optional): The y range to search for an outdoors position for. Game default 5.
        search_range (int, optional): The x and z range to search for an outdoors position for. Game default 15.
        speed_multiplier (float, optional): The movement speed modifier to apply to the entity while it is moving outdoors. Game default 0.5.
        timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after pathfinding fails. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_outdoors)
    """

    identifier = "minecraft:behavior.move_outdoors"

    goal_radius: float | None = json_field(default=None, validators=[_number])
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(default=None, validators=[_integer])
    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    timeout_cooldown: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveThroughVillage(AIGoal):
    """Can only be used by Villagers. Allows the villagers to create paths around the village.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        only_at_night (bool, optional): If true, the mob will only move through the village during night time. Game default false.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_through_village)
    """

    identifier = "minecraft:behavior.move_through_village"

    only_at_night: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToBlock(AIGoal):
    """Allows mob to move towards a block.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        on_reach (EventTrigger | str | list[EventTrigger | str], optional): Event to run on block reached.
        on_stay_completed (EventTrigger | str | list[EventTrigger | str], optional): Event to run on completing a stay of stay_duration at the block.
        search_height (int, optional): The height in blocks that the mob will look for the block. Game default 1.
        search_range (int, optional): The distance in blocks that the mob will look for the block. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        start_chance (float, optional): Chance to start the behavior (applied after each random tick_interval). Game default 1.
        stay_duration (float, optional): Number of ticks needed to complete a stay at the block. Game default 0.
        target_block_filters (Filter, optional): Conditions that need to be met for a block to be a valid target.
        target_blocks (list[BlockReference], optional): Block types to move to.
        target_offset (Vector3D, optional): Offset to add to the selected target position.
        target_selection_method (Literal["nearest", "random"], optional): Kind of block to find fitting the specification. Valid values are "random" and "nearest". Game default nearest.
        tick_interval (int, optional): Average interval in ticks to try to run this behavior. Game default 20.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_block)
    """

    identifier = "minecraft:behavior.move_to_block"

    goal_radius: float | None = json_field(default=None, validators=[_number])
    on_reach: EventTrigger | str | list[EventTrigger | str] | None = json_field(
        default=None, validators=[_events], encoder=encoders.trigger
    )
    on_stay_completed: EventTrigger | str | list[EventTrigger | str] | None = (
        json_field(default=None, validators=[_events], encoder=encoders.trigger)
    )
    search_height: int | None = json_field(default=None, validators=[_integer])
    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    start_chance: float | None = json_field(default=None, validators=[_number])
    stay_duration: float | None = json_field(default=None, validators=[_number])
    target_block_filters: Filter | None = json_field(default=None, validators=[_filter])
    target_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks]
    )
    target_offset: Vector3D | None = json_field(default=None, validators=[vector3])
    target_selection_method: Literal["nearest", "random"] | None = json_field(
        default=None, validators=[one_of("nearest", "random")]
    )
    tick_interval: int | None = json_field(default=None, validators=[_integer])


class EntityAIMoveToLand(AIGoal):
    """Allows the mob to move back onto land when in water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 10.
        search_height (int, optional): Height in blocks the mob will look for land to move towards. Game default 1.
        search_range (int, optional): The distance in blocks it will look for land to move towards. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_land)
    """

    identifier = "minecraft:behavior.move_to_land"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToLava(AIGoal):
    """Allows the mob to move into lava when on land. Not in the Microsoft reference.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks at which the mob considers it has reached the goal. Game default 0.5.
        search_count (int, optional): Number of random blocks checked each tick for lava to move to. Game default 10.
        search_height (int, optional): Height in blocks the mob looks for lava in. Game default 1.
        search_range (int, optional): Distance in blocks the mob looks for lava in. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier while using this goal. Game default 1.
    """

    identifier = "minecraft:behavior.move_to_lava"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(
        default=None, validators=[_integer, _positive]
    )
    search_height: int | None = json_field(
        default=None, validators=[_integer, _positive]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, _positive]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToLiquid(AIGoal):
    """Allows the mob to move into a liquid when on land.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        material_type (Literal["Any", "Lava", "Water"], optional): The material type of the liquid block to find. Valid values are "Any", "Water", and "Lava". Game default any.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 10.
        search_height (int, optional): Height in blocks the mob will look for the liquid block to move towards. Game default 1.
        search_range (int, optional): The distance in blocks it will look for the liquid block to move towards. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_liquid)
    """

    identifier = "minecraft:behavior.move_to_liquid"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    material_type: Literal["Any", "Lava", "Water"] | None = json_field(
        default=None, validators=[one_of("Any", "Lava", "Water")]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToPOI(AIGoal):
    """Allows the mob to move to a POI if able to.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        poi_type (Literal["bed", "jobsite", "meeting_area"], optional): Tells the goal what POI type it should be looking for. Game default null.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_poi)
    """

    identifier = "minecraft:behavior.move_to_poi"

    poi_type: Literal["bed", "jobsite", "meeting_area"] | None = json_field(
        default=None, validators=[one_of("bed", "jobsite", "meeting_area")]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToRandomBlock(AIGoal):
    """Allows mob to move towards a random block.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        block_distance (float, optional): Defines the distance from the mob, in blocks, that the block to move to will be chosen. Game default 16.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        within_radius (float, optional): Defines the distance in blocks the mob has to be from the block for the movement to be finished. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_random_block)
    """

    identifier = "minecraft:behavior.move_to_random_block"

    block_distance: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToVillage(AIGoal):
    """Allows the mob to move into a random location within a village.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 8.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 1.5.
        search_range (int, optional): The distance in blocks to search for villages. If <= 0, find the closest village regardless of distance. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_village)
    """

    identifier = "minecraft:behavior.move_to_village"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    goal_radius: float | None = json_field(default=None, validators=[_number])
    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveToWater(AIGoal):
    """Allows the mob to move back into water when on land.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 10.
        search_height (int, optional): Height in blocks the mob will look for water to move towards. Game default 1.
        search_range (int, optional): The distance in blocks it will look for water to move towards. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_water)
    """

    identifier = "minecraft:behavior.move_to_water"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveTowardsDwellingRestriction(AIGoal):
    """Allows entities with the "minecraft:dweller" component to move toward their village area that the entity should be restricted to.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): This multiplier modifies the entity's speed when moving towards its restriction. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_dwelling_restriction)
    """

    identifier = "minecraft:behavior.move_towards_dwelling_restriction"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveTowardsHomeRestriction(AIGoal):
    """Allows entities with a `minecraft:home` component to move towards their home position. If `restriction_radius` is set, entities will be able to run this behavior only if outside of it.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): This multiplier modifies the entity's speed when moving towards its restriction. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_home_restriction)
    """

    identifier = "minecraft:behavior.move_towards_home_restriction"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveTowardsRestriction(AIGoal):
    """AI goal that drives entities back toward their designated home area when they've wandered too far. Works with components like minecraft:home to define the restriction zone. Used for village-bound mobs, territorial creatures, or any entity that should patrol or return to a specific location.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): This multiplier modifies the entity's speed when moving towards its restriction. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_restriction)
    """

    identifier = "minecraft:behavior.move_towards_restriction"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIMoveTowardsTarget(AIGoal):
    """Allows mob to move towards its current target.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        within_radius (float, optional): Defines the radius in blocks that the mob tries to be from the target. A value of 0 means it tries to occupy the same block as the target. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_target)
    """

    identifier = "minecraft:behavior.move_towards_target"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAINap(AIGoal):
    """Allows mobs to occassionally stop and take a nap under certain conditions.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        can_nap_filters (Filter, optional): Conditions that need to be met for the entity to nap.
        cooldown_max (float, optional): Maximum time in seconds the mob has to wait before using the goal again. Game default 0.
        cooldown_min (float, optional): Minimum time in seconds the mob has to wait before using the goal again. Game default 0.
        mob_detect_dist (float, optional): The block distance in x and z that will be checked for mobs that this mob detects. Game default 6.
        mob_detect_height (float, optional): The block distance in y that will be checked for mobs that this mob detects. Game default 6.
        wake_mob_exceptions (Filter, optional): Filters for mobs that will not wake this entity from napping.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nap)
    """

    identifier = "minecraft:behavior.nap"

    can_nap_filters: Filter | None = json_field(default=None, validators=[_filter])
    cooldown_max: float | None = json_field(default=None, validators=[_number])
    cooldown_min: float | None = json_field(default=None, validators=[_number])
    mob_detect_dist: float | None = json_field(default=None, validators=[_number])
    mob_detect_height: float | None = json_field(default=None, validators=[_number])
    wake_mob_exceptions: Filter | None = json_field(default=None, validators=[_filter])


class EntityAINearestAttackableTarget(EntityTypesAIGoal):
    """Allows an entity to attack the closest target within a given subset of specific target types.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_interval (float | NumberRange, optional): Time range (in seconds) between searching for an attack target, range is in (0, "attack_interval"].
        attack_interval_min (float, optional): Minimum time in seconds between searches for an attack target.
        attack_owner (bool, optional): If true, this entity can attack its owner. Game default false.
        entity_types (list[GoalEntityType], optional): List of entity types that this mob considers valid targets. Add entries with `add_entity_type`.
        must_reach (bool, optional): If true, this entity requires a path to the target. Game default false.
        must_see (bool, optional): Determines if target-validity requires this entity to be in range only, or both in range and in sight. Game default false.
        must_see_forget_duration (float, optional): Time (in seconds) the target must not be seen by this entity to become invalid. Used only if "must_see" is true. Game default 3.
        persist_time (float, optional): Time (in seconds) this entity can continue attacking the target after the target is no longer valid. Game default 0.
        reselect_targets (bool, optional): Allows the attacking entity to update the nearest target, otherwise a target is only reselected after each "scan_interval" or "attack_interval". Game default false.
        scan_interval (int, optional): If "attack_interval" is 0 or isn't declared, then between attacks: scanning for a new target occurs every amount of ticks equal to "scan_interval", minimum value is 1. Game default 10.
        set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Game default false.
        target_acquisition_probability (float, optional): Probability (0-1) that the goal will succeed when a candidate target passes all filters. Game default 1.
        target_invisible_multiplier (float, optional): Multiplied with the target's armor coverage percentage to modify "max_dist" when detecting an invisible target. Game default 0.7.
        target_search_height (float, optional): Maximum vertical target-search distance, if it's greater than the target type's "max_dist". A negative value defaults to "entity_types" greatest "max_dist". Game default -1.
        target_sneak_visibility_multiplier (float, optional): Multiplied with the target type's "max_dist" when trying to detect a sneaking target. Game default 0.8.
        within_radius (float, optional): Maximum distance this entity can be from the target when following it, otherwise the target becomes invalid. This value is only used if the entity doesn't declare "minecraft:follow_range". Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nearest_attackable_target)
    """

    identifier = "minecraft:behavior.nearest_attackable_target"

    attack_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    attack_interval_min: float | None = json_field(default=None, validators=[_positive])
    attack_owner: bool | None = json_field(default=None, validators=[_boolean])
    must_reach: bool | None = json_field(default=None, validators=[_boolean])
    must_see: bool | None = json_field(default=None, validators=[_boolean])
    must_see_forget_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    persist_time: float | None = json_field(default=None, validators=[_number])
    reselect_targets: bool | None = json_field(default=None, validators=[_boolean])
    scan_interval: int | None = json_field(default=None, validators=[_integer])
    set_persistent: bool | None = json_field(default=None, validators=[_boolean])
    target_acquisition_probability: float | None = json_field(
        default=None, validators=[_number]
    )
    target_invisible_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    target_search_height: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=-1)]
    )
    target_sneak_visibility_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAINearestPrioritizedAttackableTarget(EntityTypesAIGoal):
    """Allows the mob to check for and pursue the nearest valid target.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_interval (int, optional): Time in seconds before selecting a target. Game default 0.
        cooldown (float, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Game default 0.
        entity_types (list[GoalEntityType], optional): List of entity types that this mob considers valid targets. Add entries with `add_entity_type`.
        hurt_owner (bool, optional): If true, this mob will also attack mobs that hurt its owner. Game default false.
        must_reach (bool, optional): If true, only entities that this mob can path to can be selected as targets. Game default false.
        must_see (bool, optional): If true, only entities in this mob's viewing range can be selected as targets. Game default false.
        must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Game default 3.
        persist_time (float, optional): Time in seconds for a valid target to stay targeted when it becomes an invalid target. Game default 0.
        reselect_targets (bool, optional): If true, the target will change to the current closest entity whenever a different entity is closer. Game default false.
        scan_interval (int, optional): How many ticks to wait between scanning for a target. Game default 10.
        set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Game default false.
        target_search_height (float, optional): Height in blocks to search for a target mob. -1.0f means the height does not matter. Game default -1.
        within_radius (float, optional): Distance in blocks that the target can be within to launch an attack. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nearest_prioritized_attackable_target)
    """

    identifier = "minecraft:behavior.nearest_prioritized_attackable_target"

    attack_interval: int | None = json_field(default=None, validators=[_integer])
    cooldown: float | None = json_field(default=None, validators=[_number])
    hurt_owner: bool | None = json_field(default=None, validators=[_boolean])
    must_reach: bool | None = json_field(default=None, validators=[_boolean])
    must_see: bool | None = json_field(default=None, validators=[_boolean])
    must_see_forget_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    persist_time: float | None = json_field(default=None, validators=[_number])
    reselect_targets: bool | None = json_field(default=None, validators=[_boolean])
    scan_interval: int | None = json_field(default=None, validators=[_integer])
    set_persistent: bool | None = json_field(default=None, validators=[_boolean])
    target_search_height: float | None = json_field(default=None, validators=[_number])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAIOcelotAttack(AIGoal):
    """Controls specific attack behavior for Ocelots.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time (in seconds) between attacks. Game default 1.
        max_distance (float, optional): Max distance from the target, this entity will use this attack behavior. Game default 15.
        max_sneak_range (float, optional): Max distance from the target, this entity starts sneaking. Game default 15.
        max_sprint_range (float, optional): Max distance from the target, this entity starts sprinting (sprinting takes priority over sneaking). Game default 4.
        reach_multiplier (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Game default 2.
        sneak_speed_multiplier (float, optional): Modifies the attacking entity's movement speed while sneaking. Game default 0.6.
        sprint_speed_multiplier (float, optional): Modifies the attacking entity's movement speed while sprinting. Game default 1.33.
        walk_speed_multiplier (float, optional): Modifies the attacking entity's movement speed when not sneaking or sprinting, but still within attack range. Game default 0.8.
        x_max_rotation (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity's head can rotate while trying to look at the target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelotattack)
    """

    identifier = "minecraft:behavior.ocelotattack"

    cooldown_time: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_distance: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_sneak_range: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_sprint_range: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    reach_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    sneak_speed_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    sprint_speed_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    walk_speed_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    x_max_rotation: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    y_max_head_rotation: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )


class EntityAIOcelotSitOnBlock(AIGoal):
    """Allows to mob to be able to sit in place like the ocelot.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelot_sit_on_block)
    """

    identifier = "minecraft:behavior.ocelot_sit_on_block"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIOfferFlower(AIGoal):
    """Allows the mob to offer a flower to another mob with the minecraft:take_flower behavior.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        chance_to_start (float, optional): Percent chance that the mob will start this goal from 0.0 to 1.0 (where 1.0 = 100%). Game default 0.0001.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.
        max_head_rotation_y (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Game default 30.
        max_offer_flower_duration (float, optional): The max amount of time (in seconds) that the mob will offer the flower for before exiting the Goal. Game default 20.
        max_rotation_x (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Game default 30.
        search_area (Vector3D, optional): The dimensions of the AABB used to search for a potential mob to offer flower to.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_offer_flower)
    """

    identifier = "minecraft:behavior.offer_flower"

    chance_to_start: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    filters: Filter | None = json_field(default=None, validators=[_filter])
    max_head_rotation_y: float | None = json_field(default=None, validators=[_number])
    max_offer_flower_duration: float | None = json_field(
        default=None, validators=[_number]
    )
    max_rotation_x: float | None = json_field(default=None, validators=[_number])
    search_area: Vector3D | None = json_field(default=None, validators=[vector3])


class EntityAIOpenDoor(AIGoal):
    """Allows the mob to open doors. Requires the mob to be able to path through doors, otherwise the mob won't even want to try opening them.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        close_door_after (bool, optional): If true, the mob will close the door after opening it and going through it. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_open_door)
    """

    identifier = "minecraft:behavior.open_door"

    close_door_after: bool | None = json_field(default=None, validators=[_boolean])


class EntityAIOwnerHurtByTarget(EntityTypesAIGoal):
    """Allows the mob to target another mob that hurts their owner.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        entity_types (list[GoalEntityType], optional): List of entity types that this mob can target if they hurt their owner. Add entries with `add_entity_type`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_by_target)
    """

    identifier = "minecraft:behavior.owner_hurt_by_target"


class EntityAIOwnerHurtTarget(EntityTypesAIGoal):
    """Allows the mob to target a mob that is hurt by their owner.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        entity_types (list[GoalEntityType], optional): List of entity types that this entity can target if the potential target is hurt by this mob's owner. Add entries with `add_entity_type`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_target)
    """

    identifier = "minecraft:behavior.owner_hurt_target"


class EntityAIPanic(AIGoal):
    """Allows a mob to panic when receiving damage, making it run around and away from the damage source that made it enter this state.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        damage_sources (list[DamageCause], optional): The list of damage sources that will cause this mob to panic.
        force (bool, optional): If true, the mob will stop panicking only when it can no longer find positions to run away to, or when the goal is removed. Game default false.
        ignore_mob_damage (bool, optional): If true, the mob will not panic in response to damage from other mobs. This overrides the damage types in "damage_sources". Game default false.
        panic_sound (str, optional): Sound to play while the mob is panicking.
        prefer_water (bool, optional): If true, the mob will prefer water over land. Game default false.
        sound_interval (float | NumberRange, optional): Range of random ticks to wait between playing the panic sound.
        speed_multiplier (float, optional): Movement speed multiplier when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_panic)
    """

    identifier = "minecraft:behavior.panic"

    damage_sources: list[DamageCause] | None = json_field(
        default=None, validators=[each(_damage_cause)]
    )
    force: bool | None = json_field(default=None, validators=[_boolean])
    ignore_mob_damage: bool | None = json_field(default=None, validators=[_boolean])
    panic_sound: str | None = json_field(default=None, validators=[_string])
    prefer_water: bool | None = json_field(default=None, validators=[_boolean])
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIPetSleepWithOwner(AIGoal):
    """Allows the pet mob to move onto a bed with its owner while sleeping.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        search_height (int, optional): Height in blocks from the owner the pet can be to sleep with owner. Game default 1.
        search_range (int, optional): The distance in blocks from the owner the pet can be to sleep with owner. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_pet_sleep_with_owner)
    """

    identifier = "minecraft:behavior.pet_sleep_with_owner"

    goal_radius: float | None = json_field(default=None, validators=[_number])
    search_height: int | None = json_field(default=None, validators=[_integer])
    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIPickupItems(AIGoal):
    """Allows the mob to pick up items on the ground.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        can_pickup_any_item (bool, optional): If true, the mob can pick up any item. Game default false.
        can_pickup_to_hand_or_equipment (bool, optional): If true, the mob can pick up items to its hand or armor slots. Game default true.
        cooldown_after_being_attacked (int, optional): Time in seconds the mob cannot pickup items after being attacked. Game default 0.
        excluded_items (list[ItemReference], optional): List of items this mob will not pick up.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        max_dist (int, optional): Maximum distance this mob will look for items to pick up. Game default 1.
        on_pickup_item_end (EventTrigger | str, optional): Event to run when this mob either finishes or loses interest in picking up an item.
        on_pickup_item_start (EventTrigger | str, optional): Event to run when this mob moves to pick up an item.
        pickup_based_on_chance (bool, optional): If true, depending on the difficulty, there is a random chance that the mob may not be able to pickup items. Game default false.
        pickup_same_items_as_in_hand (bool, optional): If true, the mob will only pick up items that match what it is already holding. Game default false.
        search_height (int, optional): Height in blocks the mob will search for items. Game default 1.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        stop_if_holding_item (bool, optional): If true, the mob will not begin a pickup goal while it is already holding an item. Useful for mobs that should only hold one item at a time. Game default false.
        track_target (bool, optional): If true, this mob will chase after the target as long as it's a valid target. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_pickup_items)
    """

    identifier = "minecraft:behavior.pickup_items"

    can_pickup_any_item: bool | None = json_field(default=None, validators=[_boolean])
    can_pickup_to_hand_or_equipment: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    cooldown_after_being_attacked: int | None = json_field(
        default=None, validators=[_integer]
    )
    excluded_items: list[ItemReference] | None = json_field(
        default=None, validators=[_items]
    )
    goal_radius: float | None = json_field(default=None, validators=[_number])
    max_dist: int | None = json_field(default=None, validators=[_integer])
    on_pickup_item_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_pickup_item_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    pickup_based_on_chance: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    pickup_same_items_as_in_hand: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    search_height: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    stop_if_holding_item: bool | None = json_field(default=None, validators=[_boolean])
    track_target: bool | None = json_field(default=None, validators=[_boolean])


class EntityAIPlaceBlock(AIGoal):
    """

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        affected_by_griefing_rule (bool, optional): If true, whether the goal is affected by the mob griefing game rule. Game default true.
        can_place (Filter, optional): Filters for if the entity should try to place its block. Self and Target are set.
        chance (float, optional): Chance each tick for the entity to try and place a block. Game default 1.
        on_place (EventTrigger | str, optional): Trigger ran if the entity does place its block. Self, Target, and Block are set.
        placeable_carried_blocks (list[BlockReference], optional): Block descriptors for which blocks are valid to be placed from the entity's carried item, if empty all blocks are valid.
        randomly_placeable_blocks (list[PlaceableBlock], optional): Weighted block descriptors for which blocks should be randomly placed, if empty the entity will try to place its carried block from placeable_carried_blocks. Add more with `add_randomly_placeable_block`.
        xz_range (tuple[int, int], optional): XZ range from which the entity will try and place blocks in.
        y_range (tuple[int, int], optional): Y range from which the entity will try and place blocks in.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_place_block)
    """

    identifier = "minecraft:behavior.place_block"

    affected_by_griefing_rule: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    can_place: Filter | None = json_field(default=None, validators=[_filter])
    chance: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    on_place: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    placeable_carried_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks], encoder=encoders.block_objects
    )
    randomly_placeable_blocks: list[PlaceableBlock] = json_field(
        default_factory=list,
        validators=[each(instance_of(PlaceableBlock))],
        omit_default=True,
    )
    xz_range: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )
    y_range: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )

    def add_randomly_placeable_block(
        self,
        *,
        block: BlockReference,
        filter: Filter | None = None,
        weight: int | None = None,
    ) -> "EntityAIPlaceBlock":
        """Adds a block to place at random. See `PlaceableBlock` for the parameters."""
        self.randomly_placeable_blocks.append(
            PlaceableBlock(block=block, filter=filter, weight=weight)
        )
        return self


class EntityAIPlay(AIGoal):
    """Allows the mob to offer a flower to another mob with the minecraft:take_flower behavior.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        chance_to_start (float, optional): Percent chance that the mob will start this goal, from 0 to 1. Game default 0.0025.
        follow_distance (int, optional): The distance (in blocks) that the mob tries to be in range of the friend it's following. Game default 2.
        friend_search_area (Vector3D, optional): The dimensions of the AABB used to search for a potential friend to play with.
        friend_types (list[GoalEntityType], optional): The entity type(s) to consider when searching for a potential friend to play with. Add more with `add_friend_type`.
        max_play_duration_seconds (float, optional): The max amount of seconds that the mob will play for before exiting the Goal. Game default 50.
        random_pos_search_height (int, optional): The height (in blocks) that the mob will search within to find a random position position to move to. Must be at least 1. Game default 3.
        random_pos_search_range (int, optional): The distance (in blocks) on ground that the mob will search within to find a random position to move to. Must be at least 1. Game default 16.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_play)
    """

    identifier = "minecraft:behavior.play"

    chance_to_start: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    follow_distance: int | None = json_field(default=None, validators=[_integer])
    friend_search_area: Vector3D | None = json_field(default=None, validators=[vector3])
    friend_types: list[GoalEntityType] = json_field(
        default_factory=list,
        validators=[each(instance_of(GoalEntityType))],
        omit_default=True,
    )
    max_play_duration_seconds: float | None = json_field(
        default=None, validators=[_number]
    )
    random_pos_search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    random_pos_search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])

    def add_friend_type(
        self,
        *,
        filters: Filter | None = None,
        check_if_outnumbered: bool | None = None,
        cooldown: float | None = None,
        max_dist: float | None = None,
        max_flee: float | None = None,
        max_height: float | None = None,
        must_see: bool | None = None,
        must_see_forget_duration: float | None = None,
        priority: int | None = None,
        reevaluate_description: bool | None = None,
        sprint_speed_multiplier: float | None = None,
        walk_speed_multiplier: float | None = None,
    ) -> "EntityAIPlay":
        """Adds an entity type to play with. See `GoalEntityType` for the parameters."""
        self.friend_types.append(
            GoalEntityType(
                filters=filters,
                check_if_outnumbered=check_if_outnumbered,
                cooldown=cooldown,
                max_dist=max_dist,
                max_flee=max_flee,
                max_height=max_height,
                must_see=must_see,
                must_see_forget_duration=must_see_forget_duration,
                priority=priority,
                reevaluate_description=reevaluate_description,
                sprint_speed_multiplier=sprint_speed_multiplier,
                walk_speed_multiplier=walk_speed_multiplier,
            )
        )
        return self


class EntityAIPlayDead(AIGoal):
    """Allows this entity to pretend to be dead to avoid being targeted by attackers.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        apply_regeneration (bool, optional): Whether the mob will receive the regeneration effect while playing dead. Game default false.
        damage_sources (list[DamageCause], optional): The list of Entity Damage Sources that will cause this mob to play dead.
        duration (float, optional): The amount of time the mob will remain playing dead (in seconds). Game default 1.
        filters (Filter, optional): The list of other triggers that are required for the mob to activate play dead.
        force_below_health (int, optional): The amount of health at which damage will cause the mob to play dead. Game default 0.
        random_damage_range (tuple[int, int], optional): The range of damage that may cause the goal to start depending on randomness.
        random_start_chance (float, optional): The likelihood of this goal starting upon taking damage. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_play_dead)
    """

    identifier = "minecraft:behavior.play_dead"

    apply_regeneration: bool | None = json_field(default=None, validators=[_boolean])
    damage_sources: list[DamageCause] | None = json_field(
        default=None, validators=[each(_damage_cause)]
    )
    duration: float | None = json_field(default=None, validators=[_number])
    filters: Filter | None = json_field(default=None, validators=[_filter])
    force_below_health: int | None = json_field(default=None, validators=[_integer])
    random_damage_range: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )
    random_start_chance: float | None = json_field(default=None, validators=[_number])


class EntityAIPlayerRideTamed(AIGoal):
    """Allows the mob to be ridden by the player after being tamed.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_player.ride_tamed)
    """

    identifier = "minecraft:behavior.player_ride_tamed"


class EntityAIRaidGarden(AIGoal):
    """Allows the mob to eat/raid crops out of farms until they are full.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        blocks (list[BlockReference], optional): Blocks that the mob is looking for to eat/raid.
        eat_delay (int, optional): Time in seconds between each time it eats/raids. Game default 2.
        full_delay (int, optional): Amount of time in seconds before this mob wants to eat/raid again after eating its maximum. Game default 100.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        initial_eat_delay (int, optional): Time in seconds before starting to eat/raid once it arrives at it. Game default 0.
        max_to_eat (int, optional): Maximum number of crops this entity wants to eat/raid. If set to zero or less then it doesn't have a maximum. Game default 6.
        search_height (int, optional): Height in blocks the mob will look for crops to eat. Game default 1.
        search_range (int, optional): Distance in blocks the mob will look for crops to eat. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_raid_garden)
    """

    identifier = "minecraft:behavior.raid_garden"

    blocks: list[BlockReference] | None = json_field(default=None, validators=[_blocks])
    eat_delay: int | None = json_field(default=None, validators=[_integer])
    full_delay: int | None = json_field(default=None, validators=[_integer])
    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    initial_eat_delay: int | None = json_field(default=None, validators=[_integer])
    max_to_eat: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIRamAttack(AIGoal):
    """Allows this entity to damage a target by using a running attack.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        baby_knockback_modifier (float, optional): The modifier to knockback that babies have. Game default 0.3333.
        cooldown_range (float | NumberRange, optional): Minimum and maximum cooldown time-range (positive, in seconds) between each attempted ram attack.
        knockback_force (float, optional): The force of the knockback of the ram attack. Game default 5.
        knockback_height (float, optional): The height of the knockback of the ram attack. Game default 0.1.
        min_ram_distance (int, optional): The minimum distance at which the mob can start a ram attack. Game default 4.
        on_start (EventTrigger | str, optional): The event to trigger when attacking.
        pre_ram_sound (str, optional): The sound to play when an entity is about to perform a ram attack.
        ram_distance (int, optional): The distance at which the mob start to run with ram speed. Game default 7.
        ram_impact_sound (str, optional): The sound to play when an entity is impacting on a ram attack.
        ram_speed (float, optional): Sets the entity's speed when charging toward the target. Game default 2.
        run_speed (float, optional): Sets the entity's speed when running toward the target. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ram_attack)
    """

    identifier = "minecraft:behavior.ram_attack"

    baby_knockback_modifier: float | None = json_field(
        default=None, validators=[_number]
    )
    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    knockback_force: float | None = json_field(default=None, validators=[_number])
    knockback_height: float | None = json_field(default=None, validators=[_number])
    min_ram_distance: int | None = json_field(default=None, validators=[_integer])
    on_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    pre_ram_sound: str | None = json_field(default=None, validators=[_string])
    ram_distance: int | None = json_field(default=None, validators=[_integer])
    ram_impact_sound: str | None = json_field(default=None, validators=[_string])
    ram_speed: float | None = json_field(default=None, validators=[_number])
    run_speed: float | None = json_field(default=None, validators=[_number])


class EntityAIRandomBreach(AIGoal):
    """Allows the mob to randomly break surface of the water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.
        interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Game default 120.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Game default 10.
        y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Game default 7.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_breach)
    """

    identifier = "minecraft:behavior.random_breach"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    interval: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    xz_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )


class EntityAIRandomFly(AIGoal):
    """Allows a mob to randomly fly around.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        avoid_damage_blocks (bool, optional): If true, the mob will avoid blocks that cause damage when flying.
        can_land_on_trees (bool, optional): If true, the mob can stop flying and land on a tree instead of the ground. Game default true.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Game default 10.
        y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Game default 7.
        y_offset (float, optional):

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_fly)
    """

    identifier = "minecraft:behavior.random_fly"

    avoid_damage_blocks: bool | None = json_field(default=None, validators=[_boolean])
    can_land_on_trees: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    xz_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_offset: float | None = json_field(default=None, validators=[_number])


class EntityAIRandomHover(AIGoal):
    """Allows the mob to hover around randomly, close to the surface.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        hover_height (tuple[int, int], optional): The height above the surface which the mob will try to maintain.
        interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Game default 120.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Game default 10.
        y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Game default 7.
        y_offset (float, optional): Height in blocks to add to the selected target position. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_hover)
    """

    identifier = "minecraft:behavior.random_hover"

    hover_height: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )
    interval: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    xz_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_offset: float | None = json_field(default=None, validators=[_number])


class EntityAIRandomLookAround(AIGoal):
    """Allows the mob to randomly look around.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        look_time (tuple[int, int], optional): The range of time in seconds the mob will stay looking in a random direction before looking elsewhere.
        max_angle_of_view_horizontal (float, optional): The rightmost angle a mob can look at on the horizontal plane with respect to its initial facing direction. Game default 180.
        min_angle_of_view_horizontal (float, optional): The leftmost angle a mob can look at on the horizontal plane with respect to its initial facing direction. Game default -180.
        probability (float, optional): The probability of randomly looking around. Game default 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_look_around)
    """

    identifier = "minecraft:behavior.random_look_around"

    look_time: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )
    max_angle_of_view_horizontal: float | None = json_field(
        default=None, validators=[_number]
    )
    min_angle_of_view_horizontal: float | None = json_field(
        default=None, validators=[_number]
    )
    probability: float | None = json_field(default=None, validators=[_number])


class EntityAIRandomLookAroundAndSit(AIGoal):
    """Allows the mob to randomly sit and look around for a duration. Note: Must have a sitting animation set up to use this.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        continue_if_leashed (bool, optional): If the goal should continue to be used as long as the mob is leashed. Game default false.
        continue_sitting_on_reload (bool, optional): The mob will stay sitting on reload. Game default false.
        max_angle_of_view_horizontal (float, optional): The rightmost angle a mob can look at on the horizontal plane with respect to its initial facing direction. Game default 180.
        max_look_count (int, optional): The max amount of unique looks a mob will have while looking around. Game default 2.
        max_look_time (int, optional): The max amount of time (in ticks) a mob will stay looking at a direction while looking around. Game default 40.
        min_angle_of_view_horizontal (float, optional): The leftmost angle a mob can look at on the horizontal plane with respect to its initial facing direction. Game default -180.
        min_look_count (int, optional): The min amount of unique looks a mob will have while looking around. Game default 1.
        min_look_time (int, optional): The min amount of time (in ticks) a mob will stay looking at a direction while looking around. Game default 20.
        probability (float, optional): The probability of randomly looking around. Game default 0.02.
        random_look_around_cooldown (int, optional): The cooldown in seconds before the goal can be used again. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_look_around_and_sit)
    """

    identifier = "minecraft:behavior.random_look_around_and_sit"

    continue_if_leashed: bool | None = json_field(default=None, validators=[_boolean])
    continue_sitting_on_reload: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    max_angle_of_view_horizontal: float | None = json_field(
        default=None, validators=[_number]
    )
    max_look_count: int | None = json_field(default=None, validators=[_integer])
    max_look_time: int | None = json_field(default=None, validators=[_integer])
    min_angle_of_view_horizontal: float | None = json_field(
        default=None, validators=[_number]
    )
    min_look_count: int | None = json_field(default=None, validators=[_integer])
    min_look_time: int | None = json_field(default=None, validators=[_integer])
    probability: float | None = json_field(default=None, validators=[_number])
    random_look_around_cooldown: int | None = json_field(
        default=None, validators=[_integer]
    )


class EntityAIRandomSearchAndDig(AIGoal):
    """Allows this entity to locate a random target block that it can path find to. Once found, the entity will move towards it and dig up an item. [Default target block types: Dirt, Grass, Podzol, DirtWithRoots, MossBlock, Mud, MuddyMangroveRoots].

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_range (float | NumberRange, optional): Goal cooldown range in seconds.
        digging_duration_range (float | NumberRange, optional): Digging duration in seconds.
        find_valid_position_retries (int, optional): Amount of retries to find a valid target position within search range. Game default 5.
        goal_radius (float, optional): Distance in blocks within the entity to considers it has reached it's target position. Game default 1.5.
        item_table (LootTable | str, optional): File path relative to the resource pack root for items to spawn list (loot table format).
        on_digging_start (EventTrigger | str, optional): Event to run when the goal ends searching has begins digging.
        on_fail_during_digging (EventTrigger | str, optional): Event to run when the goal failed while in digging state.
        on_fail_during_searching (EventTrigger | str, optional): Event to run when the goal failed while in searching state.
        on_item_found (EventTrigger | str, optional): Event to run when the goal find a item.
        on_searching_start (EventTrigger | str, optional): Event to run when the goal starts searching.
        on_success (EventTrigger | str, optional): Event to run when searching and digging has ended.
        search_range_xz (int, optional): Width and length of the volume around the entity used to find a valid target position. Game default 10.
        search_range_y (int, optional): Height of the volume around the entity used to find a valid target position. Game default 7.
        spawn_item_after_seconds (float, optional): Digging duration before spawning item in seconds. Game default 0.
        spawn_item_pos_offset (float, optional): Distance to offset the item's spawn location in the direction the mob is facing. Game default 0.
        speed_multiplier (float, optional): Searching movement speed multiplier. Game default 1.
        target_blocks (list[BlockReference], optional): List of target block types the goal will look to dig on. Overrides the default list.
        target_dig_position_offset (float, optional): Dig target position offset from the feet position of the mob in their facing direction. Game default 2.25.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_search_and_dig)
    """

    identifier = "minecraft:behavior.random_search_and_dig"

    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    digging_duration_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    find_valid_position_retries: int | None = json_field(
        default=None, validators=[_integer]
    )
    goal_radius: float | None = json_field(default=None, validators=[_number])
    item_table: LootTable | str | None = json_field(
        default=None, validators=[instance_of(LootTable, str)]
    )
    on_digging_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_fail_during_digging: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_fail_during_searching: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_item_found: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_searching_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_success: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    search_range_xz: int | None = json_field(default=None, validators=[_integer])
    search_range_y: int | None = json_field(default=None, validators=[_integer])
    spawn_item_after_seconds: float | None = json_field(
        default=None, validators=[_number]
    )
    spawn_item_pos_offset: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    target_blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks], encoder=encoders.block_objects
    )
    target_dig_position_offset: float | None = json_field(
        default=None, validators=[_number]
    )


class EntityAIRandomSitting(AIGoal):
    """Allows the mob to randomly sit for a duration.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 100.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.
        min_sit_time (float, optional): The minimum amount of time in seconds before the mob will stand back up. Game default 10.
        start_chance (float, optional): This is the chance that the mob will start this goal, from 0 to 1. Game default 0.1.
        stop_chance (float, optional): This is the chance that the mob will stop this goal, from 0 to 1. Game default 0.3.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_sitting)
    """

    identifier = "minecraft:behavior.random_sitting"

    cooldown: float | None = json_field(default=None, validators=[_number])
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    min_sit_time: float | None = json_field(default=None, validators=[_number])
    start_chance: float | None = json_field(default=None, validators=[_number])
    stop_chance: float | None = json_field(default=None, validators=[_number])


class EntityAIRandomStroll(AIGoal):
    """Allows a mob to randomly stroll around.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Game default 120.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Game default 10.
        y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Game default 7.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_stroll)
    """

    identifier = "minecraft:behavior.random_stroll"

    interval: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    xz_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )


class EntityAIRandomSwim(AIGoal):
    """Allows an entity to randomly move through water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        avoid_surface (bool, optional): If true, the mob will avoid surface water blocks by swimming below them. Game default true.
        interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Game default 120.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Game default 10.
        y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Game default 7.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_swim)
    """

    identifier = "minecraft:behavior.random_swim"

    avoid_surface: bool | None = json_field(default=None, validators=[_boolean])
    interval: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    xz_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )
    y_dist: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1)]
    )


class EntityAIRangedAttack(AIGoal):
    """Allows an entity to attack by using ranged shots. "charge_shoot_trigger" must be greater than 0 to enable charged up burst-shot attacks. Requires minecraft:shooter to define projectile behaviour.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_interval (float | NumberRange, optional): Reload-time range (in seconds), when not using a charged shot.
        attack_interval_max (float, optional): Maximum bound for reload-time range (in seconds), when not using a charged shot. Reload-time range scales with target-distance. Game default 0.
        attack_interval_min (float, optional): Minimum bound for reload-time range (in seconds), when not using a charged shot. Reload-time range scales with target-distance. Game default 0.
        attack_range (float | NumberRange, optional): Range of distances from the target within which the entity can perform a ranged attack. Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected.
        burst_interval (float, optional): Time (in seconds) between each individual shot when firing a burst of shots from a charged up attack. Game default 0.
        burst_shots (int, optional): Number of shots fired every time the attacking entity uses a charged up attack. Game default 1.
        charge_charged_trigger (float, optional): Time (in seconds, then add "charge_shoot_trigger"), before a charged up attack is done charging. Charge-time decays while target is not in sight. Game default 0.
        charge_shoot_trigger (float, optional): Amount of time (in seconds, then doubled) a charged shot must be charging before reloading burst shots. Charge-time decays while target is not in sight. Game default 0.
        in_range_movement_mode (Literal["follow_target", "hold_position"], optional): Controls how the entity moves while its target is within the configured attack range. Game default hold_position.
        ranged_fov (float, optional): Field of view (in degrees) when using sensing to detect a target for attack. Game default 90.
        set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Game default false.
        speed_multiplier (float, optional): During attack behavior, this multiplier modifies the entity's speed when moving toward the target. Game default 1.
        swing (bool, optional): If a swing animation (using variable.attack_time) exists, this causes the actor to swing their arm(s) upon firing the ranged attack. Game default false.
        target_in_sight_time (float, optional): Minimum amount of time (in seconds) the attacking entity needs to see the target before moving toward it. Game default 1.
        x_max_rotation (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ranged_attack)
    """

    identifier = "minecraft:behavior.ranged_attack"

    attack_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    attack_interval_max: float | None = json_field(default=None, validators=[_number])
    attack_interval_min: float | None = json_field(default=None, validators=[_number])
    attack_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    burst_interval: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    burst_shots: int | None = json_field(default=None, validators=[_integer])
    charge_charged_trigger: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    charge_shoot_trigger: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    in_range_movement_mode: Literal["follow_target", "hold_position"] | None = (
        json_field(default=None, validators=[one_of("follow_target", "hold_position")])
    )
    ranged_fov: float | None = json_field(default=None, validators=[_number])
    set_persistent: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    swing: bool | None = json_field(default=None, validators=[_boolean])
    target_in_sight_time: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_head_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAIReceiveLove(AIGoal):
    """Allows the villager to stop so another villager can breed with it. Can only be used by a Villager.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_receive_love)
    """

    identifier = "minecraft:behavior.receive_love"


class EntityAIRestrictOpenDoor(AIGoal):
    """Allows the mob to stay indoors during night time.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_restrict_open_door)
    """

    identifier = "minecraft:behavior.restrict_open_door"


class EntityAIRestrictSun(AIGoal):
    """Allows the mob to automatically start avoiding the sun when its a clear day out.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_restrict_sun)
    """

    identifier = "minecraft:behavior.restrict_sun"


class EntityAIRiseToLiquidLevel(AIGoal):
    """Allows the mob to stay at a certain level when in liquid.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        liquid_y_offset (float, optional): Target distance down from the liquid surface. i.e. Positive values move the target Y down. Game default 0.
        rise_delta (float, optional): Movement up in Y per tick when below the liquid surface. Game default 0.
        sink_delta (float, optional): Movement down in Y per tick when above the liquid surface. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_rise_to_liquid_level)
    """

    identifier = "minecraft:behavior.rise_to_liquid_level"

    liquid_y_offset: float | None = json_field(default=0, validators=[_number])
    rise_delta: float | None = json_field(default=0, validators=[_number])
    sink_delta: float | None = json_field(default=0, validators=[_number])


class EntityAIRoar(AIGoal):
    """Allows this entity to roar at another entity based on data in `minecraft:anger_level`. Once the anger threshold specified in `minecraft:anger_level` has been reached, this entity will roar for the specified amount of time, look at the other entity, apply anger boost towards it, and finally target it.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        duration (float, optional): The amount of time to roar for. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roar)
    """

    identifier = "minecraft:behavior.roar"

    duration: float | None = json_field(default=None, validators=[_number])


class EntityAIRoll(AIGoal):
    """This allows the mob to roll forward.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        probability (float, optional): The probability that the mob will use the goal. Game default 0.02.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roll)
    """

    identifier = "minecraft:behavior.roll"

    probability: float | None = json_field(default=None, validators=[_number])


class EntityAIRunAroundLikeCrazy(AIGoal):
    """Allows the mob to run around aimlessly.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_run_around_like_crazy)
    """

    identifier = "minecraft:behavior.run_around_like_crazy"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIScared(AIGoal):
    """Allows the mob to become scared when the weather outside is thundering.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        sound_delay (int, optional): The interval in which a sound will play when active in a 1/delay chance to kick off. Game default 0.
        sound_interval (int, optional): The interval in which a sound will play when active in a 1/delay chance to kick off. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_scared)
    """

    identifier = "minecraft:behavior.scared"

    sound_delay: int | None = json_field(default=None, validators=[_integer])
    sound_interval: int | None = json_field(default=None, validators=[_integer])


class EntityAISendEvent(AIGoal):
    """Allows the mob to send an event to another mob.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cast_duration (float, optional): Time in seconds for the entire event sending process.
        event_choices (list[SendEventChoice], optional): List of possible events to send with conditions, weights, and targeting parameters. Add more with `add_event_choice`.
        look_at_target (bool, optional): If true, the mob will face the entity it sends an event to. Game default true.
        sequence (list[SendEventStep], optional): Events to send, in order. Add more with `add_step`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_send_event)
    """

    identifier = "minecraft:behavior.send_event"

    cast_duration: float | None = json_field(default=None, validators=[_number])
    event_choices: list[SendEventChoice] = json_field(
        default_factory=list,
        validators=[each(instance_of(SendEventChoice))],
        omit_default=True,
    )
    look_at_target: bool | None = json_field(default=None, validators=[_boolean])
    sequence: list[SendEventStep] = json_field(
        default_factory=list,
        validators=[each(instance_of(SendEventStep))],
        omit_default=True,
    )

    def add_event_choice(
        self,
        *,
        cast_duration: float | None = None,
        cooldown_time: float | None = None,
        do_casting: bool | None = None,
        filters: Filter | None = None,
        look_at_target: bool | None = None,
        max_activation_range: float | None = None,
        min_activation_range: float | None = None,
        particle_color: str | RGBA255 | None = None,
        sequence: list[SendEventStep] | None = None,
        start_sound_event: str | None = None,
        weight: float | None = None,
    ) -> "EntityAISendEvent":
        """Adds an event choice. See `SendEventChoice` for the parameters."""
        self.event_choices.append(
            SendEventChoice(
                cast_duration=cast_duration,
                cooldown_time=cooldown_time,
                do_casting=do_casting,
                filters=filters,
                look_at_target=look_at_target,
                max_activation_range=max_activation_range,
                min_activation_range=min_activation_range,
                particle_color=particle_color,
                sequence=list(sequence or []),
                start_sound_event=start_sound_event,
                weight=weight,
            )
        )
        return self

    def add_step(
        self,
        *,
        event: str,
        base_delay: float | None = None,
        sound_event: str | None = None,
    ) -> "EntityAISendEvent":
        """Adds a step to the top-level `sequence`. See `SendEventStep` for the parameters."""
        self.sequence.append(
            SendEventStep(event=event, base_delay=base_delay, sound_event=sound_event)
        )
        return self


class EntityAIShareItems(EntityTypesAIGoal):
    """Allows the mob to give items it has to others.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        entity_types (list[GoalEntityType], optional): List of entities this mob will share items with. Add entries with `add_entity_type`.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        max_dist (int, optional): Maximum distance in blocks this mob will look for entities to share items with. Game default 1.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_share_items)
    """

    identifier = "minecraft:behavior.share_items"

    goal_radius: float | None = json_field(default=None, validators=[_number])
    max_dist: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAISilverfishMergeWithStone(AIGoal):
    """Allows the mob to go into stone blocks like Silverfish do.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_silverfish_merge_with_stone)
    """

    identifier = "minecraft:behavior.silverfish_merge_with_stone"


class EntityAISilverfishWakeUpFriends(AIGoal):
    """Allows the mob to alert mobs in nearby blocks to come out.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_silverfish_wake_up_friends)
    """

    identifier = "minecraft:behavior.silverfish_wake_up_friends"


class EntityAISkeletonHorseTrap(AIGoal):
    """Allows Equine mobs to be Horse Traps and be triggered like them, spawning a lightning bolt and a bunch of horses when a player is nearby. Can only be used by Horses, Mules, Donkeys and Skeleton Horses.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        duration (float, optional): Amount of time in seconds the trap exists. After this amount of time is elapsed, the trap is removed from the world if it hasn't been activated. Game default 1.
        within_radius (float, optional): Distance in blocks that the player has to be within to trigger the horse trap. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_skeleton_horse.trap)
    """

    identifier = "minecraft:behavior.skeleton_horse_trap"

    duration: float | None = json_field(default=None, validators=[_number])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAISleep(AIGoal):
    """Allows mobs that own a bed to in a village to move to and sleep in it.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        can_sleep_while_riding (bool, optional): If true, the mob will be able to use the sleep goal if riding something. Game default false.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.
        sleep_collider_height (float, optional): The height of the mob's collider while sleeping. Game default 1.
        sleep_collider_width (float, optional): The width of the mob's collider while sleeping. Game default 1.
        sleep_y_offset (float, optional): The y offset of the mob's collider while sleeping. Game default 1.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.
        timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after a internal failure or timeout condition. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sleep)
    """

    identifier = "minecraft:behavior.sleep"

    can_sleep_while_riding: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    sleep_collider_height: float | None = json_field(default=None, validators=[_number])
    sleep_collider_width: float | None = json_field(default=None, validators=[_number])
    sleep_y_offset: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    timeout_cooldown: float | None = json_field(default=None, validators=[_number])


class EntityAISlimeAttack(AIGoal):
    """Causes the entity to grow tired every once in a while, while attacking.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        grow_tired_cooldown_time (float, optional):  Game default 15.
        set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Game default false.
        speed_multiplier (float, optional): During attack behavior, this multiplier modifies the entity's speed when moving toward the target. Game default 1.
        x_max_rotation (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Game default 10.
        y_max_rotation (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate while trying to look at the target. Game default 10.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_attack)
    """

    identifier = "minecraft:behavior.slime_attack"

    grow_tired_cooldown_time: float | None = json_field(
        default=None, validators=[_number]
    )
    set_persistent: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAISlimeFloat(AIGoal):
    """Allow slimes to float in water / lava.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        jump_chance_percentage (float, optional): Percent chance a slime or magma cube has to jump while in water / lava. Game default 0.8.
        speed_multiplier (float, optional): Determines the multiplier the entity's speed is modified by when moving through water / lava. Game default 1.2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_float)
    """

    identifier = "minecraft:behavior.slime_float"

    jump_chance_percentage: float | None = json_field(
        default=None, validators=[_number]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAISlimeKeepOnJumping(AIGoal):
    """Allows the entity to continuously jump around like a slime.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        speed_multiplier (float, optional): Determines the multiplier this entity's speed is modified by when jumping around. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_keep_on_jumping)
    """

    identifier = "minecraft:behavior.slime_keep_on_jumping"

    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAISlimeRandomDirection(AIGoal):
    """Allows the entity to move in random directions like a slime.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        add_random_time_range (int, optional): Additional time (in whole seconds), chosen randomly in the range of [0, "add_random_time_range"], to add to "min_change_direction_time". Game default 3.
        min_change_direction_time (float, optional): Constant minimum time (in seconds) to wait before choosing a new direction. Game default 2.
        turn_range (int, optional): Maximum rotation angle range (in degrees) when randomly choosing a new direction. Game default 360.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_random_direction)
    """

    identifier = "minecraft:behavior.slime_random_direction"

    add_random_time_range: int | None = json_field(default=None, validators=[_integer])
    min_change_direction_time: float | None = json_field(
        default=None, validators=[_number]
    )
    turn_range: int | None = json_field(default=None, validators=[_integer])


class EntityAISnacking(AIGoal):
    """Allows the mob to take a load off and snack on food that it found nearby.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        items (list[ItemReference], optional): Items that we are interested in snacking on.
        snacking_cooldown (float, optional): The cooldown time in seconds before the mob is able to snack again. Game default 7.5.
        snacking_cooldown_min (float, optional): The minimum time in seconds before the mob is able to snack again. Game default 0.5.
        snacking_stop_chance (float, optional): This is the chance that the mob will stop snacking, from 0 to 1. Game default 0.0017.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_snacking)
    """

    identifier = "minecraft:behavior.snacking"

    items: list[ItemReference] | None = json_field(default=None, validators=[_items])
    snacking_cooldown: float | None = json_field(default=None, validators=[_number])
    snacking_cooldown_min: float | None = json_field(default=None, validators=[_number])
    snacking_stop_chance: float | None = json_field(default=None, validators=[_number])


class EntityAISneeze(EntityTypesAIGoal):
    """Allows the mob to sneeze, causing it to drop items and affect nearby mobs.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 0.
        drop_item_chance (float, optional): The probability that the mob will drop an item when it sneezes. Game default 1.
        entity_types (list[GoalEntityType], optional): List of entity types this mob will startle (cause to jump) when it sneezes. Add entries with `add_entity_type`.
        loot_table (LootTable | str, optional): Loot table to select dropped items from.
        prepare_sound (str, optional): Sound to play when the sneeze is about to happen.
        prepare_time (float, optional): The time in seconds that the mob takes to prepare to sneeze (while the prepare_sound is playing). Game default 1.
        probability (float, optional): The probability of sneezing. A value of 1.00 is 100%. Game default 0.02.
        sound (str, optional): Sound to play when the sneeze occurs.
        within_radius (float, optional): Distance in blocks that mobs will be startled. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sneeze)
    """

    identifier = "minecraft:behavior.sneeze"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    drop_item_chance: float | None = json_field(default=None, validators=[_number])
    loot_table: LootTable | str | None = json_field(
        default=None, validators=[instance_of(LootTable, str)]
    )
    prepare_sound: str | None = json_field(default=None, validators=[_string])
    prepare_time: float | None = json_field(default=None, validators=[_number])
    probability: float | None = json_field(default=None, validators=[_number])
    sound: str | None = json_field(default=None, validators=[_string])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAISniff(AIGoal):
    """Allows this entity to detect the nearest player within "sniffing_radius" and update its "minecraft:suspect_tracking" component state.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_range (float | NumberRange, optional): Cooldown range between sniffs in seconds.
        duration (float, optional): Sniffing duration in seconds. Game default 1.
        sniffing_radius (float, optional): Mob detection radius. Game default 5.
        suspicion_radius_horizontal (float, optional): Mob suspicion horizontal radius. When a player is within this radius horizontally, the anger level towards that player is increased. Game default 3.
        suspicion_radius_vertical (float, optional): Mob suspicion vertical radius. When a player is within this radius vertically, the anger level towards that player is increased. Game default 3.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sniff)
    """

    identifier = "minecraft:behavior.sniff"

    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    duration: float | None = json_field(default=None, validators=[_number])
    sniffing_radius: float | None = json_field(default=None, validators=[_number])
    suspicion_radius_horizontal: float | None = json_field(
        default=None, validators=[_number]
    )
    suspicion_radius_vertical: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=1)]
    )


class EntityAISonicBoom(AIGoal):
    """Allows this entity to perform a 'sonic boom' ranged attack.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_cooldown (float, optional): Cooldown in seconds required after using this attack until the entity can use sonic boom again. Game default 5.
        attack_damage (float, optional): Attack damage of the sonic boom. Game default 30.
        attack_range_horizontal (float, optional): Horizontal range (in blocks) at which the sonic boom can damage the target. Game default 15.
        attack_range_vertical (float, optional): Vertical range (in blocks) at which the sonic boom can damage the target. Game default 20.
        attack_sound (str, optional): Sound event for the attack.
        charge_sound (str, optional): Sound event for the charge up.
        duration (float, optional): Goal duration in seconds. Game default 0.
        duration_until_attack_sound (float, optional): Duration in seconds until the attack sound is played. Game default 1.7.
        knockback_height_cap (float, optional): Height cap of the attack knockback's vertical delta. Game default 0.
        knockback_horizontal_strength (float, optional): Horizontal strength of the attack's knockback applied to the attack target. Game default 0.
        knockback_vertical_strength (float, optional): Vertical strength of the attack's knockback applied to the attack target. Game default 0.
        speed_multiplier (float, optional): This multiplier modifies the attacking entity's speed when moving toward the target. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sonic_boom)
    """

    identifier = "minecraft:behavior.sonic_boom"

    attack_cooldown: float | None = json_field(default=None, validators=[_number])
    attack_damage: float | None = json_field(default=None, validators=[_number])
    attack_range_horizontal: float | None = json_field(
        default=None, validators=[_number]
    )
    attack_range_vertical: float | None = json_field(default=None, validators=[_number])
    attack_sound: str | None = json_field(default=None, validators=[_string])
    charge_sound: str | None = json_field(default=None, validators=[_string])
    duration: float | None = json_field(default=None, validators=[_number])
    duration_until_attack_sound: float | None = json_field(
        default=None, validators=[_number]
    )
    knockback_height_cap: float | None = json_field(default=None, validators=[_number])
    knockback_horizontal_strength: float | None = json_field(
        default=None, validators=[_number]
    )
    knockback_vertical_strength: float | None = json_field(
        default=None, validators=[_number]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAISquidDive(AIGoal):
    """Allows the squid to dive down in water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_dive)
    """

    identifier = "minecraft:behavior.squid_dive"


class EntityAISquidFlee(AIGoal):
    """Allows the squid to swim away.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_flee)
    """

    identifier = "minecraft:behavior.squid_flee"


class EntityAISquidIdle(AIGoal):
    """Allows the squid to swim in place idly.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_idle)
    """

    identifier = "minecraft:behavior.squid_idle"


class EntityAISquidMoveAwayFromGround(AIGoal):
    """Allows the squid to move away from ground blocks and back to water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_move_away_from_ground)
    """

    identifier = "minecraft:behavior.squid_move_away_from_ground"


class EntityAISquidOutOfWater(AIGoal):
    """Allows the squid to stick to the ground when outside water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_out_of_water)
    """

    identifier = "minecraft:behavior.squid_out_of_water"


class EntityAIStalkAndPounceOnTarget(AIGoal):
    """Allows a mob to stalk a target, then once within range pounce onto a target, on success the target will be attacked dealing damage defined by the attack component. On failure, the mob will risk getting stuck.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        interest_time (float, optional): The amount of time the mob will be interested before pouncing. This happens when the mob is within range of pouncing. Game default 2.
        leap_dist (float, optional): The distance in blocks the mob jumps in the direction of its target. Game default 0.8.
        leap_distance (float, optional): The distance in blocks the mob jumps in the direction of its target. Game default 0.8.
        leap_height (float, optional): The height in blocks the mob jumps when leaping at its target. Game default 0.9.
        max_stalk_dist (float, optional): The maximum distance away a target can be before the mob gives up on stalking. Game default 10.
        pounce_max_dist (float, optional): The maximum distance away from the target in blocks to begin pouncing at the target. Game default 5.
        set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Game default false.
        stalk_speed (float, optional): The movement speed in which you stalk your target. Game default 1.2.
        strike_dist (float, optional): The max distance away from the target when landing from the pounce that will still result in damaging the target. Game default 2.
        stuck_blocks (Filter, optional): Blocks that the mob can get stuck in after a pounce.
        stuck_time (float, optional): The amount of time the mob will be stuck if they fail and land on a block they can be stuck on. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stalk_and_pounce_on_target)
    """

    identifier = "minecraft:behavior.stalk_and_pounce_on_target"

    interest_time: float | None = json_field(default=None, validators=[_number])
    leap_dist: float | None = json_field(default=None, validators=[_number])
    leap_distance: float | None = json_field(default=None, validators=[_number])
    leap_height: float | None = json_field(default=None, validators=[_number])
    max_stalk_dist: float | None = json_field(default=None, validators=[_number])
    pounce_max_dist: float | None = json_field(default=None, validators=[_number])
    set_persistent: bool | None = json_field(default=None, validators=[_boolean])
    stalk_speed: float | None = json_field(default=None, validators=[_number])
    strike_dist: float | None = json_field(default=None, validators=[_number])
    stuck_blocks: Filter | None = json_field(default=None, validators=[_filter])
    stuck_time: float | None = json_field(default=None, validators=[_number])


class EntityAIStayNearNoteblock(AIGoal):
    """The entity will attempt to toss the items from its inventory to a nearby recently played noteblock.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        listen_time (int, optional): Sets the time an entity should stay near a noteblock after hearing it. Game default 30.
        speed (float, optional): Sets the entity's speed when moving toward the block. Game default 1.
        start_distance (float, optional): Sets the distance the entity needs to be away from the block to attempt to start the goal. Game default 10.
        stop_distance (float, optional): Sets the distance from the block the entity will attempt to reach. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_near_noteblock)
    """

    identifier = "minecraft:behavior.stay_near_noteblock"

    listen_time: int | None = json_field(default=None, validators=[_integer])
    speed: float | None = json_field(default=None, validators=[_number])
    start_distance: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])


class EntityAIStayWhileSitting(AIGoal):
    """Allows the mob to stay put while it is in a sitting state instead of doing something else.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_while_sitting)
    """

    identifier = "minecraft:behavior.stay_while_sitting"


class EntityAIStompAttack(AIGoal):
    """Allows an entity to attack using stomp AoE damage behavior.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Game default false.
        attack_types (str, optional): Defines the entity types this entity will attack.
        can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Game default false.
        cooldown_time (float, optional): Cooldown time, in seconds, between consecutive attacks. Game default 1.
        inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Game default 0.25.
        max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.55.
        min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.2.
        no_damage_range_multiplier (float, optional): Multiplied with the final AoE damage range to determine a no damage range. The stomp attack will go on cooldown if target is in this no damage range. Game default 2.
        on_attack (EventTrigger | str, optional): Defines the event to trigger when this entity successfully attacks.
        on_kill (EventTrigger | str, optional): Defines the event to trigger when this entity kills the target.
        outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Game default 0.5.
        path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Game default 0.75.
        path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Game default 16.
        path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Game default 32.
        random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Game default 0.
        reach_multiplier (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Game default 2.
        require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Game default false.
        speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Game default 1.
        stomp_range_multiplier (float, optional): Multiplied with the base size of the entity to determine stomp AoE damage range. Game default 2.
        track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Game default false.
        x_max_rotation (float, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stomp_attack)
    """

    identifier = "minecraft:behavior.stomp_attack"

    attack_once: bool | None = json_field(default=None, validators=[_boolean])
    attack_types: str | None = json_field(default=None, validators=[_string])
    can_spread_on_fire: bool | None = json_field(default=None, validators=[_boolean])
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    inner_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    max_path_time: float | None = json_field(default=None, validators=[_number])
    min_path_time: float | None = json_field(default=None, validators=[_number])
    no_damage_range_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    on_attack: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_kill: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    outer_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_fail_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_inner_boundary: float | None = json_field(default=None, validators=[_number])
    path_outer_boundary: float | None = json_field(default=None, validators=[_number])
    random_stop_interval: int | None = json_field(default=None, validators=[_integer])
    reach_multiplier: float | None = json_field(default=None, validators=[_number])
    require_complete_path: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    stomp_range_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    track_target: bool | None = json_field(default=None, validators=[_boolean])
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_head_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAIStompTurtleEgg(AIGoal):
    """Allows this mob to stomp turtle eggs.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 0.5.
        interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Game default 120.
        search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Game default 10.
        search_height (int, optional): Height in blocks the mob will look for turtle eggs to move towards. Game default 1.
        search_range (int, optional): The distance in blocks it will look for turtle eggs to move towards. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stomp_turtle_egg)
    """

    identifier = "minecraft:behavior.stomp_turtle_egg"

    goal_radius: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    interval: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_count: int | None = json_field(default=None, validators=[_integer])
    search_height: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    search_range: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=0, min_exclusive=True)]
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAIStrollTowardsVillage(AIGoal):
    """Allows the mob to move into a random location within a village within the search range.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Game default 8.
        goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Game default 1.5.
        search_range (int, optional): The distance in blocks to search for villages. If <= 0, find the closest village regardless of distance. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Game default 1.
        start_chance (float, optional): Chance that the mob will start this goal, from 0 to 1. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stroll_towards_village)
    """

    identifier = "minecraft:behavior.stroll_towards_village"

    cooldown_time: float | None = json_field(default=None, validators=[_number])
    goal_radius: float | None = json_field(default=None, validators=[_number])
    search_range: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    start_chance: float | None = json_field(default=None, validators=[_number])


class EntityAISummonEntity(AIGoal):
    """Allows the mob to attack the player by summoning other entities.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        summon_choices (list[SummonChoice], optional): List of spells for the mob to use to summon entities. Add more with `add_summon_choice`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_summon_entity)
    """

    identifier = "minecraft:behavior.summon_entity"

    summon_choices: list[SummonChoice] = json_field(
        default_factory=list,
        validators=[each(instance_of(SummonChoice))],
        omit_default=True,
    )

    def add_summon_choice(
        self,
        *,
        cast_duration: float | None = None,
        cooldown_time: float | None = None,
        do_casting: bool | None = None,
        filters: Filter | None = None,
        max_activation_range: float | None = None,
        min_activation_range: float | None = None,
        particle_color: str | RGBA255 | None = None,
        sequence: list[SummonStep] | None = None,
        start_sound_event: str | None = None,
        weight: float | None = None,
    ) -> "EntityAISummonEntity":
        """Adds a spell. See `SummonChoice` for the parameters."""
        self.summon_choices.append(
            SummonChoice(
                cast_duration=cast_duration,
                cooldown_time=cooldown_time,
                do_casting=do_casting,
                filters=filters,
                max_activation_range=max_activation_range,
                min_activation_range=min_activation_range,
                particle_color=particle_color,
                sequence=list(sequence or []),
                start_sound_event=start_sound_event,
                weight=weight,
            )
        )
        return self


class EntityAISwell(AIGoal):
    """Allows the creeper to swell up when a player is nearby. It can only be used by Creepers.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        start_distance (float, optional): This mob starts swelling when a target is at least this many blocks away. Game default 10.
        stop_distance (float, optional): This mob stops swelling when a target has moved away at least this many blocks. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swell)
    """

    identifier = "minecraft:behavior.swell"

    start_distance: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])


class EntityAISwimIdle(AIGoal):
    """Allows the entity go idle, if swimming. Entity must be in water.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        idle_time (float, optional): Amount of time (in seconds) to stay idle. Game default 5.
        success_rate (float, optional): Percent chance this entity will go idle, 1.0 = 100%. Game default 0.1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_idle)
    """

    identifier = "minecraft:behavior.swim_idle"

    idle_time: float | None = json_field(default=None, validators=[_number])
    success_rate: float | None = json_field(default=None, validators=[_number])


class EntityAISwimUpForBreath(AIGoal):
    """Allows the mob to try to move to air once it is close to running out of its total breathable supply. Requires "minecraft:breathable".

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        material_type (str, optional): The material the mob is traveling in. An air block will only be considered valid to move to with a block of this material below it. Options are: "water", "lava", or "any". Game default water.
        search_height (int, optional): The height (in blocks) above the mob's current position that it will search for a valid air block to move to. Game default 16.
        search_radius (int, optional): The radius (in blocks) around the mob's current position that it will search for a valid air block to move to. Game default 4.
        speed_mod (float, optional): Movement speed multiplier of the mob when using this Goal. Game default 1.4.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_up_for_breath)
    """

    identifier = "minecraft:behavior.swim_up_for_breath"

    material_type: str | None = json_field(default=None, validators=[_string])
    search_height: int | None = json_field(default=None, validators=[_integer])
    search_radius: int | None = json_field(default=None, validators=[_integer])
    speed_mod: float | None = json_field(default=None, validators=[_number])


class EntityAISwimWander(AIGoal):
    """Allows the entity to wander around while swimming, when not path-finding.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        interval (float, optional): Percent chance to start wandering, when not path-finding. 1 = 100%. Game default 0.0083.
        look_ahead (float, optional): Distance to look ahead for obstacle avoidance, while wandering. Game default 5.
        speed_multiplier (float, optional): This multiplier modifies the entity's speed when wandering. Game default 1.
        wander_time (float, optional): Amount of time (in seconds) to wander after wandering behavior was successfully started. Game default 5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_wander)
    """

    identifier = "minecraft:behavior.swim_wander"

    interval: float | None = json_field(default=None, validators=[_number])
    look_ahead: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    wander_time: float | None = json_field(default=None, validators=[_number])


class EntityAISwimWithEntity(EntityTypesAIGoal):
    """Allows the entity follow another entity. Both entities must be swimming [ie, in water].

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        catch_up_multiplier (float, optional): The multiplier this entity's speed is modified by when matching another entity's direction. Game default 2.5.
        catch_up_threshold (float, optional): Distance, from the entity being followed, at which this entity will speed up to reach that entity. Game default 12.
        chance_to_stop (float, optional): Percent chance to stop following the current entity, if they're riding another entity or they're not swimming. 1.0 = 100%. Game default 0.0333.
        entity_types (list[GoalEntityType], optional): Filters which types of entities are valid to follow. Add entries with `add_entity_type`.
        match_direction_threshold (float, optional): Distance, from the entity being followed, at which this entity will try to match that entity's direction. Game default 2.
        search_range (float, optional): Radius around this entity to search for another entity to follow. Game default 20.
        speed_multiplier (float, optional): The multiplier this entity's speed is modified by when trying to catch up to the entity being followed. Game default 1.5.
        state_check_interval (float, optional): Time (in seconds) between checks to determine if this entity should catch up to the entity being followed or match the direction of the entity being followed. Game default 0.5.
        stop_distance (float, optional): Distance, from the entity being followed, at which this entity will stop following that entity. Game default 5.
        success_rate (float, optional): Percent chance to start following another entity, if not already doing so. 1.0 = 100%. Game default 0.1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_with_entity)
    """

    identifier = "minecraft:behavior.swim_with_entity"

    catch_up_multiplier: float | None = json_field(default=None, validators=[_number])
    catch_up_threshold: float | None = json_field(default=None, validators=[_number])
    chance_to_stop: float | None = json_field(default=None, validators=[_number])
    match_direction_threshold: float | None = json_field(
        default=None, validators=[_number]
    )
    search_range: float | None = json_field(default=None, validators=[_number])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    state_check_interval: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])
    success_rate: float | None = json_field(default=None, validators=[_number])


class EntityAISwoopAttack(AIGoal):
    """Allows an entity to attack using swoop attack behavior; Ideal for use with flying mobs. The behavior ends if the entity has a horizontal collision or gets hit.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        damage_reach (float, optional): Added to the base size of the entity, to determine the target's maximum allowable distance, when trying to deal attack damage. Game default 0.2.
        delay_range (float | NumberRange, optional): Minimum and maximum cooldown time-range (in seconds) between each attempted swoop attack.
        speed_multiplier (float, optional): During swoop attack behavior, this determines the multiplier the entity's speed is modified by when moving toward the target. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swoop_attack)
    """

    identifier = "minecraft:behavior.swoop_attack"

    damage_reach: float | None = json_field(default=None, validators=[_number])
    delay_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAITakeBlock(AIGoal):
    """AI goal that makes entities pick up blocks from the world, like Endermen grabbing blocks to carry. Configure which blocks the entity can take and the search radius. Works with place_block behavior to create entities that relocate blocks or harvest materials from the environment.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        affected_by_griefing_rule (bool, optional): If true, whether the goal is affected by the mob griefing game rule. Game default true.
        blocks (list[BlockReference], optional): Block descriptors for which blocks are valid to be taken by the entity, if empty all blocks are valid.
        can_take (Filter, optional): Filters for if the entity should try to take a block. Self and Target are set.
        chance (float, optional): Chance each tick for the entity to try and take a block. Game default 1.
        on_take (EventTrigger | str, optional): Trigger ran if the entity does take a block. Self, Target, and Block are set.
        requires_line_of_sight (bool, optional): If true, whether the entity needs line of sight to the block they are trying to take. Game default true.
        xz_range (tuple[int, int], optional): XZ range from which the entity will try and take blocks from.
        y_range (tuple[int, int], optional): Y range from which the entity will try and take blocks from.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_take_block)
    """

    identifier = "minecraft:behavior.take_block"

    affected_by_griefing_rule: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    blocks: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks], encoder=encoders.block_objects
    )
    can_take: Filter | None = json_field(default=None, validators=[_filter])
    chance: float | None = json_field(
        default=None, validators=[_number, in_range(maximum=1)]
    )
    on_take: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    requires_line_of_sight: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    xz_range: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )
    y_range: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair], encoder=encoders.min_max
    )


class EntityAITakeFlower(AIGoal):
    """Allows the mob to accept flowers from another mob with the minecraft:offer_flower behavior.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.
        max_head_rotation_y (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Game default 30.
        max_rotation_x (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Game default 30.
        max_wait_time (float, optional): The maximum amount of time (in seconds) for the mob to randomly wait for before taking the flower. Game default 20.
        min_distance_to_target (float, optional): Minimum distance (in blocks) for the entity to be considered having reached its target. Game default 2.
        min_wait_time (float, optional): The minimum amount of time (in seconds) for the mob to randomly wait for before taking the flower. Game default 4.
        on_take_flower (EventTrigger | str, optional): Event triggered when the entity takes a flower from another entity.
        search_area (Vector3D, optional): The dimensions of the AABB used to search for a potential mob to take a flower from.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 0.5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_take_flower)
    """

    identifier = "minecraft:behavior.take_flower"

    filters: Filter | None = json_field(default=None, validators=[_filter])
    max_head_rotation_y: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_rotation_x: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    max_wait_time: float | None = json_field(default=None, validators=[_number])
    min_distance_to_target: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    min_wait_time: float | None = json_field(default=None, validators=[_number])
    on_take_flower: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    search_area: Vector3D | None = json_field(default=None, validators=[vector3])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])


class EntityAITeleportToOwner(AIGoal):
    """Allows an entity to teleport to its owner.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown (float, optional): The time in seconds that must pass for the entity to be able to try to teleport again. Game default 1.
        filters (Filter, optional): Conditions to be satisfied for the entity to teleport to its owner.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_teleport_to_owner)
    """

    identifier = "minecraft:behavior.teleport_to_owner"

    cooldown: float | None = json_field(default=None, validators=[_number])
    filters: Filter | None = json_field(default=None, validators=[_filter])


class EntityAITempt(AIGoal):
    """Allows a mob to be tempted by a player holding a specific item. Uses pathfinding for movement.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        can_get_scared (bool, optional): If true, the mob can stop being tempted if the player moves too fast while close to this mob. Game default false.
        can_tempt_vertically (bool, optional): If true, vertical distance to the player will be considered when tempting. Game default false.
        can_tempt_while_ridden (bool, optional): If true, the mob can be tempted even if it has a passenger (i.e. if being ridden). Game default false.
        items (list[ItemReference], optional): List of items that can tempt the mob.
        on_tempt_end (EventTrigger | str, optional): Event to trigger when this mob stops being tempted.
        on_tempt_start (EventTrigger | str, optional): Event to trigger when this mob starts being tempted.
        sound_interval (float | NumberRange, optional): Range of random ticks to wait between tempt sounds. Can be a number, an array [min, max], or an object with range_min/range_max or min/max.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 1.
        stop_distance (float, optional): The distance at which the mob will stop following the player. Game default 1.5.
        tempt_sound (str, optional): Sound to play while the mob is being tempted.
        within_radius (float, optional): Distance in blocks this mob can get tempted by a player holding an item they like. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_tempt)
    """

    identifier = "minecraft:behavior.tempt"

    can_get_scared: bool | None = json_field(default=None, validators=[_boolean])
    can_tempt_vertically: bool | None = json_field(default=None, validators=[_boolean])
    can_tempt_while_ridden: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    items: list[ItemReference] | None = json_field(default=None, validators=[_items])
    on_tempt_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_tempt_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    sound_interval: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    stop_distance: float | None = json_field(default=None, validators=[_number])
    tempt_sound: str | None = json_field(default=None, validators=[_string])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAITimerFlag1(AIGoal):
    """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping due to that timeout or due to being interrupted by another behavior, fires another event. query.timer_flag_1 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_range (float | NumberRange, optional): Goal cooldown range in seconds. Can be a range object or a single number.
        duration_range (float | NumberRange, optional): Goal duration range in seconds. Can be a range object or a single number.
        on_end (EventTrigger | str, optional): Event(s) to run when the goal ends.
        on_start (EventTrigger | str, optional): Event(s) to run when the goal starts.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_1)
    """

    identifier = "minecraft:behavior.timer_flag_1"

    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    duration_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    on_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAITimerFlag2(AIGoal):
    """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping due to that timeout or due to being interrupted by another behavior, fires another event. query.timer_flag_2 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_range (float | NumberRange, optional): Goal cooldown range in seconds. Can be a range object or a single number.
        duration_range (float | NumberRange, optional): Goal duration range in seconds. Can be a range object or a single number.
        on_end (EventTrigger | str, optional): Event(s) to run when the goal ends.
        on_start (EventTrigger | str, optional): Event(s) to run when the goal starts.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_2)
    """

    identifier = "minecraft:behavior.timer_flag_2"

    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    duration_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    on_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAITimerFlag3(AIGoal):
    """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping due to that timeout or due to being interrupted by another behavior, fires another event. query.timer_flag_3 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        cooldown_range (float | NumberRange, optional): Goal cooldown range in seconds. Can be a range object or a single number.
        duration_range (float | NumberRange, optional): Goal duration range in seconds. Can be a range object or a single number.
        on_end (EventTrigger | str, optional): Event(s) to run when the goal ends.
        on_start (EventTrigger | str, optional): Event(s) to run when the goal starts.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_3)
    """

    identifier = "minecraft:behavior.timer_flag_3"

    cooldown_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    duration_range: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    on_end: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_start: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )


class EntityAITradeInterest(AIGoal):
    """Allows the mob to look at a player that is holding a tradable item.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        carried_item_switch_time (float, optional): The max time in seconds that the trader will hold an item before attempting to switch for a different item that takes the same trade. Game default 2.
        cooldown (float, optional): The time in seconds before the trader can use this goal again. Game default 2.
        interest_time (float, optional): The max time in seconds that the trader will be interested with showing its trade items. Game default 45.
        remove_item_time (float, optional): The max time in seconds that the trader will wait when you no longer have items to trade. Game default 1.
        within_radius (float, optional): Distance in blocks this mob can be interested by a player holding an item they like. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_trade_interest)
    """

    identifier = "minecraft:behavior.trade_interest"

    carried_item_switch_time: float | None = json_field(
        default=None, validators=[_number]
    )
    cooldown: float | None = json_field(default=None, validators=[_number])
    interest_time: float | None = json_field(default=None, validators=[_number])
    remove_item_time: float | None = json_field(default=None, validators=[_number])
    within_radius: float | None = json_field(default=None, validators=[_number])


class EntityAITradeWithPlayer(AIGoal):
    """Allows the player to trade with this mob. When the goal starts, it will stop the mob's navigation.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        filters (Filter, optional): Conditions that need to be met for the behavior to start.
        max_distance_from_player (float, optional): The max distance that the mob can be from the player before exiting the goal. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_trade_with_player)
    """

    identifier = "minecraft:behavior.trade_with_player"

    filters: Filter | None = json_field(default=None, validators=[_filter])
    max_distance_from_player: float | None = json_field(
        default=None, validators=[_number]
    )


class EntityAITransportItems(AIGoal):
    """A behavior that enables a mob to transport items from and to containers.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        allow_simultaneous_interaction (bool, optional): When true the mob will wait until a container is not used by other entities before starting to interact with it. Game default false.
        allowed_items (list[ItemReference], optional): A list of item descriptors that are the only items the mob is allowed to transport.
        destination_container_types (list[BlockReference], optional): A list of block descriptors that should be container types to put items in. Can be simple block identifier strings or objects with name, states, and tags.
        disallowed_items (list[ItemReference], optional): A list of item descriptors that are the mob is not allowed to transport. If non-empty "allowed_items" must be empty.
        idle_cooldown (int, optional): When the mob cannot find a container in which to get or put items, the goal will stop being active for this amount of time in seconds. Game default 20.
        initial_cooldown (int, optional): How long the mob will wait after spawning or getting the goal added before the goal can start. Game default 0.
        interaction_time (float, optional): The amount of time in seconds spent interacting with the containers. Game default 3.
        max_stack_size (int, optional): The maximum stack size that the mob will try to take from a container. Game default 64.
        max_visited_containers (int, optional): The maximum number of containers that the mob will try to take/place items from before going on cooldown and starting over. Game default 16.
        place_strategy (Literal["any", "with_matching", "with_matching_or_empty"], optional): The strategy to use for placing the transported item. Game default any.
        search_distance (tuple[int, int], optional): The maximum search distance horizontally and vertically at which to find containers for taking or placing items.
        search_strategy (Literal["nearest", "random"], optional): The strategy to use for finding source or destination containers. The nearest valid container or a random valid container in range. Game default random.
        source_container_types (list[BlockReference], optional): A list of block descriptors that should be container types to take items from. Can be simple block identifier strings or objects with name, states, and tags.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_transport_items)
    """

    identifier = "minecraft:behavior.transport_items"

    allow_simultaneous_interaction: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    allowed_items: list[ItemReference] | None = json_field(
        default=None, validators=[_items]
    )
    destination_container_types: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks], encoder=encoders.block_objects
    )
    disallowed_items: list[ItemReference] | None = json_field(
        default=None, validators=[_items]
    )
    idle_cooldown: int | None = json_field(default=None, validators=[_integer])
    initial_cooldown: int | None = json_field(default=None, validators=[_integer])
    interaction_time: float | None = json_field(default=None, validators=[_number])
    max_stack_size: int | None = json_field(
        default=None, validators=[_integer, in_range(minimum=1, maximum=64)]
    )
    max_visited_containers: int | None = json_field(default=None, validators=[_integer])
    place_strategy: Literal["any", "with_matching", "with_matching_or_empty"] | None = (
        json_field(
            default=None,
            validators=[one_of("any", "with_matching", "with_matching_or_empty")],
        )
    )
    search_distance: tuple[int, int] | None = json_field(
        default=None, validators=[integer_pair]
    )
    search_strategy: Literal["nearest", "random"] | None = json_field(
        default=None, validators=[one_of("nearest", "random")]
    )
    source_container_types: list[BlockReference] | None = json_field(
        default=None, validators=[_blocks], encoder=encoders.block_objects
    )

    def __validate__(self) -> None:
        if self.allowed_items and self.disallowed_items:
            raise ValueError(
                "EntityAITransportItems takes `allowed_items` or `disallowed_items`, not both."
            )


class EntityAIUseKineticWeapon(AIGoal):
    """Enables a mob to use kinetic weaponry by intermittently charging at its target and repositioning afterward.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        approach_distance (float, optional): The distance to the target within which the mob begins using its kinetic weapon. Game default 8.
        attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Game default false.
        attack_types (str, optional): Defines the entity types this entity will attack.
        can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Game default false.
        cooldown_distance (float | NumberRange, optional): The distance the mob retreats to after all of the item's "minecraft:kinetic_weapon" component's "max_duration" values have elapsed.
        cooldown_speed_multiplier (float, optional): Multiplier applied to the mob's movement speed while on cooldown. Game default 1.
        cooldown_time (float, optional): Cooldown time, in seconds, between consecutive attacks. Game default 1.
        hijack_mount_navigation (bool, optional): Allows the mob to override its mount's navigation behavior with the logic defined by this goal. Game default false.
        inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Game default 0.25.
        max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.55.
        melee_fov (float, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Game default 90.
        min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Game default 0.2.
        on_attack (EventTrigger | str, optional): Defines the event to trigger when this entity successfully attacks.
        on_kill (EventTrigger | str, optional): Defines the event to trigger when this entity kills the target.
        outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Game default 0.5.
        path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Game default 0.75.
        path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Game default 16.
        path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Game default 32.
        random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Game default 0.
        reposition_distance (float | NumberRange, optional): The distance the mob retreats to once the target is closer than the midpoint of the item's "minecraft:kinetic_weapon" component's minimum and maximum "reach".
        reposition_speed_multiplier (float, optional): Multiplier applied to the mob's movement speed while repositioning. Game default 1.
        require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Game default false.
        speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Game default 1.
        track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Game default false.
        weapon_min_speed_multiplier (float, optional): Multiplier applied to each "min_speed" and "min_relative_speed" condition in the item's "minecraft:kinetic_weapon" component. Game default 1.
        weapon_reach_multiplier (float, optional): Multiplier applied to the item's "minecraft:kinetic_weapon" component's "reach". Game default 1.
        x_max_rotation (float, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Game default 30.
        y_max_head_rotation (float, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Game default 30.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_use_kinetic_weapon)
    """

    identifier = "minecraft:behavior.use_kinetic_weapon"

    approach_distance: float | None = json_field(default=None, validators=[_number])
    attack_once: bool | None = json_field(default=None, validators=[_boolean])
    attack_types: str | None = json_field(default=None, validators=[_string])
    can_spread_on_fire: bool | None = json_field(default=None, validators=[_boolean])
    cooldown_distance: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    cooldown_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    cooldown_time: float | None = json_field(default=None, validators=[_number])
    hijack_mount_navigation: bool | None = json_field(
        default=None, validators=[_boolean]
    )
    inner_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    max_path_time: float | None = json_field(default=None, validators=[_number])
    melee_fov: float | None = json_field(default=None, validators=[_number])
    min_path_time: float | None = json_field(default=None, validators=[_number])
    on_attack: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    on_kill: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    outer_boundary_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_fail_time_increase: float | None = json_field(
        default=None, validators=[_number]
    )
    path_inner_boundary: float | None = json_field(default=None, validators=[_number])
    path_outer_boundary: float | None = json_field(default=None, validators=[_number])
    random_stop_interval: int | None = json_field(default=None, validators=[_integer])
    reposition_distance: float | NumberRange | None = json_field(
        default=None, validators=[number_or_range], encoder=encoders.min_max
    )
    reposition_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    require_complete_path: bool | None = json_field(default=None, validators=[_boolean])
    speed_multiplier: float | None = json_field(default=None, validators=[_number])
    track_target: bool | None = json_field(default=None, validators=[_boolean])
    weapon_min_speed_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    weapon_reach_multiplier: float | None = json_field(
        default=None, validators=[_number]
    )
    x_max_rotation: float | None = json_field(default=None, validators=[_number])
    y_max_head_rotation: float | None = json_field(default=None, validators=[_number])


class EntityAIVexCopyOwnerTarget(EntityTypesAIGoal):
    """Allows the mob to target the same entity its owner is targeting.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        entity_types (list[GoalEntityType], optional): List of entities this mob can copy the owner from. Add entries with `add_entity_type`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_vex_copy_owner_target)
    """

    identifier = "minecraft:behavior.vex_copy_owner_target"


class EntityAIVexRandomMove(AIGoal):
    """Allows the mob to move around randomly like the Vex.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_vex_random_move)
    """

    identifier = "minecraft:behavior.vex_random_move"


class EntityAIWork(AIGoal):
    """Allows the NPC to use the POI.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        active_time (int, optional): The amount of ticks the NPC will stay in their the work location. Game default 0.
        can_work_in_rain (bool, optional): If true, this entity can work when their jobsite POI is being rained on. Game default false.
        goal_cooldown (int, optional): The amount of ticks the goal will be on cooldown before it can be used again. Game default 0.
        on_arrival (EventTrigger | str, optional): Event to run when the mob reaches their jobsite.
        sound_delay_max (int, optional): The max interval in which a sound will play. Game default 0.
        sound_delay_min (int, optional): The min interval in which a sound will play. Game default 0.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 0.5.
        work_in_rain_tolerance (int, optional): If "can_work_in_rain" is false, this is the maximum number of ticks left in the goal where rain will not interrupt the goal. Game default -1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_work)
    """

    identifier = "minecraft:behavior.work"

    active_time: int | None = json_field(default=None, validators=[_integer])
    can_work_in_rain: bool | None = json_field(default=None, validators=[_boolean])
    goal_cooldown: int | None = json_field(default=None, validators=[_integer])
    on_arrival: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    sound_delay_max: int | None = json_field(default=None, validators=[_integer])
    sound_delay_min: int | None = json_field(default=None, validators=[_integer])
    speed_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    work_in_rain_tolerance: int | None = json_field(default=None, validators=[_integer])


class EntityAIWorkComposter(AIGoal):
    """Allows the NPC to use the composter POI to convert excess seeds into bone meal.

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over.
        active_time (int, optional): The amount of ticks the NPC will stay in their the work location. Game default 0.
        block_interaction_max (int, optional): The maximum number of times the mob will interact with the composter. Game default 1.
        can_empty_composter (bool, optional): Determines whether the mob can empty a full composter. Game default true.
        can_fill_composter (bool, optional): Determines whether the mob can add items to a composter given that it is not full. Game default true.
        can_work_in_rain (bool, optional): If true, this entity can work when their jobsite POI is being rained on. Game default false.
        goal_cooldown (int, optional): The amount of ticks the goal will be on cooldown before it can be used again. Game default 0.
        items_per_use_max (int, optional): The maximum number of items which can be added to the composter per block interaction. Game default 20.
        min_item_count (int, optional): Limits the amount of each compostable item the mob can use. Any amount held over this number will be composted if possible. Game default 10.
        on_arrival (EventTrigger | str, optional): Event to run when the mob reaches their jobsite.
        speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Game default 0.5.
        use_block_max (int, optional): The maximum interval in which the mob will interact with the composter. Game default 200.
        use_block_min (int, optional): The minimum interval in which the mob will interact with the composter. Game default 100.
        work_in_rain_tolerance (int, optional): If "can_work_in_rain" is false, this is the maximum number of ticks left in the goal where rain will not interrupt the goal. Game default -1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_work_composter)
    """

    identifier = "minecraft:behavior.work_composter"

    active_time: int | None = json_field(default=None, validators=[_integer])
    block_interaction_max: int | None = json_field(default=None, validators=[_integer])
    can_empty_composter: bool | None = json_field(default=None, validators=[_boolean])
    can_fill_composter: bool | None = json_field(default=None, validators=[_boolean])
    can_work_in_rain: bool | None = json_field(default=None, validators=[_boolean])
    goal_cooldown: int | None = json_field(default=None, validators=[_integer])
    items_per_use_max: int | None = json_field(default=None, validators=[_integer])
    min_item_count: int | None = json_field(default=None, validators=[_integer])
    on_arrival: EventTrigger | str | None = json_field(
        default=None, validators=[_event], encoder=encoders.trigger
    )
    speed_multiplier: float | None = json_field(
        default=None, validators=[_number, in_range(minimum=0, min_exclusive=True)]
    )
    use_block_max: int | None = json_field(default=None, validators=[_integer])
    use_block_min: int | None = json_field(default=None, validators=[_integer])
    work_in_rain_tolerance: int | None = json_field(default=None, validators=[_integer])


# endregion
