import math
from typing import Any

from anvil.api.blocks.components import LootTable
from anvil.api.core.components import (
    AIGoal,
    Component,
    EventTrigger,
)
from anvil.api.core.enums import (
    BreedingMutationStrategy,
    ContainerType,
    ControlFlags,
    DamageCause,
    DamageSensor,
    Difficulty,
    ExplosionParticleEffect,
    FilterSubject,
    LeashSpringType,
    LineOfSightObstructionType,
    LookAtLocation,
    LootedAtSetTarget,
    RideableDismountMode,
    Slots,
    Vibrations,
)
from anvil.api.core.filters import Filter
from anvil.api.core.types import *
from anvil.api.logic.molang import Molang
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.api.vanilla.effects import MinecraftEffects
from anvil.api.world.trade_tables import TradeTable
from anvil.lib.config import CONFIG
from anvil.lib.format_versions import ENTITY_SERVER_VERSION
from anvil.lib.lib import AnvilFormatter, clamp
from anvil.lib.schemas import (
    MinecraftBlockDescriptor,
    MinecraftEntityDescriptor,
    MinecraftItemDescriptor,
)
from anvil.lib.translator import AnvilTranslator

# Components ==========================================================================
# Attributes ==========================================================================


class EntityAddRider(Component):
    _identifier = "minecraft:addrider"

    def __init__(
        self,
        entity_type: MinecraftEntityDescriptor | Identifier,
        spawn_event: str = None,
    ) -> None:
        """Adds a rider to the entity.

        Parameters:
            entity_type (MinecraftEntityDescriptor | Identifier): The entity type that will be riding this entity.
            spawn_event (str, optional): The spawn event that will be used when the riding entity is created. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_addrider
        """
        super().__init__("addrider")
        # self._require_components(EntityRideable)
        self._add_field(
            "riders", [{"entity_type": entity_type, "spawn_event": spawn_event}]
        )

    def add_rider(
        self,
        entity_type: MinecraftEntityDescriptor | Identifier,
        spawn_event: str = None,
    ):
        """Adds an additional rider to the entity. Requires `minecraft:rideable.`.

        Parameters:
        `entity_type` : `MinecraftEntityDescriptor` | `Identifier`.
            The type of entity to add as a rider.
        `spawn_event` : `str`, optional.
            An event to run when the rider is spawned.

        """
        self._component["riders"].append(
            {"entity_type": entity_type, "spawn_event": spawn_event}
        )
        return self


class EntityAdmireItem(Component):
    _identifier = "minecraft:admire_item"

    def __init__(
        self, cooldown_after_being_attacked: Seconds, duration: Seconds = 10
    ) -> None:
        """Allows an entity to ignore attackable targets for a given duration.

        Parameters:
            cooldown_after_being_attacked (Seconds): Duration, in seconds, for which mob won't admire items if it was hurt.
            duration (Seconds, optional): Duration, in seconds, that the mob is pacified. `Default: 10`. Defaults to 10.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_admire_item
        """
        super().__init__("admire_item")
        self._add_field("cooldown_after_being_attacked", cooldown_after_being_attacked)
        if duration != 10:
            self._add_field("duration", duration)


class EntityCollisionBox(Component):
    _identifier = "minecraft:collision_box"

    def __init__(self, height: float, width: float) -> None:
        """Sets the width and height of the Entity's collision box.

        Parameters:
            height (float): Height of the collision box in blocks. A negative value will be assumed to be 0.
            width (float): Width of the collision box in blocks. A negative value will be assumed to be 0. Min value is -100000000.000000 Max value is 100000000.000000.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_collision_box
        """
        super().__init__("collision_box")
        self._add_field("height", max(0, height))
        self._add_field("width", max(0, width))


class EntityTypeFamily(Component):
    _identifier = "minecraft:type_family"

    def __init__(self, family: list[str]) -> None:
        """Defines the family categories this entity belongs to. Type families are used by filters and other game systems to group entities (e.g., 'mob', 'monster', 'undead', 'zombie').

        Parameters:
            family (list[str]): A set of tags that describe the categories of this entity.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_type_family
        """
        super().__init__("type_family")
        self._add_field("family", family)


class EntityInstantDespawn(Component):
    _identifier = "minecraft:instant_despawn"

    def __init__(self, remove_child_entities: bool = False) -> None:
        """Despawns the Actor immediately.

        Parameters:
            remove_child_entities (bool, optional): If true, all entities linked to this entity in a child relationship (eg. leashed) will also be despawned. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_instant_despawn
        """
        super().__init__("instant_despawn")
        if remove_child_entities:
            self._add_field("remove_child_entities", True)


class EntityHealth(Component):
    _identifier = "minecraft:health"

    def __init__(self, value: int, min: int = None, max: int = None) -> None:
        """Defines the health pool for an entity, measured in health points (1 point = half a heart). Typical values: cow (10), zombie (20), iron golem (100), wither (600).

        Parameters:
            value (int): Starting health for this entity in health points (1 point = half a heart).
            min (int, optional): Description. Defaults to None.
            max (int, optional): Maximum health this entity can have. Can be higher than the starting value to allow healing beyond initial health. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_health
        """
        super().__init__("health")
        self._add_field("value", value)
        if not max is None:
            self._add_field("max", max)
        if not min is None:
            self._add_field("min", min)


class EntityPhysics(Component):
    _identifier = "minecraft:physics"

    def __init__(
        self,
        has_collision: bool = True,
        has_gravity: bool = True,
        push_towards_closest_space: bool = False,
    ) -> None:
        """Defines physics properties of an actor, including if it is affected by gravity or if it collides with objects.

        Parameters:
            has_collision (bool, optional): Whether or not the entity collides with things. Defaults to True.
            has_gravity (bool, optional): Whether or not the entity is affected by gravity. Defaults to True.
            push_towards_closest_space (bool, optional): Whether or not the entity should be pushed towards the nearest open area when stuck inside a block. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_physics
        """
        super().__init__("physics")
        if not has_collision:
            self._add_field("has_collision", has_collision)
        if not has_gravity:
            self._add_field("has_gravity", has_gravity)
        if push_towards_closest_space:
            self._add_field("push_towards_closest_space", push_towards_closest_space)


class EntityKnockbackResistance(Component):
    _identifier = "minecraft:knockback_resistance"

    def __init__(self, value: float) -> None:
        """Determines an entity's resistance to knockback from melee attacks. A value of 0.0 means no resistance, while 1.0 provides full immunity to knockback (like iron golems).

        Parameters:
            value (float): The amount of knockback resistance, from 0.0 (none) to 1.0 (full immunity).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_knockback_resistance
        """
        super().__init__("knockback_resistance")
        self._add_field("value", max(0, min(1, value)))


class EntityPushableByBlock(Component):
    _identifier = "minecraft:pushable_by_block"

    def __init__(self, value: bool) -> None:
        """Allows the entity to be pushed by certain blocks, like Shulker Boxes and Pistons.

        Parameters:
            value (bool): Description.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable_by_block
        """
        super().__init__("pushable_by_block")
        self._set_value(value)


class EntityPushableByEntity(Component):
    _identifier = "minecraft:pushable_by_entity"

    def __init__(self, value: bool) -> None:
        """Allows an entity to be pushed by other entities.

        Parameters:
            value (bool): Description.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable_by_entity
        """
        super().__init__("pushable_by_entity")
        self._set_value(value)


class EntityPushThrough(Component):
    _identifier = "minecraft:push_through"

    def __init__(self, value: float) -> None:
        """Sets the distance through which the entity can push through.

        Parameters:
            value (float): The value of the entity's push-through, in blocks.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_push_through
        """
        super().__init__("push_through")
        self._add_field("value", value)


class EntityMovement(Component):
    _identifier = "minecraft:movement"

    def __init__(self, value: int, max: int = None) -> None:
        """Defines the base movement speed of an entity. Typical values: creeper (0.2), cow (0.25), zombie baby (0.35).

        Parameters:
            value (int): The base movement speed value. Higher values result in faster movement. Can be a single number or a range object with range_min and range_max properties.
            max (int, optional): Maximum movement speed this entity can have. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement
        """
        super().__init__("movement")
        self._add_field("value", value)
        if not max is None:
            self._add_field("max", max)


class EntityTickWorld(Component):
    _identifier = "minecraft:tick_world"

    def __init__(
        self,
        never_despawn: bool = True,
        radius: int = 0,
        distance_to_players: int = 0,
    ) -> None:
        """Defines if the entity ticks the world and the radius around it to tick.

        Parameters:
            never_despawn (bool, optional): If true, this entity will not despawn even if players are far away. If false, distance_to_players will be used to determine when to despawn. Defaults to True.
            radius (int, optional): The area around the entity to tick. Value must be >= 2. Value must be <= 6. Defaults to 0.
            distance_to_players (int, optional): The distance at which the closest player has to be before this entity despawns. This option will be ignored if never_despawn is true. Value must be >= 128. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tick_world
        """
        super().__init__("tick_world")
        self._add_field("never_despawn", never_despawn)
        if radius != 0:
            self._add_field("radius", clamp(radius, 2, 6))
        if distance_to_players != 0:
            self._add_field("distance_to_players", distance_to_players)


class EntityCustomHitTest(Component):
    _identifier = "minecraft:custom_hit_test"

    def __init__(
        self, height: float, width: float, pivot: list[float, float, float] = [0, 1, 0]
    ) -> None:
        """List of hitboxes for melee and ranged hits against the entity.

        Parameters:
            height (float): Height of the hitbox.
            width (float): Width of the hitbox.
            pivot (list[float, float, float], optional): Pivot point of the hitbox. Defaults to [0, 1, 0].

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_custom_hit_test
        """
        super().__init__("custom_hit_test")
        self._add_field(
            "hitboxes", [{"width": width, "height": height, "pivot": pivot}]
        )

    def add_hitbox(
        self, height: float, width: float, pivot: list[float, float, float] = [0, 1, 0]
    ):
        self._component["hitboxes"].append(
            {"width": width, "height": height, "pivot": pivot}
        )
        return self


class EntityCanClimb(Component):
    _identifier = "minecraft:can_climb"

    def __init__(self) -> None:
        """Allows an entity to climb ladders.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_climb
        """
        super().__init__("can_climb")


class EntityAttack(Component):
    _identifier = "minecraft:attack"

    def __init__(
        self, damage: int, effect_duration: int = None, effect_name: str = None
    ) -> None:
        """Defines an entity's melee attack damage and any additional status effects applied on hit. Typical damage values range from 3 (zombie, creeper) to 7-21 (iron golem).

        Parameters:
            damage (int): Range of the random amount of damage the melee attack deals.
            effect_duration (int, optional): Duration in seconds of the status ailment applied to the damaged entity. Defaults to None.
            effect_name (str, optional): Identifier of the status ailment to apply to an entity attacked by this entity's melee attack. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack
        """
        super().__init__("attack")
        self._add_field("damage", damage)
        if not effect_duration is None:
            self._add_field("effect_duration", effect_duration)
        if not effect_name is None:
            self._add_field("effect_name", effect_name)


class EntityJumpStatic(Component):
    _identifier = "minecraft:jump.static"

    def __init__(self, jump_power: float = 0.42) -> None:
        """Gives the entity the ability to jump.

        Parameters:
            jump_power (float, optional): The initial vertical velocity for the jump. Defaults to 0.42.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_jump.static?view=minecraft-bedrock-stable
        """
        super().__init__("jump.static")
        self._add_field("jump_power", jump_power)


class EntityJumpDynamic(Component):
    _identifier = "minecraft:jump.dynamic"

    def __init__(self) -> None:
        """Defines a dynamic type jump control that will change jump properties based on the speed modifier of the mob. Requires `minecraft:movement.skip` to be used.

        ## Documentation reference:
            https://learn.microsoft.com/pt-br/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_jump.dynamic
        """
        super().__init__("jump.dynamic")

    def regular_skip_data(
        self,
        animation_duration: float,
        distance_scale: float,
        height: float,
        jump_delay: float,
    ):
        """Sets the regular skip data for the entity's jump.

        Args:
            animation_duration (float): Duration of the jump animation.
            distance_scale (float): The multiplier applied to horizontal velocity when jumping.
            height (float): The force applied vertically when jumping.
            jump_delay (float): Amount of ticks between sequential jumps.
        """
        self._add_field(
            "regular_skip_data",
            {
                "animation_duration": animation_duration,
                "distance_scale": distance_scale,
                "height": height,
                "jump_delay": jump_delay,
            },
        )
        return self

    def fast_skip_data(
        self,
        animation_duration: float,
        distance_scale: float,
        height: float,
        jump_delay: float,
    ):
        """Sets the fast skip data for the entity's jump.

        Args:
            animation_duration (float): Duration of the jump animation.
            distance_scale (float): The multiplier applied to horizontal velocity when jumping.
            height (float): The force applied vertically when jumping.
            jump_delay (float): Amount of ticks between sequential jumps.
        """
        self._add_field(
            "fast_skip_data",
            {
                "animation_duration": animation_duration,
                "distance_scale": distance_scale,
                "height": height,
                "jump_delay": jump_delay,
            },
        )
        return self


class EntityHorseJumpStrength(Component):
    _identifier = "minecraft:horse.jump_strength"

    def __init__(self, range_min: float, range_max: float) -> None:
        """Determines the jump height for a horse or similar entity, like a donkey.

        Parameters:
            range_min (float): Defines the minimum strength level.
            range_max (float): Defines the maximum strength level.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_horse.jump_strength?view=minecraft-bedrock-stable
        """
        super().__init__("horse.jump_strength")
        self._add_field("value", {"range_min": range_min, "range_max": range_max})


class EntitySpellEffects(Component):
    _identifier = "minecraft:spell_effects"

    def __init__(self) -> None:
        """Allows an entity to add or remove status effects from itself. Similarly to `addrider`, this component performs a one-time operation on the entity when added. Removing the component will not change the entity's current effects. Adding different versions of the component multiple times will perform each one in turn. Once the component has been added, it will not provide any further functionality. There is one exception to this behavior: if this component is present on a player, its effects will be re-applied every time the player enters the world. To avoid this, remove the component shortly after adding it, or add an empty component to replace it.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spell_effects
        """
        super().__init__("spell_effects")
        self._add_field("add_effects", [])
        self._add_field("remove_effects", [])

    def add_effects(
        self,
        effect: MinecraftEffects,
        duration: int | Literal["infinite"],
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

    def remove_effects(self, *effects: MinecraftEffects):
        self._component["remove_effects"] = [e.value for e in effects]
        return self


class EntityFrictionModifier(Component):
    _identifier = "minecraft:friction_modifier"

    def __init__(self, value: int) -> None:
        """Defines how much friction affects this entity.

        Parameters:
            value (int): The higher the number, the more friction affects this entity. A value of 1.0 means regular friction, while 2.0 means twice as much.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_friction_modifier
        """
        super().__init__("friction_modifier")
        self._add_field("value", value)


class EntityVariant(Component):
    _identifier = "minecraft:variant"

    def __init__(self, value: int) -> None:
        """Variant is typically used as a per-type way to express a different visual form of the same mob. For example, for cats, variant is a number that defines the breed of cat.

        Parameters:
            value (int): The Id of the variant. By convention, 0 is the Id of the base entity/default appearance.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variant
        """
        super().__init__("variant")
        self._add_field("value", value)


class EntityMarkVariant(Component):
    _identifier = "minecraft:mark_variant"

    def __init__(self, value: int) -> None:
        """Mark Variant is typically used as an additional per-type way (besides `variant`) to express a different visual form of the same mob.

        Parameters:
            value (int): The Id of the mark_variant. By convention, 0 is the Id of the base entity.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mark_variant
        """
        super().__init__("mark_variant")
        self._add_field("value", value)


class EntitySkinID(Component):
    _identifier = "minecraft:skin_id"

    def __init__(self, value: int) -> None:
        """Skin ID value. Can be used to differentiate skins, such as base skins for villagers.

        Parameters:
            value (int): The ID of the skin. By convention, 0 is the ID of the base skin.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_skin_id
        """
        super().__init__("skin_id")
        self._add_field("value", value)


class EntityScale(Component):
    _identifier = "minecraft:scale"

    def __init__(self, value: int) -> None:
        """Sets the entity's visual size multiplier. A value of 1.0 means normal size, 0.5 is half size (commonly used for baby mobs), and values above 1.0 make the entity larger.

        Parameters:
            value (int): The scale multiplier for visual size. 1.0 = normal, 0.5 = half (babies), 2.0 = double size.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scale
        """
        super().__init__("scale")
        self._add_field("value", value)


class EntityScaleByAge(Component):
    _identifier = "minecraft:scale_by_age"

    def __init__(self, start_scale: int, end_scale: int) -> None:
        """Defines the entity's size interpolation based on the entity's age.

        Parameters:
            start_scale (int): Initial scale of the newborn entity.
            end_scale (int): Ending scale of the entity when it's fully grown.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scale_by_age
        """
        super().__init__("scale_by_age")
        self._add_field("end_scale", end_scale)
        self._add_field("start_scale", start_scale)


class EntityAreaAttack(Component):
    _identifier = "minecraft:area_attack"

    def __init__(
        self,
        cause: DamageCause,
        damage_per_tick: int = 2,
        damage_range: float = 0.2,
        damage_cooldown: Seconds | None = None,
    ) -> None:
        """A component that does damage to entities that get within range.

        Parameters:
            cause (DamageCause): The type of damage that is applied to entities that enter the damage range.
            damage_per_tick (int, optional): How much damage per tick is applied to entities that enter the damage range. Defaults to 2.
            damage_range (float, optional): How close a hostile entity must be to have the damage applied. Defaults to 0.2.
            damage_cooldown (Seconds | None, optional): Attack cooldown (in seconds) for how often this entity can attack a target. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_area_attack
        """
        super().__init__("area_attack")

        self._add_field("cause", cause.value)

        if damage_per_tick != 2:
            self._add_field("damage_per_tick", damage_per_tick)
        if damage_range != 0.2:
            self._add_field("damage_range", damage_range)
        if damage_cooldown is not None:
            self._add_field("damage_cooldown", max(0.0, damage_cooldown))

    def filter(self, entity_filter: dict):
        self._add_field("entity_filter", entity_filter)
        return self


class EntityIsStackable(Component):
    _identifier = "minecraft:is_stackable"

    def __init__(self) -> None:
        """Allows instances of this entity to have vertical and horizontal collisions with each other. For a collision to occur, both instances must have a "minecraft:collision_box" component. Stackable behavior is closely related to collidable behavior. While the "minecraft:is_stackable" component describes how an entity interacts with others of its own kind, the "minecraft:is_collidable" component governs how other mobs interact with the component's owner.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_stackable
        """
        super().__init__("is_stackable")


class EntityIsIllagerCaptain(Component):
    _identifier = "minecraft:is_illager_captain"

    def __init__(self) -> None:
        """Sets that this entity is an Illager Captain.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_illager_captain
        """
        super().__init__("is_illager_captain")


class EntityIsBaby(Component):
    _identifier = "minecraft:is_baby"

    def __init__(self) -> None:
        """Sets that this entity is a baby. This is used to set the is_baby value for use in query functions like Molang and Filters.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_baby
        """
        super().__init__("is_baby")


class EntityIsIgnited(Component):
    _identifier = "minecraft:is_ignited"

    def __init__(self) -> None:
        """Sets that this entity is currently on fire.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_ignited
        """
        super().__init__("is_ignited")


class EntityIsTamed(Component):
    _identifier = "minecraft:is_tamed"

    def __init__(self) -> None:
        """Sets that this entity is currently tamed.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_tamed
        """
        super().__init__("is_tamed")


class EntityIsCharged(Component):
    _identifier = "minecraft:is_charged"

    def __init__(self) -> None:
        """Sets that this entity is charged. This is used to set the is_charged value for use in query functions like Molang and Filters.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_charged
        """
        super().__init__("is_charged")


class EntityIsStunned(Component):
    _identifier = "minecraft:is_stunned"

    def __init__(self) -> None:
        """Sets that this entity is currently stunned.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_stunned
        """
        super().__init__("is_stunned")


class EntityIsSaddled(Component):
    _identifier = "minecraft:is_saddled"

    def __init__(self) -> None:
        """Sets that this entity is currently saddled.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_saddled
        """
        super().__init__("is_saddled")


class EntityIsSheared(Component):
    _identifier = "minecraft:is_sheared"

    def __init__(self) -> None:
        """Sets that this entity is currently sheared.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_sheared
        """
        super().__init__("is_sheared")


class EntityCanFly(Component):
    _identifier = "minecraft:can_fly"

    def __init__(self) -> None:
        """Marks the entity as being able to fly, the pathfinder won't be restricted to paths where a solid block is required underneath it.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_fly
        """
        super().__init__("can_fly")


class EntityCanPowerJump(Component):
    _identifier = "minecraft:can_power_jump"

    def __init__(self) -> None:
        """Allows the entity to power jump like the Horse does in Vanilla.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_power_jump
        """
        super().__init__("can_power_jump")


class EntityIsChested(Component):
    _identifier = "minecraft:is_chested"

    def __init__(self) -> None:
        """Sets that this entity is currently carrying a chest.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_chested
        """
        super().__init__("is_chested")


class EntityOutOfControl(Component):
    _identifier = "minecraft:out_of_control"

    def __init__(self) -> None:
        """Defines the entity's 'out of control' state.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_out_of_control
        """
        super().__init__("out_of_control")


class EntityDamageSensor(Component):
    _identifier = "minecraft:damage_sensor"

    def __init__(self) -> None:
        """Defines what events to call when this entity is damaged by specific entities or items.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_sensor
        """
        super().__init__("damage_sensor")
        self._add_field("triggers", [])

    def add_trigger(
        self,
        cause: DamageCause,
        deals_damage: DamageSensor | bool = DamageSensor.Yes,
        on_damage_event: str = None,
        on_damage_filter: Filter = None,
        damage_multiplier: int = 1,
        damage_modifier: float = 0,
    ):
        if isinstance(deals_damage, bool):
            deals_damage = DamageSensor.Yes if deals_damage else DamageSensor.No

        damage = {"deals_damage": deals_damage, "on_damage": {}}
        if not cause is DamageCause.All:
            damage["cause"] = cause.value
        if not on_damage_event is None:
            damage["on_damage"] = {"event": on_damage_event}
        if not on_damage_filter is None:
            damage["on_damage"]["filters"] = on_damage_filter
        if damage_multiplier != 1:
            damage["damage_multiplier"] = damage_multiplier
        if damage_modifier != 0:
            damage["damage_modifier"] = damage_modifier

        self._get_field("triggers", []).append(damage)
        return self


class EntityFollowRange(Component):
    _identifier = "minecraft:follow_range"

    def __init__(self, value: int, max_range: int = None) -> None:
        """Defines the maximum range, in blocks, that a mob will pursue a target. This affects AI behaviors like chasing players or attacking.

        Parameters:
            value (int): The default follow range in blocks. Entities will attempt to stay within this radius of their target.
            max_range (int, optional): Maximum follow distance in blocks. The entity will not pursue targets beyond this range. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_follow_range
        """
        super().__init__("follow_range")
        self._add_field("value", value)
        if not max_range is None:
            self._add_field("max", max_range)


class EntityMovementType:
    _component_types = [
        "minecraft:movement.basic",
        "minecraft:movement.amphibious",
        "minecraft:movement.dolphin",
        "minecraft:movement.fly",
        "minecraft:movement.generic",
        "minecraft:movement.glide",
        "minecraft:movement.jump",
        "minecraft:movement.skip",
        "minecraft:movement.sway",
        "minecraft:movement.hover",
    ]

    @staticmethod
    def Basic(max_turn: float = 30):
        movement = Component("movement.basic")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        return movement

    @staticmethod
    def Amphibious(max_turn: float = 30):
        """Allows the mob to swim in water and walk on land."""
        movement = Component("movement.amphibious")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        return movement

    @staticmethod
    def Dolphin() -> None:
        """Allows the mob to swim in water like a dolphin."""
        movement = Component("movement.dolphin")
        return movement

    @staticmethod
    def Fly(
        max_turn: float = 30,
        start_speed: float = 0.1,
        speed_when_turning: float = 0.2,
    ) -> None:
        """Causes the mob to fly."""
        movement = Component("movement.fly")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        if start_speed != 0.1:
            movement._add_field("start_speed", start_speed)
        if speed_when_turning != 0.2:
            movement._add_field("speed_when_turning", speed_when_turning)
        return movement

    @staticmethod
    def Generic(max_turn: float = 30):
        """Allows a mob to fly, swim, climb, etc."""
        movement = Component("movement.generic")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        return movement

    @staticmethod
    def Glide(
        max_turn: float = 30,
        start_speed: float = 0.1,
        speed_when_turning: float = 0.2,
    ):
        """Is the move control for a flying mob that has a gliding movement."""
        movement = Component("movement.glide")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        if start_speed != 0.1:
            movement._add_field("start_speed", start_speed)
        if speed_when_turning != 0.2:
            movement._add_field("speed_when_turning", speed_when_turning)
        return movement

    @staticmethod
    def Jump(max_turn: float = 30, jump_delay: tuple[float, float] = (0, 0)):
        """Causes the mob to jump as it moves with a specified delay between jumps."""
        movement = Component("movement.jump")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        if jump_delay != (0, 0):
            movement._add_field("jump_delay", jump_delay)
        return movement

    @staticmethod
    def Skip(max_turn: float = 30):
        """Causes the mob to hop as it moves."""
        movement = Component("movement.skip")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        return movement

    @staticmethod
    def Sway(
        max_turn: float = 30,
        sway_amplitude: float = 0.05,
        sway_frequency: float = 0.5,
    ):
        """Causes the mob to sway side to side giving the impression it is swimming."""
        movement = Component("movement.sway")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        if sway_amplitude != 0.05:
            movement._add_field("sway_amplitude", sway_amplitude)
        if sway_frequency != 0.5:
            movement._add_field("sway_frequency", sway_frequency)
        return movement

    @staticmethod
    def Hover(max_turn: float = 30):
        """Causes the mob to hover."""
        movement = Component("movement.hover")
        if max_turn != 30:
            movement._add_field("max_turn", max_turn)
        return movement


class EntityNavigationType:
    @staticmethod
    def _basic(
        cls: Component,
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
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
                isinstance(block, (MinecraftBlockDescriptor, str))
                for block in blocks_to_avoid
            ):
                raise TypeError(
                    f"blocks_to_avoid must be a list of MinecraftBlockDescriptor or Identifier instances. Component [{cls._identifier}]."
                )

            cls._add_field(
                "blocks_to_avoid",
                [str(block) for block in blocks_to_avoid],
            )

        return cls

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths that include vertical walls like the vanilla Spiders do."""
        navigation = Component("navigation.climb")
        EntityNavigationType._basic(
            navigation,
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

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths by flying around the air like the regular Ghast."""
        navigation = Component("navigation.float")
        EntityNavigationType._basic(
            navigation,
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

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths in the air like the vanilla Parrots do."""
        navigation = Component("navigation.fly")
        EntityNavigationType._basic(
            navigation,
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

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths by walking, swimming, flying and/or climbing around and jumping up and down a block."""
        navigation = Component("navigation.generic")
        EntityNavigationType._basic(
            navigation,
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

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths in the air like the vanilla Bees do. Keeps them from falling out of the skies and doing predictive movement."""
        navigation = Component("navigation.hover")
        EntityNavigationType._basic(
            navigation,
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

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths that include water."""
        navigation = Component("navigation.swim")
        EntityNavigationType._basic(
            navigation,
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

    @staticmethod
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
        blocks_to_avoid: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        """Allows this entity to generate paths by walking around and jumping up and down a block like regular mobs."""
        navigation = Component("navigation.walk")
        EntityNavigationType._basic(
            navigation,
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


class EntityEnvironmentSensor(Component):
    _identifier = "minecraft:environment_sensor"

    def __init__(self) -> None:
        """Creates a trigger based on environment conditions.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_environment_sensor
        """
        super().__init__("environment_sensor")
        self._add_field("triggers", [])

    def trigger(self, event: str, filters: Filter):
        self._component["triggers"].append({"filters": filters, "event": event})
        return self


class EntityPreferredPath(Component):
    _identifier = "minecraft:preferred_path"

    def __init__(
        self, default_block_cost: int = 0, jump_cost: int = 0, max_fall_blocks: int = 3
    ) -> None:
        """Specifies costing information for mobs that prefer to walk on preferred paths.

        Parameters:
            default_block_cost (int, optional): Cost for non-preferred blocks. Defaults to 0.
            jump_cost (int, optional): Added cost for jumping up a node. Defaults to 0.
            max_fall_blocks (int, optional): Distance mob can fall without taking damage. Defaults to 3.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_preferred_path
        """
        super().__init__("preferred_path")
        self._add_field("default_block_cost", default_block_cost)
        self._add_field("jump_cost", jump_cost)
        self._add_field("max_fall_blocks", max_fall_blocks)
        self._add_field("preferred_path_blocks", [])

    def add_blocks(
        self, cost: int, blocks: list[MinecraftBlockDescriptor | Identifier]
    ):
        if not all(
            isinstance(block, (MinecraftBlockDescriptor, str)) for block in blocks
        ):
            raise TypeError(
                f"blocks must be a list of MinecraftBlockDescriptor or Identifier instances. Component [{self._identifier}]."
            )

        self._component["preferred_path_blocks"].append(
            {
                "cost": cost,
                "blocks": [str(block) for block in blocks],
            }
        )
        return self


class EntityTargetNearbySensor(Component):
    _identifier = "minecraft:target_nearby_sensor"

    def __init__(
        self, inside_range: int = 1, outside_range: int = 5, must_see: bool = False
    ) -> None:
        """Defines the entity's range within which it can see or sense other entities to target them.

        Parameters:
            inside_range (int, optional): Maximum distance in blocks that another entity will be considered in the 'inside' range. Defaults to 1.
            outside_range (int, optional): Maximum distance in blocks that another entity will be considered in the 'outside' range. Defaults to 5.
            must_see (bool, optional): Whether the other entity needs to be visible to trigger 'inside' events. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_target_nearby_sensor
        """
        super().__init__("target_nearby_sensor")
        self._add_field("inside_range", inside_range)
        self._add_field("outside_range", outside_range)
        self._add_field("must_see", must_see)

    def on_inside_range(self, event: str, target: FilterSubject):
        self._add_field("on_inside_range", {"event": event, "target": target.value})
        return self

    def on_outside_range(self, event: str, target: FilterSubject):
        self._add_field("on_outside_range", {"event": event, "target": target.value})
        return self

    def on_vision_lost_inside_range(self, event: str, target: FilterSubject):
        self._add_field(
            "on_vision_lost_inside_range", {"event": event, "target": target.value}
        )
        return self


class EntityRideable(Component):
    _identifier = "minecraft:rideable"

    def __init__(
        self,
        interact_text: str = "Mount",
        controlling_seat: int = 0,
        passenger_max_width: float = None,
        crouching_skip_interact: bool = True,
        pull_in_entities: bool = False,
        rider_can_interact: bool = False,
        dismount_mode: RideableDismountMode = RideableDismountMode.Default,
        on_rider_enter_event: str = None,
        on_rider_exit_event: str = None,
    ) -> None:
        """This entity can be ridden.

        Parameters:
            interact_text (str, optional): The text to display when the player can interact with the entity when playing with touch-screen controls. Defaults to 'Mount'.
            controlling_seat (int, optional): The seat that designates the driver of the entity. Entities with the "minecraft:behavior.controlled_by_player" goal ignore this field and give control to any player in any seat. Defaults to 0.
            passenger_max_width (float, optional): The max width a mob can have to be a rider. A value of 0 ignores this parameter. Defaults to None.
            crouching_skip_interact (bool, optional): If true, this entity can't be interacted with if the entity interacting with it is crouching. Defaults to True.
            pull_in_entities (bool, optional): If true, this entity will pull entities matching the specified "family_types" into any available seats. Defaults to False.
            rider_can_interact (bool, optional): If true, this entity will be picked when looked at by the rider. Defaults to False.
            dismount_mode (RideableDismountMode, optional): Defines where riders are placed when dismounting this entity: - "default", riders are placed on a valid ground position around the entity, or at the center of the entity's collision box if none is found. Defaults to RideableDismountMode.Default.
            on_rider_enter_event (str, optional): Event to execute on the owner entity when an entity starts riding it. This item requires a format version of at least 1.21.80. Defaults to None.
            on_rider_exit_event (str, optional): Event to execute on the owner entity when an entity stops riding it. This item requires a format version of at least 1.21.80. Defaults to None.

        ## Behaviour Observations:
            Adding a rider makes them occupy the first available seat on the rideable entity.
            Removing a rider at any seat will shift all subsequent riders forward by one seat.
            Unless the rider is a Player in which case they will occupy the very first seat and shift all other riders back by one seat.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rideable
        """
        super().__init__("rideable")
        self._seat_count = 0

        if interact_text != "Mount":
            t = interact_text.lower().replace(" ", "_")
            self._add_field("interact_text", f"action.interact.{t}")
            AnvilTranslator().add_localization_entry(
                f"action.interact.{t}", interact_text
            )

        self._add_field("controlling_seat", controlling_seat)
        if passenger_max_width is not None:
            self._add_field("passenger_max_width", max(0.0, passenger_max_width))
        if not crouching_skip_interact:
            self._add_field("crouching_skip_interact", crouching_skip_interact)
        if pull_in_entities:
            self._add_field("pull_in_entities", pull_in_entities)
        if rider_can_interact:
            self._add_field("rider_can_interact", rider_can_interact)
        if dismount_mode != RideableDismountMode.Default:
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
                "lock_rider_rotation": (
                    lock_rider_rotation if lock_rider_rotation != 181 else {}
                ),
                "min_rider_count": min_rider_count if min_rider_count != 0 else {},
                "rotate_rider_by": rotate_rider_by if rotate_rider_by != 0 else {},
                "third_person_camera_radius": (
                    third_person_camera_radius
                    if third_person_camera_radius != 1.0
                    else {}
                ),
                "camera_relax_distance_smoothing": (
                    camera_relax_distance_smoothing
                    if camera_relax_distance_smoothing != 1.0
                    else {}
                ),
            }
        )

        return self

    def family_types(self, families: list[str]):
        self._add_field("family_types", families)
        return self


class EntityProjectile(Component):
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
        hit_water: bool = False,
        homing: bool = False,
        inertia: float = 0.99,
        is_dangerous: bool = False,
        knockback: bool = True,
        lightning: bool = False,
        liquid_inertia: float = 0.6,
        multiple_targets: bool = True,
        offset: Coordinates = (0, 0.5, 0),
        on_fire_time: float = 5.0,
        particle: str = "iconcrack",
        potion_effect: int = -1,
        power: float = 1.3,
        reflect_on_hurt: bool = False,
        semi_random_diff_damage: bool = False,
        shoot_sound: str = "",
        shoot_target: bool = True,
        should_bounce: bool = False,
        splash_potion: bool = False,
        splash_range: float = 4.0,
        stop_on_hurt: bool = False,
        uncertainty_base: float = 0.0,
        uncertainty_multiplier: float = 0.0,
    ) -> None:
        """Allows the entity to be a thrown entity.

        Parameters:
            anchor (int, optional): . Defaults to 0.
            angle_offset (float, optional): Determines the angle at which the projectile is thrown. Defaults to 0.
            catch_fire (bool, optional): Determines whether the entity hit will be set on fire. Defaults to False.
            crit_particle_on_hurt (bool, optional): If true, the projectile will produce additional particles when a critical hit happens. Defaults to False.
            destroy_on_hurt (bool, optional): If true, this entity will be destroyed when hit. Defaults to False.
            fire_affected_by_griefing (bool, optional): If true, whether the projectile causes fire is affected by the mob griefing game rule. Defaults to False.
            gravity (float, optional): The gravity applied to this entity when thrown. The higher the value, the faster the entity falls. Defaults to 0.05.
            hit_sound (str, optional): The sound that plays when the projectile hits something. Defaults to ''.
            hit_ground_sound (str, optional): . Defaults to ''.
            hit_water (bool, optional): . Defaults to False.
            homing (bool, optional): If true, the projectile homes in to the nearest entity. Defaults to False.
            inertia (float, optional): The fraction of the projectile's speed maintained every frame while traveling in air. Defaults to 0.99.
            is_dangerous (bool, optional): If true, the projectile will be treated as dangerous to the players. Defaults to False.
            knockback (bool, optional): If true, the projectile will knock back the entity it hits. Defaults to True.
            lightning (bool, optional): If true, the entity hit will be struck by lightning. Defaults to False.
            liquid_inertia (float, optional): The fraction of the projectile's speed maintained every frame while traveling in water. Defaults to 0.6.
            multiple_targets (bool, optional): If true, the projectile can hit multiple entities per flight. Defaults to True.
            offset (Coordinates, optional): The offset from the entity's anchor where the projectile will spawn. Defaults to (0, 0.5, 0).
            on_fire_time (float, optional): Time in seconds that the entity hit will be on fire for. Defaults to 5.0.
            particle (str, optional): Particle to use upon collision. Defaults to 'iconcrack'.
            potion_effect (int, optional): Defines the effect the arrow will apply to the entity it hits. Defaults to -1.
            power (float, optional): Determines the velocity of the projectile. Defaults to 1.3.
            reflect_on_hurt (bool, optional): If true, this entity will be reflected back when hit. Defaults to False.
            semi_random_diff_damage (bool, optional): If true, damage will be randomized based on damage and speed. Defaults to False.
            shoot_sound (str, optional): The sound that plays when the projectile is shot. Defaults to ''.
            shoot_target (bool, optional): If true, the projectile will be shot towards the target of the entity firing it. Defaults to True.
            should_bounce (bool, optional): If true, the projectile will bounce upon hit. Defaults to False.
            splash_potion (bool, optional): If true, the projectile will be treated like a splash potion. Defaults to False.
            splash_range (float, optional): Radius in blocks of the 'splash' effect. Defaults to 4.0.
            stop_on_hurt (bool, optional): . Defaults to False.
            uncertainty_base (float, optional): The base accuracy. Accuracy is determined by the formula uncertaintyBase - difficultyLevel * uncertaintyMultiplier. Defaults to 0.0.
            uncertainty_multiplier (float, optional): Determines how much difficulty affects accuracy. Accuracy is determined by the formula uncertaintyBase - difficultyLevel * uncertaintyMultiplier. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_projectile
        """
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
        if hit_water:
            self._add_field("hit_water", hit_water)
        if homing:
            self._add_field("homing", homing)
        if inertia != 0.99:
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
        if offset != (0, 0.5, 0):
            self._add_field("offset", offset)
        if on_fire_time != 5.0:
            self._add_field("on_fire_time", on_fire_time)
        if particle != "iconcrack":
            self._add_field("particle", particle)
        if potion_effect != -1:
            self._add_field("potion_effect", potion_effect)
        if power != 1.3:
            self._add_field("power", power)
        if reflect_on_hurt:
            self._add_field("reflect_on_hurt", reflect_on_hurt)
        if semi_random_diff_damage:
            self._add_field("semi_random_diff_damage", semi_random_diff_damage)
        if shoot_sound != "":
            self._add_field("shoot_sound", shoot_sound)
        if not shoot_target:
            self._add_field("shoot_target", shoot_target)
        if should_bounce:
            self._add_field("should_bounce", should_bounce)
        if splash_potion:
            self._add_field("splash_potion", splash_potion)
        if splash_range != 4.0:
            self._add_field("splash_range", splash_range)
        if stop_on_hurt:
            self._add_field("stop_on_hurt", stop_on_hurt)
        if uncertainty_base != 0.0:
            self._add_field("uncertainty_base", uncertainty_base)
        if uncertainty_multiplier != 0.0:
            self._add_field("uncertainty_multiplier", uncertainty_multiplier)

        # Initialize on_hit dictionary to avoid checks in methods
        self._add_field("on_hit", {})

    def arrow_effect(self):
        """Enable arrow effect on hit.

        Note:
            Exact behavior unknown according to Bedrock Wiki.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["arrow_effect"] = {}
        return self

    def definition_event(
        self,
        event: str,
        target: FilterSubject,
        affect_projectile: bool = False,
        affect_shooter: bool = False,
        affect_splash_area: bool = False,
        splash_area: float = 0,
        affect_target: bool = False,
    ):
        """Call an event on hit.

        Args:
            event: Event to trigger.
            target: Target of the event.
            affect_projectile: Event will be triggered for projectile entity. Default is False.
            affect_shooter: Event will be triggered for shooter entity. Default is False.
            affect_splash_area: Event will be triggered for all entities in an area. Default is False.
            splash_area: Area of entities to affect. Default is 0.
            affect_target: Event will be triggered for hit entity. Default is False.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["definition_event"] = {
            "event_trigger": {"event": event, "target": target.value}
        }

        if affect_projectile:
            self._component["on_hit"]["definition_event"][
                "affect_projectile"
            ] = affect_projectile
        if affect_shooter:
            self._component["on_hit"]["definition_event"][
                "affect_shooter"
            ] = affect_shooter
        if affect_splash_area:
            self._component["on_hit"]["definition_event"][
                "affect_splash_area"
            ] = affect_splash_area
        if splash_area:
            self._component["on_hit"]["definition_event"]["splash_area"] = splash_area
        if affect_target:
            self._component["on_hit"]["definition_event"][
                "affect_target"
            ] = affect_target

        return self

    def filter(self, filter: Filter):
        """Set entity filter for the projectile.

        Args:
            filter: The filter to apply.

        Returns:
            Self for method chaining.
        """
        self._add_field("filter", filter)
        return self

    def freeze_on_hit(
        self,
        size: int,
        snap_to_block: bool,
        shape: str = "sphere",
    ):
        """Freeze water on hit.

        Args:
            size: The size of the freeze effect.
            snap_to_block: Whether to snap to block.
            shape: Shape of the freeze effect. Must be "sphere" or "cube". Default is "sphere".

        Returns:
            Self for method chaining.

        Note:
            Requires Education Edition toggle to be enabled.
            According to Bedrock Wiki, exact behavior is unknown.

        Raises:
            RuntimeError: If shape is not "sphere" or "cube".
        """
        self._component["on_hit"]["freeze_on_hit"] = {
            "size": size,
            "snap_to_block": snap_to_block,
        }
        if shape not in ["sphere", "cube"]:
            raise RuntimeError("Unknown shape, must be sphere or cube")
        self._component["on_hit"]["freeze_on_hit"]["shape"] = shape

        return self

    def grant_xp(self, xp: int | tuple[int, int]):
        """Grant experience points on hit.

        Args:
            xp: Experience to grant. If int, grants constant amount. If tuple, grants random amount between min and max.

        Returns:
            Self for method chaining.

        Note:
            Despite the name, this actually spawns a number of experience orbs, being worth the amount stated.

        Raises:
            ValueError: If xp is not an int or tuple of two ints.
        """
        if isinstance(xp, int):
            self._component["on_hit"]["grant_xp"] = {"xp": xp}
        elif isinstance(xp, tuple) and len(xp) == 2:
            if xp[0] == xp[1]:
                self._component["on_hit"]["grant_xp"] = {"xp": xp[0]}
            else:
                self._component["on_hit"]["grant_xp"] = {
                    "minXP": min(xp),
                    "maxXP": max(xp),
                }
        else:
            raise ValueError("xp must be an int or tuple of two ints")

        return self

    def hurt_owner(
        self,
        owner_damage: int = 0,
        knockback: bool = False,
        ignite: bool = False,
    ):
        """Configure projectile to potentially hurt its owner on hit.

        Args:
            owner_damage: Damage dealt to the owner. Default is 0.
            knockback: Whether to apply knockback to owner. Default is False.
            ignite: Whether to ignite the owner. Default is False.

        Returns:
            Self for method chaining.

        Note:
            According to Bedrock Wiki, exact behavior is unknown and this may crash Minecraft with wrong parameters.
        """
        self._component["on_hit"]["hurt_owner"] = {}

        if owner_damage != 0:
            self._component["on_hit"]["hurt_owner"]["owner_damage"] = owner_damage
        if knockback:
            self._component["on_hit"]["hurt_owner"]["knockback"] = knockback
        if ignite:
            self._component["on_hit"]["hurt_owner"]["ignite"] = ignite

        return self

    def impact_damage(
        self,
        filter: str = None,
        catch_fire: bool = False,
        channeling: bool = True,
        damage: int = 1,
        destroy_on_hit: bool = False,
        destroy_on_hit_requires_damage: bool = True,
        knockback: bool = True,
        max_critical_damage: int = 5,
        min_critical_damage: int = 0,
        power_multiplier: float = 2,
        semi_random_diff_damage: bool = False,
        set_last_hurt_requires_damage: bool = False,
        apply_knockback_to_blocking_targets: bool = False,
    ):
        """Deal damage on impact.

        Args:
            filter: Entity identifier to affect. Much more primitive than filters used elsewhere, as it cannot "test" for anything other than an identifier. Default is None.
            catch_fire: Whether targets will be engulfed in flames. Default is False.
            channeling: Whether lightning can be channeled through the weapon. Default is True.
            damage: Damage dealt to entity on hit. Default is 1.
            destroy_on_hit: Whether projectile is removed on hit. Default is False.
            destroy_on_hit_requires_damage: If true, hit must cause damage to destroy the projectile. Default is True.
            knockback: Whether the projectile will knock back the entity it hits. Default is True.
            max_critical_damage: Maximum critical damage. Default is 5.
            min_critical_damage: Minimum critical damage. Default is 0.
            power_multiplier: How much the base damage is multiplied. Default is 2.
            semi_random_diff_damage: If true, damage will be randomized based on damage and speed. Default is False.
            set_last_hurt_requires_damage: If true, hit must cause damage to update the last hurt property. Default is False.
            apply_knockback_to_blocking_targets: If true, knockback will be applied to any blocking targets. Default is False.

        Returns:
            Self for method chaining.
        """
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
            self._component["on_hit"]["impact_damage"][
                "destroy_on_hit"
            ] = destroy_on_hit
        if not destroy_on_hit_requires_damage:
            self._component["on_hit"]["impact_damage"][
                "destroy_on_hit_requires_damage"
            ] = destroy_on_hit_requires_damage
        if not knockback:
            self._component["on_hit"]["impact_damage"]["knockback"] = knockback
        if max_critical_damage != 5:
            self._component["on_hit"]["impact_damage"][
                "max_critical_damage"
            ] = max_critical_damage
        if min_critical_damage != 0:
            self._component["on_hit"]["impact_damage"][
                "min_critical_damage"
            ] = min_critical_damage
        if power_multiplier != 2:
            self._component["on_hit"]["impact_damage"][
                "power_multiplier"
            ] = power_multiplier
        if semi_random_diff_damage:
            self._component["on_hit"]["impact_damage"][
                "semi_random_diff_damage"
            ] = semi_random_diff_damage
        if set_last_hurt_requires_damage:
            self._component["on_hit"]["impact_damage"][
                "set_last_hurt_requires_damage"
            ] = set_last_hurt_requires_damage
        if apply_knockback_to_blocking_targets:
            self._component["on_hit"]["impact_damage"][
                "apply_knockback_to_blocking_targets"
            ] = apply_knockback_to_blocking_targets

        return self

    def mob_effect(
        self,
        effect: MinecraftEffects,
        amplifier: int = 1,
        ambient: bool = False,
        visible: bool = False,
        duration: int = 1,
        durationeasy: int = 0,
        durationhard: int = 800,
        durationnormal: int = 200,
    ):
        """Apply a mob effect to the target on hit.

        Args:
            effect: The effect to apply.
            amplifier: Effect amplifier. Default is 1.
            ambient: Whether the effect is ambient. Default is False.
            visible: Whether the effect is visible. Default is False.
            duration: Duration of the effect. Default is 1.
            durationeasy: Duration of the effect on easy difficulty. Default is 0.
            durationhard: Duration of the effect on hard difficulty. Default is 800.
            durationnormal: Duration of the effect on normal difficulty. Default is 200.

        Returns:
            Self for method chaining.
        """
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
        if durationhard != 800:
            self._component["on_hit"]["mob_effect"]["durationhard"] = durationhard
        if durationnormal != 200:
            self._component["on_hit"]["mob_effect"]["durationnormal"] = durationnormal

        return self

    def on_hit(
        self,
        catch_fire: bool = False,
        douse_fire: bool = False,
        ignite: bool = False,
        teleport_owner: bool = False,
    ):
        """Configure basic on_hit behaviors for the projectile.

        Args:
            catch_fire: Determines if the struck object is set on fire. Default is False.
            douse_fire: If the target is on fire, then douse the fire. Default is False.
            ignite: Determines if a fire may be started on a flammable target. Default is False.
            teleport_owner: Determines if the owner is transported on hit. Default is False.

        Returns:
            Self for method chaining.
        """
        if catch_fire:
            self._component["on_hit"]["catch_fire"] = catch_fire
        if douse_fire:
            self._component["on_hit"]["douse_fire"] = douse_fire
        if ignite:
            self._component["on_hit"]["ignite"] = ignite
        if teleport_owner:
            self._component["on_hit"]["teleport_owner"] = teleport_owner
        return self

    def particle_on_hit(
        self,
        particle_type: str,
        on_other_hit: bool = False,
        on_entity_hit: bool = False,
        num_particles: int = 0,
    ):
        """Spawn particles on hit.

        Args:
            particle_type: Vanilla particle type to use.
            on_other_hit: Whether it should spawn particles on non-entity hit. Default is False.
            on_entity_hit: Whether it should spawn particles on entity hit. Default is False.
            num_particles: Number of particles to spawn. Default is 0.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["particle_on_hit"] = {"particle_type": particle_type}

        if on_other_hit:
            self._component["on_hit"]["particle_on_hit"]["on_other_hit"] = on_other_hit
        if on_entity_hit:
            self._component["on_hit"]["particle_on_hit"][
                "on_entity_hit"
            ] = on_entity_hit
        if num_particles != 0:
            self._component["on_hit"]["particle_on_hit"][
                "num_particles"
            ] = num_particles
        return self

    @property
    def remove_on_hit(self):
        """Remove the projectile when it hits something.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["remove_on_hit"] = {"remove": True}
        return self

    def spawn_aoe_cloud(
        self,
        affect_owner: bool = True,
        color: tuple[int, int, int] = (1, 1, 1),
        duration: int = 0,
        particle: str = "",
        potion: int = -1,
        radius: float = 0.0,
        radius_on_use: float = -1.0,
        reapplication_delay: int = 0,
    ):
        """Spawn an area of effect cloud of potion effect on hit.

        Args:
            affect_owner: Whether potion effect affects the shooter. Does not appear to apply to the player. Default is True.
            color: RGB color of the particles. Default is (1, 1, 1).
            duration: Duration of the cloud in seconds. Default is 0.
            particle: Vanilla particle emitter of the cloud. Only accepts Vanilla Particles. 'dragonbreath' enables the usage of Bottles to obtain Dragon's Breath. Default is "".
            potion: Lingering Potion ID. Default is -1.
            radius: Radius of the cloud. Default is 0.0.
            radius_on_use: Radius change on use. Default is -1.0.
            reapplication_delay: Delay in ticks between application of the potion effect. Default is 0.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["spawn_aoe_cloud"] = {}

        if not affect_owner:
            self._component["on_hit"]["spawn_aoe_cloud"]["affect_owner"] = affect_owner
        if color != (1, 1, 1):
            self._component["on_hit"]["spawn_aoe_cloud"]["color"] = color
        if duration != 0:
            self._component["on_hit"]["spawn_aoe_cloud"]["duration"] = duration
        if particle != "":
            self._component["on_hit"]["spawn_aoe_cloud"]["particle"] = particle
        if potion != -1:
            self._component["on_hit"]["spawn_aoe_cloud"]["potion"] = potion
        if radius != 0.0:
            self._component["on_hit"]["spawn_aoe_cloud"]["radius"] = radius
        if radius_on_use != -1.0:
            self._component["on_hit"]["spawn_aoe_cloud"][
                "radius_on_use"
            ] = radius_on_use
        if reapplication_delay != 0:
            self._component["on_hit"]["spawn_aoe_cloud"][
                "reapplication_delay"
            ] = reapplication_delay

        return self

    def spawn_chance(
        self,
        spawn_definition: str,
        spawn_baby: bool = False,
        first_spawn_count: int = 0,
        first_spawn_percent_chance: int = 0,
        second_spawn_percent_chance: int = 32,
        second_spawn_count: int = 0,
    ):
        """Spawn an entity on hit with specified chances.

        Args:
            spawn_definition: ID of the entity to spawn.
            spawn_baby: Whether the spawned entity should be a baby. Default is False.
            first_spawn_count: Number of entities to spawn in first spawn. Default is 0.
            first_spawn_percent_chance: Percentage chance for first spawn. Default is 0.
            second_spawn_percent_chance: Percentage chance for second spawn. Default is 32.
            second_spawn_count: Number of entities to spawn in second spawn. Default is 0.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["spawn_chance"] = {
            "spawn_definition": spawn_definition
        }

        if spawn_baby:
            self._component["on_hit"]["spawn_chance"]["spawn_baby"] = spawn_baby
        if first_spawn_count:
            self._component["on_hit"]["spawn_chance"][
                "first_spawn_count"
            ] = first_spawn_count
        if first_spawn_percent_chance:
            self._component["on_hit"]["spawn_chance"][
                "first_spawn_percent_chance"
            ] = first_spawn_percent_chance
        if second_spawn_percent_chance:
            self._component["on_hit"]["spawn_chance"][
                "second_spawn_percent_chance"
            ] = second_spawn_percent_chance
        if second_spawn_count:
            self._component["on_hit"]["spawn_chance"][
                "second_spawn_count"
            ] = second_spawn_count

        return self

    def stick_in_ground(self, shake_time: float):
        """Configure projectile to stick into the ground on hit.

        Args:
            shake_time: Time in seconds the projectile shakes when stuck in ground.

        Returns:
            Self for method chaining.
        """
        self._component["on_hit"]["stick_in_ground"] = {"shake_time": shake_time}
        return self

    @property
    def thrown_potion_effect(self):
        """Enable thrown potion effect.

        Returns:
            Self for method chaining.

        Note:
            According to Bedrock Wiki, exact behavior is unknown and this may crash Minecraft as it's probably only valid for thrown potions.
        """
        self._component["on_hit"]["thrown_potion_effect"] = {}
        return self


class EntityExplode(Component):
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
        """Defines how the entity explodes.

        Parameters:
            breaks_blocks (bool, optional): If true, the explosion will destroy blocks in the explosion radius. Defaults to True.
            causes_fire (bool, optional): If true, blocks in the explosion radius will be set on fire. Defaults to False.
            destroy_affected_by_griefing (bool, optional): If true, whether the explosion breaks blocks is affected by the mob griefing game rule. Defaults to False.
            fire_affected_by_griefing (bool, optional): If true, whether the explosion causes fire is affected by the mob griefing game rule. Defaults to False.
            fuse_length (tuple[float, float], optional): The range for the random amount of time the fuse will be lit before exploding, a negative value means the explosion will be immediate. Defaults to [0.0, 0.0].
            fuse_lit (bool, optional): If true, the fuse is already lit when this component is added to the entity. Defaults to False.
            max_resistance (int, optional): A blocks explosion resistance will be capped at this value when an explosion occurs. Defaults to 3.40282e+38.
            power (int, optional): The radius of the explosion in blocks and the amount of damage the explosion deals. Defaults to 3.
            damage_scaling (float, optional): A scale factor applied to the explosion's damage to entities. A value of 0 prevents the explosion from dealing any damage. Negative values cause the explosion to heal entities instead. Defaults to 1.0.
            toggles_blocks (bool, optional): If true, the explosion will toggle blocks in the explosion radius. This item requires a format version of at least 1.21.40. Defaults to False.
            knockback_scaling (float, optional): A scale factor applied to the knockback force caused by the explosion. This item requires a format version of at least 1.21.40. Defaults to 1.0.
            particle_effect (ExplosionParticleEffect, optional): The name of the particle effect to use. The accepted strings are 'explosion', 'wind_burst', or 'breeze_wind_burst'. This item requires a format version of at least 1.21.40. Defaults to ExplosionParticleEffect.Explosion.
            sound_effect (str, optional): The name of the sound effect played when the explosion triggers. This item requires a format version of at least 1.21.40. Defaults to 'explode'.
            negates_fall_damage (bool, optional): Defines whether the explosion should apply fall damage negation to Players above the point of collision. This item requires a format version of at least 1.21.40. Defaults to False.
            allow_underwater (bool, optional): If true, the explosion will affect blocks and entities under water. This item requires a format version of at least 1.21.40. Defaults to True.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_explode
        """
        super().__init__("explode")

        if not breaks_blocks:
            self._add_field("breaks_blocks", breaks_blocks)
        if causes_fire:
            self._add_field("causes_fire", causes_fire)
        if destroy_affected_by_griefing:
            self._add_field(
                "destroy_affected_by_griefing", destroy_affected_by_griefing
            )
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


class EntityMobEffect(Component):
    _identifier = "minecraft:mob_effect"

    def __init__(
        self,
        mob_effect: MinecraftEffects,
        entity_filter: Filter,
        cooldown_time: int = 0,
        effect_range: float = 0.2,
        effect_time: int = 10,
        ambient: bool = False,
    ) -> None:
        """A component that applies a mob effect to entities that get within range.

        Parameters:
            mob_effect (MinecraftEffects): The mob effect that is applied to entities that enter this entities effect range.
            entity_filter (Filter): The set of entities that are valid to apply the mob effect to.
            cooldown_time (int, optional): Time in seconds to wait between each application of the effect. Defaults to 0.
            effect_range (float, optional): How close a hostile entity must be to have the mob effect applied. Defaults to 0.2.
            effect_time (int, optional): How long the applied mob effect lasts in seconds. Can also be set to "infinite". Defaults to 10.
            ambient (bool, optional): If the effect is considered an ambient effect (like the ones applied by Beacons or Conduits). Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mob_effect
        """
        super().__init__("mob_effect")
        self._add_field("mob_effect", mob_effect.value)
        self._add_field("entity_filter", entity_filter)

        if cooldown_time != 0:
            self._add_field("cooldown_time", cooldown_time)
        if effect_range != 0.2:
            self._add_field("effect_range", effect_range)
        if effect_time != 10:
            self._add_field("effect_time", effect_time)
        if ambient:
            self._add_field("ambient", ambient)


class EntitySpawnEntity(Component):
    _identifier = "minecraft:spawn_entity"

    def __init__(self) -> None:
        """Adds a timer after which this entity will spawn another entity or item (similar to vanilla's chicken's egg-laying behavior).

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_spawn_entity
        """
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
                "spawn_event": (
                    spawn_event if spawn_event != "minecraft:entity_born" else {}
                ),
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


class EntityLoot(Component):
    _identifier = "minecraft:loot"

    def __init__(self, loot_table: LootTable | str) -> None:
        """Specifies the loot table that determines what items this entity drops upon death. The table path is relative to the behavior pack's root folder.

        Parameters:
            loot_table (LootTable | str): Path to the loot table JSON file, relative to the behavior pack's root (e.g., 'loot_tables/entities/zombie.json').

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_loot
        """
        super().__init__("loot")
        self._add_field(
            "table",
            loot_table.table_path if isinstance(loot_table, LootTable) else loot_table,
        )


class EntityShooter(Component):
    _identifier = "minecraft:shooter"

    def __init__(
        self,
        identifier: Identifier,
        magic: bool = False,
        power: float = 0.0,
        aux_value: int = -1,
        sound: str = None,
    ) -> None:
        """Defines the entity's ranged attack behavior. The "minecraft:behavior.ranged_attack" goal uses this component to determine which projectiles to shoot.

        Parameters:
            identifier (Identifier): Actor definition to use as the default projectile for the ranged attack. The actor definition must have the projectile component to be able to be shot as a projectile.
            magic (bool, optional): Sets whether the projectiles being used are flagged as magic. If set, the ranged attack goal will not be used at the same time as other magic goals, such as minecraft:behavior.drink_potion. Defaults to False.
            power (float, optional): Velocity in which the projectiles will be shot at. A power of 0 will be overwritten by the default projectile throw power. Defaults to 0.0.
            aux_value (int, optional): ID of the Potion effect for the default projectile to be applied on hit. Defaults to -1.
            sound (str, optional): Sound that is played when the shooter shoots a projectile. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_shooter
        """
        super().__init__("shooter")
        self._add_field("def", identifier)
        if magic:
            self._add_field("magic", magic)
        if power != 0:
            self._add_field("power", power)
        if aux_value != -1:
            self._add_field("aux_value", aux_value)
        if not sound is None:
            self._add_field("sound", sound)


class EntityInsideBlockNotifier(Component):
    _identifier = "minecraft:inside_block_notifier"

    def __init__(self) -> None:
        """Verifies whether the entity is inside any of the listed blocks.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inside_block_notifier
        """
        super().__init__("inside_block_notifier")
        self._add_field("block_list", [])

    def blocks(
        self,
        block_name: MinecraftBlockDescriptor | Identifier,
        entered_block_event: str = None,
        exited_block_event: str = None,
    ):
        if not isinstance(block_name, (MinecraftBlockDescriptor, str)):
            raise TypeError(
                f"block_name must be a MinecraftBlockDescriptor or Identifier instance. Component {self._identifier}[{block_name}]."
            )

        self._component["block_list"].append(
            {
                "block": {
                    "name": (str(block_name)),
                    "states": (
                        block_name.states
                        if isinstance(block_name, MinecraftBlockDescriptor)
                        and block_name.states != ""
                        else {}
                    ),
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


class EntityTransformation(Component):
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
        """Defines an entity's transformation from the current definition into another.

        Parameters:
            into (Identifier): Entity Definition that this entity will transform into.
            transform_event (str, optional): Description. Defaults to None.
            drop_equipment (bool, optional): Cause the entity to drop all equipment upon transformation. Defaults to False.
            drop_inventory (bool, optional): Cause the entity to drop all items in inventory upon transformation. Defaults to False.
            keep_level (bool, optional): If this entity has trades and has leveled up, it should maintain that level after transformation. Defaults to False.
            keep_owner (bool, optional): If this entity is owned by another entity, it should remain owned after transformation. Defaults to False.
            preserve_equipment (bool, optional): Cause the entity to keep equipment after going through transformation. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transformation
        """
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
        block_type: list[MinecraftBlockDescriptor | Identifier] = [],
    ):
        if block_assist_chance != 0.0:
            self._component["delay"]["block_assist_chance"] = block_assist_chance
        if block_chance != 0:
            self._component["delay"]["block_chance"] = block_chance
        if block_max != 0:
            self._component["delay"]["block_max"] = block_max
        if block_radius != 0:
            self._component["delay"]["block_radius"] = block_radius
        if value != 0:
            self._component["delay"]["value"] = value
        if len(block_type) > 0:
            if not all(
                isinstance(block, (MinecraftBlockDescriptor, Identifier))
                for block in block_type
            ):
                raise TypeError(
                    f"block_type must be a list of MinecraftBlockDescriptor or Identifier instances. Component [{self._identifier}]."
                )

            self._component["delay"]["block_type"] = [
                str(block) for block in block_type
            ]

        return self


class EntityNPC(Component):
    _identifier = "minecraft:npc"

    def __init__(self, skin_list: list[int]) -> None:
        """Allows an entity to be an NPC.

        Parameters:
            skin_list (list[int]): Description.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_npc
        """
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


class EntityEquipment(Component):
    _identifier = "minecraft:equipment"

    def __init__(self, table: LootTable | str | None) -> None:
        """Sets the Equipment table to use for this Entity.

        Parameters:
            table (LootTable | str): The file path to the equipment table, relative to the behavior pack's root.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equipment
        """
        super().__init__("equipment")
        if table:
            self._add_field(
                "table",
                table.table_path if isinstance(table, LootTable) else table,
            )

    def slot_drop_chance(self, slot: str, drop_chance: float = None):
        """Adds a chance to drop an equipped item from a specific slot.

        Parameters:
            slot (str): The equipment slot name.
            drop_chance (float, optional): The chance to drop the equipped item (0.0 to 1.0). If None, it just adds the slot string.

        Returns:
            EntityEquipment: Returns the EntityEquipment component to allow for method chaining.
        """
        if drop_chance is None:
            self._get_field("slot_drop_chance", []).append(slot)
        else:
            self._get_field("slot_drop_chance", []).append(
                {"slot": slot, "drop_chance": clamp(drop_chance, 0, 1)}
            )
        return self


class EntityEquipItem(Component):
    _identifier = "minecraft:equip_item"

    def __init__(
        self,
        can_wear_armor: bool = False,
        excluded_items: list[MinecraftItemDescriptor] = [],
    ) -> None:
        """The entity puts on the desired equipment.

        Parameters:
            can_wear_armor (bool, optional): If true, the entity can pick up and wear armor items from the ground. Defaults to False.
            excluded_items (list[MinecraftItemDescriptor], optional): List of items that the entity should not equip. Defaults to [].

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equip_item
        """
        super().__init__("equip_item")
        if can_wear_armor:
            self._add_field("can_wear_armor", can_wear_armor)
        if excluded_items:
            if not all(
                isinstance(item, MinecraftItemDescriptor) for item in excluded_items
            ):
                raise TypeError(
                    f"excluded_items must be a list of MinecraftItemDescriptor instances. Component [{self._identifier}]."
                )
            self._add_field("excluded_items", excluded_items)


class EntityFireImmune(Component):
    _identifier = "minecraft:fire_immune"

    def __init__(self) -> None:
        """Sets that this entity doesn't take damage from fire.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_fire_immune
        """
        super().__init__("fire_immune")


class EntitySensor(Component):
    _identifier = "minecraft:entity_sensor"

    def __init__(
        self, relative_range: bool = True, find_players_only: bool = False
    ) -> None:
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

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_sensor
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
            sensor["range"] = (
                range if isinstance(range, (tuple, list)) else (range, range)
            )
        if cooldown != -1:
            sensor["cooldown"] = cooldown
        if y_offset != 0.0:
            sensor["y_offset"] = y_offset
        self._component["subsensors"].append(sensor)

        return self


class EntityAmbientSoundInterval(Component):
    _identifier = "minecraft:ambient_sound_interval"

    def __init__(
        self, event_name: str, sound_delay: tuple[float, float] = (8, 16)
    ) -> None:
        """Delay for an entity playing its sound.

        Parameters:
            event_name (str): Level sound event to be played as the ambient sound.
            sound_delay (tuple[float, float], optional): Minimum and maximum delay in seconds between playing the ambient sound. Defaults to (8, 16).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ambient_sound_interval
        """
        super().__init__("ambient_sound_interval")

        if sound_delay != (8, 16):
            if not isinstance(sound_delay, (tuple, list)):
                raise TypeError(
                    f"sound_delay must be a tuple or list of two floats. Component [{self._identifier}]."
                )
            if len(sound_delay) != 2:
                raise ValueError(
                    f"sound_delay must have exactly two elements. Component [{self._identifier}]."
                )
            if not all(isinstance(delay, (int, float)) for delay in sound_delay):
                raise TypeError(
                    f"Both elements of sound_delay must be numbers. Component [{self._identifier}]."
                )
            if sound_delay[0] < 0 or sound_delay[1] < 0:
                raise ValueError(
                    f"Both elements of sound_delay must be non-negative. Component [{self._identifier}]."
                )
            if sound_delay[0] > sound_delay[1]:
                raise ValueError(
                    f"The first element of sound_delay must be less than or equal to the second element. Component [{self._identifier}]."
                )
            self._add_field("range", sound_delay[0])
            self._add_field("value", sound_delay[1])
            self._add_field("event_names", [])

        self._add_field("event_name", event_name)

    def add_event(self, event_name: str, condition: Molang):
        """Adds an additional sound event to be played when the ambient sound plays, with a Molang condition for it to play.

        Parameters:
            event_name (str): Level sound event to be played as the additional sound.
            condition (Molang): Molang condition that must be satisfied for the additional sound to play when the ambient sound plays.
        """
        self._component["event_names"].append(
            {"event_name": event_name, "condition": condition}
        )
        return self


class EntityUnderwaterMovement(Component):
    _identifier = "minecraft:underwater_movement"

    def __init__(self, value: int) -> None:
        """Defines the speed with which an entity can move through water.

        Parameters:
            value (int): Movement speed of the entity under water.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_underwater_movement
        """
        super().__init__("underwater_movement")
        self._add_field("value", value)


class EntityMovementMeters(Component):
    _identifier = "minecraft:movement"

    def __init__(self, value: float, max: float = None) -> None:
        """Defines the base movement speed of an entity. Typical values: creeper (0.2), cow (0.25), zombie baby (0.35).

        Parameters:
            value (float): The base movement speed value. Higher values result in faster movement. Can be a single number or a range object with range_min and range_max properties.
            max (float, optional): Maximum movement speed this entity can have. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement
        """
        super().__init__("movement")
        self._add_field("value", round(0.152 * math.sqrt(value), 2))
        if not max is None:
            self._add_field("max", round(0.152 * math.sqrt(max), 2))


class EntityInputGroundControlled(Component):
    _identifier = "minecraft:input_ground_controlled"

    def __init__(self) -> None:
        """When configured as a rideable entity, the entity will be controlled using WASD controls. Beginning with 1.19.50 the default auto step height for rideable entities is half a block. Consider adding the "minecraft:variable_max_auto_step" component to increase it.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_input_ground_controlled
        """
        super().__init__("input_ground_controlled")


class EntityWaterMovement(Component):
    _identifier = "minecraft:water_movement"

    def __init__(self, drag_factor: float = 0.8) -> None:
        """Customizes how the entity moves through water by adjusting drag coefficient. Lower values let entities glide through water easily like fish, while higher values create resistance for entities that struggle in water. Essential for aquatic mobs, boats, and any entity needing custom underwater physics.

        Parameters:
            drag_factor (float, optional): Drag factor to determine movement speed when in water. Defaults to 0.8.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_water_movement
        """
        super().__init__("water_movement")
        if drag_factor != 0.8:
            self._add_field("drag_factor", drag_factor)


class EntityAngry(Component):
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
        """Defines an entity's 'angry' state using a timer.

        Parameters:
            angry_sound (str, optional): The sound event to play when the mob is angry. Defaults to None.
            broadcast_anger (bool, optional): If set, other entities of the same entity definition within the broadcastRange will also become angry. Defaults to False.
            broadcast_anger_on_attack (bool, optional): If set, other entities of the same entity definition within the broadcastRange will also become angry whenever this mob attacks. Defaults to False.
            broadcast_anger_on_being_attacked (bool, optional): If true, other entities of the same entity definition within the broadcastRange will also become angry whenever this mob is attacked. Defaults to False.
            broadcast_filters (Filter, optional): Conditions that make this entry in the list valid. Defaults to None.
            broadcast_range (int, optional): Distance in blocks within which other entities of the same entity type will become angry. Defaults to 20.
            broadcast_targets (list[str], optional): A list of entity families to broadcast anger to. Defaults to [].
            duration (Seconds, optional): The amount of time in seconds that the entity will be angry. Defaults to 25.
            duration_delta (Seconds, optional): Variance in seconds added to the duration [-delta, delta]. Defaults to 0.
            filters (Filter, optional): Filter out mob types that it should not attack while angry (other Piglins). Defaults to None.
            sound_interval (list[Seconds], optional): The range of time in seconds to randomly wait before playing the sound again. Defaults to [0, 0].

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_angry
        """
        super().__init__("angry")
        if not angry_sound is None:
            self._add_field("angry_sound", angry_sound)
        if broadcast_anger:
            self._add_field("broadcast_anger", broadcast_anger)
        if broadcast_anger_on_attack:
            self._add_field("broadcast_anger_on_attack", broadcast_anger_on_attack)
        if broadcast_anger_on_being_attacked:
            self._add_field(
                "broadcast_anger_on_being_attacked", broadcast_anger_on_being_attacked
            )
        if not broadcast_filters is None:
            self._add_field("broadcast_filters", broadcast_filters)
        if broadcast_range != 10:
            self._add_field("broadcast_range", broadcast_range)
        if broadcast_targets != []:
            self._add_field("broadcast_targets", broadcast_targets)
        if duration != 25:
            self._add_field("duration", duration)
        if duration_delta != 0:
            self._add_field("duration_delta", duration_delta)
        if not filters is None:
            self._add_field("filters", filters)
        if sound_interval != [0, 0]:
            self._add_field("sound_interval", sound_interval)

    def calm_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("calm_event", {"event": event, "target": target.value})
        return self


class EntityFlyingSpeed(Component):
    _identifier = "minecraft:flying_speed"

    def __init__(self, value: int) -> None:
        """Speed in Blocks that this entity flies at.

        Parameters:
            value (int): Flying speed in blocks per tick.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flying_speed
        """
        super().__init__("flying_speed")
        self._add_field("value", value)


class EntityInteract(Component):
    _identifier = "minecraft:interact"

    def __init__(self) -> None:
        """Defines interactions with this entity.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact
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
        swing: bool = True,
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

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact?view=minecraft-bedrock-stable#parameter
        """

        interaction = {
            "on_interact": {
                "filters": filter if not filter is None else {},
                "event": event,
            }
        }
        if not add_items is None:
            interaction["add_items"] = {"table": add_items}
        if cooldown != 0.0:
            interaction["cooldown"] = cooldown
        if cooldown_after_being_attacked != 0.0:
            interaction["cooldown_after_being_attacked"] = cooldown_after_being_attacked
        if drop_item_slot != -1:
            interaction["drop_item_slot"] = drop_item_slot
        if equip_item_slot != -1:
            interaction["equip_item_slot"] = equip_item_slot
        if health_amount != 0:
            interaction["health_amount"] = health_amount
        if hurt_item != 0:
            interaction["hurt_item"] = hurt_item
        if not interact_text is None:
            interaction["interact_text"] = interact_text
        if not play_sounds is None:
            interaction["play_sounds"] = play_sounds
        if not spawn_entities is None:
            interaction["spawn_entities"] = spawn_entities
        if not spawn_items is None:
            interaction["spawn_items"] = {"table": spawn_items}
        if not swing:
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

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_interact?view=minecraft-bedrock-stable#particle_on_start
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


class EntityAngerLevel(Component):
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
            angry_boost (int, optional): Anger boost applied to angry threshold when mob gets angry Value must be >= 0. Defaults to 20.
            angry_threshold (int, optional): Threshold that define when the mob is considered angry at a nuisance Value must be >= 0. Defaults to 80.
            default_annoyingness (int, optional): The default amount of annoyingness for any given nuisance. Specifies how much to raise anger level on each provocation. Defaults to 0.
            default_projectile_annoyingness (int, optional): The default amount of annoyingness for any given nuisance. Specifies how much to raise anger level on each provocation. Defaults to 0.
            max_anger (int, optional): The maximum anger level that can be reached. Applies to any nuisance Value must be >= 0. Defaults to 100.
            nuisance_filter (Filter, optional): Filter that is applied to determine if a mob can be a nuisance. Defaults to None.
            on_increase_sounds (list[dict[str, str]], optional): Sounds to play when the entity is getting provoked. Evaluated in order. First matching condition wins. Defaults to [].
            remove_targets_below_angry_threshold (bool, optional): Defines if the mob should remove target if it falls below 'angry' threshold. Defaults to True.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_anger_level
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
            self._add_field(
                "default_projectile_annoyingness", default_projectile_annoyingness
            )
        if max_anger != 100:
            self._add_field("max_anger", max_anger)
        if not nuisance_filter is None:
            self._add_field("nuisance_filter", nuisance_filter)
        if on_increase_sounds != []:
            self._add_field("on_increase_sounds", on_increase_sounds)
        if not remove_targets_below_angry_threshold:
            self._add_field(
                "remove_targets_below_angry_threshold",
                remove_targets_below_angry_threshold,
            )


class EntityCanJoinRaid(Component):
    _identifier = "minecraft:can_join_raid"

    def __init__(self) -> None:
        """Specifies if an entity can join a raid.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_can_join_raid
        """
        super().__init__("can_join_raid")


class EntityTameable(Component):
    _identifier = "minecraft:tameable"

    def __init__(
        self,
        probability: float = 1.0,
    ) -> None:
        """This entity can be tamed.

        Parameters:
            probability (float, optional): The chance of taming the entity with each item use between 0.0 and 1.0, where 1.0 is 100%. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tameable
        """
        super().__init__("tameable")

        if probability != 1.0:
            self._add_field("probability", probability)

        self._add_field("tame_items", [])

    def add_tame_item(
        self,
        item: MinecraftItemDescriptor | Identifier,
        result_item: MinecraftItemDescriptor | Identifier = None,
    ):
        """Adds an item to the list of items that can be used to tame the entity.

        Parameters:
            item (str): The item to add to the list of items that can be used to tame the entity.
            result_item (str, optional): The item that the tame item will transform into upon successful taming. Defaults to None.

            Returns:
                Tameable: Returns the Tameable component to allow for method chaining.
        """
        if result_item is None:
            self._component["tame_items"].append(item)
        else:
            self._component["tame_items"].append(
                {
                    "item": item,
                    "result_item": result_item,
                }
            )
        return self

    def tame_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets the event to initiate when the entity becomes tamed.

        Parameters:
            event (str): Event to initiate when the entity becomes tamed.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

            Returns:
                Tameable: Returns the Tameable component to allow for method chaining.
        """
        self._add_field("tame_event", {"event": event, "target": target})
        return self


class EntityAgeable(Component):
    _identifier = "minecraft:ageable"

    def __init__(
        self,
        duration: Seconds = 1200.0,
        interact_filters: Filter = None,
        result_item: str = None,
    ) -> None:
        """Adds a timer for the entity to grow up. It can be accelerated by giving the entity the items it likes as defined by feed_items.

        Parameters:
            duration (Seconds, optional): Length of time before an entity grows up (-1 to always stay a baby). Defaults to 1200.0.
            interact_filters (Filter, optional): List of conditions to meet so that the entity can be fed. Defaults to None.
            result_item (str, optional): The item identifier. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ageable
        """
        super().__init__("ageable")
        self._component["feed_items"] = []

        if duration != 1200.0:
            self._add_field("duration", duration)
        if not interact_filters is None:
            self._add_field("interact_filters", interact_filters)
        if not result_item is None:
            self._add_field("result_item", result_item)

    def drop_item(self, *items: str):
        """Adds an item to the list of items the entity drops when it grows up.

        Parameters:
            item (str): The item to add to the list of items the entity drops when it grows up.

            Returns:
                Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._add_field("drop_items", items)
        return self

    def feed_items(self, items: list[str]):
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
        self._component["feed_items"].append(
            {"item": str(item), "growth": clamp(growth, 0, 1)}
        )
        return self

    def grow_up(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets the event to initiate when the entity grows up.

        Parameters:
            event (str): Event to initiate when the entity grows up.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

            Returns:
                Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._add_field("grow_up", {"event": event, "target": target})
        return self

    def pause_growth_items(self, items: list[MinecraftItemDescriptor | Identifier]):
        """Pauses the growth of the entity when given specific items.

        Parameters:
            items (list[MinecraftItemDescriptor | Identifier]): The items that will pause the entity's growth.

            Returns:
                Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._add_field("pause_growth_items", [str(i) for i in items])
        return self

    def reset_growth_items(self, items: list[MinecraftItemDescriptor | Identifier]):
        """Resets the growth of the entity when given specific items.

        Parameters:
            items (list[MinecraftItemDescriptor | Identifier]): The items that will reset the entity's growth.

        Returns:
            Ageable: Returns the Ageable component to allow for method chaining.
        """
        self._add_field("reset_growth_items", [str(i) for i in items])
        return self


class EntityInventory(Component):
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
        """Defines this entity's inventory properties.

        Parameters:
            additional_slots_per_strength (int, optional): Number of slots that this entity can gain per extra strength. Defaults to 0.
            can_be_siphoned_from (bool, optional): If true, the contents of this inventory can be removed by a hopper. Defaults to False.
            container_type (ContainerType, optional): Type of container this entity has. Can be horse, minecart_chest, chest_boat, minecart_hopper, inventory, container or hopper. Defaults to ContainerType.Inventory.
            inventory_size (int, optional): Number of slots the container has. Defaults to 5.
            private (bool, optional): If true, the entity will not drop its inventory on death. Defaults to False.
            restrict_to_owner (bool, optional): If true, the entity's inventory can only be accessed by its owner or itself. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_inventory
        """
        super().__init__("inventory")

        self._add_field("container_type", container_type)
        if additional_slots_per_strength != 0:
            self._add_field(
                "additional_slots_per_strength", additional_slots_per_strength
            )
        if can_be_siphoned_from:
            self._add_field("can_be_siphoned_from", can_be_siphoned_from)
        if inventory_size != 5:
            self._add_field("inventory_size", inventory_size)
        if private:
            self._add_field("private", private)
        if restrict_to_owner:
            self._add_field("restrict_to_owner", restrict_to_owner)


class EntityDashAction(Component):
    _identifier = "minecraft:dash_action"

    def __init__(
        self,
        direction: Literal["entity", "passenger"] = "entity",
        cooldown_time: Seconds = 1.0,
        horizontal_momentum: float = 1.0,
        vertical_momentum: float = 1.0,
        can_dash_underwater: bool = False,
    ) -> None:
        """Ability for a rideable entity to dash.

        Parameters:
            direction (Literal['entity', 'passenger'], optional): Should the momentum be applied in the direction of the 'entity' or 'passenger'. Defaults to 'entity'.
            cooldown_time (Seconds, optional): The dash cooldown in seconds. Default value is 1.000000. Defaults to 1.0.
            horizontal_momentum (float, optional): Horizontal momentum of the dash. Defaults to 1.0.
            vertical_momentum (float, optional): Vertical momentum of the dash. Defaults to 1.0.
            can_dash_underwater (bool, optional): Whether the entity can dash underwater. Default value is false. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash_action
        """
        super().__init__("dash_action")

        if direction != "entity":
            self._add_field("direction", direction)
        if cooldown_time != 1.0:
            self._add_field("cooldown_time", cooldown_time)
        if horizontal_momentum != 1.0:
            self._add_field("horizontal_momentum", horizontal_momentum)
        if vertical_momentum != 1.0:
            self._add_field("vertical_momentum", vertical_momentum)
        if can_dash_underwater:
            self._add_field("can_dash_underwater", can_dash_underwater)


class EntityBreathable(Component):
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
        can_dehydrate: bool = False,
        breathe_blocks: list[MinecraftBlockDescriptor] = [],
        non_breathe_blocks: list[MinecraftBlockDescriptor] = [],
    ) -> None:
        """Defines what blocks this entity can breathe in and gives them the ability to suffocate.

        Parameters:
            breathes_air (bool, optional): If set, this entity can breathe in air. Defaults to True.
            breathes_lava (bool, optional): If set, this entity can breathe in lava. Defaults to True.
            breathes_solids (bool, optional): If set, this entity can breathe in solid blocks. Defaults to False.
            breathes_water (bool, optional): If set, this entity can breathe in water. Defaults to False.
            generates_bubbles (bool, optional): If set, this entity will have visible bubbles while in water. Defaults to True.
            inhale_time (Seconds, optional): Time in seconds to recover breath to maximum. Defaults to 0.0.
            suffocate_time (Seconds, optional): Time in seconds between suffocation damage. Defaults to -20.
            total_supply (Seconds, optional): Time in seconds the entity can hold its breath. Defaults to 15.
            can_dehydrate (bool, optional): Description. Defaults to False.
            breathe_blocks (list[MinecraftBlockDescriptor], optional): List of blocks this entity can breathe in, in addition to the selected items above. Defaults to [].
            non_breathe_blocks (list[MinecraftBlockDescriptor], optional): List of blocks this entity cannot breathe in, in addition to the selected items above. Defaults to [].

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breathable
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
        if breathe_blocks != []:
            self._add_field("breathe_blocks", breathe_blocks)
        if non_breathe_blocks != []:
            self._add_field("non_breathe_blocks", non_breathe_blocks)
        if can_dehydrate:
            self._add_field("can_dehydrate", can_dehydrate)


class EntityVariableMaxAutoStep(Component):
    _identifier = "minecraft:variable_max_auto_step"

    def __init__(
        self,
        base_value: float = 0.5625,
        controlled_value: float = 0.5625,
        jump_prevented_value: float = 0.5625,
    ) -> None:
        """Entities with this component will have a maximum auto step height that is different depending on whether they are on a block that prevents jumping. Incompatible with "runtime_identifier": "minecraft:horse".

        Parameters:
            base_value (float, optional): The maximum auto step height when on any other block. Defaults to 0.5625.
            controlled_value (float, optional): The maximum auto step height when on any other block and controlled by the player. Defaults to 0.5625.
            jump_prevented_value (float, optional): The maximum auto step height when on a block that prevents jumping. Defaults to 0.5625.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_variable_max_auto_step
        """
        super().__init__("variable_max_auto_step")

        if base_value != 0.5625:
            self._add_field("base_value", base_value)
        if controlled_value != 0.5625:
            self._add_field("controlled_value", controlled_value)
        if jump_prevented_value != 0.5625:
            self._add_field("jump_prevented_value", jump_prevented_value)


class EntityBuoyant(Component):
    _identifier = "minecraft:buoyant"

    def __init__(
        self,
        liquid_blocks: list[MinecraftBlockDescriptor],
        apply_gravity: bool = True,
        base_buoyancy: float = 1.0,
        big_wave_probability: float = 0.03,
        big_wave_speed: float = 10.0,
        drag_down_on_buoyancy_removed: float = 0.0,
        movement_type: Literal["waves", "bobbing", "none"] = "waves",
        can_auto_step_from_liquid: bool = False,
    ) -> None:
        """Enables an entity to float on the specified liquid blocks.

        Parameters:
            liquid_blocks (list[MinecraftBlockDescriptor]): List of blocks this entity can float on. Must be a liquid block.
            apply_gravity (bool, optional): Applies gravity each tick. Causes "movement_type" to be more impactful, but also gravity to be applied more intensely outside liquids. Defaults to True.
            base_buoyancy (float, optional): Base buoyancy used to calculate how much will a entity float. Defaults to 1.0.
            big_wave_probability (float, optional): Probability for a big wave hitting the entity. Only used if "movement_type" is "waves". Defaults to 0.03.
            big_wave_speed (float, optional): Multiplier for the speed to make a big wave. Triggered depending on "big_wave_probability". Defaults to 10.0.
            drag_down_on_buoyancy_removed (float, optional): How much an entity will be dragged down when the component is removed. Defaults to 0.0.
            movement_type (Literal["waves", "bobbing", "none"], optional): Type of vertical movement applied to the entity: "waves", simulates wave movement based on the entity speed. "bobbing", simulates waves going through. "none", simulates waves going through. Defaults to "waves".
            can_auto_step_from_liquid (bool, optional): Whether the entity can move out of a liquid block to a neighboring solid block if pushed against it. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_buoyant
        """
        super().__init__("buoyant")

        self._add_field("liquid_blocks", list(map(str, liquid_blocks)))
        if not apply_gravity:
            self._add_field("apply_gravity", apply_gravity)
        if base_buoyancy != 1.0:
            self._add_field("base_buoyancy", clamp(base_buoyancy, 0, 1))
        if drag_down_on_buoyancy_removed != 0.0:
            self._add_field(
                "drag_down_on_buoyancy_removed", drag_down_on_buoyancy_removed
            )
        if movement_type != "waves":
            self._add_field("movement_type", movement_type)

        if movement_type == "waves":
            if big_wave_probability != 0.03:
                self._add_field("big_wave_probability", big_wave_probability)
            if big_wave_speed != 10.0:
                self._add_field("big_wave_speed", big_wave_speed)


class EntityLavaMovement(Component):
    _identifier = "minecraft:lava_movement"

    def __init__(self, value: float) -> None:
        """Allows a custom movement speed across lava blocks.

        Parameters:
            value (float): The speed the mob moves over a lava block.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_lava_movement
        """
        super().__init__("lava_movement")
        self._add_field("value", value)


class EntityExperienceReward(Component):
    _identifier = "minecraft:experience_reward"

    def __init__(
        self,
        on_bred: int | float | Molang = 0,
        on_death: int | float | Molang = 0,
    ) -> None:
        """.

        Parameters:
            on_bred (int | float | Molang, optional): A Molang expression defining the amount of experience rewarded when this entity is successfully bred. Defaults to 0.
            on_death (int | float | Molang, optional): A Molang expression defining the amount of experience rewarded when this entity dies. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_experience_reward
        """
        super().__init__("experience_reward")
        if on_bred != 0:
            self._add_field("on_bred", on_bred)
        if on_death != 0:
            self._add_field("on_death", on_death)


class EntityEquippable(Component):
    _identifier = "minecraft:equippable"

    def __init__(self) -> None:
        """Defines an entity's behavior for having items equipped to it.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_equippable
        """
        super().__init__("equippable")
        self._component["slots"] = []

    def slot(
        self,
        slot: int,
        item: MinecraftItemDescriptor | Identifier,
        accepted_items: list[MinecraftItemDescriptor | Identifier],
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
            "item": str(item),
            "accepted_items": list(map(str, accepted_items)),
        }
        if not interact_text is None:
            t = interact_text.lower().replace(" ", "_")
            slot_data["interact_text"] = f"action.interact.{t}"
            AnvilTranslator().add_localization_entry(
                f"action.interact.{t}", interact_text
            )
        if not on_equip is None:
            slot_data["on_equip"] = {"event": on_equip}
        if not on_unequip is None:
            slot_data["on_unequip"] = {"event": on_unequip}

        self._component["slots"].append(slot_data)
        return self


class EntityColor(Component):
    _identifier = "minecraft:color"

    def __init__(self, value: int) -> None:
        """Defines the entity's main color.

        Parameters:
            value (int): The Palette Color value of the entity.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color
        """
        super().__init__("color")
        self._add_field("value", value)


class EntityColor2(Component):
    _identifier = "minecraft:color2"

    def __init__(self, value: int) -> None:
        """Defines the entity's second texture color.

        Parameters:
            value (int): The second Palette Color value of the entity.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_color2
        """
        super().__init__("color2")
        self._add_field("value", value)


class EntityBurnsInDaylight(Component):
    _identifier = "minecraft:burns_in_daylight"

    def __init__(self, protection_slot: Slots = None) -> None:
        """Specifies that this entity takes fire damage when exposed to direct sunlight. This component is used by undead mobs like zombies, skeletons, and phantoms. The entity will catch fire when in sunlight unless it is wearing armor in the protection slot, standing in water, or in a shaded area.

        Parameters:
            protection_slot (Slots, optional): The equipment slot that provides protection from burning in sunlight. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_burns_in_daylight
        """
        super().__init__("burns_in_daylight")

        if not protection_slot is None:
            if not isinstance(protection_slot, Slots):
                raise TypeError("protection_slot must be an instance of Slots Enum")
            if protection_slot in [
                Slots.Body,
                Slots.Chest,
                Slots.Feet,
                Slots.Head,
                Slots.Legs,
                Slots.Offhand,
            ]:
                raise ValueError(
                    "protection_slot must be one of the armor or offhand slots."
                )

            self._add_field("protection_slot", protection_slot)


class EntityBoss(Component):
    _identifier = "minecraft:boss"

    def __init__(
        self,
        name: str,
        hud_range: int = 55,
        should_darken_sky: bool = False,
    ) -> None:
        """Defines the current state of the boss for updating the boss HUD.

        Parameters:
            name (str): Description.
            hud_range (int, optional): The max distance from the boss at which the boss's health bar is present on the players screen. Defaults to 55.
            should_darken_sky (bool, optional): Whether the sky should darken in the presence of the boss. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boss
        """
        super().__init__("boss")

        self._add_field("name", name)
        if hud_range != 55:
            self._add_field("hud_range", hud_range)
        if should_darken_sky:
            self._add_field("should_darken_sky", should_darken_sky)


class EntitySittable(Component):
    _identifier = "minecraft:sittable"

    def __init__(
        self,
        sit_event: str = None,
        stand_event: str = None,
    ) -> None:
        """Defines the entity's 'sit' state.

        Parameters:
            sit_event (str, optional): Event to run when the entity enters the 'sit' state. Can be an object with event and target properties, or a simple event string. Defaults to None.
            stand_event (str, optional): Event to run when the entity exits the 'sit' state. Can be an object with event and target properties, or a simple event string. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sittable
        """
        super().__init__("sittable")

        if not sit_event is None:
            self._add_field("sit_event", {"event": sit_event})
        if not stand_event is None:
            self._add_field("stand_event", {"event": stand_event})


class EntityFlyingSpeedMeters(Component):
    _identifier = "minecraft:flying_speed"

    def __init__(self, value: float, max: float = None) -> None:
        """Speed in Blocks that this entity flies at.

        Parameters:
            value (float): Flying speed in blocks per tick.
            max (float, optional): Description. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flying_speed
        """
        super().__init__("flying_speed")
        self._add_field("value", round(0.152 * math.sqrt(value), 2))
        if not max is None:
            self._add_field("max", round(0.152 * math.sqrt(max), 2))


class EntityConditionalBandwidthOptimization(Component):
    _identifier = "minecraft:conditional_bandwidth_optimization"

    def __init__(
        self,
        max_dropped_ticks: int = 0,
        max_optimized_distance: int = 0,
        use_motion_prediction_hints: bool = False,
    ) -> None:
        """Defines the Conditional Spatial Update Bandwidth Optimizations of this entity.

        Parameters:
            max_dropped_ticks (int, optional): Determines the maximum ticks spatial update packets can be not sent. Defaults to 0.
            max_optimized_distance (int, optional): The maximum distance considered during bandwidth optimizations. Defaults to 0.
            use_motion_prediction_hints (bool, optional): When true, smaller motion packets will be sent during drop packet intervals. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_conditional_bandwidth_optimization
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
        filters: Filter = None,
        max_dropped_ticks: int = 0,
        max_optimized_distance: int = 0,
        use_motion_prediction_hints: bool = False,
    ):
        a = {
            "conditional_values": [filters] if not filters is None else [],
        }
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


class EntityItemHopper(Component):
    _identifier = "minecraft:item_hopper"

    def __init__(
        self,
    ) -> None:
        """Determines that this entity is an item hopper.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_hopper
        """
        super().__init__("item_hopper")


class EntityBodyRotationBlocked(Component):
    _identifier = "minecraft:body_rotation_blocked"

    def __init__(
        self,
    ) -> None:
        """When set, the entity will no longer visually rotate their body to match their facing direction.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_blocked
        """
        super().__init__("body_rotation_blocked")


class EntityDamageAbsorption(Component):
    _identifier = "minecraft:damage_absorption"

    def __init__(
        self, absorbable_causes: list[DamageCause] = DamageCause.Nothing
    ) -> None:
        """Allows an item to absorb damage that would otherwise be dealt to its wearer. The item must be equipped in an armor slot for this to happen. The absorbed damage reduces the item's durability, with any excess damage being ignored. The item must also have a minecraft:durability component.

        Parameters:
            absorbable_causes (list[DamageCause], optional): Description. Defaults to DamageCause.Nothing.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_absorption
        """
        super().__init__("damage_absorption")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.20")

        if absorbable_causes != DamageCause.Nothing:
            self._set_value("absorbable_causes", absorbable_causes)


class EntityDimensionBound(Component):
    _identifier = "minecraft:dimension_bound"

    def __init__(
        self,
    ) -> None:
        """Prevents the entity from changing dimension through portals.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dimension_bound
        """
        super().__init__("dimension_bound")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.40")


class EntityTransient(Component):
    _identifier = "minecraft:transient"

    def __init__(
        self,
    ) -> None:
        """An entity with this component will NEVER persist, and forever disappear when unloaded.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_transient
        """
        super().__init__("transient")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.40")


class EntityCannotBeAttacked(Component):
    _identifier = "minecraft:cannot_be_attacked"

    def __init__(
        self,
    ) -> None:
        """When set, blocks entities from attacking the owner entity unless they have the "minecraft:ignore_cannot_be_attacked" component.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_cannot_be_attacked
        """
        super().__init__("cannot_be_attacked")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.51")


class EntityIgnoreCannotBeAttacked(Component):
    _identifier = "minecraft:ignore_cannot_be_attacked"

    def __init__(self, filters: Filter = None) -> None:
        """When set, blocks entities from attacking the owner entity unless they have the "minecraft:ignore_cannot_be_attacked" component.

        Parameters:
            filters (Filter, optional): Defines which entities are exceptions and are allowed to be attacked by the owner entity, potentially attacked entity is subject "other". Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ignore_cannot_be_attacked
        """
        super().__init__("ignore_cannot_be_attacked")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.51")

        if not filters is None:
            self._add_field("filters", filters)


class EntityLookedAt(Component):
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
            field_of_view (float, optional): Defines, in degrees, the width of the field of view for entities looking at the owner entity. Defaults to 26.
            filters (Filter, optional): Defines which entities are considered when searching for entities looking at the owner entity. Defaults to None.
            find_players_only (bool, optional): Limits the search to only the nearest Player that meets the specified "filters" rather than all nearby entities. Defaults to False.
            line_of_sight_obstruction_type (LineOfSightObstructionType, optional): Defines the type of block shape used to check for line of sight obstructions. Valid values: "outline", "collision", "collision_for_camera". Defaults to LineOfSightObstructionType.Collision.
            look_at_locations (list[LookAtLocation], optional): A list of locations on the owner entity towards which line of sight checks are performed. At least one location must be unobstructed for the entity to be considered as looked at. Defaults to None.
            looked_at_cooldown (tuple[Seconds, Seconds], optional): Specifies the range for the random number of seconds that must pass before the owner entity can check again for entities looking at it, after detecting an entity looking at it. Defaults to (0, 0).
            looked_at_event (str, optional): Defines the event to trigger when an entity is detected looking at the owner entity. Defaults to None.
            not_looked_at_event (str, optional): Defines the event to trigger when no entity is found looking at the owner entity. Defaults to None.
            scale_fov_by_distance (bool, optional): When true, the field of view narrows as the distance between the owner entity and the entity looking at it increases. Defaults to True.
            search_radius (float, optional): Maximum distance the owner entity will search for entities looking at it. Defaults to 10.
            set_target (LootedAtSetTarget, optional): Defines if and how the owner entity will set entities that are looking at it as its combat targets. Valid values: 'never', 'once_and_stop_scanning', 'once_and_keep_scanning'. Defaults to LootedAtSetTarget.OnceAndStopScanning.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_looked_at
        """
        super().__init__("looked_at")

        if field_of_view != 26:
            self._add_field("field_of_view", field_of_view)
        if filters is not None:
            self._add_field("filters", filters)
        if find_players_only:
            self._add_field("find_players_only", find_players_only)
        if line_of_sight_obstruction_type != LineOfSightObstructionType.Collision:
            self._add_field(
                "line_of_sight_obstruction_type", line_of_sight_obstruction_type
            )
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


class EntityMovementSoundDistanceOffset(Component):
    _identifier = "minecraft:movement_sound_distance_offset"

    def __init__(self, value: float) -> None:
        """Sets the offset used to determine the next step distance for playing a movement sound.

        Parameters:
            value (float): The higher the number, the less often the movement sound will be played.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_movement.sound_distance_offset?view=minecraft-bedrock-stable
        """
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.60")
        super().__init__("movement_sound_distance_offset")
        self._add_field("value", value)


class EntityRendersWhenInvisible(Component):
    _identifier = "minecraft:renders_when_invisible"

    def __init__(self) -> None:
        """When set, the entity will render even when invisible. Appropriate rendering behavior can then be specified in the corresponding "minecraft:client_entity".

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_renders_when_invisible
        """
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.60")
        super().__init__("renders_when_invisible")


class EntityBreedable(Component):
    _identifier = "minecraft:breedable"

    def __init__(
        self,
        allow_sitting: bool = False,
        breed_cooldown: Seconds = 60,
        breed_items: list[str] = None,
        causes_pregnancy: bool = False,
        extra_baby_chance: float = 0,
        love_filters: Filter = None,
        property_inheritance: list[str] = None,
        require_full_health: bool = False,
        require_tame: bool = True,
        result_item: str = None,
    ) -> None:
        """Allows an entity to establish a way to get into the love state used for breeding.

        Parameters:
            allow_sitting (bool, optional): If true, entities can breed while sitting. Defaults to False.
            breed_cooldown (Seconds, optional): Time in seconds before the Entity can breed again. Defaults to 60.
            breed_items (list[str], optional): The list of items that can be used to get the entity into the 'love' state. Can be a single item or an array. Defaults to None.
            causes_pregnancy (bool, optional): If true, the entity will become pregnant instead of spawning a baby. Defaults to False.
            extra_baby_chance (float, optional): Chance that up to 16 babies will spawn. Defaults to 0.
            love_filters (Filter, optional): The filters to run when attempting to fall in love. Defaults to None.
            property_inheritance (list[str], optional): Description. Defaults to None.
            require_full_health (bool, optional): If true, the entity needs to be at full health before it can breed. Defaults to False.
            require_tame (bool, optional): If true, the entities need to be tamed first before they can breed. Defaults to True.
            result_item (str, optional): The entity definition of this entity's babies. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_breedable
        """
        super().__init__("breedable")

        if allow_sitting:
            self._add_field("allow_sitting", allow_sitting)
        if breed_cooldown != 60:
            self._add_field("breed_cooldown", breed_cooldown)
        if breed_items is not None:
            self._add_field("breed_items", breed_items)
        if causes_pregnancy:
            self._add_field("causes_pregnancy", causes_pregnancy)
        if extra_baby_chance != 0:
            self._add_field("extra_baby_chance", extra_baby_chance)
        if love_filters is not None:
            self._add_field("love_filters", love_filters)
        if property_inheritance is not None:
            self._add_field(
                "property_inheritance",
                {
                    (
                        property_name
                        if ":" in property_name
                        else f"{CONFIG.NAMESPACE}:{property_name}"
                    ): {}
                    for property_name in property_inheritance
                },
            )
        if require_full_health:
            self._add_field("require_full_health", require_full_health)
        if require_tame is not True:
            self._add_field("require_tame", require_tame)
        if result_item is not None:
            self._add_field("result_item", result_item)

    def environment_requirements(
        self, block_types: list[str], count: int, radius: float
    ) -> dict:
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

    def breeds_with(self, mate_type: str) -> dict:
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
            {mate_type: {}},
        )
        return self


class EntityOffspring(Component):
    _identifier = "minecraft:offspring"

    def __init__(
        self,
        blend_attributes: bool = True,
        inherit_tamed: bool = True,
        mutation_strategy: BreedingMutationStrategy = BreedingMutationStrategy.None_,
        offspring_pairs: list[
            tuple[
                MinecraftEntityDescriptor | Identifier,
                MinecraftEntityDescriptor | Identifier,
            ]
        ] = None,
        combine_parent_colors: bool = None,
        parent_centric_attribute_blending: list[Component] = None,
        property_inheritance: list[str] = None,
        random_extra_variant_mutation_interval: tuple[int, int] = (0, 0),
        random_variant_mutation_interval: tuple[int, int] = (0, 0),
    ):
        """Defines the way an entity can create a born offspring.

        Parameters:
            blend_attributes (bool, optional): If true, the entities will blend their attributes in the offspring after they breed. Defaults to True.
            inherit_tamed (bool, optional): If true, the babies will be automatically tamed if its parents are. Defaults to True.
            mutation_strategy (BreedingMutationStrategy, optional): Description. Defaults to BreedingMutationStrategy.None_.
            offspring_pairs (list[tuple[MinecraftEntityDescriptor | Identifier, MinecraftEntityDescriptor | Identifier]], optional): The map of entity to offspring definitions that this entity can make offspring with. Defaults to None.
            combine_parent_colors (bool, optional): Description. Defaults to None.
            parent_centric_attribute_blending (list[Component], optional): List of attributes that should benefit from parent centric attribute blending. For example, horses blend their health, movement, and jump_strength in their offspring. Defaults to None.
            property_inheritance (list[str], optional): List of Entity Properties that should be inherited from the parent entities and potentially mutated. Defaults to None.
            random_extra_variant_mutation_interval (tuple[int, int], optional): Range used to determine random extra variant. Defaults to (0, 0).
            random_variant_mutation_interval (tuple[int, int], optional): Range used to determine random variant. Defaults to (0, 0).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_offspring
        """

        super().__init__("offspring")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.26.0")
        if blend_attributes is not True:
            self._add_field("blend_attributes", blend_attributes)
        if inherit_tamed is not True:
            self._add_field("inherit_tamed", inherit_tamed)
        if offspring_pairs is not None:
            self._add_field(
                "offspring_pairs",
                {str(parent): str(offspring) for parent, offspring in offspring_pairs},
            )
        if parent_centric_attribute_blending is not None:
            self._add_field(
                "parent_centric_attribute_blending",
                [c.identifier for c in parent_centric_attribute_blending],
            )
        if property_inheritance is not None:
            self._add_field(
                "property_inheritance",
                [f"{CONFIG.NAMESPACE}:{property}" for property in property_inheritance],
            )
        if random_extra_variant_mutation_interval != (0, 0):
            self._add_field(
                "random_extra_variant_mutation_interval",
                random_extra_variant_mutation_interval,
            )
        if random_variant_mutation_interval != (0, 0):
            self._add_field(
                "random_variant_mutation_interval", random_variant_mutation_interval
            )
        if mutation_strategy != BreedingMutationStrategy.None_:
            self._add_field("mutation_strategy", mutation_strategy.value)
        if combine_parent_colors is not None:
            self._add_field("combine_parent_colors", combine_parent_colors)

    def deny_parents_variant(
        self, chance: float, min_variant: str, max_variant: str
    ) -> dict:
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

    def mutation_factor(
        self, color: float, extra_variant: float, variant: float
    ) -> dict:
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


class EntityIsCollidable(Component):
    _identifier = "minecraft:is_collidable"

    def __init__(self) -> None:
        """Allows other mobs to have vertical and horizontal collisions with this mob. For a collision to occur, both mobs must have a "minecraft:collision_box" component. This component can only be used on mobs and enables collisions exclusively between mobs. Please note that this type of collision is unreliable for moving collidable mobs. It is recommended to use this component only in scenarios where the collidable mob remains stationary. Collidable behavior is closely related to stackable behavior. While the "minecraft:is_collidable" component governs how other mobs interact with the component's owner, the "minecraft:is_stackable" component describes how an entity interacts with others of its own kind.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_collidable
        """
        super().__init__("is_collidable")


class EntityRotationAxisAligned(Component):
    _identifier = "minecraft:rotation_axis_aligned"

    def __init__(self) -> None:
        """Causes the entity to automatically rotate to align with the nearest cardinal direction based on its current facing direction. Combining this with the "minecraft:body_rotation_blocked" component will cause the entity's body to align with the nearest cardinal direction and remain fixed in that orientation, regardless of changes in its facing direction.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rotation_axis_aligned
        """
        super().__init__("rotation_axis_aligned")


class EntityFreeCameraControlled(Component):
    _identifier = "minecraft:free_camera_controlled"

    def __init__(
        self,
        backwards_movement_modifier: float = 0.5,
        strafe_speed_modifier: float = 0.4,
    ) -> None:
        """When configured as a rideable entity, the entity will be controlled using WASD controls and mouse to move in three dimensions.

        Parameters:
            backwards_movement_modifier (float, optional): Modifies speed going backwards. Defaults to 0.5.
            strafe_speed_modifier (float, optional): Modifies the strafe speed. Defaults to 0.4.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_free_camera_controlled
        """
        super().__init__("free_camera_controlled")
        if backwards_movement_modifier != 0.5:
            self._add_field("backwards_movement_modifier", backwards_movement_modifier)
        if strafe_speed_modifier != 0.4:
            self._add_field("strafe_speed_modifier", strafe_speed_modifier)


class EntityLeashable(Component):
    _identifier = "minecraft:leashable"

    def __init__(
        self,
        can_be_cut: bool = True,
        can_be_stolen: bool = True,
        hard_distance: int = 6,
        max_distance: int = None,
        soft_distance: int = 4,
        on_unleash_interact_only: bool = False,
    ) -> None:
        """Describes how this mob can be leashed to other items.

        Parameters:
            can_be_cut (bool, optional): If true, players can cut both incoming and outgoing leashes by using shears on the entity. Defaults to True.
            can_be_stolen (bool, optional): If true, players can leash this entity even if it is already leashed to another entity. Defaults to True.
            hard_distance (int, optional): Distance (in blocks) over which the entity starts being pulled towards the leash holder with a spring-like force. Defaults to 6.
            max_distance (int, optional): Distance in blocks at which the leash breaks. Defaults to None.
            soft_distance (int, optional): Distance (in blocks) over which the entity starts pathfinding toward the leash holder, if able. Defaults to 4.
            on_unleash_interact_only (bool, optional): When set to true, "on_unleash" does not trigger when the entity gets unleashed for reasons other than the player directly interacting with it. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable
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
        if on_unleash_interact_only:
            self._add_field("on_unleash_interact_only", on_unleash_interact_only)

    def on_leash(self, event: str, target: FilterSubject = FilterSubject.Self) -> dict:
        self._add_field("on_leash", {"event": event, "target": target})
        return self

    def on_unleash(
        self,
        event: str,
        interact_only: bool = False,
        target: FilterSubject = FilterSubject.Self,
    ) -> dict:
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


class EntityBodyRotationAlwaysFollowsHead(Component):
    _identifier = "minecraft:body_rotation_always_follows_head"

    def __init__(self) -> None:
        """Causes the entity's body rotation to match the one of their head. Does not override the "minecraft:body_rotation_blocked" component.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_body_rotation_always_follows_head
        """
        super().__init__("body_rotation_always_follows_head")


class EntityTimer(Component):
    _identifier = "minecraft:timer"

    def __init__(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        looping: bool = True,
        randomInterval: bool = True,
        time: tuple[float, float] | float = 0,
    ) -> None:
        """Adds a timer after which an event will fire.

        Parameters:
            event (str): Event to fire when the time on the timer runs out.
            target (FilterSubject, optional): Target for the event that fires when the time on the timer runs out. Defaults to FilterSubject.Self.
            looping (bool, optional): If true, the timer will restart every time after it fires. Defaults to True.
            randomInterval (bool, optional): If true, the amount of time on the timer will be random between the min and max values specified in time. Defaults to True.
            time (tuple[float, float] | float, optional): Amount of time in seconds for the timer. Can be specified as a number or a pair of numbers (min and max). Incompatible with random_time_choices. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_timer
        """
        super().__init__("timer")

        self._add_field("time_down_event", {"event": event, "target": target.value})

        if not looping:
            self._add_field("looping", looping)
        if not randomInterval:
            self._add_field("randomInterval", randomInterval)
        if time != (0, 0):
            self._add_field("time", time)


class EntityPersistent(Component):
    _identifier = "minecraft:persistent"

    def __init__(self) -> None:
        """Defines whether an entity should be persistent in the game world.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_persistent
        """
        super().__init__("persistent")


class EntityVerticalMovementAction(Component):
    _identifier = "minecraft:vertical_movement_action"

    def __init__(self, vertical_velocity: float = 0.5) -> None:
        """When configured as a rideable entity, the entity will move upwards or downwards when the player uses the jump action.

        Parameters:
            vertical_velocity (float, optional): Vertical velocity to apply when jump action is issued. Defaults to 0.5.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vertical_movement.action?view=minecraft-bedrock-stable
        """
        self._enforce_version(ENTITY_SERVER_VERSION, "1.21.111")
        super().__init__("vertical_movement_action")
        if vertical_velocity != 0.5:
            self._add_field("vertical_velocity", vertical_velocity)


class EntityOnDeath(EventTrigger):
    _identifier = "minecraft:on_death"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger to call on this entity's death.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_death
        """
        super().__init__(event, filters, target)


class EntityOnFriendlyAnger(EventTrigger):
    _identifier = "minecraft:on_friendly_anger"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger that will run when a nearby entity of the same type as this entity becomes Angry.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_friendly_anger
        """
        super().__init__(event, filters, target)


class EntityOnHurt(EventTrigger):
    _identifier = "minecraft:on_hurt"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger to call when this entity takes damage.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_hurt
        """
        super().__init__(event, filters, target)


class EntityOnHurtByPlayer(EventTrigger):
    _identifier = "minecraft:on_hurt_by_player"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger to call when this entity is attacked by the player.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_hurt_by_player
        """
        super().__init__(event, filters, target)


class EntityOnIgnite(EventTrigger):
    _identifier = "minecraft:on_ignite"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger to call when this entity is set on fire.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_ignite
        """
        super().__init__(event, filters, target)


class EntityOnStartLanding(EventTrigger):
    _identifier = "minecraft:on_start_landing"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Only usable by the Ender Dragon. Adds a trigger to call when this entity lands.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_start_landing
        """
        super().__init__(event, filters, target)


class EntityOnStartTakeoff(EventTrigger):
    _identifier = "minecraft:on_start_takeoff"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Only usable by the Ender Dragon. Adds a trigger to call when this entity starts flying.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_start_takeoff
        """
        super().__init__(event, filters, target)


class EntityOnTargetAcquired(EventTrigger):
    _identifier = "minecraft:on_target_acquired"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger to call when this entity finds a target.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_target_acquired
        """
        super().__init__(event, filters, target)


class EntityOnTargetEscaped(EventTrigger):
    _identifier = "minecraft:on_target_escaped"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds a trigger to call when this entity loses the target it currently has.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_target_escaped
        """
        super().__init__(event, filters, target)


class EntityOnWakeWithOwner(EventTrigger):
    _identifier = "minecraft:on_wake_with_owner"

    def __init__(
        self,
        event: str,
        filters: Filter = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        """A trigger when a mob's tamed onwer wakes up.

        Parameters:
            event (str): The event to run when the conditions for this trigger are met.
            filters (Filter, optional): The list of conditions for this trigger to execute. Defaults to None.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitytriggers/minecrafttrigger_on_wake_with_owner
        """
        super().__init__(event, filters, target)


class EntityNameable(Component):
    _identifier = "minecraft:nameable"

    def __init__(
        self, allow_name_tag_renaming: bool = True, always_show: bool = False
    ) -> None:
        """Allows this entity to be named (e.g. using a name tag).

        Parameters:
            allow_name_tag_renaming (bool, optional): If true, this entity can be renamed with name tags. Defaults to True.
            always_show (bool, optional): If true, the name will always be shown. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_nameable
        """
        super().__init__("nameable")

        if always_show:
            self._add_field("always_show", always_show)
        if not allow_name_tag_renaming:
            self._add_field("allow_name_tag_renaming", allow_name_tag_renaming)

        self._add_field("name_actions", [])

    def default_trigger(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets the default trigger event for the nameable component.

        Parameters:
            event (str): The event to trigger when the entity is named.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.
        """
        self._add_field("default_trigger", {"event": event, "target": target})
        return self

    def name_action(self, name, event: str, target: FilterSubject = FilterSubject.Self):
        """Adds a name action to the nameable component.

        Parameters:
            name (str): The name that triggers the event.
            event (str): The event to trigger when the entity is named.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.
        """
        self._component["name_actions"].append(
            {"name_filter": name, "on_named": {"event": event, "target": target}}
        )
        return self


class EntityRotationLockedToVehicle(Component):
    _identifier = "minecraft:rotation_locked_to_vehicle"

    def __init__(self) -> None:
        """Causes the entity's rotation to match their vehicle's facing direction.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rotation_locked_to_vehicle
        """
        super().__init__("rotation_locked_to_vehicle")


class EntityHealable(Component):
    _identifier = "minecraft:healable"

    def __init__(self, filters: Filter = None, force_use: bool = False) -> None:
        """How entities heal.

        Parameters:
            filters (Filter, optional): The filter group that defines the conditions for using this item to heal the entity. Defaults to None.
            force_use (bool, optional): Determines if item can be used regardless of entity being at full health. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_healable
        """
        super().__init__("healable")
        if not filters is None:
            self._add_field("filters", filters)
        if force_use:
            self._add_field("force_use", force_use)
        self._add_field("items", [])

    def add_heal_item(
        self,
        item: MinecraftItemDescriptor | Identifier,
        heal_amount: float,
        result_item: MinecraftItemDescriptor | Identifier = None,
    ) -> dict:
        """Adds a healing item to the healable component.

        Parameters:
            item (str): The item that can heal the entity.
            heal_amount (float): The amount of health the item restores.

        Returns:
            dict: A dictionary containing the healing item information.
        """
        self._component["items"].append(
            {"item": item, "heal_amount": heal_amount, "result_item": result_item}
        )
        return self


class EntityExhaustionValues(Component):
    _identifier = "minecraft:exhaustion_values"

    def __init__(
        self,
        attack: float = 0.1,
        damage: float = 0.1,
        heal: float = 6,
        jump: float = 0.05,
        lunge: float = 4,
        mine: float = 0.005,
        sprint: float = 0.01,
        sprint_jump: float = 0.2,
        swim: float = 0.01,
        walk: float = 0.0,
    ) -> None:
        """Defines how much exhaustion each player action should take.

        Parameters:
            attack (float, optional): Amount of exhaustion applied when attacking. Defaults to 0.1.
            damage (float, optional): Amount of exhaustion applied when taking damage. Defaults to 0.1.
            heal (float, optional): Amount of exhaustion applied when healed through food regeneration. Defaults to 6.
            jump (float, optional): Amount of exhaustion applied when jumping. Defaults to 0.05.
            lunge (float, optional): Amount of exhaustion applied when triggering the lunge enchantment, multiplied by the enchantment level. Defaults to 4.
            mine (float, optional): Amount of exhaustion applied when mining. Defaults to 0.005.
            sprint (float, optional): Amount of exhaustion applied when sprinting. Defaults to 0.01.
            sprint_jump (float, optional): Amount of exhaustion applied when sprint jumping. Defaults to 0.2.
            swim (float, optional): Amount of exhaustion applied when swimming. Defaults to 0.01.
            walk (float, optional): Amount of exhaustion applied when walking. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_exhaustion_values
        """
        super().__init__("exhaustion_values")

        if attack != 0.1:
            self._add_field("attack", attack)
        if damage != 0.1:
            self._add_field("damage", damage)
        if heal != 6:
            self._add_field("heal", heal)
        if jump != 0.05:
            self._add_field("jump", jump)
        if lunge != 4:
            self._add_field("lunge", lunge)
        if mine != 0.005:
            self._add_field("mine", mine)
        if sprint != 0.01:
            self._add_field("sprint", sprint)
        if sprint_jump != 0.2:
            self._add_field("sprint_jump", sprint_jump)
        if swim != 0.01:
            self._add_field("swim", swim)
        if walk != 0.0:
            self._add_field("walk", walk)


class EntityIsHiddenWhenInvisible(Component):
    _identifier = "minecraft:is_hidden_when_invisible"

    def __init__(self) -> None:
        """The entity can hide from hostile mobs while invisible.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_hidden_when_invisible
        """
        super().__init__("is_hidden_when_invisible")


class EntityHurtOnCondition(Component):
    _identifier = "minecraft:hurt_on_condition"

    def __init__(
        self,
        cause: DamageCause = None,
        filters: Filter = None,
        damage_per_tick: int = 1,
    ) -> None:
        """Defines a set of conditions under which an entity should take damage.

        Parameters:
            cause (DamageCause, optional): The kind of damage that is caused to the entity. Various armors and spells use this to determine if the entity is immune. Defaults to None.
            filters (Filter, optional): The set of conditions that must be satisfied before the entity takes the defined damage. Defaults to None.
            damage_per_tick (int, optional): The amount of damage done each tick that the conditions are met. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_hurt_on_condition
        """
        super().__init__("hurt_on_condition")
        self._add_field("damage_conditions", [])
        self.add_condition(cause, filters, damage_per_tick)

    def add_condition(
        self,
        cause: DamageCause = None,
        filters: Filter = None,
        damage_per_tick: int = 1,
    ):
        self._component["damage_conditions"].append(
            {
                "cause": cause,
                "filters": filters,
                "damage_per_tick": damage_per_tick,
            }
        )
        return self


class EntityHide(Component):
    _identifier = "minecraft:hide"

    def __init__(self) -> None:
        """Moves to and hides at their owned POI or the closest nearby.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_hide
        """
        super().__init__("hide")


class EntityAnnotationBreakDoor(Component):
    _identifier = "minecraft:annotation.break_door"

    def __init__(
        self,
        break_time: int = 12,
        min_difficulty: Difficulty = Difficulty.Hard,
    ) -> None:
        """Allows an entity to break doors, assuming that that flags set up for the component to use in navigation.

        Parameters:
            break_time (int, optional): The time in seconds required to break through doors. Defaults to 12.
            min_difficulty (Difficulty, optional): The minimum difficulty that the world must be on for this entity to break doors. Defaults to Difficulty.Hard.

        Note:
            Requires the entity's navigation component to have can_break_doors set to true.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_annotation_break_door
        """
        super().__init__("annotation.break_door")
        if break_time != 12:
            self._add_field("break_time", max(0, break_time))
        if min_difficulty != Difficulty.Hard:
            self._add_field("min_difficulty", min_difficulty.value)


class EntityAnnotationOpenDoor(Component):
    _identifier = "minecraft:annotation.open_door"

    def __init__(self) -> None:
        """Allows the entity to open doors.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_annotation_open_door
        """
        super().__init__("minecraft:annotation.open_door")


class EntityDweller(Component):
    _identifier = "minecraft:dweller"

    def __init__(
        self,
        can_find_poi: bool = False,
        can_migrate: bool = False,
        dweller_role: Literal["inhabitant", "defender", "hostile", "passive"] = None,
        dwelling_bounds_tolerance: float = 0.0,
        dwelling_type: Literal["village"] = None,
        first_founding_reward: int = 0,
        preferred_profession: str = None,
        update_interval_base: float = 0.0,
        update_interval_variant: float = 0.0,
    ) -> None:
        """Compels an entity to join and migrate between villages and other dwellings.

        Parameters:
            can_find_poi (bool, optional): Whether or not the entity can find and add POIs to the dwelling. Defaults to False.
            can_migrate (bool, optional): Determines whether the entity can migrate between dwellings, or only have its initial dwelling. Defaults to False.
            dweller_role (Literal['inhabitant', 'defender', 'hostile', 'passive'], optional): Description. Defaults to None.
            dwelling_bounds_tolerance (float, optional): A padding distance for checking if the entity is within the dwelling. Defaults to 0.0.
            dwelling_type (Literal['village'], optional): The type of dwelling the entity wishes to join. Current Types: village. Defaults to None.
            first_founding_reward (int, optional): Determines how much reputation players are rewarded on first founding. Defaults to 0.
            preferred_profession (str, optional): Allows the user to define a starting profession for this particular Dweller, instead of letting them choose organically. (They still need to gain experience from trading before this takes effect.). Defaults to None.
            update_interval_base (float, optional): How often the entity checks on their dwelling status in ticks. Positive values only. Defaults to 0.0.
            update_interval_variant (float, optional): The variant value in ticks that will be added to the update_interval_base. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dweller
        """
        super().__init__("dweller")

        if can_find_poi:
            self._add_field("can_find_poi", can_find_poi)
        if can_migrate:
            self._add_field("can_migrate", can_migrate)
        if dweller_role is not None:
            self._add_field("dweller_role", dweller_role)
        if dwelling_bounds_tolerance != 0.0:
            self._add_field("dwelling_bounds_tolerance", dwelling_bounds_tolerance)
        if dwelling_type is not None:
            self._add_field("dwelling_type", dwelling_type)
        if first_founding_reward != 0:
            self._add_field("first_founding_reward", first_founding_reward)
        if preferred_profession is not None:
            self._add_field("preferred_profession", preferred_profession)
        if update_interval_base != 0.0:
            self._add_field("update_interval_base", update_interval_base)
        if update_interval_variant != 0.0:
            self._add_field("update_interval_variant", update_interval_variant)


class EntityEconomyTradeTable(Component):
    _identifier = "minecraft:economy_trade_table"

    def __init__(
        self,
        table: TradeTable | str,
        convert_trades_economy: bool = False,
        cured_discount: list[int] = None,
        display_name: str = None,
        hero_demand_discount: int = -4,
        max_cured_discount: list[int] = None,
        max_nearby_cured_discount: int = -200,
        nearby_cured_discount: int = -20,
        new_screen: bool = False,
        persist_trades: bool = False,
        show_trade_screen: bool = True,
        use_legacy_price_formula: bool = False,
    ) -> None:
        """Defines this entity's ability to trade with players.

        Parameters:
            table (TradeTable | str): File path relative to the resource pack root for this entity's trades.
            convert_trades_economy (bool, optional): Determines when the mob transforms, if the trades should be converted when the new mob has a economy_trade_table. Defaults to False.
            cured_discount (list[int], optional): How much should the discount be modified by when the player has cured the Zombie Villager. Defaults to None.
            display_name (str, optional): Name to be displayed while trading with this entity. Defaults to None.
            hero_demand_discount (int, optional): Used in legacy prices to determine how much should Demand be modified by when the player has the Hero of the Village mob effect. Defaults to -4.
            max_cured_discount (list[int], optional): The max the discount can be modified by when the player has cured the Zombie Villager. Defaults to None.
            max_nearby_cured_discount (int, optional): The max the discount can be modified by when the player has cured a nearby Zombie Villager. Only used when use_legacy_price_formula is true, otherwise max_cured_discount (low) is used. Defaults to -200.
            nearby_cured_discount (int, optional): How much should the discount be modified by when the player has cured a nearby Zombie Villager. Defaults to -20.
            new_screen (bool, optional): Used to determine if trading with entity opens the new trade screen. Defaults to False.
            persist_trades (bool, optional): Determines if the trades should persist when the mob transforms. Defaults to False.
            show_trade_screen (bool, optional): Show an in game trade screen when interacting with the mob. Defaults to True.
            use_legacy_price_formula (bool, optional): Determines whether the legacy formula is used to determines the trade prices. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_economy_trade_table
        """
        super().__init__("economy_trade_table")
        self._add_field(
            "table", table.table_path if isinstance(table, TradeTable) else table
        )

        if convert_trades_economy:
            self._add_field("convert_trades_economy", convert_trades_economy)
        if cured_discount is not None:
            self._add_field("cured_discount", cured_discount)
        if display_name is not None:
            lower_case = display_name.lower().replace(" ", "_")
            key = (
                f"tradetable.{CONFIG.NAMESPACE}.{CONFIG.PROJECT_NAME}.{lower_case}.name"
            )
            AnvilTranslator().add_localization_entry(key, display_name)
            self._add_field("display_name", key)
        if hero_demand_discount != -4:
            self._add_field("hero_demand_discount", hero_demand_discount)
        if max_cured_discount is not None:
            self._add_field("max_cured_discount", max_cured_discount)
        if max_nearby_cured_discount != -200:
            self._add_field("max_nearby_cured_discount", max_nearby_cured_discount)
        if nearby_cured_discount != -20:
            self._add_field("nearby_cured_discount", nearby_cured_discount)
        if new_screen:
            self._add_field("new_screen", new_screen)
        if persist_trades:
            self._add_field("persist_trades", persist_trades)
        if not show_trade_screen:
            self._add_field("show_trade_screen", show_trade_screen)
        if use_legacy_price_formula:
            self._add_field("use_legacy_price_formula", use_legacy_price_formula)


class EntityScheduler(Component):
    _identifier = "minecraft:scheduler"

    def __init__(
        self,
        max_delay_secs: float = 0.0,
        min_delay_secs: float = 0.0,
    ) -> None:
        """Fires off scheduled mob events at time of day events.

        Parameters:
            max_delay_secs (float, optional): Description. Defaults to 0.0.
            min_delay_secs (float, optional): Description. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_scheduler
        """
        super().__init__("scheduler")

        if max_delay_secs != 0.0:
            self._add_field("max_delay_secs", max_delay_secs)
        if min_delay_secs != 0.0:
            self._add_field("min_delay_secs", min_delay_secs)
        self._add_field("scheduled_events", [])

    def add_scheduled_event(self, event: str, filters: Filter = None):
        """Adds a scheduled event to the scheduler.

        Parameters:
            event (str): The event to fire.
            filters (Filter, optional): The filters to check before firing the event. Defaults to None.

        Returns:
            EntityScheduler: The current instance of the class.
        """
        self._get_field("scheduled_events", []).append(
            {"event": event, "filters": filters}
        )
        return self


class EntityTradeResupply(Component):
    _identifier = "minecraft:trade_resupply"

    def __init__(self) -> None:
        """Resupplies an entity's trade.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trade_resupply
        """
        super().__init__("trade_resupply")


class EntityShareables(Component):
    _identifier = "minecraft:shareables"

    def __init__(
        self,
        all_items: bool = False,
        all_items_max_amount: int = -1,
        all_items_surplus_amount: int = -1,
        all_items_want_amount: int = -1,
        singular_pickup: bool = False,
    ) -> None:
        """Defines a list of items the mob wants to share or pick up. Items can be configured with optional parameters to control pickup, sharing, and inventory behavior.

        Parameters:
            all_items (bool, optional): A bucket for all other items in the game. Note this category is always least priority items. Defaults to False.
            all_items_max_amount (int, optional): Maximum number of this item the mob will hold. Defaults to -1.
            all_items_surplus_amount (int, optional): Number of this item considered extra that the entity wants to share. Defaults to -1.
            all_items_want_amount (int, optional): Number of this item this entity wants to share. Defaults to -1.
            singular_pickup (bool, optional): Boolean value that controls if the mob is able to pick up more of the same item if it is already holding that item. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_shareables
        """
        super().__init__("shareables")

        if all_items:
            self._add_field("all_items", all_items)
        if all_items_max_amount != -1:
            self._add_field("all_items_max_amount", all_items_max_amount)
        if all_items_surplus_amount != -1:
            self._add_field("all_items_surplus_amount", all_items_surplus_amount)
        if all_items_want_amount != -1:
            self._add_field("all_items_want_amount", all_items_want_amount)
        if singular_pickup:
            self._add_field("singular_pickup", singular_pickup)

        self._add_field("items", [])

    def item(
        self,
        item: MinecraftItemDescriptor | Identifier,
        admire: bool = False,
        barter: bool = False,
        consume_item: bool = False,
        craft_into: MinecraftItemDescriptor | Identifier = None,
        max_amount: int = -1,
        pickup_limit: int = -1,
        pickup_only: bool = False,
        priority: int = 0,
        stored_in_inventory: bool = False,
        surplus_amount: int = -1,
        want_amount: int = -1,
    ):
        """Adds an item to the shareables list.

        Parameters:
            item (str): The identifier of the item.
            admire (bool, optional): Mob will admire the item after picking up by looking at it. Defaults to False.
            barter (bool, optional): Mob will barter for the item after picking it up. Defaults to False.
            consume_item (bool, optional): Determines whether the mob will consume the item or not. Defaults to False.
            craft_into (str, optional): Item to craft this item into. Defaults to None.
            max_amount (int, optional): Maximum number of this item the mob will hold. Defaults to -1.
            pickup_limit (int, optional): Maximum number items the mob will pick up during a single goal tick. Defaults to -1.
            pickup_only (bool, optional): Determines whether the mob can only pickup the item and not drop it. Defaults to False.
            priority (int, optional): Prioritizes which items the entity prefers. 0 is the highest priority. Defaults to 0.
            stored_in_inventory (bool, optional): Determines whether the mob will try to put the item in its inventory if it has the inventory component and if it can't be equipped. Defaults to False.
            surplus_amount (int, optional): Number of this item considered extra that the entity wants to share. Defaults to -1.
            want_amount (int, optional): Number of this item this entity wants to share. Defaults to -1.
        """
        item_data = {
            "item": str(item),
            "priority": priority,
        }
        if admire:
            item_data["admire"] = admire
        if barter:
            item_data["barter"] = barter
        if consume_item:
            item_data["consume_item"] = consume_item
        if craft_into is not None:
            item_data["craft_into"] = str(craft_into)
        if max_amount != -1:
            item_data["max_amount"] = max_amount
        if pickup_limit != -1:
            item_data["pickup_limit"] = pickup_limit
        if pickup_only:
            item_data["pickup_only"] = pickup_only
        if stored_in_inventory:
            item_data["stored_in_inventory"] = stored_in_inventory
        if surplus_amount != -1:
            item_data["surplus_amount"] = surplus_amount
        if want_amount != -1:
            item_data["want_amount"] = want_amount

        self._component["items"].append(item_data)
        return self


class EntityArmorEquipmentSlotMapping(Component):
    _identifier = "minecraft:entity_armor_equipment_slot_mapping"

    def __init__(self, armor_slot: Slots) -> None:
        """It defines to which armor slot an item equipped to 'minecraft:equippable''s second slot should be equipped to. It is automatically applied to all entities for worlds with a version greater than or equal to 1.21.10. For older worlds, 'slot.armor.torso' will be used. It is strongly advised not to explicitly use this component, as no backwards compatibility for it will be provided.

        Parameters:
            armor_slot (Slots): The armor slot an item equipped to 'minecraft:equippable''s second slot should be equipped to.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_entity_armor_equipment_slot_mapping
        """
        super().__init__("entity_armor_equipment_slot_mapping")
        if not armor_slot in [Slots.Chest, Slots.Body]:
            raise ValueError(
                f"Invalid armor_slot '{armor_slot}'. Must be one of: '{Slots.Chest}', '{Slots.Body}'"
            )
        self._add_field("armor_slot", armor_slot)


class EntityDespawn(Component):
    _identifier = "minecraft:despawn"

    def __init__(
        self,
        despawn_from_chance: bool = True,
        despawn_from_distance: tuple[int, int] = None,
        despawn_from_inactivity: bool = True,
        despawn_from_simulation_edge: bool = True,
        filters: Filter = None,
        min_range_inactivity_timer: int = 30,
        min_range_random_chance: int = 800,
        remove_child_entities: bool = False,
    ) -> None:
        """Despawns the Actor when the despawn rules or optional filters evaluate to true.

        Parameters:
            despawn_from_chance (bool, optional): Determines if "min_range_random_chance" is used in the standard despawn rules. Defaults to True.
            despawn_from_distance (tuple[int, int], optional): Specifies if the 'min_distance' and 'max_distance' are used in the standard despawn rules. Defaults to None.
            despawn_from_inactivity (bool, optional): Determines if the "min_range_inactivity_timer" is used in the standard despawn rules. Defaults to True.
            despawn_from_simulation_edge (bool, optional): Determines if the mob is instantly despawned at the edge of simulation distance in the standard despawn rules. Defaults to True.
            filters (Filter, optional): The list of conditions that must be satisfied before the Actor is despawned. If a filter is defined then standard despawn rules are ignored. Defaults to None.
            min_range_inactivity_timer (int, optional): The amount of time in seconds that the mob must be inactive. Defaults to 30.
            min_range_random_chance (int, optional): A random chance between 1 and the given value. Defaults to 800.
            remove_child_entities (bool, optional): If true, all entities linked to this entity in a child relationship (eg. leashed) will also be despawned. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_despawn
        """
        super().__init__("despawn")

        if not despawn_from_chance:
            self._add_field("despawn_from_chance", despawn_from_chance)
        if despawn_from_distance is not None:
            if (
                not isinstance(despawn_from_distance, (tuple, list))
                or not len(despawn_from_distance) == 2
                or not all(isinstance(i, int) for i in despawn_from_distance)
            ):
                raise ValueError("despawn_from_distance must be a tuple of 2 integers")

            if despawn_from_distance[0] < 0 or despawn_from_distance[1] < 0:
                raise ValueError("despawn_from_distance values must be non-negative")
            if despawn_from_distance[0] > despawn_from_distance[1]:
                raise ValueError(
                    "despawn_from_distance minimum must be less than or equal to maximum"
                )

            self._add_field(
                "despawn_from_distance",
                {
                    "min_distance": despawn_from_distance[0],
                    "max_distance": despawn_from_distance[1],
                },
            )
        if not despawn_from_inactivity:
            self._add_field("despawn_from_inactivity", despawn_from_inactivity)
        if not despawn_from_simulation_edge:
            self._add_field(
                "despawn_from_simulation_edge", despawn_from_simulation_edge
            )
        if filters is not None:
            self._add_field("filters", filters)
        if min_range_inactivity_timer != 30:
            self._add_field("min_range_inactivity_timer", min_range_inactivity_timer)
        if min_range_random_chance != 800:
            self._add_field("min_range_random_chance", min_range_random_chance)
        if remove_child_entities:
            self._add_field("remove_child_entities", remove_child_entities)

    def despawn_from_distance(self, range: tuple[int, int] = (32, 128)):
        """Sets the despawn distance properties.

        Parameters:
            range (tuple[int, int], optional): A tuple containing the minimum and maximum distance for despawning. Defaults to (32, 128).

        Returns:
            EntityDespawn: Returns the EntityDespawn component to allow for method chaining.
        """
        if (
            not isinstance(range, tuple)
            or not len(range) == 2
            or not all(isinstance(i, int) for i in range)
        ):
            raise ValueError("range must be a tuple of 2 integers")
        if range[0] < 0 or range[1] < 0:
            raise ValueError("range values must be non-negative")
        if range[0] > range[1]:
            raise ValueError("range minimum must be less than or equal to maximum")
        if range != (32, 128):
            min_distance, max_distance = range
            self._add_field(
                "despawn_from_distance",
                {"min_distance": min_distance, "max_distance": max_distance},
            )
        return self


class EntityGameEventMovementTracking(Component):
    _identifier = "minecraft:game_event_movement_tracking"

    def __init__(
        self,
        emit_flap: bool = False,
        emit_move: bool = True,
        emit_swim: bool = True,
    ) -> None:
        """Allows an entity to emit `entityMove`, `swim` and `flap` game events, depending on the block the entity is moving through. It is added by default to every mob. Add it again to override its behavior.

        Parameters:
            emit_flap (bool, optional): If true, the `flap` game event will be emitted when the entity moves through air. Defaults to False.
            emit_move (bool, optional): If true, the `entityMove` game event will be emitted when the entity moves on ground or through a solid. Defaults to True.
            emit_swim (bool, optional): If true, the `swim` game event will be emitted when the entity moves through a liquid. Defaults to True.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_game_event_movement_tracking
        """
        super().__init__("game_event_movement_tracking")

        if emit_flap:
            self._add_field("emit_flap", emit_flap)
        if not emit_move:
            self._add_field("emit_move", emit_move)
        if not emit_swim:
            self._add_field("emit_swim", emit_swim)


class EntitySpawnEggInteraction(Component):
    _identifier = "minecraft:spawn_egg_interaction"

    def __init__(self) -> None:
        """Enables interacting with this entity using its own spawn egg to spawn a born child. Runs the "minecraft:entity_born" event on the created entity as well as the defined "on_spawn" event."""

        super().__init__("spawn_egg_interaction")


class EntityAttackCooldown(Component):
    _identifier = "minecraft:attack_cooldown"

    def __init__(
        self,
        attack_cooldown_time: Seconds | tuple[Seconds, Seconds] = None,
        attack_cooldown_complete_event: str = None,
        attack_cooldown_complete_target: FilterSubject = FilterSubject.Self,
    ) -> None:
        """Adds a cooldown to an entity. The intention of this cooldown is to be used to prevent the entity from attempting to acquire new attack targets.

        Parameters:
            attack_cooldown_time (Seconds | tuple[Seconds, Seconds], optional): Amount of time in seconds for the cooldown. Can be specified as a number or a pair of numbers (min and max). Defaults to None.
            attack_cooldown_complete_event (str, optional): Event to be run when the cooldown is complete. Can be an object with event and target properties, or a simple event string. Defaults to None.
            attack_cooldown_complete_target (FilterSubject, optional): Target value to serialize when attack_cooldown_complete_event is written as an event object. Defaults to FilterSubject.Self.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_attack_cooldown
        """
        super().__init__("attack_cooldown")
        if attack_cooldown_time is not None:
            if isinstance(attack_cooldown_time, (tuple, list)):
                self._add_field(
                    "attack_cooldown_time",
                    AnvilFormatter.min_max_list(
                        attack_cooldown_time,
                        "attack_cooldown_time",
                        clamp_min=0,
                    ),
                )
            else:
                self._add_field("attack_cooldown_time", max(0, attack_cooldown_time))
        if attack_cooldown_complete_event is not None:
            if attack_cooldown_complete_target is FilterSubject.Self:
                self._add_field(
                    "attack_cooldown_complete_event",
                    attack_cooldown_complete_event,
                )
            else:
                self._add_field(
                    "attack_cooldown_complete_event",
                    {
                        "event": attack_cooldown_complete_event,
                        "target": attack_cooldown_complete_target.value,
                    },
                )


class EntityCombatRegeneration(Component):
    _identifier = "minecraft:combat_regeneration"

    def __init__(
        self,
        apply_to_family: bool = False,
        apply_to_self: bool = False,
        regeneration_duration: int | Literal["infinite"] = 5,
    ) -> None:
        """Gives `Regeneration I` and removes `Mining Fatigue` from the mob that kills the entity's attack target.

        Parameters:
            apply_to_family (bool, optional): Determines if the mob will grant mobs of the same type combat buffs if they kill the target. Defaults to False.
            apply_to_self (bool, optional): Determines if the mob will grant itself the combat buffs if it kills the target. Defaults to False.
            regeneration_duration (int | Literal['infinite'], optional): The duration in seconds of Regeneration I added to the mob. Can also be set to "infinite". Defaults to 5.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_combat_regeneration
        """
        super().__init__("combat_regeneration")
        if apply_to_family:
            self._add_field("apply_to_family", apply_to_family)
        if apply_to_self:
            self._add_field("apply_to_self", apply_to_self)
        if regeneration_duration != 5:
            self._add_field("regeneration_duration", regeneration_duration)


class EntityDamageOverTime(Component):
    _identifier = "minecraft:damage_over_time"

    def __init__(
        self,
        damage_per_hurt: int = 1,
        time_between_hurt: Seconds = 0,
    ) -> None:
        """Applies defined amount of damage to the entity at specified intervals.

        Parameters:
            damage_per_hurt (int, optional): Amount of damage caused each hurt. Defaults to 1.
            time_between_hurt (Seconds, optional): Time in seconds between damage. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_damage_over_time
        """
        super().__init__("damage_over_time")
        if damage_per_hurt != 1:
            self._add_field("damage_per_hurt", damage_per_hurt)
        if time_between_hurt != 0:
            self._add_field("time_between_hurt", max(0, time_between_hurt))


class EntityDefaultLookAngle(Component):
    _identifier = "minecraft:default_look_angle"

    def __init__(self, value: float = 0) -> None:
        """Sets this entity's default head rotation angle.

        Parameters:
            value (float, optional): Angle in degrees. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_default_look_angle
        """
        super().__init__("default_look_angle")
        if value != 0:
            self._add_field("value", value)


class EntityFloatsInLiquid(Component):
    _identifier = "minecraft:floats_in_liquid"

    def __init__(self) -> None:
        """Sets that this entity can float in liquid blocks.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_floats_in_liquid
        """
        super().__init__("floats_in_liquid")


class EntityGroundOffset(Component):
    _identifier = "minecraft:ground_offset"

    def __init__(self, value: float = 0) -> None:
        """Sets the offset from the ground that the entity is actually at.

        Parameters:
            value (float, optional): The value of the entity's offset from the terrain, in blocks. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ground_offset
        """
        super().__init__("ground_offset")
        if value != 0:
            self._add_field("value", value)


class EntityInputAirControlled(Component):
    _identifier = "minecraft:input_air_controlled"

    def __init__(
        self,
        backwards_movement_modifier: float = 0.5,
        strafe_speed_modifier: float = 0.4,
    ) -> None:
        """When configured as a rideable entity, the entity will be controlled using WASD controls and mouse to move in three dimensions.

        Parameters:
            backwards_movement_modifier (float, optional): Modifies speed going backwards. Defaults to 0.5.
            strafe_speed_modifier (float, optional): Modifies the strafe speed. Defaults to 0.4.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_input_air_controlled
        """
        super().__init__("input_air_controlled")
        if backwards_movement_modifier != 0.5:
            self._add_field("backwards_movement_modifier", backwards_movement_modifier)
        if strafe_speed_modifier != 0.4:
            self._add_field("strafe_speed_modifier", strafe_speed_modifier)


class EntityIsPregnant(Component):
    _identifier = "minecraft:is_pregnant"

    def __init__(self) -> None:
        """Sets that this entity is currently pregnant.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_pregnant
        """
        super().__init__("is_pregnant")


class EntityIsShaking(Component):
    _identifier = "minecraft:is_shaking"

    def __init__(self) -> None:
        """Sets that this entity is currently shaking.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_is_shaking
        """
        super().__init__("is_shaking")


class EntityRemoveInPeaceful(Component):
    _identifier = "minecraft:remove_in_peaceful"

    def __init__(self) -> None:
        """Denotes entities that are not allowed to exist in "Peaceful" difficulty.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_remove_in_peaceful
        """
        super().__init__("remove_in_peaceful")


class EntitySoundVolume(Component):
    _identifier = "minecraft:sound_volume"

    def __init__(self, value: float = 1) -> None:
        """Sets the entity's base volume for sound effects.

        Parameters:
            value (float, optional): The value of the volume the entity uses for sound effects. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_sound_volume
        """
        super().__init__("sound_volume")
        if value != 1:
            self._add_field("value", value)


class EntityUnderwaterMountBreathing(Component):
    _identifier = "minecraft:underwater_mount_breathing"

    def __init__(self) -> None:
        """Pauses this entity's breathing under water.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_underwater_mount_breathing
        """
        super().__init__("underwater_mount_breathing")


class EntityUsesLegacyFriction(Component):
    _identifier = "minecraft:uses_legacy_friction"

    def __init__(self) -> None:
        """When set, legacy calculations are used when applying "minecraft:friction_modifier". This component is automatically added to legacy content to preserve existing behavior. The legacy calculations are incorrect and should not be used for new content.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_uses_legacy_friction
        """
        super().__init__("uses_legacy_friction")


class EntityVibrationDamper(Component):
    _identifier = "minecraft:vibration_damper"

    def __init__(self) -> None:
        """Vibrations emitted by an entity with this component will be ignored.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vibration_damper
        """
        super().__init__("vibration_damper")


class EntityWalkAnimationSpeed(Component):
    _identifier = "minecraft:walk_animation_speed"

    def __init__(self, value: float = 1) -> None:
        """Sets the speed multiplier for this entity's walk animation speed.

        Parameters:
            value (float, optional): The higher the number, the faster the animation for walking plays. A value of 1.0 means normal speed, while 2.0 means twice as fast. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_walk_animation_speed
        """
        super().__init__("walk_animation_speed")
        if value != 1:
            self._add_field("value", value)


class EntityWantsJockey(Component):
    _identifier = "minecraft:wants_jockey"

    def __init__(self) -> None:
        """Sets that this entity wants to become a jockey.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_wants_jockey
        """
        super().__init__("wants_jockey")


class EntityBlockClimber(Component):
    _identifier = "minecraft:block_climber"

    def __init__(self) -> None:
        """Allows the player to detect and manuever on the scaffolding block.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_block_climber
        """
        super().__init__("block_climber")


class EntityBlockSensor(Component):
    _identifier = "minecraft:block_sensor"

    def __init__(
        self,
        sensor_radius: float = 16,
        sources: Filter = None,
    ) -> None:
        """Fires off a specified event when a block in the block list is broken within the sensor range.

        Parameters:
            sensor_radius (float, optional): The maximum radial distance in which a specified block can be detected. The biggest radius is 32.0. Defaults to 16.
            sources (Filter, optional): List of sources that break the block to listen for. If none are specified, all block breaks will be detected. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_block_sensor
        """
        super().__init__("block_sensor")
        self._add_field("on_break", [])
        if sensor_radius != 16:
            self._add_field("sensor_radius", clamp(sensor_radius, 0, 32))
        if sources is not None:
            self._add_field("sources", sources)

    def on_break(
        self,
        block_list: list[MinecraftBlockDescriptor | Identifier],
        on_block_broken: str,
    ):
        self._component["on_break"].append(
            {
                "block_list": [str(block) for block in block_list],
                "on_block_broken": on_block_broken,
            }
        )
        return self


class EntityBribeable(Component):
    _identifier = "minecraft:bribeable"

    def __init__(
        self,
        bribe_items: str | list[MinecraftItemDescriptor | Identifier] = None,
        bribe_cooldown: Seconds = 2,
    ) -> None:
        """Defines the way an entity can get into the 'bribed' state.

        Parameters:
            bribe_items (str | list[MinecraftItemDescriptor | Identifier], optional): The list of items that can be used to bribe the entity. Can be an array or a single item string. Defaults to None.
            bribe_cooldown (Seconds, optional): Time in seconds before the Entity can be bribed again. Defaults to 2.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_bribeable
        """
        super().__init__("bribeable")
        if bribe_items is not None:
            self._add_field("bribe_items", bribe_items)
        if bribe_cooldown != 2:
            self._add_field("bribe_cooldown", max(0, bribe_cooldown))


class EntityCelebrateHunt(Component):
    _identifier = "minecraft:celebrate_hunt"

    def __init__(
        self,
        broadcast: bool = True,
        celebration_targets: Filter = None,
        celebrate_sound: str = None,
        duration: int = 4,
        radius: float = 16,
        sound_interval: int | tuple[int, int] = 0,
    ) -> None:
        """Specifies hunt celebration behaviour.

        Parameters:
            broadcast (bool, optional): If true, celebration will be broadcasted to other entities in the radius. Defaults to True.
            celebration_targets (Filter, optional): Conditions the hunt target must satisfy to initiate celebration. Defaults to None.
            celebrate_sound (str, optional): The sound event to play when the mob is celebrating. Defaults to None.
            duration (int, optional): Duration, in seconds, of celebration. Defaults to 4.
            radius (float, optional): If broadcast is enabled, specifies the radius in which it will notify other entities for celebration. Defaults to 16.
            sound_interval (int | tuple[int, int], optional): The range of time in seconds to randomly wait before playing the sound again. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_celebrate_hunt
        """
        super().__init__("celebrate_hunt")
        if not broadcast:
            self._add_field("broadcast", broadcast)
        if celebration_targets is not None:
            self._add_field("celebration_targets", celebration_targets)
        if celebrate_sound is not None:
            self._add_field("celebrate_sound", celebrate_sound)
        if duration != 4:
            self._add_field("duration", max(0, duration))
        if radius != 16:
            self._add_field("radius", max(0, radius))
        if sound_interval != 0:
            if isinstance(sound_interval, (tuple, list)):
                self._add_field(
                    "sound_interval",
                    AnvilFormatter.min_max_dict(
                        sound_interval,
                        "sound_interval",
                        value_types=(int,),
                        clamp_min=0,
                    ),
                )
            else:
                self._add_field("sound_interval", max(0, sound_interval))


class EntityHeartbeat(Component):
    _identifier = "minecraft:heartbeat"

    def __init__(
        self,
        interval: Molang | str | float = 1.0,
        sound_event: str = "heartbeat",
    ) -> None:
        """Defines the entity's heartbeat.

        Parameters:
            interval (Molang | str | float, optional): A Molang expression defining the inter-beat interval in seconds. A value of zero or less means no heartbeat. Defaults to 1.0.
            sound_event (str, optional): Level sound event to be played as the heartbeat sound. Defaults to "heartbeat".

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_heartbeat
        """
        super().__init__("heartbeat")
        if interval not in (1, 1.0, "1", "1.0"):
            self._add_field("interval", interval)
        if sound_event != "heartbeat":
            self._add_field("sound_event", sound_event)


class EntityHome(Component):
    _identifier = "minecraft:home"

    def __init__(
        self,
        home_block_list: list[MinecraftBlockDescriptor | Identifier] = None,
        restriction_radius: int = 0,
        restriction_type: Literal["none", "random_movement", "all_movement"] = "none",
    ) -> None:
        """Saves a home position for when the entity is spawned. This component allows entities like bees to remember and return to a specific location such as a hive or nest.

        Parameters:
            home_block_list (list[MinecraftBlockDescriptor | Identifier], optional): Optional list of blocks that can be considered a valid home. Defaults to None.
            restriction_radius (int, optional): Optional radius that the entity will be restricted to in relation to its home. Defaults to 0.
            restriction_type (Literal['none', 'random_movement', 'all_movement'], optional): Defines how the entity will be restricted to its home position. Defaults to "none".

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_home
        """
        super().__init__("home")
        if home_block_list is not None:
            self._add_field(
                "home_block_list", [str(block) for block in home_block_list]
            )
        if restriction_radius != 0:
            self._add_field("restriction_radius", max(0, restriction_radius))
        if restriction_type != "none":
            self._enforce_version(ENTITY_SERVER_VERSION, "1.21.40")
            self._add_field("restriction_type", restriction_type)


class EntityInsomnia(Component):
    _identifier = "minecraft:insomnia"

    def __init__(self, days_until_insomnia: float = 3) -> None:
        """Adds a timer since last rested to see if phantoms should spawn.

        Parameters:
            days_until_insomnia (float, optional): Number of days the mob has to stay up until the insomnia effect begins. Defaults to 3.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_insomnia
        """
        super().__init__("insomnia")
        if days_until_insomnia != 3:
            self._add_field("days_until_insomnia", max(0, days_until_insomnia))


class EntityLeashableTo(Component):
    _identifier = "minecraft:leashable_to"

    def __init__(self, can_retrieve_from: bool = False) -> None:
        """Allows players to leash entities to this entity, retrieve entities already leashed to it, or free them using shears. For the last interaction to work, the leashed entities must have "can_be_cut" set to true in their "minecraft:leashable" component.

        Parameters:
            can_retrieve_from (bool, optional): Allows players to retrieve entities that are leashed to this entity. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_leashable_to
        """
        super().__init__("leashable_to")
        if can_retrieve_from:
            self._add_field("can_retrieve_from", can_retrieve_from)


class EntityMobEffectImmunity(Component):
    _identifier = "minecraft:mob_effect_immunity"

    def __init__(
        self,
        mob_effects: list[MinecraftEffects | str] = None,
    ) -> None:
        """Entities with this component will have an immunity to the provided mob effects.

        Parameters:
            mob_effects (list[MinecraftEffects | str], optional): List of names of effects the entity is immune to. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_mob_effect_immunity
        """
        super().__init__("mob_effect_immunity")
        if mob_effects is not None:
            self._add_field("mob_effects", mob_effects)


class EntityPushable(Component):
    _identifier = "minecraft:pushable"

    def __init__(
        self,
        is_pushable: bool = True,
        is_pushable_by_piston: bool = True,
    ) -> None:
        """Defines what can push an entity between other entities and pistons.

        Parameters:
            is_pushable (bool, optional): Whether the entity can be pushed by other entities. Defaults to True.
            is_pushable_by_piston (bool, optional): Whether the entity can be pushed by pistons safely. Defaults to True.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_pushable
        """
        super().__init__("pushable")
        raise NotImplementedError(
            "The 'EntityPushable' component was removed in Minecraft version 1.26.10 and replaced with 'EntityPushableByEntity' and 'EntityPushableByBlock'. Please use those components instead."
        )


class EntityReflectProjectiles(Component):
    _identifier = "minecraft:reflect_projectiles"

    def __init__(
        self,
        azimuth_angle: Molang | str = None,
        elevation_angle: Molang | str = None,
        reflected_projectiles: list[MinecraftEntityDescriptor | Identifier] = None,
        reflection_scale: Molang | str = None,
        reflection_sound: str = "reflect",
    ) -> None:
        """[EXPERIMENTAL] Allows an entity to reflect projectiles.

        Parameters:
            azimuth_angle (Molang | str, optional): [EXPERIMENTAL] A Molang expression defining the angle in degrees to add to the projectile's y axis rotation. Defaults to None.
            elevation_angle (Molang | str, optional): [EXPERIMENTAL] A Molang expression defining the angle in degrees to add to the projectile's x axis rotation. Defaults to None.
            reflected_projectiles (list[MinecraftEntityDescriptor | Identifier], optional): [EXPERIMENTAL] An array of strings defining the types of projectiles that are reflected when they hit the entity. Defaults to None.
            reflection_scale (Molang | str, optional): [EXPERIMENTAL] A Molang expression defining the velocity scaling of the reflected projectile. Values below 1 decrease the projectile's velocity, and values above 1 increase it. Defaults to None.
            reflection_sound (str, optional): [EXPERIMENTAL] A string defining the name of the sound event to be played when a projectile is reflected. "reflect" unless specified. Defaults to "reflect".

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_reflect_projectiles
        """
        if not CONFIG._EXPERIMENTAL:
            raise NotImplementedError(
                "The 'EntityReflectProjectiles' component is experimental and requires the experimental flag to be enabled in anvilconfig.json."
            )

        super().__init__("reflect_projectiles")
        if azimuth_angle is not None:
            self._add_field("azimuth_angle", azimuth_angle)
        if elevation_angle is not None:
            self._add_field("elevation_angle", elevation_angle)
        if reflected_projectiles is not None:
            self._add_field("reflected_projectiles", reflected_projectiles)
        if reflection_scale is not None:
            self._add_field("reflection_scale", reflection_scale)
        if reflection_sound != "reflect":
            self._add_field("reflection_sound", reflection_sound)


class EntityStrength(Component):
    _identifier = "minecraft:strength"

    def __init__(self, value: int = 1, max: int = 5) -> None:
        """Defines the entity's strength to carry items.

        Parameters:
            value (int, optional): The initial value of the strength. Defaults to 1.
            max (int, optional): The maximum strength of this entity. Defaults to 5.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_strength
        """
        super().__init__("strength")
        if value != 1:
            self._add_field("value", 0 if value < 0 else value)
        if max != 5:
            self._add_field("max", 0 if max < 0 else max)


class EntityTamemount(Component):
    _identifier = "minecraft:tamemount"

    def __init__(
        self,
        attempt_temper_mod: int = 5,
        feed_text: str = None,
        max_temper: int = 100,
        min_temper: int = 0,
        ride_text: str = None,
    ) -> None:
        """Allows the Entity to be tamed by mounting it.

        Parameters:
            attempt_temper_mod (int, optional): The amount the entity's temper will increase when mounted. Defaults to 5.
            feed_text (str, optional): The text that shows in the feeding interact button. Defaults to None.
            max_temper (int, optional): The maximum value for the entity's random starting temper. Defaults to 100.
            min_temper (int, optional): The minimum value for the entity's random starting temper. Defaults to 0.
            ride_text (str, optional): The text that shows in the riding interact button. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_tamemount
        """
        super().__init__("tamemount")
        self._add_field("feed_items", [])
        self._add_field("auto_reject_items", [])
        if attempt_temper_mod != 5:
            self._add_field("attempt_temper_mod", attempt_temper_mod)
        if feed_text is not None:
            self._add_field("feed_text", feed_text)
        if max_temper != 100:
            self._add_field("max_temper", max(0, max_temper))
        if min_temper != 0:
            self._add_field("min_temper", max(0, min_temper))
        if ride_text is not None:
            formatted = AnvilTranslator().format_key(ride_text)
            key = f"action.interact.mount.{CONFIG.NAMESPACE}:{CONFIG.PROJECT_NAME}.{formatted}"
            AnvilTranslator().add_localization_entry(key, ride_text)
            self._add_field("ride_text", key)

    def add_feed_item(
        self,
        items: list[MinecraftItemDescriptor | Identifier],
        temper_mod: int = 0,
    ):
        for item in items:
            self._component["feed_items"].append(
                {"item": str(item), "temper_mod": temper_mod}
            )
        return self

    def add_auto_reject_item(self, items: list[MinecraftItemDescriptor | Identifier]):
        for item in items:
            self._component["auto_reject_items"].append({"item": str(item)})
        return self

    def tame_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("tame_event", {"event": event, "target": target.value})
        return self


class EntityTradeTable(Component):
    _identifier = "minecraft:trade_table"

    def __init__(
        self,
        table: TradeTable | str,
        convert_trades_economy: bool = False,
        display_name: str = None,
        new_screen: bool = False,
        persist_trades: bool = False,
    ) -> None:
        """Defines this entity's ability to trade with players.

        Parameters:
            table (TradeTable | str): File path relative to the behavior pack root for this entity's trades.
            convert_trades_economy (bool, optional): Determines when the mob transforms, if the trades should be converted when the new mob has a economy_trade_table. Defaults to False.
            display_name (str, optional): Name to be displayed while trading with this entity. Defaults to None.
            new_screen (bool, optional): Used to determine if trading with entity opens the new trade screen. Defaults to False.
            persist_trades (bool, optional): Determines if the trades should persist when the mob transforms. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trade_table
        """
        super().__init__("trade_table")
        self._add_field(
            "table", table.table_path if isinstance(table, TradeTable) else table
        )
        if convert_trades_economy:
            self._add_field("convert_trades_economy", convert_trades_economy)
        if display_name is not None:
            self._add_field("display_name", display_name)
        if new_screen:
            self._add_field("new_screen", new_screen)
        if persist_trades:
            self._add_field("persist_trades", persist_trades)


class EntityBalloonable(Component):
    _identifier = "minecraft:balloonable"

    def __init__(
        self,
        mass: float = 1.0,
        max_distance: float = 10.0,
        soft_distance: float = 2.0,
    ) -> None:
        """Allows this entity to have a balloon attached and defines the conditions and events for this entity when is ballooned.

        Parameters:
            mass (float, optional): Mass that this entity will have when computing balloon pull forces. Defaults to 1.0.
            max_distance (float, optional): Distance in blocks at which the balloon breaks. Defaults to 10.0.
            soft_distance (float, optional): Distance in blocks at which the 'spring' effect that lifts it. Defaults to 2.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_balloonable
        """
        super().__init__("balloonable")
        if mass != 1.0:
            self._add_field("mass", max(0.0, mass))
        if max_distance != 10.0:
            self._add_field("max_distance", max(0.0, max_distance))
        if soft_distance != 2.0:
            self._add_field("soft_distance", max(0.0, soft_distance))

    def on_balloon(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_balloon", {"event": event, "target": target.value})
        return self

    def on_unballoon(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_unballoon", {"event": event, "target": target.value})
        return self


class EntityBarter(Component):
    _identifier = "minecraft:barter"

    def __init__(
        self,
        barter_table: LootTable | str,
        cooldown_after_being_attacked: tuple[int, int] | int = 0,
    ) -> None:
        """Enables the component to drop an item as a barter exchange.

        Parameters:
            barter_table (LootTable | str): Loot table that's used to drop a random item.
            cooldown_after_being_attacked (tuple[int, int] | int, optional): Duration, in seconds, for which mob won't barter items if it was hurt. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_barter
        """
        super().__init__("barter")
        self._add_field(
            "barter_table",
            (
                barter_table.table_path
                if isinstance(barter_table, LootTable)
                else barter_table
            ),
        )
        if isinstance(cooldown_after_being_attacked, (tuple, list)):
            self._add_field(
                "cooldown_after_being_attacked",
                AnvilFormatter.min_max_dict(
                    cooldown_after_being_attacked,
                    "cooldown_after_being_attacked",
                    value_types=(int,),
                    clamp_min=0,
                ),
            )
        elif cooldown_after_being_attacked != 0:
            self._add_field(
                "cooldown_after_being_attacked",
                max(0, cooldown_after_being_attacked),
            )


class EntityBoostable(Component):
    _identifier = "minecraft:boostable"

    def __init__(
        self,
        duration: Seconds = 3.0,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Defines the conditions and behavior of a rideable entity's boost.

        Parameters:
            duration (Seconds, optional): Time in seconds for the boost. Defaults to 3.0.
            speed_multiplier (float, optional): Factor by which the entity's normal speed increases. E.g. 2.0 means go twice as fast. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_boostable
        """
        super().__init__("boostable")
        self._add_field("boost_items", [])
        if duration != 3.0:
            self._add_field("duration", max(0.0, duration))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))

    def add_boost_item(
        self,
        item: MinecraftItemDescriptor | Identifier,
        damage: int = None,
        replace_item: MinecraftItemDescriptor | Identifier = None,
    ):
        boost_item = {"item": str(item)}
        if damage is not None:
            boost_item["damage"] = damage
        if replace_item is not None:
            boost_item["replace_item"] = str(replace_item)
        self._component["boost_items"].append(boost_item)
        return self


class EntityBreakBlocks(Component):
    _identifier = "minecraft:break_blocks"

    def __init__(self) -> None:
        """Specifies the blocks that the entity can break as it moves around.

        This component has no configurable constructor properties. Use add_block to append breakable block identifiers.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_break_blocks
        """
        super().__init__("break_blocks")
        self._add_field("breakable_blocks", [])

    def add_block(self, *blocks: MinecraftBlockDescriptor | Identifier):
        self._component["breakable_blocks"].extend(str(block) for block in blocks)
        return self


class EntityDash(Component):
    _identifier = "minecraft:dash"

    def __init__(
        self,
        cooldown_time: Seconds = 1.0,
        horizontal_momentum: float = 1.0,
        vertical_momentum: float = 1.0,
    ) -> None:
        """Ability for a rideable entity to dash.

        Parameters:
            cooldown_time (Seconds, optional): The dash cooldown in seconds. Default value is 1.000000. Defaults to 1.0.
            horizontal_momentum (float, optional): Horizontal momentum of the dash. Defaults to 1.0.
            vertical_momentum (float, optional): Vertical momentum of the dash. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_dash
        """
        super().__init__("dash")
        if cooldown_time != 1.0:
            self._add_field("cooldown_time", max(0.0, cooldown_time))
        if horizontal_momentum != 1.0:
            self._add_field("horizontal_momentum", horizontal_momentum)
        if vertical_momentum != 1.0:
            self._add_field("vertical_momentum", vertical_momentum)


class EntityDryingOutTimer(Component):
    _identifier = "minecraft:drying_out_timer"

    def __init__(
        self,
        total_time: Seconds = 0.0,
        water_bottle_refill_time: Seconds = 0.0,
    ) -> None:
        """Adds a timer for drying out that will count down and fire 'dried_out_event' or will stop as soon as the entity will get under rain or water and fire 'stopped_drying_out_event'.

        Parameters:
            total_time (Seconds, optional): Amount of time in seconds to dry out fully. Defaults to 0.0.
            water_bottle_refill_time (Seconds, optional): Optional amount of additional time in seconds given by using splash water bottle on entity. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_drying_out_timer
        """
        super().__init__("drying_out_timer")
        if total_time != 0.0:
            self._add_field("total_time", max(0.0, total_time))
        if water_bottle_refill_time != 0.0:
            self._add_field(
                "water_bottle_refill_time", max(0.0, water_bottle_refill_time)
            )

    def dried_out_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("dried_out_event", {"event": event, "target": target.value})
        return self

    def recover_after_dried_out_event(
        self, event: str, target: FilterSubject = FilterSubject.Self
    ):
        self._add_field(
            "recover_after_dried_out_event",
            {"event": event, "target": target.value},
        )
        return self

    def stopped_drying_out_event(
        self, event: str, target: FilterSubject = FilterSubject.Self
    ):
        self._add_field(
            "stopped_drying_out_event",
            {"event": event, "target": target.value},
        )
        return self


class EntityFlocking(Component):
    _identifier = "minecraft:flocking"

    def __init__(
        self,
        block_distance: float = 0.0,
        block_weight: float = 0.0,
        breach_influence: float = 0.0,
        cohesion_threshold: float = 1.0,
        cohesion_weight: float = 1.0,
        goal_weight: float = 0.0,
        high_flock_limit: int = 0,
        in_water: bool = False,
        influence_radius: float = 0.0,
        inner_cohesion_threshold: float = 0.0,
        loner_chance: float = 0.0,
        low_flock_limit: int = 0,
        match_variants: bool = False,
        max_height: float = 0.0,
        min_height: float = 0.0,
        separation_threshold: float = 2.0,
        separation_weight: float = 1.0,
        use_center_of_mass: bool = False,
    ) -> None:
        """Allows entities to flock in groups in water or not.

        Parameters:
            block_distance (float, optional): The amount of blocks away the entity will look at to push away from. Defaults to 0.0.
            block_weight (float, optional): The weight of the push back away from blocks. Defaults to 0.0.
            breach_influence (float, optional): The amount of push back given to a flocker that breaches out of the water. Defaults to 0.0.
            cohesion_threshold (float, optional): The threshold in which to start applying cohesion. Defaults to 1.0.
            cohesion_weight (float, optional): The weight applied for the cohesion steering of the flock. Defaults to 1.0.
            goal_weight (float, optional): The weight on which to apply on the goal output. Defaults to 0.0.
            high_flock_limit (int, optional): Determines the high bound amount of entities that can be allowed in the flock. Defaults to 0.
            in_water (bool, optional): Tells the Flocking Component if the entity exists in water. Defaults to False.
            influence_radius (float, optional): The area around the entity that allows others to be added to the flock. Defaults to 0.0.
            inner_cohesion_threshold (float, optional): The distance in which the flocker will stop applying cohesion. Defaults to 0.0.
            loner_chance (float, optional): The percentage chance between 0-1 that a fish will spawn and not want to join flocks. Invalid values will be capped at the end points. Defaults to 0.0.
            low_flock_limit (int, optional): Determines the low bound amount of entities that can be allowed in the flock. Defaults to 0.
            match_variants (bool, optional): Tells the flockers that they can only match similar entities that also match the variant, mark variants, and color data of the other potential flockers. Defaults to False.
            max_height (float, optional): The max height allowable in the air or water. Defaults to 0.0.
            min_height (float, optional): The min height allowable in the air or water. Defaults to 0.0.
            separation_threshold (float, optional): The distance that is determined to be to close to another flocking and to start applying separation. Defaults to 2.0.
            separation_weight (float, optional): The weight applied to the separation of the flock. Defaults to 1.0.
            use_center_of_mass (bool, optional): Tells the flockers that they will follow flocks based on the center of mass. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_flocking
        """
        super().__init__("flocking")
        if block_distance != 0.0:
            self._add_field("block_distance", block_distance)
        if block_weight != 0.0:
            self._add_field("block_weight", block_weight)
        if breach_influence != 0.0:
            self._add_field("breach_influence", breach_influence)
        if cohesion_threshold != 1.0:
            self._add_field("cohesion_threshold", cohesion_threshold)
        if cohesion_weight != 1.0:
            self._add_field("cohesion_weight", cohesion_weight)
        if goal_weight != 0.0:
            self._add_field("goal_weight", goal_weight)
        if high_flock_limit != 0:
            self._add_field("high_flock_limit", max(0, high_flock_limit))
        if in_water:
            self._add_field("in_water", in_water)
        if influence_radius != 0.0:
            self._add_field("influence_radius", influence_radius)
        if inner_cohesion_threshold != 0.0:
            self._add_field("innner_cohesion_threshold", inner_cohesion_threshold)
        if loner_chance != 0.0:
            self._add_field("loner_chance", clamp(loner_chance, 0.0, 1.0))
        if low_flock_limit != 0:
            self._add_field("low_flock_limit", max(0, low_flock_limit))
        if match_variants:
            self._add_field("match_variants", match_variants)
        if max_height != 0.0:
            self._add_field("max_height", max_height)
        if min_height != 0.0:
            self._add_field("min_height", min_height)
        if separation_threshold != 2.0:
            self._add_field("separation_threshold", separation_threshold)
        if separation_weight != 1.0:
            self._add_field("separation_weight", separation_weight)
        if use_center_of_mass:
            self._add_field("use_center_of_mass", use_center_of_mass)


class EntityGenetics(Component):
    _identifier = "minecraft:genetics"

    def __init__(self, mutation_rate: float = 0.03125) -> None:
        """Defines the way a mob's genes and alleles are passed on to its offspring, and how those traits manifest in the child. Compatible parent genes are crossed together, the alleles are handed down from the parents to the child, and any matching genetic variants fire off JSON events to modify the child and express the traits.

        Parameters:
            mutation_rate (float, optional): If this value is non-negative, overrides the chance for this gene that an allele will be replaced with a random one instead of the parent's allele during birth. Defaults to 0.03125.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_genetics
        """
        super().__init__("genetics")
        self._add_field("genes", [])
        if mutation_rate != 0.03125:
            self._add_field("mutation_rate", clamp(mutation_rate, 0.0, 1.0))

    def _get_gene(self, gene_name: str | None):
        if not self._component["genes"]:
            raise ValueError("at least one gene must be added before adding variants")

        if gene_name is None:
            return self._component["genes"][-1]

        for gene in self._component["genes"]:
            if gene.get("name") == gene_name:
                return gene

        raise ValueError(f"gene '{gene_name}' was not found")

    def add_gene(
        self,
        name: str,
        allele_range: int | tuple[int, int],
        mutation_rate: float = -1.0,
        use_simplified_breeding: bool = False,
    ):

        range = AnvilFormatter.min_max_dict(
            allele_range, "allele_range", value_types=(int,), clamp_min=0
        )
        range["range_min"] = range.pop("min")
        range["range_max"] = range.pop("max")

        gene = {
            "name": name,
            "allele_range": range,
            "genetic_variants": [],
        }
        if mutation_rate != -1.0:
            gene["mutation_rate"] = clamp(mutation_rate, 0.0, 1.0)
        if use_simplified_breeding:
            gene["use_simplified_breeding"] = use_simplified_breeding
        self._component["genes"].append(gene)
        return self

    def add_gene_variant(
        self,
        birth_event: str,
        target: FilterSubject = FilterSubject.Self,
        gene_name: str = None,
        *,
        both_allele: int | tuple[int, int] = None,
        either_allele: int | tuple[int, int] = None,
        hidden_allele: int | tuple[int, int] = None,
        main_allele: int | tuple[int, int] = None,
    ):
        if all(
            value is None
            for value in (both_allele, either_allele, hidden_allele, main_allele)
        ):
            raise ValueError("a gene variant must define at least one allele matcher")

        variant = {"birth_event": {"event": birth_event, "target": target.value}}
        if both_allele is not None:
            variant["both_allele"] = self._serialize_allele_range(both_allele)
        if either_allele is not None:
            variant["either_allele"] = self._serialize_allele_range(either_allele)
        if hidden_allele is not None:
            variant["hidden_allele"] = self._serialize_allele_range(hidden_allele)
        if main_allele is not None:
            variant["main_allele"] = self._serialize_allele_range(main_allele)

        self._get_gene(gene_name)["genetic_variants"].append(variant)
        return self


class EntityGiveable(Component):
    _identifier = "minecraft:giveable"

    def __init__(self, cooldown: Seconds = 0.0) -> None:
        """Defines sets of items that can be used to trigger events when used on this entity. The item will also be taken and placed in the entity's inventory.

        Parameters:
            cooldown (Seconds, optional): An optional cool down in seconds to prevent spamming interactions. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_giveable
        """
        super().__init__("giveable")
        self._add_field("items", [])
        if cooldown != 0.0:
            self._add_field("cooldown", max(0.0, cooldown))

    def add_item(self, *items: MinecraftItemDescriptor | Identifier):
        self._component["items"].extend(str(item) for item in items)
        return self

    def on_give(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_give", {"event": event, "target": target.value})
        return self


class EntityGrowsCrop(Component):
    _identifier = "minecraft:grows_crop"

    def __init__(self, chance: float = 0.0, charges: int = 10) -> None:
        """Could increase crop growth when entity walks over crop.

        Parameters:
            chance (float, optional): Value between 0-1. Chance of success per tick. Defaults to 0.0.
            charges (int, optional): Number of charges. Defaults to 10.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_grows_crop
        """
        super().__init__("grows_crop")
        if chance != 0.0:
            self._add_field("chance", clamp(chance, 0.0, 1.0))
        if charges != 10:
            self._add_field("charges", max(0, charges))


class EntityItemControllable(Component):
    _identifier = "minecraft:item_controllable"

    def __init__(self) -> None:
        """Defines what items can be used to control this entity while ridden.

        This component has no configurable constructor properties. Use add_control_item to append valid control items.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_item_controllable
        """
        super().__init__("item_controllable")
        self._add_field("control_items", [])

    def add_control_items(self, items: list[MinecraftItemDescriptor | Identifier]):
        self._component["control_items"].extend(str(item) for item in items)
        return self


class EntityManagedWanderingTrader(Component):
    _identifier = "minecraft:managed_wandering_trader"

    def __init__(self) -> None:
        """Manages the entity's ability to trade.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_managed_wandering_trader
        """
        super().__init__("managed_wandering_trader")


class EntityPeek(Component):
    _identifier = "minecraft:peek"

    def __init__(self) -> None:
        """Defines the entity's 'peek' behavior, defining the events that should be called during it.

        This component has no configurable constructor properties. Use on_close, on_open, and on_target_open to define the event triggers.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_peek
        """
        super().__init__("peek")

    def on_close(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_close", {"event": event, "target": target.value})
        return self

    def on_open(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_open", {"event": event, "target": target.value})
        return self

    def on_target_open(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_target_open", {"event": event, "target": target.value})
        return self


class EntityPlayerExhaustion(Component):
    _identifier = "minecraft:player.exhaustion"

    def __init__(self, value: float = 0.0, max: float = 20.0) -> None:
        """Defines the player's exhaustion level.

        Parameters:
            value (float, optional): The initial value of a player's exhaustion level. Defaults to 0.0.
            max (float, optional): A maximum value for a player's exhaustion. Defaults to 20.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.exhaustion
        """
        super().__init__("player.exhaustion")
        if max != 20.0:
            self._add_field("max", 0.0 if max < 0.0 else max)
        if value != 0.0:
            self._add_field("value", 0.0 if value < 0.0 else value)


class EntityPlayerExperience(Component):
    _identifier = "minecraft:player.experience"

    def __init__(self, value: float = 0.0, max: float = 1.0) -> None:
        """Defines how much experience each player action should take.

        Parameters:
            value (float, optional): The initial value of the player experience. Defaults to 0.0.
            max (float, optional): The maximum player experience of this entity. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.experience
        """
        super().__init__("player.experience")
        if max != 1.0:
            self._add_field("max", 0.0 if max < 0.0 else max)
        if value != 0.0:
            self._add_field("value", 0.0 if value < 0.0 else value)


class EntityPlayerLevel(Component):
    _identifier = "minecraft:player.level"

    def __init__(self, value: int = 0, max: int = 24791) -> None:
        """Defines the player's level.

        Parameters:
            value (int, optional): The initial value of the player level. Defaults to 0.
            max (int, optional): The maximum player level value of the entity. Defaults to 24791.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.level
        """
        super().__init__("player.level")
        if max != 24791:
            self._add_field("max", 0 if max < 0 else max)
        if value != 0:
            self._add_field("value", 0 if value < 0 else value)


class EntityPlayerSaturation(Component):
    _identifier = "minecraft:player.saturation"

    def __init__(self, value: float = 5.0, max: float = 20.0) -> None:
        """Defines the player's need for food.

        Parameters:
            value (float, optional): The initial value of player saturation. Defaults to 5.0.
            max (float, optional): The maximum player saturation value. Defaults to 20.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_player.saturation
        """
        super().__init__("player.saturation")
        if max != 20.0:
            self._add_field("max", 0.0 if max < 0.0 else max)
        if value != 5.0:
            self._add_field("value", 0.0 if value < 0.0 else value)


class EntityRaidTrigger(Component):
    _identifier = "minecraft:raid_trigger"

    def __init__(self) -> None:
        """Attempts to trigger a raid at the entity's location.

        This component has no configurable constructor properties. Use triggered_event to define the raid event payload.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_raid_trigger
        """
        super().__init__("raid_trigger")

    def triggered_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("triggered_event", {"event": event, "target": target.value})
        return self


class EntityRailMovement(Component):
    _identifier = "minecraft:rail_movement"

    def __init__(self, max_speed: float = 0.4) -> None:
        """Defines the entity's movement on the rails. An entity with this component is only allowed to move on the rail.

        Parameters:
            max_speed (float, optional): Maximum speed that this entity will move at when on the rail. Defaults to 0.4.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rail_movement
        """
        super().__init__("rail_movement")
        if max_speed != 0.4:
            self._add_field("max_speed", max(0.0, max_speed))


class EntityRailSensor(Component):
    _identifier = "minecraft:rail_sensor"

    def __init__(
        self,
        check_block_types: bool = False,
        eject_on_activate: bool = True,
        eject_on_deactivate: bool = False,
        tick_command_block_on_activate: bool = True,
        tick_command_block_on_deactivate: bool = False,
    ) -> None:
        """Enables minecart-type entities to detect powered rails and respond to activation state changes. Triggers events when the entity passes over activated or deactivated rails, enabling custom minecart behaviors like launching at boosted speed, stopping at braking rails, or triggering special effects at detector rails.

        Parameters:
            check_block_types (bool, optional): If true, on tick this entity will trigger its on_deactivate behavior. Defaults to False.
            eject_on_activate (bool, optional): If true, this entity will eject all of its riders when it passes over an activated rail. Defaults to True.
            eject_on_deactivate (bool, optional): If true, this entity will eject all of its riders when it passes over a deactivated rail. Defaults to False.
            tick_command_block_on_activate (bool, optional): If true, command blocks will start ticking when passing over an activated rail. Defaults to True.
            tick_command_block_on_deactivate (bool, optional): If false, command blocks will stop ticking when passing over a deactivated rail. Defaults to False.

        Note:
            Use on_activate and on_deactivate to define the event payloads.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_rail_sensor
        """
        super().__init__("rail_sensor")
        if check_block_types:
            self._add_field("check_block_types", check_block_types)
        if eject_on_activate is not True:
            self._add_field("eject_on_activate", eject_on_activate)
        if eject_on_deactivate:
            self._add_field("eject_on_deactivate", eject_on_deactivate)
        if tick_command_block_on_activate is not True:
            self._add_field(
                "tick_command_block_on_activate", tick_command_block_on_activate
            )
        if tick_command_block_on_deactivate:
            self._add_field(
                "tick_command_block_on_deactivate", tick_command_block_on_deactivate
            )

    def on_activate(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_activate", {"event": event, "target": target.value})
        return self

    def on_deactivate(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_deactivate", {"event": event, "target": target.value})
        return self


class EntityRavagerBlocked(Component):
    _identifier = "minecraft:ravager_blocked"

    def __init__(self, knockback_strength: float = 3.0) -> None:
        """Defines the ravager's response to their melee attack being blocked.

        Parameters:
            knockback_strength (float, optional): The strength with which blocking entities should be knocked back. Defaults to 3.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_ravager_blocked
        """
        super().__init__("ravager_blocked")
        self._add_field("reaction_choices", [])
        if knockback_strength != 3.0:
            self._add_field("knockback_strength", max(0.0, knockback_strength))

    def add_reaction_choice(self, choice: str, weight: float = 1.0):
        self._component["reaction_choices"].append({"choice": choice, "weight": weight})
        return self


class EntitySuspectTracking(Component):
    _identifier = "minecraft:suspect_tracking"

    def __init__(self) -> None:
        """Allows this entity to remember suspicious locations.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_suspect_tracking
        """
        super().__init__("suspect_tracking")


class EntityTeleport(Component):
    _identifier = "minecraft:teleport"

    def __init__(
        self,
        dark_teleport_chance: float = 0.01,
        light_teleport_chance: float = 0.01,
        max_random_teleport_time: Seconds = 20.0,
        min_random_teleport_time: Seconds = 0.0,
        random_teleport_cube: tuple[float, float, float] = (32, 16, 32),
        random_teleports: bool = True,
        target_distance: float = 16.0,
        target_teleport_chance: float = 1.0,
    ) -> None:
        """Defines an entity's teleporting behavior.

        Parameters:
            dark_teleport_chance (float, optional): Modifies the chance that the entity will teleport if the entity is in darkness. Defaults to 0.01.
            light_teleport_chance (float, optional): Modifies the chance that the entity will teleport if the entity is in daylight. Defaults to 0.01.
            max_random_teleport_time (Seconds, optional): Maximum amount of time in seconds between random teleports. Defaults to 20.0.
            min_random_teleport_time (Seconds, optional): Minimum amount of time in seconds between random teleports. Defaults to 0.0.
            random_teleport_cube (tuple[float, float, float], optional): Entity will teleport to a random position within the area defined by this cube. Defaults to (32, 16, 32).
            random_teleports (bool, optional): If true, the entity will teleport randomly. Defaults to True.
            target_distance (float, optional): Maximum distance the entity will teleport when chasing a target. Defaults to 16.0.
            target_teleport_chance (float, optional): The chance that the entity will teleport between 0.0 and 1.0. 1.0 means 100%. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_teleport
        """
        super().__init__("teleport")
        if dark_teleport_chance != 0.01:
            self._add_field(
                "dark_teleport_chance", clamp(dark_teleport_chance, 0.0, 1.0)
            )
        if light_teleport_chance != 0.01:
            self._add_field(
                "light_teleport_chance", clamp(light_teleport_chance, 0.0, 1.0)
            )
        if max_random_teleport_time != 20.0:
            self._add_field(
                "max_random_teleport_time", max(0.0, max_random_teleport_time)
            )
        if min_random_teleport_time != 0.0:
            self._add_field(
                "min_random_teleport_time", max(0.0, min_random_teleport_time)
            )
        if random_teleport_cube != (32, 16, 32):
            self._add_field("random_teleport_cube", list(random_teleport_cube))
        if random_teleports is not True:
            self._add_field("random_teleports", random_teleports)
        if target_distance != 16.0:
            self._add_field("target_distance", target_distance)
        if target_teleport_chance != 1.0:
            self._add_field(
                "target_teleport_chance", clamp(target_teleport_chance, 0.0, 1.0)
            )


class EntityTrail(Component):
    _identifier = "minecraft:trail"

    def __init__(
        self,
        block_type: MinecraftBlockDescriptor | Identifier = MinecraftBlockTypes.Air(),
        spawn_filter: Filter = None,
        spawn_offset: tuple[float, float, float] = (0, 0, 0),
    ) -> None:
        """Causes an entity to leave a trail of blocks as it moves about the world.

        Parameters:
            block_type (MinecraftBlockDescriptor | Identifier, optional): The type of block you wish to be spawned by the entity as it move about the world. Solid blocks may not be spawned at an offset of (0,0,0). Defaults to air.
            spawn_filter (Filter, optional): One or more conditions that must be met in order to cause the chosen block type to spawn. Defaults to None.
            spawn_offset (tuple[float, float, float], optional): The distance from the entities current position to spawn the block. Defaults to (0, 0, 0).

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trail
        """
        super().__init__("trail")
        if str(block_type) != str(MinecraftBlockTypes.Air()):
            self._add_field("block_type", str(block_type))
        if spawn_filter is not None:
            self._add_field("spawn_filter", spawn_filter)
        if spawn_offset != (0, 0, 0):
            self._add_field("spawn_offset", list(spawn_offset))


class EntityTrust(Component):
    _identifier = "minecraft:trust"

    def __init__(self) -> None:
        """Allows this entity to trust multiple players.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trust
        """
        super().__init__("trust")


class EntityTrusting(Component):
    _identifier = "minecraft:trusting"

    def __init__(self, probability: float = 1.0) -> None:
        """Defines the rules for a mob to trust players.

        Parameters:
            probability (float, optional): The chance of the entity trusting with each item use between 0.0 and 1.0, where 1.0 is 100%. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_trusting
        """
        super().__init__("trusting")
        self._add_field("trust_items", [])
        if probability != 1.0:
            self._add_field("probability", clamp(probability, 0.0, 1.0))

    def add_trust_items(self, items: list[MinecraftItemDescriptor | Identifier]):
        self._component["trust_items"].extend(str(item) for item in items)
        return self

    def trust_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("trust_event", {"event": event, "target": target.value})
        return self


class EntityVibrationListener(Component):
    _identifier = "minecraft:vibration_listener"

    def __init__(self) -> None:
        """Allows the entity to listen to vibration events. This is a largely-internal component, that is only supported on the Warden and Allay mobs.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitycomponents/minecraftcomponent_vibration_listener
        """
        super().__init__("vibration_listener")


# AI Goals ==========================================================================


class EntityAINearestAttackableTarget(AIGoal):
    _identifier = "minecraft:behavior.nearest_attackable_target"

    def __init__(
        self,
        attack_interval: tuple[float, float] | float = 0,
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
        target_acquisition_probability: float = 1.0,
    ) -> None:
        """Allows an entity to attack the closest target within a given subset of specific target types.

        Parameters:
            attack_interval (tuple[float, float] | float, optional): String. Defaults to 0.
            attack_interval_min (int, optional): String. Defaults to 0.
            attack_owner (bool, optional): If true, this entity can attack its owner. Defaults to False.
            must_reach (bool, optional): If true, this entity requires a path to the target. Defaults to False.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            persist_time (float, optional): Time (in seconds) this entity can continue attacking the target after the target is no longer valid. Defaults to 0.0.
            reselect_targets (bool, optional): Allows the attacking entity to update the nearest target, otherwise a target is only reselected after each "scan_interval" or "attack_interval". Defaults to False.
            scan_interval (int, optional): If "attack_interval" is 0 or isn't declared, then between attacks: scanning for a new target occurs every amount of ticks equal to "scan_interval", minimum value is 1. Defaults to 10.
            set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Defaults to False.
            target_invisible_multiplier (float, optional): Multiplied with the target's armor coverage percentage to modify "max_dist" when detecting an invisible target. Defaults to 0.7.
            target_search_height (float, optional): Maximum vertical target-search distance, if it's greater than the target type's "max_dist". A negative value defaults to "entity_types" greatest "max_dist". Value must be >= -1. Defaults to -0.1.
            target_sneak_visibility_multiplier (float, optional): Multiplied with the target type's "max_dist" when trying to detect a sneaking target. Defaults to 0.8.
            within_radius (float, optional): Maximum distance this entity can be from the target when following it, otherwise the target becomes invalid. This value is only used if the entity doesn't declare "minecraft:follow_range". Defaults to 0.0.
            target_acquisition_probability (float, optional): Probability (0.0 to 1.0) that this entity will accept a found target. Checked each time a valid target is found during scanning. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nearest_attackable_target
        """
        super().__init__("behavior.nearest_attackable_target")
        self._add_field("entity_types", [])

        if attack_interval != 0:
            self._add_field(
                "attack_interval",
                AnvilFormatter.min_max_dict(attack_interval, "attack_interval"),
            )

        if attack_interval_min != 0:
            self._add_field("attack_interval_min", attack_interval_min)
        if attack_owner:
            self._add_field("attack_owner", attack_owner)
        if must_reach:
            self._add_field("must_reach", must_reach)
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if persist_time != 0.0:
            self._add_field("persist_time", persist_time)
        # if reevaluate_description: self._add_field("reevaluate_description", reevaluate_description)
        if reselect_targets:
            self._add_field("reselect_targets", reselect_targets)
        if scan_interval != 10:
            self._add_field("scan_interval", scan_interval)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if target_invisible_multiplier != 0.7:
            self._add_field("target_invisible_multiplier", target_invisible_multiplier)
        if target_search_height != -0.1:
            self._add_field("target_search_height", target_search_height)
        if target_sneak_visibility_multiplier != 0.8:
            self._add_field(
                "target_sneak_visibility_multiplier", target_sneak_visibility_multiplier
            )
        if within_radius != 0.0:
            self._add_field("within_radius", within_radius)
        if target_acquisition_probability != 1.0:
            self._add_field(
                "target_acquisition_probability", target_acquisition_probability
            )

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
                "must_see_forget_duration": (
                    must_see_forget_duration if must_see_forget_duration != 3.0 else {}
                ),
                "sprint_speed_multiplier": (
                    sprint_speed_multiplier if sprint_speed_multiplier != 1.0 else {}
                ),
                "walk_speed_multiplier": (
                    walk_speed_multiplier if walk_speed_multiplier != 1.0 else {}
                ),
            }
        )
        return self


class EntityAINearestPrioritizedAttackableTarget(AIGoal):
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
        """Allows the mob to check for and pursue the nearest valid target.

        Parameters:
            attack_interval (int, optional): Time in seconds before selecting a target. Defaults to 0.
            attack_interval_min (int, optional): Time in seconds before selecting a target. Defaults to 0.
            attack_owner (bool, optional): Description. Defaults to False.
            must_reach (bool, optional): If true, only entities that this mob can path to can be selected as targets. Defaults to False.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            persist_time (float, optional): Time in seconds for a valid target to stay targeted when it becomes and invalid target. Defaults to 0.0.
            reevaluate_description (bool, optional): If true, the mob will stop being targeted if it stops meeting any conditions. Defaults to False.
            reselect_targets (bool, optional): If true, the target will change to the current closest entity whenever a different entity is closer. Defaults to False.
            scan_interval (int, optional): How many ticks to wait between scanning for a target. Defaults to 10.
            set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Defaults to False.
            target_invisible_multiplier (float, optional): Description. Defaults to 0.7.
            target_search_height (float, optional): Height in blocks to search for a target mob. -1.0f means the height does not matter. Defaults to -0.1.
            target_sneak_visibility_multiplier (float, optional): Description. Defaults to 0.8.
            within_radius (float, optional): Distance in blocks that the target can be within to launch an attack. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nearest_prioritized_attackable_target
        """
        super().__init__("behavior.nearest_prioritized_attackable_target")
        self._add_field("entity_types", [])

        if attack_interval != 0:
            self._add_field("attack_interval", attack_interval)
        if attack_interval_min != 0:
            self._add_field("attack_interval_min", attack_interval_min)
        if attack_owner:
            self._add_field("attack_owner", attack_owner)
        if must_reach:
            self._add_field("must_reach", must_reach)
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field("must_see_forget_duration", must_see_forget_duration)
        if persist_time != 0.0:
            self._add_field("persist_time", persist_time)
        if reevaluate_description:
            self._add_field("reevaluate_description", reevaluate_description)
        if reselect_targets:
            self._add_field("reselect_targets", reselect_targets)
        if scan_interval != 10:
            self._add_field("scan_interval", scan_interval)
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if target_invisible_multiplier != 0.7:
            self._add_field("target_invisible_multiplier", target_invisible_multiplier)
        if target_search_height != -0.1:
            self._add_field("target_search_height", target_search_height)
        if target_sneak_visibility_multiplier != 0.8:
            self._add_field(
                "target_sneak_visibility_multiplier", target_sneak_visibility_multiplier
            )
        if within_radius != 0.0:
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
                "must_see_forget_duration": (
                    must_see_forget_duration if must_see_forget_duration != 3.0 else {}
                ),
                "sprint_speed_multiplier": (
                    sprint_speed_multiplier if sprint_speed_multiplier != 1.0 else {}
                ),
                "walk_speed_multiplier": (
                    walk_speed_multiplier if walk_speed_multiplier != 1.0 else {}
                ),
            }
        )
        return self


class EntityAIKnockbackRoar(AIGoal):
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
        """Allows the mob to perform a damaging knockback that affects all nearby entities.

        Parameters:
            attack_time (float, optional): The delay after which the knockback occurs (in seconds). Defaults to 0.5.
            cooldown_time (float, optional): Time (in seconds) the mob has to wait before using the goal again. Defaults to 0.1.
            damage_filters (Filter, optional): The list of conditions another entity must meet to be a valid target to apply damage to. Defaults to None.
            duration (float, optional): The max duration of the roar (in seconds). Defaults to 1.
            knockback_damage (int, optional): The damage dealt by the knockback roar. Defaults to 6.
            knockback_filters (Filter, optional): The list of conditions another entity must meet to be a valid target to apply knockback to. Defaults to None.
            knockback_height_cap (float, optional): The maximum height for vertical knockback. Defaults to 0.4.
            knockback_horizontal_strength (int, optional): The strength of the horizontal knockback. Defaults to 4.
            knockback_range (int, optional): The radius (in blocks) of the knockback effect. Defaults to 4.
            knockback_vertical_strength (int, optional): The strength of the vertical knockback. Defaults to 4.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_knockback_roar
        """
        super().__init__("behavior.knockback_roar")

        if attack_time != 0.5:
            self._add_field("attack_time", attack_time)
        if cooldown_time != 0.1:
            self._add_field("cooldown_time", cooldown_time)
        if not damage_filters is None:
            self._add_field("damage_filters", damage_filters)
        if duration != 1:
            self._add_field("duration", duration)
        if knockback_damage != 6:
            self._add_field("knockback_damage", knockback_damage)
        if not knockback_filters is None:
            self._add_field("knockback_filters", knockback_filters)
        if knockback_height_cap != 0.4:
            self._add_field("knockback_height_cap", knockback_height_cap)
        if knockback_horizontal_strength != 4:
            self._add_field(
                "knockback_horizontal_strength", knockback_horizontal_strength
            )
        if knockback_range != 4:
            self._add_field("knockback_range", knockback_range)
        if knockback_vertical_strength != 4:
            self._add_field("knockback_vertical_strength", knockback_vertical_strength)

    def on_roar_end(self, on_roar_end: str):
        self._add_field("on_roar_end", {"event": on_roar_end})
        return self


class EntityAIFloat(AIGoal):
    _identifier = "minecraft:behavior.float"

    def __init__(
        self,
        sink_with_passengers: bool = False,
        chance_per_tick_to_float: float = 0.0,
        time_under_water_to_dismount_passengers: Seconds = 0.0,
    ) -> None:
        """Allows the mob to stay afloat while swimming. Passengers will be kicked out the moment the mob's head goes underwater, which may not happen for tall mobs.

        Parameters:
            sink_with_passengers (bool, optional): If true, the mob will keep sinking as long as it has passengers. Defaults to False.
            chance_per_tick_to_float (float, optional): The chance per tick to cause an upward impulse. Defaults to 0.0.
            time_under_water_to_dismount_passengers (Seconds, optional): Time in seconds that a floating vehicles head can be underwater before it causes its passengers to dismount. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float
        """
        super().__init__("behavior.float")
        if sink_with_passengers:
            self._add_field("sink_with_passengers", sink_with_passengers)
        if chance_per_tick_to_float != 0.0:
            self._add_field("chance_per_tick_to_float", chance_per_tick_to_float)
        if time_under_water_to_dismount_passengers != 0.0:
            self._add_field(
                "time_under_water_to_dismount_passengers",
                time_under_water_to_dismount_passengers,
            )


class EntityAIRandomStroll(AIGoal):
    _identifier = "minecraft:behavior.random_stroll"

    def __init__(
        self,
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Allows a mob to randomly stroll around.

        Parameters:
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_stroll
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


class EntityAILookAtPlayer(AIGoal):
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
        """Compels an entity to look at the player by rotating the `head` bone pose within a set limit.

        Parameters:
            angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Value must be <= 360. Defaults to 360.
            angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Value must be <= 360. Defaults to 360.
            look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Defaults to 8.0.
            look_time (tuple[int, int], optional): Time range to look at the nearest entity. Defaults to (2, 4).
            probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Value must be <= 1. Defaults to 0.02.
            target_distance (float, optional): Description. Defaults to 0.6.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_player
        """
        super().__init__("behavior.look_at_player")
        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time != (2, 4):
            self._add_field(
                "look_time", AnvilFormatter.min_max_dict(look_time, "look_time")
            )

        if probability != 0.02:
            self._add_field("probability", probability)
        if target_distance != 0.6:
            self._add_field("target_distance", target_distance)


class EntityAIRandomLookAround(AIGoal):
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
        """Allows the mob to randomly look around.

        Parameters:
            angle_of_view_horizontal (int, optional): Description. Defaults to 360.
            angle_of_view_vertical (int, optional): Description. Defaults to 360.
            look_distance (float, optional): Description. Defaults to 8.0.
            look_time (tuple[int, int], optional): The range of time in seconds the mob will stay looking in a random direction before looking elsewhere. Defaults to (2, 4).
            probability (float, optional): Description. Defaults to 0.02.
            target_distance (float, optional): Description. Defaults to 0.6.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_look_around
        """
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


class EntityAIHurtByTarget(AIGoal):
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
        """Allows the mob to target another mob that hurts them.

        Parameters:
            alert_same_type (bool, optional): If true, nearby mobs of the same type will be alerted about the damage. Defaults to False.
            entity_types (Filter, optional): List of entity types that this mob can target when hurt by them. Defaults to None.
            max_dist (int, optional): Maximum distance this mob can be away to be a valid choice. Defaults to 16.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            reevaluate_description (bool, optional): If true, the mob will stop being targeted if it stops meeting any conditions. Defaults to False.
            sprint_speed_multiplier (float, optional): Multiplier for the running speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Multiplier for the walking speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.
            hurt_owner (bool, optional): If true, the mob will hurt its owner and other mobs with the same owner as itself. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hurt_by_target
        """
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


class EntityAIMeleeAttack(AIGoal):
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
        """Allows an entity to deal damage through a melee attack.

        Parameters:
            attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Defaults to False.
            cooldown_time (int, optional): Cooldown time, in seconds, between consecutive attacks. Defaults to 1.
            inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Defaults to 0.25.
            max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.55.
            melee_fov (int, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Defaults to 90.
            min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.2.
            outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (int, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Defaults to 16.
            path_outer_boundary (int, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Defaults to 32.
            random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Defaults to 0.
            reach_multiplier (int, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Defaults to False.
            speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Defaults to 1.
            track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Defaults to 30.
            can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_melee_attack
        """
        super().__init__("behavior.melee_attack")
        if attack_once:
            self._add_field("attack_once", attack_once)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if inner_boundary_time_increase != 0.75:
            self._add_field(
                "inner_boundary_time_increase", inner_boundary_time_increase
            )
        if max_path_time != 0.75:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if outer_boundary_time_increase != 0.5:
            self._add_field(
                "outer_boundary_time_increase", outer_boundary_time_increase
            )
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

    def on_attack(self, on_attack: str):
        self._add_field("on_attack", on_attack)
        return self

    def on_kill(
        self,
        on_kill: str,
        subject: FilterSubject = FilterSubject.Self,
        filter: Filter = None,
    ):
        self._add_field(
            "on_kill",
            {
                "event": on_kill,
                "filters": filter if not filter is None else {},
                "target": subject,
            },
        )


class EntityAIRangedAttack(AIGoal):
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
        """Allows an entity to attack by using ranged shots. "charge_shoot_trigger" must be greater than 0 to enable charged up burst-shot attacks. Requires minecraft:shooter to define projectile behaviour.

        Parameters:
            attack_interval (int, optional): Alternative to "attack_interval_min" & "attack_interval_max". Consistent reload-time (in seconds), when not using a charged shot. Does not scale with target-distance. Defaults to 0.
            attack_interval_max (int, optional): Maximum bound for reload-time range (in seconds), when not using a charged shot. Reload-time range scales with target-distance. Defaults to 0.
            attack_interval_min (int, optional): Minimum bound for reload-time range (in seconds), when not using a charged shot. Reload-time range scales with target-distance. Defaults to 0.
            attack_radius (int, optional): Minimum distance to target before this entity will attempt to shoot. Defaults to 0.
            attack_radius_min (int, optional): Minimum distance the target can be for this mob to fire. If the target is closer, this mob will move first before firing. Defaults to 0.
            burst_interval (int, optional): Time (in seconds) between each individual shot when firing a burst of shots from a charged up attack. Defaults to 0.
            burst_shots (int, optional): Number of shots fired every time the attacking entity uses a charged up attack. Defaults to 1.
            charge_charged_trigger (int, optional): Time (in seconds, then add "charge_shoot_trigger"), before a charged up attack is done charging. Charge-time decays while target is not in sight. Defaults to 0.
            charge_shoot_trigger (int, optional): Amount of time (in seconds, then doubled) a charged shot must be charging before reloading burst shots. Charge-time decays while target is not in sight. Defaults to 0.
            ranged_fov (int, optional): Field of view (in degrees) when using sensing to detect a target for attack. Defaults to 90.
            set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Defaults to False.
            speed_multiplier (int, optional): During attack behavior, this multiplier modifies the entity's speed when moving toward the target. Defaults to 1.
            swing (bool, optional): If a swing animation (using variable.attack_time) exists, this causes the actor to swing their arm(s) upon firing the ranged attack. Defaults to False.
            target_in_sight_time (int, optional): Minimum amount of time (in seconds) the attacking entity needs to see the target before moving toward it. Defaults to 1.
            x_max_rotation (int, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Defaults to 30.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ranged_attack
        """
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


class EntityAISummonEntity(AIGoal):
    _identifier = "minecraft:behavior.summon_entity"

    def __init__(self) -> None:
        """Allows the mob to attack the player by summoning other entities.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_summon_entity
        """
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
                "max_activation_range": (
                    max_activation_range if max_activation_range != 32 else {}
                ),
                "min_activation_range": (
                    min_activation_range if min_activation_range != 1 else {}
                ),
                "particle_color": particle_color if particle_color != 0 else {},
                "start_sound_event": (
                    start_sound_event if not start_sound_event is None else {}
                ),
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
                "summon_cap_radius": (
                    summon_cap_radius if summon_cap_radius != 0 else {}
                ),
                "target": target,
                "summon_event": (
                    summon_event if summon_event != "minecraft:entity_spawned" else {}
                ),
            }
        )
        return self


class EntityAIDelayedAttack(AIGoal):
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
        """Allows an entity to attack, while also delaying the damage-dealt until a specific time in the attack animation.

        Parameters:
            attack_duration (float, optional): The entity's attack animation will play out over this duration (in seconds). Also controls attack cooldown. Defaults to 0.75.
            attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Defaults to False.
            cooldown_time (int, optional): Description. Defaults to 1.
            hit_delay_pct (float, optional): The percentage into the attack animation to apply the damage of the attack (1.0 = 100%). Value must be <= 1. Defaults to 0.5.
            inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Defaults to 0.25.
            max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.55.
            melee_fov (int, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Defaults to 90.
            min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.2.
            outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (int, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Defaults to 16.
            path_outer_boundary (int, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Defaults to 32.
            random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Defaults to 0.
            reach_multiplier (int, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Defaults to False.
            speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Defaults to 1.
            track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Defaults to 30.
            can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_delayed_attack
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
            self._add_field(
                "inner_boundary_time_increase", inner_boundary_time_increase
            )
        if max_path_time != 0.55:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if outer_boundary_time_increase != 0.5:
            self._add_field(
                "outer_boundary_time_increase", outer_boundary_time_increase
            )
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

    def on_attack(
        self,
        on_attack: str,
        target: FilterSubject = FilterSubject.Self,
        filter: Filter = None,
    ):
        self._add_field(
            "on_attack",
            {
                "event": on_attack,
                "filters": filter if not filter is None else {},
                "target": target,
            },
        )
        return self


class EntityAIMoveToBlock(AIGoal):
    _identifier = "minecraft:behavior.move_to_block"

    def __init__(
        self,
        target_blocks: list[MinecraftBlockDescriptor | str],
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
        """Allows mob to move towards a block.

        Parameters:
            target_blocks (list[MinecraftBlockDescriptor | str]): Block types to move to.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            search_height (int, optional): The height in blocks that the mob will look for the block. Defaults to 1.
            search_range (int, optional): The distance in blocks that the mob will look for the block. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            start_chance (float, optional): Chance to start the behavior (applied after each random tick_interval). Defaults to 1.0.
            stay_duration (float, optional): Number of ticks needed to complete a stay at the block. Defaults to 0.0.
            target_offset (tuple[float, float, float], optional): Offset to add to the selected target position. Defaults to (0, 0, 0).
            target_selection_method (str, optional): Kind of block to find fitting the specification. Valid values are "random" and "nearest". Defaults to 'nearest'.
            tick_interval (int, optional): Average interval in ticks to try to run this behavior. Defaults to 20.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_block
        """
        super().__init__("behavior.move_to_block")

        from anvil.lib.schemas import MinecraftBlockDescriptor

        if not all(
            isinstance(block, (MinecraftBlockDescriptor, str))
            for block in target_blocks
        ):
            raise TypeError(
                f"All target_blocks must be either MinecraftBlockDescriptor instances or strings representing block identifiers. Component [{self._identifier}]"
            )

        self._add_field(
            "target_blocks",
            [str(block) for block in target_blocks],
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

    def on_reach(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_reach", {"event": event, "target": target.value})
        return self

    def on_stay_completed(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_stay_completed", {"event": event, "target": target.value})
        return self


class EntityAIEquipItem(AIGoal):
    _identifier = "minecraft:behavior.equip_item"

    def __init__(self) -> None:
        """The entity puts on the desired equipment.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_equip_item
        """
        super().__init__("behavior.equip_item")


class EntityAISendEvent(AIGoal):
    _identifier = "minecraft:behavior.send_event"

    def __init__(self) -> None:
        """Allows the mob to send an event to another mob.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_send_event
        """
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


class EntityAIMoveTowardsTarget(AIGoal):
    _identifier = "minecraft:behavior.move_towards_target"

    def __init__(
        self, within_radius: float = 0.0, speed_multiplier: float = 1.0
    ) -> None:
        """Allows mob to move towards its current target.

        Parameters:
            within_radius (float, optional): Defines the radius in blocks that the mob tries to be from the target. A value of 0 means it tries to occupy the same block as the target. Defaults to 0.0.
            speed_multiplier (float, optional): Description. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_target
        """
        super().__init__("behavior.move_towards_target")

        if within_radius != 0.0:
            self._add_field("within_radius", within_radius)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIRandomSitting(AIGoal):
    _identifier = "minecraft:behavior.random_sitting"

    def __init__(
        self,
        cooldown_time: float = 0,
        min_sit_time: float = 10,
        start_chance: float = 0.1,
        stop_chance: float = 0.3,
    ) -> None:
        """Allows the mob to randomly sit for a duration.

        Parameters:
            cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.
            min_sit_time (float, optional): The minimum amount of time in seconds before the mob can stand back up. Defaults to 10.
            start_chance (float, optional): This is the chance that the mob will start this goal, from 0 to 1. Defaults to 0.1.
            stop_chance (float, optional): This is the chance that the mob will stop this goal, from 0 to 1. Defaults to 0.3.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_sitting
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


class EntityAIStayWhileSitting(AIGoal):
    _identifier = "minecraft:behavior.stay_while_sitting"

    def __init__(self) -> None:
        """Allows the mob to stay put while it is in a sitting state instead of doing something else.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_while_sitting
        """
        super().__init__("behavior.stay_while_sitting")


class EntityAIRandomSwim(AIGoal):
    _identifier = "minecraft:behavior.random_swim"

    def __init__(
        self,
        avoid_surface: bool = True,
        interval: int = 120,
        speed_multiplier: float = 1,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Allows an entity to randomly move through water.

        Parameters:
            avoid_surface (bool, optional): If true, the mob will avoid surface water blocks by swimming below them. Defaults to True.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_swim
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


class EntityAIRandomBreach(AIGoal):
    _identifier = "minecraft:behavior.random_breach"

    def __init__(
        self,
        cooldown_time: float = 0,
        interval: int = 120,
        speed_multiplier: float = 1,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Allows the mob to randomly break surface of the water.

        Parameters:
            cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_breach
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


class EntityAIMoveToWater(AIGoal):
    _identifier = "minecraft:behavior.move_to_water"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1,
    ) -> None:
        """Allows the mob to move back into water when on land.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for water to move towards Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for water to move towards Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_water
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


class EntityAIMoveToLand(AIGoal):
    _identifier = "minecraft:behavior.move_to_land"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1,
    ) -> None:
        """Allows the mob to move back onto land when in water.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for land to move towards Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for land to move towards Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_land
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


class EntityAIMoveToLava(AIGoal):
    _identifier = "minecraft:behavior.move_to_lava"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1,
    ) -> None:
        """Important

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for lava to move towards Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for lava to move towards Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_lava
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


class EntityAILookAtTarget(AIGoal):
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
        """Compels an entity to look at the target by rotating the head bone pose within a set limit.

        Parameters:
            angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Value must be <= 360. Defaults to 360.
            angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Value must be <= 360. Defaults to 360.
            look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Defaults to 8.0.
            look_time (tuple[int, int], optional): Time range to look at the nearest entity. Defaults to (2, 4).
            probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Value must be <= 1. Defaults to 0.02.
            target_distance (float, optional): Description. Defaults to 0.6.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_target
        """
        super().__init__("behavior.look_at_target")
        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time != (2, 4):
            self._add_field(
                "look_time", AnvilFormatter.min_max_dict(look_time, "look_time")
            )
        if probability != 0.02:
            self._add_field("probability", probability)
        if target_distance != 0.6:
            self._add_field("target_distance", target_distance)


class EntityAIFollowParent(AIGoal):
    _identifier = "minecraft:behavior.follow_parent"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to follow their parent around.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_parent
        """
        super().__init__("behavior.follow_parent")
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIPlayerRideTamed(AIGoal):
    _identifier = "minecraft:behavior.player_ride_tamed"

    def __init__(self) -> None:
        """Allows the mob to be ridden by the player after being tamed.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_player_ride_tamed
        """
        super().__init__("behavior.player_ride_tamed")


class EntityAIFollowOwner(AIGoal):
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
        """Allows a mob to follow the player that owns it.

        Parameters:
            can_teleport (bool, optional): Defines if the mob will teleport to its owner when too far away. Defaults to True.
            ignore_vibration (bool, optional): Defines if the mob should disregard following its owner after detecting a recent vibration. Defaults to True.
            max_distance (float, optional): The maximum distance the mob can be from its owner to start following it. Applicable only when "can_teleport" is set to false. Defaults to 60.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            start_distance (float, optional): The minimum distance the mob must be from its owner to start following it. Defaults to 10.0.
            stop_distance (float, optional): The distance at which the mob will stop following its owner. Defaults to 2.0.
            post_teleport_distance (int, optional): Defines how far (in blocks) the entity will be from its owner after teleporting. If not specified, it defaults to "stop_distance" + 1, allowing the entity to seamlessly resume navigation. Defaults to 1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_owner
        """
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


class EntityAIPanic(AIGoal):
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
        """Allows the mob to enter the panic state, which makes it run around and away from the damage source that made it enter this state.

        Parameters:
            damage_sources (DamageCause, optional): The list of Entity Damage Sources that will cause this mob to panic. Defaults to DamageCause.All.
            force (bool, optional): If true, this mob will not stop panicking until it can't move anymore or the goal is removed from it. Defaults to False.
            ignore_mob_damage (bool, optional): If true, the mob will not panic in response to damage from other mobs. This overrides the damage types in "damage_sources". Defaults to False.
            panic_sound (str, optional): Description. Defaults to None.
            prefer_water (bool, optional): If true, the mob will prefer water over land. Defaults to False.
            sound_interval (float, optional): Description. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_panic
        """
        super().__init__("behavior.panic")
        if damage_sources != DamageCause.All:
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


class EntityAIChargeAttack(AIGoal):
    _identifier = "minecraft:behavior.charge_attack"

    def __init__(
        self,
        max_distance: int = 3,
        min_distance: int = 2,
        success_rate: float = 0.1428,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows this entity to damage a target by using a running attack.

        Parameters:
            max_distance (int, optional): A charge attack cannot start if the entity is farther than this distance to the target. Defaults to 3.
            min_distance (int, optional): A charge attack cannot start if the entity is closer than this distance to the target. Defaults to 2.
            success_rate (float, optional): Percent chance this entity will start a charge attack, if not already attacking (1.0 = 100%). Defaults to 0.1428.
            speed_multiplier (float, optional): Modifies the entity's speed when charging toward the target. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_attack
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


class EntityAIRamAttack(AIGoal):
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
        """Allows this entity to damage a target by using a running attack.

        Parameters:
            baby_knockback_modifier (float, optional): The modifier to knockback that babies have. Defaults to 0.333333.
            cooldown_range (list[int, int], optional): Minimum and maximum cooldown time-range (positive, in seconds) between each attempted ram attack. Defaults to [10, 20].
            knockback_force (float, optional): The force of the knockback of the ram attack. Defaults to 5.
            knockback_height (float, optional): The height of the knockback of the ram attack. Defaults to 0.1.
            min_ram_distance (float, optional): The minimum distance at which the mob can start a ram attack. Defaults to 0.0.
            pre_ram_sound (str, optional): The sound to play when an entity is about to perform a ram attack. Defaults to None.
            ram_distance (float, optional): The distance at which the mob start to run with ram speed. Defaults to 0.0.
            ram_impact_sound (str, optional): The sound to play when an entity is impacting on a ram attack. Defaults to None.
            ram_speed (float, optional): Sets the entity's speed when charging toward the target. Defaults to 2.0.
            run_speed (float, optional): Sets the entity's speed when running toward the target. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ram_attack
        """
        super().__init__("behavior.ram_attack")
        if baby_knockback_modifier != 0.333333:
            self._add_field("baby_knockback_modifier", baby_knockback_modifier)
        if cooldown_range != [10, 20]:
            self._add_field(
                "cooldown_range",
                AnvilFormatter.min_max_dict(cooldown_range, "cooldown_range"),
            )
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
        self._component.setdefault("on_start", []).append(
            {"event": event, "target": target.value}
        )
        return self


class EntityAIAvoidMobType(AIGoal):
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
        """Allows the entity to run away from other entities that meet the criteria specified.

        Parameters:
            avoid_mob_sound (str, optional): The sound event to play when the mob is avoiding another mob. Defaults to None.
            avoid_target_xz (int, optional): The next target position the entity chooses to avoid another entity will be chosen within this XZ Distance. Defaults to 16.
            avoid_target_y (int, optional): The next target position the entity chooses to avoid another entity will be chosen within this Y Distance. Defaults to 7.
            ignore_visibility (bool, optional): Whether or not to ignore direct line of sight while this entity is running away from other specified entities. Defaults to False.
            probability_per_strength (float, optional): Percent chance this entity will stop avoiding another entity based on that entity's strength, where 1.0 = 100%. Value must be <= 1. Defaults to 1.0.
            remove_target (bool, optional): Determine if we should remove target when fleeing or not. Defaults to False.
            sound_interval (list[float], optional): The range of time in seconds to randomly wait before playing the sound again. Defaults to [3.0, 8.0].
            check_if_outnumbered (bool, optional): If true, the mob will check if its outnumbered. Defaults to False.
            cooldown (float, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_mob_type
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
            if not isinstance(sound_interval, list):
                raise TypeError("sound_interval must be a list of two numbers")
            if len(sound_interval) != 2:
                raise ValueError("sound_interval must contain exactly two numbers")
            self._add_field(
                "sound_interval",
                {
                    "range_min": min(sound_interval),
                    "range_max": max(sound_interval),
                },
            )
        if check_if_outnumbered:
            self._add_field("check_if_outnumbered", check_if_outnumbered)
        if cooldown != 0.0:
            self._add_field("cooldown", cooldown)

    def add_type(
        self,
        filter: Filter,
        max_dist: float = 3.0,
        max_flee: float = 10.0,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        """Adds a new entity type to the list of conditions another entity must meet to be a valid target to avoid.

        Parameters:
            filter (Filter): Filter to determine which entities to avoid.
            max_dist (float, optional): Maximum distance to look for an avoid target for the entity. Defaults to 3.0.
            max_flee (float, optional): How many blocks away from its avoid target the entity must be for it to stop fleeing from the avoid target. Defaults to 10.0.
            sprint_speed_multiplier (float, optional): Multiplier for sprint speed. 1.0 means keep the regular speed, while higher numbers make the sprint speed faster. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Multiplier for walking speed. 1.0 means keep the regular speed, while higher numbers make the walking speed faster. Defaults to 1.0.
        """

        a = {"filters": filter}
        if max_dist != 3.0:
            a["max_dist"] = max_dist
        if max_flee != 10.0:
            a["max_flee"] = max_flee
        if sprint_speed_multiplier != 1.0:
            a["sprint_speed_multiplier"] = sprint_speed_multiplier
        if walk_speed_multiplier != 1.0:
            a["walk_speed_multiplier"] = walk_speed_multiplier
        self._get_field("entity_types", []).append(a)
        return self

    def on_escape_event(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Event that is triggered when escaping from a mob.

        Parameters:
            event (str): Event to trigger.
            target (FilterSubject, optional): Target of the event. Defaults to FilterSubject.Self.
        """
        # append to the escape event list so multiple handlers can be added
        self._get_field("on_escape_event", []).append(
            {"event": event, "target": target.value}
        )
        return self


class EntityAILeapAtTarget(AIGoal):
    _identifier = "minecraft:behavior.leap_at_target"

    def __init__(
        self,
        must_be_on_ground: bool = True,
        set_persistent: bool = False,
        target_dist: float = 0.3,
        yd: float = 0.0,
    ) -> None:
        """Allows monsters to jump at and attack their target. Can only be used by hostile mobs.

        Parameters:
            must_be_on_ground (bool, optional): If true, the mob will only jump at its target if its on the ground. Setting it to false will allow it to jump even if its already in the air. Defaults to True.
            set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Defaults to False.
            target_dist (float, optional): The height in blocks the mob jumps when leaping at its target. Defaults to 0.3.
            yd (float, optional): The height in blocks the mob jumps when leaping at its target. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_leap_at_target
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


class EntityAIOcelotAttack(AIGoal):
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
        """Controls specific attack behavior for Ocelots.

        Parameters:
            cooldown_time (int, optional): Time (in seconds) between attacks. Value must be > 0. Defaults to 1.
            max_distance (int, optional): Max distance from the target, this entity will use this attack behavior. Value must be > 0. Defaults to 15.
            max_sneak_range (int, optional): Max distance from the target, this entity starts sneaking. Value must be > 0. Defaults to 15.
            max_sprint_range (int, optional): Max distance from the target, this entity starts sprinting (sprinting takes priority over sneaking). Value must be > 0. Defaults to 4.
            reach_multiplier (int, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Value must be > 0. Defaults to 2.
            sneak_speed_multiplier (float, optional): Modifies the attacking entity's movement speed while sneaking. Value must be > 0. Defaults to 0.6.
            sprint_speed_multiplier (float, optional): Modifies the attacking entity's movement speed while sprinting. Value must be > 0. Defaults to 1.33.
            walk_speed_multiplier (float, optional): Modifies the attacking entity's movement speed when not sneaking or sprinting, but still within attack range. Value must be > 0. Defaults to 0.8.
            x_max_rotation (int, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Value must be > 0. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation (in degrees), on the Y-axis, this entity's head can rotate while trying to look at the target. Value must be > 0. Defaults to 30.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelotattack
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


class EntityAIOwnerHurtByTarget(AIGoal):
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
        """Allows the mob to target another mob that hurts their owner.

        Parameters:
            entity_types (Filter, optional): List of entity types that this mob can target if they hurt their owner. Defaults to None.
            cooldown (Seconds, optional): Description. Defaults to 0.
            filters (Filter, optional): Description. Defaults to None.
            max_dist (int, optional): Description. Defaults to 16.
            must_see (bool, optional): Description. Defaults to False.
            must_see_forget_duration (float, optional): Description. Defaults to 3.0.
            reevaluate_description (bool, optional): If true, the targeting entity will continuously reevaluate the target and stop attacking if the target no longer meets the filter conditions. Defaults to False.
            sprint_speed_multiplier (float, optional): Description. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Description. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_by_target
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


class EntityAIOwnerHurtTarget(AIGoal):
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
        """Allows the mob to target a mob that is hurt by their owner.

        Parameters:
            entity_types (Filter, optional): List of entity types that this entity can target if the potential target is hurt by this mob's owner. Defaults to None.
            cooldown (Seconds, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Defaults to 0.
            filters (Filter, optional): Conditions that make this entry in the list valid. Defaults to None.
            max_dist (int, optional): Maximum distance this mob can be away to be a valid choice. Defaults to 16.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (float, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            reevaluate_description (bool, optional): If true, the mob will stop being targeted if it stops meeting any conditions. Defaults to False.
            sprint_speed_multiplier (float, optional): Multiplier for the running speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.
            walk_speed_multiplier (float, optional): Multiplier for the walking speed. A value of 1.0 means the speed is unchanged. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_owner_hurt_target
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


class EntityAIRandomSearchAndDig(AIGoal):
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
        """Allows this entity to locate a random target block that it can path find to. Once found, the entity will move towards it and dig up an item. [Default target block types: Dirt, Grass, Podzol, DirtWithRoots, MossBlock, Mud, MuddyMangroveRoots].

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): Goal cooldown range in seconds. Defaults to (0, 0).
            digging_duration_range (tuple[Seconds, Seconds], optional): Digging duration in seconds. Defaults to (0, 0).
            find_valid_position_retries (int, optional): Amount of retries to find a valid target position within search range. Defaults to 0.
            goal_radius (float, optional): Distance in blocks within the entity to considers it has reached it's target position. Defaults to 1.5.
            item_table (str, optional): File path relative to the resource pack root for items to spawn list (loot table format). Defaults to None.
            search_range_xz (float, optional): Width and length of the volume around the entity used to find a valid target position. Defaults to 0.
            search_range_y (float, optional): Height of the volume around the entity used to find a valid target position. Defaults to 0.
            spawn_item_after_seconds (Seconds, optional): Digging duration before spawning item in seconds. Defaults to 0.
            spawn_item_pos_offset (float, optional): Distance to offset the item's spawn location in the direction the mob is facing. Defaults to 0.
            speed_multiplier (float, optional): Searching movement speed multiplier. Defaults to 0.
            target_blocks (list[str], optional): List of target block types the goal will look to dig on. Overrides the default list. Defaults to [].
            target_dig_position_offset (float, optional): Dig target position offset from the feet position of the mob in their facing direction. Defaults to 2.25.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_search_and_dig
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
        if target_blocks != []:
            self._add_field("target_blocks", target_blocks)
        if target_dig_position_offset != 2.25:
            self._add_field("target_dig_position_offset", target_dig_position_offset)

    def on_digging_start(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_digging_start", {"event": event, "target": target.value})
        return self

    def on_fail_during_digging(
        self, event: str, target: FilterSubject = FilterSubject.Self
    ):
        self._add_field(
            "on_fail_during_digging", {"event": event, "target": target.value}
        )
        return self

    def on_fail_during_searching(
        self, event: str, target: FilterSubject = FilterSubject.Self
    ):
        self._add_field(
            "on_fail_during_searching", {"event": event, "target": target.value}
        )
        return self

    def on_item_found(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_item_found", {"event": event, "target": target.value})
        return self

    def on_searching_start(
        self, event: str, target: FilterSubject = FilterSubject.Self
    ):
        self._add_field("on_searching_start", {"event": event, "target": target.value})
        return self

    def on_success(self, event: str, target: FilterSubject = FilterSubject.Self):
        self._add_field("on_success", {"event": event, "target": target.value})
        return self


class EntityAIStompAttack(AIGoal):
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
        """Allows an entity to attack using stomp AoE damage behavior.

        Parameters:
            attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Defaults to False.
            attack_types (list[str], optional): Defines the entity types this entity will attack. Defaults to [].
            cooldown_time (Seconds, optional): Cooldown time, in seconds, between consecutive attacks. Defaults to 1.
            inner_boundary_time_increase (Seconds, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Defaults to 0.25.
            max_path_time (Seconds, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.55.
            melee_fov (int, optional): Description. Defaults to 90.
            min_path_time (Seconds, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.2.
            no_damage_range_multiplier (float, optional): Multiplied with the final AoE damage range to determine a no damage range. The stomp attack will go on cooldown if target is in this no damage range. Value must be > 0. Defaults to 2.
            outer_boundary_time_increase (Seconds, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (Seconds, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Defaults to 16.
            path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Defaults to 32.
            random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Defaults to 0.
            reach_multiplier (float, optional): Used with the base size of the entity to determine minimum target-distance before trying to deal attack damage. Defaults to 2.
            require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Defaults to False.
            set_persistent (bool, optional): Description. Defaults to False.
            speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Defaults to 1.
            stomp_range_multiplier (float, optional): Multiplied with the base size of the entity to determine stomp AoE damage range. Value must be > 0. Defaults to 2.
            track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Defaults to 30.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stomp_attack
        """
        super().__init__("behavior.stomp_attack")

        if attack_once:
            self._add_field("attack_once", attack_once)
        if attack_types != []:
            self._add_field("attack_types", attack_types)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if inner_boundary_time_increase != 0.25:
            self._add_field(
                "inner_boundary_time_increase", inner_boundary_time_increase
            )
        if max_path_time != 0.55:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if no_damage_range_multiplier != 2:
            self._add_field("no_damage_range_multiplier", no_damage_range_multiplier)
        if outer_boundary_time_increase != 0.5:
            self._add_field(
                "outer_boundary_time_increase", outer_boundary_time_increase
            )
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


class EntityAIFollowMob(AIGoal):
    _identifier = "minecraft:behavior.follow_mob"

    def __init__(
        self,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        stop_distance: int = 2,
        filters: Filter = None,
        preferred_actor_type: str = None,
        use_home_position_restriction: bool = False,
    ) -> None:
        """Allows the mob to follow other mobs.

        Parameters:
            search_range (int, optional): The distance in blocks it will look for a mob to follow. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            stop_distance (int, optional): The distance in blocks this mob stops from the mob it is following. Defaults to 2.
            filters (Filter, optional): If non-empty, provides criteria for filtering which nearby Mobs can be followed. Defaults to None.
            preferred_actor_type (str, optional): The type of actor to prefer following. If left unspecified, a random actor among those in range will be chosen. Defaults to None.
            use_home_position_restriction (bool, optional): If true, the mob will respect the 'minecraft:home' component's 'restriction_radius' field when choosing a target to follow. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_mob
        """
        super().__init__("behavior.follow_mob")
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if stop_distance != 2:
            self._add_field("stop_distance", stop_distance)
        if filters != None:
            self._add_field("filters", filters)
        if preferred_actor_type != None:
            self._add_field("preferred_actor_type", preferred_actor_type)
        if use_home_position_restriction:
            self._add_field(
                "use_home_position_restriction", use_home_position_restriction
            )


class EntityAIRandomSwim(AIGoal):
    _identifier = "minecraft:behavior.random_swim"

    def __init__(
        self,
        avoid_surface: bool = True,
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
    ) -> None:
        """Allows an entity to randomly move through water.

        Parameters:
            avoid_surface (bool, optional): If true, the mob will avoid surface water blocks by swimming below them. Defaults to True.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_swim
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


class EntityAIRandomBreach(AIGoal):
    _identifier = "minecraft:behavior.random_breach"

    def __init__(
        self,
        interval: int = 120,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
        cooldown_time: Seconds = 10,
    ) -> None:
        """Allows the mob to randomly break surface of the water.

        Parameters:
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            cooldown_time (Seconds, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 10.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_breach
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


class EntityAIRandomHover(AIGoal):
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
        """Allows the mob to hover around randomly, close to the surface.

        Parameters:
            hover_height (tuple[float, float], optional): The height above the surface which the mob will try to maintain. Defaults to (0.0, 0.0).
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            y_offset (float, optional): Height in blocks to add to the selected target position. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_hover
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


class EntityAIRoar(AIGoal):
    _identifier = "minecraft:behavior.roar"

    def __init__(
        self,
        duration: Seconds = 0.0,
    ) -> None:
        """Allows this entity to roar at another entity based on data in `minecraft:anger_level`. Once the anger threshold specified in `minecraft:anger_level` has been reached, this entity will roar for the specified amount of time, look at the other entity, apply anger boost towards it, and finally target it.

        Parameters:
            duration (Seconds, optional): The amount of time to roar for. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roar
        """
        super().__init__("behavior.roar")

        if duration != 0.0:
            self._add_field("duration", duration)


class EntityAIFloatWander(AIGoal):
    _identifier = "minecraft:behavior.float_wander"

    def __init__(
        self,
        additional_collision_buffer: bool = False,
        allow_navigating_through_liquids: bool = False,
        float_duration: tuple[Seconds, Seconds] = (0.0, 0.0),
        float_wander_has_move_control: bool = True,
        must_reach: bool = False,
        navigate_around_surface: bool = False,
        random_reselect: bool = False,
        surface_xz_dist: int = 0,
        surface_y_dist: int = 0,
        use_home_position_restriction: bool = True,
        xz_dist: int = 10,
        y_dist: int = 7,
        y_offset: float = 0.0,
    ) -> None:
        """Allows the mob to float around like the Ghast.

        Parameters:
            additional_collision_buffer (bool, optional): If true, the mob will have an additional buffer zone around it to avoid collisions with blocks when picking a position to wander to. Defaults to False.
            allow_navigating_through_liquids (bool, optional): If true allows the mob to navigate through liquids on its way to the target position. Defaults to False.
            float_duration (tuple[Seconds, Seconds], optional): Range of time in seconds the mob will float around before landing and choosing to do something else. Defaults to (0.0, 0.0).
            float_wander_has_move_control (bool, optional): If true, the MoveControl flag will be added to the behavior which means that it can no longer be active at the same time as other behaviors with MoveControl. Defaults to True.
            must_reach (bool, optional): If true, the point has to be reachable to be a valid target. Defaults to False.
            navigate_around_surface (bool, optional): If true, will prioritize finding random positions in the vicinity of surfaces, i.e. blocks that are not Air or Liquid. Defaults to False.
            random_reselect (bool, optional): If true, the mob will randomly pick a new point while moving to the previously selected one. Defaults to False.
            surface_xz_dist (int, optional): The horizontal distance in blocks that the goal will check for a surface from a candidate position. Only valid when `navigate_around_surface` is true. Defaults to 0.
            surface_y_dist (int, optional): The vertical distance in blocks that the goal will check for a surface from a candidate position. Only valid when `navigate_around_surface` is true. Defaults to 0.
            use_home_position_restriction (bool, optional): If true, the mob will respect home position restrictions when choosing new target positions. If false, it will choose target position without considering home restrictions. Defaults to True.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            y_offset (float, optional): Height in blocks to add to the selected target position. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_wander
        """
        super().__init__("behavior.float_wander")

        if additional_collision_buffer:
            self._add_field("additional_collision_buffer", additional_collision_buffer)
        if allow_navigating_through_liquids:
            self._add_field(
                "allow_navigating_through_liquids", allow_navigating_through_liquids
            )
        if float_duration != (0.0, 0.0):
            self._add_field("float_duration", float_duration)
        if not float_wander_has_move_control:
            self._add_field(
                "float_wander_has_move_control", float_wander_has_move_control
            )
        if must_reach:
            self._add_field("must_reach", must_reach)
        if navigate_around_surface:
            self._add_field("navigate_around_surface", navigate_around_surface)
        if random_reselect:
            self._add_field("random_reselect", random_reselect)
        if surface_xz_dist != 0:
            self._add_field("surface_xz_dist", surface_xz_dist)
        if surface_y_dist != 0:
            self._add_field("surface_y_dist", surface_y_dist)
        if not use_home_position_restriction:
            self._add_field(
                "use_home_position_restriction", use_home_position_restriction
            )
        if xz_dist != 10:
            self._add_field("xz_dist", xz_dist)
        if y_dist != 7:
            self._add_field("y_dist", y_dist)
        if y_offset != 0.0:
            self._add_field("y_offset", y_offset)


class EntityAILayDown(AIGoal):
    _identifier = "minecraft:behavior.lay_down"

    def __init__(
        self,
        interval: int = 120,
        random_stop_interval: int = 120,
    ) -> None:
        """Allows mobs to lay down at times.

        Parameters:
            interval (int, optional): A random value to determine at what intervals something can occur. This has a 1/interval chance to choose this goal. Defaults to 120.
            random_stop_interval (int, optional): a random value in which the goal can use to pull out of the behavior. This is a 1/interval chance to play the sound. Defaults to 120.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_down
        """
        super().__init__("behavior.lay_down")

        if interval != 120:
            self._add_field("interval", interval)
        if random_stop_interval != 120:
            self._add_field("random_stop_interval", random_stop_interval)


class EntityAIMeleeBoxAttack(AIGoal):
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
        """Allows an entity to deal damage through a melee attack with reach calculations based on bounding boxes.

        Parameters:
            attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Defaults to False.
            attack_types (list[str], optional): Defines the entity types this entity will attack. Defaults to [].
            can_spread_on_fire (bool, optional): Allows the mob, if on fire and empty handed, to ignite its target upon a successful attack. Defaults to False.
            cooldown_time (Seconds, optional): Cooldown time, in seconds, between consecutive attacks. Defaults to 1.
            horizontal_reach (float, optional): The attack reach of the mob will be a box with the size of the mobs bounds increased by this value in all horizontal directions. Defaults to 0.8.
            inner_boundary_time_increase (Seconds, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Defaults to 0.25.
            max_path_time (Seconds, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.55.
            melee_fov (int, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Defaults to 90.
            min_path_time (Seconds, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to 0.2.
            outer_boundary_time_increase (Seconds, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Defaults to 0.5.
            path_fail_time_increase (Seconds, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Defaults to 0.75.
            path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Defaults to 16.
            path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Defaults to 32.
            random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Defaults to 0.
            box_increase (float, optional): Description. Defaults to 2.
            require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Defaults to False.
            set_persistent (bool, optional): Description. Defaults to False.
            speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Defaults to 1.
            track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Defaults to False.
            x_max_rotation (int, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Defaults to 30.
            y_max_head_rotation (int, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Defaults to 30.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_melee_box_attack
        """
        super().__init__("behavior.melee_box_attack")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.20.50")

        if attack_once:
            self._add_field("attack_once", attack_once)
        if attack_types != []:
            self._add_field("attack_types", attack_types)
        if can_spread_on_fire:
            self._add_field("can_spread_on_fire", can_spread_on_fire)
        if cooldown_time != 1:
            self._add_field("cooldown_time", cooldown_time)
        if horizontal_reach != 0.8:
            self._add_field("horizontal_reach", horizontal_reach)
        if inner_boundary_time_increase != 0.25:
            self._add_field(
                "inner_boundary_time_increase", inner_boundary_time_increase
            )
        if max_path_time != 0.55:
            self._add_field("max_path_time", max_path_time)
        if melee_fov != 90:
            self._add_field("melee_fov", melee_fov)
        if min_path_time != 0.2:
            self._add_field("min_path_time", min_path_time)
        if outer_boundary_time_increase != 0.5:
            self._add_field(
                "outer_boundary_time_increase", outer_boundary_time_increase
            )
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


class EntityAITimerFlag1(AIGoal):
    _identifier = "minecraft:behavior.timer_flag_1"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (10.0, 10.0),
        duration_range: tuple[Seconds, Seconds] = (2.0, 2.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping due to that timeout or due to being interrupted by another behavior, fires another event. query.timer_flag_1 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): Goal cooldown range in seconds. Can be a range object or a single number. Defaults to (10.0, 10.0).
            duration_range (tuple[Seconds, Seconds], optional): Goal duration range in seconds. Can be a range object or a single number. Defaults to (2.0, 2.0).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_1
        """
        super().__init__("behavior.timer_flag_1")

        if cooldown_range != (10.0, 10.0):
            self._add_field(
                "cooldown_range",
                AnvilFormatter.min_max_dict(cooldown_range, "cooldown_range"),
            )
        if duration_range != (2.0, 2.0):
            self._add_field(
                "duration_range",
                AnvilFormatter.min_max_dict(duration_range, "duration_range"),
            )
        if control_flags != []:
            self._add_field("control_flags", control_flags)

    def on_end(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self

    def on_start(self, on_start: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_start", {"event": on_start, "target": subject})
        return self


class EntityAITimerFlag2(AIGoal):
    _identifier = "minecraft:behavior.timer_flag_2"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (10.0, 10.0),
        duration_range: tuple[Seconds, Seconds] = (2.0, 2.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping due to that timeout or due to being interrupted by another behavior, fires another event. query.timer_flag_2 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): Goal cooldown range in seconds. Can be a range object or a single number. Defaults to (10.0, 10.0).
            duration_range (tuple[Seconds, Seconds], optional): Goal duration range in seconds. Can be a range object or a single number. Defaults to (2.0, 2.0).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_2
        """
        super().__init__("behavior.timer_flag_2")

        if cooldown_range != (10.0, 10.0):
            self._add_field(
                "cooldown_range",
                AnvilFormatter.min_max_dict(cooldown_range, "cooldown_range"),
            )
        if duration_range != (2.0, 2.0):
            self._add_field(
                "duration_range",
                AnvilFormatter.min_max_dict(duration_range, "duration_range"),
            )
        if control_flags != []:
            self._add_field("control_flags", control_flags)

    def on_end(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self

    def on_start(self, on_start: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_start", {"event": on_start, "target": subject})
        return self


class EntityAITimerFlag3(AIGoal):
    _identifier = "minecraft:behavior.timer_flag_3"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (10.0, 10.0),
        duration_range: tuple[Seconds, Seconds] = (2.0, 2.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Fires an event when this behavior starts, then waits for a duration before stopping. When stopping due to that timeout or due to being interrupted by another behavior, fires another event. query.timer_flag_3 will return 1.0 on both the client and server when this behavior is running, and 0.0 otherwise.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): Goal cooldown range in seconds. Can be a range object or a single number. Defaults to (10.0, 10.0).
            duration_range (tuple[Seconds, Seconds], optional): Goal duration range in seconds. Can be a range object or a single number. Defaults to (2.0, 2.0).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_timer_flag_3
        """
        super().__init__("behavior.timer_flag_3")

        if cooldown_range != (10.0, 10.0):
            self._add_field(
                "cooldown_range",
                AnvilFormatter.min_max_dict(cooldown_range, "cooldown_range"),
            )
        if duration_range != (2.0, 2.0):
            self._add_field(
                "duration_range",
                AnvilFormatter.min_max_dict(duration_range, "duration_range"),
            )
        if control_flags != []:
            self._add_field("control_flags", control_flags)

    def on_end(self, on_end: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_end", {"event": on_end, "target": subject})
        return self

    def on_start(self, on_start: str, subject: FilterSubject = FilterSubject.Self):
        self._add_field("on_start", {"event": on_start, "target": subject})
        return self


class EntityAIRunAroundLikeCrazy(AIGoal):
    _identifier = "minecraft:behavior.run_around_like_crazy"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to run around aimlessly.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_run_around_like_crazy
        """
        super().__init__("behavior.run_around_like_crazy")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAISlimeKeepOnJumping(AIGoal):
    _identifier = "minecraft:behavior.slime_keep_on_jumping"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the entity to continuously jump around like a slime.

        Parameters:
            speed_multiplier (float, optional): Determines the multiplier this entity's speed is modified by when jumping around. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_keep_on_jumping
        """
        super().__init__("behavior.slime_keep_on_jumping")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIRiseToLiquidLevel(AIGoal):
    _identifier = "minecraft:behavior.rise_to_liquid_level"

    def __init__(
        self,
        liquid_y_offset: float = 0.0,
        rise_delta: float = 0.0,
        sink_delta: float = 0.0,
    ) -> None:
        """Allows the mob to stay at a certain level when in liquid.

        Parameters:
            liquid_y_offset (float, optional): Target distance down from the liquid surface. i.e. Positive values move the target Y down. Defaults to 0.0.
            rise_delta (float, optional): Movement up in Y per tick when below the liquid surface. Defaults to 0.0.
            sink_delta (float, optional): Movement down in Y per tick when above the liquid surface. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_rise_to_liquid_level
        """
        super().__init__("behavior.rise_to_liquid_level")

        if liquid_y_offset != 0.0:
            self._add_field("liquid_y_offset", liquid_y_offset)
        if rise_delta != 0.0:
            self._add_field("rise_delta", rise_delta)
        if sink_delta != 0.0:
            self._add_field("sink_delta", sink_delta)


class EntityAITakeBlock(AIGoal):
    _identifier = "minecraft:behavior.take_block"

    def __init__(
        self,
        affected_by_griefing_rule: bool = False,
        blocks: list[MinecraftBlockDescriptor] = [],
        can_take: Filter = None,
        chance: float = 0.0,
        requires_line_of_sight: bool = False,
        xz_range: Vector2D = (0, 0),
        y_range: Vector2D = (0, 0),
    ):
        """AI goal that makes entities pick up blocks from the world, like Endermen grabbing blocks to carry. Configure which blocks the entity can take and the search radius. Works with place_block behavior to create entities that relocate blocks or harvest materials from the environment.

        Parameters:
            affected_by_griefing_rule (bool, optional): If true, whether the goal is affected by the mob griefing game rule. Defaults to False.
            blocks (list[MinecraftBlockDescriptor], optional): Block descriptors for which blocks are valid to be taken by the entity, if empty all blocks are valid. Defaults to [].
            can_take (Filter, optional): Filters for if the entity should try to take a block. Self and Target are set. Defaults to None.
            chance (float, optional): Chance each tick for the entity to try and take a block. Defaults to 0.0.
            requires_line_of_sight (bool, optional): If true, whether the entity needs line of sight to the block they are trying to take. Defaults to False.
            xz_range (Vector2D, optional): XZ range from which the entity will try and take blocks from. Defaults to (0, 0).
            y_range (Vector2D, optional): Y range from which the entity will try and take blocks from. Defaults to (0, 0).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_take_block
        """
        super().__init__("behavior.take_block")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.20.100")

        if affected_by_griefing_rule:
            self._add_field("affected_by_griefing_rule", affected_by_griefing_rule)
        if blocks:
            self._add_field("blocks", blocks)
        if can_take is not None:
            self._add_field("can_take", can_take)
        if chance != 0.0:
            self._add_field("chance", chance)
        if requires_line_of_sight:
            self._add_field("requires_line_of_sight", requires_line_of_sight)
        if xz_range != (0, 0):
            self._add_field("xz_range", xz_range)
        if y_range != (0, 0):
            self._add_field("y_range", y_range)

    def on_take(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets the event to be triggered when the entity successfully takes a block.

        Parameters:
            event (str): The name of the event to trigger.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        Returns:
            self: Returns the current instance for method chaining.
        """
        self._add_field("on_take", {"event": event, "target": target.value})
        return self


class EntityAIPlaceBlock(AIGoal):
    _identifier = "minecraft:behavior.place_block"

    def __init__(
        self,
        affected_by_griefing_rule: bool = False,
        can_place: Filter = None,
        chance: float = 0.0,
        placeable_carried_blocks: list[MinecraftBlockDescriptor] = [],
        xz_range: Vector2D = (0, 0),
        y_range: Vector2D = (0, 0),
    ) -> None:
        """AI goal that makes entities place blocks into the world, like Endermen placing their carried block or snow golems leaving snow trails. Configure which blocks can be placed, where they can be placed, and how often the entity attempts placement. Creates mobs that modify the environment.

        Parameters:
            affected_by_griefing_rule (bool, optional): If true, whether the goal is affected by the mob griefing game rule. Defaults to False.
            can_place (Filter, optional): Filters for if the entity should try to place its block. Self and Target are set. Defaults to None.
            chance (float, optional): Chance each tick for the entity to try and place a block. Defaults to 0.0.
            placeable_carried_blocks (list[MinecraftBlockDescriptor], optional): Block descriptors for which blocks are valid to be placed from the entity's carried item, if empty all blocks are valid. Defaults to [].
            xz_range (Vector2D, optional): XZ range from which the entity will try and place blocks in. Defaults to (0, 0).
            y_range (Vector2D, optional): Y range from which the entity will try and place blocks in. Defaults to (0, 0).

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_place_block
        """
        super().__init__("behavior.place_block")
        self._enforce_version(ENTITY_SERVER_VERSION, "1.20.100")

        if affected_by_griefing_rule:
            self._add_field("affected_by_griefing_rule", affected_by_griefing_rule)
        if can_place is not None:
            self._add_field("can_place", can_place)
        if chance:
            self._add_field("chance", chance)
        if placeable_carried_blocks:
            self._add_field("placeable_carried_blocks", placeable_carried_blocks)
        if xz_range != (0, 0):
            self._add_field("xz_range", xz_range)
        if y_range != (0, 0):
            self._add_field("y_range", y_range)
        self._add_field("randomly_placeable_blocks", [])

    def on_place(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets the event to be triggered when the entity successfully places a block.

        Parameters:
            event (str): The name of the event to trigger.
            target (FilterSubject, optional): The target of the event. Defaults to FilterSubject.Self.

        Returns:
            self: Returns the current instance for method chaining.
        """
        self._add_field("on_place", {"event": event, "target": target.value})
        return self

    def randomly_placeable_block(
        self,
        block: MinecraftBlockDescriptor,
        filter: Filter,
        states: dict[str, Any] = None,
    ):
        """Sets the block that the entity can randomly place.

        Parameters:
            block (MinecraftBlockDescriptor): The block descriptor for which the block should be randomly placed.
            filter (Filter): The filter that determines when the block can be placed.
            states (dict[str, Any], optional): The states of the block to be placed.

        Returns:
            self: Returns the current instance for method chaining.
        """
        self._get_field("randomly_placeable_blocks").append(
            {
                "block": {"name": block.name, "states": states if states else {}},
                "filter": filter,
            }
        )
        return self


class EntityAIMoveToRandomBlock(AIGoal):
    _identifier = "minecraft:behavior.move_to_random_block"

    def __init__(
        self,
        block_distance: float = 16,
        speed_multiplier: float = 1.0,
        within_radius: float = 0.0,
    ) -> None:
        """Allows mob to move towards a random block.

        Parameters:
            block_distance (float, optional): Defines the distance from the mob, in blocks, that the block to move to will be chosen. Defaults to 16.
            speed_multiplier (float, optional): Description. Defaults to 1.0.
            within_radius (float, optional): Defines the distance in blocks the mob has to be from the block for the movement to be finished. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_random_block
        """
        super().__init__("behavior.move_to_random_block")

        if block_distance != 16:
            self._add_field("block_distance", block_distance)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if within_radius != 0.0:
            self._add_field("within_radius", within_radius)


class EntityAIDig(AIGoal):
    _identifier = "minecraft:behavior.dig"

    def __init__(
        self,
        duration: Seconds = 0,
        idle_time: Seconds = 0,
        allow_dig_when_named: bool = False,
        digs_in_daylight: bool = False,
        suspicion_is_disturbance: bool = False,
        vibration_is_disturbance: bool = False,
    ) -> None:
        """Allows this entity to dig into the ground before despawning.

        Parameters:
            duration (Seconds, optional): Goal duration in seconds. Defaults to 0.
            idle_time (Seconds, optional): The minimum idle time in seconds between the last detected disturbance to the start of digging. Defaults to 0.
            allow_dig_when_named (bool, optional): If true, this behavior can run when this entity is named. Otherwise not. Defaults to False.
            digs_in_daylight (bool, optional): Indicates that the actor should start digging when it sees daylight. Defaults to False.
            suspicion_is_disturbance (bool, optional): If true, finding new suspicious locations count as disturbances that may delay the start of this goal. Defaults to False.
            vibration_is_disturbance (bool, optional): If true, vibrations count as disturbances that may delay the start of this goal. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_dig
        """
        super().__init__("behavior.dig")

        if duration != 0:
            self._add_field("duration", duration)
        if idle_time != 0:
            self._add_field("idle_time", idle_time)
        if allow_dig_when_named:
            self._add_field("allow_dig_when_named", allow_dig_when_named)
        if digs_in_daylight:
            self._add_field("digs_in_daylight", digs_in_daylight)
        if suspicion_is_disturbance:
            self._add_field("suspicion_is_disturbance", suspicion_is_disturbance)
        if vibration_is_disturbance:
            self._add_field("vibration_is_disturbance", vibration_is_disturbance)

    def on_start(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets an event to run when the dig goal starts.

        Parameters:
            event (str): The event name to trigger.
            target (FilterSubject, optional): The event target. Defaults to FilterSubject.Self.

        Returns:
            self: for chaining.
        """
        self._add_field("on_start", {"event": event, "target": target.value})
        return self


class EntityAIDrinkMilk(AIGoal):
    _identifier = "minecraft:behavior.drink_milk"

    def __init__(
        self,
        cooldown_seconds: Seconds = 5,
        filters: Filter = None,
    ) -> None:
        """Allows the mob to drink milk based on specified environment conditions.

        Parameters:
            cooldown_seconds (Seconds, optional): Time (in seconds) that the goal is on cooldown before it can be used again. Defaults to 5.
            filters (Filter, optional): Conditions that need to be met for the behavior to start. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drink_milk
        """
        super().__init__("behavior.drink_milk")

        if cooldown_seconds != 5:
            self._add_field("cooldown_seconds", cooldown_seconds)
        if filters is not None:
            self._add_field("filters", filters)


class EntityAIAvoidBlock(AIGoal):
    _identifier = "minecraft:behavior.avoid_block"

    def __init__(
        self,
        tick_interval: int = 1,
        search_range: int = 0,
        search_height: int = 0,
        walk_speed_modifier: float = 1.0,
        sprint_speed_modifier: float = 1.0,
        avoid_block_sound: str = None,
        sound_interval: list[float] = None,
        target_selection_method: Literal["nearest"] = "nearest",
        target_blocks: list[MinecraftBlockDescriptor] = [],
    ) -> None:
        """Allows this entity to avoid certain blocks.

        Parameters:
            tick_interval (int, optional): Should start tick interval. Defaults to 1.
            search_range (int, optional): Maximum distance to look for a block in xz. Defaults to 0.
            search_height (int, optional): Maximum distance to look for a block in y. Defaults to 0.
            walk_speed_modifier (float, optional): Modifier for walking speed. 1.0 means keep the regular speed, while higher numbers make the walking speed faster. Defaults to 1.0.
            sprint_speed_modifier (float, optional): Modifier for sprint speed. 1.0 means keep the regular speed, while higher numbers make the sprint speed faster. Defaults to 1.0.
            avoid_block_sound (str, optional): The sound event to play when the mob is avoiding a block. Defaults to None.
            sound_interval (list[float], optional): The range of time in seconds to randomly wait before playing the sound again. Defaults to None.
            target_selection_method (Literal['nearest'], optional): Block search method. Defaults to 'nearest'.
            target_blocks (list[MinecraftBlockDescriptor], optional): List of block types this mob avoids. Defaults to [].

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_avoid_block
        """
        super().__init__("behavior.avoid_block")

        if tick_interval != 1:
            self._add_field("tick_interval", tick_interval)
        if search_range != 0:
            self._add_field("search_range", search_range)
        if search_height != 0:
            self._add_field("search_height", search_height)
        if walk_speed_modifier != 1.0:
            self._add_field("walk_speed_modifier", walk_speed_modifier)
        if sprint_speed_modifier != 1.0:
            self._add_field("sprint_speed_modifier", sprint_speed_modifier)
        if avoid_block_sound is not None:
            self._add_field("avoid_block_sound", avoid_block_sound)
        if sound_interval is not None:
            if not isinstance(sound_interval, list):
                raise TypeError("sound_interval must be a list of two floats")
            if len(sound_interval) != 2:
                raise ValueError("sound_interval must be a list of two floats")
            self._add_field(
                "sound_interval",
                {"range_min": min(sound_interval), "range_max": max(sound_interval)},
            )
        if target_selection_method != "nearest":
            self._add_field("target_selection_method", target_selection_method)
        if target_blocks != []:
            self._add_field("target_blocks", target_blocks)

        self._add_field("on_escape", [])

    def on_escape(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Add an escape event to be triggered when the mob escapes the avoided block.

        Parameters:
            event (str): The event name to trigger.
            target (FilterSubject, optional): The event target. Defaults to FilterSubject.Self.

        Returns:
            self: for chaining.
        """
        self._get_field("on_escape").append({"event": event, "target": target.value})
        return self


class EntityAIUseKineticWeapon(AIGoal):
    _identifier = "minecraft:behavior.use_kinetic_weapon"

    def __init__(
        self,
        approach_distance: float = None,
        reposition_distance: float = None,
        reposition_speed_multiplier: float = None,
        cooldown_distance: float = None,
        cooldown_speed_multiplier: float = None,
        weapon_reach_multiplier: float = None,
        weapon_min_speed_multiplier: float = None,
        min_path_time: float = None,
        max_path_time: float = None,
        path_fail_time_increase: float = None,
        inner_boundary_time_increase: float = None,
        outer_boundary_time_increase: float = None,
        path_inner_boundary: float = None,
        path_outer_boundary: float = None,
        speed_multiplier: float = None,
        require_complete_path: bool = None,
        track_target: bool = None,
        cooldown_time: float = None,
        melee_fov: float = None,
        x_max_rotation: float = None,
        y_max_head_rotation: float = None,
        random_stop_interval: int = None,
        attack_once: bool = None,
        hijack_mount_navigation: bool = None,
    ) -> None:
        """Enables a mob to use kinetic weaponry by intermittently charging at its target and repositioning afterward.

        Parameters:
            approach_distance (float, optional): The distance to the target within which the mob begins using its kinetic weapon. Defaults to None.
            reposition_distance (float, optional): The distance the mob retreats to once the target is closer than the midpoint of the item's "minecraft:kinetic_weapon" component's minimum and maximum "reach". Defaults to None.
            reposition_speed_multiplier (float, optional): Multiplier applied to the mob's movement speed while repositioning. Defaults to None.
            cooldown_distance (float, optional): The distance the mob retreats to after all of the item's "minecraft:kinetic_weapon" component's "max_duration" values have elapsed. Defaults to None.
            cooldown_speed_multiplier (float, optional): Multiplier applied to the mob's movement speed while on cooldown. Defaults to None.
            weapon_reach_multiplier (float, optional): Multiplier applied to the item's "minecraft:kinetic_weapon" component's "reach". Defaults to None.
            weapon_min_speed_multiplier (float, optional): Multiplier applied to each "min_speed" and "min_relative_speed" condition in the item's "minecraft:kinetic_weapon" component. Defaults to None.
            min_path_time (float, optional): Minimum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to None.
            max_path_time (float, optional): Maximum base time, in seconds, before recalculating a new attack path to the target (before increases are applied). Defaults to None.
            path_fail_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the mob cannot move along the current path. Defaults to None.
            inner_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_inner_boundary". Defaults to None.
            outer_boundary_time_increase (float, optional): Time, in seconds, added to the attack path recalculation interval when the target is beyond "path_outer_boundary". Defaults to None.
            path_inner_boundary (float, optional): Distance at which to increase attack path recalculation by "inner_boundary_time_increase". Defaults to None.
            path_outer_boundary (float, optional): Distance at which to increase attack path recalculation by "outer_boundary_time_increase". Defaults to None.
            speed_multiplier (float, optional): Multiplier applied to the mob's movement speed when moving toward its target. Defaults to None.
            require_complete_path (bool, optional): Specifies whether a full navigation path from the mob to the target is required. Defaults to None.
            track_target (bool, optional): Allows the mob to track its target even if it lacks a hard-coded sensing component. Defaults to None.
            cooldown_time (float, optional): Cooldown time, in seconds, between consecutive attacks. Defaults to None.
            melee_fov (float, optional): Field of view, in degrees, used by the hard-coded sensing component to detect a valid attack target. Defaults to None.
            x_max_rotation (float, optional): Maximum rotation, in degrees, on the X-axis while the mob is trying to look at its target. Defaults to None.
            y_max_head_rotation (float, optional): Maximum rotation, in degrees, on the Y-axis while the mob is trying to look at its target. Defaults to None.
            random_stop_interval (int, optional): Defines a 1-in-N chance for the mob to stop its current attack, where N equals "random_stop_interval". Defaults to None.
            attack_once (bool, optional): Allows the mob to perform this melee attack behavior only once during its lifetime. Defaults to None.
            hijack_mount_navigation (bool, optional): Allows the mob to override its mount's navigation behavior with the logic defined by this goal. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_use_kinetic_weapon
        """
        super().__init__("behavior.use_kinetic_weapon")
        if approach_distance is not None:
            self._add_field("approach_distance", approach_distance)
        if reposition_distance is not None:
            self._add_field("reposition_distance", reposition_distance)
        if reposition_speed_multiplier is not None:
            self._add_field("reposition_speed_multiplier", reposition_speed_multiplier)
        if cooldown_distance is not None:
            self._add_field("cooldown_distance", cooldown_distance)
        if cooldown_speed_multiplier is not None:
            self._add_field("cooldown_speed_multiplier", cooldown_speed_multiplier)
        if weapon_reach_multiplier is not None:
            self._add_field("weapon_reach_multiplier", weapon_reach_multiplier)
        if weapon_min_speed_multiplier is not None:
            self._add_field("weapon_min_speed_multiplier", weapon_min_speed_multiplier)
        if min_path_time is not None:
            self._add_field("min_path_time", min_path_time)
        if max_path_time is not None:
            self._add_field("max_path_time", max_path_time)
        if path_fail_time_increase is not None:
            self._add_field("path_fail_time_increase", path_fail_time_increase)
        if inner_boundary_time_increase is not None:
            self._add_field(
                "inner_boundary_time_increase", inner_boundary_time_increase
            )
        if outer_boundary_time_increase is not None:
            self._add_field(
                "outer_boundary_time_increase", outer_boundary_time_increase
            )
        if path_inner_boundary is not None:
            self._add_field("path_inner_boundary", path_inner_boundary)
        if path_outer_boundary is not None:
            self._add_field("path_outer_boundary", path_outer_boundary)
        if speed_multiplier is not None:
            self._add_field("speed_multiplier", speed_multiplier)
        if require_complete_path is not None:
            self._add_field("require_complete_path", require_complete_path)
        if track_target is not None:
            self._add_field("track_target", track_target)
        if cooldown_time is not None:
            self._add_field("cooldown_time", cooldown_time)
        if melee_fov is not None:
            self._add_field("melee_fov", melee_fov)
        if x_max_rotation is not None:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_head_rotation is not None:
            self._add_field("y_max_head_rotation", y_max_head_rotation)
        if random_stop_interval is not None:
            self._add_field("random_stop_interval", random_stop_interval)
        if attack_once is not None:
            self._add_field("attack_once", attack_once)


class EntityAIHide(AIGoal):
    _identifier = "minecraft:behavior.hide"

    def __init__(
        self,
        duration: Seconds = 1.0,
        poi_type: str = None,
        speed_multiplier: float = 1.0,
        timeout_cooldown: float = 8.0,
    ) -> None:
        """Allows a mob with the hide component to attempt to move to - and hide at - an owned or nearby POI.

        Parameters:
            duration (Seconds, optional): Amount of time in seconds that the mob reacts. Defaults to 1.0.
            poi_type (str, optional): Tells the goal what POI type it should be looking for. Defaults to None.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.
            timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after a internal failure or timeout condition. Defaults to 8.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hide
        """
        super().__init__("behavior.hide")
        if duration != 1.0:
            self._add_field("duration", duration)
        if poi_type is not None:
            self._add_field("poi_type", poi_type)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if timeout_cooldown != 8.0:
            self._add_field("timeout_cooldown", timeout_cooldown)


class EntityAITradeWithPlayer(AIGoal):
    _identifier = "minecraft:behavior.trade_with_player"

    def __init__(
        self,
        filters: Filter = None,
        max_distance_from_player: float = 8.0,
    ) -> None:
        """Allows the player to trade with this mob. When the goal starts, it will stop the mob's navigation.

        Parameters:
            filters (Filter, optional): Conditions that need to be met for the behavior to start. Defaults to None.
            max_distance_from_player (float, optional): The max distance that the mob can be from the player before exiting the goal. Defaults to 8.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_trade_with_player
        """
        super().__init__("behavior.trade_with_player")

        if filters is not None:
            self._add_field("filters", filters)
        if max_distance_from_player != 8.0:
            self._add_field("max_distance_from_player", max_distance_from_player)


class EntityAIPickupItems(AIGoal):
    _identifier = "minecraft:behavior.pickup_items"

    def __init__(
        self,
        can_pickup_any_item: bool = False,
        can_pickup_to_hand_or_equipment: bool = True,
        cooldown_after_being_attacked: float = 0.0,
        excluded_items: list[str] = [],
        goal_radius: float = 0.5,
        max_dist: float = 0.0,
        pickup_based_on_chance: bool = False,
        pickup_same_items_as_in_hand: bool = False,
        search_height: float = 0.0,
        speed_multiplier: float = 1.0,
        track_target: bool = False,
    ) -> None:
        """Allows the mob to pick up items on the ground.

        Parameters:
            can_pickup_any_item (bool, optional): If true, the mob can pickup any item. Defaults to False.
            can_pickup_to_hand_or_equipment (bool, optional): If true, the mob can pickup items to its hand or armor slots. Defaults to True.
            cooldown_after_being_attacked (float, optional): Description. Defaults to 0.0.
            excluded_items (list[str], optional): List of items this mob will not pick up. Defaults to [].
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            max_dist (float, optional): Maximum distance this mob will look for items to pick up. Defaults to 0.0.
            pickup_based_on_chance (bool, optional): If true, depending on the difficulty, there is a random chance that the mob may not be able to pickup items. Defaults to False.
            pickup_same_items_as_in_hand (bool, optional): If true, the mob will only pick up items that match what it is already holding. Defaults to False.
            search_height (float, optional): Description. Defaults to 0.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            track_target (bool, optional): If true, this mob will chase after the target as long as it's a valid target. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_pickup_items
        """
        super().__init__("behavior.pickup_items")

        if can_pickup_any_item:
            self._add_field("can_pickup_any_item", can_pickup_any_item)
        if not can_pickup_to_hand_or_equipment:
            self._add_field(
                "can_pickup_to_hand_or_equipment", can_pickup_to_hand_or_equipment
            )
        if cooldown_after_being_attacked != 0.0:
            self._add_field(
                "cooldown_after_being_attacked", cooldown_after_being_attacked
            )
        if excluded_items:
            self._add_field("excluded_items", excluded_items)
        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if max_dist != 0.0:
            self._add_field("max_dist", max_dist)
        if pickup_based_on_chance:
            self._add_field("pickup_based_on_chance", pickup_based_on_chance)
        if pickup_same_items_as_in_hand:
            self._add_field(
                "pickup_same_items_as_in_hand", pickup_same_items_as_in_hand
            )
        if search_height != 0.0:
            self._add_field("search_height", search_height)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if track_target:
            self._add_field("track_target", track_target)


class EntityAIMoveIndoors(AIGoal):
    _identifier = "minecraft:behavior.move_indoors"

    def __init__(
        self,
        speed_multiplier: float = 0.8,
        timeout_cooldown: float = 8.0,
    ) -> None:
        """Allows this entity to move indoors.

        Parameters:
            speed_multiplier (float, optional): The movement speed modifier to apply to the entity while it is moving indoors. Defaults to 0.8.
            timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after pathfinding fails. Defaults to 8.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_indoors
        """
        super().__init__("behavior.move_indoors")

        if speed_multiplier != 0.8:
            self._add_field("speed_multiplier", speed_multiplier)
        if timeout_cooldown != 8.0:
            self._add_field("timeout_cooldown", timeout_cooldown)


class EntityAILookAtTradingPlayer(AIGoal):
    _identifier = "minecraft:behavior.look_at_trading_player"

    def __init__(
        self,
        angle_of_view_horizontal: int = 360,
        angle_of_view_vertical: int = 360,
        look_distance: float = 8.0,
        look_time: tuple[int, int] = None,
        probability: float = 0.02,
    ) -> None:
        """Compels an entity to look at the player that is currently trading with the entity.

        Parameters:
            angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Value must be <= 360. Defaults to 360.
            angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Value must be <= 360. Defaults to 360.
            look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Defaults to 8.0.
            look_time (tuple[int, int], optional): Time range to look at the nearest entity. Defaults to None.
            probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Value must be <= 1. Defaults to 0.02.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_trading_player
        """
        super().__init__("behavior.look_at_trading_player")

        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time is not None:
            self._add_field(
                "look_time", AnvilFormatter.min_max_dict(look_time, "look_time")
            )

        if probability != 0.02:
            self._add_field("probability", probability)


class EntityAIShareItems(AIGoal):
    _identifier = "minecraft:behavior.share_items"

    def __init__(
        self,
        entity_types: Filter = None,
        goal_radius: float = 0.5,
        max_dist: float = 0.0,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to give items it has to others.

        Parameters:
            entity_types (Filter, optional): List of entities this mob will share items with. Defaults to None.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            max_dist (float, optional): Maximum distance this mob can be away to be a valid choice. Defaults to 0.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_share_items
        """
        super().__init__("behavior.share_items")

        if entity_types is not None:
            self._add_field("entity_types", [{"filters": entity_types}])
        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if max_dist != 0.0:
            self._add_field("max_dist", max_dist)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIMoveTowardsDwellingRestriction(AIGoal):
    _identifier = "minecraft:behavior.move_towards_dwelling_restriction"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows entities with the "minecraft:dweller" component to move toward their village area that the entity should be restricted to.

        Parameters:
            speed_multiplier (float, optional): This multiplier modifies the entity's speed when moving towards its restriction. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_dwelling_restriction
        """
        super().__init__("behavior.move_towards_dwelling_restriction")
        # self._require_components(EntityDweller)

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAITradeInterest(AIGoal):
    _identifier = "minecraft:behavior.trade_interest"

    def __init__(
        self,
        carried_item_switch_time: float = 2.0,
        cooldown: float = 2.0,
        interest_time: float = 45.0,
        remove_item_time: float = 1.0,
        within_radius: float = 0.0,
    ) -> None:
        """Allows the mob to look at a player that is holding a tradable item.

        Parameters:
            carried_item_switch_time (float, optional): The max time in seconds that the trader will hold an item before attempting to switch for a different item that takes the same trade. Defaults to 2.0.
            cooldown (float, optional): The time in seconds before the trader can use this goal again. Defaults to 2.0.
            interest_time (float, optional): The max time in seconds that the trader will be interested with showing its trade items. Defaults to 45.0.
            remove_item_time (float, optional): The max time in seconds that the trader will wait when you no longer have items to trade. Defaults to 1.0.
            within_radius (float, optional): Distance in blocks this mob can be interested by a player holding an item they like. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_trade_interest
        """
        super().__init__("behavior.trade_interest")

        if carried_item_switch_time != 2.0:
            self._add_field("carried_item_switch_time", carried_item_switch_time)
        if cooldown != 2.0:
            self._add_field("cooldown", cooldown)
        if interest_time != 45.0:
            self._add_field("interest_time", interest_time)
        if remove_item_time != 1.0:
            self._add_field("remove_item_time", remove_item_time)
        if within_radius != 0.0:
            self._add_field("within_radius", within_radius)


class EntityAIMakeLove(AIGoal):
    _identifier = "minecraft:behavior.make_love"

    def __init__(self) -> None:
        """Allows the villager to look for a mate to spawn other villagers with.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_make_love
        """
        super().__init__("behavior.make_love")


class EntityAIReceiveLove(AIGoal):
    _identifier = "minecraft:behavior.receive_love"

    def __init__(self) -> None:
        """Allows the villager to stop so another villager can breed with it. Can only be used by a Villager.

        Parameters:

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_receive_love
        """
        super().__init__("behavior.receive_love")


class EntityAIWork(AIGoal):
    _identifier = "minecraft:behavior.work"

    def __init__(
        self,
        active_time: int = 0,
        can_work_in_rain: bool = False,
        goal_cooldown: int = 0,
        on_arrival: str = None,
        sound_delay_max: int = 0,
        sound_delay_min: int = 0,
        speed_multiplier: float = 0.5,
        work_in_rain_tolerance: int = -1,
    ) -> None:
        """Allows the NPC to use the POI.

        Parameters:
            active_time (int, optional): The amount of ticks the NPC will stay in their the work location. Defaults to 0.
            can_work_in_rain (bool, optional): If true, this entity can work when their jobsite POI is being rained on. Defaults to False.
            goal_cooldown (int, optional): The amount of ticks the goal will be on cooldown before it can be used again. Defaults to 0.
            on_arrival (str, optional): Event to run when the mob reaches their jobsite. Defaults to None.
            sound_delay_max (int, optional): The max interval in which a sound will play. Defaults to 0.
            sound_delay_min (int, optional): The min interval in which a sound will play. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal Value must be > 0. Defaults to 0.5.
            work_in_rain_tolerance (int, optional): If "can_work_in_rain" is false, this is the maximum number of ticks left in the goal where rain will not interrupt the goal. Defaults to -1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_work
        """
        super().__init__("behavior.work")

        if active_time != 0:
            self._add_field("active_time", active_time)
        if can_work_in_rain:
            self._add_field("can_work_in_rain", can_work_in_rain)
        if goal_cooldown != 0:
            self._add_field("goal_cooldown", goal_cooldown)
        if on_arrival is not None:
            self._add_field("on_arrival", {"event": on_arrival, "target": "self"})
        if sound_delay_max != 0:
            self._add_field("sound_delay_max", sound_delay_max)
        if sound_delay_min != 0:
            self._add_field("sound_delay_min", sound_delay_min)
        if speed_multiplier != 0.5:
            self._add_field("speed_multiplier", speed_multiplier)
        if work_in_rain_tolerance != -1:
            self._add_field("work_in_rain_tolerance", work_in_rain_tolerance)


class EntityAIWorkComposter(AIGoal):
    _identifier = "minecraft:behavior.work_composter"

    def __init__(
        self,
        active_time: int = 0,
        block_interaction_max: int = 1,
        can_empty_composter: bool = True,
        can_fill_composter: bool = True,
        can_work_in_rain: bool = False,
        goal_cooldown: int = 0,
        items_per_use_max: int = 20,
        min_item_count: int = 10,
        on_arrival: str = None,
        speed_multiplier: float = 0.5,
        use_block_max: int = 200,
        use_block_min: int = 100,
        work_in_rain_tolerance: int = -1,
    ) -> None:
        """Allows the NPC to use the composter POI to convert excess seeds into bone meal.

        Parameters:
            active_time (int, optional): The amount of ticks the NPC will stay in their the work location. Defaults to 0.
            block_interaction_max (int, optional): The maximum number of times the mob will interact with the composter. Defaults to 1.
            can_empty_composter (bool, optional): Determines whether the mob can empty a full composter. Defaults to True.
            can_fill_composter (bool, optional): Determines whether the mob can add items to a composter given that it is not full. Defaults to True.
            can_work_in_rain (bool, optional): If true, this entity can work when their jobsite POI is being rained on. Defaults to False.
            goal_cooldown (int, optional): The amount of ticks the goal will be on cooldown before it can be used again. Defaults to 0.
            items_per_use_max (int, optional): The maximum number of items which can be added to the composter per block interaction. Defaults to 20.
            min_item_count (int, optional): Limits the amount of each compostable item the mob can use. Any amount held over this number will be composted if possible. Defaults to 10.
            on_arrival (str, optional): Event to run when the mob reaches their jobsite. Defaults to None.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal Value must be > 0. Defaults to 0.5.
            use_block_max (int, optional): The maximum interval in which the mob will interact with the composter. Defaults to 200.
            use_block_min (int, optional): The minimum interval in which the mob will interact with the composter. Defaults to 100.
            work_in_rain_tolerance (int, optional): If "can_work_in_rain" is false, this is the maximum number of ticks left in the goal where rain will not interrupt the goal. Defaults to -1.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_work_composter
        """
        super().__init__("behavior.work_composter")

        if active_time != 0:
            self._add_field("active_time", active_time)
        if block_interaction_max != 1:
            self._add_field("block_interaction_max", block_interaction_max)
        if not can_empty_composter:
            self._add_field("can_empty_composter", can_empty_composter)
        if not can_fill_composter:
            self._add_field("can_fill_composter", can_fill_composter)
        if can_work_in_rain:
            self._add_field("can_work_in_rain", can_work_in_rain)
        if goal_cooldown != 0:
            self._add_field("goal_cooldown", goal_cooldown)
        if items_per_use_max != 20:
            self._add_field("items_per_use_max", items_per_use_max)
        if min_item_count != 10:
            self._add_field("min_item_count", min_item_count)
        if on_arrival is not None:
            self._add_field("on_arrival", {"event": on_arrival, "target": "self"})
        if speed_multiplier != 0.5:
            self._add_field("speed_multiplier", speed_multiplier)
        if use_block_max != 200:
            self._add_field("use_block_max", use_block_max)
        if use_block_min != 100:
            self._add_field("use_block_min", use_block_min)
        if work_in_rain_tolerance != -1:
            self._add_field("work_in_rain_tolerance", work_in_rain_tolerance)


class EntityAIHarvestFarmBlock(AIGoal):
    _identifier = "minecraft:behavior.harvest_farm_block"

    def __init__(
        self,
        goal_radius: float = 1.5,
        max_seconds_before_search: float = 1.0,
        search_cooldown_max_seconds: float = 8.0,
        search_count: int = 0,
        search_height: int = 1,
        search_range: int = 16,
        seconds_until_new_task: float = 0.5,
        speed_multiplier: float = 0.5,
    ) -> None:
        """Allows the entity to search within an area for farmland with air above it. If found, the entity will replace the air block by planting a seed item from its inventory on the farmland block. This goal will not execute if the entity does not have an item in its inventory.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the entity considers it has reached it's target position. Value must be > 0. Defaults to 1.5.
            max_seconds_before_search (float, optional): The maximum amount of time in seconds that the goal can take before searching for the first harvest block. The time is chosen between 0 and this number. Value must be > 0. Defaults to 1.0.
            search_cooldown_max_seconds (float, optional): The maximum amount of time in seconds that the goal can take before searching again, after failing to find a a harvest block already. The time is chosen between 0 and this number. Value must be > 0. Defaults to 8.0.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 0.
            search_height (int, optional): The height in blocks the entity will search within to find a valid target position. Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks the entity will search within to find a valid target position. Value must be > 0. Defaults to 16.
            seconds_until_new_task (float, optional): The amount of time in seconds that the goal will cooldown after a successful reap/sow, before it can start again. Value must be > 0. Defaults to 0.5.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 0.5.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_harvest_farm_block
        """
        super().__init__("behavior.harvest_farm_block")
        self._require_components(EntityInventory)

        if goal_radius != 1.5:
            self._add_field("goal_radius", goal_radius)
        if max_seconds_before_search != 1.0:
            self._add_field("max_seconds_before_search", max_seconds_before_search)
        if search_cooldown_max_seconds != 8.0:
            self._add_field("search_cooldown_max_seconds", search_cooldown_max_seconds)
        if search_count != 0:
            self._add_field("search_count", search_count)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 16:
            self._add_field("search_range", search_range)
        if seconds_until_new_task != 0.5:
            self._add_field("seconds_until_new_task", seconds_until_new_task)
        if speed_multiplier != 0.5:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIFertilizeFarmBlock(AIGoal):
    _identifier = "minecraft:behavior.fertilize_farm_block"

    def __init__(
        self,
        goal_radius: float = 1.5,
        max_fertilizer_usage: int = 1,
        search_cooldown_max_seconds: float = 8.0,
        search_count: int = 9,
        search_height: int = 1,
        search_range: int = 1,
        speed_multiplier: float = 0.5,
    ) -> None:
        """Allows the mob to search within an area for a growable crop block. If found, the mob will use any available fertilizer in their inventory on the crop. This goal will not execute if the mob does not have a fertilizer item in its inventory.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached it's target position. Value must be > 0. Defaults to 1.5.
            max_fertilizer_usage (int, optional): The maximum number of times the mob will use fertilzer on the target block. Value must be > 0. Defaults to 1.
            search_cooldown_max_seconds (float, optional): The maximum amount of time in seconds that the goal can take before searching again. The time is chosen between 0 and this number. Value must be > 0. Defaults to 8.0.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 9.
            search_height (int, optional): The height in blocks the mob will search within to find a valid target position. Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks the mob will search within to find a valid target position. Value must be > 0. Defaults to 1.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 0.5.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_fertilize_farm_block
        """
        super().__init__("behavior.fertilize_farm_block")

        if goal_radius != 1.5:
            self._add_field("goal_radius", goal_radius)
        if max_fertilizer_usage != 1:
            self._add_field("max_fertilizer_usage", max_fertilizer_usage)
        if search_cooldown_max_seconds != 8.0:
            self._add_field("search_cooldown_max_seconds", search_cooldown_max_seconds)
        if search_count != 9:
            self._add_field("search_count", search_count)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 1:
            self._add_field("search_range", search_range)
        if speed_multiplier != 0.5:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIPlay(AIGoal):
    _identifier = "minecraft:behavior.play"

    def __init__(
        self,
        chance_to_start: float = 0.0,
        follow_distance: int = 2,
        friend_search_area: Coordinates = (6, 3, 6),
        friend_types: Filter = None,
        max_play_duration_seconds: float = 50.0,
        random_pos_search_height: int = 3,
        random_pos_search_range: int = 16,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to offer a flower to another mob with the minecraft:take_flower behavior.

        Parameters:
            chance_to_start (float, optional): Percent chance that the mob will start this goal, from 0 to 1. Value must be <= 1. Defaults to 0.0.
            follow_distance (int, optional): The distance (in blocks) that the mob tries to be in range of the friend it's following. Defaults to 2.
            friend_search_area (Coordinates, optional): The dimensions of the AABB used to search for a potential friend to play with. Defaults to (6, 3, 6).
            friend_types (Filter, optional): The entity type(s) to consider when searching for a potential friend to play with. Defaults to None.
            max_play_duration_seconds (float, optional): The max amount of seconds that the mob will play for before exiting the Goal. Defaults to 50.0.
            random_pos_search_height (int, optional): The height (in blocks) that the mob will search within to find a random position position to move to. Must be at least 1. Value must be >= 1. Defaults to 3.
            random_pos_search_range (int, optional): The distance (in blocks) on ground that the mob will search within to find a random position to move to. Must be at least 1. Value must be >= 1. Defaults to 16.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_play
        """
        super().__init__("behavior.play")

        if chance_to_start != 0.0:
            self._add_field("chance_to_start", chance_to_start)
        if follow_distance != 2:
            self._add_field("follow_distance", follow_distance)
        if friend_search_area != (6, 3, 6):
            self._add_field("friend_search_area", friend_search_area)
        if friend_types is not None:
            self._add_field("friend_types", friend_types)
        if max_play_duration_seconds != 50.0:
            self._add_field("max_play_duration_seconds", max_play_duration_seconds)
        if random_pos_search_height != 3:
            self._add_field("random_pos_search_height", random_pos_search_height)
        if random_pos_search_range != 16:
            self._add_field("random_pos_search_range", random_pos_search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIMingle(AIGoal):
    _identifier = "minecraft:behavior.mingle"

    def __init__(
        self,
        cooldown_time: float = 0.0,
        duration: float = 1.0,
        mingle_distance: float = 2.0,
        mingle_partner_type: list[str] = [],
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows an entity to go to the village bell and mingle with other entities.

        Parameters:
            cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.0.
            duration (float, optional): Amount of time in seconds that the entity will chat with another entity. Defaults to 1.0.
            mingle_distance (float, optional): The distance from its partner that this entity will mingle. If the entity type is not the same as the entity, this value needs to be identical on both entities. Defaults to 2.0.
            mingle_partner_type (list[str], optional): The entity type that this entity is allowed to mingle with. Defaults to [].
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_mingle
        """
        super().__init__("behavior.mingle")

        if cooldown_time != 0.0:
            self._add_field("cooldown_time", cooldown_time)
        if duration != 1.0:
            self._add_field("duration", duration)
        if mingle_distance != 2.0:
            self._add_field("mingle_distance", mingle_distance)
        if mingle_partner_type:
            self._add_field("mingle_partner_type", mingle_partner_type)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAISleep(AIGoal):
    _identifier = "minecraft:behavior.sleep"

    def __init__(
        self,
        can_sleep_while_riding: bool = False,
        cooldown_time: float = 0.0,
        goal_radius: float = None,
        sleep_collider_height: float = 1.0,
        sleep_collider_width: float = 1.0,
        sleep_y_offset: float = 1.0,
        speed_multiplier: float = 1.0,
        timeout_cooldown: float = 8.0,
    ) -> None:
        """Allows mobs that own a bed to in a village to move to and sleep in it.

        Parameters:
            can_sleep_while_riding (bool, optional): If true, the mob will be able to use the sleep goal if riding something. Defaults to False.
            cooldown_time (float, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.0.
            goal_radius (float, optional): Description. Defaults to None.
            sleep_collider_height (float, optional): The height of the mob's collider while sleeping. Defaults to 1.0.
            sleep_collider_width (float, optional): The width of the mob's collider while sleeping. Defaults to 1.0.
            sleep_y_offset (float, optional): The y offset of the mob's collider while sleeping. Defaults to 1.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.
            timeout_cooldown (float, optional): The cooldown time in seconds before the goal can be reused after a internal failure or timeout condition. Defaults to 8.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sleep
        """
        super().__init__("behavior.sleep")

        if can_sleep_while_riding:
            self._add_field("can_sleep_while_riding", can_sleep_while_riding)
        if cooldown_time != 0.0:
            self._add_field("cooldown_time", cooldown_time)
        if goal_radius is not None:
            self._add_field("goal_radius", goal_radius)
        if sleep_collider_height != 1.0:
            self._add_field("sleep_collider_height", sleep_collider_height)
        if sleep_collider_width != 1.0:
            self._add_field("sleep_collider_width", sleep_collider_width)
        if sleep_y_offset != 1.0:
            self._add_field("sleep_y_offset", sleep_y_offset)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if timeout_cooldown != 8.0:
            self._add_field("timeout_cooldown", timeout_cooldown)


class EntityAIExploreOutskirts(AIGoal):
    _identifier = "minecraft:behavior.explore_outskirts"

    def __init__(
        self,
        dist_from_boundary: Coordinates = (5, 0, 5),
        explore_dist: float = 5.0,
        max_travel_time: float = 60.0,
        max_wait_time: float = 0.0,
        min_dist_from_target: float = 2.2,
        min_perimeter: float = 1.0,
        min_wait_time: float = 3.0,
        next_xz: int = 5,
        next_y: int = 3,
        speed_multiplier: float = 1.0,
        timer_ratio: float = 2.0,
    ) -> None:
        """Allows the entity to first travel to a random point on the outskirts of the village, and then explore random points within a small distance.

        Parameters:
            dist_from_boundary (Coordinates, optional): The distance from the boundary the villager must be within in to explore the outskirts. Defaults to (5, 0, 5).
            explore_dist (float, optional): Total distance in blocks the the entity will explore beyond the village bounds when choosing its travel point. Defaults to 5.0.
            max_travel_time (float, optional): This is the maximum amount of time an entity will attempt to reach it's travel point on the outskirts of the village before the goal exits. Defaults to 60.0.
            max_wait_time (float, optional): The wait time in seconds between choosing new explore points will be chosen on a random interval between this value and the minimum wait time. Defaults to 0.0.
            min_dist_from_target (float, optional): The entity must be within this distance for it to consider it has successfully reached its target. Defaults to 2.2.
            min_perimeter (float, optional): The minimum perimeter of the village required to run this goal. Defaults to 1.0.
            min_wait_time (float, optional): The wait time in seconds between choosing new explore points will be chosen on a random interval between this value and the maximum wait time. Defaults to 3.0.
            next_xz (int, optional): A new explore point will randomly be chosen within this XZ distance of the current target position when navigation has finished and the wait timer has elapsed. Defaults to 5.
            next_y (int, optional): A new explore point will randomly be chosen within this Y distance of the current target position when navigation has finished and the wait timer has elapsed. Defaults to 3.
            speed_multiplier (float, optional): The multiplier for speed while using this goal. 1.0 maintains the speed. Defaults to 1.0.
            timer_ratio (float, optional): Each new explore point will be chosen on a random interval between the minimum and the maximum wait time, divided by this value. Defaults to 2.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_explore_outskirts
        """
        super().__init__("behavior.explore_outskirts")
        # self._require_components(EntityDweller)

        if dist_from_boundary != (5, 0, 5):
            self._add_field("dist_from_boundary", dist_from_boundary)
        if explore_dist != 5.0:
            self._add_field("explore_dist", explore_dist)
        if max_travel_time != 60.0:
            self._add_field("max_travel_time", max_travel_time)
        if max_wait_time != 0.0:
            self._add_field("max_wait_time", max_wait_time)
        if min_dist_from_target != 2.2:
            self._add_field("min_dist_from_target", min_dist_from_target)
        if min_perimeter != 1.0:
            self._add_field("min_perimeter", min_perimeter)
        if min_wait_time != 3.0:
            self._add_field("min_wait_time", min_wait_time)
        if next_xz != 5:
            self._add_field("next_xz", next_xz)
        if next_y != 3:
            self._add_field("next_y", next_y)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if timer_ratio != 2.0:
            self._add_field("timer_ratio", timer_ratio)


class EntityAIBreed(AIGoal):
    _identifier = "minecraft:behavior.breed"

    def __init__(self, speed_multiplier: float = 1.0) -> None:
        """Allows this mob to breed with other mobs.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier applied to the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_breed
        """
        super().__init__("behavior.breed")
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIInspectBookshelf(AIGoal):
    _identifier = "minecraft:behavior.inspect_bookshelf"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to inspect bookshelves.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 10.
            search_height (int, optional): The height that the mob will search for bookshelves. Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks the mob will look for books to inspect. Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_inspect_bookshelf
        """
        super().__init__("behavior.inspect_bookshelf")

        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if search_count != 10:
            self._add_field("search_count", search_count)
        if search_height != 1:
            self._add_field("search_height", search_height)
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAIRandomFly(AIGoal):
    _identifier = "minecraft:behavior.random_fly"

    def __init__(
        self,
        avoid_damage_blocks: bool = False,
        can_land_on_trees: bool = True,
        speed_multiplier: float = 1.0,
        xz_dist: int = 10,
        y_dist: int = 7,
        y_offset: float = 0.0,
    ) -> None:
        """Allows a mob to randomly fly around.

        Parameters:
            avoid_damage_blocks (bool, optional): If true, the mob will avoid blocks that cause damage when flying. Defaults to False.
            can_land_on_trees (bool, optional): If true, the mob can stop flying and land on a tree instead of the ground. Defaults to True.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            xz_dist (int, optional): Distance in blocks on ground that the mob will look for a new spot to move to. Must be at least 1. Defaults to 10.
            y_dist (int, optional): Distance in blocks that the mob will look up or down for a new spot to move to. Must be at least 1. Defaults to 7.
            y_offset (float, optional): Description. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_fly
        """
        super().__init__("behavior.random_fly")

        if avoid_damage_blocks:
            self._add_field("avoid_damage_blocks", avoid_damage_blocks)
        if not can_land_on_trees:
            self._add_field("can_land_on_trees", can_land_on_trees)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)
        if xz_dist != 10:
            self._add_field("xz_dist", max(1, xz_dist))
        if y_dist != 7:
            self._add_field("y_dist", max(1, y_dist))
        if y_offset != 0.0:
            self._add_field("y_offset", y_offset)


class EntityAICircleAroundAnchor(AIGoal):
    _identifier = "minecraft:behavior.circle_around_anchor"

    def __init__(
        self,
        angle_change: float = 15.0,
        goal_radius: float = 0.5,
        height_above_target_range: tuple[int, int] = None,
        height_adjustment_chance: float = 0.002857,
        height_offset_range: tuple[int, int] = None,
        radius_adjustment_chance: float = 0.004,
        radius_change: float = 1.0,
        radius_range: tuple[int, int] = None,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Causes an entity to circle around an anchor point placed near a point or target.

        Parameters:
            angle_change (float, optional): Number of degrees to change this entity's facing by, when the entity selects its next anchor point. Defaults to 15.0.
            goal_radius (float, optional): Maximum distance from the anchor-point in which this entity considers itself to have reached the anchor point. Defaults to 0.5.
            height_above_target_range (tuple[int, int], optional): The number of blocks above the target that the next anchor point can be set. Defaults to None.
            height_adjustment_chance (float, optional): Percent chance to determine how often to increase or decrease the current height around the anchor point. Defaults to 0.002857.
            height_offset_range (tuple[int, int], optional): Vertical distance from the anchor point this entity must stay within, upon a successful height adjustment. Defaults to None.
            radius_adjustment_chance (float, optional): Percent chance to determine how often to increase the size of the current movement radius around the anchor point. Defaults to 0.004.
            radius_change (float, optional): The number of blocks to increase the current movement radius by, upon successful "radius_adjustment_chance". Defaults to 1.0.
            radius_range (tuple[int, int], optional): Horizontal distance from the anchor point this entity must stay within upon a successful radius adjustment. Defaults to None.
            speed_multiplier (float, optional): Multiplies the speed at which this entity travels to its next desired position. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_circle_around_anchor
        """
        super().__init__("behavior.circle_around_anchor")

        if angle_change != 15.0:
            self._add_field("angle_change", angle_change)
        if goal_radius != 0.5:
            self._add_field("goal_radius", goal_radius)
        if height_above_target_range is not None:
            self._add_field(
                "height_above_target_range",
                AnvilFormatter.min_max_dict(
                    height_above_target_range,
                    "height_above_target_range",
                ),
            )
        if height_adjustment_chance != 0.002857:
            self._add_field("height_adjustment_chance", height_adjustment_chance)
        if height_offset_range is not None:
            self._add_field(
                "height_offset_range",
                AnvilFormatter.min_max_dict(height_offset_range, "height_offset_range"),
            )
        if radius_adjustment_chance != 0.004:
            self._add_field("radius_adjustment_chance", radius_adjustment_chance)
        if radius_change != 1.0:
            self._add_field("radius_change", radius_change)
        if radius_range is not None:
            self._add_field(
                "radius_range",
                AnvilFormatter.min_max_dict(radius_range, "radius_range"),
            )
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAISwoopAttack(AIGoal):
    _identifier = "minecraft:behavior.swoop_attack"

    def __init__(
        self,
        damage_reach: float = 0.2,
        delay_range: tuple[Seconds, Seconds] = None,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows an entity to attack using swoop attack behavior; Ideal for use with flying mobs. The behavior ends if the entity has a horizontal collision or gets hit.

        Parameters:
            damage_reach (float, optional): Added to the base size of the entity, to determine the target's maximum allowable distance, when trying to deal attack damage. Defaults to 0.2.
            delay_range (tuple[Seconds, Seconds], optional): Minimum and maximum cooldown time-range (in seconds) between each attempted swoop attack. Defaults to None.
            speed_multiplier (float, optional): During swoop attack behavior, this determines the multiplier the entity's speed is modified by when moving toward the target. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swoop_attack
        """
        super().__init__("behavior.swoop_attack")

        if damage_reach != 0.2:
            self._add_field("damage_reach", damage_reach)
        if delay_range is not None:
            self._add_field(
                "delay_range", AnvilFormatter.min_max_dict(delay_range, "delay_range")
            )
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", speed_multiplier)


class EntityAISwimUpForBreath(AIGoal):
    _identifier = "minecraft:behavior.swim_up_for_breath"

    def __init__(
        self,
        material_type: Literal["water", "lava", "any"] = "water",
        search_height: int = 16,
        search_radius: int = 4,
        speed_mod: float = 1.4,
    ) -> None:
        """Allows the mob to try to move to air once it is close to running out of its total breathable supply. Requires "minecraft:breathable".

        Parameters:
            material_type (str, optional): The material the mob is traveling in. An air block will only be considered valid to move to with a block of this material below it. Options are: "water", "lava", or "any". Defaults to "water".
            search_height (int, optional): The height (in blocks) above the mob's current position that it will search for a valid air block to move to. Defaults to 16.
            search_radius (int, optional): The radius (in blocks) around the mob's current position that it will search for a valid air block to move to. Defaults to 4.
            speed_mod (float, optional): Movement speed multiplier of the mob when using this Goal. Defaults to 1.4.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_up_for_breath
        """
        super().__init__("behavior.swim_up_for_breath")
        self._require_components(EntityBreathable)

        if material_type != "water":
            self._add_field("material_type", material_type)
        if search_height != 16:
            self._add_field("search_height", search_height)
        if search_radius != 4:
            self._add_field("search_radius", search_radius)
        if speed_mod != 1.4:
            self._add_field("speed_mod", speed_mod)


class EntityAIAdmireItem(AIGoal):
    _identifier = "minecraft:behavior.admire_item"

    def __init__(
        self,
        admire_item_sound: str = None,
        sound_interval: Seconds | tuple[Seconds, Seconds] = 0.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Enables the mob to admire items that have been configured as admirable.

        Parameters:
            admire_item_sound (str, optional): The sound event to play when admiring the item. Defaults to None.
            sound_interval (Seconds | tuple[Seconds, Seconds], optional): The range of time in seconds to randomly wait before playing the sound again. Can be a number, an array [min, max], or an object with range_min and range_max. Defaults to 0.0.

        Note:
            Requires `minecraft:admire_item` in order to work properly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_admire_item
        """
        super().__init__("behavior.admire_item")
        self._require_components(EntityAdmireItem)

        if admire_item_sound is not None:
            self._add_field("admire_item_sound", admire_item_sound)
        if sound_interval != 0.0:
            if isinstance(sound_interval, (tuple, list)):
                self._add_field(
                    "sound_interval",
                    AnvilFormatter.min_max_dict(sound_interval, "sound_interval"),
                )
            else:
                self._add_field("sound_interval", max(0.0, sound_interval))
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def on_admire_item_start(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_admire_item_start", trigger)
        return self

    def on_admire_item_stop(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_admire_item_stop", trigger)
        return self


class EntityAIBarter(AIGoal):
    _identifier = "minecraft:behavior.barter"

    def __init__(self, *control_flags: ControlFlags) -> None:
        """Enables the mob to barter for items that have been configured as barter currency. Must be used in combination with the barter component.

        This component has no configurable constructor properties beyond optional control flags.

        Note:
            Requires `minecraft:barter` and a barter table in order to work properly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_barter
        """
        super().__init__("behavior.barter")
        self._require_components(EntityBarter)

        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIBeg(AIGoal):
    _identifier = "minecraft:behavior.beg"

    def __init__(
        self,
        items: list[MinecraftItemDescriptor | Identifier],
        look_distance: float = 8.0,
        look_time: int | tuple[int, int] = None,
    ) -> None:
        """Allows this mob to look at and follow the player that holds food they like.

        Parameters:
            items (list[MinecraftItemDescriptor | Identifier]): List of items that this mob likes.
            look_distance (float, optional): Distance in blocks the mob will beg from. Defaults to 8.0.
            look_time (int | tuple[int, int], optional): The range of time in seconds this mob will stare at the player holding a food they like, begging for it. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_beg
        """
        super().__init__("behavior.beg")
        self._add_field("items", [str(item) for item in items])

        if look_distance != 8.0:
            self._add_field("look_distance", max(0.0, look_distance))
        if look_time is not None:
            if isinstance(look_time, (tuple, list)):
                self._add_field(
                    "look_time",
                    AnvilFormatter.min_max_dict(
                        look_time,
                        "look_time",
                        value_types=(int,),
                        clamp_min=0,
                    ),
                )
            else:
                self._add_field("look_time", max(0, look_time))


class EntityAIBreakDoor(AIGoal):
    _identifier = "minecraft:behavior.break_door"

    def __init__(self) -> None:
        """Allows this mob to break doors.

        This component has no configurable constructor properties.

        Note:
            Learn notes that vanilla Bedrock currently prefers `can_break_doors` on the navigation component for this capability.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_break_door
        """
        super().__init__("behavior.break_door")


class EntityAIControlledByPlayer(AIGoal):
    _identifier = "minecraft:behavior.controlled_by_player"

    def __init__(
        self,
        fractional_rotation: float = 0.5,
        fractional_rotation_limit: float = 5.0,
        mount_speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity to be controlled by the player using an item in the item_controllable property (required). On every tick, the entity will attempt to rotate towards where the player is facing with the control item whilst simultaneously moving forward.

        Parameters:
            fractional_rotation (float, optional): The entity will attempt to rotate to face where the player is facing each tick. Defaults to 0.5.
            fractional_rotation_limit (float, optional): Limits the total degrees the entity can rotate to face where the player is facing on each tick. Defaults to 5.0.
            mount_speed_multiplier (float, optional): Speed multiplier of mount when controlled by player. Defaults to 1.0.

        Note:
            Requires `minecraft:rideable` and `minecraft:item_controllable`, and also expects an entity movement component to be present.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_controlled_by_player
        """
        super().__init__("behavior.controlled_by_player")
        self._require_components(EntityRideable, EntityItemControllable)

        if fractional_rotation != 0.5:
            self._add_field(
                "fractional_rotation",
                clamp(fractional_rotation, 0.5, 1.0),
            )
        if fractional_rotation_limit != 5.0:
            self._add_field(
                "fractional_rotation_limit",
                max(0.0, fractional_rotation_limit),
            )
        if mount_speed_multiplier != 1.0:
            self._add_field(
                "mount_speed_multiplier",
                max(0.0, mount_speed_multiplier),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAICroak(AIGoal):
    _identifier = "minecraft:behavior.croak"

    def __init__(
        self,
        duration: Seconds | tuple[Seconds, Seconds] = None,
        filters: Filter = None,
        interval: Seconds | tuple[Seconds, Seconds] = None,
    ) -> None:
        """Allows the entity to croak at a random time interval with configurable conditions.

        Parameters:
            duration (Seconds | tuple[Seconds, Seconds], optional): Random range in seconds after which the croaking stops. Can also be a constant. Defaults to None.
            filters (Filter, optional): Conditions for the behavior to start and keep running. The interval between runs only starts after passing the filters. Defaults to None.
            interval (Seconds | tuple[Seconds, Seconds], optional): Random range in seconds between runs of this behavior. Can also be a constant. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_croak
        """
        super().__init__("behavior.croak")

        if duration is not None:
            if isinstance(duration, (tuple, list)):
                self._add_field(
                    "duration", AnvilFormatter.min_max_list(duration, "duration")
                )
            else:
                self._add_field("duration", max(0.0, duration))
        if filters is not None:
            self._add_field("filters", filters)
        if interval is not None:
            if isinstance(interval, (tuple, list)):
                self._add_field(
                    "interval", AnvilFormatter.min_max_list(interval, "interval")
                )
            else:
                self._add_field("interval", max(0.0, interval))


class EntityAIDoorInteract(AIGoal):
    _identifier = "minecraft:behavior.door_interact"

    def __init__(self) -> None:
        """Allows the mob to open and close doors.

        This component has no configurable constructor properties.

        Note:
            Learn notes that this behavior is not currently used by vanilla Bedrock entities.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_door_interact
        """
        super().__init__("behavior.door_interact")


class EntityAIFleeSun(AIGoal):
    _identifier = "minecraft:behavior.flee_sun"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to run away from direct sunlight and seek shade.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_flee_sun
        """
        super().__init__("behavior.flee_sun")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAILayEgg(AIGoal):
    _identifier = "minecraft:behavior.lay_egg"

    def __init__(
        self,
        allow_laying_from_below: bool = False,
        egg_type: MinecraftBlockDescriptor | Identifier = "minecraft:turtle_egg",
        goal_radius: float = 0.5,
        lay_egg_sound: str = "lay_egg",
        lay_seconds: Seconds = 10.0,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        target_blocks: list[MinecraftBlockDescriptor | Identifier] = None,
        target_materials_above_block: list[Literal["Air", "Water", "Lava"]] = None,
        use_default_animation: bool = True,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to lay an egg block on certain types of blocks if the mob is pregnant.

        Parameters:
            allow_laying_from_below (bool, optional): Allows the mob to lay its eggs from below the target if it can't get there. This is useful if the target block is water with air above, since mobs may not be able to get to the air block above water. Defaults to False.
            egg_type (MinecraftBlockDescriptor | Identifier, optional): Block type for the egg to lay. If this is a turtle egg, the number of eggs in the block is randomly set. Defaults to "minecraft:turtle_egg".
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            lay_egg_sound (str, optional): Name of the sound event played when laying the egg. Defaults to lay_egg, which is used for Turtles. Defaults to "lay_egg".
            lay_seconds (Seconds, optional): Duration of the laying egg process in seconds. Defaults to 10.0.
            search_height (int, optional): The height in blocks the mob will look for the block to move towards. Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for the block to move towards. Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.
            target_blocks (list[MinecraftBlockDescriptor | Identifier], optional): Blocks that the mob can lay its eggs on top of. Defaults to the engine default when omitted.
            target_materials_above_block (list[Literal["Air", "Water", "Lava"]], optional): Types of materials that can exist above the target block. Valid types are Air, Water, and Lava. Defaults to the engine default when omitted.
            use_default_animation (bool, optional): Specifies if the default lay-egg animation should be played when the egg is placed or not. Defaults to True.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_lay_egg
        """
        super().__init__("behavior.lay_egg")
        self._require_components(EntityIsPregnant)

        if allow_laying_from_below:
            self._add_field("allow_laying_from_below", allow_laying_from_below)
        if str(egg_type) != "minecraft:turtle_egg":
            self._add_field("egg_type", str(egg_type))
        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if lay_egg_sound != "lay_egg":
            self._add_field("lay_egg_sound", lay_egg_sound)
        if lay_seconds != 10.0:
            self._add_field("lay_seconds", max(0.0, lay_seconds))
        if search_height != 1:
            self._add_field("search_height", max(1, search_height))
        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if target_blocks is not None:
            self._add_field("target_blocks", [str(block) for block in target_blocks])
        if target_materials_above_block is not None:
            self._add_field(
                "target_materials_above_block",
                list(target_materials_above_block),
            )
        if not use_default_animation:
            self._add_field("use_default_animation", use_default_animation)
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def on_lay(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_lay", trigger)
        return self


class EntityAIMoveOutdoors(AIGoal):
    _identifier = "minecraft:behavior.move_outdoors"

    def __init__(
        self,
        goal_radius: float = 2.0,
        search_count: int = 10,
        search_height: int = 5,
        search_range: int = 15,
        speed_multiplier: float = 0.5,
        timeout_cooldown: Seconds = 8.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to move outdoors.

        Parameters:
            goal_radius (float, optional): The radius away from the target block to count as reaching the goal. Defaults to 2.0.
            search_count (int, optional): The amount of times to try finding a random outdoors position before failing. Defaults to 10.
            search_height (int, optional): The y range to search for an outdoors position for. Defaults to 5.
            search_range (int, optional): The x and z range to search for an outdoors position for. Defaults to 15.
            speed_multiplier (float, optional): The movement speed modifier to apply to the entity while it is moving outdoors. Defaults to 0.5.
            timeout_cooldown (Seconds, optional): The cooldown time in seconds before the goal can be reused after pathfinding fails. Defaults to 8.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_outdoors
        """
        super().__init__("behavior.move_outdoors")

        if goal_radius != 2.0:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if search_count != 10:
            self._add_field("search_count", max(1, search_count))
        if search_height != 5:
            self._add_field("search_height", max(0, search_height))
        if search_range != 15:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 0.5:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if timeout_cooldown != 8.0:
            self._add_field("timeout_cooldown", max(0.0, timeout_cooldown))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIOpenDoor(AIGoal):
    _identifier = "minecraft:behavior.open_door"

    def __init__(self, close_door_after: bool = True) -> None:
        """Allows the mob to open doors. Requires the mob to be able to path through doors, otherwise the mob won't even want to try opening them.

        Parameters:
            close_door_after (bool, optional): If true, the mob will close the door after opening it and going through it. Defaults to True.

        Note:
            Requires the mob to be able to path through doors, otherwise the mob will not try opening them.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_open_door
        """
        super().__init__("behavior.open_door")

        if not close_door_after:
            self._add_field("close_door_after", close_door_after)


class EntityAIPlayDead(AIGoal):
    _identifier = "minecraft:behavior.play_dead"

    def __init__(
        self,
        apply_regeneration: bool = False,
        damage_sources: list[DamageCause] = None,
        duration: Seconds = 1.0,
        filters: Filter = None,
        force_below_health: int = 0,
        random_damage_range: tuple[int, int] = (0, 0),
        random_start_chance: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to pretend to be dead to avoid being targeted by attackers.

        Parameters:
            apply_regeneration (bool, optional): Whether the mob will receive the regeneration effect while playing dead. Defaults to False.
            damage_sources (list[DamageCause], optional): The list of Entity Damage Sources that will cause this mob to play dead. Defaults to None.
            duration (Seconds, optional): The amount of time the mob will remain playing dead (in seconds). Defaults to 1.0.
            filters (Filter, optional): The list of other triggers that are required for the mob to activate play dead. Defaults to None.
            force_below_health (int, optional): The amount of health at which damage will cause the mob to play dead. Defaults to 0.
            random_damage_range (tuple[int, int], optional): The range of damage that may cause the goal to start depending on randomness. Defaults to (0, 0).
            random_start_chance (float, optional): The likelihood of this goal starting upon taking damage. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_play_dead
        """
        super().__init__("behavior.play_dead")

        if apply_regeneration:
            self._add_field("apply_regeneration", apply_regeneration)
        if damage_sources is not None:
            self._add_field(
                "damage_sources",
                [
                    source.value if isinstance(source, DamageCause) else str(source)
                    for source in damage_sources
                ],
            )
        if duration != 1.0:
            self._add_field("duration", max(0.0, duration))
        if filters is not None:
            self._add_field("filters", filters)
        if force_below_health != 0:
            self._add_field("force_below_health", max(0, force_below_health))
        if random_damage_range != (0, 0):
            self._add_field(
                "random_damage_range",
                AnvilFormatter.min_max_dict(
                    random_damage_range,
                    "random_damage_range",
                    value_types=(int,),
                    clamp_min=0,
                ),
            )
        if random_start_chance != 1.0:
            self._add_field(
                "random_start_chance",
                clamp(random_start_chance, 0.0, 1.0),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIRestrictOpenDoor(AIGoal):
    _identifier = "minecraft:behavior.restrict_open_door"

    def __init__(self) -> None:
        """Allows the mob to stay indoors during night time.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_restrict_open_door
        """
        super().__init__("behavior.restrict_open_door")


class EntityAIRestrictSun(AIGoal):
    _identifier = "minecraft:behavior.restrict_sun"

    def __init__(self) -> None:
        """Allows the mob to automatically start avoiding the sun when its a clear day out.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_restrict_sun
        """
        super().__init__("behavior.restrict_sun")


class EntityAITempt(AIGoal):
    _identifier = "minecraft:behavior.tempt"

    def __init__(
        self,
        items: list[MinecraftItemDescriptor | Identifier],
        can_get_scared: bool = False,
        can_tempt_vertically: bool = False,
        can_tempt_while_ridden: bool = False,
        sound_interval: int | tuple[int, int] = None,
        speed_multiplier: float = 1.0,
        stop_distance: float = 1.5,
        tempt_sound: str = None,
        within_radius: float = 0.0,
    ) -> None:
        """Allows a mob to be tempted by a player holding a specific item. Uses pathfinding for movement.

        Parameters:
            items (list[MinecraftItemDescriptor | Identifier]): List of items that can tempt the mob.
            can_get_scared (bool, optional): If true, the mob can stop being tempted if the player moves too fast while close to this mob. Defaults to False.
            can_tempt_vertically (bool, optional): If true, vertical distance to the player will be considered when tempting. Defaults to False.
            can_tempt_while_ridden (bool, optional): If true, the mob can be tempted even if it has a passenger (i.e. if being ridden). Defaults to False.
            sound_interval (int | tuple[int, int], optional): Range of random ticks to wait between tempt sounds. Can be a number, an array [min, max], or an object with range_min/range_max or min/max. Defaults to None.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            stop_distance (float, optional): The distance at which the mob will stop following the player. Defaults to 1.5.
            tempt_sound (str, optional): Sound to play while the mob is being tempted. Defaults to None.
            within_radius (float, optional): Distance in blocks this mob can get tempted by a player holding an item they like. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_tempt
        """
        super().__init__("behavior.tempt")
        self._add_field("items", [str(item) for item in items])

        if can_get_scared:
            self._add_field("can_get_scared", can_get_scared)
        if can_tempt_vertically:
            self._add_field("can_tempt_vertically", can_tempt_vertically)
        if can_tempt_while_ridden:
            self._add_field("can_tempt_while_ridden", can_tempt_while_ridden)
        if sound_interval is not None:
            if isinstance(sound_interval, (tuple, list)):
                self._add_field(
                    "sound_interval",
                    AnvilFormatter.min_max_dict(
                        sound_interval,
                        "sound_interval",
                        value_types=(int,),
                        clamp_min=0,
                    ),
                )
            else:
                self._add_field("sound_interval", max(0, sound_interval))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if stop_distance != 1.5:
            self._add_field("stop_distance", max(0.0, stop_distance))
        if tempt_sound is not None:
            self._add_field("tempt_sound", tempt_sound)
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))


class EntityAIMoveToLiquid(AIGoal):
    _identifier = "minecraft:behavior.move_to_liquid"

    def __init__(
        self,
        goal_radius: float = 0.5,
        material_type: Literal["Any", "Water", "Lava", "any", "water", "lava"] = "Any",
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to move into a liquid when on land.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            material_type (Literal["Any", "Water", "Lava", "any", "water", "lava"], optional): The material type of the liquid block to find. Valid values are "Any", "Water", and "Lava". Defaults to "Any".
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for the liquid block to move towards Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for the liquid block to move towards Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_liquid
        """
        super().__init__("behavior.move_to_liquid")

        normalized_material_type = material_type.capitalize()
        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if normalized_material_type != "Any":
            self._add_field("material_type", normalized_material_type)
        if search_count != 10:
            self._add_field("search_count", max(0, search_count))
        if search_height != 1:
            self._add_field("search_height", max(1, search_height))
        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMoveToVillage(AIGoal):
    _identifier = "minecraft:behavior.move_to_village"

    def __init__(
        self,
        cooldown_time: Seconds = 8.0,
        goal_radius: float = 1.5,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to move into a random location within a village.

        Parameters:
            cooldown_time (Seconds, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 8.0.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 1.5.
            search_range (int, optional): The distance in blocks to search for villages. If <= 0, find the closest village regardless of distance. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_village
        """
        super().__init__("behavior.move_to_village")

        if cooldown_time != 8.0:
            self._add_field("cooldown_time", max(0.0, cooldown_time))
        if goal_radius != 1.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMoveTowardsHomeRestriction(AIGoal):
    _identifier = "minecraft:behavior.move_towards_home_restriction"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows entities with a `minecraft:home` component to move towards their home position. If `restriction_radius` is set, entities will be able to run this behavior only if outside of it.

        Parameters:
            speed_multiplier (float, optional): This multiplier modifies the entity's speed when moving towards its restriction. Defaults to 1.0.

        Note:
            Requires `minecraft:home` in order to work properly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_home_restriction
        """
        super().__init__("behavior.move_towards_home_restriction")
        self._require_components(EntityHome)

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMoveTowardsRestriction(AIGoal):
    _identifier = "minecraft:behavior.move_towards_restriction"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """AI goal that drives entities back toward their designated home area when they've wandered too far. Works with components like minecraft:home to define the restriction zone. Used for village-bound mobs, territorial creatures, or any entity that should patrol or return to a specific location.

        Parameters:
            speed_multiplier (float, optional): This multiplier modifies the entity's speed when moving towards its restriction. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_towards_restriction
        """
        super().__init__("behavior.move_towards_restriction")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIOfferFlower(AIGoal):
    _identifier = "minecraft:behavior.offer_flower"

    def __init__(
        self,
        chance_to_start: float = 0.0001250000059371814,
        filters: Filter = None,
        max_head_rotation_y: float = 30.0,
        max_offer_flower_duration: Seconds = 20.0,
        max_rotation_x: float = 30.0,
        search_area: Coordinates = (6, 2, 6),
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to offer a flower to another mob with the minecraft:take_flower behavior.

        Parameters:
            chance_to_start (float, optional): Percent chance that the mob will start this goal from 0.0 to 1.0 (where 1.0 = 100%). Value must be <= 1. Defaults to 0.0001250000059371814.
            filters (Filter, optional): Conditions that need to be met for the behavior to start. Defaults to None.
            max_head_rotation_y (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Defaults to 30.0.
            max_offer_flower_duration (Seconds, optional): The max amount of time (in seconds) that the mob will offer the flower for before exiting the Goal. Defaults to 20.0.
            max_rotation_x (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 30.0.
            search_area (Coordinates, optional): The dimensions of the AABB used to search for a potential mob to offer flower to. Defaults to (6, 2, 6).

        Note:
            Requires a flower item to be held by the entity.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_offer_flower
        """
        super().__init__("behavior.offer_flower")

        if chance_to_start != 0.0001250000059371814:
            self._add_field("chance_to_start", clamp(chance_to_start, 0.0, 1.0))
        if filters is not None:
            self._add_field("filters", filters)
        if max_head_rotation_y != 30.0:
            self._add_field("max_head_rotation_y", max(0.0, max_head_rotation_y))
        if max_offer_flower_duration != 20.0:
            self._add_field(
                "max_offer_flower_duration",
                max(0.0, max_offer_flower_duration),
            )
        if max_rotation_x != 30.0:
            self._add_field("max_rotation_x", max(0.0, max_rotation_x))
        if search_area != (6, 2, 6):
            self._add_field("search_area", list(search_area))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIPetSleepWithOwner(AIGoal):
    _identifier = "minecraft:behavior.pet_sleep_with_owner"

    def __init__(
        self,
        goal_radius: float = 0.5,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the pet mob to move onto a bed with its owner while sleeping.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            search_height (int, optional): Height in blocks from the owner the pet can be to sleep with owner. Defaults to 1.
            search_range (int, optional): The distance in blocks from the owner the pet can be to sleep with owner. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_pet_sleep_with_owner
        """
        super().__init__("behavior.pet_sleep_with_owner")

        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if search_height != 1:
            self._add_field("search_height", max(0, search_height))
        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))


class EntityAIRandomLookAroundAndSit(AIGoal):
    _identifier = "minecraft:behavior.random_look_around_and_sit"

    def __init__(
        self,
        continue_if_leashed: bool = False,
        continue_sitting_on_reload: bool = False,
        max_angle_of_view_horizontal: float = 30.0,
        max_look_count: int = 2,
        max_look_time: int = 40,
        min_angle_of_view_horizontal: float = -30.0,
        min_look_count: int = 1,
        min_look_time: int = 20,
        probability: float = 0.02,
        random_look_around_cooldown: Seconds = 0.0,
    ) -> None:
        """Allows the mob to randomly sit and look around for a duration. Note: Must have a sitting animation set up to use this.

        Parameters:
            continue_if_leashed (bool, optional): If the goal should continue to be used as long as the mob is leashed. Defaults to False.
            continue_sitting_on_reload (bool, optional): The mob will stay sitting on reload. Defaults to False.
            max_angle_of_view_horizontal (float, optional): The rightmost angle a mob can look at on the horizontal plane with respect to its initial facing direction. Defaults to 30.0.
            max_look_count (int, optional): The max amount of unique looks a mob will have while looking around. Defaults to 2.
            max_look_time (int, optional): The max amount of time (in ticks) a mob will stay looking at a direction while looking around. Defaults to 40.
            min_angle_of_view_horizontal (float, optional): The leftmost angle a mob can look at on the horizontal plane with respect to its initial facing direction. Defaults to -30.0.
            min_look_count (int, optional): The min amount of unique looks a mob will have while looking around. Defaults to 1.
            min_look_time (int, optional): The min amount of time (in ticks) a mob will stay looking at a direction while looking around. Defaults to 20.
            probability (float, optional): The probability of randomly looking around/sitting. Defaults to 0.02.
            random_look_around_cooldown (Seconds, optional): The cooldown in seconds before the goal can be used again. Defaults to 0.0.

        Note:
            Must have a sitting animation set up to use this.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_random_look_around_and_sit
        """
        super().__init__("behavior.random_look_around_and_sit")

        if continue_if_leashed:
            self._add_field("continue_if_leashed", continue_if_leashed)
        if continue_sitting_on_reload:
            self._add_field("continue_sitting_on_reload", continue_sitting_on_reload)
        if max_angle_of_view_horizontal != 30.0:
            self._add_field(
                "max_angle_of_view_horizontal",
                max_angle_of_view_horizontal,
            )
        if max_look_count != 2:
            self._add_field("max_look_count", max(0, max_look_count))
        if max_look_time != 40:
            self._add_field("max_look_time", max(0, max_look_time))
        if min_angle_of_view_horizontal != -30.0:
            self._add_field(
                "min_angle_of_view_horizontal",
                min_angle_of_view_horizontal,
            )
        if min_look_count != 1:
            self._add_field("min_look_count", max(0, min_look_count))
        if min_look_time != 20:
            self._add_field("min_look_time", max(0, min_look_time))
        if probability != 0.02:
            self._add_field("probability", clamp(probability, 0.0, 1.0))
        if random_look_around_cooldown != 0.0:
            self._add_field(
                "random_look_around_cooldown",
                max(0.0, random_look_around_cooldown),
            )


class EntityAISwell(AIGoal):
    _identifier = "minecraft:behavior.swell"

    def __init__(
        self,
        start_distance: float = 10.0,
        stop_distance: float = 2.0,
    ) -> None:
        """Allows the creeper to swell up when a player is nearby. It can only be used by Creepers.

        Parameters:
            start_distance (float, optional): This mob starts swelling when a target is at least this many blocks away. Defaults to 10.0.
            stop_distance (float, optional): This mob stops swelling when a target has moved away at least this many blocks. Defaults to 2.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swell
        """
        super().__init__("behavior.swell")

        if start_distance != 10.0:
            self._add_field("start_distance", max(0.0, start_distance))
        if stop_distance != 2.0:
            self._add_field("stop_distance", max(0.0, stop_distance))


class EntityAITakeFlower(AIGoal):
    _identifier = "minecraft:behavior.take_flower"

    def __init__(
        self,
        filters: Filter = None,
        max_head_rotation_y: float = 30.0,
        max_rotation_x: float = 30.0,
        max_wait_time: Seconds = 20.0,
        min_distance_to_target: float = 2.0,
        min_wait_time: Seconds = 4.0,
        search_area: Coordinates = (6, 2, 6),
        speed_multiplier: float = 0.5,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to accept flowers from another mob with the minecraft:offer_flower behavior.

        Parameters:
            filters (Filter, optional): Filters allow data objects to specify test criteria which allows their use. Defaults to None.
            max_head_rotation_y (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Value must be > 0. Defaults to 30.0.
            max_rotation_x (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Value must be > 0. Defaults to 30.0.
            max_wait_time (Seconds, optional): The maximum amount of time (in seconds) for the mob to randomly wait for before taking the flower. Defaults to 20.0.
            min_distance_to_target (float, optional): Minimum distance (in blocks) for the entity to be considered having reached its target. Value must be > 0. Defaults to 2.0.
            min_wait_time (Seconds, optional): The minimum amount of time (in seconds) for the mob to randomly wait for before taking the flower. Defaults to 4.0.
            search_area (Coordinates, optional): The dimensions of the AABB used to search for a potential mob to take a flower from. Defaults to (6, 2, 6).
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 0.5.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_take_flower
        """
        super().__init__("behavior.take_flower")

        if filters is not None:
            self._add_field("filters", filters)
        if max_head_rotation_y != 30.0:
            self._add_field("max_head_rotation_y", max(0.0, max_head_rotation_y))
        if max_rotation_x != 30.0:
            self._add_field("max_rotation_x", max(0.0, max_rotation_x))
        if max_wait_time != 20.0:
            self._add_field("max_wait_time", max(0.0, max_wait_time))
        if min_distance_to_target != 2.0:
            self._add_field(
                "min_distance_to_target",
                max(0.0, min_distance_to_target),
            )
        if min_wait_time != 4.0:
            self._add_field("min_wait_time", max(0.0, min_wait_time))
        if search_area != (6, 2, 6):
            self._add_field("search_area", list(search_area))
        if speed_multiplier != 0.5:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def on_take_flower(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_take_flower", trigger)
        return self


class EntityAITeleportToOwner(AIGoal):
    _identifier = "minecraft:behavior.teleport_to_owner"

    def __init__(
        self,
        cooldown: Seconds = 1.0,
        filters: Filter = None,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows an entity to teleport to its owner.

        Parameters:
            cooldown (Seconds, optional): The time in seconds that must pass for the entity to be able to try to teleport again. Defaults to 1.0.
            filters (Filter, optional): Conditions to be satisfied for the entity to teleport to its owner. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_teleport_to_owner
        """
        super().__init__("behavior.teleport_to_owner")

        if cooldown != 1.0:
            self._add_field("cooldown", max(0.0, cooldown))
        if filters is not None:
            self._add_field("filters", filters)
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIAquaticChargeAttack(AIGoal):
    _identifier = "minecraft:behavior.aquatic_charge_attack"

    def __init__(
        self,
        attack_reach: float = 0.05000000074505806,
        charge_cooldown_time: tuple[Seconds, Seconds] = (2.0, 6.0),
        charge_overshoot_distance: float = 1.5,
        charge_speed: float = 0.05999999865889549,
        knockback_force: float = 2.0,
        max_charge_distance: float = 16.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Enables an aquatic mob to dash at its target with knockback; includes overshoot and cooldown settings.

        Parameters:
            attack_reach (float, optional): Horizontal reach grown around the mob's AABB to register a hit. Defaults to 0.05000000074505806.
            charge_cooldown_time (tuple[Seconds, Seconds], optional): Range of time in seconds to wait before starting another charge. Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected. Defaults to (2.0, 6.0).
            charge_overshoot_distance (float, optional): Distance beyond the target the mob aims during a charge. Defaults to 1.5.
            charge_speed (float, optional): Absolute speed used during the charge attack. Value must be >= 0.05000000074505806. Defaults to 0.05999999865889549.
            knockback_force (float, optional): Knockback force applied to the target on hit. Defaults to 2.0.
            max_charge_distance (float, optional): Maximum distance at which the mob attempts a charge. Defaults to 16.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_aquatic_charge_attack
        """
        super().__init__("behavior.aquatic_charge_attack")

        if attack_reach != 0.05000000074505806:
            self._add_field("attack_reach", max(0.0, attack_reach))
        if charge_cooldown_time != (2.0, 6.0):
            self._add_field(
                "charge_cooldown_time",
                AnvilFormatter.min_max_dict(
                    charge_cooldown_time, "charge_cooldown_time"
                ),
            )
        if charge_overshoot_distance != 1.5:
            self._add_field(
                "charge_overshoot_distance",
                max(0.0, charge_overshoot_distance),
            )
        if charge_speed != 0.05999999865889549:
            self._add_field("charge_speed", max(0.05000000074505806, charge_speed))
        if knockback_force != 2.0:
            self._add_field("knockback_force", knockback_force)
        if max_charge_distance != 16.0:
            self._add_field("max_charge_distance", max(0.0, max_charge_distance))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIChargeHeldItem(AIGoal):
    _identifier = "minecraft:behavior.charge_held_item"

    def __init__(self, *items: str) -> None:
        """Allows an entity to charge and use their held item.

        Parameters:
            *items (str): The list of items that can be used to charge the held item. At least one item is required.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_charge_held_item
        """
        super().__init__("behavior.charge_held_item")

        if len(items) == 0:
            raise ValueError("EntityAIChargeHeldItem requires at least one item.")
        self._add_field("items", list(items))


class EntityAIDrinkPotion(AIGoal):
    _identifier = "minecraft:behavior.drink_potion"

    def __init__(self, speed_modifier: float = 0.0) -> None:
        """Allows the mob to drink potions based on specified environment conditions.

        Parameters:
            speed_modifier (float, optional): The movement speed modifier to apply to the entity while it is drinking a potion. A value of 0 represents no change in speed. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drink_potion
        """
        super().__init__("behavior.drink_potion")
        self._add_field("potions", [])

        if speed_modifier != 0.0:
            self._add_field("speed_modifier", speed_modifier)

    def add_potion(
        self,
        potion_id: int,
        chance: float = 1.0,
        filters: Filter = None,
    ):
        potion = {"id": potion_id}
        if chance != 1.0:
            potion["chance"] = clamp(chance, 0.0, 1.0)
        if filters is not None:
            potion["filters"] = filters
        self._get_field("potions", []).append(potion)
        return self


class EntityAIFollowCaravan(AIGoal):
    _identifier = "minecraft:behavior.follow_caravan"

    def __init__(
        self,
        entity_count: int = 1,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to follow mobs that are in a caravan.

        Parameters:
            entity_count (int, optional): Number of entities that can be in the caravan. Defaults to 1.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_caravan
        """
        super().__init__("behavior.follow_caravan")
        self._add_field("entity_types", [])

        if entity_count != 1:
            self._add_field("entity_count", max(1, entity_count))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))

    def add_entity_type(
        self,
        filters: Filter,
        cooldown: Seconds = 0.0,
        max_dist: float = 16.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if cooldown != 0.0:
            entity_type["cooldown"] = max(0.0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self


class EntityAIHoldGround(AIGoal):
    _identifier = "minecraft:behavior.hold_ground"

    def __init__(
        self,
        broadcast: bool = False,
        broadcast_range: float = 0.0,
        min_radius: float = 10.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Compels an entity to stop at their current location, turn to face a mob they are targeting, and react with an event.

        Parameters:
            broadcast (bool, optional): Whether to broadcast out the mob's target to other mobs of the same type. Defaults to False.
            broadcast_range (float, optional): Range in blocks for how far to broadcast. Defaults to 0.0.
            min_radius (float, optional): Minimum distance the target must be for the mob to run this goal. Defaults to 10.0.

        Note:
            Requires a target in order to work properly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_hold_ground
        """
        super().__init__("behavior.hold_ground")

        if broadcast:
            self._add_field("broadcast", broadcast)
        if broadcast_range != 0.0:
            self._add_field("broadcast_range", max(0.0, broadcast_range))
        if min_radius != 10.0:
            self._add_field("min_radius", max(0.0, min_radius))
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def within_radius_event(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("within_radius_event", trigger)
        return self


class EntityAIJumpAroundTarget(AIGoal):
    _identifier = "minecraft:behavior.jump_around_target"

    def __init__(
        self,
        check_collision: bool = False,
        entity_bounding_box_scale: float = 0.7,
        filters: Filter = None,
        jump_angles: tuple[float, ...] = (40.0, 55.0, 60.0, 75.0, 80.0),
        jump_cooldown_duration: Seconds = 0.5,
        jump_cooldown_when_hurt_duration: Seconds = 0.1,
        landing_distance_from_target: tuple[int, int] | None = None,
        landing_position_spread_degrees: int = 90,
        last_hurt_duration: Seconds = 2.0,
        line_of_sight_obstruction_height_ignore: int = 4,
        max_jump_velocity: float = 1.4,
        prepare_jump_duration: Seconds = 0.5,
        required_vertical_space: int = 4,
        snap_to_surface_block_range: int = 10,
        valid_distance_to_target: tuple[int, int] | None = None,
    ) -> None:
        """Allows an entity to jump around a target.

        Parameters:
            check_collision (bool, optional): Enables collision checks when calculating the jump. Setting check_collision to true may affect performance and should be used with care. Defaults to False.
            entity_bounding_box_scale (float, optional): Scaling temporarily applied to the entity's AABB bounds when jumping. A smaller bounding box reduces the risk of collisions during the jump. When check_collision is true it also increases the chance of being able to jump when close to obstacles. Defaults to 0.7.
            filters (Filter, optional): Conditions that need to be met for the behavior to start. Defaults to None.
            jump_angles (tuple[float, ...], optional): The jump angles in float degrees that are allowed when performing the jump. The order in which the angles are chosen is randomized. Defaults to (40.0, 55.0, 60.0, 75.0, 80.0).
            jump_cooldown_duration (Seconds, optional): The time in seconds to spend in cooldown before this goal can be used again. Defaults to 0.5.
            jump_cooldown_when_hurt_duration (Seconds, optional): The time in seconds to spend in cooldown after being hurt before this goal can be used again. Defaults to 0.1.
            landing_distance_from_target (tuple[int, int] | None, optional): The range deciding how close to and how far away from the target the landing position can be when jumping. Defaults to None.
            landing_position_spread_degrees (int, optional): This angle (in degrees) is used for controlling the spread when picking a landing position behind the target. A zero spread angle means the landing position will be straight behind the target with no variance. A 90 degree spread angle means the landing position can be up to 45 degrees to the left and to the right of the position straight behind the target's view direction. Defaults to 90.
            last_hurt_duration (Seconds, optional): If the entity was hurt within these last seconds, the jump_cooldown_when_hurt_duration will be used instead of jump_cooldown_duration. Defaults to 2.0.
            line_of_sight_obstruction_height_ignore (int, optional): If the entity's line of sight towards its target is obstructed by an obstacle with a height below this number, the obstacle will be ignored, and the goal will try to find a valid landing position. Defaults to 4.
            max_jump_velocity (float, optional): Maximum velocity a jump can be performed at. Defaults to 1.4.
            prepare_jump_duration (Seconds, optional): The time in seconds to spend preparing for the jump. Defaults to 0.5.
            required_vertical_space (int, optional): The number of blocks above the entity's head that has to be air for this goal to be usable. Defaults to 4.
            snap_to_surface_block_range (int, optional): The number of blocks above and below from the jump target position that will be checked to find a surface to land on. Defaults to 10.
            valid_distance_to_target (tuple[int, int] | None, optional): Target needs to be within this range for the jump to happen. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_jump_around_target
        """
        super().__init__("behavior.jump_around_target")

        if check_collision:
            self._add_field("check_collision", check_collision)
        if entity_bounding_box_scale != 0.7:
            self._add_field(
                "entity_bounding_box_scale", max(0.0, entity_bounding_box_scale)
            )
        if filters is not None:
            self._add_field("filters", filters)
        if jump_angles != (40.0, 55.0, 60.0, 75.0, 80.0):
            self._add_field("jump_angles", list(jump_angles))
        if jump_cooldown_duration != 0.5:
            self._add_field("jump_cooldown_duration", max(0.0, jump_cooldown_duration))
        if jump_cooldown_when_hurt_duration != 0.1:
            self._add_field(
                "jump_cooldown_when_hurt_duration",
                max(0.0, jump_cooldown_when_hurt_duration),
            )
        if landing_distance_from_target is not None:
            self._add_field(
                "landing_distance_from_target", list(landing_distance_from_target)
            )
        if landing_position_spread_degrees != 90:
            self._add_field(
                "landing_position_spread_degrees",
                max(0, landing_position_spread_degrees),
            )
        if last_hurt_duration != 2.0:
            self._add_field("last_hurt_duration", max(0.0, last_hurt_duration))
        if line_of_sight_obstruction_height_ignore != 4:
            self._add_field(
                "line_of_sight_obstruction_height_ignore",
                max(0, line_of_sight_obstruction_height_ignore),
            )
        if max_jump_velocity != 1.4:
            self._add_field("max_jump_velocity", max(0.0, max_jump_velocity))
        if prepare_jump_duration != 0.5:
            self._add_field("prepare_jump_duration", max(0.0, prepare_jump_duration))
        if required_vertical_space != 4:
            self._add_field("required_vertical_space", max(0, required_vertical_space))
        if snap_to_surface_block_range != 10:
            self._add_field(
                "snap_to_surface_block_range",
                max(0, snap_to_surface_block_range),
            )
        if valid_distance_to_target is not None:
            self._add_field("valid_distance_to_target", list(valid_distance_to_target))


class EntityAIJumpToBlock(AIGoal):
    _identifier = "minecraft:behavior.jump_to_block"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] | None = None,
        forbidden_blocks: list[str] | None = None,
        max_velocity: float = 1.5,
        minimum_distance: int = 2,
        minimum_path_length: int = 5,
        preferred_blocks: list[str] | None = None,
        preferred_blocks_chance: float = 1.0,
        scale_factor: float = 0.7,
        search_height: int = 10,
        search_width: int = 8,
    ) -> None:
        """Allows an entity to jump to another random block.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds] | None, optional): Minimum and maximum cooldown time-range (positive, in seconds) between each attempted jump. Defaults to None.
            forbidden_blocks (list[str] | None, optional): Blocks that the mob can't jump to. Defaults to None.
            max_velocity (float, optional): The maximum velocity with which the mob can jump. Defaults to 1.5.
            minimum_distance (int, optional): The minimum distance (in blocks) from the mob to a block, in order to consider jumping to it. Defaults to 2.
            minimum_path_length (int, optional): The minimum length (in blocks) of the mobs path to a block, in order to consider jumping to it. Defaults to 5.
            preferred_blocks (list[str] | None, optional): Blocks that the mob prefers jumping to. Defaults to None.
            preferred_blocks_chance (float, optional): Chance (between 0.0 and 1.0) that the mob will jump to a preferred block, if in range. Only matters if preferred blocks are defined. Defaults to 1.0.
            scale_factor (float, optional): The scalefactor of the bounding box of the mob while it is jumping. Defaults to 0.7.
            search_height (int, optional): The height (in blocks, in range [2, 15]) of the search box, centered around the mob. Defaults to 10.
            search_width (int, optional): The width (in blocks, in range [2, 15]) of the search box, centered around the mob. Defaults to 8.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_jump_to_block
        """
        super().__init__("behavior.jump_to_block")

        if cooldown_range is not None:
            self._add_field("cooldown_range", list(cooldown_range))
        if forbidden_blocks is not None:
            self._add_field("forbidden_blocks", forbidden_blocks)
        if max_velocity != 1.5:
            self._add_field("max_velocity", max(0.0, max_velocity))
        if minimum_distance != 2:
            self._add_field("minimum_distance", max(0, minimum_distance))
        if minimum_path_length != 5:
            self._add_field("minimum_path_length", max(0, minimum_path_length))
        if preferred_blocks is not None:
            self._add_field("preferred_blocks", preferred_blocks)
        if preferred_blocks_chance != 1.0:
            self._add_field(
                "preferred_blocks_chance",
                clamp(preferred_blocks_chance, 0.0, 1.0),
            )
        if scale_factor != 0.7:
            self._add_field("scale_factor", max(0.0, scale_factor))
        if search_height != 10:
            self._add_field("search_height", clamp(search_height, 2, 15))
        if search_width != 8:
            self._add_field("search_width", clamp(search_width, 2, 15))


class EntityAICelebrate(AIGoal):
    _identifier = "minecraft:behavior.celebrate"

    def __init__(
        self,
        celebration_sound: str = "celebrate",
        duration: Seconds = 30.0,
        jump_interval: tuple[Seconds, Seconds] = (1.0, 3.5),
        sound_interval: tuple[Seconds, Seconds] = (2.0, 7.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to celebrate surviving a raid by making celebration sounds and jumping.

        Parameters:
            celebration_sound (str, optional): The sound event to trigger during the celebration. Defaults to "celebrate".
            duration (Seconds, optional): The duration in seconds that the celebration lasts for. Defaults to 30.0.
            jump_interval (tuple[Seconds, Seconds], optional): Minimum and maximum time between jumping (positive, in seconds). Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected. Defaults to (1.0, 3.5).
            sound_interval (tuple[Seconds, Seconds], optional): Minimum and maximum time between sound events (positive, in seconds). Check that the limits imposed on the range (minimum, maximum and maximum distance between values) are respected. Defaults to (2.0, 7.0).

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_celebrate
        """
        super().__init__("behavior.celebrate")

        if celebration_sound != "celebrate":
            self._add_field("celebration_sound", celebration_sound)
        if duration != 30.0:
            self._add_field("duration", max(0.0, duration))
        if jump_interval != (1.0, 3.5):
            self._add_field(
                "jump_interval",
                AnvilFormatter.min_max_dict(jump_interval, "jump_interval"),
            )
        if sound_interval != (2.0, 7.0):
            self._add_field(
                "sound_interval",
                AnvilFormatter.min_max_dict(sound_interval, "sound_interval"),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def on_celebration_end(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_celebration_end_event", trigger)
        return self


class EntityAIDefendTrustedTarget(AIGoal):
    _identifier = "minecraft:behavior.defend_trusted_target"

    def __init__(
        self,
        aggro_sound: str = None,
        attack_interval: int = 0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        sound_chance: float = None,
        within_radius: float = 0.0,
    ) -> None:
        """Allows the mob to target another mob that hurts an entity it trusts.

        Parameters:
            aggro_sound (str, optional): Sound to occasionally play while defending. Defaults to None.
            attack_interval (int, optional): Time in seconds between attacks. Defaults to 0.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (Seconds, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            sound_chance (float, optional): Chance that the aggro sound will play while defending. Defaults to None.
            within_radius (float, optional): Distance in blocks that the target can be within to launch an attack. Defaults to 0.0.

        Note:
            Requires a trusted relationship in order to work properly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_defend_trusted_target
        """
        super().__init__("behavior.defend_trusted_target")
        self._require_components(EntityTrust)
        self._add_field("entity_types", [])

        if aggro_sound is not None:
            self._add_field("aggro_sound", aggro_sound)
        if attack_interval != 0:
            self._add_field("attack_interval", max(0, attack_interval))
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field(
                "must_see_forget_duration",
                max(0.0, must_see_forget_duration),
            )
        if sound_chance is not None:
            self._add_field("sound_chance", clamp(sound_chance, 0.0, 1.0))
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))

    def add_entity_type(
        self,
        filters: Filter,
        cooldown: Seconds = 0.0,
        max_dist: float = 16.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if cooldown != 0.0:
            entity_type["cooldown"] = max(0.0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self

    def on_defend_start(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_defend_start", trigger)
        return self


class EntityAIDefendVillageTarget(AIGoal):
    _identifier = "minecraft:behavior.defend_village_target"

    def __init__(
        self,
        attack_chance: float = 0.05000000074505806,
        attack_owner: bool = False,
        must_reach: bool = False,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        persist_time: Seconds = 0.0,
        within_radius: float = 0.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity to stay in a village and defend the village from aggressors. If a player is in bad standing with the village this goal will cause the entity to attack the player regardless of filter conditions.

        Parameters:
            attack_chance (float, optional): The percentage chance that the entity has to attack aggressors of its village, where 1.0 = 100%. Value must be <= 1. Defaults to 0.05000000074505806.
            attack_owner (bool, optional): If true, this entity can attack its owner. Defaults to False.
            must_reach (bool, optional): If true, this entity requires a path to the target. Defaults to False.
            must_see (bool, optional): If true, the mob has to be visible to be a valid choice. Defaults to False.
            must_see_forget_duration (Seconds, optional): Determines the amount of time in seconds that this mob will look for a target before forgetting about it and looking for a new one when the target isn't visible any more. Defaults to 3.0.
            persist_time (Seconds, optional): Time (in seconds) this entity can continue attacking the target after the target is no longer valid. Defaults to 0.0.
            within_radius (float, optional): Maximum distance this entity can be from the target when following it, otherwise the target becomes invalid. This value is only used if the entity doesn't declare "minecraft:follow_range". Defaults to 0.0.

        Note:
            This behavior is typically used with the `minecraft:dweller` component.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_defend_village_target
        """
        super().__init__("behavior.defend_village_target")
        self._add_field("entity_types", [])

        if attack_chance != 0.05000000074505806:
            self._add_field("attack_chance", clamp(attack_chance, 0.0, 1.0))
        if attack_owner:
            self._add_field("attack_owner", attack_owner)
        if must_reach:
            self._add_field("must_reach", must_reach)
        if must_see:
            self._add_field("must_see", must_see)
        if must_see_forget_duration != 3.0:
            self._add_field(
                "must_see_forget_duration",
                max(0.0, must_see_forget_duration),
            )
        if persist_time != 0.0:
            self._add_field("persist_time", max(0.0, persist_time))
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def add_entity_type(
        self,
        filters: Filter,
        check_if_outnumbered: bool = False,
        cooldown: int = 0,
        max_dist: float = 16.0,
        max_flee: float = 10.0,
        max_height: float = -1.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        priority: int = 0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if check_if_outnumbered:
            entity_type["check_if_outnumbered"] = check_if_outnumbered
        if cooldown != 0:
            entity_type["cooldown"] = max(0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if max_flee != 10.0:
            entity_type["max_flee"] = max(0.0, max_flee)
        if max_height != -1.0:
            entity_type["max_height"] = max_height
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if priority != 0:
            entity_type["priority"] = priority
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self


class EntityAIFloatTempt(AIGoal):
    _identifier = "minecraft:behavior.float_tempt"

    def __init__(
        self,
        items: list[MinecraftItemDescriptor | Identifier],
        can_get_scared: bool = False,
        can_tempt_vertically: bool = False,
        can_tempt_while_ridden: bool = False,
        sound_interval: int | tuple[int, int] = None,
        speed_multiplier: float = 1.0,
        stop_distance: float = 1.5,
        tempt_sound: str = None,
        within_radius: float = 0.0,
    ) -> None:
        """Allows a mob to be tempted by a player holding a specific item. Uses point-to-point movement. Designed for mobs that are floating (e.g. use the "minecraft:navigation.float" component).

        Parameters:
            items (list[MinecraftItemDescriptor | Identifier]): List of items that can tempt the mob.
            can_get_scared (bool, optional): If true, the mob can stop being tempted if the player moves too fast while close to this mob. Defaults to False.
            can_tempt_vertically (bool, optional): If true, vertical distance to the player will be considered when tempting. Defaults to False.
            can_tempt_while_ridden (bool, optional): If true, the mob can be tempted even if it has a passenger (i.e. if being ridden). Defaults to False.
            sound_interval (int | tuple[int, int], optional): Range of random ticks to wait between tempt sounds. Defaults to None.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            stop_distance (float, optional): The distance at which the mob will stop following the player. Defaults to 1.5.
            tempt_sound (str, optional): Sound to play while the mob is being tempted. Defaults to None.
            within_radius (float, optional): Distance in blocks this mob can get tempted by a player holding an item they like. Defaults to 0.0.

        Note:
            Designed for mobs using `minecraft:navigation.float`.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_float_tempt
        """
        super().__init__("behavior.float_tempt")
        self._add_field("items", [str(item) for item in items])

        if can_get_scared:
            self._add_field("can_get_scared", can_get_scared)
        if can_tempt_vertically:
            self._add_field("can_tempt_vertically", can_tempt_vertically)
        if can_tempt_while_ridden:
            self._add_field("can_tempt_while_ridden", can_tempt_while_ridden)
        if sound_interval is not None:
            if isinstance(sound_interval, (tuple, list)):
                self._add_field(
                    "sound_interval",
                    AnvilFormatter.min_max_dict(
                        sound_interval,
                        "sound_interval",
                        value_types=(int,),
                        clamp_min=0,
                    ),
                )
            else:
                self._add_field("sound_interval", max(0, sound_interval))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if stop_distance != 1.5:
            self._add_field("stop_distance", max(0.0, stop_distance))
        if tempt_sound is not None:
            self._add_field("tempt_sound", tempt_sound)
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))


class EntityAILookAtEntity(AIGoal):
    _identifier = "minecraft:behavior.look_at_entity"

    def __init__(
        self,
        angle_of_view_horizontal: int = 360,
        angle_of_view_vertical: int = 360,
        filters: Filter = None,
        look_distance: float = 8.0,
        look_time: tuple[int, int] = (2, 4),
        probability: float = 0.02,
        *control_flags: ControlFlags,
    ) -> None:
        """Compels an entity to look at a specific entity by rotating the `head` bone pose within a set limit.

        Parameters:
            angle_of_view_horizontal (int, optional): The angle in degrees that the mob can see rotated on the Y-axis (left-right). Value must be <= 360. Defaults to 360.
            angle_of_view_vertical (int, optional): The angle in degrees that the mob can see rotated on the X-axis (up-down). Value must be <= 360. Defaults to 360.
            filters (Filter, optional): Filter to determine the conditions for this mob to look at the entity. Defaults to None.
            look_distance (float, optional): The distance in blocks from which the entity will look at the nearest entity. Defaults to 8.0.
            look_time (tuple[int, int], optional): Time range to look at the nearest entity. Defaults to (2, 4).
            probability (float, optional): The probability of looking at the target. A value of 1.00 is 100%. Value must be <= 1. Defaults to 0.02.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_look_at_entity
        """
        super().__init__("behavior.look_at_entity")

        if angle_of_view_horizontal != 360:
            self._add_field("angle_of_view_horizontal", angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self._add_field("angle_of_view_vertical", angle_of_view_vertical)
        if filters is not None:
            self._add_field("filters", filters)
        if look_distance != 8.0:
            self._add_field("look_distance", look_distance)
        if look_time != (2, 4):
            self._add_field(
                "look_time", AnvilFormatter.min_max_dict(look_time, "look_time")
            )
        if probability != 0.02:
            self._add_field("probability", clamp(probability, 0.0, 1.0))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMoveAroundTarget(AIGoal):
    _identifier = "minecraft:behavior.move_around_target"

    def __init__(
        self,
        destination_pos_spread_degrees: float = 90.0,
        destination_position_range: tuple[float, float] = (4.0, 8.0),
        filters: Filter = None,
        height_difference_limit: float = 10.0,
        horizontal_search_distance: int = 5,
        movement_speed: float = 0.6000000238418579,
        vertical_search_distance: int = 5,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows an entity to move around a target.If the entity is too close(i.e.closer than destination range min and height difference limit) it will try to move away from its target.If the entity is too far away from its target it will try to move closer to a random position within the destination range.A randomized amount of those positions will be behind the target, and the spread can be tweaked with 'destination_pos_spread_degrees'.

        Parameters:
            destination_pos_spread_degrees (float, optional): This angle (in degrees) is used for controlling the spread when picking a destination position behind the target. Defaults to 90.0.
            destination_position_range (tuple[float, float], optional): The range of distances from the target entity within which the goal should look for a position to move the owner entity to. Defaults to (4.0, 8.0).
            filters (Filter, optional): Conditions that need to be met for the behavior to start. Defaults to None.
            height_difference_limit (float, optional): Distance in height (in blocks) between the owner entity and the target has to be less than this value when owner checks if it is too close and should move away from the target. Defaults to 10.0.
            horizontal_search_distance (int, optional): Horizontal search distance (in blocks) when searching for a position to move away from target. Defaults to 5.
            movement_speed (float, optional): The speed with which the entity should move to its target position. Defaults to 0.6000000238418579.
            vertical_search_distance (int, optional): Vertical search distance (in blocks) when searching for a position to move away from target. Defaults to 5.

        Note:
            Requires a format version of at least 1.21.30.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_around_target
        """
        super().__init__("behavior.move_around_target")

        if destination_pos_spread_degrees != 90.0:
            self._add_field(
                "destination_pos_spread_degrees",
                max(0.0, destination_pos_spread_degrees),
            )
        if destination_position_range != (4.0, 8.0):
            self._add_field(
                "destination_position_range",
                AnvilFormatter.min_max_list(
                    destination_position_range,
                    "destination_position_range",
                ),
            )
        if filters is not None:
            self._add_field("filters", filters)
        if height_difference_limit != 10.0:
            self._add_field(
                "height_difference_limit", max(0.0, height_difference_limit)
            )
        if horizontal_search_distance != 5:
            self._add_field(
                "horizontal_search_distance",
                max(0, horizontal_search_distance),
            )
        if movement_speed != 0.6000000238418579:
            self._add_field("movement_speed", max(0.0, movement_speed))
        if vertical_search_distance != 5:
            self._add_field(
                "vertical_search_distance",
                max(0, vertical_search_distance),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMoveToPOI(AIGoal):
    _identifier = "minecraft:behavior.move_to_poi"

    def __init__(
        self,
        poi_type: Literal["bed", "jobsite", "meeting_area"],
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to move to a POI if able to.

        Parameters:
            poi_type (Literal["bed", "jobsite", "meeting_area"]): Tells the goal what POI type it should be looking for.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_to_poi
        """
        super().__init__("behavior.move_to_poi")
        self._add_field("poi_type", poi_type)

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAINap(AIGoal):
    _identifier = "minecraft:behavior.nap"

    def __init__(
        self,
        can_nap_filters: Filter = None,
        cooldown_max: Seconds = 0.0,
        cooldown_min: Seconds = 0.0,
        mob_detect_dist: float = 6.0,
        mob_detect_height: float = 6.0,
        wake_mob_exceptions: Filter = None,
    ) -> None:
        """Allows mobs to occassionally stop and take a nap under certain conditions.

        Parameters:
            can_nap_filters (Filter, optional): Conditions that need to be met for the entity to nap. Defaults to None.
            cooldown_max (Seconds, optional): Maximum time in seconds the mob has to wait before using the goal again. Defaults to 0.0.
            cooldown_min (Seconds, optional): Minimum time in seconds the mob has to wait before using the goal again. Defaults to 0.0.
            mob_detect_dist (float, optional): The block distance in x and z that will be checked for mobs that this mob detects. Defaults to 6.0.
            mob_detect_height (float, optional): The block distance in y that will be checked for mobs that this mob detects. Defaults to 6.0.
            wake_mob_exceptions (Filter, optional): Filters for mobs that will not wake this entity from napping. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_nap
        """
        super().__init__("behavior.nap")

        if can_nap_filters is not None:
            self._add_field("can_nap_filters", can_nap_filters)
        if cooldown_max != 0.0:
            self._add_field("cooldown_max", max(0.0, cooldown_max))
        if cooldown_min != 0.0:
            self._add_field("cooldown_min", max(0.0, cooldown_min))
        if mob_detect_dist != 6.0:
            self._add_field("mob_detect_dist", max(0.0, mob_detect_dist))
        if mob_detect_height != 6.0:
            self._add_field("mob_detect_height", max(0.0, mob_detect_height))
        if wake_mob_exceptions is not None:
            self._add_field("wake_mob_exceptions", wake_mob_exceptions)


class EntityAIStrollTowardsVillage(AIGoal):
    _identifier = "minecraft:behavior.stroll_towards_village"

    def __init__(
        self,
        cooldown_time: Seconds = 8.0,
        goal_radius: float = 1.5,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        start_chance: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to move into a random location within a village within the search range.

        Parameters:
            cooldown_time (Seconds, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 8.0.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 1.5.
            search_range (int, optional): The distance in blocks to search for villages. If <= 0, find the closest village regardless of distance. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.
            start_chance (float, optional): Chance that the mob will start this goal, from 0 to 1. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stroll_towards_village
        """
        super().__init__("behavior.stroll_towards_village")

        if cooldown_time != 8.0:
            self._add_field("cooldown_time", max(0.0, cooldown_time))
        if goal_radius != 1.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if search_range != 0:
            self._add_field("search_range", search_range)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if start_chance != 1.0:
            self._add_field("start_chance", clamp(start_chance, 0.0, 1.0))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAICelebrateSurvive(AIGoal):
    _identifier = "minecraft:behavior.celebrate_survive"

    def __init__(
        self,
        duration: Seconds = 30.0,
        fireworks_interval: tuple[Seconds, Seconds] = (10.0, 20.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the player to trade with this mob. When the goal starts, it will stop the mob's navigation.

        Parameters:
            duration (Seconds, optional): The duration in seconds that the celebration lasts for. Defaults to 30.0.
            fireworks_interval (tuple[Seconds, Seconds], optional): Minimum and maximum time between firework (positive, in seconds). Defaults to (10.0, 20.0).

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_celebrate_survive
        """
        super().__init__("behavior.celebrate_survive")

        if duration != 30.0:
            self._add_field("duration", max(0.0, duration))
        if fireworks_interval != (10.0, 20.0):
            self._add_field(
                "fireworks_interval",
                AnvilFormatter.min_max_dict(fireworks_interval, "fireworks_interval"),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def on_celebration_end(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_celebration_end_event", trigger)
        return self


class EntityAIFindCover(AIGoal):
    _identifier = "minecraft:behavior.find_cover"

    def __init__(
        self,
        cooldown_time: Seconds = 0.0,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to seek shade.

        Parameters:
            cooldown_time (Seconds, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_cover
        """
        super().__init__("behavior.find_cover")

        if cooldown_time != 0.0:
            self._add_field("cooldown_time", max(0.0, cooldown_time))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIFindUnderwaterTreasure(AIGoal):
    _identifier = "minecraft:behavior.find_underwater_treasure"

    def __init__(
        self,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        stop_distance: float = 2.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to move towards the nearest underwater ruin or shipwreck.

        Parameters:
            search_range (int, optional): The range that the mob will search for a treasure chest within a ruin or shipwreck to move towards. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            stop_distance (float, optional): The distance the mob will move before stopping. Defaults to 2.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_underwater_treasure
        """
        super().__init__("behavior.find_underwater_treasure")

        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if stop_distance != 2.0:
            self._add_field("stop_distance", max(0.0, stop_distance))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIFireAtTarget(AIGoal):
    _identifier = "minecraft:behavior.fire_at_target"

    def __init__(
        self,
        projectile_def: MinecraftEntityDescriptor | Identifier,
        attack_cooldown: Seconds = 0.5,
        attack_range: tuple[int, int] = None,
        filters: Filter = None,
        max_head_rotation_x: float = 30.0,
        max_head_rotation_y: float = 30.0,
        owner_anchor: int = 2,
        owner_offset: tuple[float, float, float] = (0, 0, 0),
        post_shoot_delay: Seconds = 0.2,
        pre_shoot_delay: Seconds = 0.75,
        ranged_fov: float = 90.0,
        target_anchor: int = 2,
        target_offset: tuple[float, float, float] = (0, 0, 0),
    ) -> None:
        """Allows an entity to attack by firing a shot with a delay. Anchor and offset parameters of this component overrides the anchor and offset from projectile component.

        Parameters:
            projectile_def (MinecraftEntityDescriptor | Identifier): Actor definition to use as projectile for the ranged attack. The actor must be a projectile. This field is required for the goal to be usable.
            attack_cooldown (Seconds, optional): The cooldown time in seconds before this goal can be used again. Defaults to 0.5.
            attack_range (tuple[int, int], optional): Target needs to be within this range for the attack to happen. Defaults to None.
            filters (Filter, optional): Conditions that need to be met for the behavior to start. Defaults to None.
            max_head_rotation_x (float, optional): Maximum head rotation (in degrees), on the X-axis, that this entity can apply while trying to look at the target. Defaults to 30.0.
            max_head_rotation_y (float, optional): Maximum head rotation (in degrees), on the Y-axis, that this entity can apply while trying to look at the target. Defaults to 30.0.
            owner_anchor (int, optional): Entity anchor for the projectile spawn location. Defaults to 2.
            owner_offset (tuple[float, float, float], optional): Offset vector from the owner_anchor. Defaults to (0, 0, 0).
            post_shoot_delay (Seconds, optional): Time in seconds between firing the projectile and ending the goal. Defaults to 0.2.
            pre_shoot_delay (Seconds, optional): Time in seconds before firing the projectile. Defaults to 0.75.
            ranged_fov (float, optional): Field of view (in degrees) when using sensing to detect a target for attack. Defaults to 90.0.
            target_anchor (int, optional): Entity anchor for projectile target. Defaults to 2.
            target_offset (tuple[float, float, float], optional): Offset vector from the target_anchor. Defaults to (0, 0, 0).

        Note:
            Requires a format version of at least 1.21.30.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_fire_at_target
        """
        super().__init__("behavior.fire_at_target")
        self._add_field("projectile_def", str(projectile_def))

        if attack_cooldown != 0.5:
            self._add_field("attack_cooldown", max(0.0, attack_cooldown))
        if attack_range is not None:
            self._add_field("attack_range", list(attack_range))
        if filters is not None:
            self._add_field("filters", filters)
        if max_head_rotation_x != 30.0:
            self._add_field("max_head_rotation_x", max(0.0, max_head_rotation_x))
        if max_head_rotation_y != 30.0:
            self._add_field("max_head_rotation_y", max(0.0, max_head_rotation_y))
        if owner_anchor != 2:
            self._add_field("owner_anchor", owner_anchor)
        if owner_offset != (0, 0, 0):
            self._add_field("owner_offset", owner_offset)
        if post_shoot_delay != 0.2:
            self._add_field("post_shoot_delay", max(0.0, post_shoot_delay))
        if pre_shoot_delay != 0.75:
            self._add_field("pre_shoot_delay", max(0.0, pre_shoot_delay))
        if ranged_fov != 90.0:
            self._add_field("ranged_fov", max(0.0, ranged_fov))
        if target_anchor != 2:
            self._add_field("target_anchor", target_anchor)
        if target_offset != (0, 0, 0):
            self._add_field("target_offset", target_offset)


class EntityAIGoHome(AIGoal):
    _identifier = "minecraft:behavior.go_home"

    def __init__(
        self,
        calculate_new_path_radius: float = 2.0,
        goal_radius: float = 0.5,
        interval: int = 120,
        speed_multiplier: float = 1.0,
    ) -> None:
        """Allows the mob to move back to the position they were spawned.

        Parameters:
            calculate_new_path_radius (float, optional): Distance in blocks that the mob is considered close enough to the end of the current path. A new path will then be calculated to continue toward home. Defaults to 2.0.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Defaults to 0.5.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal. Defaults to 120.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_home
        """
        super().__init__("behavior.go_home")

        if calculate_new_path_radius != 2.0:
            self._add_field(
                "calculate_new_path_radius",
                max(0.0, calculate_new_path_radius),
            )
        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if interval != 120:
            self._add_field("interval", max(1, interval))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))

    def on_failed(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_failed", trigger)
        return self

    def on_home(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_home", trigger)
        return self


class EntityAIOcelotSitOnBlock(AIGoal):
    _identifier = "minecraft:behavior.ocelot_sit_on_block"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows to mob to be able to sit in place like the ocelot.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_ocelot_sit_on_block
        """
        super().__init__("behavior.ocelot_sit_on_block")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIRaidGarden(AIGoal):
    _identifier = "minecraft:behavior.raid_garden"

    def __init__(
        self,
        blocks: (
            list[MinecraftBlockDescriptor | Identifier]
            | tuple[MinecraftBlockDescriptor | Identifier, ...]
        ) = (),
        eat_delay: int = 2,
        full_delay: int = 100,
        goal_radius: float = 0.5,
        initial_eat_delay: int = 0,
        max_to_eat: int = 6,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to eat/raid crops out of farms until they are full.

        Parameters:
            blocks (list[MinecraftBlockDescriptor | Identifier] | tuple[MinecraftBlockDescriptor | Identifier, ...], optional): Blocks that the mob is looking for to eat/raid. Defaults to ().
            eat_delay (int, optional): Time in seconds between each time it eats/raids. Defaults to 2.
            full_delay (int, optional): Amount of time in seconds before this mob wants to eat/raid again after eating its maximum. Defaults to 100.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            initial_eat_delay (int, optional): Time in seconds before starting to eat/raid once it arrives at it. Defaults to 0.
            max_to_eat (int, optional): Maximum number of crops this entity wants to eat/raid. If set to zero or less then it doesn't have a maximum. Defaults to 6.
            search_height (int, optional): Height in blocks the mob will look for crops to eat Value must be > 0. Defaults to 1.
            search_range (int, optional): Distance in blocks the mob will look for crops to eat Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_raid_garden
        """
        super().__init__("behavior.raid_garden")
        self._add_field("blocks", [])

        if blocks != ():
            self._component["blocks"].extend(str(block) for block in blocks)
        if eat_delay != 2:
            self._add_field("eat_delay", max(0, eat_delay))
        if full_delay != 100:
            self._add_field("full_delay", max(0, full_delay))
        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if initial_eat_delay != 0:
            self._add_field("initial_eat_delay", max(0, initial_eat_delay))
        if max_to_eat != 6:
            self._add_field("max_to_eat", max_to_eat)
        if search_height != 1:
            self._add_field("search_height", max(1, search_height))
        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def add_block(self, *blocks: MinecraftBlockDescriptor | Identifier):
        self._component["blocks"].extend(str(block) for block in blocks)
        return self


class EntityAISwimIdle(AIGoal):
    _identifier = "minecraft:behavior.swim_idle"

    def __init__(
        self,
        idle_time: Seconds = 5.0,
        success_rate: float = 0.10000000149011612,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity go idle, if swimming. Entity must be in water.

        Parameters:
            idle_time (Seconds, optional): Amount of time (in seconds) to stay idle. Defaults to 5.0.
            success_rate (float, optional): Percent chance this entity will go idle, 1.0 = 100%. Defaults to 0.10000000149011612.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_idle
        """
        super().__init__("behavior.swim_idle")

        if idle_time != 5.0:
            self._add_field("idle_time", max(0.0, idle_time))
        if success_rate != 0.10000000149011612:
            self._add_field("success_rate", clamp(success_rate, 0.0, 1.0))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIVexCopyOwnerTarget(AIGoal):
    _identifier = "minecraft:behavior.vex_copy_owner_target"

    def __init__(self) -> None:
        """Allows the mob to target the same entity its owner is targeting.

        Note:
            No longer used for the `vex` entity.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_vex_copy_owner_target
        """
        super().__init__("behavior.vex_copy_owner_target")
        self._add_field("entity_types", [])

    def add_entity_type(
        self,
        filters: Filter,
        cooldown: Seconds = 0.0,
        max_dist: float = 16.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if cooldown != 0.0:
            entity_type["cooldown"] = max(0.0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self


class EntityAIVexRandomMove(AIGoal):
    _identifier = "minecraft:behavior.vex_random_move"

    def __init__(self) -> None:
        """Allows the mob to move around randomly like the Vex.

        Note:
            No longer used for the `vex` entity.

        This component has no configurable constructor properties.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_vex_random_move
        """
        super().__init__("behavior.vex_random_move")


class EntityAIRoll(AIGoal):
    _identifier = "minecraft:behavior.roll"

    def __init__(self, probability: float = None) -> None:
        """This allows the mob to roll forward.

        Parameters:
            probability (float, optional): The probability that the mob will use the goal. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_roll
        """
        super().__init__("behavior.roll")

        if probability is not None:
            self._add_field("probability", clamp(probability, 0.0, 1.0))


class EntityAIScared(AIGoal):
    _identifier = "minecraft:behavior.scared"

    def __init__(self, sound_interval: int = 0) -> None:
        """Allows the a mob to become scared when the weather outside is thundering.

        Parameters:
            sound_interval (int, optional): The interval in which a sound will play when active in a 1/delay chance to kick off. Defaults to 0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_scared
        """
        super().__init__("behavior.scared")

        if sound_interval != 0:
            self._add_field("sound_interval", max(0, sound_interval))


class EntityAIEmerge(AIGoal):
    _identifier = "minecraft:behavior.emerge"

    def __init__(self, cooldown_time: Seconds = 0.5, duration: Seconds = 5.0) -> None:
        """Allows this entity to emerge from the ground.

        Parameters:
            cooldown_time (Seconds, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.5.
            duration (Seconds, optional): Goal duration in seconds. Defaults to 5.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_emerge
        """
        super().__init__("behavior.emerge")

        if cooldown_time != 0.5:
            self._add_field("cooldown_time", max(0.0, cooldown_time))
        if duration != 5.0:
            self._add_field("duration", max(0.0, duration))

    def on_done(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_done", trigger)
        return self


class EntityAISniff(AIGoal):
    _identifier = "minecraft:behavior.sniff"

    def __init__(
        self,
        cooldown_range: tuple[Seconds, Seconds] = (3.0, 10.0),
        duration: Seconds = 1.0,
        sniffing_radius: float = 5.0,
        suspicion_radius_horizontal: float = 3.0,
        suspicion_radius_vertical: float = 3.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to detect the nearest player within "sniffing_radius" and update its "minecraft:suspect_tracking" component state.

        Parameters:
            cooldown_range (tuple[Seconds, Seconds], optional): Cooldown range between sniffs in seconds. Defaults to (3.0, 10.0).
            duration (Seconds, optional): Sniffing duration in seconds. Defaults to 1.0.
            sniffing_radius (float, optional): Mob detection radius. Defaults to 5.0.
            suspicion_radius_horizontal (float, optional): Mob suspicion horizontal radius. When a player is within this radius horizontally, the anger level towards that player is increased. Defaults to 3.0.
            suspicion_radius_vertical (float, optional): Mob suspicion vertical radius. When a player is within this radius vertically, the anger level towards that player is increased Value must be >= 1. Defaults to 3.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sniff
        """
        super().__init__("behavior.sniff")
        self._require_components(EntitySuspectTracking)

        if cooldown_range != (3.0, 10.0):
            self._add_field(
                "cooldown_range",
                AnvilFormatter.min_max_dict(cooldown_range, "cooldown_range"),
            )
        if duration != 1.0:
            self._add_field("duration", max(0.0, duration))
        if sniffing_radius != 5.0:
            self._add_field("sniffing_radius", max(0.0, sniffing_radius))
        if suspicion_radius_horizontal != 3.0:
            self._add_field(
                "suspicion_radius_horizontal",
                max(0.0, suspicion_radius_horizontal),
            )
        if suspicion_radius_vertical != 3.0:
            self._add_field(
                "suspicion_radius_vertical",
                max(1.0, suspicion_radius_vertical),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAISneeze(AIGoal):
    _identifier = "minecraft:behavior.sneeze"

    def __init__(
        self,
        cooldown_time: Seconds = 0.0,
        drop_item_chance: float = 1.0,
        loot_table: LootTable | str = None,
        prepare_sound: str = None,
        prepare_time: Seconds = 1.0,
        probability: float = 0.02,
        sound: str = None,
        within_radius: float = 0.0,
    ) -> None:
        """Allows the mob to stop and sneeze possibly startling nearby mobs and dropping an item.

        Parameters:
            cooldown_time (Seconds, optional): Time in seconds the mob has to wait before using the goal again. Defaults to 0.0.
            drop_item_chance (float, optional): The probability that the mob will drop an item when it sneezes. Defaults to 1.0.
            loot_table (LootTable | str, optional): Loot table to select dropped items from. Defaults to None.
            prepare_sound (str, optional): Sound to play when the sneeze is about to happen. Defaults to None.
            prepare_time (Seconds, optional): The time in seconds that the mob takes to prepare to sneeze (while the prepare_sound is playing). Defaults to 1.0.
            probability (float, optional): The probability of sneezing. A value of 1.00 is 100%. Defaults to 0.02.
            sound (str, optional): Sound to play when the sneeze occurs. Defaults to None.
            within_radius (float, optional): Distance in blocks that mobs will be startled. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sneeze
        """
        super().__init__("behavior.sneeze")
        self._add_field("entity_types", [])

        if cooldown_time != 0.0:
            self._add_field("cooldown_time", max(0.0, cooldown_time))
        if drop_item_chance != 1.0:
            self._add_field("drop_item_chance", clamp(drop_item_chance, 0.0, 1.0))
        if loot_table is not None:
            self._add_field("loot_table", str(loot_table))
        if prepare_sound is not None:
            self._add_field("prepare_sound", prepare_sound)
        if prepare_time != 1.0:
            self._add_field("prepare_time", max(0.0, prepare_time))
        if probability != 0.02:
            self._add_field("probability", clamp(probability, 0.0, 1.0))
        if sound is not None:
            self._add_field("sound", sound)
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))

    def add_entity_type(
        self,
        filters: Filter,
        cooldown: Seconds = 0.0,
        max_dist: float = 16.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if cooldown != 0.0:
            entity_type["cooldown"] = max(0.0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self


class EntityAISnacking(AIGoal):
    _identifier = "minecraft:behavior.snacking"

    def __init__(
        self,
        items: (
            list[MinecraftItemDescriptor | Identifier]
            | tuple[MinecraftItemDescriptor | Identifier, ...]
        ) = (),
        snacking_cooldown: Seconds = 7.5,
        snacking_cooldown_min: Seconds = 0.5,
        snacking_stop_chance: float = 0.0017,
    ) -> None:
        """Allows the mob to take a load off and snack on food that it found nearby.

        Parameters:
            items (list[MinecraftItemDescriptor | Identifier] | tuple[MinecraftItemDescriptor | Identifier, ...], optional): Items that we are interested in snacking on. Defaults to ().
            snacking_cooldown (Seconds, optional): The cooldown time in seconds before the mob is able to snack again. Defaults to 7.5.
            snacking_cooldown_min (Seconds, optional): The minimum time in seconds before the mob is able to snack again. Defaults to 0.5.
            snacking_stop_chance (float, optional): This is the chance that the mob will stop snacking, from 0 to 1. Defaults to 0.0017.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_snacking
        """
        super().__init__("behavior.snacking")
        self._add_field("items", [])

        if items != ():
            self._component["items"].extend(str(item) for item in items)
        if snacking_cooldown != 7.5:
            self._add_field("snacking_cooldown", max(0.0, snacking_cooldown))
        if snacking_cooldown_min != 0.5:
            self._add_field(
                "snacking_cooldown_min",
                max(0.0, snacking_cooldown_min),
            )
        if snacking_stop_chance != 0.0017:
            self._add_field(
                "snacking_stop_chance",
                clamp(snacking_stop_chance, 0.0, 1.0),
            )

    def add_item(self, *items: MinecraftItemDescriptor | Identifier):
        self._component["items"].extend(str(item) for item in items)
        return self


class EntityAISwimWander(AIGoal):
    _identifier = "minecraft:behavior.swim_wander"

    def __init__(
        self,
        interval: float = 0.008329999633133411,
        look_ahead: float = 5.0,
        speed_multiplier: float = 1.0,
        wander_time: Seconds = 5.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity to wander around while swimming, when not path-finding.

        Parameters:
            interval (float, optional): Percent chance to start wandering, when not path-finding. 1 = 100%. Defaults to 0.008329999633133411.
            look_ahead (float, optional): Distance to look ahead for obstacle avoidance, while wandering. Defaults to 5.0.
            speed_multiplier (float, optional): This multiplier modifies the entity's speed when wandering. Defaults to 1.0.
            wander_time (Seconds, optional): Amount of time (in seconds) to wander after wandering behavior was successfully started. Defaults to 5.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_wander
        """
        super().__init__("behavior.swim_wander")

        if interval != 0.008329999633133411:
            self._add_field("interval", clamp(interval, 0.0, 1.0))
        if look_ahead != 5.0:
            self._add_field("look_ahead", max(0.0, look_ahead))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if wander_time != 5.0:
            self._add_field("wander_time", max(0.0, wander_time))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAISwimWithEntity(AIGoal):
    _identifier = "minecraft:behavior.swim_with_entity"

    def __init__(
        self,
        catch_up_multiplier: float = 2.5,
        catch_up_threshold: float = 12.0,
        chance_to_stop: float = 0.0333,
        match_direction_threshold: float = 2.0,
        search_range: float = 20.0,
        speed_multiplier: float = 1.5,
        state_check_interval: Seconds = 0.5,
        stop_distance: float = 5.0,
        success_rate: float = 0.1,
    ) -> None:
        """Allows the entity follow another entity. Both entities must be swimming [ie, in water].

        Parameters:
            catch_up_multiplier (float, optional): The multiplier this entity's speed is modified by when matching another entity's direction. Defaults to 2.5.
            catch_up_threshold (float, optional): Distance, from the entity being followed, at which this entity will speed up to reach that entity. Defaults to 12.0.
            chance_to_stop (float, optional): Percent chance to stop following the current entity, if they're riding another entity or they're not swimming. 1.0 = 100%. Defaults to 0.0333.
            match_direction_threshold (float, optional): Distance, from the entity being followed, at which this entity will try to match that entity's direction. Defaults to 2.0.
            search_range (float, optional): Radius around this entity to search for another entity to follow. Defaults to 20.0.
            speed_multiplier (float, optional): The multiplier this entity's speed is modified by when trying to catch up to the entity being followed. Defaults to 1.5.
            state_check_interval (Seconds, optional): Time (in seconds) between checks to determine if this entity should catch up to the entity being followed or match the direction of the entity being followed. Defaults to 0.5.
            stop_distance (float, optional): Distance, from the entity being followed, at which this entity will stop following that entity. Defaults to 5.0.
            success_rate (float, optional): Percent chance to start following another entity, if not already doing so. 1.0 = 100%. Defaults to 0.1.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_swim_with_entity
        """
        super().__init__("behavior.swim_with_entity")
        self._add_field("entity_types", [])

        if catch_up_multiplier != 2.5:
            self._add_field("catch_up_multiplier", max(0.0, catch_up_multiplier))
        if catch_up_threshold != 12.0:
            self._add_field("catch_up_threshold", max(0.0, catch_up_threshold))
        if chance_to_stop != 0.0333:
            self._add_field("chance_to_stop", clamp(chance_to_stop, 0.0, 1.0))
        if match_direction_threshold != 2.0:
            self._add_field(
                "match_direction_threshold",
                max(0.0, match_direction_threshold),
            )
        if search_range != 20.0:
            self._add_field("search_range", max(0.0, search_range))
        if speed_multiplier != 1.5:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if state_check_interval != 0.5:
            self._add_field(
                "state_check_interval",
                max(0.0, state_check_interval),
            )
        if stop_distance != 5.0:
            self._add_field("stop_distance", max(0.0, stop_distance))
        if success_rate != 0.1:
            self._add_field("success_rate", clamp(success_rate, 0.0, 1.0))

    def add_entity_type(
        self,
        filters: Filter,
        cooldown: Seconds = 0.0,
        max_dist: float = 16.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if cooldown != 0.0:
            entity_type["cooldown"] = max(0.0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self


class EntityAIDropItemFor(AIGoal):
    _identifier = "minecraft:behavior.drop_item_for"

    def __init__(
        self,
        loot_table: LootTable | str,
        cooldown: Seconds = 0.25,
        drop_item_chance: float = 1.0,
        goal_radius: float = 0.5,
        max_head_look_at_height: float = 10.0,
        minimum_teleport_distance: float = 2.0,
        offering_distance: float = 1.0,
        search_count: int = 0,
        search_height: int = 1,
        search_range: int = 0,
        seconds_before_pickup: Seconds = 0.0,
        speed_multiplier: float = 1.0,
        target_range: tuple[float, float, float] = (1, 1, 1),
        teleport_offset: tuple[float, float, float] = (0, 1, 0),
        time_of_day_range: tuple[float, float] = (0.0, 1.0),
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity to move toward a target, and drop an item near the target.

        Parameters:
            loot_table (LootTable | str): The loot table that contains the possible loot the entity can drop with this goal.
            cooldown (Seconds, optional): The amount of time in seconds that the mob has to wait before selecting a target of the same type again. Defaults to 0.25.
            drop_item_chance (float, optional): The percent chance the entity will drop an item when using this goal. Value must be <= 1. Defaults to 1.0.
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            max_head_look_at_height (float, optional): The maximum height the entities head will look at when dropping the item. The entity will always be looking at its target. Defaults to 10.0.
            minimum_teleport_distance (float, optional): If the target position is farther away than this distance on any tick, the entity will teleport to the target position. Defaults to 2.0.
            offering_distance (float, optional): The preferred distance the entity tries to be from the target it is dropping an item for. Defaults to 1.0.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 0.
            search_height (int, optional): The height in blocks the entity will search within to find a valid target position. Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks the entity will search within to find a valid target position. Value must be > 0. Defaults to 0.
            seconds_before_pickup (Seconds, optional): The numbers of seconds that will pass before the dropped entity can be picked up from the ground. Defaults to 0.0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.
            target_range (tuple[float, float, float], optional): The range in blocks within which the entity searches to find a target to drop an item for. Defaults to (1, 1, 1).
            teleport_offset (tuple[float, float, float], optional): When the entity teleports, offset the teleport position by this many blocks in the X, Y, and Z coordinate. Defaults to (0, 1, 0).
            time_of_day_range (tuple[float, float], optional): The valid times of day that this goal can be used. For reference: noon is 0.0, sunset is 0.25, midnight is 0.5, and sunrise is 0.75, and back to noon for 1.0. Defaults to (0.0, 1.0).

        Note:
            Requires a `minecraft:navigation` component in order to work properly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_drop_item_for
        """
        super().__init__("behavior.drop_item_for")
        self._add_field("entity_types", [])
        self._add_field("loot_table", str(loot_table))

        if cooldown != 0.25:
            self._add_field("cooldown", max(0.0, cooldown))
        if drop_item_chance != 1.0:
            self._add_field("drop_item_chance", clamp(drop_item_chance, 0.0, 1.0))
        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if max_head_look_at_height != 10.0:
            self._add_field(
                "max_head_look_at_height",
                max(0.0, max_head_look_at_height),
            )
        if minimum_teleport_distance != 2.0:
            self._add_field(
                "minimum_teleport_distance",
                max(0.0, minimum_teleport_distance),
            )
        if offering_distance != 1.0:
            self._add_field("offering_distance", max(0.0, offering_distance))
        if search_count != 0:
            self._add_field("search_count", max(0, search_count))
        if search_height != 1:
            self._add_field("search_height", max(1, search_height))
        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if seconds_before_pickup != 0.0:
            self._add_field(
                "seconds_before_pickup",
                max(0.0, seconds_before_pickup),
            )
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if target_range != (1, 1, 1):
            self._add_field("target_range", list(target_range))
        if teleport_offset != (0, 1, 0):
            self._add_field("teleport_offset", list(teleport_offset))
        if time_of_day_range != (0.0, 1.0):
            self._add_field(
                "time_of_day_range",
                AnvilFormatter.min_max_dict(time_of_day_range, "time_of_day_range"),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def add_entity_type(
        self,
        filters: Filter,
        check_if_outnumbered: bool = False,
        cooldown: int = 0,
        max_dist: float = 16.0,
        max_flee: float = 10.0,
        max_height: float = -1.0,
        must_see: bool = False,
        must_see_forget_duration: Seconds = 3.0,
        priority: int = 0,
        reevaluate_description: bool = False,
        sprint_speed_multiplier: float = 1.0,
        walk_speed_multiplier: float = 1.0,
    ):
        entity_type = {"filters": filters}
        if check_if_outnumbered:
            entity_type["check_if_outnumbered"] = check_if_outnumbered
        if cooldown != 0:
            entity_type["cooldown"] = max(0, cooldown)
        if max_dist != 16.0:
            entity_type["max_dist"] = max(0.0, max_dist)
        if max_flee != 10.0:
            entity_type["max_flee"] = max(0.0, max_flee)
        if max_height != -1.0:
            entity_type["max_height"] = max_height
        if must_see:
            entity_type["must_see"] = must_see
        if must_see_forget_duration != 3.0:
            entity_type["must_see_forget_duration"] = max(0.0, must_see_forget_duration)
        if priority != 0:
            entity_type["priority"] = priority
        if reevaluate_description:
            entity_type["reevaluate_description"] = reevaluate_description
        if sprint_speed_multiplier != 1.0:
            entity_type["sprint_speed_multiplier"] = max(0.0, sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            entity_type["walk_speed_multiplier"] = max(0.0, walk_speed_multiplier)
        self._get_field("entity_types", []).append(entity_type)
        return self

    def on_drop_attempt(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
        filters: Filter = None,
    ):
        trigger = {"event": event, "target": target.value}
        if filters is not None:
            trigger["filters"] = filters
        self._add_field("on_drop_attempt", trigger)
        return self


class EntityAIFindMount(AIGoal):
    _identifier = "minecraft:behavior.find_mount"

    def __init__(
        self,
        avoid_water: bool = False,
        max_failed_attempts: int = 20,
        mount_distance: float = -1.0,
        start_delay: int = 0,
        target_needed: bool = False,
        within_radius: float = 0.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the mob to look around for another mob to ride atop it.

        Parameters:
            avoid_water (bool, optional): If true, the mob will not go into water blocks when going towards a mount. Defaults to False.
            max_failed_attempts (int, optional): Number of attempts to find mount. Defaults to 20.
            mount_distance (float, optional): This is the distance the mob needs to be, in blocks, from the desired mount to mount it. If the value is below 0, the mob will use its default attack distance. Defaults to -1.0.
            start_delay (int, optional): Time the mob will wait before starting to move towards the mount. Defaults to 0.
            target_needed (bool, optional): If true, the mob will only look for a mount if it has a target. Defaults to False.
            within_radius (float, optional): Distance in blocks within which the mob will look for a mount. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_find_mount
        """
        super().__init__("behavior.find_mount")

        if avoid_water:
            self._add_field("avoid_water", avoid_water)
        if max_failed_attempts != 20:
            self._add_field("max_failed_attempts", max(0, max_failed_attempts))
        if mount_distance != -1.0:
            self._add_field("mount_distance", mount_distance)
        if start_delay != 0:
            self._add_field("start_delay", max(0, start_delay))
        if target_needed:
            self._add_field("target_needed", target_needed)
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIFollowTargetCaptain(AIGoal):
    _identifier = "minecraft:behavior.follow_target_captain"

    def __init__(
        self, follow_distance: float = 0.0, within_radius: float = 0.0
    ) -> None:
        """Allows mob to move towards its current target captain.

        Parameters:
            follow_distance (float, optional): Defines the distance in blocks the mob will stay from its target while following. Defaults to 0.0.
            within_radius (float, optional): Defines the maximum distance in blocks a mob can get from its target captain before giving up trying to follow it. Defaults to 0.0.

        Note:
            Requires an entity to be labeled as a captain in a group.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_follow_target_captain
        """
        super().__init__("behavior.follow_target_captain")

        if follow_distance != 0.0:
            self._add_field("follow_distance", max(0.0, follow_distance))
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))


class EntityAIGuardianAttack(AIGoal):
    _identifier = "minecraft:behavior.guardian_attack"

    def __init__(
        self,
        elder_extra_magic_damage: int = 2,
        hard_mode_extra_magic_damage: int = 2,
        magic_damage: int = 1,
        min_distance: float = 3.0,
        sound_delay_time: Seconds = 0.5,
        x_max_rotation: float = 90.0,
        y_max_head_rotation: float = 90.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to use a laser beam attack. Can only be used by Guardians and Elder Guardians.

        Parameters:
            elder_extra_magic_damage (int, optional): Amount of additional damage dealt from an elder guardian's magic attack. Value must be > 0. Defaults to 2.
            hard_mode_extra_magic_damage (int, optional): In hard difficulty, amount of additional damage dealt from a guardian's magic attack. Value must be > 0. Defaults to 2.
            magic_damage (int, optional): Amount of damage dealt from a guardian's magic attack. Magic attack damage is added to the guardian's base attack damage. Value must be > 0. Defaults to 1.
            min_distance (float, optional): Guardian attack behavior stops if the target is closer than this distance (doesn't apply to elders). Defaults to 3.0.
            sound_delay_time (Seconds, optional): Time (in seconds) to wait after starting an attack before playing the guardian attack sound. Value must be > 0. Defaults to 0.5.
            x_max_rotation (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Value must be > 0. Defaults to 90.0.
            y_max_head_rotation (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate its head while trying to look at the target. Value must be > 0. Defaults to 90.0.

        Note:
            Can only be used by Guardians and Elder Guardians.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_guardian_attack
        """
        super().__init__("behavior.guardian_attack")

        if elder_extra_magic_damage != 2:
            self._add_field(
                "elder_extra_magic_damage",
                max(1, elder_extra_magic_damage),
            )
        if hard_mode_extra_magic_damage != 2:
            self._add_field(
                "hard_mode_extra_magic_damage",
                max(1, hard_mode_extra_magic_damage),
            )
        if magic_damage != 1:
            self._add_field("magic_damage", max(1, magic_damage))
        if min_distance != 3.0:
            self._add_field("min_distance", max(0.0, min_distance))
        if sound_delay_time != 0.5:
            self._add_field("sound_delay_time", max(0.0, sound_delay_time))
        if x_max_rotation != 90.0:
            self._add_field("x_max_rotation", max(1.0, x_max_rotation))
        if y_max_head_rotation != 90.0:
            self._add_field(
                "y_max_head_rotation",
                max(1.0, y_max_head_rotation),
            )
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMoveThroughVillage(AIGoal):
    _identifier = "minecraft:behavior.move_through_village"

    def __init__(
        self, only_at_night: bool = False, speed_multiplier: float = 1.0
    ) -> None:
        """Can only be used by Villagers. Allows the villagers to create paths around the village.

        Parameters:
            only_at_night (bool, optional): If true, the mob will only move through the village during night time. Defaults to False.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.

        Note:
            Can only be used by Villagers.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_move_through_village
        """
        super().__init__("behavior.move_through_village")

        if only_at_night:
            self._add_field("only_at_night", only_at_night)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))


class EntityAISonicBoom(AIGoal):
    _identifier = "minecraft:behavior.sonic_boom"

    def __init__(
        self,
        attack_cooldown: Seconds = 5.0,
        attack_damage: float = 30.0,
        attack_range_horizontal: float = 15.0,
        attack_range_vertical: float = 20.0,
        attack_sound: str = None,
        charge_sound: str = None,
        duration: Seconds = 0.0,
        duration_until_attack_sound: Seconds = 1.7000000476837158,
        knockback_height_cap: float = 0.0,
        knockback_horizontal_strength: float = 0.0,
        knockback_vertical_strength: float = 0.0,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to perform a 'sonic boom' ranged attack.

        Parameters:
            attack_cooldown (Seconds, optional): Cooldown in seconds required after using this attack until the entity can use sonic boom again. Defaults to 5.0.
            attack_damage (float, optional): Attack damage of the sonic boom. Defaults to 30.0.
            attack_range_horizontal (float, optional): Horizontal range (in blocks) at which the sonic boom can damage the target. Defaults to 15.0.
            attack_range_vertical (float, optional): Vertical range (in blocks) at which the sonic boom can damage the target. Defaults to 20.0.
            attack_sound (str, optional): Sound event for the attack. Defaults to None.
            charge_sound (str, optional): Sound event for the charge up. Defaults to None.
            duration (Seconds, optional): Goal duration in seconds. Defaults to 0.0.
            duration_until_attack_sound (Seconds, optional): Duration in seconds until the attack sound is played. Defaults to 1.7000000476837158.
            knockback_height_cap (float, optional): Height cap of the attack knockback's vertical delta. Defaults to 0.0.
            knockback_horizontal_strength (float, optional): Horizontal strength of the attack's knockback applied to the attack target. Defaults to 0.0.
            knockback_vertical_strength (float, optional): Vertical strength of the attack's knockback applied to the attack target. Defaults to 0.0.
            speed_multiplier (float, optional): This multiplier modifies the attacking entity's speed when moving toward the target. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_sonic_boom
        """
        super().__init__("behavior.sonic_boom")

        if attack_cooldown != 5.0:
            self._add_field("attack_cooldown", max(0.0, attack_cooldown))
        if attack_damage != 30.0:
            self._add_field("attack_damage", attack_damage)
        if attack_range_horizontal != 15.0:
            self._add_field(
                "attack_range_horizontal",
                max(0.0, attack_range_horizontal),
            )
        if attack_range_vertical != 20.0:
            self._add_field(
                "attack_range_vertical",
                max(0.0, attack_range_vertical),
            )
        if attack_sound is not None:
            self._add_field("attack_sound", attack_sound)
        if charge_sound is not None:
            self._add_field("charge_sound", charge_sound)
        if duration != 0.0:
            self._add_field("duration", max(0.0, duration))
        if duration_until_attack_sound != 1.7000000476837158:
            self._add_field(
                "duration_until_attack_sound",
                max(0.0, duration_until_attack_sound),
            )
        if knockback_height_cap != 0.0:
            self._add_field("knockback_height_cap", knockback_height_cap)
        if knockback_horizontal_strength != 0.0:
            self._add_field(
                "knockback_horizontal_strength",
                knockback_horizontal_strength,
            )
        if knockback_vertical_strength != 0.0:
            self._add_field(
                "knockback_vertical_strength",
                knockback_vertical_strength,
            )
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIStayNearNoteblock(AIGoal):
    _identifier = "minecraft:behavior.stay_near_noteblock"

    def __init__(
        self,
        listen_time: int = 30,
        speed: float = 1.0,
        start_distance: float = 10.0,
        stop_distance: float = 2.0,
        *control_flags: ControlFlags,
    ) -> None:
        """The entity will attempt to toss the items from its inventory to a nearby recently played noteblock.

        Parameters:
            listen_time (int, optional): Sets the time an entity should stay near a noteblock after hearing it. Defaults to 30.
            speed (float, optional): Sets the entity's speed when moving toward the block. Defaults to 1.0.
            start_distance (float, optional): Sets the distance the entity needs to be away from the block to attempt to start the goal. Defaults to 10.0.
            stop_distance (float, optional): Sets the distance from the block the entity will attempt to reach. Defaults to 2.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stay_near_noteblock
        """
        super().__init__("behavior.stay_near_noteblock")

        if listen_time != 30:
            self._add_field("listen_time", max(0, listen_time))
        if speed != 1.0:
            self._add_field("speed", max(0.0, speed))
        if start_distance != 10.0:
            self._add_field("start_distance", max(0.0, start_distance))
        if stop_distance != 2.0:
            self._add_field("stop_distance", max(0.0, stop_distance))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIStompTurtleEgg(AIGoal):
    _identifier = "minecraft:behavior.stomp_turtle_egg"

    def __init__(
        self,
        goal_radius: float = 0.5,
        interval: int = 120,
        search_count: int = 10,
        search_height: int = 1,
        search_range: int = 0,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this mob to stomp turtle eggs.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the mob considers it has reached the goal. This is the "wiggle room" to stop the AI from bouncing back and forth trying to reach a specific spot. Value must be > 0. Defaults to 0.5.
            interval (int, optional): A random value to determine when to randomly move somewhere. This has a 1/interval chance to choose this goal Value must be > 0. Defaults to 120.
            search_count (int, optional): The number of randomly selected blocks each tick that the mob will check within its search range and height for a valid block to move to. Defaults to 10.
            search_height (int, optional): Height in blocks the mob will look for turtle eggs to move towards Value must be > 0. Defaults to 1.
            search_range (int, optional): The distance in blocks it will look for turtle eggs to move towards Value must be > 0. Defaults to 0.
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this goal. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stomp_turtle_egg
        """
        super().__init__("behavior.stomp_turtle_egg")

        if goal_radius != 0.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if interval != 120:
            self._add_field("interval", max(1, interval))
        if search_count != 10:
            self._add_field("search_count", max(0, search_count))
        if search_height != 1:
            self._add_field("search_height", max(1, search_height))
        if search_range != 0:
            self._add_field("search_range", max(0, search_range))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIEatCarriedItem(AIGoal):
    _identifier = "minecraft:behavior.eat_carried_item"

    def __init__(
        self,
        delay_before_eating: Seconds = 0.0,
        *control_flags: ControlFlags,
    ) -> None:
        """If the mob is carrying a food item, the mob will eat it and the effects will be applied to the mob.

        Parameters:
            delay_before_eating (Seconds, optional): Time in seconds the mob should wait before eating the item. Defaults to 0.0.

        Note:
            Requires food items to be present in the entity's inventory.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_carried_item
        """
        super().__init__("behavior.eat_carried_item")

        if delay_before_eating != 0.0:
            self._add_field("delay_before_eating", max(0.0, delay_before_eating))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIEndermanLeaveBlock(AIGoal):
    _identifier = "minecraft:behavior.enderman_leave_block"

    def __init__(self) -> None:
        """Allows the enderman to drop a block they are carrying.

        Note:
            Can only be used by Endermen.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_enderman_leave_block
        """
        super().__init__("behavior.enderman_leave_block")


class EntityAIEndermanTakeBlock(AIGoal):
    _identifier = "minecraft:behavior.enderman_take_block"

    def __init__(self) -> None:
        """Allows the enderman to take a block and carry it around.

        Note:
            Can only be used by Endermen.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_enderman_take_block
        """
        super().__init__("behavior.enderman_take_block")


class EntityAIGoAndGiveItemsToNoteblock(AIGoal):
    _identifier = "minecraft:behavior.go_and_give_items_to_noteblock"

    def __init__(
        self,
        listen_time: int = 30,
        reach_block_distance: float = 3.0,
        run_speed: float = 1.0,
        throw_force: float = 0.2,
        throw_sound: str = None,
        vertical_throw_mul: float = 1.5,
    ) -> None:
        """The entity will attempt to toss the items from its inventory to a nearby recently played noteblock.

        Parameters:
            listen_time (int, optional): Sets the time an entity should continue delivering items to a noteblock after hearing it. Defaults to 30.
            reach_block_distance (float, optional): Sets the desired distance to be reached before throwing the items towards the block. Defaults to 3.0.
            run_speed (float, optional): Sets the entity's speed when running toward the block. Defaults to 1.0.
            throw_force (float, optional): Sets the throw force. Defaults to 0.2.
            throw_sound (str, optional): Sound to play when this mob throws an item. Defaults to None.
            vertical_throw_mul (float, optional): Sets the vertical throw multiplier that is applied on top of the throw force in the vertical direction. Defaults to 1.5.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_and_give_items_to_noteblock
        """
        super().__init__("behavior.go_and_give_items_to_noteblock")

        if listen_time != 30:
            self._add_field("listen_time", max(0, listen_time))
        if reach_block_distance != 3.0:
            self._add_field(
                "reach_block_distance",
                max(0.0, reach_block_distance),
            )
        if run_speed != 1.0:
            self._add_field("run_speed", max(0.0, run_speed))
        if throw_force != 0.2:
            self._add_field("throw_force", max(0.0, throw_force))
        if throw_sound is not None:
            self._add_field("throw_sound", throw_sound)
        if vertical_throw_mul != 1.5:
            self._add_field("vertical_throw_mul", vertical_throw_mul)

    def on_item_throw(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds an event to run when the entity throws items toward the noteblock.

        Parameters:
            event (str): Event to run when the item is thrown.
            target (FilterSubject, optional): Event target. Defaults to FilterSubject.Self.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "on_item_throw" not in self._component:
            self._add_field("on_item_throw", [])

        self._component["on_item_throw"].append(
            {"event": event, "target": target.value}
        )
        return self


class EntityAIGoAndGiveItemsToOwner(AIGoal):
    _identifier = "minecraft:behavior.go_and_give_items_to_owner"

    def __init__(
        self,
        reach_mob_distance: float = 3.0,
        run_speed: float = 1.0,
        throw_force: float = 0.2,
        throw_sound: str = "item_thrown",
        vertical_throw_mul: float = 1.5,
    ) -> None:
        """The entity will attempt to toss the items from its inventory to its owner.

        Parameters:
            reach_mob_distance (float, optional): Sets the desired distance to be reached before giving items to owner. Defaults to 3.0.
            run_speed (float, optional): Sets the entity's speed when running toward the owner. Defaults to 1.0.
            throw_force (float, optional): Sets the throw force. Defaults to 0.2.
            throw_sound (str, optional): Sound to play when this mob throws an item. Defaults to "item_thrown".
            vertical_throw_mul (float, optional): Sets the vertical throw multiplier that is applied on top of the throw force in the vertical direction. Defaults to 1.5.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_go_and_give_items_to_owner
        """
        super().__init__("behavior.go_and_give_items_to_owner")

        if reach_mob_distance != 3.0:
            self._add_field("reach_mob_distance", max(0.0, reach_mob_distance))
        if run_speed != 1.0:
            self._add_field("run_speed", max(0.0, run_speed))
        if throw_force != 0.2:
            self._add_field("throw_force", max(0.0, throw_force))
        if throw_sound != "item_thrown":
            self._add_field("throw_sound", throw_sound)
        if vertical_throw_mul != 1.5:
            self._add_field("vertical_throw_mul", vertical_throw_mul)

    def on_item_throw(
        self,
        event: str,
        target: FilterSubject = FilterSubject.Self,
    ):
        """Adds an event to run when the entity throws items to its owner.

        Parameters:
            event (str): Event to run when the item is thrown.
            target (FilterSubject, optional): Event target. Defaults to FilterSubject.Self.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "on_item_throw" not in self._component:
            self._add_field("on_item_throw", [])

        self._component["on_item_throw"].append(
            {"event": event, "target": target.value}
        )
        return self


class EntityAIInvestigateSuspiciousLocation(AIGoal):
    _identifier = "minecraft:behavior.investigate_suspicious_location"

    def __init__(
        self,
        goal_radius: float = 1.5,
        speed_multiplier: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows this entity to move towards a "suspicious" position based on data gathered in `minecraft:suspect_tracking`.

        Parameters:
            goal_radius (float, optional): Distance in blocks within the entity considers it has reached it's target position. Defaults to 1.5.
            speed_multiplier (float, optional): Movement speed multiplier. Defaults to 1.0.

        Note:
            Requires `minecraft:suspect_tracking`.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_investigate_suspicious_location
        """
        super().__init__("behavior.investigate_suspicious_location")
        self._require_components(EntitySuspectTracking)

        if goal_radius != 1.5:
            self._add_field("goal_radius", max(0.0, goal_radius))
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAIMountPathing(AIGoal):
    _identifier = "minecraft:behavior.mount_pathing"

    def __init__(
        self,
        speed_multiplier: float = 1.0,
        target_dist: float = 0.0,
        track_target: bool = False,
    ) -> None:
        """Allows the mob to move around on its own while mounted seeking a target to attack. Also will allow an entity to target another entity for an attack.

        Parameters:
            speed_multiplier (float, optional): Movement speed multiplier of the mob when using this AI Goal. Defaults to 1.0.
            target_dist (float, optional): The distance at which this mob wants to be away from its target. Defaults to 0.0.
            track_target (bool, optional): If true, this mob will chase after the target as long as it's a valid target. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_mount_pathing
        """
        super().__init__("behavior.mount_pathing")

        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if target_dist != 0.0:
            self._add_field("target_dist", max(0.0, target_dist))
        if track_target:
            self._add_field("track_target", track_target)


class EntityAIStalkAndPounceOnTarget(AIGoal):
    _identifier = "minecraft:behavior.stalk_and_pounce_on_target"

    def __init__(
        self,
        interest_time: Seconds = 2.0,
        leap_distance: float = 0.8,
        leap_height: float = 0.9,
        max_stalk_dist: float = 10.0,
        pounce_max_dist: float = 5.0,
        set_persistent: bool = False,
        stalk_speed: float = 1.2,
        strike_dist: float = 2.0,
        stuck_blocks: Filter = None,
        stuck_time: Seconds = 2.0,
    ) -> None:
        """Allows a mob to stalk a target, then once within range pounce onto a target, on success the target will be attacked dealing damage defined by the attack component. On failure, the mob will risk getting stuck.

        Parameters:
            interest_time (Seconds, optional): The amount of time the mob will be interested before pouncing. This happens when the mob is within range of pouncing. Defaults to 2.0.
            leap_distance (float, optional): The distance in blocks the mob jumps in the direction of its target. Defaults to 0.8.
            leap_height (float, optional): The height in blocks the mob jumps when leaping at its target. Defaults to 0.9.
            max_stalk_dist (float, optional): The maximum distance away a target can be before the mob gives up on stalking. Defaults to 10.0.
            pounce_max_dist (float, optional): The maximum distance away from the target in blocks to begin pouncing at the target. Defaults to 5.0.
            set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Defaults to False.
            stalk_speed (float, optional): The movement speed in which you stalk your target. Defaults to 1.2.
            strike_dist (float, optional): The max distance away from the target when landing from the pounce that will still result in damaging the target. Defaults to 2.0.
            stuck_blocks (Filter, optional): Block filter describing which landed-on blocks can cause the mob to get stuck. Defaults to None.
            stuck_time (Seconds, optional): The amount of time the mob will be stuck if they fail and land on a block they can be stuck on. Defaults to 2.0.

        Note:
            Requires a target-producing behavior and `minecraft:attack`.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_stalk_and_pounce_on_target
        """
        super().__init__("behavior.stalk_and_pounce_on_target")
        self._require_components(EntityAttack)

        if interest_time != 2.0:
            self._add_field("interest_time", max(0.0, interest_time))
        if leap_distance != 0.8:
            self._add_field("leap_dist", max(0.0, leap_distance))
        if leap_height != 0.9:
            self._add_field("leap_height", max(0.0, leap_height))
        if max_stalk_dist != 10.0:
            self._add_field("max_stalk_dist", max(0.0, max_stalk_dist))
        if pounce_max_dist != 5.0:
            self._add_field("pounce_max_dist", max(0.0, pounce_max_dist))
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if stalk_speed != 1.2:
            self._add_field("stalk_speed", max(0.0, stalk_speed))
        if strike_dist != 2.0:
            self._add_field("strike_dist", max(0.0, strike_dist))
        if stuck_blocks is not None:
            self._add_field("stuck_blocks", stuck_blocks)
        if stuck_time != 2.0:
            self._add_field("stuck_time", max(0.0, stuck_time))


class EntityAIEatBlock(AIGoal):
    _identifier = "minecraft:behavior.eat_block"

    def __init__(
        self,
        success_chance: Molang | str | float = 0.02,
        time_until_eat: Seconds = 1.8,
    ) -> None:
        """Allows the entity to consume a block, replace the eaten block with another block, and trigger an event as a result.

        Parameters:
            success_chance (Molang | str | float, optional): A molang expression defining the success chance the entity has to consume a block. Defaults to 0.02.
            time_until_eat (Seconds, optional): The amount of time (in seconds) it takes for the block to be eaten upon a successful eat attempt. Defaults to 1.8.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_block
        """
        super().__init__("behavior.eat_block")

        if success_chance != 0.02:
            self._add_field("success_chance", success_chance)
        if time_until_eat != 1.8:
            self._add_field("time_until_eat", max(0.0, time_until_eat))

    def add_block_pair(
        self,
        eat_block: MinecraftBlockDescriptor | Identifier,
        replace_block: MinecraftBlockDescriptor | Identifier,
    ):
        """Adds an eat-and-replace block pair for the behavior.

        Parameters:
            eat_block (MinecraftBlockDescriptor | Identifier): Block identifier the entity should consume.
            replace_block (MinecraftBlockDescriptor | Identifier): Block identifier that should replace the eaten block.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "eat_and_replace_block_pairs" not in self._component:
            self._add_field("eat_and_replace_block_pairs", [])

        self._component["eat_and_replace_block_pairs"].append(
            {"eat_block": eat_block, "replace_block": replace_block}
        )
        return self

    def on_eat(self, event: str, target: FilterSubject = FilterSubject.Self):
        """Sets the event triggered when the eating animation completes.

        Parameters:
            event (str): Event to trigger when the block is eaten.
            target (FilterSubject, optional): Event target. Defaults to FilterSubject.Self.

        Returns:
            self: Returns the current instance for method chaining.
        """
        self._add_field("on_eat", {"event": event, "target": target.value})
        return self


class EntityAIEatMob(AIGoal):
    _identifier = "minecraft:behavior.eat_mob"

    def __init__(
        self,
        eat_animation_time: Seconds = 1.0,
        eat_mob_sound: str = None,
        loot_table: LootTable | str = None,
        pull_in_force: float = 1.0,
        reach_mob_distance: float = 1.0,
        run_speed: float = 1.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity to eat a specified Mob.

        Parameters:
            eat_animation_time (Seconds, optional): Sets the time in seconds the eat animation should play for. Defaults to 1.0.
            eat_mob_sound (str, optional): Sets the sound that should play when eating a mob. Defaults to None.
            loot_table (LootTable | str, optional): The loot table for loot to be dropped when eating a mob. Defaults to None.
            pull_in_force (float, optional): Sets the force which the mob-to-be-eaten is pulled towards the eating mob. Defaults to 1.0.
            reach_mob_distance (float, optional): Sets the desired distance to be reached before eating the mob. Defaults to 1.0.
            run_speed (float, optional): Sets the entity's speed when running toward the target. Defaults to 1.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_eat_mob
        """
        super().__init__("behavior.eat_mob")

        if eat_animation_time != 1.0:
            self._add_field("eat_animation_time", max(0.0, eat_animation_time))
        if eat_mob_sound is not None:
            self._add_field("eat_mob_sound", eat_mob_sound)
        if loot_table is not None:
            self._add_field("loot_table", loot_table)
        if pull_in_force != 1.0:
            self._add_field("pull_in_force", max(0.0, pull_in_force))
        if reach_mob_distance != 1.0:
            self._add_field("reach_mob_distance", max(0.0, reach_mob_distance))
        if run_speed != 1.0:
            self._add_field("run_speed", max(0.0, run_speed))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAITransportItems(AIGoal):
    _identifier = "minecraft:behavior.transport_items"

    def __init__(
        self,
        allow_simultaneous_interaction: bool = False,
        allowed_items: list[MinecraftItemDescriptor | Identifier] = [],
        destination_container_types: list[
            MinecraftBlockDescriptor | Identifier | dict[str, Any]
        ] = [],
        disallowed_items: list[MinecraftItemDescriptor | Identifier] = [],
        idle_cooldown: int = 20,
        initial_cooldown: int = 0,
        interaction_time: Seconds = 3.0,
        max_stack_size: int = 64,
        max_visited_containers: int = 16,
        place_strategy: str = "any",
        search_distance: Vector2D = (64, 32),
        search_strategy: str = "random",
        source_container_types: list[
            MinecraftBlockDescriptor | Identifier | dict[str, Any]
        ] = [],
        *control_flags: ControlFlags,
    ) -> None:
        """A behavior that enables a mob to transport items from and to containers.

        Parameters:
            allow_simultaneous_interaction (bool, optional): When true the mob will wait until a container is not used by other entities before starting to interact with it. Defaults to False.
            allowed_items (list[MinecraftItemDescriptor | Identifier], optional): A list of item descriptors that are the only items the mob is allowed to transport. Defaults to [].
            destination_container_types (list[MinecraftBlockDescriptor | Identifier | dict[str, Any]], optional): A list of block descriptors that should be container types to put items in. Can be simple block identifier strings or objects with name, states, and tags. Defaults to [].
            disallowed_items (list[MinecraftItemDescriptor | Identifier], optional): A list of item descriptors that are the mob is not allowed to transport. If non-empty "allowed_items" must be empty. Defaults to [].
            idle_cooldown (int, optional): When the mob cannot find a container in which to get or put items, the goal will stop being active for this amount of time in seconds. Defaults to 20.
            initial_cooldown (int, optional): How long the mob will wait after spawning or getting the goal added before the goal can start. Defaults to 0.
            interaction_time (Seconds, optional): The amount of time in seconds spent interacting with the containers. Defaults to 3.0.
            max_stack_size (int, optional): The maximum stack size that the mob will try to take from a container. Value must be >= 1. Value must be <= 64. Defaults to 64.
            max_visited_containers (int, optional): The maximum number of containers that the mob will try to take/place items from before going on cooldown and starting over. Defaults to 16.
            place_strategy (str, optional): The strategy to use for placing the transported item. Defaults to "any".
            search_distance (Vector2D, optional): The maximum search distance horizontally and vertically at which to find containers for taking or placing items. Defaults to (64, 32).
            search_strategy (str, optional): The strategy to use for finding source or destination containers. The nearest valid container or a random valid container in range. Defaults to "random".
            source_container_types (list[MinecraftBlockDescriptor | Identifier | dict[str, Any]], optional): A list of block descriptors that should be container types to take items from. Can be simple block identifier strings or objects with name, states, and tags. Defaults to [].

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_transport_items
        """
        super().__init__("behavior.transport_items")

        if allowed_items and disallowed_items:
            raise ValueError(
                "EntityAITransportItems cannot define both allowed_items and disallowed_items."
            )

        if allow_simultaneous_interaction:
            self._add_field(
                "allow_simultaneous_interaction",
                allow_simultaneous_interaction,
            )
        if allowed_items:
            self._add_field("allowed_items", allowed_items)
        if destination_container_types:
            self._add_field(
                "destination_container_types",
                destination_container_types,
            )
        if disallowed_items:
            self._add_field("disallowed_items", disallowed_items)
        if idle_cooldown != 20:
            self._add_field("idle_cooldown", max(0, idle_cooldown))
        if initial_cooldown != 0:
            self._add_field("initial_cooldown", max(0, initial_cooldown))
        if interaction_time != 3.0:
            self._add_field("interaction_time", max(0.0, interaction_time))
        if max_stack_size != 64:
            self._add_field("max_stack_size", clamp(max_stack_size, 1, 64))
        if max_visited_containers != 16:
            self._add_field(
                "max_visited_containers",
                max(1, max_visited_containers),
            )
        if place_strategy != "any":
            self._add_field("place_strategy", place_strategy)
        if search_distance != (64, 32):
            self._add_field("search_distance", search_distance)
        if search_strategy != "random":
            self._add_field("search_strategy", search_strategy)
        if source_container_types:
            self._add_field("source_container_types", source_container_types)
        if control_flags != ():
            self._add_field("control_flags", control_flags)

    def allow_item(self, item: MinecraftItemDescriptor | Identifier):
        """Adds an item descriptor the mob is allowed to transport.

        Parameters:
            item (MinecraftItemDescriptor | Identifier): Item descriptor to allow.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "disallowed_items" in self._component:
            raise ValueError(
                "EntityAITransportItems cannot mix allowed_items with disallowed_items."
            )
        if "allowed_items" not in self._component:
            self._add_field("allowed_items", [])

        self._component["allowed_items"].append(item)
        return self

    def disallow_item(self, item: MinecraftItemDescriptor | Identifier):
        """Adds an item descriptor the mob is not allowed to transport.

        Parameters:
            item (MinecraftItemDescriptor | Identifier): Item descriptor to disallow.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "allowed_items" in self._component:
            raise ValueError(
                "EntityAITransportItems cannot mix disallowed_items with allowed_items."
            )
        if "disallowed_items" not in self._component:
            self._add_field("disallowed_items", [])

        self._component["disallowed_items"].append(item)
        return self

    def add_destination_container_type(
        self,
        container_type: MinecraftBlockDescriptor | Identifier | dict[str, Any],
        states: dict[str, Any] = None,
        tags: str = None,
    ):
        """Adds a destination container type descriptor.

        Parameters:
            container_type (MinecraftBlockDescriptor | Identifier | dict[str, Any]): Block identifier or full descriptor for a destination container.
            states (dict[str, Any], optional): Block states to match when using a simple identifier. Defaults to None.
            tags (str, optional): Block tags to match when using a simple identifier. Defaults to None.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "destination_container_types" not in self._component:
            self._add_field("destination_container_types", [])

        descriptor = container_type
        if not isinstance(container_type, dict) and (
            states is not None or tags is not None
        ):
            descriptor = {"name": container_type}
            if states is not None:
                descriptor["states"] = states
            if tags is not None:
                descriptor["tags"] = tags

        self._component["destination_container_types"].append(descriptor)
        return self

    def add_source_container_type(
        self,
        container_type: MinecraftBlockDescriptor | Identifier | dict[str, Any],
        states: dict[str, Any] = None,
        tags: str = None,
    ):
        """Adds a source container type descriptor.

        Parameters:
            container_type (MinecraftBlockDescriptor | Identifier | dict[str, Any]): Block identifier or full descriptor for a source container.
            states (dict[str, Any], optional): Block states to match when using a simple identifier. Defaults to None.
            tags (str, optional): Block tags to match when using a simple identifier. Defaults to None.

        Returns:
            self: Returns the current instance for method chaining.
        """
        if "source_container_types" not in self._component:
            self._add_field("source_container_types", [])

        descriptor = container_type
        if not isinstance(container_type, dict) and (
            states is not None or tags is not None
        ):
            descriptor = {"name": container_type}
            if states is not None:
                descriptor["states"] = states
            if tags is not None:
                descriptor["tags"] = tags

        self._component["source_container_types"].append(descriptor)
        return self


class EntityAISilverfishMergeWithStone(AIGoal):
    _identifier = "minecraft:behavior.silverfish_merge_with_stone"

    def __init__(self) -> None:
        """Allows the mob to go into stone blocks like Silverfish do.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_silverfish_merge_with_stone
        """
        super().__init__("behavior.silverfish_merge_with_stone")


class EntityAISilverfishWakeUpFriends(AIGoal):
    _identifier = "minecraft:behavior.silverfish_wake_up_friends"

    def __init__(self) -> None:
        """Allows the mob to alert mobs in nearby blocks to come out.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_silverfish_wake_up_friends
        """
        super().__init__("behavior.silverfish_wake_up_friends")


class EntityAISkeletonHorseTrap(AIGoal):
    _identifier = "minecraft:behavior.skeleton_horse_trap"

    def __init__(self, duration: Seconds = 1.0, within_radius: float = 0.0) -> None:
        """Allows Equine mobs to be Horse Traps and be triggered like them, spawning a lightning bolt and a bunch of horses when a player is nearby. Can only be used by Horses, Mules, Donkeys and Skeleton Horses.

        Parameters:
            duration (Seconds, optional): Amount of time in seconds the trap exists. After this amount of time is elapsed, the trap is removed from the world if it hasn't been activated. Defaults to 1.0.
            within_radius (float, optional): Distance in blocks that the player has to be within to trigger the horse trap. Defaults to 0.0.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_skeleton_horse_trap
        """
        super().__init__("behavior.skeleton_horse_trap")

        if duration != 1.0:
            self._add_field("duration", max(0.0, duration))
        if within_radius != 0.0:
            self._add_field("within_radius", max(0.0, within_radius))


class EntityAISlimeAttack(AIGoal):
    _identifier = "minecraft:behavior.slime_attack"

    def __init__(
        self,
        grow_tired_cooldown_time: Seconds = 15.0,
        set_persistent: bool = False,
        speed_multiplier: float = 1.0,
        x_max_rotation: float = 10.0,
        y_max_rotation: float = 10.0,
        *control_flags: ControlFlags,
    ) -> None:
        """Causes the entity to grow tired every once in a while, while attacking.

        Parameters:
            grow_tired_cooldown_time (Seconds, optional): Cooldown in seconds before the entity can grow tired again. Defaults to 15.0.
            set_persistent (bool, optional): Allows the actor to be set to persist upon targeting a player. Defaults to False.
            speed_multiplier (float, optional): During attack behavior, this multiplier modifies the entity's speed when moving toward the target. Defaults to 1.0.
            x_max_rotation (float, optional): Maximum rotation (in degrees), on the X-axis, this entity can rotate while trying to look at the target. Defaults to 10.0.
            y_max_rotation (float, optional): Maximum rotation (in degrees), on the Y-axis, this entity can rotate while trying to look at the target. Defaults to 10.0.

        Note:
            Requires a target-producing behavior, `minecraft:attack`, and `minecraft:variant`.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_attack
        """
        super().__init__("behavior.slime_attack")
        self._require_components(EntityAttack, EntityVariant)

        if grow_tired_cooldown_time != 15.0:
            self._add_field(
                "grow_tired_cooldown_time",
                max(0.0, grow_tired_cooldown_time),
            )
        if set_persistent:
            self._add_field("set_persistent", set_persistent)
        if speed_multiplier != 1.0:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if x_max_rotation != 10.0:
            self._add_field("x_max_rotation", x_max_rotation)
        if y_max_rotation != 10.0:
            self._add_field("y_max_rotation", y_max_rotation)
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAISlimeFloat(AIGoal):
    _identifier = "minecraft:behavior.slime_float"

    def __init__(
        self,
        jump_chance_percentage: float = 0.800000011920929,
        speed_multiplier: float = 1.2000000476837158,
        *control_flags: ControlFlags,
    ) -> None:
        """Allow slimes to float in water / lava.

        Parameters:
            jump_chance_percentage (float, optional): Percent chance a slime or magma cube has to jump while in water / lava. Defaults to 0.800000011920929.
            speed_multiplier (float, optional): Determines the multiplier the entity's speed is modified by when moving through water / lava. Defaults to 1.2000000476837158.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_float
        """
        super().__init__("behavior.slime_float")

        if jump_chance_percentage != 0.800000011920929:
            self._add_field("jump_chance_percentage", jump_chance_percentage)
        if speed_multiplier != 1.2000000476837158:
            self._add_field("speed_multiplier", max(0.0, speed_multiplier))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAISlimeRandomDirection(AIGoal):
    _identifier = "minecraft:behavior.slime_random_direction"

    def __init__(
        self,
        add_random_time_range: int = 3,
        min_change_direction_time: Seconds = 2.0,
        turn_range: int = 360,
        *control_flags: ControlFlags,
    ) -> None:
        """Allows the entity to move in random directions like a slime.

        Parameters:
            add_random_time_range (int, optional): Additional time (in whole seconds), chosen randomly in the range of [0, "add_random_time_range"], to add to "min_change_direction_time". Defaults to 3.
            min_change_direction_time (Seconds, optional): Constant minimum time (in seconds) to wait before choosing a new direction. Defaults to 2.0.
            turn_range (int, optional): Maximum rotation angle range (in degrees) when randomly choosing a new direction. Defaults to 360.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_slime_random_direction
        """
        super().__init__("behavior.slime_random_direction")

        if add_random_time_range != 3:
            self._add_field("add_random_time_range", max(0, add_random_time_range))
        if min_change_direction_time != 2.0:
            self._add_field(
                "min_change_direction_time",
                max(0.0, min_change_direction_time),
            )
        if turn_range != 360:
            self._add_field("turn_range", max(0, turn_range))
        if control_flags != ():
            self._add_field("control_flags", control_flags)


class EntityAISquidDive(AIGoal):
    _identifier = "minecraft:behavior.squid_dive"

    def __init__(self) -> None:
        """Allows the squid to dive down in water.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_dive
        """
        super().__init__("behavior.squid_dive")


class EntityAISquidFlee(AIGoal):
    _identifier = "minecraft:behavior.squid_flee"

    def __init__(self) -> None:
        """Allows the squid to swim away.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_flee
        """
        super().__init__("behavior.squid_flee")


class EntityAISquidIdle(AIGoal):
    _identifier = "minecraft:behavior.squid_idle"

    def __init__(self) -> None:
        """Allows the squid to swim in place idly.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_idle
        """
        super().__init__("behavior.squid_idle")


class EntityAISquidMoveAwayFromGround(AIGoal):
    _identifier = "minecraft:behavior.squid_move_away_from_ground"

    def __init__(self) -> None:
        """Allows the squid to move away from ground blocks and back to water.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_move_away_from_ground
        """
        super().__init__("behavior.squid_move_away_from_ground")


class EntityAISquidOutOfWater(AIGoal):
    _identifier = "minecraft:behavior.squid_out_of_water"

    def __init__(self) -> None:
        """Allows the squid to stick to the ground when outside water.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/entitygoals/minecraftbehavior_squid_out_of_water
        """
        super().__init__("behavior.squid_out_of_water")
