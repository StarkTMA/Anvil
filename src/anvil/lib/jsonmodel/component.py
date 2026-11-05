"""The `JsonComponent` base class: a `JsonObject` that is a Minecraft component.

`JsonValueComponent` is a component written as `{identifier: value}`, `JsonCustomComponent` is
the base of custom components, and `ComponentPlacement` says where a component may go.

A component has an `identifier` (its JSON key, such as `"minecraft:climate"`) and exports as
`{identifier: payload}`. Every concrete subclass must set `identifier`; shared bases are declared
with `abstract=True`. The text is parsed into an `Identifier` when the class is defined.

The components Anvil implements are Minecraft's, so their identifier is in the `minecraft`
namespace. Custom components (registered by a script) subclass `JsonCustomComponent`, and their
identifier is in the project namespace, `CONFIG.NAMESPACE`. `Identifier.parse` checks both.
"""

from __future__ import annotations

from enum import Flag, auto
from typing import Any, ClassVar

from .identifier import Identifier
from .object import JsonObject, only_schema, only_value


class ComponentPlacement(Flag):
    """Where a component may be placed inside its owner.

    Replaces the old pair of instance flags `_allowed_in_root` and `_allowed_in_group`.
    A group is a component group for entities and a permutation for blocks.
    """

    ROOT = auto()
    GROUP = auto()
    ANY = ROOT | GROUP


class JsonComponent(JsonObject, abstract=True):
    """Base class of every component.

    Class settings:
        identifier: The component key, for example `"minecraft:climate"`. Required. Parsed
            with `Identifier.parse`, which refuses another namespace than `minecraft`.
        _placement: Where the component may go: root, groups (permutations for blocks), or both.
        _requires: Component classes that must be present next to this one.
        _clashes: Component classes that must not be present next to this one, in the same
            container or, for a group, in the root. Checked both ways, so one side is enough.
    """

    _placement: ClassVar[ComponentPlacement] = ComponentPlacement.ANY
    _requires: ClassVar[tuple[type["JsonComponent"], ...]] = ()
    _clashes: ClassVar[tuple[type["JsonComponent"], ...]] = ()

    identifier: ClassVar[Identifier]

    def __init_subclass__(cls) -> None:
        if cls._abstract or "__dataclass_params__" in cls.__dict__:
            return
        identifier = getattr(cls, "identifier", None)
        if not isinstance(identifier, str):
            raise TypeError(
                f"{cls.__name__} must set `identifier`, or be declared with abstract=True."
            )
        cls.identifier = cls._parse_identifier(identifier)

    @classmethod
    def _parse_identifier(cls, identifier: str) -> Identifier:
        return Identifier.parse(identifier, vanilla=True, object_type=cls.__name__)

    def __json__(self) -> dict[str, Any]:
        """The component as `{identifier: payload}`."""
        return {self.identifier: JsonObject.__json__(self)}

    @classmethod
    def __schema_body__(cls, definitions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """The schema of `{identifier: payload}`."""
        return {
            "type": "object",
            "properties": {cls.identifier: cls.__payload_schema__(definitions)},
            "required": [cls.identifier],
            "additionalProperties": False,
        }

    @classmethod
    def __payload_schema__(
        cls, definitions: dict[str, dict[str, Any]]
    ) -> dict[str, Any]:
        """The schema of the payload under the identifier."""
        return JsonObject.__schema_body__.__func__(cls, definitions)


class JsonCustomComponent(JsonComponent, abstract=True):
    """Base of custom components: components registered by a script.

    The identifier is in the project namespace, `CONFIG.NAMESPACE`, and may leave it out:
    `"explosive"` is `<namespace>:explosive`. The `minecraft` namespace, or any other, is
    refused.
    """

    @classmethod
    def _parse_identifier(cls, identifier: str) -> Identifier:
        return Identifier.parse(identifier, vanilla=False, object_type=cls.__name__)


class JsonValueComponent(JsonComponent, abstract=True):
    """A component written as `{identifier: value}`, the value of its only JSON field, rather
    than as `{identifier: {...}}`.
    """

    def __json__(self) -> dict[str, Any]:
        exported = JsonComponent.__json__(self)
        return {self.identifier: only_value(self, exported[self.identifier])}

    @classmethod
    def __payload_schema__(
        cls, definitions: dict[str, dict[str, Any]]
    ) -> dict[str, Any]:
        return only_schema(cls, definitions)
