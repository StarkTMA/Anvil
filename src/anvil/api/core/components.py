from __future__ import annotations

from typing import Any, Dict, List

from anvil.lib.enums import ComponentTarget, FilterSubject
from anvil.api.core.filters import Filter
from anvil.lib.format_versions import *
from anvil.lib.schemas import AddonDescriptor
from anvil.lib.types import Event
from packaging.version import Version


class _BaseComponent(AddonDescriptor):
    _object_type = "Base Component"
    _target: ComponentTarget = ComponentTarget.Any
    _identifier: str = "base_component"

    def _require_components(self, *components: "_BaseComponent") -> None:
        self._dependencies.extend(components)

    def _add_clashes(self, *components: "_BaseComponent") -> None:
        self._clashes.extend(components)

    def _enforce_version(self, current: str, minimum: str) -> None:
        if Version(current) < Version(minimum):
            raise ValueError(f"{self.identifier} requires ≥ {minimum} (got {current}).")

    def _add_field(self, key: str, value: Any) -> None:
        self._component[key] = value

    def _set_value(self, value: Dict[str, Any]) -> None:
        self._component = value

    def _get_field(self, key: str, default: Any) -> Any:
        return self._component.get(key, default)

    def _add_dict(self, value: Dict[str, Any]) -> None:
        self._component.update(value)

    def __init__(self, component_name, is_vanilla: bool = True) -> None:
        super().__init__(component_name, is_vanilla, True)
        self._dependencies: List["_BaseComponent"] = []
        self._clashes: List["_BaseComponent"] = []
        self._component: Dict[str, Any] = {}

    def __iter__(self):
        """Iterates over the component's fields."""
        return iter({self.identifier: self._component}.items())

    def _export(self) -> Dict[str, Any]:
        """Exports the component as a dictionary.

        Returns:
            dict: The exported component.
        """
        return {self.identifier: self._component}


class _BaseAIGoal(_BaseComponent):
    def __init__(self, component_name: str) -> None:
        super().__init__(component_name)

    def priority(self, priority: int):
        """The higher the priority, the sooner this behavior will be executed as a goal.

        Parameters:
            priority (int): The higher the priority, the sooner this behavior will be executed as a goal.
        """
        self._add_field("priority", priority)
        return self


class _BaseEventTrigger(_BaseComponent):
    _identifier = "minecraft:on_event"

    def __init__(
        self,
        event: Event,
        filters: Filter = None,
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
