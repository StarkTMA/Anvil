from anvil.api.actors.actors import Attachable
from anvil.api.core.core import ANVIL
from anvil.api.items.components import ItemDisplayName
from anvil.api.items.server import ItemServer
from anvil.lib.config import CONFIG
from anvil.lib.reports import ReportType
from anvil.lib.schemas import MinecraftItemDescriptor
from anvil.lib.translator import AnvilTranslator

__all__ = ["Item"]


class Item(MinecraftItemDescriptor):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name, is_vanilla)
        self.server = ItemServer(name, is_vanilla)
        self._attachable = None

    @property
    def attachable(self) -> "Attachable":
        if not self._attachable:
            self._attachable = Attachable(self.name)

        return self._attachable

    def queue(self) -> "Item":
        self.server.queue()

        if self._attachable:
            self._attachable.queue()

        ANVIL.__queue__(self)
        return self

    def __export__(self) -> None:
        item_name_comp = self.server._server_item["minecraft:item"]["components"][
            ItemDisplayName.identifier
        ]["value"]

        if item_name_comp.startswith("item."):
            display_name = AnvilTranslator().get_localization_value(item_name_comp)
        else:
            display_name = item_name_comp

        CONFIG.Report.add_report(
            ReportType.ITEM,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
        )
