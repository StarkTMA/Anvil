from typing import Annotated, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.core.components import EventTrigger
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.api.vanilla.effects import MinecraftEffects
from anvil.lib.jsonmodel import (
    BlockId,
    Chance,
    DespawnDistance,
    InRange,
    JsonComponent,
    JsonObject,
    Length,
    NonNegative,
    Ordered,
    RangeMinMax,
    Trigger,
    json_field,
)
from anvil.lib.jsonmodel.enums import (
    DamageCause,
    Slots,
)

# region Parts: objects nested inside components


class BandwidthValues(JsonObject):
    """Bandwidth optimization values of `minecraft:conditional_bandwidth_optimization`.

    Args:
        max_dropped_ticks (int, optional): The maximum ticks spatial update packets can be not sent. Game default 10.
        max_optimized_distance (float, optional): The maximum distance considered during bandwidth optimizations. Game default 80.
        use_motion_prediction_hints (bool, optional): Sends smaller motion packets during drop packet intervals. Game default false.
    """

    max_dropped_ticks: Annotated[int, NonNegative] | None = json_field(default=None)
    max_optimized_distance: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    use_motion_prediction_hints: bool | None = json_field(default=None)


class ConditionalBandwidthValues(BandwidthValues):
    """Bandwidth optimization values used while their conditions are met.

    Args:
        conditional_values (Filter): Conditions that must be met for these values to be used.
        max_dropped_ticks (int, optional): The maximum ticks spatial update packets can be not sent. Game default 10.
        max_optimized_distance (float, optional): The maximum distance considered during bandwidth optimizations. Game default 80.
        use_motion_prediction_hints (bool, optional): Sends smaller motion packets during drop packet intervals. Game default false.
    """

    conditional_values: Filter = json_field()


class Hitbox(JsonObject):
    """A hitbox of `minecraft:custom_hit_test`.

    Args:
        width (float): Width of the hitbox.
        height (float): Height of the hitbox.
        pivot (tuple[float, float, float], optional): Pivot point of the hitbox.
    """

    width: float = json_field()
    height: float = json_field()
    pivot: tuple[float, float, float] | None = json_field(default=None)


class PushPreset(JsonObject):
    """How an entity is pushed by other entities, when the preset's filters match.

    Args:
        filters (Filter, optional): Conditions for this preset to apply.
        kick_speed_scale (float, optional): Multiplier of the pusher's speed that sets the kick force. Ball mode only. Game default 2.
        max_distance (float, optional): Maximum horizontal distance at which entities push each other.
        max_kick_speed (float, optional): Maximum speed the entity is pushed at. Ball mode only. Game default 0.5.
        min_distance (float, optional): Minimum horizontal distance at which entities push each other. Game default 0.01.
        min_kick_speed (float, optional): Minimum speed the entity is pushed at. Ball mode only. Game default 0.
        play_sound (bool, optional): Plays the `pushed_by_player` sound when pushed by any entity. Game default false.
        play_sound_cooldown_in_seconds (float, optional): Seconds between push sounds. Game default 0.2.
        play_sound_impulse_threshold (float, optional): Minimum velocity change that plays the sound. Game default 0.2.
        push_mode (Literal["ball", "default", "legacy_boat", "legacy_minecart", "none"], optional): How the push is calculated. Game default default.
        push_scale_other (float, optional): Scales the push this entity applies to the other. Game default 1.
        push_scale_self (float, optional): Scales the push this entity applies to itself. Game default 1.
        require_collision_overlap (bool, optional): Entities push each other only when their collision boxes overlap. Game default true.
        strength_multiplier (float, optional): Multiplier of the push strength. Game default 0.05.
        vertical_kick_multiplier (float, optional): Upward force when pushed on the ground. Ball mode only. Game default 0.3.
    """

    filters: Filter | None = json_field(default=None)
    kick_speed_scale: float | None = json_field(default=None)
    max_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    max_kick_speed: float | None = json_field(default=None)
    min_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    min_kick_speed: float | None = json_field(default=None)
    play_sound: bool | None = json_field(default=None)
    play_sound_cooldown_in_seconds: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    play_sound_impulse_threshold: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    push_mode: (
        Literal["ball", "default", "legacy_boat", "legacy_minecart", "none"] | None
    ) = json_field(default=None)
    push_scale_other: float | None = json_field(default=None)
    push_scale_self: float | None = json_field(default=None)
    require_collision_overlap: bool | None = json_field(default=None)
    strength_multiplier: float | None = json_field(default=None)
    vertical_kick_multiplier: float | None = json_field(default=None)


# endregion

# region Components


class EntityAirDragModifier(JsonComponent):
    """Sets how much air drag slows this entity down. Not in the Microsoft reference.

    Args:
        strength (float, optional): From 0 to 1.
    """

    identifier = "minecraft:air_drag_modifier"

    strength: Annotated[float, Chance] | None = json_field(default=None)


