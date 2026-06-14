import os

from anvil.api.core.enums import FogCameraLocation, RenderDistanceType
from anvil.lib.config import CONFIG
from anvil.lib.lib import RGB, AnvilFormatter, Color, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription


class _FogDistance:
    """
    Handles distance-based fog configurations for a specific camera location.

    Maps to the `minecraft:fog_settings/distance/<camera_location>` object in the
    Minecraft fog JSON schema. Distance-based fog limits what players can see
    beyond a specified distance from the camera position.
    """

    def __init__(
        self,
        color: str,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
        camera_location: FogCameraLocation = FogCameraLocation.Air,
    ) -> None:
        """
        Initializes a _FogDistance instance for a specific camera location.

        Args:
            color (str): Hex color code of the fog (e.g. `"#ABD2FF"`). Maps to `fog_color` in JSON.
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
        """
        self._camera_location = camera_location.value
        self._distance = {self._camera_location: {}}
        if fog_start >= fog_end:
            raise ValueError(
                f"fog_end: [{fog_end}] must be greater than fog_start: [{fog_start}]."
            )

        self._distance[self._camera_location]["fog_color"] = color
        self._distance[self._camera_location]["fog_start"] = fog_start
        self._distance[self._camera_location]["fog_end"] = fog_end
        self._distance[self._camera_location][
            "render_distance_type"
        ] = render_distance_type.value

    def transition_fog(
        self,
        color: str,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
    ):
        """
        Sets transition properties when moving into this fog environment.
        Note: According to official Minecraft documentation, `transition_fog` is only
        functional when the camera location is `water`.

        Args:
            color (str): Transition color for the fog.
            fog_start (float | int): Transition start distance/ratio.
            fog_end (float | int): Transition end distance/ratio. Must be greater than fog_start.
            render_distance_type (RenderDistanceType, optional): The type of render distance scaling.
                Defaults to RenderDistanceType.Render.

        Returns:
            _FogDistance: Returns self for method chaining.
        """
        if self._camera_location != "water":
            raise ValueError(
                "transition_fog can only be configured for the 'water' camera location."
            )
        if fog_start >= fog_end:
            raise ValueError(
                f"fog_end: [{fog_end}] must be greater than fog_start: [{fog_start}]."
            )
        self._distance[self._camera_location]["color"] = color
        self._distance[self._camera_location]["fog_start"] = fog_start
        self._distance[self._camera_location]["fog_end"] = fog_end
        self._distance[self._camera_location][
            "render_distance_type"
        ] = render_distance_type.value
        return self

    def __export__(self):
        """
        Return the instance's distance data.

        Returns:
            dict: The distance data representing distance properties.
        """
        return self._distance


