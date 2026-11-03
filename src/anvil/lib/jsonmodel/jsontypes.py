"""Field metadata: what a `JsonObject` field's annotation cannot say on its own.

A field's annotation is the source of truth. Its type is checked on export (`float`,
`tuple[float, float]`, a part), and metadata in `Annotated` adds the rest: a bound, a JSON shape,
a schema. Metadata never replaces the type, it only constrains or formats it:

    damage: Annotated[float | tuple[float, float], MinMax] | None = json_field(default=None)

Constraint types (`InRange`, `Length`, `Unique`, `OrderedPair`) refuse values. Shape types
(`Bounds`, `Wrapped`, `Keyed`, `Encoded`...) change how the value is written. Every one of them
also describes the JSON it accepts, for `JsonObject.__schema__()`.

The ready-made instances at the end (`MinMax`, `NonNegative`, `Hex`...) are ready to use.
`Encoded` covers a plain conversion: a function and the schema of what it writes.
"""

import math
from dataclasses import dataclass
from typing import Any, Callable

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, JsonSchema

NUMBER: JsonSchema = {"type": "number"}
STRING: JsonSchema = {"type": "string"}


def _object_schema(
    properties: dict[str, JsonSchema], optional: tuple[str, ...] = ()
) -> JsonSchema:
    """An object with exactly these keys, all required but the `optional` ones."""
    return {
        "type": "object",
        "properties": properties,
        "required": [key for key in properties if key not in optional],
        "additionalProperties": False,
    }


class KeptObject(dict):
    """A JSON object written even when it is empty. Anvil drops empty objects on export, but
    some keys are switches whose empty object turns a behavior on (`"remove_on_hit": {}`).
    """


class JsonType:
    """Metadata in `Annotated` that checks, encodes and describes a field's value.

    The annotation's own type is checked first; a JsonType adds what the type cannot say.
    Several stack and apply in order: `Annotated[float, MetersPerSecond(4), RangeMinMax]`
    converts the speed, then writes the pair as `range_min`/`range_max`.

    `encode` gets the Python value and returns its JSON form; parts and tuples in what it
    returns are written as usual. A JsonType that leaves `encode` alone lets the inner type
    write the value, metadata nested inside it included.
    """

    def validate(self, name: str, value: Any) -> None:
        """Checks beyond the type.

        Args:
            name (str): The field name, for the error message.
            value (Any): The value, already checked against the annotation's type.

        Raises:
            ValueError: The value breaks the rule.
        """

    def encode(self, value: Any) -> Any:
        """The JSON form of the value.

        Args:
            value (Any): The value, already validated.
        """
        return value

    def schema(self, inner: JsonSchema) -> JsonSchema:
        """The schema of the written value.

        Args:
            inner (JsonSchema): The schema of the annotation's type, or of the metadata before.
        """
        return inner


# region Constraints


@dataclass(frozen=True, slots=True)
class InRange(JsonType):
    """A number within the given bounds. On a tuple or list, every item.

    Args:
        minimum (float, optional): The lowest value.
        maximum (float, optional): The highest value.
        min_exclusive (bool): The minimum itself is refused.
        max_exclusive (bool): The maximum itself is refused.
    """

    minimum: float | None = None
    maximum: float | None = None
    min_exclusive: bool = False
    max_exclusive: bool = False

    def __str__(self) -> str:
        if self.maximum is None:
            return f"{'above' if self.min_exclusive else 'at least'} {self.minimum}"
        if self.minimum is None:
            return f"{'below' if self.max_exclusive else 'at most'} {self.maximum}"
        if self.min_exclusive or self.max_exclusive:
            low = "(" if self.min_exclusive else "["
            high = ")" if self.max_exclusive else "]"
            return f"in {low}{self.minimum}, {self.maximum}{high}"
        if self.minimum == self.maximum:
            return f"exactly {self.minimum}"
        return f"from {self.minimum} to {self.maximum}"

    def contains(self, number: float) -> bool:
        return (
            self.minimum is None
            or number > self.minimum
            or (number == self.minimum and not self.min_exclusive)
        ) and (
            self.maximum is None
            or number < self.maximum
            or (number == self.maximum and not self.max_exclusive)
        )

    def validate(self, name: str, value: Any) -> None:
        if isinstance(value, (tuple, list)):
            for index, item in enumerate(value):
                self.validate(f"{name}[{index}]", item)
        elif not self.contains(value):
            raise ValueError(f"'{name}' must be {self}, got {value}.")

    def schema(self, inner: JsonSchema) -> JsonSchema:
        if "anyOf" in inner:
            return inner | {"anyOf": [self.schema(arm) for arm in inner["anyOf"]]}
        if inner.get("type") == "array":
            if "prefixItems" in inner:
                return inner | {
                    "prefixItems": [self.schema(item) for item in inner["prefixItems"]]
                }
            return inner | {"items": self.schema(inner.get("items", NUMBER))}
        bounds: JsonSchema = {}
        if self.minimum is not None:
            bounds["exclusiveMinimum" if self.min_exclusive else "minimum"] = (
                self.minimum
            )
        if self.maximum is not None:
            bounds["exclusiveMaximum" if self.max_exclusive else "maximum"] = (
                self.maximum
            )
        return inner | bounds