class EntityAreaAttack(JsonComponent):
    """A component that does damage to entities that get within range.

    Args:
        cause (DamageCause, optional): The type of damage applied to entities in range.
        damage_cooldown (float, optional): Seconds between attacks. Game default 0.
        damage_per_tick (int, optional): Damage per tick applied to entities in range. Game default 2.
        damage_range (float, optional): How close an entity must be to be damaged. Game default 0.2.
        death_message_override (str, optional): A localization key used as the death message.
        entity_filter (Filter, optional): The entities that can be damaged.
        play_attack_sound (bool, optional): Whether the entity plays its attack sound. Game default true.
        use_self_as_damage_source (bool, optional): Whether the entity is the source of the damage. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_area_attack)
    """

    identifier = "minecraft:area_attack"

    cause: DamageCause | None = json_field(default=None)
    damage_cooldown: Annotated[float, NonNegative] | None = json_field(default=None)
    damage_per_tick: int | None = json_field(default=None)
    damage_range: Annotated[float, NonNegative] | None = json_field(default=None)
    death_message_override: str | None = json_field(default=None)
    entity_filter: Filter | None = json_field(default=None)
    play_attack_sound: bool | None = json_field(default=None)
    use_self_as_damage_source: bool | None = json_field(default=None)


class EntityAttack(JsonComponent):
    """Defines an entity's melee attack damage and any additional status effects applied on hit. Typical damage values range from 3 (zombie, creeper) to 7-21 (iron golem).

    Args:
        damage (float | tuple[float, float]): The damage the melee attack deals, or a `(min, max)` range of the random amount. A negative value heals the entity instead.
        effect_amplifier (int, optional): Amplifier level (potion tier) of the status ailment applied to the damaged entity. Game default 0.
        effect_duration (float, optional): Duration in seconds of the status ailment applied to the damaged entity. Game default 0.
        effect_name (MinecraftEffects | str, optional): Identifier of the status ailment to apply to an entity attacked by this entity's melee attack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack)
    """

    identifier = "minecraft:attack"

    damage: float | tuple[float, float] = json_field()
    effect_amplifier: Annotated[int, NonNegative] | None = json_field(default=None)
    effect_duration: Annotated[float, NonNegative] | None = json_field(default=None)
    effect_name: MinecraftEffects | str | None = json_field(default=None)


class EntityAttackCooldown(JsonComponent):
    """Adds a cooldown to an entity, to prevent it from acquiring new attack targets.

    Args:
        attack_cooldown_time (float | tuple[float, float], optional): Seconds of the cooldown, or a `(min, max)` range.
        attack_cooldown_complete_event (EventTrigger | str, optional): Event to run when the cooldown is complete.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack_cooldown)
    """

    identifier = "minecraft:attack_cooldown"

    attack_cooldown_time: float | tuple[float, float] | None = json_field(default=None)
    attack_cooldown_complete_event: Annotated[EventTrigger | str, Trigger] | None = (
        json_field(default=None)
    )


class EntityBoss(JsonComponent):
    """Defines the current state of the boss for updating the boss HUD.

    Args:
        hud_range (int, optional): The max distance from the boss at which the boss's health bar is present on the players screen. Game default 55.
        name (str, optional): The name that will be displayed above the boss's health bar. Game default 55.
        should_darken_sky (bool, optional): Whether the sky should darken in the presence of the boss. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boss)
    """

    identifier = "minecraft:boss"

    hud_range: int | None = json_field(default=None)
    name: str | None = json_field(default=None)
    should_darken_sky: bool | None = json_field(default=None)


class EntityBounciness(JsonComponent):
    """Sets how much of its speed this entity keeps when it bounces off a block. Not in the Microsoft reference.

    Args:
        strength (float, optional): From 0 (no bounce) to 1 (keeps all its speed).
    """

    identifier = "minecraft:bounciness"

    strength: Annotated[float, Chance] | None = json_field(default=None)


class EntityBreathable(JsonComponent):
    """Defines what blocks this entity can breathe in and gives them the ability to suffocate.

    Args:
        breathe_blocks (list[str | Block | BlockDescriptor], optional): Blocks this entity can breathe in, in addition to the options below.
        breathes_air (bool, optional): Whether this entity can breathe in air. Game default true.
        breathes_lava (bool, optional): Whether this entity can breathe in lava. Game default true.
        breathes_solids (bool, optional): Whether this entity can breathe in solid blocks. Game default false.
        breathes_water (bool, optional): Whether this entity can breathe in water. Game default false.
        can_dehydrate (bool, optional): Whether water-only breathers take damage out of water. Game default false.
        generates_bubbles (bool, optional): Whether this entity has visible bubbles in water. Game default true.
        inhale_time (float, optional): Seconds to recover breath to maximum. Game default 0.
        non_breathe_blocks (list[str | Block | BlockDescriptor], optional): Blocks this entity cannot breathe in.
        suffocate_time (int, optional): Seconds between suffocation damage. Game default -20.
        total_supply (int, optional): Seconds the entity can hold its breath. Game default 15.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breathable)
    """

    identifier = "minecraft:breathable"

    breathe_blocks: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = (
        json_field(default=None)
    )
    breathes_air: bool | None = json_field(default=None)
    breathes_lava: bool | None = json_field(default=None)
    breathes_solids: bool | None = json_field(default=None)
    breathes_water: bool | None = json_field(default=None)
    can_dehydrate: bool | None = json_field(default=None)
    generates_bubbles: bool | None = json_field(default=None)
    inhale_time: float | None = json_field(default=None)
    non_breathe_blocks: (
        list[Annotated[str | Block | BlockDescriptor, BlockId]] | None
    ) = json_field(default=None)
    suffocate_time: int | None = json_field(default=None)
    total_supply: int | None = json_field(default=None)


