"""Every field validator Anvil uses, in one place.

A validator is any callable `(name, value) -> None` that raises `ValueError` or `TypeError`.
Validators never see `None`: an unset optional field is skipped. Pass them to `json_field`:

    speed: float = json_field(validators=[instance_of(int, float), in_range(minimum=0)])
"""

import operator
from typing import Any, get_args

from anvil.api.core.enums import DamageSensor
from anvil.api.core.types import Validator

# region Building blocks


def instance_of(*types: type) -> Validator:
    """The value must be an instance of one of `types` (bool is not accepted as a number)."""

    def check(name: str, value: Any) -> None:
        if isinstance(value, bool) and bool not in types:
            raise TypeError(f"'{name}' must be {_names(types)}, got bool.")
        if not isinstance(value, types):
            raise TypeError(
                f"'{name}' must be {_names(types)}, got {type(value).__name__}."
            )

    return check


def in_range(
    minimum: float | None = None,
    maximum: float | None = None,
    *,
    min_exclusive: bool = False,
    max_exclusive: bool = False,
) -> Validator:
    """The value must be a number within the given bounds."""
    above = operator.gt if min_exclusive else operator.ge
    below = operator.lt if max_exclusive else operator.le
    bounds = f"in {'(' if min_exclusive else '['}{minimum}, {maximum}{')' if max_exclusive else ']'}"

    def check(name: str, value: Any) -> None:
        _number(name, value)
        if (minimum is not None and not above(value, minimum)) or (
            maximum is not None and not below(value, maximum)
        ):
            raise ValueError(f"'{name}' must be {bounds}, got {value}.")

    return check


def length(minimum: int | None = None, maximum: int | None = None) -> Validator:
    """The value must be a list or tuple with a length within the given bounds."""

    def check(name: str, value: Any) -> None:
        _sequence(name, value)
        if (minimum is not None and len(value) < minimum) or (
            maximum is not None and len(value) > maximum
        ):
            raise ValueError(
                f"'{name}' must have a length in [{minimum}, {maximum}], got {len(value)}."
            )

    return check


def each(*validators: Validator) -> Validator:
    """Every item of a list or tuple must pass all `validators`."""

    def check(name: str, value: Any) -> None:
        _sequence(name, value)
        for index, item in enumerate(value):
            for validator in validators:
                validator(f"{name}[{index}]", item)

    return check


"""The validators of a list of commands."""

_number = instance_of(int, float)
_integer = instance_of(int)
_sequence = instance_of(list, tuple)

_string = instance_of(str)
_boolean = instance_of(bool)


def one_of(*allowed: Any) -> Validator:
    """The value must equal one of `allowed`."""

    def check(name: str, value: Any) -> None:
        if value not in allowed:
            raise ValueError(
                f"'{name}' must be one of {', '.join(map(repr, allowed))}, got {value!r}."
            )

    return check


def literal_of(alias: Any) -> Validator:
    """The value must be one of the values of a `Literal` alias."""
    return one_of(*get_args(alias))


def unique(attribute: str) -> Validator:
    """No two items of a list or tuple may share the same `attribute`. Items without the
    attribute, or with it unset, are skipped."""

    def check(name: str, value: Any) -> None:
        _sequence(name, value)
        seen = set()
        for item in value:
            key = getattr(item, attribute, None)
            if key is None:
                continue
            if key in seen:
                raise ValueError(
                    f"'{name}' has more than one item with {attribute} {key!r}."
                )
            seen.add(key)

    return check


def all_of(*validators: Validator) -> Validator:
    """The value must pass every one of `validators`, in order."""

    def check(name: str, value: Any) -> None:
        for validator in validators:
            validator(name, value)

    return check


def one_or_many(*validators: Validator) -> Validator:
    """The value, or every item of a list of values, must pass all `validators`."""

    def check(name: str, value: Any) -> None:
        if isinstance(value, list):
            each(*validators)(name, value)
            return
        for validator in validators:
            validator(name, value)

    return check


def subclass_of(*classes: type) -> Validator:
    """The value must be a class that subclasses one of `classes`."""

    def check(name: str, value: Any) -> None:
        if not (isinstance(value, type) and issubclass(value, classes)):
            raise TypeError(
                f"'{name}' must be a subclass of {_names(classes)}, got {value!r}."
            )

    return check


def max_characters(maximum: int) -> Validator:
    """The value must be a string of at most `maximum` characters."""

    def check(name: str, value: Any) -> None:
        if len(value) > maximum:
            raise ValueError(
                f"'{name}' must be at most {maximum} characters, got {len(value)}."
            )

    return check


def weighted(*weight_validators: Validator, min_count: int | None = None) -> Validator:
    """A list of `(value, weight)` pairs whose weights pass all `weight_validators`."""

    def check(name: str, value: Any) -> None:
        if min_count is not None:
            length(min_count)(name, value)
        for index, item in enumerate(value):
            length(2, 2)(f"{name}[{index}]", item)
            for validator in weight_validators:
                validator(f"{name}[{index}] weight", item[1])

    return check


def _names(types: tuple[type, ...]) -> str:
    return " or ".join(t.__name__ for t in types)


# endregion

# region Numbers and ranges


def vector3(name: str, value: Any) -> None:
    """Three numbers."""
    length(3, 3)(name, value)
    each(_number)(name, value)


def number_or_range(name: str, value: Any) -> None:
    """A number, or a `(min, max)` pair of numbers."""
    if isinstance(value, (list, tuple)):
        length(2, 2)(name, value)
        each(_number)(name, value)
    else:
        _number(name, value)


def integer_or_range(name: str, value: Any) -> None:
    """A whole number, or a `(min, max)` pair of whole numbers."""
    if isinstance(value, (list, tuple)):
        length(2, 2)(name, value)
        each(_integer)(name, value)
    else:
        _integer(name, value)


def integer_pair(name: str, value: Any) -> None:
    """Two whole numbers."""
    length(2, 2)(name, value)
    each(_integer)(name, value)


def non_negative_range(name: str, value: Any) -> None:
    """A `(min, max)` pair of whole numbers from 0, with min not above max."""
    length(2, 2)(name, value)
    each(_integer)(name, value)
    each(in_range(minimum=0))(name, value)
    if value[0] > value[1]:
        raise ValueError(f"{name} minimum must not be greater than its maximum.")


def duration_or_infinite(name: str, value: Any) -> None:
    """A whole number of seconds, or `"infinite"`."""
    if value != "infinite":
        _integer(name, value)


# endregion

# region Game values


def damage_sensor_value(name: str, value: Any) -> None:
    """A damage sensor's `deals_damage`: true, false or a `DamageSensor` value."""
    if not isinstance(value, bool):
        one_of(*DamageSensor)(name, value)


def rgba_or_hex(name: str, value: Any) -> None:
    """A hex color string, or four whole numbers."""
    if not isinstance(value, str):
        length(4, 4)(name, value)
        each(_integer)(name, value)


# endregion
