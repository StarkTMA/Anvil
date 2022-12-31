from ..packages import *
from ..core import NAMESPACE

class _Query():
    def __init__(self) -> None:
        self._prefix = ''

    def _query(self, query, *arguments):
        query_str = f'{self._prefix}q.{query}'
        if len(arguments):
            args = ', '.join(f"'{arg}'" if type(arg) is str else f"{arg}" for arg in arguments)
            query_str += f"({args})"
        self._prefix = ''
        return query_str

    @property
    def IsIllagerCaptain(self):
        return self._query('is_illager_captain')

    @property
    def SkinId(self):
        return self._query('skin_id')
        
    @property
    def Variant(self):
        return self._query('variant')
        
    @property
    def IsInUI(self):
        return self._query('is_in_ui')

    @property
    def HasTarget(self):
        return self._query('has_target')

    @property
    def IsUsingItem(self):
        return self._query('is_using_item')

    def IsItemNameAny(self, slot: Slots, index: int, *item_identifiers):
        return self._query('is_item_name_any', slot, index, *item_identifiers)

    def MovementDirection(self, axis: int):
        return self._query('movement_direction', axis)

    def Property(self, property: str):
        return self._query('property', f'{NAMESPACE}:{property}')

    @property
    def Not(self):
        self._prefix = '!'
        return self
    
class _Math():
    def __init__(self) -> None:
        self._prefix = ''
    def _math(self, operation, *arguments):
        math_str = f'{self._prefix}math.{operation}'
        if len(arguments):
            math_str += f"({','.join(map(str, arguments))})"
        return math_str
        
    def abs(self, value):
        return self._math ('abs', value)
    def acos(self, value):
        return self._math ('acos', value)
    def asin(self, value):
        return self._math ('asin', value)
    def atan(self, value):
        return self._math ('atan', value)
    def atan2(self, y: str, x):
        return self._math ('atan2', y, x)
    def ceil(self, value):
        return self._math ('ceil', value)
    def clamp(self, value, min, max):
        return self._math ('clamp', value, min, max)
    def cos(self, value):
        return self._math ('cos', value)
    def die_roll(self, num, low, high):
        return self._math ('die_roll', num, low, high)
    def die_roll_integer(self, num, low, high):
        return self._math ('die_roll_integer', num, low, high)
    def exp(self, value):
        return self._math ('exp', value)
    def floor(self, value):
        return self._math ('floor', value)
    def hermite_blend(self, value):
        return self._math ('hermite_blend', value)
    def lerp(self, start, end):
        return self._math ('lerp', start, end, '0_to_1')
    def lerprotate(self, start, end):
        return self._math ('lerprotate', start, end, '0_to_1')
    def ln(self, value):
        return self._math ('ln', value)
    def max(self, A, B):
        return self._math ('max', A, B)
    def min(self, A, B):
        return self._math ('min', A, B)
    def min_angle(self, value):
        return self._math ('min_angle', value)
    def mod(self, value, denominator):
        return self._math ('mod', value, denominator)
    @property
    def pi(self):
        return self._math ('pi')
    def pow(self, base, exponent):
        return self._math ('pow', base, exponent)
    def random(self, low, high):
        return self._math ('random', low, high)
    def random_integer(self, low, high):
        return self._math ('random_integer', low, high)
    def round(self, value):
        return self._math ('round', value)
    def sin(self, value):
        return self._math ('sin', value)
    def sqrt(self, value):
        return self._math ('sqrt', value)
    def trunc(self, value):
        return self._math ('trunc', value)


Query = q = _Query()
Math = _Math()