class EntityBurnsInDaylight(JsonComponent):
    """Specifies that this entity takes fire damage when exposed to direct sunlight. The entity will catch fire when in sunlight unless it is wearing armor in the protection slot, standing in water, or in a shaded area.

    Args:
        protection_slot (Slots, optional): The equipment slot that provides protection from burning in sunlight: an armor slot, the mainhand or the offhand. Game default slot.armor.head.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_burns_in_daylight)
    """

    identifier = "minecraft:burns_in_daylight"

    protection_slot: (
        Literal[
            Slots.Body,
            Slots.Chest,
            Slots.Feet,
            Slots.Head,
            Slots.Legs,
            Slots.Mainhand,
            Slots.Offhand,
        ]
        | None
    ) = json_field(default=None)


class EntityCollisionBox(JsonComponent):
    """Sets the width and height of the Entity's collision box.

    Args:
        height (float, optional): Height of the collision box in blocks. A negative value will be assumed to be 0. Game default 1.8.
        width (float, optional): Width and Depth of the collision box in blocks. A negative value will be assumed to be 0. Game default 0.6.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_collision_box)
    """

    identifier = "minecraft:collision_box"

    height: Annotated[float, InRange(-100000000.0, 100000000.0)] | None = json_field(
        default=None
    )
    width: Annotated[float, InRange(-100000000.0, 100000000.0)] | None = json_field(
        default=None
    )


class EntityColor(JsonComponent):
    """Defines the entity's main color. This attribute only works on vanilla entities that have predefined color values (sheep, llama, shulker).

    Args:
        value (int): The Palette Color value of the entity. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color)
    """

    identifier = "minecraft:color"

    value: int = json_field()


class EntityColor2(JsonComponent):
    """Defines the entity's second texture color. Only works on vanilla entities that have a second predefined color values (tropical fish).

    Args:
        value (int): The second Palette Color value of the entity. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color2)
    """

    identifier = "minecraft:color2"

    value: int = json_field()


class EntityCombatRegeneration(JsonComponent):
    """Gives `Regeneration I` and removes `Mining Fatigue` from the mob that kills the entity's attack target.

    Args:
        apply_to_family (bool, optional): Determines if the mob will grant mobs of the same type combat buffs if they kill the target. Game default false.
        apply_to_self (bool, optional): Determines if the mob will grant itself the combat buffs if it kills the target. Game default false.
        regeneration_duration (int | Literal["infinite"], optional): The duration in seconds of Regeneration I added to the mob. Game default 5.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_combat_regeneration)
    """

    identifier = "minecraft:combat_regeneration"

    apply_to_family: bool | None = json_field(default=None)
    apply_to_self: bool | None = json_field(default=None)
    regeneration_duration: int | Literal["infinite"] | None = json_field(default=None)


class EntityConditionalBandwidthOptimization(JsonComponent):
    """Defines the Conditional Spatial Update Bandwidth Optimizations of this entity.

    Args:
        default_values (BandwidthValues, optional): The default optimization values. Set it with `set_default_values`.
        conditional_values (list[ConditionalBandwidthValues], optional): Values used while their conditions are met. Add more with `add_conditional_values`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_conditional_bandwidth_optimization)
    """

    identifier = "minecraft:conditional_bandwidth_optimization"

    default_values: BandwidthValues | None = json_field(default=None)
    conditional_values: list[ConditionalBandwidthValues] = json_field(
        default_factory=list, omit_default=True
    )

    def add_conditional_values(
        self,
        *,
        conditional_values: Filter,
        max_dropped_ticks: int | None = None,
        max_optimized_distance: float | None = None,
        use_motion_prediction_hints: bool | None = None,
    ) -> "EntityConditionalBandwidthOptimization":
        """Adds values used while their conditions are met. See `ConditionalBandwidthValues`."""
        self.conditional_values.append(
            ConditionalBandwidthValues(
                conditional_values=conditional_values,
                max_dropped_ticks=max_dropped_ticks,
                max_optimized_distance=max_optimized_distance,
                use_motion_prediction_hints=use_motion_prediction_hints,
            )
        )
        return self

    def set_default_values(
        self,
        *,
        max_dropped_ticks: int | None = None,
        max_optimized_distance: float | None = None,
        use_motion_prediction_hints: bool | None = None,
    ) -> "EntityConditionalBandwidthOptimization":
        """Sets the default optimization values. See `BandwidthValues` for the parameters."""
        self.default_values = BandwidthValues(
            max_dropped_ticks=max_dropped_ticks,
            max_optimized_distance=max_optimized_distance,
            use_motion_prediction_hints=use_motion_prediction_hints,
        )
        return self


