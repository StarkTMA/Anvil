from typing import Literal, TypedDict, Unpack

from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.jsonmodel import Identifier

class DiscPressStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class IceCrystalStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class IcicleStates(TypedDict, total=False):
    attached_bit: bool | None
    dripstone_thickness: Literal["tip", "frustum", "middle", "base", "merge"] | None
    hanging: bool | None

def DiscPress(**states: Unpack[DiscPressStates]) -> Identifier | BlockDescriptor: ...
def IceCrystal(**states: Unpack[IceCrystalStates]) -> Identifier | BlockDescriptor: ...
def Icicle(**states: Unpack[IcicleStates]) -> Identifier | BlockDescriptor: ...
