"""The `minecraft:growing_plant_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    ExactRangeMinMax,
    JsonObject,
    NonNegative,
    json_field,
)


class _GrowingPlantFeature(_Feature):
    """The `minecraft:growing_plant_feature` body."""

    __required__: ClassVar[tuple[str, ...]] = (
        "height_distribution",
        "growth_direction",
        "body_blocks",
        "head_blocks",
    )

    height_distribution: list[
        tuple[
            Annotated[float | tuple[float, float], ExactRangeMinMax],
            Annotated[float, NonNegative],
        ]
    ] = json_field(default_factory=list)
    growth_direction: Literal["UP", "DOWN"] | None = None
    age: Annotated[float | tuple[float, float], ExactRangeMinMax] | None = None
    body_blocks: list[
        tuple[
            Annotated[str | Block | BlockDescriptor, BlockId],
            Annotated[float, NonNegative],
        ]
    ] = json_field(default_factory=list)
    head_blocks: list[
        tuple[
            Annotated[str | Block | BlockDescriptor, BlockId],
            Annotated[float, NonNegative],
        ]
    ] = json_field(default_factory=list)
    allow_water: bool | None = None

    def set_growth_direction(self, growth_direction: Literal["UP", "DOWN"]) -> None:
        """Sets whether the plant grows up from the floor or down from the ceiling."""
        self.growth_direction = growth_direction

    def set_age(self, age: float | tuple[float, float]) -> None:
        """Sets the age of the head of the plant, or a range it is picked from."""
        self.age = age

    def set_allow_water(self, allow_water: bool = True) -> None:
        """Sets whether the plant can be placed in water."""
        self.allow_water = allow_water

    def add_height_distribution(
        self, height: float | tuple[float, float], weight: float
    ) -> None:
        """Adds a height, or a range it is picked from, with its weight."""
        self.height_distribution.append((height, weight))

    def add_body_block(
        self, block: str | Block | BlockDescriptor, weight: float
    ) -> None:
        """Adds a body block with its weight."""
        self.body_blocks.append((block, weight))

    def add_head_block(
        self, block: str | Block | BlockDescriptor, weight: float
    ) -> None:
        """Adds a head block with its weight."""
        self.head_blocks.append((block, weight))

    def __validate__(self) -> None:
        if self.growth_direction is None:
            raise ValueError("A growing plant feature needs a growth direction.")
        for key in ("height_distribution", "body_blocks", "head_blocks"):
            if not getattr(self, key):
                raise ValueError(f"A growing plant feature needs at least one {key}.")


class _GrowingPlantFeatureFile(JsonObject):
    """The content of a growing plant feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:growing_plant_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _GrowingPlantFeature = json_field(
        key="minecraft:growing_plant_feature", default_factory=_GrowingPlantFeature
    )


class GrowingPlantFeature(Feature[_GrowingPlantFeatureFile]):
    """Places a growing plant: a column anchored to the floor or the ceiling, made of body
    blocks and a head block at its tip, such as cave vines.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_growing_plant_feature)
    """

    def __init__(
        self,
        name: str,
        growth_direction: Literal["UP", "DOWN"],
        age: float | tuple[float, float] | None = None,
        allow_water: bool = False,
    ) -> None:
        """Creates a growing plant feature. Add heights, body blocks and head blocks next.

        Args:
            name (str): The name of the feature, also its file name.
            growth_direction (Literal["UP", "DOWN"]): Whether the plant grows up from the
                floor or down from the ceiling.
            age (float | tuple[float, float], optional): The age of the head, or a range it
                is picked from.
            allow_water (bool, optional): The plant can be placed in water. Defaults to
                False.
        """
        super().__init__(name)
        self._feature.set_growth_direction(growth_direction)
        self._feature.set_allow_water(allow_water)
        if age is not None:
            self.age(age)

    def age(self, age: float | tuple[float, float]) -> "GrowingPlantFeature":
        """Sets the age of the head of the plant.

        Args:
            age (float | tuple[float, float]): The age, or a range it is picked from.
        """
        self._feature.set_age(age)
        return self

    def add_height(
        self, height: float | tuple[float, float], weight: float = 1.0
    ) -> "GrowingPlantFeature":
        """Adds a height the plant can have.

        Args:
            height (float | tuple[float, float]): The height, or a range it is picked from.
            weight (float, optional): Its weight, relative to the others. Defaults to 1.
        """
        self._feature.add_height_distribution(height, weight)
        return self

    def height_distribution(
        self, heights: Sequence[tuple[float | tuple[float, float], float]]
    ) -> "GrowingPlantFeature":
        """Adds heights the plant can have.

        Args:
            heights (Sequence[tuple[float | tuple[float, float], float]]): `(height, weight)`
                pairs.
        """
        for height, weight in heights:
            self.add_height(height, weight)
        return self

    def add_body_block(
        self, block: str | Block | BlockDescriptor, weight: float = 1.0
    ) -> "GrowingPlantFeature":
        """Adds a block the body can be made of.

        Args:
            block (str | Block | BlockDescriptor): The block.
            weight (float, optional): Its weight, relative to the others. Defaults to 1.
        """
        self._feature.add_body_block(block, weight)
        return self

    def body_blocks(
        self, blocks: Sequence[tuple[str | Block | BlockDescriptor, float]]
    ) -> "GrowingPlantFeature":
        """Adds blocks the body can be made of.

        Args:
            blocks (Sequence[tuple[str | Block | BlockDescriptor, float]]): `(block,
                weight)` pairs.
        """
        for block, weight in blocks:
            self.add_body_block(block, weight)
        return self

    def add_head_block(
        self, block: str | Block | BlockDescriptor, weight: float = 1.0
    ) -> "GrowingPlantFeature":
        """Adds a block the head can be.

        Args:
            block (str | Block | BlockDescriptor): The block.
            weight (float, optional): Its weight, relative to the others. Defaults to 1.
        """
        self._feature.add_head_block(block, weight)
        return self

    def head_blocks(
        self, blocks: Sequence[tuple[str | Block | BlockDescriptor, float]]
    ) -> "GrowingPlantFeature":
        """Adds blocks the head can be.

        Args:
            blocks (Sequence[tuple[str | Block | BlockDescriptor, float]]): `(block,
                weight)` pairs.
        """
        for block, weight in blocks:
            self.add_head_block(block, weight)
        return self