class EntityCustomHitTest(JsonComponent):
    """Hitboxes for melee and ranged hits against the entity.

    Args:
        hitboxes (list[Hitbox], optional): The hitboxes. Add more with `add_hitbox`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_custom_hit_test)
    """

    identifier = "minecraft:custom_hit_test"

    hitboxes: list[Hitbox] = json_field(default_factory=list, omit_default=True)

    def add_hitbox(
        self,
        *,
        width: float,
        height: float,
        pivot: tuple[float, float, float] | None = None,
    ) -> "EntityCustomHitTest":
        """Adds a hitbox. See `Hitbox` for the parameters."""
        self.hitboxes.append(Hitbox(width=width, height=height, pivot=pivot))
        return self


class EntityDamageAbsorption(JsonComponent):
    """Allows this entity to absorb damage of the given causes with the armor in its body slot. Not in the Microsoft reference.

    Args:
        absorbable_causes (list[DamageCause], optional): The damage causes the entity absorbs.
    """

    identifier = "minecraft:damage_absorption"

    absorbable_causes: list[DamageCause] | None = json_field(default=None)


class EntityDamageOverTime(JsonComponent):
    """Applies defined amount of damage to the entity at specified intervals.

    Args:
        damage_per_hurt (int, optional): Amount of damage caused each hurt. Game default 1.
        time_between_hurt (float, optional): Time in seconds between damage. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_over_time)
    """

    identifier = "minecraft:damage_over_time"

    damage_per_hurt: int | None = json_field(default=None)
    time_between_hurt: float | None = json_field(default=None)


class EntityDespawn(JsonComponent):
    """Despawns the entity when the despawn rules or the optional filters are true.

    Args:
        despawn_from_chance (bool, optional): Uses `min_range_random_chance` in the standard despawn rules. Game default true.
        despawn_from_distance (tuple[int, int], optional): `(min_distance, max_distance)` used by the standard despawn rules. Game default (32, 128).
        despawn_from_inactivity (bool, optional): Uses `min_range_inactivity_timer` in the standard despawn rules. Game default true.
        despawn_from_simulation_edge (bool, optional): Despawns at once at the edge of the simulation distance. Game default true.
        filters (Filter, optional): Conditions for despawning. When set, the standard despawn rules are ignored.
        min_range_inactivity_timer (int, optional): Seconds the mob must be inactive. Game default 30.
        min_range_random_chance (int, optional): A random chance between 1 and this value. Game default 800.
        remove_child_entities (bool, optional): Also despawns entities linked as children, such as leashed ones. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_despawn)
    """

    identifier = "minecraft:despawn"

    despawn_from_chance: bool | None = json_field(default=None)
    despawn_from_distance: (
        Annotated[tuple[int, int], NonNegative, Ordered, DespawnDistance] | None
    ) = json_field(default=None)
    despawn_from_inactivity: bool | None = json_field(default=None)
    despawn_from_simulation_edge: bool | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)
    min_range_inactivity_timer: int | None = json_field(default=None)
    min_range_random_chance: int | None = json_field(default=None)
    remove_child_entities: bool | None = json_field(default=None)


class EntityDimensionBound(JsonComponent):
    """Prevents the entity from changing dimension through portals.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dimension_bound)
    """

    identifier = "minecraft:dimension_bound"


class EntityDryingOutTimer(JsonComponent):
    """Adds a timer for drying out that counts down and runs `dried_out_event`, or stops when the entity gets under rain or water and runs `stopped_drying_out_event`.

    Args:
        total_time (float, optional): Seconds to dry out fully. Game default 0.
        water_bottle_refill_time (float, optional): Extra seconds given by a splash water bottle. Game default 0.
        dried_out_event (EventTrigger | str, optional): Event to run when the drying out time runs out.
        recover_after_dried_out_event (EventTrigger | str, optional): Event to run when a dried out entity gets water again.
        stopped_drying_out_event (EventTrigger | str, optional): Event to run when the entity stops drying out.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_drying_out_timer)
    """

    identifier = "minecraft:drying_out_timer"

    total_time: Annotated[float, NonNegative] | None = json_field(default=None)
    water_bottle_refill_time: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    dried_out_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    recover_after_dried_out_event: Annotated[EventTrigger | str, Trigger] | None = (
        json_field(default=None)
    )
    stopped_drying_out_event: Annotated[EventTrigger | str, Trigger] | None = (
        json_field(default=None)
    )


