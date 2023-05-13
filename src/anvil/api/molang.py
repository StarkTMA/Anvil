from ..core import NAMESPACE
from ..packages import *


class _molang(str):
    def __invert__(self):
        return _molang(f"!({self})")
    
    def __eq__(self, other):
        o = f"'{other}'" if type(other) is str else f"{other}"
        return _molang(f"{self} == {o}")

    def __ne__(self, other):
        o = f"'{other}'" if type(other) is str else f"{other}"
        return _molang(f"{self} != {o}")

    def __lt__(self, other):
        return _molang(f"{self} < {other}")

    def __gt__(self, other):
        return _molang(f"{self} > {other}")

    def __le__(self, other):
        return _molang(f"{self} <= {other}")

    def __ge__(self, other):
        return _molang(f"{self} >= {other}")

    def __and__(self, other):
        return _molang(f"({self} && {other})")

    def __or__(self, other):
        return _molang(f"({self} || {other})")
    
    def __add__(self, other):
        return _molang(f"({self} + {other})")
    
    def __sub__(self, other):
        return _molang(f"({self} - {other})")
    
    def __mul__(self, other):
        return _molang(f"({self} * {other})")
    
    def __neg__(self):
        return _molang(f"-{self}")
    
    def __truediv__ (self, other):
        return _molang(f"({self} / {other})")
    
    def __floordiv__ (self, other):
        return Math.floor(f"({self} / {other})")
    
    def __mod__ (self, other):
        return Math.mod(self, other)
    
    def __pow__(self, other):
        return Math.pow(self, other)
    
    def __radd__(self, other):
        return _molang(f"({other} + {self})")
    
    def __rsub__(self, other):
        return _molang(f"({other} - {self})")
    
    def __rmul__(self, other):
        return _molang(f"({other} * {self})")
    
    def __rtruediv__(self, other):
        return _molang(f"({other} / {self})")
    
    def __rfloordiv__(self, other):
        return Math.floor(f"({other} / {self})")
    
    def __rmod__(self, other):
        return Math.mod(other, self)
    
    def __rpow__(self, other):
        return Math.pow(other, self)

    def __abs__(self):
        return Math.abs(self)
    
    def __round__(self):
        return Math.round(self)

    def _query(self, qtype, query, *arguments):
        a = f'{qtype}.{query}'
        if len(arguments):
            args = ', '.join(f"'{arg}'" if type(arg) is str and not arg.startswith(
                MOLANG_PREFIXES) else f"{arg}" for arg in arguments)
            a += f"({args})"
        return _molang(a)


