import os

from anvil.lib.config import CONFIG
from anvil.lib.lib import clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


class WaterSettings(AddonObject):
    """Water effects customization settings for Vibrant Visuals (PBR) rendering."""

    _extension = ".json"
    _path = os.path.join(CONFIG.RP_PATH, "water")
    _object_type = "Water Settings"

    def __init__(
        self,
        name: str = "default_water",
    ) -> None:
        """Initializes a WaterSettings instance."""
        if not CONFIG.PBR:
            raise RuntimeError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        if name == "default_water":
            super().__init__("water")
            self.content(
                JsonSchemes.water_settings(f"{CONFIG.NAMESPACE}:default_water")
            )
        else:
            super().__init__(name)
            self.content(JsonSchemes.water_settings(self.identifier))

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