@dataclass(frozen=True, slots=True)
class Length(InRange):
    """A list, tuple or string with a length within the given bounds.

    Args:
        minimum (int, optional): The shortest length.
        maximum (int, optional): The longest length.
    """

    def validate(self, name: str, value: Any) -> None:
        if not self.contains(len(value)):
            unit = "characters" if isinstance(value, str) else "items"
            raise ValueError(f"'{name}' must have {self} {unit}, got {len(value)}.")

    def schema(self, inner: JsonSchema) -> JsonSchema:
        text = inner.get("type") == "string"
        limits = {
            "minLength" if text else "minItems": self.minimum,
            "maxLength" if text else "maxItems": self.maximum,
        }
        return inner | {
            key: limit for key, limit in limits.items() if limit is not None
        }


@dataclass(frozen=True, slots=True)
class Unique(JsonType):
    """No two items share the same `attribute`. Items with the attribute unset are skipped.

    Args:
        attribute (str): The attribute compared.
    """

    attribute: str

    def validate(self, name: str, value: Any) -> None:
        seen = set()
        for item in value:
            key = getattr(item, self.attribute, None)
            if key is None:
                continue
            if key in seen:
                raise ValueError(
                    f"'{name}' has more than one item with {self.attribute} {key!r}."
                )
            seen.add(key)


@dataclass(frozen=True, slots=True)
class OrderedPair(JsonType):
    """A `(min, max)` pair with min not above max."""

    def validate(self, name: str, value: Any) -> None:
        if value[0] > value[1]:
            raise ValueError(f"'{name}' minimum must not be greater than its maximum.")


# endregion

# region Shapes


@dataclass(frozen=True, slots=True)
class Bounds(JsonType):
    """A `(min, max)` pair as `{low: ..., high: ...}`, smallest first. A single number is
    written as it is, or as both ends when `exact`.

    Args:
        low (str): The key of the smaller value.
        high (str): The key of the larger value.
        exact (bool): Write a single number as both ends.
    """

    low: str
    high: str
    exact: bool = False

    def encode(self, value: Any) -> Any:
        if isinstance(value, (tuple, list)):
            return {self.low: min(value), self.high: max(value)}
        return {self.low: value, self.high: value} if self.exact else value

    def schema(self, inner: JsonSchema) -> JsonSchema:
        arms = inner.get("anyOf", [inner])
        single = [arm for arm in arms if arm.get("type") in ("number", "integer")]
        pairs = [arm for arm in arms if arm.get("type") == "array"]
        end = single[0] if single else NUMBER
        if pairs:
            end = pairs[0].get("prefixItems", [pairs[0].get("items", end)])[0]
        pair = _object_schema({self.low: end, self.high: end})
        if self.exact or not single:
            return pair
        return {"anyOf": [single[0], pair]}


@dataclass(frozen=True, slots=True)
class Wrapped(JsonType):
    """The value as `{key: value}`.

    Args:
        key (str): The key.
    """

    key: str

    def encode(self, value: Any) -> Any:
        return {self.key: value}

    def schema(self, inner: JsonSchema) -> JsonSchema:
        return _object_schema({self.key: inner})


@dataclass(frozen=True, slots=True)
class Keyed(JsonType):
    """A list of parts as one object keyed by each part's `attribute`. Two parts with the same
    key are refused.

    Args:
        attribute (str): The attribute written as the key.
    """

    attribute: str

    def validate(self, name: str, value: Any) -> None:
        Unique(self.attribute).validate(name, value)

    def encode(self, value: Any) -> Any:
        return {str(getattr(item, self.attribute)): item for item in value}

    def schema(self, inner: JsonSchema) -> JsonSchema:
        return {"type": "object", "additionalProperties": inner.get("items", {})}


