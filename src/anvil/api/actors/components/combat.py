from typing import Annotated, Literal

from anvil.api.core.components import EventTrigger
from anvil.api.core.enums import (
    DamageCause,
    DamageSensor,
    Difficulty,
    ExplosionParticleEffect,
    FilterSubject,
    LineOfSightObstructionType,
    LookAtLocation,
    LootedAtSetTarget,
    Slots,
)
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.api.vanilla.effects import MinecraftEffects
from anvil.lib.jsonmodel import (
    AtLeastOne,
    BlockObject,
    Chance,
    EffectName,
    IndexInto,
    InRange,
    JsonComponent,
    JsonObject,
    Kept,
    MinMax,
    NonNegative,
    RangeMinMax,
    Trigger,
    Unique,
    Wrapped,
    XpRange,
    YesNo,
    json_field,
)
from anvil.lib.schemas import (
    MinecraftBlockDescriptor,
    MinecraftEntityDescriptor,
    MinecraftItemDescriptor,
)

# region Parts: objects nested inside components


class EntityEventTrigger(EventTrigger, JsonComponent, abstract=True):
    """Base of the trigger components (`minecraft:on_*`): an event, its filters and its target."""


class EquipmentChangeSlot(JsonObject):
    """An equipment slot `minecraft:on_equipment_changed` watches, and the events it runs.

    Args:
        slot (Slots, optional): The equipment slot to watch. Game default slot.weapon.mainhand.
        on_equip (str, optional): Event to run when the slot is changed to a non-empty item.
        on_unequip (str, optional): Event to run when the slot is changed to an empty item.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_equipment_changed)
    """

    slot: (
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
    on_equip: str | None = json_field(default=None)
    on_unequip: str | None = json_field(default=None)


class AmbientSoundEvent(JsonObject):
    """A level sound event `minecraft:ambient_sound_interval` plays when its condition is true.

    Args:
        event_name (str): Level sound event to be played as the ambient sound.
        condition (Molang | str): The condition that must be satisfied to select this sound.
    """

    event_name: str = json_field()
    condition: Molang | str = json_field()


class BlockBreakWatch(JsonObject):
    """Blocks `minecraft:block_sensor` watches, and the event it runs when one breaks.

    Args:
        block_list (list[str | MinecraftBlockDescriptor]): Blocks that trigger the event.
        on_block_broken (str): Event to call when a block in `block_list` is broken.
    """

    block_list: list[str | MinecraftBlockDescriptor] = json_field()
    on_block_broken: str = json_field()


class DamageCondition(JsonObject):
    """A condition under which `minecraft:hurt_on_condition` damages the entity.

    Args:
        cause (DamageCause, optional): The kind of damage caused to the entity.
        damage_per_tick (int, optional): The damage done each tick that the conditions are met. Game default 1.
        filters (Filter, optional): The conditions that must be satisfied.
    """

    cause: DamageCause | None = json_field(default=None)
    damage_per_tick: int | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)


class DamageSensorTrigger(JsonObject):
    """How `minecraft:damage_sensor` reacts to one kind of damage.

    Args:
        cause (DamageCause, optional): Type of damage that triggers the events. Game default none.
        deals_damage (DamageSensor | bool, optional): How received damage affects the entity. Game default yes.
        on_damage (EventTrigger, optional): The entities the trigger applies to, and the event to run when damaged.
        on_damage_sound_event (str, optional): The sound to play when the `on_damage` filters are met.
        damage_modifier (float, optional): Added to the base damage received. Game default 0.
        damage_multiplier (float, optional): Multiplies the base damage received. Game default 1.
    """

    cause: DamageCause | None = json_field(default=None)
    deals_damage: Annotated[bool, YesNo] | DamageSensor | None = json_field(
        default=None
    )
    on_damage: EventTrigger | None = json_field(default=None)
    on_damage_sound_event: str | None = json_field(default=None)
    damage_modifier: float | None = json_field(default=None)
    damage_multiplier: float | None = json_field(default=None)


class InsideBlockWatch(JsonObject):
    """A block `minecraft:inside_block_notifier` watches, and the events it runs.

    Args:
        block (str | MinecraftBlockDescriptor): The block to watch. A descriptor's states are matched too.
        entered_block_event (EventTrigger | str, optional): Event to run when the entity enters the block.
        exited_block_event (EventTrigger | str, optional): Event to run when the entity exits the block.
    """

    block: Annotated[str | MinecraftBlockDescriptor, BlockObject] = json_field()
    entered_block_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    exited_block_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )


class KnockbackPreset(JsonObject):
    """A rule of `minecraft:apply_knockback_rules`.

    Args:
        filter (Filter, optional): The entities affected by this rule.
        horizontal_power (float, optional): Power with which a target is knocked backwards. Game default 1.
        vertical_power (float, optional): Power with which a target is knocked upwards. Game default 0.4.
        vertical_velocity_cap (float, optional): Maximum Y velocity after knockback. Game default 0.4.
        slowdown_scale (float, optional): Scale applied to the target's velocity before knockback, at most 1. Game default 0.5.
        knockback_mode (Literal["relative_horizontal", "hit_direction"], optional): How knockback is applied. Game default relative_horizontal.
        scale_with_damage (bool, optional): Scales knockback by the inverse square of the damage. Game default false.
        extra_knockback_approach (Literal["reapply_default", "multiply", "multiply_reduced"], optional): How extra knockback from enchantments or sprinting combines. The reference names `multiply` in its notes and `multiply_reduced` in its schema. Game default reapply_default.
        check_if_target_is_immersed_in_water (bool, optional): Applies only when the target is fully in water. Game default false.
    """

    filter: Filter | None = json_field(default=None)
    horizontal_power: float | None = json_field(default=None)
    vertical_power: float | None = json_field(default=None)
    vertical_velocity_cap: float | None = json_field(default=None)
    slowdown_scale: Annotated[float, InRange(maximum=1)] | None = json_field(
        default=None
    )
    knockback_mode: Literal["relative_horizontal", "hit_direction"] | None = json_field(
        default=None
    )
    scale_with_damage: bool | None = json_field(default=None)
    extra_knockback_approach: (
        Literal["reapply_default", "multiply", "multiply_reduced"] | None
    ) = json_field(default=None)
    check_if_target_is_immersed_in_water: bool | None = json_field(default=None)


class RavagerReaction(JsonObject):
    """A weighted response of `minecraft:ravager_blocked` to its attack being blocked.

    Args:
        weight (int): The weight of this response.
        value (EventTrigger | str, optional): The event to run. Without it, nothing happens.
    """

    weight: Annotated[int, NonNegative] = json_field()
    value: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)


class ShooterProjectile(JsonObject):
    """A projectile `minecraft:shooter` can use, and when.

    Args:
        def_ (MinecraftEntityDescriptor | str): The projectile entity. Written as `def`.
        aux_val (int, optional): ID of the potion effect applied on hit.
        filters (Filter, optional): Conditions for this projectile to be used.
        lose_target (bool, optional): Whether the shooter loses its target after shooting.
    """

    def_: MinecraftEntityDescriptor | str = json_field(key="def")
    aux_val: int | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)
    lose_target: bool | None = json_field(default=None)


class SpellEffect(JsonObject):
    """An effect `minecraft:spell_effects` adds.

    Args:
        effect (MinecraftEffects | str): The effect.
        duration (int | Literal["infinite"], optional): The duration in seconds. Game default 0.
        amplifier (int, optional): The amplifier. Game default 0.
        ambient (bool, optional): Whether the effect is ambient. Game default false.
        visible (bool, optional): Whether the effect is visible. Game default true.
        display_on_screen_animation (bool, optional): Whether the effect plays an on-screen animation. Game default false.
    """

    effect: Annotated[MinecraftEffects | str, EffectName] = json_field()
    duration: int | Literal["infinite"] | None = json_field(default=None)
    amplifier: int | None = json_field(default=None)
    ambient: bool | None = json_field(default=None)
    visible: bool | None = json_field(default=None)
    display_on_screen_animation: bool | None = json_field(default=None)


class Subsensor(JsonObject):
    """A subsensor of `minecraft:entity_sensor`.

    Args:
        event (str): Event to run when the conditions are met. The game takes the name only.
        event_filters (Filter, optional): The conditions other entities must meet.
        cooldown (float, optional): Seconds before the subsensor senses again. Game default -1.
        maximum_count (int, optional): The maximum number of entities that must pass the filters. Game default -1.
        minimum_count (int, optional): The minimum number of entities that must pass the filters. Game default 1.
        range (tuple[float, float], optional): The maximum horizontal and vertical distance of other entities. Game default (10, 10).
        require_all (bool, optional): Requires every nearby entity to pass the filters. Game default false.
        y_offset (float, optional): Vertical offset applied to the entity's position. Game default 0.
    """

    event: str = json_field()
    event_filters: Filter | None = json_field(default=None)
    cooldown: float | None = json_field(default=None)
    maximum_count: int | None = json_field(default=None)
    minimum_count: int | None = json_field(default=None)
    range: tuple[float, float] | None = json_field(default=None)
    require_all: bool | None = json_field(default=None)
    y_offset: float | None = json_field(default=None)


class TimeChoice(JsonObject):
    """A weighted time `minecraft:timer` can pick.

    Args:
        value (float): The time in seconds.
        weight (int, optional): The weight of this choice.
    """

    value: Annotated[float, NonNegative] = json_field()
    weight: int | None = json_field(default=None)


class AngerSound(JsonObject):
    """A sound `minecraft:anger_level` plays when the entity is provoked.

    Args:
        sound (str): The sound to play.
        condition (Molang | str, optional): The condition under which the sound plays.
    """

    sound: str = json_field()
    condition: Molang | str | None = json_field(default=None)


class ProjectileArrowEffect(JsonObject):
    """Applies the arrow's tipped-potion effects to the entity hit.

    Args:
        apply_effect_to_blocking_targets (bool, optional): Applies the effects to targets that blocked. Game default true.
    """

    apply_effect_to_blocking_targets: bool | None = json_field(default=None)


