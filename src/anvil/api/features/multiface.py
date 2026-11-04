"""The `minecraft:multiface_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import BlockId, Chance, InRange, JsonObject, Length, json_field


class _MultifaceFeature(_Feature):
    """The `minecraft:multiface_feature` body."""

    places_block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    search_range: Annotated[int, InRange(1, 64)] = json_field()
    can_place_on_floor: bool = json_field()
    can_place_on_ceiling: bool = json_field()
    can_place_on_wall: bool = json_field()
    chance_of_spreading: Annotated[float, Chance] = json_field()
    can_place_on: (
        Annotated[
            list[Annotated[str | Block | BlockDescriptor, BlockId]], Length(minimum=1)
        ]
        | None
    ) = None

    def set_can_place_on(self, blocks: Sequence[str | Block | BlockDescriptor]) -> None:
        """Sets the blocks the block can be placed on."""
        self.can_place_on = _blocks(blocks)


class _MultifaceFeatureFile(JsonObject):
    """The content of a multiface feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:multiface_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _MultifaceFeature | None = json_field(
        key="minecraft:multiface_feature", default=None
    )

    def set_feature(self, feature: _MultifaceFeature) -> None:
        """Sets the body of the feature."""
        self.feature = feature


class MultifaceFeature(Feature):
    """Places a block on floors, walls or ceilings, and spreads it around, such as glow
    lichen. Any block can be placed.

    - Succeeds if at least one block is placed.
    - Fails if every placement fails.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_multiface_feature)
    """

    _document = _MultifaceFeatureFile

    def __init__(
        self,
        name: str,
        places_block: str | Block | BlockDescriptor,
        search_range: int,
        can_place_on_floor: bool,
        can_place_on_ceiling: bool,
        can_place_on_wall: bool,
        chance_of_spreading: float,
        can_place_on: Sequence[str | Block | BlockDescriptor] | None = None,
    ) -> None:
        """Creates a multiface feature.

        Args:
            name (str): The name of the feature, also its file name.
            places_block (str | Block | BlockDescriptor): The block placed.
            search_range (int): How far, in blocks, a valid position is searched for, from
                1 to 64.
            can_place_on_floor (bool): The block can be placed on the top face of a block.
            can_place_on_ceiling (bool): The block can be placed on the bottom face of a
                block.
            can_place_on_wall (bool): The block can be placed on the side faces of a block.
            chance_of_spreading (float): The chance each placed block spreads to another,
                from 0 to 1.
            can_place_on (Sequence[str | Block | BlockDescriptor], optional): The blocks it
                can be placed on. Any block when left out.
        """
        super().__init__(name)
        self._content.set_feature(
            _MultifaceFeature(
                description=self._description(),
                places_block=places_block,
                search_range=search_range,
                can_place_on_floor=can_place_on_floor,
                can_place_on_ceiling=can_place_on_ceiling,
                can_place_on_wall=can_place_on_wall,
                chance_of_spreading=chance_of_spreading,
            )
        )
        if can_place_on is not None:
            self.can_place_on(can_place_on)

    def can_place_on(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "MultifaceFeature":
        """Sets the blocks the block can be placed on.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks. At least one.
        """
        self._feature.set_can_place_on(blocks)
        return self
