"""Field metadata: what a `JsonObject` field's annotation cannot say on its own.

A field's annotation is the source of truth. Its type is checked on export (`float`,
`tuple[float, float]`, a part), and metadata in `Annotated` adds the rest: a bound, a JSON shape,
a schema. Metadata never replaces the type, it only constrains or formats it:

    damage: Annotated[float | tuple[float, float], MinMax] | None = json_field(default=None)

Constraint types (`InRange`, `Length`, `Unique`, `OrderedPair`) refuse values. Shape types
(`Bounds`, `Wrapped`, `Keyed`, `Encoded`, `KeyFramed`...) change how the value is written. Every one of them
also describes the JSON it accepts, for `JsonObject.__schema__()`.

The ready-made instances at the end (`MinMax`, `NonNegative`, `Hex`...) are ready to use.
`Encoded` covers a plain conversion: a function and the schema of what it writes.
"""

import math
from collections.abc import Callable
from dataclasses import dataclass
from functools import cache
from typing import Any, Literal

from anvil.lib.jsonmodel.types import RGB, RGB255, RGBA, RGBA255, HexRGB

NUMBER: dict[str, Any] = {"type": "number"}
STRING: dict[str, Any] = {"type": "string"}


def _object_schema(
    properties: dict[str, dict[str, Any]], optional: tuple[str, ...] = ()
) -> dict[str, Any]:
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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        """The schema of the written value.

        Args:
            inner (dict[str, Any]): The schema of the annotation's type, or of the metadata
                before.
        """
        return inner

    def decode(self, data: Any) -> Any:
        """The value `encode` was given, from its parsed JSON form.

        Args:
            data (Any): The parsed JSON.

        Raises:
            TypeError: The metadata writes the value in another form and cannot read it back.
        """
        if type(self).encode is not JsonType.encode:
            raise TypeError(f"{type(self).__name__} cannot be read back from JSON.")
        return data


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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        if "anyOf" in inner:
            return inner | {"anyOf": [self.schema(arm) for arm in inner["anyOf"]]}
        if inner.get("type") == "array":
            if "prefixItems" in inner:
                return inner | {
                    "prefixItems": [self.schema(item) for item in inner["prefixItems"]]
                }
            return inner | {"items": self.schema(inner.get("items", NUMBER))}
        bounds: dict[str, Any] = {}
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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
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
class NumeratorDenominator(JsonType):
    """A `(numerator, denominator)` pair as `{"numerator": ..., "denominator": ...}`. Other
    values, such as a number or a Molang expression, are written as they are. The denominator
    must be above 0."""

    def validate(self, name: str, value: Any) -> None:
        if isinstance(value, (tuple, list)) and value[1] <= 0:
            raise ValueError(f"'{name}' denominator must be above 0, got {value[1]}.")

    def encode(self, value: Any) -> Any:
        if isinstance(value, (tuple, list)):
            return {"numerator": value[0], "denominator": value[1]}
        return value

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        fraction = _object_schema(
            {
                "numerator": {"type": "integer"},
                "denominator": {"type": "integer", "exclusiveMinimum": 0},
            }
        )
        arms = [
            fraction if arm.get("type") == "array" else arm
            for arm in inner.get("anyOf", [inner])
        ]
        return arms[0] if len(arms) == 1 else {"anyOf": arms}


@dataclass(frozen=True, slots=True)
class Wrapped(JsonType):
    """The value as `{key: value}`.

    Args:
        key (str): The key.
    """

    key: str

    def encode(self, value: Any) -> Any:
        return {self.key: value}

    def decode(self, data: Any) -> Any:
        if not isinstance(data, dict) or set(data) != {self.key}:
            raise TypeError(f"Expected an object with only '{self.key}'.")
        return data[self.key]

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
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
    written: dict[str, Any] | Callable[[dict[str, Any]], dict[str, Any]] | None = None

    def encode(self, value: Any) -> Any:
        return self.function(value)

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        return {"enum": list(self.names)}


