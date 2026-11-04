"""`JsonContainer`: a named group of `JsonComponent`s, written under its name as one JSON object
keyed by each component's identifier, and `validate_components`, which checks the components of an owner
against each one's placement, requirements and clashes.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Annotated, Any, Self

from .component import ComponentPlacement, JsonComponent
from .fields import json_field
from .jsontypes import Merged
from .object import JsonObject


def validate_components(
    owner: Any,
    root: JsonContainer,
    groups: list[JsonContainer],
    *,
    is_block: bool = False,
) -> None:
    """Checks where each component is placed, and the components each one requires or clashes
    with. A component in a group may rely on one in the root.

    Raises:
        ValueError: A component is misplaced, misses a component it requires, or clashes.
    """
    groups_name = "permutations" if is_block else "component groups"

    def check(
        components: list[JsonComponent], present: list[JsonComponent], where: str
    ) -> None:
        identifiers = {component.identifier for component in components}
        available = identifiers | {component.identifier for component in present}
        for component in components:
            cls = type(component)
            for clash in cls._clashes:
                if clash.identifier in identifiers:
                    raise ValueError(
                        f"Component '{component.identifier}' clashes with "
                        f"'{clash.identifier}'. Remove one of them. "
                        f"Found in {where} of '{owner.identifier}'."
                    )
            for requirement in cls._requires:
                if requirement.identifier not in available:
                    raise ValueError(
                        f"Component '{component.identifier}' requires "
                        f"'{requirement.identifier}'. Add it. "
                        f"Found in {where} of '{owner.identifier}'."
                    )

    for component in root._components:
        if ComponentPlacement.ROOT not in type(component)._placement:
            raise ValueError(
                f"Component '{component.identifier}' is not allowed in the root components. "
                f"Found in '{owner.identifier}'."
            )
    check(root._components, [], root._where())

    for group in groups:
        where = group._where()
        for component in group._components:
            if ComponentPlacement.GROUP not in type(component)._placement:
                raise ValueError(
                    f"Component '{component.identifier}' is not allowed in {groups_name}. "
                    f"Found in {where} of '{owner.identifier}'."
                )
        check(group._components, root._components, where)


class JsonContainer(JsonObject):
    """A group of components, written under its name as one JSON object keyed by each
    component's identifier: `{"components": {...}}` for the root, `{"adult": {...}}` for a
    group. The owner merges it into its own object. The root components of an entity, block, item or biome are the container named
    `components`; any other name is an entity component group, added and removed by events.

    Args:
        name (str): The group name: `components` for the root, or the key under `component_groups`.
    """

    _components: Annotated[list[JsonComponent], Merged()] = json_field(
        default_factory=list, init=False, key="components"
    )

    name: str = json_field(exclude=True)

    def add(self, *components: JsonComponent) -> Self:
        """Adds components. A component replaces the one with the same identifier, in its place.

        Args:
            *components (JsonComponent): The components to add.
        """
        for component in components:
            for index, existing in enumerate(self._components):
                if existing.identifier == component.identifier:
                    self._components[index] = component
                    break
            else:
                self._components.append(component)
        return self

    def remove(self, *components: JsonComponent | type[JsonComponent]) -> Self:
        """Removes components by identifier.

        Args:
            *components (JsonComponent | type[JsonComponent]): The components, or their classes.
        """
        identifiers = {component.identifier for component in components}
        self._components[:] = [
            component
            for component in self._components
            if component.identifier not in identifiers
        ]
        return self

    def __json__(self) -> Any:
        """The components under the container name, with any other fields beside them."""
        payload = JsonObject.__json__(self)
        return {
            self.name if key == "components" else key: value
            for key, value in payload.items()
        }

    @classmethod
    def __schema_body__(cls, definitions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        """Any components, keyed by identifier, under the container name."""
        return {"type": "object", "additionalProperties": {"type": "object"}}

    def __payload__(self) -> dict[str, Any]:
        """The components only, as one object keyed by identifier, without the container name."""
        return Merged().encode(self._components)

    def __iter__(self) -> Iterator[JsonComponent]:
        return iter(self._components)

    def _where(self) -> str:
        """Where the container is, for error messages."""
        if self.name == "components":
            return "the root components"
        return f"the component group '{self.name}'"

    def has(self, component: JsonComponent | type[JsonComponent]) -> bool:
        """Whether a component with the same identifier is present.

        Args:
            component (JsonComponent | type[JsonComponent]): The component, or its class.
        """
        identifier = component.identifier
        return any(existing.identifier == identifier for existing in self._components)
