import os

from anvil.api.core.types import (
    Color,
)
from anvil.api.pbr.texture_set import KeyFrame
from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilFormatter
from anvil.lib.schemas import AddonObject, JsonSchemes


class AtmosphericSettings(AddonObject):
    """Atmospheric settings for Vibrant Visuals (PBR) rendering.

    Allows customizing Rayleigh and Mie scattering, glare, blend stops, and sky colors.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "atmospherics")
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
        if name == "default_atmospherics":
            super().__init__("atmospherics")
            self.content(
                JsonSchemes.atmosphere_settings(
                    f"{CONFIG.NAMESPACE}:default_atmospherics"
                )
            )
        else:
            super().__init__(name)
            self.content(JsonSchemes.atmosphere_settings(self.identifier))

    def horizon_blend_stops(
        self,
        min: float | list[KeyFrame],
        start: float | list[KeyFrame],
        mie_start: float | list[KeyFrame],
        max: float | list[KeyFrame],
    ):
        """How the atmosphere is divided up.

        Parameters:
            min (float | list[KeyFrame]): The minimum horizon height.
            start (float | list[KeyFrame]): The height relative to the horizon where the zenith contribution will take over.
            mie_start (float | list[KeyFrame]): The height relative to the horizon where mie scattering begins.
            max (float | list[KeyFrame]): The maximum horizon height.
        """
        self._content["minecraft:atmosphere_settings"]["horizon_blend_stops"] = {
            "min": (
                min if isinstance(min, (int, float)) else KeyFrame.keyframe_dict(min)
            ),
            "start": (
                start
                if isinstance(start, (int, float))
                else KeyFrame.keyframe_dict(start)
            ),
            "mie_start": (
                mie_start
                if isinstance(mie_start, (int, float))
                else KeyFrame.keyframe_dict(mie_start)
            ),
            "max": (
                max if isinstance(max, (int, float)) else KeyFrame.keyframe_dict(max)
            ),
        }

    def rayleigh_strength(self, value: float | list[KeyFrame]):
        """How strong the atmosphere's rayleigh scattering term is.

        Parameters:
            value (float | list[KeyFrame]): Rayleigh scattering strength.
        """
        self._content["minecraft:atmosphere_settings"]["rayleigh_strength"] = (
            value if isinstance(value, (int, float)) else KeyFrame.keyframe_dict(value)
        )

    def sun_mie_strength(self, value: float | list[KeyFrame]):
        """How strong the sun's mie scattering term is.

        Parameters:
            value (float | list[KeyFrame]): Sun Mie scattering strength.
        """
        self._content["minecraft:atmosphere_settings"]["sun_mie_strength"] = (
            value if isinstance(value, (int, float)) else KeyFrame.keyframe_dict(value)
        )

    def moon_mie_strength(self, value: float | list[KeyFrame]):
        """How strong the moon's mie scattering term is.

        Parameters:
            value (float | list[KeyFrame]): Moon Mie scattering strength.
        """
        self._content["minecraft:atmosphere_settings"]["moon_mie_strength"] = (
            value if isinstance(value, (int, float)) else KeyFrame.keyframe_dict(value)
        )

    def sun_glare_shape(self, value: float | list[KeyFrame]):
        """How the lobe of the mie scattering is shaped.

        Parameters:
            value (float | list[KeyFrame]): Sun glare shape factor.
        """
        self._content["minecraft:atmosphere_settings"]["sun_glare_shape"] = (
            value if isinstance(value, (int, float)) else KeyFrame.keyframe_dict(value)
        )

    def sky_zenith_color(self, color: Color | list[KeyFrame]):
        """The RGB color of the zenith region of the atmosphere. Supports RGB array or HEX string.

        Parameters:
            color (Color | list[KeyFrame]): Sky zenith color.
        """
        is_kf = (
            isinstance(color, list)
            and len(color) > 0
            and isinstance(color[0], KeyFrame)
        )
        self._content["minecraft:atmosphere_settings"]["sky_zenith_color"] = (
            KeyFrame.keyframe_dict(color)
            if is_kf
            else AnvilFormatter.convert_color(color)
        )

    def sky_horizon_color(self, color: Color | list[KeyFrame]):
        """The RGB color of the horizon region of the atmosphere. Supports RGB array or HEX string.

        Parameters:
            color (Color | list[KeyFrame]): Sky horizon color.
        """
        is_kf = (
            isinstance(color, list)
            and len(color) > 0
            and isinstance(color[0], KeyFrame)
        )
        self._content["minecraft:atmosphere_settings"]["sky_horizon_color"] = (
            KeyFrame.keyframe_dict(color)
            if is_kf
            else AnvilFormatter.convert_color(color)
        )