class ProjectileCatchFire(JsonObject):
    """Sets the entity or block hit on fire.

    Args:
        fire_affected_by_griefing (bool, optional): No block catches fire when a mob shot it and mob griefing is off. Game default false.
        on_fire_time (float, optional): Seconds the entity hit burns. Game default 0.
    """

    fire_affected_by_griefing: bool | None = json_field(default=None)
    on_fire_time: Annotated[float, NonNegative] | None = json_field(default=None)


class ProjectileDefinitionEvent(JsonObject):
    """Runs an event when the projectile hits.

    Args:
        event_trigger (EventTrigger): The event to run, its filters and target.
        affect_projectile (bool, optional): Runs the event on the projectile. Game default false.
        affect_shooter (bool, optional): Runs the event on the shooter. Game default false.
        affect_splash_area (bool, optional): Runs the event on every entity within `splash_area`. Game default false.
        affect_target (bool, optional): Runs the event on the entity hit. Game default false.
        splash_area (float, optional): Radius in blocks used by `affect_splash_area`. Game default 0.
    """

    event_trigger: EventTrigger = json_field()
    affect_projectile: bool | None = json_field(default=None)
    affect_shooter: bool | None = json_field(default=None)
    affect_splash_area: bool | None = json_field(default=None)
    affect_target: bool | None = json_field(default=None)
    splash_area: Annotated[float, NonNegative] | None = json_field(default=None)


class ProjectileFreezeOnHit(JsonObject):
    """Freezes nearby water to ice around the impact.

    Args:
        shape (Literal["cube", "sphere"], optional): Shape of the frozen volume. Game default cube.
        size (float, optional): Half-extent of the frozen volume in blocks. Game default 1.
        snap_to_block (bool, optional): Centers the volume on the hit block. Game default false.
    """

    shape: Literal["cube", "sphere"] | None = json_field(default=None)
    size: Annotated[float, NonNegative] | None = json_field(default=None)
    snap_to_block: bool | None = json_field(default=None)


class ProjectileHurtOwner(JsonObject):
    """Damages the projectile's owner when the projectile lands.

    Args:
        ignite (bool, optional): Sets the owner on fire. Game default false.
        knockback (bool, optional): Knocks the owner back. Game default false.
        owner_damage (float, optional): Damage dealt to the owner. Game default 0.
    """

    ignite: bool | None = json_field(default=None)
    knockback: bool | None = json_field(default=None)
    owner_damage: float | None = json_field(default=None)


class ProjectileImpactDamage(JsonObject):
    """Damages the entity hit.

    Args:
        apply_knockback_to_blocking_targets (bool, optional): Knocks back targets that blocked. Game default false.
        catch_fire (bool, optional): Sets the entity hit on fire for the projectile's `on_fire_time`. Game default false.
        ceil_pre_critical_damage (bool, optional): Rounds the damage up before the critical multiplier. Game default false.
        channeling (bool, optional): Calls down lightning on the entity hit during a thunderstorm. Game default false.
        damage (float | tuple[float, float], optional): Damage dealt, or a `(min, max)` range rolled per hit. Written as `{"min", "max"}`. Game default 0.
        destroy_on_hit (bool, optional): Removes the projectile when it deals damage. Game default false.
        destroy_on_hit_requires_damage (bool, optional): `destroy_on_hit` needs at least one point of damage dealt. Game default true.
        difficulty_randomization (Literal["none", "additive", "multiplicative"], optional): How the world difficulty changes the damage. Game default none.
        filter (str, optional): The entity family or type the projectile can damage.
        knockback (bool, optional): Knocks the entity hit back. Game default false.
        max_critical_damage (int, optional): Maximum damage of a critical hit. Game default 2147483647.
        min_critical_damage (int, optional): Minimum damage of a critical hit. Game default 0.
        power_multiplier (float, optional): Multiplied by the projectile's speed and added to the damage. Game default 0.
        set_last_hurt_requires_damage (bool, optional): The projectile counts as the last attacker only when it deals damage. Game default true.
    """

    apply_knockback_to_blocking_targets: bool | None = json_field(default=None)
    catch_fire: bool | None = json_field(default=None)
    ceil_pre_critical_damage: bool | None = json_field(default=None)
    channeling: bool | None = json_field(default=None)
    damage: Annotated[float | tuple[float, float], MinMax] | None = json_field(
        default=None
    )
    destroy_on_hit: bool | None = json_field(default=None)
    destroy_on_hit_requires_damage: bool | None = json_field(default=None)
    difficulty_randomization: Literal["none", "additive", "multiplicative"] | None = (
        json_field(default=None)
    )
    filter: str | None = json_field(default=None)
    knockback: bool | None = json_field(default=None)
    max_critical_damage: int | None = json_field(default=None)
    min_critical_damage: int | None = json_field(default=None)
    power_multiplier: float | None = json_field(default=None)
    set_last_hurt_requires_damage: bool | None = json_field(default=None)


class ProjectileMobEffect(JsonObject):
    """An effect a projectile applies to the entity hit.

    Args:
        effect (MinecraftEffects | str): The effect.
        amplifier (int, optional): The amplifier. Game default 1.
        durationeasy (int | Literal["infinite"], optional): Duration in ticks on easy.
        durationnormal (int | Literal["infinite"], optional): Duration in ticks on normal.
        durationhard (int | Literal["infinite"], optional): Duration in ticks on hard.
    """

    effect: Annotated[MinecraftEffects | str, EffectName] = json_field()
    amplifier: int | None = json_field(default=None)
    durationeasy: int | Literal["infinite"] | None = json_field(default=None)
    durationnormal: int | Literal["infinite"] | None = json_field(default=None)
    durationhard: int | Literal["infinite"] | None = json_field(default=None)


class ProjectileParticleOnHit(JsonObject):
    """A particle effect at the impact.

    Args:
        particle_type (str): The particle to spawn.
        num_particles (int, optional): Particles spawned per hit. Game default 1.
        on_entity_hit (bool, optional): Spawns particles when an entity is hit. Game default false.
        on_other_hit (bool, optional): Spawns particles when something else is hit. Game default false.
    """

    particle_type: str = json_field()
    num_particles: int | None = json_field(default=None)
    on_entity_hit: bool | None = json_field(default=None)
    on_other_hit: bool | None = json_field(default=None)


class ProjectileSpawnAoeCloud(JsonObject):
    """An area effect cloud spawned at the impact.

    Args:
        affect_owner (bool, optional): The cloud affects the projectile's owner. Game default true.
        duration (int, optional): Seconds the cloud lasts. Game default 0.
        particle (str, optional): The particle the cloud emits. Game default mobspellambient.
        potion (int, optional): Aux value of the potion the cloud applies; -1 uses the projectile's. Game default -1.
        radius (float, optional): Initial radius in blocks. Game default 0.
        radius_on_use (float, optional): Radius change each time the cloud applies its effects; -1 keeps it. Game default -1.
        reapplication_delay (int, optional): Ticks before the cloud affects the same entity again. Game default 0.
    """

    affect_owner: bool | None = json_field(default=None)
    duration: int | None = json_field(default=None)
    particle: str | None = json_field(default=None)
    potion: int | None = json_field(default=None)
    radius: float | None = json_field(default=None)
    radius_on_use: float | None = json_field(default=None)
    reapplication_delay: int | None = json_field(default=None)


class ProjectileSpawnChance(JsonObject):
    """Spawns entities at the impact.

    Args:
        spawn_definition (MinecraftEntityDescriptor | str): The entity to spawn.
        first_spawn_chance (float, optional): Chance the first group spawns, from 0 to 1. Game default 0.
        first_spawn_count (int, optional): Entities in the first group. Game default 0.
        on_spawn (list[EventTrigger], optional): Events run on each spawned entity.
        second_spawn_chance (float, optional): Chance the second group spawns, from 0 to 1. Game default 0.
        second_spawn_count (int, optional): Entities in the second group. Game default 0.
        spawn_baby (bool, optional): Spawned entities start as babies. Game default false.
    """

    spawn_definition: MinecraftEntityDescriptor | str = json_field()
    first_spawn_chance: Annotated[float, Chance] | None = json_field(default=None)
    first_spawn_count: int | None = json_field(default=None)
    on_spawn: list[EventTrigger] | None = json_field(default=None)
    second_spawn_chance: Annotated[float, Chance] | None = json_field(default=None)
    second_spawn_count: int | None = json_field(default=None)
    spawn_baby: bool | None = json_field(default=None)


class ProjectileStickInGround(JsonObject):
    """Makes the projectile stick in the block it hits.

    Args:
        shake_time (float, optional): Seconds the projectile shakes after sticking. Game default 0.
    """

    shake_time: Annotated[float, NonNegative] | None = json_field(default=None)


class ProjectileThrownPotionEffect(JsonObject):
    """Applies a thrown potion's splash effects around the impact.

    Args:
        effect (int, optional): Aux value of the potion. Game default -1.
    """

    effect: int | None = json_field(default=None)


