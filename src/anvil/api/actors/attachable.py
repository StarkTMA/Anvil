from anvil.api.actors.description import _ActorClientDescription
from anvil.lib.config import CONFIG, Pack
from anvil.lib.reports import ReportType
from anvil.lib.schemas import (
    AddonObject,
    JsonSchemes,
)

__all__ = ["Attachable"]


class _AttachableClientDescription(_ActorClientDescription):
    """Base class for all client attachable descriptions."""

    _type = "attachable"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client attachable descriptions.

        Args:
            name (str): The name of the attachable.
            is_vanilla (bool, optional): Whether or not the attachable is a vanilla attachable. Defaults to False.
        """
        super().__init__(name, is_vanilla)


class Attachable(AddonObject):
    _extension = ".attachable.json"
    _pack = Pack.RP
    _folder = "attachables"
    _object_type = "Attachable"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes the attachable.

        Args:
            name (str): The name of the attachable.
        """
        super().__init__(name, is_vanilla)

        self._attachable = JsonSchemes.attachable()
        self._description = _AttachableClientDescription(self.identifier, False)

    @property
    def description(self) -> "_AttachableClientDescription":
        """Returns the description of the attachable."""
        return self._description

    def queue(self) -> "Attachable":
        """Queues the attachable."""

        self._attachable["minecraft:attachable"].update(self._description.__export__())
        self.content(self._attachable)

        CONFIG.Report.add_report(
            ReportType.ATTACHABLE,
            vanilla=self._is_vanilla,
            col0=self._display_name,
            col1=self.identifier,
        )
        super().queue()

    def __str__(self):
        """Returns the identifier of the attachable."""
        return self.identifier