class EntityExhaustionValues(JsonComponent):
    """Defines how much exhaustion each player action should take.

    Args:
        attack (float, optional): Amount of exhaustion applied when attacking. Game default 0.1.
        damage (float, optional): Amount of exhaustion applied when taking damage. Game default 0.1.
        heal (float, optional): Amount of exhaustion applied when healed through food regeneration. Game default 6.
        jump (float, optional): Amount of exhaustion applied when jumping. Game default 0.05.
        lunge (float, optional): Amount of exhaustion applied when triggering the Lunge enchantment, multiplied by the enchantment level. This item requires a format version of at least 1.21.130. Game default 4.
        mine (float, optional): Amount of exhaustion applied when mining. Game default 0.005.
        sprint (float, optional): Amount of exhaustion applied when sprinting. Game default 0.01.
        sprint_jump (float, optional): Amount of exhaustion applied when sprint jumping. Game default 0.2.
        swim (float, optional): Amount of exhaustion applied when swimming. Game default 0.01.
        walk (float, optional): Amount of exhaustion applied when walking. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_exhaustion_values)
    """

    identifier = "minecraft:exhaustion_values"

    attack: float | None = json_field(default=None)
    damage: float | None = json_field(default=None)
    heal: float | None = json_field(default=None)
    jump: float | None = json_field(default=None)
    lunge: float | None = json_field(default=None)
    mine: float | None = json_field(default=None)
    sprint: float | None = json_field(default=None)
    sprint_jump: float | None = json_field(default=None)
    swim: float | None = json_field(default=None)
    walk: float | None = json_field(default=None)


class EntityExperienceReward(JsonComponent):
    """Defines the experience this entity rewards.

    Args:
        on_bred (Molang | float, optional): The amount of experience rewarded when this entity is successfully bred.
        on_death (Molang | float, optional): The amount of experience rewarded when this entity dies.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_experience_reward)
    """

    identifier = "minecraft:experience_reward"

    on_bred: Molang | str | float | None = json_field(default=None)
    on_death: Molang | str | float | None = json_field(default=None)


class EntityFireImmune(JsonComponent):
    """Sets that this entity doesn't take damage from fire.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_fire_immune)
    """

    identifier = "minecraft:fire_immune"


class EntityFollowRange(JsonComponent):
    """Defines the maximum range, in blocks, that a mob will pursue a target. This affects AI behaviors like chasing players or attacking.

    Args:
        value (int): The default follow range in blocks. Entities will attempt to stay within this radius of their target.
        max (int, optional): Maximum follow distance in blocks. The entity will not pursue targets beyond this range.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_follow_range)
    """

    identifier = "minecraft:follow_range"

    value: int = json_field()
    max: int | None = json_field(default=None)


class EntityFreezingImmune(JsonComponent):
    """Makes this entity immune to freezing in powder snow. Not in the Microsoft reference."""

    identifier = "minecraft:freezing_immune"


class EntityFreezingVulnerable(JsonComponent):
    """Makes this entity take extra damage from freezing. Not in the Microsoft reference."""

    identifier = "minecraft:freezing_vulnerable"


class EntityFrictionModifier(JsonComponent):
    """Defines how much friction affects this entity. In format version 1.26.20, the component's behavior was corrected to match its description: higher values cause more friction (0.0 = no friction, 1.0 = regular, 2.0 = double). It now affects ground friction only (no longer partially affecting air or liquid drag) and works correctly on players and other client-predicted entities. Add `minecraft:uses_legacy_friction` to opt back into the legacy behavior; entities authored against format versions older than 1.26.20 receive it automatically.

    Args:
        value (float): The higher the number, the more friction affects this entity. A value of 1.0 means regular friction, while 2.0 means twice as much. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_friction_modifier)
    """

    identifier = "minecraft:friction_modifier"

    value: float = json_field()


class EntityHealth(JsonComponent):
    """Defines the health pool for an entity, measured in health points (1 point = half a heart). Typical values: cow (10), zombie (20), iron golem (100), wither (600).

    Args:
        value (int | tuple[float, float]): Starting health for this entity in health points, or a `(min, max)` range to pick it from. Game default 20.
        max (int, optional): Maximum health this entity can have. Can be higher than the starting value to allow healing beyond initial health. Game default 20.
        min (int, optional): Minimum health. Not in the Microsoft reference.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_health)
    """

    identifier = "minecraft:health"

    value: Annotated[int | tuple[int, int], RangeMinMax] = json_field()
    max: int | None = json_field(default=None)
    min: int | None = json_field(default=None)


class EntityHeartbeat(JsonComponent):
    """Defines the entity's heartbeat.

    Args:
        interval (Molang | float, optional): The inter-beat interval in seconds. A value of zero or less means no heartbeat. Game default 1.00.
        sound_event (str, optional): Level sound event to be played as the heartbeat sound. Game default heartbeat.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_heartbeat)
    """

    identifier = "minecraft:heartbeat"

    interval: Molang | str | float | None = json_field(default=None)
    sound_event: str | None = json_field(default=None)


class EntityInsomnia(JsonComponent):
    """Adds a timer since last rested to see if phantoms should spawn.

    Args:
        days_until_insomnia (float, optional): Number of days the mob has to stay up until the insomnia effect begins. Game default 3.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_insomnia)
    """

    identifier = "minecraft:insomnia"

    days_until_insomnia: float | None = json_field(default=None)