class ProjectileOnHit(JsonObject):
    """What happens when a projectile hits a block, a fluid or an entity.

    A part set to an object with no options, or a switch set to True, is written as `{}`,
    which turns that behavior on with the game's defaults.

    Args:
        arrow_effect (ProjectileArrowEffect, optional): Applies the arrow's tipped-potion effects.
        catch_fire (ProjectileCatchFire, optional): Sets the entity or block hit on fire.
        definition_event (ProjectileDefinitionEvent, optional): Runs an event.
        douse_fire (bool, optional): A water potion puts out fires around the hit block.
        freeze_on_hit (ProjectileFreezeOnHit, optional): Freezes nearby water.
        grant_xp (int | tuple[float, float], optional): Experience dropped, or a `(min, max)` range. Written as `{"minXP", "maxXP"}`.
        hurt_owner (ProjectileHurtOwner, optional): Damages the owner.
        ignite (bool, optional): Runs the entity's `on_ignite` trigger.
        impact_damage (ProjectileImpactDamage, optional): Damages the entity hit.
        mob_effect (list[ProjectileMobEffect], optional): Effects applied to the entity hit. Written as `{"effects": [...]}`.
        particle_on_hit (ProjectileParticleOnHit, optional): A particle effect at the impact.
        remove_on_hit (bool, optional): Removes the projectile.
        spawn_aoe_cloud (ProjectileSpawnAoeCloud, optional): Spawns an area effect cloud.
        spawn_chance (ProjectileSpawnChance, optional): Spawns entities.
        stick_in_ground (ProjectileStickInGround, optional): The projectile sticks in the block it hits.
        teleport_owner (bool, optional): Teleports the owner to the impact.
        thrown_potion_effect (ProjectileThrownPotionEffect, optional): Applies a thrown potion's effects.
        wind_burst_on_hit (bool, optional): Releases a wind burst that pushes entities away.
    """

    arrow_effect: Annotated[ProjectileArrowEffect, Kept] | None = json_field(
        default=None
    )
    catch_fire: Annotated[ProjectileCatchFire, Kept] | None = json_field(default=None)
    definition_event: ProjectileDefinitionEvent | None = json_field(default=None)
    douse_fire: Annotated[bool, Kept] | None = json_field(default=None)
    freeze_on_hit: Annotated[ProjectileFreezeOnHit, Kept] | None = json_field(
        default=None
    )
    grant_xp: Annotated[int | tuple[int, int], XpRange] | None = json_field(
        default=None
    )
    hurt_owner: Annotated[ProjectileHurtOwner, Kept] | None = json_field(default=None)
    ignite: Annotated[bool, Kept] | None = json_field(default=None)
    impact_damage: Annotated[ProjectileImpactDamage, Kept] | None = json_field(
        default=None
    )
    mob_effect: Annotated[list[ProjectileMobEffect], Wrapped("effects")] | None = (
        json_field(default=None)
    )
    particle_on_hit: ProjectileParticleOnHit | None = json_field(default=None)
    remove_on_hit: Annotated[bool, Kept] | None = json_field(default=None)
    spawn_aoe_cloud: Annotated[ProjectileSpawnAoeCloud, Kept] | None = json_field(
        default=None
    )
    spawn_chance: ProjectileSpawnChance | None = json_field(default=None)
    stick_in_ground: Annotated[ProjectileStickInGround, Kept] | None = json_field(
        default=None
    )
    teleport_owner: Annotated[bool, Kept] | None = json_field(default=None)
    thrown_potion_effect: Annotated[ProjectileThrownPotionEffect, Kept] | None = (
        json_field(default=None)
    )
    wind_burst_on_hit: Annotated[bool, Kept] | None = json_field(default=None)


class SpawnedEntity(JsonObject):
    """An entity or item `minecraft:spawn_entity` spawns on a timer.

    Set `spawn_entity` to spawn an entity, or leave it out to spawn `spawn_item`.

    Args:
        spawn_entity (MinecraftEntityDescriptor | str, optional): The entity to spawn.
        spawn_item (str | MinecraftItemDescriptor, optional): The item to spawn when no entity is set. Game default egg.
        spawn_event (EventTrigger | str, optional): Event run on the spawned entity. Game default minecraft:entity_born.
        spawn_item_event (EventTrigger | str, optional): Event run on this entity when the item spawns.
        spawn_method (str, optional): How the entity is spawned. Game default born.
        spawn_sound (str, optional): Sound played on spawning. Game default plop.
        filters (Filter, optional): Conditions for spawning.
        max_wait_time (int, optional): Maximum seconds between spawns. Game default 600.
        min_wait_time (int, optional): Minimum seconds between spawns. Game default 300.
        num_to_spawn (int, optional): Entities spawned each time. Game default 1.
        should_leash (bool, optional): Leashes the spawned entity to this entity. Game default false.
        single_use (bool, optional): Spawns only once. Game default false.
    """

    spawn_entity: MinecraftEntityDescriptor | str | None = json_field(default=None)
    spawn_item: str | MinecraftItemDescriptor | None = json_field(default=None)
    spawn_event: EventTrigger | str | None = json_field(default=None)
    spawn_item_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    spawn_method: str | None = json_field(default=None)
    spawn_sound: str | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)
    max_wait_time: int | None = json_field(default=None)
    min_wait_time: int | None = json_field(default=None)
    num_to_spawn: int | None = json_field(default=None)
    should_leash: bool | None = json_field(default=None)
    single_use: bool | None = json_field(default=None)


class TransformationDelay(JsonObject):
    """The delay before `minecraft:transformation` happens.

    Args:
        value (float, optional): Seconds before the entity transforms. Game default 0.
        range_min (float, optional): Seconds added to `value` for the lower end of a random delay. Game default 0.
        range_max (float, optional): Seconds added to `value` for the upper end of a random delay. Game default 0.
        block_assist_chance (float, optional): Chance the entity looks for nearby blocks that speed up the transformation, from 0 to 1. Game default 0.
        block_chance (float, optional): Chance a found block speeds up the transformation, from 0 to 1. Game default 0.
        block_max (int, optional): Maximum number of helping blocks. 0 uses the block radius. Game default 0.
        block_radius (int, optional): Distance in blocks searched for helping blocks. Game default 0.
        block_types (list[str | MinecraftBlockDescriptor], optional): Blocks that help the transformation.
    """

    value: Annotated[float, NonNegative] | None = json_field(default=None)
    range_min: Annotated[float, NonNegative] | None = json_field(default=None)
    range_max: Annotated[float, NonNegative] | None = json_field(default=None)
    block_assist_chance: Annotated[float, Chance] | None = json_field(default=None)
    block_chance: Annotated[float, Chance] | None = json_field(default=None)
    block_max: int | None = json_field(default=None)
    block_radius: int | None = json_field(default=None)
    block_types: list[str | MinecraftBlockDescriptor] | None = json_field(default=None)


# endregion

# region Components


class EntityAmbientSoundInterval(JsonComponent):
    """Delay for an entity playing its sound.

    Args:
        event_name (str, optional): Level sound event to be played as the ambient sound. Game default ambient.
        event_names (list[AmbientSoundEvent], optional): Sounds with conditions, evaluated in order; the first true one plays. Add more with `add_event_name`.
        range (float, optional): Maximum time in seconds to randomly add to the delay. Game default 16.
        value (float, optional): Minimum time in seconds before the entity plays its ambient sound again. Game default 8.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ambient_sound_interval)
    """

    identifier = "minecraft:ambient_sound_interval"

    event_name: str | None = json_field(default=None)
    event_names: list[AmbientSoundEvent] = json_field(
        default_factory=list, omit_default=True
    )
    range: Annotated[float, NonNegative] | None = json_field(default=None)
    value: Annotated[float, NonNegative] | None = json_field(default=None)

    def add_event_name(
        self, *, event_name: str, condition: Molang | str
    ) -> "EntityAmbientSoundInterval":
        """Adds a sound played when its condition is true.

        Args:
            event_name (str): Level sound event to be played.
            condition (Molang | str): The condition that selects this sound.
        """
        self.event_names.append(
            AmbientSoundEvent(event_name=event_name, condition=condition)
        )
        return self


class EntityAngerLevel(JsonComponent):
    """Compels the entity to track anger towards a set of nuisances.

    Args:
        anger_decrement_interval (float, optional): Seconds between each decrease of anger towards every nuisance. Game default 1.
        angry_boost (int, optional): Anger boost applied to the threshold when the mob gets angry. Game default 20.
        angry_threshold (int, optional): Anger level at which the mob is angry at a nuisance. Game default 80.
        broadcast_anger (bool, optional): Entities of the same type within `broadcast_range` also become angry. Game default false.
        broadcast_anger_on_attack (bool, optional): Broadcasts anger whenever this mob attacks. Game default false.
        broadcast_filters (Filter, optional): Conditions for other entities to receive the anger.
        broadcast_range (int, optional): Distance in blocks within which anger is broadcast. Game default 20.
        broadcast_targets (list[str], optional): Entity families to broadcast anger to.
        calm_event (EventTrigger | str, optional): Event to run when this entity calms down.
        default_annoyingness (int, optional): How much each provocation raises the anger level. Game default 0.
        default_projectile_annoyingness (int, optional): How much each projectile provocation raises the anger level. Game default 0.
        duration (int, optional): Seconds the entity stays angry.
        duration_delta (int, optional): Variance in seconds added to the duration.
        filters (Filter, optional): Mob types it should not attack while angry.
        max_anger (int, optional): Maximum anger level towards any nuisance. Game default 100.
        nuisance_filter (Filter, optional): Conditions for a mob to be a nuisance.
        on_increase_sounds (list[AngerSound], optional): Sounds played when provoked, the first matching one plays. Add more with `add_on_increase_sound`.
        remove_targets_below_angry_threshold (bool, optional): The mob drops its target when anger falls below the threshold. Game default true.
        sound_interval (int | tuple[float, float], optional): Seconds between sounds, or a `(min, max)` range.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_anger_level)
    """

    identifier = "minecraft:anger_level"

    anger_decrement_interval: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    angry_boost: Annotated[int, NonNegative] | None = json_field(default=None)
    angry_threshold: Annotated[int, NonNegative] | None = json_field(default=None)
    broadcast_anger: bool | None = json_field(default=None)
    broadcast_anger_on_attack: bool | None = json_field(default=None)
    broadcast_filters: Filter | None = json_field(default=None)
    broadcast_range: int | None = json_field(default=None)
    broadcast_targets: list[str] | None = json_field(default=None)
    calm_event: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    default_annoyingness: int | None = json_field(default=None)
    default_projectile_annoyingness: int | None = json_field(default=None)
    duration: int | None = json_field(default=None)
    duration_delta: int | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)
    max_anger: Annotated[int, NonNegative] | None = json_field(default=None)
    nuisance_filter: Filter | None = json_field(default=None)
    on_increase_sounds: list[AngerSound] = json_field(
        default_factory=list, omit_default=True
    )
    remove_targets_below_angry_threshold: bool | None = json_field(default=None)
    sound_interval: Annotated[int | tuple[int, int], RangeMinMax] | None = json_field(
        default=None
    )

    def add_on_increase_sound(
        self, *, sound: str, condition: Molang | str | None = None
    ) -> "EntityAngerLevel":
        """Adds a sound played when the entity is provoked.

        Args:
            sound (str): The sound to play.
            condition (Molang | str, optional): The condition under which the sound plays.
        """
        self.on_increase_sounds.append(AngerSound(sound=sound, condition=condition))
        return self


