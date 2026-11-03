from typing import Literal

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
from anvil.api.biomes.server import BiomeDescription
from anvil.api.core.components import ComponentGroup
from anvil.api.core.enums import MusicCategory, SoundCategory
from anvil.api.core.sounds import MusicDefinition, SoundEvent, _SoundDescription
from anvil.api.core.types import Color, FoliageColorMap, GrassColorMap
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import JsonFile, validate_components
from anvil.lib.schemas import JsonSchemes

from anvil.api.pbr.atmosphere import AtmosphericSettings
from anvil.api.pbr.color_grading import ColorGradingSettings
from anvil.api.pbr.cubemap import CubeMapSettings
from anvil.api.pbr.fog import FogSettings
from anvil.api.pbr.lighting import LightingSettings
from anvil.api.pbr.water import WaterSettings

__all__ = ["BiomeClient"]


class BiomeClient(JsonFile):
    """The biome client object."""

    _extension = ".client_biome.json"
    _pack = Pack.RP
    _folder = "biomes"
    _object_type = "Biome Client"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The biome client object. Set the client biome components with the builder methods,
        or add the `BiomeClient` components from `anvil.api.biomes.components` to `components`.

        Args:
            name (str): The name of the biome.
            is_vanilla (bool, optional): Whether or not the biome is a vanilla biome. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.content(JsonSchemes.biome_client())
        self._description = BiomeDescription(name, is_vanilla)
        self._components = ComponentGroup(name="components")

    @property
    def components(self) -> ComponentGroup:
        """The client biome components."""
        return self._components

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
        self._components.add(
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
        self._components.add(
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
        self._components.add(
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
        self._components.add(
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
        self._components.add(
            BiomeClientCubemapIdentifier(cubemap_identifier=cubemap_identifier)
        )
        return self

    def dry_foliage_appearance(self, color: Color) -> "BiomeClient":
        """Sets the dry foliage color.

        Args:
            color (Color): The dry foliage color.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_dry_foliage_color)
        """
        self._components.add(BiomeClientDryFoliageColor(color=color))
        return self

    def fog_appearance(self, fog: "FogSettings | str") -> "BiomeClient":
        """Sets the fog used during rendering.

        Args:
            fog (FogSettings | str): The fog definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_fog_appearance)
        """
        self._components.add(BiomeClientFogAppearance(fog_identifier=fog))
        return self

    def foliage_appearance(self, color: Color | FoliageColorMap) -> "BiomeClient":
        """Sets the foliage color or color map.

        Args:
            color (Color | FoliageColorMap): A color, or a foliage color map name.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_foliage_appearance)
        """
        self._components.add(BiomeClientFoliageAppearance(color=color))
        return self

    def grass_appearance(self, color: Color | GrassColorMap) -> "BiomeClient":
        """Sets the grass color or color map.

        Args:
            color (Color | GrassColorMap): A color, or a grass color map name.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_grass_appearance)
        """
        self._components.add(BiomeClientGrassAppearance(color=color))
        return self

    def lighting_identifier(
        self, lighting_identifier: "LightingSettings | str"
    ) -> "BiomeClient":
        """Sets the lighting used in Vibrant Visuals mode.

        Args:
            lighting_identifier (LightingSettings | str): The lighting definition.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_lighting_identifier)
        """
        self._components.add(
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
        self._components.add(
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
        self._components.add(BiomeClientSkyColor(sky_color=color))
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
        self._components.add(
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
        self._components.add(
            BiomeClientWaterIdentifier(water_identifier=water_identifier)
        )
        return self

    def queue(self) -> "BiomeClient":
        """Queues the client biome to be exported.

        Raises:
            ValueError: A server biome component was added to the client biome.
        """
        for component in self._components:
            if not isinstance(component, BiomeClientComponent):
                raise ValueError(
                    f"{type(component).__name__} is a server biome component. "
                    f"Add it to the biome server instead. {self._object_type}[{self.identifier.name}]"
                )
        validate_components(self, self._components, [])
        self._content["minecraft:client_biome"].update(self._description.__export__())
        self._content["minecraft:client_biome"][
            "components"
        ] = self._components.__payload__()
        return super().queue()
