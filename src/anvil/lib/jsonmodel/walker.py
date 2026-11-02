"""Compiles a `JsonObject` class's field annotations into the checks, encoders and schemas its
export and `__schema__()` use.

Each class compiles once, on its first export or schema, and keeps the result. By then every
module is loaded, so an annotation may name its own class or a class declared further down.
Names in annotations must be imported at runtime, not only under `TYPE_CHECKING`. `| None`
is dropped: an unset field is skipped, not checked.

| Annotation                 | Check                              | Written as         |
| -------------------------- | ---------------------------------- | ------------------ |
| `bool`, `int`, `str`       | isinstance; a bool is not an int   | as is              |
| `float`                    | int or float, not bool             | as is              |
| `Literal[a, b]`, an `Enum` | one of the values                  | as is              |
| `X \\| Y`                  | the first arm that passes          | as that arm        |
| `list[X]`, `tuple[X, ...]` | a list or tuple of X               | a list             |
| `tuple[A, B]`              | a list or tuple of that length     | a list             |
| a `JsonObject`             | isinstance                         | its `__json__()`   |
| `type[X]`                  | a subclass of X                    | as is              |
| another class              | isinstance                         | as is              |
| `Annotated[T, *metadata]`  | T, then each metadata              | see `JsonType`     |
| `type Alias = ...`         | its value                          | its value          |
"""

import annotationlib
import dataclasses
import types
import typing
from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Any, Callable, Literal, TypeAliasType, Union

from anvil.api.core.types import JsonSchema

from .jsontypes import JsonType

DRAFT_2020_12 = "https://json-schema.org/draft/2020-12/schema"


def encode_value(value: Any) -> Any:
    """Turns nested objects, lists and dicts into their JSON form."""
    from .object import JsonObject

    if isinstance(value, JsonObject):
        return value.__json__()
    if isinstance(value, (list, tuple)):
        return [encode_value(item) for item in value]
    if isinstance(value, dict):
        return type(value)((key, encode_value(item)) for key, item in value.items())
    return value


def _as_is(value: Any) -> Any:
    return value


def _anything(definitions: dict[str, JsonSchema]) -> JsonSchema:
    return {}


@dataclass(slots=True)
class Node:
    """What one annotation checks, how it writes a value, and how it describes it.

    Attributes:
        label: The type as text, for error messages.
        check: `check(name, value)` raises TypeError for a wrong type and ValueError for a
            refused value.
        encode: `encode(value)` returns the JSON form.
        describe: `describe(definitions)` returns the schema, adding the parts it uses to
            `definitions`.
    """

    label: str
    check: Callable[[str, Any], None]
    encode: Callable[[Any], Any] = encode_value
    describe: Callable[[dict[str, JsonSchema]], JsonSchema] = _anything


@dataclass(frozen=True, slots=True)
class FieldSpec:
    """A compiled field.

    Attributes:
        exclude: The field is not written to the JSON.
        internal: State the object keeps for its own methods (excluded and not a constructor
            option). It is never checked.
        required: The field has no default, so its key is required in the schema.
    """

    name: str
    key: str
    node: Node
    exclude: bool
    internal: bool
    omit_default: bool
    required: bool
    default: Callable[[], Any]


# region Nodes


def _type_error(name: str, label: str, value: Any) -> TypeError:
    return TypeError(f"'{name}' must be {label}, got {type(value).__name__}.")


def _instance(
    cls: type, test: Callable[[Any], bool] | None = None, **node: Any
) -> Node:
    """A value that passes `test`, `isinstance(value, cls)` by default."""
    test = test or (lambda value: isinstance(value, cls))

    def check(name: str, value: Any) -> None:
        if not test(value):
            raise _type_error(name, cls.__name__, value)

    return Node(cls.__name__, check, **node)


_JSON_TYPES = {bool: "boolean", int: "integer", float: "number", str: "string"}


def _plain(cls: type) -> Node:
    """A bool, int, float or str. A bool is never a number; an int is a float."""
    accepted = (int, float) if cls is float else cls
    return _instance(
        cls,
        lambda value: (
            isinstance(value, accepted) and (cls is bool or not isinstance(value, bool))
        ),
        encode=_as_is,
        describe=lambda definitions: {"type": _JSON_TYPES[cls]},
    )


def _choice(values: tuple[Any, ...], label: str, enum: type | None = None) -> Node:
    """A Literal's or an Enum's values. A value of another type raises TypeError, a value of
    the right type that is not allowed ValueError. True never matches 1, nor 1 True."""
    plain = [value.value if isinstance(value, Enum) else value for value in values]
    kinds = tuple({type(value) for value in values + tuple(plain)})

    def check(name: str, value: Any) -> None:
        if enum is not None and isinstance(value, enum):
            return
        for allowed in plain:
            if (
                isinstance(value, bool) == isinstance(allowed, bool)
                and value == allowed
            ):
                return
        if not isinstance(value, kinds):
            raise _type_error(name, label, value)
        raise ValueError(f"'{name}' must be one of {label}, got {value!r}.")

    return Node(label, check, _as_is, lambda definitions: {"enum": plain})


def _object(cls: type) -> Node:
    """A part, written by its `__json__()` and described under `$defs`. The `$defs` entry is
    set before the part's body is built, so a part that contains itself ends in a `$ref`."""

    def describe(definitions: dict[str, JsonSchema]) -> JsonSchema:
        if cls.__name__ not in definitions:
            definitions[cls.__name__] = {}
            definitions[cls.__name__] = cls.__schema_body__(definitions)
        return {"$ref": f"#/$defs/{cls.__name__}"}

    return _instance(cls, encode=lambda value: value.__json__(), describe=describe)