class EntityAngry(JsonComponent):
    """Defines an entity's 'angry' state using a timer.

    Args:
        angry_sound (str, optional): The sound event to play when the mob is angry.
        broadcast_anger (bool, optional): Other entities of the same type within `broadcast_range` also become angry. Game default false.
        broadcast_anger_on_attack (bool, optional): Broadcasts anger whenever this mob attacks. Game default false.
        broadcast_anger_on_being_attacked (bool, optional): Broadcasts anger whenever this mob is attacked. Game default false.
        broadcast_anger_when_dying (bool, optional): If false, this mob does not spread its anger when killed. Game default true.
        broadcast_filters (Filter, optional): Conditions for other entities to receive the anger.
        broadcast_range (int, optional): Distance in blocks within which anger is broadcast. Game default 20.
        broadcast_targets (list[str], optional): Entity families to broadcast anger to.
        calm_event (EventTrigger | str, optional): Event to run when this entity calms down.
        duration (int, optional): Seconds the entity stays angry. Game default 25.
        duration_delta (int, optional): Variance in seconds added to the duration. Game default 0.
        filters (Filter, optional): Mob types it should not attack while angry.
        sound_interval (int | tuple[float, float], optional): Seconds to wait before playing the sound again, or a `(min, max)` range. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_angry)
    """

    identifier = "minecraft:angry"

    angry_sound: str | None = json_field(default=None)
    broadcast_anger: bool | None = json_field(default=None)
    broadcast_anger_on_attack: bool | None = json_field(default=None)
    broadcast_anger_on_being_attacked: bool | None = json_field(default=None)
    broadcast_anger_when_dying: bool | None = json_field(default=None)
    broadcast_filters: Filter | None = json_field(default=None)
    broadcast_range: int | None = json_field(default=None)
    broadcast_targets: list[str] | None = json_field(default=None)
    calm_event: Annotated[EventTrigger | str, Trigger] | None = json_field(default=None)
    duration: int | None = json_field(default=None)
    duration_delta: int | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)
    sound_interval: Annotated[int | tuple[float, float], RangeMinMax] | None = (
        json_field(default=None)
    )


class EntityAnnotationBreakDoor(JsonComponent):
    """Allows an entity to break doors, assuming that that flags set up for the component to use in navigation. Requires the entity's `navigation` component to have the parameter `can_break_doors` set to `true`.

    Args:
        break_time (int, optional): The time in seconds required to break through doors. Game default 12.
        min_difficulty (Difficulty, optional): The minimum difficulty that the world must be on for this entity to break doors. Game default hard.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_annotation_break_door)
    """

    identifier = "minecraft:annotation.break_door"

    break_time: Annotated[int, NonNegative] | None = json_field(default=None)
    min_difficulty: Difficulty | None = json_field(default=None)


class EntityAnnotationOpenDoor(JsonComponent):
    """Allows the entity to open doors. Requires the entity's `navigation` component to have the parameter `can_open_doors` set to `true`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_annotation_open_door)
    """

    identifier = "minecraft:annotation.open_door"


class EntityApplyKnockbackRules(JsonComponent):
    """Defines how an entity applies knockback.

    Args:
        presets (list[KnockbackPreset], optional): The rules that define how knockback is applied. Add more with `add_preset`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_apply_knockback_rules)
    """

    identifier = "minecraft:apply_knockback_rules"

    presets: list[KnockbackPreset] = json_field(default_factory=list, omit_default=True)

    def add_preset(
        self,
        *,
        filter: Filter | None = None,
        horizontal_power: float | None = None,
        vertical_power: float | None = None,
        vertical_velocity_cap: float | None = None,
        slowdown_scale: float | None = None,
        knockback_mode: Literal["relative_horizontal", "hit_direction"] | None = None,
        scale_with_damage: bool | None = None,
        extra_knockback_approach: (
            Literal["reapply_default", "multiply", "multiply_reduced"] | None
        ) = None,
        check_if_target_is_immersed_in_water: bool | None = None,
    ) -> "EntityApplyKnockbackRules":
        """Adds a rule. See `KnockbackPreset` for the parameters."""
        self.presets.append(
            KnockbackPreset(
                filter=filter,
                horizontal_power=horizontal_power,
                vertical_power=vertical_power,
                vertical_velocity_cap=vertical_velocity_cap,
                slowdown_scale=slowdown_scale,
                knockback_mode=knockback_mode,
                scale_with_damage=scale_with_damage,
                extra_knockback_approach=extra_knockback_approach,
                check_if_target_is_immersed_in_water=check_if_target_is_immersed_in_water,
            )
        )
        return self


class EntityBlockSensor(JsonComponent):
    """Runs an event when a watched block is broken within the sensor range.

    Args:
        on_break (list[BlockBreakWatch], optional): The blocks to watch and the events to run. Add more with `add_on_break`.
        sensor_radius (float, optional): The radius in which a broken block is detected, at most 32. Game default 16.
        sources (Filter, optional): The sources of the block break to listen for. Without it, every break.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_block_sensor)
    """

    identifier = "minecraft:block_sensor"

    on_break: list[BlockBreakWatch] = json_field(
        default_factory=list, omit_default=True
    )
    sensor_radius: Annotated[float, InRange(0, 32)] | None = json_field(default=None)
    sources: Filter | None = json_field(default=None)

    def add_on_break(
        self, *, block_list: list[str | MinecraftBlockDescriptor], on_block_broken: str
    ) -> "EntityBlockSensor":
        """Adds blocks to watch.

        Args:
            block_list (list[str | MinecraftBlockDescriptor]): Blocks that trigger the event.
            on_block_broken (str): Event to run when one of them is broken.
        """
        self.on_break.append(
            BlockBreakWatch(block_list=block_list, on_block_broken=on_block_broken)
        )
        return self


class EntityBreakBlocks(JsonComponent):
    """Specifies the blocks that the entity can break as it moves around.

    Args:
        breakable_blocks (list[str | MinecraftBlockDescriptor], optional): The blocks that can be broken as this entity moves around. Add more with `add_breakable_blocks`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_break_blocks)
    """

    identifier = "minecraft:break_blocks"

    breakable_blocks: list[str | MinecraftBlockDescriptor] = json_field(
        default_factory=list, omit_default=True
    )

    def add_breakable_blocks(
        self, *blocks: str | MinecraftBlockDescriptor
    ) -> "EntityBreakBlocks":
        """Adds blocks the entity can break."""
        self.breakable_blocks.extend(blocks)
        return self


class EntityCanJoinRaid(JsonComponent):
    """Specifies if an entity can join a raid.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_join_raid)
    """

    identifier = "minecraft:can_join_raid"


class EntityCannotBeAttacked(JsonComponent):
    """When set, blocks entities from attacking the owner entity unless they have the "minecraft:ignore_cannot_be_attacked" component.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_cannot_be_attacked)
    """

    identifier = "minecraft:cannot_be_attacked"


class EntityCelebrateHunt(JsonComponent):
    """Specifies hunt celebration behaviour.

    Args:
        broadcast (bool, optional): Whether the celebration is broadcast to other entities in `radius`. Game default true.
        celeberation_targets (Filter, optional): Conditions the target of the hunt must meet to start the celebration. The game's key is spelled this way.
        celebrate_sound (str, optional): The sound event to play when the mob is celebrating.
        duration (int, optional): Seconds the celebration lasts. Game default 4.
        radius (float, optional): Radius in which other entities are notified. Game default 16.
        sound_interval (int | tuple[float, float], optional): Seconds to wait before playing the sound again, or a `(min, max)` range. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_celebrate_hunt)
    """

    identifier = "minecraft:celebrate_hunt"

    broadcast: bool | None = json_field(default=None)
    celeberation_targets: Filter | None = json_field(default=None)
    celebrate_sound: str | None = json_field(default=None)
    duration: Annotated[int, NonNegative] | None = json_field(default=None)
    radius: Annotated[float, NonNegative] | None = json_field(default=None)
    sound_interval: Annotated[int | tuple[float, float], RangeMinMax] | None = (
        json_field(default=None)
    )


class EntityDamageSensor(JsonComponent):
    """Defines what events to call when this entity is damaged by specific entities or items.

    Args:
        triggers (list[DamageSensorTrigger], optional): How the entity reacts to each kind of damage. Add more with `add_trigger`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_sensor)
    """

    identifier = "minecraft:damage_sensor"

    triggers: list[DamageSensorTrigger] = json_field(
        default_factory=list, omit_default=True
    )

    def add_trigger(
        self,
        *,
        cause: DamageCause | None = None,
        deals_damage: DamageSensor | bool | None = None,
        on_damage: EventTrigger | None = None,
        on_damage_sound_event: str | None = None,
        damage_modifier: float | None = None,
        damage_multiplier: float | None = None,
    ) -> "EntityDamageSensor":
        """Adds a reaction to a kind of damage. See `DamageSensorTrigger` for the parameters."""
        self.triggers.append(
            DamageSensorTrigger(
                cause=cause,
                deals_damage=deals_damage,
                on_damage=on_damage,
                on_damage_sound_event=on_damage_sound_event,
                damage_modifier=damage_modifier,
                damage_multiplier=damage_multiplier,
            )
        )
        return self


class EntityEnvironmentSensor(JsonComponent):
    """Creates a trigger based on environment conditions.

    Args:
        triggers (list[EventTrigger], optional): The triggers that fire when the environment conditions match their filters. Add more with `add_trigger`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_environment_sensor)
    """

    identifier = "minecraft:environment_sensor"

    triggers: list[EventTrigger] = json_field(default_factory=list, omit_default=True)

    def add_trigger(
        self,
        *,
        event: str,
        filters: Filter | None = None,
        target: FilterSubject | None = None,
    ) -> "EntityEnvironmentSensor":
        """Adds a trigger.

        Args:
            event (str): The event to run when the filters match.
            filters (Filter, optional): The environment conditions.
            target (FilterSubject, optional): The target of the event. Game default self.
        """
        self.triggers.append(EventTrigger(event=event, filters=filters, target=target))
        return self


