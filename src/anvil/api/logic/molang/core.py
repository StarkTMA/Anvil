from enum import StrEnum

import orjson

__all__ = ["Molang"]


def _math():
    """The Math class, imported on first use since it subclasses Molang."""
    from anvil.api.logic.molang.math import Math

    return Math


class Molang(str):
    __hash__ = str.__hash__

    prefixes = (
        "q.",
        "v.",
        "c.",
        "t.",
        "query.",
        "variable.",
        "context.",
        "temp.",
        "math.",
    )

    this: "Molang"
    break_: "Molang"
    continue_: "Molang"

    @staticmethod
    def arrow(left: "Molang", right: "Molang") -> "Molang":
        """Returns a Molang object representing the arrow operator for Molang."""
        return Molang(f"(({left}) -> ({right}))")

    @staticmethod
    def condition(
        condition: "Molang",
        expression: "Molang",
        expression2: "Molang" | None = None,
    ) -> "Molang":
        """Returns a Molang object representing a conditional expression for Molang."""
        if expression2 is not None:
            return Molang(f"({condition} ? {expression} : {expression2})")
        else:
            return Molang(f"({condition} ? {expression})")

    @staticmethod
    def molang_return(molang: "Molang") -> "Molang":
        return Molang(f"return {molang}")

    @staticmethod
    def molang_block(statements: list["Molang"]) -> "Molang":
        body = "; ".join(str(s) for s in statements)
        return Molang(f"{{ {body}; }}")

    @staticmethod
    def molang_loop(n: int, statements: list["Molang"]) -> "Molang":
        return Molang(f"loop({n}, {Molang.molang_block(statements)})")

    @staticmethod
    def molang_for_each(
        variable: "Molang", array: "Molang", statements: list["Molang"]
    ) -> "Molang":
        return Molang(
            f"for_each({variable}, {array}, {Molang.molang_block(statements)})"
        )

    def __getitem__(self, molang: "Molang") -> "Molang":
        return Molang(f"{self}[{molang}]")

    def __parse_other__(self, other):
        if isinstance(other, (str, StrEnum)) and not isinstance(other, Molang):
            o = f"'{other}'"
        elif isinstance(other, bool):
            o = orjson.dumps(other).decode("utf-8")
        else:
            o = f"{other}"
        return o

    def __invert__(self) -> "Molang":
        return Molang(f"!({self})")

    def __eq__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} == {o})")

    def __ne__(self, other) -> "Molang":
        o = self.__parse_other__(other)

        return Molang(f"({self} != {o})")

    def __lt__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} < {o})")

    def __gt__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} > {o})")

    def __le__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} <= {o})")

    def __ge__(self, other) -> "Molang":
        o = self.__parse_other__(other)
        return Molang(f"({self} >= {o})")

    def __and__(self, other) -> "Molang":
        return Molang(f"({self} && {other})")

    def __or__(self, other) -> "Molang":
        return Molang(f"({self} || {other})")

    def __add__(self, other) -> "Molang":
        return Molang(f"({self} + {other})")

    def __sub__(self, other) -> "Molang":
        return Molang(f"({self} - {other})")

    def __mul__(self, other) -> "Molang":
        return Molang(f"({self} * {other})")

    def __neg__(self) -> "Molang":
        return Molang(f"-{self}")

    def __truediv__(self, other) -> "Molang":
        return Molang(f"({self} / {other})")

    def __floordiv__(self, other) -> "Molang":
        return _math().floor(self / other)

    def __mod__(self, other) -> "Molang":
        return _math().mod(self, other)

    def __pow__(self, other) -> "Molang":
        return _math().pow(self, other)

    def __radd__(self, other) -> "Molang":
        return Molang(f"({other} + {self})")

    def __rsub__(self, other) -> "Molang":
        return Molang(f"({other} - {self})")

    def __rmul__(self, other) -> "Molang":
        return Molang(f"({other} * {self})")

    def __rtruediv__(self, other) -> "Molang":
        return Molang(f"({other} / {self})")

    def __rfloordiv__(self, other) -> "Molang":
        return _math().floor(other / self)

    def __rmod__(self, other) -> "Molang":
        return _math().mod(other, self)

    def __rpow__(self, other) -> "Molang":
        return _math().pow(other, self)

    def __abs__(self) -> "Molang":
        return _math().abs(self)

    def __round__(self) -> "Molang":
        return _math().round(self)

    def __xor__(self, other) -> "Molang":
        return Molang(f"({self} ?? {other})")

    def __pos__(self) -> "Molang":
        return self

    def __rand__(self, other) -> "Molang":
        return Molang(f"({other} && {self})")

    def __ror__(self, other) -> "Molang":
        return Molang(f"({other} || {self})")

    def __rxor__(self, other) -> "Molang":
        return Molang(f"({other} ?? {self})")

    @staticmethod
    def __power_of_two__(shift):
        return 2 ** shift if isinstance(shift, int) else _math().pow(2, shift)

    def __lshift__(self, other) -> "Molang":
        return self * Molang.__power_of_two__(other)

    def __rshift__(self, other) -> "Molang":
        return self // Molang.__power_of_two__(other)

    def __rlshift__(self, other) -> "Molang":
        return other * Molang.__power_of_two__(self)

    def __rrshift__(self, other) -> "Molang":
        return _math().floor(other / Molang.__power_of_two__(self))

    def __struct__(self, *Parameters) -> "Molang":
        return Molang(f"{self}.{'.'.join(Parameters)}")

    def __query__(self, qtype, query, *arguments) -> "Molang":
        a = f"{qtype}.{query}"
        if len(arguments):
            Parameters = ", ".join(
                (
                    f"'{arg}'"
                    if isinstance(arg, (str, StrEnum))
                    and not isinstance(arg, Molang)
                    and not any(arg.startswith(v) for v in Molang.prefixes)
                    else f"{arg}"
                )
                for arg in arguments
                if arg is not None
            )
            a += f"({Parameters})"
        return Molang(a)


Molang.this = Molang("this")
Molang.break_ = Molang("break")
Molang.continue_ = Molang("continue")
