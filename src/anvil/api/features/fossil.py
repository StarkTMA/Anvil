"""The `minecraft:fossil_feature`."""

from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import BlockId, JsonObject, NonNegative, json_field


class _FossilFeature(_Feature):
    """The `minecraft:fossil_feature` body."""

    __required__: ClassVar[tuple[str, ...]] = ("ore_block", "max_empty_corners")

    ore_block: Annotated[str | Block | BlockDescriptor, BlockId] | None = None
    max_empty_corners: Annotated[int, NonNegative] | None = None

    def set_fossil(
        self, ore_block: str | Block | BlockDescriptor, max_empty_corners: int
    ) -> None:
        """Sets the ore block and how many corners may be empty."""
        self.ore_block = ore_block
        self.max_empty_corners = max_empty_corners

    def __validate__(self) -> None:
        if self.ore_block is None or self.max_empty_corners is None:
            raise ValueError(
                "A fossil feature needs an ore block and max_empty_corners."
            )


class _FossilFeatureFile(JsonObject):
    """The content of a fossil feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:fossil_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _FossilFeature = json_field(
        key="minecraft:fossil_feature", default_factory=_FossilFeature
    )


class FossilFeature(Feature):
    """Places a skeleton of bone blocks with ore blocks in it.

    - Succeeds if the fossil is placed.
    - Fails if it overlaps another structure, or too many corners of its bounding box are
      air or fluid.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_fossil_feature)
    """

    _document = _FossilFeatureFile

    def __init__(
        self,
        name: str,
        ore_block: str | Block | BlockDescriptor,
        max_empty_corners: int,
    ) -> None:
        """Creates a fossil feature.

        Args:
            name (str): The name of the feature, also its file name.
            ore_block (str | Block | BlockDescriptor): The ore block in the fossil.
            max_empty_corners (int): How many corners of the bounding box may be air or
                fluid. At least 0.
        """
        super().__init__(name)
        self._feature.set_fossil(ore_block, max_empty_corners)
