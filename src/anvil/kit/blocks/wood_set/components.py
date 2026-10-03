"""The custom components the wood set blocks use, one per script in `typescript/`."""

from enum import StrEnum

from anvil.api.blocks.components import BlockCustomComponents
from anvil.api.core.core import CONFIG
from anvil.api.core.types import Vector3D

__all__ = [
    "SupportedBy",
    "BlockWoodSetSupport",
    "BlockWoodSetTogglable",
    "BlockWoodSetInteractable",
    "BlockWoodSetRedstoneConsumer",
    "BlockWoodSetStrippable",
    "BlockWoodSetSlab",
    "BlockWoodSetSign",
]


class _WoodSetComponent(BlockCustomComponents):
    _name: str

    @classmethod
    def __component_identifier__(cls) -> str:
        return f"{CONFIG.NAMESPACE}:wood_set_{cls._name}"

    def __init__(self) -> None:
        super().__init__(self.__component_identifier__())


class SupportedBy(StrEnum):
    """Where the block holding up a supported block is."""

    Below = "below"
    """The block below."""
    BlockFace = "block_face"
    """The block it was placed against, read from `minecraft:block_face`."""
    Facing = "facing"
    """The block its `minecraft:cardinal_direction` points at."""


class BlockWoodSetSupport(_WoodSetComponent):
    _name = "support"

    def __init__(self, supported_by: SupportedBy = SupportedBy.Below) -> None:
        """Breaks the block when the block holding it up is broken.

        Parameters:
            supported_by (SupportedBy): Where the block holding it up is.
        """
        super().__init__()
        self._add_field("supported_by", str(supported_by))


class BlockWoodSetTogglable(_WoodSetComponent):
    _name = "togglable"

    def __init__(self) -> None:
        """Turns `powered` on when interacted with or stepped on, and off on tick once clear."""
        super().__init__()


class BlockWoodSetInteractable(_WoodSetComponent):
    _name = "interactable"

    def __init__(self, multi_part: bool = False) -> None:
        """Opens and closes the block when interacted with.

        Parameters:
            multi_part (bool): Also opens and closes the other part of a two-block block.
        """
        super().__init__()
        self._add_field("multi_part", multi_part)


class BlockWoodSetRedstoneConsumer(_WoodSetComponent):
    _name = "redstone_consumer"

    def __init__(self, multi_part: bool = False) -> None:
        """Opens the block while it is powered.

        Parameters:
            multi_part (bool): Also opens and closes the other part of a two-block block.
        """
        super().__init__()
        self._add_field("multi_part", multi_part)


class BlockWoodSetStrippable(_WoodSetComponent):
    _name = "strippable"

    def __init__(self, stripped_block: str) -> None:
        """Turns into `stripped_block` when used with an axe, keeping its states.

        Parameters:
            stripped_block (str): The identifier of the stripped block.
        """
        super().__init__()
        self._add_field("stripped_block", stripped_block)


class BlockWoodSetSlab(_WoodSetComponent):
    _name = "slab"

    def __init__(self) -> None:
        """Turns into a double slab when another slab is placed on it."""
        super().__init__()


class BlockWoodSetSign(_WoodSetComponent):
    _name = "sign"

    def __init__(
        self,
        text_offset: Vector3D = (0, 0, 0),
        text_scale: float = 0.46,
        line_length: int = 15,
        double_sided: bool = False,
        wall_sign: str | None = None,
    ) -> None:
        """Asks for the text when placed or interacted with, and shows it on the sign.

        Parameters:
            text_offset (Vector3D): Where the text sits in the block, in 1/16 block units
                (0-16 on each axis), measured with the sign at rotation 0 from the block's
                north-west bottom corner (x east, y up, z south). It turns with the sign.
            text_scale (float): The size of the text; its outline grows with it.
            line_length (int): The most visible characters on a line.
            double_sided (bool): Also shows the text on the back, turned around the block's
                centre.
            wall_sign (str, optional): The wall sign placed instead when the sign is put on
                the side of a block.
        """
        super().__init__()
        values = list(text_offset)
        if len(values) != 3 or any(not 0 <= value <= 16 for value in values):
            raise ValueError(
                f"text_offset must be three values from 0 to 16, got {text_offset}."
            )
        if text_scale <= 0:
            raise ValueError(f"text_scale must be above 0, got {text_scale}.")
        if line_length < 1:
            raise ValueError(f"line_length must be at least 1, got {line_length}.")
        self._add_field_if_not_default("text_offset", values, [0, 0, 0])
        self._add_field("text_scale", text_scale)
        self._add_field_if_not_default("line_length", line_length, 15)
        self._add_field_if_not_default("double_sided", double_sided, False)
        if wall_sign:
            self._add_field("wall_sign", wall_sign)
