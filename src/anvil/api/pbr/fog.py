from typing import Annotated, ClassVar

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import FOG_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    RGBColor,
    Wrapped,
    json_field,
)
from anvil.lib.jsonmodel.enums import FogCameraLocation, RenderDistanceType
from anvil.lib.jsonmodel.types import RGB, RGB255, RGBA, RGBA255, HexRGB, HexRGBA

__all__ = ["FogSettings", "Fog"]


class _InitFog(JsonObject):
    """A distance fog: where it starts and ends, and its color."""

    fog_start: float | None = None
    fog_end: float | None = None
    fog_color: HexRGB | None = None
    render_distance_type: RenderDistanceType | None = None

    def set_fog_start(self, fog_start: float) -> None:
        """Sets where the fog begins, as a render distance ratio or in blocks."""
        self.fog_start = fog_start

    def set_fog_end(self, fog_end: float) -> None:
        """Sets where the fog becomes fully opaque, as a render distance ratio or in blocks."""
        self.fog_end = fog_end

    def set_fog_color(self, fog_color: HexRGB) -> None:
        """Sets the fog color, as a hex string."""
        self.fog_color = fog_color

    def set_render_distance_type(
        self, render_distance_type: RenderDistanceType
    ) -> None:
        """Sets how fog_start and fog_end are read."""
        self.render_distance_type = render_distance_type

    def __validate__(self) -> None:
        if (
            self.fog_start is not None
            and self.fog_end is not None
            and self.fog_start >= self.fog_end
        ):
            raise ValueError(
                f"fog_end: [{self.fog_end}] must be greater than fog_start: [{self.fog_start}]."
            )


class _TransitionFog(JsonObject):
    """The fog the camera starts in when it enters water, and how it turns into the water
    fog. Unset keys are left out."""

    init_fog: _InitFog = json_field(default_factory=_InitFog)
    min_percent: float | None = None
    mid_seconds: float | None = None
    mid_percent: float | None = None
    max_seconds: float | None = None

    def set_min_percent(self, min_percent: float) -> None:
        """Sets the minimum progress of the transition."""
        self.min_percent = min_percent

    def set_mid_seconds(self, mid_seconds: float) -> None:
        """Sets the seconds it takes to reach mid_percent."""
        self.mid_seconds = mid_seconds

    def set_mid_percent(self, mid_percent: float) -> None:
        """Sets the progress reached after mid_seconds."""
        self.mid_percent = mid_percent

    def set_max_seconds(self, max_seconds: float) -> None:
        """Sets the total seconds of the transition."""
        self.max_seconds = max_seconds


class _FogDistance(_InitFog):
    """The distance fog of one camera location, which `add_distance_location` returns."""

    camera_location: FogCameraLocation = json_field(
        default=FogCameraLocation.Air, exclude=True
    )
    transition_fog: _TransitionFog = json_field(default_factory=_TransitionFog)

    def set_transition_fog(
        self,
        color: HexRGB,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
        min_percent: float | None = None,
        mid_seconds: float | None = None,
        mid_percent: float | None = None,
        max_seconds: float | None = None,
    ) -> "_FogDistance":
        """Sets the fog the camera starts in when it enters water, and how it turns into
        this fog. Only the 'water' camera location reads it.

        Args:
            color (HexRGB): Hex color of the starting fog.
            fog_start (float | int): Where the starting fog begins.
            fog_end (float | int): Where the starting fog ends. Must be greater than fog_start.
            render_distance_type (RenderDistanceType, optional): How fog_start and fog_end are
                read. Defaults to RenderDistanceType.Render.
            min_percent (float, optional): The minimum progress of the transition.
            mid_seconds (float, optional): The seconds it takes to reach mid_percent.
            mid_percent (float, optional): The progress reached after mid_seconds.
            max_seconds (float, optional): The total seconds of the transition.

        Returns:
            _FogDistance: Returns self for method chaining.
        """
        if self.camera_location != FogCameraLocation.Water:
            raise ValueError(
                "transition_fog can only be configured for the 'water' camera location."
            )
        init_fog = self.transition_fog.init_fog
        init_fog.set_fog_color(color)
        init_fog.set_fog_start(fog_start)
        init_fog.set_fog_end(fog_end)
        init_fog.set_render_distance_type(render_distance_type)
        if min_percent is not None:
            self.transition_fog.set_min_percent(min_percent)
        if mid_seconds is not None:
            self.transition_fog.set_mid_seconds(mid_seconds)
        if mid_percent is not None:
            self.transition_fog.set_mid_percent(mid_percent)
        if max_seconds is not None:
            self.transition_fog.set_max_seconds(max_seconds)
        return self