class Query(_molang):
    
    @classmethod
    @property
    def IsIllagerCaptain(self):
        return self._query(self, 'q', 'is_illager_captain')

    @classmethod
    @property
    def SkinId(self):
        return self._query(self, 'q', 'skin_id')

    @classmethod
    @property
    def Variant(self):
        return self._query(self, 'q', 'variant')

    @classmethod
    @property
    def MarkVariant(self):
        return self._query(self, 'q', 'mark_variant')

    @classmethod
    @property
    def IsInUI(self):
        return self._query(self, 'q', 'is_in_ui')

    @classmethod
    @property
    def HasTarget(self):
        return self._query(self, 'q', 'has_target')

    @classmethod
    @property
    def IsUsingItem(self):
        return self._query(self, 'q', 'is_using_item')

    @classmethod
    def IsItemNameAny(self, slot: Slots, index: int, *item_identifiers):
        return self._query(self, 'q', 'is_item_name_any', slot, index, *item_identifiers)

    @classmethod
    def InRange(self, value: float, min: float, max: float):
        return self._query(self, 'q', 'in_range', value, min, max)

    @classmethod
    def MovementDirection(self, axis: int):
        return self._query(self, 'q', 'movement_direction', axis)

    @classmethod
    def Property(self, property: str):
        return self._query(self, 'q', 'property', f'{NAMESPACE}:{property}')

    @classmethod
    def HasProperty(self, property: str):
        return self._query(self, 'q', 'has_property', f'{NAMESPACE}:{property}')

    @classmethod
    @property
    def BodyXRotation(self):
        return self._query(self, 'q', 'body_x_rotation')

    @classmethod
    @property
    def BodyYRotation(self):
        return self._query(self, 'q', 'body_y_rotation')

    @classmethod
    def HeadXRotation(self, head_number: int = 0):
        return self._query(self, 'q', 'head_x_rotation', head_number)

    @classmethod
    def HeadYRotation(self, head_number: int = 0):
        return self._query(self, 'q', 'head_y_rotation', head_number)

    @classmethod
    @property
    def TargetYRotation(self):
        return self._query(self, 'q', 'target_y_rotation')

    @classmethod
    @property
    def TargetXRotation(self):
        return self._query(self, 'q', 'target_x_rotation')

    @classmethod
    @property
    def IsFirstPerson(self):
        return self._query(self, 'q', 'is_first_person')

    @classmethod
    @property
    def DistanceFromCamera(self):
        return self._query(self, 'q', 'distance_from_camera')

    @classmethod
    @property
    def LifeTime(self):
        return self._query(self, 'q', 'life_time')
    
    @classmethod
    @property
    def GroundSpeed(self):
        return self._query(self, 'q', 'ground_speed')
    
    @classmethod
    @property
    def IsOnGround(self):
        return self._query(self, 'q', 'is_on_ground')
    
    @classmethod
    @property
    def IsJumping(self):
        return self._query(self, 'q', 'is_jumping')
    
    @classmethod
    @property
    def IsSneaking(self):
        return self._query(self, 'q', 'is_sneaking')

    @classmethod
    @property
    def IsLocalPlayer(self):
        return self._query(self, 'q', 'is_local_player')
    
    @classmethod
    def IsItemNameAny(self, slot: Slots, index: int = 0, *items: str):
        return self._query(self, 'q', 'is_item_name_any', slot, index, ','.join(items))
    
    @classmethod
    def BlockProperty(self, property: str):
        return self._query(self, 'q', 'block_property', f'{NAMESPACE}:{property}')

    @classmethod
    def GetEquippedItemName(self, hand_slot: int, index = 0):
        return self._query(self, 'q', 'get_equipped_item_name', clamp(hand_slot, 0, 1), index)
    
    @classmethod
    def Position(self, axis: int):
        return self._query(self, 'q', 'position', clamp(axis, 0, 2))
    
    @classmethod
    def PositionDelta(self, axis: int):
        return self._query(self, 'q', 'position_delta', clamp(axis, 0, 2))
    
    @classmethod
    @property
    def AllAnimationsFinished(self):
        return self._query(self, 'q', 'all_animations_finished')
    
    @classmethod
    @property
    def AnyAnimationFinished(self):
        return self._query(self, 'q', 'any_animation_finished')
    
    @classmethod
    @property
    def ItemIsCharged(self):
        return self._query(self, 'q', 'item_is_charged')
    
    @classmethod
    @property
    def ItemInUseDuration(self):
        return self._query(self, 'q', 'item_in_use_duration')
    
    @classmethod
    @property
    def AnimTime(self):
        return self._query(self, 'q', 'anim_time')
    
    @classmethod
    @property
    def IsRiding(self):
        return self._query(self, 'q', 'is_riding')

    @classmethod
    @property
    def ModifiedMoveSpeed(self):
        return self._query(self, 'q', 'modified_move_speed')
    
    @classmethod
    @property
    def IsDelayedAttacking(self):
        return self._query(self, 'q', 'is_delayed_attacking')
    
    @classmethod
    @property
    def IsCharged(self):
        return self._query(self, 'q', 'is_charged')
    
    @classmethod
    @property
    def IsCharging(self):
        return self._query(self, 'q', 'is_charging')
    
    @classmethod
    @property
    def IsCasting(self):
        return self._query(self, 'q', 'is_casting')

    @classmethod
    @property
    def IsRoaring(self):
        return self._query(self, 'q', 'is_roaring')

    @classmethod
    def RotationToCamera(self, axis: int):
        return self._query(self, 'q', 'rotation_to_camera', clamp(axis, 0, 1))

    @classmethod
    @property
    def Health(self):
        return self._query(self, 'q', 'health')
    
    @classmethod
    @property
    def MaxHealth(self):
        return self._query(self, 'q', 'max_health')

  
