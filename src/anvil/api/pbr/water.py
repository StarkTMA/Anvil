from typing import Annotated, ClassVar

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import WATER_SETTINGS_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    Wrapped,
    json_field,
)

__all__ = ["WaterSettings"]


class _ParticleConcentrations(JsonObject):
    """The particles in the water, in mg/L, which set its color and how light travels
    through it. Unset keys are left out."""

    cdom: Annotated[float, InRange(0.0, 15.0)] | None = None
    chlorophyll: Annotated[float, InRange(0.0, 10.0)] | None = None
    suspended_sediment: Annotated[float, InRange(0.0, 300.0)] | None = None

    def set_cdom(self, cdom: float) -> None:
        """Sets the colored dissolved organic matter, from 0.0 to 15.0."""
        self.cdom = cdom

    def set_chlorophyll(self, chlorophyll: float) -> None:
        """Sets the chlorophyll, from 0.0 to 10.0."""
        self.chlorophyll = chlorophyll

    def set_suspended_sediment(self, suspended_sediment: float) -> None:
        """Sets the suspended sediment, from 0.0 to 300.0."""
        self.suspended_sediment = suspended_sediment


class _Waves(JsonObject):
    """Image-based waves on the water surface. Unset keys are left out."""

    enabled: bool | None = None
    depth: Annotated[float, InRange(0.0, 3.0)] | None = None
    direction_increment: Annotated[float, InRange(0.0, 360.0)] | None = None
    frequency: Annotated[float, InRange(0.01, 3.0)] | None = None
    frequency_scaling: Annotated[float, InRange(0.0, 2.0)] | None = None
    mix: Annotated[float, InRange(0.0, 1.0)] | None = None
    octaves: Annotated[int, InRange(1, 30)] | None = None
    pull: Annotated[float, InRange(-1.0, 1.0)] | None = None
    sampleWidth: Annotated[float, InRange(0.01, 1.0)] | None = None
    shape: Annotated[float, InRange(1.0, 10.0)] | None = None
    speed: Annotated[float, InRange(0.01, 10.0)] | None = None
    speed_scaling: Annotated[float, InRange(0.0, 2.0)] | None = None

    def set_enabled(self, enabled: bool) -> None:
        """Turns the waves on or off."""
        self.enabled = enabled

    def set_depth(self, depth: float) -> None:
        """Sets the wave displacement, from 0.0 to 3.0."""
        self.depth = depth

    def set_direction_increment(self, direction_increment: float) -> None:
        """Sets the heading change between octaves, from 0.0 to 360.0."""
        self.direction_increment = direction_increment

    def set_frequency(self, frequency: float) -> None:
        """Sets the wave size, from 0.01 to 3.0."""
        self.frequency = frequency

    def set_frequency_scaling(self, frequency_scaling: float) -> None:
        """Sets the frequency change between octaves, from 0.0 to 2.0."""
        self.frequency_scaling = frequency_scaling

    def set_mix(self, mix: float) -> None:
        """Sets how much each octave blends into the next, from 0.0 to 1.0."""
        self.mix = mix

    def set_octaves(self, octaves: int) -> None:
        """Sets the layers of waves, from 1 to 30."""
        self.octaves = octaves

    def set_pull(self, pull: float) -> None:
        """Sets how much smaller waves are pulled into larger ones, from -1.0 to 1.0."""
        self.pull = pull

    def set_sampleWidth(self, sampleWidth: float) -> None:
        """Sets the resolution of the fractal effect, from 0.01 to 1.0."""
        self.sampleWidth = sampleWidth

    def set_shape(self, shape: float) -> None:
        """Sets the wave shape, from 1.0 to 10.0."""
        self.shape = shape

    def set_speed(self, speed: float) -> None:
        """Sets the speed of the first waves, from 0.01 to 10.0."""
        self.speed = speed

    def set_speed_scaling(self, speed_scaling: float) -> None:
        """Sets the speed change between octaves, from 0.0 to 2.0."""
        self.speed_scaling = speed_scaling


class _Caustics(JsonObject):
    """Light patterns projected on underwater surfaces. Unset keys are left out."""

    enabled: bool | None = None
    frame_length: Annotated[float, InRange(0.01, 5.0)] | None = None
    power: Annotated[int, InRange(1, 6)] | None = None
    scale: Annotated[float, InRange(0.1, 5.0)] | None = None
    texture: str | None = None

    def set_enabled(self, enabled: bool) -> None:
        """Turns the caustics on or off."""
        self.enabled = enabled

    def set_frame_length(self, frame_length: float) -> None:
        """Sets the duration of each texture frame, from 0.01 to 5.0."""
        self.frame_length = frame_length

    def set_power(self, power: int) -> None:
        """Sets the brightness, from 1 to 6."""
        self.power = power

    def set_scale(self, scale: float) -> None:
        """Sets the size of the texture repetition, from 0.1 to 5.0."""
        self.scale = scale

    def set_texture(self, texture: str) -> None:
        """Sets the resource location of a custom caustics texture."""
        self.texture = texture


