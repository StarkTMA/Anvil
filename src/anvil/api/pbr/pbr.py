import os
from ast import List
from dataclasses import dataclass
from typing import Dict, Literal, overload

from anvil.api.core.types import (
    RGB,
    RGB255,
    RGBA,
    RGBA255,
    Block,
    Color,
    HexRGB,
    HexRGBA,
    Identifier,
    Vector3D,
)
from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG
from anvil.lib.lib import CopyFiles, FileExists, clamp, convert_color
from anvil.lib.schemas import AddonObject, JsonSchemes


def _is_color_value(value) -> bool:
    """
    Check if a value is a color value (not a texture file name).
    Returns True for RGB/RGBA tuples and hex color strings.
    Returns False for texture file names (plain strings without # prefix).
    """
    if value is None:
        return False

    # Check for tuple types (RGB, RGBA)
    if isinstance(value, tuple):
        return True

    # Check for hex color strings (start with #)
    if isinstance(value, str) and value.startswith("#"):
        return True

    # Everything else (including plain strings) are treated as texture file names
    return False


def _is_texture_filename(value) -> bool:
    """
    Check if a value is a texture filename (not a color value).
    Returns True for strings that don't start with # (texture file names).
    Returns False for color values (tuples, hex strings, None).
    """
    if value is None:
        return False

    # Only plain strings (not starting with #) are texture filenames
    return isinstance(value, str) and not value.startswith("#")


@dataclass
class KeyFrame:
    time: float
    value: float

    @classmethod
    def keyframe_dict(
        cls,
        keyframes: list["KeyFrame"],
    ) -> dict[str, float]:
        """
        Converts a list of KeyFrame into a dict suitable for Minecraft JSON.
        Example input: [KeyFrame(0,1), ...]
        Example output: {"0.0": 1, ...}
        """
        return {str(clamp(k.time, 0.0, 1.0)): k.value for k in keyframes}


@dataclass(frozen=True)
class TextureComponents:
    """PBR texture components for blocks, items, and entities.

    Attributes:
        color: Base color texture filename or color value
        normal: Normal map texture filename or color value (mutually exclusive with heightmap)
        heightmap: Height/displacement map texture filename or color value (mutually exclusive with normal)
        mer: MER texture filename or color value (mutually exclusive with mers)
        mers: MERS texture filename or color value (mutually exclusive with mer)
    """

    color: str
    normal: str | Color | None = None
    height: str | Color | None = None
    mer: str | Color | None = None
    mers: str | Color | None = None

    def has_aux(self) -> bool:
        return bool(self.normal or self.height or self.mer or self.mers)


