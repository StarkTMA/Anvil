"""The resource pack's `biomes/<biome>.client_biome.json`: a client biome, its description
and components."""

from typing import Annotated, Any, ClassVar, Literal

from anvil.api.biomes.components import (
    BiomeClientAmbientSounds,
    BiomeClientAtmosphereIdentifier,
    BiomeClientColorGradingIdentifier,
    BiomeClientComponent,
    BiomeClientCubemapIdentifier,
    BiomeClientDryFoliageColor,
    BiomeClientFogAppearance,
    BiomeClientFoliageAppearance,
    BiomeClientGrassAppearance,
    BiomeClientLightingIdentifier,
    BiomeClientMusic,
    BiomeClientPrecipitation,
    BiomeClientSkyColor,
    BiomeClientWaterAppearance,
    BiomeClientWaterIdentifier,
)
from anvil.api.biomes.description import _BiomeDescription
from anvil.api.core.components import ComponentGroup
from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.color_grading import ColorGradingSettings
from anvil.api.pbr.cubemap import CubeMapSettings
from anvil.api.pbr.fog import FogSettings
from anvil.api.pbr.lighting import LightingSettings
from anvil.api.pbr.water import WaterSettings
from anvil.api.sounds import MusicDefinition, SoundEvent
from anvil.api.sounds.sound_definitions import _SoundDescription
from anvil.lib.config import Pack
from anvil.lib.format_versions import BIOME_CLIENT_VERSION
from anvil.lib.jsonmodel import (
    Encoded,
    JsonFile,
    JsonObject,
    json_field,
    validate_components,
)
from anvil.lib.jsonmodel.enums import MusicCategory, SoundCategory
from anvil.lib.jsonmodel.types import Color

__all__ = ["BiomeClient"]


# region Parts


def _components(group: ComponentGroup) -> Any:
    return group.__payload__()


class _BiomeClient(JsonObject):
    """The `minecraft:client_biome` body."""

    description: _BiomeDescription = json_field(default_factory=_BiomeDescription)
    components: Annotated[ComponentGroup, Encoded(_components, {"type": "object"})] = (
        json_field(default_factory=lambda: ComponentGroup(name="components"))
    )


