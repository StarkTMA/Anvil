import os
from typing import Literal

from anvil.api.core.types import (
    Vector3D,
)
from anvil.lib.config import CONFIG
from anvil.lib.lib import clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


class ColorGradingSettings(AddonObject):
    """Color grading and tone mapping configuration settings for Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "color_grading")
    _object_type = "Color Grading Settings"

    def __init__(self, name: str = "default_color_grading") -> None:
        """Initializes a ColorGradingSettings instance.

        Raises:
            RuntimeError: If PBR is not enabled in the config.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        if name == "default_color_grading":
            super().__init__("color_grading")
            self.content(
                JsonSchemes.color_grading_settings(
                    f"{CONFIG.NAMESPACE}:default_color_grading"
                )
            )
        else:
            super().__init__(name)
            self.content(JsonSchemes.color_grading_settings(self.identifier))

    def midtones(
        self,
        contrast: Vector3D | None = None,
        gain: Vector3D | None = None,
        gamma: Vector3D | None = None,
        offset: Vector3D | None = None,
        saturation: Vector3D | None = None,
    ):
        """Sets color grading parameters for midtones (or globally if highlights/shadows are disabled).

        Parameters:
            contrast (Vector3D, optional): Tonal range contrast multiplier per RGB channel. Valid range: 0.0 to 4.0.
            gain (Vector3D, optional): Multiplicative gain per RGB channel. Valid range: 0.0 to 10.0.
            gamma (Vector3D, optional): Exponential gamma correction per RGB channel. Valid range: 0.0 to 4.0.
            offset (Vector3D, optional): Additive offset per RGB channel. Valid range: -1.0 to 1.0.
            saturation (Vector3D, optional): Saturation intensity per RGB channel. Valid range: 0.0 to 10.0.
        """
        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "midtones", {}
        )
        mid = self._content["minecraft:color_grading_settings"]["color_grading"][
            "midtones"
        ]
        if contrast is not None:
            mid["contrast"] = [clamp(c, 0.0, 4.0) for c in contrast]
        if gain is not None:
            mid["gain"] = [clamp(c, 0.0, 10.0) for c in gain]
        if gamma is not None:
            mid["gamma"] = [clamp(c, 0.0, 4.0) for c in gamma]
        if offset is not None:
            mid["offset"] = [clamp(c, -1.0, 1.0) for c in offset]
        if saturation is not None:
            mid["saturation"] = [clamp(c, 0.0, 10.0) for c in saturation]

    def highlights(
        self,
        highlightsMin: float | None = None,
        contrast: list[float] | None = None,
        gain: list[float] | None = None,
        gamma: list[float] | None = None,
        offset: list[float] | None = None,
        saturation: list[float] | None = None,
    ):
        """Sets color grading parameters for highlights.

        Parameters:
            enabled (bool): Whether to enable highlight color grading.
            highlightsMin (float, optional): Multiplier for average luminance determining highlight threshold. Valid range: 1.0 to 4.0.
            contrast (list[float], optional): Highlight contrast multiplier per RGB channel. Valid range: 0.0 to 4.0.
            gain (list[float], optional): Highlight multiplicative gain per RGB channel. Valid range: 0.0 to 10.0.
            gamma (list[float], optional): Highlight exponential gamma correction per RGB channel. Valid range: 0.0 to 4.0.
            offset (list[float], optional): Highlight additive offset per RGB channel. Valid range: -1.0 to 1.0.
            saturation (list[float], optional): Highlight saturation intensity per RGB channel. Valid range: 0.0 to 10.0.
        """

        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "highlights", {}
        )
        high = self._content["minecraft:color_grading_settings"]["color_grading"][
            "highlights"
        ]
        high["enabled"] = True
        if highlightsMin is not None:
            high["highlightsMin"] = clamp(highlightsMin, 1.0, 4.0)
        if contrast is not None:
            high["contrast"] = [clamp(c, 0.0, 4.0) for c in contrast]
        if gain is not None:
            high["gain"] = [clamp(c, 0.0, 10.0) for c in gain]
        if gamma is not None:
            high["gamma"] = [clamp(c, 0.0, 4.0) for c in gamma]
        if offset is not None:
            high["offset"] = [clamp(c, -1.0, 1.0) for c in offset]
        if saturation is not None:
            high["saturation"] = [clamp(c, 0.0, 10.0) for c in saturation]

    def shadows(
        self,
        shadowsMax: float | None = None,
        contrast: list[float] | None = None,
        gain: list[float] | None = None,
        gamma: list[float] | None = None,
        offset: list[float] | None = None,
        saturation: list[float] | None = None,
    ):
        """Sets color grading parameters for shadows.

        Parameters:
            enabled (bool): Whether to enable shadow color grading.
            shadowsMax (float, optional): Multiplier for average luminance determining shadow threshold. Valid range: 0.1 to 1.0.
            contrast (list[float], optional): Shadow contrast multiplier per RGB channel. Valid range: 0.0 to 4.0.
            gain (list[float], optional): Shadow multiplicative gain per RGB channel. Valid range: 0.0 to 10.0.
            gamma (list[float], optional): Shadow exponential gamma correction per RGB channel. Valid range: 0.0 to 4.0.
            offset (list[float], optional): Shadow additive offset per RGB channel. Valid range: -1.0 to 1.0.
            saturation (list[float], optional): Shadow saturation intensity per RGB channel. Valid range: 0.0 to 10.0.
        """
        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "shadows", {}
        )
        shad = self._content["minecraft:color_grading_settings"]["color_grading"][
            "shadows"
        ]
        shad["enabled"] = True
        if shadowsMax is not None:
            shad["shadowsMax"] = clamp(shadowsMax, 0.1, 1.0)
        if contrast is not None:
            shad["contrast"] = [clamp(c, 0.0, 4.0) for c in contrast]
        if gain is not None:
            shad["gain"] = [clamp(c, 0.0, 10.0) for c in gain]
        if gamma is not None:
            shad["gamma"] = [clamp(c, 0.0, 4.0) for c in gamma]
        if offset is not None:
            shad["offset"] = [clamp(c, -1.0, 1.0) for c in offset]
        if saturation is not None:
            shad["saturation"] = [clamp(c, 0.0, 10.0) for c in saturation]

    def temperature_grade(
        self,
        temp_value: float | None = None,
        type: Literal["white_balance", "color_temperature"] | None = None,
    ):
        """Globally adjusts how warm or cool the scene is.

        Parameters:
            temp_value (float, optional): Overall image temperature in Kelvin. Default is 6500.0. Valid range: 1000.0 to 15000.0.
            type (Literal["white_balance", "color_temperature"], optional): Inverts scale logic. Default is "white_balance".
        """
        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "temperature", {}
        )
        temp = self._content["minecraft:color_grading_settings"]["color_grading"][
            "temperature"
        ]
        temp["enabled"] = True
        if temp_value is not None:
            temp["temperature"] = clamp(temp_value, 1000.0, 15000.0)
        if type is not None:
            temp["type"] = type

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
    ):
        """Remaps HDR colors to SDR-space for display.

        Parameters:
            operator (Literal["reinhard", "reinhard_luma", "reinhard_luminance", "hable", "aces", "generic"]): The tone mapping operator.
        """
        self._content["minecraft:color_grading_settings"].setdefault("tone_mapping", {})
        self._content["minecraft:color_grading_settings"]["tone_mapping"][
            "operator"
        ] = operator
