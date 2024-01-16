import os

from anvil import CONFIG
from anvil.lib.lib import Color, clamp, process_color
from anvil.lib.schemas import AddonObject, JsonSchemes


def _optkeyframe(range_min: int | float, range_max: int | float, values):
    if isinstance(values, tuple):
        return {
            (i * (range_max-range_min) + range_min) / (len(values) - 1): process_color(v, True) if isinstance(v, str) else v
            for i, v in enumerate(values)
        }
    else:
        return process_color(values, True) if isinstance(values, str) else values


class _DirectionalLighting:
    def __init__(self) -> None:
        self.content = {}

    def sun(self, illuminance: int | tuple[int] = 100000, color: Color | tuple[Color] = "#ffffffff"):
        self.content["sun"] = {
            "illuminance": _optkeyframe(0, 1, illuminance),
            "color": _optkeyframe(0, 1, color),
        }

    def moon(self, illuminance: int | tuple[int] = 0.27, color: Color | tuple[Color] = "#ffffffff"):
        self.content["moon"] = {
            "illuminance": _optkeyframe(0, 1, illuminance),
            "color": _optkeyframe(0, 1, color),
        }

    def orbital_offset_degrees(self, degree: float):
        self.content["orbital_offset_degrees"] = degree


class _PBR:
    def __init__(self) -> None:
        self.content = {}

    def blocks(self, MER: Color):
        self.content["blocks"] = {"global_metalness_emissive_roughness": process_color(MER, False)}

    def actors(self, MER: Color):
        self.content["actors"] = {"global_metalness_emissive_roughness": process_color(MER, False)}


class GlobalLighting(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "lighting")

    def __init__(self) -> None:
        super().__init__("global")
        self.content(JsonSchemes.directional_lights())
        self._directional_lights = _DirectionalLighting()
        self._pbr = _PBR()

    @property
    def directional_lights(self) -> _DirectionalLighting:
        return self._directional_lights

    @property
    def pbr(self) -> _PBR:
        return self._pbr

    @property
    def queue(self):
        self._content["directional_lights"] = self._directional_lights.content
        self._content["pbr"] = self._pbr.content

        return super().queue()


class _HorizonBlendStops:
    def __init__(self) -> None:
        self.content = {}

    def min(self, value: float | tuple[float]):
        self.content["min"] = _optkeyframe(0, 1, value)

    def max(self, value: float | tuple[float]):
        self.content["max"] = _optkeyframe(0, 1, value)

    def start(self, value: float | tuple[float]):
        self.content["start"] = _optkeyframe(0, 1, value)

    def mie_start(self, value: float | tuple[float]):
        self.content["mie_start"] = _optkeyframe(0, 1, value)


class Atmospherics(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "lighting")
    
    def __init__(self) -> None:
        super().__init__("atmospherics")
        self.content(JsonSchemes.atmospherics())
        self._horizon_blend_stops = _HorizonBlendStops()

    @property
    def horizon_blend_stops(self) -> _HorizonBlendStops:
        return self._horizon_blend_stops

    def rayleigh_strength(self, value: float | tuple[float]):
        self._content["rayleigh_strength"] = _optkeyframe(0, 1, value)
        
    def sun_mie_strength(self, value: float | tuple[float]):
        self._content["sun_mie_strength"] = _optkeyframe(0, 1, value)
        
    def moon_mie_strength(self, value: float | tuple[float]):
        self._content["moon_mie_strength"] = _optkeyframe(0, 1, value)
        
    def sun_glare_shape(self, value: float | tuple[float]):
        self._content["sun_glare_shape"] = _optkeyframe(0, 1, value)
        
    def sky_zenith_color(self, value: Color | tuple[Color]):
        self._content["sky_zenith_color"] = _optkeyframe(0, 1, value)
        
    def sky_horizon_color(self, value: Color | tuple[Color]):
        self._content["sky_horizon_color"] = _optkeyframe(0, 1, value)

    @property
    def queue(self):
        self._content["horizon_blend_stops"] = self._horizon_blend_stops.content

        return super().queue()