@cache
def _vanilla_ids(kind: str, experimental: bool) -> frozenset[str]:
    """The vanilla ids of a kind, with the experimental ones when `experimental`."""
    if kind == "item":
        from anvil.api.vanilla.items import vanilla_items_ids
        from anvil.beta.vanilla.items import vanilla_items_ids as beta_items_ids

        return frozenset(
            [*vanilla_items_ids(), *(beta_items_ids() if experimental else ())]
        )
    if kind == "block":
        from anvil.api.vanilla.blocks import vanilla_block_ids
        from anvil.beta.vanilla.blocks import vanilla_block_ids as beta_block_ids

        return frozenset(
            [*vanilla_block_ids(), *(beta_block_ids() if experimental else ())]
        )
    from anvil.api.vanilla.entities import vanilla_entities_ids
    from anvil.beta.vanilla.entities import vanilla_entities_ids as beta_entities_ids

    return frozenset(
        [*vanilla_entities_ids(), *(beta_entities_ids() if experimental else ())]
    )


@dataclass(frozen=True, slots=True)
class VanillaId(JsonType):
    """A reference to an item, block or entity. A vanilla `Identifier`, such as one from
    `MinecraftItemTypes`, must name a vanilla object of that kind, and so must the name of a
    `BlockDescriptor`. An `Item`, `Block` or `Entity` checked itself when it was created, and
    a plain string is written as given.

    Args:
        kind (Literal["item", "block", "entity"]): What the reference names.
    """

    kind: Literal["item", "block", "entity"]

    def validate(self, name: str, value: Any) -> None:
        from anvil.api.blocks.descriptor import BlockDescriptor
        from anvil.lib.config import CONFIG

        from .identifier import Identifier

        if isinstance(value, BlockDescriptor):
            value = value.name
        if not isinstance(value, Identifier) or not value.is_vanilla:
            return
        if f"{value.namespace}:{value.name}" not in _vanilla_ids(
            self.kind, CONFIG._EXPERIMENTAL
        ):
            raise ValueError(f"'{value}' is not a vanilla {self.kind}. Field [{name}]")


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

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        return {"type": "object"}


def _trigger(value: Any) -> Any:
    from anvil.api.core.components import EventTrigger
    from anvil.lib.jsonmodel.enums import FilterSubject

    if isinstance(value, str):
        return EventTrigger(event=value, target=FilterSubject.Self)
    return value


def _trigger_schema(inner: dict[str, Any]) -> dict[str, Any]:
    arms = inner.get("anyOf", [inner])
    return next((arm for arm in arms if "$ref" in arm), inner)


def _kept(value: Any) -> Any:
    if isinstance(value, bool):
        return KeptObject() if value else None
    return KeptObject(value.__json__())


def _kept_schema(inner: dict[str, Any]) -> dict[str, Any]:
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


def _block_name(value: Any) -> Any:
    from anvil.api.blocks.descriptor import BlockDescriptor

    if isinstance(value, BlockDescriptor):
        return value.name
    return getattr(value, "identifier", value)


def _block_object(value: Any) -> dict[str, Any]:
    from anvil.api.blocks.descriptor import BlockDescriptor

    if isinstance(value, BlockDescriptor) and value.states:
        return {"name": value.name, "states": dict(value.states)}
    return {"name": _block_name(value)}


def _block_specifier(value: Any) -> Any:
    from anvil.api.blocks.descriptor import BlockDescriptor

    if isinstance(value, BlockDescriptor) and value.states:
        return {"name": value.name, "states": dict(value.states)}
    return _block_name(value)


def _in_project(value: str) -> str:
    from anvil.lib.config import CONFIG

    return value if ":" in value else f"{CONFIG.NAMESPACE}:{value}"


def _faces(value: Any) -> list[str]:
    from anvil.lib.jsonmodel.enums import expand_block_face_sides

    return [str(face) for face in expand_block_face_sides(list(value))]


def _icon_texture(value: Any) -> dict[str, str]:
    from anvil.lib.config import CONFIG

    return {"default": f"{CONFIG.NAMESPACE}:{value.color}"}


_TIME = InRange(0.0, 1.0)


def _frames(value: Any) -> list[tuple[float, Any]] | None:
    if (
        isinstance(value, list)
        and value
        and all(isinstance(frame, tuple) and len(frame) == 2 for frame in value)
    ):
        return value
    return None


def _over_the_day_dict(frames: list[tuple[float, Any]], encode) -> dict[str, Any]:
    return {str(time): encode(value) for time, value in frames}