class _FogDistances(JsonObject):
    """The `distance` object: the distance fog of each camera location."""

    air: _FogDistance | None = None
    lava: _FogDistance | None = None
    lava_resistance: _FogDistance | None = None
    powder_snow: _FogDistance | None = None
    water: _FogDistance | None = None
    weather: _FogDistance | None = None

    def set_location(self, distance: _FogDistance) -> None:
        """Sets the distance fog of the camera location the part was made for."""
        setattr(self, distance.camera_location.value, distance)


class _FogDensity(JsonObject):
    """The volumetric fog density of one medium."""

    max_density: Annotated[float, InRange(0.0, 1.0)] | None = None
    uniform: bool | None = None
    zero_density_height: float | None = None
    max_density_height: float | None = None

    def set_max_density(self, max_density: float) -> None:
        """Sets the density, from 0.0 (no fog) to 1.0 (near opaque)."""
        self.max_density = max_density

    def set_uniform(self, uniform: bool) -> None:
        """Sets whether the density is the same at all heights."""
        self.uniform = uniform

    def set_zero_density_height(self, zero_density_height: float) -> None:
        """Sets the height in blocks where the density fades to 0."""
        self.zero_density_height = zero_density_height

    def set_max_density_height(self, max_density_height: float) -> None:
        """Sets the height in blocks where the density starts at max_density."""
        self.max_density_height = max_density_height


class _FogDensities(JsonObject):
    """The `density` object of each medium. Unset media are left out."""

    air: _FogDensity = json_field(default_factory=_FogDensity)
    weather: _FogDensity = json_field(default_factory=_FogDensity)
    water: _FogDensity = json_field(default_factory=_FogDensity)
    lava: _FogDensity = json_field(default_factory=_FogDensity)
    lava_resistance: _FogDensity = json_field(default_factory=_FogDensity)


class _MediaCoefficients(JsonObject):
    """How one medium scatters and absorbs light, per RGB channel."""

    scattering: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, RGBColor] | None
    ) = None
    absorption: (
        Annotated[HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, RGBColor] | None
    ) = None

    def set_scattering(
        self, scattering: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> None:
        """Sets the scattering coefficients."""
        self.scattering = scattering

    def set_absorption(
        self, absorption: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255
    ) -> None:
        """Sets the absorption coefficients."""
        self.absorption = absorption


class _MediaCoefficientsSet(JsonObject):
    """The `media_coefficients` object of each medium. Unset media are left out."""

    air: _MediaCoefficients = json_field(default_factory=_MediaCoefficients)
    water: _MediaCoefficients = json_field(default_factory=_MediaCoefficients)
    cloud: _MediaCoefficients = json_field(default_factory=_MediaCoefficients)


class _HenyeyGreenstein(JsonObject):
    """The Henyey-Greenstein phase asymmetry of one medium."""

    henyey_greenstein_g: Annotated[float, InRange(-1.0, 1.0)] | None = None

    def set_henyey_greenstein_g(self, henyey_greenstein_g: float) -> None:
        """Sets the asymmetry, from -1.0 (back-scattering) to 1.0 (forward-scattering)."""
        self.henyey_greenstein_g = henyey_greenstein_g


class _HenyeyGreensteinSet(JsonObject):
    """The `henyey_greenstein_g` object of air and water."""

    air: _HenyeyGreenstein = json_field(default_factory=_HenyeyGreenstein)
    water: _HenyeyGreenstein = json_field(default_factory=_HenyeyGreenstein)


class _Volumetric(JsonObject):
    """The `volumetric` object, used by Vibrant Visuals and ray tracing. Parts with nothing
    set are left out."""

    density: _FogDensities = json_field(default_factory=_FogDensities)
    media_coefficients: _MediaCoefficientsSet = json_field(
        default_factory=_MediaCoefficientsSet
    )
    henyey_greenstein_g: _HenyeyGreensteinSet = json_field(
        default_factory=_HenyeyGreensteinSet
    )


class _FogSettings(JsonObject):
    """The `minecraft:fog_settings` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description",)

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    distance: _FogDistances = json_field(default_factory=_FogDistances)
    volumetric: _Volumetric = json_field(default_factory=_Volumetric)

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The settings have no identifier.")


class _FogSettingsFile(JsonObject):
    """The content of a `fogs/*.fog.json` file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:fog_settings",
    )

    format_version: str = json_field(default=FOG_VERSION, init=False)
    settings: _FogSettings = json_field(
        key="minecraft:fog_settings", default_factory=_FogSettings
    )


