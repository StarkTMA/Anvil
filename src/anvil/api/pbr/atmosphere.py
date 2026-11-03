from typing import Annotated, ClassVar

from anvil.api.core.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import ATMOSPHERE_SETTINGS_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    JsonFile,
    JsonObject,
    KeyFrame,
    KeyFramed,
    KeyFramedColor,
    Wrapped,
    json_field,
)

__all__ = ["AtmosphericSettings"]


class _HorizonBlendStops(JsonObject):
    """How the atmosphere is divided up. Each value is a number or keyframes."""

    __required__: ClassVar[tuple[str, ...]] = ("min", "start", "mie_start", "max")

    min: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    start: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    mie_start: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    max: Annotated[float | list[KeyFrame], KeyFramed()] | None = None

    def set_min(self, min: float | list[KeyFrame]) -> None:
        """Sets the minimum horizon height."""
        self.min = min

    def set_start(self, start: float | list[KeyFrame]) -> None:
        """Sets the height relative to the horizon where the zenith contribution takes over."""
        self.start = start

    def set_mie_start(self, mie_start: float | list[KeyFrame]) -> None:
        """Sets the height relative to the horizon where mie scattering begins."""
        self.mie_start = mie_start

    def set_max(self, max: float | list[KeyFrame]) -> None:
        """Sets the maximum horizon height."""
        self.max = max


class _AtmosphereSettings(JsonObject):
    """The `minecraft:atmosphere_settings` object. Unset keys are left out."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    horizon_blend_stops: _HorizonBlendStops = json_field(
        default_factory=_HorizonBlendStops
    )
    rayleigh_strength: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    sun_mie_strength: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    moon_mie_strength: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    sun_glare_shape: Annotated[float | list[KeyFrame], KeyFramed()] | None = None
    sky_zenith_color: (
        Annotated[
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame],
            KeyFramedColor(),
        ]
        | None
    ) = None
    sky_horizon_color: (
        Annotated[
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame],
            KeyFramedColor(),
        ]
        | None
    ) = None

    def set_rayleigh_strength(self, value: float | list[KeyFrame]) -> None:
        """Sets how strong the atmosphere's rayleigh scattering term is."""
        self.rayleigh_strength = value

    def set_sun_mie_strength(self, value: float | list[KeyFrame]) -> None:
        """Sets how strong the sun's mie scattering term is."""
        self.sun_mie_strength = value

    def set_moon_mie_strength(self, value: float | list[KeyFrame]) -> None:
        """Sets how strong the moon's mie scattering term is."""
        self.moon_mie_strength = value

    def set_sun_glare_shape(self, value: float | list[KeyFrame]) -> None:
        """Sets how the lobe of the mie scattering is shaped."""
        self.sun_glare_shape = value

    def set_sky_zenith_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]
    ) -> None:
        """Sets the color of the zenith region of the atmosphere."""
        self.sky_zenith_color = color

    def set_sky_horizon_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]
    ) -> None:
        """Sets the color of the horizon region of the atmosphere."""
        self.sky_horizon_color = color

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The settings have no identifier.")


class _AtmosphereSettingsFile(JsonObject):
    """The content of an `atmospherics/*.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:atmosphere_settings",
    )

    format_version: str = json_field(default=ATMOSPHERE_SETTINGS_VERSION, init=False)
    settings: _AtmosphereSettings = json_field(
        key="minecraft:atmosphere_settings", default_factory=_AtmosphereSettings
    )


class AtmosphericSettings(JsonFile):
    """Atmospheric settings for Vibrant Visuals (PBR) rendering.

    Allows customizing Rayleigh and Mie scattering, glare, blend stops, and sky colors.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/atmosphericscustomization)
    """

    _document = _AtmosphereSettingsFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "atmospherics"
    _object_type = "Atmospheric Settings"

    def __init__(self, name: str = "default_atmospherics") -> None:
        """Initializes an AtmosphericSettings instance.

        Raises:
            RuntimeError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__(
            "atmospherics" if name == "default_atmospherics" else name, identifier=name
        )
        self._content.settings.set_description(self.identifier)

    def horizon_blend_stops(
        self,
        min: float | list[KeyFrame],
        start: float | list[KeyFrame],
        mie_start: float | list[KeyFrame],
        max: float | list[KeyFrame],
    ) -> "AtmosphericSettings":
        """How the atmosphere is divided up.

        Args:
            min (float | list[KeyFrame]): The minimum horizon height.
            start (float | list[KeyFrame]): The height relative to the horizon where the zenith contribution will take over.
            mie_start (float | list[KeyFrame]): The height relative to the horizon where mie scattering begins.
            max (float | list[KeyFrame]): The maximum horizon height.
        """
        stops = self._content.settings.horizon_blend_stops
        stops.set_min(min)
        stops.set_start(start)
        stops.set_mie_start(mie_start)
        stops.set_max(max)
        return self

    def rayleigh_strength(self, value: float | list[KeyFrame]) -> "AtmosphericSettings":
        """How strong the atmosphere's rayleigh scattering term is.

        Args:
            value (float | list[KeyFrame]): Rayleigh scattering strength.
        """
        self._content.settings.set_rayleigh_strength(value)
        return self

    def sun_mie_strength(self, value: float | list[KeyFrame]) -> "AtmosphericSettings":
        """How strong the sun's mie scattering term is.

        Args:
            value (float | list[KeyFrame]): Sun Mie scattering strength.
        """
        self._content.settings.set_sun_mie_strength(value)
        return self

    def moon_mie_strength(self, value: float | list[KeyFrame]) -> "AtmosphericSettings":
        """How strong the moon's mie scattering term is.

        Args:
            value (float | list[KeyFrame]): Moon Mie scattering strength.
        """
        self._content.settings.set_moon_mie_strength(value)
        return self

    def sun_glare_shape(self, value: float | list[KeyFrame]) -> "AtmosphericSettings":
        """How the lobe of the mie scattering is shaped.

        Args:
            value (float | list[KeyFrame]): Sun glare shape factor.
        """
        self._content.settings.set_sun_glare_shape(value)
        return self

    def sky_zenith_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]
    ) -> "AtmosphericSettings":
        """The RGB color of the zenith region of the atmosphere. Supports RGB array or HEX string.

        Args:
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]): Sky zenith color.
        """
        self._content.settings.set_sky_zenith_color(color)
        return self

    def sky_horizon_color(
        self, color: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]
    ) -> "AtmosphericSettings":
        """The RGB color of the horizon region of the atmosphere. Supports RGB array or HEX string.

        Args:
            color (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | list[KeyFrame]): Sky horizon color.
        """
        self._content.settings.set_sky_horizon_color(color)
        return self
