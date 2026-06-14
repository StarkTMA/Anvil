import os
from typing import Literal

from anvil.api.core.types import (
    Color,
    Identifier,
)
from anvil.api.pbr.texture_set import KeyFrame
from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilFormatter, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftBlockDescriptor


class LightingSettings(AddonObject):
    """Global lighting settings for Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "lighting")
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

        if name == "default_lighting":
            super().__init__("global")
            self.content(
                JsonSchemes.lighting_settings(f"{CONFIG.NAMESPACE}:default_lighting")
            )
        else:

            super().__init__(name)
            self.content(JsonSchemes.lighting_settings(self.identifier))

    def orbital_lights(
        self,
        sun_illuminance: float | list[KeyFrame] | None = None,
        sun_color: Color | list[KeyFrame] | None = None,
        moon_illuminance: float | list[KeyFrame] | None = None,
        moon_color: Color | list[KeyFrame] | None = None,
        orbital_offset_degrees: float | list[KeyFrame] | None = None,
    ) -> None:
        """Configures the orbital celestial lights (sun and moon).

        Parameters:
            sun_illuminance (float | list[KeyFrame]): Brightness of the sun in lux (lx).
            sun_color (Color | list[KeyFrame]): Color contributed by the sun. Supports RGB array or HEX string.
            moon_illuminance (float | list[KeyFrame]): Brightness of the moon in lux (lx).
            moon_color (Color | list[KeyFrame]): Color contributed by the moon. Supports RGB array or HEX string.
            orbital_offset_degrees (float | list[KeyFrame]): Rotational offset of celestial bodies from standard orbital axis.
        """
        self._content["minecraft:lighting_settings"]["directional_lights"][
            "orbital"
        ] = {
            "sun": {
                "illuminance": (
                    sun_illuminance
                    if isinstance(sun_illuminance, (int, float))
                    else (
                        KeyFrame.keyframe_dict(sun_illuminance)
                        if sun_illuminance is not None
                        else None
                    )
                ),
                "color": (
                    KeyFrame.keyframe_dict(sun_color)
                    if isinstance(sun_color, list)
                    and len(sun_color) > 0
                    and isinstance(sun_color[0], KeyFrame)
                    else (
                        AnvilFormatter.convert_color(sun_color)
                        if sun_color is not None
                        else None
                    )
                ),
            },
            "moon": {
                "illuminance": (
                    moon_illuminance
                    if isinstance(moon_illuminance, (int, float))
                    else (
                        KeyFrame.keyframe_dict(moon_illuminance)
                        if moon_illuminance is not None
                        else None
                    )
                ),
                "color": (
                    KeyFrame.keyframe_dict(moon_color)
                    if isinstance(moon_color, list)
                    and len(moon_color) > 0
                    and isinstance(moon_color[0], KeyFrame)
                    else (
                        AnvilFormatter.convert_color(moon_color)
                        if moon_color is not None
                        else None
                    )
                ),
            },
            "orbital_offset_degrees": (
                orbital_offset_degrees
                if isinstance(orbital_offset_degrees, (int, float))
                else (
                    KeyFrame.keyframe_dict(orbital_offset_degrees)
                    if orbital_offset_degrees is not None
                    else None
                )
            ),
        }

    def flash_light(self, illuminance: float, color: Color) -> None:
        """Configures the End flash light source (exclusive to the End dimension).

        Parameters:
            illuminance (float): Peak brightness of the End flash in lux (lx).
            color (Color): Color contributed by the End flash. Supports RGB array or HEX string.
        """
        self._content["minecraft:lighting_settings"]["directional_lights"]["flash"] = {
            "illuminance": illuminance,
            "color": AnvilFormatter.convert_color(color),
        }

    def emissive(self, desaturation: float) -> None:
        """Configures global settings for emissive light sources.

        Parameters:
            desaturation (float): Factor (0.0 to 1.0) controlling how much the albedo of a given pixel is desaturated.
        """
        self._content["minecraft:lighting_settings"]["emissive"] = {
            "desaturation": clamp(desaturation, 0.0, 1.0)
        }

    def ambient(
        self, illuminance: float | list[KeyFrame], color: Color | list[KeyFrame]
    ) -> None:
        """Controls how surfaces are lit when there are no other light sources available.

        Parameters:
            illuminance (float | list[KeyFrame]): Minimum fallback light strength in lux (lx). Valid range: 0.0 to 5.0.
            color (Color | list[KeyFrame]): Color of the ambient fallback light. Supports RGB array or HEX string.
        """
        self._content["minecraft:lighting_settings"]["ambient"] = {
            "illuminance": (
                clamp(illuminance, 0.0, 5.0)
                if isinstance(illuminance, (int, float))
                else KeyFrame.keyframe_dict(
                    [KeyFrame(k.time, clamp(k.value, 0.0, 5.0)) for k in illuminance]
                )
            ),
            "color": (
                KeyFrame.keyframe_dict(color)
                if isinstance(color, list)
                and len(color) > 0
                and isinstance(color[0], KeyFrame)
                else AnvilFormatter.convert_color(color)
            ),
        }

    def sky(self, intensity: float | list[KeyFrame]) -> None:
        """Controls indirect lighting contribution from the sky.

        Parameters:
            intensity (float | list[KeyFrame]): Energy scaling factor. Valid range: 0.1 to 1.0.
        """
        self._content["minecraft:lighting_settings"]["sky"] = {
            "intensity": (
                clamp(intensity, 0.1, 1.0)
                if isinstance(intensity, (int, float))
                else KeyFrame.keyframe_dict(
                    [KeyFrame(k.time, clamp(k.value, 0.1, 1.0)) for k in intensity]
                )
            )
        }

    def queue(self):
        return super().queue()


class LocalLighting(AddonObject):
    """Local lighting configurations (point lights and static lights) for Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "local_lighting")
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
        block_identifier: MinecraftBlockDescriptor | Identifier,
        color: Color,
        light_type: Literal["static_light", "point_light"] = "point_light",
    ) -> None:
        """Adds a local light to the local lighting configuration.

        Parameters:
            block_identifier (MinecraftBlockDescriptor | Identifier): The identifier of the block that emits the light.
            color (Color): The color of the light.
            light_type (Literal["static_light", "point_light"]): The type of local light.
        """
        self._content["minecraft:local_light_settings"][str(block_identifier)] = {
            "light_color": AnvilFormatter.convert_color(color),
            "light_type": light_type,
        }

    def add_point_light(
        self, block_identifier: MinecraftBlockDescriptor | Identifier, color: Color
    ) -> None:
        """Adds a point light to the point lights configuration (legacy fallback).

        Parameters:
            block_identifier (MinecraftBlockDescriptor | Identifier): The identifier of the block that emits the light.
            color (Color): The color of the light.
        """
        self.add_local_light(block_identifier, color, "static_light")
