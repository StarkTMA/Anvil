"""The `minecraft:partially_exposed_blob_feature`."""

from typing import Annotated, ClassVar, Literal

from anvil.api.core.enums import BlockFaceValues
from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import Chance, InRange, JsonObject, json_field
from anvil.lib.schemas import MinecraftBlockDescriptor


class _PartiallyExposedBlobFeature(_Feature):
    """The `minecraft:partially_exposed_blob_feature` body."""

    places_block: str | MinecraftBlockDescriptor = json_field()
    placement_radius_around_floor: Annotated[int, InRange(1, 8)] = json_field()
    placement_probability_per_valid_position: Annotated[float, Chance] = json_field()
    exposed_face: Literal["up", "down", "north", "south", "east", "west"] | None = None


class _PartiallyExposedBlobFeatureFile(JsonObject):
    """The content of a partially exposed blob feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:partially_exposed_blob_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _PartiallyExposedBlobFeature | None = json_field(
        key="minecraft:partially_exposed_blob_feature", default=None
    )

    def set_feature(self, feature: _PartiallyExposedBlobFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class PartiallyExposedBlobFeature(Feature):
    """Places a blob of a block, embedded in the surface but for one face that may be
    exposed to air or water.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_partially_exposed_blob_feature)
    """

    _document = _PartiallyExposedBlobFeatureFile

    def __init__(
        self,
        name: str,
        places_block: str | MinecraftBlockDescriptor,
        placement_radius_around_floor: int,
        placement_probability_per_valid_position: float,
        exposed_face: BlockFaceValues | None = BlockFaceValues.Up,
    ) -> None:
        """Creates a partially exposed blob feature.

        Args:
            name (str): The name of the feature, also its file name.
            places_block (str | MinecraftBlockDescriptor): The block placed.
            placement_radius_around_floor (int): The cubic radius of the blob, from 1 to 8.
            placement_probability_per_valid_position (float): The chance a block is placed
                at each valid position, from 0 to 1.
            exposed_face (BlockFaceValues, optional): The face that may be exposed: up,
                down, north, south, east or west. Defaults to up.
        """
        super().__init__(name)
        self._content.set_feature(
            _PartiallyExposedBlobFeature(
                description=self._description(),
                places_block=places_block,
                placement_radius_around_floor=placement_radius_around_floor,
                placement_probability_per_valid_position=placement_probability_per_valid_position,
                exposed_face=exposed_face,
            )
        )
