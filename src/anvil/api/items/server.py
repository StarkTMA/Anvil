from anvil.api.core.components import ComponentGroup
from anvil.api.core.enums import ItemCategory, ItemGroups
from anvil.api.items.components import ItemDisplayName
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import encoders, validate_components
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription

__all__ = ["ItemServer"]


class _ItemServerDescription(MinecraftDescription):
    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._description["description"].update({"properties": {}, "menu_category": {}})

    def menu_category(
        self,
        category: ItemCategory,
        group: ItemGroups | None = None,
        is_hidden_in_commands: bool = False,
    ) -> "_ItemServerDescription":
        """Sets the menu category for the item.

        Parameters:
            category (ItemCategory, optional): The category of the item. Defaults to ItemCategory.none.
            group (str, optional): The group of the item. Defaults to None.
            is_hidden_in_commands (bool, optional): Whether the item is hidden in commands. Defaults to False.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemdefinition)

        """
        self._description["description"]["menu_category"]["category"] = category
        self._description["description"]["menu_category"]["group"] = group
        self._description["description"]["menu_category"]["is_hidden_in_commands"] = (
            is_hidden_in_commands if is_hidden_in_commands else {}
        )
        return self

    def __export__(self) -> dict:
        return super().__export__()


class ItemServer(AddonObject):
    _extension = ".item.json"
    _pack = Pack.BP
    _folder = "items"
    _object_type = "Item Server"

    def __init__(self, name: str, is_vanilla: bool) -> None:
        super().__init__(name)
        self._server_item = JsonSchemes.server_item()
        self._description = _ItemServerDescription(name, is_vanilla)
        self._components = ComponentGroup(name="components")

    @property
    def description(self) -> "_ItemServerDescription":
        return self._description

    @property
    def components(self) -> "ComponentGroup":
        return self._components

    def __export__(self) -> None:
        if not list(self._components):
            raise ValueError(
                f"Item '{self.name}' must have at least one component defined."
            )

        validate_components(self, self._components, [])

        if not any(isinstance(c, ItemDisplayName) for c in self._components):
            self._components.add(ItemDisplayName(value=self._display_name))
        for component in self._components:
            component.__prepare_export__(self)

        self._server_item["minecraft:item"].update(self.description.__export__())
        self._server_item["minecraft:item"]["components"].update(
            encoders.contents(self._components)
        )

        self.content(self._server_item)
        super().__export__()
