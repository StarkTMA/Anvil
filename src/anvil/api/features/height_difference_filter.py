"""The `minecraft:height_difference_filter_feature`."""

from typing import Annotated, ClassVar

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import JsonObject, NonNegative, json_field


class _HeightDifferenceFilterFeature(_Feature):
    """The `minecraft:height_difference_filter_feature` body."""

    places_feature: str = json_field()
    search_radius: Annotated[int, NonNegative] | None = None
    min_required_upward_height_diff: int | None = None
    max_allowed_upward_height_diff: int | None = None
    min_required_downward_height_diff: int | None = None
    max_allowed_downward_height_diff: int | None = None


class _HeightDifferenceFilterFeatureFile(JsonObject):
    """The content of a height difference filter feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:height_difference_filter_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _HeightDifferenceFilterFeature | None = json_field(
        key="minecraft:height_difference_filter_feature", default=None
    )

    def set_feature(self, feature: _HeightDifferenceFilterFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class HeightDifferenceFilterFeature(Feature[_HeightDifferenceFilterFeatureFile]):
    """Places a feature only where the terrain has the right shape: the height differences
    up and down, within a radius in each cardinal direction, must be within the limits
    given. Useful for features that only fit cliffs, slopes or flat ground.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_height_difference_filter_feature)
    """

    def __init__(
        self,
        name: str,
        places_feature: "Feature | str",
        search_radius: int | None = None,
        min_required_upward_height_diff: int | None = None,
        max_allowed_upward_height_diff: int | None = None,
        min_required_downward_height_diff: int | None = None,
        max_allowed_downward_height_diff: int | None = None,
    ) -> None:
        """Creates a height difference filter feature.

        Args:
            name (str): The name of the feature, also its file name.
            places_feature (Feature | str): The feature placed when the terrain fits.
            search_radius (int, optional): How far, in each cardinal direction, heights are
                checked.
            min_required_upward_height_diff (int, optional): The least height difference
                upwards.
            max_allowed_upward_height_diff (int, optional): The greatest height difference
                upwards.
            min_required_downward_height_diff (int, optional): The least height difference
                downwards.
            max_allowed_downward_height_diff (int, optional): The greatest height difference
                downwards.
        """
        super().__init__(name)
        self._document.set_feature(
            _HeightDifferenceFilterFeature(
                description=self._description(),
                places_feature=str(places_feature),
                search_radius=search_radius,
                min_required_upward_height_diff=min_required_upward_height_diff,
                max_allowed_upward_height_diff=max_allowed_upward_height_diff,
                min_required_downward_height_diff=min_required_downward_height_diff,
                max_allowed_downward_height_diff=max_allowed_downward_height_diff,
            )
        )