class _BiomeClientFile(JsonObject):
    """The content of a `.client_biome.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:client_biome",
    )

    format_version: str = json_field(default=BIOME_CLIENT_VERSION, init=False)
    client_biome: _BiomeClient = json_field(
        default_factory=_BiomeClient, key="minecraft:client_biome"
    )


# endregion


class BiomeClient(JsonFile):
    """A client biome: its description and the components that render it.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/)
    """

    _document = _BiomeClientFile
    _extension = ".client_biome.json"
    _pack = Pack.RP
    _folder = "biomes"
    _object_type = "Biome Client"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a client biome. Set the client biome components with the builder methods,
        or add the `BiomeClient` components from `anvil.api.biomes.components` to `components`.

        Args:
            name (str): The biome's name.
            is_vanilla (bool, optional): If the biome is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _BiomeDescription:
        """The biome description."""
        return self._content.client_biome.description

    @property
    def components(self) -> ComponentGroup:
        """The client biome components."""
        return self._content.client_biome.components

    def ambient_sounds(
        self,
        *,
        addition: str | None = None,
        loop: str | None = None,
        mood: str | None = None,
    ) -> dict[Literal["addition", "loop", "mood"], _SoundDescription]:
        """Adds `BiomeClientAmbientSounds` and registers each sound as an ambient sound event.

        Args:
            addition (str, optional): Named sound that occasionally plays at the listener position.
            loop (str, optional): Named sound that loops while the listener is inside the biome.
            mood (str, optional): Named sound that rarely plays at a nearby air block when the
                light level is low.

        Returns:
            The sound description of each sound set, keyed by `addition`, `loop` and `mood`.
        """
        self.components.add(
            BiomeClientAmbientSounds(addition=addition, loop=loop, mood=mood)
        )
        return {
            key: SoundEvent().add_individual_event(sound, SoundCategory.Ambient)
            for key, sound in (("addition", addition), ("loop", loop), ("mood", mood))
            if sound
        }

    def biome_music(
        self,
        *,
        music_definition: MusicCategory | str | None = None,
        underwater_music: MusicCategory | str | None = None,
        volume_multiplier: float | None = None,
    ) -> dict[Literal["music_definition", "underwater_music"], _SoundDescription]:
        """Adds `BiomeClientMusic` and registers each music definition.

        Args:
            music_definition (MusicCategory | str, optional): Music played in the biome.
            underwater_music (MusicCategory | str, optional): Music played underwater in the biome.
            volume_multiplier (float, optional): Applied gradually to the music volume, from 0 to 1.

        Returns:
            The sound description of each music set, keyed by `music_definition` and
            `underwater_music`.
        """
        self.components.add(
            BiomeClientMusic(
                music_definition=music_definition,
                underwater_music=underwater_music,
                volume_multiplier=volume_multiplier,
            )
        )
        return {
            key: MusicDefinition().music_definition(music)
            for key, music in (
                ("music_definition", music_definition),
                ("underwater_music", underwater_music),
            )
            if music
        }

    def atmosphere_identifier(
        self, atmosphere_identifier: "AtmosphericSettings | str"
    ) -> "BiomeClient":
        """Sets the atmospherics used in Vibrant Visuals mode.

        Args:
            atmosphere_identifier (AtmosphericSettings | str): The atmospherics definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_atmosphere_identifier)
        """
        self.components.add(
            BiomeClientAtmosphereIdentifier(atmosphere_identifier=atmosphere_identifier)
        )
        return self

    def color_grading_identifier(
        self, color_grading_identifier: "ColorGradingSettings | str"
    ) -> "BiomeClient":
        """Sets the color grading used in Vibrant Visuals mode.

        Args:
            color_grading_identifier (ColorGradingSettings | str): The color grading definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_color_grading_identifier)
        """
        self.components.add(
            BiomeClientColorGradingIdentifier(
                color_grading_identifier=color_grading_identifier
            )
        )
        return self

    def cubemap_identifier(
        self, cubemap_identifier: "CubeMapSettings | str"
    ) -> "BiomeClient":
        """Sets the cubemap used for the Vibrant Visuals skybox lighting.

        Args:
            cubemap_identifier (CubeMapSettings | str): The cubemap definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_cubemap_identifier)
        """
        self.components.add(
            BiomeClientCubemapIdentifier(cubemap_identifier=cubemap_identifier)
        )
        return self

    def dry_foliage_appearance(self, color: Color) -> "BiomeClient":
        """Sets the dry foliage color.

        Args:
            color (Color): The dry foliage color.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_dry_foliage_color)
        """
        self.components.add(BiomeClientDryFoliageColor(color=color))
        return self

    def fog_appearance(self, fog: "FogSettings | str") -> "BiomeClient":
        """Sets the fog used during rendering.

        Args:
            fog (FogSettings | str): The fog definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_fog_appearance)
        """
        self.components.add(BiomeClientFogAppearance(fog_identifier=fog))
        return self

    def foliage_appearance(
        self,
        color: (
            Color
            | Literal[
                "birch",
                "dry_foliage",
                "evergreen",
                "foliage",
                "mangrove_swamp_foliage",
                "swamp_foliage",
            ]
        ),
    ) -> "BiomeClient":
        """Sets the foliage color or color map.

        Args:
            color (Color | FoliageColorMap): A color, or a foliage color map name.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_foliage_appearance)
        """
        self.components.add(BiomeClientFoliageAppearance(color=color))
        return self

    def grass_appearance(
        self, color: Color | Literal["grass", "swamp_grass"]
    ) -> "BiomeClient":
        """Sets the grass color or color map.

        Args:
            color (Color | GrassColorMap): A color, or a grass color map name.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_grass_appearance)
        """
        self.components.add(BiomeClientGrassAppearance(color=color))
        return self

    def lighting_identifier(
        self, lighting_identifier: "LightingSettings | str"
    ) -> "BiomeClient":
        """Sets the lighting used in Vibrant Visuals mode.

        Args:
            lighting_identifier (LightingSettings | str): The lighting definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_lighting_identifier)
        """
        self.components.add(
            BiomeClientLightingIdentifier(lighting_identifier=lighting_identifier)
        )
        return self

    def precipitation(
        self,
        ash: float | None = None,
        blue_spores: float | None = None,
        red_spores: float | None = None,
        white_ash: float | None = None,
    ) -> "BiomeClient":
        """Sets the precipitation visuals. Set at most one of them.

        Args:
            ash (float, optional): Density of ash, as in the soul sand valley.
            blue_spores (float, optional): Density of blue spores, as in the warped forest.
            red_spores (float, optional): Density of red spores, as in the crimson forest.
            white_ash (float, optional): Density of white ash, as in the basalt deltas.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_precipitation)
        """
        self.components.add(
            BiomeClientPrecipitation(
                ash=ash,
                blue_spores=blue_spores,
                red_spores=red_spores,
                white_ash=white_ash,
            )
        )
        return self

    def sky_color(self, color: Color) -> "BiomeClient":
        """Sets the sky color.

        Args:
            color (Color): The sky color.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_sky_color)
        """
        self.components.add(BiomeClientSkyColor(sky_color=color))
        return self

    def water_appearance(
        self, surface_color: Color, surface_opacity: float = 0.8
    ) -> "BiomeClient":
        """Sets the water surface color.

        Args:
            surface_color (Color): The water surface color.
            surface_opacity (float, optional): From 0, invisible, to 1, opaque. Defaults to 0.8.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_appearance)
        """
        self.components.add(
            BiomeClientWaterAppearance(
                surface_color=surface_color, surface_opacity=surface_opacity
            )
        )
        return self

    def water_identifier(
        self, water_identifier: "WaterSettings | str"
    ) -> "BiomeClient":
        """Sets the water rendering used in Vibrant Visuals mode.

        Args:
            water_identifier (WaterSettings | str): The water definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_identifier)
        """
        self.components.add(
            BiomeClientWaterIdentifier(water_identifier=water_identifier)
        )
        return self

    def __export__(self) -> None:
        """Checks the components before the file is written.

        Raises:
            ValueError: A server biome component was added to the client biome.
        """
        for component in self.components:
            if not isinstance(component, BiomeClientComponent):
                raise ValueError(
                    f"{type(component).__name__} is a server biome component. "
                    f"Add it to the biome server instead. {self._object_type}[{self.identifier}]"
                )
        validate_components(self, self.components, [])
        return super().__export__()
