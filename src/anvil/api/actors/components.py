import math
from typing import Any, Dict, List, TypedDict

from anvil import ANVIL, CONFIG
from anvil.api.logic.molang import Molang
from anvil.lib.enums import (Biomes, BreedingMutationStrategy, ContainerType,
                             ControlFlags, DamageCause, DamageSensor,
                             Difficulty, Effects, ExplosionParticleEffect,
                             FilterEquipmentDomain, FilterOperation,
                             FilterSubject, LeashSpringType,
                             LineOfSightObstructionType, LookAtLocation,
                             LootedAtSetTarget, MinecraftBiomeTags,
                             RideableDismountMode, Slots, Vibrations)
from anvil.lib.format_versions import ENTITY_SERVER_VERSION
from anvil.lib.lib import clamp
from anvil.lib.schemas import BlockDescriptor, _BaseComponent
from anvil.lib.types import *

__all__ = [
    "EntityAddRider",
    "EntityAdmireItem",
    "EntityCollisionBox",
    "EntityTypeFamily",
    "EntityInstantDespawn",
    "EntityHealth",
    "EntityPhysics",
    "EntityKnockbackResistance",
    "EntityPushable",
    "EntityPushThrough",
    "EntityMovement",
    "EntityTickWorld",
    "EntityCustomHitTest",
    "EntityCanClimb",
    "EntityAttack",
    "EntityJumpStatic",
    "EntityHorseJumpStrength",
    "EntitySpellEffects",
    "EntityFrictionModifier",
    "EntityVariant",
    "EntityMarkVariant",
    "EntitySkinID",
    "EntityScale",
    "EntityScaleByAge",
    "EntityAreaAttack",
    "EntityIsStackable",
    "EntityIsIllagerCaptain",
    "EntityIsBaby",
    "EntityIsIgnited",
    "EntityIsTamed",
    "EntityIsCharged",
    "EntityIsStunned",
    "EntityIsSaddled",
    "EntityIsSheared",
    "EntityCanFly",
    "EntityCanPowerJump",
    "EntityIsChested",
    "EntityOutOfControl",
    "EntityDamageSensor",
    "EntityFollowRange",
    "EntityMovementType",
    "EntityNavigationType",
    "EntityEnvironmentSensor",
    "EntityPreferredPath",
    "EntityTargetNearbySensor",
    "EntityNearestAttackableTarget",
    "EntityNearestPrioritizedAttackableTarget",
    "EntityTimer",
    "EntityRideable",
    "EntityProjectile",
    "EntityExplode",
    "EntityKnockbackRoar",
    "EntityMobEffect",
    "EntitySpawnEntity",
    "EntityLoot",
    "EntityFloat",
    "EntityRandomStroll",
    "EntityLookAtPlayer",
    "EntityRandomLookAround",
    "EntityHurtByTarget",
    "EntityMeleeAttack",
    "EntityRangedAttack",
    "EntityShooter",
    "EntitySummonEntity",
    "EntityDelayedAttack",
    "EntityMoveToBlock",
    "EntityInsideBlockNotifier",
    "EntityTransformation",
    "EntityNPC",
    "EntityEquipment",
    "Entity_EquipItem",
    "EntityEquipItem",
    "EntityFireImmune",
    "EntitySendEvent",
    "EntityMoveTowardsTarget",
    "EntityEntitySensor",
    "EntityAmbientSoundInterval",
    "EntityRandomSitting",
    "EntityStayWhileSitting",
    "EntityUnderwaterMovement",
    "EntityRandomSwim",
    "EntityRandomBreach",
    "EntityMoveToWater",
    "EntityMoveToLand",
    "EntityMoveToLava",
    "EntityLookAtTarget",
    "EntityMovementMeters",
    "EntityFollowParent",
    "EntityPlayerRideTamed",
    "EntityInputGroundControlled",
    "EntityFollowOwner",
    "EntityWaterMovement",
    "EntityPanic",
    "EntityChargeAttack",
    "EntityRamAttack",
    "EntityAvoidMobType",
    "EntityLeapAtTarget",
    "EntityOcelotAttack",
    "EntityAngry",
    "EntityOwnerHurtByTarget",
    "EntityOwnerHurtTarget",
    "EntityRandomSearchAndDig",
    "EntityStompAttack",
    "EntityFollowMob",
    "EntityRandomSwim",  # duplicate if defined again
    "EntityRandomBreach",  # duplicate if defined again
    "EntityFlyingSpeed",
    "EntityRandomHover",
    "EntityInteract",
    "EntityAngerLevel",
    "EntityRoar",
    "EntityFloatWander",
    "EntityLayDown",
    "EntityMeleeBoxAttack",
    "EntityCanJoinRaid",
    "EntityTimerFlag1",
    "EntityTimerFlag2",
    "EntityTimerFlag3",
    "EntityTameable",
    "EntityRunAroundLikeCrazy",
    "EntitySlimeKeepOnJumping",
    "EntityAgeable",
    "EntityInventory",
    "EntityDash",
    "EntityBreathable",
    "EntityVariableMaxAutoStep",
    "EntityRiseToLiquidLevel",
    "EntityBuoyant",
    "EntityLavaMovement",
    "EntityExperienceReward",
    "EntityEquippable",
    "EntityColor",
    "EntityColor2",
    "EntityBurnsInDaylight",
    "EntityBoss",
    "EntitySittable",
    "EntityFlyingSpeedMeters",
    "EntityConditionalBandwidthOptimization",
    "EntityItemHopper",
    "EntityBodyRotationBlocked",
    "EntityDamageAbsorption",
    "EntityDimensionBound",
    "EntityTransient",
    "EntityCannotBeAttacked",
    "EntityIgnoreCannotBeAttacked",
    "EntityLookedAt",
    "EntityMovementSoundDistanceOffset",
    "EntityRendersWhenInvisible",
    "EntityBreedable",
    "EntityIsCollidable",
    "EntityBodyRotationAxisAligned",
    "EntityInputAirControlled",
    "EntityLeashable",
    "EntityBodyRotationAlwaysFollowsHead",
]

class _ai_goal(_BaseComponent):
    def __init__(self, component_name: str) -> None:
        super().__init__(component_name)

    def priority(self, priority: int):
        """The higher the priority, the sooner this behavior will be executed as a goal.

        Parameters:
            priority (int): The higher the priority, the sooner this behavior will be executed as a goal.
        """
        self._add_field("priority", priority)
        return self