def _over_the_day(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "anyOf": [
            value,
            {
                "type": "object",
                "propertyNames": {"pattern": "^(0(\\.[0-9]+)?|1(\\.0+)?)$"},
                "additionalProperties": value,
            },
        ]
    }


@dataclass(frozen=True, slots=True)
class KeyFramed(JsonType):
    """A number, or `(time, number)` keyframes written as `{"<time>": number}` over the day.
    Each time must be from 0.0 to 1.0.

    Args:
        minimum (float, optional): The lowest value, of the number or of every keyframe.
        maximum (float, optional): The highest value, of the number or of every keyframe.
    """

    minimum: float | None = None
    maximum: float | None = None

    def validate(self, name: str, value: Any) -> None:
        frames = _frames(value)
        values = InRange(self.minimum, self.maximum)
        if frames is None:
            values.validate(name, value)
            return
        for index, (time, frame_value) in enumerate(frames):
            _TIME.validate(f"{name}[{index}] time", time)
            values.validate(f"{name}[{index}] value", frame_value)

    def encode(self, value: Any) -> Any:
        frames = _frames(value)
        return value if frames is None else _over_the_day_dict(frames, lambda v: v)

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        number = InRange(self.minimum, self.maximum).schema({"type": "number"})
        return _over_the_day(number)


@dataclass(frozen=True, slots=True)
class KeyFramedColor(JsonType):
    """A color in any format, or `(time, color)` keyframes written as `{"<time>": color}` over
    the day. Each time must be from 0.0 to 1.0. A hex color is written in full, in lower
    case."""

    def validate(self, name: str, value: Any) -> None:
        for index, (time, _) in enumerate(_frames(value) or []):
            _TIME.validate(f"{name}[{index}] time", time)

    def encode(self, value: Any) -> Any:
        from anvil.lib.lib import AnvilFormatter

        frames = _frames(value)
        if frames is None:
            return AnvilFormatter.convert_color(value)
        return _over_the_day_dict(frames, AnvilFormatter.convert_color)

    def schema(self, inner: dict[str, Any]) -> dict[str, Any]:
        return _over_the_day(COLOR_SCHEMA)


# endregion

# region Ready-made metadata

NonNegative = InRange(minimum=0)
Positive = InRange(minimum=0, min_exclusive=True)
AtLeastOne = InRange(minimum=1)
Chance = InRange(0, 1)
RedstoneSignal = InRange(0, 15)
ShortTag = Length(maximum=64)
Ordered = OrderedPair()
Fraction = NumeratorDenominator()

MinMax = Bounds("min", "max")
ExactMinMax = Bounds("min", "max", exact=True)
"""A range as `min`/`max`, a single number as both ends."""
RangeMinMax = Bounds("range_min", "range_max")
ExactRangeMinMax = Bounds("range_min", "range_max", exact=True)
"""A range as `range_min`/`range_max`, a single number as both ends."""
XpRange = Bounds("minXP", "maxXP", exact=True)
DespawnDistance = Bounds("min_distance", "max_distance")
ItemObject = Wrapped("item")
ItemId = VanillaId("item")
BlockId = VanillaId("block")
EntityId = VanillaId("entity")
ColorMap = Wrapped("color_map")

Trigger = Encoded(_trigger, _trigger_schema)
"""An event name as `{"event": name, "target": "self"}`; an `EventTrigger` as it is. The game
reads a bare event name only on some keys, so a name is always written in full."""

Kept = Encoded(_kept, _kept_schema)
"""Written even when empty: a part with no options as `{}`, a switch as `{}` when True and
left out when False."""

Hex = Encoded(_hex, {"type": "string", "pattern": "^#[0-9a-fA-F]{6}$"})
"""A color in any format as a `#rrggbb` string."""

COLOR_SCHEMA: dict[str, Any] = {
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

BlockSpecifier = Encoded(
    _block_specifier,
    {
        "anyOf": [
            STRING,
            _object_schema(
                {"name": STRING, "states": {"type": "object"}}, optional=("states",)
            ),
        ]
    },
)
"""A block as its identifier, or as `{"name": ..., "states": ...}` when it has states."""

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

Pairs = Encoded(
    lambda pairs: {str(key): item for key, item in pairs},
    {"type": "object"},
)
"""`(key, value)` pairs as one object, the values written as they are."""

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