class EntityExplode(JsonComponent):
    """Defines how the entity explodes.

    Args:
        allow_underwater (bool, optional): The explosion affects blocks and entities under water. Game default false.
        breaks_blocks (bool, optional): The explosion destroys blocks in its radius. Game default true.
        causes_fire (bool, optional): Blocks in the radius are set on fire. Game default false.
        damage_scaling (float, optional): Scale of the explosion's damage to entities. Game default 1.
        destroy_affected_by_griefing (bool, optional): The mob griefing game rule decides whether blocks break. Game default false.
        fire_affected_by_griefing (bool, optional): The mob griefing game rule decides whether fire is caused. Game default false.
        fuse_length (float | tuple[float, float], optional): Seconds the fuse burns, or a `(min, max)` range written as `[min, max]`. Negative explodes at once.
        fuse_lit (bool, optional): The fuse is lit when the component is added. Game default false.
        knockback_scaling (float, optional): Scale of the explosion's knockback. Game default 1.
        max_resistance (float, optional): Caps the explosion resistance of blocks. Game default 3.40282e+38.
        negates_fall_damage (bool, optional): Players above the explosion take no fall damage. Game default false.
        particle_effect (ExplosionParticleEffect, optional): The particle effect. Game default explosion.
        power (float, optional): Radius in blocks and damage of the explosion. Game default 3.
        sound_effect (str, optional): The sound played when the explosion happens. Game default explode.
        toggles_blocks (bool, optional): The explosion toggles blocks in its radius. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_explode)
    """

    identifier = "minecraft:explode"

    allow_underwater: bool | None = json_field(default=None)
    breaks_blocks: bool | None = json_field(default=None)
    causes_fire: bool | None = json_field(default=None)
    damage_scaling: float | None = json_field(default=None)
    destroy_affected_by_griefing: bool | None = json_field(default=None)
    fire_affected_by_griefing: bool | None = json_field(default=None)
    fuse_length: float | tuple[float, float] | None = json_field(default=None)
    fuse_lit: bool | None = json_field(default=None)
    knockback_scaling: float | None = json_field(default=None)
    max_resistance: float | None = json_field(default=None)
    negates_fall_damage: bool | None = json_field(default=None)
    particle_effect: ExplosionParticleEffect | None = json_field(default=None)
    power: Annotated[float, NonNegative] | None = json_field(default=None)
    sound_effect: str | None = json_field(default=None)
    toggles_blocks: bool | None = json_field(default=None)


class EntityGameEventMovementTracking(JsonComponent):
    """Allows an entity to emit `entityMove`, `swim` and `flap` game events, depending on the block the entity is moving through. It is added by default to every mob. Add it again to override its behavior.

    Args:
        emit_flap (bool, optional): If true, the `flap` game event will be emitted when the entity moves through air. Game default false.
        emit_move (bool, optional): If true, the `entityMove` game event will be emitted when the entity moves on ground or through a solid. Game default true.
        emit_swim (bool, optional): If true, the `swim` game event will be emitted when the entity moves through a liquid. Game default true.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_game_event_movement_tracking)
    """

    identifier = "minecraft:game_event_movement_tracking"

    emit_flap: bool | None = json_field(default=None)
    emit_move: bool | None = json_field(default=None)
    emit_swim: bool | None = json_field(default=None)


class EntityHurtOnCondition(JsonComponent):
    """Defines a set of conditions under which an entity should take damage.

    Args:
        damage_conditions (list[DamageCondition], optional): The conditions. Add more with `add_damage_condition`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_hurt_on_condition)
    """

    identifier = "minecraft:hurt_on_condition"

    damage_conditions: list[DamageCondition] = json_field(
        default_factory=list, omit_default=True
    )

    def add_damage_condition(
        self,
        *,
        cause: DamageCause | None = None,
        damage_per_tick: int | None = None,
        filters: Filter | None = None,
    ) -> "EntityHurtOnCondition":
        """Adds a condition. See `DamageCondition` for the parameters."""
        self.damage_conditions.append(
            DamageCondition(
                cause=cause, damage_per_tick=damage_per_tick, filters=filters
            )
        )
        return self


class EntityIgnoreCannotBeAttacked(JsonComponent):
    """Allows the owner entity to ignore the "minecraft:cannot_be_attacked" component on entities that fulfill the filter.

    Args:
        filters (Filter, optional): The entities this entity may attack. Without it, every entity.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ignore_cannot_be_attacked)
    """

    identifier = "minecraft:ignore_cannot_be_attacked"

    filters: Filter | None = json_field(default=None)


class EntityInsideBlockNotifier(JsonComponent):
    """Runs events when the entity enters or exits one of the listed blocks.

    Args:
        block_list (list[InsideBlockWatch], optional): The blocks to watch. Add more with `add_block`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inside_block_notifier)
    """

    identifier = "minecraft:inside_block_notifier"

    block_list: list[InsideBlockWatch] = json_field(
        default_factory=list, omit_default=True
    )

    def add_block(
        self,
        *,
        block: str | MinecraftBlockDescriptor,
        entered_block_event: EventTrigger | str | None = None,
        exited_block_event: EventTrigger | str | None = None,
    ) -> "EntityInsideBlockNotifier":
        """Adds a block to watch. See `InsideBlockWatch` for the parameters."""
        self.block_list.append(
            InsideBlockWatch(
                block=block,
                entered_block_event=entered_block_event,
                exited_block_event=exited_block_event,
            )
        )
        return self


class EntityLookedAt(JsonComponent):
    """Defines the behavior when another entity looks at the owner entity.

    Args:
        field_of_view (float, optional): Width in degrees of the field of view of entities looking at the owner. Game default 26.
        filters (Filter, optional): The entities considered when searching for entities looking at the owner.
        find_players_only (bool, optional): Searches only the nearest player that meets `filters`. Game default false.
        line_of_sight_obstruction_type (LineOfSightObstructionType, optional): Block shape used for line of sight checks. Game default collision.
        look_at_locations (list[LookAtLocation], optional): Locations on the owner towards which line of sight is checked.
        looked_at_cooldown (int | tuple[float, float], optional): Seconds before checking again after being looked at, or a `(min, max)` range.
        looked_at_event (EventTrigger | str, optional): Event to run when an entity looking at the owner is detected.
        min_looked_at_duration (float, optional): Seconds the owner must be looked at continuously. Game default 0.
        not_looked_at_event (EventTrigger | str, optional): Event to run when no entity is looking at the owner.
        scale_fov_by_distance (bool, optional): Narrows the field of view with distance. Game default true.
        search_radius (float, optional): Maximum distance searched. Game default 10.
        set_target (LootedAtSetTarget, optional): If and how the owner sets entities looking at it as its targets.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_looked_at)
    """

    identifier = "minecraft:looked_at"

    field_of_view: float | None = json_field(default=None)
    filters: Filter | None = json_field(default=None)
    find_players_only: bool | None = json_field(default=None)
    line_of_sight_obstruction_type: LineOfSightObstructionType | None = json_field(
        default=None
    )
    look_at_locations: list[LookAtLocation] | None = json_field(default=None)
    looked_at_cooldown: Annotated[int | tuple[float, float], RangeMinMax] | None = (
        json_field(default=None)
    )
    looked_at_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    min_looked_at_duration: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    not_looked_at_event: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    scale_fov_by_distance: bool | None = json_field(default=None)
    search_radius: Annotated[float, NonNegative] | None = json_field(default=None)
    set_target: LootedAtSetTarget | None = json_field(default=None)


class EntityMobEffect(JsonComponent):
    """Applies a mob effect to entities that get within range.

    Args:
        mob_effect (MinecraftEffects | str): The effect applied to entities in range.
        entity_filter (Filter, optional): The entities the effect can be applied to.
        ambient (bool, optional): Renders the effect with the ambient background. Game default false.
        cooldown_time (int, optional): Seconds between applications. Game default 0.
        effect_range (float, optional): How close an entity must be. Game default 0.2.
        effect_time (int | Literal["infinite"], optional): Seconds the effect lasts. Game default 10.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mob_effect)
    """

    identifier = "minecraft:mob_effect"

    mob_effect: MinecraftEffects | str = json_field()
    entity_filter: Filter | None = json_field(default=None)
    ambient: bool | None = json_field(default=None)
    cooldown_time: Annotated[int, NonNegative] | None = json_field(default=None)
    effect_range: Annotated[float, NonNegative] | None = json_field(default=None)
    effect_time: int | Literal["infinite"] | None = json_field(default=None)


class EntityMobEffectImmunity(JsonComponent):
    """Entities with this component will have an immunity to the provided mob effects.

    Args:
        mob_effects (list[MinecraftEffects | str], optional): The effects the entity is immune to. Add more with `add_mob_effects`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mob_effect_immunity)
    """

    identifier = "minecraft:mob_effect_immunity"

    mob_effects: list[MinecraftEffects | str] = json_field(
        default_factory=list, omit_default=True
    )

    def add_mob_effects(
        self, *effects: MinecraftEffects | str
    ) -> "EntityMobEffectImmunity":
        """Adds effects the entity is immune to."""
        self.mob_effects.extend(effects)
        return self


class EntityOnDeath(EntityEventTrigger):
    """Adds a trigger to call on this entity's death.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_death)
    """

    identifier = "minecraft:on_death"


class EntityOnEquipmentChanged(JsonComponent):
    """Runs events when equipment is set in the entity's default equipment slots. Doesn't apply to "minecraft:inventory", use "minecraft:equippable" instead. When equipment changes, only the first matching slot entry is used.

    Args:
        slots (list[EquipmentChangeSlot], optional): The slots to watch and their events. Add more with `add_slot`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_equipment_changed)
    """

    identifier = "minecraft:on_equipment_changed"

    slots: Annotated[list[EquipmentChangeSlot], Unique("slot")] = json_field(
        default_factory=list, omit_default=True
    )

    def add_slot(
        self,
        *,
        slot: Slots | None = None,
        on_equip: str | None = None,
        on_unequip: str | None = None,
    ) -> "EntityOnEquipmentChanged":
        """Adds a slot to watch.

        Args:
            slot (Slots, optional): The equipment slot to watch. Game default slot.weapon.mainhand.
            on_equip (str, optional): Event to run when a non-empty item is placed in the slot.
            on_unequip (str, optional): Event to run when the slot is cleared.
        """
        self.slots.append(
            EquipmentChangeSlot(slot=slot, on_equip=on_equip, on_unequip=on_unequip)
        )
        return self


