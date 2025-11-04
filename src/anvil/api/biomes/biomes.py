import os
from typing import Literal

from anvil.api.actors.actors import _Components
from anvil.api.core.sounds import MusicDefinition, SoundEvent, _SoundDescription
from anvil.api.pbr.pbr import (
    AtmosphericSettings,
    ColorGradingSettings,
    LightingSettings,
    WaterSettings,
)
from anvil.api.world.fog import Fog
from anvil.lib.config import CONFIG, ConfigPackageTarget
from anvil.lib.enums import MusicCategory, SoundCategory
from anvil.lib.lib import clamp, convert_color
from anvil.lib.reports import ReportType
from anvil.lib.schemas import (
    AddonObject,
    BiomeDescriptor,
    JsonSchemes,
    MinecraftDescription,
)
from anvil.lib.types import RGB, Color


class _BiomeDescription(MinecraftDescription):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The biome description.

        Parameters:
            name (str): The name of the biome.
            is_vanilla (bool, optional): Whether or not the biome is a vanilla biome. Defaults to False.
        """
        super().__init__(name, is_vanilla)

    def _export(self):
        return super()._export()


class _BiomeServer(AddonObject):
    """The biome server object."""

    _extension = ".biome.json"
    _path = os.path.join(CONFIG.BP_PATH, "biomes")
    _object_type = "Biomes Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The biome server object.

        Parameters:
            name (str): The name of the biome.
            is_vanilla (bool, optional): Whether or not the biome is a vanilla biome. Defaults to False.
        """
        super().__init__(name)
        self._server_biome = JsonSchemes.biome_server()
        self._description = _BiomeDescription(name, is_vanilla)
        self._components = _Components()

    @property
    def description(self):
        """The biome description."""
        return self._description

    @property
    def components(self):
        """The biome components."""
        return self._components

    def queue(self):
        """Queues the biome to be exported."""
        self._server_biome["minecraft:biome"].update(self.description._export())
        self._server_biome["minecraft:biome"].update(self._components._export())

        self.content(self._server_biome)
        super().queue()


