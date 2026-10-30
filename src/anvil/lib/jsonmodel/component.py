"""The `JsonComponent` base class: a `JsonObject` that is a Minecraft component.

`JsonValueComponent` is a component written as `{identifier: value}`, and `ComponentPlacement`
says where a component may go.

A component has an `identifier` (its JSON key, such as `"minecraft:climate"`) and exports as
`{identifier: payload}`. Every concrete subclass must set `identifier`; shared bases are declared
with `abstract=True`. The text is parsed into an `Identifier` when the class is defined.

The components Anvil implements are Minecraft's, so their identifier is in the `minecraft`
namespace. Custom components (registered by a script) set `_custom = True` on their base, and
their identifier is in the project namespace, `CONFIG.NAMESPACE`. `Identifier.parse` checks both.
"""

from __future__ import annotations

from enum import Flag, auto
from typing import ClassVar

from anvil.api.core.types import ComponentClasses, JsonExport

from .identifier import Identifier
from .object import JsonObject, only_value


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
            with `Identifier.parse`, which refuses another namespace than `minecraft`, or the
            project namespace for a custom component. A custom component may leave out the
            namespace.
        _custom: True on the base of custom components.
        _placement: Where the component may go: root, groups (permutations for blocks), or both.
        _requires: Component classes that must be present next to this one.
        _clashes: Component classes that must not be present next to this one.
    """

    _custom: ClassVar[bool] = False
    _placement: ClassVar[ComponentPlacement] = ComponentPlacement.ANY
    _requires: ClassVar[ComponentClasses] = ()
    _clashes: ClassVar[ComponentClasses] = ()

    identifier: ClassVar[Identifier]

    def __init_subclass__(cls) -> None:
        if cls._abstract or "__dataclass_params__" in cls.__dict__:
            return
        identifier = getattr(cls, "identifier", None)
        if not isinstance(identifier, str):
            raise TypeError(
                f"{cls.__name__} must set `identifier`, or be declared with abstract=True."
            )
        cls.identifier = Identifier.parse(
            identifier, vanilla=not cls._custom, object_type=cls.__name__
        )

    def __json__(self) -> JsonExport:
        """The component as `{identifier: payload}`."""
        return {self.identifier: JsonObject.__json__(self)}


class JsonValueComponent(JsonComponent, abstract=True):
    """A component written as `{identifier: value}`, the value of its only JSON field, rather
    than as `{identifier: {...}}`.
    """

    def __json__(self) -> JsonExport:
        exported = JsonComponent.__json__(self)
        return {self.identifier: only_value(self, exported[self.identifier])}
