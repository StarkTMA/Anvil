"""The `minecraft:scatter_feature`."""

from typing import ClassVar

from anvil.api.features.feature import (
    DistributionMixin,
    Feature,
    _Feature,
    _ScatterParams,
)
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import JsonObject, json_field


class _ScatterFeature(_Feature):
    """The `minecraft:scatter_feature` body."""

    __required__: ClassVar[tuple[str, ...]] = ("places_feature", "distribution")

    places_feature: str | None = None
    project_input_to_floor: bool | None = None
    distribution: _ScatterParams | None = None

    def set_places_feature(self, feature: str) -> None:
        """Sets the feature scattered."""
        self.places_feature = feature

    def set_project_input_to_floor(self, project: bool = True) -> None:
        """Sets whether the scattered positions snap to the terrain height."""
        self.project_input_to_floor = project

    def set_distribution(self, distribution: _ScatterParams) -> None:
        """Sets where, how many times and how likely the feature is placed."""
        self.distribution = distribution

    def __validate__(self) -> None:
        if self.places_feature is None or self.distribution is None:
            raise ValueError("A scatter feature needs a feature and a distribution.")


class _ScatterFeatureFile(JsonObject):
    """The content of a scatter feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:scatter_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _ScatterFeature = json_field(
        key="minecraft:scatter_feature", default_factory=_ScatterFeature
    )


class ScatterFeature(DistributionMixin, Feature[_ScatterFeatureFile]):
    """Places a feature several times around its position, as set by `distribution()`.

    Coordinates are offsets from the position, not absolute positions. The scatter chance
    is checked once: either every iteration runs, or none does.

    - Succeeds if at least one placement succeeds.
    - Fails if every placement fails.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_scatter_feature)
    """

    def __init__(
        self,
        name: str,
        places_feature: "Feature | str",
        project_input_to_floor: bool = False,
    ) -> None:
        """Creates a scatter feature. Set its distribution next.

        Args:
            name (str): The name of the feature, also its file name.
            places_feature (Feature | str): The feature scattered.
            project_input_to_floor (bool, optional): Snap the y of each position to the
                terrain height. Defaults to False.
        """
        super().__init__(name)
        self._feature.set_places_feature(str(places_feature))
        self._feature.set_project_input_to_floor(project_input_to_floor)

    def _distribution_owner(self) -> _ScatterFeature:
        return self._feature
