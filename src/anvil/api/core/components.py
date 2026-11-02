from __future__ import annotations

from typing import Annotated, ClassVar

from anvil.api.core.enums import ControlFlags, FilterSubject, ItemCategory
from anvil.api.core.filters import Filter
from anvil.api.logic.molang import Molang
from anvil.lib.jsonmodel import (
    JsonComponent,
    JsonContainer,
    JsonObject,
    NonNegative,
    json_field,
)


class AIGoal(JsonComponent, abstract=True):
    """Base of the AI goals (`minecraft:behavior.*`).

    Args:
        priority (int, optional): Lower values run first. Game default 0.
        control_flags (list[ControlFlags], optional): The controls this goal takes over while it runs.
    """

    priority: Annotated[int, NonNegative] | None = json_field(default=None)
    control_flags: list[ControlFlags] | None = json_field(default=None)


class EventTrigger(JsonObject):
    """An event to run, the entity it runs on, and the conditions for it to run.

    Args:
        event (str): The event to run.
        filters (Filter, optional): The conditions for the event to run.
        target (FilterSubject, optional): The entity the event runs on. Game default self.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/entityreference/examples/definitions/nestedtables/triggers)
    """

    event: str = json_field()
    filters: Filter | None = json_field(default=None)
    target: FilterSubject | None = json_field(default=None)


class MenuCategory(JsonObject):
    """Where a block or item appears in the creative inventory and the crafting book.

    Args:
        category (ItemCategory): The tab. Without a menu category the block or item is hidden.
        group (ItemGroups | str, optional): The expandable group in the tab, as its group key.
        is_hidden_in_commands (bool, optional): Hides it from commands such as /give. Game default False.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockdescription)
    """

    category: ItemCategory = json_field()
    group: str | None = json_field(default=None)
    is_hidden_in_commands: bool | None = json_field(default=None)


# region Containers


class ComponentGroup(JsonContainer):
    """The components of an entity, block, item or biome. The root components are the group
    named `components`; any other name is an entity component group, added and removed by events.

    Args:
        name (str): The group name: `components` for the root, or the key under `component_groups`.
        components (list[JsonComponent], optional): The components. Add more with `add`.
    """


class Permutation(JsonContainer):
    """Block components that apply while a condition is true.

    Args:
        condition (Molang | str): The Molang condition.
        components (list[JsonComponent], optional): The components. Add more with `add`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/permutations)
    """

    _count: ClassVar[int] = 0
    """Permutations made in this run. The game allows 10000 across all blocks."""

    name: str = json_field(default="components", init=False, exclude=True)
    condition: Molang | str = json_field()

    def __post_init__(self) -> None:
        Permutation._count += 1

    def _where(self) -> str:
        return f"the permutation '{self.condition}'"


# endregion
