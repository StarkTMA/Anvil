import os
from typing import Any

from anvil.api.core.enums import FeatureRulePlacementPass
from anvil.api.core.filters import Filter
from anvil.api.core.types import Identifier
from anvil.api.features.features import DistributionMixin, Feature
from anvil.lib.config import CONFIG
from anvil.lib.schemas import AddonObject, JsonSchemes


class FeatureRule(AddonObject, DistributionMixin):
    """Controls where and when a feature is placed during world generation.

    Each feature rule controls exactly one feature and can attach that feature to
    biomes via minecraft:biome_filter, while placement_pass controls when the
    rule runs relative to other feature rules.

    ## Documentation reference:
        https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction?view=minecraft-bedrock-stable#feature-rules
    """

    _object_type = "Feature Rule"
    _extension = ".json"
    _template_name = "feature_rule_base"
    _path = os.path.join(
        CONFIG.BP_PATH,
        "feature_rules",
    )

    def __init__(
        self,
        name: str,
        feature: Identifier | Feature,
        placement_pass: FeatureRulePlacementPass,
    ):
        """Creates a feature rule that controls where and when one feature is placed.

        Parameters:
            name (str): The name of this feature rule. The resulting identifier
                uses the format 'namespace_name:rule_name'. 'rule_name' must
                match the filename.
            feature (Identifier | Feature): Named reference to the feature
                controlled by this rule.
            placement_pass (FeatureRulePlacementPass): When the feature should
                be placed relative to others. Earlier passes are guaranteed to
                occur before later passes, but order is not guaranteed within
                each pass.

        ## Documentation reference:
            https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction?view=minecraft-bedrock-stable#feature-rules
        """
        super().__init__(name, False)
        self.content(JsonSchemes.worldgen_feature_rule(self.identifier, str(feature)))
        self._content["minecraft:feature_rules"].setdefault("conditions", {})[
            "placement_pass"
        ] = str(placement_pass)

    def biome_filter(
        self,
        filters: Filter | dict[str, Any] | list[Filter | dict[str, Any]],
    ):
        """Sets the minecraft:biome_filter Filter Group.

        This determines which biomes the rule attaches to. Filter groups may be
        expressed as a single filter object, a grouped filter object such as
        all_of/any_of/none_of, or a list of filter tests.
        """
        self._content["minecraft:feature_rules"].setdefault("conditions", {})[
            "minecraft:biome_filter"
        ] = filters

    def _distribution_target(self) -> dict[str, Any]:
        return self._content["minecraft:feature_rules"]

    def queue(self):
        """Queues the feature rule definition for export."""
        return super().queue()
