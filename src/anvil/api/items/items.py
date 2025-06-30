import os

from anvil import ANVIL, CONFIG
from anvil.api.actors.actors import Attachable, _Components
from anvil.lib.enums import ItemCategory, ItemGroups
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription

__all__ = [
    "Item"
]


# Items
class _ItemServerDescription(MinecraftDescription):
    def __init__(self, name, is_vanilla) -> None:
        super().__init__(name, is_vanilla)
        self._description["description"]["properties"] = {}
        self._description["description"]["menu_category"] = {}

    def group(self, group: ItemGroups):
        self._description["description"]["menu_category"]["group"] = f"{CONFIG.NAMESPACE}:{group}"
        return self

    def category(self, category: ItemCategory):
        self._description["description"]["menu_category"]["category"] = str(category)
        return self

    @property
    def is_hidden_in_commands(self):
        self._description["description"]["menu_category"]["is_hidden_in_commands"] = True
        return self

    def _export(self):
        return super()._export()


class _ItemServer(AddonObject):
    _extension = ".item.json"
    _path = os.path.join(CONFIG.BP_PATH, "items")

    def __init__(self, name: str, is_vanilla: bool) -> None:
        super().__init__(name)
        self._name = name
        self._is_vanilla = is_vanilla
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
        self._server_item["minecraft:item"]["components"].update(self._components._export()["components"])

        if not ItemDisplayName.component_namespace in self._server_item["minecraft:item"]["components"]:
            display_name = self._name.replace("_", " ").title()
            self._server_item["minecraft:item"]["components"][ItemDisplayName.component_namespace] = {"value": display_name}

        self.content(self._server_item)

        super().queue()


class Item:
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        self._name = name
        self._is_vanilla = is_vanilla
        self._server = _ItemServer(name, is_vanilla)
        self._attachable = None

        self._namespace_format = "minecraft" if self._is_vanilla else CONFIG.NAMESPACE

    @property
    def Server(self):
        return self._server

    @property
    def identifier(self):
        return f"{self._namespace_format}:{self._name}"

    @property
    def name(self):
        return self._name

    @property
    def attachable(self):
        if not self._attachable:
            self._attachable = Attachable(self.name)

        return self._attachable

    def queue(self):
        self.Server.queue()
        if self._attachable:
            self._attachable.queue

        if self.Server._server_item["minecraft:item"]["components"]["minecraft:display_name"]["value"].startswith("item."):
            display_name = ANVIL.definitions._language[
                self.Server._server_item["minecraft:item"]["components"]["minecraft:display_name"]["value"]
            ]

        else:
            display_name = self.Server._server_item["minecraft:item"]["components"]["minecraft:display_name"]["value"]

        CONFIG.Report.add_report(
            ReportType.ITEM,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
        )