@dataclass(frozen=True, slots=True)
class Encoded(JsonType):
    """Writes the value through a function.

    Args:
        function (Callable[[Any], Any]): Turns the value into its JSON form.
        written (JsonSchema | Callable[[JsonSchema], JsonSchema], optional): The schema of
            what the function writes, or a function of the annotation type's schema. None
            keeps the annotation type's schema.
    """

    function: Callable[[Any], Any]
    written: JsonSchema | Callable[[JsonSchema], JsonSchema] | None = None

    def encode(self, value: Any) -> Any:
        return self.function(value)

    def schema(self, inner: JsonSchema) -> JsonSchema:
        if callable(self.written):
            return self.written(inner)
        return inner if self.written is None else self.written


@dataclass(frozen=True, slots=True)
class MetersPerSecond(JsonType):
    """A speed in blocks per second, or a `(min, max)` pair of them, as the game's speed value.

    Args:
        digits (int): The decimals kept.
    """

    digits: int

    def encode(self, value: Any) -> Any:
        if isinstance(value, (tuple, list)):
            return tuple(self.encode(speed) for speed in value)
        return round(0.152 * math.sqrt(value), self.digits)


@dataclass(frozen=True, slots=True)
class IndexInto(JsonType):
    """A position in `names` as the name at that position.

    Args:
        names (tuple[str, ...]): The names, in order.
    """

    names: tuple[str, ...]

    def encode(self, value: Any) -> Any:
        return self.names[value]

    def schema(self, inner: JsonSchema) -> JsonSchema:
        return {"enum": list(self.names)}


class Merged(JsonType):
    """Components as one object keyed by each component's identifier. Two components with
    the same identifier are refused."""

    def validate(self, name: str, value: Any) -> None:
        Unique("identifier").validate(name, value)

    def encode(self, value: Any) -> Any:
        payload: dict[str, Any] = {}
        for component in value:
            payload.update(component.__json__())
        return payload

    def schema(self, inner: JsonSchema) -> JsonSchema:
        return {"type": "object"}


def _trigger(value: Any) -> Any:
    from anvil.api.core.components import EventTrigger
    from anvil.api.core.enums import FilterSubject

    if isinstance(value, str):
        return EventTrigger(event=value, target=FilterSubject.Self)
    return value


def _trigger_schema(inner: JsonSchema) -> JsonSchema:
    arms = inner.get("anyOf", [inner])
    return next((arm for arm in arms if "$ref" in arm), inner)


def _kept(value: Any) -> Any:
    if isinstance(value, bool):
        return KeptObject() if value else None
    return KeptObject(value.__json__())


def _kept_schema(inner: JsonSchema) -> JsonSchema:
    if inner.get("type") == "boolean":
        return {"type": "object", "additionalProperties": False}
    return inner


def _hex(value: Any) -> str:
    from anvil.lib.lib import AnvilFormatter

    return AnvilFormatter.convert_color(value, HexRGB)


def _color(value: Any) -> Any:
    from anvil.lib.lib import AnvilFormatter

    return AnvilFormatter.convert_color(value)


def _rgb(value: Any) -> Any:
    from anvil.lib.lib import AnvilFormatter

    return AnvilFormatter.convert_color(value, RGB)


def _rgba(value: Any) -> Any:
    from anvil.lib.lib import AnvilFormatter

    return AnvilFormatter.convert_color(value, RGBA)


def _rgb255(value: Any) -> Any:
    from anvil.lib.lib import AnvilFormatter

    if isinstance(value, str) and len(value.removeprefix("#")) in (4, 8):
        raise ValueError(
            f"The color {value} has an alpha channel; give only the color channels."
        )
    return AnvilFormatter.convert_color(value, RGB255)


def _rgba255(value: Any) -> Any:
    from anvil.lib.lib import AnvilFormatter

    return AnvilFormatter.convert_color(value, RGBA255)


def _block_object(value: Any) -> dict[str, Any]:
    from anvil.lib.schemas import MinecraftBlockDescriptor

    if isinstance(value, MinecraftBlockDescriptor) and value.states:
        return {"name": value.identifier, "states": dict(value.states)}
    return {"name": getattr(value, "identifier", value)}


def _in_project(value: str) -> str:
    from anvil.lib.config import CONFIG

    return value if ":" in value else f"{CONFIG.NAMESPACE}:{value}"


def _faces(value: Any) -> list[str]:
    from anvil.api.core.enums import expand_block_face_sides

    return [str(face) for face in expand_block_face_sides(list(value))]


