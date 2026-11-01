from anvil.api.biomes.components import BiomeClientComponent
from anvil.api.core.components import ComponentGroup
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import encoders, validate_components
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription

__all__ = ["BiomeDescription", "BiomeServer"]


class BiomeDescription(MinecraftDescription):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The biome description.

        Args:
            name (str): The name of the biome.
            is_vanilla (bool, optional): Whether or not the biome is a vanilla biome. Defaults to False.
        """
        super().__init__(name, is_vanilla)


class BiomeServer(AddonObject):
    """The biome server object."""

    _extension = ".biome.json"
    _pack = Pack.BP
    _folder = "biomes"
    _object_type = "Biomes Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The biome server object. Add the biome components from
        `anvil.api.biomes.components` to `components`.

        Args:
            name (str): The name of the biome.
            is_vanilla (bool, optional): Whether or not the biome is a vanilla biome. Defaults to False.
        """
        super().__init__(name)
        self.content(JsonSchemes.biome_server())
        self._description = BiomeDescription(name, is_vanilla)
        self._components = ComponentGroup(name="components")

    @property
    def description(self) -> BiomeDescription:
        """The biome description."""
        return self._description

    @property
    def components(self) -> ComponentGroup:
        """The biome components."""
        return self._components

    def queue(self) -> "BiomeServer":
        """Queues the biome to be exported.

        Raises:
            ValueError: A client biome component was added to the server biome.
        """
        for component in self._components:
            if isinstance(component, BiomeClientComponent):
                raise ValueError(
                    f"{type(component).__name__} is a client biome component. "
                    f"Add it to the biome client instead. {self._object_type}[{self._name}]"
                )
        validate_components(self, self._components, [])
        self._content["minecraft:biome"].update(self.description.__export__())
        self._content["minecraft:biome"]["components"] = encoders.contents(
            self._components
        )

        self.content(self._content)
        super().queue()
