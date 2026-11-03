from typing import Annotated, ClassVar, Literal

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import LIGHTING_SETTINGS_VERSION
from anvil.lib.jsonmodel import (
    AnyColor,
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    KeyFrame,
    KeyFramed,
    KeyFramedColor,
    Wrapped,
    json_field,
)
from anvil.lib.lib import AnvilFormatter
from anvil.lib.schemas import JsonSchemes, MinecraftBlockDescriptor


class _OrbitalLight(JsonObject):
    """The sun or the moon. Unset keys are left out."""

    illuminance: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    color: (
        Annotated[
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame],
            KeyFramedColor(),
        ]
        | None
    ) = None

    def set_illuminance(self, illuminance: float | list[KeyFrame]) -> None:
        """Sets the brightness in lux."""
        self.illuminance = illuminance

    def set_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]
    ) -> None:
        """Sets the light color."""
        self.color = color


class _OrbitalLights(JsonObject):
    """The `orbital` object: the sun, the moon and their orbit."""

    sun: _OrbitalLight = json_field(default_factory=_OrbitalLight)
    moon: _OrbitalLight = json_field(default_factory=_OrbitalLight)
    orbital_offset_degrees: Annotated[float | list[KeyFrame], KeyFramed()] | None = None

    def set_orbital_offset_degrees(
        self, orbital_offset_degrees: float | list[KeyFrame]
    ) -> None:
        """Sets the rotational offset of the sun and moon from the standard orbital axis."""
        self.orbital_offset_degrees = orbital_offset_degrees


class _FlashLight(JsonObject):
    """The End flash, which only lights the End."""

    __required__: ClassVar[tuple[str, ...]] = ("illuminance", "color")

    illuminance: float | None = None
    color: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, AnyColor] | None
    ) = None

    def set_illuminance(self, illuminance: float) -> None:
        """Sets the peak brightness in lux."""
        self.illuminance = illuminance

    def set_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> None:
        """Sets the light color."""
        self.color = color


class _DirectionalLights(JsonObject):
    """The `directional_lights` object. Parts with nothing set are left out."""

    orbital: _OrbitalLights = json_field(default_factory=_OrbitalLights)
    flash: _FlashLight = json_field(default_factory=_FlashLight)

    def set_orbital(self, orbital: _OrbitalLights) -> None:
        """Replaces the sun, moon and orbit settings."""
        self.orbital = orbital


class _Emissive(JsonObject):
    """Global settings of emissive light sources."""

    desaturation: Annotated[float, InRange(0.0, 1.0)] | None = None

    def set_desaturation(self, desaturation: float) -> None:
        """Sets how much a pixel's albedo is desaturated, from 0.0 to 1.0."""
        self.desaturation = desaturation


class _Ambient(JsonObject):
    """The light of surfaces that no other light reaches. Unset keys are left out."""

    illuminance: Annotated[float | list[KeyFrame], KeyFramed(0.0, 5.0)] | None = None
    color: (
        Annotated[
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame],
            KeyFramedColor(),
        ]
        | None
    ) = None

    def set_illuminance(self, illuminance: float | list[KeyFrame]) -> None:
        """Sets the light strength in lux, from 0.0 to 5.0."""
        self.illuminance = illuminance

    def set_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]
    ) -> None:
        """Sets the light color."""
        self.color = color


class _Sky(JsonObject):
    """The indirect light from the sky."""

    intensity: Annotated[float | list[KeyFrame], KeyFramed(0.1, 1.0)] | None = None

    def set_intensity(self, intensity: float | list[KeyFrame]) -> None:
        """Sets the energy scaling factor, from 0.1 to 1.0."""
        self.intensity = intensity


