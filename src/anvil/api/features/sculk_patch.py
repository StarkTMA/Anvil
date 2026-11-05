"""The `minecraft:sculk_patch_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    Chance,
    ExactRangeMinMax,
    InRange,
    JsonObject,
    json_field,
)


class _SculkPatchFeature(_Feature):
    """The `minecraft:sculk_patch_feature` body."""

    can_place_sculk_patch_on: list[
        Annotated[str | Block | BlockDescriptor, BlockId]
    ] = json_field()
    central_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    central_block_placement_chance: Annotated[float, Chance] | None = None
    cursor_count: Annotated[int, InRange(0, 32)] = json_field()
    charge_amount: Annotated[int, InRange(1, 1000)] = json_field()
    spread_attempts: Annotated[int, InRange(1, 64)] = json_field()
    growth_rounds: Annotated[int, InRange(0, 8)] = json_field()
    spread_rounds: Annotated[int, InRange(0, 8)] = json_field()
    extra_growth_chance: (
        Annotated[float | tuple[float, float], ExactRangeMinMax] | None
    ) = None

    def set_can_place_sculk_patch_on(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> None:
        """Sets the blocks the patch can be placed on."""
        self.can_place_sculk_patch_on = _blocks(blocks)

    def set_central_block(
        self,
        block: str | Block | BlockDescriptor,
        placement_chance: float | None = None,
    ) -> None:
        """Sets the block placed at the centre of the patch, and the chance it is placed."""
        self.central_block = block
        if placement_chance is not None:
            self.central_block_placement_chance = placement_chance

    def set_extra_growth_chance(self, chance: float | tuple[float, float]) -> None:
        """Sets the extra growth chance, or a range it is picked from."""
        self.extra_growth_chance = chance


class _SculkPatchFeatureFile(JsonObject):
    """The content of a sculk patch feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:sculk_patch_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _SculkPatchFeature | None = json_field(
        key="minecraft:sculk_patch_feature", default=None
    )

    def set_feature(self, feature: _SculkPatchFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class SculkPatchFeature(Feature[_SculkPatchFeatureFile]):
    """Places a patch of sculk that spreads from cursors, with an optional block at its
    centre.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction)
    """

    def __init__(
        self,
        name: str,
        can_place_sculk_patch_on: Sequence[str | Block | BlockDescriptor],
        cursor_count: int,
        charge_amount: int,
        spread_attempts: int,
        growth_rounds: int,
        spread_rounds: int,
        central_block: str | Block | BlockDescriptor | None = None,
        central_block_placement_chance: float | None = None,
        extra_growth_chance: float | tuple[float, float] | None = None,
    ) -> None:
        """Creates a sculk patch feature.

        Args:
            name (str): The name of the feature, also its file name.
            can_place_sculk_patch_on (Sequence[str | Block | BlockDescriptor]): The blocks
                the patch can be placed on.
            cursor_count (int): The number of cursors, from 0 to 32.
            charge_amount (int): The charge of each cursor, from 1 to 1000.
            spread_attempts (int): The spread attempts of each cursor, from 1 to 64.
            growth_rounds (int): The growth rounds, from 0 to 8.
            spread_rounds (int): The spread rounds, from 0 to 8.
            central_block (str | Block | BlockDescriptor, optional): The block at the
                centre of the patch.
            central_block_placement_chance (float, optional): The chance the central block
                is placed, from 0 to 1.
            extra_growth_chance (float | tuple[float, float], optional): The extra growth
                chance, or a range it is picked from.
        """
        super().__init__(name)
        self._document.set_feature(
            _SculkPatchFeature(
                description=self._description(),
                can_place_sculk_patch_on=_blocks(can_place_sculk_patch_on),
                cursor_count=cursor_count,
                charge_amount=charge_amount,
                spread_attempts=spread_attempts,
                growth_rounds=growth_rounds,
                spread_rounds=spread_rounds,
            )
        )
        if central_block is not None:
            self.central_block(central_block, central_block_placement_chance)
        if extra_growth_chance is not None:
            self._feature.set_extra_growth_chance(extra_growth_chance)

    def can_place_sculk_patch_on(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "SculkPatchFeature":
        """Sets the blocks the patch can be placed on.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_can_place_sculk_patch_on(blocks)
        return self

    def central_block(
        self,
        block: str | Block | BlockDescriptor,
        placement_chance: float | None = None,
    ) -> "SculkPatchFeature":
        """Sets the block placed at the centre of the patch.

        Args:
            block (str | Block | BlockDescriptor): The block.
            placement_chance (float, optional): The chance it is placed, from 0 to 1.
        """
        self._feature.set_central_block(block, placement_chance)
        return self