class _BiomeClient(AddonObject):
    """The biome client object."""

    _extension = ".biome.json"
    _path = os.path.join(CONFIG.RP_PATH, "biomes")
    _object_type = "Biome Client"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name)
        self._server_biome = JsonSchemes.biome_client()
        self._description = _BiomeDescription(name, is_vanilla)

    def ambient_sounds(
        self,
        sound_reference: str | None = None,
        loop_reference: str | None = None,
        mood_reference: str | None = None,
    ) -> dict[Literal["addition", "loop", "mood"], _SoundDescription | None]:
        """
        Sets the ambient sounds for the biome.

        Parameters:
            sound_reference (str): Named sound that occasionally plays at the listener position.
            loop_reference (str): Named sound that loops while the listener position is inside the biome.
            mood_reference (str, optional): Named sound that rarely plays at a nearby air block position when the light level is low. Biomes without an ambient mood sound will use the 'ambient.cave' sound.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_ambient_sounds)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:ambient_sounds"
        ] = {
            "addition": sound_reference,
            "loop": loop_reference,
            "mood": mood_reference,
        }

        sound_event_obj = SoundEvent()

        return {
            "addition": (
                sound_event_obj.add_individual_event(
                    sound_reference, SoundCategory.Ambient
                )
                if sound_reference
                else None
            ),
            "loop": (
                sound_event_obj.add_individual_event(
                    loop_reference, SoundCategory.Ambient
                )
                if loop_reference
                else None
            ),
            "mood": (
                sound_event_obj.add_individual_event(
                    mood_reference, SoundCategory.Ambient
                )
                if mood_reference
                else None
            ),
        }

    def atmosphere_identifier(self, atmosphere_identifier: AtmosphericSettings) -> None:
        """Set the identifier used for atmospherics in Vibrant Visuals mode. Identifiers must resolve to identifiers in valid Atmospheric Scattering JSON schemas under the "atmospherics" directory. Biomes without this component will have default atmosphere settings.

        Parameters:
            atmosphere_identifier (AtmosphericSettings): Identifier of atmosphere definition to use.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_atmosphere_identifier)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:atmosphere_identifier"
        ] = {"atmosphere_identifier": atmosphere_identifier.identifier}

    def biome_music(
        self,
        music_reference: MusicCategory | str = None,
        underwater_music: MusicCategory | str = None,
        volume_multiplier: float = 1.0,
    ) -> dict[Literal["music_definition", "underwater_music"], MusicCategory | str]:
        """
        Affects how music plays within the biome.

        Parameters:
            music_reference (str): Music to be played when inside this biome. If left off or not found the default music will be determined by the dimension. Empty string will result in no music.
            underwater_music (str, optional): Music to be played when underwater in this biome. If left off or not found the default music will be determined by the dimension. Empty string will result in no music.
            volume_multiplier (float, optional): Multiplier temporarily and gradually applied to music volume when within this biome. Must be a value between 0 and 1, inclusive.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_biome_music)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:biome_music"
        ] = {
            "music_definition": music_reference,
            "underwater_music": underwater_music,
            "volume_multiplier": clamp(volume_multiplier, 0, 1),
        }

        music_definition_object = MusicDefinition()

        return {
            "music_definition": music_definition_object.music_definition(
                music_reference
            ),
            "underwater_music": music_definition_object.music_definition(
                underwater_music
            ),
        }

    def color_grading_identifier(
        self, color_grading_identifier: ColorGradingSettings
    ) -> None:
        """Set the identifier used for color grading in Vibrant Visuals mode. Identifiers must resolve to identifiers in valid Color Grading JSON schemas under the "color_grading" directory. Biomes without this component will have default color_grading settings.

        Parameters:
            color_grading_identifier (ColorGradingSettings): Identifier of color_grading definition to use.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_color_grading_identifier)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:color_grading_identifier"
        ] = {"color_grading_identifier": color_grading_identifier.identifier}

    def dry_foliage_appearance(self, color: Color):
        """
        Sets the dry foliage color for the biome.

        Parameters:
            color (RGB): The color of the dry foliage.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_dry_foliage_color)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:dry_foliage_color"
        ] = {"color": convert_color(color, RGB)}

    def fog_appearance(self, fog: str | Fog):
        """
        Sets the fog settings used during rendering. Biomes without this component will have default fog settings.

        Parameters:
            fog (str | Fog): Identifier of fog definition to use.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_fog_appearance)
        """
        if isinstance(fog, str):
            self._fog = Fog(fog)
        elif isinstance(fog, Fog):
            self._fog = fog

        self._content["minecraft:client_biome"]["components"][
            "minecraft:fog_appearance"
        ] = {"fog_appearance": self._fog.identifier}

    def foliage_appearance(self, color: RGB):
        """Sets the foliage color or color map used during rendering. Biomes without this component will have default foliage appearance.

        Parameters:
            color (RGB): RGB color of foliage, or a Foliage Color Map object.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_foliage_appearance)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:foliage_appearance"
        ] = {"color": convert_color(color, RGB)}

    def grass_appearance(self, color: RGB):
        """Set the grass color or color map used during rendering. Biomes without this component will have default grass appearance.

        Parameters:
            color (RGB): RGB color of grass.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_grass_appearance)
        """

        self._content["minecraft:client_biome"]["components"][
            "minecraft:grass_appearance"
        ] = {"color": convert_color(color, RGB)}

    def lighting_identifier(self, lighting_identifier: LightingSettings) -> None:
        """Set the identifier used for lighting in Vibrant Visuals mode. Identifiers must resolve to identifiers in valid Lighting JSON schemas under the "lighting" directory. Biomes without this component will have default lighting settings.

        Parameters:
            lighting_identifier (LightingSettings): Identifier of lighting definition to use.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_lighting_identifier)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:lighting_identifier"
        ] = {"lighting_identifier": lighting_identifier}

    def precipitation(
        self,
        ash: float = None,
        blue_spores: float = None,
        red_spores: float = None,
        white_ash: float = None,
    ):
        """
        Sets the precipitation visuals for the biome.

        Parameters:
            ash (float, optional): Density of ash precipitation visuals.
            blue_spores (float, optional): Density of blue spore precipitation visuals.
            red_spores (float, optional): Density of red spore precipitation visuals.
            white_ash (float, optional): Density of white ash precipitation visuals.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_precipitation)
        """
        precipitation_data = {}

        if ash is not None:
            precipitation_data["ash"] = ash
        if blue_spores is not None:
            precipitation_data["blue_spores"] = blue_spores
        if red_spores is not None:
            precipitation_data["red_spores"] = red_spores
        if white_ash is not None:
            precipitation_data["white_ash"] = white_ash

        if precipitation_data:
            self._content["minecraft:client_biome"]["components"][
                "minecraft:precipitation"
            ] = precipitation_data

    def sky_color(self, color: Color):
        """
        Sets the sky color used during rendering. Biomes without this component will have default sky color behavior.

        Parameters:
            color (Color): 	RGB color of the sky.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_sky_color)
        """
        self._content["minecraft:client_biome"]["components"]["minecraft:sky_color"] = {
            "sky_color": convert_color(color, RGB)
        }

    def water_appearance(self, surface_color: Color, surface_opacity: float = 0.8):
        """
        Set the water surface color used during rendering. Biomes without this component will have default water surface color behavior.

        Parameters:
            surface_color (Color): RGB color of the water surface.
            surface_opacity (float, optional): Opacity of the water surface (must be between 0 for invisible and 1 for opaque, inclusive).


        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_appearance)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:water_appearance"
        ] = {
            "surface_color": convert_color(surface_color, RGB),
            "surface_opacity": clamp(surface_opacity, 0, 1),
        }

    def water_identifier(self, water_identifier: WaterSettings) -> None:
        """Set the identifier used for rendering water in Vibrant Visuals mode. Identifiers must resolve to identifiers in valid Water JSON schemas under the "water" directory. Biomes without this component will have default water settings.

        Args:
            water_identifier (WaterSettings): Identifier of water definition to use.

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/clientbiomesreference/examples/components/minecraftclientbiomes_water_identifier)
        """
        self._content["minecraft:client_biome"]["components"][
            "minecraft:water_identifier"
        ] = {"water_identifier": water_identifier.identifier}

    def queue(self):
        if self._fog:
            self._fog.queue()
        return super().queue()


class Biome(BiomeDescriptor):
    _object_type = "Biome"

    def __init__(self, name, is_vanilla=False):
        # Released in 1.21.111
        # if not CONFIG._EXPERIMENTAL:
        #    raise RuntimeError("Biome support is experimental and must be enabled in the config.")

        if CONFIG.TARGET == ConfigPackageTarget.ADDON and is_vanilla:
            raise ValueError(
                "Vanilla biomes overrides cannot be used in addons, use Partial overrides instead."
            )

        super().__init__(name, is_vanilla)

        self._server = None
        self._client = None

    @property
    def server(self):
        if self._server is None:
            self._server = _BiomeServer(self._name, self._is_vanilla)
        return self._server

    @property
    def client(self):
        if self._client is None:
            self._client = _BiomeClient(self._name, self._is_vanilla)
        return self._client

    def queue(self):
        """Queues the biome to be exported."""
        if self._server:
            self.server.queue()

        CONFIG.Report.add_report(
            ReportType.BIOME,
            vanilla=self._is_vanilla,
            col0=self._display_name,
            col1=self.identifier,
        )
