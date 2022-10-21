from ..packages import *

#__all__ = [
#    'AddRider', 'AdmireItem', 'Ageable',
#    'Variant', 'MarkVariant', 'SkinID', 'CollisionBox', 'IsStackable', 'TypeFamily',
#    'InstantDespawn', 'Health', 'Physics', 'KnockbackResistance', 'Pushable', 'IsIllagerCaptain',
#    'IsBaby', 'PushThrough', 'Movement', 'TickWorld'
#]

Component = NewType('Component',str)
Identifier = NewType('Identifier',str)
Seconds = NewType('Seconds',str)
Event = NewType('Event',str)

class Target():
    Block = 'block'
    Damager = 'damager'
    Other = 'other'
    Parent = 'parent'
    Player = 'player'
    Self = 'self'
    Target = 'target'
    
class EventObject():
    def __init__(self, event: Event, target : Target) -> None:
        return {
            'event': event,
            'target': target
        }

# Components
class _component(dict):
    def __init__(self, component_name) -> None:
        self._component_name = component_name
        self._component_namespace = f'minecraft:{self._component_name}'
        self.__setitem__(self._component_namespace, {})
    
    def AddField(self, key,value):
        self[self._component_namespace][key] = value

class AddRider(_component):
    def __init__(self, entity_type: Identifier, spawn_event: Event = None) -> None:
        '''Adds a rider to the entity. Requires `minecraft:rideable.`.
        
        Parameters
        ----------
        `entity_type` : `Identifier` `str`.
            The entity type that will be riding this entity
        `spawn_event` : `Event` `str`, `optional`.
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
        self.AddField('cooldown_after_being_attacked', cooldown_after_being_attacked)
        if not duration == 10:
            self.AddField('duration', duration)

class Ageable(_component):

    @overload
    def __init__(self, duration: Seconds, event: Event) -> None:
        '''Adds a timer for the entity to grow up. It can be accelerated by giving the entity the items it likes.
        
        Parameters
        ----------
        `duration` : `Seconds` `int`.
            Amount of time before the entity grows up, -1 for always a baby. `Default: 1200`
        `event` : `Event` `str`.
            Minecraft behavior event.

        '''
        super().__init__('ageable')
        self.AddField('duration', duration)
        self.AddField('event', event)

    @overload
    def __init__(self, duration: Seconds, event: EventObject) -> None:
        '''Adds a timer for the entity to grow up. It can be accelerated by giving the entity the items it likes.
        
        Parameters
        ----------
        `duration` : `Seconds` `int`.
            Amount of time before the entity grows up, -1 for always a baby. `Default: 1200`
        `event` : `Event` `str`.
            Minecraft behavior event object.

        '''
        super().__init__('ageable')
        self.AddField('duration', duration)
        self.AddField('event', event)

class Variant(_component):
    def __init__(self, value: int) -> None:
        """Used to differentiate the component group of a variant of an entity from others. (e.g. ocelot, villager)."""
        super().__init__('variant')
        self.AddField('value', value)

class MarkVariant(_component):
    def __init__(self, value: int) -> None:
        """Additional variant value. Can be used to further differentiate variants."""
        super().__init__('skin_id')
        self.AddField('value', value)

class SkinID(_component):
    def __init__(self, value: int) -> None:
        """Skin ID value. Can be used to differentiate skins, such as base skins for villagers."""
        super().__init__('skin_id')
        self.AddField('value', value)

class CollisionBox(_component):
    def __init__(self, height: float, width: float) -> None:
        """Sets the width and height of the Entity's collision box."""
        super().__init__('collision_box')
        self.AddField('height', height)
        self.AddField('width', width)

class IsStackable(_component):
    def __init__(self) -> None:
        """Sets that this entity can be stacked."""
        super().__init__('is_stackable')

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
        self.AddField('value', max(0,min(1,value)))

class Pushable(_component):
    def __init__(self, is_pushable: bool = True, is_pushable_by_piston: bool = True) -> None:
        """Defines what can push an entity between other entities and pistons."""
        super().__init__('pushable')
        self.AddField('is_pushable', is_pushable)
        self.AddField('is_pushable_by_piston', is_pushable_by_piston)

class IsIllagerCaptain(_component):
    def __init__(self) -> None:
        """Sets that this entity is an illager captain."""
        super().__init__('is_illager_captain')

class IsBaby(_component):
    def __init__(self) -> None:
        """Sets that this entity is a baby."""
        super().__init__('is_baby')

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
    def __init__(self, height: float, width: float, pivot : list[float,float,float] = [0,1,0]) -> None:
        """List of hitboxes for melee and ranged hits against the entity."""
        super().__init__('custom_hit_test')
        self.AddField('hitboxes', [{
            "width": width,
            "height": height,
            "pivot": pivot
        }])
    
    def add_hitbox(self, height: float, width: float, pivot : list[float,float,float] = [0,1,0]):
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
    def __init__(self, damage: int, effect_duration: str = None, effect_name: str = None) -> None:
        """Defines an entity's melee attack and any additional effects on it."""
        super().__init__('attack')
        self.AddField('damage', damage)
        if not effect_duration is None:
            self.AddField('effect_duration', effect_duration)
        if not effect_name is None:
            self.AddField('effect_name', effect_name)

class IsIgnited(_component):
    def __init__(self) -> None:
        """Sets that this entity is currently on fire."""
        super().__init__('is_ignited')

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

