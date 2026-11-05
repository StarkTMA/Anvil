"""The `minecraft:multi_block_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import BlockId, JsonObject, json_field


class _MultiBlockFeature(_Feature):
    """The `minecraft:multi_block_feature` body."""

    __required__: ClassVar[tuple[str, ...]] = ("places_block",)

    places_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    enforce_placement_rules: bool | None = None
    randomize_rotation: bool | None = None
    may_replace: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None

    def set_places_block(self, block: str | Block | BlockDescriptor) -> None:
        """Sets the first part of the multi-block placed."""
        self.places_block = block

    def set_enforce_placement_rules(self, enforce: bool = True) -> None:
        """Sets whether each part checks the block's placement rules."""
        self.enforce_placement_rules = enforce

    def set_randomize_rotation(self, randomize: bool = True) -> None:
        """Sets whether the multi-block faces a random cardinal direction."""
        self.randomize_rotation = randomize

    def set_may_replace(self, blocks: Sequence[str | Block | BlockDescriptor]) -> None:
        """Sets the blocks the parts may replace."""
        self.may_replace = _blocks(blocks)

    def __validate__(self) -> None:
        if self.places_block is None:
            raise ValueError("A multi-block feature needs a block to place.")


class _MultiBlockFeatureFile(JsonObject):
    """The content of a multi-block feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:multi_block_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _MultiBlockFeature = json_field(
        key="minecraft:multi_block_feature", default_factory=_MultiBlockFeature
    )


class MultiBlockFeature(Feature[_MultiBlockFeatureFile]):
    """Places a multi-block, a block with the `minecraft:multi_block` trait.

    `places_block` must be the first part of the multi-block, the one whose
    `minecraft:multi_block_part` state is 0. Without `may_replace`, the parts can replace any
    block but the parts of other multi-blocks. With `randomize_rotation`, the multi-block
    needs a cardinal direction state. With `enforce_placement_rules`, each part checks it can
    be placed, including against its `minecraft:placement_filter`.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_multi_block_feature)
    """

    def __init__(
        self,
        name: str,
        places_block: str | Block | BlockDescriptor,
        randomize_rotation: bool = False,
        enforce_placement_rules: bool = False,
    ) -> None:
        """Creates a multi-block feature.

        Args:
            name (str): The name of the feature, also its file name.
            places_block (str | Block | BlockDescriptor): The first part of the multi-block.
            randomize_rotation (bool, optional): The multi-block faces a random cardinal
                direction. Defaults to False.
            enforce_placement_rules (bool, optional): Each part checks it can be placed.
                Defaults to False.
        """
        super().__init__(name)
        self._feature.set_places_block(places_block)
        if randomize_rotation:
            self._feature.set_randomize_rotation()
        if enforce_placement_rules:
            self._feature.set_enforce_placement_rules()

    def may_replace(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "MultiBlockFeature":
        """Sets the blocks the parts may replace.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_may_replace(blocks)
        return self
