"""Dataclass-based JSON model for Anvil components.

`JsonObject` is the base of every object that serialises to JSON from its fields;
`JsonComponent` adds what makes one a Minecraft component (its identifier, placement,
dependencies and clashes), `JsonCustomComponent` is the base of custom components, `JsonValue` and `JsonValueComponent` are written as the value of
their only field, and `JsonContainer` holds a named group of components. See
`anvil.lib.jsonmodel.object` for the rules both enforce.

A field's annotation says what it accepts and how it is written. Metadata from `jsontypes`
adds bounds and JSON shapes inside `Annotated`: `Annotated[float | tuple[float, float], MinMax]`.

`Identifier` is the `namespace:name` of everything in a pack, components included; it checks
the `minecraft` namespace of vanilla names and the project namespace of custom ones.
"""

from .component import (
    ComponentPlacement,
    JsonComponent,
    JsonCustomComponent,
    JsonValueComponent,
)
from .container import JsonContainer, validate_components
from .fields import json_field
from .file import JsonFile
from .identifier import VANILLA_NAMESPACE, Identifier
from .jsontypes import (
    COLOR_SCHEMA,
    AnyColor,
    AsObject,
    AsString,
    AtLeastOne,
    BlockObject,
    Bounds,
    Chance,
    ColorMap,
    DespawnDistance,
    Encoded,
    EffectName,
    ExpandFaces,
    FitToFrame,
    Hex,
    IconTexture,
    IndexInto,
    InRange,
    ItemObject,
    JsonType,
    Kept,
    KeptObject,
    Keyed,
    Length,
    Merged,
    MetersPerSecond,
    MinMax,
    NonNegative,
    Ordered,
    OrderedPair,
    Positive,
    PropertyName,
    RangeMinMax,
    RedstoneSignal,
    RGB255Color,
    RGBA255Color,
    RGBAColor,
    RGBColor,
    ShortTag,
    Trigger,
    Unique,
    Wrapped,
    XpRange,
    YesNo,
)
from .keyframes import KeyFrame, KeyFramed, KeyFramedColor
from .object import JsonObject, JsonValue

__all__ = [
    "JsonObject",
    "JsonComponent",
    "JsonCustomComponent",
    "JsonContainer",
    "JsonFile",
    "JsonValue",
    "JsonValueComponent",
    "validate_components",
    "Identifier",
    "KeyFrame",
    "KeyFramed",
    "KeyFramedColor",
    "VANILLA_NAMESPACE",
    "json_field",
    "ComponentPlacement",
    "JsonType",
    "KeptObject",
    "InRange",
    "Length",
    "Unique",
    "OrderedPair",
    "Bounds",
    "Encoded",
    "Wrapped",
    "Keyed",
    "MetersPerSecond",
    "IndexInto",
    "AsObject",
    "ExpandFaces",
    "Merged",
    "AsString",
    "IconTexture",
    "FitToFrame",
    "NonNegative",
    "Positive",
    "AtLeastOne",
    "Chance",
    "RedstoneSignal",
    "ShortTag",
    "Ordered",
    "Trigger",
    "MinMax",
    "RangeMinMax",
    "XpRange",
    "DespawnDistance",
    "Kept",
    "Hex",
    "AnyColor",
    "RGBColor",
    "RGBAColor",
    "COLOR_SCHEMA",
    "RGB255Color",
    "RGBA255Color",
    "BlockObject",
    "ItemObject",
    "ColorMap",
    "EffectName",
    "PropertyName",
    "YesNo",
]
