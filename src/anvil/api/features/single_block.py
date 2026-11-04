"""The `minecraft:single_block_feature`."""

from collections.abc import Sequence
from typing import Annotated, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.features.feature import Feature, _blocks, _Feature
from anvil.lib.format_versions import FEATURE_VERSION
from anvil.lib.jsonmodel import BlockId, InRange, JsonObject, NonNegative, json_field
from anvil.lib.jsonmodel.enums import BlockFaceValues


class _WeightedBlock(JsonObject):
    """A block of a single block feature's `places_block`, with its weight."""

    block: Annotated[str | Block | BlockDescriptor, BlockId] = json_field()
    weight: Annotated[float, NonNegative] = json_field()


class _MayNotAttachTo(JsonObject):
    """The `may_not_attach_to` of a single block feature: the blocks the block may not be
    next to, by face."""

    top: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    bottom: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    north: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    east: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    south: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    west: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    all: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    sides: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None
    diagonal: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None

    def add_face(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: Sequence[str | Block | BlockDescriptor],
    ) -> None:
        """Adds blocks to a face: `Up` is the top face, `Down` the bottom one and `Side`
        every side face."""
        key = {
            BlockFaceValues.Up: "top",
            BlockFaceValues.Down: "bottom",
            BlockFaceValues.Side: "sides",
        }.get(face, str(face))
        setattr(self, key, [*(getattr(self, key) or []), *_blocks(blocks)])


class _MayAttachTo(_MayNotAttachTo):
    """The `may_attach_to` of a single block feature: the blocks the block may be placed
    next to, by face."""

    min_sides_must_attach: Annotated[int, InRange(1, 4)] | None = None
    auto_rotate: bool | None = None

    def set_attach_rules(
        self, min_sides_must_attach: int | None, auto_rotate: bool | None
    ) -> None:
        """Sets how many side faces must attach, and whether the block rotates to attach."""
        if min_sides_must_attach is not None:
            self.min_sides_must_attach = min_sides_must_attach
        if auto_rotate is not None:
            self.auto_rotate = auto_rotate


class _SingleBlockFeature(_Feature):
    """The `minecraft:single_block_feature` body."""

    __required__: ClassVar[tuple[str, ...]] = ("places_block",)

    places_block: list[_WeightedBlock] = json_field(default_factory=list)
    enforce_placement_rules: bool | None = None
    enforce_survivability_rules: bool | None = None
    randomize_rotation: bool | None = None
    may_attach_to: _MayAttachTo | None = None
    may_not_attach_to: _MayNotAttachTo | None = None
    may_replace: list[Annotated[str | Block | BlockDescriptor, BlockId]] | None = None

    def add_places_block(
        self, block: str | Block | BlockDescriptor, weight: float
    ) -> None:
        """Adds a block that can be placed, with its weight."""
        self.places_block.append(_WeightedBlock(block=block, weight=weight))

    def set_rules(
        self,
        enforce_placement_rules: bool,
        enforce_survivability_rules: bool,
        randomize_rotation: bool,
    ) -> None:
        """Sets the block's checks and whether it faces a random direction."""
        self.enforce_placement_rules = enforce_placement_rules
        self.enforce_survivability_rules = enforce_survivability_rules
        self.randomize_rotation = randomize_rotation

    def add_may_attach_to(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: Sequence[str | Block | BlockDescriptor],
        min_sides_must_attach: int | None,
        auto_rotate: bool | None,
    ) -> None:
        """Adds blocks the block may be placed next to on a face."""
        if self.may_attach_to is None:
            self.may_attach_to = _MayAttachTo()
        self.may_attach_to.add_face(face, blocks)
        self.may_attach_to.set_attach_rules(min_sides_must_attach, auto_rotate)

    def add_may_not_attach_to(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: Sequence[str | Block | BlockDescriptor],
    ) -> None:
        """Adds blocks the block may not be placed next to on a face."""
        if self.may_not_attach_to is None:
            self.may_not_attach_to = _MayNotAttachTo()
        self.may_not_attach_to.add_face(face, blocks)

    def set_may_replace(self, blocks: Sequence[str | Block | BlockDescriptor]) -> None:
        """Sets the blocks the block may replace."""
        self.may_replace = _blocks(blocks)

    def __validate__(self) -> None:
        if not self.places_block:
            raise ValueError("A single block feature needs a block to place.")


