from enum import StrEnum
from typing import Literal, Optional, TypeAlias

from anvil.lib.schemas import MinecraftBlockDescriptor

Active: TypeAlias = Literal["0b", "1b"]
Age: TypeAlias = Literal[
    "12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"
]
AgeBit: TypeAlias = Literal["0b", "1b"]
AllowUnderwaterBit: TypeAlias = Literal["0b", "1b"]
AttachedBit: TypeAlias = Literal["0b", "1b"]
Attachment: TypeAlias = Literal["standing", "side", "multiple", "hanging"]
BambooLeafSize: TypeAlias = Literal["no_leaves", "small_leaves", "large_leaves"]
BambooStalkThickness: TypeAlias = Literal["thin", "thick"]
BigDripleafHead: TypeAlias = Literal["0b", "1b"]
BigDripleafTilt: TypeAlias = Literal["none", "unstable", "partial_tilt", "full_tilt"]
BiteCounter: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6"]
BlockFace: TypeAlias = Literal["down", "up", "north", "south", "east", "west"]
Bloom: TypeAlias = Literal["0b", "1b"]
BooksStored: TypeAlias = Literal[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "60",
    "61",
    "62",
    "63",
]
BrewingStandSlotABit: TypeAlias = Literal["0b", "1b"]
BrewingStandSlotBBit: TypeAlias = Literal["0b", "1b"]
BrewingStandSlotCBit: TypeAlias = Literal["0b", "1b"]
BrushedProgress: TypeAlias = Literal["0", "2", "1", "3"]
ButtonPressedBit: TypeAlias = Literal["0b", "1b"]
CanSummon: TypeAlias = Literal["0b", "1b"]
Candles: TypeAlias = Literal["0", "2", "1", "3"]
CardinalDirection: TypeAlias = Literal["south", "west", "north", "east"]
CauldronLiquid: TypeAlias = Literal["water", "lava", "powder_snow"]
ChiselType: TypeAlias = Literal["chiseled", "default", "smooth", "lines"]
ClusterCount: TypeAlias = Literal["0", "1", "2", "3"]
Color: TypeAlias = Literal[
    "black",
    "silver",
    "red",
    "orange",
    "lime",
    "pink",
    "purple",
    "magenta",
    "light_blue",
    "yellow",
    "gray",
    "cyan",
    "white",
    "blue",
    "green",
    "brown",
]
ColorBit: TypeAlias = Literal["0b", "1b"]
ComposterFillLevel: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8"]
ConditionalBit: TypeAlias = Literal["0b", "1b"]
CoralColor: TypeAlias = Literal["red", "pink", "purple", "yellow", "blue"]
CoralDirection: TypeAlias = Literal["0", "2", "1", "3"]
CoralFanDirection: TypeAlias = Literal["0", "1"]
CoralHangTypeBit: TypeAlias = Literal["0b", "1b"]
CoveredBit: TypeAlias = Literal["0b", "1b"]
CrackedState: TypeAlias = Literal["max_cracked", "cracked", "no_cracks"]
Crafting: TypeAlias = Literal["0b", "1b"]
Damage: TypeAlias = Literal["undamaged", "slightly_damaged", "very_damaged", "broken"]
DeadBit: TypeAlias = Literal["0b", "1b"]
Deprecated: TypeAlias = Literal["0", "2", "1", "3"]
Direction: TypeAlias = Literal["0", "2", "1", "3"]
DirtType: TypeAlias = Literal["normal", "coarse"]
DisarmedBit: TypeAlias = Literal["0b", "1b"]
DoorHingeBit: TypeAlias = Literal["0b", "1b"]
DragDown: TypeAlias = Literal["0b", "1b"]
DripstoneThickness: TypeAlias = Literal["tip", "frustum", "middle", "base", "merge"]
EndPortalEyeBit: TypeAlias = Literal["0b", "1b"]
ExplodeBit: TypeAlias = Literal["0b", "1b"]
Extinguished: TypeAlias = Literal["0b", "1b"]
FacingDirection: TypeAlias = Literal["5", "4", "0", "1", "2", "3"]
FillLevel: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6"]
FlowerType: TypeAlias = Literal[
    "poppy",
    "orchid",
    "allium",
    "houstonia",
    "tulip_red",
    "tulip_orange",
    "tulip_white",
    "tulip_pink",
    "oxeye",
    "cornflower",
    "lily_of_the_valley",
]
GroundSignDirection: TypeAlias = Literal[
    "12", "10", "5", "7", "13", "9", "4", "11", "0", "6", "14", "1", "2", "3", "8", "15"
]
GrowingPlantAge: TypeAlias = Literal[
    "22",
    "0",
    "23",
    "15",
    "17",
    "9",
    "4",
    "16",
    "19",
    "8",
    "11",
    "5",
    "24",
    "13",
    "18",
    "6",
    "2",
    "3",
    "7",
    "20",
    "12",
    "10",
    "21",
    "25",
    "14",
    "1",
]
Growth: TypeAlias = Literal["5", "4", "0", "6", "1", "2", "3", "7"]
Hanging: TypeAlias = Literal["0b", "1b"]
HeadPieceBit: TypeAlias = Literal["0b", "1b"]
Height: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7"]
HoneyLevel: TypeAlias = Literal["5", "4", "0", "1", "2", "3"]
HugeMushroomBits: TypeAlias = Literal[
    "12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"
]
InWallBit: TypeAlias = Literal["0b", "1b"]
InfiniburnBit: TypeAlias = Literal["0b", "1b"]
ItemFrameMapBit: TypeAlias = Literal["0b", "1b"]
ItemFramePhotoBit: TypeAlias = Literal["0b", "1b"]
KelpAge: TypeAlias = Literal[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
]
LeverDirection: TypeAlias = Literal[
    "down_east_west",
    "east",
    "west",
    "south",
    "north",
    "up_north_south",
    "up_east_west",
    "down_north_south",
]
LiquidDepth: TypeAlias = Literal[
    "12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"
]
Lit: TypeAlias = Literal["0b", "1b"]
MoisturizedAmount: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7"]
MultiFaceDirectionBits: TypeAlias = Literal[
    "35",
    "22",
    "62",
    "45",
    "0",
    "36",
    "53",
    "30",
    "59",
    "47",
    "23",
    "15",
    "50",
    "17",
    "9",
    "4",
    "16",
    "27",
    "60",
    "32",
    "33",
    "19",
    "8",
    "26",
    "31",
    "11",
    "38",
    "46",
    "58",
    "5",
    "24",
    "13",
    "18",
    "40",
    "54",
    "63",
    "42",
    "6",
    "29",
    "43",
    "52",
    "2",
    "3",
    "41",
    "44",
    "7",
    "20",
    "51",
    "12",
    "10",
    "21",
    "61",
    "56",
    "25",
    "57",
    "55",
    "34",
    "14",
    "1",
    "39",
    "28",
    "49",
    "37",
    "48",
]
NewLeafType: TypeAlias = Literal["acacia", "dark_oak"]
OccupiedBit: TypeAlias = Literal["0b", "1b"]
OldLeafType: TypeAlias = Literal["oak", "spruce", "birch", "jungle"]
OpenBit: TypeAlias = Literal["0b", "1b"]
OutputLitBit: TypeAlias = Literal["0b", "1b"]
OutputSubtractBit: TypeAlias = Literal["0b", "1b"]
PersistentBit: TypeAlias = Literal["0b", "1b"]
PillarAxis: TypeAlias = Literal["z", "x", "y"]
PortalAxis: TypeAlias = Literal["unknown", "x", "z"]
PoweredBit: TypeAlias = Literal["0b", "1b"]
PrismarineBlockType: TypeAlias = Literal["default", "dark", "bricks"]
PropaguleStage: TypeAlias = Literal["0", "1", "2", "3", "4"]
RailDataBit: TypeAlias = Literal["0b", "1b"]
RailDirection: TypeAlias = Literal["5", "9", "4", "0", "6", "1", "8", "2", "3", "7"]
RedstoneSignal: TypeAlias = Literal[
    "12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"
]
RepeaterDelay: TypeAlias = Literal["0", "2", "1", "3"]
RespawnAnchorCharge: TypeAlias = Literal["0", "1", "2", "3", "4"]
Rotation: TypeAlias = Literal["0", "1", "2", "3"]
SandStoneType: TypeAlias = Literal["heiroglyphs", "default", "cut", "smooth"]
SandType: TypeAlias = Literal["normal", "red"]
SaplingType: TypeAlias = Literal[
    "dark_oak", "acacia", "spruce", "birch", "jungle", "oak"
]
SculkSensorPhase: TypeAlias = Literal["0", "2", "1"]
SeaGrassType: TypeAlias = Literal["default", "double_top", "double_bot"]
SpongeType: TypeAlias = Literal["dry", "wet"]
Stability: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7"]
StabilityCheck: TypeAlias = Literal["0b", "1b"]
StoneBrickType: TypeAlias = Literal["default", "mossy", "cracked", "chiseled", "smooth"]
StoneType: TypeAlias = Literal[
    "stone",
    "granite",
    "granite_smooth",
    "diorite",
    "diorite_smooth",
    "andesite",
    "andesite_smooth",
]
StrippedBit: TypeAlias = Literal["0b", "1b"]
StructureBlockType: TypeAlias = Literal[
    "data", "save", "load", "corner", "invalid", "export"
]
StructureVoidType: TypeAlias = Literal["void", "air"]
SuspendedBit: TypeAlias = Literal["0b", "1b"]
ToggleBit: TypeAlias = Literal["0b", "1b"]
TopSlotBit: TypeAlias = Literal["0b", "1b"]
TorchFacingDirection: TypeAlias = Literal[
    "unknown", "west", "south", "north", "east", "top"
]
TrialSpawnerState: TypeAlias = Literal["5", "4", "3", "2", "1", "0"]
TriggeredBit: TypeAlias = Literal["0b", "1b"]
TurtleEggCount: TypeAlias = Literal["one_egg", "two_egg", "three_egg", "four_egg"]
TwistingVinesAge: TypeAlias = Literal[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
]
UpdateBit: TypeAlias = Literal["0b", "1b"]
UpperBlockBit: TypeAlias = Literal["0b", "1b"]
UpsideDownBit: TypeAlias = Literal["0b", "1b"]
VaultState: TypeAlias = Literal["active", "ejecting", "interactive", "unlocking"]
VerticalHalf: TypeAlias = Literal["bottom", "top"]
VineDirectionBits: TypeAlias = Literal[
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"
]
WallBlockType: TypeAlias = Literal[
    "cobblestone",
    "mossy_cobblestone",
    "granite",
    "diorite",
    "andesite",
    "sandstone",
    "brick",
    "stone_brick",
    "mossy_stone_brick",
    "nether_brick",
    "end_brick",
    "prismarine",
    "red_sandstone",
    "red_nether_brick",
]
WallConnectionTypeEast: TypeAlias = Literal["tall", "none", "short"]
WallConnectionTypeNorth: TypeAlias = Literal["tall", "none", "short"]
WallConnectionTypeSouth: TypeAlias = Literal["tall", "none", "short"]
WallConnectionTypeWest: TypeAlias = Literal["tall", "none", "short"]
WallPostBit: TypeAlias = Literal["0b", "1b"]
WeepingVinesAge: TypeAlias = Literal[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
]
WeirdoDirection: TypeAlias = Literal["0", "2", "1", "3"]
WoodType: TypeAlias = Literal["dark_oak", "acacia", "spruce", "birch", "jungle", "oak"]
Orientation: TypeAlias = Literal[
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"
]
CreakingHeartState: TypeAlias = Literal["0b", "1b"]
Natural: TypeAlias = Literal["0b", "1b"]
RehydrationLevel: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7"]
Tip: TypeAlias = Literal["0b", "1b"]
PaleMossCarpetSideEast: TypeAlias = Literal["none", "short", "tall"]
PaleMossCarpetSideNorth: TypeAlias = Literal["none", "short", "tall"]
PaleMossCarpetSideSouth: TypeAlias = Literal["none", "short", "tall"]
PaleMossCarpetSideWest: TypeAlias = Literal["none", "short", "tall"]
Ominous: TypeAlias = Literal["0b", "1b"]


class BlockStateKeys(StrEnum):
    Active = "active"
    Age = "age"
    AgeBit = "age_bit"
    AllowUnderwaterBit = "allow_underwater_bit"
    AttachedBit = "attached_bit"
    Attachment = "attachment"
    BambooLeafSize = "bamboo_leaf_size"
    BambooStalkThickness = "bamboo_stalk_thickness"
    BigDripleafHead = "big_dripleaf_head"
    BigDripleafTilt = "big_dripleaf_tilt"
    BiteCounter = "bite_counter"
    BlockLightLevel = "block_light_level"
    Bloom = "bloom"
    BooksStored = "books_stored"
    BrewingStandSlotABit = "brewing_stand_slot_a_bit"
    BrewingStandSlotBBit = "brewing_stand_slot_b_bit"
    BrewingStandSlotCBit = "brewing_stand_slot_c_bit"
    BrushedProgress = "brushed_progress"
    ButtonPressedBit = "button_pressed_bit"
    CanSummon = "can_summon"
    Candles = "candles"
    CauldronLiquid = "cauldron_liquid"
    ChemistryTableType = "chemistry_table_type"
    ChiselType = "chisel_type"
    ClusterCount = "cluster_count"
    Color = "color"
    ColorBit = "color_bit"
    ComposterFillLevel = "composter_fill_level"
    ConditionalBit = "conditional_bit"
    CoralColor = "coral_color"
    CoralDirection = "coral_direction"
    CoralFanDirection = "coral_fan_direction"
    CoralHangTypeBit = "coral_hang_type_bit"
    CoveredBit = "covered_bit"
    CrackedState = "cracked_state"
    Crafting = "crafting"
    CreakingHeartState = "creaking_heart_state"
    Damage = "damage"
    DeadBit = "dead_bit"
    Deprecated = "deprecated"
    Direction = "direction"
    DirtType = "dirt_type"
    DisarmedBit = "disarmed_bit"
    DoorHingeBit = "door_hinge_bit"
    DoublePlantType = "double_plant_type"
    DragDown = "drag_down"
    DripstoneThickness = "dripstone_thickness"
    EndPortalEyeBit = "end_portal_eye_bit"
    ExplodeBit = "explode_bit"
    Extinguished = "extinguished"
    FacingDirection = "facing_direction"
    FillLevel = "fill_level"
    FlowerType = "flower_type"
    GroundSignDirection = "ground_sign_direction"
    GrowingPlantAge = "growing_plant_age"
    Growth = "growth"
    Hanging = "hanging"
    HeadPieceBit = "head_piece_bit"
    Height = "height"
    HoneyLevel = "honey_level"
    HugeMushroomBits = "huge_mushroom_bits"
    InWallBit = "in_wall_bit"
    InfiniburnBit = "infiniburn_bit"
    ItemFrameMapBit = "item_frame_map_bit"
    ItemFramePhotoBit = "item_frame_photo_bit"
    KelpAge = "kelp_age"
    LeverDirection = "lever_direction"
    LiquidDepth = "liquid_depth"
    Lit = "lit"
    MinecraftBlockFace = "minecraft:block_face"
    MinecraftCardinalDirection = "minecraft:cardinal_direction"
    MinecraftFacingDirection = "minecraft:facing_direction"
    MinecraftVerticalHalf = "minecraft:vertical_half"
    MoisturizedAmount = "moisturized_amount"
    MonsterEggStoneType = "monster_egg_stone_type"
    MultiFaceDirectionBits = "multi_face_direction_bits"
    Natural = "natural"
    NewLeafType = "new_leaf_type"
    NewLogType = "new_log_type"
    NoDropBit = "no_drop_bit"
    OccupiedBit = "occupied_bit"
    OldLeafType = "old_leaf_type"
    OldLogType = "old_log_type"
    Ominous = "ominous"
    OpenBit = "open_bit"
    Orientation = "orientation"
    OutputLitBit = "output_lit_bit"
    OutputSubtractBit = "output_subtract_bit"
    PaleMossCarpetSideEast = "pale_moss_carpet_side_east"
    PaleMossCarpetSideNorth = "pale_moss_carpet_side_north"
    PaleMossCarpetSideSouth = "pale_moss_carpet_side_south"
    PaleMossCarpetSideWest = "pale_moss_carpet_side_west"
    PersistentBit = "persistent_bit"
    PillarAxis = "pillar_axis"
    PortalAxis = "portal_axis"
    PoweredBit = "powered_bit"
    PoweredShelfType = "powered_shelf_type"
    PrismarineBlockType = "prismarine_block_type"
    PropaguleStage = "propagule_stage"
    RailDataBit = "rail_data_bit"
    RailDirection = "rail_direction"
    RedstoneSignal = "redstone_signal"
    RehydrationLevel = "rehydration_level"
    RepeaterDelay = "repeater_delay"
    RespawnAnchorCharge = "respawn_anchor_charge"
    Rotation = "rotation"
    SandStoneType = "sand_stone_type"
    SandType = "sand_type"
    SaplingType = "sapling_type"
    SculkSensorPhase = "sculk_sensor_phase"
    SeaGrassType = "sea_grass_type"
    SpongeType = "sponge_type"
    Stability = "stability"
    StabilityCheck = "stability_check"
    StoneBrickType = "stone_brick_type"
    StoneSlabType = "stone_slab_type"
    StoneSlabType2 = "stone_slab_type_2"
    StoneSlabType3 = "stone_slab_type_3"
    StoneSlabType4 = "stone_slab_type_4"
    StoneType = "stone_type"
    StrippedBit = "stripped_bit"
    StructureBlockType = "structure_block_type"
    StructureVoidType = "structure_void_type"
    SuspendedBit = "suspended_bit"
    TallGrassType = "tall_grass_type"
    Tip = "tip"
    ToggleBit = "toggle_bit"
    TopSlotBit = "top_slot_bit"
    TorchFacingDirection = "torch_facing_direction"
    TrialSpawnerState = "trial_spawner_state"
    TriggeredBit = "triggered_bit"
    TurtleEggCount = "turtle_egg_count"
    TwistingVinesAge = "twisting_vines_age"
    UpdateBit = "update_bit"
    UpperBlockBit = "upper_block_bit"
    UpsideDownBit = "upside_down_bit"
    VaultState = "vault_state"
    VineDirectionBits = "vine_direction_bits"
    WallBlockType = "wall_block_type"
    WallConnectionTypeEast = "wall_connection_type_east"
    WallConnectionTypeNorth = "wall_connection_type_north"
    WallConnectionTypeSouth = "wall_connection_type_south"
    WallConnectionTypeWest = "wall_connection_type_west"
    WallPostBit = "wall_post_bit"
    WeepingVinesAge = "weeping_vines_age"
    WeirdoDirection = "weirdo_direction"
    WoodType = "wood_type"


def AcaciaButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaButton"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def AcaciaDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def AcaciaDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def AcaciaFence() -> MinecraftBlockDescriptor:
    """Factory for AcaciaFence"""
    return MinecraftBlockDescriptor("minecraft:acacia_fence", True)


def AcaciaFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def AcaciaHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def AcaciaLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def AcaciaLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for AcaciaLog"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def AcaciaPlanks() -> MinecraftBlockDescriptor:
    """Factory for AcaciaPlanks"""
    return MinecraftBlockDescriptor("minecraft:acacia_planks", True)


def AcaciaPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def AcaciaSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for AcaciaSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def AcaciaShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def AcaciaSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def AcaciaStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def AcaciaStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def AcaciaTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def AcaciaWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AcaciaWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def AcaciaWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for AcaciaWood"""
    return MinecraftBlockDescriptor(
        "minecraft:acacia_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def ActivatorRail(
    rail_data_bit: Optional[RailDataBit] = None,
    rail_direction: Optional[RailDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ActivatorRail"""
    return MinecraftBlockDescriptor(
        "minecraft:activator_rail",
        True,
        {
            BlockStateKeys.RailDataBit: rail_data_bit,
            BlockStateKeys.RailDirection: rail_direction,
        },
    )


def Air() -> MinecraftBlockDescriptor:
    """Factory for Air"""
    return MinecraftBlockDescriptor("minecraft:air", True)


def Allium() -> MinecraftBlockDescriptor:
    """Factory for Allium"""
    return MinecraftBlockDescriptor("minecraft:allium", True)


def Allow() -> MinecraftBlockDescriptor:
    """Factory for Allow"""
    return MinecraftBlockDescriptor("minecraft:allow", True)


def AmethystBlock() -> MinecraftBlockDescriptor:
    """Factory for AmethystBlock"""
    return MinecraftBlockDescriptor("minecraft:amethyst_block", True)


