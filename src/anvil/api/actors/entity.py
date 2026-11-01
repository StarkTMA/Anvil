from anvil.api.actors.client import EntityClient
from anvil.api.actors.server import EntityServer
from anvil.api.core.core import ANVIL
from anvil.lib.config import CONFIG
from anvil.lib.reports import ReportType
from anvil.lib.schemas import (
    MinecraftEntityDescriptor,
)
from anvil.lib.translator import AnvilTranslator

__all__ = ["Entity"]


class Entity(MinecraftEntityDescriptor):
    def __init__(self, name, is_vanilla=False, allow_runtime=True) -> None:
        super().__init__(name, is_vanilla, allow_runtime)

        self.server = EntityServer(name, is_vanilla)
        self.client = EntityClient(name, is_vanilla)

    def queue(
        self,
        directory: str = None,
        display_name: str = None,
        spawn_egg_name: str = None,
    ) -> "Entity":
        self._display_name = (
            self._display_name if display_name is None else display_name
        )
        spawn_egg_name = (
            f"Spawn {self._display_name}" if spawn_egg_name is None else spawn_egg_name
        )
        if self._is_vanilla:
            directory = "vanilla"

        AnvilTranslator().add_localization_entry(
            f"entity.{self.identifier}.name", self._display_name
        )
        AnvilTranslator().add_localization_entry(
            f"entity.{self.identifier}<>.name", self._display_name
        )
        AnvilTranslator().add_localization_entry(
            f"item.spawn_egg.entity.{self.identifier}.name",
            spawn_egg_name,
        )
        self.client.queue(directory)
        self.server.queue(directory)
        ANVIL.__queue__(self)
        return self

    def __export__(self) -> None:
        CONFIG.Report.add_report(
            ReportType.ENTITY,
            vanilla=self._is_vanilla,
            col0=self._display_name,
            col1=self.identifier,
            col2=[event._event_name for event in self.server._events.values()],
            col3=[prop for prop in self.server.description._properties],
        )
