"""The `minecraft:surface_relative_threshold_feature`."""

from typing import Annotated, ClassVar

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import JsonObject, NonNegative, json_field


class _SurfaceRelativeThresholdFeature(_Feature):
    """The `minecraft:surface_relative_threshold_feature` body."""

    feature_to_place: str = json_field()
    minimum_distance_below_surface: Annotated[int, NonNegative] | None = None


class _SurfaceRelativeThresholdFeatureFile(JsonObject):
    """The content of a surface relative threshold feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:surface_relative_threshold_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _SurfaceRelativeThresholdFeature | None = json_field(
        key="minecraft:surface_relative_threshold_feature", default=None
    )

    def set_feature(self, feature: _SurfaceRelativeThresholdFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class SurfaceRelativeThresholdFeature(Feature):
    """Places a feature only when its position is below the estimated surface of the
    world. Only works in the Overworld, with the 1.18 world generation or later.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_surface_relative_threshold_feature)
    """

    _document = _SurfaceRelativeThresholdFeatureFile

    def __init__(
        self,
        name: str,
        feature_to_place: "Feature | str",
        minimum_distance_below_surface: int = 0,
    ) -> None:
        """Creates a surface relative threshold feature.

        Args:
            name (str): The name of the feature, also its file name.
            feature_to_place (Feature | str): The feature placed.
            minimum_distance_below_surface (int, optional): How many blocks below the
                surface the position must be. Defaults to 0.
        """
        super().__init__(name)
        self._content.set_feature(
            _SurfaceRelativeThresholdFeature(
                description=self._description(),
                feature_to_place=str(feature_to_place),
                minimum_distance_below_surface=minimum_distance_below_surface,
            )
        )
