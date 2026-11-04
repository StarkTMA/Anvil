"""The resource pack's `attachables/<item>.attachable.json`: the item client, how an item
renders when an entity holds or wears it."""

from typing import ClassVar

from anvil.api.actors.client import _ActorClientDescription
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import ENTITY_CLIENT_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, json_field
from anvil.lib.reports import ReportType

__all__ = ["ItemClient"]


class _ItemClientDescription(_ActorClientDescription):
    """The `description` of an item's attachable, and its builders. Unset keys are left out."""

    _type = "attachable"


class _Attachable(JsonObject):
    """The `minecraft:attachable` body."""

    description: _ItemClientDescription = json_field(
        default_factory=_ItemClientDescription
    )


class _AttachableFile(JsonObject):
    """The content of an `.attachable.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:attachable")

    format_version: str = json_field(default=ENTITY_CLIENT_VERSION, init=False)
    attachable: _Attachable = json_field(
        default_factory=_Attachable, key="minecraft:attachable"
    )


class ItemClient(JsonFile):
    """The item client: its attachable, how the item renders when an entity holds or wears
    it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/attachables)
    """

    _document = _AttachableFile
    _extension = ".attachable.json"
    _pack = Pack.RP
    _folder = "attachables"
    _object_type = "Attachable"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates an item client.

        Args:
            name (str): The item's name.
            is_vanilla (bool, optional): If the item is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _ItemClientDescription:
        """The description builders."""
        return self._content.attachable.description

    def queue(self) -> "ItemClient":
        """Queues the item client for export."""
        CONFIG.Report.add_report(
            ReportType.ATTACHABLE,
            vanilla=self.identifier.is_vanilla,
            col0=self.identifier.display_name,
            col1=self.identifier,
        )
        return super().queue()

    def __export__(self) -> None:
        self.description.__prepare_export__(self)
        return super().__export__()

    def __str__(self) -> str:
        return self.identifier