class EntityOnFriendlyAnger(EntityEventTrigger):
    """Adds a trigger that will run when a nearby entity of the same type as this entity becomes Angry.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_friendly_anger)
    """

    identifier = "minecraft:on_friendly_anger"


class EntityOnHurt(EntityEventTrigger):
    """Adds a trigger to call when this entity takes damage.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_hurt)
    """

    identifier = "minecraft:on_hurt"


class EntityOnHurtByPlayer(EntityEventTrigger):
    """Adds a trigger to call when this entity is attacked by the player.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_hurt_by_player)
    """

    identifier = "minecraft:on_hurt_by_player"


class EntityOnIgnite(EntityEventTrigger):
    """Adds a trigger to call when this entity is set on fire.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_ignite)
    """

    identifier = "minecraft:on_ignite"


class EntityOnStartLanding(EntityEventTrigger):
    """Only usable by the Ender Dragon. Adds a trigger to call when this entity lands.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_start_landing)
    """

    identifier = "minecraft:on_start_landing"


class EntityOnStartTakeoff(EntityEventTrigger):
    """Only usable by the Ender Dragon. Adds a trigger to call when this entity starts flying.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_start_takeoff)
    """

    identifier = "minecraft:on_start_takeoff"


class EntityOnTargetAcquired(EntityEventTrigger):
    """Adds a trigger to call when this entity finds a target.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_target_acquired)
    """

    identifier = "minecraft:on_target_acquired"


class EntityOnTargetEscape(EntityEventTrigger):
    """Adds a trigger to call when this entity loses the target it currently has.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_target_escape)
    """

    identifier = "minecraft:on_target_escape"


class EntityOnWakeWithOwner(EntityEventTrigger):
    """A trigger when a mob's tamed onwer wakes up.

    Args:
        event (str): The event to run when the conditions for this trigger are met.
        filters (Filter, optional): The conditions for this trigger to run.
        target (FilterSubject, optional): The target of the event. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_wake_with_owner)
    """

    identifier = "minecraft:on_wake_with_owner"


class EntityProjectile(JsonComponent):
    """Turns the entity into a projectile.

    Args:
        anchor (int | Literal["origin", "eye_height", "middle"], optional): Point of the shooter the projectile spawns from: 0 origin, 1 eye height, 2 middle. Game default origin.
        angle_offset (float, optional): Extra upward pitch in degrees at launch. Game default 0.
        catch_fire (bool, optional): Sets the entity hit on fire. Game default false.
        crit_particle_on_hurt (bool, optional): Spawns critical-hit particles when the projectile is struck. Game default false.
        destroy_on_hurt (bool, optional): Removes the projectile when it is struck. Game default false.
        gravity (float, optional): Downward acceleration per tick. Game default 0.05.
        hit_ground_sound (str, optional): Sound played when hitting a block. Defaults to `hit_sound`.
        hit_nearest_passenger (bool, optional): Hits the passenger nearest the impact instead of the vehicle. Game default false.
        hit_sound (str, optional): Sound played when hitting an entity.
        hit_water (bool, optional): Water stops the projectile. Game default false.
        homing (bool, optional): The projectile steers towards its target. Game default false.
        ignored_entities (list[MinecraftEntityDescriptor | str], optional): Entities the projectile passes through.
        inertia (float, optional): Fraction of velocity kept each tick in air. Game default 0.99.
        is_dangerous (bool, optional): Marks the projectile as dangerous to AI. Game default false.
        isolated_physics (bool, optional): Outside forces such as friction do not affect the projectile. Game default true.
        lightning (bool, optional): Channels lightning on the entity hit during a thunderstorm. Game default false.
        liquid_inertia (float, optional): Fraction of velocity kept each tick in fluid. Game default 0.6.
        multiple_targets (bool, optional): The projectile can hit more than one entity. Game default false.
        offset (tuple[float, float, float], optional): Spawn offset from the anchor. Game default (0, 0, 0).
        on_fire_time (float, optional): Seconds an entity set on fire burns. Game default 5.
        on_hit (ProjectileOnHit, optional): What happens when the projectile hits. Set it with `set_on_hit`.
        owner_launch_immunity_ticks (int, optional): Ticks after launch during which the projectile cannot hit its shooter. Game default 5.
        particle (str, optional): Particle emitted at the impact. Game default iconcrack.
        potion_effect (int, optional): Potion aux value of the projectile. Game default -1.
        power (float, optional): Launch speed in blocks per tick. Game default 1.3.
        reflect_immunity (float, optional): Seconds after launch during which the projectile cannot be reflected. Game default 0.
        reflect_on_hurt (bool, optional): The projectile is reflected when struck. Game default false.
        shoot_sound (str, optional): Sound played when the projectile is fired.
        shoot_target (bool, optional): The projectile is aimed at the shooter's target. Game default true.
        should_bounce (Literal["no", "if_invulnerable", "if_no_damage_dealt"], optional): Whether the projectile bounces off entities. Game default no.
        splash_range (float, optional): Splash radius in blocks of potion effects. Game default 4.
        spread_fire (bool, optional): A burning projectile sets the entity hit on fire. Game default true.
        stop_on_hurt (bool, optional): The projectile stops when struck. Game default false.
        uncertainty_base (float, optional): Base inaccuracy of the launch direction. Game default 0.
        uncertainty_multiplier (float, optional): Inaccuracy removed per difficulty level. Game default 0.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_projectile)
    """

    identifier = "minecraft:projectile"

    anchor: (
        Annotated[Literal[0, 1, 2], IndexInto(("origin", "eye_height", "middle"))]
        | Literal["origin", "eye_height", "middle"]
        | None
    ) = json_field(default=None)
    angle_offset: float | None = json_field(default=None)
    catch_fire: bool | None = json_field(default=None)
    crit_particle_on_hurt: bool | None = json_field(default=None)
    destroy_on_hurt: bool | None = json_field(default=None)
    gravity: float | None = json_field(default=None)
    hit_ground_sound: str | None = json_field(default=None)
    hit_nearest_passenger: bool | None = json_field(default=None)
    hit_sound: str | None = json_field(default=None)
    hit_water: bool | None = json_field(default=None)
    homing: bool | None = json_field(default=None)
    ignored_entities: list[MinecraftEntityDescriptor | str] | None = json_field(
        default=None
    )
    inertia: float | None = json_field(default=None)
    is_dangerous: bool | None = json_field(default=None)
    isolated_physics: bool | None = json_field(default=None)
    lightning: bool | None = json_field(default=None)
    liquid_inertia: float | None = json_field(default=None)
    multiple_targets: bool | None = json_field(default=None)
    offset: tuple[float, float, float] | None = json_field(default=None)
    on_fire_time: Annotated[float, NonNegative] | None = json_field(default=None)
    on_hit: ProjectileOnHit | None = json_field(default=None)
    owner_launch_immunity_ticks: int | None = json_field(default=None)
    particle: str | None = json_field(default=None)
    potion_effect: int | None = json_field(default=None)
    power: float | None = json_field(default=None)
    reflect_immunity: Annotated[float, NonNegative] | None = json_field(default=None)
    reflect_on_hurt: bool | None = json_field(default=None)
    shoot_sound: str | None = json_field(default=None)
    shoot_target: bool | None = json_field(default=None)
    should_bounce: Literal["no", "if_invulnerable", "if_no_damage_dealt"] | None = (
        json_field(default=None)
    )
    splash_range: Annotated[float, NonNegative] | None = json_field(default=None)
    spread_fire: bool | None = json_field(default=None)
    stop_on_hurt: bool | None = json_field(default=None)
    uncertainty_base: float | None = json_field(default=None)
    uncertainty_multiplier: float | None = json_field(default=None)

    def set_on_hit(
        self,
        *,
        arrow_effect: ProjectileArrowEffect | None = None,
        catch_fire: ProjectileCatchFire | None = None,
        definition_event: ProjectileDefinitionEvent | None = None,
        douse_fire: bool | None = None,
        freeze_on_hit: ProjectileFreezeOnHit | None = None,
        grant_xp: int | tuple[float, float] | None = None,
        hurt_owner: ProjectileHurtOwner | None = None,
        ignite: bool | None = None,
        impact_damage: ProjectileImpactDamage | None = None,
        mob_effect: list[ProjectileMobEffect] | None = None,
        particle_on_hit: ProjectileParticleOnHit | None = None,
        remove_on_hit: bool | None = None,
        spawn_aoe_cloud: ProjectileSpawnAoeCloud | None = None,
        spawn_chance: ProjectileSpawnChance | None = None,
        stick_in_ground: ProjectileStickInGround | None = None,
        teleport_owner: bool | None = None,
        thrown_potion_effect: ProjectileThrownPotionEffect | None = None,
        wind_burst_on_hit: bool | None = None,
    ) -> "EntityProjectile":
        """Sets what happens when the projectile hits. See `ProjectileOnHit` for the parameters."""
        self.on_hit = ProjectileOnHit(
            arrow_effect=arrow_effect,
            catch_fire=catch_fire,
            definition_event=definition_event,
            douse_fire=douse_fire,
            freeze_on_hit=freeze_on_hit,
            grant_xp=grant_xp,
            hurt_owner=hurt_owner,
            ignite=ignite,
            impact_damage=impact_damage,
            mob_effect=mob_effect,
            particle_on_hit=particle_on_hit,
            remove_on_hit=remove_on_hit,
            spawn_aoe_cloud=spawn_aoe_cloud,
            spawn_chance=spawn_chance,
            stick_in_ground=stick_in_ground,
            teleport_owner=teleport_owner,
            thrown_potion_effect=thrown_potion_effect,
            wind_burst_on_hit=wind_burst_on_hit,
        )
        return self


