from anvil.api.biomes.client import BiomeClient
from anvil.api.biomes.server import BiomeServer
from anvil.lib.config import CONFIG, ConfigPackageTarget
from anvil.lib.jsonmodel import Identifier
from anvil.lib.reports import ReportType

__all__ = ["Biome"]


class Biome:
    _object_type = "Biome"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a biome: its server and client files share one identifier.

        Args:
            name (str): The biome's name, with or without its namespace.
            is_vanilla (bool, optional): If the biome is a vanilla one. Defaults to False.

        Raises:
            ValueError: When the name is not valid (see `Identifier.parse`), or a vanilla
                biome is overridden in a package of type addon.
        """
        if CONFIG._TARGET == ConfigPackageTarget.ADDON and is_vanilla:
            raise ValueError(
                "Vanilla biome overrides are not allowed for packages of type 'addon', "
                f"use partial overrides instead. {self._object_type}[{name}]"
            )
        self.identifier = Identifier.parse(
            name, vanilla=is_vanilla, object_type=self._object_type
        )
        self._server: BiomeServer | None = None
        self._client: BiomeClient | None = None

    @property
    def name(self) -> str:
        """The biome's name, without its namespace."""
        return self.identifier.name

    def __str__(self) -> str:
        return self.identifier

    @property
    def server(self) -> BiomeServer:
        """The server biome, created on first use."""
        if self._server is None:
            self._server = BiomeServer(self.identifier, self.identifier.is_vanilla)
        return self._server

    @property
    def client(self) -> BiomeClient:
        """The client biome, created on first use."""
        if self._client is None:
            self._client = BiomeClient(self.identifier, self.identifier.is_vanilla)
        return self._client

    def queue(self) -> "Biome":
        """Queues the biome files that were used to be exported."""
        if self._server is not None:
            self._server.queue()
        if self._client is not None:
            self._client.queue()

        CONFIG.Report.add_report(
            ReportType.BIOME,
            vanilla=self.identifier.is_vanilla,
            col0=self.identifier.display_name,
            col1=self.identifier,
        )
        return self
