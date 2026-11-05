"""The behavior pack's `items/<item>.item.json`: a server item, its description and
components."""

from typing import Annotated, Any, ClassVar

from anvil.api.core.components import ComponentGroup
from anvil.api.items.components import ItemDisplayName
from anvil.lib.config import Pack
from anvil.lib.format_versions import ITEM_SERVER_VERSION
from anvil.lib.jsonmodel import (
    Encoded,
    Identifier,
    JsonFile,
    JsonObject,
    json_field,
    validate_components,
)
from anvil.lib.jsonmodel.enums import ItemCategory, ItemGroups

__all__ = ["ItemServer"]


# region Parts


def _components(group: ComponentGroup) -> Any:
    return group.__payload__()


class _ItemMenuCategory(JsonObject):
    """Where the item is in the creative inventory."""

    category: ItemCategory = json_field()
    group: ItemGroups | str | None = None
    is_hidden_in_commands: bool | None = None


class _ItemServerDescription(JsonObject):
    """The `description` of a server item: its identifier and menu category.

    ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemdefinition)
    """

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: Identifier | None = None
    menu_category: _ItemMenuCategory | None = None

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the identifier, already parsed by the file."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The description has no identifier.")

    def set_menu_category(
        self,
        category: ItemCategory,
        group: ItemGroups | str | None = None,
        is_hidden_in_commands: bool = False,
    ) -> "_ItemServerDescription":
        """Puts the item in the creative inventory.

        Args:
            category (ItemCategory): The creative tab.
            group (ItemGroups | str, optional): The group inside the tab, a vanilla one or
                a `tag.<namespace>:<name>` key from the crafting item catalog.
            is_hidden_in_commands (bool, optional): Hides the item from commands. Defaults
                to False.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemdefinition)
        """
        self.menu_category = _ItemMenuCategory(
            category=category,
            group=group,
            is_hidden_in_commands=True if is_hidden_in_commands else None,
        )
        return self


class _ItemServer(JsonObject):
    """The `minecraft:item` body."""

    description: _ItemServerDescription = json_field(
        default_factory=_ItemServerDescription
    )
    components: Annotated[ComponentGroup, Encoded(_components, {"type": "object"})] = (
        json_field(default_factory=lambda: ComponentGroup(name="components"))
    )


class _ItemServerFile(JsonObject):
    """The content of an `.item.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:item")

    format_version: str = json_field(default=ITEM_SERVER_VERSION, init=False)
    item: _ItemServer = json_field(default_factory=_ItemServer, key="minecraft:item")


# endregion


class ItemServer(JsonFile[_ItemServerFile]):
    """A server item: its description and components.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/itemreference/)
    """

    _extension = ".item.json"
    _pack = Pack.BP
    _folder = "items"
    _object_type = "Item Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a server item. Add the item components from
        `anvil.api.items.components` to `components`.

        Args:
            name (str): The item's name.
            is_vanilla (bool, optional): If the item is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _ItemServerDescription:
        """The description builders, such as `set_menu_category`."""
        return self._document.item.description

    @property
    def components(self) -> ComponentGroup:
        """The item components."""
        return self._document.item.components

    def __export__(self) -> None:
        """Gives the item a display name when it has none and checks the components before
        the file is written.

        Raises:
            ValueError: The item has no components, or a component is misplaced, misses one
                it requires, or clashes.
        """
        if not list(self.components):
            raise ValueError(
                f"Item '{self.name}' must have at least one component defined."
            )
        validate_components(self, self.components, [])
        if not any(isinstance(c, ItemDisplayName) for c in self.components):
            self.components.add(ItemDisplayName(value=self.identifier.display_name))
        for component in self.components:
            component.__prepare_export__(self)
        return super().__export__()