class EntityRaidTrigger(JsonComponent):
    """Attempts to trigger a raid at the entity's location.

    Args:
        triggered_event (EventTrigger, optional): Event to run when a raid is triggered on the village.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_raid_trigger)
    """

    identifier = "minecraft:raid_trigger"

    triggered_event: EventTrigger | None = json_field(default=None)


class EntityRailSensor(JsonComponent):
    """Defines the behavior of the entity when the rail gets activated or deactivated.

    Args:
        check_block_types (bool, optional): On tick, the entity runs its `on_deactivate` behavior. Game default false.
        eject_on_activate (bool, optional): Ejects all riders on an activated rail. Game default true.
        eject_on_deactivate (bool, optional): Ejects all riders on a deactivated rail. Game default false.
        on_activate (EventTrigger | str, optional): Event to run when the rail is activated.
        on_deactivate (EventTrigger | str, optional): Event to run when the rail is deactivated.
        tick_command_block_on_activate (bool, optional): Command blocks tick on an activated rail. Game default true.
        tick_command_block_on_deactivate (bool, optional): If false, command blocks stop ticking on a deactivated rail. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rail_sensor)
    """

    identifier = "minecraft:rail_sensor"

    check_block_types: bool | None = json_field(default=None)
    eject_on_activate: bool | None = json_field(default=None)
    eject_on_deactivate: bool | None = json_field(default=None)
    on_activate: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    on_deactivate: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    tick_command_block_on_activate: bool | None = json_field(default=None)
    tick_command_block_on_deactivate: bool | None = json_field(default=None)


class EntityRavagerBlocked(JsonComponent):
    """Defines the ravager's response to its melee attack being blocked.

    Args:
        knockback_strength (float, optional): Strength with which blocking entities are knocked back. Game default 3.
        reaction_choices (list[RavagerReaction], optional): Weighted responses. Add more with `add_reaction_choice`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ravager_blocked)
    """

    identifier = "minecraft:ravager_blocked"

    knockback_strength: Annotated[float, NonNegative] | None = json_field(default=None)
    reaction_choices: list[RavagerReaction] = json_field(
        default_factory=list, omit_default=True
    )

    def add_reaction_choice(
        self, *, weight: int, value: EventTrigger | str | None = None
    ) -> "EntityRavagerBlocked":
        """Adds a weighted response. See `RavagerReaction`."""
        self.reaction_choices.append(RavagerReaction(weight=weight, value=value))
        return self


class EntityRemoveInPeaceful(JsonComponent):
    """Denotes entities that are not allowed to exist in "Peaceful" difficulty.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_remove_in_peaceful)
    """

    identifier = "minecraft:remove_in_peaceful"


class EntityScheduler(JsonComponent):
    """Runs scheduled events at time of day events.

    Args:
        scheduled_events (list[EventTrigger], optional): The events and the conditions they run on. Add more with `add_scheduled_event`.
        max_delay_secs (float, optional): Maximum delay in seconds.
        min_delay_secs (float, optional): Minimum delay in seconds.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scheduler)
    """

    identifier = "minecraft:scheduler"

    scheduled_events: list[EventTrigger] = json_field(
        default_factory=list, omit_default=True
    )
    max_delay_secs: Annotated[float, NonNegative] | None = json_field(default=None)
    min_delay_secs: Annotated[float, NonNegative] | None = json_field(default=None)

    def add_scheduled_event(
        self,
        *,
        event: str,
        filters: Filter | None = None,
        target: FilterSubject | None = None,
    ) -> "EntityScheduler":
        """Adds a scheduled event. See `EventTrigger` for the parameters."""
        self.scheduled_events.append(
            EventTrigger(event=event, filters=filters, target=target)
        )
        return self


class EntitySensor(JsonComponent):
    """Owns subsensors, each running an event when other entities in range meet its conditions.

    Args:
        find_players_only (bool, optional): Searches only players, for every subsensor. Game default false.
        relative_range (bool, optional): Adds the entity's size to the subsensors' range. Game default true.
        subsensors (list[Subsensor], optional): The subsensors. Add more with `add_subsensor`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_sensor)
    """

    identifier = "minecraft:entity_sensor"

    find_players_only: bool | None = json_field(default=None)
    relative_range: bool | None = json_field(default=None)
    subsensors: list[Subsensor] = json_field(default_factory=list, omit_default=True)

    def add_subsensor(
        self,
        *,
        event: str,
        event_filters: Filter | None = None,
        cooldown: float | None = None,
        maximum_count: int | None = None,
        minimum_count: int | None = None,
        range: tuple[float, float] | None = None,
        require_all: bool | None = None,
        y_offset: float | None = None,
    ) -> "EntitySensor":
        """Adds a subsensor. See `Subsensor` for the parameters."""
        self.subsensors.append(
            Subsensor(
                event=event,
                event_filters=event_filters,
                cooldown=cooldown,
                maximum_count=maximum_count,
                minimum_count=minimum_count,
                range=range,
                require_all=require_all,
                y_offset=y_offset,
            )
        )
        return self


class EntityShooter(JsonComponent):
    """Defines the entity's ranged attack behavior, used by `minecraft:behavior.ranged_attack`.

    Args:
        def_ (MinecraftEntityDescriptor | str, optional): The default projectile entity. Written as `def`.
        aux_val (int, optional): ID of the potion effect applied by the default projectile. Game default -1.
        magic (bool, optional): Flags the projectiles as magic. Game default false.
        power (float, optional): Velocity of the projectiles; 0 uses the projectile's default. Game default 0.
        projectiles (list[ShooterProjectile], optional): Projectiles with conditions; the first match is used. Add more with `add_projectile`.
        sound (str, optional): Sound played when shooting.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_shooter)
    """

    identifier = "minecraft:shooter"

    def_: MinecraftEntityDescriptor | str | None = json_field(default=None, key="def")
    aux_val: int | None = json_field(default=None)
    magic: bool | None = json_field(default=None)
    power: Annotated[float, NonNegative] | None = json_field(default=None)
    projectiles: list[ShooterProjectile] = json_field(
        default_factory=list, omit_default=True
    )
    sound: str | None = json_field(default=None)

    def add_projectile(
        self,
        *,
        def_: MinecraftEntityDescriptor | str,
        aux_val: int | None = None,
        filters: Filter | None = None,
        lose_target: bool | None = None,
    ) -> "EntityShooter":
        """Adds a projectile. See `ShooterProjectile` for the parameters."""
        self.projectiles.append(
            ShooterProjectile(
                def_=def_, aux_val=aux_val, filters=filters, lose_target=lose_target
            )
        )
        return self


class EntitySpawnEntity(JsonComponent):
    """Spawns other entities or items on a timer, like chickens laying eggs.

    Args:
        entities (list[SpawnedEntity], optional): What to spawn. Add more with `add_entity`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spawn_entity)
    """

    identifier = "minecraft:spawn_entity"

    entities: list[SpawnedEntity] = json_field(default_factory=list, omit_default=True)

    def add_entity(
        self,
        *,
        spawn_entity: MinecraftEntityDescriptor | str | None = None,
        spawn_item: str | MinecraftItemDescriptor | None = None,
        spawn_event: EventTrigger | str | None = None,
        spawn_item_event: EventTrigger | str | None = None,
        spawn_method: str | None = None,
        spawn_sound: str | None = None,
        filters: Filter | None = None,
        max_wait_time: int | None = None,
        min_wait_time: int | None = None,
        num_to_spawn: int | None = None,
        should_leash: bool | None = None,
        single_use: bool | None = None,
    ) -> "EntitySpawnEntity":
        """Adds an entity or item to spawn. See `SpawnedEntity` for the parameters."""
        self.entities.append(
            SpawnedEntity(
                spawn_entity=spawn_entity,
                spawn_item=spawn_item,
                spawn_event=spawn_event,
                spawn_item_event=spawn_item_event,
                spawn_method=spawn_method,
                spawn_sound=spawn_sound,
                filters=filters,
                max_wait_time=max_wait_time,
                min_wait_time=min_wait_time,
                num_to_spawn=num_to_spawn,
                should_leash=should_leash,
                single_use=single_use,
            )
        )
        return self


class EntitySpawnOnDeath(JsonComponent):
    """Spawns entities when the entity dies.

    Args:
        entity_to_spawn (MinecraftEntityDescriptor | str, optional): The entity to spawn. Game default the entity itself.
        additional_spawn_range (tuple[float, float], optional): A `(min, max)` range of extra entities to spawn. Game default (0, 0).
        filters (Filter, optional): Conditions for the entities to spawn.
        inherit_parent_name (bool, optional): Whether spawned entities take the name of the parent. Game default true.
        spawn_amount (int, optional): How many entities to spawn. Game default 1.
        spawn_method (Literal["born", "spawned", "summoned"], optional): The spawn method. Game default spawned.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spawn_on_death)
    """

    identifier = "minecraft:spawn_on_death"

    entity_to_spawn: MinecraftEntityDescriptor | str | None = json_field(default=None)
    additional_spawn_range: Annotated[tuple[float, float], MinMax] | None = json_field(
        default=None
    )
    filters: Filter | None = json_field(default=None)
    inherit_parent_name: bool | None = json_field(default=None)
    spawn_amount: Annotated[int, AtLeastOne] | None = json_field(default=None)
    spawn_method: Literal["born", "spawned", "summoned"] | None = json_field(
        default=None
    )


class EntitySpellEffects(JsonComponent):
    """Adds or removes status effects on the entity once, when the component is added.

    Args:
        add_effects (list[SpellEffect], optional): Effects to add. Add more with `add_effect`.
        remove_effects (list[MinecraftEffects | str], optional): Effects to remove.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spell_effects)
    """

    identifier = "minecraft:spell_effects"

    add_effects: list[SpellEffect] = json_field(default_factory=list, omit_default=True)
    remove_effects: list[Annotated[MinecraftEffects | str, EffectName]] | None = (
        json_field(default=None)
    )

    def add_effect(
        self,
        *,
        effect: MinecraftEffects | str,
        duration: int | Literal["infinite"] | None = None,
        amplifier: int | None = None,
        ambient: bool | None = None,
        visible: bool | None = None,
        display_on_screen_animation: bool | None = None,
    ) -> "EntitySpellEffects":
        """Adds an effect. See `SpellEffect` for the parameters."""
        self.add_effects.append(
            SpellEffect(
                effect=effect,
                duration=duration,
                amplifier=amplifier,
                ambient=ambient,
                visible=visible,
                display_on_screen_animation=display_on_screen_animation,
            )
        )
        return self


