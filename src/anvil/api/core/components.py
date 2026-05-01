from __future__ import annotations

from typing import Any, Dict, List

from anvil.api.core.enums import ComponentTarget, FilterSubject
from anvil.api.core.filters import Filter
from anvil.lib.format_versions import *
from anvil.lib.schemas import AddonDescriptor
from packaging.version import Version


class Component(AddonDescriptor):
    _object_type = "Base Component"
    _target: ComponentTarget = ComponentTarget.Any
    _identifier: str = "base_component"

    def _require_components(self, *components: "Component") -> None:
        self._dependencies.extend(components)

    def _add_clashes(self, *components: "Component") -> None:
        self._clashes.extend(components)

    def _enforce_version(self, current: str, minimum: str) -> None:
        if Version(current) < Version(minimum):
            raise ValueError(f"{self.identifier} requires ≥ {minimum} (got {current}).")

    def _add_field(self, key: str, value: Any) -> None:
        self._component[key] = value

    def _add_field_if_not_default(self, key: str, value: Any, default: Any) -> None:
        if value != default:
            self._component[key] = value

    def _set_value(self, value: Dict[str, Any]) -> None:
        self._component = value

    def _get_field(self, key: str, default: Any) -> Any:
        return self._component.get(key, default)

    def _add_dict(self, value: Dict[str, Any]) -> None:
        self._component.update(value)

    def __init__(self, component_name: str, is_vanilla: bool = True) -> None:
        super().__init__(component_name, is_vanilla, True)
        self._dependencies: List["Component"] = []
        self._clashes: List["Component"] = []
        self._component: Dict[str, Any] = {}

    def __iter__(self):
        """Iterates over the component's fields."""
        return iter({self.identifier: self._component}.items())

    def __export__(self) -> Dict[str, Any]:
        """Exports the component as a dictionary.

        Returns:
            dict: The exported component.
        """
        return {self.identifier: self._component}

    @classmethod
    def __component_identifier__(cls) -> str:
        return cls._identifier

    def __component_dependencies__(self) -> List["Component"]:
        return self._dependencies

    def __component_clashes__(self) -> List["Component"]:
        return self._clashes


class AIGoal(Component):
    def __init__(self, component_name: str) -> None:
        super().__init__(component_name)

    def priority(self, priority: int):
        """The higher the priority, the sooner this behavior will be executed as a goal.

        Parameters:
            priority (int): The higher the priority, the sooner this behavior will be executed as a goal.
        """
        self._add_field("priority", priority)
        return self


class EventTrigger(Component):
    _identifier = "minecraft:on_event"

    def __init__(
        self,
        event: str,
        filters: Filter | None = None,
        target: FilterSubject = FilterSubject.Self,
    ):
        super().__init__(self._identifier)
        self._add_dict(
            {
                "event": event,
                "filters": filters if filters is not None else {},
                "target": target.value,
            }
        )
        return self


class _Components:
    """Container for a named group of :class:`Component` instances.

    The *group_name* parameter determines the top-level key in the exported
    dict.  Pass ``"components"`` (the default) for a normal entity components
    block, or any other string to produce a named component group.
    """

    def __init__(self, group_name: str = "components") -> None:
        self._component_group_name = group_name
        self._components: List[Component] = []

    def _set(self, component: Component) -> None:
        self.remove(component)
        self.add(component)

    def _remove(self, component: Component) -> None:
        if self._has(component):
            self._components.remove(component)

    def _has(self, component: Component) -> bool:
        """Return True if a component with the same identifier is already present."""
        return component.__component_identifier__() in self._components_list()

    def _components_list(self) -> List[str]:
        return [cmp.identifier for cmp in self._components]

    def add(self, *components: Component) -> "_Components":
        for component in components:
            self._components.append(component)
        return self

    def remove(self, *components: Component) -> "_Components":
        for component in components:
            self._remove(component)
        return self

    def __export__(self) -> Dict[str, Any]:
        component_classes = {
            component.__component_identifier__() for component in self._components
        }

        cmp_dict: Dict[str, Any] = {}
        for component in self._components:
            missing_dependencies = [
                dep.__component_identifier__()
                for dep in component.__component_dependencies__()
                if dep.__component_identifier__() not in component_classes
            ]
            conflicting = [
                cla.__component_identifier__()
                for cla in component.__component_clashes__()
                if cla.__component_identifier__() in component_classes
            ]

            if missing_dependencies:
                raise RuntimeError(
                    f"Component '{component.__class__.__name__}' requires missing dependency "
                    f"{missing_dependencies} in '{self._component_group_name}' group."
                )

            if conflicting:
                raise RuntimeError(
                    f"Component '{component.__class__.__name__}' conflicts with "
                    f"{conflicting} in '{self._component_group_name}' group. Remove the conflicting component(s)."
                )

            cmp_dict.update(component.__export__())
        return {self._component_group_name: cmp_dict}


class ComponentGroup(_Components):
    """Named component group. Wraps :class:`_Components` with a fixed group name."""

    def __init__(self, component_group_name: str) -> None:
        super().__init__(group_name=component_group_name)
