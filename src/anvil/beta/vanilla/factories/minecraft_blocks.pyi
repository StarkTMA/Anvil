from enum import StrEnum
from typing import Literal, TypedDict, Unpack

from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.jsonmodel import Identifier

class BlockStateKeys(StrEnum):
    """Newly introduced state keys in the beta vanilla blocks."""

    Bottom = "bottom"
    Locked = "locked"

class BrittleIceStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class DiscPressStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class IceCrystalStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class IcicleStates(TypedDict, total=False):
    attached_bit: bool | None
    dripstone_thickness: Literal["tip", "frustum", "middle", "base", "merge"] | None
    hanging: bool | None

class PackedIceBricksDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PackedIceBricksSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PackedIceBricksStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PackedIceBricksWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PoweredRepeaterStates(TypedDict, total=False):
    """Beta introduced the locked state key for powered repeaters."""

    locked: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    repeater_delay: Literal[0, 1, 2, 3] | None

class ScaffoldingStates(TypedDict, total=False):
    """Beta introduced the bottom and stability state keys for scaffolding."""

    bottom: bool | None
    stability: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    stability_check: bool | None

class UnpoweredRepeaterStates(TypedDict, total=False):
    """Beta introduced the locked state key for unpowered repeaters."""

    locked: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    repeater_delay: Literal[0, 1, 2, 3] | None

def BrittleIce(**states: Unpack[BrittleIceStates]) -> Identifier | BlockDescriptor: ...
def IceCrystal(**states: Unpack[IceCrystalStates]) -> Identifier | BlockDescriptor: ...
def Icicle(**states: Unpack[IcicleStates]) -> Identifier | BlockDescriptor: ...
def PackedIceBricks() -> Identifier: ...
def PackedIceBricksChiseled() -> Identifier: ...
def PackedIceBricksDoubleSlab(
    **states: Unpack[PackedIceBricksDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBricksSlab(
    **states: Unpack[PackedIceBricksSlabStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBricksStairs(
    **states: Unpack[PackedIceBricksStairsStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBricksWall(
    **states: Unpack[PackedIceBricksWallStates],
) -> Identifier | BlockDescriptor: ...
def PoweredRepeater(
    **states: Unpack[PoweredRepeaterStates],
) -> Identifier | BlockDescriptor: ...
def Scaffolding(
    **states: Unpack[ScaffoldingStates],
) -> Identifier | BlockDescriptor: ...
def UnpoweredRepeater(
    **states: Unpack[UnpoweredRepeaterStates],
) -> Identifier | BlockDescriptor: ...
