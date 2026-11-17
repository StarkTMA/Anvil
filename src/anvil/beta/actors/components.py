from typing import Annotated, Literal

from anvil.api.actors.components.combat import EntityProjectile as _EntityProjectile
from anvil.api.actors.components.combat import EntityTeleport as _EntityTeleport
from anvil.api.actors.components.combat import EntityTrail as _EntityTrail
from anvil.api.actors.components.combat import (
    ProjectileArrowEffect,
    ProjectileCatchFire,
    ProjectileDefinitionEvent,
    ProjectileFreezeOnHit,
    ProjectileHurtOwner,
)
from anvil.api.actors.components.combat import (
    ProjectileImpactDamage as _ProjectileImpactDamage,
)
from anvil.api.actors.components.combat import (
    ProjectileMobEffect,
    ProjectileOnHit,
    ProjectileParticleOnHit,
    ProjectileSpawnAoeCloud,
    ProjectileSpawnChance,
    ProjectileStickInGround,
    ProjectileThrownPotionEffect,
)
from anvil.api.actors.entity import Entity
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.core.components import EventTrigger
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import (
    BlockId,
    EntityId,
    ExactMinMax,
    InRange,
    JsonComponent,
    JsonObject,
    Length,
    json_field,
)
from anvil.lib.jsonmodel.enums import FilterSubject


class TimeMarkerSensorTrigger(JsonObject):
    """A world clock time marker `minecraft:time_marker_sensor` listens for, and the event it runs.

    Args:
        clock (str): The name of the world clock to listen to.
        time_marker (str): The name of the time marker on the clock to listen for.
        on_time_marker (EventTrigger): Event to run when the time marker fires, with its conditions and target.
    """

    clock: str = json_field()
    time_marker: str = json_field()
    on_time_marker: EventTrigger = json_field()


class ProjectileImpactDamage(_ProjectileImpactDamage):
    """[EXPERIMENTAL] Damages the entity hit, with the 1.26.70 options.
    Needs the experimental flag in anvilconfig.json.

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
        scale_damage_with_difficulty (bool, optional): Whether impact damage dealt to players by mob-fired projectiles scales with the world difficulty. Entity format 1.26.70 and later; earlier formats never scale it. Game default true.
        set_last_hurt_requires_damage (bool, optional): The projectile counts as the last attacker only when it deals damage. Game default true.
    """

    scale_damage_with_difficulty: bool | None = json_field(default=None)

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "ProjectileImpactDamage is experimental: turn on features.experimental in anvilconfig.json."
            )


