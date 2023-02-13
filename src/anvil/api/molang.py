from ..packages import *
from ..core import NAMESPACE

class _molang(str):
    def __eq__(self, other):
        return _molang(f'{self} == {other}')
    def __ne__(self, other):
        return _molang(f'{self} != {other}')
    def __lt__(self, other):
        return _molang(f'{self} < {other}')
    def __gt__(self, other):
        return _molang(f'{self} > {other}')
    def __le__(self, other):
        return _molang(f'{self} <= {other}')
    def __ge__(self, other):
        return _molang(f'{self} >= {other}')
    def __and__(self, other):
        return _molang(f'{self} && {other}')
    def __or__(self, other):
        return _molang(f'{self} || {other}')
    def __invert__(self):
        return _molang(f'!{self}')
    
    def _query(self, qtype, query, *arguments):
        a = f'{qtype}.{query}'
        if len(arguments):
            args = ', '.join(f"'{arg}'" if type(arg) is str and not arg.startswith(MOLANG_PREFIXES) else f"{arg}" for arg in arguments)
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
    @property
    def BodyYRotation(self):
        return self._query(self, 'q', 'body_y_rotation')

    @classmethod
    @property
    def BodyXRotation(self):
        return self._query(self, 'q', 'body_x_rotation')

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

class Variable(_molang):
    def __init__(self) -> None:
        super().__init__('v')

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

q = Query
v = Variable