class FogSettings(JsonFile):
    """
    Represents a Minecraft Fog resource pack definition.

    Generates a `.fog.json` file in the pack's `fogs/` directory. Fog settings define
    both distance-based fog properties and volumetric (PBR/Ray Tracing) settings.
    Settings are resolved in the game via the Active Fog Stack:
    Command (highest precedence) -> Biomes -> Data Default -> Engine Default (lowest).

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/foginresourcepacks)

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/fogsreference/fogs)
    """

    _document = _FogSettingsFile
    _extension = ".fog.json"
    _pack = Pack.RP
    _folder = "fogs"
    _object_type = "Fog"

    def __init__(self, name: str = "fog", is_vanilla: bool = False) -> None:
        """Initializes a Fog definition instance.

        Args:
            name (str, optional): The identifier and filename of the fog setting. Defaults to "fog".
            is_vanilla (bool, optional): True if referencing/overriding a vanilla fog definition
                (under the `minecraft` namespace). Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._content.settings.set_description(self.identifier)

    def add_distance_location(
        self,
        color: HexRGB,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
        camera_location: FogCameraLocation = FogCameraLocation.Air,
    ) -> "_FogDistance":
        """Adds and configures distance-based fog settings for a specific camera location environment.

        Args:
            color (HexRGB): Hex color code of the fog (e.g. `"#ABD2FF"`). Maps to `fog_color` in JSON.
            fog_start (float | int): Relative ratio or absolute block distance where fog begins to appear.
                Maps to `fog_start` in JSON.
            fog_end (float | int): Relative ratio or absolute block distance where fog becomes fully opaque.
                Maps to `fog_end` in JSON. Must be greater than fog_start.
            render_distance_type (RenderDistanceType, optional): Determines how start and end values are used.
                - `RenderDistanceType.Fixed`: Measured in absolute block distance away from the camera.
                - `RenderDistanceType.Render`: Ratio multiplied against the player's current render distance.
                Defaults to RenderDistanceType.Render.
            camera_location (FogCameraLocation, optional): The camera location environment
                (e.g., Air, Water, Weather, Lava, LavaResistance) matching the corresponding
                key in the JSON schema. Defaults to FogCameraLocation.Air.

        Returns:
            _FogDistance: The configured distance settings object for method chaining.
        """
        distance = _FogDistance(
            camera_location=camera_location,
            fog_color=color,
            fog_start=fog_start,
            fog_end=fog_end,
            render_distance_type=render_distance_type,
        )
        self._content.settings.distance.set_location(distance)
        return distance

    def water_density(
        self,
        max_density: float,
        uniform: bool = True,
        zero_density_height: float = 0.0,
        max_density_height: float = 0.0,
    ) -> "FogSettings":
        """Sets the volumetric density parameters for water. Used for Ray Tracing / PBR rendering.

        Args:
            max_density (float): Density multiplier disrupting light passing through water.
                Range: [0.0 (no fog), 1.0 (near opaque)].
            uniform (bool, optional): If True, fog density is uniform at all heights. Defaults to True.
            zero_density_height (float, optional): Y-level height in blocks where water fog density fades to 0.0.
                Only active when `uniform` is False. Must be greater than or equal to max_density_height. Defaults to 0.0.
            max_density_height (float, optional): Y-level height in blocks where water fog density starts at max_density.
                Only active when `uniform` is False. Defaults to 0.0.

        Raises:
            ValueError: If PBR is not enabled in CONFIG.
            ValueError: If zero_density_height is less than max_density_height.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        if not uniform and zero_density_height < max_density_height:
            raise ValueError(
                f"zero_density_height ({zero_density_height}) must be greater than or equal to "
                f"max_density_height ({max_density_height})."
            )

        density = self._content.settings.volumetric.density.water
        density.set_max_density(max_density)
        density.set_uniform(uniform)
        if not uniform:
            density.set_zero_density_height(zero_density_height)
            density.set_max_density_height(max_density_height)
        return self

    def air_density(
        self,
        max_density: float,
        uniform: bool = False,
        zero_density_height: float = 0.0,
        max_density_height: float = 0.0,
    ) -> "FogSettings":
        """Sets the volumetric density parameters for air. Used for Ray Tracing / PBR rendering.

        Args:
            max_density (float): Density multiplier disrupting light passing through air.
                Range: [0.0 (no fog), 1.0 (near opaque)].
            uniform (bool, optional): If True, fog density is uniform at all heights. Defaults to False.
            zero_density_height (float, optional): Y-level height in blocks where air fog density fades to 0.0.
                Only active when `uniform` is False. Must be greater than or equal to max_density_height. Defaults to 0.0.
            max_density_height (float, optional): Y-level height in blocks where air fog density starts at max_density.
                Only active when `uniform` is False. Defaults to 0.0.

        Raises:
            ValueError: If PBR is not enabled in CONFIG.
            ValueError: If zero_density_height is less than max_density_height.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        if not uniform and zero_density_height < max_density_height:
            raise ValueError(
                f"zero_density_height ({zero_density_height}) must be greater than or equal to "
                f"max_density_height ({max_density_height})."
            )

        density = self._content.settings.volumetric.density.air
        density.set_max_density(max_density)
        density.set_uniform(uniform)
        if not uniform:
            density.set_zero_density_height(zero_density_height)
            density.set_max_density_height(max_density_height)
        return self

    def media_coefficients(
        self,
        water_scattering: (
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None
        ) = None,
        water_absorption: (
            HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None
        ) = None,
        air_scattering: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None,
        air_absorption: HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255 | None = None,
    ) -> "FogSettings":
        """Sets media scattering and absorption RGB coefficients for water and air volumetric mediums.

        Args:
            water_scattering (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): RGB scattering multipliers.
            water_absorption (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): RGB absorption multipliers.
            air_scattering (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): RGB scattering multipliers.
            air_absorption (HexRGB | HexRGBA | RGB | RGBA | RGB255 | RGBA255, optional): RGB absorption multipliers.

        Raises:
            ValueError: If PBR is not enabled in CONFIG.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        media = self._content.settings.volumetric.media_coefficients
        if water_scattering is not None or water_absorption is not None:
            media.water.set_scattering(water_scattering or (0, 0, 0))
            media.water.set_absorption(water_absorption or (0, 0, 0))
        if air_scattering is not None or air_absorption is not None:
            media.air.set_scattering(air_scattering or (0, 0, 0))
            media.air.set_absorption(air_absorption or (0, 0, 0))
        return self

    def henyey_greenstein_g(
        self, air_g: float = 0.0, water_g: float = 0.0
    ) -> "FogSettings":
        """Sets Henyey-Greenstein phase function asymmetry parameters for air and water.
        Supported in format_version 1.21.90+ and only applicable in Vibrant Visuals (PBR) packs.

        Args:
            air_g (float, optional): Asymmetry factor for air scattering. Range [-1.0 (back-scattering),
                1.0 (forward-scattering)]. Default is 0.75.
            water_g (float, optional): Asymmetry factor for water scattering. Range [-1.0 (back-scattering),
                1.0 (forward-scattering)]. Default is 0.6.

        Raises:
            ValueError: If PBR is not enabled in CONFIG.
        """
        if not CONFIG.PBR:
            raise ValueError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        hg = self._content.settings.volumetric.henyey_greenstein_g
        hg.air.set_henyey_greenstein_g(air_g)
        hg.water.set_henyey_greenstein_g(water_g)
        return self


Fog = FogSettings
