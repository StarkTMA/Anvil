from typing import Annotated, ClassVar, Literal

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import COLOR_GRADING_SETTINGS_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    Wrapped,
    json_field,
)

__all__ = ["ColorGradingSettings"]


class _ColorGrade(JsonObject):
    """Color grading of one tonal range, each value per RGB channel. Unset keys are left out."""

    contrast: Annotated[tuple[float, float, float], InRange(0.0, 4.0)] | None = None
    gain: Annotated[tuple[float, float, float], InRange(0.0, 10.0)] | None = None
    gamma: Annotated[tuple[float, float, float], InRange(0.0, 4.0)] | None = None
    offset: Annotated[tuple[float, float, float], InRange(-1.0, 1.0)] | None = None
    saturation: Annotated[tuple[float, float, float], InRange(0.0, 10.0)] | None = None

    def set_contrast(self, contrast: tuple[float, float, float]) -> None:
        """Sets the contrast multiplier, from 0.0 to 4.0."""
        self.contrast = contrast

    def set_gain(self, gain: tuple[float, float, float]) -> None:
        """Sets the multiplicative gain, from 0.0 to 10.0."""
        self.gain = gain

    def set_gamma(self, gamma: tuple[float, float, float]) -> None:
        """Sets the exponential gamma correction, from 0.0 to 4.0."""
        self.gamma = gamma

    def set_offset(self, offset: tuple[float, float, float]) -> None:
        """Sets the additive offset, from -1.0 to 1.0."""
        self.offset = offset

    def set_saturation(self, saturation: tuple[float, float, float]) -> None:
        """Sets the saturation intensity, from 0.0 to 10.0."""
        self.saturation = saturation


class _HighlightsGrade(_ColorGrade):
    """Color grading of the highlights, used when enabled."""

    __required__: ClassVar[tuple[str, ...]] = ("enabled",)

    enabled: bool | None = None
    highlightsMin: Annotated[float, InRange(1.0, 4.0)] | None = None

    def set_enabled(self, enabled: bool) -> None:
        """Turns highlight color grading on or off."""
        self.enabled = enabled

    def set_highlightsMin(self, highlightsMin: float) -> None:
        """Sets the average luminance multiplier above which a pixel is a highlight, from 1.0
        to 4.0."""
        self.highlightsMin = highlightsMin


class _ShadowsGrade(_ColorGrade):
    """Color grading of the shadows, used when enabled."""

    __required__: ClassVar[tuple[str, ...]] = ("enabled",)

    enabled: bool | None = None
    shadowsMax: Annotated[float, InRange(0.1, 1.0)] | None = None

    def set_enabled(self, enabled: bool) -> None:
        """Turns shadow color grading on or off."""
        self.enabled = enabled

    def set_shadowsMax(self, shadowsMax: float) -> None:
        """Sets the average luminance multiplier below which a pixel is a shadow, from 0.1 to
        1.0."""
        self.shadowsMax = shadowsMax


class _Temperature(JsonObject):
    """How warm or cool the whole scene is. Unset keys are left out, so the game uses 6500
    and `white_balance`."""

    enabled: bool | None = None
    temperature: Annotated[float, InRange(1000.0, 15000.0)] | None = None
    type: Literal["white_balance", "color_temperature"] | None = None

    def set_enabled(self, enabled: bool) -> None:
        """Turns the temperature grade on or off."""
        self.enabled = enabled

    def set_temperature(self, temperature: float) -> None:
        """Sets the temperature in Kelvin, from 1000.0 to 15000.0."""
        self.temperature = temperature

    def set_type(self, type: Literal["white_balance", "color_temperature"]) -> None:
        """Sets how the temperature scale is read."""
        self.type = type


class _ColorGrading(JsonObject):
    """The `color_grading` object. Parts with nothing set are left out."""

    midtones: _ColorGrade = json_field(default_factory=_ColorGrade)
    highlights: _HighlightsGrade = json_field(default_factory=_HighlightsGrade)
    shadows: _ShadowsGrade = json_field(default_factory=_ShadowsGrade)
    temperature: _Temperature = json_field(default_factory=_Temperature)