class TextureSet(AddonObject):
    _object_type = "Texture Set"
    _extension = ".texture_set.json"
    _path = os.path.join(
        CONFIG.RP_PATH,
        "textures",
        CONFIG.NAMESPACE,
        CONFIG.PROJECT_NAME,
    )

    def __init__(self, texture_name: str, target: str) -> None:
        super().__init__(texture_name)
        self.content(JsonSchemes.texture_set())
        self._target = target
        if not CONFIG._PBR:
            raise RuntimeError("Texture sets require PBR to be enabled in the config.")

    def __validate(
        self,
        components: TextureComponents,
    ):

        color_map: dict[str, str] = {}
        if components.normal is not None and components.height is not None:
            raise ValueError("Normal and heightmap textures are mutually exclusive.")
        if components.mer is not None and components.mers is not None:
            raise ValueError(
                "Metalness, emissive, roughness and subsurface textures are mutually exclusive."
            )

        if _is_color_value(components.color):
            color_map["color"] = convert_color(components.color, HexRGB)
        if _is_color_value(components.normal):
            color_map["normal"] = convert_color(components.normal, HexRGB)
        if _is_color_value(components.height):
            color_map["heightmap"] = convert_color(components.height, HexRGB)
        if _is_color_value(components.mer):
            color_map["metalness_emissive_roughness"] = convert_color(
                components.mer, HexRGB
            )
        if _is_color_value(components.mers):
            color_map["metalness_emissive_roughness_subsurface"] = convert_color(
                components.mers, HexRGBA
            )

        return color_map

    def __set_individual_textures(
        self,
        source: str,
        components: TextureComponents,
    ):
        color_map = self.__validate(components)

        color_map["color"] = components.color
        self._queued_textures: dict[str, dict[str, list[str]]] = {
            source: {components.color: [components.color]}
        }
        if not FileExists(os.path.join("assets", source, f"{components.color}.png")):
            raise FileNotFoundError(
                f"Color texture file '{components.color}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
            )

        if _is_texture_filename(components.normal):
            if not FileExists(
                os.path.join("assets", source, f"{components.normal}.png")
            ):
                raise FileNotFoundError(
                    f"Normal texture file '{components.normal}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["normal"] = components.normal
            self._queued_textures.get(source).get(components.color).append(
                components.normal
            )

        if _is_texture_filename(components.height):
            if not FileExists(
                os.path.join("assets", source, f"{components.height}.png")
            ):
                raise FileNotFoundError(
                    f"Height texture file '{components.height}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["heightmap"] = components.height
            self._queued_textures.get(source).get(components.color).append(
                components.height
            )

        if _is_texture_filename(components.mer):
            if not FileExists(os.path.join("assets", source, f"{components.mer}.png")):
                raise FileNotFoundError(
                    f"MER texture file '{components.mer}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["metalness_emissive_roughness"] = components.mer
            self._queued_textures.get(source).get(components.color).append(
                components.mer
            )

        if _is_texture_filename(components.mers):
            if not FileExists(os.path.join("assets", source, f"{components.mers}.png")):
                raise FileNotFoundError(
                    f"MERS texture file '{components.mers}.png' does not exist in 'assets/{source}'. {self._object_type}[{self._name}]"
                )
            color_map["metalness_emissive_roughness_subsurface"] = components.mers
            self._queued_textures.get(source).get(components.color).append(
                components.mers
            )

        self._content["minecraft:texture_set"].update(color_map)
        self._path = os.path.join(self._path, self._target)

    def set_particle_textures(
        self,
        components: TextureComponents,
    ):
        self.__set_individual_textures(
            "particles",
            components,
        )

    def set_item_textures(
        self,
        components: TextureComponents,
    ):
        self.__set_individual_textures("textures/items", components)

    def set_blockbench_textures(
        self,
        blockbench_name: str,
        components: TextureComponents,
    ):
        color_map = self.__validate(components)

        self._blockbench = _Blockbench(blockbench_name, self._target)
        self._blockbench.textures.queue_texture(components.color)
        color_map["color"] = components.color
        if _is_texture_filename(components.normal):
            self._blockbench.textures.queue_texture(components.normal)
            color_map["normal"] = components.normal
        if _is_texture_filename(components.height):
            self._blockbench.textures.queue_texture(components.height)
            color_map["heightmap"] = components.height
        if _is_texture_filename(components.mer):
            self._blockbench.textures.queue_texture(components.mer)
            color_map["metalness_emissive_roughness"] = components.mer
        if _is_texture_filename(components.mers):
            self._blockbench.textures.queue_texture(components.mers)
            color_map["metalness_emissive_roughness_subsurface"] = components.mers

        self._path = os.path.join(self._path, self._target, blockbench_name)
        self._content["minecraft:texture_set"].update(color_map)

    def _export(self):
        if hasattr(self, "_queued_textures"):
            for source, textures in self._queued_textures.items():
                for color, texture_list in textures.items():
                    for texture in texture_list:
                        CopyFiles(
                            os.path.join("assets", source),
                            os.path.join(
                                CONFIG.RP_PATH,
                                "textures",
                                CONFIG.NAMESPACE,
                                CONFIG.PROJECT_NAME,
                                self._target,
                            ),
                            f"{texture}.png",
                        )

        if len(self._content["minecraft:texture_set"].keys()) > 1:
            super()._export()


class AtmosphericSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "atmospherics")
    _object_type = "Atmospheric Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("atmospherics")
        self.content(
            JsonSchemes.atmosphere_settings(f"{CONFIG.NAMESPACE}:atmosphere_settings")
        )

    def horizon_blend_stops(
        self,
        min: list[KeyFrame],
        start: list[KeyFrame],
        mie_start: list[KeyFrame],
        max: list[KeyFrame],
    ):
        self._content["horizon_blend_stops"] = {
            "min": KeyFrame.keyframe_dict(min),
            "start": KeyFrame.keyframe_dict(start),
            "mie_start": KeyFrame.keyframe_dict(mie_start),
            "max": KeyFrame.keyframe_dict(max),
        }

    def rayleigh_strength(self, keyframe: list[KeyFrame]):
        self._content["rayleigh_strength"] = KeyFrame.keyframe_dict(keyframe)

    def sun_mie_strength(self, keyframe: list[KeyFrame]):
        self._content["sun_mie_strength"] = KeyFrame.keyframe_dict(keyframe)

    def moon_mie_strength(self, keyframe: list[KeyFrame]):
        self._content["moon_mie_strength"] = KeyFrame.keyframe_dict(keyframe)

    def sun_glare_shape(self, keyframe: list[KeyFrame]):
        self._content["sun_glare_shape"] = KeyFrame.keyframe_dict(keyframe)

    def sky_zenith_color(self, keyframe: list[KeyFrame]):
        self._content["sky_zenith_color"] = KeyFrame.keyframe_dict(keyframe)

    def sky_horizon_color(self, keyframe: dict[float, RGB]):
        self._content["sky_horizon_color"] = KeyFrame.keyframe_dict(keyframe)


class FogSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "fog")
    _object_type = "Fog Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("fog")
        self.content(JsonSchemes.fog_settings(f"{CONFIG.NAMESPACE}:fog_settings"))

    def water_density(self, max_density: float, uniform: bool = False):
        self._content["minecraft:fog_settings"]["volumetric"]["density"]["water"] = {
            "max_density": clamp(max_density, 0.0, 1.0),
            "uniform": uniform,
        }

    def air_density(
        self,
        max_density: float,
        zero_density_height: float = 0.0,
        max_density_height: float = 0.0,
    ):
        self._content["minecraft:fog_settings"]["volumetric"]["density"]["air"] = {
            "max_density": clamp(max_density, 0.0, 1.0),
            "zero_density_height": zero_density_height,
            "max_density_height": max_density_height,
        }

    def media_coefficients(
        self,
        water_scattering: tuple[float, float, float] = (0, 0, 0),
        water_absorption: tuple[float, float, float] = (0, 0, 0),
        air_scattering: tuple[float, float, float] = (0, 0, 0),
        air_absorption: tuple[float, float, float] = (0, 0, 0),
    ):
        self._content["minecraft:fog_settings"]["volumetric"]["media_coefficients"] = {
            "water": {
                "scattering": [clamp(k, 0, 1) for k in water_scattering],
                "absorption": [clamp(k, 0, 1) for k in water_absorption],
            },
            "air": {
                "scattering": [clamp(k, 0, 1) for k in air_scattering],
                "absorption": [clamp(k, 0, 1) for k in air_absorption],
            },
        }


class ShadowSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "shadows")
    _object_type = "Shadow Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("shadows")
        self.content(JsonSchemes.shadow_settings(f"{CONFIG.NAMESPACE}:shadow_settings"))

    def shadow_style(
        self, style: Literal["blocky_shadows", "soft_shadows"], texel_size: float = 16
    ):
        self._content["minecraft:shadow_settings"]["shadow_style"] = style
        self._content["minecraft:shadow_settings"]["texel_size"] = texel_size


class WaterSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "water")
    _object_type = "Water Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("water_settings")
        self.content(JsonSchemes.water_settings(f"{CONFIG.NAMESPACE}:water_settings"))

    def particle_concentrations(
        self,
        cdom: float | None = None,
        chlorophyll: float | None = None,
        suspended_sediment: float | None = None,
    ):
        """
        The composition of particles in a body of water determines its color and how light behaves as it
        travels through the water. We've boiled them down to three concentrations in mg/L. Use these values
        to simulate crystal clear lakes, deep oceans, or muddy rivers.
        Parameters:
            cdom (float | None): Concentration of colored dissolved organic matter (CDOM) in the water.
            chlorophyll (float | None): Concentration of chlorophyll in the water.
            suspended_sediment (float | None): Concentration of suspended sediment in the water.
        """
        pc = self._content["minecraft:water_settings"].setdefault(
            "particle_concentrations", {}
        )
        if cdom is not None:
            pc["cdom"] = clamp(cdom, 0.0, 15.0)
        if chlorophyll is not None:
            pc["chlorophyll"] = clamp(chlorophyll, 0.0, 10.0)
        if suspended_sediment is not None:
            pc["suspended_sediment"] = clamp(suspended_sediment, 0.0, 300.0)

    def waves(
        self,
        enabled: bool | None = None,
        depth: float | None = None,
        direction_increment: float | None = None,
        frequency: float | None = None,
        frequency_scaling: float | None = None,
        mix: float | None = None,
        octaves: int | None = None,
        pull: float | None = None,
        sampleWidth: float | None = None,
        shape: float | None = None,
        speed: float | None = None,
        speed_scaling: float | None = None,
    ):
        """
        Waves are an optional effect that can be used to complement water surface animations to make your water appear more
        realistic. You can blend them with existing water texture animations, or replace them entirely.
        The waves in Vibrant Visuals are purely an image-based effect—waves don't actually move the vertices of the water
        surface, so the water surface geometry will remain unchanged.
        Parameters:
            enabled (bool, optional): Whether or not waves are on or off.
            depth (float, optional): Controls the amount of wave displacement. Valid range: 0.0 to 3.0.
            direction_increment (float, optional): Controls how much the heading changes between each octave. Valid range: 0.0 to 360.0.
            frequency (float, optional): Controls the size of individual waves; higher values create more tightly packed waves. Valid range: 0.01 to 3.0.
            frequency_scaling (float, optional): Controls how much frequencies change in subsequent octaves. Valid range: 0.0 to 2.0.
            mix (float, optional): Controls how much each octave will blend into the neighboring octave. Valid range: 0.0 to 1.0.
            octaves (int, optional): Determines how many layers of waves to simulate; high values result in more complex waves. Valid range: 1 to 30.
            pull (float, optional): Controls how much smaller waves are pulled into larger ones. Valid range: -1.0 to 1.0.
            sampleWidth (float, optional): Controls the resolution of the fractal effect; higher values result in smoother waves. Valid range: 0.01 to 1.0.
            shape (float, optional): Adjusts the shape of the wave. Valid range: 1.0 to 10.0.
            speed (float, optional): Controls the starting speed of the first waves. Valid range: 0.01 to 10.0.
            speed_scaling (float, optional): Controls how much faster/slower subsequent octaves move. Valid range: 0.0 to 2.0.
        """

        waves = self._content["minecraft:water_settings"].setdefault("waves", {})
        if enabled is not None:
            waves["enabled"] = enabled
        if depth is not None:
            waves["depth"] = clamp(depth, 0.0, 3.0)
        if direction_increment is not None:
            waves["direction_increment"] = clamp(direction_increment, 0.0, 360.0)
        if frequency is not None:
            waves["frequency"] = clamp(frequency, 0.01, 3.0)
        if frequency_scaling is not None:
            waves["frequency_scaling"] = clamp(frequency_scaling, 0.0, 2.0)
        if mix is not None:
            waves["mix"] = clamp(mix, 0.0, 1.0)
        if octaves is not None:
            waves["octaves"] = max(1, min(octaves, 30))
        if pull is not None:
            waves["pull"] = clamp(pull, -1.0, 1.0)
        if sampleWidth is not None:
            waves["sampleWidth"] = clamp(sampleWidth, 0.01, 1.0)
        if shape is not None:
            waves["shape"] = clamp(shape, 1.0, 10.0)
        if speed is not None:
            waves["speed"] = clamp(speed, 0.01, 10.0)
        if speed_scaling is not None:
            waves["speed_scaling"] = clamp(speed_scaling, 0.0, 2.0)

    def caustics(
        self,
        enabled: bool | None = None,
        frame_length: float | None = None,
        power: int | None = None,
        scale: float | None = None,
        texture: str | None = None,
    ):
        """
        Caustics make bodies of water more realistic by projecting light rays on underwater surfaces.
        These rays then scatter and dance as the surface of the water moves. This effect is enabled by default,
        but can be selectively disabled in given water configurations.

        Parameters:
            enabled (bool, optional): Whether or not caustics are on or off.
            frame_length (float, optional): Duration for each frame in the caustics texture animation (0.01 - 5.0).
            power (int, optional): Controls brightness of the caustics effect (1 - 6).
            scale (float, optional): Controls the size of the caustics texture repetition (0.1 - 5.0).
            texture (str, optional): Resource location for a custom caustics texture; defaults to built-in texture if not provided.
        """
        caustics = self._content["minecraft:water_settings"].setdefault("caustics", {})
        if enabled is not None:
            caustics["enabled"] = enabled
        if frame_length is not None:
            caustics["frame_length"] = clamp(frame_length, 0.01, 5.0)
        if power is not None:
            caustics["power"] = max(1, min(power, 6))
        if scale is not None:
            caustics["scale"] = clamp(scale, 0.1, 5.0)
        if texture is not None:
            caustics["texture"] = texture


class ColorGradingSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "color_grading")
    _object_type = "Color Grading Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("color_grading_settings")
        self.content(
            JsonSchemes.color_grading_settings(
                f"{CONFIG.NAMESPACE}:color_grading_settings"
            )
        )

    def midtones(
        self,
        contrast: Vector3D | None = None,
        gain: Vector3D | None = None,
        gamma: Vector3D | None = None,
        offset: Vector3D | None = None,
        saturation: Vector3D | None = None,
    ):
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
        enabled: bool,
        highlightsMin: float | None = None,
        contrast: list[float] | None = None,
        gain: list[float] | None = None,
        gamma: list[float] | None = None,
        offset: list[float] | None = None,
        saturation: list[float] | None = None,
    ):

        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "highlights", {}
        )
        high = self._content["minecraft:color_grading_settings"]["color_grading"][
            "highlights"
        ]
        high["enabled"] = enabled
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
        enabled: bool,
        shadowsMax: float | None = None,
        contrast: list[float] | None = None,
        gain: list[float] | None = None,
        gamma: list[float] | None = None,
        offset: list[float] | None = None,
        saturation: list[float] | None = None,
    ):
        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "shadows", {}
        )
        shad = self._content["minecraft:color_grading_settings"]["color_grading"][
            "shadows"
        ]
        shad["enabled"] = enabled
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
        enabled: bool,
        temp_value: float | None = None,
        type: Literal["white_balance", "color_temperature"] | None = None,
    ):
        self._content["minecraft:color_grading_settings"]["color_grading"].setdefault(
            "temperature_grade", {}
        )
        temp = self._content["minecraft:color_grading_settings"]["color_grading"][
            "temperature_grade"
        ]
        temp["enabled"] = enabled
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
        self._content["minecraft:color_grading_settings"].setdefault("tone_mapping", {})
        self._content["minecraft:color_grading_settings"]["tone_mapping"][
            "operator"
        ] = operator


class LightingSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "lighting")
    _object_type = "Lighting Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Lighting settings require PBR to be enabled in the config."
            )
        super().__init__("global")
        self.content(
            JsonSchemes.lighting_settings(f"{CONFIG.NAMESPACE}:default_lighting")
        )

    def orbital_lights(
        self,
        sun_illuminance: float | list[KeyFrame],
        sun_color: RGB | HexRGB,
        moon_illuminance: float | list[KeyFrame],
        moon_color: RGB | HexRGB,
        orbital_offset_degrees: float,
    ) -> None:
        self._content["minecraft:lighting_settings"]["directional_lights"][
            "orbital"
        ] = {
            "sun": {
                "illuminance": (
                    sun_illuminance
                    if type(sun_illuminance) is float
                    else KeyFrame.keyframe_dict(sun_illuminance)
                ),
                "color": convert_color(sun_color),
            },
            "moon": {
                "illuminance": (
                    moon_illuminance
                    if type(moon_illuminance) is float
                    else KeyFrame.keyframe_dict(moon_illuminance)
                ),
                "color": convert_color(moon_color),
            },
            "orbital_offset_degrees": orbital_offset_degrees,
        }

    def flash_light(self, illuminance: float, color: RGB | HexRGB) -> None:
        self._content["minecraft:lighting_settings"]["directional_lights"]["flash"] = {
            "illuminance": illuminance,
            "color": convert_color(color),
        }

    def emissive(self, desaturation: float) -> None:
        self._content["minecraft:lighting_settings"]["emissive"] = {
            "desaturation": clamp(desaturation, 0.0, 1.0)
        }

    def ambient(self, illuminance: float, color: RGB | HexRGB) -> None:
        self._content["minecraft:lighting_settings"]["ambient"] = {
            "illuminance": clamp(illuminance, 0.0, 5.0),
            "color": convert_color(color),
        }

    def sky(self, intensity: float) -> None:
        self._content["minecraft:lighting_settings"]["sky"] = {
            "intensity": clamp(intensity, 0.1, 1.0)
        }


class LocalLighting(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "local_lighting")
    _object_type = "Local Lighting Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Local lighting requires PBR to be enabled in the config."
            )
        super().__init__("local_lighting")
        self.content(JsonSchemes.local_lighting())

    def add_point_light(
        self, block_identifier: Block | Identifier, color: HexRGB
    ) -> None:
        """
        Adds a point light to the point lights configuration.

        Parameters:
            block_identifier (Block | Identifier): The identifier of the block that emits the light.
            color (ColorHex): The color of the light in hexadecimal format (e.g., "#RRGGBB").
        """

        self._content["minecraft:point_light_settings"][str(block_identifier)] = {
            "light_color": convert_color(color, HexRGB),
            "light_type": "point_light",
        }