class _LightingSettings(JsonObject):
    """The `minecraft:lighting_settings` object. Parts with nothing set are left out."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    directional_lights: _DirectionalLights = json_field(
        default_factory=_DirectionalLights
    )
    emissive: _Emissive = json_field(default_factory=_Emissive)
    ambient: _Ambient = json_field(default_factory=_Ambient)
    sky: _Sky = json_field(default_factory=_Sky)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The settings have no identifier.")


class _LightingSettingsFile(JsonObject):
    """The content of a `lighting/*.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:lighting_settings",
    )

    format_version: str = json_field(default=LIGHTING_SETTINGS_VERSION, init=False)
    settings: _LightingSettings = json_field(
        key="minecraft:lighting_settings", default_factory=_LightingSettings
    )


class LightingSettings(JsonFile):
    """Global lighting settings for Vibrant Visuals (PBR) rendering.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/lightingcustomization)
    """

    _document = _LightingSettingsFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "lighting"
    _object_type = "Lighting Settings"

    def __init__(self, name: str = "default_lighting") -> None:
        """Initializes a LightingSettings instance.

        Raises:
            RuntimeError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Lighting settings require PBR to be enabled in the config."
            )

        super().__init__(
            "global" if name == "default_lighting" else name, identifier=name
        )
        self._content.settings.set_description(self.identifier)

    def orbital_lights(
        self,
        sun_illuminance: float | list[KeyFrame] | None = None,
        sun_color: (
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame] | None
        ) = None,
        moon_illuminance: float | list[KeyFrame] | None = None,
        moon_color: (
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame] | None
        ) = None,
        orbital_offset_degrees: float | list[KeyFrame] | None = None,
    ) -> None:
        """Configures the orbital celestial lights (sun and moon).

        Args:
            sun_illuminance (float | list[KeyFrame]): Brightness of the sun in lux (lx).
            sun_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]): Color contributed by the sun. Supports RGB array or HEX string.
            moon_illuminance (float | list[KeyFrame]): Brightness of the moon in lux (lx).
            moon_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]): Color contributed by the moon. Supports RGB array or HEX string.
            orbital_offset_degrees (float | list[KeyFrame]): Rotational offset of celestial bodies from standard orbital axis.
        """
        orbital = _OrbitalLights()
        if sun_illuminance is not None:
            orbital.sun.set_illuminance(sun_illuminance)
        if sun_color is not None:
            orbital.sun.set_color(sun_color)
        if moon_illuminance is not None:
            orbital.moon.set_illuminance(moon_illuminance)
        if moon_color is not None:
            orbital.moon.set_color(moon_color)
        if orbital_offset_degrees is not None:
            orbital.set_orbital_offset_degrees(orbital_offset_degrees)
        self._content.settings.directional_lights.set_orbital(orbital)

    def flash_light(
        self,
        illuminance: float,
        color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
    ) -> None:
        """Configures the End flash light source (exclusive to the End dimension).

        Args:
            illuminance (float): Peak brightness of the End flash in lux (lx).
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): Color contributed by the End flash. Supports RGB array or HEX string.
        """
        flash = self._content.settings.directional_lights.flash
        flash.set_illuminance(illuminance)
        flash.set_color(color)

    def emissive(self, desaturation: float) -> None:
        """Configures global settings for emissive light sources.

        Args:
            desaturation (float): Factor (0.0 to 1.0) controlling how much the albedo of a given pixel is desaturated.
        """
        self._content.settings.emissive.set_desaturation(desaturation)

    def ambient(
        self,
        illuminance: float | list[KeyFrame],
        color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame],
    ) -> None:
        """Controls how surfaces are lit when there are no other light sources available.

        Args:
            illuminance (float | list[KeyFrame]): Minimum fallback light strength in lux (lx). Valid range: 0.0 to 5.0.
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]): Color of the ambient fallback light. Supports RGB array or HEX string.
        """
        ambient = self._content.settings.ambient
        ambient.set_illuminance(illuminance)
        ambient.set_color(color)

    def sky(self, intensity: float | list[KeyFrame]) -> None:
        """Controls indirect lighting contribution from the sky.

        Args:
            intensity (float | list[KeyFrame]): Energy scaling factor. Valid range: 0.1 to 1.0.
        """
        self._content.settings.sky.set_intensity(intensity)

    def queue(self) -> "LightingSettings":
        return super().queue()


class LocalLighting(JsonFile):
    """Local lighting configurations (point lights and static lights) for Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _pack = Pack.RP
    _folder = "local_lighting"
    _object_type = "Local Lighting Settings"

    def __init__(self) -> None:
        """Initializes a LocalLighting instance.

        Raises:
            RuntimeError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Local lighting requires PBR to be enabled in the config."
            )
        super().__init__("local_lighting")
        self.content(JsonSchemes.local_lighting())

    def add_local_light(
        self,
        block_identifier: MinecraftBlockDescriptor | str,
        color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
        light_type: Literal["static_light", "point_light"] = "point_light",
    ) -> None:
        """Adds a local light to the local lighting configuration.

        Args:
            block_identifier (MinecraftBlockDescriptor | str): The identifier of the block that emits the light.
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The color of the light.
            light_type (Literal["static_light", "point_light"]): The type of local light.
        """
        self._content["minecraft:local_light_settings"][str(block_identifier)] = {
            "light_color": AnvilFormatter.convert_color(color),
            "light_type": light_type,
        }

    def add_point_light(
        self,
        block_identifier: MinecraftBlockDescriptor | str,
        color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
    ) -> None:
        """Adds a point light to the point lights configuration (legacy fallback).

        Args:
            block_identifier (MinecraftBlockDescriptor | str): The identifier of the block that emits the light.
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The color of the light.
        """
        self.add_local_light(block_identifier, color, "static_light")