class EntityInstantDespawn(JsonComponent):
    """Despawns the Actor immediately.

    Args:
        remove_child_entities (bool, optional): If true, all entities linked to this entity in a child relationship (eg. leashed) will also be despawned. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_instant_despawn)
    """

    identifier = "minecraft:instant_despawn"

    remove_child_entities: bool | None = json_field(default=None)


class EntityIsBaby(JsonComponent):
    """Sets that this entity is a baby. This is used to set the is_baby value for use in query functions like Molang and Filters.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_baby)
    """

    identifier = "minecraft:is_baby"


class EntityIsCharged(JsonComponent):
    """Sets that this entity is charged. This is used to set the is_charged value for use in query functions like Molang and Filters.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_charged)
    """

    identifier = "minecraft:is_charged"


class EntityIsChested(JsonComponent):
    """Sets that this entity is currently carrying a chest.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_chested)
    """

    identifier = "minecraft:is_chested"


class EntityIsCollidable(JsonComponent):
    """Allows other mobs to have vertical and horizontal collisions with this mob. For a collision to occur, both mobs must have a "minecraft:collision_box" component. This component can only be used on mobs and enables collisions exclusively between mobs. Please note that this type of collision is unreliable for moving collidable mobs. It is recommended to use this component only in scenarios where the collidable mob remains stationary. Collidable behavior is closely related to stackable behavior. While the "minecraft:is_collidable" component governs how other mobs interact with the component's owner, the "minecraft:is_stackable" component describes how an entity interacts with others of its own kind.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_collidable)
    """

    identifier = "minecraft:is_collidable"


class EntityIsHiddenWhenInvisible(JsonComponent):
    """The entity can hide from hostile mobs while invisible.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_hidden_when_invisible)
    """

    identifier = "minecraft:is_hidden_when_invisible"


class EntityIsIgnited(JsonComponent):
    """Sets that this entity is currently on fire.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_ignited)
    """

    identifier = "minecraft:is_ignited"


class EntityIsIllagerCaptain(JsonComponent):
    """Sets that this entity is an Illager Captain.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_illager_captain)
    """

    identifier = "minecraft:is_illager_captain"


class EntityIsPregnant(JsonComponent):
    """Sets that this entity is currently pregnant.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_pregnant)
    """

    identifier = "minecraft:is_pregnant"


class EntityIsSaddled(JsonComponent):
    """Sets that this entity is currently saddled.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_saddled)
    """

    identifier = "minecraft:is_saddled"


class EntityIsShaking(JsonComponent):
    """Sets that this entity is currently shaking.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_shaking)
    """

    identifier = "minecraft:is_shaking"


class EntityIsSheared(JsonComponent):
    """Sets that this entity is currently sheared.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_sheared)
    """

    identifier = "minecraft:is_sheared"


class EntityIsStackable(JsonComponent):
    """Allows instances of this entity to have vertical and horizontal collisions with each other. For a collision to occur, both instances must have a "minecraft:collision_box" component. Stackable behavior is closely related to collidable behavior. While the "minecraft:is_stackable" component describes how an entity interacts with others of its own kind, the "minecraft:is_collidable" component governs how other mobs interact with the component's owner.

    Args:
        value (bool, optional): Whether this entity is stackable. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_stackable)
    """

    identifier = "minecraft:is_stackable"

    value: bool | None = json_field(default=None)


class EntityIsStunned(JsonComponent):
    """Sets that this entity is currently stunned.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_stunned)
    """

    identifier = "minecraft:is_stunned"


class EntityIsTamed(JsonComponent):
    """Sets that this entity is currently tamed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_tamed)
    """

    identifier = "minecraft:is_tamed"


class EntityItemHopper(JsonComponent):
    """Determines that this entity is an item hopper.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_hopper)
    """

    identifier = "minecraft:item_hopper"


class EntityKnockbackResistance(JsonComponent):
    """Determines an entity's resistance to knockback from melee attacks. A value of 0.0 means no resistance, while 1.0 provides full immunity to knockback (like iron golems). Negative values down to -2 amplify knockback instead of diminishing it.

    Args:
        value (float): The amount of knockback resistance, from -2 to 1 (full immunity).
        max (float, optional): Maximum potential knockback resistance for this entity.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_knockback_resistance)
    """

    identifier = "minecraft:knockback_resistance"

    value: Annotated[float, InRange(-2.0, 1.0)] = json_field()
    max: float | None = json_field(default=None)


class EntityMarkVariant(JsonComponent):
    """Mark Variant is typically used as an additional per-type way (besides `variant`) to express a different visual form of the same mob.

    Args:
        value (int): The Id of the mark_variant. By convention, 0 is the Id of the base entity. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mark_variant)
    """

    identifier = "minecraft:mark_variant"

    value: int = json_field()


class EntityNotPickableFromInside(JsonComponent):
    """Prevents players inside this entity from picking it. Not in the Microsoft reference."""

    identifier = "minecraft:not_pickable_from_inside"


class EntityOutOfControl(JsonComponent):
    """Defines the entity's 'out of control' state.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_out_of_control)
    """

    identifier = "minecraft:out_of_control"


