from anvil.api.core.core import ANVIL
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import Identifier
from anvil.lib.reports import ReportType
from anvil.lib.translator import AnvilTranslator

__all__ = ["Entity"]


class Entity:
    _object_type = "Entity"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates an entity: its server and client files share one identifier.

        Args:
            name (str): The entity's name, with or without its namespace.
            is_vanilla (bool, optional): If the entity is a vanilla one. Defaults to False.

        Raises:
            ValueError: When the name is not valid (see `Identifier.parse`).
        """
        from anvil.api.actors.client import EntityClient
        from anvil.api.actors.server import EntityServer
        from anvil.api.vanilla.entities import vanilla_entities_ids

        self.identifier = Identifier.parse(
            name, vanilla=is_vanilla, object_type=self._object_type
        )
        if self.identifier.is_vanilla and self.identifier not in vanilla_entities_ids():
            raise ValueError(
                f"Invalid vanilla entity '{self.identifier}'. Please use a valid vanilla "
                f"entity from MinecraftEntityTypes. Entity [{self.identifier}]"
            )
        self._display_name = self.identifier.display_name
        self._spawn_egg_name: str | None = None

        self.server = EntityServer(self.identifier, self.identifier.is_vanilla)
        self.client = EntityClient(self.identifier, self.identifier.is_vanilla)

    @property
    def name(self) -> str:
        """The entity's name, without its namespace."""
        return self.identifier.name

    def __str__(self) -> str:
        return self.identifier

    def set_display_name(
        self, display_name: str, spawn_egg_name: str | None = None
    ) -> "Entity":
        """Sets the names players see, localized by Anvil.

        Args:
            display_name (str): The entity's name. Defaults to its name in title case.
            spawn_egg_name (str, optional): Its spawn egg's name. Defaults to
                `Spawn <display name>`.
        """
        self._display_name = display_name
        self._spawn_egg_name = spawn_egg_name
        return self

    def queue(self, directory: str | None = None) -> "Entity":
        """Queues the entity's files to be exported.

        Args:
            directory (str, optional): The folder its files go in, under each pack's
                folder. Vanilla entities go in `vanilla`.
        """
        spawn_egg_name = self._spawn_egg_name or f"Spawn {self._display_name}"
        if self.identifier.is_vanilla:
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
            vanilla=self.identifier.is_vanilla,
            col0=self._display_name,
            col1=self.identifier,
            col2=[event.name for event in self.server.events],
            col3=[p.name for p in self.server.description.properties],
        )