def AmethystCluster(
    minecraft_block_face: Optional[BlockFace] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AmethystCluster"""
    return MinecraftBlockDescriptor(
        "minecraft:amethyst_cluster",
        True,
        {BlockStateKeys.MinecraftBlockFace: minecraft_block_face},
    )


def AncientDebris() -> MinecraftBlockDescriptor:
    """Factory for AncientDebris"""
    return MinecraftBlockDescriptor("minecraft:ancient_debris", True)


def Andesite() -> MinecraftBlockDescriptor:
    """Factory for Andesite"""
    return MinecraftBlockDescriptor("minecraft:andesite", True)


def AndesiteDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AndesiteDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:andesite_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def AndesiteSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AndesiteSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:andesite_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def AndesiteStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AndesiteStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:andesite_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def AndesiteWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AndesiteWall"""
    return MinecraftBlockDescriptor(
        "minecraft:andesite_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Anvil(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Anvil"""
    return MinecraftBlockDescriptor(
        "minecraft:anvil",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def Azalea() -> MinecraftBlockDescriptor:
    """Factory for Azalea"""
    return MinecraftBlockDescriptor("minecraft:azalea", True)


def AzaleaLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AzaleaLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:azalea_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def AzaleaLeavesFlowered(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for AzaleaLeavesFlowered"""
    return MinecraftBlockDescriptor(
        "minecraft:azalea_leaves_flowered",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def AzureBluet() -> MinecraftBlockDescriptor:
    """Factory for AzureBluet"""
    return MinecraftBlockDescriptor("minecraft:azure_bluet", True)


def Bamboo(
    age_bit: Optional[AgeBit] = None,
    bamboo_leaf_size: Optional[BambooLeafSize] = None,
    bamboo_stalk_thickness: Optional[BambooStalkThickness] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Bamboo"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo",
        True,
        {
            BlockStateKeys.AgeBit: age_bit,
            BlockStateKeys.BambooLeafSize: bamboo_leaf_size,
            BlockStateKeys.BambooStalkThickness: bamboo_stalk_thickness,
        },
    )


def BambooBlock(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for BambooBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_block", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def BambooButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooButton"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def BambooDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def BambooDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BambooFence() -> MinecraftBlockDescriptor:
    """Factory for BambooFence"""
    return MinecraftBlockDescriptor("minecraft:bamboo_fence", True)


def BambooFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def BambooHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def BambooMosaic() -> MinecraftBlockDescriptor:
    """Factory for BambooMosaic"""
    return MinecraftBlockDescriptor("minecraft:bamboo_mosaic", True)


def BambooMosaicDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooMosaicDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_mosaic_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BambooMosaicSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooMosaicSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_mosaic_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BambooMosaicStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooMosaicStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_mosaic_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def BambooPlanks() -> MinecraftBlockDescriptor:
    """Factory for BambooPlanks"""
    return MinecraftBlockDescriptor("minecraft:bamboo_planks", True)


def BambooPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def BambooSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for BambooSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def BambooShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def BambooSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BambooStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def BambooStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def BambooTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def BambooWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BambooWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:bamboo_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def Barrel(
    facing_direction: Optional[FacingDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Barrel"""
    return MinecraftBlockDescriptor(
        "minecraft:barrel",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def Barrier() -> MinecraftBlockDescriptor:
    """Factory for Barrier"""
    return MinecraftBlockDescriptor("minecraft:barrier", True)


def Basalt(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for Basalt"""
    return MinecraftBlockDescriptor(
        "minecraft:basalt", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def Beacon() -> MinecraftBlockDescriptor:
    """Factory for Beacon"""
    return MinecraftBlockDescriptor("minecraft:beacon", True)


def Bed(
    direction: Optional[Direction] = None,
    head_piece_bit: Optional[HeadPieceBit] = None,
    occupied_bit: Optional[OccupiedBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Bed"""
    return MinecraftBlockDescriptor(
        "minecraft:bed",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.HeadPieceBit: head_piece_bit,
            BlockStateKeys.OccupiedBit: occupied_bit,
        },
    )


def Bedrock(infiniburn_bit: Optional[InfiniburnBit] = None) -> MinecraftBlockDescriptor:
    """Factory for Bedrock"""
    return MinecraftBlockDescriptor(
        "minecraft:bedrock", True, {BlockStateKeys.InfiniburnBit: infiniburn_bit}
    )


def BeeNest(
    direction: Optional[Direction] = None, honey_level: Optional[HoneyLevel] = None
) -> MinecraftBlockDescriptor:
    """Factory for BeeNest"""
    return MinecraftBlockDescriptor(
        "minecraft:bee_nest",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.HoneyLevel: honey_level,
        },
    )


def Beehive(
    direction: Optional[Direction] = None, honey_level: Optional[HoneyLevel] = None
) -> MinecraftBlockDescriptor:
    """Factory for Beehive"""
    return MinecraftBlockDescriptor(
        "minecraft:beehive",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.HoneyLevel: honey_level,
        },
    )


def Beetroot(growth: Optional[Growth] = None) -> MinecraftBlockDescriptor:
    """Factory for Beetroot"""
    return MinecraftBlockDescriptor(
        "minecraft:beetroot", True, {BlockStateKeys.Growth: growth}
    )


def Bell(
    attachment: Optional[Attachment] = None,
    direction: Optional[Direction] = None,
    toggle_bit: Optional[ToggleBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Bell"""
    return MinecraftBlockDescriptor(
        "minecraft:bell",
        True,
        {
            BlockStateKeys.Attachment: attachment,
            BlockStateKeys.Direction: direction,
            BlockStateKeys.ToggleBit: toggle_bit,
        },
    )


def BigDripleaf(
    big_dripleaf_head: Optional[BigDripleafHead] = None,
    big_dripleaf_tilt: Optional[BigDripleafTilt] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BigDripleaf"""
    return MinecraftBlockDescriptor(
        "minecraft:big_dripleaf",
        True,
        {
            BlockStateKeys.BigDripleafHead: big_dripleaf_head,
            BlockStateKeys.BigDripleafTilt: big_dripleaf_tilt,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def BirchButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchButton"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def BirchDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def BirchDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BirchFence() -> MinecraftBlockDescriptor:
    """Factory for BirchFence"""
    return MinecraftBlockDescriptor("minecraft:birch_fence", True)


def BirchFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def BirchHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def BirchLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def BirchLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for BirchLog"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def BirchPlanks() -> MinecraftBlockDescriptor:
    """Factory for BirchPlanks"""
    return MinecraftBlockDescriptor("minecraft:birch_planks", True)


def BirchPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def BirchSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for BirchSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def BirchShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def BirchSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BirchStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def BirchStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def BirchTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def BirchWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BirchWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def BirchWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for BirchWood"""
    return MinecraftBlockDescriptor(
        "minecraft:birch_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def BlackCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for BlackCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:black_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def BlackCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for BlackCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:black_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def BlackCarpet() -> MinecraftBlockDescriptor:
    """Factory for BlackCarpet"""
    return MinecraftBlockDescriptor("minecraft:black_carpet", True)


def BlackConcrete() -> MinecraftBlockDescriptor:
    """Factory for BlackConcrete"""
    return MinecraftBlockDescriptor("minecraft:black_concrete", True)


def BlackConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for BlackConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:black_concrete_powder", True)


def BlackGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlackGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:black_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def BlackShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for BlackShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:black_shulker_box", True)


def BlackStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for BlackStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:black_stained_glass", True)


def BlackStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for BlackStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:black_stained_glass_pane", True)


def BlackTerracotta() -> MinecraftBlockDescriptor:
    """Factory for BlackTerracotta"""
    return MinecraftBlockDescriptor("minecraft:black_terracotta", True)


def BlackWool() -> MinecraftBlockDescriptor:
    """Factory for BlackWool"""
    return MinecraftBlockDescriptor("minecraft:black_wool", True)


def Blackstone() -> MinecraftBlockDescriptor:
    """Factory for Blackstone"""
    return MinecraftBlockDescriptor("minecraft:blackstone", True)


def BlackstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlackstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:blackstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BlackstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlackstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:blackstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BlackstoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlackstoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:blackstone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def BlackstoneWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlackstoneWall"""
    return MinecraftBlockDescriptor(
        "minecraft:blackstone_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def BlastFurnace(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlastFurnace"""
    return MinecraftBlockDescriptor(
        "minecraft:blast_furnace",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def BlueCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for BlueCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:blue_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def BlueCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for BlueCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:blue_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def BlueCarpet() -> MinecraftBlockDescriptor:
    """Factory for BlueCarpet"""
    return MinecraftBlockDescriptor("minecraft:blue_carpet", True)


def BlueConcrete() -> MinecraftBlockDescriptor:
    """Factory for BlueConcrete"""
    return MinecraftBlockDescriptor("minecraft:blue_concrete", True)


def BlueConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for BlueConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:blue_concrete_powder", True)


def BlueGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BlueGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:blue_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def BlueIce() -> MinecraftBlockDescriptor:
    """Factory for BlueIce"""
    return MinecraftBlockDescriptor("minecraft:blue_ice", True)


def BlueOrchid() -> MinecraftBlockDescriptor:
    """Factory for BlueOrchid"""
    return MinecraftBlockDescriptor("minecraft:blue_orchid", True)


def BlueShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for BlueShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:blue_shulker_box", True)


def BlueStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for BlueStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:blue_stained_glass", True)


def BlueStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for BlueStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:blue_stained_glass_pane", True)


def BlueTerracotta() -> MinecraftBlockDescriptor:
    """Factory for BlueTerracotta"""
    return MinecraftBlockDescriptor("minecraft:blue_terracotta", True)


def BlueWool() -> MinecraftBlockDescriptor:
    """Factory for BlueWool"""
    return MinecraftBlockDescriptor("minecraft:blue_wool", True)


def BoneBlock(
    deprecated: Optional[Deprecated] = None, pillar_axis: Optional[PillarAxis] = None
) -> MinecraftBlockDescriptor:
    """Factory for BoneBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:bone_block",
        True,
        {
            BlockStateKeys.Deprecated: deprecated,
            BlockStateKeys.PillarAxis: pillar_axis,
        },
    )


def Bookshelf() -> MinecraftBlockDescriptor:
    """Factory for Bookshelf"""
    return MinecraftBlockDescriptor("minecraft:bookshelf", True)


def BorderBlock(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BorderBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:border_block",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def BrainCoral() -> MinecraftBlockDescriptor:
    """Factory for BrainCoral"""
    return MinecraftBlockDescriptor("minecraft:brain_coral", True)


def BrainCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for BrainCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:brain_coral_block", True)


def BrainCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrainCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:brain_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def BrainCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrainCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:brain_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def BrewingStand(
    brewing_stand_slot_a_bit: Optional[BrewingStandSlotABit] = None,
    brewing_stand_slot_b_bit: Optional[BrewingStandSlotBBit] = None,
    brewing_stand_slot_c_bit: Optional[BrewingStandSlotCBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrewingStand"""
    return MinecraftBlockDescriptor(
        "minecraft:brewing_stand",
        True,
        {
            BlockStateKeys.BrewingStandSlotABit: brewing_stand_slot_a_bit,
            BlockStateKeys.BrewingStandSlotBBit: brewing_stand_slot_b_bit,
            BlockStateKeys.BrewingStandSlotCBit: brewing_stand_slot_c_bit,
        },
    )


def BrickBlock() -> MinecraftBlockDescriptor:
    """Factory for BrickBlock"""
    return MinecraftBlockDescriptor("minecraft:brick_block", True)


def BrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def BrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def BrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def BrownCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for BrownCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:brown_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def BrownCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for BrownCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:brown_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def BrownCarpet() -> MinecraftBlockDescriptor:
    """Factory for BrownCarpet"""
    return MinecraftBlockDescriptor("minecraft:brown_carpet", True)


def BrownConcrete() -> MinecraftBlockDescriptor:
    """Factory for BrownConcrete"""
    return MinecraftBlockDescriptor("minecraft:brown_concrete", True)


def BrownConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for BrownConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:brown_concrete_powder", True)


def BrownGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrownGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:brown_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def BrownMushroom() -> MinecraftBlockDescriptor:
    """Factory for BrownMushroom"""
    return MinecraftBlockDescriptor("minecraft:brown_mushroom", True)


def BrownMushroomBlock(
    huge_mushroom_bits: Optional[HugeMushroomBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BrownMushroomBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:brown_mushroom_block",
        True,
        {BlockStateKeys.HugeMushroomBits: huge_mushroom_bits},
    )


def BrownShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for BrownShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:brown_shulker_box", True)


def BrownStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for BrownStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:brown_stained_glass", True)


def BrownStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for BrownStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:brown_stained_glass_pane", True)


def BrownTerracotta() -> MinecraftBlockDescriptor:
    """Factory for BrownTerracotta"""
    return MinecraftBlockDescriptor("minecraft:brown_terracotta", True)


def BrownWool() -> MinecraftBlockDescriptor:
    """Factory for BrownWool"""
    return MinecraftBlockDescriptor("minecraft:brown_wool", True)


def BubbleColumn(drag_down: Optional[DragDown] = None) -> MinecraftBlockDescriptor:
    """Factory for BubbleColumn"""
    return MinecraftBlockDescriptor(
        "minecraft:bubble_column", True, {BlockStateKeys.DragDown: drag_down}
    )


def BubbleCoral() -> MinecraftBlockDescriptor:
    """Factory for BubbleCoral"""
    return MinecraftBlockDescriptor("minecraft:bubble_coral", True)


def BubbleCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for BubbleCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:bubble_coral_block", True)


def BubbleCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BubbleCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:bubble_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def BubbleCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for BubbleCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:bubble_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def BuddingAmethyst() -> MinecraftBlockDescriptor:
    """Factory for BuddingAmethyst"""
    return MinecraftBlockDescriptor("minecraft:budding_amethyst", True)


def Bush() -> MinecraftBlockDescriptor:
    """Factory for Bush"""
    return MinecraftBlockDescriptor("minecraft:bush", True)


def Cactus(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for Cactus"""
    return MinecraftBlockDescriptor("minecraft:cactus", True, {BlockStateKeys.Age: age})


def CactusFlower() -> MinecraftBlockDescriptor:
    """Factory for CactusFlower"""
    return MinecraftBlockDescriptor("minecraft:cactus_flower", True)


def Cake(bite_counter: Optional[BiteCounter] = None) -> MinecraftBlockDescriptor:
    """Factory for Cake"""
    return MinecraftBlockDescriptor(
        "minecraft:cake", True, {BlockStateKeys.BiteCounter: bite_counter}
    )


def Calcite() -> MinecraftBlockDescriptor:
    """Factory for Calcite"""
    return MinecraftBlockDescriptor("minecraft:calcite", True)


def CalibratedSculkSensor(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    sculk_sensor_phase: Optional[SculkSensorPhase] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CalibratedSculkSensor"""
    return MinecraftBlockDescriptor(
        "minecraft:calibrated_sculk_sensor",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.SculkSensorPhase: sculk_sensor_phase,
        },
    )


def Camera() -> MinecraftBlockDescriptor:
    """Factory for Camera"""
    return MinecraftBlockDescriptor("minecraft:camera", True)


def Campfire(
    extinguished: Optional[Extinguished] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Campfire"""
    return MinecraftBlockDescriptor(
        "minecraft:campfire",
        True,
        {
            BlockStateKeys.Extinguished: extinguished,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def Candle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for Candle"""
    return MinecraftBlockDescriptor(
        "minecraft:candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def CandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for CandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def Carrots(growth: Optional[Growth] = None) -> MinecraftBlockDescriptor:
    """Factory for Carrots"""
    return MinecraftBlockDescriptor(
        "minecraft:carrots", True, {BlockStateKeys.Growth: growth}
    )


def CartographyTable() -> MinecraftBlockDescriptor:
    """Factory for CartographyTable"""
    return MinecraftBlockDescriptor("minecraft:cartography_table", True)


def CarvedPumpkin(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CarvedPumpkin"""
    return MinecraftBlockDescriptor(
        "minecraft:carved_pumpkin",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def Cauldron(
    cauldron_liquid: Optional[CauldronLiquid] = None,
    fill_level: Optional[FillLevel] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Cauldron"""
    return MinecraftBlockDescriptor(
        "minecraft:cauldron",
        True,
        {
            BlockStateKeys.CauldronLiquid: cauldron_liquid,
            BlockStateKeys.FillLevel: fill_level,
        },
    )


def CaveVines(
    growing_plant_age: Optional[GrowingPlantAge] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CaveVines"""
    return MinecraftBlockDescriptor(
        "minecraft:cave_vines",
        True,
        {BlockStateKeys.GrowingPlantAge: growing_plant_age},
    )


def CaveVinesBodyWithBerries(
    growing_plant_age: Optional[GrowingPlantAge] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CaveVinesBodyWithBerries"""
    return MinecraftBlockDescriptor(
        "minecraft:cave_vines_body_with_berries",
        True,
        {BlockStateKeys.GrowingPlantAge: growing_plant_age},
    )


def CaveVinesHeadWithBerries(
    growing_plant_age: Optional[GrowingPlantAge] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CaveVinesHeadWithBerries"""
    return MinecraftBlockDescriptor(
        "minecraft:cave_vines_head_with_berries",
        True,
        {BlockStateKeys.GrowingPlantAge: growing_plant_age},
    )


#
# def Chain(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
#    """Factory for Chain"""
#    return MinecraftBlockDescriptor("minecraft:chain", True, {BlockStateKeys.PillarAxis: pillar_axis})


def ChainCommandBlock(
    conditional_bit: Optional[ConditionalBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ChainCommandBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:chain_command_block",
        True,
        {
            BlockStateKeys.ConditionalBit: conditional_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def ChemicalHeat() -> MinecraftBlockDescriptor:
    """Factory for ChemicalHeat"""
    return MinecraftBlockDescriptor("minecraft:chemical_heat", True)


def CherryButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryButton"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def CherryDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def CherryDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CherryFence() -> MinecraftBlockDescriptor:
    """Factory for CherryFence"""
    return MinecraftBlockDescriptor("minecraft:cherry_fence", True)


def CherryFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def CherryHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def CherryLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def CherryLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for CherryLog"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def CherryPlanks() -> MinecraftBlockDescriptor:
    """Factory for CherryPlanks"""
    return MinecraftBlockDescriptor("minecraft:cherry_planks", True)


def CherryPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def CherrySapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for CherrySapling"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def CherryShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def CherrySlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherrySlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CherryStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def CherryStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def CherryTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def CherryWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CherryWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def CherryWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for CherryWood"""
    return MinecraftBlockDescriptor(
        "minecraft:cherry_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def Chest(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Chest"""
    return MinecraftBlockDescriptor(
        "minecraft:chest",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def ChippedAnvil(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ChippedAnvil"""
    return MinecraftBlockDescriptor(
        "minecraft:chipped_anvil",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def ChiseledBookshelf(
    books_stored: Optional[BooksStored] = None, direction: Optional[Direction] = None
) -> MinecraftBlockDescriptor:
    """Factory for ChiseledBookshelf"""
    return MinecraftBlockDescriptor(
        "minecraft:chiseled_bookshelf",
        True,
        {
            BlockStateKeys.BooksStored: books_stored,
            BlockStateKeys.Direction: direction,
        },
    )


def ChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for ChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:chiseled_copper", True)


def ChiseledDeepslate() -> MinecraftBlockDescriptor:
    """Factory for ChiseledDeepslate"""
    return MinecraftBlockDescriptor("minecraft:chiseled_deepslate", True)


def ChiseledNetherBricks() -> MinecraftBlockDescriptor:
    """Factory for ChiseledNetherBricks"""
    return MinecraftBlockDescriptor("minecraft:chiseled_nether_bricks", True)


def ChiseledPolishedBlackstone() -> MinecraftBlockDescriptor:
    """Factory for ChiseledPolishedBlackstone"""
    return MinecraftBlockDescriptor("minecraft:chiseled_polished_blackstone", True)


def ChiseledQuartzBlock(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ChiseledQuartzBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:chiseled_quartz_block",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def ChiseledRedSandstone() -> MinecraftBlockDescriptor:
    """Factory for ChiseledRedSandstone"""
    return MinecraftBlockDescriptor("minecraft:chiseled_red_sandstone", True)


def ChiseledResinBricks() -> MinecraftBlockDescriptor:
    """Factory for ChiseledResinBricks"""
    return MinecraftBlockDescriptor("minecraft:chiseled_resin_bricks", True)


def ChiseledSandstone() -> MinecraftBlockDescriptor:
    """Factory for ChiseledSandstone"""
    return MinecraftBlockDescriptor("minecraft:chiseled_sandstone", True)


def ChiseledStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for ChiseledStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:chiseled_stone_bricks", True)


def ChiseledTuff() -> MinecraftBlockDescriptor:
    """Factory for ChiseledTuff"""
    return MinecraftBlockDescriptor("minecraft:chiseled_tuff", True)


def ChiseledTuffBricks() -> MinecraftBlockDescriptor:
    """Factory for ChiseledTuffBricks"""
    return MinecraftBlockDescriptor("minecraft:chiseled_tuff_bricks", True)


def ChorusFlower(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for ChorusFlower"""
    return MinecraftBlockDescriptor(
        "minecraft:chorus_flower", True, {BlockStateKeys.Age: age}
    )


def ChorusPlant() -> MinecraftBlockDescriptor:
    """Factory for ChorusPlant"""
    return MinecraftBlockDescriptor("minecraft:chorus_plant", True)


def Clay() -> MinecraftBlockDescriptor:
    """Factory for Clay"""
    return MinecraftBlockDescriptor("minecraft:clay", True)


def ClosedEyeblossom() -> MinecraftBlockDescriptor:
    """Factory for ClosedEyeblossom"""
    return MinecraftBlockDescriptor("minecraft:closed_eyeblossom", True)


def CoalBlock() -> MinecraftBlockDescriptor:
    """Factory for CoalBlock"""
    return MinecraftBlockDescriptor("minecraft:coal_block", True)


def CoalOre() -> MinecraftBlockDescriptor:
    """Factory for CoalOre"""
    return MinecraftBlockDescriptor("minecraft:coal_ore", True)


def CobbledDeepslate() -> MinecraftBlockDescriptor:
    """Factory for CobbledDeepslate"""
    return MinecraftBlockDescriptor("minecraft:cobbled_deepslate", True)


def CobbledDeepslateDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobbledDeepslateDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cobbled_deepslate_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CobbledDeepslateSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobbledDeepslateSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cobbled_deepslate_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CobbledDeepslateStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobbledDeepslateStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:cobbled_deepslate_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def CobbledDeepslateWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobbledDeepslateWall"""
    return MinecraftBlockDescriptor(
        "minecraft:cobbled_deepslate_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Cobblestone() -> MinecraftBlockDescriptor:
    """Factory for Cobblestone"""
    return MinecraftBlockDescriptor("minecraft:cobblestone", True)


def CobblestoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobblestoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cobblestone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CobblestoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobblestoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cobblestone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CobblestoneWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CobblestoneWall"""
    return MinecraftBlockDescriptor(
        "minecraft:cobblestone_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Cocoa(
    age: Optional[Age] = None, direction: Optional[Direction] = None
) -> MinecraftBlockDescriptor:
    """Factory for Cocoa"""
    return MinecraftBlockDescriptor(
        "minecraft:cocoa",
        True,
        {BlockStateKeys.Age: age, BlockStateKeys.Direction: direction},
    )


def ColoredTorchBlue(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ColoredTorchBlue"""
    return MinecraftBlockDescriptor(
        "minecraft:colored_torch_blue",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def ColoredTorchGreen(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ColoredTorchGreen"""
    return MinecraftBlockDescriptor(
        "minecraft:colored_torch_green",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def ColoredTorchPurple(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ColoredTorchPurple"""
    return MinecraftBlockDescriptor(
        "minecraft:colored_torch_purple",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def ColoredTorchRed(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ColoredTorchRed"""
    return MinecraftBlockDescriptor(
        "minecraft:colored_torch_red",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def CommandBlock(
    conditional_bit: Optional[ConditionalBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CommandBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:command_block",
        True,
        {
            BlockStateKeys.ConditionalBit: conditional_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def Composter(
    composter_fill_level: Optional[ComposterFillLevel] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Composter"""
    return MinecraftBlockDescriptor(
        "minecraft:composter",
        True,
        {BlockStateKeys.ComposterFillLevel: composter_fill_level},
    )


def CompoundCreator(direction: Optional[Direction] = None) -> MinecraftBlockDescriptor:
    """Factory for CompoundCreator"""
    return MinecraftBlockDescriptor(
        "minecraft:compound_creator", True, {BlockStateKeys.Direction: direction}
    )


def Conduit() -> MinecraftBlockDescriptor:
    """Factory for Conduit"""
    return MinecraftBlockDescriptor("minecraft:conduit", True)


def CopperBars() -> MinecraftBlockDescriptor:
    """Factory for CopperBars"""
    return MinecraftBlockDescriptor("minecraft:copper_bars", True)


def CopperBlock() -> MinecraftBlockDescriptor:
    """Factory for CopperBlock"""
    return MinecraftBlockDescriptor("minecraft:copper_block", True)


def CopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for CopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def CopperChain(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for CopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_chain", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def CopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def CopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def CopperGrate() -> MinecraftBlockDescriptor:
    """Factory for CopperGrate"""
    return MinecraftBlockDescriptor("minecraft:copper_grate", True)


def CopperLantern(hanging: Optional[Hanging] = None) -> MinecraftBlockDescriptor:
    """Factory for CopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_lantern", True, {BlockStateKeys.Hanging: hanging}
    )


def CopperOre() -> MinecraftBlockDescriptor:
    """Factory for CopperOre"""
    return MinecraftBlockDescriptor("minecraft:copper_ore", True)


def CopperTorch(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CopperTorch"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_torch",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def CopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def Cornflower() -> MinecraftBlockDescriptor:
    """Factory for Cornflower"""
    return MinecraftBlockDescriptor("minecraft:cornflower", True)


def CrackedDeepslateBricks() -> MinecraftBlockDescriptor:
    """Factory for CrackedDeepslateBricks"""
    return MinecraftBlockDescriptor("minecraft:cracked_deepslate_bricks", True)


def CrackedDeepslateTiles() -> MinecraftBlockDescriptor:
    """Factory for CrackedDeepslateTiles"""
    return MinecraftBlockDescriptor("minecraft:cracked_deepslate_tiles", True)


def CrackedNetherBricks() -> MinecraftBlockDescriptor:
    """Factory for CrackedNetherBricks"""
    return MinecraftBlockDescriptor("minecraft:cracked_nether_bricks", True)


def CrackedPolishedBlackstoneBricks() -> MinecraftBlockDescriptor:
    """Factory for CrackedPolishedBlackstoneBricks"""
    return MinecraftBlockDescriptor(
        "minecraft:cracked_polished_blackstone_bricks", True
    )


def CrackedStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for CrackedStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:cracked_stone_bricks", True)


def Crafter(
    crafting: Optional[Crafting] = None,
    orientation: Optional[Orientation] = None,
    triggered_bit: Optional[TriggeredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Crafter"""
    return MinecraftBlockDescriptor(
        "minecraft:crafter",
        True,
        {
            BlockStateKeys.Crafting: crafting,
            BlockStateKeys.Orientation: orientation,
            BlockStateKeys.TriggeredBit: triggered_bit,
        },
    )


def CraftingTable() -> MinecraftBlockDescriptor:
    """Factory for CraftingTable"""
    return MinecraftBlockDescriptor("minecraft:crafting_table", True)


def CreakingHeart(
    creaking_heart_state: Optional[CreakingHeartState] = None,
    natural: Optional[Natural] = None,
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CreakingHeart"""
    return MinecraftBlockDescriptor(
        "minecraft:creaking_heart",
        True,
        {
            BlockStateKeys.CreakingHeartState: creaking_heart_state,
            BlockStateKeys.Natural: natural,
            BlockStateKeys.PillarAxis: pillar_axis,
        },
    )


def CreeperHead(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CreeperHead"""
    return MinecraftBlockDescriptor(
        "minecraft:creeper_head",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def CrimsonButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonButton"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def CrimsonDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def CrimsonDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CrimsonFence() -> MinecraftBlockDescriptor:
    """Factory for CrimsonFence"""
    return MinecraftBlockDescriptor("minecraft:crimson_fence", True)


def CrimsonFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def CrimsonFungus() -> MinecraftBlockDescriptor:
    """Factory for CrimsonFungus"""
    return MinecraftBlockDescriptor("minecraft:crimson_fungus", True)


def CrimsonHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def CrimsonHyphae(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for CrimsonHyphae"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_hyphae", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def CrimsonNylium() -> MinecraftBlockDescriptor:
    """Factory for CrimsonNylium"""
    return MinecraftBlockDescriptor("minecraft:crimson_nylium", True)


def CrimsonPlanks() -> MinecraftBlockDescriptor:
    """Factory for CrimsonPlanks"""
    return MinecraftBlockDescriptor("minecraft:crimson_planks", True)


def CrimsonPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def CrimsonRoots() -> MinecraftBlockDescriptor:
    """Factory for CrimsonRoots"""
    return MinecraftBlockDescriptor("minecraft:crimson_roots", True)


def CrimsonShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def CrimsonSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CrimsonStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def CrimsonStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def CrimsonStem(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for CrimsonStem"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_stem", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def CrimsonTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def CrimsonWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CrimsonWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:crimson_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def CryingObsidian() -> MinecraftBlockDescriptor:
    """Factory for CryingObsidian"""
    return MinecraftBlockDescriptor("minecraft:crying_obsidian", True)


def CutCopper() -> MinecraftBlockDescriptor:
    """Factory for CutCopper"""
    return MinecraftBlockDescriptor("minecraft:cut_copper", True)


def CutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def CutRedSandstone() -> MinecraftBlockDescriptor:
    """Factory for CutRedSandstone"""
    return MinecraftBlockDescriptor("minecraft:cut_red_sandstone", True)


def CutRedSandstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CutRedSandstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cut_red_sandstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CutRedSandstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CutRedSandstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cut_red_sandstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CutSandstone() -> MinecraftBlockDescriptor:
    """Factory for CutSandstone"""
    return MinecraftBlockDescriptor("minecraft:cut_sandstone", True)


def CutSandstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CutSandstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cut_sandstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CutSandstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CutSandstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:cut_sandstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def CyanCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for CyanCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:cyan_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def CyanCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for CyanCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:cyan_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def CyanCarpet() -> MinecraftBlockDescriptor:
    """Factory for CyanCarpet"""
    return MinecraftBlockDescriptor("minecraft:cyan_carpet", True)


def CyanConcrete() -> MinecraftBlockDescriptor:
    """Factory for CyanConcrete"""
    return MinecraftBlockDescriptor("minecraft:cyan_concrete", True)


def CyanConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for CyanConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:cyan_concrete_powder", True)


def CyanGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for CyanGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:cyan_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def CyanShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for CyanShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:cyan_shulker_box", True)


def CyanStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for CyanStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:cyan_stained_glass", True)


def CyanStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for CyanStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:cyan_stained_glass_pane", True)


def CyanTerracotta() -> MinecraftBlockDescriptor:
    """Factory for CyanTerracotta"""
    return MinecraftBlockDescriptor("minecraft:cyan_terracotta", True)


def CyanWool() -> MinecraftBlockDescriptor:
    """Factory for CyanWool"""
    return MinecraftBlockDescriptor("minecraft:cyan_wool", True)


def DamagedAnvil(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DamagedAnvil"""
    return MinecraftBlockDescriptor(
        "minecraft:damaged_anvil",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def Dandelion() -> MinecraftBlockDescriptor:
    """Factory for Dandelion"""
    return MinecraftBlockDescriptor("minecraft:dandelion", True)


def DarkOakButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakButton"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def DarkOakDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def DarkOakDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DarkOakFence() -> MinecraftBlockDescriptor:
    """Factory for DarkOakFence"""
    return MinecraftBlockDescriptor("minecraft:dark_oak_fence", True)


def DarkOakFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def DarkOakHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def DarkOakLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def DarkOakLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for DarkOakLog"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def DarkOakPlanks() -> MinecraftBlockDescriptor:
    """Factory for DarkOakPlanks"""
    return MinecraftBlockDescriptor("minecraft:dark_oak_planks", True)


def DarkOakPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def DarkOakSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for DarkOakSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def DarkOakShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def DarkOakSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DarkOakStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def DarkOakTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkOakTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def DarkOakWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for DarkOakWood"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_oak_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def DarkPrismarine() -> MinecraftBlockDescriptor:
    """Factory for DarkPrismarine"""
    return MinecraftBlockDescriptor("minecraft:dark_prismarine", True)


def DarkPrismarineDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkPrismarineDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_prismarine_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DarkPrismarineSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkPrismarineSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_prismarine_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DarkPrismarineStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkPrismarineStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:dark_prismarine_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def DarkoakStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkoakStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:darkoak_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def DarkoakWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DarkoakWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:darkoak_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def DaylightDetector(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DaylightDetector"""
    return MinecraftBlockDescriptor(
        "minecraft:daylight_detector",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def DaylightDetectorInverted(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DaylightDetectorInverted"""
    return MinecraftBlockDescriptor(
        "minecraft:daylight_detector_inverted",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def DeadBrainCoral() -> MinecraftBlockDescriptor:
    """Factory for DeadBrainCoral"""
    return MinecraftBlockDescriptor("minecraft:dead_brain_coral", True)


def DeadBrainCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for DeadBrainCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:dead_brain_coral_block", True)


def DeadBrainCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadBrainCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_brain_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def DeadBrainCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadBrainCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_brain_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def DeadBubbleCoral() -> MinecraftBlockDescriptor:
    """Factory for DeadBubbleCoral"""
    return MinecraftBlockDescriptor("minecraft:dead_bubble_coral", True)


def DeadBubbleCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for DeadBubbleCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:dead_bubble_coral_block", True)


def DeadBubbleCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadBubbleCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_bubble_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def DeadBubbleCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadBubbleCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_bubble_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def DeadFireCoral() -> MinecraftBlockDescriptor:
    """Factory for DeadFireCoral"""
    return MinecraftBlockDescriptor("minecraft:dead_fire_coral", True)


def DeadFireCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for DeadFireCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:dead_fire_coral_block", True)


def DeadFireCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadFireCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_fire_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def DeadFireCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadFireCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_fire_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def DeadHornCoral() -> MinecraftBlockDescriptor:
    """Factory for DeadHornCoral"""
    return MinecraftBlockDescriptor("minecraft:dead_horn_coral", True)


def DeadHornCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for DeadHornCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:dead_horn_coral_block", True)


def DeadHornCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadHornCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_horn_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def DeadHornCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadHornCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_horn_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def DeadTubeCoral() -> MinecraftBlockDescriptor:
    """Factory for DeadTubeCoral"""
    return MinecraftBlockDescriptor("minecraft:dead_tube_coral", True)


def DeadTubeCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for DeadTubeCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:dead_tube_coral_block", True)


def DeadTubeCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadTubeCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_tube_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def DeadTubeCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeadTubeCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:dead_tube_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def Deadbush() -> MinecraftBlockDescriptor:
    """Factory for Deadbush"""
    return MinecraftBlockDescriptor("minecraft:deadbush", True)


def DecoratedPot(direction: Optional[Direction] = None) -> MinecraftBlockDescriptor:
    """Factory for DecoratedPot"""
    return MinecraftBlockDescriptor(
        "minecraft:decorated_pot", True, {BlockStateKeys.Direction: direction}
    )


def Deepslate(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for Deepslate"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def DeepslateBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DeepslateBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DeepslateBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def DeepslateBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def DeepslateBricks() -> MinecraftBlockDescriptor:
    """Factory for DeepslateBricks"""
    return MinecraftBlockDescriptor("minecraft:deepslate_bricks", True)


def DeepslateCoalOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateCoalOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_coal_ore", True)


def DeepslateCopperOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateCopperOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_copper_ore", True)


def DeepslateDiamondOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateDiamondOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_diamond_ore", True)


def DeepslateEmeraldOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateEmeraldOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_emerald_ore", True)


def DeepslateGoldOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateGoldOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_gold_ore", True)


def DeepslateIronOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateIronOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_iron_ore", True)


def DeepslateLapisOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateLapisOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_lapis_ore", True)


def DeepslateRedstoneOre() -> MinecraftBlockDescriptor:
    """Factory for DeepslateRedstoneOre"""
    return MinecraftBlockDescriptor("minecraft:deepslate_redstone_ore", True)


def DeepslateTileDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateTileDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_tile_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DeepslateTileSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateTileSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_tile_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DeepslateTileStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateTileStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_tile_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def DeepslateTileWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DeepslateTileWall"""
    return MinecraftBlockDescriptor(
        "minecraft:deepslate_tile_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def DeepslateTiles() -> MinecraftBlockDescriptor:
    """Factory for DeepslateTiles"""
    return MinecraftBlockDescriptor("minecraft:deepslate_tiles", True)


def Deny() -> MinecraftBlockDescriptor:
    """Factory for Deny"""
    return MinecraftBlockDescriptor("minecraft:deny", True)


def DetectorRail(
    rail_data_bit: Optional[RailDataBit] = None,
    rail_direction: Optional[RailDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DetectorRail"""
    return MinecraftBlockDescriptor(
        "minecraft:detector_rail",
        True,
        {
            BlockStateKeys.RailDataBit: rail_data_bit,
            BlockStateKeys.RailDirection: rail_direction,
        },
    )


def DiamondBlock() -> MinecraftBlockDescriptor:
    """Factory for DiamondBlock"""
    return MinecraftBlockDescriptor("minecraft:diamond_block", True)


def DiamondOre() -> MinecraftBlockDescriptor:
    """Factory for DiamondOre"""
    return MinecraftBlockDescriptor("minecraft:diamond_ore", True)


def Diorite() -> MinecraftBlockDescriptor:
    """Factory for Diorite"""
    return MinecraftBlockDescriptor("minecraft:diorite", True)


def DioriteDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DioriteDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:diorite_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DioriteSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DioriteSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:diorite_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DioriteStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DioriteStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:diorite_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def DioriteWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DioriteWall"""
    return MinecraftBlockDescriptor(
        "minecraft:diorite_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Dirt(dirt_type: Optional[DirtType | None] = None) -> MinecraftBlockDescriptor:
    """Factory for Dirt"""
    return MinecraftBlockDescriptor(
        "minecraft:dirt", True, {BlockStateKeys.DirtType: dirt_type}
    )


def DirtWithRoots() -> MinecraftBlockDescriptor:
    """Factory for DirtWithRoots"""
    return MinecraftBlockDescriptor("minecraft:dirt_with_roots", True)


def Dispenser(
    facing_direction: Optional[FacingDirection] = None,
    triggered_bit: Optional[TriggeredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Dispenser"""
    return MinecraftBlockDescriptor(
        "minecraft:dispenser",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.TriggeredBit: triggered_bit,
        },
    )


def DoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def DragonEgg() -> MinecraftBlockDescriptor:
    """Factory for DragonEgg"""
    return MinecraftBlockDescriptor("minecraft:dragon_egg", True)


def DragonHead(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DragonHead"""
    return MinecraftBlockDescriptor(
        "minecraft:dragon_head",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def DriedGhast(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    rehydration_level: Optional[RehydrationLevel] = None,
) -> MinecraftBlockDescriptor:
    """Factory for DriedGhast"""
    return MinecraftBlockDescriptor(
        "minecraft:dried_ghast",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.RehydrationLevel: rehydration_level,
        },
    )


def DriedKelpBlock() -> MinecraftBlockDescriptor:
    """Factory for DriedKelpBlock"""
    return MinecraftBlockDescriptor("minecraft:dried_kelp_block", True)


def DripstoneBlock() -> MinecraftBlockDescriptor:
    """Factory for DripstoneBlock"""
    return MinecraftBlockDescriptor("minecraft:dripstone_block", True)


def Dropper(
    facing_direction: Optional[FacingDirection] = None,
    triggered_bit: Optional[TriggeredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Dropper"""
    return MinecraftBlockDescriptor(
        "minecraft:dropper",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.TriggeredBit: triggered_bit,
        },
    )


def Element0() -> MinecraftBlockDescriptor:
    """Factory for Element0"""
    return MinecraftBlockDescriptor("minecraft:element_0", True)


def Element1() -> MinecraftBlockDescriptor:
    """Factory for Element1"""
    return MinecraftBlockDescriptor("minecraft:element_1", True)


def Element10() -> MinecraftBlockDescriptor:
    """Factory for Element10"""
    return MinecraftBlockDescriptor("minecraft:element_10", True)


def Element100() -> MinecraftBlockDescriptor:
    """Factory for Element100"""
    return MinecraftBlockDescriptor("minecraft:element_100", True)


def Element101() -> MinecraftBlockDescriptor:
    """Factory for Element101"""
    return MinecraftBlockDescriptor("minecraft:element_101", True)


def Element102() -> MinecraftBlockDescriptor:
    """Factory for Element102"""
    return MinecraftBlockDescriptor("minecraft:element_102", True)


def Element103() -> MinecraftBlockDescriptor:
    """Factory for Element103"""
    return MinecraftBlockDescriptor("minecraft:element_103", True)


def Element104() -> MinecraftBlockDescriptor:
    """Factory for Element104"""
    return MinecraftBlockDescriptor("minecraft:element_104", True)


def Element105() -> MinecraftBlockDescriptor:
    """Factory for Element105"""
    return MinecraftBlockDescriptor("minecraft:element_105", True)


def Element106() -> MinecraftBlockDescriptor:
    """Factory for Element106"""
    return MinecraftBlockDescriptor("minecraft:element_106", True)


def Element107() -> MinecraftBlockDescriptor:
    """Factory for Element107"""
    return MinecraftBlockDescriptor("minecraft:element_107", True)


def Element108() -> MinecraftBlockDescriptor:
    """Factory for Element108"""
    return MinecraftBlockDescriptor("minecraft:element_108", True)


def Element109() -> MinecraftBlockDescriptor:
    """Factory for Element109"""
    return MinecraftBlockDescriptor("minecraft:element_109", True)


def Element11() -> MinecraftBlockDescriptor:
    """Factory for Element11"""
    return MinecraftBlockDescriptor("minecraft:element_11", True)


def Element110() -> MinecraftBlockDescriptor:
    """Factory for Element110"""
    return MinecraftBlockDescriptor("minecraft:element_110", True)


def Element111() -> MinecraftBlockDescriptor:
    """Factory for Element111"""
    return MinecraftBlockDescriptor("minecraft:element_111", True)


def Element112() -> MinecraftBlockDescriptor:
    """Factory for Element112"""
    return MinecraftBlockDescriptor("minecraft:element_112", True)


def Element113() -> MinecraftBlockDescriptor:
    """Factory for Element113"""
    return MinecraftBlockDescriptor("minecraft:element_113", True)


def Element114() -> MinecraftBlockDescriptor:
    """Factory for Element114"""
    return MinecraftBlockDescriptor("minecraft:element_114", True)


def Element115() -> MinecraftBlockDescriptor:
    """Factory for Element115"""
    return MinecraftBlockDescriptor("minecraft:element_115", True)


def Element116() -> MinecraftBlockDescriptor:
    """Factory for Element116"""
    return MinecraftBlockDescriptor("minecraft:element_116", True)


def Element117() -> MinecraftBlockDescriptor:
    """Factory for Element117"""
    return MinecraftBlockDescriptor("minecraft:element_117", True)


def Element118() -> MinecraftBlockDescriptor:
    """Factory for Element118"""
    return MinecraftBlockDescriptor("minecraft:element_118", True)


def Element12() -> MinecraftBlockDescriptor:
    """Factory for Element12"""
    return MinecraftBlockDescriptor("minecraft:element_12", True)


def Element13() -> MinecraftBlockDescriptor:
    """Factory for Element13"""
    return MinecraftBlockDescriptor("minecraft:element_13", True)


def Element14() -> MinecraftBlockDescriptor:
    """Factory for Element14"""
    return MinecraftBlockDescriptor("minecraft:element_14", True)


def Element15() -> MinecraftBlockDescriptor:
    """Factory for Element15"""
    return MinecraftBlockDescriptor("minecraft:element_15", True)


def Element16() -> MinecraftBlockDescriptor:
    """Factory for Element16"""
    return MinecraftBlockDescriptor("minecraft:element_16", True)


def Element17() -> MinecraftBlockDescriptor:
    """Factory for Element17"""
    return MinecraftBlockDescriptor("minecraft:element_17", True)


def Element18() -> MinecraftBlockDescriptor:
    """Factory for Element18"""
    return MinecraftBlockDescriptor("minecraft:element_18", True)


def Element19() -> MinecraftBlockDescriptor:
    """Factory for Element19"""
    return MinecraftBlockDescriptor("minecraft:element_19", True)


def Element2() -> MinecraftBlockDescriptor:
    """Factory for Element2"""
    return MinecraftBlockDescriptor("minecraft:element_2", True)


def Element20() -> MinecraftBlockDescriptor:
    """Factory for Element20"""
    return MinecraftBlockDescriptor("minecraft:element_20", True)


def Element21() -> MinecraftBlockDescriptor:
    """Factory for Element21"""
    return MinecraftBlockDescriptor("minecraft:element_21", True)


def Element22() -> MinecraftBlockDescriptor:
    """Factory for Element22"""
    return MinecraftBlockDescriptor("minecraft:element_22", True)


def Element23() -> MinecraftBlockDescriptor:
    """Factory for Element23"""
    return MinecraftBlockDescriptor("minecraft:element_23", True)


def Element24() -> MinecraftBlockDescriptor:
    """Factory for Element24"""
    return MinecraftBlockDescriptor("minecraft:element_24", True)


def Element25() -> MinecraftBlockDescriptor:
    """Factory for Element25"""
    return MinecraftBlockDescriptor("minecraft:element_25", True)


def Element26() -> MinecraftBlockDescriptor:
    """Factory for Element26"""
    return MinecraftBlockDescriptor("minecraft:element_26", True)


def Element27() -> MinecraftBlockDescriptor:
    """Factory for Element27"""
    return MinecraftBlockDescriptor("minecraft:element_27", True)


def Element28() -> MinecraftBlockDescriptor:
    """Factory for Element28"""
    return MinecraftBlockDescriptor("minecraft:element_28", True)


def Element29() -> MinecraftBlockDescriptor:
    """Factory for Element29"""
    return MinecraftBlockDescriptor("minecraft:element_29", True)


def Element3() -> MinecraftBlockDescriptor:
    """Factory for Element3"""
    return MinecraftBlockDescriptor("minecraft:element_3", True)


def Element30() -> MinecraftBlockDescriptor:
    """Factory for Element30"""
    return MinecraftBlockDescriptor("minecraft:element_30", True)


def Element31() -> MinecraftBlockDescriptor:
    """Factory for Element31"""
    return MinecraftBlockDescriptor("minecraft:element_31", True)


def Element32() -> MinecraftBlockDescriptor:
    """Factory for Element32"""
    return MinecraftBlockDescriptor("minecraft:element_32", True)


def Element33() -> MinecraftBlockDescriptor:
    """Factory for Element33"""
    return MinecraftBlockDescriptor("minecraft:element_33", True)


def Element34() -> MinecraftBlockDescriptor:
    """Factory for Element34"""
    return MinecraftBlockDescriptor("minecraft:element_34", True)


def Element35() -> MinecraftBlockDescriptor:
    """Factory for Element35"""
    return MinecraftBlockDescriptor("minecraft:element_35", True)


def Element36() -> MinecraftBlockDescriptor:
    """Factory for Element36"""
    return MinecraftBlockDescriptor("minecraft:element_36", True)


def Element37() -> MinecraftBlockDescriptor:
    """Factory for Element37"""
    return MinecraftBlockDescriptor("minecraft:element_37", True)


def Element38() -> MinecraftBlockDescriptor:
    """Factory for Element38"""
    return MinecraftBlockDescriptor("minecraft:element_38", True)


def Element39() -> MinecraftBlockDescriptor:
    """Factory for Element39"""
    return MinecraftBlockDescriptor("minecraft:element_39", True)


def Element4() -> MinecraftBlockDescriptor:
    """Factory for Element4"""
    return MinecraftBlockDescriptor("minecraft:element_4", True)


def Element40() -> MinecraftBlockDescriptor:
    """Factory for Element40"""
    return MinecraftBlockDescriptor("minecraft:element_40", True)


def Element41() -> MinecraftBlockDescriptor:
    """Factory for Element41"""
    return MinecraftBlockDescriptor("minecraft:element_41", True)


def Element42() -> MinecraftBlockDescriptor:
    """Factory for Element42"""
    return MinecraftBlockDescriptor("minecraft:element_42", True)


def Element43() -> MinecraftBlockDescriptor:
    """Factory for Element43"""
    return MinecraftBlockDescriptor("minecraft:element_43", True)


def Element44() -> MinecraftBlockDescriptor:
    """Factory for Element44"""
    return MinecraftBlockDescriptor("minecraft:element_44", True)


def Element45() -> MinecraftBlockDescriptor:
    """Factory for Element45"""
    return MinecraftBlockDescriptor("minecraft:element_45", True)


def Element46() -> MinecraftBlockDescriptor:
    """Factory for Element46"""
    return MinecraftBlockDescriptor("minecraft:element_46", True)


def Element47() -> MinecraftBlockDescriptor:
    """Factory for Element47"""
    return MinecraftBlockDescriptor("minecraft:element_47", True)


def Element48() -> MinecraftBlockDescriptor:
    """Factory for Element48"""
    return MinecraftBlockDescriptor("minecraft:element_48", True)


def Element49() -> MinecraftBlockDescriptor:
    """Factory for Element49"""
    return MinecraftBlockDescriptor("minecraft:element_49", True)


def Element5() -> MinecraftBlockDescriptor:
    """Factory for Element5"""
    return MinecraftBlockDescriptor("minecraft:element_5", True)


def Element50() -> MinecraftBlockDescriptor:
    """Factory for Element50"""
    return MinecraftBlockDescriptor("minecraft:element_50", True)


def Element51() -> MinecraftBlockDescriptor:
    """Factory for Element51"""
    return MinecraftBlockDescriptor("minecraft:element_51", True)


def Element52() -> MinecraftBlockDescriptor:
    """Factory for Element52"""
    return MinecraftBlockDescriptor("minecraft:element_52", True)


def Element53() -> MinecraftBlockDescriptor:
    """Factory for Element53"""
    return MinecraftBlockDescriptor("minecraft:element_53", True)


def Element54() -> MinecraftBlockDescriptor:
    """Factory for Element54"""
    return MinecraftBlockDescriptor("minecraft:element_54", True)


def Element55() -> MinecraftBlockDescriptor:
    """Factory for Element55"""
    return MinecraftBlockDescriptor("minecraft:element_55", True)


def Element56() -> MinecraftBlockDescriptor:
    """Factory for Element56"""
    return MinecraftBlockDescriptor("minecraft:element_56", True)


def Element57() -> MinecraftBlockDescriptor:
    """Factory for Element57"""
    return MinecraftBlockDescriptor("minecraft:element_57", True)


def Element58() -> MinecraftBlockDescriptor:
    """Factory for Element58"""
    return MinecraftBlockDescriptor("minecraft:element_58", True)


def Element59() -> MinecraftBlockDescriptor:
    """Factory for Element59"""
    return MinecraftBlockDescriptor("minecraft:element_59", True)


def Element6() -> MinecraftBlockDescriptor:
    """Factory for Element6"""
    return MinecraftBlockDescriptor("minecraft:element_6", True)


def Element60() -> MinecraftBlockDescriptor:
    """Factory for Element60"""
    return MinecraftBlockDescriptor("minecraft:element_60", True)


def Element61() -> MinecraftBlockDescriptor:
    """Factory for Element61"""
    return MinecraftBlockDescriptor("minecraft:element_61", True)


def Element62() -> MinecraftBlockDescriptor:
    """Factory for Element62"""
    return MinecraftBlockDescriptor("minecraft:element_62", True)


def Element63() -> MinecraftBlockDescriptor:
    """Factory for Element63"""
    return MinecraftBlockDescriptor("minecraft:element_63", True)


def Element64() -> MinecraftBlockDescriptor:
    """Factory for Element64"""
    return MinecraftBlockDescriptor("minecraft:element_64", True)


def Element65() -> MinecraftBlockDescriptor:
    """Factory for Element65"""
    return MinecraftBlockDescriptor("minecraft:element_65", True)


def Element66() -> MinecraftBlockDescriptor:
    """Factory for Element66"""
    return MinecraftBlockDescriptor("minecraft:element_66", True)


def Element67() -> MinecraftBlockDescriptor:
    """Factory for Element67"""
    return MinecraftBlockDescriptor("minecraft:element_67", True)


def Element68() -> MinecraftBlockDescriptor:
    """Factory for Element68"""
    return MinecraftBlockDescriptor("minecraft:element_68", True)


def Element69() -> MinecraftBlockDescriptor:
    """Factory for Element69"""
    return MinecraftBlockDescriptor("minecraft:element_69", True)


def Element7() -> MinecraftBlockDescriptor:
    """Factory for Element7"""
    return MinecraftBlockDescriptor("minecraft:element_7", True)


def Element70() -> MinecraftBlockDescriptor:
    """Factory for Element70"""
    return MinecraftBlockDescriptor("minecraft:element_70", True)


def Element71() -> MinecraftBlockDescriptor:
    """Factory for Element71"""
    return MinecraftBlockDescriptor("minecraft:element_71", True)


def Element72() -> MinecraftBlockDescriptor:
    """Factory for Element72"""
    return MinecraftBlockDescriptor("minecraft:element_72", True)


def Element73() -> MinecraftBlockDescriptor:
    """Factory for Element73"""
    return MinecraftBlockDescriptor("minecraft:element_73", True)


def Element74() -> MinecraftBlockDescriptor:
    """Factory for Element74"""
    return MinecraftBlockDescriptor("minecraft:element_74", True)


def Element75() -> MinecraftBlockDescriptor:
    """Factory for Element75"""
    return MinecraftBlockDescriptor("minecraft:element_75", True)


def Element76() -> MinecraftBlockDescriptor:
    """Factory for Element76"""
    return MinecraftBlockDescriptor("minecraft:element_76", True)


def Element77() -> MinecraftBlockDescriptor:
    """Factory for Element77"""
    return MinecraftBlockDescriptor("minecraft:element_77", True)


def Element78() -> MinecraftBlockDescriptor:
    """Factory for Element78"""
    return MinecraftBlockDescriptor("minecraft:element_78", True)


def Element79() -> MinecraftBlockDescriptor:
    """Factory for Element79"""
    return MinecraftBlockDescriptor("minecraft:element_79", True)


def Element8() -> MinecraftBlockDescriptor:
    """Factory for Element8"""
    return MinecraftBlockDescriptor("minecraft:element_8", True)


def Element80() -> MinecraftBlockDescriptor:
    """Factory for Element80"""
    return MinecraftBlockDescriptor("minecraft:element_80", True)


def Element81() -> MinecraftBlockDescriptor:
    """Factory for Element81"""
    return MinecraftBlockDescriptor("minecraft:element_81", True)


def Element82() -> MinecraftBlockDescriptor:
    """Factory for Element82"""
    return MinecraftBlockDescriptor("minecraft:element_82", True)


def Element83() -> MinecraftBlockDescriptor:
    """Factory for Element83"""
    return MinecraftBlockDescriptor("minecraft:element_83", True)


def Element84() -> MinecraftBlockDescriptor:
    """Factory for Element84"""
    return MinecraftBlockDescriptor("minecraft:element_84", True)


def Element85() -> MinecraftBlockDescriptor:
    """Factory for Element85"""
    return MinecraftBlockDescriptor("minecraft:element_85", True)


def Element86() -> MinecraftBlockDescriptor:
    """Factory for Element86"""
    return MinecraftBlockDescriptor("minecraft:element_86", True)


def Element87() -> MinecraftBlockDescriptor:
    """Factory for Element87"""
    return MinecraftBlockDescriptor("minecraft:element_87", True)


def Element88() -> MinecraftBlockDescriptor:
    """Factory for Element88"""
    return MinecraftBlockDescriptor("minecraft:element_88", True)


def Element89() -> MinecraftBlockDescriptor:
    """Factory for Element89"""
    return MinecraftBlockDescriptor("minecraft:element_89", True)


def Element9() -> MinecraftBlockDescriptor:
    """Factory for Element9"""
    return MinecraftBlockDescriptor("minecraft:element_9", True)


def Element90() -> MinecraftBlockDescriptor:
    """Factory for Element90"""
    return MinecraftBlockDescriptor("minecraft:element_90", True)


def Element91() -> MinecraftBlockDescriptor:
    """Factory for Element91"""
    return MinecraftBlockDescriptor("minecraft:element_91", True)


def Element92() -> MinecraftBlockDescriptor:
    """Factory for Element92"""
    return MinecraftBlockDescriptor("minecraft:element_92", True)


def Element93() -> MinecraftBlockDescriptor:
    """Factory for Element93"""
    return MinecraftBlockDescriptor("minecraft:element_93", True)


def Element94() -> MinecraftBlockDescriptor:
    """Factory for Element94"""
    return MinecraftBlockDescriptor("minecraft:element_94", True)


def Element95() -> MinecraftBlockDescriptor:
    """Factory for Element95"""
    return MinecraftBlockDescriptor("minecraft:element_95", True)


def Element96() -> MinecraftBlockDescriptor:
    """Factory for Element96"""
    return MinecraftBlockDescriptor("minecraft:element_96", True)


def Element97() -> MinecraftBlockDescriptor:
    """Factory for Element97"""
    return MinecraftBlockDescriptor("minecraft:element_97", True)


def Element98() -> MinecraftBlockDescriptor:
    """Factory for Element98"""
    return MinecraftBlockDescriptor("minecraft:element_98", True)


def Element99() -> MinecraftBlockDescriptor:
    """Factory for Element99"""
    return MinecraftBlockDescriptor("minecraft:element_99", True)


def ElementConstructor(
    direction: Optional[Direction] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ElementConstructor"""
    return MinecraftBlockDescriptor(
        "minecraft:element_constructor",
        True,
        {BlockStateKeys.Direction: direction},
    )


def EmeraldBlock() -> MinecraftBlockDescriptor:
    """Factory for EmeraldBlock"""
    return MinecraftBlockDescriptor("minecraft:emerald_block", True)


def EmeraldOre() -> MinecraftBlockDescriptor:
    """Factory for EmeraldOre"""
    return MinecraftBlockDescriptor("minecraft:emerald_ore", True)


def EnchantingTable() -> MinecraftBlockDescriptor:
    """Factory for EnchantingTable"""
    return MinecraftBlockDescriptor("minecraft:enchanting_table", True)


def EndBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EndBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:end_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def EndBricks() -> MinecraftBlockDescriptor:
    """Factory for EndBricks"""
    return MinecraftBlockDescriptor("minecraft:end_bricks", True)


def EndPortal() -> MinecraftBlockDescriptor:
    """Factory for EndPortal"""
    return MinecraftBlockDescriptor("minecraft:end_portal", True)


def EndPortalFrame(
    end_portal_eye_bit: Optional[EndPortalEyeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EndPortalFrame"""
    return MinecraftBlockDescriptor(
        "minecraft:end_portal_frame",
        True,
        {
            BlockStateKeys.EndPortalEyeBit: end_portal_eye_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def EndRod(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EndRod"""
    return MinecraftBlockDescriptor(
        "minecraft:end_rod",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def EndStone() -> MinecraftBlockDescriptor:
    """Factory for EndStone"""
    return MinecraftBlockDescriptor("minecraft:end_stone", True)


def EndStoneBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EndStoneBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:end_stone_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def EndStoneBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EndStoneBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:end_stone_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def EndStoneBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EndStoneBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:end_stone_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def EnderChest(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for EnderChest"""
    return MinecraftBlockDescriptor(
        "minecraft:ender_chest",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def ExposedChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for ExposedChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:exposed_chiseled_copper", True)


def ExposedCopper() -> MinecraftBlockDescriptor:
    """Factory for ExposedCopper"""
    return MinecraftBlockDescriptor("minecraft:exposed_copper", True)


def ExposedCopperBars() -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperBars"""
    return MinecraftBlockDescriptor("minecraft:exposed_copper_bars", True)


def ExposedCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def ExposedCopperChain() -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperChain"""
    return MinecraftBlockDescriptor("minecraft:exposed_copper_chain", True)


def ExposedCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def ExposedCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def ExposedCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:exposed_copper_grate", True)


def ExposedCopperLantern(hanging: Optional[Hanging] = None) -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_copper_lantern", True, {BlockStateKeys.Hanging: hanging}
    )


def ExposedCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def ExposedCutCopper() -> MinecraftBlockDescriptor:
    """Factory for ExposedCutCopper"""
    return MinecraftBlockDescriptor("minecraft:exposed_cut_copper", True)


def ExposedCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def ExposedCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def ExposedDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def ExposedLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ExposedLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:exposed_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def Farmland(
    moisturized_amount: Optional[MoisturizedAmount] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Farmland"""
    return MinecraftBlockDescriptor(
        "minecraft:farmland",
        True,
        {BlockStateKeys.MoisturizedAmount: moisturized_amount},
    )


def FenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for FenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def Fern() -> MinecraftBlockDescriptor:
    """Factory for Fern"""
    return MinecraftBlockDescriptor("minecraft:fern", True)


def Fire(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for Fire"""
    return MinecraftBlockDescriptor("minecraft:fire", True, {BlockStateKeys.Age: age})


def FireCoral() -> MinecraftBlockDescriptor:
    """Factory for FireCoral"""
    return MinecraftBlockDescriptor("minecraft:fire_coral", True)


def FireCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for FireCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:fire_coral_block", True)


def FireCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for FireCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:fire_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def FireCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for FireCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:fire_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def FireflyBush() -> MinecraftBlockDescriptor:
    """Factory for FireflyBush"""
    return MinecraftBlockDescriptor("minecraft:firefly_bush", True)


def FletchingTable() -> MinecraftBlockDescriptor:
    """Factory for FletchingTable"""
    return MinecraftBlockDescriptor("minecraft:fletching_table", True)


def FlowerPot(update_bit: Optional[UpdateBit] = None) -> MinecraftBlockDescriptor:
    """Factory for FlowerPot"""
    return MinecraftBlockDescriptor(
        "minecraft:flower_pot", True, {BlockStateKeys.UpdateBit: update_bit}
    )


def FloweringAzalea() -> MinecraftBlockDescriptor:
    """Factory for FloweringAzalea"""
    return MinecraftBlockDescriptor("minecraft:flowering_azalea", True)


def FlowingLava(liquid_depth: Optional[LiquidDepth] = None) -> MinecraftBlockDescriptor:
    """Factory for FlowingLava"""
    return MinecraftBlockDescriptor(
        "minecraft:flowing_lava", True, {BlockStateKeys.LiquidDepth: liquid_depth}
    )


def FlowingWater(
    liquid_depth: Optional[LiquidDepth] = None,
) -> MinecraftBlockDescriptor:
    """Factory for FlowingWater"""
    return MinecraftBlockDescriptor(
        "minecraft:flowing_water", True, {BlockStateKeys.LiquidDepth: liquid_depth}
    )


def Frame(
    facing_direction: Optional[FacingDirection] = None,
    item_frame_map_bit: Optional[ItemFrameMapBit] = None,
    item_frame_photo_bit: Optional[ItemFramePhotoBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Frame"""
    return MinecraftBlockDescriptor(
        "minecraft:frame",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.ItemFrameMapBit: item_frame_map_bit,
            BlockStateKeys.ItemFramePhotoBit: item_frame_photo_bit,
        },
    )


def FrogSpawn() -> MinecraftBlockDescriptor:
    """Factory for FrogSpawn"""
    return MinecraftBlockDescriptor("minecraft:frog_spawn", True)


def FrostedIce(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for FrostedIce"""
    return MinecraftBlockDescriptor(
        "minecraft:frosted_ice", True, {BlockStateKeys.Age: age}
    )


def Furnace(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Furnace"""
    return MinecraftBlockDescriptor(
        "minecraft:furnace",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def GildedBlackstone() -> MinecraftBlockDescriptor:
    """Factory for GildedBlackstone"""
    return MinecraftBlockDescriptor("minecraft:gilded_blackstone", True)


def Glass() -> MinecraftBlockDescriptor:
    """Factory for Glass"""
    return MinecraftBlockDescriptor("minecraft:glass", True)


def GlassPane() -> MinecraftBlockDescriptor:
    """Factory for GlassPane"""
    return MinecraftBlockDescriptor("minecraft:glass_pane", True)


def GlowFrame(
    facing_direction: Optional[FacingDirection] = None,
    item_frame_map_bit: Optional[ItemFrameMapBit] = None,
    item_frame_photo_bit: Optional[ItemFramePhotoBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GlowFrame"""
    return MinecraftBlockDescriptor(
        "minecraft:glow_frame",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.ItemFrameMapBit: item_frame_map_bit,
            BlockStateKeys.ItemFramePhotoBit: item_frame_photo_bit,
        },
    )


def GlowLichen(
    multi_face_direction_bits: Optional[MultiFaceDirectionBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GlowLichen"""
    return MinecraftBlockDescriptor(
        "minecraft:glow_lichen",
        True,
        {BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits},
    )


def Glowstone() -> MinecraftBlockDescriptor:
    """Factory for Glowstone"""
    return MinecraftBlockDescriptor("minecraft:glowstone", True)


def GoldBlock() -> MinecraftBlockDescriptor:
    """Factory for GoldBlock"""
    return MinecraftBlockDescriptor("minecraft:gold_block", True)


def GoldOre() -> MinecraftBlockDescriptor:
    """Factory for GoldOre"""
    return MinecraftBlockDescriptor("minecraft:gold_ore", True)


def GoldenDandelion() -> MinecraftBlockDescriptor:
    """Factory for GoldenDandelion"""
    return MinecraftBlockDescriptor("minecraft:golden_dandelion", True)


def GoldenRail(
    rail_data_bit: Optional[RailDataBit] = None,
    rail_direction: Optional[RailDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GoldenRail"""
    return MinecraftBlockDescriptor(
        "minecraft:golden_rail",
        True,
        {
            BlockStateKeys.RailDataBit: rail_data_bit,
            BlockStateKeys.RailDirection: rail_direction,
        },
    )


def Granite() -> MinecraftBlockDescriptor:
    """Factory for Granite"""
    return MinecraftBlockDescriptor("minecraft:granite", True)


def GraniteDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GraniteDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:granite_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def GraniteSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GraniteSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:granite_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def GraniteStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GraniteStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:granite_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def GraniteWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GraniteWall"""
    return MinecraftBlockDescriptor(
        "minecraft:granite_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def GrassBlock() -> MinecraftBlockDescriptor:
    """Factory for GrassBlock"""
    return MinecraftBlockDescriptor("minecraft:grass_block", True)


def GrassPath() -> MinecraftBlockDescriptor:
    """Factory for GrassPath"""
    return MinecraftBlockDescriptor("minecraft:grass_path", True)


def Gravel() -> MinecraftBlockDescriptor:
    """Factory for Gravel"""
    return MinecraftBlockDescriptor("minecraft:gravel", True)


def GrayCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for GrayCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:gray_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def GrayCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for GrayCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:gray_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def GrayCarpet() -> MinecraftBlockDescriptor:
    """Factory for GrayCarpet"""
    return MinecraftBlockDescriptor("minecraft:gray_carpet", True)


def GrayConcrete() -> MinecraftBlockDescriptor:
    """Factory for GrayConcrete"""
    return MinecraftBlockDescriptor("minecraft:gray_concrete", True)


def GrayConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for GrayConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:gray_concrete_powder", True)


def GrayGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GrayGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:gray_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def GrayShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for GrayShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:gray_shulker_box", True)


def GrayStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for GrayStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:gray_stained_glass", True)


def GrayStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for GrayStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:gray_stained_glass_pane", True)


def GrayTerracotta() -> MinecraftBlockDescriptor:
    """Factory for GrayTerracotta"""
    return MinecraftBlockDescriptor("minecraft:gray_terracotta", True)


def GrayWool() -> MinecraftBlockDescriptor:
    """Factory for GrayWool"""
    return MinecraftBlockDescriptor("minecraft:gray_wool", True)


def GreenCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for GreenCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:green_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def GreenCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for GreenCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:green_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def GreenCarpet() -> MinecraftBlockDescriptor:
    """Factory for GreenCarpet"""
    return MinecraftBlockDescriptor("minecraft:green_carpet", True)


def GreenConcrete() -> MinecraftBlockDescriptor:
    """Factory for GreenConcrete"""
    return MinecraftBlockDescriptor("minecraft:green_concrete", True)


def GreenConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for GreenConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:green_concrete_powder", True)


def GreenGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for GreenGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:green_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def GreenShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for GreenShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:green_shulker_box", True)


def GreenStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for GreenStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:green_stained_glass", True)


def GreenStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for GreenStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:green_stained_glass_pane", True)


def GreenTerracotta() -> MinecraftBlockDescriptor:
    """Factory for GreenTerracotta"""
    return MinecraftBlockDescriptor("minecraft:green_terracotta", True)


def GreenWool() -> MinecraftBlockDescriptor:
    """Factory for GreenWool"""
    return MinecraftBlockDescriptor("minecraft:green_wool", True)


def Grindstone(
    attachment: Optional[Attachment] = None, direction: Optional[Direction] = None
) -> MinecraftBlockDescriptor:
    """Factory for Grindstone"""
    return MinecraftBlockDescriptor(
        "minecraft:grindstone",
        True,
        {
            BlockStateKeys.Attachment: attachment,
            BlockStateKeys.Direction: direction,
        },
    )


def HangingRoots() -> MinecraftBlockDescriptor:
    """Factory for HangingRoots"""
    return MinecraftBlockDescriptor("minecraft:hanging_roots", True)


def HardBlackStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardBlackStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_black_stained_glass", True)


def HardBlackStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardBlackStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_black_stained_glass_pane", True)


def HardBlueStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardBlueStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_blue_stained_glass", True)


def HardBlueStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardBlueStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_blue_stained_glass_pane", True)


def HardBrownStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardBrownStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_brown_stained_glass", True)


def HardBrownStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardBrownStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_brown_stained_glass_pane", True)


def HardCyanStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardCyanStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_cyan_stained_glass", True)


def HardCyanStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardCyanStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_cyan_stained_glass_pane", True)


def HardGlass() -> MinecraftBlockDescriptor:
    """Factory for HardGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_glass", True)


def HardGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_glass_pane", True)


def HardGrayStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardGrayStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_gray_stained_glass", True)


def HardGrayStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardGrayStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_gray_stained_glass_pane", True)


def HardGreenStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardGreenStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_green_stained_glass", True)


def HardGreenStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardGreenStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_green_stained_glass_pane", True)


def HardLightBlueStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardLightBlueStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_light_blue_stained_glass", True)


def HardLightBlueStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardLightBlueStainedGlassPane"""
    return MinecraftBlockDescriptor(
        "minecraft:hard_light_blue_stained_glass_pane", True
    )


def HardLightGrayStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardLightGrayStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_light_gray_stained_glass", True)


def HardLightGrayStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardLightGrayStainedGlassPane"""
    return MinecraftBlockDescriptor(
        "minecraft:hard_light_gray_stained_glass_pane", True
    )


def HardLimeStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardLimeStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_lime_stained_glass", True)


def HardLimeStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardLimeStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_lime_stained_glass_pane", True)


def HardMagentaStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardMagentaStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_magenta_stained_glass", True)


def HardMagentaStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardMagentaStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_magenta_stained_glass_pane", True)


def HardOrangeStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardOrangeStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_orange_stained_glass", True)


def HardOrangeStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardOrangeStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_orange_stained_glass_pane", True)


def HardPinkStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardPinkStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_pink_stained_glass", True)


def HardPinkStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardPinkStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_pink_stained_glass_pane", True)


def HardPurpleStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardPurpleStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_purple_stained_glass", True)


def HardPurpleStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardPurpleStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_purple_stained_glass_pane", True)


def HardRedStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardRedStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_red_stained_glass", True)


def HardRedStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardRedStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_red_stained_glass_pane", True)


def HardWhiteStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardWhiteStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_white_stained_glass", True)


def HardWhiteStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardWhiteStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_white_stained_glass_pane", True)


def HardYellowStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for HardYellowStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:hard_yellow_stained_glass", True)


def HardYellowStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for HardYellowStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:hard_yellow_stained_glass_pane", True)


def HardenedClay() -> MinecraftBlockDescriptor:
    """Factory for HardenedClay"""
    return MinecraftBlockDescriptor("minecraft:hardened_clay", True)


def HayBlock(
    deprecated: Optional[Deprecated] = None, pillar_axis: Optional[PillarAxis] = None
) -> MinecraftBlockDescriptor:
    """Factory for HayBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:hay_block",
        True,
        {
            BlockStateKeys.Deprecated: deprecated,
            BlockStateKeys.PillarAxis: pillar_axis,
        },
    )


def HeavyCore() -> MinecraftBlockDescriptor:
    """Factory for HeavyCore"""
    return MinecraftBlockDescriptor("minecraft:heavy_core", True)


def HeavyWeightedPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for HeavyWeightedPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:heavy_weighted_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def HoneyBlock() -> MinecraftBlockDescriptor:
    """Factory for HoneyBlock"""
    return MinecraftBlockDescriptor("minecraft:honey_block", True)


def HoneycombBlock() -> MinecraftBlockDescriptor:
    """Factory for HoneycombBlock"""
    return MinecraftBlockDescriptor("minecraft:honeycomb_block", True)


def Hopper(
    facing_direction: Optional[FacingDirection] = None,
    toggle_bit: Optional[ToggleBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Hopper"""
    return MinecraftBlockDescriptor(
        "minecraft:hopper",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.ToggleBit: toggle_bit,
        },
    )


def HornCoral() -> MinecraftBlockDescriptor:
    """Factory for HornCoral"""
    return MinecraftBlockDescriptor("minecraft:horn_coral", True)


def HornCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for HornCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:horn_coral_block", True)


def HornCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for HornCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:horn_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def HornCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for HornCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:horn_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def Ice() -> MinecraftBlockDescriptor:
    """Factory for Ice"""
    return MinecraftBlockDescriptor("minecraft:ice", True)


def InfestedChiseledStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for InfestedChiseledStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:infested_chiseled_stone_bricks", True)


def InfestedCobblestone() -> MinecraftBlockDescriptor:
    """Factory for InfestedCobblestone"""
    return MinecraftBlockDescriptor("minecraft:infested_cobblestone", True)


def InfestedCrackedStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for InfestedCrackedStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:infested_cracked_stone_bricks", True)


def InfestedDeepslate(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for InfestedDeepslate"""
    return MinecraftBlockDescriptor(
        "minecraft:infested_deepslate",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def InfestedMossyStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for InfestedMossyStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:infested_mossy_stone_bricks", True)


def InfestedStone() -> MinecraftBlockDescriptor:
    """Factory for InfestedStone"""
    return MinecraftBlockDescriptor("minecraft:infested_stone", True)


def InfestedStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for InfestedStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:infested_stone_bricks", True)


def IronBars() -> MinecraftBlockDescriptor:
    """Factory for IronBars"""
    return MinecraftBlockDescriptor("minecraft:iron_bars", True)


def IronBlock() -> MinecraftBlockDescriptor:
    """Factory for IronBlock"""
    return MinecraftBlockDescriptor("minecraft:iron_block", True)


def IronChain(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for IronChain"""
    return MinecraftBlockDescriptor(
        "minecraft:iron_chain", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def IronDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for IronDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:iron_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def IronOre() -> MinecraftBlockDescriptor:
    """Factory for IronOre"""
    return MinecraftBlockDescriptor("minecraft:iron_ore", True)


def IronTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for IronTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:iron_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def Jigsaw(
    facing_direction: Optional[FacingDirection] = None,
    rotation: Optional[Rotation] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Jigsaw"""
    return MinecraftBlockDescriptor(
        "minecraft:jigsaw",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.Rotation: rotation,
        },
    )


def Jukebox() -> MinecraftBlockDescriptor:
    """Factory for Jukebox"""
    return MinecraftBlockDescriptor("minecraft:jukebox", True)


def JungleButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleButton"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def JungleDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def JungleDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def JungleFence() -> MinecraftBlockDescriptor:
    """Factory for JungleFence"""
    return MinecraftBlockDescriptor("minecraft:jungle_fence", True)


def JungleFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def JungleHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def JungleLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def JungleLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for JungleLog"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def JunglePlanks() -> MinecraftBlockDescriptor:
    """Factory for JunglePlanks"""
    return MinecraftBlockDescriptor("minecraft:jungle_planks", True)


def JunglePressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JunglePressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def JungleSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for JungleSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def JungleShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def JungleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def JungleStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def JungleStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def JungleTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def JungleWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for JungleWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def JungleWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for JungleWood"""
    return MinecraftBlockDescriptor(
        "minecraft:jungle_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def Kelp(kelp_age: Optional[KelpAge] = None) -> MinecraftBlockDescriptor:
    """Factory for Kelp"""
    return MinecraftBlockDescriptor(
        "minecraft:kelp", True, {BlockStateKeys.KelpAge: kelp_age}
    )


def LabTable(direction: Optional[Direction] = None) -> MinecraftBlockDescriptor:
    """Factory for LabTable"""
    return MinecraftBlockDescriptor(
        "minecraft:lab_table", True, {BlockStateKeys.Direction: direction}
    )


def Ladder(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Ladder"""
    return MinecraftBlockDescriptor(
        "minecraft:ladder",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def Lantern(hanging: Optional[Hanging] = None) -> MinecraftBlockDescriptor:
    """Factory for Lantern"""
    return MinecraftBlockDescriptor(
        "minecraft:lantern", True, {BlockStateKeys.Hanging: hanging}
    )


def LapisBlock() -> MinecraftBlockDescriptor:
    """Factory for LapisBlock"""
    return MinecraftBlockDescriptor("minecraft:lapis_block", True)


def LapisOre() -> MinecraftBlockDescriptor:
    """Factory for LapisOre"""
    return MinecraftBlockDescriptor("minecraft:lapis_ore", True)


def LargeAmethystBud(
    minecraft_block_face: Optional[BlockFace] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LargeAmethystBud"""
    return MinecraftBlockDescriptor(
        "minecraft:large_amethyst_bud",
        True,
        {BlockStateKeys.MinecraftBlockFace: minecraft_block_face},
    )


def LargeFern(
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LargeFern"""
    return MinecraftBlockDescriptor(
        "minecraft:large_fern",
        True,
        {BlockStateKeys.UpperBlockBit: upper_block_bit},
    )


def Lava(liquid_depth: Optional[LiquidDepth] = None) -> MinecraftBlockDescriptor:
    """Factory for Lava"""
    return MinecraftBlockDescriptor(
        "minecraft:lava", True, {BlockStateKeys.LiquidDepth: liquid_depth}
    )


def LeafLitter(
    growth: Optional[Growth] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LeafLitter"""
    return MinecraftBlockDescriptor(
        "minecraft:leaf_litter",
        True,
        {
            BlockStateKeys.Growth: growth,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def Lectern(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Lectern"""
    return MinecraftBlockDescriptor(
        "minecraft:lectern",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def Lever(
    lever_direction: Optional[LeverDirection] = None, open_bit: Optional[OpenBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for Lever"""
    return MinecraftBlockDescriptor(
        "minecraft:lever",
        True,
        {
            BlockStateKeys.LeverDirection: lever_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def LightBlock0() -> MinecraftBlockDescriptor:
    """Factory for LightBlock0"""
    return MinecraftBlockDescriptor("minecraft:light_block_0", True)


def LightBlock1() -> MinecraftBlockDescriptor:
    """Factory for LightBlock1"""
    return MinecraftBlockDescriptor("minecraft:light_block_1", True)


def LightBlock10() -> MinecraftBlockDescriptor:
    """Factory for LightBlock10"""
    return MinecraftBlockDescriptor("minecraft:light_block_10", True)


def LightBlock11() -> MinecraftBlockDescriptor:
    """Factory for LightBlock11"""
    return MinecraftBlockDescriptor("minecraft:light_block_11", True)


def LightBlock12() -> MinecraftBlockDescriptor:
    """Factory for LightBlock12"""
    return MinecraftBlockDescriptor("minecraft:light_block_12", True)


def LightBlock13() -> MinecraftBlockDescriptor:
    """Factory for LightBlock13"""
    return MinecraftBlockDescriptor("minecraft:light_block_13", True)


def LightBlock14() -> MinecraftBlockDescriptor:
    """Factory for LightBlock14"""
    return MinecraftBlockDescriptor("minecraft:light_block_14", True)


def LightBlock15() -> MinecraftBlockDescriptor:
    """Factory for LightBlock15"""
    return MinecraftBlockDescriptor("minecraft:light_block_15", True)


def LightBlock2() -> MinecraftBlockDescriptor:
    """Factory for LightBlock2"""
    return MinecraftBlockDescriptor("minecraft:light_block_2", True)


def LightBlock3() -> MinecraftBlockDescriptor:
    """Factory for LightBlock3"""
    return MinecraftBlockDescriptor("minecraft:light_block_3", True)


def LightBlock4() -> MinecraftBlockDescriptor:
    """Factory for LightBlock4"""
    return MinecraftBlockDescriptor("minecraft:light_block_4", True)


def LightBlock5() -> MinecraftBlockDescriptor:
    """Factory for LightBlock5"""
    return MinecraftBlockDescriptor("minecraft:light_block_5", True)


def LightBlock6() -> MinecraftBlockDescriptor:
    """Factory for LightBlock6"""
    return MinecraftBlockDescriptor("minecraft:light_block_6", True)


def LightBlock7() -> MinecraftBlockDescriptor:
    """Factory for LightBlock7"""
    return MinecraftBlockDescriptor("minecraft:light_block_7", True)


def LightBlock8() -> MinecraftBlockDescriptor:
    """Factory for LightBlock8"""
    return MinecraftBlockDescriptor("minecraft:light_block_8", True)


def LightBlock9() -> MinecraftBlockDescriptor:
    """Factory for LightBlock9"""
    return MinecraftBlockDescriptor("minecraft:light_block_9", True)


def LightBlueCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for LightBlueCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:light_blue_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def LightBlueCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for LightBlueCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:light_blue_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def LightBlueCarpet() -> MinecraftBlockDescriptor:
    """Factory for LightBlueCarpet"""
    return MinecraftBlockDescriptor("minecraft:light_blue_carpet", True)


def LightBlueConcrete() -> MinecraftBlockDescriptor:
    """Factory for LightBlueConcrete"""
    return MinecraftBlockDescriptor("minecraft:light_blue_concrete", True)


def LightBlueConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for LightBlueConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:light_blue_concrete_powder", True)


def LightBlueGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LightBlueGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:light_blue_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def LightBlueShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for LightBlueShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:light_blue_shulker_box", True)


def LightBlueStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for LightBlueStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:light_blue_stained_glass", True)


def LightBlueStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for LightBlueStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:light_blue_stained_glass_pane", True)


def LightBlueTerracotta() -> MinecraftBlockDescriptor:
    """Factory for LightBlueTerracotta"""
    return MinecraftBlockDescriptor("minecraft:light_blue_terracotta", True)


def LightBlueWool() -> MinecraftBlockDescriptor:
    """Factory for LightBlueWool"""
    return MinecraftBlockDescriptor("minecraft:light_blue_wool", True)


def LightGrayCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for LightGrayCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:light_gray_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def LightGrayCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for LightGrayCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:light_gray_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def LightGrayCarpet() -> MinecraftBlockDescriptor:
    """Factory for LightGrayCarpet"""
    return MinecraftBlockDescriptor("minecraft:light_gray_carpet", True)


def LightGrayConcrete() -> MinecraftBlockDescriptor:
    """Factory for LightGrayConcrete"""
    return MinecraftBlockDescriptor("minecraft:light_gray_concrete", True)


def LightGrayConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for LightGrayConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:light_gray_concrete_powder", True)


def LightGrayShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for LightGrayShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:light_gray_shulker_box", True)


def LightGrayStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for LightGrayStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:light_gray_stained_glass", True)


def LightGrayStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for LightGrayStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:light_gray_stained_glass_pane", True)


def LightGrayTerracotta() -> MinecraftBlockDescriptor:
    """Factory for LightGrayTerracotta"""
    return MinecraftBlockDescriptor("minecraft:light_gray_terracotta", True)


def LightGrayWool() -> MinecraftBlockDescriptor:
    """Factory for LightGrayWool"""
    return MinecraftBlockDescriptor("minecraft:light_gray_wool", True)


def LightWeightedPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LightWeightedPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:light_weighted_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def LightningRod(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:lightning_rod",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def Lilac(upper_block_bit: Optional[UpperBlockBit] = None) -> MinecraftBlockDescriptor:
    """Factory for Lilac"""
    return MinecraftBlockDescriptor(
        "minecraft:lilac", True, {BlockStateKeys.UpperBlockBit: upper_block_bit}
    )


def LilyOfTheValley() -> MinecraftBlockDescriptor:
    """Factory for LilyOfTheValley"""
    return MinecraftBlockDescriptor("minecraft:lily_of_the_valley", True)


def LimeCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for LimeCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:lime_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def LimeCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for LimeCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:lime_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def LimeCarpet() -> MinecraftBlockDescriptor:
    """Factory for LimeCarpet"""
    return MinecraftBlockDescriptor("minecraft:lime_carpet", True)


def LimeConcrete() -> MinecraftBlockDescriptor:
    """Factory for LimeConcrete"""
    return MinecraftBlockDescriptor("minecraft:lime_concrete", True)


def LimeConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for LimeConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:lime_concrete_powder", True)


def LimeGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LimeGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:lime_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def LimeShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for LimeShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:lime_shulker_box", True)


def LimeStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for LimeStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:lime_stained_glass", True)


def LimeStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for LimeStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:lime_stained_glass_pane", True)


def LimeTerracotta() -> MinecraftBlockDescriptor:
    """Factory for LimeTerracotta"""
    return MinecraftBlockDescriptor("minecraft:lime_terracotta", True)


def LimeWool() -> MinecraftBlockDescriptor:
    """Factory for LimeWool"""
    return MinecraftBlockDescriptor("minecraft:lime_wool", True)


def LitBlastFurnace(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LitBlastFurnace"""
    return MinecraftBlockDescriptor(
        "minecraft:lit_blast_furnace",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def LitDeepslateRedstoneOre() -> MinecraftBlockDescriptor:
    """Factory for LitDeepslateRedstoneOre"""
    return MinecraftBlockDescriptor("minecraft:lit_deepslate_redstone_ore", True)


def LitFurnace(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LitFurnace"""
    return MinecraftBlockDescriptor(
        "minecraft:lit_furnace",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def LitPumpkin(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LitPumpkin"""
    return MinecraftBlockDescriptor(
        "minecraft:lit_pumpkin",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def LitRedstoneLamp() -> MinecraftBlockDescriptor:
    """Factory for LitRedstoneLamp"""
    return MinecraftBlockDescriptor("minecraft:lit_redstone_lamp", True)


def LitRedstoneOre() -> MinecraftBlockDescriptor:
    """Factory for LitRedstoneOre"""
    return MinecraftBlockDescriptor("minecraft:lit_redstone_ore", True)


def LitSmoker(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for LitSmoker"""
    return MinecraftBlockDescriptor(
        "minecraft:lit_smoker",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def Lodestone() -> MinecraftBlockDescriptor:
    """Factory for Lodestone"""
    return MinecraftBlockDescriptor("minecraft:lodestone", True)


def Loom(direction: Optional[Direction] = None) -> MinecraftBlockDescriptor:
    """Factory for Loom"""
    return MinecraftBlockDescriptor(
        "minecraft:loom", True, {BlockStateKeys.Direction: direction}
    )


def MagentaCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for MagentaCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:magenta_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def MagentaCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for MagentaCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:magenta_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def MagentaCarpet() -> MinecraftBlockDescriptor:
    """Factory for MagentaCarpet"""
    return MinecraftBlockDescriptor("minecraft:magenta_carpet", True)


def MagentaConcrete() -> MinecraftBlockDescriptor:
    """Factory for MagentaConcrete"""
    return MinecraftBlockDescriptor("minecraft:magenta_concrete", True)


def MagentaConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for MagentaConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:magenta_concrete_powder", True)


def MagentaGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MagentaGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:magenta_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def MagentaShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for MagentaShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:magenta_shulker_box", True)


def MagentaStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for MagentaStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:magenta_stained_glass", True)


def MagentaStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for MagentaStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:magenta_stained_glass_pane", True)


def MagentaTerracotta() -> MinecraftBlockDescriptor:
    """Factory for MagentaTerracotta"""
    return MinecraftBlockDescriptor("minecraft:magenta_terracotta", True)


def MagentaWool() -> MinecraftBlockDescriptor:
    """Factory for MagentaWool"""
    return MinecraftBlockDescriptor("minecraft:magenta_wool", True)


def Magma() -> MinecraftBlockDescriptor:
    """Factory for Magma"""
    return MinecraftBlockDescriptor("minecraft:magma", True)


def MangroveButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveButton"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def MangroveDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def MangroveDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MangroveFence() -> MinecraftBlockDescriptor:
    """Factory for MangroveFence"""
    return MinecraftBlockDescriptor("minecraft:mangrove_fence", True)


def MangroveFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def MangroveHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def MangroveLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def MangroveLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for MangroveLog"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def MangrovePlanks() -> MinecraftBlockDescriptor:
    """Factory for MangrovePlanks"""
    return MinecraftBlockDescriptor("minecraft:mangrove_planks", True)


def MangrovePressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangrovePressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def MangrovePropagule(
    hanging: Optional[Hanging] = None, propagule_stage: Optional[PropaguleStage] = None
) -> MinecraftBlockDescriptor:
    """Factory for MangrovePropagule"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_propagule",
        True,
        {
            BlockStateKeys.Hanging: hanging,
            BlockStateKeys.PropaguleStage: propagule_stage,
        },
    )


def MangroveRoots() -> MinecraftBlockDescriptor:
    """Factory for MangroveRoots"""
    return MinecraftBlockDescriptor("minecraft:mangrove_roots", True)


def MangroveShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def MangroveSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MangroveStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def MangroveStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def MangroveTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def MangroveWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MangroveWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def MangroveWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for MangroveWood"""
    return MinecraftBlockDescriptor(
        "minecraft:mangrove_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def MaterialReducer(direction: Optional[Direction] = None) -> MinecraftBlockDescriptor:
    """Factory for MaterialReducer"""
    return MinecraftBlockDescriptor(
        "minecraft:material_reducer", True, {BlockStateKeys.Direction: direction}
    )


def MediumAmethystBud(
    minecraft_block_face: Optional[BlockFace] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MediumAmethystBud"""
    return MinecraftBlockDescriptor(
        "minecraft:medium_amethyst_bud",
        True,
        {BlockStateKeys.MinecraftBlockFace: minecraft_block_face},
    )


def MelonBlock() -> MinecraftBlockDescriptor:
    """Factory for MelonBlock"""
    return MinecraftBlockDescriptor("minecraft:melon_block", True)


def MelonStem(
    facing_direction: Optional[FacingDirection] = None, growth: Optional[Growth] = None
) -> MinecraftBlockDescriptor:
    """Factory for MelonStem"""
    return MinecraftBlockDescriptor(
        "minecraft:melon_stem",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.Growth: growth,
        },
    )


def MobSpawner() -> MinecraftBlockDescriptor:
    """Factory for MobSpawner"""
    return MinecraftBlockDescriptor("minecraft:mob_spawner", True)


def MossBlock() -> MinecraftBlockDescriptor:
    """Factory for MossBlock"""
    return MinecraftBlockDescriptor("minecraft:moss_block", True)


def MossCarpet() -> MinecraftBlockDescriptor:
    """Factory for MossCarpet"""
    return MinecraftBlockDescriptor("minecraft:moss_carpet", True)


def MossyCobblestone() -> MinecraftBlockDescriptor:
    """Factory for MossyCobblestone"""
    return MinecraftBlockDescriptor("minecraft:mossy_cobblestone", True)


def MossyCobblestoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyCobblestoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_cobblestone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MossyCobblestoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyCobblestoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_cobblestone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MossyCobblestoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyCobblestoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_cobblestone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def MossyCobblestoneWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyCobblestoneWall"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_cobblestone_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def MossyStoneBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyStoneBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_stone_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MossyStoneBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyStoneBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_stone_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MossyStoneBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyStoneBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_stone_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def MossyStoneBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MossyStoneBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:mossy_stone_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def MossyStoneBricks() -> MinecraftBlockDescriptor:
    """Factory for MossyStoneBricks"""
    return MinecraftBlockDescriptor("minecraft:mossy_stone_bricks", True)


def Mud() -> MinecraftBlockDescriptor:
    """Factory for Mud"""
    return MinecraftBlockDescriptor("minecraft:mud", True)


def MudBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MudBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mud_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MudBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MudBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:mud_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def MudBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MudBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:mud_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def MudBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MudBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:mud_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def MudBricks() -> MinecraftBlockDescriptor:
    """Factory for MudBricks"""
    return MinecraftBlockDescriptor("minecraft:mud_bricks", True)


def MuddyMangroveRoots(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MuddyMangroveRoots"""
    return MinecraftBlockDescriptor(
        "minecraft:muddy_mangrove_roots",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def MushroomStem(
    huge_mushroom_bits: Optional[HugeMushroomBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for MushroomStem"""
    return MinecraftBlockDescriptor(
        "minecraft:mushroom_stem",
        True,
        {BlockStateKeys.HugeMushroomBits: huge_mushroom_bits},
    )


def Mycelium() -> MinecraftBlockDescriptor:
    """Factory for Mycelium"""
    return MinecraftBlockDescriptor("minecraft:mycelium", True)


def NetherBrick() -> MinecraftBlockDescriptor:
    """Factory for NetherBrick"""
    return MinecraftBlockDescriptor("minecraft:nether_brick", True)


def NetherBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NetherBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:nether_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def NetherBrickFence() -> MinecraftBlockDescriptor:
    """Factory for NetherBrickFence"""
    return MinecraftBlockDescriptor("minecraft:nether_brick_fence", True)


def NetherBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NetherBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:nether_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def NetherBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NetherBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:nether_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def NetherBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NetherBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:nether_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def NetherGoldOre() -> MinecraftBlockDescriptor:
    """Factory for NetherGoldOre"""
    return MinecraftBlockDescriptor("minecraft:nether_gold_ore", True)


def NetherSprouts() -> MinecraftBlockDescriptor:
    """Factory for NetherSprouts"""
    return MinecraftBlockDescriptor("minecraft:nether_sprouts", True)


def NetherWart(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for NetherWart"""
    return MinecraftBlockDescriptor(
        "minecraft:nether_wart", True, {BlockStateKeys.Age: age}
    )


def NetherWartBlock() -> MinecraftBlockDescriptor:
    """Factory for NetherWartBlock"""
    return MinecraftBlockDescriptor("minecraft:nether_wart_block", True)


def NetheriteBlock() -> MinecraftBlockDescriptor:
    """Factory for NetheriteBlock"""
    return MinecraftBlockDescriptor("minecraft:netherite_block", True)


def Netherrack() -> MinecraftBlockDescriptor:
    """Factory for Netherrack"""
    return MinecraftBlockDescriptor("minecraft:netherrack", True)


def NormalStoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NormalStoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:normal_stone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def NormalStoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NormalStoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:normal_stone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def NormalStoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for NormalStoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:normal_stone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def Noteblock() -> MinecraftBlockDescriptor:
    """Factory for Noteblock"""
    return MinecraftBlockDescriptor("minecraft:noteblock", True)


def OakDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OakDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def OakFence() -> MinecraftBlockDescriptor:
    """Factory for OakFence"""
    return MinecraftBlockDescriptor("minecraft:oak_fence", True)


def OakHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OakHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def OakLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OakLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def OakLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for OakLog"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def OakPlanks() -> MinecraftBlockDescriptor:
    """Factory for OakPlanks"""
    return MinecraftBlockDescriptor("minecraft:oak_planks", True)


def OakSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for OakSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def OakShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OakShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def OakSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OakSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def OakStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OakStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def OakWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for OakWood"""
    return MinecraftBlockDescriptor(
        "minecraft:oak_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def Observer(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Observer"""
    return MinecraftBlockDescriptor(
        "minecraft:observer",
        True,
        {
            BlockStateKeys.MinecraftFacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def Obsidian() -> MinecraftBlockDescriptor:
    """Factory for Obsidian"""
    return MinecraftBlockDescriptor("minecraft:obsidian", True)


def OchreFroglight(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OchreFroglight"""
    return MinecraftBlockDescriptor(
        "minecraft:ochre_froglight", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def OpenEyeblossom() -> MinecraftBlockDescriptor:
    """Factory for OpenEyeblossom"""
    return MinecraftBlockDescriptor("minecraft:open_eyeblossom", True)


def OrangeCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for OrangeCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:orange_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def OrangeCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for OrangeCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:orange_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def OrangeCarpet() -> MinecraftBlockDescriptor:
    """Factory for OrangeCarpet"""
    return MinecraftBlockDescriptor("minecraft:orange_carpet", True)


def OrangeConcrete() -> MinecraftBlockDescriptor:
    """Factory for OrangeConcrete"""
    return MinecraftBlockDescriptor("minecraft:orange_concrete", True)


def OrangeConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for OrangeConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:orange_concrete_powder", True)


def OrangeGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OrangeGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:orange_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def OrangeShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for OrangeShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:orange_shulker_box", True)


def OrangeStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for OrangeStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:orange_stained_glass", True)


def OrangeStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for OrangeStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:orange_stained_glass_pane", True)


def OrangeTerracotta() -> MinecraftBlockDescriptor:
    """Factory for OrangeTerracotta"""
    return MinecraftBlockDescriptor("minecraft:orange_terracotta", True)


def OrangeTulip() -> MinecraftBlockDescriptor:
    """Factory for OrangeTulip"""
    return MinecraftBlockDescriptor("minecraft:orange_tulip", True)


def OrangeWool() -> MinecraftBlockDescriptor:
    """Factory for OrangeWool"""
    return MinecraftBlockDescriptor("minecraft:orange_wool", True)


def OxeyeDaisy() -> MinecraftBlockDescriptor:
    """Factory for OxeyeDaisy"""
    return MinecraftBlockDescriptor("minecraft:oxeye_daisy", True)


def OxidizedChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for OxidizedChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:oxidized_chiseled_copper", True)


def OxidizedCopper() -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopper"""
    return MinecraftBlockDescriptor("minecraft:oxidized_copper", True)


def OxidizedCopperBars() -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperBars"""
    return MinecraftBlockDescriptor("minecraft:oxidized_copper_bars", True)


def OxidizedCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def OxidizedCopperChain(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_chain",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def OxidizedCopperChest(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperChest"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_chest",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def OxidizedCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def OxidizedCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def OxidizedCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:oxidized_copper_grate", True)


def OxidizedCopperLantern(
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_lantern",
        True,
        {BlockStateKeys.Hanging: hanging},
    )


def OxidizedCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def OxidizedCutCopper() -> MinecraftBlockDescriptor:
    """Factory for OxidizedCutCopper"""
    return MinecraftBlockDescriptor("minecraft:oxidized_cut_copper", True)


def OxidizedCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def OxidizedCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def OxidizedDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def OxidizedLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for OxidizedLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:oxidized_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def PackedIce() -> MinecraftBlockDescriptor:
    """Factory for PackedIce"""
    return MinecraftBlockDescriptor("minecraft:packed_ice", True)


def PackedMud() -> MinecraftBlockDescriptor:
    """Factory for PackedMud"""
    return MinecraftBlockDescriptor("minecraft:packed_mud", True)


def PaleHangingMoss(tip: Optional[Tip] = None) -> MinecraftBlockDescriptor:
    """Factory for PaleHangingMoss"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_hanging_moss", True, {BlockStateKeys.Tip: tip}
    )


def PaleMossBlock() -> MinecraftBlockDescriptor:
    """Factory for PaleMossBlock"""
    return MinecraftBlockDescriptor("minecraft:pale_moss_block", True)


def PaleMossCarpet(
    pale_moss_carpet_side_east: Optional[PaleMossCarpetSideEast] = None,
    pale_moss_carpet_side_north: Optional[PaleMossCarpetSideNorth] = None,
    pale_moss_carpet_side_south: Optional[PaleMossCarpetSideSouth] = None,
    pale_moss_carpet_side_west: Optional[PaleMossCarpetSideWest] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleMossCarpet"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_moss_carpet",
        True,
        {
            BlockStateKeys.PaleMossCarpetSideEast: pale_moss_carpet_side_east,
            BlockStateKeys.PaleMossCarpetSideNorth: pale_moss_carpet_side_north,
            BlockStateKeys.PaleMossCarpetSideSouth: pale_moss_carpet_side_south,
            BlockStateKeys.PaleMossCarpetSideWest: pale_moss_carpet_side_west,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def PaleOakButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakButton"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def PaleOakDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def PaleOakDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PaleOakFence() -> MinecraftBlockDescriptor:
    """Factory for PaleOakFence"""
    return MinecraftBlockDescriptor("minecraft:pale_oak_fence", True)


def PaleOakFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def PaleOakHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def PaleOakLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def PaleOakLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for PaleOakLog"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def PaleOakPlanks() -> MinecraftBlockDescriptor:
    """Factory for PaleOakPlanks"""
    return MinecraftBlockDescriptor("minecraft:pale_oak_planks", True)


def PaleOakPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def PaleOakSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for PaleOakSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def PaleOakShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def PaleOakSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PaleOakStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PaleOakStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def PaleOakTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def PaleOakWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PaleOakWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def PaleOakWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for PaleOakWood"""
    return MinecraftBlockDescriptor(
        "minecraft:pale_oak_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def PearlescentFroglight(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PearlescentFroglight"""
    return MinecraftBlockDescriptor(
        "minecraft:pearlescent_froglight",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def Peony(upper_block_bit: Optional[UpperBlockBit] = None) -> MinecraftBlockDescriptor:
    """Factory for Peony"""
    return MinecraftBlockDescriptor(
        "minecraft:peony", True, {BlockStateKeys.UpperBlockBit: upper_block_bit}
    )


def PetrifiedOakDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PetrifiedOakDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:petrified_oak_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PetrifiedOakSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PetrifiedOakSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:petrified_oak_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PiglinHead(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PiglinHead"""
    return MinecraftBlockDescriptor(
        "minecraft:piglin_head",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def PinkCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for PinkCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:pink_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def PinkCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for PinkCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:pink_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def PinkCarpet() -> MinecraftBlockDescriptor:
    """Factory for PinkCarpet"""
    return MinecraftBlockDescriptor("minecraft:pink_carpet", True)


def PinkConcrete() -> MinecraftBlockDescriptor:
    """Factory for PinkConcrete"""
    return MinecraftBlockDescriptor("minecraft:pink_concrete", True)


def PinkConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for PinkConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:pink_concrete_powder", True)


def PinkGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PinkGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:pink_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def PinkPetals(
    growth: Optional[Growth] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PinkPetals"""
    return MinecraftBlockDescriptor(
        "minecraft:pink_petals",
        True,
        {
            BlockStateKeys.Growth: growth,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def PinkShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for PinkShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:pink_shulker_box", True)


def PinkStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for PinkStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:pink_stained_glass", True)


def PinkStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for PinkStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:pink_stained_glass_pane", True)


def PinkTerracotta() -> MinecraftBlockDescriptor:
    """Factory for PinkTerracotta"""
    return MinecraftBlockDescriptor("minecraft:pink_terracotta", True)


def PinkTulip() -> MinecraftBlockDescriptor:
    """Factory for PinkTulip"""
    return MinecraftBlockDescriptor("minecraft:pink_tulip", True)


def PinkWool() -> MinecraftBlockDescriptor:
    """Factory for PinkWool"""
    return MinecraftBlockDescriptor("minecraft:pink_wool", True)


def Piston(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Piston"""
    return MinecraftBlockDescriptor(
        "minecraft:piston",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def PistonArmCollision(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PistonArmCollision"""
    return MinecraftBlockDescriptor(
        "minecraft:piston_arm_collision",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def PitcherCrop(
    growth: Optional[Growth] = None, upper_block_bit: Optional[UpperBlockBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for PitcherCrop"""
    return MinecraftBlockDescriptor(
        "minecraft:pitcher_crop",
        True,
        {
            BlockStateKeys.Growth: growth,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def PitcherPlant(
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PitcherPlant"""
    return MinecraftBlockDescriptor(
        "minecraft:pitcher_plant",
        True,
        {BlockStateKeys.UpperBlockBit: upper_block_bit},
    )


def PlayerHead(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PlayerHead"""
    return MinecraftBlockDescriptor(
        "minecraft:player_head",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def Podzol() -> MinecraftBlockDescriptor:
    """Factory for Podzol"""
    return MinecraftBlockDescriptor("minecraft:podzol", True)


def PointedDripstone(
    dripstone_thickness: Optional[DripstoneThickness] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PointedDripstone"""
    return MinecraftBlockDescriptor(
        "minecraft:pointed_dripstone",
        True,
        {
            BlockStateKeys.DripstoneThickness: dripstone_thickness,
            BlockStateKeys.Hanging: hanging,
        },
    )


def PolishedAndesite() -> MinecraftBlockDescriptor:
    """Factory for PolishedAndesite"""
    return MinecraftBlockDescriptor("minecraft:polished_andesite", True)


def PolishedAndesiteDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedAndesiteDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_andesite_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedAndesiteSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedAndesiteSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_andesite_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedAndesiteStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedAndesiteStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_andesite_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedBasalt(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBasalt"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_basalt", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def PolishedBlackstone() -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstone"""
    return MinecraftBlockDescriptor("minecraft:polished_blackstone", True)


def PolishedBlackstoneBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedBlackstoneBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedBlackstoneBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedBlackstoneBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def PolishedBlackstoneBricks() -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneBricks"""
    return MinecraftBlockDescriptor("minecraft:polished_blackstone_bricks", True)


def PolishedBlackstoneButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneButton"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def PolishedBlackstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedBlackstonePressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstonePressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def PolishedBlackstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedBlackstoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedBlackstoneWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedBlackstoneWall"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_blackstone_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def PolishedDeepslate() -> MinecraftBlockDescriptor:
    """Factory for PolishedDeepslate"""
    return MinecraftBlockDescriptor("minecraft:polished_deepslate", True)


def PolishedDeepslateDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDeepslateDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_deepslate_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedDeepslateSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDeepslateSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_deepslate_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedDeepslateStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDeepslateStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_deepslate_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedDeepslateWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDeepslateWall"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_deepslate_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def PolishedDiorite() -> MinecraftBlockDescriptor:
    """Factory for PolishedDiorite"""
    return MinecraftBlockDescriptor("minecraft:polished_diorite", True)


def PolishedDioriteDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDioriteDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_diorite_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedDioriteSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDioriteSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_diorite_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedDioriteStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedDioriteStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_diorite_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedGranite() -> MinecraftBlockDescriptor:
    """Factory for PolishedGranite"""
    return MinecraftBlockDescriptor("minecraft:polished_granite", True)


def PolishedGraniteDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedGraniteDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_granite_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedGraniteSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedGraniteSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_granite_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedGraniteStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedGraniteStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_granite_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedTuff() -> MinecraftBlockDescriptor:
    """Factory for PolishedTuff"""
    return MinecraftBlockDescriptor("minecraft:polished_tuff", True)


def PolishedTuffDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedTuffDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_tuff_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedTuffSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedTuffSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_tuff_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PolishedTuffStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedTuffStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_tuff_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PolishedTuffWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PolishedTuffWall"""
    return MinecraftBlockDescriptor(
        "minecraft:polished_tuff_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Poppy() -> MinecraftBlockDescriptor:
    """Factory for Poppy"""
    return MinecraftBlockDescriptor("minecraft:poppy", True)


def Portal(portal_axis: Optional[PortalAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for Portal"""
    return MinecraftBlockDescriptor(
        "minecraft:portal", True, {BlockStateKeys.PortalAxis: portal_axis}
    )


def Potatoes(growth: Optional[Growth] = None) -> MinecraftBlockDescriptor:
    """Factory for Potatoes"""
    return MinecraftBlockDescriptor(
        "minecraft:potatoes", True, {BlockStateKeys.Growth: growth}
    )


def PowderSnow() -> MinecraftBlockDescriptor:
    """Factory for PowderSnow"""
    return MinecraftBlockDescriptor("minecraft:powder_snow", True)


def PoweredComparator(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    output_lit_bit: Optional[OutputLitBit] = None,
    output_subtract_bit: Optional[OutputSubtractBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PoweredComparator"""
    return MinecraftBlockDescriptor(
        "minecraft:powered_comparator",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OutputLitBit: output_lit_bit,
            BlockStateKeys.OutputSubtractBit: output_subtract_bit,
        },
    )


def PoweredRepeater(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    repeater_delay: Optional[RepeaterDelay] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PoweredRepeater"""
    return MinecraftBlockDescriptor(
        "minecraft:powered_repeater",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.RepeaterDelay: repeater_delay,
        },
    )


def Prismarine() -> MinecraftBlockDescriptor:
    """Factory for Prismarine"""
    return MinecraftBlockDescriptor("minecraft:prismarine", True)


def PrismarineBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PrismarineBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PrismarineBricks() -> MinecraftBlockDescriptor:
    """Factory for PrismarineBricks"""
    return MinecraftBlockDescriptor("minecraft:prismarine_bricks", True)


def PrismarineBricksStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineBricksStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_bricks_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PrismarineDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PrismarineSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PrismarineStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def PrismarineWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PrismarineWall"""
    return MinecraftBlockDescriptor(
        "minecraft:prismarine_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Pumpkin(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Pumpkin"""
    return MinecraftBlockDescriptor(
        "minecraft:pumpkin",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def PumpkinStem(
    facing_direction: Optional[FacingDirection] = None, growth: Optional[Growth] = None
) -> MinecraftBlockDescriptor:
    """Factory for PumpkinStem"""
    return MinecraftBlockDescriptor(
        "minecraft:pumpkin_stem",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.Growth: growth,
        },
    )


def PurpleCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for PurpleCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:purple_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def PurpleCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for PurpleCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:purple_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def PurpleCarpet() -> MinecraftBlockDescriptor:
    """Factory for PurpleCarpet"""
    return MinecraftBlockDescriptor("minecraft:purple_carpet", True)


def PurpleConcrete() -> MinecraftBlockDescriptor:
    """Factory for PurpleConcrete"""
    return MinecraftBlockDescriptor("minecraft:purple_concrete", True)


def PurpleConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for PurpleConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:purple_concrete_powder", True)


def PurpleGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PurpleGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:purple_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def PurpleShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for PurpleShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:purple_shulker_box", True)


def PurpleStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for PurpleStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:purple_stained_glass", True)


def PurpleStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for PurpleStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:purple_stained_glass_pane", True)


def PurpleTerracotta() -> MinecraftBlockDescriptor:
    """Factory for PurpleTerracotta"""
    return MinecraftBlockDescriptor("minecraft:purple_terracotta", True)


def PurpleWool() -> MinecraftBlockDescriptor:
    """Factory for PurpleWool"""
    return MinecraftBlockDescriptor("minecraft:purple_wool", True)


def PurpurBlock(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for PurpurBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:purpur_block", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def PurpurDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PurpurDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:purpur_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PurpurPillar(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for PurpurPillar"""
    return MinecraftBlockDescriptor(
        "minecraft:purpur_pillar", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def PurpurSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PurpurSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:purpur_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def PurpurStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for PurpurStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:purpur_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def QuartzBlock(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for QuartzBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:quartz_block", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def QuartzBricks() -> MinecraftBlockDescriptor:
    """Factory for QuartzBricks"""
    return MinecraftBlockDescriptor("minecraft:quartz_bricks", True)


def QuartzDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for QuartzDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:quartz_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def QuartzOre() -> MinecraftBlockDescriptor:
    """Factory for QuartzOre"""
    return MinecraftBlockDescriptor("minecraft:quartz_ore", True)


def QuartzPillar(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for QuartzPillar"""
    return MinecraftBlockDescriptor(
        "minecraft:quartz_pillar", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def QuartzSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for QuartzSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:quartz_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def QuartzStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for QuartzStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:quartz_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def Rail(rail_direction: Optional[RailDirection] = None) -> MinecraftBlockDescriptor:
    """Factory for Rail"""
    return MinecraftBlockDescriptor(
        "minecraft:rail", True, {BlockStateKeys.RailDirection: rail_direction}
    )


def RawCopperBlock() -> MinecraftBlockDescriptor:
    """Factory for RawCopperBlock"""
    return MinecraftBlockDescriptor("minecraft:raw_copper_block", True)


def RawGoldBlock() -> MinecraftBlockDescriptor:
    """Factory for RawGoldBlock"""
    return MinecraftBlockDescriptor("minecraft:raw_gold_block", True)


def RawIronBlock() -> MinecraftBlockDescriptor:
    """Factory for RawIronBlock"""
    return MinecraftBlockDescriptor("minecraft:raw_iron_block", True)


def RedCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for RedCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:red_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def RedCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for RedCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:red_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def RedCarpet() -> MinecraftBlockDescriptor:
    """Factory for RedCarpet"""
    return MinecraftBlockDescriptor("minecraft:red_carpet", True)


def RedConcrete() -> MinecraftBlockDescriptor:
    """Factory for RedConcrete"""
    return MinecraftBlockDescriptor("minecraft:red_concrete", True)


def RedConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for RedConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:red_concrete_powder", True)


def RedGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:red_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def RedMushroom() -> MinecraftBlockDescriptor:
    """Factory for RedMushroom"""
    return MinecraftBlockDescriptor("minecraft:red_mushroom", True)


def RedMushroomBlock(
    huge_mushroom_bits: Optional[HugeMushroomBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedMushroomBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:red_mushroom_block",
        True,
        {BlockStateKeys.HugeMushroomBits: huge_mushroom_bits},
    )


def RedNetherBrick() -> MinecraftBlockDescriptor:
    """Factory for RedNetherBrick"""
    return MinecraftBlockDescriptor("minecraft:red_nether_brick", True)


def RedNetherBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedNetherBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:red_nether_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def RedNetherBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedNetherBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:red_nether_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def RedNetherBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedNetherBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:red_nether_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def RedNetherBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedNetherBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:red_nether_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def RedSand() -> MinecraftBlockDescriptor:
    """Factory for RedSand"""
    return MinecraftBlockDescriptor("minecraft:red_sand", True)


def RedSandstone() -> MinecraftBlockDescriptor:
    """Factory for RedSandstone"""
    return MinecraftBlockDescriptor("minecraft:red_sandstone", True)


def RedSandstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedSandstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:red_sandstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def RedSandstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedSandstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:red_sandstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def RedSandstoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedSandstoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:red_sandstone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def RedSandstoneWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedSandstoneWall"""
    return MinecraftBlockDescriptor(
        "minecraft:red_sandstone_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def RedShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for RedShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:red_shulker_box", True)


def RedStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for RedStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:red_stained_glass", True)


def RedStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for RedStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:red_stained_glass_pane", True)


def RedTerracotta() -> MinecraftBlockDescriptor:
    """Factory for RedTerracotta"""
    return MinecraftBlockDescriptor("minecraft:red_terracotta", True)


def RedTulip() -> MinecraftBlockDescriptor:
    """Factory for RedTulip"""
    return MinecraftBlockDescriptor("minecraft:red_tulip", True)


def RedWool() -> MinecraftBlockDescriptor:
    """Factory for RedWool"""
    return MinecraftBlockDescriptor("minecraft:red_wool", True)


def RedstoneBlock() -> MinecraftBlockDescriptor:
    """Factory for RedstoneBlock"""
    return MinecraftBlockDescriptor("minecraft:redstone_block", True)


def RedstoneLamp() -> MinecraftBlockDescriptor:
    """Factory for RedstoneLamp"""
    return MinecraftBlockDescriptor("minecraft:redstone_lamp", True)


def RedstoneOre() -> MinecraftBlockDescriptor:
    """Factory for RedstoneOre"""
    return MinecraftBlockDescriptor("minecraft:redstone_ore", True)


def RedstoneTorch(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedstoneTorch"""
    return MinecraftBlockDescriptor(
        "minecraft:redstone_torch",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def RedstoneWire(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RedstoneWire"""
    return MinecraftBlockDescriptor(
        "minecraft:redstone_wire",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def Reeds(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for Reeds"""
    return MinecraftBlockDescriptor("minecraft:reeds", True, {BlockStateKeys.Age: age})


def ReinforcedDeepslate() -> MinecraftBlockDescriptor:
    """Factory for ReinforcedDeepslate"""
    return MinecraftBlockDescriptor("minecraft:reinforced_deepslate", True)


def RepeatingCommandBlock(
    conditional_bit: Optional[ConditionalBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RepeatingCommandBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:repeating_command_block",
        True,
        {
            BlockStateKeys.ConditionalBit: conditional_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def ResinBlock() -> MinecraftBlockDescriptor:
    """Factory for ResinBlock"""
    return MinecraftBlockDescriptor("minecraft:resin_block", True)


def ResinBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ResinBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:resin_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def ResinBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ResinBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:resin_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def ResinBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ResinBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:resin_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def ResinBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ResinBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:resin_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def ResinBricks() -> MinecraftBlockDescriptor:
    """Factory for ResinBricks"""
    return MinecraftBlockDescriptor("minecraft:resin_bricks", True)


def ResinClump(
    multi_face_direction_bits: Optional[MultiFaceDirectionBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ResinClump"""
    return MinecraftBlockDescriptor(
        "minecraft:resin_clump",
        True,
        {BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits},
    )


def RespawnAnchor(
    respawn_anchor_charge: Optional[RespawnAnchorCharge] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RespawnAnchor"""
    return MinecraftBlockDescriptor(
        "minecraft:respawn_anchor",
        True,
        {BlockStateKeys.RespawnAnchorCharge: respawn_anchor_charge},
    )


def RoseBush(
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for RoseBush"""
    return MinecraftBlockDescriptor(
        "minecraft:rose_bush",
        True,
        {BlockStateKeys.UpperBlockBit: upper_block_bit},
    )


def Sand() -> MinecraftBlockDescriptor:
    """Factory for Sand"""
    return MinecraftBlockDescriptor("minecraft:sand", True)


def Sandstone() -> MinecraftBlockDescriptor:
    """Factory for Sandstone"""
    return MinecraftBlockDescriptor("minecraft:sandstone", True)


def SandstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SandstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:sandstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SandstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SandstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:sandstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SandstoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SandstoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:sandstone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def SandstoneWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SandstoneWall"""
    return MinecraftBlockDescriptor(
        "minecraft:sandstone_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def Scaffolding(
    stability: Optional[Stability] = None,
    stability_check: Optional[StabilityCheck] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Scaffolding"""
    return MinecraftBlockDescriptor(
        "minecraft:scaffolding",
        True,
        {
            BlockStateKeys.Stability: stability,
            BlockStateKeys.StabilityCheck: stability_check,
        },
    )


def Sculk() -> MinecraftBlockDescriptor:
    """Factory for Sculk"""
    return MinecraftBlockDescriptor("minecraft:sculk", True)


def SculkCatalyst(bloom: Optional[Bloom] = None) -> MinecraftBlockDescriptor:
    """Factory for SculkCatalyst"""
    return MinecraftBlockDescriptor(
        "minecraft:sculk_catalyst", True, {BlockStateKeys.Bloom: bloom}
    )


def SculkSensor(
    sculk_sensor_phase: Optional[SculkSensorPhase] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SculkSensor"""
    return MinecraftBlockDescriptor(
        "minecraft:sculk_sensor",
        True,
        {BlockStateKeys.SculkSensorPhase: sculk_sensor_phase},
    )


def SculkShrieker(
    active: Optional[Active] = None, can_summon: Optional[CanSummon] = None
) -> MinecraftBlockDescriptor:
    """Factory for SculkShrieker"""
    return MinecraftBlockDescriptor(
        "minecraft:sculk_shrieker",
        True,
        {BlockStateKeys.Active: active, BlockStateKeys.CanSummon: can_summon},
    )


def SculkVein(
    multi_face_direction_bits: Optional[MultiFaceDirectionBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SculkVein"""
    return MinecraftBlockDescriptor(
        "minecraft:sculk_vein",
        True,
        {BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits},
    )


def SeaLantern() -> MinecraftBlockDescriptor:
    """Factory for SeaLantern"""
    return MinecraftBlockDescriptor("minecraft:sea_lantern", True)


def SeaPickle(
    cluster_count: Optional[ClusterCount] = None, dead_bit: Optional[DeadBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for SeaPickle"""
    return MinecraftBlockDescriptor(
        "minecraft:sea_pickle",
        True,
        {
            BlockStateKeys.ClusterCount: cluster_count,
            BlockStateKeys.DeadBit: dead_bit,
        },
    )


def Seagrass(sea_grass_type: Optional[SeaGrassType] = None) -> MinecraftBlockDescriptor:
    """Factory for Seagrass"""
    return MinecraftBlockDescriptor(
        "minecraft:seagrass", True, {BlockStateKeys.SeaGrassType: sea_grass_type}
    )


def ShortDryGrass() -> MinecraftBlockDescriptor:
    """Factory for ShortDryGrass"""
    return MinecraftBlockDescriptor("minecraft:short_dry_grass", True)


def ShortGrass() -> MinecraftBlockDescriptor:
    """Factory for ShortGrass"""
    return MinecraftBlockDescriptor("minecraft:short_grass", True)


def Shroomlight() -> MinecraftBlockDescriptor:
    """Factory for Shroomlight"""
    return MinecraftBlockDescriptor("minecraft:shroomlight", True)


def SilverGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SilverGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:silver_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def SkeletonSkull(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SkeletonSkull"""
    return MinecraftBlockDescriptor(
        "minecraft:skeleton_skull",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def Slime() -> MinecraftBlockDescriptor:
    """Factory for Slime"""
    return MinecraftBlockDescriptor("minecraft:slime", True)


def SmallAmethystBud(
    minecraft_block_face: Optional[BlockFace] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmallAmethystBud"""
    return MinecraftBlockDescriptor(
        "minecraft:small_amethyst_bud",
        True,
        {BlockStateKeys.MinecraftBlockFace: minecraft_block_face},
    )


def SmallDripleafBlock(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmallDripleafBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:small_dripleaf_block",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def SmithingTable() -> MinecraftBlockDescriptor:
    """Factory for SmithingTable"""
    return MinecraftBlockDescriptor("minecraft:smithing_table", True)


def Smoker(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Smoker"""
    return MinecraftBlockDescriptor(
        "minecraft:smoker",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def SmoothBasalt() -> MinecraftBlockDescriptor:
    """Factory for SmoothBasalt"""
    return MinecraftBlockDescriptor("minecraft:smooth_basalt", True)


def SmoothQuartz(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for SmoothQuartz"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_quartz", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def SmoothQuartzDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothQuartzDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_quartz_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothQuartzSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothQuartzSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_quartz_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothQuartzStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothQuartzStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_quartz_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def SmoothRedSandstone() -> MinecraftBlockDescriptor:
    """Factory for SmoothRedSandstone"""
    return MinecraftBlockDescriptor("minecraft:smooth_red_sandstone", True)


def SmoothRedSandstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothRedSandstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_red_sandstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothRedSandstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothRedSandstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_red_sandstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothRedSandstoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothRedSandstoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_red_sandstone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def SmoothSandstone() -> MinecraftBlockDescriptor:
    """Factory for SmoothSandstone"""
    return MinecraftBlockDescriptor("minecraft:smooth_sandstone", True)


def SmoothSandstoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothSandstoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_sandstone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothSandstoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothSandstoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_sandstone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothSandstoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothSandstoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_sandstone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def SmoothStone() -> MinecraftBlockDescriptor:
    """Factory for SmoothStone"""
    return MinecraftBlockDescriptor("minecraft:smooth_stone", True)


def SmoothStoneDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothStoneDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_stone_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SmoothStoneSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SmoothStoneSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:smooth_stone_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SnifferEgg(
    cracked_state: Optional[CrackedState] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SnifferEgg"""
    return MinecraftBlockDescriptor(
        "minecraft:sniffer_egg", True, {BlockStateKeys.CrackedState: cracked_state}
    )


def Snow() -> MinecraftBlockDescriptor:
    """Factory for Snow"""
    return MinecraftBlockDescriptor("minecraft:snow", True)


def SnowLayer(
    covered_bit: Optional[CoveredBit] = None, height: Optional[Height] = None
) -> MinecraftBlockDescriptor:
    """Factory for SnowLayer"""
    return MinecraftBlockDescriptor(
        "minecraft:snow_layer",
        True,
        {BlockStateKeys.CoveredBit: covered_bit, BlockStateKeys.Height: height},
    )


def SoulCampfire(
    extinguished: Optional[Extinguished] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SoulCampfire"""
    return MinecraftBlockDescriptor(
        "minecraft:soul_campfire",
        True,
        {
            BlockStateKeys.Extinguished: extinguished,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def SoulFire(age: Optional[Age] = None) -> MinecraftBlockDescriptor:
    """Factory for SoulFire"""
    return MinecraftBlockDescriptor(
        "minecraft:soul_fire", True, {BlockStateKeys.Age: age}
    )


def SoulLantern(hanging: Optional[Hanging] = None) -> MinecraftBlockDescriptor:
    """Factory for SoulLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:soul_lantern", True, {BlockStateKeys.Hanging: hanging}
    )


def SoulSand() -> MinecraftBlockDescriptor:
    """Factory for SoulSand"""
    return MinecraftBlockDescriptor("minecraft:soul_sand", True)


def SoulSoil() -> MinecraftBlockDescriptor:
    """Factory for SoulSoil"""
    return MinecraftBlockDescriptor("minecraft:soul_soil", True)


def SoulTorch(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SoulTorch"""
    return MinecraftBlockDescriptor(
        "minecraft:soul_torch",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def Sponge() -> MinecraftBlockDescriptor:
    """Factory for Sponge"""
    return MinecraftBlockDescriptor("minecraft:sponge", True)


def SporeBlossom() -> MinecraftBlockDescriptor:
    """Factory for SporeBlossom"""
    return MinecraftBlockDescriptor("minecraft:spore_blossom", True)


def SpruceButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceButton"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def SpruceDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def SpruceDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SpruceFence() -> MinecraftBlockDescriptor:
    """Factory for SpruceFence"""
    return MinecraftBlockDescriptor("minecraft:spruce_fence", True)


def SpruceFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def SpruceHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def SpruceLeaves(
    persistent_bit: Optional[PersistentBit] = None,
    update_bit: Optional[UpdateBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceLeaves"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_leaves",
        True,
        {
            BlockStateKeys.PersistentBit: persistent_bit,
            BlockStateKeys.UpdateBit: update_bit,
        },
    )


def SpruceLog(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for SpruceLog"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_log", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def SprucePlanks() -> MinecraftBlockDescriptor:
    """Factory for SprucePlanks"""
    return MinecraftBlockDescriptor("minecraft:spruce_planks", True)


def SprucePressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SprucePressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def SpruceSapling(age_bit: Optional[AgeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for SpruceSapling"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_sapling", True, {BlockStateKeys.AgeBit: age_bit}
    )


def SpruceShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def SpruceSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def SpruceStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def SpruceStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def SpruceTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def SpruceWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SpruceWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def SpruceWood(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for SpruceWood"""
    return MinecraftBlockDescriptor(
        "minecraft:spruce_wood", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def StandingBanner(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StandingBanner"""
    return MinecraftBlockDescriptor(
        "minecraft:standing_banner",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def StandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def StickyPiston(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StickyPiston"""
    return MinecraftBlockDescriptor(
        "minecraft:sticky_piston",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def StickyPistonArmCollision(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StickyPistonArmCollision"""
    return MinecraftBlockDescriptor(
        "minecraft:sticky_piston_arm_collision",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def Stone() -> MinecraftBlockDescriptor:
    """Factory for Stone"""
    return MinecraftBlockDescriptor("minecraft:stone", True)


def StoneBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StoneBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def StoneBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StoneBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def StoneBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StoneBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def StoneBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StoneBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def StoneBricks() -> MinecraftBlockDescriptor:
    """Factory for StoneBricks"""
    return MinecraftBlockDescriptor("minecraft:stone_bricks", True)


def StoneButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StoneButton"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def StonePressurePlate(
    redstone_signal: Optional[RedstoneSignal | None] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StonePressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def StoneStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StoneStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:stone_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def StonecutterBlock(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StonecutterBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:stonecutter_block",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def StrippedAcaciaLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedAcaciaLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_acacia_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedAcaciaWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedAcaciaWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_acacia_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedBambooBlock(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedBambooBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_bamboo_block",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedBirchLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedBirchLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_birch_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedBirchWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedBirchWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_birch_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedCherryLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedCherryLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_cherry_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedCherryWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedCherryWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_cherry_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedCrimsonHyphae(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedCrimsonHyphae"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_crimson_hyphae",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedCrimsonStem(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedCrimsonStem"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_crimson_stem",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedDarkOakLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedDarkOakLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_dark_oak_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedDarkOakWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedDarkOakWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_dark_oak_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedJungleLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedJungleLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_jungle_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedJungleWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedJungleWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_jungle_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedMangroveLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedMangroveLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_mangrove_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedMangroveWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedMangroveWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_mangrove_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedOakLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedOakLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_oak_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedOakWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedOakWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_oak_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedPaleOakLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedPaleOakLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_pale_oak_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedPaleOakWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedPaleOakWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_pale_oak_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedSpruceLog(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedSpruceLog"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_spruce_log",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedSpruceWood(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedSpruceWood"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_spruce_wood",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedWarpedHyphae(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedWarpedHyphae"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_warped_hyphae",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StrippedWarpedStem(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StrippedWarpedStem"""
    return MinecraftBlockDescriptor(
        "minecraft:stripped_warped_stem",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def StructureBlock(
    structure_block_type: Optional[StructureBlockType] = None,
) -> MinecraftBlockDescriptor:
    """Factory for StructureBlock"""
    return MinecraftBlockDescriptor(
        "minecraft:structure_block",
        True,
        {BlockStateKeys.StructureBlockType: structure_block_type},
    )


def StructureVoid() -> MinecraftBlockDescriptor:
    """Factory for StructureVoid"""
    return MinecraftBlockDescriptor("minecraft:structure_void", True)


def Sunflower(
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Sunflower"""
    return MinecraftBlockDescriptor(
        "minecraft:sunflower",
        True,
        {BlockStateKeys.UpperBlockBit: upper_block_bit},
    )


def SuspiciousGravel(
    brushed_progress: Optional[BrushedProgress] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SuspiciousGravel"""
    return MinecraftBlockDescriptor(
        "minecraft:suspicious_gravel",
        True,
        {
            BlockStateKeys.BrushedProgress: brushed_progress,
            BlockStateKeys.Hanging: hanging,
        },
    )


def SuspiciousSand(
    brushed_progress: Optional[BrushedProgress] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for SuspiciousSand"""
    return MinecraftBlockDescriptor(
        "minecraft:suspicious_sand",
        True,
        {
            BlockStateKeys.BrushedProgress: brushed_progress,
            BlockStateKeys.Hanging: hanging,
        },
    )


def SweetBerryBush(growth: Optional[Growth] = None) -> MinecraftBlockDescriptor:
    """Factory for SweetBerryBush"""
    return MinecraftBlockDescriptor(
        "minecraft:sweet_berry_bush", True, {BlockStateKeys.Growth: growth}
    )


def TallDryGrass() -> MinecraftBlockDescriptor:
    """Factory for TallDryGrass"""
    return MinecraftBlockDescriptor("minecraft:tall_dry_grass", True)


def TallGrass(
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TallGrass"""
    return MinecraftBlockDescriptor(
        "minecraft:tall_grass",
        True,
        {BlockStateKeys.UpperBlockBit: upper_block_bit},
    )


def Target() -> MinecraftBlockDescriptor:
    """Factory for Target"""
    return MinecraftBlockDescriptor("minecraft:target", True)


def TintedGlass() -> MinecraftBlockDescriptor:
    """Factory for TintedGlass"""
    return MinecraftBlockDescriptor("minecraft:tinted_glass", True)


def Tnt(explode_bit: Optional[ExplodeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for Tnt"""
    return MinecraftBlockDescriptor(
        "minecraft:tnt", True, {BlockStateKeys.ExplodeBit: explode_bit}
    )


def Torch(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Torch"""
    return MinecraftBlockDescriptor(
        "minecraft:torch",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def Torchflower() -> MinecraftBlockDescriptor:
    """Factory for Torchflower"""
    return MinecraftBlockDescriptor("minecraft:torchflower", True)


def TorchflowerCrop(growth: Optional[Growth] = None) -> MinecraftBlockDescriptor:
    """Factory for TorchflowerCrop"""
    return MinecraftBlockDescriptor(
        "minecraft:torchflower_crop", True, {BlockStateKeys.Growth: growth}
    )


def Trapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Trapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def TrappedChest(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TrappedChest"""
    return MinecraftBlockDescriptor(
        "minecraft:trapped_chest",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
    )


def TrialSpawner(
    ominous: Optional[Ominous] = None,
    trial_spawner_state: Optional[TrialSpawnerState] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TrialSpawner"""
    return MinecraftBlockDescriptor(
        "minecraft:trial_spawner",
        True,
        {
            BlockStateKeys.Ominous: ominous,
            BlockStateKeys.TrialSpawnerState: trial_spawner_state,
        },
    )


def TripWire(
    attached_bit: Optional[AttachedBit] = None,
    disarmed_bit: Optional[DisarmedBit] = None,
    powered_bit: Optional[PoweredBit] = None,
    suspended_bit: Optional[SuspendedBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TripWire"""
    return MinecraftBlockDescriptor(
        "minecraft:trip_wire",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.DisarmedBit: disarmed_bit,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.SuspendedBit: suspended_bit,
        },
    )


def TripwireHook(
    attached_bit: Optional[AttachedBit] = None,
    direction: Optional[Direction] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TripwireHook"""
    return MinecraftBlockDescriptor(
        "minecraft:tripwire_hook",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.Direction: direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def TubeCoral() -> MinecraftBlockDescriptor:
    """Factory for TubeCoral"""
    return MinecraftBlockDescriptor("minecraft:tube_coral", True)


def TubeCoralBlock() -> MinecraftBlockDescriptor:
    """Factory for TubeCoralBlock"""
    return MinecraftBlockDescriptor("minecraft:tube_coral_block", True)


def TubeCoralFan(
    coral_fan_direction: Optional[CoralFanDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TubeCoralFan"""
    return MinecraftBlockDescriptor(
        "minecraft:tube_coral_fan",
        True,
        {BlockStateKeys.CoralFanDirection: coral_fan_direction},
    )


def TubeCoralWallFan(
    coral_direction: Optional[CoralDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TubeCoralWallFan"""
    return MinecraftBlockDescriptor(
        "minecraft:tube_coral_wall_fan",
        True,
        {BlockStateKeys.CoralDirection: coral_direction},
    )


def Tuff() -> MinecraftBlockDescriptor:
    """Factory for Tuff"""
    return MinecraftBlockDescriptor("minecraft:tuff", True)


def TuffBrickDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffBrickDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_brick_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def TuffBrickSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffBrickSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_brick_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def TuffBrickStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffBrickStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_brick_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def TuffBrickWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffBrickWall"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_brick_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def TuffBricks() -> MinecraftBlockDescriptor:
    """Factory for TuffBricks"""
    return MinecraftBlockDescriptor("minecraft:tuff_bricks", True)


def TuffDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def TuffSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def TuffStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def TuffWall(
    wall_connection_type_east: Optional[WallConnectionTypeEast] = None,
    wall_connection_type_north: Optional[WallConnectionTypeNorth] = None,
    wall_connection_type_south: Optional[WallConnectionTypeSouth] = None,
    wall_connection_type_west: Optional[WallConnectionTypeWest] = None,
    wall_post_bit: Optional[WallPostBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TuffWall"""
    return MinecraftBlockDescriptor(
        "minecraft:tuff_wall",
        True,
        {
            BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
            BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
            BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
            BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
            BlockStateKeys.WallPostBit: wall_post_bit,
        },
    )


def TurtleEgg(
    cracked_state: Optional[CrackedState] = None,
    turtle_egg_count: Optional[TurtleEggCount] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TurtleEgg"""
    return MinecraftBlockDescriptor(
        "minecraft:turtle_egg",
        True,
        {
            BlockStateKeys.CrackedState: cracked_state,
            BlockStateKeys.TurtleEggCount: turtle_egg_count,
        },
    )


def TwistingVines(
    twisting_vines_age: Optional[TwistingVinesAge] = None,
) -> MinecraftBlockDescriptor:
    """Factory for TwistingVines"""
    return MinecraftBlockDescriptor(
        "minecraft:twisting_vines",
        True,
        {BlockStateKeys.TwistingVinesAge: twisting_vines_age},
    )


def UnderwaterTnt(explode_bit: Optional[ExplodeBit] = None) -> MinecraftBlockDescriptor:
    """Factory for UnderwaterTnt"""
    return MinecraftBlockDescriptor(
        "minecraft:underwater_tnt", True, {BlockStateKeys.ExplodeBit: explode_bit}
    )


def UnderwaterTorch(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for UnderwaterTorch"""
    return MinecraftBlockDescriptor(
        "minecraft:underwater_torch",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def UndyedShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for UndyedShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:undyed_shulker_box", True)


def Unknown() -> MinecraftBlockDescriptor:
    """Factory for Unknown"""
    return MinecraftBlockDescriptor("minecraft:unknown", True)


def UnlitRedstoneTorch(
    torch_facing_direction: Optional[TorchFacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for UnlitRedstoneTorch"""
    return MinecraftBlockDescriptor(
        "minecraft:unlit_redstone_torch",
        True,
        {BlockStateKeys.TorchFacingDirection: torch_facing_direction},
    )


def UnpoweredComparator(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    output_lit_bit: Optional[OutputLitBit] = None,
    output_subtract_bit: Optional[OutputSubtractBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for UnpoweredComparator"""
    return MinecraftBlockDescriptor(
        "minecraft:unpowered_comparator",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OutputLitBit: output_lit_bit,
            BlockStateKeys.OutputSubtractBit: output_subtract_bit,
        },
    )


def UnpoweredRepeater(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    repeater_delay: Optional[RepeaterDelay] = None,
) -> MinecraftBlockDescriptor:
    """Factory for UnpoweredRepeater"""
    return MinecraftBlockDescriptor(
        "minecraft:unpowered_repeater",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.RepeaterDelay: repeater_delay,
        },
    )


def Vault(
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    ominous: Optional[Ominous] = None,
    vault_state: Optional[VaultState] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Vault"""
    return MinecraftBlockDescriptor(
        "minecraft:vault",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.Ominous: ominous,
            BlockStateKeys.VaultState: vault_state,
        },
    )


def VerdantFroglight(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for VerdantFroglight"""
    return MinecraftBlockDescriptor(
        "minecraft:verdant_froglight",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def Vine(
    vine_direction_bits: Optional[VineDirectionBits] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Vine"""
    return MinecraftBlockDescriptor(
        "minecraft:vine",
        True,
        {BlockStateKeys.VineDirectionBits: vine_direction_bits},
    )


def WallBanner(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WallBanner"""
    return MinecraftBlockDescriptor(
        "minecraft:wall_banner",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def WallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def WarpedButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedButton"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def WarpedDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WarpedDoubleSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedDoubleSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_double_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WarpedFence() -> MinecraftBlockDescriptor:
    """Factory for WarpedFence"""
    return MinecraftBlockDescriptor("minecraft:warped_fence", True)


def WarpedFenceGate(
    in_wall_bit: Optional[InWallBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedFenceGate"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_fence_gate",
        True,
        {
            BlockStateKeys.InWallBit: in_wall_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
        },
    )


def WarpedFungus() -> MinecraftBlockDescriptor:
    """Factory for WarpedFungus"""
    return MinecraftBlockDescriptor("minecraft:warped_fungus", True)


def WarpedHangingSign(
    attached_bit: Optional[AttachedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
    ground_sign_direction: Optional[GroundSignDirection] = None,
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedHangingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_hanging_sign",
        True,
        {
            BlockStateKeys.AttachedBit: attached_bit,
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.GroundSignDirection: ground_sign_direction,
            BlockStateKeys.Hanging: hanging,
        },
    )


def WarpedHyphae(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for WarpedHyphae"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_hyphae", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def WarpedNylium() -> MinecraftBlockDescriptor:
    """Factory for WarpedNylium"""
    return MinecraftBlockDescriptor("minecraft:warped_nylium", True)


def WarpedPlanks() -> MinecraftBlockDescriptor:
    """Factory for WarpedPlanks"""
    return MinecraftBlockDescriptor("minecraft:warped_planks", True)


def WarpedPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def WarpedRoots() -> MinecraftBlockDescriptor:
    """Factory for WarpedRoots"""
    return MinecraftBlockDescriptor("minecraft:warped_roots", True)


def WarpedShelf(
    cardinal_direction: Optional[CardinalDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
    powered_shelf_type: Optional[int] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedShelf"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_shelf",
        True,
        {
            BlockStateKeys.MinecraftCardinalDirection: cardinal_direction,
            BlockStateKeys.PoweredBit: powered_bit,
            BlockStateKeys.PoweredShelfType: powered_shelf_type,
        },
    )


def WarpedSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WarpedStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def WarpedStandingSign(
    ground_sign_direction: Optional[GroundSignDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedStandingSign"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_standing_sign",
        True,
        {BlockStateKeys.GroundSignDirection: ground_sign_direction},
    )


def WarpedStem(pillar_axis: Optional[PillarAxis] = None) -> MinecraftBlockDescriptor:
    """Factory for WarpedStem"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_stem", True, {BlockStateKeys.PillarAxis: pillar_axis}
    )


def WarpedTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def WarpedWallSign(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WarpedWallSign"""
    return MinecraftBlockDescriptor(
        "minecraft:warped_wall_sign",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def WarpedWartBlock() -> MinecraftBlockDescriptor:
    """Factory for WarpedWartBlock"""
    return MinecraftBlockDescriptor("minecraft:warped_wart_block", True)


def Water(liquid_depth: Optional[LiquidDepth] = None) -> MinecraftBlockDescriptor:
    """Factory for Water"""
    return MinecraftBlockDescriptor(
        "minecraft:water", True, {BlockStateKeys.LiquidDepth: liquid_depth}
    )


def Waterlily() -> MinecraftBlockDescriptor:
    """Factory for Waterlily"""
    return MinecraftBlockDescriptor("minecraft:waterlily", True)


def WaxedChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_chiseled_copper", True)


def WaxedCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_copper", True)


def WaxedCopperBars() -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperBars"""
    return MinecraftBlockDescriptor("minecraft:waxed_copper_bars", True)


def WaxedCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def WaxedCopperChain(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_copper_chain",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def WaxedCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WaxedCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def WaxedCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:waxed_copper_grate", True)


def WaxedCopperLantern(hanging: Optional[Hanging] = None) -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_copper_lantern", True, {BlockStateKeys.Hanging: hanging}
    )


def WaxedCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def WaxedCutCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedCutCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_cut_copper", True)


def WaxedCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def WaxedDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedExposedChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_exposed_chiseled_copper", True)


def WaxedExposedCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_exposed_copper", True)


def WaxedExposedCopperBars() -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperBars"""
    return MinecraftBlockDescriptor("minecraft:waxed_exposed_copper_bars", True)


def WaxedExposedCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def WaxedExposedCopperChain(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_copper_chain",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def WaxedExposedCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WaxedExposedCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def WaxedExposedCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:waxed_exposed_copper_grate", True)


def WaxedExposedCopperLantern(
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_copper_lantern",
        True,
        {BlockStateKeys.Hanging: hanging},
    )


def WaxedExposedCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def WaxedExposedCutCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCutCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_exposed_cut_copper", True)


def WaxedExposedCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedExposedCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def WaxedExposedDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedExposedLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedExposedLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_exposed_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def WaxedLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def WaxedOxidizedChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_oxidized_chiseled_copper", True)


def WaxedOxidizedCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_oxidized_copper", True)


def WaxedOxidizedCopperBars() -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperBars"""
    return MinecraftBlockDescriptor("minecraft:waxed_oxidized_copper_bars", True)


def WaxedOxidizedCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def WaxedOxidizedCopperChain(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_copper_chain",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def WaxedOxidizedCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WaxedOxidizedCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def WaxedOxidizedCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:waxed_oxidized_copper_grate", True)


def WaxedOxidizedCopperLantern(
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_copper_lantern",
        True,
        {BlockStateKeys.Hanging: hanging},
    )


def WaxedOxidizedCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def WaxedOxidizedCutCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCutCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_oxidized_cut_copper", True)


def WaxedOxidizedCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedOxidizedCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def WaxedOxidizedDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedOxidizedLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedOxidizedLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_oxidized_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def WaxedWeatheredChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_weathered_chiseled_copper", True)


def WaxedWeatheredCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_weathered_copper", True)


def WaxedWeatheredCopperBars() -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperBars"""
    return MinecraftBlockDescriptor("minecraft:waxed_weathered_copper_bars", True)


def WaxedWeatheredCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def WaxedWeatheredCopperChain(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_copper_chain",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def WaxedWeatheredCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WaxedWeatheredCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def WaxedWeatheredCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:waxed_weathered_copper_grate", True)


def WaxedWeatheredCopperLantern(
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_copper_lantern",
        True,
        {BlockStateKeys.Hanging: hanging},
    )


def WaxedWeatheredCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def WaxedWeatheredCutCopper() -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCutCopper"""
    return MinecraftBlockDescriptor("minecraft:waxed_weathered_cut_copper", True)


def WaxedWeatheredCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedWeatheredCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def WaxedWeatheredDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WaxedWeatheredLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WaxedWeatheredLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:waxed_weathered_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def WeatheredChiseledCopper() -> MinecraftBlockDescriptor:
    """Factory for WeatheredChiseledCopper"""
    return MinecraftBlockDescriptor("minecraft:weathered_chiseled_copper", True)


def WeatheredCopper() -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopper"""
    return MinecraftBlockDescriptor("minecraft:weathered_copper", True)


def WeatheredCopperBars() -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperBars"""
    return MinecraftBlockDescriptor("minecraft:weathered_copper_bars", True)


def WeatheredCopperBulb(
    lit: Optional[Lit] = None, powered_bit: Optional[PoweredBit] = None
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperBulb"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_copper_bulb",
        True,
        {BlockStateKeys.Lit: lit, BlockStateKeys.PoweredBit: powered_bit},
    )


def WeatheredCopperChain(
    pillar_axis: Optional[PillarAxis] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperChain"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_copper_chain",
        True,
        {BlockStateKeys.PillarAxis: pillar_axis},
    )


def WeatheredCopperDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_copper_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WeatheredCopperGolemStatue(
    cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperGolemStatue"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_copper_golem_statue",
        True,
        {BlockStateKeys.MinecraftCardinalDirection: cardinal_direction},
    )


def WeatheredCopperGrate() -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperGrate"""
    return MinecraftBlockDescriptor("minecraft:weathered_copper_grate", True)


def WeatheredCopperLantern(
    hanging: Optional[Hanging] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperLantern"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_copper_lantern",
        True,
        {BlockStateKeys.Hanging: hanging},
    )


def WeatheredCopperTrapdoor(
    direction: Optional[Direction] = None,
    open_bit: Optional[OpenBit] = None,
    upside_down_bit: Optional[UpsideDownBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCopperTrapdoor"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_copper_trapdoor",
        True,
        {
            BlockStateKeys.Direction: direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpsideDownBit: upside_down_bit,
        },
    )


def WeatheredCutCopper() -> MinecraftBlockDescriptor:
    """Factory for WeatheredCutCopper"""
    return MinecraftBlockDescriptor("minecraft:weathered_cut_copper", True)


def WeatheredCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WeatheredCutCopperStairs(
    upside_down_bit: Optional[UpsideDownBit] = None,
    weirdo_direction: Optional[WeirdoDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredCutCopperStairs"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_cut_copper_stairs",
        True,
        {
            BlockStateKeys.UpsideDownBit: upside_down_bit,
            BlockStateKeys.WeirdoDirection: weirdo_direction,
        },
    )


def WeatheredDoubleCutCopperSlab(
    minecraft_vertical_half: Optional[VerticalHalf] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredDoubleCutCopperSlab"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_double_cut_copper_slab",
        True,
        {BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half},
    )


def WeatheredLightningRod(
    facing_direction: Optional[FacingDirection] = None,
    powered_bit: Optional[PoweredBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeatheredLightningRod"""
    return MinecraftBlockDescriptor(
        "minecraft:weathered_lightning_rod",
        True,
        {
            BlockStateKeys.FacingDirection: facing_direction,
            BlockStateKeys.PoweredBit: powered_bit,
        },
    )


def Web() -> MinecraftBlockDescriptor:
    """Factory for Web"""
    return MinecraftBlockDescriptor("minecraft:web", True)


def WeepingVines(
    weeping_vines_age: Optional[WeepingVinesAge] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WeepingVines"""
    return MinecraftBlockDescriptor(
        "minecraft:weeping_vines",
        True,
        {BlockStateKeys.WeepingVinesAge: weeping_vines_age},
    )


def WetSponge() -> MinecraftBlockDescriptor:
    """Factory for WetSponge"""
    return MinecraftBlockDescriptor("minecraft:wet_sponge", True)


def Wheat(growth: Optional[Growth] = None) -> MinecraftBlockDescriptor:
    """Factory for Wheat"""
    return MinecraftBlockDescriptor(
        "minecraft:wheat", True, {BlockStateKeys.Growth: growth}
    )


def WhiteCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for WhiteCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:white_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def WhiteCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for WhiteCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:white_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def WhiteCarpet() -> MinecraftBlockDescriptor:
    """Factory for WhiteCarpet"""
    return MinecraftBlockDescriptor("minecraft:white_carpet", True)


def WhiteConcrete() -> MinecraftBlockDescriptor:
    """Factory for WhiteConcrete"""
    return MinecraftBlockDescriptor("minecraft:white_concrete", True)


def WhiteConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for WhiteConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:white_concrete_powder", True)


def WhiteGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WhiteGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:white_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def WhiteShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for WhiteShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:white_shulker_box", True)


def WhiteStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for WhiteStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:white_stained_glass", True)


def WhiteStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for WhiteStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:white_stained_glass_pane", True)


def WhiteTerracotta() -> MinecraftBlockDescriptor:
    """Factory for WhiteTerracotta"""
    return MinecraftBlockDescriptor("minecraft:white_terracotta", True)


def WhiteTulip() -> MinecraftBlockDescriptor:
    """Factory for WhiteTulip"""
    return MinecraftBlockDescriptor("minecraft:white_tulip", True)


def WhiteWool() -> MinecraftBlockDescriptor:
    """Factory for WhiteWool"""
    return MinecraftBlockDescriptor("minecraft:white_wool", True)


def Wildflowers(
    growth: Optional[Growth] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for Wildflowers"""
    return MinecraftBlockDescriptor(
        "minecraft:wildflowers",
        True,
        {
            BlockStateKeys.Growth: growth,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
        },
    )


def WitherRose() -> MinecraftBlockDescriptor:
    """Factory for WitherRose"""
    return MinecraftBlockDescriptor("minecraft:wither_rose", True)


def WitherSkeletonSkull(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WitherSkeletonSkull"""
    return MinecraftBlockDescriptor(
        "minecraft:wither_skeleton_skull",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def WoodenButton(
    button_pressed_bit: Optional[ButtonPressedBit] = None,
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WoodenButton"""
    return MinecraftBlockDescriptor(
        "minecraft:wooden_button",
        True,
        {
            BlockStateKeys.ButtonPressedBit: button_pressed_bit,
            BlockStateKeys.FacingDirection: facing_direction,
        },
    )


def WoodenDoor(
    door_hinge_bit: Optional[DoorHingeBit] = None,
    minecraft_cardinal_direction: Optional[CardinalDirection] = None,
    open_bit: Optional[OpenBit] = None,
    upper_block_bit: Optional[UpperBlockBit] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WoodenDoor"""
    return MinecraftBlockDescriptor(
        "minecraft:wooden_door",
        True,
        {
            BlockStateKeys.DoorHingeBit: door_hinge_bit,
            BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            BlockStateKeys.OpenBit: open_bit,
            BlockStateKeys.UpperBlockBit: upper_block_bit,
        },
    )


def WoodenPressurePlate(
    redstone_signal: Optional[RedstoneSignal] = None,
) -> MinecraftBlockDescriptor:
    """Factory for WoodenPressurePlate"""
    return MinecraftBlockDescriptor(
        "minecraft:wooden_pressure_plate",
        True,
        {BlockStateKeys.RedstoneSignal: redstone_signal},
    )


def YellowCandle(
    candles: Optional[Candles] = None, lit: Optional[Lit] = None
) -> MinecraftBlockDescriptor:
    """Factory for YellowCandle"""
    return MinecraftBlockDescriptor(
        "minecraft:yellow_candle",
        True,
        {BlockStateKeys.Candles: candles, BlockStateKeys.Lit: lit},
    )


def YellowCandleCake(lit: Optional[Lit] = None) -> MinecraftBlockDescriptor:
    """Factory for YellowCandleCake"""
    return MinecraftBlockDescriptor(
        "minecraft:yellow_candle_cake", True, {BlockStateKeys.Lit: lit}
    )


def YellowCarpet() -> MinecraftBlockDescriptor:
    """Factory for YellowCarpet"""
    return MinecraftBlockDescriptor("minecraft:yellow_carpet", True)


def YellowConcrete() -> MinecraftBlockDescriptor:
    """Factory for YellowConcrete"""
    return MinecraftBlockDescriptor("minecraft:yellow_concrete", True)


def YellowConcretePowder() -> MinecraftBlockDescriptor:
    """Factory for YellowConcretePowder"""
    return MinecraftBlockDescriptor("minecraft:yellow_concrete_powder", True)


def YellowGlazedTerracotta(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for YellowGlazedTerracotta"""
    return MinecraftBlockDescriptor(
        "minecraft:yellow_glazed_terracotta",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )


def YellowShulkerBox() -> MinecraftBlockDescriptor:
    """Factory for YellowShulkerBox"""
    return MinecraftBlockDescriptor("minecraft:yellow_shulker_box", True)


def YellowStainedGlass() -> MinecraftBlockDescriptor:
    """Factory for YellowStainedGlass"""
    return MinecraftBlockDescriptor("minecraft:yellow_stained_glass", True)


def YellowStainedGlassPane() -> MinecraftBlockDescriptor:
    """Factory for YellowStainedGlassPane"""
    return MinecraftBlockDescriptor("minecraft:yellow_stained_glass_pane", True)


def YellowTerracotta() -> MinecraftBlockDescriptor:
    """Factory for YellowTerracotta"""
    return MinecraftBlockDescriptor("minecraft:yellow_terracotta", True)


def YellowWool() -> MinecraftBlockDescriptor:
    """Factory for YellowWool"""
    return MinecraftBlockDescriptor("minecraft:yellow_wool", True)


def ZombieHead(
    facing_direction: Optional[FacingDirection] = None,
) -> MinecraftBlockDescriptor:
    """Factory for ZombieHead"""
    return MinecraftBlockDescriptor(
        "minecraft:zombie_head",
        True,
        {BlockStateKeys.FacingDirection: facing_direction},
    )