class PBRFallback(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "pbr")
    _object_type = "PBR Fallback Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError("PBR fallback requires PBR to be enabled in the config.")
        super().__init__("global")
        self.content(
            JsonSchemes.pbr_fallback_settings(f"{CONFIG.NAMESPACE}:pbr_fallback")
        )

    def block_fallback(self, MERS: RGBA) -> None:
        """
        Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for blocks that do not have PBR textures.

        Parameters:
            MERS (RGBA): The RGBA values representing the fallback MERS.
        """
        self._content["minecraft:pbr_fallback_settings"]["blocks"] = {
            "global_metalness_emissive_roughness_subsurface": convert_color(MERS)
        }

    def actors_fallback(self, MERS: RGBA) -> None:
        """
        Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for actors that do not have PBR textures.

        Parameters:
            MERS (RGBA): The RGBA values representing the fallback MERS.
        """
        self._content["minecraft:pbr_fallback_settings"]["actors"] = {
            "global_metalness_emissive_roughness_subsurface": convert_color(MERS)
        }

    def particles_fallback(self, MERS: RGBA) -> None:
        """
        Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for particles that do not have PBR textures.

        Parameters:
            MERS (RGBA): The RGBA values representing the fallback MERS.
        """
        self._content["minecraft:pbr_fallback_settings"]["particles"] = {
            "global_metalness_emissive_roughness_subsurface": convert_color(MERS)
        }

    def items_fallback(self, MERS: RGBA) -> None:
        """
        Sets the fallback MERS (Metallic, Emissive, Roughness, Specular) values for items that do not have PBR textures.

        Parameters:
            MERS (RGBA): The RGBA values representing the fallback MERS.
        """
        self._content["minecraft:pbr_fallback_settings"]["items"] = {
            "global_metalness_emissive_roughness_subsurface": convert_color(MERS)
        }


class CubeMapSettings(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "cubemaps")
    _object_type = "Cube Map Settings"

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, identifier: str) -> None: ...

    def __init__(self, identifier: str = "minecraft:default_cubemap") -> None:
        if not CONFIG._PBR:
            raise RuntimeError(
                "Cube map settings require PBR to be enabled in the config."
            )

        if identifier == "minecraft:default_cubemap":
            super().__init__(identifier, True)
        else:
            super().__init__(identifier)

        self.content(JsonSchemes.cubemap_settings(self.identifier))

    def set_lighting(
        self,
        ambient_light_illuminance: list[KeyFrame] = [
            KeyFrame(0.0, 5.625),
            KeyFrame(1.0, 5.625),
        ],
        sky_light_contribution: float = 1.0,
        directional_light_contribution: float = 1.0,
        affected_by_atmospheric_scattering: bool = False,
        affected_by_volumetric_scattering: bool = False,
    ):
        """
        Set lighting parameters for the cubemap.

        Args:
            ambient_light_illuminance : list[KeyFrame], optional
                Keyframed ambient illuminance (lux) over the day cycle. Each keyframe's
                time is clamped to [0.0, 1.0] and values should be in [0.0, 100000.0].
                If not provided, defaults to a constant 5.625 lux across the day.
            sky_light_contribution : float, optional
                How much the sky light contributes to the cubemap, in [0.0, 1.0]. Default 1.0.
            directional_light_contribution : float, optional
                How much directional light (sun/moon) contributes to the cubemap, in [0.0, 1.0].
                Default 1.0.
            affected_by_atmospheric_scattering : bool, optional
                Whether the cubemap is affected by atmospheric scattering (horizon/sky effects).
                Use True for near-surface sky content (clouds, airships). Default False.
            affected_by_volumetric_scattering : bool, optional
                Whether the cubemap is affected by volumetric scattering (fog/light shafts).
                Use True if cubemap content should interact with volumetric fog. Default False.
        """

        self._content["minecraft:cubemap_settings"]["lighting"] = {
            "ambient_light_illuminance": KeyFrame.keyframe_dict(
                ambient_light_illuminance
            ),
            "sky_light_contribution": clamp(sky_light_contribution, 0.0, 1.0),
            "directional_light_contribution": clamp(
                directional_light_contribution, 0.0, 1.0
            ),
            "affected_by_atmospheric_scattering": affected_by_atmospheric_scattering,
            "affected_by_volumetric_scattering": affected_by_volumetric_scattering,
        }
