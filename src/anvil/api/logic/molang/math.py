from anvil.api.logic.molang._helpers import _in_range
from anvil.api.logic.molang.core import Molang

__all__ = ["Math"]


class Math(Molang):
    handle = "math"

    @classmethod
    def abs(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "abs", value)

    @classmethod
    def acos(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "acos", value)

    @classmethod
    def asin(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "asin", value)

    @classmethod
    def atan(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "atan", value)

    @classmethod
    def atan2(cls, y: str, x) -> Molang:
        return cls.__query__(cls, cls.handle, "atan2", y, x)

    @classmethod
    def ceil(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "ceil", value)

    @classmethod
    def clamp(cls, value, min, max) -> Molang:
        return cls.__query__(cls, cls.handle, "clamp", value, min, max)

    @classmethod
    def copy_sign(cls, value, sign) -> Molang:
        return cls.__query__(cls, cls.handle, "copy_sign", value, sign)

    @classmethod
    def cos(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "cos", value)

    @classmethod
    def die_roll(cls, num, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "die_roll", num, low, high)

    @classmethod
    def die_roll_integer(cls, num, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "die_roll_integer", num, low, high)

    @classmethod
    def exp(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "exp", value)

    @classmethod
    def floor(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "floor", value)

    @classmethod
    def hermite_blend(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "hermite_blend", value)

    @classmethod
    def lerp(cls, start, end, factor) -> Molang:
        return cls.__query__(
            cls,
            cls.handle,
            "lerp",
            start,
            end,
            _in_range("factor", factor, 0, 1),
        )

    @classmethod
    def lerprotate(cls, start, end, factor) -> Molang:
        return cls.__query__(
            cls,
            cls.handle,
            "lerprotate",
            start,
            end,
            _in_range("factor", factor, 0, 1),
        )

    @classmethod
    def ln(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "ln", value)

    @classmethod
    def max(cls, A, B) -> Molang:
        return cls.__query__(cls, cls.handle, "max", A, B)

    @classmethod
    def min(cls, A, B) -> Molang:
        return cls.__query__(cls, cls.handle, "min", A, B)

    @classmethod
    def min_angle(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "min_angle", value)

    @classmethod
    def mod(cls, value, denominator) -> Molang:
        return cls.__query__(cls, cls.handle, "mod", value, denominator)

    @classmethod
    def pi(cls) -> Molang:
        return cls.__query__(cls, cls.handle, "pi")

    @classmethod
    def pow(cls, base, exponent) -> Molang:
        return cls.__query__(cls, cls.handle, "pow", base, exponent)

    @classmethod
    def random(cls, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "random", low, high)

    @classmethod
    def random_integer(cls, low, high) -> Molang:
        return cls.__query__(cls, cls.handle, "random_integer", low, high)

    @classmethod
    def round(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "round", value)

    @classmethod
    def sign(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "sign", value)

    @classmethod
    def sin(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "sin", value)

    @classmethod
    def sqrt(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "sqrt", value)

    @classmethod
    def trunc(cls, value) -> Molang:
        return cls.__query__(cls, cls.handle, "trunc", value)

    @classmethod
    def inverse_lerp(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "inverse_lerp", start, end, factor)

    @classmethod
    def ease_in_quad(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_quad", start, end, factor)

    @classmethod
    def ease_out_quad(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_quad", start, end, factor)

    @classmethod
    def ease_in_out_quad(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_quad", start, end, factor)

    @classmethod
    def ease_in_cubic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_cubic", start, end, factor)

    @classmethod
    def ease_out_cubic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_cubic", start, end, factor)

    @classmethod
    def ease_in_out_cubic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_cubic", start, end, factor)

    @classmethod
    def ease_in_quart(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_quart", start, end, factor)

    @classmethod
    def ease_out_quart(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_quart", start, end, factor)

    @classmethod
    def ease_in_out_quart(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_quart", start, end, factor)

    @classmethod
    def ease_in_quint(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_quint", start, end, factor)

    @classmethod
    def ease_out_quint(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_quint", start, end, factor)

    @classmethod
    def ease_in_out_quint(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_quint", start, end, factor)

    @classmethod
    def ease_in_sine(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_sine", start, end, factor)

    @classmethod
    def ease_out_sine(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_sine", start, end, factor)

    @classmethod
    def ease_in_out_sine(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_sine", start, end, factor)

    @classmethod
    def ease_in_expo(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_expo", start, end, factor)

    @classmethod
    def ease_out_expo(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_expo", start, end, factor)

    @classmethod
    def ease_in_out_expo(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_expo", start, end, factor)

    @classmethod
    def ease_in_circ(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_circ", start, end, factor)

    @classmethod
    def ease_out_circ(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_circ", start, end, factor)

    @classmethod
    def ease_in_out_circ(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_circ", start, end, factor)

    @classmethod
    def ease_in_bounce(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_bounce", start, end, factor)

    @classmethod
    def ease_out_bounce(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_bounce", start, end, factor)

    @classmethod
    def ease_in_out_bounce(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_bounce", start, end, factor)

    @classmethod
    def ease_in_back(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_back", start, end, factor)

    @classmethod
    def ease_out_back(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_back", start, end, factor)

    @classmethod
    def ease_in_out_back(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_back", start, end, factor)

    @classmethod
    def ease_in_elastic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_elastic", start, end, factor)

    @classmethod
    def ease_out_elastic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_out_elastic", start, end, factor)

    @classmethod
    def ease_in_out_elastic(cls, start, end, factor) -> Molang:
        return cls.__query__(cls, cls.handle, "ease_in_out_elastic", start, end, factor)