class EntityPeek(JsonComponent):
    """Defines the entity's 'peek' behavior, and the events it runs.

    Args:
        on_close (EventTrigger | str, optional): Event to run when the entity is done peeking.
        on_open (EventTrigger | str, optional): Event to run when the entity starts peeking.
        on_target_open (EventTrigger | str, optional): Event to run when the entity's target starts peeking.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_peek)
    """

    identifier = "minecraft:peek"

    on_close: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    on_open: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    on_target_open: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )


class EntityPersistent(JsonComponent):
    """Defines whether an entity should be persistent in the game world.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_persistent)
    """

    identifier = "minecraft:persistent"


class EntityPhysics(JsonComponent):
    """Defines physics properties of an actor, including if it is affected by gravity or if it collides with objects.

    Args:
        has_collision (bool, optional): Whether or not the entity collides with things. Game default true.
        has_gravity (bool, optional): Whether or not the entity is affected by gravity. Game default true.
        push_towards_closest_space (bool, optional): Whether or not the entity should be pushed towards the nearest open area when stuck inside a block. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_physics)
    """

    identifier = "minecraft:physics"

    has_collision: bool | None = json_field(default=None)
    has_gravity: bool | None = json_field(default=None)
    push_towards_closest_space: bool | None = json_field(default=None)


class EntityPlayerExhaustion(JsonComponent):
    """Defines the player's exhaustion level.

    Args:
        max (float, optional): A maximum value for a player's exhaustion.
        value (float, optional): The initial value of a player's exhaustion level.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.exhaustion)
    """

    identifier = "minecraft:player.exhaustion"

    max: Annotated[float, NonNegative] | None = json_field(default=None)
    value: Annotated[float, NonNegative] | None = json_field(default=None)


class EntityPlayerExperience(JsonComponent):
    """Defines how much experience each player action should take.

    Args:
        max (int, optional): The maximum player experience of this entity. Game default 5.
        value (int, optional): The initial value of the player experience. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.experience)
    """

    identifier = "minecraft:player.experience"

    max: int | None = json_field(default=None)
    value: int | None = json_field(default=None)


class EntityPlayerLevel(JsonComponent):
    """Defines the player's level.

    Args:
        max (int, optional): The maximum player level value of the entity.
        value (int, optional): The initial value of the player level.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.level)
    """

    identifier = "minecraft:player.level"

    max: int | None = json_field(default=None)
    value: int | None = json_field(default=None)


class EntityPlayerSaturation(JsonComponent):
    """Defines the player's need for food.

    Args:
        max (float, optional): The maximum player saturation value.
        value (float, optional): The initial value of player saturation.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.saturation)
    """

    identifier = "minecraft:player.saturation"

    max: Annotated[float, NonNegative] | None = json_field(default=None)
    value: Annotated[float, NonNegative] | None = json_field(default=None)


class EntityPushThrough(JsonComponent):
    """Sets the distance through which the entity can push through.

    Args:
        value (float): The value of the entity's push-through, in blocks. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_push_through)
    """

    identifier = "minecraft:push_through"

    value: float = json_field()


class EntityPushableByBlock(JsonComponent):
    """Allows the entity to be pushed by certain blocks, like Shulker Boxes and Pistons. Added in 1.26.10 as part of the split of `minecraft:pushable` into `minecraft:pushable_by_block` (pistons and Shulker Boxes) and `minecraft:pushable_by_entity` (other entities). The legacy `minecraft:pushable` component is no longer parsed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable_by_block)
    """

    identifier = "minecraft:pushable_by_block"


class EntityPushableByEntity(JsonComponent):
    """Allows the entity to be pushed by other entities.

    Args:
        presets (list[PushPreset], optional): How the entity is pushed; the first preset whose filters match applies. Add more with `add_preset`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable_by_entity)
    """

    identifier = "minecraft:pushable_by_entity"

    presets: list[PushPreset] = json_field(default_factory=list, omit_default=True)

    def add_preset(
        self,
        *,
        filters: Filter | None = None,
        kick_speed_scale: float | None = None,
        max_distance: float | None = None,
        max_kick_speed: float | None = None,
        min_distance: float | None = None,
        min_kick_speed: float | None = None,
        play_sound: bool | None = None,
        play_sound_cooldown_in_seconds: float | None = None,
        play_sound_impulse_threshold: float | None = None,
        push_mode: (
            Literal["ball", "default", "legacy_boat", "legacy_minecart", "none"] | None
        ) = None,
        push_scale_other: float | None = None,
        push_scale_self: float | None = None,
        require_collision_overlap: bool | None = None,
        strength_multiplier: float | None = None,
        vertical_kick_multiplier: float | None = None,
    ) -> "EntityPushableByEntity":
        """Adds a preset. See `PushPreset` for the parameters."""
        self.presets.append(
            PushPreset(
                filters=filters,
                kick_speed_scale=kick_speed_scale,
                max_distance=max_distance,
                max_kick_speed=max_kick_speed,
                min_distance=min_distance,
                min_kick_speed=min_kick_speed,
                play_sound=play_sound,
                play_sound_cooldown_in_seconds=play_sound_cooldown_in_seconds,
                play_sound_impulse_threshold=play_sound_impulse_threshold,
                push_mode=push_mode,
                push_scale_other=push_scale_other,
                push_scale_self=push_scale_self,
                require_collision_overlap=require_collision_overlap,
                strength_multiplier=strength_multiplier,
                vertical_kick_multiplier=vertical_kick_multiplier,
            )
        )
        return self


