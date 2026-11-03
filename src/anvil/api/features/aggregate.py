"""The `minecraft:aggregate_feature`."""

from typing import Annotated, ClassVar, Literal, Sequence

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import JsonObject, Length, json_field


class _AggregateFeature(_Feature):
    """The `minecraft:aggregate_feature` body."""

    features: Annotated[list[str], Length(minimum=1)] = json_field(default_factory=list)
    early_out: Literal["none", "first_failure", "first_success"] | None = None

    def add_features(self, features: Sequence[str]) -> None:
        """Adds features to place, all at the same position, in no guaranteed order."""
        self.features.extend(features)

    def set_early_out(
        self, early_out: Literal["none", "first_failure", "first_success"]
    ) -> None:
        """Stops placing features after the first success or the first failure."""
        self.early_out = early_out


class _AggregateFeatureFile(JsonObject):
    """The content of an aggregate feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:aggregate_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _AggregateFeature = json_field(
        key="minecraft:aggregate_feature", default_factory=_AggregateFeature
    )


class AggregateFeature(Feature):
    """Places a collection of features, all at the same position, in no guaranteed order.
    The features should not depend on each other.

    - Succeeds if at least one feature is placed.
    - Fails if every feature fails to be placed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_aggregate_feature)
    """

    _document = _AggregateFeatureFile

    def features(self, feature_list: Sequence["Feature | str"]) -> "AggregateFeature":
        """Adds features to place. At least one is needed.

        Args:
            feature_list (Sequence[Feature | str]): The features, or their identifiers.
        """
        self._feature.add_features([str(feature) for feature in feature_list])
        return self

    def early_out(
        self, early_out: Literal["none", "first_failure", "first_success"]
    ) -> "AggregateFeature":
        """Stops placing features after the first success or the first failure.

        Args:
            early_out (Literal["none", "first_failure", "first_success"]): When to stop.
        """
        self._feature.set_early_out(early_out)
        return self