def _icon_texture(value: Any) -> dict[str, str]:
    from anvil.lib.config import CONFIG

    return {"default": f"{CONFIG.NAMESPACE}:{value.color}"}


# endregion

# region Ready-made metadata

NonNegative = InRange(minimum=0)
Positive = InRange(minimum=0, min_exclusive=True)
AtLeastOne = InRange(minimum=1)
Chance = InRange(0, 1)
RedstoneSignal = InRange(0, 15)
ShortTag = Length(maximum=64)
Ordered = OrderedPair()

MinMax = Bounds("min", "max")
RangeMinMax = Bounds("range_min", "range_max")
XpRange = Bounds("minXP", "maxXP", exact=True)
DespawnDistance = Bounds("min_distance", "max_distance")
ItemObject = Wrapped("item")
ColorMap = Wrapped("color_map")

Trigger = Encoded(_trigger, _trigger_schema)
"""An event name as `{"event": name, "target": "self"}`; an `EventTrigger` as it is. The game
reads a bare event name only on some keys, so a name is always written in full."""

Kept = Encoded(_kept, _kept_schema)
"""Written even when empty: a part with no options as `{}`, a switch as `{}` when True and
left out when False."""

Hex = Encoded(_hex, {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"})
"""A color in any format as a `#rrggbb` string."""

COLOR_SCHEMA: JsonSchema = {
    "anyOf": [
        {"type": "string", "pattern": "^#([0-9a-fA-F]{6}|[0-9a-fA-F]{8})$"},
        {
            "type": "array",
            "items": {"type": "number", "minimum": 0},
            "minItems": 3,
            "maxItems": 4,
        },
    ]
}
"""A color as the game reads it: a `#rrggbb(aa)` string, or three or four numbers."""

AnyColor = Encoded(_color, COLOR_SCHEMA)
"""A color in any format, written in that format. A hex string is written in full, in
lower case."""

RGBColor = Encoded(
    _rgb,
    {
        "type": "array",
        "items": {"type": "number", "minimum": 0, "maximum": 1},
        "minItems": 3,
        "maxItems": 3,
    },
)
"""A color in any format as three numbers from 0 to 1."""

RGBAColor = Encoded(
    _rgba,
    {
        "type": "array",
        "items": {"type": "number", "minimum": 0, "maximum": 1},
        "minItems": 4,
        "maxItems": 4,
    },
)
"""A color in any format as four numbers from 0 to 1."""

RGB255Color = Encoded(
    _rgb255,
    {
        "type": "array",
        "items": {"type": "integer", "minimum": 0, "maximum": 255},
        "minItems": 3,
        "maxItems": 3,
    },
)
"""A color without alpha, in any format, as three whole numbers from 0 to 255. A hex color
with an alpha channel is refused."""

RGBA255Color = Encoded(
    _rgba255,
    {
        "type": "array",
        "items": {"type": "integer", "minimum": 0, "maximum": 255},
        "minItems": 4,
        "maxItems": 4,
    },
)
"""A color in any format as four whole numbers from 0 to 255."""

BlockObject = Encoded(
    _block_object,
    _object_schema(
        {"name": STRING, "states": {"type": "object"}}, optional=("states",)
    ),
)
"""A block as `{"name": ..., "states": ...}`, `states` only when it has any."""

AsString = Encoded(str, STRING)
"""The value as its text, for objects written as their identifier."""

EffectName = Encoded(lambda value: str(value).removeprefix("minecraft:"), STRING)
"""A name without its `minecraft:` namespace."""

PropertyName = Encoded(_in_project)
"""A name in the project namespace when it has none: `"size"` is `"<namespace>:size"`."""

YesNo = Encoded(lambda value: "yes" if value else "no", {"enum": ["yes", "no"]})
"""True as `"yes"`, False as `"no"`."""

AsObject = Encoded(
    lambda pairs: {str(key): str(item) for key, item in pairs},
    {"type": "object", "additionalProperties": STRING},
)
"""`(key, value)` pairs as one object, both written as text."""

ExpandFaces = Encoded(_faces)
"""Block faces with `side` and `all` written as the faces they stand for."""

IconTexture = Encoded(_icon_texture, _object_schema({"default": STRING}))
"""An item's textures as `{"default": "<namespace>:<color texture>"}`."""

FitToFrame = Encoded(
    lambda value: {} if value else False,
    {"anyOf": [{"type": "object", "additionalProperties": False}, {"const": False}]},
)
"""True as `{}`, the way Blockbench writes it; False as `false`."""

# endregion