class Filter:
    # Basic configuration
    def _construct_filter(filter_name, subject, operator, domain, value):
        _filter = {"test": filter_name, "value": value}
        if subject != FilterSubject.Self:
            _filter.update({"subject": subject})
        if operator != FilterOperation.Equals:
            _filter.update({"operator": operator})
        if domain != None:
            _filter.update({"domain": domain})

        return _filter
    
    # Filter Groups
    @staticmethod
    def all_of(*filters: "Filter"):
        return {"all_of": [*filters]}

    @staticmethod
    def any_of(*filters: "Filter"):
        return {"any_of": [*filters]}

    @staticmethod
    def none_of(*filters: "Filter"):
        return {"none_of": [*filters]}

    # Actual Filters
    @classmethod
    def distance_to_nearest_player(
        self,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("distance_to_nearest_player", subject, operator, None, max(0, value))

    @classmethod
    def has_component(
        self,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_component", subject, operator, None, value)

    @classmethod
    def is_family(
        self,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_family", subject, operator, None, value)

    @classmethod
    def is_block(
        self,
        value: Block | Identifier,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):  
        from anvil.lib.schemas import BlockDescriptor

        if not isinstance(value, (BlockDescriptor, str)):
            raise TypeError(f"Expected BlockDescriptor or Identifier, got {type(value).__name__}. Filter [is_block]")

        return self._construct_filter(
            "is_block",
            subject,
            operator,
            None,
            str(value),
        )

    @classmethod
    def is_visible(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_visible", subject, operator, None, value)

    @classmethod
    def is_target(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_target", subject, operator, None, value)

    @classmethod
    def is_riding(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_riding", subject, operator, None, value)

    @classmethod
    def has_target(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_target", subject, operator, None, value)

    @classmethod
    def has_component(
        self,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_component", subject, operator, None, value)

    @classmethod
    def is_owner(
        self,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_owner", subject, operator, None, value)

    @classmethod
    def has_equipment(
        self,
        value: int,
        domain: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_equipment", subject, operator, domain, value)

    @classmethod
    def actor_health(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("actor_health", subject, operator, None, value)

    @classmethod
    def random_chance(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("random_chance", subject, operator, None, value)

    @classmethod
    def target_distance(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("target_distance", subject, operator, None, value)

    @classmethod
    def is_raider(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_raider", subject, operator, None, value)

    @classmethod
    def is_variant(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_variant", subject, operator, None, value)

    @classmethod
    def is_mark_variant(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_mark_variant", subject, operator, None, value)

    @classmethod
    def is_skin_id(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_skin_id", subject, operator, None, value)

    @classmethod
    def all_slots_empty(
        self,
        value: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the designated equipment location for the subject entity is completely empty.

        Parameters:
            value (FilterEquipmentDomain, optional): The equipment location to test. Defaults to FilterEquipmentDomain.Any.
            subject (FilterSubject, optional): Subject to test the value against. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use in testing. Defaults to FilterOperation.Equals.
        """
        return self._construct_filter("all_slots_empty", subject, operator, None, value)

    @classmethod
    def any_slot_empty(
        self,
        value: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Returns true when the designated equipment location for the subject entity has any empty slot.

        Parameters:
            value (FilterEquipmentDomain, optional): The equipment location to test. Defaults to FilterEquipmentDomain.Any.
            subject (FilterSubject, optional): Subject to test the value against. Defaults to FilterSubject.Self.
            operator (FilterOperation, optional): Operation to use in testing. Defaults to FilterOperation.Equals.
        """
        return self._construct_filter("all_slots_empty", subject, operator, None, value)

    @classmethod
    def is_biome(
        self,
        value: Biomes,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_biome", subject, operator, None, value.value)

    @classmethod
    def is_underwater(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_underwater", subject, operator, None, value)

    @classmethod
    def in_water(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("in_water", subject, operator, None, value)

    @classmethod
    def on_ground(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("on_ground", subject, operator, None, value)

    # Properties

    @classmethod
    def int_property(
        self,
        value: int,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("int_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value)

    @classmethod
    def bool_property(
        self,
        value: bool,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("bool_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value)

    @classmethod
    def float_property(
        self,
        value: float,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("float_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value)

    @classmethod
    def enum_property(
        self,
        value: str,
        domain: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("enum_property", subject, operator, f"{CONFIG.NAMESPACE}:{domain}", value)

    @classmethod
    def has_property(
        self,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_property", subject, operator, None, f"{CONFIG.NAMESPACE}:{value}")

    @classmethod
    def is_daytime(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_daytime", subject, operator, None, value)

    @classmethod
    def has_damage(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_damage", subject, operator, None, value)

    @classmethod
    def rider_count(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("rider_count", subject, operator, None, value)

    @classmethod
    def is_panicking(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_panicking", subject, operator, None, value)

    @classmethod
    def is_sprinting(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_sprinting", subject, operator, None, value)

    @classmethod
    def was_last_hurt_by(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("was_last_hurt_by", subject, operator, None, value)

    @classmethod
    def has_tag(
        self,
        value: str,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_tag", subject, operator, None, value)

    @classmethod
    def is_difficulty(
        self,
        value: Difficulty,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_difficulty", subject, operator, None, str(value))

    @classmethod
    def is_sitting(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_sitting", subject, operator, None, value)

    @classmethod
    def has_damaged_equipment(
        self,
        value: str,
        domain: FilterEquipmentDomain,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_damaged_equipment", subject, operator, domain, value)

    @classmethod
    def owner_distance(
        self,
        value: int,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("owner_distance", subject, operator, None, value)

    @classmethod
    def home_distance(
        self,
        value: float,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("home_distance", subject, operator, None, value)

    @classmethod
    def is_bound_to_creaking_heart(
        self,
        value: bool,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("is_bound_to_creaking_heart", subject, operator, None, value)

    @classmethod
    def has_equipment_tag(
        self,
        value: str,
        domain: FilterEquipmentDomain = FilterEquipmentDomain.Any,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        return self._construct_filter("has_equipment", subject, operator, domain, value)

    @classmethod
    def has_biome_tag(
        self,
        value: MinecraftBiomeTags,
        *,
        subject: FilterSubject = FilterSubject.Self,
        operator: FilterOperation = FilterOperation.Equals,
    ):
        """Checks if the entity is in a biome with the specified tag."""
        return self._construct_filter("has_biome_tag", subject, operator, None, value)

# Components ==========================================================================
# Attributes ==========================================================================


class EntityAddRider(_BaseComponent):
    _identifier = "minecraft:addrider"

    def __init__(self, entity_type: Identifier, spawn_event: Event = None) -> None:
        """Adds a rider to the entity. Requires `minecraft:rideable.`.

        Parameters
        ----------
        `entity_type` : `Identifier`.
            The entity type that will be riding this
        `spawn_event` : `Event`, `optional`.
            The spawn event that will be used when the riding entity is created.

        """
        super().__init__("addrider")
        self._add_field("entity_type", str(entity_type))
        if not spawn_event is None:
            self._add_field("spawn_event", spawn_event)


class EntityAdmireItem(_BaseComponent):
    _identifier = "minecraft:admire_item"

    def __init__(self, cooldown_after_being_attacked: Seconds, duration: Seconds = 10) -> None:
        """Causes the mob to ignore attackable targets for a given duration.

        Parameters
        ----------
        `cooldown_after_being_attacked` : `seconds` `int`.
            Duration, in seconds, for which mob won't admire items if it was hurt
        `duration` : `seconds` `int`.
            Duration, in seconds, that the mob is pacified. `Default: 10`

        """
        super().__init__("admire_item")
        self._add_field("cooldown_after_being_attacked", cooldown_after_being_attacked)
        if not duration == 10:
            self._add_field("duration", duration)


class EntityCollisionBox(_BaseComponent):
    _identifier = "minecraft:collision_box"

    def __init__(self, height: float, width: float) -> None:
        """Sets the width and height of the Entity's collision box."""
        super().__init__("collision_box")
        self._add_field("height", height)
        self._add_field("width", width)


class EntityTypeFamily(_BaseComponent):
    _identifier = "minecraft:type_family"

    def __init__(self, *family: str) -> None:
        """Defines the families this entity belongs to."""
        super().__init__("type_family")
        self._add_field("family", family)


class EntityInstantDespawn(_BaseComponent):
    _identifier = "minecraft:instant_despawn"

    def __init__(self, remove_child_entities: bool = False) -> None:
        """"""
        super().__init__("instant_despawn")
        if remove_child_entities:
            self._add_field("remove_child_entities", True)


class EntityHealth(_BaseComponent):
    _identifier = "minecraft:health"

    def __init__(self, value: int, min: int = None, max: int = None) -> None:
        """Sets the amount of health this mob has."""
        super().__init__("health")
        self._add_field("value", value)
        if not max is None:
            self._add_field("max", max)
        if not min is None:
            self._add_field("min", min)


class EntityPhysics(_BaseComponent):
    _identifier = "minecraft:physics"

    def __init__(self, has_collision: bool = True, has_gravity: bool = True, push_towards_closest_space: bool = False) -> None:
        """Defines physics properties of an actor, including if it is affected by gravity or if it collides with objects."""
        super().__init__("physics")
        if not has_collision:
            self._add_field("has_collision", has_collision)
        if not has_gravity:
            self._add_field("has_gravity", has_gravity)
        if push_towards_closest_space:
            self._add_field("push_towards_closest_space", push_towards_closest_space)


class EntityKnockbackResistance(_BaseComponent):
    _identifier = "minecraft:knockback_resistance"

    def __init__(self, value: float) -> None:
        """Determines the amount of knockback resistance that the item has."""
        super().__init__("knockback_resistance")
        self._add_field("value", max(0, min(1, value)))


class EntityPushable(_BaseComponent):
    _identifier = "minecraft:pushable"

    def __init__(self, is_pushable: bool = True, is_pushable_by_piston: bool = True) -> None:
        """Defines what can push an entity between other entities and pistons."""
        super().__init__("pushable")
        self._add_field("is_pushable", is_pushable)
        self._add_field("is_pushable_by_piston", is_pushable_by_piston)


class EntityPushThrough(_BaseComponent):
    _identifier = "minecraft:push_through"

    def __init__(self, value: float) -> None:
        """Sets the distance through which the entity can push through.

        This component sets the distance through which an entity can exert force to move through other entities or blocks.

        Parameters
        ----------
        value : float, optional
            The distance in blocks that the entity can push through. It can be thought of as a "buffer zone" that the entity creates around itself to navigate through crowded spaces. The default value is 0.0, which means the entity follows the standard collision rules of the game and cannot move through solid entities or blocks. Positive values increase the entity's ability to move through crowds, while negative values are rounded to 0.

        """
        super().__init__("push_through")
        self._add_field("value", value)


class EntityMovement(_BaseComponent):
    _identifier = "minecraft:movement"

    def __init__(self, value: int, max: int = None) -> None:
        """Defined the movement speed of the entity in block/tick.

        Parameters:
            value (int): The movement speed of the entity in block/tick.
            max (int, optional): The maximum movement speed of the entity in block/tick. Defaults to None.
        """
        super().__init__("movement")
        self._add_field("value", value)
        if not max is None:
            self._add_field("max", max)


class EntityTickWorld(_BaseComponent):
    _identifier = "minecraft:tick_world"

    def __init__(
        self,
        never_despawn: bool = True,
        radius: int = None,
        distance_to_players: int = None,
    ) -> None:
        """Defines if the entity ticks the world and the radius around it to tick."""
        super().__init__("tick_world")
        self._add_field("never_despawn", never_despawn)
        if not radius is None:
            self._add_field("radius", radius)
        if not distance_to_players is None:
            self._add_field("distance_to_players", distance_to_players)


class EntityCustomHitTest(_BaseComponent):
    _identifier = "minecraft:custom_hit_test"

    def __init__(self, height: float, width: float, pivot: list[float, float, float] = [0, 1, 0]) -> None:
        """List of hitboxes for melee and ranged hits against the entity."""
        super().__init__("custom_hit_test")
        self._add_field("hitboxes", [{"width": width, "height": height, "pivot": pivot}])

    def add_hitbox(self, height: float, width: float, pivot: list[float, float, float] = [0, 1, 0]):
        self._component["hitboxes"].append({"width": width, "height": height, "pivot": pivot})
        return self


class EntityCanClimb(_BaseComponent):
    _identifier = "minecraft:can_climb"

    def __init__(self) -> None:
        """Allows this entity to climb up ladders."""
        super().__init__("can_climb")


class EntityAttack(_BaseComponent):
    _identifier = "minecraft:attack"

    def __init__(self, damage: int, effect_duration: int = None, effect_name: str = None) -> None:
        """Defines an entity's melee attack and any additional effects on it."""
        super().__init__("attack")
        self._add_field("damage", damage)
        if not effect_duration is None:
            self._add_field("effect_duration", effect_duration)
        if not effect_name is None:
            self._add_field("effect_name", effect_name)


class EntityJumpStatic(_BaseComponent):
    _identifier = "minecraft:jump.static"

    def __init__(self, jump_power: float = 0.42) -> None:
        """Gives the entity the ability to jump."""
        super().__init__("jump.static")
        self._add_field("jump_power", jump_power)


class EntityHorseJumpStrength(_BaseComponent):
    _identifier = "minecraft:horse.jump_strength"

    def __init__(self, range_min: float, range_max: float) -> None:
        """Allows this mob to jump higher when being ridden by a player."""
        super().__init__("horse.jump_strength")
        self._add_field("value", {"range_min": range_min, "range_max": range_max})


class EntitySpellEffects(_BaseComponent):
    _identifier = "minecraft:spell_effects"

    def __init__(self) -> None:
        """Defines what mob effects to add and remove to the entity when adding this component."""
        super().__init__("spell_effects")
        self._add_field("add_effects", [])
        self._add_field("remove_effects", [])

    def add_effects(
        self,
        effect: Effects,
        duration: int,
        amplifier: int,
        ambient: bool = True,
        visible: bool = True,
        display_on_screen_animation: bool = True,
    ):
        effect = {
            "effect": effect,
            "duration": duration,
            "amplifier": amplifier,
        }
        if ambient is not True:
            effect.update({"ambient": ambient})
        if visible is not True:
            effect.update({"visible": visible})
        if display_on_screen_animation is not True:
            effect.update({"display_on_screen_animation": display_on_screen_animation})

        self._component["add_effects"].append(effect)
        return self

    def remove_effects(self, *effects: Effects):
        self._component["remove_effects"] = [e.value for e in effects]
        return self


class EntityFrictionModifier(_BaseComponent):
    _identifier = "minecraft:friction_modifier"

    def __init__(self, value: int) -> None:
        """Defines how much friction affects this entity."""
        super().__init__("friction_modifier")
        self._add_field("value", value)


class EntityVariant(_BaseComponent):
    _identifier = "minecraft:variant"

    def __init__(self, value: int) -> None:
        """Used to differentiate the component group of a variant of an entity from others. (e.g. ocelot, villager)."""
        super().__init__("variant")
        self._add_field("value", value)


class EntityMarkVariant(_BaseComponent):
    _identifier = "minecraft:mark_variant"

    def __init__(self, value: int) -> None:
        """Additional variant value. Can be used to further differentiate variants."""
        super().__init__("mark_variant")
        self._add_field("value", value)


class EntitySkinID(_BaseComponent):
    _identifier = "minecraft:skin_id"

    def __init__(self, value: int) -> None:
        """Skin ID value. Can be used to differentiate skins, such as base skins for villagers."""
        super().__init__("skin_id")
        self._add_field("value", value)


class EntityScale(_BaseComponent):
    _identifier = "minecraft:scale"

    def __init__(self, value: int) -> None:
        """Sets the entity's visual size."""
        super().__init__("scale")
        self._add_field("value", value)


class EntityScaleByAge(_BaseComponent):
    _identifier = "minecraft:scale_by_age"

    def __init__(self, start_scale: int, end_scale: int) -> None:
        """Defines the entity's size interpolation based on the entity's age."""
        super().__init__("scale_by_age")
        self._add_field("end_scale", end_scale)
        self._add_field("start_scale", start_scale)


class EntityAreaAttack(_BaseComponent):
    _identifier = "minecraft:area_attack"

    def __init__(self, cause: DamageCause, damage_per_tick: int = 2, damage_range: float = 0.2) -> None:
        """Is a component that does damage to entities that get within range."""
        super().__init__("area_attack")

        self._add_field("cause", cause.value)

        if not damage_per_tick == 2:
            self._add_field("damage_per_tick", damage_per_tick)
        if not damage_range == 0.2:
            self._add_field("damage_range", damage_range)

    def filter(self, entity_filter: dict):
        self._add_field("entity_filter", entity_filter)
        return self


class EntityIsStackable(_BaseComponent):
    _identifier = "minecraft:is_stackable"

    def __init__(self) -> None:
        """Sets that this entity can be stacked."""
        super().__init__("is_stackable")


class EntityIsIllagerCaptain(_BaseComponent):
    _identifier = "minecraft:is_illager_captain"

    def __init__(self) -> None:
        """Sets that this entity is an illager captain."""
        super().__init__("is_illager_captain")


class EntityIsBaby(_BaseComponent):
    _identifier = "minecraft:is_baby"

    def __init__(self) -> None:
        """Sets that this entity is a baby."""
        super().__init__("is_baby")


class EntityIsIgnited(_BaseComponent):
    _identifier = "minecraft:is_ignited"

    def __init__(self) -> None:
        """Sets that this entity is currently on fire."""
        super().__init__("is_ignited")


class EntityIsTamed(_BaseComponent):
    _identifier = "minecraft:is_tamed"

    def __init__(self) -> None:
        """Sets that this entity is currently tamed."""
        super().__init__("is_tamed")


class EntityIsCharged(_BaseComponent):
    _identifier = "minecraft:is_charged"

    def __init__(self) -> None:
        """Sets that this entity is charged."""
        super().__init__("is_charged")


class EntityIsStunned(_BaseComponent):
    _identifier = "minecraft:is_stunned"

    def __init__(self) -> None:
        """Sets that this entity is currently stunned."""
        super().__init__("is_stunned")


class EntityIsSaddled(_BaseComponent):
    _identifier = "minecraft:is_saddled"

    def __init__(self) -> None:
        """Sets that this entity is currently saddled."""
        super().__init__("is_saddled")


class EntityIsSheared(_BaseComponent):
    _identifier = "minecraft:is_sheared"

    def __init__(self) -> None:
        """Sets that this entity is currently sheared."""
        super().__init__("is_sheared")


class EntityCanFly(_BaseComponent):
    _identifier = "minecraft:can_fly"

    def __init__(self) -> None:
        """Marks the entity as being able to fly, the pathfinder won't be restricted to paths where a solid block is required underneath it."""
        super().__init__("can_fly")


class EntityCanPowerJump(_BaseComponent):
    _identifier = "minecraft:can_power_jump"

    def __init__(self) -> None:
        """Allows the entity to power jump like the horse does in vanilla."""
        super().__init__("can_power_jump")


class EntityIsChested(_BaseComponent):
    _identifier = "minecraft:is_chested"

    def __init__(self) -> None:
        """Sets that this entity is currently carrying a chest."""
        super().__init__("is_chested")


class EntityOutOfControl(_BaseComponent):
    _identifier = "minecraft:out_of_control"

    def __init__(self) -> None:
        """Defines the entity's 'out of control' state."""
        super().__init__("out_of_control")


class EntityDamageSensor(_BaseComponent):
    _identifier = "minecraft:damage_sensor"

    def __init__(self) -> None:
        """Defines what events to call when this entity is damaged by specific entities or items."""
        super().__init__("damage_sensor")
        self._add_field("triggers", [])

    def add_trigger(
        self,
        cause: DamageCause,
        deals_damage: DamageSensor = DamageSensor.Yes,
        on_damage_event: str = None,
        on_damage_filter: Filter = None,
        damage_multiplier: int = 1,
        damage_modifier: float = 0,
    ):
        damage = {"deals_damage": deals_damage, "on_damage": {}}
        if not cause is DamageCause.All:
            damage["cause"] = cause.value
        if not on_damage_event is None:
            damage["on_damage"] = {"event": on_damage_event}
        if not on_damage_filter is None:
            damage["on_damage"]["filters"] = on_damage_filter
        if not damage_multiplier == 1:
            damage["damage_multiplier"] = damage_multiplier
        if not damage_modifier == 0:
            damage["damage_modifier"] = damage_modifier

        self._get_field("triggers", []).append(damage)
        return self


class EntityFollowRange(_BaseComponent):
    _identifier = "minecraft:follow_range"

    def __init__(self, value: int, max_range: int = None) -> None:
        """Defines the range of blocks that a mob will pursue a target."""
        super().__init__("follow_range")
        self._add_field("value", value)
        if not max_range is None:
            self._add_field("max", max_range)


class EntityMovementType:
    def Basic(max_turn: float = 30):
        movement = _BaseComponent("movement.basic")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        return movement

    def Amphibious(max_turn: float = 30):
        """Allows the mob to swim in water and walk on land."""
        movement = _BaseComponent("movement.amphibious")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        return movement

    def Dolphin() -> None:
        """Allows the mob to swim in water like a dolphin."""
        movement = _BaseComponent("movement.dolphin")
        return movement

    def Fly(
        max_turn: float = 30,
        start_speed: float = 0.1,
        speed_when_turning: float = 0.2,
    ) -> None:
        """Causes the mob to fly."""
        movement = _BaseComponent("movement.fly")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        if not start_speed == 0.1:
            movement._add_field("start_speed", start_speed)
        if not speed_when_turning == 0.2:
            movement._add_field("speed_when_turning", speed_when_turning)
        return movement

    def Generic(max_turn: float = 30):
        """Allows a mob to fly, swim, climb, etc."""
        movement = _BaseComponent("movement.generic")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        return movement

    def Glide(
        max_turn: float = 30,
        start_speed: float = 0.1,
        speed_when_turning: float = 0.2,
    ):
        """Is the move control for a flying mob that has a gliding movement."""
        movement = _BaseComponent("movement.glide")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        if not start_speed == 0.1:
            movement._add_field("start_speed", start_speed)
        if not speed_when_turning == 0.2:
            movement._add_field("speed_when_turning", speed_when_turning)
        return movement

    def Jump(max_turn: float = 30, jump_delay: tuple[float, float] = (0, 0)):
        """Causes the mob to jump as it moves with a specified delay between jumps."""
        movement = _BaseComponent("movement.jump")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        if not jump_delay == (0, 0):
            movement._add_field("jump_delay", jump_delay)
        return movement

    def Skip(max_turn: float = 30):
        """Causes the mob to hop as it moves."""
        movement = _BaseComponent("movement.skip")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        return movement

    def Sway(
        max_turn: float = 30,
        sway_amplitude: float = 0.05,
        sway_frequency: float = 0.5,
    ):
        """Causes the mob to sway side to side giving the impression it is swimming."""
        movement = _BaseComponent("movement.sway")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        if not sway_amplitude == 0.05:
            movement._add_field("sway_amplitude", sway_amplitude)
        if not sway_frequency == 0.5:
            movement._add_field("sway_frequency", sway_frequency)
        return movement

    def Hover(max_turn: float = 30):
        """Causes the mob to hover."""
        movement = _BaseComponent("movement.hover")
        if not max_turn == 30:
            movement._add_field("max_turn", max_turn)
        return movement


class EntityNavigationType:
    def _basic(
        cls: _BaseComponent,
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ) -> None:
        if avoid_damage_blocks:
            cls._add_field("avoid_damage_blocks", avoid_damage_blocks)
        if avoid_portals:
            cls._add_field("avoid_portals", avoid_portals)
        if avoid_sun:
            cls._add_field("avoid_sun", avoid_sun)
        if avoid_water:
            cls._add_field("avoid_water", avoid_water)
        if can_breach:
            cls._add_field("can_breach", can_breach)
        if can_break_doors:
            cls._add_field("can_break_doors", can_break_doors)
        if can_float:
            cls._add_field("can_float", can_float)
        if not can_jump:
            cls._add_field("can_jump", can_jump)
        if can_open_doors:
            cls._add_field("can_open_doors", can_open_doors)
        if can_open_iron_doors:
            cls._add_field("can_open_iron_doors", can_open_iron_doors)
        if not can_pass_doors:
            cls._add_field("can_pass_doors", can_pass_doors)
        if can_path_from_air:
            cls._add_field("can_path_from_air", can_path_from_air)
        if can_path_over_lava:
            cls._add_field("can_path_over_lava", can_path_over_lava)
        if can_path_over_water:
            cls._add_field("can_path_over_water", can_path_over_water)
        if not can_sink:
            cls._add_field("can_sink", can_sink)
        if can_swim:
            cls._add_field("can_swim", can_swim)
        if not can_walk:
            cls._add_field("can_walk", can_walk)
        if can_walk_in_lava:
            cls._add_field("can_walk_in_lava", can_walk_in_lava)
        if is_amphibious:
            cls._add_field("is_amphibious", is_amphibious)
        if len(blocks_to_avoid) > 0:
            if not all(
                isinstance(block, (BlockDescriptor, str)) for block in blocks_to_avoid
            ):
                raise TypeError(
                    f"blocks_to_avoid must be a list of BlockDescriptor or Identifier instances. Component [{cls._identifier}]."
                )
                
            cls._add_field(
                "blocks_to_avoid",
                [
                    str(block)
                    for block in blocks_to_avoid
                ],
            )
        
        return cls
    
    def Climb(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_float: bool = False,
        can_jump: bool = True,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths that include vertical walls like the vanilla Spiders do."""
        navigation = _BaseComponent("navigation.climb")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation

    def Float(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths by flying around the air like the regular Ghast."""
        navigation = _BaseComponent("navigation.float")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation

    def Fly(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths in the air like the vanilla Parrots do."""
        navigation = _BaseComponent("navigation.fly")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation

    def Generic(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths by walking, swimming, flying and/or climbing around and jumping up and down a block."""
        navigation = _BaseComponent("navigation.generic")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation

    def Hover(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths in the air like the vanilla Bees do. Keeps them from falling out of the skies and doing predictive movement."""
        navigation = _BaseComponent("navigation.hover")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation

    def Swim(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths that include water."""
        navigation = _BaseComponent("navigation.swim")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation

    def Walk(
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
        can_jump: bool = True,
        can_float: bool = False,
        can_open_doors: bool = False,
        can_open_iron_doors: bool = False,
        can_pass_doors: bool = True,
        can_path_from_air: bool = False,
        can_path_over_lava: bool = False,
        can_path_over_water: bool = False,
        can_sink: bool = True,
        can_swim: bool = False,
        can_walk: bool = True,
        can_walk_in_lava: bool = False,
        is_amphibious: bool = False,
        blocks_to_avoid: list[Block | Identifier] = [],
    ):
        """Allows this entity to generate paths by walking around and jumping up and down a block like regular mobs."""
        navigation = _BaseComponent("navigation.walk")
        EntityNavigationType._basic(navigation, 
            avoid_damage_blocks,
            avoid_portals,
            avoid_sun,
            avoid_water,
            can_breach,
            can_break_doors,
            can_jump,
            can_float,
            can_open_doors,
            can_open_iron_doors,
            can_pass_doors,
            can_path_from_air,
            can_path_over_lava,
            can_path_over_water,
            can_sink,
            can_swim,
            can_walk,
            can_walk_in_lava,
            is_amphibious,
            blocks_to_avoid,
        )
        return navigation


class EntityEnvironmentSensor(_BaseComponent):
    _identifier = "minecraft:environment_sensor"

    def __init__(self) -> None:
        """Creates a trigger based on environment conditions."""
        super().__init__("environment_sensor")
        self._add_field("triggers", [])

    def trigger(self, event: Event, filters: Filter):
        self._component["triggers"].append({"filters": filters, "event": event})
        return self


class EntityPreferredPath(_BaseComponent):
    _identifier = "minecraft:preferred_path"

    def __init__(self, default_block_cost: int = 0, jump_cost: int = 0, max_fall_blocks: int = 3) -> None:
        """Specifies costing information for mobs that prefer to walk on preferred paths."""
        super().__init__("preferred_path")
        self._add_field("default_block_cost", default_block_cost)
        self._add_field("jump_cost", jump_cost)
        self._add_field("max_fall_blocks", max_fall_blocks)
        self._add_field("preferred_path_blocks", [])

    def add_blocks(self, cost: int, *blocks: list[Block | Identifier]):
        if not all(
            isinstance(block, (BlockDescriptor, str)) for block in blocks
        ):
            raise TypeError(
                f"blocks must be a list of BlockDescriptor or Identifier instances. Component [{self._identifier}]."
            )
        
        self._component["preferred_path_blocks"].append(
            {
                "cost": cost,
                "blocks": [
                    str(block)
                    for block in blocks
                ],
            }
        )
        return self


class EntityTargetNearbySensor(_BaseComponent):
    _identifier = "minecraft:target_nearby_sensor"

    def __init__(self, inside_range: int = 1, outside_range: int = 5, must_see: bool = False) -> None:
        """Defines the entity's range within which it can see or sense other entities to target them."""
        super().__init__("target_nearby_sensor")
        self._add_field("inside_range", inside_range)
        self._add_field("outside_range", outside_range)
        self._add_field("must_see", must_see)

    def on_inside_range(self, event: Event, target: FilterSubject):
        self._add_field("on_inside_range", {"event": event, "target": target.value})
        return self

    def on_outside_range(self, event: Event, target: FilterSubject):
        self._add_field("on_outside_range", {"event": event, "target": target.value})
        return self

    def on_vision_lost_inside_range(self, event: Event, target: FilterSubject):
        self._add_field("on_vision_lost_inside_range", {"event": event, "target": target.value})
        return self


class EntityRideable(_BaseComponent):
    _identifier = "minecraft:rideable"

    def __init__(
        self,
        interact_text: str = "Mount",
        controlling_seat: int = 0,
        crouching_skip_interact: bool = True,
        pull_in_entities: bool = False,
        rider_can_interact: bool = False,
        dismount_mode: RideableDismountMode = RideableDismountMode.Default,
        on_rider_enter_event: str = None,
        on_rider_exit_event: str = None,
    ) -> None:
        """Determines whether this entity can be ridden. Allows specifying the different seat positions and quantity."""
        super().__init__("rideable")
        self._seat_count = 0

        if not interact_text == "Mount":
            t = interact_text.lower().replace(" ", "_")
            self._add_field("interact_text", f"action.interact.{t}")
            ANVIL.definitions.register_lang(f"action.interact.{t}", interact_text)
        if not controlling_seat == 0:
            self._add_field("controlling_seat", controlling_seat)
        if not crouching_skip_interact:
            self._add_field("crouching_skip_interact", crouching_skip_interact)
        if pull_in_entities:
            self._add_field("pull_in_entities", pull_in_entities)
        if rider_can_interact:
            self._add_field("rider_can_interact", rider_can_interact)
        if not dismount_mode == RideableDismountMode.Default:
            self._add_field("dismount_mode", dismount_mode.value)
        if on_rider_enter_event:
            self._add_field("on_rider_enter_event", on_rider_enter_event)
        if on_rider_exit_event:
            self._add_field("on_rider_exit_event", on_rider_exit_event)

        self._add_field("seats", [])

    def add_seat(
        self,
        position: Vector3D,
        max_rider_count: int,
        min_rider_count: int = 0,
        lock_rider_rotation: int = 181,
        rotate_rider_by: int = 0,
        third_person_camera_radius: float = 1.0,
        camera_relax_distance_smoothing: float = 1.0,
    ):
        self._seat_count += 1
        self._add_field("seat_count", self._seat_count)
        third_person_camera_radius = clamp(third_person_camera_radius, 1, 64)
        camera_relax_distance_smoothing = clamp(camera_relax_distance_smoothing, 1, 32)
        self._get_field("seats", []).append(
            {
                "max_rider_count": max_rider_count,
                "position": position,
                "lock_rider_rotation": lock_rider_rotation if not lock_rider_rotation == 181 else {},
                "min_rider_count": min_rider_count if not min_rider_count == 0 else {},
                "rotate_rider_by": rotate_rider_by if not rotate_rider_by == 0 else {},
                "third_person_camera_radius": third_person_camera_radius if not third_person_camera_radius == 1.0 else {},
                "camera_relax_distance_smoothing": (
                    camera_relax_distance_smoothing if not camera_relax_distance_smoothing == 1.0 else {}
                ),
            }
        )

        return self

    def family_types(self, *families: str):
        self._add_field("family_types", families)
        return self


class EntityProjectile(_BaseComponent):
    _identifier = "minecraft:projectile"

    def __init__(
        self,
        anchor: int = 0,
        angle_offset: float = 0,
        catch_fire: bool = False,
        crit_particle_on_hurt: bool = False,
        destroy_on_hurt: bool = False,
        fire_affected_by_griefing: bool = False,
        gravity: float = 0.05,
        hit_sound: str = "",
        hit_ground_sound: str = "",
        homing: bool = False,
        inertia: float = 0.09,
        is_dangerous: bool = False,
        knockback: bool = True,
        lightning: bool = False,
        liquid_inertia: float = 0.6,
        multiple_targets: bool = True,
        offset: Coordinates = (0, 0, 0),
        on_fire_timer: float = 0.0,
        # particle: str = 'particle', Not used in game
        power: float = 1.3,
        reflect_on_hurt: bool = False,
        shoot_sound: str = "",
        shoot_target: bool = True,
        should_bounce: bool = False,
        splash_potion: bool = False,
        splash_range: int = 4,
        stop_on_hurt: bool = False,  # Determines if the projectile stops when the target is hurt.
        uncertainty_base: int = 0,  # Decimal The base accuracy. Accuracy is determined by the formula uncertaintyBase - difficultyLevel * uncertaintyMultiplier.
        uncertainty_multiplier: int = 0,  # Determines how much difficulty affects accuracy. Accuracy is determined by the formula uncertaintyBase - difficultyLevel * uncertaintyMultiplier.
    ) -> None:
        """Allows the entity to be a thrown entity."""
        super().__init__("projectile")
        if anchor != 0:
            self._add_field("anchor", anchor)
        if angle_offset != 0:
            self._add_field("angle_offset", angle_offset)
        if catch_fire:
            self._add_field("catch_fire", catch_fire)
        if crit_particle_on_hurt:
            self._add_field("crit_particle_on_hurt", crit_particle_on_hurt)
        if destroy_on_hurt:
            self._add_field("destroy_on_hurt", destroy_on_hurt)
        if fire_affected_by_griefing:
            self._add_field("fire_affected_by_griefing", fire_affected_by_griefing)
        if gravity != 0.05:
            self._add_field("gravity", gravity)
        if hit_sound != "":
            self._add_field("hit_sound", hit_sound)
        if hit_ground_sound != "":
            self._add_field("hit_ground_sound", hit_ground_sound)
        if homing:
            self._add_field("homing", homing)
        if inertia != 0.09:
            self._add_field("inertia", inertia)
        if is_dangerous:
            self._add_field("is_dangerous", is_dangerous)
        if not knockback:
            self._add_field("knockback", knockback)
        if lightning:
            self._add_field("lightning", lightning)
        if liquid_inertia != 0.6:
            self._add_field("liquid_inertia", liquid_inertia)
        if not multiple_targets:
            self._add_field("multiple_targets", multiple_targets)
        if offset != (0, 0, 0):
            self._add_field("offset", offset)
        if on_fire_timer != 0.0:
            self._add_field("on_fire_timer", on_fire_timer)
        # if particle != 'particle':
        #    self._add_field('particle', particle)
        if power != 1.3:
            self._add_field("power", power)
        if reflect_on_hurt:
            self._add_field("reflect_on_hurt", reflect_on_hurt)
        if shoot_sound != "":
            self._add_field("shoot_sound", shoot_sound)
        if not shoot_target:
            self._add_field("shoot_target", shoot_target)
        if should_bounce:
            self._add_field("should_bounce", should_bounce)
        if splash_potion:
            self._add_field("splash_potion", splash_potion)
        if splash_range != 4:
            self._add_field("splash_range", splash_range)
        if stop_on_hurt:
            self._add_field("stop_on_hurt", stop_on_hurt)
        if uncertainty_base != 0:
            self._add_field("uncertainty_base", uncertainty_base)
        if uncertainty_multiplier != 0:
            self._add_field("uncertainty_multiplier", uncertainty_multiplier)

    def filter(self, filter: Filter):
        self._add_field("filter", filter)
        return self

    def on_hit(
        self,
        catch_fire: bool = False,
        douse_fire: bool = False,
        ignite: bool = False,
        on_fire_time: float = 0,
        potion_effect: int = -1,
        spawn_aoe_cloud: bool = False,
        teleport_owner: bool = False,
    ):
        """_summary_

        Parameters:
            catch_fire (bool, optional): Determines if the struck object is set on fire. Defaults to False.
            douse_fire (bool, optional): If the target is on fire, then douse the fire. Defaults to False.
            ignite (bool, optional): Determines if a fire may be started on a flammable target. Defaults to False.
            on_fire_time (float, optional): The amount of time a target will remain on fire. Defaults to 0.
            potion_effect (int, optional): Defines the effect the arrow will apply to the entity it hits. Defaults to -1.
            spawn_aoe_cloud (bool, optional): Potion spawns an area of effect cloud. See the table below for all spawn_aoe_cloud parameters. Defaults to False.
            teleport_owner (bool, optional): Determines if the owner is transported on hit. Defaults to False.
        """
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})
        if catch_fire:
            self._component["on_hit"]["catch_fire"] = catch_fire
        if douse_fire:
            self._component["on_hit"]["douse_fire"] = douse_fire
        if ignite:
            self._component["on_hit"]["ignite"] = ignite
        if on_fire_time != 0:
            self._component["on_hit"]["on_fire_time"] = on_fire_time
        if potion_effect != -1:
            self._component["on_hit"]["potion_effect"] = potion_effect
        if spawn_aoe_cloud:
            self._component["on_hit"]["spawn_aoe_cloud"] = spawn_aoe_cloud
        if teleport_owner:
            self._component["on_hit"]["teleport_owner"] = teleport_owner
        return self

    def impact_damage(
        self,
        filter: str = None,  # The identifier of an entity that can be hit.
        catch_fire: bool = False,  # Determines if the struck object is set on fire.
        channeling: bool = True,  # Whether lightning can be channeled through the weapon.
        damage: int = 1,  # The damage dealt on impact.
        destroy_on_hit: bool = False,  # Projectile is removed on hit.
        destroy_on_hit_requires_damage: bool = True,  # If true, then the hit must cause damage to destroy the projectile.
        knockback: bool = True,  # If true, the projectile will knock back the entity it hits.
        max_critical_damage: int = 5,  # Maximum critical damage.
        min_critical_damage: int = 0,  # Minimum critical damage.
        power_multiplier: float = 2,  # How much the base damage is multiplied.
        semi_random_diff_damage: bool = False,  # If true, damage will be randomized based on damage and speed
        set_last_hurt_requires_damage: bool = False,  # If true, then the hit must cause damage to update the last hurt property.
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})
        self._component["on_hit"]["impact_damage"] = {}
        if not filter is None:
            self._component["on_hit"]["impact_damage"]["filter"] = filter
        if catch_fire:
            self._component["on_hit"]["impact_damage"]["catch_fire"] = catch_fire
        if not channeling:
            self._component["on_hit"]["impact_damage"]["channeling"] = channeling
        if damage != 1:
            self._component["on_hit"]["impact_damage"]["damage"] = damage
        if destroy_on_hit:
            self._component["on_hit"]["impact_damage"]["destroy_on_hit"] = destroy_on_hit
        if not destroy_on_hit_requires_damage:
            self._component["on_hit"]["impact_damage"][
                "destroy_on_hit_requires_damage"
            ] = destroy_on_hit_requires_damage
        if not knockback:
            self._component["on_hit"]["impact_damage"]["knockback"] = knockback
        if max_critical_damage != 5:
            self._component["on_hit"]["impact_damage"]["max_critical_damage"] = max_critical_damage
        if min_critical_damage != 0:
            self._component["on_hit"]["impact_damage"]["min_critical_damage"] = min_critical_damage
        if power_multiplier != 2:
            self._component["on_hit"]["impact_damage"]["power_multiplier"] = power_multiplier
        if semi_random_diff_damage:
            self._component["on_hit"]["impact_damage"]["semi_random_diff_damage"] = semi_random_diff_damage
        if set_last_hurt_requires_damage:
            self._component["on_hit"]["impact_damage"][
                "set_last_hurt_requires_damage"
            ] = set_last_hurt_requires_damage

        return self

    def definition_event(
        self,
        event: Event,
        target: FilterSubject,
        affect_projectile: bool = False,  # The projectile that will be affected by this event.
        affect_shooter: bool = False,  # The shooter that will be affected by this event.
        affect_splash_area: bool = False,  # All entities in the splash area will be affected by this event.
        splash_area: float = 0,  # The splash area that will be affected.
        affect_target: bool = False,  # The target will be affected by this event.
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})
        self._component["on_hit"]["definition_event"] = {"event_trigger": {"event": event, "target": target.value}}

        if affect_projectile:
            self._component["on_hit"]["definition_event"]["affect_projectile"] = affect_projectile
        if affect_shooter:
            self._component["on_hit"]["definition_event"]["affect_shooter"] = affect_shooter
        if affect_splash_area:
            self._component["on_hit"]["definition_event"]["affect_splash_area"] = affect_splash_area
        if splash_area:
            self._component["on_hit"]["definition_event"]["splash_area"] = splash_area
        if affect_target:
            self._component["on_hit"]["definition_event"]["affect_target"] = affect_target

        return self

    def spawn_aoe_cloud(
        self,
        affect_owner: bool = True,
        color: tuple[int, int, int] = (1, 1, 1),
        duration: int = 0,
        particle: int = 0,
        potion: int = -1,
        radius: int = 0,
        radius_on_use: int = -1,
        reapplication_delay: int = 0,
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["spawn_aoe_cloud"] = {}

        if not affect_owner:
            self._component["on_hit"]["spawn_aoe_cloud"]["affect_owner"] = affect_owner
        if color != (1, 1, 1):
            self._component["on_hit"]["spawn_aoe_cloud"]["color"] = color
        if duration != 0:
            self._component["on_hit"]["spawn_aoe_cloud"]["duration"] = duration
        if particle != 0:
            self._component["on_hit"]["spawn_aoe_cloud"]["particle"] = particle
        if potion != -1:
            self._component["on_hit"]["spawn_aoe_cloud"]["potion"] = potion
        if radius != 0:
            self._component["on_hit"]["spawn_aoe_cloud"]["radius"] = radius
        if radius_on_use != -1:
            self._component["on_hit"]["spawn_aoe_cloud"]["radius_on_use"] = radius_on_use
        if reapplication_delay != 0:
            self._component["on_hit"]["spawn_aoe_cloud"]["reapplication_delay"] = reapplication_delay

        return self

    def spawn_chance(
        self,
        spawn_definition: str,
        spawn_baby: bool = False,
        first_spawn_count: int = 0,
        first_spawn_percent_chance: int = 0,
        second_spawn_chance: int = 32,
        second_spawn_count: int = 0,
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["spawn_chance"] = {"spawn_definition": spawn_definition}

        if spawn_baby:
            self._component["on_hit"]["spawn_chance"]["spawn_baby"] = spawn_baby
        if first_spawn_count:
            self._component["on_hit"]["spawn_chance"]["first_spawn_count"] = first_spawn_count
        if first_spawn_percent_chance:
            self._component["on_hit"]["spawn_chance"]["first_spawn_percent_chance"] = first_spawn_percent_chance
        if second_spawn_chance:
            self._component["on_hit"]["spawn_chance"]["second_spawn_chance"] = second_spawn_chance
        if second_spawn_count:
            self._component["on_hit"]["spawn_chance"]["second_spawn_count"] = second_spawn_count

        return self

    def particle_on_hit(
        self,
        particle_type: str,
        on_other_hit: bool = False,
        on_entity_hit: bool = False,
        num_particles: int = 0,
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["particle_on_hit"] = {"particle_type": f"{particle_type}"}

        if on_other_hit:
            self._component["on_hit"]["particle_on_hit"]["on_other_hit"] = on_other_hit
        if on_entity_hit:
            self._component["on_hit"]["particle_on_hit"]["on_entity_hit"] = on_entity_hit
        if num_particles != 0:
            self._component["on_hit"]["particle_on_hit"]["num_particles"] = num_particles
        return self

    def mob_effect(
        self,
        effect: Effects,
        amplifier: int = 1,
        ambient: bool = False,
        visible: bool = False,
        duration: int = 1,
        durationeasy: int = 0,
        durationheard: int = 800,
        durationnormal: int = 200,
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["mob_effect"] = {"effect": effect.value}

        if amplifier != 1:
            self._component["on_hit"]["mob_effect"]["amplifier"] = amplifier
        if ambient:
            self._component["on_hit"]["mob_effect"]["ambient"] = ambient
        if visible:
            self._component["on_hit"]["mob_effect"]["visible"] = visible
        if duration != 1:
            self._component["on_hit"]["mob_effect"]["duration"] = duration
        if durationeasy != 0:
            self._component["on_hit"]["mob_effect"]["durationeasy"] = durationeasy
        if durationheard != 800:
            self._component["on_hit"]["mob_effect"]["durationheard"] = durationheard
        if durationnormal != 200:
            self._component["on_hit"]["mob_effect"]["durationnormal"] = durationnormal

        return self

    def freeze_on_hit(
        self,
        size: int,
        snap_to_block: bool,
        shape: str = "sphere",
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["freeze_on_hit"] = {
            "size": size,
            "snap_to_block": snap_to_block,
        }
        if shape not in ["sphere", "cube"]:
            raise RuntimeError("Unknown shape, must be sphere or cube")
        self._component["on_hit"]["freeze_on_hit"]["shape"] = shape

        return self

    def grant_xp(self, xp: tuple[int, int]):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        if xp[0] == xp[1]:
            self._component["on_hit"]["grant_xp"] = {"xp": xp}
        else:
            self._component["on_hit"]["grant_xp"] = {
                "minXP": min(xp),
                "maxXP": max(xp),
            }

        return self

    def hurt_owner(
        self,
        owner_damage: int = 0,
        knockback: bool = False,
        ignite: bool = False,
    ):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["hurt_owner"] = {}

        if owner_damage != 0:
            self._component["on_hit"]["hurt_owner"]["owner_damage"] = owner_damage
        if knockback:
            self._component["on_hit"]["hurt_owner"]["knockback"] = knockback
        if ignite:
            self._component["on_hit"]["hurt_owner"]["ignite"] = ignite

        return self

    @property
    def remove_on_hit(self):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["remove_on_hit"] = {"remove": True}

        return self

    def stick_in_ground(self, shake_time: float):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["stick_in_ground"] = {"shake_time": shake_time}

        return self

    @property
    def thrown_potion_effect(self):
        try:
            self._component["on_hit"]
        except KeyError:
            self._add_field("on_hit", {})

        self._component["on_hit"]["thrown_potion_effect"] = {}

        return self


class EntityExplode(_BaseComponent):
    _identifier = "minecraft:explode"

    def __init__(
        self,
        breaks_blocks: bool = True,
        causes_fire: bool = False,
        destroy_affected_by_griefing: bool = False,
        fire_affected_by_griefing: bool = False,
        fuse_length: tuple[float, float] = [0.0, 0.0],
        fuse_lit: bool = False,
        max_resistance: int = 3.40282e38,
        power: int = 3,
        damage_scaling: float = 1.0,
        toggles_blocks: bool = False,
        knockback_scaling: float = 1.0,
        particle_effect: ExplosionParticleEffect = ExplosionParticleEffect.Explosion,
        sound_effect: str = "explode",
        negates_fall_damage: bool = False,
        allow_underwater: bool = True,
    ) -> None:
        """Defines how the entity explodes."""
        super().__init__("explode")

        if not breaks_blocks:
            self._add_field("breaks_blocks", breaks_blocks)
        if causes_fire:
            self._add_field("causes_fire", causes_fire)
        if destroy_affected_by_griefing:
            self._add_field("destroy_affected_by_griefing", destroy_affected_by_griefing)
        if fire_affected_by_griefing:
            self._add_field("fire_affected_by_griefing", fire_affected_by_griefing)
        if fuse_length != [0.0, 0.0]:
            self._add_field("fuse_length", fuse_length)
        if fuse_lit:
            self._add_field("fuse_lit", fuse_lit)
        if max_resistance != 3.40282e38:
            self._add_field("max_resistance", max_resistance)
        if power != 3:
            self._add_field("power", power)
        if damage_scaling != 1.0:
            self._add_field("damage_scaling", damage_scaling)
        if toggles_blocks != False:
            self._add_field("toggles_blocks", toggles_blocks)
        if knockback_scaling != 1.0:
            self._add_field("knockback_scaling", knockback_scaling)
        if particle_effect is not ExplosionParticleEffect.Explosion:
            self._add_field("particle_effect", particle_effect)
        if sound_effect != "explode":
            self._add_field("sound_effect", sound_effect)
        if negates_fall_damage != False:
            self._add_field("negates_fall_damage", negates_fall_damage)
        if allow_underwater != True:
            self._add_field("allow_underwater", allow_underwater)


class EntityMobEffect(_BaseComponent):
    _identifier = "minecraft:mob_effect"

    def __init__(
        self,
        mob_effect: Effects,
        entity_filter: Filter,
        cooldown_time: int = 0,
        effect_range: float = 0.2,
        effect_time: int = 10,
    ) -> None:
        """Applies a mob effect to entities that get within range."""
        super().__init__("mob_effect")
        self._add_field("mob_effect", mob_effect.value)
        self._add_field("entity_filter", entity_filter)

        if not cooldown_time == 0:
            self._add_field("cooldown_time", cooldown_time)
        if not effect_range == 0.2:
            self._add_field("effect_range", effect_range)
        if not effect_time == 10:
            self._add_field("effect_time", effect_time)


class EntitySpawnEntity(_BaseComponent):
    _identifier = "minecraft:spawn_entity"

    def __init__(self) -> None:
        """Adds a timer after which this entity will spawn another entity or item (similar to vanilla's chicken's egg-laying behavior)."""
        super().__init__("spawn_entity")
        self._add_field("entities", [])

    def _template(
        self,
        identifier: str,
        spawn_type: str = "spawn_entity",
        spawn_event: str = "minecraft:entity_born",
        spawn_method: str = "born",
        spawn_sound: str = "plop",
        filters: Filter = None,
        max_wait_time: int = 600,
        min_wait_time: int = 300,
        num_to_spawn: int = 1,
        should_leash: bool = False,
        single_use: bool = False,
    ):
        self._component["entities"].append(
            {
                spawn_type: identifier,
                "spawn_event": spawn_event if spawn_event != "minecraft:entity_born" else {},
                "spawn_method": spawn_method if spawn_method != "born" else {},
                "spawn_sound": spawn_sound if spawn_sound != "plop" else {},
                "filters": filters if not filters is None else {},
                "max_wait_time": max_wait_time if max_wait_time != 600 else {},
                "min_wait_time": min_wait_time if min_wait_time != 300 else {},
                "num_to_spawn": num_to_spawn if num_to_spawn != 1 else {},
                "should_leash": should_leash if should_leash else {},
                "single_use": single_use if single_use else {},
            }
        )
        return self

    def spawn_entity(
        self,
        identifier: str,
        spawn_event: str = "minecraft:entity_born",
        spawn_method: str = "born",
        spawn_sound: str = "plop",
        filters: Filter = None,
        max_wait_time: int = 600,
        min_wait_time: int = 300,
        num_to_spawn: int = 1,
        should_leash: bool = False,
        single_use: bool = False,
    ):
        return self._template(
            identifier,
            "spawn_entity",
            spawn_event,
            spawn_method,
            spawn_sound,
            filters,
            max_wait_time,
            min_wait_time,
            num_to_spawn,
            should_leash,
            single_use,
        )

    def spawn_item(
        self,
        identifier: str,
        spawn_item_event: str = "minecraft:entity_born",
        spawn_method: str = "born",
        spawn_sound: str = "plop",
        filters: Filter = None,
        max_wait_time: int = 600,
        min_wait_time: int = 300,
        num_to_spawn: int = 1,
        should_leash: bool = False,
        single_use: bool = False,
    ):
        return self._template(
            identifier,
            "spawn_item",
            spawn_item_event,
            spawn_method,
            spawn_sound,
            filters,
            max_wait_time,
            min_wait_time,
            num_to_spawn,
            should_leash,
            single_use,
        )


class EntityLoot(_BaseComponent):
    _identifier = "minecraft:loot"

    def __init__(self, path) -> None:
        """Sets the loot table for what items this entity drops upon death."""
        super().__init__("loot")
        self._add_field("table", path)


class EntityShooter(_BaseComponent):
    _identifier = "minecraft:shooter"

    def __init__(
        self,
        identifier: Identifier,
        magic: bool = False,
        power: float = 0.0,
        aux_value: int = -1,
    ) -> None:
        """Defines the entity's ranged attack behavior. The "minecraft:behavior.ranged_attack" goal uses this component to determine which projectiles to shoot."""
        super().__init__("shooter")
        self._add_field("def", identifier)
        if magic:
            self._add_field("magic", magic)
        if power != 0:
            self._add_field("power", power)
        if aux_value != -1:
            self._add_field("aux_value", aux_value)


class EntityInsideBlockNotifier(_BaseComponent):
    _identifier = "minecraft:inside_block_notifier"

    def __init__(self) -> None:
        """Verifies whether the entity is inside any of the listed blocks."""
        super().__init__("inside_block_notifier")
        self._add_field("block_list", [])

    def blocks(
        self,
        block_name: Block | Identifier,
        entered_block_event: str = None,
        exited_block_event: str = None,
    ): 
        from anvil.lib.schemas import BlockDescriptor
        if not isinstance(block_name, (BlockDescriptor, str)):
            raise TypeError(
                f"block_name must be a Block or Identifier instance. Component [{self._identifier}]."
            )
        
        self._component["block_list"].append(
            {
                "block": {
                    "name": (
                        str(block_name)
                    ),
                    "states": block_name.states if isinstance(block_name, BlockDescriptor) else {},
                }
            }
        )
        if not entered_block_event is None:
            self._component["block_list"][-1]["entered_block_event"] = {
                "event": entered_block_event,
                "target": FilterSubject.Self,
            }
        if not exited_block_event is None:
            self._component["block_list"][-1]["exited_block_event"] = {
                "event": exited_block_event,
                "target": FilterSubject.Self,
            }
        return self


class EntityTransformation(_BaseComponent):
    _identifier = "minecraft:transformation"

    def __init__(
        self,
        into: Identifier,
        transform_event: str = None,
        drop_equipment: bool = False,
        drop_inventory: bool = False,
        keep_level: bool = False,
        keep_owner: bool = False,
        preserve_equipment: bool = False,
    ) -> None:
        """Defines an entity's transformation from the current definition into another."""
        super().__init__("transformation")
        self._add_field(
            "into",
            into + f"<{transform_event}>" if not transform_event is None else into,
        )
        self._add_field("add", {"component_groups": []})
        self._add_field("delay", {})
        if drop_equipment:
            self._add_field("drop_equipment", drop_equipment)
        if drop_inventory:
            self._add_field("drop_inventory", drop_inventory)
        if keep_level:
            self._add_field("keep_level", keep_level)
        if keep_owner:
            self._add_field("keep_owner", keep_owner)
        if preserve_equipment:
            self._add_field("preserve_equipment", preserve_equipment)

    def add(self, *component_groups: str):
        self._component["add"]["component_groups"].extend(component_groups)
        return self

    def begin_transform_sound(self, sound: str):
        self._add_field("begin_transform_sound", sound)
        return self

    def transformation_sound(self, sound: str):
        self._add_field("transformation_sound", sound)
        return self

    def delay(
        self,
        block_assist_chance: float = 0.0,
        block_chance: int = 0,
        block_max: int = 0,
        block_radius: int = 0,
        value: int = 0,
        block_type: list[Block | Identifier] = [],
    ):
        if not block_assist_chance == 0.0:
            self._component["delay"]["block_assist_chance"] = block_assist_chance
        if not block_chance == 0:
            self._component["delay"]["block_chance"] = block_chance
        if not block_max == 0:
            self._component["delay"]["block_max"] = block_max
        if not block_radius == 0:
            self._component["delay"]["block_radius"] = block_radius
        if not value == 0:
            self._component["delay"]["value"] = value
        if len(block_type) > 0:
            if not all(
                isinstance(block, (Block, Identifier)) for block in block_type
            ):
                raise TypeError(
                    f"block_type must be a list of Block or Identifier instances. Component [{self._identifier}]."
                )
                
            self._component["delay"]["block_type"] = [
                str(block)
                for block in block_type
            ]

        return self


class EntityNPC(_BaseComponent):
    _identifier = "minecraft:npc"

    def __init__(self, skin_list: list[int]) -> None:
        """Allows an entity to be an NPC."""
        super().__init__("npc")
        self._add_field("npc_data", {"skin_list": [{"variant": i} for i in skin_list]})

    def portrait_offsets(self, translate: Coordinates, scale: Coordinates):
        self._component["npc_data"]["portrait_offsets"] = {
            "translate": translate,
            "scale": scale,
        }
        return self

    def picker_offsets(self, translate: Coordinates, scale: Coordinates):
        self._component["npc_data"]["picker_offsets"] = {
            "translate": translate,
            "scale": scale,
        }
        return self


class EntityEquipment(_BaseComponent):
    _identifier = "minecraft:equipment"

    def __init__(self, path) -> None:
        """Sets the loot table for what items this entity drops upon death."""
        super().__init__("equipment")
        self._add_field("table", path)


class Entity_EquipItem(_BaseComponent):
    _identifier = "minecraft:equip_item"

    def __init__(self) -> None:
        """Compels the entity to equip desired equipment."""
        super().__init__("equip_item")


class EntityFireImmune(_BaseComponent):
    _identifier = "minecraft:fire_immune"

    def __init__(self) -> None:
        """Allows an entity to take 0 damage from fire."""
        super().__init__("fire_immune")


class EntityEntitySensor(_BaseComponent):
    _identifier = "minecraft:entity_sensor"

    def __init__(self, relative_range: bool = True, find_players_only: bool = False) -> None:
        super().__init__("entity_sensor")
        self._add_field("subsensors", [])
        if not relative_range:
            self._add_field("relative_range", relative_range)
        if find_players_only:
            self._add_field("find_players_only", find_players_only)

    def add_sensor(
        self,
        event: str,
        event_filters: Filter,
        maximum_count: int = -1,
        minimum_count: int = -1,
        require_all: bool = False,
        range: range = [10, 10],
        cooldown: int = -1,
        y_offset: float = 0.0,
    ):
        """A component that initiates an event when a set of conditions are met by other entities within the defined range.

        Parameters:
            event (str): Event to initiate when the conditions are met.
            event_filter (Filter): The set of conditions that must be satisfied to initiate the event.
            maximum_count (int, optional): The maximum number of entities that must pass the filter conditions for the event to send. Defaults to -1.
            minimum_count (int, optional): The minimum number of entities that must pass the filter conditions for the event to send. Defaults to -1.
            relative_range (bool, optional): If true, the sensor range is additive on top of the entity's size. Defaults to True.
            require_all (bool, optional): If true, requires all nearby entities to pass the filter conditions for the event to send. Defaults to False.
            range (range, optional): The maximum horizontal and vertical distance another entity can be from this and have the filters checked against it. Defaults to (10, 10).
            cooldown (int, optional): How many seconds should elapse before the subsensor can once again sense for entities. The cooldown is applied on top of the base 1 tick (0.05 seconds) delay. Negative values will result in no cooldown being used. Defaults to -1.
            y_offset (float, optional): Vertical offset applied to the entity's position when computing the distance from other entities.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_sensor
        """
        sensor = {}
        sensor["event"] = event
        sensor["event_filters"] = event_filters
        if maximum_count != -1:
            sensor["maximum_count"] = maximum_count
        if minimum_count != -1:
            sensor["minimum_count"] = minimum_count
        if require_all:
            sensor["require_all"] = require_all
        if range != (10, 10):
            sensor["range"] = range if isinstance(range, (tuple, list)) else (range, range)
        if cooldown != -1:
            sensor["cooldown"] = cooldown
        if y_offset != 0.0:
            sensor["y_offset"] = y_offset
        self._component["subsensors"].append(sensor)

        return self


class EntityAmbientSoundInterval(_BaseComponent):
    _identifier = "minecraft:ambient_sound_interval"

    def __init__(self, event_name: str, range: float = 16, value: float = 8) -> None:
        """A component that will set the entity's delay between playing its ambient sound.

        Parameters:
            event_name (str): Level sound event to be played as the ambient sound.
            range (float, optional): Maximum time in seconds to randomly add to the ambient sound delay time. Defaults to 16.
            value (float, optional): Minimum time in seconds before the entity plays its ambient sound again. Defaults to 8.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ambient_sound_interval
        """
        super().__init__("ambient_sound_interval")

        self._add_field("event_name", event_name)
        if range != 16:
            self._add_field("range", range)
        if value != 8:
            self._add_field("value", value)


class EntityUnderwaterMovement(_BaseComponent):
    _identifier = "minecraft:underwater_movement"

    def __init__(self, value: int) -> None:
        """A component that defines the entity's movement speed while underwater in block/tick

        Parameters:
            value (int): Movement speed of the entity while underwater in block/tick.
        """
        super().__init__("underwater_movement")
        self._add_field("value", value)


class EntityMovementMeters(_BaseComponent):
    _identifier = "minecraft:movement"

    def __init__(self, value: float, max: float = None) -> None:
        """A component that defines the entity's movement speed in meters per second.

        Parameters:
            value (float): Movement speed of the entity in meters per second.
            max (float, optional): Maximum movement speed of the entity in meters per second. Defaults to None.
        """
        super().__init__("movement")
        self._add_field("value", round(0.152 * math.sqrt(value), 2))
        if not max is None:
            self._add_field("max", round(0.152 * math.sqrt(max), 2))


class EntityInputGroundControlled(_BaseComponent):
    _identifier = "minecraft:input_ground_controlled"

    def __init__(self) -> None:
        """Allows a ridable entity the ability to be controlled using keyboard controls when ridden by a player."""
        super().__init__("input_ground_controlled")


class EntityWaterMovement(_BaseComponent):
    _identifier = "minecraft:water_movement"

    def __init__(self, drag_factor: float = 0.8) -> None:
        """Defines the speed with which an entity can move through water."""
        super().__init__("water_movement")
        if not drag_factor == 0.8:
            self._add_field("drag_factor", drag_factor)


class EntityAngry(_BaseComponent):
    _identifier = "minecraft:angry"

    def __init__(
        self,
        angry_sound: str = None,
        broadcast_anger: bool = False,
        broadcast_anger_on_attack: bool = False,
        broadcast_anger_on_being_attacked: bool = False,
        broadcast_filters: Filter = None,
        broadcast_range: int = 20,
        broadcast_targets: list[str] = [],
        duration: Seconds = 25,
        duration_delta: Seconds = 0,
        filters: Filter = None,
        sound_interval: list[Seconds] = [0, 0],
    ) -> None:
        """Defines the entity's 'angry' state using a timer.

        Parameters:
            angry_sound (str, optional): The sound event to play when the entity is angry. Defaults to None.
            broadcast_anger (bool, optional): If true, other entities of the same entity definition within the broadcast_range will also become angry. Defaults to False.
            broadcast_anger_on_attack (bool, optional): If true, other entities of the same entity definition within the broadcast_range will also become angry whenever this entity attacks. Defaults to False.
            broadcast_anger_on_being_attacked (bool, optional): If true, other entities of the same entity definition within the broadcast_range will also become angry whenever this entity is attacked. Defaults to False.
            broadcast_filters (Filter, optional): Conditions that make this entry in the list valid. Defaults to None.
            broadcast_range (int, optional): Distance in blocks where other entities of the same entity definition will become angry. Defaults to 20.
            broadcast_targets (list[str], optional): A list of entity families to broadcast anger to. Defaults to [].
            duration (Seconds, optional): The amount of time in seconds that the entity will be angry. Defaults to 25.
            duration_delta (Seconds, optional): Variance in seconds added to the duration [-delta, delta]. Defaults to 0.
            filters (Filter, optional): Filter out mob types that should not be attacked while the entity is angry (other Piglins). Defaults to None.
            sound_interval (list[Seconds], optional): The range of time in seconds to wait before playing the angry_sound again. Defaults to [0, 0].

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_angry
        """
        super().__init__("angry")
        if not angry_sound is None:
            self._add_field("angry_sound", angry_sound)
        if broadcast_anger:
            self._add_field("broadcast_anger", broadcast_anger)
        if broadcast_anger_on_attack:
            self._add_field("broadcast_anger_on_attack", broadcast_anger_on_attack)
        if broadcast_anger_on_being_attacked:
            self._add_field("broadcast_anger_on_being_attacked", broadcast_anger_on_being_attacked)
        if not broadcast_filters is None:
            self._add_field("broadcast_filters", broadcast_filters)
        if broadcast_range != 10:
            self._add_field("broadcast_range", broadcast_range)
        if not broadcast_targets == []:
            self._add_field("broadcast_targets", broadcast_targets)
        if duration != 25:
            self._add_field("duration", duration)
        if duration_delta != 0:
            self._add_field("duration_delta", duration_delta)
        if not filters is None:
            self._add_field("filters", filters)
        if not sound_interval == [0, 0]:
            self._add_field("sound_interval", sound_interval)

    def calm_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("calm_event", {"event": event, "target": target.value})
        return self


class EntityFlyingSpeed(_BaseComponent):
    _identifier = "minecraft:flying_speed"

    def __init__(self, value: int) -> None:
        """Sets the speed, in Blocks, at which the entity flies.

        Parameters:
            value (int): Flying speed in blocks per tick.
        """
        super().__init__("flying_speed")
        self._add_field("value", value)


class EntityInteract(_BaseComponent):
    _identifier = "minecraft:interact"

    def __init__(self) -> None:
        """Defines the interactions that can be used with an entity.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact
        """
        super().__init__("interact")
        self._add_field("interactions", [])

    def add_interaction(
        self,
        event: str,
        filter: Filter = None,
        add_items: str = None,
        cooldown: float = 0.0,
        cooldown_after_being_attacked: float = 0.0,
        drop_item_slot: int | Slots = -1,
        equip_item_slot: int | Slots = -1,
        health_amount: int = 0,
        hurt_item: int = 0,
        interact_text: str = None,
        play_sounds: str = None,
        spawn_entities: Identifier = None,
        spawn_items: str = None,
        swing: bool = False,
        transform_to_item: str = None,
        use_item: bool = False,
        vibration: Vibrations = Vibrations.EntityInteract,
        repair_entity_item: tuple[Slots, int] = None,
        # entity_act: str = None,
    ):
        """Adds an interaction to the entity.

        Parameters:
            event (str): Event to trigger when the interaction occurs.
            filter (Filter, optional): Filter to determine which entities can interact with this entity. Defaults to None.
            add_items (str, optional): File path, relative to the behavior Pack's path, to the loot table file. Defaults to None.
            cooldown (float, optional): Time in seconds before this entity can be interacted with again. Defaults to 0.0.
            cooldown_after_being_attacked (float, optional): Time in seconds before this entity can be interacted with after being attacked. Defaults to 0.0.
            drop_item_slot (int | Slots, optional): Slot from which the item will be dropped when interacting with this entity. Defaults to -1.
            equip_item_slot (int | Slots, optional): Slot from which the item will be equipped when interacting with this entity. Defaults to -1.
            health_amount (int, optional): The amount of health this entity will recover or hurt when interacting with this item. Negative values will harm the entity. Defaults to 0.
            hurt_item (int, optional): The amount of damage the item will take when used to interact with this entity. A value of 0 means the item won't lose durability. Defaults to 0.
            interact_text (str, optional): Text to show while playing with touch-screen controls when the player is able to interact in this way with this entity. Defaults to None.
            play_sounds (str, optional): One or more sound identifiers to play when the interaction occurs. Defaults to None.
            spawn_entities (str, optional): Entity to spawn when the interaction occurs. Defaults to None.
            spawn_items (str, optional): Loot table with items to drop on the ground upon successful interaction. Defaults to None.
            swing (bool, optional): If true, the player will do the 'swing' animation when interacting with this entity. Defaults to False.
            transform_to_item (str, optional): The item used will transform to this item upon successful interaction. Format: itemName:auxValue. Defaults to None.
            use_item (bool, optional): If true, the interaction will use an item. Defaults to False.
            vibration (str, optional): Vibration to emit when the interaction occurs. Admitted values are entity_interact (used by default), shear, and none (no vibration emitted). Defaults to None.
            repair_entity_item (tuple[Slots, int], optional): Slot and amount to repair the item used to interact with this entity. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact?view=minecraft-bedrock-stable#parameter
        """

        interaction = {
            "on_interact": {
                "filters": filter if not filter is None else {},
                "event": event,
            }
        }
        if not add_items is None:
            interaction["add_items"] = {"table": add_items}
        if not cooldown == 0.0:
            interaction["cooldown"] = cooldown
        if not cooldown_after_being_attacked == 0.0:
            interaction["cooldown_after_being_attacked"] = cooldown_after_being_attacked
        if not drop_item_slot == -1:
            interaction["drop_item_slot"] = drop_item_slot
        if not equip_item_slot == -1:
            interaction["equip_item_slot"] = equip_item_slot
        if not health_amount == 0:
            interaction["health_amount"] = health_amount
        if not hurt_item == 0:
            interaction["hurt_item"] = hurt_item
        if not interact_text is None:
            interaction["interact_text"] = interact_text
        if not play_sounds is None:
            interaction["play_sounds"] = play_sounds
        if not spawn_entities is None:
            interaction["spawn_entities"] = spawn_entities
        if not spawn_items is None:
            interaction["spawn_items"] = {"table": spawn_items}
        if swing:
            interaction["swing"] = swing
        if not transform_to_item is None:
            interaction["transform_to_item"] = transform_to_item
        if use_item:
            interaction["use_item"] = use_item
        if not vibration is Vibrations.EntityInteract:
            interaction["vibration"] = vibration.value
        if not repair_entity_item is None:
            interaction["repair_entity_item"] = {
                "slot": repair_entity_item[0],
                "repair_amount": repair_entity_item[1],
            }

        self._component["interactions"].append(interaction)
        return self

    def particle_on_start(
        self,
        particle_type: str,
        particle_offset_towards_interactor: bool = False,
        particle_y_offset: float = 0.0,
    ):
        """Adds a particle effect when the interaction starts.

        Parameters:
            particle_type (str): Name of the particle system to run.
            particle_offset_towards_interactor (bool, optional): Whether or not the particle will appear closer to who performed the interaction. Defaults to False.
            particle_y_offset (float, optional): Vertical offset of the particle system. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact?view=minecraft-bedrock-stable#particle_on_start
        """

        # add this to the last interaction, if none exists, raise an error
        if not self._component["interactions"]:
            raise ValueError("No interaction found to add the particle to.")
        else:
            self._component["interactions"][-1]["particle_on_start"] = {
                "particle_type": particle_type,
                "particle_offset_towards_interactor": particle_offset_towards_interactor,
                "particle_y_offset": particle_y_offset,
            }


class EntityAngerLevel(_BaseComponent):
    _identifier = "minecraft:anger_level"

    def __init__(
        self,
        anger_decrement_interval: Seconds = 1.0,
        angry_boost: int = 20,
        angry_threshold: int = 80,
        default_annoyingness: int = 0,
        default_projectile_annoyingness: int = 0,
        max_anger: int = 100,
        nuisance_filter: Filter = None,
        on_increase_sounds: list[dict[str, str]] = [],
        remove_targets_below_angry_threshold: bool = True,
    ) -> None:
        """Compels the entity to track anger towards a set of nuisances.

        Parameters:
            anger_decrement_interval (Seconds, optional): Anger level will decay over time. Defines how often anger towards all nuisances will decrease by one. Defaults to 1.0.
            angry_boost (int, optional): Anger boost applied to angry threshold when the entity gets angry. Defaults to 20.
            angry_threshold (int, optional): Defines when the entity is considered angry at a nuisance. Defaults to 80.
            default_annoyingness (int, optional): Specifies the amount to raise anger level with each provocation. Defaults to 0.
            default_projectile_annoyingness (int, optional): Specifies the amount to raise anger level with each projectile hit. Defaults to 0.
            max_anger (int, optional): The maximum anger level that can be reached. Applies to any nuisance. Defaults to 100.
            nuisance_filter (Filter, optional): Filter that is applied to determine if a mob can be a nuisance. Defaults to None.
            on_increase_sounds (list[dict[str, str]], optional): Sounds to play when the entity is getting provoked. Evaluated in order; the first matching condition wins. Defaults to [].
            remove_targets_below_angry_threshold (bool, optional): Defines if the entity should remove target if it falls below 'angry' threshold. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_anger_level
        """
        super().__init__("anger_level")

        if anger_decrement_interval != 1.0:
            self._add_field("anger_decrement_interval", anger_decrement_interval)
        if angry_boost != 20:
            self._add_field("angry_boost", angry_boost)
        if angry_threshold != 80:
            self._add_field("angry_threshold", angry_threshold)
        if default_annoyingness != 0:
            self._add_field("default_annoyingness", default_annoyingness)
        if default_projectile_annoyingness != 0:
            self._add_field("default_projectile_annoyingness", default_projectile_annoyingness)
        if max_anger != 100:
            self._add_field("max_anger", max_anger)
        if not nuisance_filter is None:
            self._add_field("nuisance_filter", nuisance_filter)
        if not on_increase_sounds == []:
            self._add_field("on_increase_sounds", on_increase_sounds)
        if not remove_targets_below_angry_threshold:
            self._add_field("remove_targets_below_angry_threshold", remove_targets_below_angry_threshold)


class EntityCanJoinRaid(_BaseComponent):
    _identifier = "minecraft:can_join_raid"

    def __init__(self) -> None:
        """Determines that a given entity can join an existing raid."""
        super().__init__("can_join_raid")


class EntityTameable(_BaseComponent):
    _identifier = "minecraft:tameable"

    def __init__(
        self,
        probability: float = 1.0,
        tame_event: str = None,
        tame_subject: FilterSubject = FilterSubject.Self,
        *tame_items: str,
    ) -> None:
        """Defines the rules for an entity to be tamed by the player.

        Parameters:
            probability (float, optional): The chance of taming the entity with each item use between 0.0 and 1.0, where 1.0 is 100%. Defaults to 1.0.
            tame_event (dict[str, str], optional): Event to initiate when the entity becomes tamed. Defaults to None.
            tame_items (str, optional): The list of items that can be used to tame the entity. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tameable
        """
        super().__init__("tameable")

        if probability != 1.0:
            self._add_field("probability", probability)
        if not tame_event is None:
            self._add_field("tame_event", {"event": tame_event, "target": tame_subject})
        if len(tame_items) > 0:
            self._add_field("tame_items", [str(i) for i in tame_items])


class EntityAgeable(_BaseComponent):
    _identifier = "minecraft:ageable"

    def __init__(
        self,
        duration: Seconds = 1200.0,
        grow_up_event: str = None,
        grow_up_target: FilterSubject = FilterSubject.Self,
        interact_filters: Filter = None,
        transform_to_item: str = None,
    ) -> None:
        """Adds a timer for the entity to grow up. The timer can be accelerated by giving the entity items it likes as defined by feed_items.

        Parameters:
            duration (Seconds, optional): Amount of time before the entity grows up, -1 for always a baby. Defaults to 1200.0.
            grow_up_event (str, optional): Event to initiate when the entity grows up. Defaults to None.
            interact_filters (Filter, optional): A list of conditions to meet for the entity to be fed. Defaults to None.
            transform_to_item (str, optional): The feed item used will transform into this item upon successful interaction. Format: itemName:auxValue. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ageable
        """
        super().__init__("ageable")
        self._component["feed_items"] = []

        if duration != 1200.0:
            self._add_field("duration", duration)
        if not grow_up_event is None:
            self._add_field("grow_up", {"event": grow_up_event, "target": grow_up_target})
        if not interact_filters is None:
            self._add_field("interact_filters", interact_filters)
        if not transform_to_item is None:
            self._add_field("transform_to_item", transform_to_item)

    def drop_item(self, *items: str):
        """Adds an item to the list of items the entity drops when it grows up.

        Parameters:
            item (str): The item to add to the list of items the entity drops when it grows up.

            Returns:
                Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._add_field("drop_items", items)
        return self

    def feed_items(self, *items: str):
        """Adds an item to the list of items the entity can be fed.

        Parameters:
            item (str): The item to add to the list of items the entity can be fed.

            Returns:
                Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._component["feed_items"].extend([str(i) for i in items])
        return self

    def feed_item_growth(self, item: str, growth: float):
        """Adds an item to the list of items the entity can be fed.

        Parameters:
            item (str): The item to add to the list of items the entity can be fed.
            growth (float): The amount of growth to add to the entity when fed this item.

            Returns:
                Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._component["feed_items"].append({"item": str(item), "growth": clamp(growth, 0, 1)})
        return self


class EntityInventory(_BaseComponent):
    _identifier = "minecraft:inventory"

    def __init__(
        self,
        additional_slots_per_strength: int = 0,
        can_be_siphoned_from: bool = False,
        container_type: ContainerType = ContainerType.Inventory,
        inventory_size: int = 5,
        private: bool = False,
        restrict_to_owner: bool = False,
    ) -> None:
        """Defines how an entity's inventory is managed.

        Parameters:
            additional_slots_per_strength (int, optional): Number of slots that this entity can gain per extra strength. Defaults to 0.
            can_be_siphoned_from (bool, optional): If true, the contents of this inventory can be removed by a hopper. Defaults to False.
            container_type (str, optional): Type of container the entity has. Can be horse, minecart_chest, chest_boat, minecart_hopper, inventory, container or hopper. Defaults to inventory.
            inventory_size (int, optional): Number of slots the container has. Defaults to 5.
            private (bool, optional): If true, the entity will not drop its inventory on death. Defaults to False.
            restrict_to_owner (bool, optional): If true, the entity's inventory can only be accessed by its owner or itself. Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inventory
        """
        super().__init__("inventory")

        self._add_field("container_type", container_type)
        if additional_slots_per_strength != 0:
            self._add_field("additional_slots_per_strength", additional_slots_per_strength)
        if can_be_siphoned_from:
            self._add_field("can_be_siphoned_from", can_be_siphoned_from)
        if inventory_size != 5:
            self._add_field("inventory_size", inventory_size)
        if private:
            self._add_field("private", private)
        if restrict_to_owner:
            self._add_field("restrict_to_owner", restrict_to_owner)


class EntityDash(_BaseComponent):
    _identifier = "minecraft:dash"

    def __init__(
        self,
        cooldown_time: Seconds = 1.0,
        horizontal_momentum: float = 1.0,
        vertical_momentum: float = 1.0,
    ) -> None:
        """Determines a rideable entity's ability to dash.

        Parameters:
            cooldown_time (Seconds, optional): The dash cooldown time, in seconds. Defaults to 1.0.
            horizontal_momentum (float, optional): Horizontal momentum of the dash. Defaults to 1.0.
            vertical_momentum (float, optional): Vertical momentum of the dash. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash
        """
        super().__init__("dash")

        if cooldown_time != 1.0:
            self._add_field("cooldown_time", cooldown_time)
        if horizontal_momentum != 1.0:
            self._add_field("horizontal_momentum", horizontal_momentum)
        if vertical_momentum != 1.0:
            self._add_field("vertical_momentum", vertical_momentum)


class EntityBreathable(_BaseComponent):
    _identifier = "minecraft:breathable"

    def __init__(
        self,
        breathes_air: bool = True,
        breathes_lava: bool = True,
        breathes_solids: bool = False,
        breathes_water: bool = False,
        generates_bubbles: bool = True,
        inhale_time: Seconds = 0.0,
        suffocate_time: Seconds = -20,
        total_supply: Seconds = 15,
        breathe_blocks: list[str] = [],
        non_breathe_blocks: list[str] = [],
    ) -> None:
        """Defines which blocks an entity can breathe in and defines the ability to suffocate in those blocks.

        Parameters:
            breathe_blocks (list[str], optional): List of blocks the entity can breathe in. Defaults to [].
            breathes_air (bool, optional): If true, the entity can breathe in air. Defaults to True.
            breathes_lava (bool, optional): If true, the entity can breathe in lava. Defaults to True.
            breathes_solids (bool, optional): If true, the entity can breathe in solid blocks. Defaults to False.
            breathes_water (bool, optional): If true, the entity can breathe in water. Defaults to False.
            generates_bubbles (bool, optional): If true, the entity will have visible bubbles while in water. Defaults to True.
            inhale_time (Seconds, optional): Time in seconds to recover breath to maximum. Defaults to 0.0.
            non_breathe_blocks (list[str], optional): List of blocks the entity can't breathe in, in addition to the other "breathes" parameters. Defaults to [].
            suffocate_time (int, optional): Time in seconds between suffocation damage. Defaults to -20.
            total_supply (int, optional): Time in seconds the entity can hold its breath. Defaults to 15.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breathable
        """
        super().__init__("breathable")

        if not breathes_air:
            self._add_field("breathes_air", breathes_air)
        if not breathes_lava:
            self._add_field("breathes_lava", breathes_lava)
        if breathes_solids:
            self._add_field("breathes_solids", breathes_solids)
        if breathes_water:
            self._add_field("breathes_water", breathes_water)
        if not generates_bubbles:
            self._add_field("generates_bubbles", generates_bubbles)
        if inhale_time != 0.0:
            self._add_field("inhale_time", inhale_time)
        if suffocate_time != -20:
            self._add_field("suffocate_time", suffocate_time)
        if total_supply != 15:
            self._add_field("total_supply", total_supply)
        if not breathe_blocks == []:
            self._add_field("breathe_blocks", breathe_blocks)
        if not non_breathe_blocks == []:
            self._add_field("non_breathe_blocks", non_breathe_blocks)


class EntityVariableMaxAutoStep(_BaseComponent):
    _identifier = "minecraft:variable_max_auto_step"

    def __init__(
        self,
        base_value: float = 0.5625,
        controlled_value: float = 0.5625,
        jump_prevented_value: float = 0.5625,
    ) -> None:
        """Allows entities have a maximum auto step height that is different depending on whether they are on a block that prevents jumping.

        Parameters:
            base_value (float, optional): The maximum auto step height when on any other block. Defaults to 0.5625.
            controlled_value (float, optional): The maximum auto step height when on any other block and controlled by the player. Defaults to 0.5625.
            jump_prevented_value (float, optional): The maximum auto step height when on a block that prevents jumping. Defaults to 0.5625.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variable_max_auto_step
        """
        super().__init__("variable_max_auto_step")

        if base_value != 0.5625:
            self._add_field("base_value", base_value)
        if controlled_value != 0.5625:
            self._add_field("controlled_value", controlled_value)
        if jump_prevented_value != 0.5625:
            self._add_field("jump_prevented_value", jump_prevented_value)


class EntityBuoyant(_BaseComponent):
    _identifier = "minecraft:buoyant"

    def __init__(
        self,
        liquid_blocks: list[str],
        apply_gravity: bool = True,
        base_buoyancy: float = 1.0,
        big_wave_probability: float = 0.03,
        big_wave_speed: float = 10.0,
        drag_down_on_buoyancy_removed: float = 0.0,
        simulate_waves: bool = True,
    ) -> None:
        """Allows an entity to float on the specified liquid blocks.

        Parameters:
            liquid_blocks (list[str], optional): List of blocks this entity can float on. Must be a liquid block.
            apply_gravity (bool, optional): Applies gravity each tick. Causes more of a wave simulation, but will cause more gravity to be applied outside liquids. Defaults to True.
            base_buoyancy (float, optional): Base buoyancy used to calculate how much the entity will float. Defaults to 1.0.
            big_wave_probability (float, optional): Probability of a big wave hitting the entity. Only used if simulate_waves is true. Defaults to 0.03.
            big_wave_speed (float, optional): Multiplier for the speed to make a big wave. Triggered depending on big_wave_probability. Defaults to 10.0.
            drag_down_on_buoyancy_removed (float, optional): How much an entity will be dragged down when the buoyancy component is removed. Defaults to 0.0.
            simulate_waves (bool, optional): If true, the movement simulates waves going through. Defaults to True.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_buoyant
        """
        super().__init__("buoyant")

        self._add_field("liquid_blocks", liquid_blocks)
        if not apply_gravity:
            self._add_field("apply_gravity", apply_gravity)
        if base_buoyancy != 1.0:
            self._add_field("base_buoyancy", clamp(base_buoyancy, 0, 1))
        if big_wave_probability != 0.03:
            self._add_field("big_wave_probability", big_wave_probability)
        if big_wave_speed != 10.0:
            self._add_field("big_wave_speed", big_wave_speed)
        if drag_down_on_buoyancy_removed != 0.0:
            self._add_field("drag_down_on_buoyancy_removed", drag_down_on_buoyancy_removed)
        if not simulate_waves:
            self._add_field("simulate_waves", simulate_waves)


class EntityLavaMovement(_BaseComponent):
    _identifier = "minecraft:lava_movement"

    def __init__(self, value: float) -> None:
        """Defines the speed with which an entity can move through lava."""
        super().__init__("lava_movement")
        self._add_field("value", value)


class EntityExperienceReward(_BaseComponent):
    _identifier = "minecraft:experience_reward"

    def __init__(
        self,
    ) -> None:
        """Defines the amount of experience rewarded when the entity dies or is successfully bred.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_experience_reward
        """
        super().__init__("experience_reward")

    def on_bred(self, on_bred: str | int | Molang):
        self._add_field("on_bred", on_bred)
        return self

    def on_death(self, on_death: str | int | Molang):
        self._add_field("on_death", on_death)
        return self


class EntityEquippable(_BaseComponent):
    _identifier = "minecraft:equippable"

    def __init__(self) -> None:
        """Defines an entity's behavior for having items equipped to it."""
        super().__init__("equippable")
        self._component["slots"] = []

    def slot(
        self,
        slot: int,
        item: str,
        accepted_items: list[str],
        interact_text: str = None,
        on_equip: str = None,
        on_unequip: str = None,
    ):
        """Adds a slot to the entity's equippable slots.

        Parameters:
            slot (int): The slot number of this slot.
            item (str): Identifier of the item that can be equipped for the slot.
            accepted_items (list[str]): The list of items that can fill this slot.
            interact_text (str, optional): Text to be displayed while playing with touch-screen controls when the entity can be equipped with this item. Defaults to None.
            on_equip (str, optional): Event to trigger when the entity is equipped with the item. Defaults to None.
            on_unequip (str, optional): Event to trigger when the item is removed from the entity. Defaults to None.

        Returns:
            Equippable: Returns the Equippable component to allow for method chaining.
        """
        slot_data = {
            "slot": slot,
            "item": item,
            "accepted_items": accepted_items,
        }
        if not interact_text is None:
            t = interact_text.lower().replace(" ", "_")
            slot_data["interact_text"] = f"action.interact.{t}"
            ANVIL.definitions.register_lang(f"action.interact.{t}", interact_text)
        if not on_equip is None:
            slot_data["on_equip"] = {"event": on_equip}
        if not on_unequip is None:
            slot_data["on_unequip"] = {"event": on_unequip}

        self._component["slots"].append(slot_data)
        return self


class EntityColor(_BaseComponent):
    _identifier = "minecraft:color"

    def __init__(self, value: int) -> None:
        """Defines the entity's main color.

        Parameters:
            value (int): The Palette Color value of the entity.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color
        """
        super().__init__("color")
        self._add_field("value", value)


class EntityColor2(_BaseComponent):
    _identifier = "minecraft:color2"

    def __init__(self, value: int) -> None:
        """Defines the entity's second texture color.

        Parameters:
            value (int): The Palette Color value of the entity.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color2
        """
        super().__init__("color2")
        self._add_field("value", value)


class EntityBurnsInDaylight(_BaseComponent):
    _identifier = "minecraft:burns_in_daylight"

    def __init__(self) -> None:
        """Compels an entity to burn when it's daylight.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_burns_in_daylight
        """
        super().__init__("burns_in_daylight")


class EntityBoss(_BaseComponent):
    _identifier = "minecraft:boss"

    def __init__(
        self,
        name: str,
        hud_range: int = 55,
        should_darken_sky: bool = False,
    ) -> None:
        """Defines the current state of the boss for updating the boss HUD.

        Parameters:
            name (str, optional): The name that displays above the boss's health bar.
            hud_range (int, optional): The max distance from the boss at which the boss's health bar appears on the screen. Defaults to 55.
            should_darken_sky (bool, optional): Whether the sky should darken in the presence of the boss. Defaults to False.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boss
        """
        super().__init__("boss")

        self._add_field("name", name)
        if hud_range != 55:
            self._add_field("hud_range", hud_range)
        if should_darken_sky:
            self._add_field("should_darken_sky", should_darken_sky)


class EntitySittable(_BaseComponent):
    _identifier = "minecraft:sittable"

    def __init__(
        self,
        sit_event: str = None,
        stand_event: str = None,
    ) -> None:
        """Defines the entity's 'sit' state.

        Parameters:
            sit_event (str, optional): Event to run when the entity enters the 'sit' state. Defaults to None.
            stand_event (str, optional): Event to run when the entity exits the 'sit' state. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sittable
        """
        super().__init__("sittable")

        if not sit_event is None:
            self._add_field("sit_event", {"event": sit_event})
        if not stand_event is None:
            self._add_field("stand_event", {"event": stand_event})


class EntityFlyingSpeedMeters(_BaseComponent):
    _identifier = "minecraft:flying_speed"

    def __init__(self, value: float, max: float = None) -> None:
        """A component that defines the entity's flying movement speed in meters per second.

        Parameters:
            value (float): Flying movement speed of the entity in meters per second.
            max (float, optional): Maximum flying movement speed of the entity in meters per second. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flying_speed
        """
        super().__init__("flying_speed")
        self._add_field("value", round(0.152 * math.sqrt(value), 2))
        if not max is None:
            self._add_field("max", round(0.152 * math.sqrt(max), 2))


class EntityConditionalBandwidthOptimization(_BaseComponent):
    _identifier = "minecraft:conditional_bandwidth_optimization"

    def __init__(
        self,
        max_dropped_ticks: int = 0,
        max_optimized_distance: int = 0,
        use_motion_prediction_hints: bool = False,
    ) -> None:
        """Defines the Conditional Spatial Update Bandwidth Optimizations of the entity.

        Parameters:
            max_dropped_ticks (int): In relation to the optimization value, determines the maximum ticks spatial update packets can be not sent.
            max_optimized_distance (int): The maximum distance considered during bandwidth optimizations. Any value below the max is interpolated to find optimization, and any value greater than or equal to the max results in max optimization.
            use_motion_prediction_hints (bool): When set to true, smaller motion packets will be sent during drop packet intervals, resulting in the same amount of packets being sent as without optimizations but with less data being sent. This should be used to prevent visual oddities when entities are traveling quickly or teleporting.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_conditional_bandwidth_optimization
        """
        super().__init__("conditional_bandwidth_optimization")
        a = {}
        if max_dropped_ticks != 0:
            a["max_dropped_ticks"] = max_dropped_ticks
        if max_optimized_distance != 0:
            a["max_optimized_distance"] = max_optimized_distance
        if use_motion_prediction_hints:
            a["use_motion_prediction_hints"] = use_motion_prediction_hints

        self._add_field(
            "default_values",
            a,
        )

    def conditional_values(
        self,
        max_dropped_ticks: int = 0,
        max_optimized_distance: int = 0,
        use_motion_prediction_hints: bool = False,
    ):
        a = {}
        if max_dropped_ticks != 0:
            a["max_dropped_ticks"] = max_dropped_ticks
        if max_optimized_distance != 0:
            a["max_optimized_distance"] = max_optimized_distance
        if use_motion_prediction_hints:
            a["use_motion_prediction_hints"] = use_motion_prediction_hints

        self._add_field(
            "conditional_values",
            a,
        )
        return self


class EntityItemHopper(_BaseComponent):
    _identifier = "minecraft:item_hopper"

    def __init__(
        self,
    ) -> None:
        """Allows an entity to function like a hopper block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_hopper
        """
        super().__init__("item_hopper")


class EntityBodyRotationBlocked(_BaseComponent):
    _identifier = "minecraft:body_rotation_blocked"

    def __init__(
        self,
    ) -> None:
        """When set, the entity will no longer visually rotate their body to match their facing direction.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_blocked
        """
        super().__init__("body_rotation_blocked")


class EntityDamageAbsorption(_BaseComponent):
    _identifier = "minecraft:damage_absorption"

    def __init__(self, absorbable_causes: list[DamageCause] = DamageCause.Nothing) -> None:
        """Allows an item to absorb damage that would otherwise be dealt to its wearer. The item must be equipped in an armor slot for this to happen. The absorbed damage reduces the item's durability, with any excess damage being ignored. The item must also have a minecraft:durability component.

        Parameters:
            absorbable_causes (list[str], optional): A list of damage causes that can be absorbed by the item. By default, no damage cause is absorbed.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_absorption
        """
        super().__init__("damage_absorption")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.20")

        if absorbable_causes != DamageCause.Nothing:
            self._set_value("absorbable_causes", absorbable_causes)


class EntityDimensionBound(_BaseComponent):
    _identifier = "minecraft:dimension_bound"

    def __init__(
        self,
    ) -> None:
        """Prevents the entity from changing dimension through portals.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dimension_bound
        """
        super().__init__("dimension_bound")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.40")


class EntityTransient(_BaseComponent):
    _identifier = "minecraft:transient"

    def __init__(
        self,
    ) -> None:
        """An entity with this component will NEVER persist, and will forever disappear when unloaded.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transient
        """
        super().__init__("transient")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.40")


class EntityCannotBeAttacked(_BaseComponent):
    _identifier = "minecraft:cannot_be_attacked"

    def __init__(
        self,
    ) -> None:
        """An entity with this component will NEVER be attacked by other entities.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_cannot_be_attacked
        """
        super().__init__("cannot_be_attacked")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.51")


class EntityIgnoreCannotBeAttacked(_BaseComponent):
    _identifier = "minecraft:ignore_cannot_be_attacked"

    def __init__(self, filters: Filter = None) -> None:
        """When set, blocks entities from attacking the owner entity unless they have the minecraft:ignore_cannot_be_attacked component.

        Parameters:
            filters (Filter, optional): Defines which entities are exceptions and are allowed to be attacked by the owner entity, potentially attacked entity is subject "other". If this is not specified then all attacks by the owner are allowed.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ignore_cannot_be_attacked
        """
        super().__init__("ignore_cannot_be_attacked")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.51")

        if not filters is None:
            self._add_field("filters", filters)


class EntityLookedAt(_BaseComponent):
    _identifier = "minecraft:looked_at"

    def __init__(
        self,
        field_of_view: float = 26,
        filters: Filter = None,
        find_players_only: bool = False,
        line_of_sight_obstruction_type: LineOfSightObstructionType = LineOfSightObstructionType.Collision,
        look_at_locations: list[LookAtLocation] = None,
        looked_at_cooldown: tuple[Seconds, Seconds] = (0, 0),
        looked_at_event: str = None,
        not_looked_at_event: str = None,
        scale_fov_by_distance: bool = True,
        search_radius: float = 10,
        set_target: LootedAtSetTarget = LootedAtSetTarget.OnceAndStopScanning,
    ) -> None:
        """Defines the behavior when another entity looks at the owner entity.

        Parameters:
            field_of_view (float, optional): The field of view in degrees. Defaults to 26.
            filters (Filter, optional): Defines which entities can trigger the looked_at_event. Defaults to None.
            find_players_only (bool, optional): If true, only players will trigger the looked_at_event. Defaults to False.
            line_of_sight_obstruction_type (LineOfSightObstructionType, optional): The type of obstruction to consider when checking line of sight. Defaults to LineOfSightObstructionType.Collision.
            look_at_locations (list[LookAtLocation], optional): List of locations to look at. Defaults to None.
            looked_at_cooldown (tuple[float, float], optional): The cooldown range in seconds. Defaults to (0, 0).
            looked_at_event (str, optional): Event to trigger when the entity is looked at. Defaults to None.
            not_looked_at_event (str, optional): Event to trigger when the entity is no longer looked at. Defaults to None.
            scale_fov_by_distance (bool, optional): If true, the field of view will be scaled based on the distance between the entities. Defaults to True.
            search_radius (float, optional): The radius in blocks to search for entities. Defaults to 10.
            set_target (LootedAtSetTarget, optional): The target selection strategy. Defaults to LootedAtSetTarget.OnceAndStopScanning.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_looked_at
        """
        super().__init__("looked_at")

        if field_of_view != 26:
            self._add_field("field_of_view", field_of_view)
        if filters is not None:
            self._add_field("filters", filters)
        if find_players_only:
            self._add_field("find_players_only", find_players_only)
        if line_of_sight_obstruction_type != LineOfSightObstructionType.Collision:
            self._add_field("line_of_sight_obstruction_type", line_of_sight_obstruction_type)
        if look_at_locations is not None:
            self._add_field("look_at_locations", look_at_locations)
        if looked_at_cooldown != (0, 0):
            self._add_field("looked_at_cooldown", looked_at_cooldown)
        if looked_at_event is not None:
            self._add_field("looked_at_event", looked_at_event)
        if not_looked_at_event is not None:
            self._add_field("not_looked_at_event", not_looked_at_event)
        if not scale_fov_by_distance:
            self._add_field("scale_fov_by_distance", scale_fov_by_distance)
        if search_radius != 10:
            self._add_field("search_radius", search_radius)
        if set_target != LootedAtSetTarget.OnceAndStopScanning:
            self._add_field("set_target", set_target)


class EntityMovementSoundDistanceOffset(_BaseComponent):
    _identifier = "minecraft:movement_sound_distance_offset"

    def __init__(self, value: float) -> None:
        """Sets the offset used to determine the next step distance for playing a movement sound.

        Parameters:
            value (float): The higher the number, the less often the movement sound will be played.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.sound_distance_offset
        """
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.60")
        super().__init__("movement_sound_distance_offset")
        self._add_field("value", value)


class EntityRendersWhenInvisible(_BaseComponent):
    _identifier = "minecraft:renders_when_invisible"

    def __init__(self) -> None:
        """When set, the entity will render even when invisible. Appropriate rendering behavior can then be specified in the corresponding "minecraft:client_entity".

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_renders_when_invisible
        """
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.60")
        super().__init__("renders_when_invisible")


class EntityBreedable(_BaseComponent):
    _identifier = "minecraft:breedable"

    def __init__(
        self,
        allow_sitting: bool = False,
        blend_attributes: bool = True,
        breed_cooldown: Seconds = 60,
        breed_items: list[str] = None,
        causes_pregnancy: bool = False,
        combine_parent_colors: bool = None,
        extra_baby_chance: float = 0,
        inherit_tamed: bool = True,
        love_filters: Filter = None,
        mutation_strategy: BreedingMutationStrategy = BreedingMutationStrategy.None_,
        parent_centric_attribute_blending: list[_BaseComponent] = None,
        property_inheritance: list[str] = None,
        random_extra_variant_mutation_interval: tuple[int, int] = (0, 0),
        random_variant_mutation_interval: tuple[int, int] = (0, 0),
        require_full_health: bool = False,
        require_tame: bool = True,
        transform_to_item: str = None,
    ) -> None:
        """Allows an entity to get into the 'love' state used for breeding.

        Commonly used in conjunction with the 'minecraft:behavior.breed' component.

        Breedable Properties:
            - allow_sitting: If true, entities can breed while sitting.
            - blend_attributes: If true, parent attributes will be blended for the offspring.
            - breed_cooldown: Time in seconds before the entity can breed again.
            - breed_items: The list of items that can trigger the 'love' state.
            - causes_pregnancy: If true, the entity becomes pregnant instead of spawning a baby.
            - combine_parent_colors: If true, parent's colors blend in the offspring.
            - extra_baby_chance: Chance that up to 16 babies will spawn.
            - inherit_tamed: If true, babies will inherit the tamed state.
            - love_filters: Filters to run when attempting to enter the love state.
            - mutation_strategy: Strategy used for mutating variants ('random' or 'none').
            - parent_centric_attribute_blending: List of attributes to blend from parents.
            - property_inheritance: List of entity properties inherited from parents.
            - random_extra_variant_mutation_interval: Interval for extra variant mutation.
            - random_variant_mutation_interval: Interval for variant mutation.
            - require_full_health: If true, entity must be at full health to breed.
            - require_tame: If true, entity must be tamed to breed.
            - transform_to_item: Breed item used will transform to this item on use.
        """
        super().__init__("breedable")

        if allow_sitting:
            self._add_field("allow_sitting", allow_sitting)
        if blend_attributes is not True:
            self._add_field("blend_attributes", blend_attributes)
        if breed_cooldown != 60:
            self._add_field("breed_cooldown", breed_cooldown)
        if breed_items is not None:
            self._add_field("breed_items", breed_items)
        if causes_pregnancy:
            self._add_field("causes_pregnancy", causes_pregnancy)
        if combine_parent_colors is not None:
            self._add_field("combine_parent_colors", combine_parent_colors)
        if extra_baby_chance != 0:
            self._add_field("extra_baby_chance", extra_baby_chance)
        if inherit_tamed is not True:
            self._add_field("inherit_tamed", inherit_tamed)
        if love_filters is not None:
            self._add_field("love_filters", love_filters)
        if mutation_strategy != BreedingMutationStrategy.None_:
            self._add_field("mutation_strategy", mutation_strategy.value)
        if parent_centric_attribute_blending is not None:
            self._add_field(
                "parent_centric_attribute_blending", [c.identifier for c in parent_centric_attribute_blending]
            )
        if property_inheritance is not None:
            self._add_field(
                "property_inheritance", [f"{CONFIG.NAMESPACE}:{property}" for property in property_inheritance]
            )
        if random_extra_variant_mutation_interval != (0, 0):
            self._add_field("random_extra_variant_mutation_interval", random_extra_variant_mutation_interval)
        if random_variant_mutation_interval != (0, 0):
            self._add_field("random_variant_mutation_interval", random_variant_mutation_interval)
        if require_full_health:
            self._add_field("require_full_health", require_full_health)
        if require_tame is not True:
            self._add_field("require_tame", require_tame)
        if transform_to_item is not None:
            self._add_field("transform_to_item", transform_to_item)

    def breeds_with(self, mate_type: str, baby_type: str, breed_event: str) -> dict:
        """Defines the breeding partner for the entity.

        Parameters:
            mate_type (str): The entity type of the breeding partner.
            baby_type (str): The entity type of the offspring.
            breed_event (str): The event to trigger when breeding occurs.

        Returns:
            dict: A dictionary containing the breeding information.
        """

        self._add_field(
            "breeds_with",
            {
                "mate_type": mate_type,
                "baby_type": baby_type,
                "breed_event": breed_event,
            },
        )
        return self

    def deny_parents_variant(self, chance: float, min_variant: str, max_variant: str) -> dict:
        """Defines the chance of denying the parents' variant.

        Parameters:
            chance (float): The percentage chance of denying the parents' variant.
            min_variant (str): The inclusive minimum of the variant range.
            max_variant (str): The inclusive maximum of the variant range.

        Returns:
            dict: A dictionary containing the deny parents variant information.
        """
        self._add_field(
            "deny_parents_variant",
            {
                "chance": chance,
                "min_variant": min_variant,
                "max_variant": max_variant,
            },
        )
        return self

    def environment_requirements(self, block_types: list[str], count: int, radius: float) -> dict:
        """Defines the nearby block requirements for breeding.

        Parameters:
            block_types (list[str]): The block types required nearby for breeding.
            count (int): The number of required block types nearby for breeding.
            radius (float): The radius in blocks to search for the required blocks.

        Returns:
            dict: A dictionary containing the environment requirements information.
        """
        self._add_field(
            "environment_requirements",
            {
                "block_types": block_types,
                "count": count,
                "radius": clamp(radius, 0, 16),
            },
        )
        return self

    def mutation_factor(self, color: float, extra_variant: float, variant: float) -> dict:
        """Defines the mutation factor for the entity.

        Parameters:
            color (float): The percentage chance of denying the parents' variant.
            extra_variant (float): The percentage chance of a mutation on the entity's extra variant type.
            variant (float): The percentage chance of a mutation on the entity's variant type.

        Returns:
            dict: A dictionary containing the mutation factor information.
        """
        self._add_field(
            "mutation_factor",
            {
                "color": clamp(color, 0, 1),
                "extra_variant": clamp(extra_variant, 0, 1),
                "variant": clamp(variant, 0, 1),
            },
        )
        return self


class EntityIsCollidable(_BaseComponent):
    _identifier = "minecraft:is_collidable"

    def __init__(self) -> None:
        """Allows other mobs to have vertical and horizontal collisions with this mob.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_collidable
        """
        super().__init__("is_collidable")


class EntityBodyRotationAxisAligned(_BaseComponent):
    _identifier = "minecraft:body_rotation_axis_aligned"

    def __init__(self) -> None:
        """Causes the entity's body to automatically rotate to align with the nearest cardinal direction based on its current facing direction.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_axis_aligned
        """
        super().__init__("body_rotation_axis_aligned")


class EntityInputAirControlled(_BaseComponent):
    _identifier = "minecraft:input_air_controlled"

    def __init__(
        self,
        backwards_movement_modifier: float = 0.5,
        strafe_speed_modifier: float = 0.4,
    ) -> None:
        """Allows a rideable entity to be controlled in the air using WASD and mouse controls.

        Only available with "use_beta_features": true and may be drastically changed or removed.

        Parameters:
            backwards_movement_modifier (float, optional): Modifies speed when moving backwards. Defaults to 0.5.
            strafe_speed_modifier (float, optional): Modifies the strafe speed. Defaults to 0.4.
        """
        super().__init__("input_air_controlled")
        if backwards_movement_modifier != 0.5:
            self._add_field("backwards_movement_modifier", backwards_movement_modifier)
        if strafe_speed_modifier != 0.4:
            self._add_field("strafe_speed_modifier", strafe_speed_modifier)


class EntityLeashable(_BaseComponent):
    _identifier = "minecraft:leashable"

    def __init__(
        self,
        can_be_cut: bool = True,
        can_be_stolen: bool = True,
        hard_distance: int = 6,
        max_distance: int = None,
        soft_distance: int = 4,
    ) -> None:
        """Defines how this mob can be leashed to other items.

        Parameters:
            can_be_cut (bool, optional): If true, players can cut both incoming and outgoing leashes by using shears on the entity. Defaults to True.
            can_be_stolen (bool, optional): If true, players can leash this entity even if it is already leashed to another entity. Defaults to True.
            hard_distance (int, optional): Distance in blocks at which the leash stiffens, restricting movement. Defaults to 6.
            max_distance (int, optional): Distance in blocks at which the leash breaks. Defaults to None.
            soft_distance (int, optional): Distance in blocks at which the 'spring' effect starts acting to keep this entity close to the entity that leashed it. Defaults to 4.

        [Documentation reference]: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable
        """
        super().__init__("leashable")

        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.70")

        if not can_be_cut:
            self._add_field("can_be_cut", can_be_cut)
        if not can_be_stolen:
            self._add_field("can_be_stolen", can_be_stolen)
        if hard_distance != 6:
            self._add_field("hard_distance", hard_distance)
        if max_distance is not None:
            self._add_field("max_distance", max_distance)
        if soft_distance != 4:
            self._add_field("soft_distance", soft_distance)

    def on_leash(self, event: str, target: FilterSubject = FilterSubject.Self) -> dict:
        self._add_field("on_leash", {"event": event, "target": target})
        return self

    def on_unleash(self, event: str, interact_only: bool = False, target: FilterSubject = FilterSubject.Self) -> dict:
        """Defines the event to trigger when the entity is unleashed.

        Parameters:
            event (str): The event to trigger when the entity is unleashed.
            interact_only (bool, optional): If true, the event will only trigger when the player directly interacts with the entity. Defaults to False.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        Returns:
            dict: A dictionary containing the unleash information.
        """

        self._add_field("on_unleash", {"event": event, "target": target})
        if interact_only:
            self._add_field("on_unleash_interact_only", interact_only)
        return self

    def preset(
        self,
        filter: Filter = None,
        hard_distance: int = 7,
        max_distance: int = 12,
        rotation_adjustment: float = 0,
        soft_distance: float = 4,
        spring_type: LeashSpringType = LeashSpringType.Dampened,
    ) -> dict:
        """Defines a preset for the leashable component.

        Parameters:
            filter (Filter, optional): Conditions that must be met for this preset to be applied. Defaults to None.
            hard_distance (int, optional): Distance (in blocks) over which the entity starts being pulled toward the leash holder with a spring-like force. Defaults to 7.
            max_distance (int, optional): Distance in blocks at which the leash breaks. Defaults to 12.
            rotation_adjustment (float, optional): Adjusts the rotation at which the entity reaches equilibrium. Defaults to 0.
            soft_distance (float, optional): Distance (in blocks) over which the entity begins pathfinding toward the leash holder. Defaults to 4.
            spring_type (LeashSpringType, optional): Defines the type of spring-like force that pulls the entity towards its leash holder. Defaults to LeashSpringType.Dampened.

        Returns:
            dict: A dictionary containing the preset information.
        """
        a = {}
        if not filter is None:
            a["filter"] = filter
        if hard_distance != 7:
            a["hard_distance"] = hard_distance
        if max_distance != 12:
            a["max_distance"] = max_distance
        if rotation_adjustment != 0:
            a["rotation_adjustment"] = rotation_adjustment
        if soft_distance != 4:
            a["soft_distance"] = soft_distance
        if spring_type != LeashSpringType.Dampened:
            a["spring_type"] = spring_type.value

        self._add_field("presets", [a])
        return self


class EntityBodyRotationAlwaysFollowsHead(_BaseComponent):
    _identifier = "minecraft:body_rotation_always_follows_head"

    def __init__(self) -> None:
        """Causes the entity's body to always be automatically rotated to align with the entity's head. Does not override the "minecraft:body_rotation_blocked" component.
        
        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_always_follows_head
        """
        super().__init__("body_rotation_always_follows_head")

# AI Goals ==========================================================================


class EntityAINearestAttackableTarget(_ai_goal):
    _identifier = "minecraft:behavior.nearest_attackable_target"

    def __init__(
        self,
        attack_interval: int = 0,
        attack_interval_min: int = 0,
        attack_owner: bool = False,
        must_reach: bool = False,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        persist_time: float = 0.0,
        # reevaluate_description: bool = False,
        reselect_targets: bool = False,
        scan_interval: int = 10,
        set_persistent: bool = False,
        target_invisible_multiplier: float = 0.7,
        target_search_height: float = -0.1,
        target_sneak_visibility_multiplier: float = 0.8,
        within_radius: float = 0.0,
    ) -> None:
        """Allows an entity to attack the closest target within a given subset of specific target types."""
        super().__init__("behavior.nearest_attackable_target")
        self._add_field("entity_types", [])

        if not attack_interval == 0:
            self._add_field("attack_interval", attack_interval)
        if not attack_interval_min == 0:
            self._add_field("attack_interval_min", attack_interval_min)
        if attack_owner:
            self._add_field("attack_owner", attack_owner)
        if must_reach:
            self._add_field("must_reach", must_reach)
        if must_see:
            self._add_field("must_see", must_see)
        if not must_see_forget_duration == 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if not persist_time == 0.0:
            self._add_field("persist_time", persist_time)
        # if reevaluate_description: self._add_field("reevaluate_description", reevaluate_description)
        if reselect_targets:
            self._add_field("reselect_targets", reselect_targets)
        if not scan_interval == 10:
            self._add_field("scan_interval", scan_interval)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if not target_invisible_multiplier == 0.7:
            self._add_field("target_invisible_multiplier", target_invisible_multiplier)
        if not target_search_height == -0.1:
            self._add_field("target_search_height", target_search_height)
        if not target_sneak_visibility_multiplier == 0.8:
            self._add_field("target_sneak_visibility_multiplier", target_sneak_visibility_multiplier)
        if not within_radius == 0.0:
            self._add_field("within_radius", within_radius)

    def add_target(
        self,
        filters: Filter,
        cooldown: int = 0,
        max_dist: int = 32,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        # empty dicts will be removed at compilation
        self._component["entity_types"].append(
            {
                "filters": filters,
                "cooldown": cooldown if cooldown > 0 else {},
                "max_dist": max_dist if max_dist != 32 else {},
                "must_see": must_see if must_see else {},
                "must_see_forget_duration": must_see_forget_duration if must_see_forget_duration != 3.0 else {},
                "sprint_speed_multiplier": sprint_speed_multiplier if sprint_speed_multiplier != 1.0 else {},
                "walk_speed_multiplier": walk_speed_multiplier if walk_speed_multiplier != 1.0 else {},
            }
        )
        return self


class EntityAINearestPrioritizedAttackableTarget(_ai_goal):
    _identifier = "minecraft:behavior.nearest_prioritized_attackable_target"

    def __init__(
        self,
        attack_interval: int = 0,
        attack_interval_min: int = 0,
        attack_owner: bool = False,
        must_reach: bool = False,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        persist_time: float = 0.0,
        reevaluate_description: bool = False,
        reselect_targets: bool = False,
        scan_interval: int = 10,
        set_persistent: bool = False,
        target_invisible_multiplier: float = 0.7,
        target_search_height: float = -0.1,
        target_sneak_visibility_multiplier: float = 0.8,
        within_radius: float = 0.0,
    ) -> None:
        """Allows an entity to attack the closest target within a given subset of specific target types."""
        super().__init__("behavior.nearest_prioritized_attackable_target")
        self._add_field("entity_types", [])

        if not attack_interval == 0:
            self._add_field("attack_interval", attack_interval)
        if not attack_interval_min == 0:
            self._add_field("attack_interval_min", attack_interval_min)
        if attack_owner:
            self._add_field("attack_owner", attack_owner)
        if must_reach:
            self._add_field("must_reach", must_reach)
        if must_see:
            self._add_field("must_see", must_see)
        if not must_see_forget_duration == 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if not persist_time == 0.0:
            self._add_field("persist_time", persist_time)
        if reevaluate_description:
            self._add_field("reevaluate_description", reevaluate_description)
        if reselect_targets:
            self._add_field("reselect_targets", reselect_targets)
        if not scan_interval == 10:
            self._add_field("scan_interval", scan_interval)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if not target_invisible_multiplier == 0.7:
            self._add_field("target_invisible_multiplier", target_invisible_multiplier)
        if not target_search_height == -0.1:
            self._add_field("target_search_height", target_search_height)
        if not target_sneak_visibility_multiplier == 0.8:
            self._add_field("target_sneak_visibility_multiplier", target_sneak_visibility_multiplier)
        if not within_radius == 0.0:
            self._add_field("within_radius", within_radius)

    def add_target(
        self,
        filters: Filter,
        cooldown: int = 0,
        max_dist: int = 32,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        # empty dicts will be removed at compilation
        self._component["entity_types"].append(
            {
                "filters": filters,
                "cooldown": cooldown if cooldown > 0 else {},
                "max_dist": max_dist if max_dist != 32 else {},
                "must_see": must_see if must_see else {},
                "must_see_forget_duration": must_see_forget_duration if must_see_forget_duration != 3.0 else {},
                "sprint_speed_multiplier": sprint_speed_multiplier if sprint_speed_multiplier != 1.0 else {},
                "walk_speed_multiplier": walk_speed_multiplier if walk_speed_multiplier != 1.0 else {},
            }
        )
        return self


class EntityAITimer(_ai_goal):
    _identifier = "minecraft:timer"

    def __init__(
        self,
        event: Event,
        target: FilterSubject = FilterSubject.Self,
        looping: bool = True,
        randomInterval: bool = True,
        time: tuple[float, float] | float = 0,
    ) -> None:
        """Adds a timer after which an event will fire."""
        super().__init__("timer")

        self._add_field("time_down_event", {"event": event, "target": target.value})

        if not looping:
            self._add_field("looping", looping)
        if not randomInterval:
            self._add_field("randomInterval", randomInterval)
        if not time == (0, 0):
            self._add_field("time", time)


class EntityAIKnockbackRoar(_ai_goal):
    _identifier = "minecraft:behavior.knockback_roar"

    def __init__(
        self,
        attack_time: float = 0.5,
        cooldown_time: float = 0.1,
        damage_filters: Filter = None,
        duration: float = 1,
        knockback_damage: int = 6,
        knockback_filters: Filter = None,
        knockback_height_cap: float = 0.4,
        knockback_horizontal_strength: int = 4,
        knockback_range: int = 4,
        knockback_vertical_strength: int = 4,
    ) -> None:
        """Compels an entity to emit a roar effect that knocks back other entities in a set radius from where the roar was emitted."""
        super().__init__("behavior.knockback_roar")

        if not attack_time == 0.5:
            self._add_field("attack_time", attack_time)
        if not cooldown_time == 0.1:
            self._add_field("cooldown_time", cooldown_time)
        if not damage_filters is None:
            self._add_field("damage_filters", damage_filters)
        if not duration == 1:
            self._add_field("duration", duration)
        if not knockback_damage == 6:
            self._add_field("knockback_damage", knockback_damage)
        if not knockback_filters is None:
            self._add_field("knockback_filters", knockback_filters)
        if not knockback_height_cap == 0.4:
            self._add_field("knockback_height_cap", knockback_height_cap)
        if not knockback_horizontal_strength == 4:
            self._add_field("knockback_horizontal_strength", knockback_horizontal_strength)
        if not knockback_range == 4:
            self._add_field("knockback_range", knockback_range)
        if not knockback_vertical_strength == 4:
            self._add_field("knockback_vertical_strength", knockback_vertical_strength)

    def on_roar_end(self, on_roar_end: str):
        self._add_field("on_roar_end", {"event": on_roar_end})
        return self


class EntityAIFloat(_ai_goal):
    _identifier = "minecraft:behavior.float"

    def __init__(self, sink_with_passengers: bool = False) -> None:
        """Allows an entity to float on water. Passengers will be kicked out the moment the mob's head goes underwater, which may not happen for tall mobs."""
        super().__init__("behavior.float")
        if sink_with_passengers:
            self._add_field("sink_with_passengers", sink_with_passengers)


class EntityAIRandomStroll(_ai_goal):
    _identifier = "minecraft:behavior.random_stroll"

    def __init__(
        self,
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Compels an entity to choose a random direction to walk towards.

        Parameters:
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the entity when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the entity will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the entity will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_stroll
        """
        super().__init__("behavior.random_stroll")
        if interval != 120:
            self._add_field("interval", interval)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", max(1, xz_dist))
        if y_dist != 7:
            self._add_field("y_dist", max(1, y_dist))


class EntityAILookAtPlayer(_ai_goal):
    _identifier = "minecraft:behavior.look_at_player"

    def __init__(
        self,
        angle_of_view_horizontal: int = 360,
        angle_of_view_vertical: int = 360,
        look_distance: float = 8.0,
        look_time: tuple[int, int] = (2, 4),
        probability: float = 0.02,
        target_distance: float = 0.6,
    ) -> None:
        """Compels an entity to look at the player by rotating the head bone pose within a set limit."""
        super().__init__("behavior.look_at_player")
        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time != (2, 4):
            self._add_field("look_time", look_time)
        if probability != 0.02:
            self._add_field("probability", probability)
        if target_distance != 0.6:
            self._add_field("target_distance", target_distance)


class EntityAIRandomLookAround(_ai_goal):
    _identifier = "minecraft:behavior.random_look_around"

    def __init__(
        self,
        angle_of_view_horizontal: int = 360,
        angle_of_view_vertical: int = 360,
        look_distance: float = 8.0,
        look_time: tuple[int, int] = (2, 4),
        probability: float = 0.02,
        target_distance: float = 0.6,
    ) -> None:
        """Compels an entity to choose a random direction to look in for a random duration within a range."""
        super().__init__("behavior.random_look_around")
        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time != (2, 4):
            self._add_field("look_time", look_time)
        if probability != 0.02:
            self._add_field("probability", probability)
        if target_distance != 0.6:
            self._add_field("target_distance", target_distance)


class EntityAIHurtByTarget(_ai_goal):
    _identifier = "minecraft:behavior.hurt_by_target"

    def __init__(
        self,
        alert_same_type: bool = False,
        entity_types: Filter = None,
        max_dist: int = 16,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
        hurt_owner: bool = False,
    ) -> None:
        """Compels an entity to react when hit by set target."""
        super().__init__("behavior.hurt_by_target")

        if alert_same_type:
            self._add_field("alert_same_type", alert_same_type)
        if entity_types != None:
            self._add_field("entity_types", {"filters": entity_types})
        if max_dist != 16:
            self._add_field("max_dist", max_dist)
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if reevaluate_description:
            self._add_field("reevaluate_description", reevaluate_description)
        if sprint_speed_multiplier != 1.0:
            self._add_field("sprint_speed_multiplier", sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            self._add_field("walk_speed_multiplier", walk_speed_multiplier)
        if hurt_owner:
            self._add_field("hurt_owner", hurt_owner)


class EntityAIMeleeAttack(_ai_goal):
    _identifier = "minecraft:behavior.melee_attack"

    def __init__(
        self,
        attack_once: bool = False,
        cooldown_time: int = 1,
        inner_boundary_time_increase: float = 0.25,
        max_path_time: float = 0.55,
        melee_fov: int = 90,
        min_path_time: float = 0.2,
        outer_boundary_time_increase: float = 0.5,
        path_fail_time_increase: float = 0.75,
        path_inner_boundary: int = 16,
        path_outer_boundary: int = 32,
        random_stop_interval: int = 0,
        reach_multiplier: int = 2,
        require_complete_path: bool = False,
        # set_persistent: bool = False,
        speed_multiplier: float = 1,
        track_target: bool = False,
        x_max_rotation: int = 30,
        y_max_head_rotation: int = 30,
        can_spread_on_fire: bool = False,
    ) -> None:
        """Compels entities to make close combat melee attacks."""
        super().__init__("behavior.melee_attack")
        if attack_once:
            self._add_field("attack_once", attack_once)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if inner_boundary_time_increase != 0.75:
            self._add_field("inner_boundary_time_increase", inner_boundary_time_increase)
        if max_path_time != 0.75:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if outer_boundary_time_increase != 0.5:
            self._add_field("outer_boundary_time_increase", outer_boundary_time_increase)
        if path_fail_time_increase != 0.75:
            self._add_field("path_fail_time_increase", path_fail_time_increase)
        if path_inner_boundary != 16:
            self._add_field("path_inner_boundary", path_inner_boundary)
        if path_outer_boundary != 32:
            self._add_field("path_outer_boundary", path_outer_boundary)
        if random_stop_interval != 0:
            self._add_field("random_stop_interval", random_stop_interval)
        if reach_multiplier != 2:
            self._add_field("reach_multiplier", reach_multiplier)
        if require_complete_path:
            self._add_field("require_complete_path", require_complete_path)
        # if set_persistent:
        #    self._add_field("set_persistent", set_persistent)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if track_target:
            self._add_field("track_target", track_target)
        if x_max_rotation != 30:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation != 30:
            self._add_field("y_max_head_rotation", y_max_head_rotation)
        if can_spread_on_fire:
            self._add_field("can_spread_on_fire", can_spread_on_fire)

    def attack_types(self, attack_types: str):
        self._add_field("attack_types", attack_types)
        return self

    def on_attack(self, on_attack: Event):
        self._add_field("on_attack", on_attack)
        return self

    def on_kill(self, on_kill: str, subject: FilterSubject = FilterSubject.Self, filter: Filter = None):
        self._add_field(
            "on_kill", {"event": on_kill, "filters": filter if not filter is None else {}, "target": subject}
        )


class EntityAIRangedAttack(_ai_goal):
    _identifier = "minecraft:behavior.ranged_attack"

    def __init__(
        self,
        attack_interval: int = 0,
        attack_interval_max: int = 0,
        attack_interval_min: int = 0,
        attack_radius: int = 0,
        attack_radius_min: int = 0,
        burst_interval: int = 0,
        burst_shots: int = 1,
        charge_charged_trigger: int = 0,
        charge_shoot_trigger: int = 0,
        ranged_fov: int = 90,
        set_persistent: bool = False,
        speed_multiplier: int = 1,
        swing: bool = False,
        target_in_sight_time: int = 1,
        x_max_rotation: int = 30,
        y_max_head_rotation: int = 30,
    ) -> None:
        """Allows an entity to attack by using ranged shots. charge_shoot_trigger must be greater than 0 to enable charged up burst-shot attacks. Requires minecraft:shooter to define projectile behavior."""
        super().__init__("behavior.ranged_attack")

        if attack_interval != 0:
            self._add_field("attack_interval", attack_interval)
        if attack_interval_max != 0:
            self._add_field("attack_interval_max", attack_interval_max)
        if attack_interval_min != 0:
            self._add_field("attack_interval_min", attack_interval_min)
        if attack_radius != 0:
            self._add_field("attack_radius", attack_radius)
        if attack_radius_min != 0:
            self._add_field("attack_radius_min", attack_radius_min)
        if burst_interval != 0:
            self._add_field("burst_interval", burst_interval)
        if burst_shots != 1:
            self._add_field("burst_shots", burst_shots)
        if charge_charged_trigger != 0:
            self._add_field("charge_charged_trigger", charge_charged_trigger)
        if charge_shoot_trigger != 0:
            self._add_field("charge_shoot_trigger", charge_shoot_trigger)
        if ranged_fov != 90:
            self._add_field("ranged_fov", ranged_fov)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if swing:
            self._add_field("swing", swing)
        if target_in_sight_time != 1:
            self._add_field("target_in_sight_time", target_in_sight_time)
        if x_max_rotation != 30:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation != 30:
            self._add_field("y_max_head_rotation", y_max_head_rotation)


class EntityAISummonEntity(_ai_goal):
    _identifier = "minecraft:behavior.summon_entity"

    def __init__(self) -> None:
        """compels an entity to attack other entities by summoning new entities."""
        super().__init__("behavior.summon_entity")
        self._add_field("summon_choices", [])

    def summon_choice(
        self,
        cast_duration: int,
        cooldown_time: int = 0,
        do_casting: bool = True,
        filters: Filter = None,
        max_activation_range: float = 32.0,
        min_activation_range: float = 1,
        particle_color: int = 0,
        start_sound_event: str = None,
        weight: int = 1,
    ):
        self._component["summon_choices"].append(
            {
                "cast_duration": cast_duration,
                "cooldown_time": cooldown_time if cooldown_time != 0 else {},
                "do_casting": do_casting if not do_casting else {},
                "filters": filters if not filters is None != 0 else {},
                "max_activation_range": max_activation_range if max_activation_range != 32 else {},
                "min_activation_range": min_activation_range if min_activation_range != 1 else {},
                "particle_color": particle_color if particle_color != 0 else {},
                "start_sound_event": start_sound_event if not start_sound_event is None else {},
                "weight": weight,
                "sequence": [],
            }
        )
        return self

    def sequence(
        self,
        entity_type: Identifier,
        base_delay: float = 0.0,
        delay_per_summon: float = 0.0,
        entity_lifespan: int = -1,
        num_entities_spawned: int = 1,
        shape: str = "line",
        size: int = 1,
        sound_event: str = None,
        summon_cap: int = 0,
        summon_cap_radius: float = 0.0,
        target: FilterSubject = FilterSubject.Self,
        summon_event: str = "minecraft:entity_spawned",
    ):
        self._component["summon_choices"][-1]["sequence"].append(
            {
                "entity_type": entity_type,
                "base_delay": base_delay,
                "delay_per_summon": delay_per_summon,
                "entity_lifespan": entity_lifespan,
                "num_entities_spawned": num_entities_spawned,
                "shape": shape,
                "size": size,
                "sound_event": sound_event if not sound_event is None else {},
                "summon_cap": summon_cap if summon_cap != 0 else {},
                "summon_cap_radius": summon_cap_radius if summon_cap_radius != 0 else {},
                "target": target,
                "summon_event": summon_event if summon_event != "minecraft:entity_spawned" else {},
            }
        )
        return self


class EntityAIDelayedAttack(_ai_goal):
    _identifier = "minecraft:behavior.delayed_attack"

    def __init__(
        self,
        attack_duration: float = 0.75,
        attack_once: bool = False,
        cooldown_time: int = 1,
        hit_delay_pct: float = 0.5,
        inner_boundary_time_increase: float = 0.25,
        max_path_time: float = 0.55,
        melee_fov: int = 90,
        min_path_time: float = 0.2,
        outer_boundary_time_increase: float = 0.5,
        path_fail_time_increase: float = 0.75,
        path_inner_boundary: int = 16,
        path_outer_boundary: int = 32,
        random_stop_interval: int = 0,
        reach_multiplier: int = 2,
        require_complete_path: bool = False,
        # set_persistent: bool = False,
        speed_multiplier: float = 1,
        track_target: bool = False,
        x_max_rotation: int = 30,
        y_max_head_rotation: int = 30,
        can_spread_on_fire: bool = False,
    ) -> None:
        """Compels an entity to attack while also delaying the damage dealt until a specific time in the attack animation.

        Parameters:
            attack_duration (float, optional): The entity's attack animation will play out over this duration (in seconds). Also controls attack cooldown. Defaults to 0.75.
            attack_once (bool, optional): Allows the entity to use this attack behavior, only once EVER. Defaults to False.
            cooldown_time (int, optional): Cooldown time (in seconds) between attacks. Defaults to 1.
            hit_delay_pct (float, optional): The percentage into the attack animation to apply the damage of the attack (1.0 = 100%). Defaults to 0.5.
            inner_boundary_time_increase (float, optional): Time (in seconds) to add to attack path recalculation when the target is beyond the "path_inner_boundary". Defaults to 0.25.
            max_path_time (float, optional): Maximum base time (in seconds) to recalculate new attack path to target (before increases applied). Defaults to 0.55.
            melee_fov (int, optional): Field of view (in degrees) when using the sensing component to detect an attack target. Defaults to 90.
            min_path_time (float, optional): Minimum base time (in seconds) to recalculate new attack path to target (before increases applied). Defaults to 0.2.
            outer_boundary_time_increase (float, optional): Time (in seconds) to add to attack path recalculation when the target is beyond the "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (float, optional): Time (in seconds) to add to attack path recalculation when this entity cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (int, optional): Distance at which to increase attack path recalculation by "inner_boundary_tick_increase". Defaults to 16.
            path_outer_boundary (int, optional): Distance at which to increase attack path recalculation by "outer_boundary_tick_increase". Defaults to 32.
            random_stop_interval (int, optional): This entity will have a 1 in N chance to stop its current attack, where N = "random_stop_interval". Defaults to 0.
            reach_multiplier (int, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            require_complete_path (bool, optional): Toggles (on/off) the need to have a full path from the entity to the target when using this melee attack behavior. Defaults to False.
            speed_multiplier (float, optional): This multiplier modifies the attacking entity's speed when moving toward the target. Defaults to 1.
            track_target (bool, optional): Allows the entity to track the attack target, even if the entity has no sensing. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Defaults to 30.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_delayed_attack
        """

        super().__init__("behavior.delayed_attack")
        if attack_duration != 0.75:
            self._add_field("attack_duration", attack_duration)
        if attack_once:
            self._add_field("attack_once", attack_once)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if hit_delay_pct != 0.5:
            self._add_field("hit_delay_pct", clamp(hit_delay_pct, 0, 1))
        if inner_boundary_time_increase != 0.25:
            self._add_field("inner_boundary_time_increase", inner_boundary_time_increase)
        if max_path_time != 0.55:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if outer_boundary_time_increase != 0.5:
            self._add_field("outer_boundary_time_increase", outer_boundary_time_increase)
        if path_fail_time_increase != 0.75:
            self._add_field("path_fail_time_increase", path_fail_time_increase)
        if path_inner_boundary != 16:
            self._add_field("path_inner_boundary", path_inner_boundary)
        if path_outer_boundary != 32:
            self._add_field("path_outer_boundary", path_outer_boundary)
        if random_stop_interval != 0:
            self._add_field("random_stop_interval", random_stop_interval)
        if reach_multiplier != 2:
            self._add_field("reach_multiplier", reach_multiplier)
        if require_complete_path:
            self._add_field("require_complete_path", require_complete_path)
        # if set_persistent:
        #    self._add_field("set_persistent", set_persistent)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if track_target:
            self._add_field("track_target", track_target)
        if x_max_rotation != 30:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation != 30:
            self._add_field("y_max_head_rotation", y_max_head_rotation)
        if can_spread_on_fire:
            self._add_field("can_spread_on_fire", can_spread_on_fire)

    def attack_types(self, attack_types: str):
        self._add_field("attack_types", attack_types)
        return self

    def on_attack(self, on_attack: str, target: FilterSubject = FilterSubject.Self, filter: Filter = None):
        self._add_field(
            "on_attack", {"event": on_attack, "filters": filter if not filter is None else {}, "target": target}
        )
        return self


class EntityAIMoveToBlock(_ai_goal):
    _identifier = "minecraft:behavior.move_to_block"

    def __init__(
        self,
        target_blocks: list[Block | str],
        goal_radius: float = 0.5,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        start_chance: float = 1.0,
        stay_duration: float = 0.0,
        target_offset: tuple[float, float, float] = (0, 0, 0),
        target_selection_method: str = "nearest",
        tick_interval: int = 20,
    ) -> None:
        """Compels a mob to move towards a block."""
        super().__init__("behavior.move_to_block")
        
        from anvil.lib.schemas import BlockDescriptor

        if not all(isinstance(block, (BlockDescriptor, str)) for block in target_blocks):
            raise TypeError(
                f"All target_blocks must be either BlockDescriptor instances or strings representing block identifiers. Component [{self._identifier}]"
            ) 
        
        self._add_field(
            "target_blocks",
            [
                str(block)
                for block in target_blocks
            ],
        )

        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if start_chance != 1.0:
            self._add_field("start_chance", start_chance)
        if stay_duration != 0.0:
            self._add_field("stay_duration", stay_duration)
        if target_offset != (0, 0, 0):
            self._add_field("target_offset", target_offset)
        if target_selection_method != "nearest":
            self._add_field("target_selection_method", target_selection_method)
        if tick_interval != 20:
            self._add_field("tick_interval", tick_interval)

    def on_reach(self, event: Event, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_reach", {"event": event, "target": target.value})
        return self

    def on_stay_completed(self, event: Event, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_stay_completed", {"event": event, "target": target.value})
        return self


class EntityAIEquipItem(_ai_goal):
    _identifier = "minecraft:behavior.equip_item"

    def __init__(self) -> None:
        """Compels an entity to equip an item."""
        super().__init__("behavior.equip_item")


class EntityAISendEvent(_ai_goal):
    _identifier = "minecraft:behavior.send_event"

    def __init__(self) -> None:
        """Compels an entity to send an event to another entity."""
        super().__init__("behavior.send_event")
        self._add_field("event_choices", [])

    def choice(
        self,
        cast_duration: Seconds,
        cooldown_time: Seconds,
        # look_at_target: bool = True,
        min_activation_range: float = 0.0,
        max_activation_range: float = 16.0,
        particle_color: str = None,
        weight: int = 1,
        filters: Filter = None,
        start_sound_event: str = None,
    ):
        choice = {
            "cast_duration": cast_duration,
            "cooldown_time": cooldown_time,
            "min_activation_range": min_activation_range,
            "max_activation_range": max_activation_range,
            "weight": weight,
            "sequence": [],
        }
        # if not look_at_target:
        #    choice["look_at_target"] = look_at_target
        if not particle_color is None:
            choice["particle_color"] = particle_color
        if not filters is None:
            choice["filters"] = filters
        if not start_sound_event is None:
            choice["start_sound_event"] = start_sound_event

        self._component["event_choices"].append(choice)

        return self

    def sequence(self, base_delay: Seconds, event: str, sound_event: str = None):
        seq = {
            "base_delay": base_delay,
            "event": event,
        }
        if not sound_event is None:
            seq["sound_event"] = sound_event

        self._component["event_choices"][-1]["sequence"].append(seq)
        return self


class EntityAIMoveTowardsTarget(_ai_goal):
    _identifier = "minecraft:behavior.move_towards_target"

    def __init__(self, within_radius: float = 0.0, speed_multiplier: float = 1.0) -> None:
        """Compels an entity to move towards a target.

        Parameters:
            within_radius (float, optional): Defines the radius in blocks that the mob tries to be from the target. A value of 0 means it tries to occupy the same block as the target. Defaults to 0.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_target
        """
        super().__init__("behavior.move_towards_target")

        if within_radius != 0.0:
            self._add_field("within_radius", within_radius)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIRandomSitting(_ai_goal):
    _identifier = "minecraft:behavior.random_sitting"

    def __init__(
        self, cooldown_time: float = 0, min_sit_time: float = 10, start_chance: float = 0.1, stop_chance: float = 0.3
    ) -> None:
        """Compels an entity to stop and sit for a random duration of time.

        Parameters:
            cooldown_time (float, optional): Time in seconds the entity has to wait before using the goal again. Defaults to 0.
            min_sit_time (float, optional): The minimum amount of time in seconds before the entity can stand back up. Defaults to 10.
            start_chance (float, optional): This is the chance that the entity will start this goal, from 0 to 1. Defaults to 0.1.
            stop_chance (float, optional): This is the chance that the entity will stop this goal, from 0 to 1. Defaults to 0.3.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_sitting
        """
        super().__init__("behavior.random_sitting")

        if cooldown_time != 0:
            self._add_field("cooldown_time", cooldown_time)
        if min_sit_time != 10:
            self._add_field("min_sit_time", min_sit_time)
        if start_chance != 0.1:
            self._add_field("start_chance", clamp(start_chance, 0, 1))
        if stop_chance != 0.3:
            self._add_field("stop_chance", clamp(stop_chance, 0, 1))


class EntityAIStayWhileSitting(_ai_goal):
    _identifier = "minecraft:behavior.stay_while_sitting"

    def __init__(self) -> None:
        """Compels an entity to stay in place while sitting.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_while_sitting
        """
        super().__init__("behavior.stay_while_sitting")


class EntityAIRandomSwim(_ai_goal):
    _identifier = "minecraft:behavior.random_swim"

    def __init__(
        self,
        avoid_surface: bool = True,
        interval: int = 120,
        speed_multiplier: float = 1,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Compels an entity to swim in a random point in water.

        Parameters:
            avoid_surface (bool, optional): If true, the entity will avoid surface water blocks by swimming below them. Defaults to True.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the entity when using this AI Goal. Defaults to 1.
            xz_dist (int, optional): Distance in blocks on ground that the entity will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the entity will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_swim
        """

        super().__init__("behavior.random_swim")

        if not avoid_surface:
            self._add_field("avoid_surface", avoid_surface)
        if interval != 120:
            self._add_field("interval", interval)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", max(1, xz_dist))
        if y_dist != 7:
            self._add_field("y_dist", max(1, y_dist))


class EntityAIRandomBreach(_ai_goal):
    _identifier = "minecraft:behavior.random_breach"

    def __init__(
        self,
        cooldown_time: float = 0,
        interval: int = 120,
        speed_multiplier: float = 1,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Compels an entity to swim in a random point in water.

        Parameters:
            cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the entity when using this AI Goal. Defaults to 1.
            xz_dist (int, optional): Distance in blocks on ground that the entity will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the entity will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_breach
        """

        super().__init__("behavior.random_breach")

        if not cooldown_time:
            self._add_field("avoid_surface", cooldown_time)
        if interval != 120:
            self._add_field("interval", interval)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", max(1, xz_dist))
        if y_dist != 7:
            self._add_field("y_dist", max(1, y_dist))


class EntityAIMoveToWater(_ai_goal):
    _identifier = "minecraft:behavior.move_to_water"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1,
    ) -> None:
        """Compels an entity to move to water when on land.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            search_count (int, optional): The number of blocks each tick that the mob will check within its search range and height for a valid block to move to. A value of 0 will have the mob check every block within range in one tick. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for water to move towards. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for water to move towards. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_water
        """
        super().__init__("behavior.move_to_water")

        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if search_count != 10:
            self._add_field("search_count", search_count)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIMoveToLand(_ai_goal):
    _identifier = "minecraft:behavior.move_to_land"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1,
    ) -> None:
        """Compels an entity to move to land when on land.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            search_count (int, optional): The number of blocks each tick that the mob will check within its search range and height for a valid block to move to. A value of 0 will have the mob check every block within range in one tick. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for land to move towards. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for land to move towards. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_land
        """
        super().__init__("behavior.move_to_land")

        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if search_count != 10:
            self._add_field("search_count", search_count)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIMoveToLava(_ai_goal):
    _identifier = "minecraft:behavior.move_to_lava"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1,
    ) -> None:
        """Compels an entity to move to lava when on lava.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            search_count (int, optional): The number of blocks each tick that the mob will check within its search range and height for a valid block to move to. A value of 0 will have the mob check every block within range in one tick. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for lava to move towards. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for lava to move towards. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_lava
        """
        super().__init__("behavior.move_to_lava")

        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if search_count != 10:
            self._add_field("search_count", search_count)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAILookAtTarget(_ai_goal):
    _identifier = "minecraft:behavior.look_at_target"

    def __init__(
        self,
        angle_of_view_horizontal: int = 360,
        angle_of_view_vertical: int = 360,
        look_distance: float = 8.0,
        look_time: tuple[int, int] = (2, 4),
        probability: float = 0.02,
        target_distance: float = 0.6,
    ) -> None:
        """Compels an entity to look at the target by rotating the head bone pose within a set limit."""
        super().__init__("behavior.look_at_target")
        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time != (2, 4):
            self._add_field("look_time", look_time)
        if probability != 0.02:
            self._add_field("probability", probability)
        if target_distance != 0.6:
            self._add_field("target_distance", target_distance)


class EntityAIFollowParent(_ai_goal):
    _identifier = "minecraft:behavior.follow_parent"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity that has been tagged as a baby to follow their parent around."""
        super().__init__("behavior.follow_parent")
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIPlayerRideTamed(_ai_goal):
    _identifier = "minecraft:behavior.player_ride_tamed"

    def __init__(self) -> None:
        """Allows an entity to be rideable after being tamed by a player."""
        super().__init__("behavior.player_ride_tamed")


class EntityAIFollowOwner(_ai_goal):
    _identifier = "minecraft:behavior.follow_owner"

    def __init__(
        self,
        can_teleport: bool = True,
        ignore_vibration: bool = True,
        max_distance: float = 60.0,
        speed_multiplier: float = 1.0,
        start_distance: float = 10.0,
        stop_distance: float = 2.0,
        post_teleport_distance: int = 1,
    ) -> None:
        """Compels an entity to follow a player marked as an owner."""
        super().__init__("behavior.follow_owner")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.20")

        if not can_teleport:
            self._add_field("can_teleport", can_teleport)
        if not ignore_vibration:
            self._add_field("ignore_vibration", ignore_vibration)
        if max_distance != 60.0:
            self._add_field("max_distance", max_distance)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if start_distance != 10.0:
            self._add_field("start_distance", start_distance)
        if stop_distance != 2.0:
            self._add_field("stop_distance", stop_distance)
        if post_teleport_distance > 1:
            self._add_field("post_teleport_distance", post_teleport_distance)


class EntityAIPanic(_ai_goal):
    _identifier = "minecraft:behavior.panic"

    def __init__(
        self,
        damage_sources: DamageCause = DamageCause.All,
        force: bool = False,
        ignore_mob_damage: bool = False,
        panic_sound: str = None,
        prefer_water: bool = False,
        sound_interval: float = 0,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity to react when it receives damage."""
        super().__init__("behavior.panic")
        if not damage_sources == DamageCause.All:
            self._add_field("damage_sources", damage_sources)
        if force:
            self._add_field("force", force)
        if ignore_mob_damage:
            self._add_field("ignore_mob_damage", ignore_mob_damage)
        if not panic_sound is None:
            self._add_field("panic_sound", panic_sound)
        if prefer_water:
            self._add_field("prefer_water", prefer_water)
        if sound_interval != 0:
            self._add_field("sound_interval", sound_interval)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIChargeAttack(_ai_goal):
    _identifier = "minecraft:behavior.charge_attack"

    def __init__(
        self,
        max_distance: int = 3,
        min_distance: int = 2,
        success_rate: float = 0.1428,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity to damage a target by using a running attack.

        Parameters:
            max_distance (int, optional): A charge attack cannot start if the entity is farther than this distance to the target. Defaults to 3.
            min_distance (int, optional): A charge attack cannot start if the entity is closer than this distance to the target. Defaults to 2.
            success_rate (float, optional): Percent chance this entity will start a charge attack, if not already attacking (1.0 = 100%). Defaults to 0.1428.
            speed_multiplier (float, optional): Modifies the entity's speed when charging toward the target. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_attack
        """
        super().__init__("behavior.charge_attack")
        if max_distance != 3:
            self._add_field("max_distance", max_distance)
        if min_distance != 2:
            self._add_field("min_distance", min_distance)
        if success_rate != 0.1428:
            self._add_field("success_rate", success_rate)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIRamAttack(_ai_goal):
    _identifier = "minecraft:behavior.ram_attack"

    def __init__(
        self,
        baby_knockback_modifier: float = 0.333333,
        cooldown_range: list[int, int] = [10, 20],
        knockback_force: float = 5,
        knockback_height: float = 0.1,
        min_ram_distance: float = 0.0,
        pre_ram_sound: str = None,
        ram_distance: float = 0.0,
        ram_impact_sound: str = None,
        ram_speed: float = 2.0,
        run_speed: float = 1.0,
    ) -> None:
        """Compels an entity to search for a random target and, if a direct path exists between the entity and the target, it will perform a charge. If the attack hits, the target will be knocked back based on the entity's speed.

        Parameters:
            baby_knockback_modifier (float, optional): The modifier to knockback that babies have. Defaults to 0.333333.
            cooldown_range (list[int, int], optional): Minimum and maximum cooldown time-range (positive, in seconds) between each attempted ram attack. Defaults to [10, 20].
            knockback_force (float, optional): The force of the ram attack knockback. Defaults to 5.
            knockback_height (float, optional): The height of the ram attack knockback. Defaults to 0.1.
            min_ram_distance (float, optional): The minimum distance the entity can start a ram attack. Defaults to 0.0.
            pre_ram_sound (str, optional): The sound to play when an entity is about to perform a ram attack. Defaults to None.
            ram_distance (float, optional): The distance the mob start to run with ram speed. Defaults to 0.0.
            ram_impact_sound (str, optional): The sound to play when an entity is impacting on a ram attack. Defaults to None.
            ram_speed (float, optional): The entity's speed when charging toward the target. Defaults to 2.0.
            run_speed (float, optional): The entity's speed when running toward the target. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ram_attack
        """
        super().__init__("behavior.ram_attack")
        if baby_knockback_modifier != 0.333333:
            self._add_field("baby_knockback_modifier", baby_knockback_modifier)
        if cooldown_range != [10, 20]:
            self._add_field("cooldown_range", cooldown_range)
        if knockback_force != 5:
            self._add_field("knockback_force", knockback_force)
        if knockback_height != 0.1:
            self._add_field("knockback_height", knockback_height)
        if min_ram_distance != 0.0:
            self._add_field("min_ram_distance", min_ram_distance)
        if not pre_ram_sound is None:
            self._add_field("pre_ram_sound", pre_ram_sound)
        if ram_distance != 0.0:
            self._add_field("ram_distance", ram_distance)
        if not ram_impact_sound is None:
            self._add_field("ram_impact_sound", ram_impact_sound)
        if ram_speed != 2.0:
            self._add_field("ram_speed", ram_speed)
        if run_speed != 1.0:
            self._add_field("run_speed", run_speed)

    def on_start(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_start", {"event": event, "target": target.value})
        return self


class EntityAIAvoidMobType(_ai_goal):
    _identifier = "minecraft:behavior.avoid_mob_type"

    def __init__(
        self,
        avoid_mob_sound: str = None,
        avoid_target_xz: int = 16,
        avoid_target_y: int = 7,
        ignore_visibility: bool = False,
        probability_per_strength: float = 1.0,
        remove_target: bool = False,
        sound_interval: list[float] = [3.0, 8.0],
        check_if_outnumbered: bool = False,
        cooldown: float = 0.0,
    ) -> None:
        """Compels an entity to run away from other entities that meet the criteria specified.

        Parameters:
            avoid_mob_sound (str, optional): The sound event to play when the mob is avoiding another mob. Defaults to None.
            avoid_target_xz (int, optional): The next target position the entity chooses to avoid another entity will be chosen within this XZ Distance. Defaults to 16.
            avoid_target_y (int, optional): The next target position the entity chooses to avoid another entity will be chosen within this Y Distance. Defaults to 7.
            ignore_visibility (bool, optional): Whether or not to ignore direct line of sight while this entity is running away from other specified entities. Defaults to False.
            probability_per_strength (float, optional): Percent chance this entity will stop avoiding another entity based on that entity's strength, where 1.0 = 100%. Defaults to 1.0.
            remove_target (bool, optional): Determine if we should remove target when fleeing or not. Defaults to False.
            sound_interval (list[float], optional): The range of time in seconds to randomly wait before playing the sound again. Defaults to [3.0, 8.0].
            check_if_outnumbered (bool, optional): If true, the entity will only avoid other entities if it is outnumbered. Defaults to False.
            cooldown (float, optional): Time in seconds the entity has to wait before using the goal again. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_mob_type
        """
        super().__init__("behavior.avoid_mob_type")

        self._add_field("entity_types", [])
        if not avoid_mob_sound is None:
            self._add_field("avoid_mob_sound", avoid_mob_sound)
        if avoid_target_xz != 16:
            self._add_field("avoid_target_xz", avoid_target_xz)
        if avoid_target_y != 7:
            self._add_field("avoid_target_y", avoid_target_y)
        if ignore_visibility:
            self._add_field("ignore_visibility", ignore_visibility)
        if probability_per_strength != 1.0:
            self._add_field("probability_per_strength", probability_per_strength)
        if remove_target:
            self._add_field("remove_target", remove_target)
        if sound_interval != [3.0, 8.0]:
            self._add_field("sound_interval", sound_interval)
        if check_if_outnumbered:
            self._add_field("check_if_outnumbered", check_if_outnumbered)
        if cooldown != 0.0:
            self._add_field("cooldown", cooldown)

    def add_type(
        self,
        filter: Filter,
        max_dist: float = 3.0,
        max_flee: float = 10.0,
        sprint_distance: float = 7.0,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        """Adds a new entity type to the list of conditions another entity must meet to be a valid target to avoid.

        Parameters:
            filter (Filter): Filter to determine which entities to avoid.
            max_dist (float, optional): Maximum distance to look for an avoid target for the entity. Defaults to 3.0.
            max_flee (float, optional): How many blocks away from its avoid target the entity must be for it to stop fleeing from the avoid target. Defaults to 10.0.
            sprint_distance (float, optional): How many blocks within range of its avoid target the entity must be for it to begin sprinting away from the avoid target. Defaults to 7.0.
            sprint_speed_multiplier (float, optional): Multiplier for sprint speed. 1.0 means keep the regular speed, while higher numbers make the sprint speed faster. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Multiplier for walking speed. 1.0 means keep the regular speed, while higher numbers make the walking speed faster. Defaults to 1.0.
        """

        a = {"filters": filter}
        if max_dist != 3.0:
            a["max_dist"] = max_dist
        if max_flee != 10.0:
            a["max_flee"] = max_flee
        if sprint_distance != 7.0:
            a["sprint_distance"] = sprint_distance
        if sprint_speed_multiplier != 1.0:
            a["sprint_speed_multiplier"] = sprint_speed_multiplier
        if walk_speed_multiplier != 1.0:
            a["walk_speed_multiplier"] = walk_speed_multiplier
        self._component["entity_types"].append(a)
        return self

    def on_escape_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Event that is triggered when escaping from a mob.

        Parameters:
            event (str): Event to trigger.
            target (FilterSubject, optional): Target of the event. Defaults to FilterSubject.Self.
        """
        self._add_field("on_escape_event", {"event": event, "target": target.value})
        return self


class EntityAILeapAtTarget(_ai_goal):
    _identifier = "minecraft:behavior.leap_at_target"

    def __init__(
        self,
        must_be_on_ground: bool = True,
        set_persistent: bool = False,
        target_dist: float = 0.3,
        yd: float = 0.0,
    ) -> None:
        """Compels an entity to jump towards a target.

        Parameters:
            must_be_on_ground (bool, optional): If true, the mob will only jump at its target if its on the ground. Setting it to false will allow it to jump even if its already in the air. Defaults to True.
            set_persistent (bool, optional): Allows the entity to be set to persist upon targeting a player. Defaults to False.
            target_dist (float, optional): Distance in blocks the mob jumps when leaping at its target. Defaults to 0.3.
            yd (float, optional): Height in blocks the mob jumps when leaping at its target. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_leap_at_target
        """

        super().__init__("behavior.leap_at_target")
        if not must_be_on_ground:
            self._add_field("must_be_on_ground", must_be_on_ground)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if target_dist != 0.3:
            self._add_field("target_dist", target_dist)
        if yd != 0.0:
            self._add_field("yd", yd)


class EntityAIOcelotAttack(_ai_goal):
    _identifier = "minecraft:behavior.ocelotattack"

    def __init__(
        self,
        cooldown_time: int = 1,
        max_distance: int = 15,
        max_sneak_range: int = 15,
        max_sprint_range: int = 4,
        reach_multiplier: int = 2,
        sneak_speed_multiplier: float = 0.6,
        sprint_speed_multiplier: float = 1.33,
        walk_speed_multiplier: float = 0.8,
        x_max_rotation: int = 30,
        y_max_head_rotation: int = 30,
    ) -> None:
        """Allows an entity to attack by sneaking and pouncing.

        Parameters:
            cooldown_time (int, optional): Time (in seconds) between attacks. Defaults to 1.
            max_distance (int, optional): Max distance from the target, this entity will use this attack behavior. Defaults to 15.
            max_sneak_range (int, optional): Max distance from the target, this entity starts sneaking. Defaults to 15.
            max_sprint_range (int, optional): Max distance from the target, this entity starts sprinting (sprinting takes priority over sneaking). Defaults to 4.
            reach_multiplier (int, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            sneak_speed_multiplier (float, optional): Modifies the attacking entity's movement speed while sneaking. Defaults to 0.6.
            sprint_speed_multiplier (float, optional): Modifies the attacking entity's movement speed while sprinting. Defaults to 1.33.
            walk_speed_multiplier (float, optional): Modifies the attacking entity's movement speed when not sneaking or sprinting, but still within attack range. Defaults to 0.8.
            x_max_rotation (int, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Defaults to 30.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelotattack
        """
        super().__init__("behavior.ocelotattack")
        if cooldown_time != 5:
            self._add_field("cooldown_time", cooldown_time)
        if x_max_rotation != 30.0:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation != 30.0:
            self._add_field("y_max_head_rotation", y_max_head_rotation)
        if max_distance != 20:
            self._add_field("max_distance", max_distance)
        if max_sneak_range != 15.0:
            self._add_field("max_sneak_range", max_sneak_range)
        if max_sprint_range != 4.0:
            self._add_field("max_sprint_range", max_sprint_range)
        if reach_multiplier != 2.0:
            self._add_field("reach_multiplier", reach_multiplier)
        if sneak_speed_multiplier != 0.6:
            self._add_field("sneak_speed_multiplier", sneak_speed_multiplier)
        if sprint_speed_multiplier != 1.33:
            self._add_field("sprint_speed_multiplier", sprint_speed_multiplier)
        if walk_speed_multiplier != 0.8:
            self._add_field("walk_speed_multiplier", walk_speed_multiplier)


class EntityAIOwnerHurtByTarget(_ai_goal):
    _identifier = "minecraft:behavior.owner_hurt_by_target"

    def __init__(
        self,
        entity_types: Filter = None,
        cooldown: Seconds = 0,
        filters: Filter = None,
        max_dist: int = 16,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity to react when the owner is hit by a target.

        Parameters:
            entity_types (Filter, optional): List of entity types that this mob can target if they hurt their owner. Defaults to None.
            cooldown (seconds, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Defaults to 0.
            filters (Filter, optional): Conditions that make this entry in the list valid. Defaults to None.
            max_dist (int, optional): Maximum distance this mob can be away to be a valid choice. Defaults to 16.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            reevaluate_description (bool, optional): If true, the mob will stop being targeted if it stops meeting any conditions. Defaults to False.
            sprint_speed_multiplier (float, optional): Multiplier for the running speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Multiplier for the walking speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_by_target
        """
        super().__init__("behavior.owner_hurt_by_target")

        if entity_types != None:
            self._add_field("entity_types", {"filters": entity_types})
        if cooldown != 0:
            self._add_field("cooldown", cooldown)
        if filters != None:
            self._add_field("filters", filters)
        if max_dist != 16:
            self._add_field("max_dist", max_dist)
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if reevaluate_description:
            self._add_field("reevaluate_description", reevaluate_description)
        if sprint_speed_multiplier != 1.0:
            self._add_field("sprint_speed_multiplier", sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            self._add_field("walk_speed_multiplier", walk_speed_multiplier)


class EntityAIOwnerHurtTarget(_ai_goal):
    _identifier = "minecraft:behavior.owner_hurt_target"

    def __init__(
        self,
        entity_types: Filter = None,
        cooldown: Seconds = 0,
        filters: Filter = None,
        max_dist: int = 16,
        must_see: bool = False,
        must_see_forget_duration: float = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity to react when the owner hits a target.

        Parameters:
            entity_types (Filter, optional): List of entity types that this mob can target if they hurt their owner. Defaults to None.
            cooldown (seconds, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Defaults to 0.
            filters (Filter, optional): Conditions that make this entry in the list valid. Defaults to None.
            max_dist (int, optional): Maximum distance this mob can be away to be a valid choice. Defaults to 16.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            reevaluate_description (bool, optional): If true, the mob will stop being targeted if it stops meeting any conditions. Defaults to False.
            sprint_speed_multiplier (float, optional): Multiplier for the running speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Multiplier for the walking speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_target
        """
        super().__init__("behavior.owner_hurt_target")

        if entity_types != None:
            self._add_field("entity_types", {"filters": entity_types})
        if cooldown != 0:
            self._add_field("cooldown", cooldown)
        if filters != None:
            self._add_field("filters", filters)
        if max_dist != 16:
            self._add_field("max_dist", max_dist)
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if reevaluate_description:
            self._add_field("reevaluate_description", reevaluate_description)
        if sprint_speed_multiplier != 1.0:
            self._add_field("sprint_speed_multiplier", sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            self._add_field("walk_speed_multiplier", walk_speed_multiplier)


class EntityAIRandomSearchAndDig(_ai_goal):
    _identifier = "minecraft:behavior.random_search_and_dig"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (0, 0),
        digging_duration_range: tuple[Seconds, Seconds] = (0, 0),
        find_valid_position_retries: int = 0,
        goal_radius: float = 1.5,
        item_table: str = None,
        search_range_xz: float = 0,
        search_range_y: float = 0,
        spawn_item_after_seconds: Seconds = 0,
        spawn_item_pos_offset: float = 0,
        speed_multiplier: float = 0,
        target_blocks: list[str] = [],
        target_dig_position_offset: float = 2.25,
    ) -> None:
        """Compels an entity to locate a random target block that it can find a path towards. Once found, the entity will move towards the target block and dig up an item.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): Goal cooldown range in seconds. Defaults to (0, 0).
            digging_duration_range (tuple[Seconds, Seconds], optional): Digging duration in seconds. Defaults to (0, 0).
            find_valid_position_retries (int, optional): Amount of retries to find a valid target position within search range. Defaults to 0.
            goal_radius (float, optional): Distance in blocks within the entity to consider it has reached the target position. Defaults to 1.5.
            item_table (str, optional): File path relative to the resource pack root for items to spawn list (loot table format). Defaults to None.
            search_range_xz (float, optional): Width and length of the volume around the entity used to find a valid target position. Defaults to 0.
            search_range_y (float, optional): Height of the volume around the entity used to find a valid target position. Defaults to 0.
            spawn_item_after_seconds (seconds, optional): Digging duration before spawning item in seconds. Defaults to 0.
            spawn_item_pos_offset (float, optional): Distance to offset the item's spawn location in the direction the mob is facing. Defaults to 0.
            speed_multiplier (float, optional): Search movement speed multiplier. Defaults to 0.
            target_blocks (list[str], optional): List of target block types on which the goal will look to dig. Overrides the default list. Defaults to [].
            target_dig_position_offset (float, optional): Dig target position offset from the feet position of the entity in their facing direction. Defaults to 2.25.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_search_and_dig
        """
        super().__init__("behavior.random_search_and_dig")

        if cooldown_range != (0, 0):
            self._add_field("cooldown_range", cooldown_range)
        if digging_duration_range != (0, 0):
            self._add_field("digging_duration_range", digging_duration_range)
        if find_valid_position_retries != 0:
            self._add_field("find_valid_position_retries", find_valid_position_retries)
        if goal_radius != 1.5:
            self._add_field("goal_radius", goal_radius)
        if not item_table is None:
            self._add_field("item_table", item_table)
        if search_range_xz != 0:
            self._add_field("search_range_xz", search_range_xz)
        if search_range_y != 0:
            self._add_field("search_range_y", search_range_y)
        if spawn_item_after_seconds != 0:
            self._add_field("spawn_item_after_seconds", spawn_item_after_seconds)
        if spawn_item_pos_offset != 0:
            self._add_field("spawn_item_pos_offset", spawn_item_pos_offset)
        if speed_multiplier != 0:
            self._add_field("speed_multiplier", speed_multiplier)
        if not target_blocks == []:
            self._add_field("target_blocks", target_blocks)
        if target_dig_position_offset != 2.25:
            self._add_field("target_dig_position_offset", target_dig_position_offset)

    def on_digging_start(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_digging_start", {"event": event, "target": target.value})
        return self

    def on_fail_during_digging(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_fail_during_digging", {"event": event, "target": target.value})
        return self

    def on_fail_during_searching(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_fail_during_searching", {"event": event, "target": target.value})
        return self

    def on_item_found(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_item_found", {"event": event, "target": target.value})
        return self

    def on_searching_start(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_searching_start", {"event": event, "target": target.value})
        return self

    def on_success(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_success", {"event": event, "target": target.value})
        return self


class EntityAIStompAttack(_ai_goal):
    _identifier = "minecraft:behavior.stomp_attack"

    def __init__(
        self,
        attack_once: bool = False,
        attack_types: list[str] = [],
        cooldown_time: Seconds = 1,
        inner_boundary_time_increase: Seconds = 0.25,
        max_path_time: Seconds = 0.55,
        melee_fov: int = 90,
        min_path_time: Seconds = 0.2,
        no_damage_range_multiplier: float = 2,
        outer_boundary_time_increase: Seconds = 0.5,
        path_fail_time_increase: Seconds = 0.75,
        path_inner_boundary: float = 16,
        path_outer_boundary: float = 32,
        random_stop_interval: int = 0,
        reach_multiplier: float = 2,
        require_complete_path: bool = False,
        set_persistent: bool = False,
        speed_multiplier: float = 1,
        stomp_range_multiplier: float = 2,
        track_target: bool = False,
        x_max_rotation: int = 30,
        y_max_head_rotation: int = 30,
    ) -> None:
        """Compels an entity to attack a target by stomping on them.

        Parameters:
            attack_once (bool, optional): If true, the entity will only use this attack behavior once. Defaults to False.
            attack_types (list[str], optional): Defines the entity types this entity will attack. Defaults to [].
            cooldown_time (seconds, optional): Cooldown time (in seconds) between attacks. Defaults to 1.
            inner_boundary_time_increase (seconds, optional): Time (in seconds) to add to attack path recalculation when the target is beyond the "path_inner_boundary". Defaults to 0.25.
            max_path_time (seconds, optional): Maximum base time (in seconds) to recalculate new attack path to target (before increases applied). Defaults to 0.55.
            melee_fov (int, optional): Field of view (in degrees) when using the sensing component to detect an attack target. Defaults to 90.
            min_path_time (seconds, optional): Minimum base time (in seconds) to recalculate new attack path to target (before increases applied). Defaults to 0.2.
            no_damage_range_multiplier (float, optional): Multiplied with the final AoE damage range to determine a no damage range. The stomp attack will go on cooldown if target is in this no damage range. Defaults to 2.
            outer_boundary_time_increase (seconds, optional): Time (in seconds) to add to attack path recalculation when the target is beyond the "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (seconds, optional): Time (in seconds) to add to attack path recalculation when this entity cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_tick_increase". Defaults to 16.
            path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_tick_increase". Defaults to 32.
            random_stop_interval (int, optional): This entity will have a 1 in N chance to stop its current attack, where N = "random_stop_interval". Defaults to 0.
            reach_multiplier (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            require_complete_path (bool, optional): Toggles (on/off) the need to have a full path from the entity to the target when using this melee attack behavior. Defaults to False.
            set_persistent (bool, optional): Allows the entity to be set to persist upon targeting a player. Defaults to False.
            speed_multiplier (float, optional): This multiplier modifies the attacking entity's speed when moving toward the target. Defaults to 1.
            stomp_range_multiplier (float, optional): Multiplied with the base size of the entity to determine stomp AoE damage range. Defaults to 2.
            track_target (bool, optional): Allows the entity to track the attack target, even if the entity has no sensing. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Defaults to 30.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stomp_attack
        """
        super().__init__("behavior.stomp_attack")

        if attack_once:
            self._add_field("attack_once", attack_once)
        if not attack_types == []:
            self._add_field("attack_types", attack_types)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if inner_boundary_time_increase != 0.25:
            self._add_field("inner_boundary_time_increase", inner_boundary_time_increase)
        if max_path_time != 0.55:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if no_damage_range_multiplier != 2:
            self._add_field("no_damage_range_multiplier", no_damage_range_multiplier)
        if outer_boundary_time_increase != 0.5:
            self._add_field("outer_boundary_time_increase", outer_boundary_time_increase)
        if path_fail_time_increase != 0.75:
            self._add_field("path_fail_time_increase", path_fail_time_increase)
        if path_inner_boundary != 16:
            self._add_field("path_inner_boundary", path_inner_boundary)
        if path_outer_boundary != 32:
            self._add_field("path_outer_boundary", path_outer_boundary)
        if random_stop_interval != 0:
            self._add_field("random_stop_interval", random_stop_interval)
        if reach_multiplier != 2:
            self._add_field("reach_multiplier", reach_multiplier)
        if require_complete_path:
            self._add_field("require_complete_path", require_complete_path)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if stomp_range_multiplier != 2:
            self._add_field("stomp_range_multiplier", stomp_range_multiplier)
        if track_target:
            self._add_field("track_target", track_target)
        if x_max_rotation != 30:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation != 30:
            self._add_field("y_max_head_rotation", y_max_head_rotation)

    def on_attack(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_attack", {"event": event, "target": target.value})
        return self


class EntityAIFollowMob(_ai_goal):
    _identifier = "minecraft:behavior.follow_mob"

    def __init__(
        self,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        stop_distance: int = 2,
    ) -> None:
        """Compels an entity to follow and gather around other mobs of the same type.

        Parameters:
            search_range (int, optional): The distance in blocks it will look for a mob to follow. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            stop_distance (int, optional): The distance in blocks this mob stops from the mob it is following. Defaults to 2.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_mob
        """
        super().__init__("behavior.follow_mob")
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if stop_distance != 2:
            self._add_field("stop_distance", stop_distance)


class EntityAIRandomSwim(_ai_goal):
    _identifier = "minecraft:behavior.random_swim"

    def __init__(
        self,
        avoid_surface: bool = True,
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Compels an entity to swim in a random point in water.

        Parameters:
            avoid_surface (bool, optional): If true, the entity will avoid surface water blocks by swimming below them. Defaults to True.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the entity when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the entity will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the entity will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_swim
        """
        super().__init__("behavior.random_swim")

        if not avoid_surface:
            self._add_field("avoid_surface", avoid_surface)
        if interval != 120:
            self._add_field("interval", interval)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", xz_dist)
        if y_dist != 7:
            self._add_field("y_dist", y_dist)


class EntityAIRandomBreach(_ai_goal):
    _identifier = "minecraft:behavior.random_breach"

    def __init__(
        self,
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
        cooldown_time: Seconds = 10,
    ) -> None:
        """Compels an entity to breach the surface of the water at a random interval.

        Parameters:
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the entity when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the entity will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the entity will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            cooldown_time (seconds, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Defaults to 10.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior
        """
        super().__init__("behavior.random_breach")

        if interval != 120:
            self._add_field("interval", interval)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", xz_dist)
        if y_dist != 7:
            self._add_field("y_dist", y_dist)
        if cooldown_time != 10:
            self._add_field("cooldown_time", cooldown_time)


class EntityAIRandomHover(_ai_goal):
    _identifier = "minecraft:behavior.random_hover"

    def __init__(
        self,
        hover_height: tuple[float, float] = (0.0, 0.0),
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
        y_offset: float = 0.0,
    ) -> None:
        """Compels an entity to hover around randomly, close to the surface.

        Parameters:
            hover_height (tuple[float, float], optional): The height above the surface which the entity will try to maintain. Defaults to (0.0, 0.0).
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the entity when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the entity will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the entity will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            y_offset (float, optional): Height in blocks to add to the selected target position. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_hover
        """
        super().__init__("behavior.random_hover")

        if hover_height != (0.0, 0.0):
            self._add_field("hover_height", hover_height)
        if interval != 120:
            self._add_field("interval", interval)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", xz_dist)
        if y_dist != 7:
            self._add_field("y_dist", y_dist)
        if y_offset != 0.0:
            self._add_field("y_offset", y_offset)


class EntityAIRoar(_ai_goal):
    _identifier = "minecraft:behavior.roar"

    def __init__(
        self,
        duration: Seconds = 0.0,
    ) -> None:
        """Compels the entity to roar at another entity based on data in minecraft:anger_level. When the anger threshold specified in minecraft:anger_level has been reached, this entity will roar for the specified amount of time, look at the other entity, apply anger boost towards it, and finally target it.

        Parameters:
            duration (seconds, optional): The amount of time to roar for. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roar
        """
        super().__init__("behavior.roar")

        if duration != 0.0:
            self._add_field("duration", duration)


class EntityAIFloatWander(_ai_goal):
    _identifier = "minecraft:behavior.float_wander"

    def __init__(
        self,
        float_duration: tuple[Seconds, Seconds] = (0.0, 0.0),
        must_reach: bool = False,
        priority: int = 0,
        random_reselect: bool = False,
        xz_dist: int = 10,
        y_dist: int = 7,
        y_offset: float = 0.0,
    ) -> None:
        """Compels an entity to float around in a random direction, similar to the ghast entity.

        Parameters:
            float_duration (tuple[Seconds, Seconds], optional): Range of time in seconds the mob will float around before landing and choosing to do something else. Defaults to (0.0, 0.0).
            must_reach (bool, optional): If true, the point has to be reachable to be a valid target. Defaults to False.
            priority (int, optional): The higher the priority, the sooner this behavior will be executed as a goal. Defaults to 0.
            random_reselect (bool, optional): If true, the mob will randomly pick a new point while moving to the previously selected one. Defaults to False.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            y_offset (float, optional): Height in blocks to add to the selected target position. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_wander
        """
        super().__init__("behavior.float_wander")

        if float_duration != (0.0, 0.0):
            self._add_field("float_duration", float_duration)
        if must_reach:
            self._add_field("must_reach", must_reach)
        if priority != 0:
            self._add_field("priority", priority)
        if random_reselect:
            self._add_field("random_reselect", random_reselect)
        if xz_dist != 10:
            self._add_field("xz_dist", xz_dist)
        if y_dist != 7:
            self._add_field("y_dist", y_dist)


class EntityAILayDown(_ai_goal):
    _identifier = "minecraft:behavior.lay_down"

    def __init__(
        self,
        interval: int = 120,
        random_stop_interval: int = 120,
    ) -> None:
        """Compels an entity randomly lay down for a period of time.

        Parameters:
            interval (int, optional): A random value to determine at what intervals something can occur. This has a 1/interval chance to choose this goal. Defaults to 120.
            random_stop_interval (int, optional): A random value to determine at what interval the AI goal can stop. This has a 1/interval chance to stop this goal. Defaults to 120.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_down
        """
        super().__init__("behavior.lay_down")

        if interval != 120:
            self._add_field("interval", interval)
        if random_stop_interval != 120:
            self._add_field("random_stop_interval", random_stop_interval)


class EntityAIMeleeBoxAttack(_ai_goal):
    _identifier = "minecraft:behavior.melee_box_attack"

    def __init__(
        self,
        attack_once: bool = False,
        attack_types: list[str] = [],
        can_spread_on_fire: bool = False,
        cooldown_time: Seconds = 1,
        horizontal_reach: float = 0.8,
        inner_boundary_time_increase: Seconds = 0.25,
        max_path_time: Seconds = 0.55,
        melee_fov: int = 90,
        min_path_time: Seconds = 0.2,
        outer_boundary_time_increase: Seconds = 0.5,
        path_fail_time_increase: Seconds = 0.75,
        path_inner_boundary: float = 16,
        path_outer_boundary: float = 32,
        random_stop_interval: int = 0,
        box_increase: float = 2,
        require_complete_path: bool = False,
        set_persistent: bool = False,
        speed_multiplier: float = 1,
        track_target: bool = False,
        x_max_rotation: int = 30,
        y_max_head_rotation: int = 30,
    ) -> None:
        """Compels an entity to attack a target by stomping on them.

        Parameters:
            attack_once (bool, optional): If true, the entity will only use this attack behavior once. Defaults to False.
            attack_types (list[str], optional): Defines the entity types this entity will attack. Defaults to [].
            can_spread_on_fire (bool, optional): If the entity is on fire, this allows the entity's target to catch on fire after being hit. Defaults to False.
            cooldown_time (seconds, optional): Cooldown time (in seconds) between attacks. Defaults to 1.
            horizontal_reach (float, optional): The attack reach of the entity will be a box with the size of the entity's bounds increased by this value in all horizontal directions. Defaults to 0.8.
            inner_boundary_time_increase (seconds, optional): Time (in seconds) to add to attack path recalculation when the target is beyond the "path_inner_boundary". Defaults to 0.25.
            max_path_time (seconds, optional): Maximum base time (in seconds) to recalculate new attack path to target (before increases applied). Defaults to 0.55.
            melee_fov (int, optional): Field of view (in degrees) when using the sensing component to detect an attack target. Defaults to 90.
            min_path_time (seconds, optional): Minimum base time (in seconds) to recalculate new attack path to target (before increases applied). Defaults to 0.2.
            outer_boundary_time_increase (seconds, optional): Time (in seconds) to add to attack path recalculation when the target is beyond the "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (seconds, optional): Time (in seconds) to add to attack path recalculation when this entity cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_tick_increase". Defaults to 16.
            path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_tick_increase". Defaults to 32.
            random_stop_interval (int, optional): This entity will have a 1 in N chance to stop its current attack, where N = "random_stop_interval". Defaults to 0.
            box_increase (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            require_complete_path (bool, optional): Toggles (on/off) the need to have a full path from the entity to the target when using this melee attack behavior. Defaults to False.
            set_persistent (bool, optional): Allows the entity to be set to persist upon targeting a player. Defaults to False.
            speed_multiplier (float, optional): This multiplier modifies the attacking entity's speed when moving toward the target. Defaults to 1.
            track_target (bool, optional): Allows the entity to track the attack target, even if the entity has no sensing. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Defaults to 30.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_melee_box_attack
        """
        super().__init__("behavior.melee_box_attack")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.20.50")

        if attack_once:
            self._add_field("attack_once", attack_once)
        if not attack_types == []:
            self._add_field("attack_types", attack_types)
        if can_spread_on_fire:
            self._add_field("can_spread_on_fire", can_spread_on_fire)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if horizontal_reach != 0.8:
            self._add_field("horizontal_reach", horizontal_reach)
        if inner_boundary_time_increase != 0.25:
            self._add_field("inner_boundary_time_increase", inner_boundary_time_increase)
        if max_path_time != 0.55:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if outer_boundary_time_increase != 0.5:
            self._add_field("outer_boundary_time_increase", outer_boundary_time_increase)
        if path_fail_time_increase != 0.75:
            self._add_field("path_fail_time_increase", path_fail_time_increase)
        if path_inner_boundary != 16:
            self._add_field("path_inner_boundary", path_inner_boundary)
        if path_outer_boundary != 32:
            self._add_field("path_outer_boundary", path_outer_boundary)
        if random_stop_interval != 0:
            self._add_field("random_stop_interval", random_stop_interval)
        if box_increase != 2:
            self._add_field("box_increase", box_increase)
        if require_complete_path:
            self._add_field("require_complete_path", require_complete_path)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if speed_multiplier != 1:
            self._add_field("speed_multiplier", speed_multiplier)
        if track_target:
            self._add_field("track_target", track_target)
        if x_max_rotation != 30:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation != 30:
            self._add_field("y_max_head_rotation", y_max_head_rotation)

    def on_attack(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_attack", {"event": event, "target": target.value})
        return self


class EntityAITimerFlag1(_ai_goal):
    _identifier = "minecraft:behavior.timer_flag_1"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (10.0, 10.0),
        duration_range: tuple[Seconds, Seconds] = (2.0, 2.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping to due the timeout or due to being interrupted by another behavior, the goal fires another event. query.timer_flag_1 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): The goal cooldown range, in seconds. Defaults to (10.0, 10.0).
            duration_range (tuple[Seconds, Seconds], optional): The goal duration range, in seconds. Defaults to (2.0, 2.0).

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_1
        """
        super().__init__("behavior.timer_flag_1")

        if cooldown_range != (10.0, 10.0):
            self._add_field("cooldown_range", cooldown_range)
        if duration_range != (2.0, 2.0):
            self._add_field("duration_range", duration_range)
        if not control_flags == []:
            self._add_field("control_flags", control_flags)

    def on_end(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self

    def on_start(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_start", {"event": on_end, "target": subject})
        return self


class EntityAITimerFlag2(_ai_goal):
    _identifier = "minecraft:behavior.timer_flag_2"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (10.0, 10.0),
        duration_range: tuple[Seconds, Seconds] = (2.0, 2.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping to due the timeout or due to being interrupted by another behavior, the goal fires another event. query.timer_flag_2 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): The goal cooldown range, in seconds. Defaults to (10.0, 10.0).
            duration_range (tuple[Seconds, Seconds], optional): The goal duration range, in seconds. Defaults to (2.0, 2.0).

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_2
        """
        super().__init__("behavior.timer_flag_2")

        if cooldown_range != (10.0, 10.0):
            self._add_field("cooldown_range", cooldown_range)
        if duration_range != (2.0, 2.0):
            self._add_field("duration_range", duration_range)
        if not control_flags == []:
            self._add_field("control_flags", control_flags)

    def on_end(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self

    def on_start(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self


class EntityAITimerFlag3(_ai_goal):
    _identifier = "minecraft:behavior.timer_flag_3"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (10.0, 10.0),
        duration_range: tuple[Seconds, Seconds] = (2.0, 2.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping to due the timeout or due to being interrupted by another behavior, the goal fires another event. query.timer_flag_3 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): The goal cooldown range, in seconds. Defaults to (10.0, 10.0).
            duration_range (tuple[Seconds, Seconds], optional): The goal duration range, in seconds. Defaults to (2.0, 2.0).

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_3
        """
        super().__init__("behavior.timer_flag_3")

        if cooldown_range != (10.0, 10.0):
            self._add_field("cooldown_range", cooldown_range)
        if duration_range != (2.0, 2.0):
            self._add_field("duration_range", duration_range)
        if not control_flags == []:
            self._add_field("control_flags", control_flags)

    def on_end(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self

    def on_start(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self


class EntityAIRunAroundLikeCrazy(_ai_goal):
    _identifier = "minecraft:behavior.run_around_like_crazy"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity to run around without a set goal.

        Parameters:
            priority (int, optional): The higher the priority, the sooner this behavior will be executed as a goal. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_run_around_like_crazy
        """
        super().__init__("behavior.run_around_like_crazy")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAISlimeKeepOnJumping(_ai_goal):
    _identifier = "minecraft:behavior.slime_keep_on_jumping"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Compels an entity to continuously jump around like a slime.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_keep_on_jumping
        """
        super().__init__("behavior.slime_keep_on_jumping")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIRiseToLiquidLevel(_ai_goal):
    _identifier = "minecraft:behavior.rise_to_liquid_level"

    def __init__(
        self,
        liquid_y_offset: float = 0.0,
        rise_delta: float = 0.0,
        sink_delta: float = 0.0,
    ) -> None:
        """Compels an entity to rise to the top of a liquid block if they are located in one or have spawned under a liquid block.

        Parameters:
            liquid_y_offset (float, optional): Vertical offset from the liquid. Defaults to 0.0.
            priority (int, optional): The higher the priority, the sooner this behavior will be executed as a goal. Defaults to 0.
            rise_delta (float, optional): Displacement for how much the entity will move up in the vertical axis. Defaults to 0.0.
            sink_delta (float, optional): Displacement for how much the entity will move down in the vertical axis. Defaults to 0.0.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_rise_to_liquid_level
        """
        super().__init__("behavior.rise_to_liquid_level")

        if liquid_y_offset != 0.0:
            self._add_field("liquid_y_offset", liquid_y_offset)
        if rise_delta != 0.0:
            self._add_field("rise_delta", rise_delta)
        if sink_delta != 0.0:
            self._add_field("sink_delta", sink_delta)
