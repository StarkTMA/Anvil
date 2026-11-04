from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import (
    LIGHTING_SETTINGS_VERSION,
    LOCAL_LIGHTING_SETTINGS_VERSION,
)
from anvil.lib.jsonmodel import (
    AnyColor,
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    KeyFramed,
    KeyFramedColor,
    Wrapped,
    json_field,
)
from anvil.lib.jsonmodel.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA


class _OrbitalLight(JsonObject):
    """The sun or the moon. Unset keys are left out."""

    illuminance: Annotated[float | list[tuple[float, float]], KeyFramed()] | None = None
    color: (
        Annotated[
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]],
            KeyFramedColor(),
        ]
        | None
    ) = None

    def set_illuminance(self, illuminance: float | list[tuple[float, float]]) -> None:
        """Sets the brightness in lux."""
        self.illuminance = illuminance

    def set_color(
        self,
        color: (
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]
        ),
    ) -> None:
        """Sets the light color."""
        self.color = color


class _OrbitalLights(JsonObject):
    """The `orbital` object: the sun, the moon and their orbit."""

    sun: _OrbitalLight = json_field(default_factory=_OrbitalLight)
    moon: _OrbitalLight = json_field(default_factory=_OrbitalLight)
    orbital_offset_degrees: (
        Annotated[float | list[tuple[float, float]], KeyFramed()] | None
    ) = None

    def set_orbital_offset_degrees(
        self, orbital_offset_degrees: float | list[tuple[float, float]]
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

    illuminance: (
        Annotated[float | list[tuple[float, float]], KeyFramed(0.0, 5.0)] | None
    ) = None
    color: (
        Annotated[
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]],
            KeyFramedColor(),
        ]
        | None
    ) = None

    def set_illuminance(self, illuminance: float | list[tuple[float, float]]) -> None:
        """Sets the light strength in lux, from 0.0 to 5.0."""
        self.illuminance = illuminance

    def set_color(
        self,
        color: (
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]
        ),
    ) -> None:
        """Sets the light color."""
        self.color = color


class _Sky(JsonObject):
    """The indirect light from the sky."""

    intensity: (
        Annotated[float | list[tuple[float, float]], KeyFramed(0.1, 1.0)] | None
    ) = None

    def set_intensity(self, intensity: float | list[tuple[float, float]]) -> None:
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
            ValueError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Lighting settings require PBR to be enabled in the config."
            )

        super().__init__(
            "global" if name == "default_lighting" else name, identifier=name
        )
        self._content.settings.set_description(self.identifier)

    def orbital_lights(
        self,
        sun_illuminance: float | list[tuple[float, float]] | None = None,
        sun_color: (
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]
            | None
        ) = None,
        moon_illuminance: float | list[tuple[float, float]] | None = None,
        moon_color: (
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]
            | None
        ) = None,
        orbital_offset_degrees: float | list[tuple[float, float]] | None = None,
    ) -> None:
        """Configures the orbital celestial lights (sun and moon).

        Args:
            sun_illuminance (float | list[tuple[float, float]]): Brightness of the sun in lux (lx).
            sun_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]): Color contributed by the sun. Supports RGB array or HEX string.
            moon_illuminance (float | list[tuple[float, float]]): Brightness of the moon in lux (lx).
            moon_color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]): Color contributed by the moon. Supports RGB array or HEX string.
            orbital_offset_degrees (float | list[tuple[float, float]]): Rotational offset of celestial bodies from standard orbital axis.
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
        illuminance: float | list[tuple[float, float]],
        color: (
            HexRGB
            | HexRGBA
            | RGB
            | RGBA
            | RGB255
            | RGBA255
            | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]
        ),
    ) -> None:
        """Controls how surfaces are lit when there are no other light sources available.

        Args:
            illuminance (float | list[tuple[float, float]]): Minimum fallback light strength in lux (lx). Valid range: 0.0 to 5.0.
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[tuple[float, HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255]]): Color of the ambient fallback light. Supports RGB array or HEX string.
        """
        ambient = self._content.settings.ambient
        ambient.set_illuminance(illuminance)
        ambient.set_color(color)

    def sky(self, intensity: float | list[tuple[float, float]]) -> None:
        """Controls indirect lighting contribution from the sky.

        Args:
            intensity (float | list[tuple[float, float]]): Energy scaling factor. Valid range: 0.1 to 1.0.
        """
        self._content.settings.sky.set_intensity(intensity)

    def queue(self) -> "LightingSettings":
        return super().queue()


class _LocalLight(JsonObject):
    """A block that gives off light in Vibrant Visuals."""

    __required__: ClassVar[tuple[str, ...]] = ("light_color", "light_type")

    light_color: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, AnyColor] | None
    ) = None
    light_type: Literal["static_light", "point_light"] = json_field(
        default="point_light"
    )


class _LocalLightingFile(JsonObject):
    """The content of the `local_lighting/local_lighting.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:local_light_settings",
    )

    format_version: str = json_field(
        default=LOCAL_LIGHTING_SETTINGS_VERSION, init=False
    )
    lights: dict[str, _LocalLight] = json_field(
        default_factory=dict, key="minecraft:local_light_settings"
    )


class LocalLighting(JsonFile):
    """The blocks that give off light in Vibrant Visuals: point lights and static lights.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/locallightingsettings)
    """

    _document = _LocalLightingFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "local_lighting"
    _object_type = "Local Lighting Settings"

    def __init__(self) -> None:
        """Creates the local lighting settings.

        Raises:
            ValueError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise ValueError("Local lighting requires PBR to be enabled in the config.")
        super().__init__("local_lighting")

    @property
    def lights(self) -> dict[str, _LocalLight]:
        """The lights, by block identifier."""
        return self._content.lights

    def add_local_light(
        self,
        block_identifier: str | Block | BlockDescriptor,
        color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
        light_type: Literal["static_light", "point_light"] = "point_light",
    ) -> "LocalLighting":
        """Makes a block give off light.

        Args:
            block_identifier (Block | BlockDescriptor | str): The block.
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The light's color.
            light_type (Literal["static_light", "point_light"], optional): Defaults to
                `point_light`.
        """
        self.lights[str(block_identifier)] = _LocalLight(
            light_color=color, light_type=light_type
        )
        return self

    def add_point_light(
        self,
        block_identifier: str | Block | BlockDescriptor,
        color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255,
    ) -> "LocalLighting":
        """Makes a block a static light.

        Args:
            block_identifier (Block | BlockDescriptor | str): The block.
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255): The light's color.
        """
        return self.add_local_light(block_identifier, color, "static_light")
