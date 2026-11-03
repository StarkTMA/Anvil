"""The `minecraft:sequence_feature`."""

from typing import Annotated, ClassVar, Sequence

from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import JsonObject, Length, json_field


class _SequenceFeature(_Feature):
    """The `minecraft:sequence_feature` body."""

    features: Annotated[list[str], Length(minimum=1)] = json_field(default_factory=list)

    def add_features(self, features: Sequence[str]) -> None:
        """Adds features to place in order, each at the position the previous one ended."""
        self.features.extend(features)


class _SequenceFeatureFile(JsonObject):
    """The content of a sequence feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:sequence_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _SequenceFeature = json_field(
        key="minecraft:sequence_feature", default_factory=_SequenceFeature
    )


class SequenceFeature(Feature):
    """Places a collection of features in order. Each feature starts at the position the
    previous one ended at.

    - Succeeds if every feature is placed.
    - Fails if any feature fails to be placed; the features after it are skipped.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_sequence_feature)
    """

    _document = _SequenceFeatureFile

    def features(self, feature_list: Sequence["Feature | str"]) -> "SequenceFeature":
        """Adds features to place in order. At least one is needed.

        Args:
            feature_list (Sequence[Feature | str]): The features, or their identifiers.
        """
        self._feature.add_features([str(feature) for feature in feature_list])
        return self
