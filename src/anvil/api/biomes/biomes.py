from anvil.api.biomes.client import BiomeClient
from anvil.api.biomes.server import BiomeServer
from anvil.lib.config import CONFIG, ConfigPackageTarget
from anvil.lib.reports import ReportType
from anvil.lib.schemas import MinecraftBiomeDescriptor

__all__ = ["Biome"]


class Biome(MinecraftBiomeDescriptor):
    _object_type = "Biome"

    def __init__(self, name, is_vanilla=False) -> None:
        if CONFIG._TARGET == ConfigPackageTarget.ADDON and is_vanilla:
            raise RuntimeError(
                "Vanilla biomes overrides cannot be used in addons, use Partial overrides instead."
            )

        super().__init__(name, is_vanilla)

        self._server = None
        self._client = None

    @property
    def server(self) -> BiomeServer:
        if self._server is None:
            self._server = BiomeServer(self.identifier, self._is_vanilla)
        return self._server

    @property
    def client(self) -> BiomeClient:
        if self._client is None:
            self._client = BiomeClient(self.identifier, self._is_vanilla)
        return self._client

    def queue(self) -> None:
        """Queues the biome to be exported."""
        if self._server:
            self.server.queue()

        if self._client:
            self.client.queue()

        CONFIG.Report.add_report(
            ReportType.BIOME,
            vanilla=self._is_vanilla,
            col0=self._display_name,
            col1=self.identifier,
        )