class FogSettings(AddonObject):
    """
    Represents a Minecraft Fog resource pack definition.

    Generates a `.fog.json` file in the pack's `fogs/` directory. Fog settings define
    both distance-based fog properties and volumetric (PBR/Ray Tracing) settings.
    Settings are resolved in the game via the Active Fog Stack:
    Command (highest precedence) -> Biomes -> Data Default -> Engine Default (lowest).
    """

    _extension = ".fog.json"
    _path = os.path.join(CONFIG.RP_PATH, "fogs")
    _object_type = "Fog"

    def __init__(self, name: str = "fog", is_vanilla: bool = False) -> None:
        """Initializes a Fog definition instance.

        Args:
            name (str, optional): The identifier and filename of the fog setting. Defaults to "fog".
            is_vanilla (bool, optional): True if referencing/overriding a vanilla fog definition
                (under the `minecraft` namespace). Defaults to False.
        """
        super().__init__(name)
        self._description = MinecraftDescription(self.identifier, is_vanilla)
        self.content(JsonSchemes.fog())
        self._locations: list[_FogDistance] = []
        self._volumes = []

    def add_distance_location(
        self,
        color: str,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
        camera_location: FogCameraLocation = FogCameraLocation.Air,
    ):
        """Adds and configures distance-based fog settings for a specific camera location environment.

        Args:
            color (str): Hex color code of the fog (e.g. `"#ABD2FF"`). Maps to `fog_color` in JSON.
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
        self._locations.append(
            _FogDistance(
                color, fog_start, fog_end, render_distance_type, camera_location
            )
        )
        return self._locations[-1]

    def water_density(
        self,
        max_density: float,
        uniform: bool = True,
        zero_density_height: float = 0.0,
        max_density_height: float = 0.0,
    ):
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
            RuntimeError: If PBR is not enabled in CONFIG.
            ValueError: If zero_density_height is less than max_density_height.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        if not uniform and zero_density_height < max_density_height:
            raise ValueError(
                f"zero_density_height ({zero_density_height}) must be greater than or equal to "
                f"max_density_height ({max_density_height})."
            )

        volumetric = self._content["minecraft:fog_settings"].setdefault(
            "volumetric", {}
        )
        density = volumetric.setdefault("density", {})
        data = {
            "max_density": clamp(max_density, 0.0, 1.0),
            "uniform": uniform,
        }
        if not uniform:
            data["zero_density_height"] = zero_density_height
            data["max_density_height"] = max_density_height
        density["water"] = data
        return self

    def air_density(
        self,
        max_density: float,
        uniform: bool = False,
        zero_density_height: float = 0.0,
        max_density_height: float = 0.0,
    ):
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
            RuntimeError: If PBR is not enabled in CONFIG.
            ValueError: If zero_density_height is less than max_density_height.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        if not uniform and zero_density_height < max_density_height:
            raise ValueError(
                f"zero_density_height ({zero_density_height}) must be greater than or equal to "
                f"max_density_height ({max_density_height})."
            )

        volumetric = self._content["minecraft:fog_settings"].setdefault(
            "volumetric", {}
        )
        density = volumetric.setdefault("density", {})
        data = {
            "max_density": clamp(max_density, 0.0, 1.0),
            "uniform": uniform,
        }
        if not uniform:
            data["zero_density_height"] = zero_density_height
            data["max_density_height"] = max_density_height
        density["air"] = data
        return self

    def media_coefficients(
        self,
        water_scattering: Color | None = None,
        water_absorption: Color | None = None,
        air_scattering: Color | None = None,
        air_absorption: Color | None = None,
    ):
        """Sets media scattering and absorption RGB coefficients for water and air volumetric mediums.

        Args:
            water_scattering (Color, optional): RGB scattering multipliers.
            water_absorption (Color, optional): RGB absorption multipliers.
            air_scattering (Color, optional): RGB scattering multipliers.
            air_absorption (Color, optional): RGB absorption multipliers.

        Raises:
            RuntimeError: If PBR is not enabled in CONFIG.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        volumetric = self._content["minecraft:fog_settings"].setdefault(
            "volumetric", {}
        )
        media = volumetric.setdefault("media_coefficients", {})

        if water_scattering is not None or water_absorption is not None:
            media["water"] = {
                "scattering": (
                    AnvilFormatter.convert_color(water_scattering, RGB)
                    if water_scattering
                    else [0, 0, 0]
                ),
                "absorption": (
                    AnvilFormatter.convert_color(water_absorption, RGB)
                    if water_absorption
                    else [0, 0, 0]
                ),
            }
        if air_scattering is not None or air_absorption is not None:
            media["air"] = {
                "scattering": (
                    AnvilFormatter.convert_color(air_scattering, RGB)
                    if air_scattering
                    else [0, 0, 0]
                ),
                "absorption": (
                    AnvilFormatter.convert_color(air_absorption, RGB)
                    if air_absorption
                    else [0, 0, 0]
                ),
            }
        return self

    def henyey_greenstein_g(self, air_g: float = 0.0, water_g: float = 0.0):
        """Sets Henyey-Greenstein phase function asymmetry parameters for air and water.
        Supported in format_version 1.21.90+ and only applicable in Vibrant Visuals (PBR) packs.

        Args:
            air_g (float, optional): Asymmetry factor for air scattering. Range [-1.0 (back-scattering),
                1.0 (forward-scattering)]. Default is 0.75.
            water_g (float, optional): Asymmetry factor for water scattering. Range [-1.0 (back-scattering),
                1.0 (forward-scattering)]. Default is 0.6.

        Raises:
            RuntimeError: If PBR is not enabled in CONFIG.
        """
        if not CONFIG.PBR:
            raise RuntimeError(
                "Volumetric fog settings require PBR to be enabled in the config."
            )
        volumetric = self._content["minecraft:fog_settings"].setdefault(
            "volumetric", {}
        )
        hg = volumetric.setdefault("henyey_greenstein_g", {})
        hg["air"] = {"henyey_greenstein_g": clamp(air_g, -1.0, 1.0)}
        hg["water"] = {"henyey_greenstein_g": clamp(water_g, -1.0, 1.0)}
        return self

    def queue(self):
        """
        Validates, orders the JSON structure canonically, and queues the fog file for export.

        Arranges properties in the canonical order: `description` -> `distance` -> `volumetric`
        as required or recommended by Minecraft Bedrock schemas.
        """
        fog_settings = self._content["minecraft:fog_settings"]

        # Build in canonical order: description → distance → volumetric
        ordered: dict = {}

        # 1. description always comes first
        ordered.update(self._description.__export__())

        # 2. distance only if any locations were configured
        if self._locations:
            distance: dict = {}
            for location in self._locations:
                distance.update(location.__export__())
            ordered["distance"] = distance

        # 3. volumetric is written directly into fog_settings by the volumetric
        #    helper methods (water_density, air_density, etc.) — pull it across
        #    if present so it ends up last.
        if "volumetric" in fog_settings:
            ordered["volumetric"] = fog_settings["volumetric"]

        self._content["minecraft:fog_settings"] = ordered
        return super().queue()


Fog = FogSettings
