from .. import ANVIL, NAMESPACE
from ..packages import *

# __all__ = [
#    'AddRider', 'AdmireItem', 'Ageable',
#    'Variant', 'MarkVariant', 'SkinID', 'CollisionBox', 'IsStackable', 'TypeFamily',
#    'InstantDespawn', 'Health', 'Physics', 'KnockbackResistance', 'Pushable', 'IsIllagerCaptain',
#    'IsBaby', 'PushThrough', 'Movement', 'TickWorld'
# ]


class EventObject():
    def __init__(self, event: event, target: Target) -> None:
        return {
            'event': event,
            'target': target
        }

# Filters ==========================================================================


class Filter:
    # Basic configuration
    def _construct_filter(filter_name, subject, operator, domain, value):
        filter = {"test": filter_name, "value": value}
        if subject != FilterSubject.Self:
            filter.update({'subject': subject})
        if operator != FilterOperation.Equals:
            filter.update({'operator': operator})
        if domain != None:
            filter.update({'domain': domain})

        return filter

    # Filter Groups
    @staticmethod
    def all_of(*filters: 'Filter'):
        return {'all_of': [filters]}

    @staticmethod
    def any_of(*filters: 'Filter'):
        return {'any_of': [filters]}

    @staticmethod
    def none_of(*filters: 'Filter'):
        return {'none_of': [filters]}

    # Actual Filters
    @classmethod
    def distance_to_nearest_player(self, value: float, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('distance_to_nearest_player', subject, operator, None, max(0, value))

    @classmethod
    def has_component(self, value: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('has_component', subject, operator, None, value)

    @classmethod
    def is_family(self, value: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('is_family', subject, operator, None, value)

    @classmethod
    def is_block(self, value: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('is_block', subject, operator, None, value)

    @classmethod
    def is_visible(self, value: bool, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('is_visible', subject, operator, None, value)

    @classmethod
    def is_target(self, value: bool, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('is_target', subject, operator, None, value)

    @classmethod
    def is_riding(self, value: bool, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('is_riding', subject, operator, None, value)

    @classmethod
    def has_target(self, value: bool, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('has_target', subject, operator, None, value)

    # Properties

    @classmethod
    def int_property(self, value: int, domain: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('int_property', subject, operator, f'{NAMESPACE}:{domain}', value)

    @classmethod
    def bool_property(self, value: bool, domain: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('bool_property', subject, operator, f'{NAMESPACE}:{domain}', value)

    @classmethod
    def float_property(self, value: float, domain: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('float_property', subject, operator, f'{NAMESPACE}:{domain}', value)

    @classmethod
    def enum_property(self, value: str, domain: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('enum_property', subject, operator, f'{NAMESPACE}:{domain}', value)

    @classmethod
    def has_property(self, value: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('has_property', subject, operator, None, f'{NAMESPACE}:{value}')

    @classmethod
    def has_component(self, value: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('has_component', subject, operator, None, value)

    @classmethod
    def is_owner(self, value: str, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('is_owner', subject, operator, None, value)

    @classmethod
    def has_equipment(self, value: int, domain: FilterEquipmentDomain = FilterEquipmentDomain.Any, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('has_equipment', subject, operator, domain, value)

    @classmethod
    def actor_health(self, value: int, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('actor_health', subject, operator, None, value)

    @classmethod
    def random_chance(self, value: int, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('random_chance', subject, operator, None, value)

    @classmethod
    def target_distance(self, value: int, *, subject: FilterSubject = FilterSubject.Self, operator: FilterOperation = FilterOperation.Equals):
        return self._construct_filter('target_distance', subject, operator, None, value)


class _component(dict):
    def __init__(self, component_name) -> None:
        self.ResetNamespace(component_name)

    def ResetNamespace(self, component_name):
        self.clear()
        self._component_name = component_name
        self._component_namespace = f'minecraft:{self._component_name}'
        self.__setitem__(self._component_namespace, {})

    def AddField(self, key, value):
        self[self._component_namespace][key] = value

    def SetValue(self, value):
        self[self._component_namespace] = value

# Components ==========================================================================


class AddRider(_component):
    def __init__(self, entity_type: Identifier, spawn_event: event = None) -> None:
        '''Adds a rider to the entity. Requires `minecraft:rideable.`.

        Parameters
        ----------
        `entity_type` : `Identifier` `str`.
            The entity type that will be riding this entity
        `spawn_event` : `event` `str`, `optional`.
            The spawn event that will be used when the riding entity is created.

        '''
        super().__init__('addrider')
        self.AddField('entity_type', entity_type)
        if not spawn_event is None:
            self.AddField('spawn_event', spawn_event)


class AdmireItem(_component):
    def __init__(self, cooldown_after_being_attacked: Seconds, duration: Seconds = 10) -> None:
        '''Causes the mob to ignore attackable targets for a given duration.

        Parameters
        ----------
        `cooldown_after_being_attacked` : `Seconds` `int`.
            Duration, in seconds, for which mob won't admire items if it was hurt
        `duration` : `Seconds` `int`.
            Duration, in seconds, that the mob is pacified. `Default: 10`

        '''
        super().__init__('admire_item')
        self.AddField('cooldown_after_being_attacked',
                      cooldown_after_being_attacked)
        if not duration == 10:
            self.AddField('duration', duration)


class Ageable(_component):
    def __init__(self, duration: Seconds, event: event) -> None:
        '''Adds a timer for the entity to grow up. It can be accelerated by giving the entity the items it likes.

        Parameters
        ----------
        `duration` : `Seconds` `int`.
            Amount of time before the entity grows up, -1 for always a baby. `Default: 1200`
        `event` : `event` `str`.
            Minecraft behavior event.

        '''
        super().__init__('ageable')
        self.AddField('duration', duration)
        self[self._component_namespace]['grow_up'] = {
            "event": event,
            "target": "self"
        }


class CollisionBox(_component):
    def __init__(self, height: float, width: float) -> None:
        """Sets the width and height of the Entity's collision box."""
        super().__init__('collision_box')
        self.AddField('height', height)
        self.AddField('width', width)


class TypeFamily(_component):
    def __init__(self, *family: str) -> None:
        """Defines the families this entity belongs to."""
        super().__init__('type_family')
        self.AddField('family', family)


class InstantDespawn(_component):
    def __init__(self, remove_child_entities: bool = False) -> None:
        """"""
        super().__init__('instant_despawn')
        if remove_child_entities:
            self.AddField('remove_child_entities', True)


class Health(_component):
    def __init__(self, value: int, min: int = None, max: int = None) -> None:
        """Sets the amount of health this mob has."""
        super().__init__('health')
        self.AddField('value', value)
        if not max is None:
            self.AddField('max', max)
        if not min is None:
            self.AddField('min', min)


class Physics(_component):
    def __init__(self, has_collision: bool = True, has_gravity: bool = True) -> None:
        """Defines physics properties of an actor, including if it is affected by gravity or if it collides with objects."""
        super().__init__('physics')
        self.AddField('has_collision', has_collision)
        self.AddField('has_gravity', has_gravity)


class KnockbackResistance(_component):
    def __init__(self, value: float) -> None:
        """Determines the amount of knockback resistance that the item has."""
        super().__init__('knockback_resistance')
        self.AddField('value', max(0, min(1, value)))


class Pushable(_component):
    def __init__(self, is_pushable: bool = True, is_pushable_by_piston: bool = True) -> None:
        """Defines what can push an entity between other entities and pistons."""
        super().__init__('pushable')
        self.AddField('is_pushable', is_pushable)
        self.AddField('is_pushable_by_piston', is_pushable_by_piston)


class PushThrough(_component):
    def __init__(self, value: int) -> None:
        """Sets the distance through which the entity can push through."""
        super().__init__('push_through')
        self.AddField('value', value)


class Movement(_component):
    def __init__(self, value: int, max: int = None) -> None:
        """Sets the amount of movement this mob has."""
        super().__init__('movement')
        self.AddField('value', value)
        if not max is None:
            self.AddField('max', max)


class TickWorld(_component):
    def __init__(self, never_despawn: bool = True, radius: int = None, distance_to_players: int = None) -> None:
        """Defines if the entity ticks the world and the radius around it to tick."""
        super().__init__('tick_world')
        self.AddField('never_despawn', never_despawn)
        if not radius is None:
            self.AddField('radius', radius)
        if not distance_to_players is None:
            self.AddField('distance_to_players', distance_to_players)


class CustomHitTest(_component):
    def __init__(self, height: float, width: float, pivot: list[float, float, float] = [0, 1, 0]) -> None:
        """List of hitboxes for melee and ranged hits against the entity."""
        super().__init__('custom_hit_test')
        self.AddField('hitboxes', [{
            "width": width,
            "height": height,
            "pivot": pivot
        }])

    def add_hitbox(self, height: float, width: float, pivot: list[float, float, float] = [0, 1, 0]):
        self[self._component_namespace]['hitboxes'].append({
            "width": width,
            "height": height,
            "pivot": pivot
        })


class CanClimb(_component):
    def __init__(self) -> None:
        """Allows this entity to climb up ladders."""
        super().__init__('can_climb')


class Attack(_component):
    def __init__(self, damage: int, effect_duration: int = None, effect_name: str = None) -> None:
        """Defines an entity's melee attack and any additional effects on it."""
        super().__init__('attack')
        self.AddField('damage', damage)
        if not effect_duration is None:
            self.AddField('effect_duration', effect_duration)
        if not effect_name is None:
            self.AddField('effect_name', effect_name)


class JumpStatic(_component):
    def __init__(self, jump_power: float) -> None:
        """Gives the entity the ability to jump."""
        super().__init__('jump.static')
        self.AddField('jump_power', jump_power)


class HorseJumpStrength(_component):
    def __init__(self, range_min: float, range_max: float) -> None:
        """Allows this mob to jump higher when being ridden by a player."""
        super().__init__('horse.jump_strength')
        self.AddField('hitboxes', [{
            "range_min": range_min,
            "range_max": range_max
        }])


class SpellEffects(_component):
    def __init__(self) -> None:
        """Defines what mob effects to add and remove to the entity when adding this component."""
        super().__init__('spell_effects')
        self.AddField('add_effects', [])
        self.AddField('remove_effects', [])

    def add_effects(self, effect: Effects, duration: int, amplifier: int, ambient: bool = True, visible: bool = True, display_on_screen_animation: bool = True):
        effect = {
            'effect': effect,
            'duration': duration,
            'amplifier': amplifier,
        }
        if ambient is not True:
            effect.update({'ambient': ambient})
        if visible is not True:
            effect.update({'visible': visible})
        if display_on_screen_animation is not True:
            effect.update(
                {'display_on_screen_animation': display_on_screen_animation})

        self[self._component_namespace]['add_effects'].append(effect)
        return self

    def remove_effects(self, *effects: str):
        self[self._component_namespace]['remove_effects'] = effects
        return self


class FrictionModifier(_component):
    def __init__(self, value: int) -> None:
        """Defines how much friction affects this entity."""
        super().__init__('friction_modifier')
        self.AddField('value', value)


class Breathable(_component):
    def __init__(self, breathes_air: bool = True, total_supply: int = 15, suffocate_time: int = -20, inhale_time: int = 0) -> None:
        """Defines what blocks this entity can breathe in and gives them the ability to suffocate."""
        super().__init__('breathable')
        self.AddField('breathes_air', breathes_air)
        if total_supply != 15:
            self.AddField('total_supply', total_supply)
        if suffocate_time != -20:
            self.AddField('suffocate_time', suffocate_time)
        if inhale_time != 0:
            self.AddField('inhale_time', inhale_time)

    @property
    def breathes_lava(self):
        self.AddField('breathes_lava', True)
        return self

    @property
    def breathes_solids(self):
        self.AddField('breathes_solids', True)
        return self

    def breathes_water(self, generates_bubbles: bool = False):
        self.AddField('breathes_water', True)
        if generates_bubbles:
            self.AddField('generates_bubbles', generates_bubbles)
        return self

    @property
    def breathes_solids(self):
        self.AddField('breathes_solids', True)
        return self

    def breathe_blocks(self, *blocks: str):
        self.AddField('blocks', blocks)
        return self

    def non_breathe_blocks(self, *blocks: str):
        self.AddField('non_breathe_blocks', blocks)
        return self


class Variant(_component):
    def __init__(self, value: int) -> None:
        """Used to differentiate the component group of a variant of an entity from others. (e.g. ocelot, villager)."""
        super().__init__('variant')
        self.AddField('value', value)


class MarkVariant(_component):
    def __init__(self, value: int) -> None:
        """Additional variant value. Can be used to further differentiate variants."""
        super().__init__('mark_variant')
        self.AddField('value', value)


class SkinID(_component):
    def __init__(self, value: int) -> None:
        """Skin ID value. Can be used to differentiate skins, such as base skins for villagers."""
        super().__init__('skin_id')
        self.AddField('value', value)


class Scale(_component):
    def __init__(self, value: int) -> None:
        """Sets the entity's visual size."""
        super().__init__('scale')
        self.AddField('value', value)


class ScaleByAge(_component):
    def __init__(self, start_scale: int, end_scale: int) -> None:
        """Defines the entity's size interpolation based on the entity's age."""
        super().__init__('scale_by_age')
        self.AddField('end_scale', end_scale)
        self.AddField('start_scale', start_scale)


class AreaAttack(_component):
    def __init__(self,
                 cause: DamageCause,
                 damage_per_tick: int = 2,
                 damage_range: float = 0.2) -> None:
        """Is a component that does damage to entities that get within range."""
        super().__init__('area_attack')

        self.AddField('cause', cause)
        
        if not damage_per_tick == 2:
            self.AddField('damage_per_tick', damage_per_tick)
        if not damage_range == 0.2:
            self.AddField('damage_range', damage_range)

    def filter(self, entity_filter: dict):
        self.AddField('entity_filter', entity_filter)
        return self


class IsStackable(_component):
    def __init__(self) -> None:
        """Sets that this entity can be stacked."""
        super().__init__('is_stackable')


class IsIllagerCaptain(_component):
    def __init__(self) -> None:
        """Sets that this entity is an illager captain."""
        super().__init__('is_illager_captain')


class IsBaby(_component):
    def __init__(self) -> None:
        """Sets that this entity is a baby."""
        super().__init__('is_baby')


class IsIgnited(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently on fire."""
        super().__init__('is_ignited')


class IsTamed(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently tamed."""
        super().__init__('is_tamed')


class IsCharged(_component):
    def __init__(self) -> None:
        """Sets that this entity is charged."""
        super().__init__('is_charged')


class IsStunned(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently stunned."""
        super().__init__('is_stunned')


class IsSaddled(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently saddled."""
        super().__init__('is_saddled')


class CanClimb(_component):
    def __init__(self) -> None:
        """Allows this entity to climb up ladders."""
        super().__init__('can_climb')


class IsSheared(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently sheared."""
        super().__init__('is_sheared')


class CanFly(_component):
    def __init__(self) -> None:
        """Marks the entity as being able to fly, the pathfinder won't be restricted to paths where a solid block is required underneath it."""
        super().__init__('can_fly')


class CanPowerJump(_component):
    def __init__(self) -> None:
        """Allows the entity to power jump like the horse does in vanilla."""
        super().__init__('can_power_jump')


class IsChested(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently carrying a chest."""
        super().__init__('is_chested')


class OutOfControl(_component):
    def __init__(self) -> None:
        """Defines the entity's 'out of control' state."""
        super().__init__('out_of_control')


class DamageSensor(_component):
    def __init__(self) -> None:
        """Defines what events to call when this entity is damaged by specific entities or items."""
        super().__init__('damage_sensor')
        self.AddField('triggers', [])

    def add_trigger(self,
                    cause: DamageCause, deals_damage: bool = True,
                    on_damage_event: event = None, on_damage_filter: Filter = None,  damage_multiplier: int = 1, damage_modifier: float = 0
                    ):
        damage = {
            'deals_damage': deals_damage,
            'on_damage': {}
        }
        if not cause is DamageCause.All:
            damage['cause'] = cause
        if not on_damage_event is None:
            damage['on_damage'] = {
                'event': on_damage_event
            }
        if not on_damage_filter is None:
            damage['on_damage']['filters'] = on_damage_filter
        if not damage_multiplier == 1:
            damage['damage_multiplier'] = damage_multiplier
        if not damage_modifier == 0:
            damage['damage_modifier'] = damage_modifier

        self[self._component_namespace]['triggers'].append(damage)
        return self


class FollowRange(_component):
    def __init__(self, value: int, max: int = None) -> None:
        """Defines the range of blocks that a mob will pursue a target."""
        super().__init__('follow_range')
        self.AddField('value', value)
        if not max is None:
            self.AddField('max', max)


class MovementType(_component):
    def _basic(self, type: str, max_turn: float = 30) -> None:
        super().ResetNamespace(f'movement.{type}')
        if not max_turn == 30:
            self.AddField('max_turn', max_turn)

    def __init__(self) -> None:
        """Defines the movement of an entity."""
        super().__init__(f'movement.basic')

    def Basic(self, max_turn: float = 30):
        """Defines the movement of an entity."""
        self._basic('basic', max_turn)
        return self

    def Amphibious(self, max_turn: float = 30):
        """Allows the mob to swim in water and walk on land."""
        self._basic('amphibious', max_turn)
        return self

    def Dolphin(self) -> None:
        """Allows the mob to swim in water like a dolphin."""
        self._basic('dolphin')
        return self

    def Fly(self, max_turn: float = 30, start_speed: float = 0.1, speed_when_turning: float = 0.2) -> None:
        """Causes the mob to fly."""
        self._basic('fly', max_turn)
        if not start_speed == 0.1:
            self.AddField('start_speed', start_speed)
        if not speed_when_turning == 0.2:
            self.AddField('speed_when_turning', speed_when_turning)
        return self

    def Generic(self, max_turn: float = 30):
        """Allows a mob to fly, swim, climb, etc."""
        self._basic('generic', max_turn)
        return self

    def Glide(self, max_turn: float = 30, start_speed: float = 0.1, speed_when_turning: float = 0.2):
        """Is the move control for a flying mob that has a gliding movement."""
        self._basic('generic', max_turn)
        if not start_speed == 0.1:
            self.AddField('start_speed', start_speed)
        if not speed_when_turning == 0.2:
            self.AddField('speed_when_turning', speed_when_turning)
        return self

    def Jump(self, max_turn: float = 30, jump_delay: tuple[float, float] = (0, 0)):
        """Causes the mob to jump as it moves with a specified delay between jumps."""
        self._basic('hover', max_turn)
        if not jump_delay == (0, 0):
            self.AddField('jump_delay', jump_delay)
        return self

    def Skip(self, max_turn: float = 30):
        """Causes the mob to hop as it moves."""
        self._basic('skip', max_turn)
        return self

    def Sway(self, max_turn: float = 30, sway_amplitude: float = 0.05, sway_frequency: float = 0.5):
        """Causes the mob to sway side to side giving the impression it is swimming."""
        self._basic('skip', max_turn)
        if not sway_amplitude == 0.05:
            self.AddField('sway_amplitude', sway_amplitude)
        if not sway_frequency == 0.5:
            self.AddField('sway_frequency', sway_frequency)
        return self


class NavigationType(_component):
    def _basic(
        self,
        type: str,
        avoid_damage_blocks: bool = False,
        avoid_portals: bool = False,
        avoid_sun: bool = False,
        avoid_water: bool = False,
        can_breach: bool = False,
        can_break_doors: bool = False,
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
        blocks_to_avoid: list[str] = [],
    ) -> None:
        super().ResetNamespace(f'navigation.{type}')
        if avoid_damage_blocks:
            self.AddField('avoid_damage_blocks', avoid_damage_blocks)
        if avoid_portals:
            self.AddField('avoid_portals', avoid_portals)
        if avoid_sun:
            self.AddField('avoid_sun', avoid_sun)
        if avoid_water:
            self.AddField('avoid_water', avoid_water)
        if can_breach:
            self.AddField('can_breach', can_breach)
        if can_break_doors:
            self.AddField('can_break_doors', can_break_doors)
        if not can_jump:
            self.AddField('can_jump', can_jump)
        if can_open_doors:
            self.AddField('can_open_doors', can_open_doors)
        if can_open_iron_doors:
            self.AddField('can_open_iron_doors', can_open_iron_doors)
        if not can_pass_doors:
            self.AddField('can_pass_doors', can_pass_doors)
        if can_path_from_air:
            self.AddField('can_path_from_air', can_path_from_air)
        if can_path_over_lava:
            self.AddField('can_path_over_lava', can_path_over_lava)
        if can_path_over_water:
            self.AddField('can_path_over_water', can_path_over_water)
        if not can_sink:
            self.AddField('can_sink', can_sink)
        if can_swim:
            self.AddField('can_swim', can_swim)
        if not can_walk:
            self.AddField('can_walk', can_walk)
        if can_walk_in_lava:
            self.AddField('can_walk_in_lava', can_walk_in_lava)
        if is_amphibious:
            self.AddField('is_amphibious', is_amphibious)
        if blocks_to_avoid == []:
            self.AddField('blocks_to_avoid', blocks_to_avoid)

    def __init__(self) -> None:
        """Allows this entity to generate paths by walking, swimming, flying and/or climbing around and jumping up and down a block."""
        super().__init__(f'navigation.generic')

    def Climb(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """Allows this entity to generate paths that include vertical walls like the vanilla Spiders do."""
        self._basic('climb', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self

    def Float(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """Allows this entity to generate paths by flying around the air like the regular Ghast."""
        self._basic('float', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self

    def Fly(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """Allows this entity to generate paths in the air like the vanilla Parrots do."""
        self._basic('fly', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self

    def Generic(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """Allows this entity to generate paths by walking, swimming, flying and/or climbing around and jumping up and down a block."""
        self._basic('generic', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self

    def Hover(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """Allows this entity to generate paths in the air like the vanilla Bees do. Keeps them from falling out of the skies and doing predictive movement."""
        self._basic('hover', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self

    def Swim(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """Allows this entity to generate paths that include water."""
        self._basic('swim', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self

    def Walk(self, avoid_damage_blocks: bool = False, avoid_portals: bool = False, avoid_sun: bool = False, avoid_water: bool = False, can_breach: bool = False, can_break_doors: bool = False, can_jump: bool = True, can_open_doors: bool = False, can_open_iron_doors: bool = False, can_pass_doors: bool = True, can_path_from_air: bool = False, can_path_over_lava: bool = False, can_path_over_water: bool = False, can_sink: bool = True, can_swim: bool = False, can_walk: bool = True, can_walk_in_lava: bool = False, is_amphibious: bool = False, blocks_to_avoid: list[str] = []):
        """llows this entity to generate paths by walking around and jumping up and down a block like regular mobs."""
        self._basic('walk', avoid_damage_blocks, avoid_portals, avoid_sun, avoid_water, can_breach, can_break_doors, can_jump, can_open_doors, can_open_iron_doors,
                    can_pass_doors, can_path_from_air, can_path_over_lava, can_path_over_water, can_sink, can_swim, can_walk, can_walk_in_lava, is_amphibious, blocks_to_avoid)
        return self


class EnvironmentSensor(_component):
    def __init__(self) -> None:
        """Creates a trigger based on environment conditions."""
        super().__init__('environment_sensor')
        self.AddField('triggers', [])

    def trigger(self, event: event, filters: Filter):
        self[self._component_namespace]['triggers'].append({
            'filters': filters,
            'event': event
        })
        return self


class PreferredPath(_component):
    def __init__(self, default_block_cost: int = 0, jump_cost: int = 0, max_fall_blocks: int = 3) -> None:
        """Specifies costing information for mobs that prefer to walk on preferred paths."""
        super().__init__('preferred_path')
        self.AddField('default_block_cost', default_block_cost)
        self.AddField('jump_cost', jump_cost)
        self.AddField('max_fall_blocks', max_fall_blocks)
        self.AddField('preferred_path_blocks', [])

    def add_blocks(self, cost: int, *blocks: list[str]):
        self[self._component_namespace]['preferred_path_blocks'].append({
            "cost": cost,
            "blocks": blocks
        })
        return self


class TargetNearbySensor(_component):
    def __init__(self, inside_range: int = 1, outside_range: int = 5, must_see: bool = False) -> None:
        """Defines the entity's range within which it can see or sense other entities to target them."""
        super().__init__('target_nearby_sensor')
        self.AddField('inside_range', inside_range)
        self.AddField('outside_range', outside_range)
        self.AddField('must_see', must_see)

    def on_inside_range(self, event: event, target: FilterSubject):
        self.AddField('on_inside_range', {"event": event, "target": target})
        return self

    def on_outside_range(self, event: event, target: FilterSubject):
        self.AddField('on_outside_range', {"event": event, "target": target})
        return self

    def on_vision_lost_inside_range(self, event: event, target: FilterSubject):
        self.AddField('on_vision_lost_inside_range', {
                      "event": event, "target": target})
        return self


class NearestAttackableTarget(_component):
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
        super().__init__('behavior.nearest_attackable_target')
        self.AddField('entity_types', [])

        if not attack_interval == 0:
            self.AddField('attack_interval', attack_interval)
        if not attack_interval_min == 0:
            self.AddField('attack_interval_min', attack_interval_min)
        if attack_owner:
            self.AddField('attack_owner', attack_owner)
        if must_reach:
            self.AddField('must_reach', must_reach)
        if must_see:
            self.AddField('must_see', must_see)
        if not must_see_forget_duration == 3.0:
            self.AddField('must_see_forget_duration', must_see_forget_duration)
        if not persist_time == 0.0:
            self.AddField('persist_time', persist_time)
        if reevaluate_description:
            self.AddField('reevaluate_description', reevaluate_description)
        if reselect_targets:
            self.AddField('reselect_targets', reselect_targets)
        if not scan_interval == 10:
            self.AddField('scan_interval', scan_interval)
        if set_persistent:
            self.AddField('set_persistent', set_persistent)
        if not target_invisible_multiplier == 0.7:
            self.AddField('target_invisible_multiplier',
                          target_invisible_multiplier)
        if not target_search_height == -0.1:
            self.AddField('target_search_height', target_search_height)
        if not target_sneak_visibility_multiplier == 0.8:
            self.AddField('target_sneak_visibility_multiplier',
                          target_sneak_visibility_multiplier)
        if not within_radius == 0.0:
            self.AddField('within_radius', within_radius)

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self

    def add_target(self, 
                   filters: Filter, 
                   max_dist: int = 32, 
                   must_see: bool = False,
                   must_see_forget_duration : float = 3.0,
                   sprint_speed_multiplier : float = 1.0,
                   walk_speed_multiplier : float = 1.0,
                ):
        # empty dicts will be removed at compilation
        self[self._component_namespace]['entity_types'].append({
            "filters": filters,
            "max_dist": max_dist if max_dist != 32 else {},
            "must_see": must_see if must_see else {},
            "must_see_forget_duration": must_see_forget_duration if must_see_forget_duration != 3.0 else {},
            "sprint_speed_multiplier": sprint_speed_multiplier if sprint_speed_multiplier != 1.0 else {},
            "walk_speed_multiplier": walk_speed_multiplier if walk_speed_multiplier != 1.0 else {},
        })
        return self


class NearestPrioritizedAttackableTarget(_component):
    def __init__(
            self,
            attack_interval: int = 0,
            attack_interval_min: int = 0,
            attack_owner: bool = False,
            must_reach: bool = False,
            must_see: bool = False,
            must_see_forget_duration: float = 3.0,
            persist_time: float = 0.0,

        reselect_targets: bool = False,
        scan_interval: int = 10,
        set_persistent: bool = False,
        target_invisible_multiplier: float = 0.7,
        target_search_height: float = -0.1,
        target_sneak_visibility_multiplier: float = 0.8,
        within_radius: float = 0.0,
    ) -> None:
        """Allows an entity to attack the closest target within a given subset of specific target types."""
        super().__init__('behavior.nearest_prioritized_attackable_target')
        self.AddField('entity_types', [])

        if not attack_interval == 0:
            self.AddField('attack_interval', attack_interval)
        if not attack_interval_min == 0:
            self.AddField('attack_interval_min', attack_interval_min)
        if attack_owner:
            self.AddField('attack_owner', attack_owner)
        if must_reach:
            self.AddField('must_reach', must_reach)
        if must_see:
            self.AddField('must_see', must_see)
        if not must_see_forget_duration == 3.0:
            self.AddField('must_see_forget_duration', must_see_forget_duration)
        if not persist_time == 0.0:
            self.AddField('persist_time', persist_time)
        if reselect_targets:
            self.AddField('reselect_targets', reselect_targets)
        if not scan_interval == 10:
            self.AddField('scan_interval', scan_interval)
        if set_persistent:
            self.AddField('set_persistent', set_persistent)
        if not target_invisible_multiplier == 0.7:
            self.AddField('target_invisible_multiplier',
                          target_invisible_multiplier)
        if not target_search_height == -0.1:
            self.AddField('target_search_height', target_search_height)
        if not target_sneak_visibility_multiplier == 0.8:
            self.AddField('target_sneak_visibility_multiplier',
                          target_sneak_visibility_multiplier)
        if not within_radius == 0.0:
            self.AddField('within_radius', within_radius)

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self

    def add_target(self, filters: Filter, must_see: bool = False, max_dist: int = 32, reevaluate_description: bool = False,):
        # empty dicts will be removed at compilation
        self[self._component_namespace]['entity_types'].append({
            "filters": filters,
            "must_see": must_see if must_see else {},
            "max_dist": max_dist if max_dist != max_dist else {},
            "reevaluate_description": reevaluate_description if reevaluate_description else {}
        })
        return self


class RandomLookAround(_component):
    def __init__(self,
                 probability: float = 0.2,
                 angle_of_view_horizontal: int = 360,
                 angle_of_view_vertical: int = 360,
                 look_distance: float = 8.0,
                 look_time: list[float, float] | float = (2, 4)) -> None:
        """Allows an entity to choose a random direction to look in for a random duration within a range."""
        super().__init__('behavior.random_look_around')
        self.AddField('probability', clamp(probability, 0, 1))
        if not angle_of_view_horizontal == 360:
            self.AddField('angle_of_view_horizontal', angle_of_view_horizontal)
        if not angle_of_view_vertical == 360:
            self.AddField('angle_of_view_vertical', angle_of_view_vertical)
        if not look_distance == 8:
            self.AddField('look_distance', look_distance)
        if not look_time == (2, 4):
            self.AddField('look_time', look_time)

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class Timer(_component):
    def __init__(self,
                 event: event,
                 target: FilterSubject = FilterSubject.Self,
                 looping: bool = True,
                 randomInterval: bool = True,
                 time: list[float, float] | float = 0) -> None:
        """Adds a timer after which an event will fire."""
        super().__init__('timer')

        self.AddField('time_down_event', {
            "event": event,
            "target": target
        })

        if not looping:
            self.AddField('looping', looping)
        if not randomInterval:
            self.AddField('randomInterval', randomInterval)
        if not time == (0, 0):
            self.AddField('time', time)

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class Rideable(_component):
    component_name = 'rideable'
    def __init__(self,
                 interact_text: str = 'Mount',
                 controlling_seat: int = 0,
                 crouching_skip_interact: bool = True,
                 pull_in_entities: bool = False,
                 rider_can_interact: bool = False,
                 *family_types: str) -> None:
        """Determines whether this entity can be ridden. Allows specifying the different seat positions and quantity."""
        super().__init__(self.component_name)
        self._seat_count = 0

        if not interact_text == 'Mount':
            t = interact_text.lower().replace(' ', '_')
            self.AddField('interact_text', f'action.interact.{t}')
            ANVIL.localize(f'action.interact.{t}={interact_text}')
        if not controlling_seat == 0:
            self.AddField('controlling_seat', controlling_seat)
        if not crouching_skip_interact:
            self.AddField('crouching_skip_interact', crouching_skip_interact)
        if pull_in_entities:
            self.AddField('pull_in_entities', pull_in_entities)
        if rider_can_interact:
            self.AddField('rider_can_interact', rider_can_interact)

        self.AddField('family_types', family_types if len(
            family_types) > 0 else [])
        self.AddField('seats', [])

    def add_seat(self, position: position, max_rider_count: int, min_rider_count: int = 0, lock_rider_rotation: int = 181, rotate_rider_by: int = 0):
        self._seat_count += 1
        self.AddField('seat_count', self._seat_count)

        self[self._component_namespace]['seats'].append({
            "max_rider_count": max_rider_count,
            "position": position,
            "lock_rider_rotation": lock_rider_rotation if not lock_rider_rotation == 181 else {},
            "min_rider_count": min_rider_count if not min_rider_count == 0 else {},
            "rotate_rider_by": rotate_rider_by if not rotate_rider_by == 0 else {},
        })

        return self


class Projectile(_component):
    def __init__(self, 
                 anchor: int = 0, 
                 angle_offset: float = 0,
                 catch_fire: bool = False,
                 crit_particle_on_hurt: bool = False,
                 destroy_on_hurt: bool = False,
                 fire_affected_by_griefing: bool = False, 
                 gravity: float = 0.05,
                 hit_sound : str = '',
                 hit_ground_sound: str = '',
                 homing: bool = False,
                 inertia: float = 0.09,
                 is_dangerous: bool = False,
                 knockback: bool = True,
                 lightning: bool = False, 
                 liquid_inertia: float = 0.6,
                 multiple_targets: bool =  True,
                 offset: coordinate = (0, 0, 0),
                 on_fire_timer: float = 0.0,
                 particle: str = 'particle',
                 power: float = 1.3,
                 reflect_on_hurt : bool = False,
                 shoot_sound: str = '',
                 shoot_target: bool = True,
                 should_bounce: bool = False,
                 splash_potion: bool = False,
                 splash_range: int = 4,
                 stop_on_hurt: bool = False, #Determines if the projectile stops when the target is hurt.
                 uncertainty_base: int = 0,	#Decimal The base accuracy. Accuracy is determined by the formula uncertaintyBase - difficultyLevel * uncertaintyMultiplier.
                 uncertainty_multiplier: int = 0 #Determines how much difficulty affects accuracy. Accuracy is determined by the formula uncertaintyBase - difficultyLevel * uncertaintyMultiplier.
                 ) -> None:
        """Allows the entity to be a thrown entity."""
        super().__init__('projectile')
        if anchor != 0:
            self.AddField('anchor', anchor)
        if angle_offset != 0:
            self.AddField('angle_offset', angle_offset)
        if catch_fire:
            self.AddField('catch_fire', catch_fire)
        if crit_particle_on_hurt:
            self.AddField('crit_particle_on_hurt', crit_particle_on_hurt)
        if destroy_on_hurt:
            self.AddField('destroy_on_hurt', destroy_on_hurt)
        if fire_affected_by_griefing:
            self.AddField('fire_affected_by_griefing', fire_affected_by_griefing)
        if gravity != 0.05:
            self.AddField('gravity', gravity)
        if hit_sound != '':
            self.AddField('hit_sound', hit_sound)
        if hit_ground_sound != '':
            self.AddField('hit_ground_sound', hit_ground_sound)
        if homing:
            self.AddField('homing', homing)
        if inertia != 0.09:
            self.AddField('inertia', inertia)
        if is_dangerous:
            self.AddField('is_dangerous', is_dangerous)
        if not knockback:
            self.AddField('knockback', knockback)
        if lightning:
            self.AddField('lightning', lightning)
        if liquid_inertia != 0.6:
            self.AddField('liquid_inertia', liquid_inertia)
        if not multiple_targets:
            self.AddField('multiple_targets', multiple_targets)
        if offset != (0, 0, 0):
            self.AddField('offset', offset)
        if on_fire_timer != 0.0:
            self.AddField('on_fire_timer', on_fire_timer)
        if particle != 'particle':
            self.AddField('particle', particle)
        if power != 1.3:
            self.AddField('power', power)
        if reflect_on_hurt :
            self.AddField('reflect_on_hurt', reflect_on_hurt)
        if shoot_sound != '':
            self.AddField('shoot_sound', shoot_sound)
        if not shoot_target:
            self.AddField('shoot_target', shoot_target)
        if should_bounce:
            self.AddField('should_bounce', should_bounce)
        if splash_potion:
            self.AddField('splash_potion', splash_potion)
        if splash_range != 4:
            self.AddField('splash_range', splash_range)
        if stop_on_hurt:
            self.AddField('stop_on_hurt', stop_on_hurt)
        if uncertainty_base != 0:
            self.AddField('uncertainty_base', uncertainty_base)
        if uncertainty_multiplier != 0:
            self.AddField('uncertainty_multiplier', uncertainty_multiplier)

    def filter(self, filter: Filter):
        self.AddField('filter', filter)
        return self
    
    def on_hit(self,
                catch_fire: bool = False,   #Determines if the struck object is set on fire.
                douse_fire: bool = False,   #If the target is on fire, then douse the fire.
                ignite: bool = False,   #Determines if a fire may be started on a flammable target.
                on_fire_time: float = 0, #The amount of time a target will remain on fire.
                potion_effect: int = -1,    #Defines the effect the arrow will apply to the entity it hits.
                spawn_aoe_cloud: bool = False,  #Potion spawns an area of effect cloud. See the table below for all spawn_aoe_cloud parameters.
                teleport_owner: bool = False,   #Determines if the owner is transported on hit.
            ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})
        if catch_fire:
            self[self._component_namespace]['on_hit']['catch_fire'] = catch_fire
        if douse_fire:
            self[self._component_namespace]['on_hit']['douse_fire'] = douse_fire
        if ignite:
            self[self._component_namespace]['on_hit']['ignite'] = ignite
        if on_fire_time != 0:
            self[self._component_namespace]['on_hit']['on_fire_time'] = on_fire_time
        if potion_effect != -1:
            self[self._component_namespace]['on_hit']['potion_effect'] = potion_effect
        if spawn_aoe_cloud:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud'] = spawn_aoe_cloud
        if teleport_owner:
            self[self._component_namespace]['on_hit']['teleport_owner'] = teleport_owner
        return self

    def impact_damage(self,
            filter: Filter = None,   #The identifier of an entity that can be hit.
            catch_fire: bool = False,   #Determines if the struck object is set on fire.
            channeling: bool = True,   #Whether lightning can be channeled through the weapon.
            damage: int = 1,   #The damage dealt on impact.
            destroy_on_hit: bool = False,   #Projectile is removed on hit.
            destroy_on_hit_requires_damage: bool = True,   #If true, then the hit must cause damage to destroy the projectile.
            knockback: bool = True,   #If true, the projectile will knock back the entity it hits.
            max_critical_damage: int = 5,   #Maximum critical damage.
            min_critical_damage: int = 0,   #Minimum critical damage.
            power_multiplier: float = 2,   #How much the base damage is multiplied.
            semi_random_diff_damage: bool = False,   #If true, damage will be randomized based on damage and speed
            set_last_hurt_requires_damage: bool = False,   #If true, then the hit must cause damage to update the last hurt property.
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})
        self[self._component_namespace]['on_hit']['impact_damage'] = {}
        if not filter is None:
            self[self._component_namespace]['on_hit']['impact_damage']['filter'] = filter
        if catch_fire:
            self[self._component_namespace]['on_hit']['impact_damage']['catch_fire'] = catch_fire
        if not channeling:
            self[self._component_namespace]['on_hit']['impact_damage']['channeling'] = channeling
        if damage != 1:
            self[self._component_namespace]['on_hit']['impact_damage']['damage'] = damage
        if destroy_on_hit:
            self[self._component_namespace]['on_hit']['impact_damage']['destroy_on_hit'] = destroy_on_hit
        if not destroy_on_hit_requires_damage:
            self[self._component_namespace]['on_hit']['impact_damage']['destroy_on_hit_requires_damage'] = destroy_on_hit_requires_damage
        if not knockback:
            self[self._component_namespace]['on_hit']['impact_damage']['knockback'] = knockback
        if max_critical_damage != 5:
            self[self._component_namespace]['on_hit']['impact_damage']['max_critical_damage'] = max_critical_damage
        if min_critical_damage != 0:
            self[self._component_namespace]['on_hit']['impact_damage']['min_critical_damage'] = min_critical_damage
        if power_multiplier != 2:
            self[self._component_namespace]['on_hit']['impact_damage']['power_multiplier'] = power_multiplier
        if semi_random_diff_damage:
            self[self._component_namespace]['on_hit']['impact_damage']['semi_random_diff_damage'] = semi_random_diff_damage
        if set_last_hurt_requires_damage:
            self[self._component_namespace]['on_hit']['impact_damage']['set_last_hurt_requires_damage'] = set_last_hurt_requires_damage
        
        return self
    
    def definition_event(self,
            event: event,
            target: FilterSubject,
            affect_projectile: bool = False,    #The projectile that will be affected by this event.
            affect_shooter: bool = False,    #The shooter that will be affected by this event.
            affect_splash_area: bool = False,    #All entities in the splash area will be affected by this event.
            splash_area: float = 0,     #The splash area that will be affected.
            affect_target: bool = False,    #The target will be affected by this event.
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})
        self[self._component_namespace]['on_hit']['definition_event'] = {'event_trigger': {'event': event, 'target': target}}

        if affect_projectile:
            self[self._component_namespace]['on_hit']['definition_event']['affect_projectile'] = affect_projectile
        if affect_shooter:
            self[self._component_namespace]['on_hit']['definition_event']['affect_shooter'] = affect_shooter
        if affect_splash_area:
            self[self._component_namespace]['on_hit']['definition_event']['affect_splash_area'] = affect_splash_area
        if splash_area:
            self[self._component_namespace]['on_hit']['definition_event']['splash_area'] = splash_area
        if affect_target:
            self[self._component_namespace]['on_hit']['definition_event']['affect_target'] = affect_target

        return self
    
    def spawn_aoe_cloud(self,
                         affect_owner: bool = True,
                         color: tuple[int, int, int] = (1, 1, 1),
                         duration: int = 0,
                         particle: int = 0,
                         potion: int = -1,
                         radius: int = 0,
                         radius_on_use: int = -1,
                         reapplication_delay: int = 0,
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        self[self._component_namespace]['on_hit']['spawn_aoe_cloud'] = {}
        
        if not affect_owner:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['affect_owner'] = affect_owner
        if color != (1, 1, 1):
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['color'] = color
        if duration != 0:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['duration'] = duration
        if particle != 0:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['particle'] = particle
        if potion != -1:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['potion'] = potion
        if radius != 0:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['radius'] = radius
        if radius_on_use != -1:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['radius_on_use'] = radius_on_use
        if reapplication_delay != 0:
            self[self._component_namespace]['on_hit']['spawn_aoe_cloud']['reapplication_delay'] = reapplication_delay

        return self
    
    def spawn_chance(self,
                     spawn_definition: str,
                     spawn_baby: bool = False,
                     first_spawn_count: int = 0,
                     first_spawn_percent_chance: int = 0,
                     second_spawn_chance: int = 32,
                     second_spawn_count: int = 0,
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        self[self._component_namespace]['on_hit']['spawn_chance'] = {'spawn_definition': spawn_definition}

        if spawn_baby:
            self[self._component_namespace]['on_hit']['spawn_chance']['spawn_baby'] = spawn_baby
        if first_spawn_count:
            self[self._component_namespace]['on_hit']['spawn_chance']['first_spawn_count'] = first_spawn_count
        if first_spawn_percent_chance:
            self[self._component_namespace]['on_hit']['spawn_chance']['first_spawn_percent_chance'] = first_spawn_percent_chance
        if second_spawn_chance:
            self[self._component_namespace]['on_hit']['spawn_chance']['second_spawn_chance'] = second_spawn_chance
        if second_spawn_count:
            self[self._component_namespace]['on_hit']['spawn_chance']['second_spawn_count'] = second_spawn_count

        return self
    
    def particle_on_hit(self,
                     particle_type: str,
                     on_other_hit: bool = False,
                     on_entity_hit: bool = False,
                     num_particles: int = 6,
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        self[self._component_namespace]['on_hit']['particle_on_hit'] = {'particle_type': particle_type}

        if on_other_hit:
            self[self._component_namespace]['on_hit']['particle_on_hit']['on_other_hit'] = on_other_hit
        if on_entity_hit:
            self[self._component_namespace]['on_hit']['particle_on_hit']['on_entity_hit'] = on_entity_hit
        if num_particles != 6:
            self[self._component_namespace]['on_hit']['particle_on_hit']['num_particles'] = num_particles

        return self
    
    def mob_effect(self,
                   effect: str,
                   amplifier: int = 1,
                   ambient: bool = False,
                   visible: bool = False,
                   duration: int = 1,
                   durationeasy: int = 0,
                   durationheard: int = 800,
                   durationnormal: int = 200,
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        self[self._component_namespace]['on_hit']['mob_effect'] = {'effect': effect}

        if amplifier != 1:
            self[self._component_namespace]['on_hit']['mob_effect']['amplifier'] = amplifier
        if ambient:
            self[self._component_namespace]['on_hit']['mob_effect']['ambient'] = ambient
        if visible:
            self[self._component_namespace]['on_hit']['mob_effect']['visible'] = visible
        if duration != 1:
            self[self._component_namespace]['on_hit']['mob_effect']['duration'] = duration
        if durationeasy != 0:
            self[self._component_namespace]['on_hit']['mob_effect']['durationeasy'] = durationeasy
        if durationheard != 800:
            self[self._component_namespace]['on_hit']['mob_effect']['durationheard'] = durationheard
        if durationnormal != 200:
            self[self._component_namespace]['on_hit']['mob_effect']['durationnormal'] = durationnormal

        return self
    
    def freeze_on_hit(self,
                      size: int,
                      snap_to_block: bool,
                      shape: str = "sphere",
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        self[self._component_namespace]['on_hit']['freeze_on_hit'] = {'size': size, 'snap_to_block': snap_to_block}
        if shape not in ['sphere', 'cube']:
            RaiseError('Unknown shape, must be sphere or cube')
        self[self._component_namespace]['on_hit']['freeze_on_hit']['shape'] = shape

        return self
    
    def grant_xp(self, xp: tuple[int, int]):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        if xp[0] == xp[1]:
            self[self._component_namespace]['on_hit']['grant_xp'] = {'xp': xp}
        else:
            self[self._component_namespace]['on_hit']['grant_xp'] = {'minXP': min(xp), 'maxXP': max(xp)}

        return self
    
    def hurt_owner(self,
                   owner_damage: int = 0,
                   knockback: bool = False,
                   ignite: bool = False,
        ):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})

        self[self._component_namespace]['on_hit']['hurt_owner'] = {}

        if owner_damage != 0:
            self[self._component_namespace]['on_hit']['hurt_owner']['owner_damage'] = owner_damage
        if knockback:
            self[self._component_namespace]['on_hit']['hurt_owner']['knockback'] = knockback
        if ignite:
            self[self._component_namespace]['on_hit']['hurt_owner']['ignite'] = ignite

        return self
    
    @property
    def remove_on_hit(self):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})
        
        self[self._component_namespace]['on_hit']['remove_on_hit'] = {'remove': True}

        return self
    
    def stick_in_ground(self, shake_time: float):
        try: self[self._component_namespace]['on_hit']
        except KeyError:
            self.AddField('on_hit', {})
        
        self[self._component_namespace]['on_hit']['stick_in_ground'] = {'shake_time': shake_time}

        return self
    
    @property
    def thrown_potion_effect(self):
        try: self[self._component_namespace]['on_hit']
        except KeyError: self.AddField('on_hit', {})
        
        self[self._component_namespace]['on_hit']['thrown_potion_effect'] = {}

        return self


class Explode(_component):
    def __init__(self,
                 breaks_blocks: bool = True,
                 causes_fire : bool = False,
                 destroy_affected_by_griefing: bool = False,
                 fire_affected_by_griefing: bool = False,
                 fuse_length: tuple[float, float] = [0.0, 0.0],
                 fuse_lit: bool = False,
                 max_resistance: int = 	3.40282e+38,
                 power: int = 3) -> None:
        """Defines how the entity explodes."""
        super().__init__('explode')

        if not breaks_blocks:
            self.AddField('breaks_blocks', breaks_blocks)
        if causes_fire:
            self.AddField('causes_fire', causes_fire)
        if destroy_affected_by_griefing:
            self.AddField('destroy_affected_by_griefing', destroy_affected_by_griefing)
        if fire_affected_by_griefing:
            self.AddField('fire_affected_by_griefing', fire_affected_by_griefing)
        if fuse_length != [0.0, 0.0]:
            self.AddField('fuse_length', fuse_length)
        if fuse_lit:
            self.AddField('fuse_lit', fuse_lit)
        if max_resistance != 3.40282e+38:
            self.AddField('max_resistance', max_resistance)
        if power != 3:
            self.AddField('power', power)


class KnockbackRoar(_component):
    def __init__(self,
                 attack_time: float = 0.5,
                 cooldown_time: float = 0.1,
                 damage_filters: Filter = None,
                 duration: float = 1,
                 knockback_damage: int = 6,
                 knockback_filters: Filter = None,
                 knockback_height_cap: float = 0.4,
                 knockback_horizontal_strength: int = 4,
                 knockback_range: int = 4,
                 knockback_vertical_strength: int = 4) -> None:
        """Compels an entity to emit a roar effect that knocks back other entities in a set radius from where the roar was emitted."""
        super().__init__('behavior.knockback_roar')
        
        if not attack_time == 0.5:
            self.AddField('attack_time', attack_time)
        if not cooldown_time == 0.1:
            self.AddField('cooldown_time', cooldown_time)
        if not damage_filters is None:
            self.AddField('damage_filters', damage_filters)
        if not duration == 1:
            self.AddField('duration', duration)
        if not knockback_damage == 6:
            self.AddField('knockback_damage', knockback_damage)
        if not knockback_filters is None:
            self.AddField('knockback_filters', knockback_filters)
        if not knockback_height_cap == 0.4:
            self.AddField('knockback_height_cap', knockback_height_cap)
        if not knockback_horizontal_strength == 4:
            self.AddField('knockback_horizontal_strength', knockback_horizontal_strength)
        if not knockback_range == 4:
            self.AddField('knockback_range', knockback_range)
        if not knockback_vertical_strength == 4:
            self.AddField('knockback_vertical_strength', knockback_vertical_strength)

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self
    
    def on_roar_end(self, on_roar_end: event):
        self.AddField('on_roar_end', {'event': on_roar_end})
        return self


class MobEffect(_component):
    def __init__(self,
                 mob_effect: Effects,
                 entity_filter: Filter,
                 cooldown_time: int = 0,
                 effect_range: float = 0.2,
                 effect_time: int = 10) -> None:
        """Applies a mob effect to entities that get within range."""
        super().__init__('mob_effect')
        self.AddField('mob_effect', mob_effect)
        self.AddField('entity_filter', entity_filter)
        
        if not cooldown_time == 0:
            self.AddField('cooldown_time', cooldown_time)
        if not effect_range == 0.2:
            self.AddField('effect_range', effect_range)
        if not effect_time == 10:
            self.AddField('effect_time', effect_time)


class SpawnEntity(_component):
    def __init__(self) -> None:
        """Adds a timer after which this entity will spawn another entity or item (similar to vanilla's chicken's egg-laying behavior)."""
        super().__init__('spawn_entity')
        self.AddField('entities', [])

    def _template(self, 
                     identifier: str,
                     spawn_type: str = 'spawn_entity',
                     spawn_event: str = 'minecraft:entity_born',
                     spawn_method: str = 'born',
                     spawn_sound: str = 'plop',
                     filters: Filter = None, 
                     max_wait_time: int = 600, 
                     min_wait_time: int = 300, 
                     num_to_spawn: int = 1, 
                     should_leash: bool = False,
                     single_use: bool = False):
        
        self[self._component_namespace]['entities'].append({
            spawn_type: identifier,
            'spawn_event': spawn_event if spawn_event != 'minecraft:entity_born' else {},
            'spawn_method': spawn_method if spawn_method != 'born' else {},
            'spawn_sound': spawn_sound if spawn_sound != 'plop' else {},
            'filters': filters if not filters is None else {},
            'max_wait_time': max_wait_time if max_wait_time != 600 else {},
            'min_wait_time': min_wait_time if min_wait_time != 300 else {},
            'num_to_spawn': num_to_spawn if num_to_spawn != 1 else {},
            'should_leash': should_leash if should_leash else {},
            'single_use': single_use if single_use else {},
        })
        return self
    
    def spawn_entity(self,
                     identifier: str,
                     spawn_event: str = 'minecraft:entity_born',
                     spawn_method: str = 'born',
                     spawn_sound: str = 'plop',
                     filters: Filter = None, 
                     max_wait_time: int = 600, 
                     min_wait_time: int = 300, 
                     num_to_spawn: int = 1, 
                     should_leash: bool = False,
                     single_use: bool = False):
        return self._template(
            identifier, 
            'spawn_entity', 
            spawn_event, 
            spawn_method, 
            spawn_sound, 
            filters, 
            max_wait_time, 
            min_wait_time, 
            num_to_spawn, 
            should_leash, 
            single_use)

    def spawn_item(self,
                     identifier: str,
                     spawn_event: str = 'minecraft:entity_born',
                     spawn_method: str = 'born',
                     spawn_sound: str = 'plop',
                     filters: Filter = None, 
                     max_wait_time: int = 600, 
                     min_wait_time: int = 300, 
                     num_to_spawn: int = 1, 
                     should_leash: bool = False,
                     single_use: bool = False):
        return self._template(
            identifier, 
            'spawn_item', 
            spawn_event, 
            spawn_method, 
            spawn_sound, 
            filters, 
            max_wait_time, 
            min_wait_time, 
            num_to_spawn, 
            should_leash, 
            single_use)


class Loot(_component):
    def __init__(self, path) -> None:
        """Sets the loot table for what items this entity drops upon death."""
        super().__init__('loot')
        self.AddField('table', MakePath('loot_tables', path + '.loot_table.json'))


class Float(_component):
    def __init__(self,
                 sink_with_passengers: bool = False) -> None:
        """Allows an entity to float on water. Passengers will be kicked out the moment the mob's head goes underwater, which may not happen for tall mobs."""
        super().__init__('behavior.float')
        if sink_with_passengers:
            self.AddField('sink_with_passengers', sink_with_passengers)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class RandomStroll(_component):
    def __init__(self,
                 interval: int = 120,
                 speed_multiplier: float = 1.0,
                 xz_dist: int = 10,
                 y_dist: int = 7) -> None:
        """Compels an entity to choose a random direction to walk towards."""
        super().__init__('behavior.random_stroll')
        if interval != 120:
            self.AddField('interval', interval)
        if speed_multiplier != 1.0:
            self.AddField('speed_multiplier', speed_multiplier)
        if xz_dist != 10:
            self.AddField('xz_dist', xz_dist)
        if y_dist != 7:
            self.AddField('y_dist', y_dist)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class LookAtPlayer(_component):
    def __init__(self,
                 angle_of_view_horizontal: int = 360,
                 angle_of_view_vertical: int = 360,
                 look_distance: float = 8.0,
                 look_time: tuple[int, int] = (2, 4),
                 probability: float = 0.02,
                 target_distance: float = 0.6) -> None:
        """Compels an entity to look at the player by rotating the head bone pose within a set limit."""
        super().__init__('behavior.look_at_player')
        if angle_of_view_horizontal != 360:
            self.AddField('angle_of_view_horizontal', angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self.AddField('angle_of_view_vertical', angle_of_view_vertical)
        if look_distance != 8.0:
            self.AddField('look_distance', look_distance)
        if look_time != (2, 4):
            self.AddField('look_time', look_time)
        if probability != 0.02:
            self.AddField('probability', probability)
        if target_distance != 0.6:
            self.AddField('target_distance', target_distance)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class RandomLookAround(_component):
    def __init__(self,
                 angle_of_view_horizontal: int = 360,
                 angle_of_view_vertical: int = 360,
                 look_distance: float = 8.0,
                 look_time: tuple[int, int] = (2, 4),
                 probability: float = 0.02,
                 target_distance: float = 0.6) -> None:
        """Compels an entity to choose a random direction to look in for a random duration within a range."""
        super().__init__('behavior.random_look_around')
        if angle_of_view_horizontal != 360:
            self.AddField('angle_of_view_horizontal', angle_of_view_horizontal)
        if angle_of_view_vertical != 360:
            self.AddField('angle_of_view_vertical', angle_of_view_vertical)
        if look_distance != 8.0:
            self.AddField('look_distance', look_distance)
        if look_time != (2, 4):
            self.AddField('look_time', look_time)
        if probability != 0.02:
            self.AddField('probability', probability)
        if target_distance != 0.6:
            self.AddField('target_distance', target_distance)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class HurtByTarget(_component):
    def __init__(self,
                 alert_same_type: bool = False,
                 entity_types: Filter = None,
                 max_dist: int = 16,
                 must_see: bool = False,
                 must_see_forget_duration: float = 3.0,
                 reevaluate_description: bool = False,
                 sprint_speed_multiplier: float = 1.0,
                 walk_speed_multiplier: float = 1.0,
                 hurt_owner: bool = False
                 ) -> None:
        """Compels an entity to react when hit by set target."""
        super().__init__('behavior.hurt_by_target')

        if alert_same_type:
            self.AddField('alert_same_type', alert_same_type)
        if entity_types != None:
            self.AddField('entity_types', {"filters": entity_types})
        if max_dist != 16:
            self.AddField('max_dist', max_dist)
        if must_see:
            self.AddField('must_see', must_see)
        if must_see_forget_duration != 3.0:
            self.AddField('must_see_forget_duration', must_see_forget_duration)
        if reevaluate_description:
            self.AddField('reevaluate_description', reevaluate_description)
        if sprint_speed_multiplier != 1.0:
            self.AddField('sprint_speed_multiplier', sprint_speed_multiplier)
        if walk_speed_multiplier != 1.0:
            self.AddField('walk_speed_multiplier', walk_speed_multiplier)
        if hurt_owner:
            self.AddField('hurt_owner', hurt_owner)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class MeleeAttack(_component):
    def __init__(self,
                 attack_once : bool = False,
                 cooldown_time : int = 1,
                 inner_boundary_time_increase : float = 0.25,
                 max_path_time : float = 0.55,
                 melee_fov : int = 90,
                 min_path_time : float = 0.2,
                 outer_boundary_time_increase : float = 0.5,
                 path_fail_time_increase : float = 0.75,
                 path_inner_boundary : int = 16,
                 path_outer_boundary : int = 32,
                 random_stop_interval : int = 0,
                 reach_multiplier : int = 2,
                 require_complete_path : bool = False,
                 set_persistent : bool = False,
                 speed_multiplier : float = 1,
                 track_target : bool = False,
                 x_max_rotation : int = 30,
                 y_max_head_rotation : int = 30) -> None:
        """Compels entities to make close combat melee attacks."""
        super().__init__('behavior.melee_attack')
        if attack_once:
            self.AddField('attack_once', attack_once)
        if cooldown_time != 1:
            self.AddField('cooldown_time', cooldown_time)
        if inner_boundary_time_increase != 0.75:
            self.AddField('inner_boundary_time_increase', inner_boundary_time_increase)
        if max_path_time != 0.75:
            self.AddField('max_path_time', max_path_time)
        if melee_fov != 90:
            self.AddField('melee_fov', melee_fov)
        if min_path_time != 0.2:
            self.AddField('min_path_time', min_path_time)
        if outer_boundary_time_increase != 0.5:
            self.AddField('outer_boundary_time_increase', outer_boundary_time_increase)
        if path_fail_time_increase != 0.75:
            self.AddField('path_fail_time_increase', path_fail_time_increase)
        if path_inner_boundary != 16:
            self.AddField('path_inner_boundary', path_inner_boundary)
        if path_outer_boundary != 32:
            self.AddField('path_outer_boundary', path_outer_boundary)
        if random_stop_interval != 0:
            self.AddField('random_stop_interval', random_stop_interval)
        if reach_multiplier != 2:
            self.AddField('reach_multiplier', reach_multiplier)
        if require_complete_path:
            self.AddField('require_complete_path', require_complete_path)
        if set_persistent:
            self.AddField('set_persistent', set_persistent)
        if speed_multiplier != 1:
            self.AddField('speed_multiplier', speed_multiplier)
        if track_target:
            self.AddField('track_target', track_target)
        if x_max_rotation != 30:
            self.AddField('x_max_rotation', x_max_rotation)
        if y_max_head_rotation != 30:
            self.AddField('y_max_head_rotation', y_max_head_rotation)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self

    def attack_types(self, attack_types : str):
        self.AddField('attack_types', attack_types)
        return self

    def on_attack(self, on_attack : event):
        self.AddField('on_attack', on_attack)
        return self

    def on_kill(self, on_kill : event):
        self.AddField('on_kill', on_kill)
        return self


class RangedAttack(_component):
    def __init__(self,
                 attack_interval : int = 0,
                 attack_interval_max : int = 0,
                 attack_interval_min : int = 0,
                 attack_radius : int = 0,
                 attack_radius_min : int = 0,
                 burst_interval : int = 0,
                 burst_shots : int = 1,
                 charge_charged_trigger : int = 0,
                 charge_shoot_trigger : int = 0,
                 ranged_fov : int = 90,
                 set_persistent : bool = False,
                 speed_multiplier : int = 1,
                 swing : bool = False,
                 target_in_sight_time : int = 1,
                 x_max_rotation : int = 30,
                 y_max_head_rotation : int = 30) -> None:
        """Allows an entity to attack by using ranged shots. charge_shoot_trigger must be greater than 0 to enable charged up burst-shot attacks. Requires minecraft:shooter to define projectile behavior."""
        super().__init__('behavior.ranged_attack')

        if attack_interval != 0:
            self.AddField('attack_interval', attack_interval)
        if attack_interval_max != 0:
            self.AddField('attack_interval_max', attack_interval_max)
        if attack_interval_min != 0:
            self.AddField('attack_interval_min', attack_interval_min)
        if attack_radius != 0:
            self.AddField('attack_radius', attack_radius)
        if attack_radius_min != 0:
            self.AddField('attack_radius_min', attack_radius_min)
        if burst_interval != 0:
            self.AddField('burst_interval', burst_interval)
        if burst_shots != 1:
            self.AddField('burst_shots', burst_shots)
        if charge_charged_trigger != 0:
            self.AddField('charge_charged_trigger', charge_charged_trigger)
        if charge_shoot_trigger != 0:
            self.AddField('charge_shoot_trigger', charge_shoot_trigger)
        if ranged_fov != 90:
            self.AddField('ranged_fov', ranged_fov)
        if set_persistent:
            self.AddField('set_persistent', set_persistent)
        if speed_multiplier != 1:
            self.AddField('speed_multiplier', speed_multiplier)
        if swing:
            self.AddField('swing', swing)
        if target_in_sight_time != 1:
            self.AddField('target_in_sight_time', target_in_sight_time)
        if x_max_rotation != 30:
            self.AddField('x_max_rotation', x_max_rotation)
        if y_max_head_rotation != 30:
            self.AddField('y_max_head_rotation', y_max_head_rotation)

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self


class Shooter(_component):
    def __init__(self, 
                 identifier: Identifier, 
                 magic: bool = False,
                 power: float = 0.0,
                 aux_value: int = -1
                ) -> None:
        """Defines the entity's ranged attack behavior. The "minecraft:behavior.ranged_attack" goal uses this component to determine which projectiles to shoot."""
        super().__init__('shooter')
        self.AddField('def', identifier)
        if magic:
            self.AddField('magic', magic)
        if power != 0:
            self.AddField('power', power)
        if aux_value != -1:
            self.AddField('aux_value', aux_value)


class SummonEntity(_component):
    def __init__(self) -> None:
        """compels an entity to attack other entities by summoning new entities."""
        super().__init__('behavior.summon_entity')
        self.AddField('summon_choices', [])

    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self
    
    def summon_choice(self, 
                      cast_duration : int, 
                      cooldown_time : int = 0,
                      do_casting: bool = True,
                      filters: Filter = None,
                      max_activation_range: float = 32.0,
                      min_activation_range : float = 1,
                      particle_color : int = 0,
                      start_sound_event: str = None,
                      weight: int = 1):
        self[self._component_namespace]['summon_choices'].append({
            'cast_duration': cast_duration,
            'cooldown_time': cooldown_time if cooldown_time != 0 else {},
            'do_casting': do_casting if not do_casting else {},
            'filters': filters if not filters is None != 0 else {},
            'max_activation_range': max_activation_range if max_activation_range != 32 else {},
            'min_activation_range': min_activation_range if min_activation_range != 1 else {},
            'particle_color': particle_color if particle_color != 0 else {},
            'start_sound_event': start_sound_event if not start_sound_event is None else {},
            'weight': weight if weight != 1 else {},
            'sequence': []
        })
        return self

    def sequence(self,
        entity_type: Identifier,
        base_delay: float = 0.0,
        delay_per_summon : float = 0.0,
        entity_lifespan : int = -1,
        num_entities_spawned : int = 1,
        shape : str = 'line',
        size : int = 1,
        sound_event : str = None,
        summon_cap : int = 0,
        summon_cap_radius : float = 0.0,
        target : FilterSubject = FilterSubject.Self):
        
        self[self._component_namespace]['summon_choices'][-1]['sequence'].append({
            'entity_type': entity_type,
            'base_delay': base_delay if base_delay != 0.0 else {},
            'delay_per_summon': delay_per_summon if delay_per_summon != 0.0 else {},
            'entity_lifespan': entity_lifespan if entity_lifespan != -1 else {},
            'num_entities_spawned': num_entities_spawned if num_entities_spawned != 1 else {},
            'shape': shape if shape != 'line' else {},
            'size': size if size != 1 else {},
            'sound_event': sound_event if not sound_event is None else {},
            'summon_cap': summon_cap if summon_cap != 0 else {},
            'summon_cap_radius': summon_cap_radius if summon_cap_radius != 0 else {},
            'target': target if target != FilterSubject.Self else {},
        })
        return self


class Boss(_component):
    def __init__(self, 
                 name : str,
                 hud_range : int = 55, 
                 should_darken_sky: bool = False) -> None:
        """Defines the current state of the boss for updating the boss HUD."""
        super().__init__('boss')
        self.AddField('name', name)
        if hud_range != 55:
            self.AddField('power', hud_range)
        if should_darken_sky:
            self.AddField('should_darken_sky', should_darken_sky)


class DelayedAttack(_component):
    def __init__(self,
                 attack_duration: float = 0.75,
                 attack_once : bool = False,
                 cooldown_time : int = 1,
                 hit_delay_pct: float = 0.5,
                 inner_boundary_time_increase : float = 0.25,
                 max_path_time : float = 0.55,
                 melee_fov : int = 90,
                 min_path_time : float = 0.2,
                 outer_boundary_time_increase : float = 0.5,
                 path_fail_time_increase : float = 0.75,
                 path_inner_boundary : int = 16,
                 path_outer_boundary : int = 32,
                 random_stop_interval : int = 0,
                 reach_multiplier : int = 2,
                 require_complete_path : bool = False,
                 set_persistent : bool = False,
                 speed_multiplier : float = 1,
                 track_target : bool = False,
                 x_max_rotation : int = 30,
                 y_max_head_rotation : int = 30) -> None:
        """Compels an entity to attack while also delaying the damage dealt until a specific time in the attack animation."""
        super().__init__('behavior.delayed_attack')
        if attack_duration != 0.75:
            self.AddField('attack_duration', attack_duration)
        if attack_once:
            self.AddField('attack_once', attack_once)
        if cooldown_time != 1:
            self.AddField('cooldown_time', cooldown_time)
        if hit_delay_pct != 0.5:
            self.AddField('hit_delay_pct', clamp(hit_delay_pct, 0, 1))
        if inner_boundary_time_increase != 0.75:
            self.AddField('inner_boundary_time_increase', inner_boundary_time_increase)
        if max_path_time != 0.75:
            self.AddField('max_path_time', max_path_time)
        if melee_fov != 90:
            self.AddField('melee_fov', melee_fov)
        if min_path_time != 0.2:
            self.AddField('min_path_time', min_path_time)
        if outer_boundary_time_increase != 0.5:
            self.AddField('outer_boundary_time_increase', outer_boundary_time_increase)
        if path_fail_time_increase != 0.75:
            self.AddField('path_fail_time_increase', path_fail_time_increase)
        if path_inner_boundary != 16:
            self.AddField('path_inner_boundary', path_inner_boundary)
        if path_outer_boundary != 32:
            self.AddField('path_outer_boundary', path_outer_boundary)
        if random_stop_interval != 0:
            self.AddField('random_stop_interval', random_stop_interval)
        if reach_multiplier != 2:
            self.AddField('reach_multiplier', reach_multiplier)
        if require_complete_path:
            self.AddField('require_complete_path', require_complete_path)
        if set_persistent:
            self.AddField('set_persistent', set_persistent)
        if speed_multiplier != 1:
            self.AddField('speed_multiplier', speed_multiplier)
        if track_target:
            self.AddField('track_target', track_target)
        if x_max_rotation != 30:
            self.AddField('x_max_rotation', x_max_rotation)
        if y_max_head_rotation != 30:
            self.AddField('y_max_head_rotation', y_max_head_rotation)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self

    def attack_types(self, attack_types : str):
        self.AddField('attack_types', attack_types)
        return self

    def on_attack(self, on_attack : event):
        self.AddField('on_attack', on_attack)
        return self

    def on_kill(self, on_kill : event):
        self.AddField('on_kill', on_kill)
        return self


class MoveToBlock(_component):
    def __init__(self,
                 target_blocks : list,
                 goal_radius : float = 0.5,
                 search_height : int = 1,
                 search_range : int = 0,
                 speed_multiplier : float = 1.0,
                 start_chance : float = 1.0,
                 stay_duration : float = 0.0,
                 target_offset : tuple[float, float, float] = (0, 0, 0),
                 target_selection_method : str = 'nearest',
                 tick_interval : int = 20) -> None:
        """Compels a mob to move towards a block."""
        super().__init__('behavior.move_to_block')
        self.AddField('target_blocks', target_blocks)
        if goal_radius != 0.5:
            self.AddField('goal_radius', goal_radius)
        if search_height != 1:
            self.AddField('search_height', search_height)
        if search_range != 0:
            self.AddField('search_range', search_range)
        if speed_multiplier != 1.0:
            self.AddField('speed_multiplier', speed_multiplier)
        if start_chance != 1.0:
            self.AddField('start_chance', start_chance)
        if stay_duration != 0.0:
            self.AddField('stay_duration', stay_duration)
        if target_offset != (0, 0, 0):
            self.AddField('target_offset', target_offset)
        if target_selection_method != 'nearest':
            self.AddField('target_selection_method', target_selection_method)
        if tick_interval != 20:
            self.AddField('tick_interval', tick_interval)
            
    def priority(self, priority : int):
        self.AddField('priority', priority)
        return self

    def on_reach(self, event: event, target: FilterSubject = FilterSubject.Self):
        self.AddField('on_reach', {'event': event, 'target': target})
        return self

    def on_stay_completed(self, event: event, target: FilterSubject = FilterSubject.Self):
        self.AddField('on_stay_completed', {'event': event, 'target': target})
        return self



# Unfinished


class ConditionalBandwidthOptimization(_component):
    def __init__(self) -> None:
        """Defines the Conditional Spatial Update Bandwidth Optimizations of this entity."""
        super().__init__('conditional_bandwidth_optimization')
