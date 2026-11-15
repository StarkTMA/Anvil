"""The `minecraft:ore_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    AtLeastOne,
    BlockId,
    Chance,
    JsonObject,
    Length,
    json_field,
)


class _OreReplaceRule(JsonObject):
    """A `replace_rules` entry of an ore feature."""

    places_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    may_replace: (
        Annotated[
            list[Annotated[str | Block | BlockDescriptor, BlockId]], Length(minimum=1)
        ]
        | None
    ) = None


class _OreFeature(_Feature):
    """The `minecraft:ore_feature` body."""

    __required__: ClassVar[tuple[str, ...]] = ("count",)

    count: Annotated[int, AtLeastOne] | None = None
    discard_chance_on_air_exposure: Annotated[float, Chance] | None = None
    replace_rules: Annotated[list[_OreReplaceRule], Length(minimum=1)] | None = None

    def set_count(self, count: int) -> None:
        """Sets the number of blocks placed."""
        self.count = count

    def set_discard_chance_on_air_exposure(self, chance: float) -> None:
        """Sets the chance a block next to air is not placed."""
        self.discard_chance_on_air_exposure = chance

    def add_replace_rule(
        self,
        places_block: str | Block | BlockDescriptor,
        may_replace: Sequence[str | Block | BlockDescriptor] | None = None,
    ) -> None:
        """Adds a rule: the block placed, and the blocks it may replace."""
        rule = _OreReplaceRule(
            places_block=places_block,
            may_replace=None if may_replace is None else _blocks(may_replace),
        )
        self.replace_rules = [*(self.replace_rules or []), rule]

    def __validate__(self) -> None:
        if self.count is None:
            raise ValueError("An ore feature needs a count.")


class _OreFeatureFile(JsonObject):
    """The content of an ore feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:ore_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _OreFeature = json_field(
        key="minecraft:ore_feature", default_factory=_OreFeature
    )


class OreFeature(Feature[_OreFeatureFile]):
    """Places a vein of blocks, like an ore deposit. Any block can be placed.

    Each position checks the replace rules in order and uses the first one whose
    `may_replace` has the block there; a rule without `may_replace` replaces any block.

    - Succeeds if at least one block is placed.
    - Fails if every placement fails.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_ore_feature)
    """

    def __init__(
        self,
        name: str,
        count: int,
        discard_chance_on_air_exposure: float | None = None,
    ) -> None:
        """Creates an ore feature. Add replace rules next.

        Args:
            name (str): The name of the feature, also its file name.
            count (int): The number of blocks placed. At least 1.
            discard_chance_on_air_exposure (float, optional): The chance a block next to
                air is not placed, from 0 to 1.
        """
        super().__init__(name)
        self._feature.set_count(count)
        if discard_chance_on_air_exposure is not None:
            self._feature.set_discard_chance_on_air_exposure(
                discard_chance_on_air_exposure
            )

    def add_replace_rule(
        self,
        places_block: str | Block | BlockDescriptor,
        may_replace: Sequence[str | Block | BlockDescriptor] | None = None,
    ) -> "OreFeature":
        """Adds a replace rule.

        Args:
            places_block (str | Block | BlockDescriptor): The block placed.
            may_replace (Sequence[str | Block | BlockDescriptor], optional): The blocks it
                may replace. Any block when left out.
        """
        self._feature.add_replace_rule(places_block, may_replace)
        return self