class _WaterSettings(JsonObject):
    """The `minecraft:water_settings` object. Parts with nothing set are left out."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    particle_concentrations: _ParticleConcentrations = json_field(
        default_factory=_ParticleConcentrations
    )
    waves: _Waves = json_field(default_factory=_Waves)
    caustics: _Caustics = json_field(default_factory=_Caustics)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The settings have no identifier.")


class _WaterSettingsFile(JsonObject):
    """The content of a `water/*.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:water_settings",
    )

    format_version: str = json_field(default=WATER_SETTINGS_VERSION, init=False)
    settings: _WaterSettings = json_field(
        key="minecraft:water_settings", default_factory=_WaterSettings
    )


class WaterSettings(JsonFile[_WaterSettingsFile]):
    """Water effects customization settings for Vibrant Visuals (PBR) rendering.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/watercustomization)
    """

    _extension = ".json"
    _pack = Pack.RP
    _folder = "water"
    _object_type = "Water Settings"

    def __init__(
        self,
        name: str = "default_water",
    ) -> None:
        """Initializes a WaterSettings instance."""
        if not CONFIG.PBR:
            raise ValueError(
                "Atmospherics addon requires PBR to be enabled in the config."
            )
        super().__init__("water" if name == "default_water" else name, identifier=name)
        self._document.settings.set_description(self.identifier)

    def particle_concentrations(
        self,
        cdom: float | None = None,
        chlorophyll: float | None = None,
        suspended_sediment: float | None = None,
    ) -> "WaterSettings":
        """
        The composition of particles in a body of water determines its color and how light behaves as it
        travels through the water. We've boiled them down to three concentrations in mg/L. Use these values
        to simulate crystal clear lakes, deep oceans, or muddy rivers.
        Args:
            cdom (float | None): Concentration of colored dissolved organic matter (CDOM) in the water.
            chlorophyll (float | None): Concentration of chlorophyll in the water.
            suspended_sediment (float | None): Concentration of suspended sediment in the water.
        """
        pc = self._document.settings.particle_concentrations
        if cdom is not None:
            pc.set_cdom(cdom)
        if chlorophyll is not None:
            pc.set_chlorophyll(chlorophyll)
        if suspended_sediment is not None:
            pc.set_suspended_sediment(suspended_sediment)
        return self

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
    ) -> "WaterSettings":
        """
        Waves are an optional effect that can be used to complement water surface animations to make your water appear more
        realistic. You can blend them with existing water texture animations, or replace them entirely.
        The waves in Vibrant Visuals are purely an image-based effect—waves don't actually move the vertices of the water
        surface, so the water surface geometry will remain unchanged.
        Args:
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

        waves = self._document.settings.waves
        if enabled is not None:
            waves.set_enabled(enabled)
        if depth is not None:
            waves.set_depth(depth)
        if direction_increment is not None:
            waves.set_direction_increment(direction_increment)
        if frequency is not None:
            waves.set_frequency(frequency)
        if frequency_scaling is not None:
            waves.set_frequency_scaling(frequency_scaling)
        if mix is not None:
            waves.set_mix(mix)
        if octaves is not None:
            waves.set_octaves(octaves)
        if pull is not None:
            waves.set_pull(pull)
        if sampleWidth is not None:
            waves.set_sampleWidth(sampleWidth)
        if shape is not None:
            waves.set_shape(shape)
        if speed is not None:
            waves.set_speed(speed)
        if speed_scaling is not None:
            waves.set_speed_scaling(speed_scaling)
        return self

    def caustics(
        self,
        enabled: bool | None = None,
        frame_length: float | None = None,
        power: int | None = None,
        scale: float | None = None,
        texture: str | None = None,
    ) -> "WaterSettings":
        """
        Caustics make bodies of water more realistic by projecting light rays on underwater surfaces.
        These rays then scatter and dance as the surface of the water moves. This effect is enabled by default,
        but can be selectively disabled in given water configurations.

        Args:
            enabled (bool, optional): Whether or not caustics are on or off.
            frame_length (float, optional): Duration for each frame in the caustics texture animation (0.01 - 5.0).
            power (int, optional): Controls brightness of the caustics effect (1 - 6).
            scale (float, optional): Controls the size of the caustics texture repetition (0.1 - 5.0).
            texture (str, optional): Resource location for a custom caustics texture; defaults to built-in texture if not provided.
        """
        caustics = self._document.settings.caustics
        if enabled is not None:
            caustics.set_enabled(enabled)
        if frame_length is not None:
            caustics.set_frame_length(frame_length)
        if power is not None:
            caustics.set_power(power)
        if scale is not None:
            caustics.set_scale(scale)
        if texture is not None:
            caustics.set_texture(texture)
        return self