class EntityRendersWhenInvisible(JsonComponent):
    """When set, the entity will render even when invisible. Appropriate rendering behavior can then be specified in the corresponding "minecraft:client_entity".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_renders_when_invisible)
    """

    identifier = "minecraft:renders_when_invisible"


class EntityScale(JsonComponent):
    """Sets the entity's visual size multiplier. A value of 1.0 means normal size, 0.5 is half size (commonly used for baby mobs), and values above 1.0 make the entity larger.

    Args:
        value (float): The scale multiplier for visual size. 1.0 = normal, 0.5 = half (babies), 2.0 = double size. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scale)
    """

    identifier = "minecraft:scale"

    value: float = json_field()


class EntityScaleByAge(JsonComponent):
    """Defines the entity's size interpolation based on the entity's age.

    Args:
        end_scale (float, optional): Ending scale of the entity when it's fully grown. Game default 1.
        start_scale (float, optional): Initial scale of the newborn entity. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scale_by_age)
    """

    identifier = "minecraft:scale_by_age"

    end_scale: float | None = json_field(default=None)
    start_scale: float | None = json_field(default=None)


class EntitySittable(JsonComponent):
    """Defines the entity's 'sit' state.

    Args:
        sit_event (EventTrigger | str, optional): Event to run when the entity enters the 'sit' state.
        stand_event (EventTrigger | str, optional): Event to run when the entity exits the 'sit' state.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sittable)
    """

    identifier = "minecraft:sittable"

    sit_event: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    stand_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )


class EntitySkinID(JsonComponent):
    """Skin ID value. Can be used to differentiate skins, such as base skins for villagers. Requires multiple texture sets to be set up for the entity.

    Args:
        value (int): The ID of the skin. By convention, 0 is the ID of the base skin. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_skin_id)
    """

    identifier = "minecraft:skin_id"

    value: int = json_field()


class EntitySoundVolume(JsonComponent):
    """Sets the entity's base volume for sound effects.

    Args:
        value (float, optional): The value of the volume the entity uses for sound effects. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sound_volume)
    """

    identifier = "minecraft:sound_volume"

    value: float | None = json_field(default=None)


class EntityStrength(JsonComponent):
    """Defines the strength of this entity.

    Args:
        max (int, optional): The maximum strength of this entity. Game default 5.
        value (int, optional): The initial value of the strength. Game default 1.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_strength)
    """

    identifier = "minecraft:strength"

    max: int | None = json_field(default=None)
    value: int | None = json_field(default=None)


class EntityTransient(JsonComponent):
    """An entity with this component will NEVER persist, and forever disappear when unloaded.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transient)
    """

    identifier = "minecraft:transient"


class EntityTypeFamily(JsonComponent):
    """Defines the family categories this entity belongs to. Type families are used by filters and other game systems to group entities (e.g., 'mob', 'monster', 'undead', 'zombie').

    Args:
        family (list[str]): A set of tags that describe the categories of this entity.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_type_family)
    """

    identifier = "minecraft:type_family"

    family: Annotated[list[str], Length(minimum=1)] = json_field()


class EntityUnderwaterMountBreathing(JsonComponent):
    """Pauses this entity's breathing under water.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_underwater_mount_breathing)
    """

    identifier = "minecraft:underwater_mount_breathing"


class EntityUseUniformAirDrag(JsonComponent):
    """Applies the same air drag on every axis. Not in the Microsoft reference."""

    identifier = "minecraft:use_uniform_air_drag"


class EntityUsesLegacyFriction(JsonComponent):
    """When set, legacy calculations are used when applying "minecraft:friction_modifier". This component is automatically added to legacy content to preserve existing behavior. The legacy calculations are incorrect and should not be used for new content. Added in 1.26.20 alongside the `minecraft:friction_modifier` behavior fix. Adding this component opts an entity back into the legacy (pre-1.26.20) friction calculations, which also partially affected air and liquid drag. Entities whose `format_version` is older than 1.26.20 receive this component automatically so that existing content keeps its prior behavior.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_uses_legacy_friction)
    """

    identifier = "minecraft:uses_legacy_friction"


class EntityVariant(JsonComponent):
    """Variant is typically used as a per-type way to express a different visual form of the same mob. For example, for cats, variant is a number that defines the breed of cat. This behavior is a requirement for setting up multiple types of variants for an entity.

    Args:
        value (int): The Id of the variant. By convention, 0 is the Id of the base entity/default appearance. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variant)
    """

    identifier = "minecraft:variant"

    value: int = json_field()


class EntityWantsJockey(JsonComponent):
    """Sets that this entity wants to become a jockey.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_wants_jockey)
    """

    identifier = "minecraft:wants_jockey"


# endregion
