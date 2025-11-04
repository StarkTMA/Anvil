from typing import List

from anvil.api.core.components import _BaseComponent
from anvil.lib.config import CONFIG


class _Components:
    def __init__(self):
        self._component_group_name = "components"
        self._components: List[_BaseComponent] = []

    def _set(self, component: _BaseComponent):
        self.remove(component)
        self.add(component)

    def _remove(self, component: _BaseComponent):
        if self._has(component):
            self._components.remove(component)

    def _has(self, component: _BaseComponent):
        """Checks if the component is already set."""
        return component._identifier in self._components_list()

    def _components_list(self):
        return [cmp._identifier for cmp in self._components]

    def add(self, *components: _BaseComponent):
        for component in components:
            self._components.append(component)
        return self

    def remove(self, *components: _BaseComponent):
        for component in components:
            self._remove(component)
        return self

    def _export(self):
        component_classes = {component.__class__ for component in self._components}
        cmp_dict = {}
        for component in self._components:
            missing_dependencies = [
                dep.__name__
                for dep in component._dependencies
                if dep not in component_classes
            ]
            conflicting = [
                cla.__name__ for cla in component._clashes if cla in component_classes
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

            cmp_dict.update(component)
        return {self._component_group_name: cmp_dict}


class _ComponentGroup(_Components):
    def __init__(self, component_group_name: str):
        super().__init__()
        self._component_group_name = component_group_name


class _Properties:
    def __init__(self):
        self._properties = {}

    def enum(
        self, name: str, values: tuple[str], default: str, *, client_sync: bool = False
    ):
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "enum",
            "default": default,
            "values": values,
            "client_sync": client_sync,
        }
        return self

    def int(
        self,
        name: str,
        range: tuple[int, int],
        *,
        default: int = 0,
        client_sync: bool = False,
    ):
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "int",
            "default": int(default),
            "range": range,
            "client_sync": client_sync,
        }
        return self

    def float(
        self,
        name: str,
        range: tuple[float, float],
        *,
        default: float = 0,
        client_sync: bool = False,
    ):
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "float",
            "default": float(default),
            "range": [float(f) for f in range],
            "client_sync": client_sync,
        }
        return self

    def bool(self, name: str, *, default: bool = False, client_sync: bool = False):
        self._properties[f"{CONFIG.NAMESPACE}:{name}"] = {
            "type": "bool",
            "default": default,
            "client_sync": client_sync,
        }
        return self

    @property
    def _export(self):
        return self._properties
