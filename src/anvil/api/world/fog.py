import os

from anvil.lib.config import CONFIG
from anvil.lib.enums import FogCameraLocation, RenderDistanceType
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription


class _FogDistance:
    """
    Class to handle fog distances based on camera location, color, and other parameters. Allows for setting fog color,
    distance, and transition.

    Attributes:
        _camera_location (FogCameraLocation): Specifies the location of the camera.
        _distance (dict): A dictionary containing the fog properties related to the camera location.
    """

    def __init__(
        self, camera_location: FogCameraLocation = FogCameraLocation.Air
    ) -> None:
        """
        Initialize the _FogDistance instance.

        Parameters:
            camera_location (FogCameraLocation, optional): Enum specifying the location of the camera. Defaults to FogCameraLocation.Air.
        """
        self._camera_location = camera_location.value
        self._distance = {self._camera_location: {}}

    def color(self, color: str):
        """
        Set the color of the fog.

        Parameters:
            color (str | hex): The color to set the fog.

        Returns:
            _FogDistance: Returns self for chaining.
        """
        self._distance[self._camera_location]["fog_color"] = color
        return self

    def distance(
        self,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
    ):
        """
        Set the starting and ending distance of the fog along with the render distance type.

        Parameters:
            fog_start (int): The starting distance of the fog.
            fog_end (int): The ending distance of the fog.
            render_distance_type (RenderDistanceType, optional): The type of render distance. Defaults to RenderDistanceType.Render.

        Returns:
            _FogDistance: Returns self for chaining.
        """
        if fog_start >= fog_end:
            raise ValueError(
                f"fog_end: [{fog_end}] must be greater than fog_start: [{fog_start}]."
            )

        self._distance[self._camera_location]["fog_start"] = fog_start
        self._distance[self._camera_location]["fog_end"] = fog_end
        self._distance[self._camera_location][
            "render_distance_type"
        ] = render_distance_type.value
        return self

    def transition_fog(
        self,
        color: str,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
    ):
        """
        Set the color, starting and ending distance of the fog for transitioning along with the render distance type.

        Parameters:
            color (str): The color to set the fog.
            fog_start (int): The starting distance of the fog.
            fog_end (int): The ending distance of the fog.
            render_distance_type (RenderDistanceType, optional): The type of render distance. Defaults to RenderDistanceType.Render.

        Returns:
            _FogDistance: Returns self for chaining.
        """
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

    def _export(self):
        """
        Return the instance's distance data.

        Returns:
            dict: The distance data of the instance.
        """
        return self._distance


class Fog(AddonObject):
    """A class representing a Fog."""

    _extension = ".fog.json"
    _path = os.path.join(CONFIG.RP_PATH, "fogs")
    _object_type = "Fog"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes a Fog instance.

        Parameters:
            name (str): The name of the fog.
            is_vanilla (bool, optional): Whether the fog is a vanilla fog. Defaults to False.
        """
        super().__init__(name)
        self._description = MinecraftDescription(self.identifier, is_vanilla)
        self._fog = JsonSchemes.fog()
        self._locations: list[_FogDistance] = []
        self._volumes = []

    def add_distance_location(
        self, camera_location: FogCameraLocation = FogCameraLocation.Air
    ):
        """Adds a distance location to the fog.

        Parameters:
            camera_location (FogCameraLocation, optional): The camera location of the fog. Defaults to FogCameraLocation.Air.
        """
        self._locations.append(_FogDistance(camera_location))
        return self._locations[-1]

    def add_volume(self):
        pass

    def queue(self):
        """Queues the fog to be exported."""
        for location in self._locations:
            self._fog["minecraft:fog_settings"]["distance"].update(location._export())
        self._fog["minecraft:fog_settings"].update(self._description._export())
        self.content(self._fog)
        return super().queue()