class EntitySuspectTracking(JsonComponent):
    """Allows this entity to remember suspicious locations.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_suspect_tracking)
    """

    identifier = "minecraft:suspect_tracking"


class EntityTargetNearbySensor(JsonComponent):
    """Defines the range within which the entity can see or sense other entities to target them.

    Args:
        inside_range (float, optional): Maximum distance of the 'inside' range. Game default 1.
        outside_range (float, optional): Maximum distance of the 'outside' range. Game default 5.
        must_see (bool, optional): Whether the other entity must be visible for 'inside' events. Game default false.
        on_inside_range (EventTrigger | str, optional): Event to run when an entity gets in the inside range.
        on_outside_range (EventTrigger | str, optional): Event to run when an entity gets outside the outside range.
        on_vision_lost_inside_range (EventTrigger | str, optional): Event to run when an entity exits visual range.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_target_nearby_sensor)
    """

    identifier = "minecraft:target_nearby_sensor"

    inside_range: Annotated[float, NonNegative] | None = json_field(default=None)
    outside_range: Annotated[float, NonNegative] | None = json_field(default=None)
    must_see: bool | None = json_field(default=None)
    on_inside_range: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    on_outside_range: Annotated[EventTrigger | str, Trigger] | None = json_field(
        default=None
    )
    on_vision_lost_inside_range: Annotated[EventTrigger | str, Trigger] | None = (
        json_field(default=None)
    )


class EntityTeleport(JsonComponent):
    """Defines an entity's teleporting behavior.

    Args:
        dark_teleport_chance (float, optional): Chance to teleport in darkness. Game default 0.01.
        light_teleport_chance (float, optional): Chance to teleport in daylight. Game default 0.01.
        max_random_teleport_time (float, optional): Maximum seconds between random teleports. Game default 20.
        min_random_teleport_time (float, optional): Minimum seconds between random teleports. Game default 0.
        projectile_filter (Filter, optional): Projectiles that make the entity try to teleport. Without it, every projectile.
        random_teleport_cube (tuple[float, float, float], optional): The area of random teleports. Game default (32, 16, 32).
        random_teleports (bool, optional): Whether the entity teleports randomly. Game default true.
        target_distance (float, optional): Maximum teleport distance when chasing a target. Game default 16.
        target_teleport_chance (float, optional): Chance to teleport, from 0 to 1. Game default 1.
        teleports_on_projectile_hit (bool, optional): Whether the entity teleports away from projectiles about to hit it. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_teleport)
    """

    identifier = "minecraft:teleport"

    dark_teleport_chance: Annotated[float, Chance] | None = json_field(default=None)
    light_teleport_chance: Annotated[float, Chance] | None = json_field(default=None)
    max_random_teleport_time: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    min_random_teleport_time: Annotated[float, NonNegative] | None = json_field(
        default=None
    )
    projectile_filter: Filter | None = json_field(default=None)
    random_teleport_cube: tuple[float, float, float] | None = json_field(default=None)
    random_teleports: bool | None = json_field(default=None)
    target_distance: Annotated[float, NonNegative] | None = json_field(default=None)
    target_teleport_chance: Annotated[float, Chance] | None = json_field(default=None)
    teleports_on_projectile_hit: bool | None = json_field(default=None)


class EntityTickWorld(JsonComponent):
    """Defines if the entity ticks the world and the radius around it to tick.

    Args:
        distance_to_players (float, optional): The distance at which the closest player has to be before this entity despawns. This option will be ignored if never_despawn is true. Game default 128.
        never_despawn (bool, optional): If true, this entity will not despawn even if players are far away. If false, distance_to_players will be used to determine when to despawn. Game default true.
        radius (int, optional): The area around the entity to tick. Game default 2.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tick_world)
    """

    identifier = "minecraft:tick_world"

    distance_to_players: Annotated[float, InRange(128.0, None)] | None = json_field(
        default=None
    )
    never_despawn: bool | None = json_field(default=None)
    radius: Annotated[int, InRange(2.0, 6.0)] | None = json_field(default=None)


class EntityTimer(JsonComponent):
    """Adds a timer after which an event runs.

    Args:
        time_down_event (EventTrigger | str): Event to run when the time runs out.
        looping (bool, optional): Whether the timer restarts after it fires. Game default true.
        randomInterval (bool, optional): Whether the time is random between the `time` range. Game default true.
        time (float | tuple[float, float], optional): Seconds of the timer, or a `(min, max)` range. Incompatible with `random_time_choices`.
        random_time_choices (list[TimeChoice], optional): Weighted times to pick from. Incompatible with `time`. Add more with `add_random_time_choice`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_timer)
    """

    identifier = "minecraft:timer"

    time_down_event: Annotated[EventTrigger | str, Trigger] = json_field()
    looping: bool | None = json_field(default=None)
    randomInterval: bool | None = json_field(default=None)
    time: float | tuple[float, float] | None = json_field(default=None)
    random_time_choices: list[TimeChoice] | None = json_field(default=None)

    def __validate__(self) -> None:
        if self.time is not None and self.random_time_choices is not None:
            raise ValueError(
                "EntityTimer takes `time` or `random_time_choices`, not both."
            )

    def add_random_time_choice(
        self,
        *,
        value: float,
        weight: int | None = None,
    ) -> "EntityTimer":
        """Adds a weighted time to pick from. See `TimeChoice` for the parameters."""
        if self.random_time_choices is None:
            self.random_time_choices = []
        self.random_time_choices.append(
            TimeChoice(
                value=value,
                weight=weight,
            )
        )
        return self


class EntityTrail(JsonComponent):
    """Makes the entity leave a trail of blocks as it moves. Obeys Mob Griefing rules.

    Args:
        block_type (str | MinecraftBlockDescriptor, optional): The block spawned behind the entity. Game default air.
        force_replace_matched_blocks (bool, optional): Replaces matching blocks even where placement rules prevent it. Game default false.
        radius (int, optional): Spawns blocks over a (2 * radius + 1) square around the offset. Game default -1.
        replaceable_blocks (list[str | MinecraftBlockDescriptor], optional): Blocks the trail may replace. Game default air only.
        spawn_filter (Filter, optional): Conditions for the block to spawn.
        spawn_offset (tuple[float, float, float], optional): Offset from the entity where the block spawns, at most 16 blocks. Game default (0, 0, 0).

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trail)
    """

    identifier = "minecraft:trail"

    block_type: str | MinecraftBlockDescriptor | None = json_field(default=None)
    force_replace_matched_blocks: bool | None = json_field(default=None)
    radius: int | None = json_field(default=None)
    replaceable_blocks: list[str | MinecraftBlockDescriptor] | None = json_field(
        default=None
    )
    spawn_filter: Filter | None = json_field(default=None)
    spawn_offset: tuple[float, float, float] | None = json_field(default=None)


class EntityTransformation(JsonComponent):
    """Transforms the entity into another entity.

    Args:
        into (MinecraftEntityDescriptor | str): The entity to transform into. Add an event to run on it as `"namespace:name<event>"`.
        add (list[str], optional): Component groups added after the transformation. Add more with `add_component_groups`.
        begin_transform_sound (str, optional): Sound played when the transformation starts.
        delay (float | TransformationDelay, optional): Seconds before the entity transforms, or the full delay options. Set it with `set_delay`.
        drop_equipment (bool, optional): The entity drops its equipment. Game default false.
        drop_inventory (bool, optional): The entity drops its inventory. Game default false.
        keep_level (bool, optional): A trader keeps its level. Game default false.
        keep_owner (bool, optional): An owned entity stays owned. Game default false.
        preserve_equipment (bool, optional): The entity keeps its equipment. Game default false.
        transformation_sound (str, optional): Sound played when the transformation is done.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transformation)
    """

    identifier = "minecraft:transformation"

    into: MinecraftEntityDescriptor | str = json_field()
    add: Annotated[list[str], Wrapped("component_groups")] = json_field(
        default_factory=list, omit_default=True
    )
    begin_transform_sound: str | None = json_field(default=None)
    delay: float | TransformationDelay | None = json_field(default=None)
    drop_equipment: bool | None = json_field(default=None)
    drop_inventory: bool | None = json_field(default=None)
    keep_level: bool | None = json_field(default=None)
    keep_owner: bool | None = json_field(default=None)
    preserve_equipment: bool | None = json_field(default=None)
    transformation_sound: str | None = json_field(default=None)

    def add_component_groups(self, *component_groups: str) -> "EntityTransformation":
        """Adds component groups added after the transformation."""
        self.add.extend(component_groups)
        return self

    def set_delay(
        self,
        *,
        value: float | None = None,
        range_min: float | None = None,
        range_max: float | None = None,
        block_assist_chance: float | None = None,
        block_chance: float | None = None,
        block_max: int | None = None,
        block_radius: int | None = None,
        block_types: list[str | MinecraftBlockDescriptor] | None = None,
    ) -> "EntityTransformation":
        """Sets the full delay options before the entity transforms. See `TransformationDelay` for the parameters."""
        self.delay = TransformationDelay(
            value=value,
            range_min=range_min,
            range_max=range_max,
            block_assist_chance=block_assist_chance,
            block_chance=block_chance,
            block_max=block_max,
            block_radius=block_radius,
            block_types=block_types,
        )
        return self


class EntityVibrationDamper(JsonComponent):
    """Vibrations emitted by an entity with this component will be ignored.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vibration_damper)
    """

    identifier = "minecraft:vibration_damper"


class EntityVibrationListener(JsonComponent):
    """Allows the entity to listen to vibration events. This is a largely-internal component, that is only supported on the Warden and Allay mobs.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vibration_listener)
    """

    identifier = "minecraft:vibration_listener"


# endregion
