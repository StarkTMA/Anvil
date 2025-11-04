import os

from anvil.api.actors._component_group import _Components
from anvil.api.actors.actors import Attachable
from anvil.lib.config import CONFIG
from anvil.lib.enums import ItemCategory, ItemGroups
from anvil.lib.reports import ReportType
from anvil.lib.schemas import (
    AddonObject,
    ItemDescriptor,
    JsonSchemes,
    MinecraftDescription,
)
from anvil.lib.translator import AnvilTranslator

__all__ = ["Item"]


# Items
class _ItemServerDescription(MinecraftDescription):
    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._description["description"].update({"properties": {}, "menu_category": {}})

    def menu_category(
        self,
        category: ItemCategory = ItemCategory.none,
        group: ItemGroups | str = ItemGroups.none,
        is_hidden_in_commands: bool = False,
    ):
        """Sets the menu category for the item.

        Parameters:
            category (ItemCategory, optional): The category of the item. Defaults to ItemCategory.none.
            group (str, optional): The group of the item. Defaults to None.
            is_hidden_in_commands (bool, optional): Whether the item is hidden in commands. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/itemreference/examples/itemdefinition?view=minecraft-bedrock-stable

        """
        self._description["description"]["menu_category"] = {
            "category": category.value if not category == ItemCategory.none else {},
            "group": group.value if not group == ItemGroups.none else {},
            "is_hidden_in_commands": (
                is_hidden_in_commands if is_hidden_in_commands else {}
            ),
        }
        return self

    def _export(self):
        return super()._export()


class _ItemServer(AddonObject):
    _extension = ".item.json"
    _path = os.path.join(CONFIG.BP_PATH, "items")
    _object_type = "Item Server"

    def __init__(self, name: str, is_vanilla: bool) -> None:
        super().__init__(name)
        self._server_item = JsonSchemes.server_item()
        self._description = _ItemServerDescription(name, is_vanilla)
        self._components = _Components()

    @property
    def description(self):
        return self._description

    @property
    def components(self):
        return self._components

    def queue(self):
        from anvil.api.items.components import ItemDisplayName

        self._server_item["minecraft:item"].update(self.description._export())
        self._server_item["minecraft:item"]["components"].update(
            self._components._export()["components"]
        )

        if not self._components._has(ItemDisplayName):
            self._server_item["minecraft:item"]["components"][
                ItemDisplayName._identifier
            ] = {"value": f"item.{self.identifier}.name"}

            AnvilTranslator().add_localization_entry(
                f"item.{self.identifier}.name",
                self._display_name,
            )

        self.content(self._server_item)

        super().queue()


class Item(ItemDescriptor):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name, is_vanilla)
        self.server = _ItemServer(name, is_vanilla)
        self._attachable = None

    @property
    def attachable(self):
        if not self._attachable:
            self._attachable = Attachable(self.name)

        return self._attachable

    def queue(self):
        self.server.queue()
        if self._attachable:
            self._attachable.queue()

        display_name = self.server._server_item["minecraft:item"]["components"][
            "minecraft:display_name"
        ]["value"]

        CONFIG.Report.add_report(
            ReportType.ITEM,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
        )
