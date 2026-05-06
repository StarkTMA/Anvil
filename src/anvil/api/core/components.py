from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List
from warnings import deprecated


from anvil.api.core.enums import ComponentTarget, FilterSubject
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.lib.format_versions import *
from anvil.lib.schemas import AddonDescriptor, AddonObject
from packaging.version import Version

if TYPE_CHECKING:
    from anvil.api.blocks.blocks import BlockServer


class Component(AddonDescriptor):
    _object_type = "Base Component"
    _target: ComponentTarget = ComponentTarget.Any
    _identifier: str = "base_component"

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
        self._allowed_in_root: bool = True
        self._allowed_in_group: bool = True

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


class RootComponent:
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

    def add(self, *components: Component) -> "RootComponent":
        for component in components:
            self._components.append(component)
        return self

    def remove(self, *components: Component) -> "RootComponent":
        for component in components:
            self._remove(component)
        return self

    def __iter__(self):
        """Iterates over the components in this group."""
        return iter(self._components)

    def __export__(self) -> Dict[str, Any]:
        return {
            self._component_group_name: {
                k: v
                for component in self._components
                for k, v in component.__export__().items()
            }
        }


class ComponentGroup(RootComponent):
    """Named component group. Wraps :class:`RootComponent` with a fixed group name."""

    def __init__(self, component_group_name: str) -> None:
        super().__init__(group_name=component_group_name)


class PermutationGroup(RootComponent):
    _count = 0

    def __init__(self, condition: str | Molang = None):
        """The permutation components.

        Args:
            condition (str | Molang, optional): The condition for the permutation.
        """
        super().__init__()
        PermutationGroup._count += 1
        self._component_group_name = "components"
        self._condition = condition
        self._tags = []

    @deprecated(
        "The 'tag' method is deprecated and remains for backward compatibility to automatically convert old tags to the new system. Update your code to use 'BlockTagComponent' directly instead."
    )
    def tag(self, *tags: MinecraftBlockTags):
        """The tags for the block.

        Args:
            *tags (MinecraftBlockTags): The tags for the block.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktags
        """

        from anvil.api.blocks.components import BlockTagComponent

        self._tags.extend(tags)
        self.add(BlockTagComponent(self._tags))

        return self

    def __export__(self):
        cmp = super().__export__()
        if self._condition:
            cmp["condition"] = self._condition
        return cmp


def component_clashes(addon_object: AddonObject, components: List[Component]) -> None:
    """Checks for component clashes within a list of components.

    Args:
        components (List[Component]): The list of components to check.
    Raises:
        ValueError: If a component clashes with another component in the list.
    """
    component_classes = [
        component.__component_identifier__() for component in components
    ]
    for component in components:
        for clash in component.__component_clashes__():
            if clash.__component_identifier__() in component_classes:
                raise ValueError(
                    f"Component '{component.__component_identifier__()}' clashes with "
                    f"'{clash.__component_identifier__()}'. Remove one of the conflicting components."
                    f"Found in '{addon_object.identifier}' components."
                )


def component_dependencies(
    addon_object: AddonObject, components: List[Component]
) -> None:
    """Checks for missing component dependencies within a list of components.

    Args:
        components (List[Component]): The list of components to check.
    Raises:
        ValueError: If a component has a missing dependency in the list.
    """
    component_classes = [
        component.__component_identifier__() for component in components
    ]
    for component in components:
        for dependency in component.__component_dependencies__():
            if dependency.__component_identifier__() not in component_classes:
                print(dependency.__component_identifier__(), component_classes)
                raise ValueError(
                    f"Component '{component.__component_identifier__()}' requires missing dependency "
                    f"'{dependency.__component_identifier__()}'. Add the missing dependency."
                    f"Found in '{addon_object.identifier}' components."
                )


def components_validations(
    addon_object: AddonObject,
    root_components: RootComponent,
    group_components: List[RootComponent | PermutationGroup],
    is_block: bool = False,
) -> None:
    groups_name = "permutations" if is_block else "component groups"

    component_clashes(addon_object, list(root_components))
    component_dependencies(addon_object, list(root_components))

    for component in root_components:
        if not component._allowed_in_root:
            raise ValueError(
                f"Component '{component.__component_identifier__()}' is not allowed in root components. Found in '{addon_object.identifier}' root components."
            )

    for group in group_components:
        component_clashes(addon_object, list(group))
        component_dependencies(addon_object, list(group))

        for comp in group:
            if not comp._allowed_in_group:
                raise ValueError(
                    f"Component '{comp.__component_identifier__()}' is not allowed in {groups_name}. Found in group '{group._component_group_name}' of '{addon_object.identifier}'."
                )


def component_block_visuals(
    block: BlockServer,
    root_components: RootComponent,
    group_components: List[PermutationGroup],
):
    from anvil.api.blocks.components import (
        BlockGeometry,
        BlockMaterialInstance,
    )

    components = [component.__component_identifier__() for component in root_components]

    if not BlockGeometry.__component_identifier__() in components:
        raise RuntimeError(
            f"Block {block.identifier} missing at least one geometry in the root components. Block [{block.identifier}]"
        )

    if not BlockMaterialInstance.__component_identifier__() in components:
        raise RuntimeError(
            f"Block {block.identifier} missing at least one material instance in the root components. Block [{block.identifier}]"
        )