class EntityProjectile(_EntityProjectile):
    """[EXPERIMENTAL] Turns the entity into a projectile, with the 1.26.70 `on_hit` options.
    Needs the experimental flag in anvilconfig.json. Takes the same arguments as the public
    `EntityProjectile`; `set_on_hit` takes this module's `ProjectileImpactDamage`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_projectile)
    """

    def __validate__(self) -> None:
        super().__validate__()
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityProjectile is experimental: turn on features.experimental in anvilconfig.json."
            )

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
        """Sets what happens when the projectile hits a block, a fluid or an entity.

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
            impact_damage (ProjectileImpactDamage, optional): Damages the entity hit, with the 1.26.70 options.
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


class EntityReflectProjectiles(JsonComponent):
    """[EXPERIMENTAL] Allows an entity to reflect projectiles. Needs the experimental flag in anvilconfig.json.

    Args:
        azimuth_angle (Molang | str | float, optional): Angle in degrees added to the projectile's y axis rotation. Game default 0.
        elevation_angle (Molang | str | float, optional): Angle in degrees added to the projectile's x axis rotation. Game default 0.
        reflected_projectiles (list[str | Entity], optional): Projectiles that are reflected when they hit the entity.
        reflection_scale (Molang | str | float, optional): Velocity scale of the reflected projectile. Below 1 slows it, above 1 speeds it up. Game default 1.
        reflection_sound (str, optional): Sound event played when a projectile is reflected. Game default reflect.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_reflect_projectiles)
    """

    identifier = "minecraft:reflect_projectiles"

    azimuth_angle: Molang | str | float | None = json_field(default=None)
    elevation_angle: Molang | str | float | None = json_field(default=None)
    reflected_projectiles: list[Annotated[str | Entity, EntityId]] | None = json_field(
        default=None
    )
    reflection_scale: Molang | str | float | None = json_field(default=None)
    reflection_sound: str | None = json_field(default=None)

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityReflectProjectiles is experimental: turn on features.experimental in anvilconfig.json."
            )


class EntityCanStandOnBrittleIce(JsonComponent):
    """[EXPERIMENTAL] Allows an entity to stand on brittle ice. Needs the experimental flag in anvilconfig.json.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_stand_on_brittle_ice)
    """

    identifier = "minecraft:can_stand_on_brittle_ice"

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityCanStandOnBrittleIce is experimental: turn on features.experimental in anvilconfig.json."
            )


class EntityTimeMarkerSensor(JsonComponent):
    """[EXPERIMENTAL] Runs events on this entity when named time markers fire on named world clocks. Needs the experimental flag in anvilconfig.json.

    Args:
        triggers (list[TimeMarkerSensorTrigger]): The world clock time markers to listen for, at least one. Entries identical to an earlier one are ignored by the game. Add them with `add_trigger`.
    """

    identifier = "minecraft:time_marker_sensor"

    triggers: list[TimeMarkerSensorTrigger] = json_field(default_factory=list)

    def add_trigger(
        self,
        *,
        clock: str,
        time_marker: str,
        event: str,
        filters: Filter | None = None,
        target: FilterSubject | None = None,
    ) -> "EntityTimeMarkerSensor":
        """Adds a world clock time marker to listen for, and the event to run when it fires.

        Args:
            clock (str): The name of the world clock to listen to.
            time_marker (str): The name of the time marker on the clock to listen for.
            event (str): The event to run when the time marker fires.
            filters (Filter, optional): The conditions for the event to run.
            target (FilterSubject, optional): The entity the event runs on. Game default self.
        """
        self.triggers.append(
            TimeMarkerSensorTrigger(
                clock=clock,
                time_marker=time_marker,
                on_time_marker=EventTrigger(
                    event=event, filters=filters, target=target
                ),
            )
        )
        return self

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityTimeMarkerSensor is experimental: turn on features.experimental in anvilconfig.json."
            )
        if not self.triggers:
            raise ValueError("EntityTimeMarkerSensor needs at least one trigger.")


class EntityTeleport(_EntityTeleport):
    """[EXPERIMENTAL] Defines an entity's teleporting behavior, with the 1.26.70 options.
    Needs the experimental flag in anvilconfig.json.

    Args:
        can_teleport_into_liquid (bool, optional): Whether the entity can teleport into blocks that hold a liquid, such as water. Game default false.
        dark_teleport_chance (float, optional): Chance to teleport in darkness. Game default 0.01.
        light_teleport_chance (float, optional): Chance to teleport in daylight. Game default 0.01.
        max_random_teleport_time (float, optional): Maximum seconds between random teleports. Game default 20.
        min_random_teleport_time (float, optional): Minimum seconds between random teleports. Game default 0.
        on_teleport_sound (str, optional): Level sound event played after a successful teleport. An entity with no sound bound to it plays the default teleport sound; "undefined" teleports silently. Game default teleport.
        projectile_filter (Filter, optional): Projectiles that make the entity try to teleport. Without it, every projectile.
        random_teleport_cube (tuple[float, float, float], optional): The area of random teleports. Game default (32, 16, 32).
        random_teleports (bool, optional): Whether the entity teleports randomly. Game default true.
        target_distance (float, optional): Minimum distance from the target before the entity starts teleporting towards it. Game default 16.
        target_teleport_chance (float, optional): Chance to teleport, from 0 to 1. Game default 1.
        target_teleport_distance (float | tuple[float, float], optional): Distance teleported towards the target, or a `(min, max)` range, from -32 to 32. Negative values teleport away from the target. Written as `{"min", "max"}`. Game default (16, 16).
        target_teleport_offset (tuple[float, float, float], optional): Maximum random offset on each axis, in either direction, added to the teleport direction, from 0 to 32. The y offset is rounded down to whole blocks. Game default (4, 8, 4).
        teleports_on_projectile_hit (bool, optional): Whether the entity teleports away from projectiles about to hit it. Game default false.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_teleport)
    """

    can_teleport_into_liquid: bool | None = json_field(default=None)
    on_teleport_sound: str | None = json_field(default=None)
    target_teleport_distance: (
        Annotated[float | tuple[float, float], InRange(-32, 32), ExactMinMax] | None
    ) = json_field(default=None)
    target_teleport_offset: (
        Annotated[tuple[float, float, float], InRange(0, 32)] | None
    ) = json_field(default=None)

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityTeleport is experimental: turn on features.experimental in anvilconfig.json."
            )


class TrailPlacementCondition(JsonObject):
    """A block requirement of `minecraft:trail`, checked at a vertical offset from each
    placement position. All conditions must pass; the block types of one condition are
    alternatives.

    Args:
        block_types (list[str | Block | BlockDescriptor]): Blocks that satisfy the condition, at least one.
        y_offset (int, optional): Vertical offset from the placement position, from -16 to 16. Game default 0.
    """

    block_types: Annotated[
        list[Annotated[str | Block | BlockDescriptor, BlockId]], Length(1)
    ] = json_field()
    y_offset: Annotated[int, InRange(-16, 16)] | None = json_field(default=None)


class EntityTrail(JsonComponent):
    """[EXPERIMENTAL] Makes the entity leave a trail of blocks as it moves, in the 1.26.70 form.
    Obeys Mob Griefing rules. Needs the experimental flag in anvilconfig.json.
    It writes `minecraft:trail` like the public `EntityTrail`, which keeps the older options,
    and clashes with it: an entity cannot use both.

    Args:
        block_type (str | Block | BlockDescriptor, optional): The block placed. A solid block cannot be placed at the entity's position when `offset` is (0, 0, 0). Game default air.
        extent (int, optional): Maximum horizontal distance from the center at which blocks are placed, from 0 to 16. Game default 0.
        offset (tuple[float, float, float], optional): Offset from the entity where blocks are placed and checked, capped at 16 blocks. X and Z follow the entity's nearest cardinal facing; Y is vertical. Game default (0, 0, 0).
        place_only_on_block_position_change (bool, optional): Places blocks only on ticks where the bottom of the entity moves into another block position, or where it lands. Game default false.
        placement_checks (Literal["none", "block", "standard"], optional): The checks at each placement position: "none" skips them, "block" applies the block placement conditions, "standard" applies the standard block placement rules, including clearance from entities in the way. Game default "block".
        placement_conditions (list[TrailPlacementCondition], optional): Block requirements around each placement position, at least one. Add them with `add_placement_condition`. Game default one condition, air at y offset 0.
        placement_filter (Filter, optional): Conditions on the entity for blocks to be placed.
        shape (Literal["corners", "square", "circle"], optional): The horizontal placement pattern: four corner blocks, a filled square or a filled disk. Game default "corners".

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trail)
    """

    identifier = "minecraft:trail"
    _clashes = (_EntityTrail,)

    block_type: Annotated[str | Block | BlockDescriptor, BlockId] | None = json_field(
        default=None
    )
    extent: Annotated[int, InRange(0, 16)] | None = json_field(default=None)
    offset: tuple[float, float, float] | None = json_field(default=None)
    place_only_on_block_position_change: bool | None = json_field(default=None)
    placement_checks: Literal["none", "block", "standard"] | None = json_field(
        default=None
    )
    placement_conditions: Annotated[list[TrailPlacementCondition], Length(1)] | None = (
        json_field(default=None)
    )
    placement_filter: Filter | None = json_field(default=None)
    shape: Literal["corners", "square", "circle"] | None = json_field(default=None)

    def add_placement_condition(
        self,
        *,
        block_types: list[str | Block | BlockDescriptor],
        y_offset: int | None = None,
    ) -> "EntityTrail":
        """Adds a block requirement checked at a vertical offset from each placement position.

        Args:
            block_types (list[str | Block | BlockDescriptor]): Blocks that satisfy the condition, at least one. Any of them passes.
            y_offset (int, optional): Vertical offset from the placement position, from -16 to 16. Game default 0.
        """
        if self.placement_conditions is None:
            self.placement_conditions = []
        self.placement_conditions.append(
            TrailPlacementCondition(block_types=block_types, y_offset=y_offset)
        )
        return self

    def __validate__(self) -> None:
        if not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "EntityTrail is experimental: turn on features.experimental in anvilconfig.json."
            )
