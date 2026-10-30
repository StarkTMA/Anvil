"""The `JsonObject` base class, and `JsonValue`, an object written as the value of its only
field.

A `JsonObject` subclass is declared with fields only. The base class:

- turns every subclass into `@dataclass(kw_only=True, slots=True, eq=False)`;
- refuses a subclass that defines `__init__` (use `__post_init__` for side effects);
- lets only the object's own methods change its fields;
- builds the JSON from the fields in `__json__()`, validating them first.

A class declared with `abstract=True` is a shared base that cannot be instantiated.
"""

from __future__ import annotations

import dataclasses
import sys
from typing import Any, ClassVar, Self, dataclass_transform

from anvil.api.core.types import JsonPayload

from .fields import default_of, json_field


def _encode(value: Any) -> Any:
    """Turns nested objects, lists and dicts into their JSON form."""
    if isinstance(value, JsonObject):
        return value.__json__()
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return type(value)((key, _encode(item)) for key, item in value.items())
    return value


def _encode_field(field: dataclasses.Field, value: Any) -> Any:
    """The JSON form of a field's value, through the field's encoder when it has one."""
    if value is not None and field.metadata.get("encoder") is not None:
        value = field.metadata["encoder"](value)
    return _encode(value)


@dataclass_transform(
    kw_only_default=True, field_specifiers=(json_field, dataclasses.field)
)
class _JsonObjectMeta(type):
    def __new__(mcs, name, bases, namespace, abstract: bool = False, **kwargs):
        if "__dataclass_params__" in namespace:
            return super().__new__(mcs, name, bases, namespace, **kwargs)

        if "__init__" in namespace:
            raise TypeError(
                f"{name} must not define __init__. Declare fields, and use __post_init__ "
                "for side effects or __validate__ for checks."
            )
        namespace["_abstract"] = abstract
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        return dataclasses.dataclass(kw_only=True, slots=True, eq=False)(cls)


class JsonObject(metaclass=_JsonObjectMeta, abstract=True):
    """Base class of every object that serialises to JSON from its fields.

    Used directly for nested objects that only appear inside a component (a surface builder
    variant, a replacement entry). Components themselves use `JsonComponent`.
    """

    _abstract: ClassVar[bool]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        if cls._abstract:
            raise TypeError(
                f"{cls.__name__} is an abstract base and cannot be instantiated."
            )
        return object.__new__(cls)

    def __post_init__(self) -> None:
        """Side effects after construction."""

    def __prepare_export__(self, owner: Any, *, root: bool = True) -> None:
        """Finishes the object for export, where its owner calls it. Components with a
        localized name override it. `root` is False for a permutation's components.
        """

    def __validate__(self) -> None:
        """Cross-field checks, run on export after the field validators."""

    def __setattr__(self, name: str, value: Any) -> None:
        caller = sys._getframe(1)
        code = caller.f_code
        first_argument = code.co_varnames[0] if code.co_argcount else None
        if caller.f_locals.get(first_argument) is not self:
            raise AttributeError(
                f"{type(self).__name__}.{name} is read-only. Set it in the constructor or "
                "with a builder method."
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"{type(self).__name__}.{name} is read-only.")

    def __json__(self) -> JsonPayload:
        """The JSON payload of this object, built from its fields after validating them."""
        cls = type(self)
        fields = dataclasses.fields(self)

        for field in fields:
            value = getattr(self, field.name)
            if value is not None:
                for validator in field.metadata.get("validators", ()):
                    validator(f"{cls.__name__}.{field.name}", value)
        self.__validate__()

        payload: JsonPayload = {}
        for field in fields:
            value = getattr(self, field.name)
            if value is None or field.metadata.get("exclude"):
                continue
            if field.metadata.get("omit_default") and value == default_of(field):
                continue
            payload[field.metadata.get("key") or field.name] = _encode_field(
                field, value
            )
        return payload


def only_value(obj: JsonObject, payload: JsonPayload) -> Any:
    """The value of the only key in an object's payload."""
    if len(payload) > 1:
        raise TypeError(
            f"{type(obj).__name__} is written as the value of one field, but has "
            f"{', '.join(payload)}."
        )
    return next(iter(payload.values()), None)


class JsonValue(JsonObject, abstract=True):
    """A part written as the value of its only JSON field (`3`, `"path"`, `{face: ...}`),
    rather than as a JSON object of its fields.
    """

    def __json__(self) -> Any:
        return only_value(self, JsonObject.__json__(self))
