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

class CalciteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CalcitePillarStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class CalciteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CalciteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CalciteWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class DiscPressStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class IceCrystalStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class IcicleStates(TypedDict, total=False):
    attached_bit: bool | None
    dripstone_thickness: Literal["tip", "frustum", "middle", "base", "merge"] | None
    hanging: bool | None

class PackedIceBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PackedIceBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PackedIceBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PackedIceBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedCalciteBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedCalciteBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedCalciteBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedCalciteBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedCalciteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedCalciteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedCalciteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedCalciteWallStates(TypedDict, total=False):
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

class SnowBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SnowBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SnowBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SnowBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class UnpoweredRepeaterStates(TypedDict, total=False):
    """Beta introduced the locked state key for unpowered repeaters."""

    locked: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    repeater_delay: Literal[0, 1, 2, 3] | None

def BrittleIce(**states: Unpack[BrittleIceStates]) -> Identifier | BlockDescriptor: ...
def CalciteDoubleSlab(
    **states: Unpack[CalciteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CalcitePillar(
    **states: Unpack[CalcitePillarStates],
) -> Identifier | BlockDescriptor: ...
def CalciteSlab(
    **states: Unpack[CalciteSlabStates],
) -> Identifier | BlockDescriptor: ...
def CalciteStairs(
    **states: Unpack[CalciteStairsStates],
) -> Identifier | BlockDescriptor: ...
def CalciteWall(
    **states: Unpack[CalciteWallStates],
) -> Identifier | BlockDescriptor: ...
def ChiseledPackedIce() -> Identifier: ...
def ChiseledSoulshale() -> Identifier: ...
def IceCrystal(**states: Unpack[IceCrystalStates]) -> Identifier | BlockDescriptor: ...
def Icicle(**states: Unpack[IcicleStates]) -> Identifier | BlockDescriptor: ...
def PackedIceBrickDoubleSlab(
    **states: Unpack[PackedIceBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBrickSlab(
    **states: Unpack[PackedIceBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBrickStairs(
    **states: Unpack[PackedIceBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBrickWall(
    **states: Unpack[PackedIceBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def PackedIceBricks() -> Identifier: ...
def PolishedCalcite() -> Identifier: ...
def PolishedCalciteBrickDoubleSlab(
    **states: Unpack[PolishedCalciteBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteBrickSlab(
    **states: Unpack[PolishedCalciteBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteBrickStairs(
    **states: Unpack[PolishedCalciteBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteBrickWall(
    **states: Unpack[PolishedCalciteBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteBricks() -> Identifier: ...
def PolishedCalciteDoubleSlab(
    **states: Unpack[PolishedCalciteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteSlab(
    **states: Unpack[PolishedCalciteSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteStairs(
    **states: Unpack[PolishedCalciteStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCalciteWall(
    **states: Unpack[PolishedCalciteWallStates],
) -> Identifier | BlockDescriptor: ...
def PoweredRepeater(
    **states: Unpack[PoweredRepeaterStates],
) -> Identifier | BlockDescriptor: ...
def Scaffolding(
    **states: Unpack[ScaffoldingStates],
) -> Identifier | BlockDescriptor: ...
def SnowBrickDoubleSlab(
    **states: Unpack[SnowBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SnowBrickSlab(
    **states: Unpack[SnowBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def SnowBrickStairs(
    **states: Unpack[SnowBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def SnowBrickWall(
    **states: Unpack[SnowBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def SnowBricks() -> Identifier: ...
def UnpoweredRepeater(
    **states: Unpack[UnpoweredRepeaterStates],
) -> Identifier | BlockDescriptor: ...