class Variable(_molang):
    def __init__(self) -> None:
        super().__init__('v')

    @classmethod
    def _set_var(self, name):
        @classmethod
        @property
        def method(self):
            return self._query(self, "v", name)
        setattr(self, name, method)
        
    @classmethod
    @property
    def IsFirstPerson(self):
        return self._query(self, 'v', 'is_first_person')

    @classmethod
    @property
    def IsPaperdoll(self):
        return self._query(self, 'v', 'is_paperdoll')


class Math(_molang):
    def __init__(self) -> None:
        super().__init__('math')

    @classmethod
    def abs(self, value):
        return self._query(self, 'math', 'abs', value)

    @classmethod
    def acos(self, value):
        return self._query(self, 'math', 'acos', value)

    @classmethod
    def asin(self, value):
        return self._query(self, 'math', 'asin', value)

    @classmethod
    def atan(self, value):
        return self._query(self, 'math', 'atan', value)

    @classmethod
    def atan2(self, y: str, x):
        return self._query(self, 'math', 'atan2', y, x)

    @classmethod
    def ceil(self, value):
        return self._query(self, 'math', 'ceil', value)

    @classmethod
    def clamp(self, value, min, max):
        return self._query(self, 'math', 'clamp', value, min, max)

    @classmethod
    def cos(self, value):
        return self._query(self, 'math', 'cos', value)

    @classmethod
    def die_roll(self, num, low, high):
        return self._query(self, 'math', 'die_roll', num, low, high)

    @classmethod
    def die_roll_integer(self, num, low, high):
        return self._query(self, 'math', 'die_roll_integer', num, low, high)

    @classmethod
    def exp(self, value):
        return self._query(self, 'math', 'exp', value)

    @classmethod
    def floor(self, value):
        return self._query(self, 'math', 'floor', value)

    @classmethod
    def hermite_blend(self, value):
        return self._query(self, 'math', 'hermite_blend', value)

    @classmethod
    def lerp(self, start, end):
        return self._query(self, 'math', 'lerp', start, end, '0_to_1')

    @classmethod
    def lerprotate(self, start, end):
        return self._query(self, 'math', 'lerprotate', start, end, '0_to_1')

    @classmethod
    def ln(self, value):
        return self._query(self, 'math', 'ln', value)

    @classmethod
    def max(self, A, B):
        return self._query(self, 'math', 'max', A, B)

    @classmethod
    def min(self, A, B):
        return self._query(self, 'math', 'min', A, B)

    @classmethod
    def min_angle(self, value):
        return self._query(self, 'math', 'min_angle', value)

    @classmethod
    def mod(self, value, denominator):
        return self._query(self, 'math', 'mod', value, denominator)

    @classmethod
    @property
    def pi(self):
        return self._query(self, 'math', 'pi')

    @classmethod
    def pow(self, base, exponent):
        return self._query(self, 'math', 'pow', base, exponent)

    @classmethod
    def random(self, low, high):
        return self._query(self, 'math', 'random', low, high)

    @classmethod
    def random_integer(self, low, high):
        return self._query(self, 'math', 'random_integer', low, high)

    @classmethod
    def round(self, value):
        return self._query(self, 'math', 'round', value)

    @classmethod
    def sin(self, value):
        return self._query(self, 'math', 'sin', value)

    @classmethod
    def sqrt(self, value):
        return self._query(self, 'math', 'sqrt', value)

    @classmethod
    def trunc(self, value):
        return self._query(self, 'math', 'trunc', value)


def molang_conditions(condition, expression, expression2):
    return f'{condition} ? {expression} : ({expression2})'
    

q = Query
v = Variable