class _ToneMapping(JsonObject):
    """The `tone_mapping` object, which remaps HDR colors to SDR for display."""

    __required__: ClassVar[tuple[str, ...]] = ("operator",)

    operator: (
        Literal[
            "reinhard",
            "reinhard_luma",
            "reinhard_luminance",
            "hable",
            "aces",
            "generic",
        ]
        | None
    ) = None

    def set_operator(
        self,
        operator: Literal[
            "reinhard",
            "reinhard_luma",
            "reinhard_luminance",
            "hable",
            "aces",
            "generic",
        ],
    ) -> None:
        """Sets the tone mapping operator."""
        self.operator = operator


class _ColorGradingSettings(JsonObject):
    """The `minecraft:color_grading_settings` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    color_grading: _ColorGrading = json_field(default_factory=_ColorGrading)
    tone_mapping: _ToneMapping = json_field(default_factory=_ToneMapping)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The settings have no identifier.")


class _ColorGradingSettingsFile(JsonObject):
    """The content of a `color_grading/*.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:color_grading_settings",
    )

    format_version: str = json_field(default=COLOR_GRADING_SETTINGS_VERSION, init=False)
    settings: _ColorGradingSettings = json_field(
        key="minecraft:color_grading_settings", default_factory=_ColorGradingSettings
    )


class ColorGradingSettings(JsonFile):
    """Color grading and tone mapping configuration settings for Vibrant Visuals (PBR) rendering.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/colorgradingtonemappingcustomization)
    """

    _document = _ColorGradingSettingsFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "color_grading"
    _object_type = "Color Grading Settings"

    def __init__(self, name: str = "default_color_grading") -> None:
        """Initializes a ColorGradingSettings instance.

        Raises:
            ValueError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__(
            "color_grading" if name == "default_color_grading" else name,
            identifier=name,
        )
        self._content.settings.set_description(self.identifier)

    def midtones(
        self,
        contrast: tuple[float, float, float] | None = None,
        gain: tuple[float, float, float] | None = None,
        gamma: tuple[float, float, float] | None = None,
        offset: tuple[float, float, float] | None = None,
        saturation: tuple[float, float, float] | None = None,
    ) -> "ColorGradingSettings":
        """Sets color grading parameters for midtones (or globally if highlights/shadows are disabled).

        Args:
            contrast (tuple[float, float, float], optional): Tonal range contrast multiplier per RGB channel. Valid range: 0.0 to 4.0.
            gain (tuple[float, float, float], optional): Multiplicative gain per RGB channel. Valid range: 0.0 to 10.0.
            gamma (tuple[float, float, float], optional): Exponential gamma correction per RGB channel. Valid range: 0.0 to 4.0.
            offset (tuple[float, float, float], optional): Additive offset per RGB channel. Valid range: -1.0 to 1.0.
            saturation (tuple[float, float, float], optional): Saturation intensity per RGB channel. Valid range: 0.0 to 10.0.
        """
        mid = self._content.settings.color_grading.midtones
        if contrast is not None:
            mid.set_contrast(contrast)
        if gain is not None:
            mid.set_gain(gain)
        if gamma is not None:
            mid.set_gamma(gamma)
        if offset is not None:
            mid.set_offset(offset)
        if saturation is not None:
            mid.set_saturation(saturation)
        return self

    def highlights(
        self,
        highlightsMin: float | None = None,
        contrast: tuple[float, float, float] | None = None,
        gain: tuple[float, float, float] | None = None,
        gamma: tuple[float, float, float] | None = None,
        offset: tuple[float, float, float] | None = None,
        saturation: tuple[float, float, float] | None = None,
    ) -> "ColorGradingSettings":
        """Sets color grading parameters for highlights.

        Args:
            enabled (bool): Whether to enable highlight color grading.
            highlightsMin (float, optional): Multiplier for average luminance determining highlight threshold. Valid range: 1.0 to 4.0.
            contrast (tuple[float, float, float], optional): Highlight contrast multiplier per RGB channel. Valid range: 0.0 to 4.0.
            gain (tuple[float, float, float], optional): Highlight multiplicative gain per RGB channel. Valid range: 0.0 to 10.0.
            gamma (tuple[float, float, float], optional): Highlight exponential gamma correction per RGB channel. Valid range: 0.0 to 4.0.
            offset (tuple[float, float, float], optional): Highlight additive offset per RGB channel. Valid range: -1.0 to 1.0.
            saturation (tuple[float, float, float], optional): Highlight saturation intensity per RGB channel. Valid range: 0.0 to 10.0.
        """

        high = self._content.settings.color_grading.highlights
        high.set_enabled(True)
        if highlightsMin is not None:
            high.set_highlightsMin(highlightsMin)
        if contrast is not None:
            high.set_contrast(contrast)
        if gain is not None:
            high.set_gain(gain)
        if gamma is not None:
            high.set_gamma(gamma)
        if offset is not None:
            high.set_offset(offset)
        if saturation is not None:
            high.set_saturation(saturation)
        return self

    def shadows(
        self,
        shadowsMax: float | None = None,
        contrast: tuple[float, float, float] | None = None,
        gain: tuple[float, float, float] | None = None,
        gamma: tuple[float, float, float] | None = None,
        offset: tuple[float, float, float] | None = None,
        saturation: tuple[float, float, float] | None = None,
    ) -> "ColorGradingSettings":
        """Sets color grading parameters for shadows.

        Args:
            enabled (bool): Whether to enable shadow color grading.
            shadowsMax (float, optional): Multiplier for average luminance determining shadow threshold. Valid range: 0.1 to 1.0.
            contrast (tuple[float, float, float], optional): Shadow contrast multiplier per RGB channel. Valid range: 0.0 to 4.0.
            gain (tuple[float, float, float], optional): Shadow multiplicative gain per RGB channel. Valid range: 0.0 to 10.0.
            gamma (tuple[float, float, float], optional): Shadow exponential gamma correction per RGB channel. Valid range: 0.0 to 4.0.
            offset (tuple[float, float, float], optional): Shadow additive offset per RGB channel. Valid range: -1.0 to 1.0.
            saturation (tuple[float, float, float], optional): Shadow saturation intensity per RGB channel. Valid range: 0.0 to 10.0.
        """
        shad = self._content.settings.color_grading.shadows
        shad.set_enabled(True)
        if shadowsMax is not None:
            shad.set_shadowsMax(shadowsMax)
        if contrast is not None:
            shad.set_contrast(contrast)
        if gain is not None:
            shad.set_gain(gain)
        if gamma is not None:
            shad.set_gamma(gamma)
        if offset is not None:
            shad.set_offset(offset)
        if saturation is not None:
            shad.set_saturation(saturation)
        return self

    def temperature_grade(
        self,
        temp_value: float | None = None,
        type: Literal["white_balance", "color_temperature"] | None = None,
    ) -> "ColorGradingSettings":
        """Globally adjusts how warm or cool the scene is.

        Args:
            temp_value (float, optional): Overall image temperature in Kelvin. Default is 6500.0. Valid range: 1000.0 to 15000.0.
            type (Literal["white_balance", "color_temperature"], optional): Inverts scale logic. Default is "white_balance".
        """
        temp = self._content.settings.color_grading.temperature
        temp.set_enabled(True)
        if temp_value is not None:
            temp.set_temperature(temp_value)
        if type is not None:
            temp.set_type(type)
        return self

    def tone_mapping(
        self,
        operator: Literal[
            "reinhard",
            "reinhard_luma",
            "reinhard_luminance",
            "hable",
            "aces",
            "generic",
        ],
    ) -> "ColorGradingSettings":
        """Remaps HDR colors to SDR-space for display.

        Args:
            operator (Literal["reinhard", "reinhard_luma", "reinhard_luminance", "hable", "aces", "generic"]): The tone mapping operator.
        """
        self._content.settings.tone_mapping.set_operator(operator)
        return self
