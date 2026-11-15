"""The `minecraft:weighted_random_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import JsonObject, Length, NonNegative, json_field


class _WeightedRandomFeature(_Feature):
    """The `minecraft:weighted_random_feature` body."""

    features: Annotated[
        list[tuple[str, Annotated[float, NonNegative]]], Length(minimum=1)
    ] = json_field(default_factory=list)

    def add_feature(self, feature: str, weight: float) -> None:
        """Adds a feature that can be picked, with its weight."""
        self.features.append((feature, weight))


class _WeightedRandomFeatureFile(JsonObject):
    """The content of a weighted random feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:weighted_random_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _WeightedRandomFeature = json_field(
        key="minecraft:weighted_random_feature", default_factory=_WeightedRandomFeature
    )


class WeightedRandomFeature(Feature[_WeightedRandomFeatureFile]):
    """Places one feature, picked at random by weight.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_weighted_random_feature)
    """

    def add_feature(
        self, feature: "Feature | str", weight: float = 1.0
    ) -> "WeightedRandomFeature":
        """Adds a feature that can be picked.

        Args:
            feature (Feature | str): The feature, or its identifier.
            weight (float, optional): Its weight, relative to the others. Defaults to 1.
        """
        self._feature.add_feature(str(feature), weight)
        return self

    def features(
        self, feature_list: Sequence[tuple["Feature | str", float]]
    ) -> "WeightedRandomFeature":
        """Adds features that can be picked.

        Args:
            feature_list (Sequence[tuple[Feature | str, float]]): `(feature, weight)` pairs.
        """
        for feature, weight in feature_list:
            self.add_feature(feature, weight)
        return self
