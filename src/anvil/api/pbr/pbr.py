import os
from typing import Literal

from anvil.lib.blockbench import _Blockbench
from anvil.lib.config import CONFIG
from anvil.lib.lib import Color, HexRGB, clamp, convert_color
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import RGB, RGBA, Block, HexRGBA, Identifier, Vector3D


class TextureSet(AddonObject):
    _extension = ".texture_set.json"
    _path = os.path.join(
        CONFIG.RP_PATH,
        "textures",
        CONFIG.NAMESPACE,
        CONFIG.PROJECT_NAME,
    )
    _object_type = "Texture Set"

    def __init__(self, texture_name: str, target: str) -> None:
        super().__init__(texture_name)
        self.content(JsonSchemes.texture_set())
        self._target = target
        if not CONFIG._PBR:
            raise RuntimeError("Texture sets require PBR to be enabled in the config.")

    def set_textures(
        self,
        blockbench_name: str,
        color_texture: str,
        normal_texture: str | Color | None,
        heightmap_texture: str | Color | None,
        metalness_emissive_roughness_texture: str | Color | None,
        metalness_emissive_roughness_subsurface_texture: str | Color | None,
    ):
        if normal_texture is not None and heightmap_texture is not None:
            raise ValueError("Normal and heightmap textures are mutually exclusive.")

        if (
            metalness_emissive_roughness_texture is not None
            and metalness_emissive_roughness_subsurface_texture is not None
        ):
            raise ValueError(
                "Metalness, emissive, roughness and subsurface textures are mutually exclusive."
            )

        self._blockbench = _Blockbench(blockbench_name, "actors")
        self._blockbench.textures.queue_texture(color_texture)

        self._content["minecraft:texture_set"]["color"] = color_texture
        self._path = os.path.join(self._path, self._target, blockbench_name)

        if type(normal_texture) is str:
            self._blockbench.textures.queue_texture(normal_texture)
            self._content["minecraft:texture_set"]["normal"] = color_texture
        elif type(normal_texture) is Color:
            self._content["minecraft:texture_set"]["normal"] = convert_color(
                normal_texture, HexRGB
            )

        if type(heightmap_texture) is str:
            self._blockbench.textures.queue_texture(heightmap_texture)
            self._content["minecraft:texture_set"]["heightmap"] = heightmap_texture
        elif type(heightmap_texture) is Color:
            self._content["minecraft:texture_set"]["heightmap"] = convert_color(
                heightmap_texture, HexRGB
            )

        if type(metalness_emissive_roughness_texture) is str:
            self._blockbench.textures.queue_texture(
                metalness_emissive_roughness_texture
            )
            self._content["minecraft:texture_set"][
                "metalness_emissive_roughness"
            ] = metalness_emissive_roughness_texture
        elif type(metalness_emissive_roughness_texture) is Color:
            self._content["minecraft:texture_set"]["metalness_emissive_roughness"] = (
                convert_color(metalness_emissive_roughness_texture, HexRGB)
            )

        if type(metalness_emissive_roughness_subsurface_texture) is str:
            self._blockbench.textures.queue_texture(
                metalness_emissive_roughness_subsurface_texture
            )
            self._content["minecraft:texture_set"][
                "metalness_emissive_roughness_subsurface"
            ] = metalness_emissive_roughness_subsurface_texture
        elif type(metalness_emissive_roughness_subsurface_texture) is Color:
            self._content["minecraft:texture_set"][
                "metalness_emissive_roughness_subsurface"
            ] = convert_color(metalness_emissive_roughness_subsurface_texture, HexRGBA)

    def _export(self):
        if self._content["minecraft:texture_set"] != {}:
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
        min: dict[float, float],
        start: dict[float, float],
        mie_start: dict[float, float],
        max: dict[float, float],
    ):
        self._content["horizon_blend_stops"] = {
            "min": {
                **{clamp(k, 0.0, 1.0): v for k, v in min.items()},
            },
            "start": {
                **{clamp(k, 0.0, 1.0): v for k, v in start.items()},
            },
            "mie_start": {
                **{clamp(k, 0.0, 1.0): v for k, v in mie_start.items()},
            },
            "max": {
                **{clamp(k, 0.0, 1.0): v for k, v in max.items()},
            },
        }

    def rayleigh_strength(self, keyframe: dict[float, float]):
        self._content["rayleigh_strength"] = {
            **{clamp(k, 0.0, 1.0): v for k, v in keyframe.items()},
        }

    def sun_mie_strength(self, keyframe: dict[float, float]):
        self._content["sun_mie_strength"] = {
            **{clamp(k, 0.0, 1.0): v for k, v in keyframe.items()},
        }

    def moon_mie_strength(self, keyframe: dict[float, float]):
        self._content["moon_mie_strength"] = {
            **{clamp(k, 0.0, 1.0): v for k, v in keyframe.items()},
        }

    def sun_glare_shape(self, keyframe: dict[float, float]):
        self._content["sun_glare_shape"] = {
            **{clamp(k, 0.0, 1.0): v for k, v in keyframe.items()},
        }

    def sky_zenith_color(self, keyframe: dict[float, float]):
        self._content["sky_zenith_color"] = {
            **{clamp(k, 0.0, 1.0): v for k, v in keyframe.items()},
        }

    def sky_horizon_color(self, keyframe: dict[float, RGB]):
        self._content["sky_horizon_color"] = {
            **{
                clamp(k, 0.0, 1.0): convert_color(
                    v,
                )
                for k, v in keyframe.items()
            },
        }


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
        sun_illuminance: float | dict[float, float],
        sun_color: RGB | HexRGB,
        moon_illuminance: float | dict[float, float],
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
                    else {clamp(k, 0.0, 1.0): v for k, v in sun_illuminance.items()}
                ),
                "color": convert_color(sun_color),
            },
            "moon": {
                "illuminance": (
                    moon_illuminance
                    if type(moon_illuminance) is float
                    else {clamp(k, 0.0, 1.0): v for k, v in moon_illuminance.items()}
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


class PointLights(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "local_lighting")
    _object_type = "Point Lights Settings"

    def __init__(self) -> None:
        if not CONFIG._PBR:
            raise RuntimeError("Point lights require PBR to be enabled in the config.")
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
