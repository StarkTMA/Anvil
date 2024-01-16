from enum import Enum

from anvil import ANVIL, CONFIG
from anvil.api.enums import Dimension

ENTITY_LIST = []
ITEMS_LIST = []

# Updated on 05-04-2023
# Latest Updated release: 1.19.81.01
class BlockStates:
    class ButtonPressedBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class FacingDirection(Enum):
        ENUM5 = "5"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"

    class Direction(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class DoorHingeBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class OpenBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class UpperBlockBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class InWallBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class AttachedBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class GroundSignDirection(Enum):
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM5 = "5"
        ENUM7 = "7"
        ENUM13 = "13"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM11 = "11"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM14 = "14"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM8 = "8"
        ENUM15 = "15"

    class Hanging(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class PillarAxis(Enum):
        Z = "z"
        X = "x"
        Y = "y"

    class RedstoneSignal(Enum):
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM5 = "5"
        ENUM13 = "13"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM14 = "14"
        ENUM1 = "1"
        ENUM15 = "15"
        ENUM8 = "8"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"
        ENUM11 = "11"

    class UpsideDownBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class WeirdoDirection(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class RailDataBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class RailDirection(Enum):
        ENUM5 = "5"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM1 = "1"
        ENUM8 = "8"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"

    class Damage(Enum):
        UNDAMAGED = "undamaged"
        SLIGHTLY_DAMAGED = "slightly_damaged"
        VERY_DAMAGED = "very_damaged"
        BROKEN = "broken"

    class PersistentBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class UpdateBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class AgeBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class BambooLeafSize(Enum):
        NO_LEAVES = "no_leaves"
        SMALL_LEAVES = "small_leaves"
        LARGE_LEAVES = "large_leaves"

    class BambooStalkThickness(Enum):
        THIN = "thin"
        THICK = "thick"

    class TopSlotBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class SaplingType(Enum):
        DARK_OAK = "dark_oak"
        ACACIA = "acacia"
        SPRUCE = "spruce"
        BIRCH = "birch"
        JUNGLE = "jungle"
        OAK = "oak"

    class HeadPieceBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class OccupiedBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class InfiniburnBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class HoneyLevel(Enum):
        ENUM5 = "5"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"

    class Growth(Enum):
        ENUM5 = "5"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"

    class Attachment(Enum):
        STANDING = "standing"
        SIDE = "side"
        MULTIPLE = "multiple"
        HANGING = "hanging"

    class ToggleBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class BigDripleafHead(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class BigDripleafTilt(Enum):
        NONE = "none"
        UNSTABLE = "unstable"
        PARTIAL_TILT = "partial_tilt"
        FULL_TILT = "full_tilt"

    class WallConnectionTypeEast(Enum):
        TALL = "tall"
        NONE = "none"
        SHORT = "short"

    class WallConnectionTypeNorth(Enum):
        TALL = "tall"
        NONE = "none"
        SHORT = "short"

    class WallConnectionTypeSouth(Enum):
        TALL = "tall"
        NONE = "none"
        SHORT = "short"

    class WallConnectionTypeWest(Enum):
        TALL = "tall"
        NONE = "none"
        SHORT = "short"

    class WallPostBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class Candles(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class Lit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class Deprecated(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class BrewingStandSlotABit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class BrewingStandSlotBBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class BrewingStandSlotCBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class HugeMushroomBits(Enum):
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM5 = "5"
        ENUM13 = "13"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM14 = "14"
        ENUM1 = "1"
        ENUM15 = "15"
        ENUM8 = "8"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"
        ENUM11 = "11"

    class DragDown(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class Age(Enum):
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM5 = "5"
        ENUM13 = "13"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM14 = "14"
        ENUM1 = "1"
        ENUM15 = "15"
        ENUM8 = "8"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"
        ENUM11 = "11"

    class BiteCounter(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"

    class SculkSensorPhase(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"

    class Extinguished(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class CardinalDirection(Enum):
        SOUTH = "south"
        WEST = "west"
        NORTH = "north"
        EAST = "east"

    class CauldronLiquid(Enum):
        WATER = "water"
        LAVA = "lava"
        POWDER_SNOW = "powder_snow"

    class FillLevel(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"

    class GrowingPlantAge(Enum):
        ENUM22 = "22"
        ENUM0 = "0"
        ENUM23 = "23"
        ENUM15 = "15"
        ENUM17 = "17"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM16 = "16"
        ENUM19 = "19"
        ENUM8 = "8"
        ENUM11 = "11"
        ENUM5 = "5"
        ENUM24 = "24"
        ENUM13 = "13"
        ENUM18 = "18"
        ENUM6 = "6"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"
        ENUM20 = "20"
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM21 = "21"
        ENUM25 = "25"
        ENUM14 = "14"
        ENUM1 = "1"

    class ConditionalBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class ChemistryTableType(Enum):
        COMPOUND_CREATOR = "compound_creator"
        MATERIAL_REDUCER = "material_reducer"
        ELEMENT_CONSTRUCTOR = "element_constructor"
        LAB_TABLE = "lab_table"

    class StrippedBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class BooksStored(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"
        ENUM9 = "9"
        ENUM10 = "10"
        ENUM11 = "11"
        ENUM12 = "12"
        ENUM13 = "13"
        ENUM14 = "14"
        ENUM15 = "15"
        ENUM16 = "16"
        ENUM17 = "17"
        ENUM18 = "18"
        ENUM19 = "19"
        ENUM20 = "20"
        ENUM21 = "21"
        ENUM22 = "22"
        ENUM23 = "23"
        ENUM24 = "24"
        ENUM25 = "25"
        ENUM26 = "26"
        ENUM27 = "27"
        ENUM28 = "28"
        ENUM29 = "29"
        ENUM30 = "30"
        ENUM31 = "31"
        ENUM32 = "32"
        ENUM33 = "33"
        ENUM34 = "34"
        ENUM35 = "35"
        ENUM36 = "36"
        ENUM37 = "37"
        ENUM38 = "38"
        ENUM39 = "39"
        ENUM40 = "40"
        ENUM41 = "41"
        ENUM42 = "42"
        ENUM43 = "43"
        ENUM44 = "44"
        ENUM45 = "45"
        ENUM46 = "46"
        ENUM47 = "47"
        ENUM48 = "48"
        ENUM49 = "49"
        ENUM50 = "50"
        ENUM51 = "51"
        ENUM52 = "52"
        ENUM53 = "53"
        ENUM54 = "54"
        ENUM55 = "55"
        ENUM56 = "56"
        ENUM57 = "57"
        ENUM58 = "58"
        ENUM59 = "59"
        ENUM60 = "60"
        ENUM61 = "61"
        ENUM62 = "62"
        ENUM63 = "63"

    class WallBlockType(Enum):
        COBBLESTONE = "cobblestone"
        MOSSY_COBBLESTONE = "mossy_cobblestone"
        GRANITE = "granite"
        DIORITE = "diorite"
        ANDESITE = "andesite"
        SANDSTONE = "sandstone"
        BRICK = "brick"
        STONE_BRICK = "stone_brick"
        MOSSY_STONE_BRICK = "mossy_stone_brick"
        NETHER_BRICK = "nether_brick"
        END_BRICK = "end_brick"
        PRISMARINE = "prismarine"
        RED_SANDSTONE = "red_sandstone"
        RED_NETHER_BRICK = "red_nether_brick"

    class ColorBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class TorchFacingDirection(Enum):
        UNKNOWN = "unknown"
        WEST = "west"
        SOUTH = "south"
        NORTH = "north"
        EAST = "east"
        TOP = "top"

    class ComposterFillLevel(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"

    class Color(Enum):
        BLACK = "black"
        SILVER = "silver"
        RED = "red"
        ORANGE = "orange"
        LIME = "lime"
        PINK = "pink"
        PURPLE = "purple"
        MAGENTA = "magenta"
        LIGHT_BLUE = "light_blue"
        YELLOW = "yellow"
        GRAY = "gray"
        CYAN = "cyan"
        WHITE = "white"
        BLUE = "blue"
        GREEN = "green"
        BROWN = "brown"

    class CoralColor(Enum):
        RED = "red"
        PINK = "pink"
        PURPLE = "purple"
        YELLOW = "yellow"
        BLUE = "blue"

    class DeadBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class CoralFanDirection(Enum):
        ENUM0 = "0"
        ENUM1 = "1"

    class CoralDirection(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class CoralHangTypeBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class DirtType(Enum):
        NORMAL = "normal"
        COARSE = "coarse"

    class TriggeredBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class DoublePlantType(Enum):
        SUNFLOWER = "sunflower"
        SYRINGA = "syringa"
        GRASS = "grass"
        FERN = "fern"
        ROSE = "rose"
        PAEONIA = "paeonia"

    class StoneSlabType(Enum):
        BRICK = "brick"
        SANDSTONE = "sandstone"
        WOOD = "wood"
        STONE_BRICK = "stone_brick"
        SMOOTH_STONE = "smooth_stone"
        COBBLESTONE = "cobblestone"
        NETHER_BRICK = "nether_brick"
        QUARTZ = "quartz"

    class StoneSlabType2(Enum):
        RED_SANDSTONE = "red_sandstone"
        PRISMARINE_ROUGH = "prismarine_rough"
        PURPUR = "purpur"
        PRISMARINE_BRICK = "prismarine_brick"
        SMOOTH_SANDSTONE = "smooth_sandstone"
        PRISMARINE_DARK = "prismarine_dark"
        MOSSY_COBBLESTONE = "mossy_cobblestone"
        RED_NETHER_BRICK = "red_nether_brick"

    class StoneSlabType3(Enum):
        END_STONE_BRICK = "end_stone_brick"
        DIORITE = "diorite"
        GRANITE = "granite"
        POLISHED_ANDESITE = "polished_andesite"
        ANDESITE = "andesite"
        POLISHED_GRANITE = "polished_granite"
        SMOOTH_RED_SANDSTONE = "smooth_red_sandstone"
        POLISHED_DIORITE = "polished_diorite"

    class StoneSlabType4(Enum):
        STONE = "stone"
        CUT_SANDSTONE = "cut_sandstone"
        CUT_RED_SANDSTONE = "cut_red_sandstone"
        SMOOTH_QUARTZ = "smooth_quartz"
        MOSSY_STONE_BRICK = "mossy_stone_brick"

    class WoodType(Enum):
        DARK_OAK = "dark_oak"
        ACACIA = "acacia"
        SPRUCE = "spruce"
        BIRCH = "birch"
        JUNGLE = "jungle"
        OAK = "oak"

    class EndPortalEyeBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class MoisturizedAmount(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"

    class LiquidDepth(Enum):
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM5 = "5"
        ENUM13 = "13"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM0 = "0"
        ENUM6 = "6"
        ENUM14 = "14"
        ENUM1 = "1"
        ENUM15 = "15"
        ENUM8 = "8"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM7 = "7"
        ENUM11 = "11"

    class ItemFrameMapBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class ItemFramePhotoBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class MultiFaceDirectionBits(Enum):
        ENUM35 = "35"
        ENUM22 = "22"
        ENUM62 = "62"
        ENUM45 = "45"
        ENUM0 = "0"
        ENUM36 = "36"
        ENUM53 = "53"
        ENUM30 = "30"
        ENUM59 = "59"
        ENUM47 = "47"
        ENUM23 = "23"
        ENUM15 = "15"
        ENUM50 = "50"
        ENUM17 = "17"
        ENUM9 = "9"
        ENUM4 = "4"
        ENUM16 = "16"
        ENUM27 = "27"
        ENUM60 = "60"
        ENUM32 = "32"
        ENUM33 = "33"
        ENUM19 = "19"
        ENUM8 = "8"
        ENUM26 = "26"
        ENUM31 = "31"
        ENUM11 = "11"
        ENUM38 = "38"
        ENUM46 = "46"
        ENUM58 = "58"
        ENUM5 = "5"
        ENUM24 = "24"
        ENUM13 = "13"
        ENUM18 = "18"
        ENUM40 = "40"
        ENUM54 = "54"
        ENUM63 = "63"
        ENUM42 = "42"
        ENUM6 = "6"
        ENUM29 = "29"
        ENUM43 = "43"
        ENUM52 = "52"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM41 = "41"
        ENUM44 = "44"
        ENUM7 = "7"
        ENUM20 = "20"
        ENUM51 = "51"
        ENUM12 = "12"
        ENUM10 = "10"
        ENUM21 = "21"
        ENUM61 = "61"
        ENUM56 = "56"
        ENUM25 = "25"
        ENUM57 = "57"
        ENUM55 = "55"
        ENUM34 = "34"
        ENUM14 = "14"
        ENUM1 = "1"
        ENUM39 = "39"
        ENUM28 = "28"
        ENUM49 = "49"
        ENUM37 = "37"
        ENUM48 = "48"

    class Rotation(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"

    class KelpAge(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"
        ENUM9 = "9"
        ENUM10 = "10"
        ENUM11 = "11"
        ENUM12 = "12"
        ENUM13 = "13"
        ENUM14 = "14"
        ENUM15 = "15"
        ENUM16 = "16"
        ENUM17 = "17"
        ENUM18 = "18"
        ENUM19 = "19"
        ENUM20 = "20"
        ENUM21 = "21"
        ENUM22 = "22"
        ENUM23 = "23"
        ENUM24 = "24"
        ENUM25 = "25"

    class OldLeafType(Enum):
        OAK = "oak"
        SPRUCE = "spruce"
        BIRCH = "birch"
        JUNGLE = "jungle"

    class NewLeafType(Enum):
        ACACIA = "acacia"
        DARK_OAK = "dark_oak"

    class PoweredBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class LeverDirection(Enum):
        DOWN_EAST_WEST = "down_east_west"
        EAST = "east"
        WEST = "west"
        SOUTH = "south"
        NORTH = "north"
        UP_NORTH_SOUTH = "up_north_south"
        UP_EAST_WEST = "up_east_west"
        DOWN_NORTH_SOUTH = "down_north_south"

    class BlockLightLevel(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"
        ENUM9 = "9"
        ENUM10 = "10"
        ENUM11 = "11"
        ENUM12 = "12"
        ENUM13 = "13"
        ENUM14 = "14"
        ENUM15 = "15"

    class PropaguleStage(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"

    class MonsterEggStoneType(Enum):
        STONE = "stone"
        COBBLESTONE = "cobblestone"
        STONE_BRICK = "stone_brick"
        MOSSY_STONE_BRICK = "mossy_stone_brick"
        CRACKED_STONE_BRICK = "cracked_stone_brick"
        CHISELED_STONE_BRICK = "chiseled_stone_brick"

    class DripstoneThickness(Enum):
        TIP = "tip"
        FRUSTUM = "frustum"
        MIDDLE = "middle"
        BASE = "base"
        MERGE = "merge"

    class PortalAxis(Enum):
        UNKNOWN = "unknown"
        X = "x"
        Z = "z"

    class OutputLitBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class OutputSubtractBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class RepeaterDelay(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class PrismarineBlockType(Enum):
        DEFAULT = "default"
        DARK = "dark"
        BRICKS = "bricks"

    class ChiselType(Enum):
        CHISELED = "chiseled"
        DEFAULT = "default"
        SMOOTH = "smooth"
        LINES = "lines"

    class FlowerType(Enum):
        POPPY = "poppy"
        ORCHID = "orchid"
        ALLIUM = "allium"
        HOUSTONIA = "houstonia"
        TULIP_RED = "tulip_red"
        TULIP_ORANGE = "tulip_orange"
        TULIP_WHITE = "tulip_white"
        TULIP_PINK = "tulip_pink"
        OXEYE = "oxeye"
        CORNFLOWER = "cornflower"
        LILY_OF_THE_VALLEY = "lily_of_the_valley"

    class SandStoneType(Enum):
        HEIROGLYPHS = "heiroglyphs"
        DEFAULT = "default"
        CUT = "cut"
        SMOOTH = "smooth"

    class RespawnAnchorCharge(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"

    class SandType(Enum):
        NORMAL = "normal"
        RED = "red"

    class Stability(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"

    class StabilityCheck(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class Bloom(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class Active(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class CanSummon(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class SeaGrassType(Enum):
        DEFAULT = "default"
        DOUBLE_TOP = "double_top"
        DOUBLE_BOT = "double_bot"

    class ClusterCount(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"

    class CrackedState(Enum):
        MAX_CRACKED = "max_cracked"
        CRACKED = "cracked"
        NO_CRACKS = "no_cracks"

    class CoveredBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class Height(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"

    class SpongeType(Enum):
        DRY = "dry"
        WET = "wet"

    class StoneType(Enum):
        STONE = "stone"
        GRANITE = "granite"
        GRANITE_SMOOTH = "granite_smooth"
        DIORITE = "diorite"
        DIORITE_SMOOTH = "diorite_smooth"
        ANDESITE = "andesite"
        ANDESITE_SMOOTH = "andesite_smooth"

    class StoneBrickType(Enum):
        DEFAULT = "default"
        MOSSY = "mossy"
        CRACKED = "cracked"
        CHISELED = "chiseled"
        SMOOTH = "smooth"

    class StructureBlockType(Enum):
        DATA = "data"
        SAVE = "save"
        LOAD = "load"
        CORNER = "corner"
        INVALID = "invalid"
        EXPORT = "export"

    class StructureVoidType(Enum):
        VOID = "void"
        AIR = "air"

    class BrushedProgress(Enum):
        ENUM0 = "0"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM3 = "3"

    class TallGrassType(Enum):
        DEFAULT = "default"
        TALL = "tall"
        FERN = "fern"
        SNOW = "snow"

    class AllowUnderwaterBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class ExplodeBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class DisarmedBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class SuspendedBit(Enum):
        ENUM0B = "0b"
        ENUM1B = "1b"

    class TurtleEggCount(Enum):
        ONE_EGG = "one_egg"
        TWO_EGG = "two_egg"
        THREE_EGG = "three_egg"
        FOUR_EGG = "four_egg"

    class TwistingVinesAge(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"
        ENUM9 = "9"
        ENUM10 = "10"
        ENUM11 = "11"
        ENUM12 = "12"
        ENUM13 = "13"
        ENUM14 = "14"
        ENUM15 = "15"
        ENUM16 = "16"
        ENUM17 = "17"
        ENUM18 = "18"
        ENUM19 = "19"
        ENUM20 = "20"
        ENUM21 = "21"
        ENUM22 = "22"
        ENUM23 = "23"
        ENUM24 = "24"
        ENUM25 = "25"

    class VineDirectionBits(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"
        ENUM9 = "9"
        ENUM10 = "10"
        ENUM11 = "11"
        ENUM12 = "12"
        ENUM13 = "13"
        ENUM14 = "14"
        ENUM15 = "15"

    class WeepingVinesAge(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"
        ENUM5 = "5"
        ENUM6 = "6"
        ENUM7 = "7"
        ENUM8 = "8"
        ENUM9 = "9"
        ENUM10 = "10"
        ENUM11 = "11"
        ENUM12 = "12"
        ENUM13 = "13"
        ENUM14 = "14"
        ENUM15 = "15"
        ENUM16 = "16"
        ENUM17 = "17"
        ENUM18 = "18"
        ENUM19 = "19"
        ENUM20 = "20"
        ENUM21 = "21"
        ENUM22 = "22"
        ENUM23 = "23"
        ENUM24 = "24"
        ENUM25 = "25"

    #1.20.30
    class BlockFace(Enum):
        DOWN = "down"
        UP = "up"
        NORTH = "north"
        SOUTH = "south"
        EAST = "east"
        WEST = "west"

    class VerticalHalf(Enum):
        BOTTOM = "bottom"
        TOP = "top"


class Items:
    class _basic_item():
        def __init__(self, name : str, is_vanilla: bool = True, item_dimension: Dimension = Dimension.Overworld) -> None:
            self._namespace = 'minecraft' if is_vanilla else ANVIL.NAMESPACE
            self._name = name
            self.dimension = item_dimension
            ITEMS_LIST.append(self)

        def __str__(self) -> str:
            return f'{self._namespace}:{self._name}'
    # Waiting to be added
    # - Piglin Mob Head

    # Added in 1.20.0
    # ---------------------------------------------------------------------------------------------------
    CoastArmorTrim = _basic_item('coast_armor_trim_smithing_template')
    DuneArmorTrim = _basic_item('dune_armor_trim_smithing_template')
    EyeArmorTrim = _basic_item('eye_armor_trim_smithing_template')
    HostArmorTrim = _basic_item('host_armor_trim_smithing_template')
    RaiserArmorTrim = _basic_item('raiser_armor_trim_smithing_template')
    RibArmorTrim = _basic_item('rib_armor_trim_smithing_template')
    SentryArmorTrim = _basic_item('sentry_armor_trim_smithing_template')
    ShaperArmorTrim = _basic_item('shaper_armor_trim_smithing_template')
    SilenceArmorTrim = _basic_item('silence_armor_trim_smithing_template')
    SnoutArmorTrim = _basic_item('snout_armor_trim_smithing_template')
    SpireArmorTrim = _basic_item('spire_armor_trim_smithing_template')
    TideArmorTrim = _basic_item('tide_armor_trim_smithing_template')
    VexArmorTrim = _basic_item('vex_armor_trim_smithing_template')
    WardArmorTrim = _basic_item('ward_armor_trim_smithing_template')
    WayfinderArmorTrim = _basic_item('wayfinder_armor_trim_smithing_template')
    WildArmorTrim = _basic_item('wild_armor_trim_smithing_template')
    NetheriteUpgradeSmithingTemplate = _basic_item('netherite_upgrade_smithing_template')

    AnglerPotteryShard = _basic_item("angler_pottery_shard")
    ArcherPotteryShard = _basic_item("archer_pottery_shard")
    ArmsUpPotteryShard = _basic_item("arms_up_pottery_shard")
    BladePotteryShard = _basic_item("blade_pottery_shard")
    BrewerPotteryShard = _basic_item("brewer_pottery_shard")
    BurnPotteryShard = _basic_item("burn_pottery_shard")
    DangerPotteryShard = _basic_item("danger_pottery_shard")
    ExplorerPotteryShard = _basic_item("explorer_pottery_shard")
    FriendPotteryShard = _basic_item("friend_pottery_shard")
    HeartPotteryShard = _basic_item("heart_pottery_shard")
    HeartbreakPotteryShard = _basic_item("heartbreak_pottery_shard")
    HowlPotteryShard = _basic_item("howl_pottery_shard")
    MinerPotteryShard = _basic_item("miner_pottery_shard")
    MournerPotteryShard = _basic_item("mourner_pottery_shard")
    PlentyPotteryShard = _basic_item("plenty_pottery_shard")
    PrizePotteryShard = _basic_item("prize_pottery_shard")
    SheafPotteryShard = _basic_item("sheaf_pottery_shard")
    ShelterPotteryShard = _basic_item("shelter_pottery_shard")
    SkullPotteryShard = _basic_item("skull_pottery_shard")
    SnortPotteryShard = _basic_item("snort_pottery_shard")
    
    Brush = _basic_item("brush")

    Torchflower = _basic_item("torchflower")
    TorchflowerSeeds = _basic_item("torchflower_seeds")
    PitcherPod = _basic_item("pitcher_pod")

    RelicMusicDisc = _basic_item("music_disc_relic")
    # ---------------------------------------------------------------------------------------------------
    
    Bone = _basic_item("bone")
    Beef = _basic_item("beef")
    CookedBeef = _basic_item("cooked_beef")
    Chicken = _basic_item("chicken")
    CookedChicken = _basic_item("cooked_chicken")
    Egg = _basic_item("egg")
    Flint = _basic_item("flint")
    IronNugget = _basic_item("iron_nugget")
    GoldNugget = _basic_item("gold_nugget")
    Emerald = _basic_item("emerald")
    Coal = _basic_item("coal")
    RottenFlesh = _basic_item("rotten_flesh")
    Leather = _basic_item("leather")
    RabbitFoot = _basic_item("rabbit_foot")
    ClayBall = _basic_item("clay_ball")
    RawCopper = _basic_item("raw_copper")
    Arrow = _basic_item("arrow")
    String = _basic_item("string")

#TO BE REMOVED
class LEGACYItems:
    class _block:
        def __init__(self, identifier, dimension, is_vanilla, creative, *states):
            self._identifier = identifier
            self.dimension = dimension
            self._vanilla = is_vanilla
            self._creative = creative

            self.states = {}
            for state in states:
                self.add_state(state)

        def add_state(self, state):
            self.states[state.name] = state
            setattr(self, state.name, state)

        def __str__(self):
            return f"{'minecraft' if self._vanilla else ANVIL.NAMESPACE}:{self._identifier}"

        def __repr__(self):
            return f"{'minecraft' if self._vanilla else ANVIL.NAMESPACE}:{self._identifier}"

    class _state:
        def __init__(self, name, values):
            self.name = name
            self.values = values

        def __getattr__(self, name):
            if name in self.values:
                return str(name)
            else:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{name}'")

    # Added in 1.20.0
    # ---------------------------------------------------------------------------------------------------

    CherryBoat = _block("cherry_boat", Dimension.Overworld, True, False)
    CherryChestBoat = _block("cherry_chest_boat", Dimension.Overworld, True, False)

    BambooMosaic = _block("bamboo_mosaic", Dimension.Overworld, True, False)
    BambooFence = _block("bamboo_fence", Dimension.Overworld, True, False)
    BambooFenceGate = _block("bamboo_fence_gate", Dimension.Overworld, True, False)
    BambooStairs = _block("bamboo_stairs", Dimension.Overworld, True, False)
    BambooDoor = _block("bamboo_door", Dimension.Overworld, True, False)
    BambooTrapdoor = _block("bamboo_trapdoor", Dimension.Overworld, True, False)
    BambooSlab = _block("bamboo_slab", Dimension.Overworld, True, False)
    BambooMosaicSlab = _block("bamboo_mosaic_slab", Dimension.Overworld, True, False)
    BambooMosaicStairs = _block("bamboo_mosaic_stairs", Dimension.Overworld, True, False)
    BambooRaft = _block("bamboo_raft", Dimension.Overworld, True, False)
    BambooChestRaft = _block("bamboo_raft_boat", Dimension.Overworld, True, False)
    BambooButton = _block("bamboo_button", Dimension.Overworld, True, False)
    BambooPressurePlate = _block("bamboo_pressure_plate", Dimension.Overworld, True, False)
    BambooSign = _block("bamboo_sign", Dimension.Overworld, True, False)

    CamelSpawnEgg = _block("camel_spawn_egg", Dimension.Overworld, True, True)
    ChiseledBookshelf = _block("chiseled_bookshelf", Dimension.Overworld, True, True)
    BambooHangingSign = _block("bamboo_hanging_sign", Dimension.Overworld, True, True)
    MangroveHangingSign = _block("mangrove_hanging_sign", Dimension.Overworld, True, True)
    WarpedHangingSign = _block("warped_hanging_sign", Dimension.Overworld, True, True)
    CrimsonHangingSign = _block("crimson_hanging_sign", Dimension.Overworld, True, True)
    DarkOakHangingSign = _block("dark_oak_hanging_sign", Dimension.Overworld, True, True)
    AcaciaHangingSign = _block("acacia_hanging_sign", Dimension.Overworld, True, True)
    JungleHangingSign = _block("jungle_hanging_sign", Dimension.Overworld, True, True)
    BirchHangingSign = _block("birch_hanging_sign",Dimension.Overworld, True, True)
    SpruceHangingSign = _block("spruce_hanging_sign", Dimension.Overworld, True, True)
    OakHangingSign = _block("oak_hanging_sign", Dimension.Overworld, True, True)

    CobblestoneWall = _block("cobblestone_wall", Dimension.Overworld, True, False,_state("variant", ["cobblestone_wall", "mossy_cobblestone_wall", "granite_wall", "diorite_wall", "andesite_wall", "sandstone_wall", "red_sandstone_wall", "stone_brick_wall", "mossy_stone_brick_wall", "brick_wall", "nether_brick_wall", "red_nether_brick_wall", "end_stone_brick_wall", "prismarine_wall", ]))
    BlackstoneWall = _block("blackstone_wall", Dimension.Nether, True, False)
    PolishedBlackstoneWall = _block("polished_blackstone_wall", Dimension.Nether, True, False)
    PolishedBlackstoneBrickWall = _block("polished_blackstone_brick_wall", Dimension.Nether, True, False)
    CobbledDeepslateWall = _block("cobbled_deepslate_wall", Dimension.Overworld, True, False)
    DeepslateTileWall = _block("deepslate_tile_wall", Dimension.Overworld, True, False)
    PolishedDeepslateWall = _block("polished_deepslate_wall", Dimension.Overworld, True, False)
    DeepslateBrickWall = _block("deepslate_brick_wall", Dimension.Overworld, True, False)
    MudBrickWall = _block("mud_brick_wall", Dimension.Overworld, True, False)

    OakFence = _block("oak_fence", Dimension.Overworld, True, False)
    SpruceFence = _block("spruce_fence", Dimension.Overworld, True, False)
    BirchFence = _block("birch_fence", Dimension.Overworld, True, False)
    JungleFence = _block("jungle_fence", Dimension.Overworld, True, False)
    AcaciaFence = _block("acacia_fence", Dimension.Overworld, True, False)
    DarkOakFence = _block("dark_oak_fence", Dimension.Overworld, True, False)
    MangroveFence = _block("mangrove_fence", Dimension.Overworld, True, False)
    NetherBrickFence = _block("nether_brick_fence",Dimension.Nether, True, False)
    CrimsonFence = _block("crimson_fence", Dimension.Nether, True, False)
    WarpedFence = _block("warped_fence", Dimension.Nether, True, False)
    OakFenceGate = _block("fence_gate", Dimension.Overworld, True, False)
    SpruceFenceGate = _block("spruce_fence_gate", Dimension.Overworld, True, False)
    BirchFenceGate = _block("birch_fence_gate", Dimension.Overworld, True, False)
    JungleFenceGate = _block("jungle_fence_gate", Dimension.Overworld, True, False)
    AcaciaFenceGate = _block("acacia_fence_gate", Dimension.Overworld, True, False)
    DarkOakFenceGate = _block("dark_oak_fence_gate",Dimension.Overworld, True, False)
    MangroveFenceGate = _block("mangrove_fence_gate", Dimension.Overworld, True, False)
    CrimsonFenceGate = _block("crimson_fence_gate",Dimension.Nether, True, False)
    WarpedFenceGate = _block("warped_fence_gate", Dimension.Nether, True, False)
    NormalStoneStairs = _block("normal_stone_stairs", Dimension.Overworld, True, False)
    StoneStairs = _block("stone_stairs", Dimension.Overworld, True, False)
    MossyCobblestoneStairs = _block("mossy_cobblestone_stairs", Dimension.Overworld, True, False)
    OakStairs = _block("oak_stairs", Dimension.Overworld, True, False)
    SpruceStairs = _block("spruce_stairs", Dimension.Overworld, True, False)
    BirchStairs = _block("birch_stairs", Dimension.Overworld, True, False)
    JungleStairs = _block("jungle_stairs", Dimension.Overworld, True, False)
    AcaciaStairs = _block("acacia_stairs", Dimension.Overworld, True, False)
    DarkOakStairs = _block("dark_oak_stairs", Dimension.Overworld, True, False)
    MangroveStairs = _block("mangrove_stairs", Dimension.Overworld, True, False)
    StoneBrickStairs = _block("stone_brick_stairs",Dimension.Overworld, True, False)
    MossyStoneBrickStairs = _block("mossy_stone_brick_stairs", Dimension.Overworld, True, False)
    SandstoneStairs = _block("sandstone_stairs", Dimension.Overworld, True, False)
    SmoothSandstoneStairs = _block("smooth_sandstone_stairs", Dimension.Overworld, True, False)
    RedSandstoneStairs = _block("red_sandstone_stairs", Dimension.Overworld, True, False)
    SmoothRedSandstoneStairs = _block("smooth_red_sandstone_stairs", Dimension.Overworld, True, False)
    GraniteStairs = _block("granite_stairs", Dimension.Overworld, True, False)
    PolishedGraniteStairs = _block("polished_granite_stairs", Dimension.Overworld, True, False)
    DioriteStairs = _block("diorite_stairs", Dimension.Overworld, True, False)
    PolishedDioriteStairs = _block("polished_diorite_stairs", Dimension.Overworld, True, False)
    AndesiteStairs = _block("andesite_stairs", Dimension.Overworld, True, False)
    PolishedAndesiteStairs = _block("polished_andesite_stairs", Dimension.Overworld, True, False)
    BrickStairs = _block("brick_stairs", Dimension.Overworld, True, False)
    NetherBrickStairs = _block("nether_brick_stairs", Dimension.Nether, True, False)
    RedNetherBrickStairs = _block("red_nether_brick_stairs", Dimension.Nether, True, False)
    EndBrickStairs = _block("end_brick_stairs", Dimension.End, True, False)
    QuartzStairs = _block("quartz_stairs", Dimension.Nether, True, False)
    SmoothQuartzStairs = _block("smooth_quartz_stairs", Dimension.Nether, True, False)
    PurpurStairs = _block("purpur_stairs", Dimension.End, True, False,)
    PrismarineStairs = _block("prismarine_stairs", Dimension.Overworld, True, False)
    DarkPrismarineStairs = _block("dark_prismarine_stairs", Dimension.Overworld, True, False)
    PrismarineBricksStairs = _block("prismarine_bricks_stairs", Dimension.Overworld, True, False)
    CrimsonStairs = _block("crimson_stairs", Dimension.Nether, True, False)
    WarpedStairs = _block("warped_stairs", Dimension.Nether, True, False)
    BlackstoneStairs = _block("blackstone_stairs", Dimension.Nether, True, False)
    PolishedBlackstoneStairs = _block("polished_blackstone_stairs", Dimension.Nether, True, False)
    PolishedBlackstoneBrickStairs = _block("polished_blackstone_brick_stairs", Dimension.Nether, True, False)
    CutCopperStairs = _block("cut_copper_stairs", Dimension.Overworld, True, False)
    ExposedCutCopperStairs = _block("exposed_cut_copper_stairs", Dimension.Overworld, True, False)
    WeatheredCutCopperStairs = _block("weathered_cut_copper_stairs", Dimension.Overworld, True, False)
    OxidizedCutCopperStairs = _block("oxidized_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedCutCopperStairs = _block("waxed_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedExposedCutCopperStairs = _block("waxed_exposed_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedWeatheredCutCopperStairs = _block("waxed_weathered_cut_copper_stairs", Dimension.Overworld, True, False)
    WaxedOxidizedCutCopperStairs = _block("waxed_oxidized_cut_copper_stairs", Dimension.Overworld, True, False)
    CobbledDeepslateStairs = _block("cobbled_deepslate_stairs", Dimension.Overworld, True, False)
    DeepslateTileStairs = _block("deepslate_tile_stairs", Dimension.Overworld, True, False)
    PolishedDeepslateStairs = _block("polished_deepslate_stairs", Dimension.Overworld, True, False)
    DeepslateBrickStairs = _block("deepslate_brick_stairs", Dimension.Overworld, True, False)
    MudBrickStairs = _block("mud_brick_stairs", Dimension.Overworld, True, False)
    WoodenDoor = _block("wooden_door", Dimension.Overworld, True, False)
    SpruceDoor = _block("spruce_door", Dimension.Overworld, True, False)
    BirchDoor = _block("birch_door", Dimension.Overworld, True, False)
    JungleDoor = _block("jungle_door", Dimension.Overworld, True, False)
    AcaciaDoor = _block("acacia_door", Dimension.Overworld, True, False)
    DarkOakDoor = _block("dark_oak_door", Dimension.Overworld, True, False)
    MangroveDoor = _block("mangrove_door", Dimension.Overworld, True, False)
    IronDoor = _block("iron_door", Dimension.Overworld, True, False)
    CrimsonDoor = _block("crimson_door", Dimension.Nether, True, False)
    WarpedDoor = _block("warped_door", Dimension.Nether, True, False)
    Trapdoor = _block("trapdoor", Dimension.Overworld, True, False)
    SpruceTrapdoor = _block("spruce_trapdoor", Dimension.Overworld, True, False)
    BirchTrapdoor = _block("birch_trapdoor", Dimension.Overworld, True, False)
    JungleTrapdoor = _block("jungle_trapdoor", Dimension.Overworld, True, False)
    AcaciaTrapdoor = _block("acacia_trapdoor", Dimension.Overworld, True, False)
    DarkOakTrapdoor = _block("dark_oak_trapdoor", Dimension.Overworld, True, False)
    MangroveTrapdoor = _block("mangrove_trapdoor", Dimension.Overworld, True, False)
    IronTrapdoor = _block("iron_trapdoor", Dimension.Overworld, True, False)
    CrimsonTrapdoor = _block("crimson_trapdoor", Dimension.Nether, True, False)
    WarpedTrapdoor = _block("warped_trapdoor", Dimension.Nether, True, False)
    IronBars = _block("iron_bars", Dimension.Overworld, True, False)
    Glass = _block("glass", Dimension.Overworld, True, False)
    StainedGlass = _block("stained_glass", Dimension.Overworld, True, False, _state("variant", ["white_stained_glass", "gray_stained_glass", "light_gray_stained_glass", "black_stained_glass", "brown_stained_glass", "red_stained_glass", "orange_stained_glass", "yellow_stained_glass", "lime_stained_glass", "green_stained_glass", "cyan_stained_glass", "light_blue_stained_glass", "blue_stained_glass", "purple_stained_glass", "magenta_stained_glass", "pink_stained_glass", ]))
    TintedGlass = _block("tinted_glass", Dimension.Overworld, True, False)
    GlassPane = _block("glass_pane", Dimension.Overworld, True, False)
    StainedGlassPane = _block("stained_glass_pane", Dimension.Overworld, True, False, _state("variant", ["white_stained_glass_pane", "gray_stained_glass_pane", "light_gray_stained_glass_pane", "black_stained_glass_pane", "brown_stained_glass_pane", "red_stained_glass_pane", "orange_stained_glass_pane", "yellow_stained_glass_pane", "lime_stained_glass_pane", "green_stained_glass_pane", "cyan_stained_glass_pane", "light_blue_stained_glass_pane", "blue_stained_glass_pane", "purple_stained_glass_pane", "magenta_stained_glass_pane", "pink_stained_glass_pane", ]))
    Ladder = _block("ladder", Dimension.Overworld, True, False)
    Scaffolding = _block("scaffolding", Dimension.Overworld, True, False)
    StoneSlab4 = _block("stone_slab4", Dimension.Overworld, True, False, _state("variant", ["stone_slab", "mossy_stone_brick_slab", "cut_sandstone_slab", "cut_red_sandstone_slab", "smooth_quartz_slab", ]))
    StoneSlab = _block("stone_slab", Dimension.Overworld, True, False, _state("variant", ["smooth_stone_slab", "cobblestone_slab", "stone_brick_slab", "sandstone_slab", "brick_slab", "nether_brick_slab", "quartz_slab", ]))
    StoneSlab2 = _block("stone_slab2", Dimension.Overworld, True, False, _state("variant", ["mossy_cobblestone_slab", "smooth_sandstone_slab", "red_sandstone_slab", "red_nether_brick_slab", "purpur_slab", "prismarine_slab", "dark_prismarine_slab", "prismarine_brick_slab", ]))
    WoodenSlab = _block("wooden_slab", Dimension.Overworld, True, False, _state("variant", ["oak_slab", "spruce_slab", "birch_slab", "jungle_slab", "acacia_slab", "dark_oak_slab", ]))
    MangroveSlab = _block("mangrove_slab", Dimension.Overworld, True, False)
    StoneSlab3 = _block("stone_slab3", Dimension.Overworld, True, False, _state("variant", ["smooth_red_sandstone_slab", "granite_slab", "polished_granite_slab", "diorite_slab", "polished_diorite_slab", "andesite_slab", "polished_andesite_slab", "end_stone_slab", ]))
    CrimsonSlab = _block("crimson_slab", Dimension.Nether, True, False)
    WarpedSlab = _block("warped_slab", Dimension.Nether, True, False)
    BlackstoneSlab = _block("blackstone_slab", Dimension.Nether, True, False)
    PolishedBlackstoneSlab = _block("polished_blackstone_slab", Dimension.Nether, True, False)
    PolishedBlackstoneBrickSlab = _block("polished_blackstone_brick_slab", Dimension.Nether, True, False)
    CutCopperSlab = _block("cut_copper_slab", Dimension.Overworld, True, False)
    ExposedCutCopperSlab = _block("exposed_cut_copper_slab", Dimension.Overworld, True, False)
    WeatheredCutCopperSlab = _block("weathered_cut_copper_slab", Dimension.Overworld, True, False)
    OxidizedCutCopperSlab = _block("oxidized_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedCutCopperSlab = _block("waxed_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedExposedCutCopperSlab = _block("waxed_exposed_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedWeatheredCutCopperSlab = _block("waxed_weathered_cut_copper_slab", Dimension.Overworld, True, False)
    WaxedOxidizedCutCopperSlab = _block("waxed_oxidized_cut_copper_slab", Dimension.Overworld, True, False)
    CobbledDeepslateSlab = _block("cobbled_deepslate_slab", Dimension.Overworld, True, False)
    PolishedDeepslateSlab = _block("polished_deepslate_slab", Dimension.Overworld, True, False)
    DeepslateTileSlab = _block("deepslate_tile_slab", Dimension.Overworld, True, False)
    DeepslateBrickSlab = _block("deepslate_brick_slab", Dimension.Overworld, True, False)
    MudBrickSlab = _block("mud_brick_slab", Dimension.Overworld, True, False)
    BrickBlock = _block("brick_block", Dimension.Overworld, True, False)
    ChiseledNetherBricks = _block("chiseled_nether_bricks", Dimension.Nether, True, False)
    CrackedNetherBricks = _block("cracked_nether_bricks", Dimension.Nether, True, False)
    QuartzBricks = _block("quartz_bricks", Dimension.Nether, True, False)
    Stonebrick = _block("stonebrick", Dimension.Overworld, True, False,_state("variant", ["stone_bricks", "mossy_stone_bricks", "cracked_stone_bricks", "chiseled_stone_bricks", ]))
    EndBricks = _block("end_bricks",Dimension.End,True,False)
    Prismarine = _block("prismarine", Dimension.Overworld, True, False,_state("variant", ["prismarine_bricks", "prismarine", "dark_prismarine"]))
    PolishedBlackstoneBricks = _block("polished_blackstone_bricks", Dimension.Nether, True, False)
    CrackedPolishedBlackstoneBricks = _block("cracked_polished_blackstone_bricks", Dimension.Nether, True, False)
    GildedBlackstone = _block("gilded_blackstone", Dimension.Nether, True, False)
    ChiseledPolishedBlackstone = _block("chiseled_polished_blackstone", Dimension.Nether, True, False)
    DeepslateTiles = _block("deepslate_tiles", Dimension.Overworld, True, False)
    CrackedDeepslateTiles = _block("cracked_deepslate_tiles", Dimension.Overworld, True, False)
    DeepslateBricks = _block("deepslate_bricks", Dimension.Overworld, True, False)
    CrackedDeepslateBricks = _block("cracked_deepslate_bricks", Dimension.Overworld, True, False)
    ChiseledDeepslate = _block("chiseled_deepslate", Dimension.Overworld, True, False)
    Cobblestone = _block("cobblestone", Dimension.Overworld, True, False)
    MossyCobblestone = _block("mossy_cobblestone", Dimension.Overworld, True, False)
    CobbledDeepslate = _block("cobbled_deepslate", Dimension.Overworld, True, False)
    SmoothStone = _block("smooth_stone", Dimension.Overworld, True, False)
    Sandstone = _block("sandstone", Dimension.Overworld, True, False,_state("variant", ["sandstone", "chiseled_sandstone", "cut_sandstone", "smooth_sandstone", ]))
    RedSandstone = _block("red_sandstone", Dimension.Overworld, True, False,_state("variant", ["red_sandstone", "chiseled_red_sandstone", "cut_red_sandstone", "smooth_red_sandstone", ]))
    CoalBlock = _block("coal_block", Dimension.Overworld, True, False)
    DriedKelpBlock = _block("dried_kelp_block", Dimension.Overworld, True, False)
    GoldBlock = _block("gold_block", Dimension.Overworld, True, False)
    IronBlock = _block("iron_block", Dimension.Overworld, True, False)
    CopperBlock = _block("copper_block", Dimension.Overworld, True, False)
    ExposedCopper = _block("exposed_copper", Dimension.Overworld, True, False)
    WeatheredCopper = _block("weathered_copper", Dimension.Overworld, True, False)
    OxidizedCopper = _block("oxidized_copper", Dimension.Overworld, True, False)
    WaxedCopper = _block("waxed_copper", Dimension.Overworld, True, False)
    WaxedExposedCopper = _block("waxed_exposed_copper", Dimension.Overworld, True, False)
    WaxedWeatheredCopper = _block("waxed_weathered_copper", Dimension.Overworld, True, False)
    WaxedOxidizedCopper = _block("waxed_oxidized_copper", Dimension.Overworld, True, False)
    CutCopper = _block("cut_copper", Dimension.Overworld, True, False)
    ExposedCutCopper = _block("exposed_cut_copper",Dimension.Overworld, True, False)
    WeatheredCutCopper = _block("weathered_cut_copper", Dimension.Overworld, True, False)
    OxidizedCutCopper = _block("oxidized_cut_copper", Dimension.Overworld, True, False)
    WaxedCutCopper = _block("waxed_cut_copper", Dimension.Overworld, True, False)
    WaxedExposedCutCopper = _block("waxed_exposed_cut_copper", Dimension.Overworld, True, False)
    WaxedWeatheredCutCopper = _block("waxed_weathered_cut_copper", Dimension.Overworld, True, False)
    WaxedOxidizedCutCopper = _block("waxed_oxidized_cut_copper", Dimension.Overworld, True, False)
    EmeraldBlock = _block("emerald_block", Dimension.Overworld, True, False)
    DiamondBlock = _block("diamond_block", Dimension.Overworld, True, False)
    LapisBlock = _block("lapis_block", Dimension.Overworld, True, False)
    RawIronBlock = _block("raw_iron_block", Dimension.Overworld, True, False)
    RawCopperBlock = _block("raw_copper_block", Dimension.Overworld, True, False)
    RawGoldBlock = _block("raw_gold_block", Dimension.Overworld, True, False)
    QuartzBlock = _block("quartz_block", Dimension.Nether, True, False, _state("variant", ["quartz_block", "quartz_pillar", "chiseled_quartz_block", "smooth_quartz", ]))
    Slime = _block("slime", Dimension.Overworld, True, False)
    HoneyBlock = _block("honey_block", Dimension.Overworld, True, False)
    HoneycombBlock = _block("honeycomb_block", Dimension.Overworld, True, False)
    HayBlock = _block("hay_block", Dimension.Overworld, True, False)
    BoneBlock = _block("bone_block", Dimension.Overworld, True, False)
    NetherBrick = _block("nether_brick", Dimension.Nether, True, False)
    RedNetherBrick = _block("red_nether_brick", Dimension.Nether, True, False)
    NetheriteBlock = _block("netherite_block", Dimension.Nether, True, False)
    Lodestone = _block("lodestone", Dimension.Overworld, True, False)

    ConcretePowder = _block("concrete_powder", Dimension.Overworld, True, False, _state("variant", ["white_concrete_powder", "light_gray_concrete_powder", "gray_concrete_powder", "black_concrete_powder", "brown_concrete_powder", "red_concrete_powder", "orange_concrete_powder", "yellow_concrete_powder", "lime_concrete_powder", "green_concrete_powder", "cyan_concrete_powder", "light_blue_concrete_powder", "blue_concrete_powder", "purple_concrete_powder", "magenta_concrete_powder", "pink_concrete_powder", ]))
    Concrete = _block("concrete", Dimension.Overworld, True, False, _state("variant", ["white_concrete", "light_gray_concrete", "gray_concrete", "black_concrete", "brown_concrete", "red_concrete", "orange_concrete", "yellow_concrete", "lime_concrete", "green_concrete", "cyan_concrete", "light_blue_concrete", "blue_concrete", "purple_concrete", "magenta_concrete", "pink_concrete", ]))
    Clay = _block("clay", Dimension.Overworld, True, False)
    HardenedClay = _block("hardened_clay", Dimension.Overworld, True, False)
    StainedHardenedClay = _block("stained_hardened_clay", Dimension.Overworld, True, False, _state("variant", ["white_terracotta", "light_gray_terracotta", "gray_terracotta", "black_terracotta", "brown_terracotta", "red_terracotta", "orange_terracotta", "yellow_terracotta", "lime_terracotta", "green_terracotta", "cyan_terracotta", "light_blue_terracotta", "blue_terracotta", "purple_terracotta", "magenta_terracotta", "pink_terracotta", ]))
    WhiteGlazedTerracotta = _block("white_glazed_terracotta", Dimension.Overworld, True, False)
    SilverGlazedTerracotta = _block("silver_glazed_terracotta", Dimension.Overworld, True, False)
    GrayGlazedTerracotta = _block("gray_glazed_terracotta", Dimension.Overworld, True, False)
    BlackGlazedTerracotta = _block("black_glazed_terracotta", Dimension.Overworld, True, False)
    BrownGlazedTerracotta = _block("brown_glazed_terracotta", Dimension.Overworld, True, False)
    RedGlazedTerracotta = _block("red_glazed_terracotta", Dimension.Overworld, True, False)
    OrangeGlazedTerracotta = _block("orange_glazed_terracotta", Dimension.Overworld, True, False)
    YellowGlazedTerracotta = _block("yellow_glazed_terracotta", Dimension.Overworld, True, False)
    LimeGlazedTerracotta = _block("lime_glazed_terracotta", Dimension.Overworld, True, False)
    GreenGlazedTerracotta = _block("green_glazed_terracotta", Dimension.Overworld, True, False)
    CyanGlazedTerracotta = _block("cyan_glazed_terracotta", Dimension.Overworld, True, False)
    LightBlueGlazedTerracotta = _block("light_blue_glazed_terracotta", Dimension.Overworld, True, False)
    BlueGlazedTerracotta = _block("blue_glazed_terracotta", Dimension.Overworld, True, False)
    PurpleGlazedTerracotta = _block("purple_glazed_terracotta", Dimension.Overworld, True, False)
    MagentaGlazedTerracotta = _block("magenta_glazed_terracotta", Dimension.Overworld, True, False)
    PinkGlazedTerracotta = _block("pink_glazed_terracotta", Dimension.Overworld, True, False)
    PurpurBlock = _block("purpur_block",Dimension.End,True,False,_state("variant", ["purpur_block", "purpur_pillar"]))
    PackedMud = _block("packed_mud", Dimension.Overworld, True, False)
    MudBricks = _block("mud_bricks", Dimension.Overworld, True, False)
    NetherWartBlock = _block("nether_wart_block", Dimension.Nether, True, False)
    WarpedWartBlock = _block("warped_wart_block", Dimension.Nether, True, False)
    Shroomlight = _block("shroomlight", Dimension.Nether, True, False)
    CrimsonNylium = _block("crimson_nylium", Dimension.Nether, True, False)
    WarpedNylium = _block("warped_nylium", Dimension.Nether, True, False)
    Basalt = _block("basalt", Dimension.Nether, True, False)
    PolishedBasalt = _block("polished_basalt", Dimension.Nether, True, False)
    SmoothBasalt = _block("smooth_basalt", Dimension.Nether, True, False)
    SoulSoil = _block("soul_soil", Dimension.Nether, True, False)
    Dirt = _block("dirt", Dimension.Overworld, True, False,_state("variant", ["dirt", "coarse_dirt", ]))
    Farmland = _block("farmland", Dimension.Overworld, True, False)
    Grass = _block("grass", Dimension.Overworld, True, False)
    GrassPath = _block("grass_path", Dimension.Overworld, True, False)
    Podzol = _block("podzol", Dimension.Overworld, True, False)
    Mycelium = _block("mycelium", Dimension.Overworld, True, False)
    Mud = _block("mud", Dimension.Overworld, True, False)
    IronOre = _block("iron_ore", Dimension.Overworld, True, False)
    GoldOre = _block("gold_ore", Dimension.Overworld, True, False)
    DiamondOre = _block("diamond_ore", Dimension.Overworld, True, False)
    LapisOre = _block("lapis_ore", Dimension.Overworld, True, False)
    RedstoneOre = _block("redstone_ore", Dimension.Overworld, True, False)
    CoalOre = _block("coal_ore", Dimension.Overworld, True, False)
    CopperOre = _block("copper_ore", Dimension.Overworld, True, False)
    EmeraldOre = _block("emerald_ore", Dimension.Overworld, True, False)
    QuartzOre = _block("quartz_ore", Dimension.Nether, True, False)
    NetherGoldOre = _block("nether_gold_ore", Dimension.Nether, True, False)
    AncientDebris = _block("ancient_debris", Dimension.Nether, True, False)
    DeepslateIronOre = _block("deepslate_iron_ore",Dimension.Overworld, True, False)
    DeepslateGoldOre = _block("deepslate_gold_ore",Dimension.Overworld, True, False)
    DeepslateDiamondOre = _block("deepslate_diamond_ore", Dimension.Overworld, True, False)
    DeepslateLapisOre = _block("deepslate_lapis_ore", Dimension.Overworld, True, False)
    DeepslateRedstoneOre = _block("deepslate_redstone_ore", Dimension.Overworld, True, False)
    DeepslateEmeraldOre = _block("deepslate_emerald_ore", Dimension.Overworld, True, False)
    DeepslateCoalOre = _block("deepslate_coal_ore",Dimension.Overworld, True, False)
    DeepslateCopperOre = _block("deepslate_copper_ore", Dimension.Overworld, True, False)
    Gravel = _block("gravel", Dimension.Overworld, True, False)
    Blackstone = _block("blackstone", Dimension.Nether, True, False)
    Deepslate = _block("deepslate", Dimension.Overworld, True, False)
    PolishedBlackstone = _block("polished_blackstone", Dimension.Nether, True, False)
    PolishedDeepslate = _block("polished_deepslate", Dimension.Overworld, True, False)
    Sand = _block("sand", Dimension.Overworld, True, False,_state("variant", ["sand", "red_sand", ]))
    Cactus = _block("cactus", Dimension.Overworld, True, False)
    StrippedOakLog = _block("stripped_oak_log", Dimension.Overworld, True, False)
    StrippedSpruceLog = _block("stripped_spruce_log", Dimension.Overworld, True, False)
    StrippedBirchLog = _block("stripped_birch_log",Dimension.Overworld, True, False)
    StrippedJungleLog = _block("stripped_jungle_log", Dimension.Overworld, True, False)
    StrippedAcaciaLog = _block("stripped_acacia_log", Dimension.Overworld, True, False)
    StrippedDarkOakLog = _block("stripped_dark_oak_log", Dimension.Overworld, True, False)
    MangroveLog = _block("mangrove_log", Dimension.Overworld, True, False)
    StrippedMangroveLog = _block("stripped_mangrove_log", Dimension.Overworld, True, False)
    CrimsonStem = _block("crimson_stem", Dimension.Nether, True, False)
    StrippedCrimsonStem = _block("stripped_crimson_stem", Dimension.Nether, True, False)
    WarpedStem = _block("warped_stem", Dimension.Nether, True, False)
    StrippedWarpedStem = _block("stripped_warped_stem", Dimension.Nether, True, False)
    Wood = _block("wood", Dimension.Overworld, True, False,_state("variant", ["oak_wood", "stripped_oak_wood", "spruce_wood", "stripped_spruce_wood", "birch_wood", "stripped_birch_wood", "jungle_wood", "stripped_jungle_wood", "acacia_wood", "stripped_acacia_wood", "dark_oak_wood", "stripped_dark_oak_wood", ]))
    MangroveWood = _block("mangrove_wood", Dimension.Overworld, True, False)
    StrippedMangroveWood = _block("stripped_mangrove_wood", Dimension.Overworld, True, False)
    CrimsonHyphae = _block("crimson_hyphae", Dimension.Nether, True, False)
    StrippedCrimsonHyphae = _block("stripped_crimson_hyphae", Dimension.Nether, True, False)
    WarpedHyphae = _block("warped_hyphae", Dimension.Nether, True, False)
    StrippedWarpedHyphae = _block("stripped_warped_hyphae", Dimension.Nether, True, False)
    Leaves = _block("leaves", Dimension.Overworld, True, False,_state("variant", ["oak_leaves", "spruce_leaves", "birch_leaves", "jungle_leaves", ]))
    Leaves2 = _block("leaves2", Dimension.Overworld, True, False,_state("variant", ["acacia_leaves", "dark_oak_leaves", ]))
    MangroveLeaves = _block("mangrove_leaves", Dimension.Overworld, True, False)
    AzaleaLeaves = _block("azalea_leaves", Dimension.Overworld, True, False)
    AzaleaLeavesFlowered = _block("azalea_leaves_flowered", Dimension.Overworld, True, False)
    Sapling = _block("sapling", Dimension.Overworld, True, False,_state("variant", ["oak_sapling", "spruce_sapling", "birch_sapling", "jungle_sapling", "acacia_sapling", "dark_oak_sapling", ]))
    MangrovePropagule = _block("mangrove_propagule", Dimension.Overworld, True, False)
    BeeNest = _block("bee_nest", Dimension.Overworld, True, False)
    WheatSeeds = _block("wheat_seeds", Dimension.Overworld, True, False)
    PumpkinSeeds = _block("pumpkin_seeds", Dimension.Overworld, True, False)
    MelonSeeds = _block("melon_seeds", Dimension.Overworld, True, False)
    BeetrootSeeds = _block("beetroot_seeds", Dimension.Overworld, True, False)
    Wheat = _block("wheat", Dimension.Overworld, True, False)
    Beetroot = _block("beetroot", Dimension.Overworld, True, False)
    Potato = _block("potato", Dimension.Overworld, True, False)
    PoisonousPotato = _block("poisonous_potato", Dimension.Overworld, True, False)
    Carrot = _block("carrot", Dimension.Overworld, True, False)
    GoldenCarrot = _block("golden_carrot", Dimension.Overworld, True, False)
    Apple = _block("apple", Dimension.Overworld, True, False)
    GoldenApple = _block("golden_apple", Dimension.Overworld, True, False)
    EnchantedGoldenApple = _block("enchanted_golden_apple", Dimension.Overworld, True, False)
    MelonBlock = _block("melon_block", Dimension.Overworld, True, False)
    MelonSlice = _block("melon_slice", Dimension.Overworld, True, False)
    GlisteringMelonSlice = _block("glistering_melon_slice", Dimension.Overworld, True, False)
    SweetBerries = _block("sweet_berries", Dimension.Overworld, True, False)
    GlowBerries = _block("glow_berries", Dimension.Overworld, True, False)
    Pumpkin = _block("pumpkin", Dimension.Overworld, True, False)
    CarvedPumpkin = _block("carved_pumpkin", Dimension.Overworld, True, False)
    LitPumpkin = _block("lit_pumpkin", Dimension.Overworld, True, False)
    Honeycomb = _block("honeycomb", Dimension.Overworld, True, False)
    Tallgrass = _block("tallgrass", Dimension.Overworld, True, False,_state("variant", ["fern", "grass", ]))
    DoublePlant = _block("double_plant", Dimension.Overworld, True, False,_state("variant", ["large_fern", "tall_grass", "sunflower", "lilac", "rose_bush", "peony", ]))
    NetherSprouts = _block("nether_sprouts", Dimension.Nether, True, False)
    CoralFan = _block("coral_fan", Dimension.Overworld, True, False,_state("variant", ["fire_coral_fan", "brain_coral_fan", "bubble_coral_fan", "tube_coral_fan", "horn_coral_fan", ]))
    CoralFanDead = _block("coral_fan_dead", Dimension.Overworld, True, False,_state("variant", ["dead_fire_coral_fan", "dead_brain_coral_fan", "dead_bubble_coral_fan", "dead_tube_coral_fan", "dead_horn_coral_fan", ]))
    Kelp = _block("kelp", Dimension.Overworld, True, False)
    Seagrass = _block("seagrass", Dimension.Overworld, True, False)
    CrimsonRoots = _block("crimson_roots", Dimension.Nether, True, False)
    WarpedRoots = _block("warped_roots", Dimension.Nether, True, False)
    YellowFlower = _block("yellow_flower", Dimension.Overworld, True, False)
    RedFlower = _block("red_flower", Dimension.Overworld, True, False,_state("variant", ["poppy", "blue_orchid", "allium", "azure_bluet", "red_tulip", "orange_tulip", "white_tulip", "pink_tulip", "oxeye_daisy", "cornflower", "lily_of_the_valley", ]))
    WitherRose = _block("wither_rose", Dimension.Overworld, True, False)
    WhiteDye = _block("white_dye", Dimension.Overworld, True, False)
    LightGrayDye = _block("light_gray_dye", Dimension.Overworld, True, False)
    GrayDye = _block("gray_dye", Dimension.Overworld, True, False)
    BrownDye = _block("brown_dye", Dimension.Overworld, True, False)
    BlackDye = _block("black_dye", Dimension.Overworld, True, False)
    RedDye = _block("red_dye", Dimension.Overworld, True, False)
    OrangeDye = _block("orange_dye", Dimension.Overworld, True, False)
    YellowDye = _block("yellow_dye", Dimension.Overworld, True, False)
    LimeDye = _block("lime_dye", Dimension.Overworld, True, False)
    GreenDye = _block("green_dye", Dimension.Overworld, True, False)
    CyanDye = _block("cyan_dye", Dimension.Overworld, True, False)
    LightBlueDye = _block("light_blue_dye", Dimension.Overworld, True, False)
    BlueDye = _block("blue_dye", Dimension.Overworld, True, False)
    PurpleDye = _block("purple_dye", Dimension.Overworld, True, False)
    MagentaDye = _block("magenta_dye", Dimension.Overworld, True, False)
    PinkDye = _block("pink_dye", Dimension.Overworld, True, False)
    InkSac = _block("ink_sac", Dimension.Overworld, True, False)
    GlowInkSac = _block("glow_ink_sac", Dimension.Overworld, True, False)
    CocoaBeans = _block("cocoa_beans", Dimension.Overworld, True, False)
    LapisLazuli = _block("lapis_lazuli", Dimension.Overworld, True, False)
    BoneMeal = _block("bone_meal", Dimension.Overworld, True, False)
    Vine = _block("vine", Dimension.Overworld, True, False)
    WeepingVines = _block("weeping_vines", Dimension.Nether, True, False)
    TwistingVines = _block("twisting_vines", Dimension.Nether, True, False)
    Waterlily = _block("waterlily", Dimension.Overworld, True, False)
    Deadbush = _block("deadbush", Dimension.Overworld, True, False)
    Bamboo = _block("bamboo", Dimension.Overworld, True, False)
    Snow = _block("snow", Dimension.Overworld, True, False)
    Ice = _block("ice", Dimension.Overworld, True, False)
    PackedIce = _block("packed_ice", Dimension.Overworld, True, False)
    BlueIce = _block("blue_ice", Dimension.Overworld, True, False)
    SnowLayer = _block("snow_layer", Dimension.Overworld, True, False)
    PointedDripstone = _block("pointed_dripstone", Dimension.Overworld, True, False)
    DripstoneBlock = _block("dripstone_block", Dimension.Overworld, True, False)
    MossCarpet = _block("moss_carpet", Dimension.Overworld, True, False)
    MossBlock = _block("moss_block", Dimension.Overworld, True, False)
    DirtWithRoots = _block("dirt_with_roots", Dimension.Overworld, True, False)
    HangingRoots = _block("hanging_roots", Dimension.Overworld, True, False)
    MangroveRoots = _block("mangrove_roots", Dimension.Overworld, True, False)
    MuddyMangroveRoots = _block("muddy_mangrove_roots", Dimension.Overworld, True, False)
    BigDripleaf = _block("big_dripleaf", Dimension.Overworld, True, False)
    SmallDripleafBlock = _block("small_dripleaf_block", Dimension.Overworld, True, False)
    SporeBlossom = _block("spore_blossom", Dimension.Overworld, True, False)
    Azalea = _block("azalea", Dimension.Overworld, True, False)
    FloweringAzalea = _block("flowering_azalea", Dimension.Overworld, True, False)
    GlowLichen = _block("glow_lichen", Dimension.Overworld, True, False)
    AmethystBlock = _block("amethyst_block", Dimension.Overworld, True, False)
    BuddingAmethyst = _block("budding_amethyst", Dimension.Overworld, True, False)
    AmethystCluster = _block("amethyst_cluster", Dimension.Overworld, True, False)
    LargeAmethystBud = _block("large_amethyst_bud",Dimension.Overworld, True, False)
    MediumAmethystBud = _block("medium_amethyst_bud", Dimension.Overworld, True, False)
    SmallAmethystBud = _block("small_amethyst_bud",Dimension.Overworld, True, False)
    Tuff = _block("tuff", Dimension.Overworld, True, False)
    Calcite = _block("calcite", Dimension.Overworld, True, False)
    Porkchop = _block("porkchop", Dimension.Overworld, True, False)
    Mutton = _block("mutton", Dimension.Overworld, True, False)
    Rabbit = _block("rabbit", Dimension.Overworld, True, False)
    Cod = _block("cod", Dimension.Overworld, True, False)
    Salmon = _block("salmon", Dimension.Overworld, True, False)
    TropicalFish = _block("tropical_fish", Dimension.Overworld, True, False)
    Pufferfish = _block("pufferfish", Dimension.Overworld, True, False)
    BrownMushroom = _block("brown_mushroom", Dimension.Overworld, True, False)
    RedMushroom = _block("red_mushroom", Dimension.Overworld, True, False)
    CrimsonFungus = _block("crimson_fungus", Dimension.Nether, True, False)
    WarpedFungus = _block("warped_fungus", Dimension.Nether, True, False)
    BrownMushroomBlock = _block("brown_mushroom_block", Dimension.Overworld, True, False,_state("variant", ["brown_mushroom_block", "mushroom_stem", "mushroom", ]))
    RedMushroomBlock = _block("red_mushroom_block",Dimension.Overworld, True, False)

    SugarCane = _block("sugar_cane", Dimension.Overworld, True, False)
    Sugar = _block("sugar", Dimension.Overworld, True, False)
    RottenFlesh = _block("rotten_flesh", Dimension.Overworld, True, False)
    Web = _block("web", Dimension.Overworld, True, False)
    SpiderEye = _block("spider_eye", Dimension.Overworld, True, False)
    MobSpawner = _block("mob_spawner", Dimension.Nether, True, False)
    MonsterEgg = _block("monster_egg", Dimension.Overworld, True, False,_state("variant", ["infested_stone", "infested_cobblestone", "infested_stone_bricks", "infested_mossy_stone_bricks", "infested_cracked_stone_bricks", "infested_chiseled_stone_bricks", ]))
    InfestedDeepslate = _block("infested_deepslate", Dimension.Overworld, True, False)
    DragonEgg = _block("dragon_egg",Dimension.End,True,False, )
    TurtleEgg = _block("turtle_egg", Dimension.Overworld, True, False)
    FrogSpawn = _block("frog_spawn", Dimension.Overworld, True, False)
    PearlescentFroglight = _block("pearlescent_froglight", Dimension.Overworld, True, False)
    VerdantFroglight = _block("verdant_froglight", Dimension.Overworld, True, False)
    OchreFroglight = _block("ochre_froglight", Dimension.Overworld, True, False)
    ChickenSpawnEgg = _block("chicken_spawn_egg", Dimension.Overworld, True, True)
    BeeSpawnEgg = _block("bee_spawn_egg", Dimension.Overworld, True, True)
    CowSpawnEgg = _block("cow_spawn_egg", Dimension.Overworld, True, True)
    PigSpawnEgg = _block("pig_spawn_egg", Dimension.Overworld, True, True)
    SheepSpawnEgg = _block("sheep_spawn_egg", Dimension.Overworld, True, True)
    WolfSpawnEgg = _block("wolf_spawn_egg", Dimension.Overworld, True, True)
    PolarBearSpawnEgg = _block("polar_bear_spawn_egg", Dimension.Overworld, True, True)
    OcelotSpawnEgg = _block("ocelot_spawn_egg", Dimension.Overworld, True, True)
    CatSpawnEgg = _block("cat_spawn_egg", Dimension.Overworld, True, True)
    MooshroomSpawnEgg = _block("mooshroom_spawn_egg", Dimension.Overworld, True, True)
    BatSpawnEgg = _block("bat_spawn_egg", Dimension.Overworld, True, True)
    ParrotSpawnEgg = _block("parrot_spawn_egg", Dimension.Overworld, True, True)
    RabbitSpawnEgg = _block("rabbit_spawn_egg", Dimension.Overworld, True, True)
    LlamaSpawnEgg = _block("llama_spawn_egg", Dimension.Overworld, True, True)
    HorseSpawnEgg = _block("horse_spawn_egg", Dimension.Overworld, True, True)
    DonkeySpawnEgg = _block("donkey_spawn_egg", Dimension.Overworld, True, True)
    MuleSpawnEgg = _block("mule_spawn_egg", Dimension.Overworld, True, True)
    SkeletonHorseSpawnEgg = _block("skeleton_horse_spawn_egg", Dimension.Overworld, True, True)
    ZombieHorseSpawnEgg = _block("zombie_horse_spawn_egg", Dimension.Overworld, True, True)
    TropicalFishSpawnEgg = _block("tropical_fish_spawn_egg", Dimension.Overworld, True, True)
    CodSpawnEgg = _block("cod_spawn_egg", Dimension.Overworld, True, True)
    PufferfishSpawnEgg = _block("pufferfish_spawn_egg", Dimension.Overworld, True, True)
    SalmonSpawnEgg = _block("salmon_spawn_egg", Dimension.Overworld, True, True)
    DolphinSpawnEgg = _block("dolphin_spawn_egg", Dimension.Overworld, True, True)
    TurtleSpawnEgg = _block("turtle_spawn_egg", Dimension.Overworld, True, True)
    PandaSpawnEgg = _block("panda_spawn_egg", Dimension.Overworld, True, True)
    FoxSpawnEgg = _block("fox_spawn_egg", Dimension.Overworld, True, True)
    CreeperSpawnEgg = _block("creeper_spawn_egg", Dimension.Overworld, True, True)
    EndermanSpawnEgg = _block("enderman_spawn_egg",Dimension.End,True,True, )
    SilverfishSpawnEgg = _block("silverfish_spawn_egg", Dimension.Overworld, True, True)
    SkeletonSpawnEgg = _block("skeleton_spawn_egg",Dimension.Overworld, True, True)
    WitherSkeletonSpawnEgg = _block("wither_skeleton_spawn_egg", Dimension.Overworld, True, True)
    StraySpawnEgg = _block("stray_spawn_egg", Dimension.Overworld, True, True)
    SlimeSpawnEgg = _block("slime_spawn_egg", Dimension.Overworld, True, True)
    SpiderSpawnEgg = _block("spider_spawn_egg", Dimension.Overworld, True, True)
    ZombieSpawnEgg = _block("zombie_spawn_egg", Dimension.Overworld, True, True)
    ZombiePigmanSpawnEgg = _block("zombie_pigman_spawn_egg", Dimension.Overworld, True, True)
    HuskSpawnEgg = _block("husk_spawn_egg", Dimension.Overworld, True, True)
    DrownedSpawnEgg = _block("drowned_spawn_egg", Dimension.Overworld, True, True)
    SquidSpawnEgg = _block("squid_spawn_egg", Dimension.Overworld, True, True)
    GlowSquidSpawnEgg = _block("glow_squid_spawn_egg", Dimension.Overworld, True, True)
    CaveSpiderSpawnEgg = _block("cave_spider_spawn_egg", Dimension.Overworld, True, True)
    WitchSpawnEgg = _block("witch_spawn_egg", Dimension.Overworld, True, True)
    GuardianSpawnEgg = _block("guardian_spawn_egg",Dimension.Overworld, True, True)
    ElderGuardianSpawnEgg = _block("elder_guardian_spawn_egg", Dimension.Overworld, True, True)
    EndermiteSpawnEgg = _block("endermite_spawn_egg",Dimension.End,True,True, )
    MagmaCubeSpawnEgg = _block("magma_cube_spawn_egg", Dimension.Nether, True, True)
    StriderSpawnEgg = _block("strider_spawn_egg", Dimension.Overworld, True, True)
    HoglinSpawnEgg = _block("hoglin_spawn_egg", Dimension.Overworld, True, True)
    PiglinSpawnEgg = _block("piglin_spawn_egg", Dimension.Overworld, True, True)
    ZoglinSpawnEgg = _block("zoglin_spawn_egg", Dimension.Overworld, True, True)
    PiglinBruteSpawnEgg = _block("piglin_brute_spawn_egg", Dimension.Overworld, True, True)
    GoatSpawnEgg = _block("goat_spawn_egg", Dimension.Overworld, True, True)
    AxolotlSpawnEgg = _block("axolotl_spawn_egg", Dimension.Overworld, True, True)
    WardenSpawnEgg = _block("warden_spawn_egg", Dimension.Overworld, True, True)
    AllaySpawnEgg = _block("allay_spawn_egg", Dimension.Overworld, True, True)
    FrogSpawnEgg = _block("frog_spawn_egg", Dimension.Overworld, True, True)
    TadpoleSpawnEgg = _block("tadpole_spawn_egg", Dimension.Overworld, True, True)
    GhastSpawnEgg = _block("ghast_spawn_egg", Dimension.Overworld, True, True)
    BlazeSpawnEgg = _block("blaze_spawn_egg", Dimension.Overworld, True, True)
    ShulkerSpawnEgg = _block("shulker_spawn_egg", Dimension.Overworld, True, True)
    VindicatorSpawnEgg = _block("vindicator_spawn_egg", Dimension.Overworld, True, True)
    EvokerSpawnEgg = _block("evoker_spawn_egg", Dimension.Overworld, True, True)
    VexSpawnEgg = _block("vex_spawn_egg", Dimension.Overworld, True, True)
    VillagerSpawnEgg = _block("villager_spawn_egg",Dimension.Overworld, True, True)
    WanderingTraderSpawnEgg = _block("wandering_trader_spawn_egg", Dimension.Overworld, True, True)
    ZombieVillagerSpawnEgg = _block("zombie_villager_spawn_egg", Dimension.Overworld, True, True)
    PhantomSpawnEgg = _block("phantom_spawn_egg", Dimension.Overworld, True, True)
    PillagerSpawnEgg = _block("pillager_spawn_egg",Dimension.Overworld, True, True)
    RavagerSpawnEgg = _block("ravager_spawn_egg", Dimension.Overworld, True, True)
    Obsidian = _block("obsidian", Dimension.Overworld, True, False)
    CryingObsidian = _block("crying_obsidian", Dimension.Nether, True, False)
    Bedrock = _block("bedrock", Dimension.Overworld, True, False)
    SoulSand = _block("soul_sand", Dimension.Nether, True, False)
    Netherrack = _block("netherrack", Dimension.Nether, True, False)
    Magma = _block("magma", Dimension.Nether, True, False)
    NetherWart = _block("nether_wart", Dimension.Nether, True, False)
    EndStone = _block("end_stone",Dimension.End,True,False, )
    ChorusFlower = _block("chorus_flower",Dimension.End,True,False, )
    ChorusPlant = _block("chorus_plant",Dimension.End,True,False, )
    ChorusFruit = _block("chorus_fruit",Dimension.End,True,False, )
    PoppedChorusFruit = _block("popped_chorus_fruit",Dimension.End,True,False, )
    Sponge = _block("sponge", Dimension.Overworld, True, False,_state("variant", ["sponge", "wet_sponge", ]))
    CoralBlock = _block("coral_block", Dimension.Overworld, True, False,_state("variant", ["tube_coral_block", "brain_coral_block", "bubble_coral_block", "fire_coral_block", "horn_coral_block", "dead_tube_coral_block", "dead_brain_coral_block", "dead_bubble_coral_block", "dead_fire_coral_block", "dead_horn_coral_block", ]))
    Sculk = _block("sculk", Dimension.Overworld, True, False)
    SculkVein = _block("sculk_vein", Dimension.Overworld, True, False)
    SculkCatalyst = _block("sculk_catalyst", Dimension.Overworld, True, False)
    SculkShrieker = _block("sculk_shrieker", Dimension.Overworld, True, False)
    SculkSensor = _block("sculk_sensor", Dimension.Overworld, True, False)
    ReinforcedDeepslate = _block("reinforced_deepslate", Dimension.Overworld, True, False)
    LeatherHelmet = _block("leather_helmet", Dimension.Overworld, True, False)
    ChainmailHelmet = _block("chainmail_helmet", Dimension.Overworld, True, False)
    IronHelmet = _block("iron_helmet", Dimension.Overworld, True, False)
    GoldenHelmet = _block("golden_helmet", Dimension.Overworld, True, False)
    DiamondHelmet = _block("diamond_helmet", Dimension.Overworld, True, False)
    NetheriteHelmet = _block("netherite_helmet", Dimension.Nether, True, False)
    LeatherChestplate = _block("leather_chestplate", Dimension.Overworld, True, False)
    ChainmailChestplate = _block("chainmail_chestplate", Dimension.Overworld, True, False)
    IronChestplate = _block("iron_chestplate", Dimension.Overworld, True, False)
    GoldenChestplate = _block("golden_chestplate", Dimension.Overworld, True, False)
    DiamondChestplate = _block("diamond_chestplate", Dimension.Overworld, True, False)
    NetheriteChestplate = _block("netherite_chestplate", Dimension.Nether, True, False)
    LeatherLeggings = _block("leather_leggings", Dimension.Overworld, True, False)
    ChainmailLeggings = _block("chainmail_leggings", Dimension.Overworld, True, False)
    IronLeggings = _block("iron_leggings", Dimension.Overworld, True, False)
    GoldenLeggings = _block("golden_leggings", Dimension.Overworld, True, False)
    DiamondLeggings = _block("diamond_leggings", Dimension.Overworld, True, False)
    NetheriteLeggings = _block("netherite_leggings", Dimension.Nether, True, False)
    LeatherBoots = _block("leather_boots", Dimension.Overworld, True, False)
    ChainmailBoots = _block("chainmail_boots", Dimension.Overworld, True, False)
    IronBoots = _block("iron_boots", Dimension.Overworld, True, False)
    GoldenBoots = _block("golden_boots", Dimension.Overworld, True, False)
    DiamondBoots = _block("diamond_boots", Dimension.Overworld, True, False)
    NetheriteBoots = _block("netherite_boots", Dimension.Nether, True, False)
    WoodenSword = _block("wooden_sword", Dimension.Overworld, True, False)
    StoneSword = _block("stone_sword", Dimension.Overworld, True, False)
    IronSword = _block("iron_sword", Dimension.Overworld, True, False)
    GoldenSword = _block("golden_sword", Dimension.Overworld, True, False)
    DiamondSword = _block("diamond_sword", Dimension.Overworld, True, False)
    NetheriteSword = _block("netherite_sword", Dimension.Nether, True, False)
    WoodenAxe = _block("wooden_axe", Dimension.Overworld, True, False)
    StoneAxe = _block("stone_axe", Dimension.Overworld, True, False)
    IronAxe = _block("iron_axe", Dimension.Overworld, True, False)
    GoldenAxe = _block("golden_axe", Dimension.Overworld, True, False)
    DiamondAxe = _block("diamond_axe", Dimension.Overworld, True, False)
    NetheriteAxe = _block("netherite_axe", Dimension.Nether, True, False)
    WoodenPickaxe = _block("wooden_pickaxe", Dimension.Overworld, True, False)
    StonePickaxe = _block("stone_pickaxe", Dimension.Overworld, True, False)
    IronPickaxe = _block("iron_pickaxe", Dimension.Overworld, True, False)
    GoldenPickaxe = _block("golden_pickaxe", Dimension.Overworld, True, False)
    DiamondPickaxe = _block("diamond_pickaxe", Dimension.Overworld, True, False)
    NetheritePickaxe = _block("netherite_pickaxe", Dimension.Nether, True, False)
    WoodenShovel = _block("wooden_shovel", Dimension.Overworld, True, False)
    StoneShovel = _block("stone_shovel", Dimension.Overworld, True, False)
    IronShovel = _block("iron_shovel", Dimension.Overworld, True, False)
    GoldenShovel = _block("golden_shovel", Dimension.Overworld, True, False)
    DiamondShovel = _block("diamond_shovel", Dimension.Overworld, True, False)
    NetheriteShovel = _block("netherite_shovel", Dimension.Nether, True, False)
    WoodenHoe = _block("wooden_hoe", Dimension.Overworld, True, False)
    StoneHoe = _block("stone_hoe", Dimension.Overworld, True, False)
    IronHoe = _block("iron_hoe", Dimension.Overworld, True, False)
    GoldenHoe = _block("golden_hoe", Dimension.Overworld, True, False)
    DiamondHoe = _block("diamond_hoe", Dimension.Overworld, True, False)
    NetheriteHoe = _block("netherite_hoe", Dimension.Nether, True, False)
    Bow = _block("bow", Dimension.Overworld, True, False)
    Crossbow = _block("crossbow", Dimension.Overworld, True, False)
    Arrow = _block("arrow", Dimension.Overworld, True, False,_state("variant", ["arrow", "night_vision_arrow_0_22", "night_vision_arrow_1", "invisibility_arrow_0_22", "invisibility_arrow_1", "leaping_arrow_0_22", "leaping_arrow_1", "leaping_2_arrow_1", "fire_resistance_arrow_0_22", "fire_resistance_arrow_1", "speed_arrow_0_22", "speed_arrow_1", "speed_2_arrow_1", "slowness_arrow_0_22", "slowness_arrow_1", "water_breathing_arrow_0_22", "water_breathing_arrow_1", "healing_arrow_1", "healing_arrow_2", "harming_arrow_1", "harming_arrow_2", "poison_arrow_0_05", "poison_arrow_0_15", "poison_2_arrow_0_02", "regeneration_arrow_0_05", "regeneration_arrow_0_15", "regeneration_2_arrow_0_02", "strength_arrow_0_22", "strength_arrow_1", "strength_2_arrow_0_11", "weakness_arrow_0_11", "weakness_arrow_0_30", "decay_arrow_0_05", "turtle_master_arrow_0_02", "turtle_master_arrow_0_05", "turtle_master_2_arrow_0_02", "slow_falling_arrow_0_11", "slow_falling_arrow_0_30", "slowness_arrow_0_02", ]))
    Shield = _block("shield", Dimension.Overworld, True, False)
    CookedPorkchop = _block("cooked_porkchop", Dimension.Overworld, True, False)
    CookedMutton = _block("cooked_mutton", Dimension.Overworld, True, False)
    CookedRabbit = _block("cooked_rabbit", Dimension.Overworld, True, False)
    CookedCod = _block("cooked_cod", Dimension.Overworld, True, False)
    CookedSalmon = _block("cooked_salmon", Dimension.Overworld, True, False)
    Bread = _block("bread", Dimension.Overworld, True, False)
    MushroomStew = _block("mushroom_stew", Dimension.Overworld, True, False)
    BeetrootSoup = _block("beetroot_soup", Dimension.Overworld, True, False)
    RabbitStew = _block("rabbit_stew", Dimension.Overworld, True, False)
    BakedPotato = _block("baked_potato", Dimension.Overworld, True, False)
    Cookie = _block("cookie", Dimension.Overworld, True, False)
    PumpkinPie = _block("pumpkin_pie", Dimension.Overworld, True, False)
    Cake = _block("cake", Dimension.Overworld, True, False)
    DriedKelp = _block("dried_kelp", Dimension.Overworld, True, False)
    FishingRod = _block("fishing_rod", Dimension.Overworld, True, False)
    CarrotOnAStick = _block("carrot_on_a_stick",Dimension.Overworld, True, False)
    WarpedFungusOnAStick = _block("warped_fungus_on_a_stick", Dimension.Nether, True, False)
    Snowball = _block("snowball", Dimension.Overworld, True, False)
    Shears = _block("shears", Dimension.Overworld, True, False)
    FlintAndSteel = _block("flint_and_steel", Dimension.Overworld, True, False)
    Lead = _block("lead", Dimension.Overworld, True, False)
    Clock = _block("clock", Dimension.Overworld, True, False)
    Compass = _block("compass", Dimension.Overworld, True, False)
    RecoveryCompass = _block("recovery_compass", Dimension.Overworld, True, False)
    EmptyMap = _block("empty_map", Dimension.Overworld, True, False,_state("variant", ["map", "locator_map", ]))
    Saddle = _block("saddle", Dimension.Overworld, True, False)
    GoatHorn = _block("goat_horn", Dimension.Overworld, True, False,_state("variant", ["goat_horn_ponder", "goat_horn_sing", "goat_horn_seek", "goat_horn_feel", "goat_horn_admire", "goat_horn_call", "goat_horn_yearn", "goat_horn_resist", ]))
    LeatherHorseArmor = _block("leather_horse_armor", Dimension.Overworld, True, False)
    IronHorseArmor = _block("iron_horse_armor", Dimension.Overworld, True, False)
    GoldenHorseArmor = _block("golden_horse_armor",Dimension.Overworld, True, False)
    DiamondHorseArmor = _block("diamond_horse_armor", Dimension.Overworld, True, False)
    Trident = _block("trident", Dimension.Overworld, True, False)
    TurtleHelmet = _block("turtle_helmet", Dimension.Overworld, True, False)
    Elytra = _block("elytra", Dimension.Overworld, True, False)
    TotemOfUndying = _block("totem_of_undying", Dimension.Overworld, True, False)
    GlassBottle = _block("glass_bottle", Dimension.Overworld, True, False)
    ExperienceBottle = _block("experience_bottle", Dimension.Overworld, True, False)
    Potion = _block("potion", Dimension.Overworld, True, False,_state("variant", ["water_bottle", "mundane_potion", "long_mundane_potion", "thick_potion", "awkward_potion", "night_vision_potion_3", "night_vision_potion_8", "invisibility_potion_3", "invisibility_potion_8", "leaping_potion_3", "leaping_potion_8", "leaping_potion_1_3", "fire_resistance_potion_3", "fire_resistance_potion_8", "swiftness_potion_3", "swiftness_potion_8", "swiftness_potion_1_3", "slowness_potion_1_3", "slowness_potion_4", "water_breathing_potion_3", "water_breathing_potion_8", "healing_potion_1", "healing_potion_2", "harming_potion_1", "harming_potion_2", "poison_potion_0_45", "poison_potion_2", "poison_potion_0_22", "regeneration_potion_0_45", "regeneration_potion_2", "regeneration_potion_0_22", "strength_potion_3", "strength_potion_8", "strength_potion_1_3", "weakness_potion_1_3", "weakness_potion_4", "decay_potion", "turtle_master_potion_0_2", "turtle_master_potion_0_4", "turtle_master_2_potion_0_2", "slow_falling_potion_1_3", "slow_falling_potion_4", "slowness_potion_0_2", ]))
    SplashPotion = _block("splash_potion", Dimension.Overworld, True, False,_state("variant", ["splash_water_bottle", "splash_mundane_potion", "splash_long_mundane_potion", "splash_thick_potion", "splash_awkward_potion", "splash_night_vision_potion_3", "splash_night_vision_potion_8", "splash_invisibility_potion_3", "splash_invisibility_potion_8", "splash_leaping_potion_3", "splash_leaping_potion_8", "splash_leaping_potion_1_3", "splash_fire_resistance_potion_3", "splash_fire_resistance_potion_8", "splash_swiftness_potion_3", "splash_swiftness_potion_8", "splash_swiftness_potion_1_3", "splash_slowness_potion_1_3", "splash_slowness_potion_4", "splash_water_breathing_potion_3", "splash_water_breathing_potion_8", "splash_healing_potion_1", "splash_healing_potion_2", "splash_harming_potion_1", "splash_harming_potion_2", "splash_poison_potion_0_45", "splash_poison_potion_2", "splash_poison_potion_0_22", "splash_regeneration_potion_0_45", "splash_regeneration_potion_2", "splash_regeneration_potion_0_22", "splash_strength_potion_3", "splash_strength_potion_8", "splash_strength_potion_1_3", "splash_weakness_potion_1_3", "splash_weakness_potion_4", "splash_decay_potion", "splash_turtle_master_potion_0_2", "splash_turtle_master_potion_0_4", "splash_turtle_master_2_potion_0_2", "splash_slow_falling_potion_1_3", "splash_slow_falling_potion_4", "splash_slowness_potion_0_2", ]))
    LingeringPotion = _block("lingering_potion", Dimension.Overworld, True, False,_state("variant", ["lingering_water_bottle", "lingering_mundane_potion", "lingering_long_mundane_potion", "lingering_thick_potion", "lingering_awkward_potion", "lingering_night_vision_potion_3", "lingering_night_vision_potion_8", "lingering_invisibility_potion_3", "lingering_invisibility_potion_8", "lingering_leaping_potion_3", "lingering_leaping_potion_8", "lingering_leaping_potion_1_3", "lingering_fire_resistance_potion_3", "lingering_fire_resistance_potion_8", "lingering_swiftness_potion_3", "lingering_swiftness_potion_8", "lingering_swiftness_potion_1_3", "lingering_slowness_potion_1_3", "lingering_slowness_potion_4", "lingering_water_breathing_potion_3", "lingering_water_breathing_potion_8", "lingering_healing_potion_1", "lingering_healing_potion_2", "lingering_harming_potion_1", "lingering_harming_potion_2", "lingering_poison_potion_0_45", "lingering_poison_potion_2", "lingering_poison_potion_0_22", "lingering_regeneration_potion_0_45", "lingering_regeneration_potion_2", "lingering_regeneration_potion_0_22", "lingering_strength_potion_3", "lingering_strength_potion_8", "lingering_strength_potion_1_3", "lingering_weakness_potion_1_3", "lingering_weakness_potion_4", "lingering_decay_potion", "lingering_turtle_master_potion_0_2", "lingering_turtle_master_potion_0_4", "lingering_turtle_master_2_potion_0_2", "lingering_slow_falling_potion_1_3", "lingering_slow_falling_potion_4", "lingering_slowness_potion_0_2", ]))
    Spyglass = _block("spyglass", Dimension.Overworld, True, False)
    Stick = _block("stick", Dimension.Overworld, True, False)
    Bed = _block("bed", Dimension.Overworld, True, False,_state("variant", ["white_bed", "light_gray_bed", "gray_bed", "black_bed", "brown_bed", "red_bed", "orange_bed", "yellow_bed", "lime_bed", "green_bed", "cyan_bed", "light_blue_bed", "blue_bed", "purple_bed", "magenta_bed", "pink_bed", ]))
    Torch = _block("torch", Dimension.Overworld, True, False)
    SoulTorch = _block("soul_torch", Dimension.Nether, True, False)
    SeaPickle = _block("sea_pickle", Dimension.Overworld, True, False)
    Lantern = _block("lantern", Dimension.Overworld, True, False)
    SoulLantern = _block("soul_lantern", Dimension.Nether, True, False)
    Candle = _block("candle", Dimension.Overworld, True, False)
    WhiteCandle = _block("white_candle", Dimension.Overworld, True, False)
    OrangeCandle = _block("orange_candle", Dimension.Overworld, True, False)
    MagentaCandle = _block("magenta_candle", Dimension.Overworld, True, False)
    LightBlueCandle = _block("light_blue_candle", Dimension.Overworld, True, False)
    YellowCandle = _block("yellow_candle", Dimension.Overworld, True, False)
    LimeCandle = _block("lime_candle", Dimension.Overworld, True, False)
    PinkCandle = _block("pink_candle", Dimension.Overworld, True, False)
    GrayCandle = _block("gray_candle", Dimension.Overworld, True, False)
    LightGrayCandle = _block("light_gray_candle", Dimension.Overworld, True, False)
    CyanCandle = _block("cyan_candle", Dimension.Overworld, True, False)
    PurpleCandle = _block("purple_candle", Dimension.Overworld, True, False)
    BlueCandle = _block("blue_candle", Dimension.Overworld, True, False)
    BrownCandle = _block("brown_candle", Dimension.Overworld, True, False)
    GreenCandle = _block("green_candle", Dimension.Overworld, True, False)
    RedCandle = _block("red_candle", Dimension.Overworld, True, False)
    BlackCandle = _block("black_candle", Dimension.Overworld, True, False)
    CraftingTable = _block("crafting_table", Dimension.Overworld, True, False)
    CartographyTable = _block("cartography_table", Dimension.Overworld, True, False)
    FletchingTable = _block("fletching_table", Dimension.Overworld, True, False)
    SmithingTable = _block("smithing_table", Dimension.Overworld, True, False)
    Beehive = _block("beehive", Dimension.Overworld, True, False)
    Campfire = _block("campfire", Dimension.Overworld, True, False)
    SoulCampfire = _block("soul_campfire", Dimension.Nether, True, False)
    Furnace = _block("furnace", Dimension.Overworld, True, False)
    BlastFurnace = _block("blast_furnace", Dimension.Overworld, True, False)
    Smoker = _block("smoker", Dimension.Overworld, True, False)
    RespawnAnchor = _block("respawn_anchor", Dimension.Nether, True, False)
    BrewingStand = _block("brewing_stand", Dimension.Overworld, True, False)
    Anvil = _block("anvil", Dimension.Overworld, True, False,_state("variant", ["anvil", "slighlty_damaged_anvil", "very_damaged_anvil", ]))
    Grindstone = _block("grindstone", Dimension.Overworld, True, False)
    EnchantingTable = _block("enchanting_table", Dimension.Overworld, True, False)
    Bookshelf = _block("bookshelf", Dimension.Overworld, True, False)
    Lectern = _block("lectern", Dimension.Overworld, True, False)
    Cauldron = _block("cauldron", Dimension.Overworld, True, False)
    Composter = _block("composter", Dimension.Overworld, True, False)
    Chest = _block("chest", Dimension.Overworld, True, False)
    TrappedChest = _block("trapped_chest", Dimension.Overworld, True, False)
    EnderChest = _block("ender_chest",Dimension.End,True,False, )
    Barrel = _block("barrel", Dimension.Overworld, True, False)
    UndyedShulkerBox = _block("undyed_shulker_box",Dimension.Overworld, True, False)
    ShulkerBox = _block("shulker_box", Dimension.Overworld, True, False,_state("variant", ["white_shulker_box", "gray_shulker_box", "light_gray_shulker_box", "black_shulker_box", "brown_shulker_box", "red_shulker_box", "orange_shulker_box", "yellow_shulker_box", "lime_shulker_box", "green_shulker_box", "cyan_shulker_box", "light_blue_shulker_box", "blue_shulker_box", "purple_shulker_box", "magenta_shulker_box", "pink_shulker_box", ]))
    ArmorStand = _block("armor_stand", Dimension.Overworld, True, False)
    Noteblock = _block("noteblock", Dimension.Overworld, True, False)
    Jukebox = _block("jukebox", Dimension.Overworld, True, False)
    MusicDisc13 = _block("music_disc_13", Dimension.Overworld, True, False)
    MusicDiscCat = _block("music_disc_cat", Dimension.Overworld, True, False)
    MusicDiscBlocks = _block("music_disc_blocks", Dimension.Overworld, True, False)
    MusicDiscChirp = _block("music_disc_chirp", Dimension.Overworld, True, False)
    MusicDiscFar = _block("music_disc_far", Dimension.Overworld, True, False)
    MusicDiscMall = _block("music_disc_mall", Dimension.Overworld, True, False)
    MusicDiscMellohi = _block("music_disc_mellohi",Dimension.Overworld, True, False)
    MusicDiscStal = _block("music_disc_stal", Dimension.Overworld, True, False)
    MusicDiscStrad = _block("music_disc_strad", Dimension.Overworld, True, False)
    MusicDiscWard = _block("music_disc_ward", Dimension.Overworld, True, False)
    MusicDisc11 = _block("music_disc_11", Dimension.Overworld, True, False)
    MusicDiscWait = _block("music_disc_wait", Dimension.Overworld, True, False)
    MusicDiscOtherside = _block("music_disc_otherside", Dimension.Overworld, True, False)
    MusicDisc5 = _block("music_disc_5", Dimension.Overworld, True, False)
    MusicDiscPigstep = _block("music_disc_pigstep",Dimension.Overworld, True, False)
    DiscFragment5 = _block("disc_fragment_5", Dimension.Overworld, True, False)
    GlowstoneDust = _block("glowstone_dust", Dimension.Nether, True, False)
    Glowstone = _block("glowstone", Dimension.Nether, True, False)
    RedstoneLamp = _block("redstone_lamp", Dimension.Overworld, True, False)
    SeaLantern = _block("sea_lantern", Dimension.Overworld, True, False)
    OakSign = _block("oak_sign", Dimension.Overworld, True, False)
    SpruceSign = _block("spruce_sign", Dimension.Overworld, True, False)
    BirchSign = _block("birch_sign", Dimension.Overworld, True, False)
    JungleSign = _block("jungle_sign", Dimension.Overworld, True, False)
    AcaciaSign = _block("acacia_sign", Dimension.Overworld, True, False)
    DarkOakSign = _block("dark_oak_sign", Dimension.Overworld, True, False)
    MangroveSign = _block("mangrove_sign", Dimension.Overworld, True, False)
    CrimsonSign = _block("crimson_sign", Dimension.Nether, True, False)
    WarpedSign = _block("warped_sign", Dimension.Nether, True, False)
    Painting = _block("painting", Dimension.Overworld, True, False)
    Frame = _block("frame", Dimension.Overworld, True, False)
    GlowFrame = _block("glow_frame", Dimension.Overworld, True, False)
    HoneyBottle = _block("honey_bottle", Dimension.Overworld, True, False)
    FlowerPot = _block("flower_pot", Dimension.Overworld, True, False)
    Bowl = _block("bowl", Dimension.Overworld, True, False)
    Bucket = _block("bucket", Dimension.Overworld, True, False)
    MilkBucket = _block("milk_bucket", Dimension.Overworld, True, False)
    WaterBucket = _block("water_bucket", Dimension.Overworld, True, False)
    LavaBucket = _block("lava_bucket", Dimension.Overworld, True, False)
    CodBucket = _block("cod_bucket", Dimension.Overworld, True, False)
    SalmonBucket = _block("salmon_bucket", Dimension.Overworld, True, False)
    TropicalFishBucket = _block("tropical_fish_bucket", Dimension.Overworld, True, False)
    PufferfishBucket = _block("pufferfish_bucket", Dimension.Overworld, True, False)
    PowderSnowBucket = _block("powder_snow_bucket",Dimension.Overworld, True, False)
    AxolotlBucket = _block("axolotl_bucket", Dimension.Overworld, True, False)
    TadpoleBucket = _block("tadpole_bucket", Dimension.Overworld, True, False)
    Skull = _block("skull", Dimension.Overworld, True, False,_state("variant", ["player_head", "zombie_head", "creeper_head", "dragon_head", "skeleton_skull", "wither_skeleton_skull"]))
    Beacon = _block("beacon", Dimension.Overworld, True, False)
    Bell = _block("bell", Dimension.Overworld, True, False)
    Conduit = _block("conduit", Dimension.Overworld, True, False)
    StonecutterBlock = _block("stonecutter_block", Dimension.Overworld, True, False)
    EndPortalFrame = _block("end_portal_frame",Dimension.End,True,False, )
    Coal = _block("coal", Dimension.Overworld, True, False)
    Charcoal = _block("charcoal", Dimension.Overworld, True, False)
    Diamond = _block("diamond", Dimension.Overworld, True, False)
    IronNugget = _block("iron_nugget", Dimension.Overworld, True, False)
    RawIron = _block("raw_iron", Dimension.Overworld, True, False)
    RawGold = _block("raw_gold", Dimension.Overworld, True, False)
    RawCopper = _block("raw_copper", Dimension.Overworld, True, False)
    CopperIngot = _block("copper_ingot", Dimension.Overworld, True, False)
    IronIngot = _block("iron_ingot", Dimension.Overworld, True, False)
    NetheriteScrap = _block("netherite_scrap", Dimension.Nether, True, False)
    NetheriteIngot = _block("netherite_ingot", Dimension.Nether, True, False)
    GoldNugget = _block("gold_nugget", Dimension.Overworld, True, False)
    GoldIngot = _block("gold_ingot", Dimension.Overworld, True, False)
    Emerald = _block("emerald", Dimension.Overworld, True, False)
    Quartz = _block("quartz", Dimension.Nether, True, False)
    ClayBall = _block("clay_ball", Dimension.Overworld, True, False)
    Brick = _block("brick", Dimension.Overworld, True, False)
    Netherbrick = _block("netherbrick", Dimension.Nether, True, False)
    PrismarineShard = _block("prismarine_shard", Dimension.Overworld, True, False)
    AmethystShard = _block("amethyst_shard", Dimension.Overworld, True, False)
    PrismarineCrystals = _block("prismarine_crystals", Dimension.Overworld, True, False)
    NautilusShell = _block("nautilus_shell", Dimension.Overworld, True, False)
    HeartOfTheSea = _block("heart_of_the_sea", Dimension.Overworld, True, False)
    Scute = _block("scute", Dimension.Overworld, True, False)
    PhantomMembrane = _block("phantom_membrane", Dimension.Overworld, True, False)
    String = _block("string", Dimension.Overworld, True, False)
    Feather = _block("feather", Dimension.Overworld, True, False)
    Flint = _block("flint", Dimension.Overworld, True, False)
    Gunpowder = _block("gunpowder", Dimension.Overworld, True, False)
    Leather = _block("leather", Dimension.Overworld, True, False)
    RabbitHide = _block("rabbit_hide", Dimension.Overworld, True, False)
    RabbitFoot = _block("rabbit_foot", Dimension.Overworld, True, False)
    FireCharge = _block("fire_charge", Dimension.Overworld, True, False)
    BlazeRod = _block("blaze_rod", Dimension.Overworld, True, False)
    BlazePowder = _block("blaze_powder", Dimension.Overworld, True, False)
    MagmaCream = _block("magma_cream", Dimension.Nether, True, False)
    FermentedSpiderEye = _block("fermented_spider_eye", Dimension.Overworld, True, False)
    EchoShard = _block("echo_shard", Dimension.Overworld, True, False)
    DragonBreath = _block("dragon_breath",Dimension.End,True,False, )
    ShulkerShell = _block("shulker_shell", Dimension.Overworld, True, False)
    GhastTear = _block("ghast_tear", Dimension.Overworld, True, False)
    SlimeBall = _block("slime_ball", Dimension.Overworld, True, False)
    EnderPearl = _block("ender_pearl",Dimension.End,True,False, )
    EnderEye = _block("ender_eye",Dimension.End,True,False, )
    NetherStar = _block("nether_star", Dimension.Nether, True, False)
    EndRod = _block("end_rod",Dimension.End,True,False, )
    LightningRod = _block("lightning_rod", Dimension.Overworld, True, False)
    EndCrystal = _block("end_crystal",Dimension.End,True,False, )
    Paper = _block("paper", Dimension.Overworld, True, False)
    Book = _block("book", Dimension.Overworld, True, False)
    WritableBook = _block("writable_book", Dimension.Overworld, True, False)
    WrittenBook = _block("written_book", Dimension.Overworld, True, False)
    EnchantedBook = _block("enchanted_book", Dimension.Overworld, True, False)
    OakBoat = _block("oak_boat", Dimension.Overworld, True, False)
    SpruceBoat = _block("spruce_boat", Dimension.Overworld, True, False)
    BirchBoat = _block("birch_boat", Dimension.Overworld, True, False)
    JungleBoat = _block("jungle_boat", Dimension.Overworld, True, False)
    AcaciaBoat = _block("acacia_boat", Dimension.Overworld, True, False)
    DarkOakBoat = _block("dark_oak_boat", Dimension.Overworld, True, False)
    MangroveBoat = _block("mangrove_boat", Dimension.Overworld, True, False)
    OakChestBoat = _block("oak_chest_boat", Dimension.Overworld, True, False)
    SpruceChestBoat = _block("spruce_chest_boat", Dimension.Overworld, True, False)
    BirchChestBoat = _block("birch_chest_boat", Dimension.Overworld, True, False)
    JungleChestBoat = _block("jungle_chest_boat", Dimension.Overworld, True, False)
    AcaciaChestBoat = _block("acacia_chest_boat", Dimension.Overworld, True, False)
    DarkOakChestBoat = _block("dark_oak_chest_boat",Dimension.Overworld, True, False)
    MangroveChestBoat = _block("mangrove_chest_boat", Dimension.Overworld, True, False)
    Rail = _block("rail", Dimension.Overworld, True, False)
    GoldenRail = _block("golden_rail", Dimension.Overworld, True, False)
    DetectorRail = _block("detector_rail", Dimension.Overworld, True, False)
    ActivatorRail = _block("activator_rail", Dimension.Overworld, True, False)
    Minecart = _block("minecart", Dimension.Overworld, True, False)
    ChestMinecart = _block("chest_minecart", Dimension.Overworld, True, False)
    HopperMinecart = _block("hopper_minecart", Dimension.Overworld, True, False)
    TntMinecart = _block("tnt_minecart", Dimension.Overworld, True, False)
    RedstoneBlock = _block("redstone_block", Dimension.Overworld, True, False)
    RedstoneTorch = _block("redstone_torch", Dimension.Overworld, True, False)
    Lever = _block("lever", Dimension.Overworld, True, False)
    WoodenButton = _block("wooden_button", Dimension.Overworld, True, False)
    SpruceButton = _block("spruce_button", Dimension.Overworld, True, False)
    BirchButton = _block("birch_button", Dimension.Overworld, True, False)
    JungleButton = _block("jungle_button", Dimension.Overworld, True, False)
    AcaciaButton = _block("acacia_button", Dimension.Overworld, True, False)
    DarkOakButton = _block("dark_oak_button", Dimension.Overworld, True, False)
    MangroveButton = _block("mangrove_button", Dimension.Overworld, True, False)
    StoneButton = _block("stone_button", Dimension.Overworld, True, False)
    CrimsonButton = _block("crimson_button", Dimension.Nether, True, False)
    WarpedButton = _block("warped_button", Dimension.Nether, True, False)
    PolishedBlackstoneButton = _block("polished_blackstone_button", Dimension.Nether, True, False)
    TripwireHook = _block("tripwire_hook", Dimension.Overworld, True, False)
    WoodenPressurePlate = _block("wooden_pressure_plate", Dimension.Overworld, True, False)
    SprucePressurePlate = _block("spruce_pressure_plate", Dimension.Overworld, True, False)
    BirchPressurePlate = _block("birch_pressure_plate", Dimension.Overworld, True, False)
    JunglePressurePlate = _block("jungle_pressure_plate", Dimension.Overworld, True, False)
    AcaciaPressurePlate = _block("acacia_pressure_plate", Dimension.Overworld, True, False)
    DarkOakPressurePlate = _block("dark_oak_pressure_plate", Dimension.Overworld, True, False)
    MangrovePressurePlate = _block("mangrove_pressure_plate", Dimension.Overworld, True, False)
    CrimsonPressurePlate = _block("crimson_pressure_plate", Dimension.Nether, True, False)
    WarpedPressurePlate = _block("warped_pressure_plate", Dimension.Nether, True, False)
    StonePressurePlate = _block("stone_pressure_plate", Dimension.Overworld, True, False)
    LightWeightedPressurePlate = _block("light_weighted_pressure_plate", Dimension.Overworld, True, False)
    HeavyWeightedPressurePlate = _block("heavy_weighted_pressure_plate", Dimension.Overworld, True, False)
    PolishedBlackstonePressurePlate = _block("polished_blackstone_pressure_plate", Dimension.Nether, True, False)
    Observer = _block("observer", Dimension.Overworld, True, False)
    DaylightDetector = _block("daylight_detector", Dimension.Overworld, True, False)
    Repeater = _block("repeater", Dimension.Overworld, True, False)
    Comparator = _block("comparator", Dimension.Overworld, True, False)
    Hopper = _block("hopper", Dimension.Overworld, True, False)
    Dropper = _block("dropper", Dimension.Overworld, True, False)
    Dispenser = _block("dispenser", Dimension.Overworld, True, False)
    Piston = _block("piston", Dimension.Overworld, True, False)
    StickyPiston = _block("sticky_piston", Dimension.Overworld, True, False)
    Tnt = _block("tnt", Dimension.Overworld, True, False)
    NameTag = _block("name_tag", Dimension.Overworld, True, False)
    Loom = _block("loom", Dimension.Overworld, True, False)
    Banner = _block("banner", Dimension.Overworld, True, False,_state("variant", ["black_banner", "gray_banner", "light_gray_banner", "white_banner", "light_blue_banner", "orange_banner", "red_banner", "blue_banner", "purple_banner", "magenta_banner", "pink_banner", "brown_banner", "yellow_banner", "lime_banner", "green_banner", "cyan_banner", "illager_banner", ]))
    BordureIndentedBannerPattern = _block("bordure_indented_banner_pattern", Dimension.Overworld, True, False)
    CreeperBannerPattern = _block("creeper_banner_pattern", Dimension.Overworld, True, False)
    FieldMasonedBannerPattern = _block("field_masoned_banner_pattern", Dimension.Overworld, True, False)
    FlowerBannerPattern = _block("flower_banner_pattern", Dimension.Overworld, True, False)
    BannerPattern = _block("banner_pattern", Dimension.Overworld, True, False)
    MojangBannerPattern = _block("mojang_banner_pattern", Dimension.Overworld, True, False)
    PiglinBannerPattern = _block("piglin_banner_pattern", Dimension.Overworld, True, False)
    SkullBannerPattern = _block("skull_banner_pattern", Dimension.Overworld, True, False)
    FireworkRocket = _block("firework_rocket", Dimension.Overworld, True, False)
    FireworkStar = _block("firework_star", Dimension.Overworld, True, False)
    Chain = _block("chain", Dimension.Nether, True, False)
    Target = _block("target", Dimension.Overworld, True, False)
    Air = _block("air", Dimension.Overworld, True, True)
    Allow = _block("allow", Dimension.Overworld, True, True)
    Barrier = _block("barrier", Dimension.Overworld, True, True)
    CommandBlock = _block("command_block", Dimension.Overworld, True, True)
    ChainCommandBlock = _block("chain_command_block", Dimension.Overworld, True, True)
    RepeatingCommandBlock = _block("repeating_command_block", Dimension.Overworld, True, True)
    CommandBlockMinecart = _block("command_block_minecart", Dimension.Overworld, True, True)
    StructureBlock = _block("structure_block", Dimension.Overworld, True, True)
    StructureVoid = _block("structure_void", Dimension.Overworld, True, True)
    Jigsaw = _block("jigsaw", Dimension.Overworld, True, True)
    LightBlock = _block("light_block", Dimension.Overworld, True, True)
    SuspiciousStew = _block("suspicious_stew", Dimension.Overworld, True, True)
    FilledMap = _block("filled_map", Dimension.Overworld, True, True)
    FrostedIce = _block("frosted_ice", Dimension.Overworld, True, True)
    Portal = _block("portal", Dimension.Nether, True, True)
    EndPortal = _block("end_portal", Dimension.End, True, True, )
    EndGateway = _block("end_gateway", Dimension.End, True, True, )
    CalibratedSculkSensor = _block('calibrated_sculk_sensor', Dimension.Overworld, True, False)
    SnifferEgg = _block('sniffer_egg', Dimension.Overworld, True, False)
    PitcherPlant = _block('pitcher_plant', Dimension.Overworld, True, False)

    
    WhiteCarpet = _block("white_carpet", Dimension.Overworld, True, False)
    LightGrayCarpet = _block("light_gray_carpet", Dimension.Overworld, True, False)
    GrayCarpet = _block("gray_carpet", Dimension.Overworld, True, False)
    BlackCarpet = _block("black_carpet", Dimension.Overworld, True, False)
    BrownCarpet = _block("brown_carpet", Dimension.Overworld, True, False)
    RedCarpet = _block("red_carpet", Dimension.Overworld, True, False)
    OrangeCarpet = _block("orange_carpet", Dimension.Overworld, True, False)
    YellowCarpet = _block("yellow_carpet", Dimension.Overworld, True, False)
    LimeCarpet = _block("lime_carpet", Dimension.Overworld, True, False)
    GreenCarpet = _block("green_carpet", Dimension.Overworld, True, False)
    CyanCarpet = _block("cyan_carpet", Dimension.Overworld, True, False)
    LightBlueCarpet = _block("light_blue_carpet", Dimension.Overworld, True, False)
    BlueCarpet = _block("blue_carpet", Dimension.Overworld, True, False)
    PurpleCarpet = _block("purple_carpet", Dimension.Overworld, True, False)
    MagentaCarpet = _block("magenta_carpet", Dimension.Overworld, True, False)
    PinkCarpet = _block("pink_carpet", Dimension.Overworld, True, False)
    
    WhiteWool = _block("white_wool", Dimension.Overworld, True, False)
    LightGrayWool = _block("light_gray_wool", Dimension.Overworld, True, False)
    GrayWool = _block("gray_wool", Dimension.Overworld, True, False)
    BlackWool = _block("black_wool", Dimension.Overworld, True, False)
    BrownWool = _block("brown_wool", Dimension.Overworld, True, False)
    RedWool = _block("red_wool", Dimension.Overworld, True, False)
    OrangeWool = _block("orange_wool", Dimension.Overworld, True, False)
    YellowWool = _block("yellow_wool", Dimension.Overworld, True, False)
    LimeWool = _block("lime_wool", Dimension.Overworld, True, False)
    GreenWool = _block("green_wool", Dimension.Overworld, True, False)
    CyanWool = _block("cyan_wool", Dimension.Overworld, True, False)
    LightBlueWool = _block("light_blue_wool", Dimension.Overworld, True, False)
    BlueWool = _block("blue_wool", Dimension.Overworld, True, False)
    PurpleWool = _block("purple_wool", Dimension.Overworld, True, False)
    MagentaWool = _block("magenta_wool", Dimension.Overworld, True, False)
    PinkWool = _block("pink_wool", Dimension.Overworld, True, False)
    
    OakLog = _block("oak_log", Dimension.Overworld, True, False)
    SpruceLog = _block("spruce_log", Dimension.Overworld, True, False)
    BirchLog = _block("birch_log", Dimension.Overworld, True, False)
    JungleLog = _block("jungle_log", Dimension.Overworld, True, False)

    AcaciaLog = _block("acacia_log", Dimension.Overworld, True, False)
    DarkOakLog = _block("dark_oak_log", Dimension.Overworld, True, False)

    FireCoral = _block("fire_coral", Dimension.Overworld, True, False)
    BrainCoral = _block("brain_coral", Dimension.Overworld, True, False)
    BubbleCoral = _block("bubble_coral", Dimension.Overworld, True, False)
    TubeCoral = _block("tube_coral", Dimension.Overworld, True, False)
    HornCoral = _block("horn_coral", Dimension.Overworld, True, False)
    DeadFireCoral = _block("dead_fire_coral", Dimension.Overworld, True, False)
    DeadBrainCoral = _block("dead_brain_coral", Dimension.Overworld, True, False)
    DeadBubbleCoral = _block("dead_bubble_coral", Dimension.Overworld, True, False)
    DeadTubeCoral = _block("dead_tube_coral", Dimension.Overworld, True, False)
    DeadHornCoral = _block("dead_horn_coral", Dimension.Overworld, True, False)

    #For backward compability
    Carpet = _block("carpet", Dimension.Overworld, True, False)
    Wool = _block("wool", Dimension.Overworld, True, False)
    Log = _block("log", Dimension.Overworld, True, False)
    Log2 = _block("log2", Dimension.Overworld, True, False)
    Coral = _block("coral", Dimension.Overworld, True, False)


class Entities:
    class vanilla_entity():
        def __init__(self, name : str, is_vanilla: bool = True, allow_runtime: bool = True) -> None:
            super().__init__()
            ENTITY_LIST.append(self)
            self._namespace = 'minecraft' if is_vanilla else CONFIG.NAMESPACE
            self._name = name
            self._allow_runtime = allow_runtime
        
        @property
        def namespace(self):
            return self._namespace
        
        @property
        def identifier(self):
            return self._namespace + ':' + self._name
        
        def __str__(self) -> str:
            return self._name
        
        def __eq__(self, __value: object) -> bool:
            return __value == (self._namespace + ':' + self._name)

        def __iter__(self):
            yield self._name

    ArmorStand = vanilla_entity("armor_stand")
    Arrow = vanilla_entity("arrow")
    Axolotl = vanilla_entity("axolotl")
    Bat = vanilla_entity("bat")
    Bee = vanilla_entity("bee")
    Blaze = vanilla_entity("blaze")
    Cat = vanilla_entity("cat")
    CaveSpider = vanilla_entity("cave_spider")
    Chicken = vanilla_entity("chicken")
    Cow = vanilla_entity("cow")
    Creeper = vanilla_entity("creeper")
    Dolphin = vanilla_entity("dolphin")
    Donkey = vanilla_entity("donkey")
    Drowned = vanilla_entity("drowned")
    ElderGuardian = vanilla_entity("elder_guardian")
    EnderDragon = vanilla_entity("ender_dragon")
    Enderman = vanilla_entity("enderman")
    Endermite = vanilla_entity("endermite")
    EvocationIllager = vanilla_entity("evocation_illager")
    Fish = vanilla_entity("fish")
    FishingHook = vanilla_entity("fishing_hook")
    Fireball = vanilla_entity("fireball")
    Fox = vanilla_entity("fox")
    Ghast = vanilla_entity("ghast")
    GlowSquid = vanilla_entity("glow_squid")
    Goat = vanilla_entity("goat")
    Guardian = vanilla_entity("guardian")
    Hoglin = vanilla_entity("hoglin")
    Horse = vanilla_entity("horse")
    Husk = vanilla_entity("husk")
    IronGolem = vanilla_entity("iron_golem")
    Llama = vanilla_entity("llama")
    LlamaSpit = vanilla_entity("llama_spit")
    MagmaCube = vanilla_entity("magma_cube")
    Mooshroom = vanilla_entity("mooshroom")
    Mule = vanilla_entity("mule")
    Npc = vanilla_entity("npc")
    Ocelot = vanilla_entity("ocelot")
    Panda = vanilla_entity("panda")
    Parrot = vanilla_entity("parrot")
    Phantom = vanilla_entity("phantom")
    Pig = vanilla_entity("pig")
    PiglinBrute = vanilla_entity("piglin_brute")
    Piglin = vanilla_entity("piglin")
    Pillager = vanilla_entity("pillager")
    Player = vanilla_entity("player")
    PolarBear = vanilla_entity("polar_bear")
    Pufferfish = vanilla_entity("pufferfish")
    Rabbit = vanilla_entity("rabbit")
    Ravager = vanilla_entity("ravager")
    Salmon = vanilla_entity("salmon")
    Sheep = vanilla_entity("sheep")
    Shulker = vanilla_entity("shulker")
    Silverfish = vanilla_entity("silverfish")
    SkeletonHorse = vanilla_entity("skeleton_horse")
    Skeleton = vanilla_entity("skeleton")
    Slime = vanilla_entity("slime")
    SnowGolem = vanilla_entity("snow_golem")
    Spider = vanilla_entity("spider")
    Squid = vanilla_entity("squid")
    Stray = vanilla_entity("stray")
    Strider = vanilla_entity("strider")
    Tropicalfish = vanilla_entity("tropicalfish")
    ThrownTrident = vanilla_entity("thrown_trident")
    Turtle = vanilla_entity("turtle")
    Vex = vanilla_entity("vex")
    Villager = vanilla_entity("villager_v2")
    Vindicator = vanilla_entity("vindicator")
    WanderingTrader = vanilla_entity("wandering_trader")
    Witch = vanilla_entity("witch")
    WitherSkull = vanilla_entity("wither_skull")
    WitherSkullDangeroud = vanilla_entity("wither_skull_dangerous")
    WitherSkeleton = vanilla_entity("wither_skeleton")
    Wither = vanilla_entity("wither")
    Wolf = vanilla_entity("wolf")
    Zoglin = vanilla_entity("zoglin")
    ZombieHorse = vanilla_entity("zombie_horse")
    ZombiePigman = vanilla_entity("zombie_pigman")
    ZombieVillager = vanilla_entity("zombie_villager_v2")
    Zombie = vanilla_entity("zombie")
    Boat = vanilla_entity("boat")
    Snowball = vanilla_entity("snowball")
    LightningBolt = vanilla_entity('lightning_bolt')
    # 1.19.0
    # Updated on 11-07-2022
    Warden = vanilla_entity("warden")
    # 1.19.50.21
    # Updated on 21-10-2022
    Camel = vanilla_entity("camel")
    # 1.19.70.23
    # Updated on 28-02-2023
    Sniffer = vanilla_entity("sniffer")


class Blocks:
    class _MinecraftBlock():
        def __init__(self, name: str, is_vanilla: bool = True):
            self._namespace = 'minecraft' if is_vanilla else ANVIL.NAMESPACE
            self._name = name
            self._is_vanilla = is_vanilla

        @property
        def identifier(self):
            return f'{self._namespace}:{self._name}'
        
        @property
        def states(self):
            return {
                k: v
                for k, v in self.__dict__.items() 
                if v is not None
                if (k[1:].removeprefix('namespace').removeprefix('name').removeprefix('is_vanilla')) == k[1:] 
            }
        
        def __str__(self):
            return f'{self.identifier} [{", ".join([f'"{k[1:]}":"{v.value}"' for k, v in self.states])}]'

    class AcaciaButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("acacia_button", True)

    class AcaciaDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("acacia_door", True)

    class AcaciaFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("acacia_fence", True)

    class AcaciaFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("acacia_fence_gate", True)

    class AcaciaHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("acacia_hanging_sign", True)

    class AcaciaLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("acacia_log", True)

    class AcaciaPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("acacia_pressure_plate", True)

    class AcaciaStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("acacia_stairs", True)

    class AcaciaStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("acacia_standing_sign", True)

    class AcaciaTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("acacia_trapdoor", True)

    class AcaciaWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("acacia_wall_sign", True)

    class ActivatorRail(_MinecraftBlock):
        def __init__(self, rail_data_bit:'BlockStates.RailDataBit'=None, rail_direction:'BlockStates.RailDirection'=None):
            self._rail_data_bit = rail_data_bit
            self._rail_direction = rail_direction
            super().__init__("activator_rail", True)

    class Air(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("air", True)

    class Allow(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("allow", True)

    class AmethystBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("amethyst_block", True)

    class AmethystCluster(_MinecraftBlock):
        def __init__(self, block_face:'BlockStates.BlockFace'=None):
            self._block_face = block_face
            super().__init__("amethyst_cluster", True)

    class AncientDebris(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("ancient_debris", True)

    class AndesiteStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("andesite_stairs", True)

    class Anvil(_MinecraftBlock):
        def __init__(self, damage:'BlockStates.Damage'=None, cardinal_direction:'BlockStates.CardinalDirection'=None):
            self._damage = damage
            self._cardinal_direction = cardinal_direction
            super().__init__("anvil", True)

    class Azalea(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("azalea", True)

    class AzaleaLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("azalea_leaves", True)

    class AzaleaLeavesFlowered(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("azalea_leaves_flowered", True)

    class Bamboo(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None, bamboo_leaf_size:'BlockStates.BambooLeafSize'=None, bamboo_stalk_thickness:'BlockStates.BambooStalkThickness'=None):
            self._age_bit = age_bit
            self._bamboo_leaf_size = bamboo_leaf_size
            self._bamboo_stalk_thickness = bamboo_stalk_thickness
            super().__init__("bamboo", True)

    class BambooBlock(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("bamboo_block", True)

    class BambooButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("bamboo_button", True)

    class BambooDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("bamboo_door", True)

    class BambooDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("bamboo_double_slab", True)

    class BambooFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("bamboo_fence", True)

    class BambooFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("bamboo_fence_gate", True)

    class BambooHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("bamboo_hanging_sign", True)

    class BambooMosaic(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("bamboo_mosaic", True)

    class BambooMosaicDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("bamboo_mosaic_double_slab", True)

    class BambooMosaicSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("bamboo_mosaic_slab", True)

    class BambooMosaicStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("bamboo_mosaic_stairs", True)

    class BambooPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("bamboo_planks", True)

    class BambooPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("bamboo_pressure_plate", True)

    class BambooSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None, sapling_type:'BlockStates.SaplingType'=None):
            self._age_bit = age_bit
            self._sapling_type = sapling_type
            super().__init__("bamboo_sapling", True)

    class BambooSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("bamboo_slab", True)

    class BambooStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("bamboo_stairs", True)

    class BambooStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("bamboo_standing_sign", True)

    class BambooTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("bamboo_trapdoor", True)

    class BambooWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("bamboo_wall_sign", True)

    class Barrel(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, open_bit:'BlockStates.OpenBit'=None):
            self._facing_direction = facing_direction
            self._open_bit = open_bit
            super().__init__("barrel", True)

    class Barrier(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("barrier", True)

    class Basalt(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("basalt", True)

    class Beacon(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("beacon", True)

    class Bed(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, head_piece_bit:'BlockStates.HeadPieceBit'=None, occupied_bit:'BlockStates.OccupiedBit'=None):
            self._direction = direction
            self._head_piece_bit = head_piece_bit
            self._occupied_bit = occupied_bit
            super().__init__("bed", True)

    class Bedrock(_MinecraftBlock):
        def __init__(self, infiniburn_bit:'BlockStates.InfiniburnBit'=None):
            self._infiniburn_bit = infiniburn_bit
            super().__init__("bedrock", True)

    class Beehive(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, honey_level:'BlockStates.HoneyLevel'=None):
            self._direction = direction
            self._honey_level = honey_level
            super().__init__("beehive", True)

    class Beetroot(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None):
            self._growth = growth
            super().__init__("beetroot", True)

    class BeeNest(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, honey_level:'BlockStates.HoneyLevel'=None):
            self._direction = direction
            self._honey_level = honey_level
            super().__init__("bee_nest", True)

    class Bell(_MinecraftBlock):
        def __init__(self, attachment:'BlockStates.Attachment'=None, direction:'BlockStates.Direction'=None, toggle_bit:'BlockStates.ToggleBit'=None):
            self._attachment = attachment
            self._direction = direction
            self._toggle_bit = toggle_bit
            super().__init__("bell", True)

    class BigDripleaf(_MinecraftBlock):
        def __init__(self, big_dripleaf_head:'BlockStates.BigDripleafHead'=None, big_dripleaf_tilt:'BlockStates.BigDripleafTilt'=None, cardinal_direction:'BlockStates.CardinalDirection'=None):
            self._big_dripleaf_head = big_dripleaf_head
            self._big_dripleaf_tilt = big_dripleaf_tilt
            self._cardinal_direction = cardinal_direction
            super().__init__("big_dripleaf", True)

    class BirchButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("birch_button", True)

    class BirchDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("birch_door", True)

    class BirchFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("birch_fence", True)

    class BirchFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("birch_fence_gate", True)

    class BirchHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("birch_hanging_sign", True)

    class BirchLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("birch_log", True)

    class BirchPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("birch_pressure_plate", True)

    class BirchStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("birch_stairs", True)

    class BirchStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("birch_standing_sign", True)

    class BirchTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("birch_trapdoor", True)

    class BirchWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("birch_wall_sign", True)

    class Blackstone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("blackstone", True)

    class BlackstoneDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("blackstone_double_slab", True)

    class BlackstoneSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("blackstone_slab", True)

    class BlackstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("blackstone_stairs", True)

    class BlackstoneWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("blackstone_wall", True)

    class BlackCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("black_candle", True)

    class BlackCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("black_candle_cake", True)

    class BlackCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("black_carpet", True)

    class BlackGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("black_glazed_terracotta", True)

    class BlackWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("black_wool", True)

    class BlastFurnace(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("blast_furnace", True)

    class BlueCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("blue_candle", True)

    class BlueCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("blue_candle_cake", True)

    class BlueCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("blue_carpet", True)

    class BlueGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("blue_glazed_terracotta", True)

    class BlueIce(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("blue_ice", True)

    class BlueWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("blue_wool", True)

    class BoneBlock(_MinecraftBlock):
        def __init__(self, deprecated:'BlockStates.Deprecated'=None, pillar_axis:'BlockStates.PillarAxis'=None):
            self._deprecated = deprecated
            self._pillar_axis = pillar_axis
            super().__init__("bone_block", True)

    class Bookshelf(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("bookshelf", True)

    class BorderBlock(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("border_block", True)

    class BrainCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("brain_coral", True)

    class BrewingStand(_MinecraftBlock):
        def __init__(self, brewing_stand_slot_a_bit:'BlockStates.BrewingStandSlotABit'=None, brewing_stand_slot_b_bit:'BlockStates.BrewingStandSlotBBit'=None, brewing_stand_slot_c_bit:'BlockStates.BrewingStandSlotCBit'=None):
            self._brewing_stand_slot_a_bit = brewing_stand_slot_a_bit
            self._brewing_stand_slot_b_bit = brewing_stand_slot_b_bit
            self._brewing_stand_slot_c_bit = brewing_stand_slot_c_bit
            super().__init__("brewing_stand", True)

    class BrickBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("brick_block", True)

    class BrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("brick_stairs", True)

    class BrownCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("brown_candle", True)

    class BrownCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("brown_candle_cake", True)

    class BrownCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("brown_carpet", True)

    class BrownGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("brown_glazed_terracotta", True)

    class BrownMushroom(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("brown_mushroom", True)

    class BrownMushroomBlock(_MinecraftBlock):
        def __init__(self, huge_mushroom_bits:'BlockStates.HugeMushroomBits'=None):
            self._huge_mushroom_bits = huge_mushroom_bits
            super().__init__("brown_mushroom_block", True)

    class BrownWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("brown_wool", True)

    class BubbleColumn(_MinecraftBlock):
        def __init__(self, drag_down:'BlockStates.DragDown'=None):
            self._drag_down = drag_down
            super().__init__("bubble_column", True)

    class BubbleCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("bubble_coral", True)

    class BuddingAmethyst(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("budding_amethyst", True)

    class Cactus(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("cactus", True)

    class Cake(_MinecraftBlock):
        def __init__(self, bite_counter:'BlockStates.BiteCounter'=None):
            self._bite_counter = bite_counter
            super().__init__("cake", True)

    class Calcite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("calcite", True)

    class CalibratedSculkSensor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, sculk_sensor_phase:'BlockStates.SculkSensorPhase'=None):
            self._direction = direction
            self._sculk_sensor_phase = sculk_sensor_phase
            super().__init__("calibrated_sculk_sensor", True)

    class Camera(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("camera", True)

    class Campfire(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, extinguished:'BlockStates.Extinguished'=None):
            self._direction = direction
            self._extinguished = extinguished
            super().__init__("campfire", True)

    class Candle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("candle", True)

    class CandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("candle_cake", True)

    class Carrots(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None):
            self._growth = growth
            super().__init__("carrots", True)

    class CartographyTable(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cartography_table", True)

    class CarvedPumpkin(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None):
            self._cardinal_direction = cardinal_direction
            super().__init__("carved_pumpkin", True)

    class Cauldron(_MinecraftBlock):
        def __init__(self, cauldron_liquid:'BlockStates.CauldronLiquid'=None, fill_level:'BlockStates.FillLevel'=None):
            self._cauldron_liquid = cauldron_liquid
            self._fill_level = fill_level
            super().__init__("cauldron", True)

    class CaveVines(_MinecraftBlock):
        def __init__(self, growing_plant_age:'BlockStates.GrowingPlantAge'=None):
            self._growing_plant_age = growing_plant_age
            super().__init__("cave_vines", True)

    class CaveVinesBodyWithBerries(_MinecraftBlock):
        def __init__(self, growing_plant_age:'BlockStates.GrowingPlantAge'=None):
            self._growing_plant_age = growing_plant_age
            super().__init__("cave_vines_body_with_berries", True)

    class CaveVinesHeadWithBerries(_MinecraftBlock):
        def __init__(self, growing_plant_age:'BlockStates.GrowingPlantAge'=None):
            self._growing_plant_age = growing_plant_age
            super().__init__("cave_vines_head_with_berries", True)

    class Chain(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("chain", True)

    class ChainCommandBlock(_MinecraftBlock):
        def __init__(self, conditional_bit:'BlockStates.ConditionalBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._conditional_bit = conditional_bit
            self._facing_direction = facing_direction
            super().__init__("chain_command_block", True)

    class ChemicalHeat(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("chemical_heat", True)

    class ChemistryTable(_MinecraftBlock):
        def __init__(self, chemistry_table_type:'BlockStates.ChemistryTableType'=None, direction:'BlockStates.Direction'=None):
            self._chemistry_table_type = chemistry_table_type
            self._direction = direction
            super().__init__("chemistry_table", True)

    class CherryButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("cherry_button", True)

    class CherryDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("cherry_door", True)

    class CherryDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("cherry_double_slab", True)

    class CherryFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cherry_fence", True)

    class CherryFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("cherry_fence_gate", True)

    class CherryHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("cherry_hanging_sign", True)

    class CherryLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("cherry_leaves", True)

    class CherryLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("cherry_log", True)

    class CherryPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cherry_planks", True)

    class CherryPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("cherry_pressure_plate", True)

    class CherrySapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("cherry_sapling", True)

    class CherrySlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("cherry_slab", True)

    class CherryStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("cherry_stairs", True)

    class CherryStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("cherry_standing_sign", True)

    class CherryTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("cherry_trapdoor", True)

    class CherryWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("cherry_wall_sign", True)

    class CherryWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None, stripped_bit:'BlockStates.StrippedBit'=None):
            self._pillar_axis = pillar_axis
            self._stripped_bit = stripped_bit
            super().__init__("cherry_wood", True)

    class Chest(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("chest", True)

    class ChiseledBookshelf(_MinecraftBlock):
        def __init__(self, books_stored:'BlockStates.BooksStored'=None, direction:'BlockStates.Direction'=None):
            self._books_stored = books_stored
            self._direction = direction
            super().__init__("chiseled_bookshelf", True)

    class ChiseledDeepslate(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("chiseled_deepslate", True)

    class ChiseledNetherBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("chiseled_nether_bricks", True)

    class ChiseledPolishedBlackstone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("chiseled_polished_blackstone", True)

    class ChorusFlower(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("chorus_flower", True)

    class ChorusPlant(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("chorus_plant", True)

    class Clay(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("clay", True)

    class ClientRequestPlaceholderBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("client_request_placeholder_block", True)

    class CoalBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("coal_block", True)

    class CoalOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("coal_ore", True)

    class CobbledDeepslate(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cobbled_deepslate", True)

    class CobbledDeepslateDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("cobbled_deepslate_double_slab", True)

    class CobbledDeepslateSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("cobbled_deepslate_slab", True)

    class CobbledDeepslateStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("cobbled_deepslate_stairs", True)

    class CobbledDeepslateWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("cobbled_deepslate_wall", True)

    class Cobblestone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cobblestone", True)

    class CobblestoneWall(_MinecraftBlock):
        def __init__(self, wall_block_type:'BlockStates.WallBlockType'=None, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_block_type = wall_block_type
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("cobblestone_wall", True)

    class Cocoa(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None, direction:'BlockStates.Direction'=None):
            self._age = age
            self._direction = direction
            super().__init__("cocoa", True)

    class ColoredTorchBp(_MinecraftBlock):
        def __init__(self, color_bit:'BlockStates.ColorBit'=None, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._color_bit = color_bit
            self._torch_facing_direction = torch_facing_direction
            super().__init__("colored_torch_bp", True)

    class ColoredTorchRg(_MinecraftBlock):
        def __init__(self, color_bit:'BlockStates.ColorBit'=None, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._color_bit = color_bit
            self._torch_facing_direction = torch_facing_direction
            super().__init__("colored_torch_rg", True)

    class CommandBlock(_MinecraftBlock):
        def __init__(self, conditional_bit:'BlockStates.ConditionalBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._conditional_bit = conditional_bit
            self._facing_direction = facing_direction
            super().__init__("command_block", True)

    class Composter(_MinecraftBlock):
        def __init__(self, composter_fill_level:'BlockStates.ComposterFillLevel'=None):
            self._composter_fill_level = composter_fill_level
            super().__init__("composter", True)

    class Concrete(_MinecraftBlock):
        def __init__(self, color:'BlockStates.Color'=None):
            self._color = color
            super().__init__("concrete", True)

    class Concretepowder(_MinecraftBlock):
        def __init__(self, color:'BlockStates.Color'=None):
            self._color = color
            super().__init__("concretePowder", True)

    class ConcretePowder(_MinecraftBlock):
        def __init__(self, color:'BlockStates.Color'=None):
            self._color = color
            super().__init__("concrete_powder", True)

    class Conduit(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("conduit", True)

    class CopperBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("copper_block", True)

    class CopperOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("copper_ore", True)

    class CoralBlock(_MinecraftBlock):
        def __init__(self, coral_color:'BlockStates.CoralColor'=None, dead_bit:'BlockStates.DeadBit'=None):
            self._coral_color = coral_color
            self._dead_bit = dead_bit
            super().__init__("coral_block", True)

    class CoralFan(_MinecraftBlock):
        def __init__(self, coral_color:'BlockStates.CoralColor'=None, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_color = coral_color
            self._coral_fan_direction = coral_fan_direction
            super().__init__("coral_fan", True)

    class CoralFanDead(_MinecraftBlock):
        def __init__(self, coral_color:'BlockStates.CoralColor'=None, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_color = coral_color
            self._coral_fan_direction = coral_fan_direction
            super().__init__("coral_fan_dead", True)

    class CoralFanHang(_MinecraftBlock):
        def __init__(self, coral_direction:'BlockStates.CoralDirection'=None, coral_hang_type_bit:'BlockStates.CoralHangTypeBit'=None, dead_bit:'BlockStates.DeadBit'=None):
            self._coral_direction = coral_direction
            self._coral_hang_type_bit = coral_hang_type_bit
            self._dead_bit = dead_bit
            super().__init__("coral_fan_hang", True)

    class CoralFanHang2(_MinecraftBlock):
        def __init__(self, coral_direction:'BlockStates.CoralDirection'=None, coral_hang_type_bit:'BlockStates.CoralHangTypeBit'=None, dead_bit:'BlockStates.DeadBit'=None):
            self._coral_direction = coral_direction
            self._coral_hang_type_bit = coral_hang_type_bit
            self._dead_bit = dead_bit
            super().__init__("coral_fan_hang2", True)

    class CoralFanHang3(_MinecraftBlock):
        def __init__(self, coral_direction:'BlockStates.CoralDirection'=None, coral_hang_type_bit:'BlockStates.CoralHangTypeBit'=None, dead_bit:'BlockStates.DeadBit'=None):
            self._coral_direction = coral_direction
            self._coral_hang_type_bit = coral_hang_type_bit
            self._dead_bit = dead_bit
            super().__init__("coral_fan_hang3", True)

    class CrackedDeepslateBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cracked_deepslate_bricks", True)

    class CrackedDeepslateTiles(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cracked_deepslate_tiles", True)

    class CrackedNetherBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cracked_nether_bricks", True)

    class CrackedPolishedBlackstoneBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cracked_polished_blackstone_bricks", True)

    class CraftingTable(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crafting_table", True)

    class CrimsonButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("crimson_button", True)

    class CrimsonDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("crimson_door", True)

    class CrimsonDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("crimson_double_slab", True)

    class CrimsonFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crimson_fence", True)

    class CrimsonFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("crimson_fence_gate", True)

    class CrimsonFungus(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crimson_fungus", True)

    class CrimsonHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("crimson_hanging_sign", True)

    class CrimsonHyphae(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("crimson_hyphae", True)

    class CrimsonNylium(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crimson_nylium", True)

    class CrimsonPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crimson_planks", True)

    class CrimsonPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("crimson_pressure_plate", True)

    class CrimsonRoots(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crimson_roots", True)

    class CrimsonSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("crimson_slab", True)

    class CrimsonStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("crimson_stairs", True)

    class CrimsonStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("crimson_standing_sign", True)

    class CrimsonStem(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("crimson_stem", True)

    class CrimsonTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("crimson_trapdoor", True)

    class CrimsonWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("crimson_wall_sign", True)

    class CryingObsidian(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("crying_obsidian", True)

    class CutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cut_copper", True)

    class CutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("cut_copper_slab", True)

    class CutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("cut_copper_stairs", True)

    class CyanCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("cyan_candle", True)

    class CyanCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("cyan_candle_cake", True)

    class CyanCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cyan_carpet", True)

    class CyanGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("cyan_glazed_terracotta", True)

    class CyanWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("cyan_wool", True)

    class DarkoakStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("darkoak_standing_sign", True)

    class DarkoakWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("darkoak_wall_sign", True)

    class DarkOakButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("dark_oak_button", True)

    class DarkOakDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("dark_oak_door", True)

    class DarkOakFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dark_oak_fence", True)

    class DarkOakFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("dark_oak_fence_gate", True)

    class DarkOakHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("dark_oak_hanging_sign", True)

    class DarkOakLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("dark_oak_log", True)

    class DarkOakPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("dark_oak_pressure_plate", True)

    class DarkOakStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("dark_oak_stairs", True)

    class DarkOakTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("dark_oak_trapdoor", True)

    class DarkPrismarineStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("dark_prismarine_stairs", True)

    class DaylightDetector(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("daylight_detector", True)

    class DaylightDetectorInverted(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("daylight_detector_inverted", True)

    class Deadbush(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deadbush", True)

    class DeadBrainCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dead_brain_coral", True)

    class DeadBubbleCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dead_bubble_coral", True)

    class DeadFireCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dead_fire_coral", True)

    class DeadHornCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dead_horn_coral", True)

    class DeadTubeCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dead_tube_coral", True)

    class DecoratedPot(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None):
            self._direction = direction
            super().__init__("decorated_pot", True)

    class Deepslate(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("deepslate", True)

    class DeepslateBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_bricks", True)

    class DeepslateBrickDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("deepslate_brick_double_slab", True)

    class DeepslateBrickSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("deepslate_brick_slab", True)

    class DeepslateBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("deepslate_brick_stairs", True)

    class DeepslateBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("deepslate_brick_wall", True)

    class DeepslateCoalOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_coal_ore", True)

    class DeepslateCopperOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_copper_ore", True)

    class DeepslateDiamondOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_diamond_ore", True)

    class DeepslateEmeraldOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_emerald_ore", True)

    class DeepslateGoldOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_gold_ore", True)

    class DeepslateIronOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_iron_ore", True)

    class DeepslateLapisOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_lapis_ore", True)

    class DeepslateRedstoneOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_redstone_ore", True)

    class DeepslateTiles(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deepslate_tiles", True)

    class DeepslateTileDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("deepslate_tile_double_slab", True)

    class DeepslateTileSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("deepslate_tile_slab", True)

    class DeepslateTileStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("deepslate_tile_stairs", True)

    class DeepslateTileWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("deepslate_tile_wall", True)

    class Deny(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("deny", True)

    class DetectorRail(_MinecraftBlock):
        def __init__(self, rail_data_bit:'BlockStates.RailDataBit'=None, rail_direction:'BlockStates.RailDirection'=None):
            self._rail_data_bit = rail_data_bit
            self._rail_direction = rail_direction
            super().__init__("detector_rail", True)

    class DiamondBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("diamond_block", True)

    class DiamondOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("diamond_ore", True)

    class DioriteStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("diorite_stairs", True)

    class Dirt(_MinecraftBlock):
        def __init__(self, dirt_type:'BlockStates.DirtType'=None):
            self._dirt_type = dirt_type
            super().__init__("dirt", True)

    class DirtWithRoots(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dirt_with_roots", True)

    class Dispenser(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, triggered_bit:'BlockStates.TriggeredBit'=None):
            self._facing_direction = facing_direction
            self._triggered_bit = triggered_bit
            super().__init__("dispenser", True)

    class DoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("double_cut_copper_slab", True)

    class DoublePlant(_MinecraftBlock):
        def __init__(self, double_plant_type:'BlockStates.DoublePlantType'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._double_plant_type = double_plant_type
            self._upper_block_bit = upper_block_bit
            super().__init__("double_plant", True)

    class DoubleStoneBlockSlab(_MinecraftBlock):
        def __init__(self, stone_slab_type:'BlockStates.StoneSlabType'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type = stone_slab_type
            self._vertical_half = vertical_half
            super().__init__("double_stone_block_slab", True)

    class DoubleStoneBlockSlab2(_MinecraftBlock):
        def __init__(self, stone_slab_type_2:'BlockStates.StoneSlabType2'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type_2 = stone_slab_type_2
            self._vertical_half = vertical_half
            super().__init__("double_stone_block_slab2", True)

    class DoubleStoneBlockSlab3(_MinecraftBlock):
        def __init__(self, stone_slab_type_3:'BlockStates.StoneSlabType3'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type_3 = stone_slab_type_3
            self._vertical_half = vertical_half
            super().__init__("double_stone_block_slab3", True)

    class DoubleStoneBlockSlab4(_MinecraftBlock):
        def __init__(self, stone_slab_type_4:'BlockStates.StoneSlabType4'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type_4 = stone_slab_type_4
            self._vertical_half = vertical_half
            super().__init__("double_stone_block_slab4", True)

    class DoubleWoodenSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None, wood_type:'BlockStates.WoodType'=None):
            self._vertical_half = vertical_half
            self._wood_type = wood_type
            super().__init__("double_wooden_slab", True)

    class DragonEgg(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dragon_egg", True)

    class DriedKelpBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dried_kelp_block", True)

    class DripstoneBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dripstone_block", True)

    class Dropper(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, triggered_bit:'BlockStates.TriggeredBit'=None):
            self._facing_direction = facing_direction
            self._triggered_bit = triggered_bit
            super().__init__("dropper", True)

    class Element0(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_0", True)

    class Element1(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_1", True)

    class Element10(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_10", True)

    class Element100(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_100", True)

    class Element101(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_101", True)

    class Element102(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_102", True)

    class Element103(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_103", True)

    class Element104(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_104", True)

    class Element105(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_105", True)

    class Element106(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_106", True)

    class Element107(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_107", True)

    class Element108(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_108", True)

    class Element109(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_109", True)

    class Element11(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_11", True)

    class Element110(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_110", True)

    class Element111(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_111", True)

    class Element112(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_112", True)

    class Element113(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_113", True)

    class Element114(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_114", True)

    class Element115(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_115", True)

    class Element116(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_116", True)

    class Element117(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_117", True)

    class Element118(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_118", True)

    class Element12(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_12", True)

    class Element13(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_13", True)

    class Element14(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_14", True)

    class Element15(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_15", True)

    class Element16(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_16", True)

    class Element17(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_17", True)

    class Element18(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_18", True)

    class Element19(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_19", True)

    class Element2(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_2", True)

    class Element20(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_20", True)

    class Element21(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_21", True)

    class Element22(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_22", True)

    class Element23(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_23", True)

    class Element24(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_24", True)

    class Element25(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_25", True)

    class Element26(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_26", True)

    class Element27(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_27", True)

    class Element28(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_28", True)

    class Element29(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_29", True)

    class Element3(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_3", True)

    class Element30(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_30", True)

    class Element31(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_31", True)

    class Element32(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_32", True)

    class Element33(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_33", True)

    class Element34(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_34", True)

    class Element35(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_35", True)

    class Element36(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_36", True)

    class Element37(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_37", True)

    class Element38(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_38", True)

    class Element39(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_39", True)

    class Element4(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_4", True)

    class Element40(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_40", True)

    class Element41(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_41", True)

    class Element42(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_42", True)

    class Element43(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_43", True)

    class Element44(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_44", True)

    class Element45(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_45", True)

    class Element46(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_46", True)

    class Element47(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_47", True)

    class Element48(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_48", True)

    class Element49(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_49", True)

    class Element5(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_5", True)

    class Element50(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_50", True)

    class Element51(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_51", True)

    class Element52(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_52", True)

    class Element53(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_53", True)

    class Element54(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_54", True)

    class Element55(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_55", True)

    class Element56(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_56", True)

    class Element57(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_57", True)

    class Element58(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_58", True)

    class Element59(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_59", True)

    class Element6(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_6", True)

    class Element60(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_60", True)

    class Element61(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_61", True)

    class Element62(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_62", True)

    class Element63(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_63", True)

    class Element64(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_64", True)

    class Element65(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_65", True)

    class Element66(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_66", True)

    class Element67(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_67", True)

    class Element68(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_68", True)

    class Element69(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_69", True)

    class Element7(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_7", True)

    class Element70(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_70", True)

    class Element71(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_71", True)

    class Element72(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_72", True)

    class Element73(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_73", True)

    class Element74(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_74", True)

    class Element75(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_75", True)

    class Element76(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_76", True)

    class Element77(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_77", True)

    class Element78(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_78", True)

    class Element79(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_79", True)

    class Element8(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_8", True)

    class Element80(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_80", True)

    class Element81(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_81", True)

    class Element82(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_82", True)

    class Element83(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_83", True)

    class Element84(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_84", True)

    class Element85(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_85", True)

    class Element86(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_86", True)

    class Element87(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_87", True)

    class Element88(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_88", True)

    class Element89(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_89", True)

    class Element9(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_9", True)

    class Element90(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_90", True)

    class Element91(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_91", True)

    class Element92(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_92", True)

    class Element93(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_93", True)

    class Element94(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_94", True)

    class Element95(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_95", True)

    class Element96(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_96", True)

    class Element97(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_97", True)

    class Element98(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_98", True)

    class Element99(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("element_99", True)

    class EmeraldBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("emerald_block", True)

    class EmeraldOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("emerald_ore", True)

    class EnchantingTable(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("enchanting_table", True)

    class EnderChest(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("ender_chest", True)

    class EndBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("end_bricks", True)

    class EndBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("end_brick_stairs", True)

    class EndGateway(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("end_gateway", True)

    class EndPortal(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("end_portal", True)

    class EndPortalFrame(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, end_portal_eye_bit:'BlockStates.EndPortalEyeBit'=None):
            self._cardinal_direction = cardinal_direction
            self._end_portal_eye_bit = end_portal_eye_bit
            super().__init__("end_portal_frame", True)

    class EndRod(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("end_rod", True)

    class EndStone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("end_stone", True)

    class ExposedCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("exposed_copper", True)

    class ExposedCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("exposed_cut_copper", True)

    class ExposedCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("exposed_cut_copper_slab", True)

    class ExposedCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("exposed_cut_copper_stairs", True)

    class ExposedDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("exposed_double_cut_copper_slab", True)

    class Farmland(_MinecraftBlock):
        def __init__(self, moisturized_amount:'BlockStates.MoisturizedAmount'=None):
            self._moisturized_amount = moisturized_amount
            super().__init__("farmland", True)

    class FenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("fence_gate", True)

    class Fire(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("fire", True)

    class FireCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("fire_coral", True)

    class FletchingTable(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("fletching_table", True)

    class FloweringAzalea(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("flowering_azalea", True)

    class FlowerPot(_MinecraftBlock):
        def __init__(self, update_bit:'BlockStates.UpdateBit'=None):
            self._update_bit = update_bit
            super().__init__("flower_pot", True)

    class FlowingLava(_MinecraftBlock):
        def __init__(self, liquid_depth:'BlockStates.LiquidDepth'=None):
            self._liquid_depth = liquid_depth
            super().__init__("flowing_lava", True)

    class FlowingWater(_MinecraftBlock):
        def __init__(self, liquid_depth:'BlockStates.LiquidDepth'=None):
            self._liquid_depth = liquid_depth
            super().__init__("flowing_water", True)

    class Frame(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, item_frame_map_bit:'BlockStates.ItemFrameMapBit'=None, item_frame_photo_bit:'BlockStates.ItemFramePhotoBit'=None):
            self._facing_direction = facing_direction
            self._item_frame_map_bit = item_frame_map_bit
            self._item_frame_photo_bit = item_frame_photo_bit
            super().__init__("frame", True)

    class FrogSpawn(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("frog_spawn", True)

    class FrostedIce(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("frosted_ice", True)

    class Furnace(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("furnace", True)

    class GildedBlackstone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("gilded_blackstone", True)

    class Glass(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("glass", True)

    class GlassPane(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("glass_pane", True)

    class Glowingobsidian(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("glowingobsidian", True)

    class Glowstone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("glowstone", True)

    class GlowFrame(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, item_frame_map_bit:'BlockStates.ItemFrameMapBit'=None, item_frame_photo_bit:'BlockStates.ItemFramePhotoBit'=None):
            self._facing_direction = facing_direction
            self._item_frame_map_bit = item_frame_map_bit
            self._item_frame_photo_bit = item_frame_photo_bit
            super().__init__("glow_frame", True)

    class GlowLichen(_MinecraftBlock):
        def __init__(self, multi_face_direction_bits:'BlockStates.MultiFaceDirectionBits'=None):
            self._multi_face_direction_bits = multi_face_direction_bits
            super().__init__("glow_lichen", True)

    class GoldenRail(_MinecraftBlock):
        def __init__(self, rail_data_bit:'BlockStates.RailDataBit'=None, rail_direction:'BlockStates.RailDirection'=None):
            self._rail_data_bit = rail_data_bit
            self._rail_direction = rail_direction
            super().__init__("golden_rail", True)

    class GoldBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("gold_block", True)

    class GoldOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("gold_ore", True)

    class GraniteStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("granite_stairs", True)

    class Grass(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("grass", True)

    class GrassPath(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("grass_path", True)

    class Gravel(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("gravel", True)

    class GrayCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("gray_candle", True)

    class GrayCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("gray_candle_cake", True)

    class GrayCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("gray_carpet", True)

    class GrayGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("gray_glazed_terracotta", True)

    class GrayWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("gray_wool", True)

    class GreenCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("green_candle", True)

    class GreenCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("green_candle_cake", True)

    class GreenCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("green_carpet", True)

    class GreenGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("green_glazed_terracotta", True)

    class GreenWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("green_wool", True)

    class Grindstone(_MinecraftBlock):
        def __init__(self, attachment:'BlockStates.Attachment'=None, direction:'BlockStates.Direction'=None):
            self._attachment = attachment
            self._direction = direction
            super().__init__("grindstone", True)

    class HangingRoots(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("hanging_roots", True)

    class HardenedClay(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("hardened_clay", True)

    class HardGlass(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("hard_glass", True)

    class HardGlassPane(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("hard_glass_pane", True)

    class HardStainedGlass(_MinecraftBlock):
        def __init__(self, color:'BlockStates.Color'=None):
            self._color = color
            super().__init__("hard_stained_glass", True)

    class HardStainedGlassPane(_MinecraftBlock):
        def __init__(self, color:'BlockStates.Color'=None):
            self._color = color
            super().__init__("hard_stained_glass_pane", True)

    class HayBlock(_MinecraftBlock):
        def __init__(self, deprecated:'BlockStates.Deprecated'=None, pillar_axis:'BlockStates.PillarAxis'=None):
            self._deprecated = deprecated
            self._pillar_axis = pillar_axis
            super().__init__("hay_block", True)

    class HeavyWeightedPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("heavy_weighted_pressure_plate", True)

    class HoneycombBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("honeycomb_block", True)

    class HoneyBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("honey_block", True)

    class Hopper(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, toggle_bit:'BlockStates.ToggleBit'=None):
            self._facing_direction = facing_direction
            self._toggle_bit = toggle_bit
            super().__init__("hopper", True)

    class HornCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("horn_coral", True)

    class Ice(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("ice", True)

    class InfestedDeepslate(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("infested_deepslate", True)

    class InfoUpdate(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("info_update", True)

    class InfoUpdate2(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("info_update2", True)

    class InvisibleBedrock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("invisible_bedrock", True)

    class IronBars(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("iron_bars", True)

    class IronBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("iron_block", True)

    class IronDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("iron_door", True)

    class IronOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("iron_ore", True)

    class IronTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("iron_trapdoor", True)

    class Jigsaw(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, rotation:'BlockStates.Rotation'=None):
            self._facing_direction = facing_direction
            self._rotation = rotation
            super().__init__("jigsaw", True)

    class Jukebox(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("jukebox", True)

    class JungleButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("jungle_button", True)

    class JungleDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("jungle_door", True)

    class JungleFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("jungle_fence", True)

    class JungleFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("jungle_fence_gate", True)

    class JungleHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("jungle_hanging_sign", True)

    class JungleLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("jungle_log", True)

    class JunglePressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("jungle_pressure_plate", True)

    class JungleStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("jungle_stairs", True)

    class JungleStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("jungle_standing_sign", True)

    class JungleTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("jungle_trapdoor", True)

    class JungleWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("jungle_wall_sign", True)

    class Kelp(_MinecraftBlock):
        def __init__(self, kelp_age:'BlockStates.KelpAge'=None):
            self._kelp_age = kelp_age
            super().__init__("kelp", True)

    class Ladder(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("ladder", True)

    class Lantern(_MinecraftBlock):
        def __init__(self, hanging:'BlockStates.Hanging'=None):
            self._hanging = hanging
            super().__init__("lantern", True)

    class LapisBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lapis_block", True)

    class LapisOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lapis_ore", True)

    class LargeAmethystBud(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("large_amethyst_bud", True)

    class Lava(_MinecraftBlock):
        def __init__(self, liquid_depth:'BlockStates.LiquidDepth'=None):
            self._liquid_depth = liquid_depth
            super().__init__("lava", True)

    class Leaves(_MinecraftBlock):
        def __init__(self, old_leaf_type:'BlockStates.OldLeafType'=None, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._old_leaf_type = old_leaf_type
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("leaves", True)

    class Leaves2(_MinecraftBlock):
        def __init__(self, new_leaf_type:'BlockStates.NewLeafType'=None, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._new_leaf_type = new_leaf_type
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("leaves2", True)

    class Lectern(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, powered_bit:'BlockStates.PoweredBit'=None):
            self._cardinal_direction = cardinal_direction
            self._powered_bit = powered_bit
            super().__init__("lectern", True)

    class Lever(_MinecraftBlock):
        def __init__(self, lever_direction:'BlockStates.LeverDirection'=None, open_bit:'BlockStates.OpenBit'=None):
            self._lever_direction = lever_direction
            self._open_bit = open_bit
            super().__init__("lever", True)

    class LightningRod(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("lightning_rod", True)

    class LightBlock(_MinecraftBlock):
        def __init__(self, block_light_level:'BlockStates.BlockLightLevel'=None):
            self._block_light_level = block_light_level
            super().__init__("light_block", True)

    class LightBlueCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("light_blue_candle", True)

    class LightBlueCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("light_blue_candle_cake", True)

    class LightBlueCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("light_blue_carpet", True)

    class LightBlueGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("light_blue_glazed_terracotta", True)

    class LightBlueWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("light_blue_wool", True)

    class LightGrayCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("light_gray_candle", True)

    class LightGrayCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("light_gray_candle_cake", True)

    class LightGrayCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("light_gray_carpet", True)

    class LightGrayWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("light_gray_wool", True)

    class LightWeightedPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("light_weighted_pressure_plate", True)

    class LimeCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("lime_candle", True)

    class LimeCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("lime_candle_cake", True)

    class LimeCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lime_carpet", True)

    class LimeGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("lime_glazed_terracotta", True)

    class LimeWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lime_wool", True)

    class LitBlastFurnace(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("lit_blast_furnace", True)

    class LitDeepslateRedstoneOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lit_deepslate_redstone_ore", True)

    class LitFurnace(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("lit_furnace", True)

    class LitPumpkin(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None):
            self._cardinal_direction = cardinal_direction
            super().__init__("lit_pumpkin", True)

    class LitRedstoneLamp(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lit_redstone_lamp", True)

    class LitRedstoneOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lit_redstone_ore", True)

    class LitSmoker(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("lit_smoker", True)

    class Lodestone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("lodestone", True)

    class Loom(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None):
            self._direction = direction
            super().__init__("loom", True)

    class MagentaCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("magenta_candle", True)

    class MagentaCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("magenta_candle_cake", True)

    class MagentaCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("magenta_carpet", True)

    class MagentaGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("magenta_glazed_terracotta", True)

    class MagentaWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("magenta_wool", True)

    class Magma(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("magma", True)

    class MangroveButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("mangrove_button", True)

    class MangroveDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("mangrove_door", True)

    class MangroveDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("mangrove_double_slab", True)

    class MangroveFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mangrove_fence", True)

    class MangroveFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("mangrove_fence_gate", True)

    class MangroveHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("mangrove_hanging_sign", True)

    class MangroveLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("mangrove_leaves", True)

    class MangroveLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("mangrove_log", True)

    class MangrovePlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mangrove_planks", True)

    class MangrovePressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("mangrove_pressure_plate", True)

    class MangrovePropagule(_MinecraftBlock):
        def __init__(self, hanging:'BlockStates.Hanging'=None, propagule_stage:'BlockStates.PropaguleStage'=None):
            self._hanging = hanging
            self._propagule_stage = propagule_stage
            super().__init__("mangrove_propagule", True)

    class MangroveRoots(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mangrove_roots", True)

    class MangroveSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("mangrove_slab", True)

    class MangroveStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("mangrove_stairs", True)

    class MangroveStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("mangrove_standing_sign", True)

    class MangroveTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("mangrove_trapdoor", True)

    class MangroveWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("mangrove_wall_sign", True)

    class MangroveWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None, stripped_bit:'BlockStates.StrippedBit'=None):
            self._pillar_axis = pillar_axis
            self._stripped_bit = stripped_bit
            super().__init__("mangrove_wood", True)

    class MediumAmethystBud(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("medium_amethyst_bud", True)

    class MelonBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("melon_block", True)

    class MelonStem(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, growth:'BlockStates.Growth'=None):
            self._facing_direction = facing_direction
            self._growth = growth
            super().__init__("melon_stem", True)

    class MobSpawner(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mob_spawner", True)

    class MonsterEgg(_MinecraftBlock):
        def __init__(self, monster_egg_stone_type:'BlockStates.MonsterEggStoneType'=None):
            self._monster_egg_stone_type = monster_egg_stone_type
            super().__init__("monster_egg", True)

    class MossyCobblestone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mossy_cobblestone", True)

    class MossyCobblestoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("mossy_cobblestone_stairs", True)

    class MossyStoneBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("mossy_stone_brick_stairs", True)

    class MossBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("moss_block", True)

    class MossCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("moss_carpet", True)

    class MovingBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("moving_block", True)

    class Mud(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mud", True)

    class MuddyMangroveRoots(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("muddy_mangrove_roots", True)

    class MudBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mud_bricks", True)

    class MudBrickDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("mud_brick_double_slab", True)

    class MudBrickSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("mud_brick_slab", True)

    class MudBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("mud_brick_stairs", True)

    class MudBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("mud_brick_wall", True)

    class Mycelium(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("mycelium", True)

    class NetheriteBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("netherite_block", True)

    class Netherrack(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("netherrack", True)

    class Netherreactor(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("netherreactor", True)

    class NetherBrick(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("nether_brick", True)

    class NetherBrickFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("nether_brick_fence", True)

    class NetherBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("nether_brick_stairs", True)

    class NetherGoldOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("nether_gold_ore", True)

    class NetherSprouts(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("nether_sprouts", True)

    class NetherWart(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("nether_wart", True)

    class NetherWartBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("nether_wart_block", True)

    class NormalStoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("normal_stone_stairs", True)

    class Noteblock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("noteblock", True)

    class OakFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("oak_fence", True)

    class OakHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("oak_hanging_sign", True)

    class OakLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("oak_log", True)

    class OakStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("oak_stairs", True)

    class Observer(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, powered_bit:'BlockStates.PoweredBit'=None):
            self._facing_direction = facing_direction
            self._powered_bit = powered_bit
            super().__init__("observer", True)

    class Obsidian(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("obsidian", True)

    class OchreFroglight(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("ochre_froglight", True)

    class OrangeCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("orange_candle", True)

    class OrangeCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("orange_candle_cake", True)

    class OrangeCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("orange_carpet", True)

    class OrangeGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("orange_glazed_terracotta", True)

    class OrangeWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("orange_wool", True)

    class OxidizedCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("oxidized_copper", True)

    class OxidizedCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("oxidized_cut_copper", True)

    class OxidizedCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("oxidized_cut_copper_slab", True)

    class OxidizedCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("oxidized_cut_copper_stairs", True)

    class OxidizedDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("oxidized_double_cut_copper_slab", True)

    class PackedIce(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("packed_ice", True)

    class PackedMud(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("packed_mud", True)

    class PearlescentFroglight(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("pearlescent_froglight", True)

    class PinkCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("pink_candle", True)

    class PinkCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("pink_candle_cake", True)

    class PinkCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("pink_carpet", True)

    class PinkGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("pink_glazed_terracotta", True)

    class PinkPetals(_MinecraftBlock):
        def __init__(self, cardina_direction:'BlockStates.CardinalDirection'=None, growth:'BlockStates.Growth'=None):
            self._cardina_direction = cardina_direction
            self._growth = growth
            super().__init__("pink_petals", True)

    class PinkWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("pink_wool", True)

    class Piston(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("piston", True)

    class Pistonarmcollision(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("pistonArmCollision", True)

    class PistonArmCollision(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("piston_arm_collision", True)

    class PitcherCrop(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._growth = growth
            self._upper_block_bit = upper_block_bit
            super().__init__("pitcher_crop", True)

    class PitcherPlant(_MinecraftBlock):
        def __init__(self, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._upper_block_bit = upper_block_bit
            super().__init__("pitcher_plant", True)

    class Podzol(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("podzol", True)

    class PointedDripstone(_MinecraftBlock):
        def __init__(self, dripstone_thickness:'BlockStates.DripstoneThickness'=None, hanging:'BlockStates.Hanging'=None):
            self._dripstone_thickness = dripstone_thickness
            self._hanging = hanging
            super().__init__("pointed_dripstone", True)

    class PolishedAndesiteStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("polished_andesite_stairs", True)

    class PolishedBasalt(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("polished_basalt", True)

    class PolishedBlackstone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("polished_blackstone", True)

    class PolishedBlackstoneBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("polished_blackstone_bricks", True)

    class PolishedBlackstoneBrickDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("polished_blackstone_brick_double_slab", True)

    class PolishedBlackstoneBrickSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("polished_blackstone_brick_slab", True)

    class PolishedBlackstoneBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("polished_blackstone_brick_stairs", True)

    class PolishedBlackstoneBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("polished_blackstone_brick_wall", True)

    class PolishedBlackstoneButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("polished_blackstone_button", True)

    class PolishedBlackstoneDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("polished_blackstone_double_slab", True)

    class PolishedBlackstonePressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("polished_blackstone_pressure_plate", True)

    class PolishedBlackstoneSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("polished_blackstone_slab", True)

    class PolishedBlackstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("polished_blackstone_stairs", True)

    class PolishedBlackstoneWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("polished_blackstone_wall", True)

    class PolishedDeepslate(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("polished_deepslate", True)

    class PolishedDeepslateDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("polished_deepslate_double_slab", True)

    class PolishedDeepslateSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("polished_deepslate_slab", True)

    class PolishedDeepslateStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("polished_deepslate_stairs", True)

    class PolishedDeepslateWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east:'BlockStates.WallConnectionTypeEast'=None, wall_connection_type_north:'BlockStates.WallConnectionTypeNorth'=None, wall_connection_type_south:'BlockStates.WallConnectionTypeSouth'=None, wall_connection_type_west:'BlockStates.WallConnectionTypeWest'=None, wall_post_bit:'BlockStates.WallPostBit'=None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("polished_deepslate_wall", True)

    class PolishedDioriteStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("polished_diorite_stairs", True)

    class PolishedGraniteStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("polished_granite_stairs", True)

    class Portal(_MinecraftBlock):
        def __init__(self, portal_axis:'BlockStates.PortalAxis'=None):
            self._portal_axis = portal_axis
            super().__init__("portal", True)

    class Potatoes(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None):
            self._growth = growth
            super().__init__("potatoes", True)

    class PowderSnow(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("powder_snow", True)

    class PoweredComparator(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, output_lit_bit:'BlockStates.OutputLitBit'=None, output_subtract_bit:'BlockStates.OutputSubtractBit'=None):
            self._cardinal_direction = cardinal_direction
            self._output_lit_bit = output_lit_bit
            self._output_subtract_bit = output_subtract_bit
            super().__init__("powered_comparator", True)

    class PoweredRepeater(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, repeater_delay:'BlockStates.RepeaterDelay'=None):
            self._cardinal_direction = cardinal_direction
            self._repeater_delay = repeater_delay
            super().__init__("powered_repeater", True)

    class Prismarine(_MinecraftBlock):
        def __init__(self, prismarine_block_type:'BlockStates.PrismarineBlockType'=None):
            self._prismarine_block_type = prismarine_block_type
            super().__init__("prismarine", True)

    class PrismarineBricksStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("prismarine_bricks_stairs", True)

    class PrismarineStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("prismarine_stairs", True)

    class Pumpkin(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None):
            self._cardinal_direction = cardinal_direction
            super().__init__("pumpkin", True)

    class PumpkinStem(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None, growth:'BlockStates.Growth'=None):
            self._facing_direction = facing_direction
            self._growth = growth
            super().__init__("pumpkin_stem", True)

    class PurpleCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("purple_candle", True)

    class PurpleCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("purple_candle_cake", True)

    class PurpleCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("purple_carpet", True)

    class PurpleGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("purple_glazed_terracotta", True)

    class PurpleWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("purple_wool", True)

    class PurpurBlock(_MinecraftBlock):
        def __init__(self, chisel_type:'BlockStates.ChiselType'=None, pillar_axis:'BlockStates.PillarAxis'=None):
            self._chisel_type = chisel_type
            self._pillar_axis = pillar_axis
            super().__init__("purpur_block", True)

    class PurpurStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("purpur_stairs", True)

    class QuartzBlock(_MinecraftBlock):
        def __init__(self, chisel_type:'BlockStates.ChiselType'=None, pillar_axis:'BlockStates.PillarAxis'=None):
            self._chisel_type = chisel_type
            self._pillar_axis = pillar_axis
            super().__init__("quartz_block", True)

    class QuartzBricks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("quartz_bricks", True)

    class QuartzOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("quartz_ore", True)

    class QuartzStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("quartz_stairs", True)

    class Rail(_MinecraftBlock):
        def __init__(self, rail_direction:'BlockStates.RailDirection'=None):
            self._rail_direction = rail_direction
            super().__init__("rail", True)

    class RawCopperBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("raw_copper_block", True)

    class RawGoldBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("raw_gold_block", True)

    class RawIronBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("raw_iron_block", True)

    class RedstoneBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("redstone_block", True)

    class RedstoneLamp(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("redstone_lamp", True)

    class RedstoneOre(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("redstone_ore", True)

    class RedstoneTorch(_MinecraftBlock):
        def __init__(self, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("redstone_torch", True)

    class RedstoneWire(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("redstone_wire", True)

    class RedCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("red_candle", True)

    class RedCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("red_candle_cake", True)

    class RedCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("red_carpet", True)

    class RedFlower(_MinecraftBlock):
        def __init__(self, flower_type:'BlockStates.FlowerType'=None):
            self._flower_type = flower_type
            super().__init__("red_flower", True)

    class RedGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("red_glazed_terracotta", True)

    class RedMushroom(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("red_mushroom", True)

    class RedMushroomBlock(_MinecraftBlock):
        def __init__(self, huge_mushroom_bits:'BlockStates.HugeMushroomBits'=None):
            self._huge_mushroom_bits = huge_mushroom_bits
            super().__init__("red_mushroom_block", True)

    class RedNetherBrick(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("red_nether_brick", True)

    class RedNetherBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("red_nether_brick_stairs", True)

    class RedSandstone(_MinecraftBlock):
        def __init__(self, sand_stone_type:'BlockStates.SandStoneType'=None):
            self._sand_stone_type = sand_stone_type
            super().__init__("red_sandstone", True)

    class RedSandstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("red_sandstone_stairs", True)

    class RedWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("red_wool", True)

    class Reeds(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("reeds", True)

    class ReinforcedDeepslate(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("reinforced_deepslate", True)

    class RepeatingCommandBlock(_MinecraftBlock):
        def __init__(self, conditional_bit:'BlockStates.ConditionalBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._conditional_bit = conditional_bit
            self._facing_direction = facing_direction
            super().__init__("repeating_command_block", True)

    class Reserved6(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("reserved6", True)

    class RespawnAnchor(_MinecraftBlock):
        def __init__(self, respawn_anchor_charge:'BlockStates.RespawnAnchorCharge'=None):
            self._respawn_anchor_charge = respawn_anchor_charge
            super().__init__("respawn_anchor", True)

    class Sand(_MinecraftBlock):
        def __init__(self, sand_type:'BlockStates.SandType'=None):
            self._sand_type = sand_type
            super().__init__("sand", True)

    class Sandstone(_MinecraftBlock):
        def __init__(self, sand_stone_type:'BlockStates.SandStoneType'=None):
            self._sand_stone_type = sand_stone_type
            super().__init__("sandstone", True)

    class SandstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("sandstone_stairs", True)

    class Sapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None, sapling_type:'BlockStates.SaplingType'=None):
            self._age_bit = age_bit
            self._sapling_type = sapling_type
            super().__init__("sapling", True)

    class Scaffolding(_MinecraftBlock):
        def __init__(self, stability:'BlockStates.Stability'=None, stability_check:'BlockStates.StabilityCheck'=None):
            self._stability = stability
            self._stability_check = stability_check
            super().__init__("scaffolding", True)

    class Sculk(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("sculk", True)

    class SculkCatalyst(_MinecraftBlock):
        def __init__(self, bloom:'BlockStates.Bloom'=None):
            self._bloom = bloom
            super().__init__("sculk_catalyst", True)

    class SculkSensor(_MinecraftBlock):
        def __init__(self, sculk_sensor_phase:'BlockStates.SculkSensorPhase'=None):
            self._sculk_sensor_phase = sculk_sensor_phase
            super().__init__("sculk_sensor", True)

    class SculkShrieker(_MinecraftBlock):
        def __init__(self, active:'BlockStates.Active'=None, can_summon:'BlockStates.CanSummon'=None):
            self._active = active
            self._can_summon = can_summon
            super().__init__("sculk_shrieker", True)

    class SculkVein(_MinecraftBlock):
        def __init__(self, multi_face_direction_bits:'BlockStates.MultiFaceDirectionBits'=None):
            self._multi_face_direction_bits = multi_face_direction_bits
            super().__init__("sculk_vein", True)

    class Seagrass(_MinecraftBlock):
        def __init__(self, sea_grass_type:'BlockStates.SeaGrassType'=None):
            self._sea_grass_type = sea_grass_type
            super().__init__("seagrass", True)

    class SeaLantern(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("sea_lantern", True)

    class SeaPickle(_MinecraftBlock):
        def __init__(self, cluster_count:'BlockStates.ClusterCount'=None, dead_bit:'BlockStates.DeadBit'=None):
            self._cluster_count = cluster_count
            self._dead_bit = dead_bit
            super().__init__("sea_pickle", True)

    class Shroomlight(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("shroomlight", True)

    class ShulkerBox(_MinecraftBlock):
        def __init__(self, color:'BlockStates.Color'=None):
            self._color = color
            super().__init__("shulker_box", True)

    class SilverGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("silver_glazed_terracotta", True)

    class Skull(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("skull", True)

    class Slime(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("slime", True)

    class SmallAmethystBud(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("small_amethyst_bud", True)

    class SmallDripleafBlock(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._cardinal_direction = cardinal_direction
            self._upper_block_bit = upper_block_bit
            super().__init__("small_dripleaf_block", True)

    class SmithingTable(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("smithing_table", True)

    class Smoker(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("smoker", True)

    class SmoothBasalt(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("smooth_basalt", True)

    class SmoothQuartzStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("smooth_quartz_stairs", True)

    class SmoothRedSandstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("smooth_red_sandstone_stairs", True)

    class SmoothSandstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("smooth_sandstone_stairs", True)

    class SmoothStone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("smooth_stone", True)

    class SnifferEgg(_MinecraftBlock):
        def __init__(self, cracked_state:'BlockStates.CrackedState'=None):
            self._cracked_state = cracked_state
            super().__init__("sniffer_egg", True)

    class Snow(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("snow", True)

    class SnowLayer(_MinecraftBlock):
        def __init__(self, covered_bit:'BlockStates.CoveredBit'=None, height:'BlockStates.Height'=None):
            self._covered_bit = covered_bit
            self._height = height
            super().__init__("snow_layer", True)

    class SoulCampfire(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.CardinalDirection'=None, extinguished:'BlockStates.Extinguished'=None):
            self._direction = direction
            self._extinguished = extinguished
            super().__init__("soul_campfire", True)

    class SoulFire(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None):
            self._age = age
            super().__init__("soul_fire", True)

    class SoulLantern(_MinecraftBlock):
        def __init__(self, hanging:'BlockStates.Hanging'=None):
            self._hanging = hanging
            super().__init__("soul_lantern", True)

    class SoulSand(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("soul_sand", True)

    class SoulSoil(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("soul_soil", True)

    class SoulTorch(_MinecraftBlock):
        def __init__(self, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("soul_torch", True)

    class Sponge(_MinecraftBlock):
        def __init__(self, sponge_type:'BlockStates.SpongeType'=None):
            self._sponge_type = sponge_type
            super().__init__("sponge", True)

    class SporeBlossom(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("spore_blossom", True)

    class SpruceButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("spruce_button", True)

    class SpruceDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("spruce_door", True)

    class SpruceFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("spruce_fence", True)

    class SpruceFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("spruce_fence_gate", True)

    class SpruceHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("spruce_hanging_sign", True)

    class SpruceLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("spruce_log", True)

    class SprucePressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("spruce_pressure_plate", True)

    class SpruceStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("spruce_stairs", True)

    class SpruceStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("spruce_standing_sign", True)

    class SpruceTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("spruce_trapdoor", True)

    class SpruceWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("spruce_wall_sign", True)

    class StandingBanner(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("standing_banner", True)

    class StandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("standing_sign", True)

    class Stickypistonarmcollision(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("stickyPistonArmCollision", True)

    class StickyPiston(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("sticky_piston", True)

    class StickyPistonArmCollision(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("sticky_piston_arm_collision", True)

    class Stonebrick(_MinecraftBlock):
        def __init__(self, stone_brick_type:'BlockStates.StoneBrickType'=None):
            self._stone_brick_type = stone_brick_type
            super().__init__("stonebrick", True)

    class Stonecutter(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("stonecutter", True)

    class StonecutterBlock(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("stonecutter_block", True)

    class StoneBlockSlab(_MinecraftBlock):
        def __init__(self, stone_slab_type:'BlockStates.StoneSlabType'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type = stone_slab_type
            self._vertical_half = vertical_half
            super().__init__("stone_block_slab", True)

    class StoneBlockSlab2(_MinecraftBlock):
        def __init__(self, stone_slab_type_2:'BlockStates.StoneSlabType2'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type_2 = stone_slab_type_2
            self._vertical_half = vertical_half
            super().__init__("stone_block_slab2", True)

    class StoneBlockSlab3(_MinecraftBlock):
        def __init__(self, stone_slab_type_3:'BlockStates.StoneSlabType3'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type_3 = stone_slab_type_3
            self._vertical_half = vertical_half
            super().__init__("stone_block_slab3", True)

    class StoneBlockSlab4(_MinecraftBlock):
        def __init__(self, stone_slab_type_4:'BlockStates.StoneSlabType4'=None, vertical_half:'BlockStates.VerticalHalf'=None):
            self._stone_slab_type_4 = stone_slab_type_4
            self._vertical_half = vertical_half
            super().__init__("stone_block_slab4", True)

    class StoneBrickStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("stone_brick_stairs", True)

    class StoneButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("stone_button", True)

    class StonePressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("stone_pressure_plate", True)

    class StoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("stone_stairs", True)

    class StrippedAcaciaLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_acacia_log", True)

    class StrippedBambooBlock(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_bamboo_block", True)

    class StrippedBirchLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_birch_log", True)

    class StrippedCherryLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_cherry_log", True)

    class StrippedCherryWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_cherry_wood", True)

    class StrippedCrimsonHyphae(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_crimson_hyphae", True)

    class StrippedCrimsonStem(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_crimson_stem", True)

    class StrippedDarkOakLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_dark_oak_log", True)

    class StrippedJungleLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_jungle_log", True)

    class StrippedMangroveLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_mangrove_log", True)

    class StrippedMangroveWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_mangrove_wood", True)

    class StrippedOakLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_oak_log", True)

    class StrippedSpruceLog(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_spruce_log", True)

    class StrippedWarpedHyphae(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_warped_hyphae", True)

    class StrippedWarpedStem(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_warped_stem", True)

    class StructureBlock(_MinecraftBlock):
        def __init__(self, structure_block_type:'BlockStates.StructureBlockType'=None):
            self._structure_block_type = structure_block_type
            super().__init__("structure_block", True)

    class StructureVoid(_MinecraftBlock):
        def __init__(self, structure_void_type:'BlockStates.StructureVoidType'=None):
            self._structure_void_type = structure_void_type
            super().__init__("structure_void", True)

    class SuspiciousGravel(_MinecraftBlock):
        def __init__(self, brushed_progress:'BlockStates.BrushedProgress'=None, hanging:'BlockStates.Hanging'=None):
            self._brushed_progress = brushed_progress
            self._hanging = hanging
            super().__init__("suspicious_gravel", True)

    class SuspiciousSand(_MinecraftBlock):
        def __init__(self, brushed_progress:'BlockStates.BrushedProgress'=None, hanging:'BlockStates.Hanging'=None):
            self._brushed_progress = brushed_progress
            self._hanging = hanging
            super().__init__("suspicious_sand", True)

    class SweetBerryBush(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None):
            self._growth = growth
            super().__init__("sweet_berry_bush", True)

    class Tallgrass(_MinecraftBlock):
        def __init__(self, tall_grass_type:'BlockStates.TallGrassType'=None):
            self._tall_grass_type = tall_grass_type
            super().__init__("tallgrass", True)

    class Target(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("target", True)

    class TintedGlass(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("tinted_glass", True)

    class Tnt(_MinecraftBlock):
        def __init__(self, allow_underwater_bit:'BlockStates.AllowUnderwaterBit'=None, explode_bit:'BlockStates.ExplodeBit'=None):
            self._allow_underwater_bit = allow_underwater_bit
            self._explode_bit = explode_bit
            super().__init__("tnt", True)

    class Torch(_MinecraftBlock):
        def __init__(self, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("torch", True)

    class Torchflower(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("torchflower", True)

    class TorchflowerCrop(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None):
            self._growth = growth
            super().__init__("torchflower_crop", True)

    class Trapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("trapdoor", True)

    class TrappedChest(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("trapped_chest", True)

    class Tripwire(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, disarmed_bit:'BlockStates.DisarmedBit'=None, powered_bit:'BlockStates.PoweredBit'=None, suspended_bit:'BlockStates.SuspendedBit'=None):
            self._attached_bit = attached_bit
            self._disarmed_bit = disarmed_bit
            self._powered_bit = powered_bit
            self._suspended_bit = suspended_bit
            super().__init__("tripWire", True)

    class TripwireHook(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, direction:'BlockStates.Direction'=None, powered_bit:'BlockStates.PoweredBit'=None):
            self._attached_bit = attached_bit
            self._direction = direction
            self._powered_bit = powered_bit
            super().__init__("tripwire_hook", True)

    class TripWire(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, disarmed_bit:'BlockStates.DisarmedBit'=None, powered_bit:'BlockStates.PoweredBit'=None, suspended_bit:'BlockStates.SuspendedBit'=None):
            self._attached_bit = attached_bit
            self._disarmed_bit = disarmed_bit
            self._powered_bit = powered_bit
            self._suspended_bit = suspended_bit
            super().__init__("trip_wire", True)

    class TubeCoral(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("tube_coral", True)

    class Tuff(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("tuff", True)

    class TurtleEgg(_MinecraftBlock):
        def __init__(self, cracked_state:'BlockStates.CrackedState'=None, turtle_egg_count:'BlockStates.TurtleEggCount'=None):
            self._cracked_state = cracked_state
            self._turtle_egg_count = turtle_egg_count
            super().__init__("turtle_egg", True)

    class TwistingVines(_MinecraftBlock):
        def __init__(self, twisting_vines_age:'BlockStates.TwistingVinesAge'=None):
            self._twisting_vines_age = twisting_vines_age
            super().__init__("twisting_vines", True)

    class UnderwaterTorch(_MinecraftBlock):
        def __init__(self, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("underwater_torch", True)

    class UndyedShulkerBox(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("undyed_shulker_box", True)

    class Unknown(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("unknown", True)

    class UnlitRedstoneTorch(_MinecraftBlock):
        def __init__(self, torch_facing_direction:'BlockStates.TorchFacingDirection'=None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("unlit_redstone_torch", True)

    class UnpoweredComparator(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, output_lit_bit:'BlockStates.OutputLitBit'=None, output_subtract_bit:'BlockStates.OutputSubtractBit'=None):
            self._cardinal_direction = cardinal_direction
            self._output_lit_bit = output_lit_bit
            self._output_subtract_bit = output_subtract_bit
            super().__init__("unpowered_comparator", True)

    class UnpoweredRepeater(_MinecraftBlock):
        def __init__(self, cardinal_direction:'BlockStates.CardinalDirection'=None, repeater_delay:'BlockStates.RepeaterDelay'=None):
            self._cardinal_direction = cardinal_direction
            self._repeater_delay = repeater_delay
            super().__init__("unpowered_repeater", True)

    class VerdantFroglight(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("verdant_froglight", True)

    class Vine(_MinecraftBlock):
        def __init__(self, vine_direction_bits:'BlockStates.VineDirectionBits'=None):
            self._vine_direction_bits = vine_direction_bits
            super().__init__("vine", True)

    class WallBanner(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("wall_banner", True)

    class WallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("wall_sign", True)

    class WarpedButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("warped_button", True)

    class WarpedDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("warped_door", True)

    class WarpedDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("warped_double_slab", True)

    class WarpedFence(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("warped_fence", True)

    class WarpedFenceGate(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, in_wall_bit:'BlockStates.InWallBit'=None, open_bit:'BlockStates.OpenBit'=None):
            self._direction = direction
            self._in_wall_bit = in_wall_bit
            self._open_bit = open_bit
            super().__init__("warped_fence_gate", True)

    class WarpedFungus(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("warped_fungus", True)

    class WarpedHangingSign(_MinecraftBlock):
        def __init__(self, attached_bit:'BlockStates.AttachedBit'=None, facing_direction:'BlockStates.FacingDirection'=None, ground_sign_direction:'BlockStates.GroundSignDirection'=None, hanging:'BlockStates.Hanging'=None):
            self._attached_bit = attached_bit
            self._facing_direction = facing_direction
            self._ground_sign_direction = ground_sign_direction
            self._hanging = hanging
            super().__init__("warped_hanging_sign", True)

    class WarpedHyphae(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("warped_hyphae", True)

    class WarpedNylium(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("warped_nylium", True)

    class WarpedPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("warped_planks", True)

    class WarpedPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("warped_pressure_plate", True)

    class WarpedRoots(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("warped_roots", True)

    class WarpedSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("warped_slab", True)

    class WarpedStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("warped_stairs", True)

    class WarpedStandingSign(_MinecraftBlock):
        def __init__(self, ground_sign_direction:'BlockStates.GroundSignDirection'=None):
            self._ground_sign_direction = ground_sign_direction
            super().__init__("warped_standing_sign", True)

    class WarpedStem(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("warped_stem", True)

    class WarpedTrapdoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, open_bit:'BlockStates.OpenBit'=None, upside_down_bit:'BlockStates.UpsideDownBit'=None):
            self._direction = direction
            self._open_bit = open_bit
            self._upside_down_bit = upside_down_bit
            super().__init__("warped_trapdoor", True)

    class WarpedWallSign(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("warped_wall_sign", True)

    class WarpedWartBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("warped_wart_block", True)

    class Water(_MinecraftBlock):
        def __init__(self, liquid_depth:'BlockStates.LiquidDepth'=None):
            self._liquid_depth = liquid_depth
            super().__init__("water", True)

    class Waterlily(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waterlily", True)

    class WaxedCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_copper", True)

    class WaxedCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_cut_copper", True)

    class WaxedCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_cut_copper_slab", True)

    class WaxedCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("waxed_cut_copper_stairs", True)

    class WaxedDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_double_cut_copper_slab", True)

    class WaxedExposedCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_exposed_copper", True)

    class WaxedExposedCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_exposed_cut_copper", True)

    class WaxedExposedCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_exposed_cut_copper_slab", True)

    class WaxedExposedCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("waxed_exposed_cut_copper_stairs", True)

    class WaxedExposedDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_exposed_double_cut_copper_slab", True)

    class WaxedOxidizedCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_oxidized_copper", True)

    class WaxedOxidizedCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_oxidized_cut_copper", True)

    class WaxedOxidizedCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_oxidized_cut_copper_slab", True)

    class WaxedOxidizedCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("waxed_oxidized_cut_copper_stairs", True)

    class WaxedOxidizedDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_oxidized_double_cut_copper_slab", True)

    class WaxedWeatheredCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_weathered_copper", True)

    class WaxedWeatheredCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("waxed_weathered_cut_copper", True)

    class WaxedWeatheredCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_weathered_cut_copper_slab", True)

    class WaxedWeatheredCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("waxed_weathered_cut_copper_stairs", True)

    class WaxedWeatheredDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("waxed_weathered_double_cut_copper_slab", True)

    class WeatheredCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("weathered_copper", True)

    class WeatheredCutCopper(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("weathered_cut_copper", True)

    class WeatheredCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("weathered_cut_copper_slab", True)

    class WeatheredCutCopperStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("weathered_cut_copper_stairs", True)

    class WeatheredDoubleCutCopperSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("weathered_double_cut_copper_slab", True)

    class Web(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("web", True)

    class WeepingVines(_MinecraftBlock):
        def __init__(self, weeping_vines_age:'BlockStates.WeepingVinesAge'=None):
            self._weeping_vines_age = weeping_vines_age
            super().__init__("weeping_vines", True)

    class Wheat(_MinecraftBlock):
        def __init__(self, growth:'BlockStates.Growth'=None):
            self._growth = growth
            super().__init__("wheat", True)

    class WhiteCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("white_candle", True)

    class WhiteCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("white_candle_cake", True)

    class WhiteCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("white_carpet", True)

    class WhiteGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("white_glazed_terracotta", True)

    class WhiteWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("white_wool", True)

    class WitherRose(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("wither_rose", True)

    class Wood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None, stripped_bit:'BlockStates.StrippedBit'=None, wood_type:'BlockStates.WoodType'=None):
            self._pillar_axis = pillar_axis
            self._stripped_bit = stripped_bit
            self._wood_type = wood_type
            super().__init__("wood", True)

    class WoodenButton(_MinecraftBlock):
        def __init__(self, button_pressed_bit:'BlockStates.ButtonPressedBit'=None, facing_direction:'BlockStates.FacingDirection'=None):
            self._button_pressed_bit = button_pressed_bit
            self._facing_direction = facing_direction
            super().__init__("wooden_button", True)

    class WoodenDoor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None, door_hinge_bit:'BlockStates.DoorHingeBit'=None, open_bit:'BlockStates.OpenBit'=None, upper_block_bit:'BlockStates.UpperBlockBit'=None):
            self._direction = direction
            self._door_hinge_bit = door_hinge_bit
            self._open_bit = open_bit
            self._upper_block_bit = upper_block_bit
            super().__init__("wooden_door", True)

    class WoodenPressurePlate(_MinecraftBlock):
        def __init__(self, redstone_signal:'BlockStates.RedstoneSignal'=None):
            self._redstone_signal = redstone_signal
            super().__init__("wooden_pressure_plate", True)

    class WoodenSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None, wood_type:'BlockStates.WoodType'=None):
            self._vertical_half = vertical_half
            self._wood_type = wood_type
            super().__init__("wooden_slab", True)

    class YellowCandle(_MinecraftBlock):
        def __init__(self, candles:'BlockStates.Candles'=None, lit:'BlockStates.Lit'=None):
            self._candles = candles
            self._lit = lit
            super().__init__("yellow_candle", True)

    class YellowCandleCake(_MinecraftBlock):
        def __init__(self, lit:'BlockStates.Lit'=None):
            self._lit = lit
            super().__init__("yellow_candle_cake", True)

    class YellowCarpet(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("yellow_carpet", True)

    class YellowFlower(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("yellow_flower", True)

    class YellowGlazedTerracotta(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("yellow_glazed_terracotta", True)

    class YellowWool(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("yellow_wool", True)

    # 1.20.30.1
    # Too repetitive, thanks ChatGPT
    # Terracotta
    class WhiteTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("white_terracotta", True)
            
    class OrangeTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("orange_terracotta", True)
            
    class MagentaTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("magenta_terracotta", True)
            
    class Light_blueTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_blue_terracotta", True)
            
    class YellowTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("yellow_terracotta", True)
            
    class LimeTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("lime_terracotta", True)
            
    class PinkTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("pink_terracotta", True)
            
    class GrayTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("gray_terracotta", True)
            
    class Light_grayTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_gray_terracotta", True)
            
    class CyanTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("cyan_terracotta", True)
            
    class PurpleTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("purple_terracotta", True)
            
    class BlueTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("blue_terracotta", True)
            
    class BrownTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("brown_terracotta", True)
            
    class GreenTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("green_terracotta", True)
            
    class RedTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_terracotta", True)
            
    class BlackTerracotta(_MinecraftBlock):
        def __init__(self):
            super().__init__("black_terracotta", True)

    # StainedGlass
    class WhiteStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("white_stained_glass", True)

    class OrangeStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("orange_stained_glass", True)

    class MagentaStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("magenta_stained_glass", True)

    class LightBlueStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_blue_stained_glass", True)

    class YellowStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("yellow_stained_glass", True)

    class LimeStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("lime_stained_glass", True)

    class PinkStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("pink_stained_glass", True)

    class GrayStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("gray_stained_glass", True)

    class LightGrayStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_gray_stained_glass", True)

    class CyanStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("cyan_stained_glass", True)

    class PurpleStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("purple_stained_glass", True)

    class BlueStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("blue_stained_glass", True)

    class BrownStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("brown_stained_glass", True)

    class GreenStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("green_stained_glass", True)

    class RedStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_stained_glass", True)

    class BlackStainedGlass(_MinecraftBlock):
        def __init__(self):
            super().__init__("black_stained_glass", True)

    # Stained Glass Pane
    class WhiteStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("white_stained_glass_pane", True)

    class OrangeStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("orange_stained_glass_pane", True)

    class MagentaStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("magenta_stained_glass_pane", True)

    class LightBlueStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_blue_stained_glass_pane", True)

    class YellowStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("yellow_stained_glass_pane", True)

    class LimeStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("lime_stained_glass_pane", True)

    class PinkStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("pink_stained_glass_pane", True)

    class GrayStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("gray_stained_glass_pane", True)

    class LightGrayStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_gray_stained_glass_pane", True)

    class CyanStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("cyan_stained_glass_pane", True)

    class PurpleStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("purple_stained_glass_pane", True)

    class BlueStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("blue_stained_glass_pane", True)

    class BrownStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("brown_stained_glass_pane", True)

    class GreenStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("green_stained_glass_pane", True)

    class RedStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_stained_glass_pane", True)

    class BlackStainedGlassPane(_MinecraftBlock):
        def __init__(self):
            super().__init__("black_stained_glass_pane", True)

    # Concrete Powder
    class WhiteConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("white_concrete_powder", True)
            
    class OrangeConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("orange_concrete_powder", True)

    class MagentaConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("magenta_concrete_powder", True)

    class LightBlueConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("light_blue_concrete_powder", True)
            
    class YellowConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("yellow_concrete_powder", True)
            
    class LimeConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("lime_concrete_powder", True)
            
    class PinkConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("pink_concrete_powder", True)
            
    class GrayConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("gray_concrete_powder", True)
            
    class LightGrayConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("light_gray_concrete_powder", True)
            
    class CyanConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("cyan_concrete_powder", True)
            
    class PurpleConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("purple_concrete_powder", True)
            
    class BlueConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("blue_concrete_powder", True)
            
    class BrownConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("brown_concrete_powder", True)
            
    class GreenConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("green_concrete_powder", True)
            
    class RedConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("red_concrete_powder", True)
            
    class BlackConcretePowder(_MinecraftBlock):
        def __init__(self,):
            super().__init__("black_concrete_powder", True)

    # Added in 1.20.50
    # Planks
    class OakPlans(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("oak_planks", True)

    class SprucePlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("spruce_planks", True)

    class BirchPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("birch_planks", True)

    class JunglePlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("jungle_planks", True)

    class AcaciaPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("acacia_planks", True)

    class DarkOakPlanks(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dark_oak_planks", True)
    
    # Stones
    class Stone(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("stone", True)

    class Granite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("granite", True)

    class Diorite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("diorite", True)

    class Andesite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("andesite", True)

    class PolishedGranite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("polished_granite", True)

    class PolishedDiorite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("polished_diorite", True)

    class PolishedAndesite(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("polished_andesite", True)

# Take all the subclasses of Blocks and add them to BLOCK_LIST
BLOCK_LIST = []
for block in Blocks.__dict__.values():
    if isinstance(block, type) and issubclass(block, Blocks._MinecraftBlock) and block is not Blocks._MinecraftBlock:
        BLOCK_LIST.append(block())
