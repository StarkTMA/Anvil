"""Feature rules: they attach one feature to biomes, and say when and where it is placed."""

from typing import ClassVar, Sequence

from anvil.api.core.enums import FeatureRulePlacementPass
from anvil.api.core.filters import Filter
from anvil.api.features.feature import DistributionMixin, Feature, _ScatterParams
from anvil.lib.config import Pack
from anvil.lib.format_versions import FEATURE_RULE_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, json_field


class _FeatureRuleDescription(JsonObject):
    """The `description` of a feature rule."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier", "places_feature")

    identifier: str | None = None
    places_feature: str | None = None

    def set_description(self, identifier: str, places_feature: str) -> None:
        """Sets the rule's identifier and the feature it places."""
        self.identifier = identifier
        self.places_feature = places_feature

    def __validate__(self) -> None:
        if self.identifier is None or self.places_feature is None:
            raise ValueError(
                "A feature rule needs an identifier and a feature to place."
            )


class _FeatureRuleConditions(JsonObject):
    """The `conditions` of a feature rule."""

    __required__: ClassVar[tuple[str, ...]] = ("placement_pass",)

    placement_pass: FeatureRulePlacementPass | None = None
    biome_filter: Filter | list[Filter] | None = json_field(
        key="minecraft:biome_filter", default=None
    )

    def set_placement_pass(self, placement_pass: FeatureRulePlacementPass) -> None:
        """Sets the pass the rule runs in."""
        self.placement_pass = placement_pass

    def set_biome_filter(self, filters: Filter | Sequence[Filter]) -> None:
        """Sets the filter the biomes must pass."""
        self.biome_filter = filters if isinstance(filters, Filter) else list(filters)

    def __validate__(self) -> None:
        if self.placement_pass is None:
            raise ValueError("A feature rule needs a placement pass.")


class _FeatureRule(JsonObject):
    """The `minecraft:feature_rules` object."""

    description: _FeatureRuleDescription = json_field(
        default_factory=_FeatureRuleDescription
    )
    conditions: _FeatureRuleConditions = json_field(
        default_factory=_FeatureRuleConditions
    )
    distribution: _ScatterParams | None = None

    def set_distribution(self, distribution: _ScatterParams) -> None:
        """Sets where, how many times and how likely the feature is placed."""
        self.distribution = distribution


class _FeatureRuleFile(JsonObject):
    """The content of a feature rule file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:feature_rules",
    )

    format_version: str = json_field(default=FEATURE_RULE_VERSION, init=False)
    feature_rules: _FeatureRule = json_field(
        key="minecraft:feature_rules", default_factory=_FeatureRule
    )


class FeatureRule(DistributionMixin, JsonFile):
    """Attaches one feature to the biomes that pass its biome filter, and says in which
    pass and where in each chunk the feature is placed.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction#feature-rules)
    """

    _document = _FeatureRuleFile
    _object_type = "Feature Rule"
    _extension = ".json"
    _pack = Pack.BP
    _folder = "feature_rules"

    def __init__(
        self,
        name: str,
        feature: Feature | str,
        placement_pass: FeatureRulePlacementPass,
    ) -> None:
        """Creates a feature rule.

        Args:
            name (str): The name of the rule, also its file name. The identifier is
                `<namespace>:<name>`.
            feature (Feature | str): The feature the rule places, or its identifier.
            placement_pass (FeatureRulePlacementPass): The pass the rule runs in. Earlier
                passes run before later ones; rules of one pass run in no set order.
        """
        super().__init__(name)
        rule = self._content.feature_rules
        rule.description.set_description(self.identifier, str(feature))
        rule.conditions.set_placement_pass(placement_pass)

    def biome_filter(self, filters: Filter | Sequence[Filter]) -> "FeatureRule":
        """Sets the biomes the rule attaches its feature to, usually with
        `Filter.has_biome_tag`. A list of filters must all pass.

        Args:
            filters (Filter | Sequence[Filter]): The filter, a group of filters such as
                `Filter.any_of(...)`, or a list of filters.
        """
        self._content.feature_rules.conditions.set_biome_filter(filters)
        return self

    def _distribution_owner(self) -> _FeatureRule:
        return self._content.feature_rules

    def queue(self) -> "FeatureRule":
        """Queues the feature rule for export."""
        return super().queue()
