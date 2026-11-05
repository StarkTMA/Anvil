from typing import TYPE_CHECKING

from anvil.api.core.core import ANVIL
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import Identifier
from anvil.lib.reports import ReportType
from anvil.lib.translator import AnvilTranslator

if TYPE_CHECKING:
    from anvil.api.items.client import ItemClient

__all__ = ["Item"]


class Item:
    _object_type = "Item"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates an item: its server and client files share one identifier.

        Args:
            name (str): The item's name, with or without its namespace.
            is_vanilla (bool, optional): If the item is a vanilla one. Defaults to False.

        Raises:
            ValueError: When the name is not valid (see `Identifier.parse`), or a vanilla
                item is not in `MinecraftItemTypes`.
        """
        from anvil.api.items.server import ItemServer
        from anvil.api.vanilla.items import vanilla_items_ids

        self.identifier = Identifier.parse(
            name, vanilla=is_vanilla, object_type=self._object_type
        )
        if self.identifier.is_vanilla and self.identifier not in vanilla_items_ids():
            raise ValueError(
                f"Invalid vanilla item '{self.identifier}'. Please use a valid vanilla "
                f"item from MinecraftItemTypes. Item [{self.identifier}]"
            )
        self.server = ItemServer(self.identifier, self.identifier.is_vanilla)
        self._client: ItemClient | None = None

    @property
    def name(self) -> str:
        """The item's name, without its namespace."""
        return self.identifier.name

    def __str__(self) -> str:
        return self.identifier

    @property
    def client(self) -> ItemClient:
        """The item client (its attachable), created the first time it is used."""
        from anvil.api.items.client import ItemClient

        if self._client is None:
            self._client = ItemClient(self.identifier, self.identifier.is_vanilla)
        return self._client

    def queue(self) -> "Item":
        """Queues the item's files to be exported."""
        self.server.queue()
        if self._client is not None:
            self._client.queue()
        ANVIL.__queue__(self)
        return self

    def __export__(self) -> None:
        from anvil.api.items.components import ItemDisplayName

        display_name = next(
            component.value
            for component in self.server.components
            if isinstance(component, ItemDisplayName)
        )
        if display_name.startswith("item."):
            display_name = AnvilTranslator().get_localization_value(display_name)

        CONFIG.Report.add_report(
            ReportType.ITEM,
            vanilla=self.identifier.is_vanilla,
            col0=display_name,
            col1=self.identifier,
        )
