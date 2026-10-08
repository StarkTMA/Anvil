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
    "BlockWoodSetLeaves",
    "BlockWoodSetSapling",
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
    Sign = "sign"
    """The block below when its `standing` state is on, otherwise the block its
    `minecraft:cardinal_direction` points at."""


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
        wall_text_offset: Vector3D | None = None,
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
            wall_text_offset (Vector3D, optional): Makes the sign two shapes in one block,
                told apart by its `standing` state: standing (on top of a block, turning in
                16 steps) and on a wall (on the side of a block, with its cardinal direction
                pointing at the wall). `text_offset` is where the text sits when standing and
                this is where it sits on the wall, measured like `text_offset` with the sign
                pointing north. A sign placed on the side of a block turns its `standing`
                state off.
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
        if wall_text_offset is not None:
            wall_values = list(wall_text_offset)
            if len(wall_values) != 3 or any(
                not 0 <= value <= 16 for value in wall_values
            ):
                raise ValueError(
                    f"wall_text_offset must be three values from 0 to 16, got {wall_text_offset}."
                )
            self._add_field("wall_text_offset", wall_values)


class BlockWoodSetLeaves(_WoodSetComponent):
    _name = "leaves"

    def __init__(
        self,
        trunks: list[str],
        sapling: str | None = None,
        distance: int = 4,
        sapling_chance: float = 0.05,
        stick_chance: float = 0.02,
    ) -> None:
        """Decays the leaves that don't hold on to a trunk, and drops what leaves drop.

        Only leaves whose `natural` state is on decay: those a player placed stay. On a
        random tick they look for one of `trunks` within `distance` blocks, going through
        leaves of the same kind, and break when there is none.

        Breaking them with shears or a silk touch tool drops the leaves; any other way (or
        decaying) drops a sapling or sticks by chance. Nothing drops in creative mode or from
        explosions.

        Parameters:
            trunks (list[str]): The identifiers of the blocks that hold the leaves up.
            sapling (str, optional): The identifier of the sapling they drop.
            distance (int): The most blocks away a trunk can be.
            sapling_chance (float): The chance of a sapling when broken or decayed.
            stick_chance (float): The chance of sticks when broken or decayed.
        """
        super().__init__()
        if distance < 1:
            raise ValueError(f"distance must be at least 1, got {distance}.")
        for name, chance in (
            ("sapling_chance", sapling_chance),
            ("stick_chance", stick_chance),
        ):
            if not 0 <= chance <= 1:
                raise ValueError(f"{name} must be from 0 to 1, got {chance}.")
        self._add_field("trunks", list(trunks))
        if sapling is not None:
            self._add_field("sapling", sapling)
        self._add_field_if_not_default("distance", distance, 4)
        self._add_field_if_not_default("sapling_chance", sapling_chance, 0.05)
        self._add_field_if_not_default("stick_chance", stick_chance, 0.02)


class BlockWoodSetSapling(_WoodSetComponent):
    _name = "sapling"

    def __init__(self, tree_feature: str) -> None:
        """Grows into a tree on random ticks, or faster with bone meal.

        As in vanilla, it has two stages. A random tick (1 in 7, only with light 9 or more
        above it) or a bone meal (45% in survival, any light) advances it one stage, and
        advancing the second stage turns it into the tree. It stays a sapling if the tree
        doesn't fit. A bone meal in creative grows the tree at once.

        Parameters:
            tree_feature (str): The identifier of the feature `/place feature` builds the
                tree with, at the sapling's position.
        """
        super().__init__()
        self._add_field("tree_feature", tree_feature)