def _items(item: Node | list[Node]) -> Node:
    """`list[X]` given one node, `tuple[A, B]` given a node per position."""
    fixed = isinstance(item, list)
    if fixed:
        label = f"tuple[{', '.join(node.label for node in item)}]"
    else:
        label = f"list[{item.label}]"

    def nodes(value: Any) -> list[Node]:
        return item if fixed else [item] * len(value)

    def check(name: str, value: Any) -> None:
        if not isinstance(value, (list, tuple)):
            raise _type_error(name, label, value)
        if fixed and len(value) != len(item):
            raise ValueError(f"'{name}' must have {len(item)} items, got {len(value)}.")
        for index, (node, entry) in enumerate(zip(nodes(value), value)):
            node.check(f"{name}[{index}]", entry)

    def describe(definitions: dict[str, JsonSchema]) -> JsonSchema:
        if not fixed:
            return {"type": "array", "items": item.describe(definitions)}
        return {
            "type": "array",
            "prefixItems": [node.describe(definitions) for node in item],
            "minItems": len(item),
            "maxItems": len(item),
        }

    return Node(
        label,
        check,
        lambda value: [node.encode(entry) for node, entry in zip(nodes(value), value)],
        describe,
    )


def _union(arms: list[Node]) -> Node:
    """The first arm that passes. An arm that raises TypeError does not match the type; when
    no arm passes, the first ValueError is raised, since its arm matched the type."""
    label = " | ".join(arm.label for arm in arms)

    def matching(name: str, value: Any) -> Node:
        refusal: ValueError | None = None
        for arm in arms:
            try:
                arm.check(name, value)
                return arm
            except TypeError:
                pass
            except ValueError as error:
                refusal = refusal or error
        raise refusal or _type_error(name, label, value)

    def describe(definitions: dict[str, JsonSchema]) -> JsonSchema:
        schemas: list[JsonSchema] = []
        for arm in arms:
            schema = arm.describe(definitions)
            for entry in schema.get("anyOf", [schema]):
                if entry not in schemas:
                    schemas.append(entry)
        if {} in schemas:
            return {}
        return schemas[0] if len(schemas) == 1 else {"anyOf": schemas}

    return Node(
        label,
        matching,
        lambda value: matching("", value).encode(value),
        describe,
    )


def _annotated(inner: Node, metadata: list[JsonType]) -> Node:
    """The inner type, then each metadata. Metadata that overrides `encode` writes the value
    in place of the inner type, in order."""
    encoders = [meta for meta in metadata if type(meta).encode is not JsonType.encode]

    def check(name: str, value: Any) -> None:
        inner.check(name, value)
        for meta in metadata:
            meta.validate(name, value)

    def encode(value: Any) -> Any:
        for meta in encoders:
            value = meta.encode(value)
        return encode_value(value)

    def describe(definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = inner.describe(definitions)
        for meta in metadata:
            schema = meta.schema(schema)
        return schema

    return Node(inner.label, check, encode if encoders else inner.encode, describe)


# endregion

# region Compiling


def _compile(annotation: Any) -> Node:
    """The node of a field annotation."""
    from .object import JsonObject

    if isinstance(annotation, TypeAliasType):
        return _compile(annotation.__value__)
    if annotation is Any:
        return Node("Any", lambda name, value: None)

    origin, arguments = typing.get_origin(annotation), typing.get_args(annotation)
    if origin is Annotated:
        metadata = [
            meta for meta in annotation.__metadata__ if isinstance(meta, JsonType)
        ]
        return _annotated(_compile(annotation.__origin__), metadata)
    if origin in (Union, types.UnionType):
        arms = [_compile(arm) for arm in arguments if arm is not type(None)]
        return arms[0] if len(arms) == 1 else _union(arms)
    if origin is Literal:
        label = " | ".join(repr(getattr(value, "value", value)) for value in arguments)
        return _choice(arguments, label)
    if origin is list or (origin is tuple and arguments[1:] == (Ellipsis,)):
        return _items(_compile(arguments[0]))
    if origin is tuple:
        return _items([_compile(argument) for argument in arguments])
    if origin is type:
        return _instance(
            type,
            lambda value: isinstance(value, type) and issubclass(value, arguments[0]),
            encode=_as_is,
            describe=lambda definitions: {"type": "string"},
        )

    cls = origin or annotation
    if not isinstance(cls, type):
        raise TypeError(f"Cannot read the annotation {annotation!r}.")
    if cls in _JSON_TYPES:
        return _plain(cls)
    if issubclass(cls, Enum):
        return _choice(tuple(cls), cls.__name__, cls)
    if issubclass(cls, JsonObject):
        return _object(cls)
    if issubclass(cls, str):
        return _instance(cls, describe=lambda definitions: {"type": "string"})
    return _instance(cls)


def compile_fields(cls: type) -> tuple[FieldSpec, ...]:
    """The compiled fields of a `JsonObject` class."""
    annotations: dict[str, Any] = {}
    for owner in reversed(cls.__mro__):
        if dataclasses.is_dataclass(owner):
            annotations |= annotationlib.get_annotations(owner, eval_str=True)

    specs = []
    for field in dataclasses.fields(cls):
        exclude = bool(field.metadata.get("exclude"))
        if field.default_factory is not dataclasses.MISSING:
            default = field.default_factory
        else:
            default = lambda value=field.default: value
        specs.append(
            FieldSpec(
                name=field.name,
                key=field.metadata.get("key") or field.name,
                node=_compile(annotations[field.name]),
                exclude=exclude,
                internal=exclude and not field.init,
                omit_default=bool(field.metadata.get("omit_default")),
                required=field.default is dataclasses.MISSING
                and field.default_factory is dataclasses.MISSING,
                default=default,
            )
        )
    return tuple(specs)


# endregion
