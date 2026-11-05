"""The behavior pack's `biomes/<biome>.biome.json`: a server biome, its description and
components."""

from typing import Annotated, Any, ClassVar

from anvil.api.biomes.components import BiomeClientComponent
from anvil.api.biomes.description import _BiomeDescription
from anvil.api.core.components import ComponentGroup
from anvil.lib.config import Pack
from anvil.lib.format_versions import BIOME_SERVER_VERSION
from anvil.lib.jsonmodel import (
    Encoded,
    JsonFile,
    JsonObject,
    json_field,
    validate_components,
)

__all__ = ["BiomeServer"]


# region Parts


def _components(group: ComponentGroup) -> Any:
    return group.__payload__()


class _BiomeServer(JsonObject):
    """The `minecraft:biome` body."""

    description: _BiomeDescription = json_field(default_factory=_BiomeDescription)
    components: Annotated[ComponentGroup, Encoded(_components, {"type": "object"})] = (
        json_field(default_factory=lambda: ComponentGroup(name="components"))
    )


class _BiomeServerFile(JsonObject):
    """The content of a `.biome.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:biome")

    format_version: str = json_field(default=BIOME_SERVER_VERSION, init=False)
    biome: _BiomeServer = json_field(
        default_factory=_BiomeServer, key="minecraft:biome"
    )


# endregion


class BiomeServer(JsonFile[_BiomeServerFile]):
    """A server biome: its description and the components that generate it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/biomesreference/)
    """

    _extension = ".biome.json"
    _pack = Pack.BP
    _folder = "biomes"
    _object_type = "Biomes Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a server biome. Add the biome components from
        `anvil.api.biomes.components` to `components`.

        Args:
            name (str): The biome's name.
            is_vanilla (bool, optional): If the biome is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _BiomeDescription:
        """The biome description."""
        return self._document.biome.description

    @property
    def components(self) -> ComponentGroup:
        """The biome components."""
        return self._document.biome.components

    def __export__(self) -> None:
        """Checks the components before the file is written.

        Raises:
            ValueError: A client biome component was added to the server biome.
        """
        for component in self.components:
            if isinstance(component, BiomeClientComponent):
                raise ValueError(
                    f"{type(component).__name__} is a client biome component. "
                    f"Add it to the biome client instead. {self._object_type}[{self.identifier}]"
                )
        validate_components(self, self.components, [])
        return super().__export__()
