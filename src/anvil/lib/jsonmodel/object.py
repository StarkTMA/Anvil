"""The `JsonObject` base class, and `JsonValue`, an object written as the value of its only
field.

A `JsonObject` subclass is declared with fields only. The base class:

- turns every subclass into `@dataclass(kw_only=True, slots=True, eq=False)`;
- refuses a subclass that defines `__init__` (use `__post_init__` for side effects);
- lets only the object's own methods change its fields;
- builds the JSON from the fields in `__json__()`, checking them against their annotations
  first;
- describes that JSON in `__schema__()`.

A class declared with `abstract=True` is a shared base that cannot be instantiated.
"""

from __future__ import annotations

import dataclasses
import sys
from typing import Any, ClassVar, Self, dataclass_transform

from anvil.api.core.types import JsonPayload, JsonSchema

from .fields import json_field
from .walker import DRAFT_2020_12, FieldSpec, compile_fields

_FIELDS: dict[type, tuple[FieldSpec, ...]] = {}


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
    __required__: ClassVar[tuple[str, ...]] = ()
    """JSON keys the schema marks required although their field is optional, because
    `__validate__` requires them."""

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
        """Cross-field checks, run on export after the fields are checked."""

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

    @classmethod
    def __json_fields__(cls) -> tuple[FieldSpec, ...]:
        """The compiled fields of this class, compiled on first use."""
        specs = _FIELDS.get(cls)
        if specs is None:
            specs = _FIELDS[cls] = compile_fields(cls)
        return specs

    def __json__(self) -> JsonPayload:
        """The JSON payload of this object, built from its fields after checking them."""
        cls = type(self)
        specs = cls.__json_fields__()

        for spec in specs:
            value = getattr(self, spec.name)
            if value is not None and not spec.internal:
                spec.node.check(f"{cls.__name__}.{spec.name}", value)
        self.__validate__()

        payload: JsonPayload = {}
        for spec in specs:
            value = getattr(self, spec.name)
            if value is None or spec.exclude:
                continue
            if spec.omit_default and value == spec.default():
                continue
            payload[spec.key] = spec.node.encode(value)
        return payload

    @classmethod
    def __schema__(cls) -> JsonSchema:
        """The JSON Schema (draft 2020-12) of this object's JSON, its parts under `$defs`."""
        definitions: dict[str, JsonSchema] = {}
        body = cls.__schema_body__(definitions)
        schema = {"$schema": DRAFT_2020_12, **body}
        if definitions:
            schema["$defs"] = definitions
        return schema

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        """The schema of this object's JSON, adding the parts it uses to `definitions`.

        Args:
            definitions (dict[str, JsonSchema]): The `$defs` of the schema being built.
        """
        properties: JsonSchema = {}
        required: list[str] = []
        for spec in cls.__json_fields__():
            if spec.exclude:
                continue
            properties[spec.key] = spec.node.describe(definitions)
            if (
                spec.required and not spec.omit_default
            ) or spec.key in cls.__required__:
                required.append(spec.key)
        schema: JsonSchema = {"type": "object", "properties": properties}
        if required:
            schema["required"] = required
        schema["additionalProperties"] = False
        return schema


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

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        return only_schema(cls, definitions)


def only_schema(
    cls: type[JsonObject], definitions: dict[str, JsonSchema]
) -> JsonSchema:
    """The schema of the only field a class writes."""
    specs = [spec for spec in cls.__json_fields__() if not spec.exclude]
    if len(specs) != 1:
        raise TypeError(
            f"{cls.__name__} is written as the value of one field, but has "
            f"{', '.join(spec.key for spec in specs)}."
        )
    return specs[0].node.describe(definitions)
