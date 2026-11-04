"""The custom components the wood set blocks use, one per script in `typescript/`."""

from typing import Annotated

from anvil.api.blocks.components import BlockCustomComponent
from anvil.lib.jsonmodel import AtLeastOne, Chance, InRange, Positive, json_field
from anvil.lib.jsonmodel.enums import SupportedBy

__all__ = [
    "BlockWoodSetSupport",
    "BlockWoodSetTogglable",
    "BlockWoodSetInteractable",
    "BlockWoodSetDoor",
    "BlockWoodSetRedstoneConsumer",
    "BlockWoodSetStrippable",
    "BlockWoodSetSlab",
    "BlockWoodSetSign",
    "BlockWoodSetLeaves",
    "BlockWoodSetSapling",
]


class _WoodSetComponent(BlockCustomComponent, abstract=True):
    """Base of the wood set components, named `<namespace>:wood_set_<name>`."""


class BlockWoodSetSupport(_WoodSetComponent):
    """Breaks the block when the block holding it up is broken.

    Args:
        supported_by (SupportedBy): Where the block holding it up is. Defaults to below.
    """

    identifier = "wood_set_support"

    supported_by: SupportedBy = json_field(default=SupportedBy.Below)


class BlockWoodSetTogglable(_WoodSetComponent):
    """Turns `powered` on when stepped on (and when interacted with, unless `on_interact` is
    off), and off on tick once clear.

    Args:
        on_interact (bool): Whether a player interacting with it turns it on, like a
            button. Off for a pressure plate, which only reacts to being stepped on.
        on_sound (str, optional): The id of the sound played when it turns on.
        off_sound (str, optional): The id of the sound played when it turns off.
    """

    identifier = "wood_set_togglable"

    on_interact: bool = json_field(default=True)
    on_sound: str | None = json_field(default=None)
    off_sound: str | None = json_field(default=None)


class BlockWoodSetInteractable(_WoodSetComponent):
    """Opens and closes the block when interacted with.

    Args:
        multi_part (bool): Also opens and closes the other part of a two-block block.
        open_sound (str, optional): The id of the sound played when it opens.
        close_sound (str, optional): The id of the sound played when it closes.
    """

    identifier = "wood_set_interactable"

    multi_part: bool = json_field(default=False)
    open_sound: str | None = json_field(default=None)
    close_sound: str | None = json_field(default=None)


class BlockWoodSetDoor(_WoodSetComponent):
    """Hinges the door on the right as it is placed next to a door on its left, so the two
    make a double door, as in vanilla. Needs the `hinge_right` state."""

    identifier = "wood_set_door"


class BlockWoodSetRedstoneConsumer(_WoodSetComponent):
    """Opens the block when it gets power and closes it when the power goes, like vanilla.

    It only acts when the power changes, tracked in a `powered` state the block must
    have, so a block a player opened stays open when the world reloads.

    Args:
        multi_part (bool): Also opens and closes the other part of a two-block block,
            and counts as powered while either part is.
        open_sound (str, optional): The id of the sound played when it opens.
        close_sound (str, optional): The id of the sound played when it closes.
    """

    identifier = "wood_set_redstone_consumer"

    multi_part: bool = json_field(default=False)
    open_sound: str | None = json_field(default=None)
    close_sound: str | None = json_field(default=None)


class BlockWoodSetStrippable(_WoodSetComponent):
    """Turns into `stripped_block` when used with an axe, keeping its states.

    Args:
        stripped_block (str): The identifier of the stripped block.
    """

    identifier = "wood_set_strippable"

    stripped_block: str = json_field()


class BlockWoodSetSlab(_WoodSetComponent):
    """Turns into a double slab when another slab is placed on it."""

    identifier = "wood_set_slab"


class BlockWoodSetSign(_WoodSetComponent):
    """Asks for the text when placed or interacted with, and shows it on the sign.

    Args:
        text_offset (tuple[float, float, float]): Where the text sits in the block, in 1/16 block units
            (0-16 on each axis), measured with the sign at rotation 0 from the block's
            north-west bottom corner (x east, y up, z south). It turns with the sign.
        text_scale (float): The size of the text; its outline grows with it.
        line_length (int): The most visible characters on a line.
        double_sided (bool): Also shows the text on the back, turned around the block's
            centre.
        wall_text_offset (tuple[float, float, float], optional): Makes the sign two shapes in one block,
            told apart by its `standing` state: standing (on top of a block, turning in
            16 steps) and on a wall (on the side of a block, with its cardinal direction
            pointing at the wall). `text_offset` is where the text sits when standing and
            this is where it sits on the wall, measured like `text_offset` with the sign
            pointing north. A sign placed on the side of a block turns its `standing`
            state off.
    """

    identifier = "wood_set_sign"

    text_offset: Annotated[tuple[float, float, float], InRange(0, 16)] = json_field(
        default=(0, 0, 0), omit_default=True
    )
    text_scale: Annotated[float, Positive] = json_field(default=0.46)
    line_length: Annotated[int, AtLeastOne] = json_field(default=15, omit_default=True)
    double_sided: bool = json_field(default=False, omit_default=True)
    wall_text_offset: Annotated[tuple[float, float, float], InRange(0, 16)] | None = (
        json_field(default=None)
    )


class BlockWoodSetLeaves(_WoodSetComponent):
    """Decays the leaves that don't hold on to a trunk, and drops what leaves drop.

    Only leaves whose `natural` state is on decay: those a player placed stay. On a
    random tick they look for one of `trunks` within `distance` blocks, going through
    leaves of the same kind, and break when there is none.

    Breaking them with shears or a silk touch tool drops the leaves; any other way (or
    decaying) drops a sapling or sticks by chance. Nothing drops in creative mode or from
    explosions.

    Args:
        trunks (list[str]): The identifiers of the blocks that hold the leaves up.
        sapling (str, optional): The identifier of the sapling they drop.
        distance (int): The most blocks away a trunk can be.
        sapling_chance (float): The chance of a sapling when broken or decayed.
        stick_chance (float): The chance of sticks when broken or decayed.
    """

    identifier = "wood_set_leaves"

    trunks: list[str] = json_field()
    sapling: str | None = json_field(default=None)
    distance: Annotated[int, AtLeastOne] = json_field(default=4, omit_default=True)
    sapling_chance: Annotated[float, Chance] = json_field(
        default=0.05, omit_default=True
    )
    stick_chance: Annotated[float, Chance] = json_field(default=0.02, omit_default=True)


class BlockWoodSetSapling(_WoodSetComponent):
    """Grows into a tree on random ticks, or faster with bone meal.

    As in vanilla, it has two stages. A random tick (1 in 7, only with light 9 or more
    above it) or a bone meal (45% in survival, any light) advances it one stage, and
    advancing the second stage turns it into the tree. It stays a sapling if the tree
    doesn't fit. A bone meal in creative grows the tree at once.

    Args:
        tree_feature (str): The identifier of the feature `/place feature` builds the
            tree with, at the sapling's position.
    """

    identifier = "wood_set_sapling"

    tree_feature: str = json_field()
