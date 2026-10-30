"""Dataclass-based JSON model for Anvil components.

`JsonObject` is the base of every object that serialises to JSON from its fields;
`JsonComponent` adds what makes one a Minecraft component (its identifier, placement,
dependencies and clashes), `JsonCustomComponent` is the base of custom components, `JsonValue` and `JsonValueComponent` are written as the value of
their only field, and `JsonContainer` holds a named group of components. See
`anvil.lib.jsonmodel.object` for the rules both enforce.

`Identifier` is the `namespace:name` of everything in a pack, components included; it checks
the `minecraft` namespace of vanilla names and the project namespace of custom ones.
"""

from . import encoders
from .component import (
    ComponentPlacement,
    JsonComponent,
    JsonCustomComponent,
    JsonValueComponent,
)
from .container import JsonContainer, validate_components
from .fields import json_field
from .identifier import VANILLA_NAMESPACE, Identifier
from .object import JsonObject, JsonValue

__all__ = [
    "JsonObject",
    "JsonComponent",
    "JsonCustomComponent",
    "JsonContainer",
    "JsonValue",
    "JsonValueComponent",
    "validate_components",
    "Identifier",
    "VANILLA_NAMESPACE",
    "json_field",
    "ComponentPlacement",
    "encoders",
]