class _SingleBlockFeatureFile(JsonObject):
    """The content of a single block feature file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:single_block_feature",
    )

    format_version: str = json_field(default=FEATURE_VERSION, init=False)
    feature: _SingleBlockFeature = json_field(
        key="minecraft:single_block_feature", default_factory=_SingleBlockFeature
    )


class SingleBlockFeature(Feature):
    """Places one block, picked at random by weight from the blocks added.

    `may_attach_to` and `may_replace` are allowlists of where the block can be placed: any
    place when left out. `may_not_attach_to` is a denylist of blocks it cannot be next to.
    The block's own placement and survival rules are only checked when enforced, which gives
    natural results but can make failures harder to debug.

    - Succeeds if the block is placed.
    - Fails if it is not.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecraft_single_block_feature)
    """

    _document = _SingleBlockFeatureFile

    def __init__(
        self,
        name: str,
        enforce_placement_rules: bool = False,
        enforce_survivability_rules: bool = False,
        randomize_rotation: bool = False,
    ) -> None:
        """Creates a single block feature. Add the blocks it places next.

        Args:
            name (str): The name of the feature, also its file name.
            enforce_placement_rules (bool, optional): Check the block can be placed there.
                Defaults to False.
            enforce_survivability_rules (bool, optional): Check the block can survive
                there. Defaults to False.
            randomize_rotation (bool, optional): The block faces a random cardinal
                direction. Defaults to False.
        """
        super().__init__(name)
        self._feature.set_rules(
            enforce_placement_rules, enforce_survivability_rules, randomize_rotation
        )

    def place_block(
        self, block: str | Block | BlockDescriptor, weight: float = 1.0
    ) -> "SingleBlockFeature":
        """Adds a block that can be placed.

        Args:
            block (str | Block | BlockDescriptor): The block.
            weight (float, optional): Its weight, relative to the others. Defaults to 1.
        """
        self._feature.add_places_block(block, weight)
        return self

    def may_attach_to(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: Sequence[str | Block | BlockDescriptor],
        min_sides_must_attach: int | None = 1,
        auto_rotate: bool | None = False,
    ) -> "SingleBlockFeature":
        """Adds blocks the block may be placed next to on a face. Call it once per face.

        Args:
            face (BlockFaceValues | Literal["diagonal"]): The face: `Up` is the top face,
                `Down` the bottom one, `Side` every side face and `All` every face.
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
            min_sides_must_attach (int, optional): How many side faces must pass, from 1 to
                4. Defaults to 1; None leaves it as it is.
            auto_rotate (bool, optional): Rotate the block to attach sensibly, unless the
                rotation is random. Defaults to False; None leaves it as it is.
        """
        self._feature.add_may_attach_to(
            face, blocks, min_sides_must_attach, auto_rotate
        )
        return self

    def may_not_attach_to(
        self,
        face: BlockFaceValues | Literal["diagonal"],
        blocks: Sequence[str | Block | BlockDescriptor],
    ) -> "SingleBlockFeature":
        """Adds blocks the block may not be placed next to on a face. Call it once per
        face.

        Args:
            face (BlockFaceValues | Literal["diagonal"]): The face: `Up` is the top face,
                `Down` the bottom one, `Side` every side face and `All` every face.
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.add_may_not_attach_to(face, blocks)
        return self

    def may_replace(
        self, blocks: Sequence[str | Block | BlockDescriptor]
    ) -> "SingleBlockFeature":
        """Sets the blocks the block may replace.

        Args:
            blocks (Sequence[str | Block | BlockDescriptor]): The blocks.
        """
        self._feature.set_may_replace(blocks)
        return self
