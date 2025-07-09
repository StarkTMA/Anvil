from enum import StrEnum
from typing import Literal, TypeAlias

from anvil.lib.schemas import MinecraftBlockDescriptor

Active: TypeAlias = Literal["0b", "1b"]
Age: TypeAlias = Literal["12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"]
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
GroundSignDirection: TypeAlias = Literal["12", "10", "5", "7", "13", "9", "4", "11", "0", "6", "14", "1", "2", "3", "8", "15"]
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
HugeMushroomBits: TypeAlias = Literal["12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"]
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
    "down_east_west", "east", "west", "south", "north", "up_north_south", "up_east_west", "down_north_south"
]
LiquidDepth: TypeAlias = Literal["12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"]
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
RedstoneSignal: TypeAlias = Literal["12", "10", "5", "13", "9", "4", "0", "6", "14", "1", "15", "8", "2", "3", "7", "11"]
RepeaterDelay: TypeAlias = Literal["0", "2", "1", "3"]
RespawnAnchorCharge: TypeAlias = Literal["0", "1", "2", "3", "4"]
Rotation: TypeAlias = Literal["0", "1", "2", "3"]
SandStoneType: TypeAlias = Literal["heiroglyphs", "default", "cut", "smooth"]
SandType: TypeAlias = Literal["normal", "red"]
SaplingType: TypeAlias = Literal["dark_oak", "acacia", "spruce", "birch", "jungle", "oak"]
SculkSensorPhase: TypeAlias = Literal["0", "2", "1"]
SeaGrassType: TypeAlias = Literal["default", "double_top", "double_bot"]
SpongeType: TypeAlias = Literal["dry", "wet"]
Stability: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7"]
StabilityCheck: TypeAlias = Literal["0b", "1b"]
StoneBrickType: TypeAlias = Literal["default", "mossy", "cracked", "chiseled", "smooth"]
StoneType: TypeAlias = Literal["stone", "granite", "granite_smooth", "diorite", "diorite_smooth", "andesite", "andesite_smooth"]
StrippedBit: TypeAlias = Literal["0b", "1b"]
StructureBlockType: TypeAlias = Literal["data", "save", "load", "corner", "invalid", "export"]
StructureVoidType: TypeAlias = Literal["void", "air"]
SuspendedBit: TypeAlias = Literal["0b", "1b"]
ToggleBit: TypeAlias = Literal["0b", "1b"]
TopSlotBit: TypeAlias = Literal["0b", "1b"]
TorchFacingDirection: TypeAlias = Literal["unknown", "west", "south", "north", "east", "top"]
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
VineDirectionBits: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]
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
Orientation: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
CreakingHeartState: TypeAlias = Literal["0b", "1b"]
Natural: TypeAlias = Literal["0b", "1b"]
RehydrationLevel: TypeAlias = Literal["0", "1", "2", "3", "4", "5", "6", "7"]
Tip: TypeAlias = Literal["0b", "1b"]
PaleMossCarpetSideEast: TypeAlias = Literal["none", "short", "tall"]
PaleMossCarpetSideNorth: TypeAlias = Literal["none", "short", "tall"]
PaleMossCarpetSideSouth: TypeAlias = Literal["none", "short", "tall"]
PaleMossCarpetSideWest: TypeAlias = Literal["none", "short", "tall"]
Ominous: TypeAlias = Literal["0b", "1b"]


class _BlockStateKeys(StrEnum):
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


class MinecraftBlockTypes:
    @staticmethod
    def AcaciaButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for AcaciaButton"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def AcaciaDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for AcaciaDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def AcaciaDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for AcaciaDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:acacia_double_slab", True,{_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AcaciaFence() -> MinecraftBlockDescriptor:
        """Factory for AcaciaFence"""
        return MinecraftBlockDescriptor("minecraft:acacia_fence", True)

    @staticmethod
    def AcaciaFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for AcaciaFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def AcaciaHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for AcaciaHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def AcaciaLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for AcaciaLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_leaves", True,{_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def AcaciaLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for AcaciaLog"""
        return MinecraftBlockDescriptor("minecraft:acacia_log", True,{_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def AcaciaPlanks() -> MinecraftBlockDescriptor:
        """Factory for AcaciaPlanks"""
        return MinecraftBlockDescriptor("minecraft:acacia_planks", True)

    @staticmethod
    def AcaciaPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for AcaciaPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:acacia_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def AcaciaSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for AcaciaSapling"""
        return MinecraftBlockDescriptor("minecraft:acacia_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def AcaciaSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for AcaciaSlab"""
        return MinecraftBlockDescriptor("minecraft:acacia_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AcaciaStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for AcaciaStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def AcaciaStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for AcaciaStandingSign"""
        return MinecraftBlockDescriptor("minecraft:acacia_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def AcaciaTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for AcaciaTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:acacia_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def AcaciaWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for AcaciaWallSign"""
        return MinecraftBlockDescriptor("minecraft:acacia_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def AcaciaWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for AcaciaWood"""
        return MinecraftBlockDescriptor("minecraft:acacia_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def ActivatorRail(rail_data_bit: RailDataBit, rail_direction: RailDirection) -> MinecraftBlockDescriptor:
        """Factory for ActivatorRail"""
        return MinecraftBlockDescriptor(
            "minecraft:activator_rail", True,
            {_BlockStateKeys.RailDataBit: rail_data_bit, _BlockStateKeys.RailDirection: rail_direction},
        )

    @staticmethod
    def Air() -> MinecraftBlockDescriptor:
        """Factory for Air"""
        return MinecraftBlockDescriptor("minecraft:air", True)

    @staticmethod
    def Allium() -> MinecraftBlockDescriptor:
        """Factory for Allium"""
        return MinecraftBlockDescriptor("minecraft:allium", True)

    @staticmethod
    def Allow() -> MinecraftBlockDescriptor:
        """Factory for Allow"""
        return MinecraftBlockDescriptor("minecraft:allow", True)

    @staticmethod
    def AmethystBlock() -> MinecraftBlockDescriptor:
        """Factory for AmethystBlock"""
        return MinecraftBlockDescriptor("minecraft:amethyst_block", True)

    @staticmethod
    def AmethystCluster(minecraft_block_face: BlockFace) -> MinecraftBlockDescriptor:
        """Factory for AmethystCluster"""
        return MinecraftBlockDescriptor("minecraft:amethyst_cluster", True, {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def AncientDebris() -> MinecraftBlockDescriptor:
        """Factory for AncientDebris"""
        return MinecraftBlockDescriptor("minecraft:ancient_debris", True)

    @staticmethod
    def Andesite() -> MinecraftBlockDescriptor:
        """Factory for Andesite"""
        return MinecraftBlockDescriptor("minecraft:andesite", True)

    @staticmethod
    def AndesiteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for AndesiteDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:andesite_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AndesiteSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for AndesiteSlab"""
        return MinecraftBlockDescriptor("minecraft:andesite_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AndesiteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for AndesiteStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:andesite_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def AndesiteWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for AndesiteWall"""
        return MinecraftBlockDescriptor(
            "minecraft:andesite_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Anvil(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Anvil"""
        return MinecraftBlockDescriptor("minecraft:anvil", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def Azalea() -> MinecraftBlockDescriptor:
        """Factory for Azalea"""
        return MinecraftBlockDescriptor("minecraft:azalea", True)

    @staticmethod
    def AzaleaLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for AzaleaLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:azalea_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def AzaleaLeavesFlowered(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for AzaleaLeavesFlowered"""
        return MinecraftBlockDescriptor(
            "minecraft:azalea_leaves_flowered", True,
            {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit},
        )

    @staticmethod
    def AzureBluet() -> MinecraftBlockDescriptor:
        """Factory for AzureBluet"""
        return MinecraftBlockDescriptor("minecraft:azure_bluet", True)

    @staticmethod
    def Bamboo(
        age_bit: AgeBit, bamboo_leaf_size: BambooLeafSize, bamboo_stalk_thickness: BambooStalkThickness
    ) -> MinecraftBlockDescriptor:
        """Factory for Bamboo"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo", True,
            {
                _BlockStateKeys.AgeBit: age_bit,
                _BlockStateKeys.BambooLeafSize: bamboo_leaf_size,
                _BlockStateKeys.BambooStalkThickness: bamboo_stalk_thickness,
            },
        )

    @staticmethod
    def BambooBlock(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for BambooBlock"""
        return MinecraftBlockDescriptor("minecraft:bamboo_block", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def BambooButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BambooButton"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def BambooDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for BambooDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def BambooDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BambooDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:bamboo_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BambooFence() -> MinecraftBlockDescriptor:
        """Factory for BambooFence"""
        return MinecraftBlockDescriptor("minecraft:bamboo_fence", True)

    @staticmethod
    def BambooFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for BambooFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def BambooHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for BambooHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def BambooMosaic() -> MinecraftBlockDescriptor:
        """Factory for BambooMosaic"""
        return MinecraftBlockDescriptor("minecraft:bamboo_mosaic", True)

    @staticmethod
    def BambooMosaicDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BambooMosaicDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_mosaic_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def BambooMosaicSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BambooMosaicSlab"""
        return MinecraftBlockDescriptor("minecraft:bamboo_mosaic_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BambooMosaicStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for BambooMosaicStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_mosaic_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BambooPlanks() -> MinecraftBlockDescriptor:
        """Factory for BambooPlanks"""
        return MinecraftBlockDescriptor("minecraft:bamboo_planks", True)

    @staticmethod
    def BambooPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for BambooPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:bamboo_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def BambooSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for BambooSapling"""
        return MinecraftBlockDescriptor("minecraft:bamboo_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def BambooSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BambooSlab"""
        return MinecraftBlockDescriptor("minecraft:bamboo_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BambooStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for BambooStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BambooStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for BambooStandingSign"""
        return MinecraftBlockDescriptor("minecraft:bamboo_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def BambooTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for BambooTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:bamboo_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def BambooWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BambooWallSign"""
        return MinecraftBlockDescriptor("minecraft:bamboo_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Barrel(facing_direction: FacingDirection, open_bit: OpenBit) -> MinecraftBlockDescriptor:
        """Factory for Barrel"""
        return MinecraftBlockDescriptor(
            "minecraft:barrel", True, {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.OpenBit: open_bit}
        )

    @staticmethod
    def Barrier() -> MinecraftBlockDescriptor:
        """Factory for Barrier"""
        return MinecraftBlockDescriptor("minecraft:barrier", True)

    @staticmethod
    def Basalt(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for Basalt"""
        return MinecraftBlockDescriptor("minecraft:basalt", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Beacon() -> MinecraftBlockDescriptor:
        """Factory for Beacon"""
        return MinecraftBlockDescriptor("minecraft:beacon", True)

    @staticmethod
    def Bed(direction: Direction, head_piece_bit: HeadPieceBit, occupied_bit: OccupiedBit) -> MinecraftBlockDescriptor:
        """Factory for Bed"""
        return MinecraftBlockDescriptor(
            "minecraft:bed", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.HeadPieceBit: head_piece_bit,
                _BlockStateKeys.OccupiedBit: occupied_bit,
            },
        )

    @staticmethod
    def Bedrock(infiniburn_bit: InfiniburnBit) -> MinecraftBlockDescriptor:
        """Factory for Bedrock"""
        return MinecraftBlockDescriptor("minecraft:bedrock", True, {_BlockStateKeys.InfiniburnBit: infiniburn_bit})

    @staticmethod
    def BeeNest(direction: Direction, honey_level: HoneyLevel) -> MinecraftBlockDescriptor:
        """Factory for BeeNest"""
        return MinecraftBlockDescriptor(
            "minecraft:bee_nest", True, {_BlockStateKeys.Direction: direction, _BlockStateKeys.HoneyLevel: honey_level}
        )

    @staticmethod
    def Beehive(direction: Direction, honey_level: HoneyLevel) -> MinecraftBlockDescriptor:
        """Factory for Beehive"""
        return MinecraftBlockDescriptor(
            "minecraft:beehive", True, {_BlockStateKeys.Direction: direction, _BlockStateKeys.HoneyLevel: honey_level}
        )

    @staticmethod
    def Beetroot(growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for Beetroot"""
        return MinecraftBlockDescriptor("minecraft:beetroot", True, {_BlockStateKeys.Growth: growth})

    @staticmethod
    def Bell(attachment: Attachment, direction: Direction, toggle_bit: ToggleBit) -> MinecraftBlockDescriptor:
        """Factory for Bell"""
        return MinecraftBlockDescriptor(
            "minecraft:bell", True,
            {_BlockStateKeys.Attachment: attachment, _BlockStateKeys.Direction: direction, _BlockStateKeys.ToggleBit: toggle_bit},
        )

    @staticmethod
    def BigDripleaf(
        big_dripleaf_head: BigDripleafHead, big_dripleaf_tilt: BigDripleafTilt, minecraft_cardinal_direction: CardinalDirection
    ) -> MinecraftBlockDescriptor:
        """Factory for BigDripleaf"""
        return MinecraftBlockDescriptor(
            "minecraft:big_dripleaf", True,
            {
                _BlockStateKeys.BigDripleafHead: big_dripleaf_head,
                _BlockStateKeys.BigDripleafTilt: big_dripleaf_tilt,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def BirchButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BirchButton"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def BirchDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for BirchDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def BirchDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BirchDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:birch_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BirchFence() -> MinecraftBlockDescriptor:
        """Factory for BirchFence"""
        return MinecraftBlockDescriptor("minecraft:birch_fence", True)

    @staticmethod
    def BirchFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for BirchFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def BirchHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for BirchHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def BirchLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for BirchLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def BirchLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for BirchLog"""
        return MinecraftBlockDescriptor("minecraft:birch_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def BirchPlanks() -> MinecraftBlockDescriptor:
        """Factory for BirchPlanks"""
        return MinecraftBlockDescriptor("minecraft:birch_planks", True)

    @staticmethod
    def BirchPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for BirchPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:birch_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def BirchSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for BirchSapling"""
        return MinecraftBlockDescriptor("minecraft:birch_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def BirchSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BirchSlab"""
        return MinecraftBlockDescriptor("minecraft:birch_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BirchStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for BirchStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BirchStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for BirchStandingSign"""
        return MinecraftBlockDescriptor("minecraft:birch_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def BirchTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for BirchTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:birch_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def BirchWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BirchWallSign"""
        return MinecraftBlockDescriptor("minecraft:birch_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BirchWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for BirchWood"""
        return MinecraftBlockDescriptor("minecraft:birch_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def BlackCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for BlackCandle"""
        return MinecraftBlockDescriptor("minecraft:black_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def BlackCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for BlackCandleCake"""
        return MinecraftBlockDescriptor("minecraft:black_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def BlackCarpet() -> MinecraftBlockDescriptor:
        """Factory for BlackCarpet"""
        return MinecraftBlockDescriptor("minecraft:black_carpet", True)

    @staticmethod
    def BlackConcrete() -> MinecraftBlockDescriptor:
        """Factory for BlackConcrete"""
        return MinecraftBlockDescriptor("minecraft:black_concrete", True)

    @staticmethod
    def BlackConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for BlackConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:black_concrete_powder", True)

    @staticmethod
    def BlackGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BlackGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:black_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BlackShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for BlackShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:black_shulker_box", True)

    @staticmethod
    def BlackStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for BlackStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:black_stained_glass", True)

    @staticmethod
    def BlackStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for BlackStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:black_stained_glass_pane", True)

    @staticmethod
    def BlackTerracotta() -> MinecraftBlockDescriptor:
        """Factory for BlackTerracotta"""
        return MinecraftBlockDescriptor("minecraft:black_terracotta", True)

    @staticmethod
    def BlackWool() -> MinecraftBlockDescriptor:
        """Factory for BlackWool"""
        return MinecraftBlockDescriptor("minecraft:black_wool", True)

    @staticmethod
    def Blackstone() -> MinecraftBlockDescriptor:
        """Factory for Blackstone"""
        return MinecraftBlockDescriptor("minecraft:blackstone", True)

    @staticmethod
    def BlackstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BlackstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:blackstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def BlackstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BlackstoneSlab"""
        return MinecraftBlockDescriptor("minecraft:blackstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BlackstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for BlackstoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:blackstone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BlackstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for BlackstoneWall"""
        return MinecraftBlockDescriptor(
            "minecraft:blackstone_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def BlastFurnace(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for BlastFurnace"""
        return MinecraftBlockDescriptor(
            "minecraft:blast_furnace", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def BlueCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for BlueCandle"""
        return MinecraftBlockDescriptor("minecraft:blue_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def BlueCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for BlueCandleCake"""
        return MinecraftBlockDescriptor("minecraft:blue_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def BlueCarpet() -> MinecraftBlockDescriptor:
        """Factory for BlueCarpet"""
        return MinecraftBlockDescriptor("minecraft:blue_carpet", True)

    @staticmethod
    def BlueConcrete() -> MinecraftBlockDescriptor:
        """Factory for BlueConcrete"""
        return MinecraftBlockDescriptor("minecraft:blue_concrete", True)

    @staticmethod
    def BlueConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for BlueConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:blue_concrete_powder", True)

    @staticmethod
    def BlueGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BlueGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:blue_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BlueIce() -> MinecraftBlockDescriptor:
        """Factory for BlueIce"""
        return MinecraftBlockDescriptor("minecraft:blue_ice", True)

    @staticmethod
    def BlueOrchid() -> MinecraftBlockDescriptor:
        """Factory for BlueOrchid"""
        return MinecraftBlockDescriptor("minecraft:blue_orchid", True)

    @staticmethod
    def BlueShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for BlueShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:blue_shulker_box", True)

    @staticmethod
    def BlueStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for BlueStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:blue_stained_glass", True)

    @staticmethod
    def BlueStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for BlueStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:blue_stained_glass_pane", True)

    @staticmethod
    def BlueTerracotta() -> MinecraftBlockDescriptor:
        """Factory for BlueTerracotta"""
        return MinecraftBlockDescriptor("minecraft:blue_terracotta", True)

    @staticmethod
    def BlueWool() -> MinecraftBlockDescriptor:
        """Factory for BlueWool"""
        return MinecraftBlockDescriptor("minecraft:blue_wool", True)

    @staticmethod
    def BoneBlock(deprecated: Deprecated, pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for BoneBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:bone_block", True, {_BlockStateKeys.Deprecated: deprecated, _BlockStateKeys.PillarAxis: pillar_axis}
        )

    @staticmethod
    def Bookshelf() -> MinecraftBlockDescriptor:
        """Factory for Bookshelf"""
        return MinecraftBlockDescriptor("minecraft:bookshelf", True)

    @staticmethod
    def BorderBlock(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for BorderBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:border_block", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def BrainCoral() -> MinecraftBlockDescriptor:
        """Factory for BrainCoral"""
        return MinecraftBlockDescriptor("minecraft:brain_coral", True)

    @staticmethod
    def BrainCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for BrainCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:brain_coral_block", True)

    @staticmethod
    def BrainCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for BrainCoralFan"""
        return MinecraftBlockDescriptor("minecraft:brain_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def BrainCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for BrainCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:brain_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def BrewingStand(
        brewing_stand_slot_a_bit: BrewingStandSlotABit,
        brewing_stand_slot_b_bit: BrewingStandSlotBBit,
        brewing_stand_slot_c_bit: BrewingStandSlotCBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for BrewingStand"""
        return MinecraftBlockDescriptor(
            "minecraft:brewing_stand", True,
            {
                _BlockStateKeys.BrewingStandSlotABit: brewing_stand_slot_a_bit,
                _BlockStateKeys.BrewingStandSlotBBit: brewing_stand_slot_b_bit,
                _BlockStateKeys.BrewingStandSlotCBit: brewing_stand_slot_c_bit,
            },
        )

    @staticmethod
    def BrickBlock() -> MinecraftBlockDescriptor:
        """Factory for BrickBlock"""
        return MinecraftBlockDescriptor("minecraft:brick_block", True)

    @staticmethod
    def BrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BrickDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for BrickSlab"""
        return MinecraftBlockDescriptor("minecraft:brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for BrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for BrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def BrownCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for BrownCandle"""
        return MinecraftBlockDescriptor("minecraft:brown_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def BrownCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for BrownCandleCake"""
        return MinecraftBlockDescriptor("minecraft:brown_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def BrownCarpet() -> MinecraftBlockDescriptor:
        """Factory for BrownCarpet"""
        return MinecraftBlockDescriptor("minecraft:brown_carpet", True)

    @staticmethod
    def BrownConcrete() -> MinecraftBlockDescriptor:
        """Factory for BrownConcrete"""
        return MinecraftBlockDescriptor("minecraft:brown_concrete", True)

    @staticmethod
    def BrownConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for BrownConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:brown_concrete_powder", True)

    @staticmethod
    def BrownGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for BrownGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:brown_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BrownMushroom() -> MinecraftBlockDescriptor:
        """Factory for BrownMushroom"""
        return MinecraftBlockDescriptor("minecraft:brown_mushroom", True)

    @staticmethod
    def BrownMushroomBlock(huge_mushroom_bits: HugeMushroomBits) -> MinecraftBlockDescriptor:
        """Factory for BrownMushroomBlock"""
        return MinecraftBlockDescriptor("minecraft:brown_mushroom_block", True, {_BlockStateKeys.HugeMushroomBits: huge_mushroom_bits})

    @staticmethod
    def BrownShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for BrownShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:brown_shulker_box", True)

    @staticmethod
    def BrownStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for BrownStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:brown_stained_glass", True)

    @staticmethod
    def BrownStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for BrownStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:brown_stained_glass_pane", True)

    @staticmethod
    def BrownTerracotta() -> MinecraftBlockDescriptor:
        """Factory for BrownTerracotta"""
        return MinecraftBlockDescriptor("minecraft:brown_terracotta", True)

    @staticmethod
    def BrownWool() -> MinecraftBlockDescriptor:
        """Factory for BrownWool"""
        return MinecraftBlockDescriptor("minecraft:brown_wool", True)

    @staticmethod
    def BubbleColumn(drag_down: DragDown) -> MinecraftBlockDescriptor:
        """Factory for BubbleColumn"""
        return MinecraftBlockDescriptor("minecraft:bubble_column", True, {_BlockStateKeys.DragDown: drag_down})

    @staticmethod
    def BubbleCoral() -> MinecraftBlockDescriptor:
        """Factory for BubbleCoral"""
        return MinecraftBlockDescriptor("minecraft:bubble_coral", True)

    @staticmethod
    def BubbleCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for BubbleCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:bubble_coral_block", True)

    @staticmethod
    def BubbleCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for BubbleCoralFan"""
        return MinecraftBlockDescriptor("minecraft:bubble_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def BubbleCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for BubbleCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:bubble_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def BuddingAmethyst() -> MinecraftBlockDescriptor:
        """Factory for BuddingAmethyst"""
        return MinecraftBlockDescriptor("minecraft:budding_amethyst", True)

    @staticmethod
    def Bush() -> MinecraftBlockDescriptor:
        """Factory for Bush"""
        return MinecraftBlockDescriptor("minecraft:bush", True)

    @staticmethod
    def Cactus(age: Age) -> MinecraftBlockDescriptor:
        """Factory for Cactus"""
        return MinecraftBlockDescriptor("minecraft:cactus", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def CactusFlower() -> MinecraftBlockDescriptor:
        """Factory for CactusFlower"""
        return MinecraftBlockDescriptor("minecraft:cactus_flower", True)

    @staticmethod
    def Cake(bite_counter: BiteCounter) -> MinecraftBlockDescriptor:
        """Factory for Cake"""
        return MinecraftBlockDescriptor("minecraft:cake", True, {_BlockStateKeys.BiteCounter: bite_counter})

    @staticmethod
    def Calcite() -> MinecraftBlockDescriptor:
        """Factory for Calcite"""
        return MinecraftBlockDescriptor("minecraft:calcite", True)

    @staticmethod
    def CalibratedSculkSensor(
        minecraft_cardinal_direction: CardinalDirection, sculk_sensor_phase: SculkSensorPhase
    ) -> MinecraftBlockDescriptor:
        """Factory for CalibratedSculkSensor"""
        return MinecraftBlockDescriptor(
            "minecraft:calibrated_sculk_sensor", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.SculkSensorPhase: sculk_sensor_phase,
            },
        )

    @staticmethod
    def Camera() -> MinecraftBlockDescriptor:
        """Factory for Camera"""
        return MinecraftBlockDescriptor("minecraft:camera", True)

    @staticmethod
    def Campfire(extinguished: Extinguished, minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Campfire"""
        return MinecraftBlockDescriptor(
            "minecraft:campfire", True,
            {
                _BlockStateKeys.Extinguished: extinguished,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def Candle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for Candle"""
        return MinecraftBlockDescriptor("minecraft:candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def CandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for CandleCake"""
        return MinecraftBlockDescriptor("minecraft:candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def Carrots(growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for Carrots"""
        return MinecraftBlockDescriptor("minecraft:carrots", True, {_BlockStateKeys.Growth: growth})

    @staticmethod
    def CartographyTable() -> MinecraftBlockDescriptor:
        """Factory for CartographyTable"""
        return MinecraftBlockDescriptor("minecraft:cartography_table", True)

    @staticmethod
    def CarvedPumpkin(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for CarvedPumpkin"""
        return MinecraftBlockDescriptor(
            "minecraft:carved_pumpkin", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def Cauldron(cauldron_liquid: CauldronLiquid, fill_level: FillLevel) -> MinecraftBlockDescriptor:
        """Factory for Cauldron"""
        return MinecraftBlockDescriptor(
            "minecraft:cauldron", True, {_BlockStateKeys.CauldronLiquid: cauldron_liquid, _BlockStateKeys.FillLevel: fill_level}
        )

    @staticmethod
    def CaveVines(growing_plant_age: GrowingPlantAge) -> MinecraftBlockDescriptor:
        """Factory for CaveVines"""
        return MinecraftBlockDescriptor("minecraft:cave_vines", True, {_BlockStateKeys.GrowingPlantAge: growing_plant_age})

    @staticmethod
    def CaveVinesBodyWithBerries(growing_plant_age: GrowingPlantAge) -> MinecraftBlockDescriptor:
        """Factory for CaveVinesBodyWithBerries"""
        return MinecraftBlockDescriptor("minecraft:cave_vines_body_with_berries", True, {_BlockStateKeys.GrowingPlantAge: growing_plant_age})

    @staticmethod
    def CaveVinesHeadWithBerries(growing_plant_age: GrowingPlantAge) -> MinecraftBlockDescriptor:
        """Factory for CaveVinesHeadWithBerries"""
        return MinecraftBlockDescriptor("minecraft:cave_vines_head_with_berries", True, {_BlockStateKeys.GrowingPlantAge: growing_plant_age})

    @staticmethod
    def Chain(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for Chain"""
        return MinecraftBlockDescriptor("minecraft:chain", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def ChainCommandBlock(conditional_bit: ConditionalBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for ChainCommandBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:chain_command_block", True,
            {_BlockStateKeys.ConditionalBit: conditional_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def ChemicalHeat() -> MinecraftBlockDescriptor:
        """Factory for ChemicalHeat"""
        return MinecraftBlockDescriptor("minecraft:chemical_heat", True)

    @staticmethod
    def CherryButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CherryButton"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def CherryDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for CherryDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def CherryDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CherryDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:cherry_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CherryFence() -> MinecraftBlockDescriptor:
        """Factory for CherryFence"""
        return MinecraftBlockDescriptor("minecraft:cherry_fence", True)

    @staticmethod
    def CherryFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for CherryFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def CherryHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for CherryHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def CherryLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for CherryLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def CherryLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for CherryLog"""
        return MinecraftBlockDescriptor("minecraft:cherry_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def CherryPlanks() -> MinecraftBlockDescriptor:
        """Factory for CherryPlanks"""
        return MinecraftBlockDescriptor("minecraft:cherry_planks", True)

    @staticmethod
    def CherryPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for CherryPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:cherry_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def CherrySapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for CherrySapling"""
        return MinecraftBlockDescriptor("minecraft:cherry_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def CherrySlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CherrySlab"""
        return MinecraftBlockDescriptor("minecraft:cherry_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CherryStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for CherryStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CherryStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for CherryStandingSign"""
        return MinecraftBlockDescriptor("minecraft:cherry_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def CherryTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for CherryTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:cherry_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def CherryWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CherryWallSign"""
        return MinecraftBlockDescriptor("minecraft:cherry_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CherryWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for CherryWood"""
        return MinecraftBlockDescriptor("minecraft:cherry_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Chest(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Chest"""
        return MinecraftBlockDescriptor("minecraft:chest", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def ChippedAnvil(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for ChippedAnvil"""
        return MinecraftBlockDescriptor(
            "minecraft:chipped_anvil", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def ChiseledBookshelf(books_stored: BooksStored, direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for ChiseledBookshelf"""
        return MinecraftBlockDescriptor(
            "minecraft:chiseled_bookshelf", True, {_BlockStateKeys.BooksStored: books_stored, _BlockStateKeys.Direction: direction}
        )

    @staticmethod
    def ChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for ChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:chiseled_copper", True)

    @staticmethod
    def ChiseledDeepslate() -> MinecraftBlockDescriptor:
        """Factory for ChiseledDeepslate"""
        return MinecraftBlockDescriptor("minecraft:chiseled_deepslate", True)

    @staticmethod
    def ChiseledNetherBricks() -> MinecraftBlockDescriptor:
        """Factory for ChiseledNetherBricks"""
        return MinecraftBlockDescriptor("minecraft:chiseled_nether_bricks", True)

    @staticmethod
    def ChiseledPolishedBlackstone() -> MinecraftBlockDescriptor:
        """Factory for ChiseledPolishedBlackstone"""
        return MinecraftBlockDescriptor("minecraft:chiseled_polished_blackstone", True)

    @staticmethod
    def ChiseledQuartzBlock(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for ChiseledQuartzBlock"""
        return MinecraftBlockDescriptor("minecraft:chiseled_quartz_block", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def ChiseledRedSandstone() -> MinecraftBlockDescriptor:
        """Factory for ChiseledRedSandstone"""
        return MinecraftBlockDescriptor("minecraft:chiseled_red_sandstone", True)

    @staticmethod
    def ChiseledResinBricks() -> MinecraftBlockDescriptor:
        """Factory for ChiseledResinBricks"""
        return MinecraftBlockDescriptor("minecraft:chiseled_resin_bricks", True)

    @staticmethod
    def ChiseledSandstone() -> MinecraftBlockDescriptor:
        """Factory for ChiseledSandstone"""
        return MinecraftBlockDescriptor("minecraft:chiseled_sandstone", True)

    @staticmethod
    def ChiseledStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for ChiseledStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:chiseled_stone_bricks", True)

    @staticmethod
    def ChiseledTuff() -> MinecraftBlockDescriptor:
        """Factory for ChiseledTuff"""
        return MinecraftBlockDescriptor("minecraft:chiseled_tuff", True)

    @staticmethod
    def ChiseledTuffBricks() -> MinecraftBlockDescriptor:
        """Factory for ChiseledTuffBricks"""
        return MinecraftBlockDescriptor("minecraft:chiseled_tuff_bricks", True)

    @staticmethod
    def ChorusFlower(age: Age) -> MinecraftBlockDescriptor:
        """Factory for ChorusFlower"""
        return MinecraftBlockDescriptor("minecraft:chorus_flower", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def ChorusPlant() -> MinecraftBlockDescriptor:
        """Factory for ChorusPlant"""
        return MinecraftBlockDescriptor("minecraft:chorus_plant", True)

    @staticmethod
    def Clay() -> MinecraftBlockDescriptor:
        """Factory for Clay"""
        return MinecraftBlockDescriptor("minecraft:clay", True)

    @staticmethod
    def ClosedEyeblossom() -> MinecraftBlockDescriptor:
        """Factory for ClosedEyeblossom"""
        return MinecraftBlockDescriptor("minecraft:closed_eyeblossom", True)

    @staticmethod
    def CoalBlock() -> MinecraftBlockDescriptor:
        """Factory for CoalBlock"""
        return MinecraftBlockDescriptor("minecraft:coal_block", True)

    @staticmethod
    def CoalOre() -> MinecraftBlockDescriptor:
        """Factory for CoalOre"""
        return MinecraftBlockDescriptor("minecraft:coal_ore", True)

    @staticmethod
    def CoarseDirt() -> MinecraftBlockDescriptor:
        """Factory for CoarseDirt"""
        return MinecraftBlockDescriptor("minecraft:coarse_dirt", True)

    @staticmethod
    def CobbledDeepslate() -> MinecraftBlockDescriptor:
        """Factory for CobbledDeepslate"""
        return MinecraftBlockDescriptor("minecraft:cobbled_deepslate", True)

    @staticmethod
    def CobbledDeepslateDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CobbledDeepslateDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:cobbled_deepslate_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CobbledDeepslateSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CobbledDeepslateSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:cobbled_deepslate_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CobbledDeepslateStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for CobbledDeepslateStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:cobbled_deepslate_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CobbledDeepslateWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for CobbledDeepslateWall"""
        return MinecraftBlockDescriptor(
            "minecraft:cobbled_deepslate_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Cobblestone() -> MinecraftBlockDescriptor:
        """Factory for Cobblestone"""
        return MinecraftBlockDescriptor("minecraft:cobblestone", True)

    @staticmethod
    def CobblestoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CobblestoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:cobblestone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CobblestoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CobblestoneSlab"""
        return MinecraftBlockDescriptor("minecraft:cobblestone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CobblestoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for CobblestoneWall"""
        return MinecraftBlockDescriptor(
            "minecraft:cobblestone_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Cocoa(age: Age, direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for Cocoa"""
        return MinecraftBlockDescriptor("minecraft:cocoa", True, {_BlockStateKeys.Age: age, _BlockStateKeys.Direction: direction})

    @staticmethod
    def ColoredTorchBlue(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for ColoredTorchBlue"""
        return MinecraftBlockDescriptor("minecraft:colored_torch_blue", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def ColoredTorchGreen(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for ColoredTorchGreen"""
        return MinecraftBlockDescriptor("minecraft:colored_torch_green", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def ColoredTorchPurple(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for ColoredTorchPurple"""
        return MinecraftBlockDescriptor("minecraft:colored_torch_purple", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def ColoredTorchRed(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for ColoredTorchRed"""
        return MinecraftBlockDescriptor("minecraft:colored_torch_red", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def CommandBlock(conditional_bit: ConditionalBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CommandBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:command_block", True,
            {_BlockStateKeys.ConditionalBit: conditional_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def Composter(composter_fill_level: ComposterFillLevel) -> MinecraftBlockDescriptor:
        """Factory for Composter"""
        return MinecraftBlockDescriptor("minecraft:composter", True, {_BlockStateKeys.ComposterFillLevel: composter_fill_level})

    @staticmethod
    def CompoundCreator(direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for CompoundCreator"""
        return MinecraftBlockDescriptor("minecraft:compound_creator", True, {_BlockStateKeys.Direction: direction})

    @staticmethod
    def Conduit() -> MinecraftBlockDescriptor:
        """Factory for Conduit"""
        return MinecraftBlockDescriptor("minecraft:conduit", True)

    @staticmethod
    def CopperBlock() -> MinecraftBlockDescriptor:
        """Factory for CopperBlock"""
        return MinecraftBlockDescriptor("minecraft:copper_block", True)

    @staticmethod
    def CopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for CopperBulb"""
        return MinecraftBlockDescriptor("minecraft:copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit})

    @staticmethod
    def CopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for CopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def CopperGrate() -> MinecraftBlockDescriptor:
        """Factory for CopperGrate"""
        return MinecraftBlockDescriptor("minecraft:copper_grate", True)

    @staticmethod
    def CopperOre() -> MinecraftBlockDescriptor:
        """Factory for CopperOre"""
        return MinecraftBlockDescriptor("minecraft:copper_ore", True)

    @staticmethod
    def CopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for CopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def Cornflower() -> MinecraftBlockDescriptor:
        """Factory for Cornflower"""
        return MinecraftBlockDescriptor("minecraft:cornflower", True)

    @staticmethod
    def CrackedDeepslateBricks() -> MinecraftBlockDescriptor:
        """Factory for CrackedDeepslateBricks"""
        return MinecraftBlockDescriptor("minecraft:cracked_deepslate_bricks", True)

    @staticmethod
    def CrackedDeepslateTiles() -> MinecraftBlockDescriptor:
        """Factory for CrackedDeepslateTiles"""
        return MinecraftBlockDescriptor("minecraft:cracked_deepslate_tiles", True)

    @staticmethod
    def CrackedNetherBricks() -> MinecraftBlockDescriptor:
        """Factory for CrackedNetherBricks"""
        return MinecraftBlockDescriptor("minecraft:cracked_nether_bricks", True)

    @staticmethod
    def CrackedPolishedBlackstoneBricks() -> MinecraftBlockDescriptor:
        """Factory for CrackedPolishedBlackstoneBricks"""
        return MinecraftBlockDescriptor("minecraft:cracked_polished_blackstone_bricks", True)

    @staticmethod
    def CrackedStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for CrackedStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:cracked_stone_bricks", True)

    @staticmethod
    def Crafter(crafting: Crafting, orientation: Orientation, triggered_bit: TriggeredBit) -> MinecraftBlockDescriptor:
        """Factory for Crafter"""
        return MinecraftBlockDescriptor(
            "minecraft:crafter", True,
            {
                _BlockStateKeys.Crafting: crafting,
                _BlockStateKeys.Orientation: orientation,
                _BlockStateKeys.TriggeredBit: triggered_bit,
            },
        )

    @staticmethod
    def CraftingTable() -> MinecraftBlockDescriptor:
        """Factory for CraftingTable"""
        return MinecraftBlockDescriptor("minecraft:crafting_table", True)

    @staticmethod
    def CreakingHeart(creaking_heart_state: CreakingHeartState, natural: Natural, pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for CreakingHeart"""
        return MinecraftBlockDescriptor(
            "minecraft:creaking_heart", True,
            {
                _BlockStateKeys.CreakingHeartState: creaking_heart_state,
                _BlockStateKeys.Natural: natural,
                _BlockStateKeys.PillarAxis: pillar_axis,
            },
        )

    @staticmethod
    def CreeperHead(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CreeperHead"""
        return MinecraftBlockDescriptor("minecraft:creeper_head", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CrimsonButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CrimsonButton"""
        return MinecraftBlockDescriptor(
            "minecraft:crimson_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def CrimsonDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for CrimsonDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:crimson_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def CrimsonDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CrimsonDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:crimson_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CrimsonFence() -> MinecraftBlockDescriptor:
        """Factory for CrimsonFence"""
        return MinecraftBlockDescriptor("minecraft:crimson_fence", True)

    @staticmethod
    def CrimsonFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for CrimsonFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:crimson_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def CrimsonFungus() -> MinecraftBlockDescriptor:
        """Factory for CrimsonFungus"""
        return MinecraftBlockDescriptor("minecraft:crimson_fungus", True)

    @staticmethod
    def CrimsonHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for CrimsonHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:crimson_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def CrimsonHyphae(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for CrimsonHyphae"""
        return MinecraftBlockDescriptor("minecraft:crimson_hyphae", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def CrimsonNylium() -> MinecraftBlockDescriptor:
        """Factory for CrimsonNylium"""
        return MinecraftBlockDescriptor("minecraft:crimson_nylium", True)

    @staticmethod
    def CrimsonPlanks() -> MinecraftBlockDescriptor:
        """Factory for CrimsonPlanks"""
        return MinecraftBlockDescriptor("minecraft:crimson_planks", True)

    @staticmethod
    def CrimsonPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for CrimsonPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:crimson_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def CrimsonRoots() -> MinecraftBlockDescriptor:
        """Factory for CrimsonRoots"""
        return MinecraftBlockDescriptor("minecraft:crimson_roots", True)

    @staticmethod
    def CrimsonSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CrimsonSlab"""
        return MinecraftBlockDescriptor("minecraft:crimson_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CrimsonStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for CrimsonStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:crimson_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CrimsonStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for CrimsonStandingSign"""
        return MinecraftBlockDescriptor("minecraft:crimson_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def CrimsonStem(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for CrimsonStem"""
        return MinecraftBlockDescriptor("minecraft:crimson_stem", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def CrimsonTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for CrimsonTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:crimson_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def CrimsonWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CrimsonWallSign"""
        return MinecraftBlockDescriptor("minecraft:crimson_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CryingObsidian() -> MinecraftBlockDescriptor:
        """Factory for CryingObsidian"""
        return MinecraftBlockDescriptor("minecraft:crying_obsidian", True)

    @staticmethod
    def CutCopper() -> MinecraftBlockDescriptor:
        """Factory for CutCopper"""
        return MinecraftBlockDescriptor("minecraft:cut_copper", True)

    @staticmethod
    def CutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CutCopperSlab"""
        return MinecraftBlockDescriptor("minecraft:cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for CutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CutRedSandstone() -> MinecraftBlockDescriptor:
        """Factory for CutRedSandstone"""
        return MinecraftBlockDescriptor("minecraft:cut_red_sandstone", True)

    @staticmethod
    def CutRedSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CutRedSandstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:cut_red_sandstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CutRedSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CutRedSandstoneSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:cut_red_sandstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CutSandstone() -> MinecraftBlockDescriptor:
        """Factory for CutSandstone"""
        return MinecraftBlockDescriptor("minecraft:cut_sandstone", True)

    @staticmethod
    def CutSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CutSandstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:cut_sandstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CutSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for CutSandstoneSlab"""
        return MinecraftBlockDescriptor("minecraft:cut_sandstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CyanCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for CyanCandle"""
        return MinecraftBlockDescriptor("minecraft:cyan_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def CyanCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for CyanCandleCake"""
        return MinecraftBlockDescriptor("minecraft:cyan_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def CyanCarpet() -> MinecraftBlockDescriptor:
        """Factory for CyanCarpet"""
        return MinecraftBlockDescriptor("minecraft:cyan_carpet", True)

    @staticmethod
    def CyanConcrete() -> MinecraftBlockDescriptor:
        """Factory for CyanConcrete"""
        return MinecraftBlockDescriptor("minecraft:cyan_concrete", True)

    @staticmethod
    def CyanConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for CyanConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:cyan_concrete_powder", True)

    @staticmethod
    def CyanGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for CyanGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:cyan_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CyanShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for CyanShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:cyan_shulker_box", True)

    @staticmethod
    def CyanStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for CyanStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:cyan_stained_glass", True)

    @staticmethod
    def CyanStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for CyanStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:cyan_stained_glass_pane", True)

    @staticmethod
    def CyanTerracotta() -> MinecraftBlockDescriptor:
        """Factory for CyanTerracotta"""
        return MinecraftBlockDescriptor("minecraft:cyan_terracotta", True)

    @staticmethod
    def CyanWool() -> MinecraftBlockDescriptor:
        """Factory for CyanWool"""
        return MinecraftBlockDescriptor("minecraft:cyan_wool", True)

    @staticmethod
    def DamagedAnvil(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for DamagedAnvil"""
        return MinecraftBlockDescriptor(
            "minecraft:damaged_anvil", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def Dandelion() -> MinecraftBlockDescriptor:
        """Factory for Dandelion"""
        return MinecraftBlockDescriptor("minecraft:dandelion", True)

    @staticmethod
    def DarkOakButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for DarkOakButton"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def DarkOakDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for DarkOakDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def DarkOakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DarkOakDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DarkOakFence() -> MinecraftBlockDescriptor:
        """Factory for DarkOakFence"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_fence", True)

    @staticmethod
    def DarkOakFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for DarkOakFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def DarkOakHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for DarkOakHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def DarkOakLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for DarkOakLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def DarkOakLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for DarkOakLog"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def DarkOakPlanks() -> MinecraftBlockDescriptor:
        """Factory for DarkOakPlanks"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_planks", True)

    @staticmethod
    def DarkOakPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for DarkOakPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def DarkOakSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for DarkOakSapling"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def DarkOakSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DarkOakSlab"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DarkOakStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for DarkOakStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DarkOakTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for DarkOakTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_oak_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def DarkOakWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for DarkOakWood"""
        return MinecraftBlockDescriptor("minecraft:dark_oak_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def DarkPrismarine() -> MinecraftBlockDescriptor:
        """Factory for DarkPrismarine"""
        return MinecraftBlockDescriptor("minecraft:dark_prismarine", True)

    @staticmethod
    def DarkPrismarineDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DarkPrismarineDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_prismarine_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DarkPrismarineSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DarkPrismarineSlab"""
        return MinecraftBlockDescriptor("minecraft:dark_prismarine_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DarkPrismarineStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for DarkPrismarineStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:dark_prismarine_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DarkoakStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for DarkoakStandingSign"""
        return MinecraftBlockDescriptor("minecraft:darkoak_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def DarkoakWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for DarkoakWallSign"""
        return MinecraftBlockDescriptor("minecraft:darkoak_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def DaylightDetector(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for DaylightDetector"""
        return MinecraftBlockDescriptor("minecraft:daylight_detector", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def DaylightDetectorInverted(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for DaylightDetectorInverted"""
        return MinecraftBlockDescriptor("minecraft:daylight_detector_inverted", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def DeadBrainCoral() -> MinecraftBlockDescriptor:
        """Factory for DeadBrainCoral"""
        return MinecraftBlockDescriptor("minecraft:dead_brain_coral", True)

    @staticmethod
    def DeadBrainCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for DeadBrainCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:dead_brain_coral_block", True)

    @staticmethod
    def DeadBrainCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadBrainCoralFan"""
        return MinecraftBlockDescriptor("minecraft:dead_brain_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadBrainCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadBrainCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:dead_brain_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadBubbleCoral() -> MinecraftBlockDescriptor:
        """Factory for DeadBubbleCoral"""
        return MinecraftBlockDescriptor("minecraft:dead_bubble_coral", True)

    @staticmethod
    def DeadBubbleCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for DeadBubbleCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:dead_bubble_coral_block", True)

    @staticmethod
    def DeadBubbleCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadBubbleCoralFan"""
        return MinecraftBlockDescriptor("minecraft:dead_bubble_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadBubbleCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadBubbleCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:dead_bubble_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadFireCoral() -> MinecraftBlockDescriptor:
        """Factory for DeadFireCoral"""
        return MinecraftBlockDescriptor("minecraft:dead_fire_coral", True)

    @staticmethod
    def DeadFireCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for DeadFireCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:dead_fire_coral_block", True)

    @staticmethod
    def DeadFireCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadFireCoralFan"""
        return MinecraftBlockDescriptor("minecraft:dead_fire_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadFireCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadFireCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:dead_fire_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadHornCoral() -> MinecraftBlockDescriptor:
        """Factory for DeadHornCoral"""
        return MinecraftBlockDescriptor("minecraft:dead_horn_coral", True)

    @staticmethod
    def DeadHornCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for DeadHornCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:dead_horn_coral_block", True)

    @staticmethod
    def DeadHornCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadHornCoralFan"""
        return MinecraftBlockDescriptor("minecraft:dead_horn_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadHornCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadHornCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:dead_horn_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadTubeCoral() -> MinecraftBlockDescriptor:
        """Factory for DeadTubeCoral"""
        return MinecraftBlockDescriptor("minecraft:dead_tube_coral", True)

    @staticmethod
    def DeadTubeCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for DeadTubeCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:dead_tube_coral_block", True)

    @staticmethod
    def DeadTubeCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadTubeCoralFan"""
        return MinecraftBlockDescriptor("minecraft:dead_tube_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadTubeCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for DeadTubeCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:dead_tube_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def Deadbush() -> MinecraftBlockDescriptor:
        """Factory for Deadbush"""
        return MinecraftBlockDescriptor("minecraft:deadbush", True)

    @staticmethod
    def DecoratedPot(direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for DecoratedPot"""
        return MinecraftBlockDescriptor("minecraft:decorated_pot", True, {_BlockStateKeys.Direction: direction})

    @staticmethod
    def Deepslate(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for Deepslate"""
        return MinecraftBlockDescriptor("minecraft:deepslate", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def DeepslateBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DeepslateBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:deepslate_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DeepslateBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DeepslateBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:deepslate_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DeepslateBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for DeepslateBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:deepslate_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DeepslateBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for DeepslateBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:deepslate_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def DeepslateBricks() -> MinecraftBlockDescriptor:
        """Factory for DeepslateBricks"""
        return MinecraftBlockDescriptor("minecraft:deepslate_bricks", True)

    @staticmethod
    def DeepslateCoalOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateCoalOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_coal_ore", True)

    @staticmethod
    def DeepslateCopperOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateCopperOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_copper_ore", True)

    @staticmethod
    def DeepslateDiamondOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateDiamondOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_diamond_ore", True)

    @staticmethod
    def DeepslateEmeraldOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateEmeraldOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_emerald_ore", True)

    @staticmethod
    def DeepslateGoldOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateGoldOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_gold_ore", True)

    @staticmethod
    def DeepslateIronOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateIronOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_iron_ore", True)

    @staticmethod
    def DeepslateLapisOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateLapisOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_lapis_ore", True)

    @staticmethod
    def DeepslateRedstoneOre() -> MinecraftBlockDescriptor:
        """Factory for DeepslateRedstoneOre"""
        return MinecraftBlockDescriptor("minecraft:deepslate_redstone_ore", True)

    @staticmethod
    def DeepslateTileDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DeepslateTileDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:deepslate_tile_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DeepslateTileSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DeepslateTileSlab"""
        return MinecraftBlockDescriptor("minecraft:deepslate_tile_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DeepslateTileStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for DeepslateTileStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:deepslate_tile_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DeepslateTileWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for DeepslateTileWall"""
        return MinecraftBlockDescriptor(
            "minecraft:deepslate_tile_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def DeepslateTiles() -> MinecraftBlockDescriptor:
        """Factory for DeepslateTiles"""
        return MinecraftBlockDescriptor("minecraft:deepslate_tiles", True)

    @staticmethod
    def Deny() -> MinecraftBlockDescriptor:
        """Factory for Deny"""
        return MinecraftBlockDescriptor("minecraft:deny", True)

    @staticmethod
    def DetectorRail(rail_data_bit: RailDataBit, rail_direction: RailDirection) -> MinecraftBlockDescriptor:
        """Factory for DetectorRail"""
        return MinecraftBlockDescriptor(
            "minecraft:detector_rail", True, {_BlockStateKeys.RailDataBit: rail_data_bit, _BlockStateKeys.RailDirection: rail_direction}
        )

    @staticmethod
    def DiamondBlock() -> MinecraftBlockDescriptor:
        """Factory for DiamondBlock"""
        return MinecraftBlockDescriptor("minecraft:diamond_block", True)

    @staticmethod
    def DiamondOre() -> MinecraftBlockDescriptor:
        """Factory for DiamondOre"""
        return MinecraftBlockDescriptor("minecraft:diamond_ore", True)

    @staticmethod
    def Diorite() -> MinecraftBlockDescriptor:
        """Factory for Diorite"""
        return MinecraftBlockDescriptor("minecraft:diorite", True)

    @staticmethod
    def DioriteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DioriteDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:diorite_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DioriteSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DioriteSlab"""
        return MinecraftBlockDescriptor("minecraft:diorite_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DioriteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for DioriteStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:diorite_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DioriteWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for DioriteWall"""
        return MinecraftBlockDescriptor(
            "minecraft:diorite_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Dirt() -> MinecraftBlockDescriptor:
        """Factory for Dirt"""
        return MinecraftBlockDescriptor("minecraft:dirt", True)

    @staticmethod
    def DirtWithRoots() -> MinecraftBlockDescriptor:
        """Factory for DirtWithRoots"""
        return MinecraftBlockDescriptor("minecraft:dirt_with_roots", True)

    @staticmethod
    def Dispenser(facing_direction: FacingDirection, triggered_bit: TriggeredBit) -> MinecraftBlockDescriptor:
        """Factory for Dispenser"""
        return MinecraftBlockDescriptor(
            "minecraft:dispenser", True,
            {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.TriggeredBit: triggered_bit},
        )

    @staticmethod
    def DoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for DoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DragonEgg() -> MinecraftBlockDescriptor:
        """Factory for DragonEgg"""
        return MinecraftBlockDescriptor("minecraft:dragon_egg", True)

    @staticmethod
    def DragonHead(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for DragonHead"""
        return MinecraftBlockDescriptor("minecraft:dragon_head", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def DriedGhast(minecraft_cardinal_direction: CardinalDirection, rehydration_level: RehydrationLevel) -> MinecraftBlockDescriptor:
        """Factory for DriedGhast"""
        return MinecraftBlockDescriptor(
            "minecraft:dried_ghast", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.RehydrationLevel: rehydration_level,
            },
        )

    @staticmethod
    def DriedKelpBlock() -> MinecraftBlockDescriptor:
        """Factory for DriedKelpBlock"""
        return MinecraftBlockDescriptor("minecraft:dried_kelp_block", True)

    @staticmethod
    def DripstoneBlock() -> MinecraftBlockDescriptor:
        """Factory for DripstoneBlock"""
        return MinecraftBlockDescriptor("minecraft:dripstone_block", True)

    @staticmethod
    def Dropper(facing_direction: FacingDirection, triggered_bit: TriggeredBit) -> MinecraftBlockDescriptor:
        """Factory for Dropper"""
        return MinecraftBlockDescriptor(
            "minecraft:dropper", True, {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.TriggeredBit: triggered_bit}
        )

    @staticmethod
    def Element0() -> MinecraftBlockDescriptor:
        """Factory for Element0"""
        return MinecraftBlockDescriptor("minecraft:element_0", True)

    @staticmethod
    def Element1() -> MinecraftBlockDescriptor:
        """Factory for Element1"""
        return MinecraftBlockDescriptor("minecraft:element_1", True)

    @staticmethod
    def Element10() -> MinecraftBlockDescriptor:
        """Factory for Element10"""
        return MinecraftBlockDescriptor("minecraft:element_10", True)

    @staticmethod
    def Element100() -> MinecraftBlockDescriptor:
        """Factory for Element100"""
        return MinecraftBlockDescriptor("minecraft:element_100", True)

    @staticmethod
    def Element101() -> MinecraftBlockDescriptor:
        """Factory for Element101"""
        return MinecraftBlockDescriptor("minecraft:element_101", True)

    @staticmethod
    def Element102() -> MinecraftBlockDescriptor:
        """Factory for Element102"""
        return MinecraftBlockDescriptor("minecraft:element_102", True)

    @staticmethod
    def Element103() -> MinecraftBlockDescriptor:
        """Factory for Element103"""
        return MinecraftBlockDescriptor("minecraft:element_103", True)

    @staticmethod
    def Element104() -> MinecraftBlockDescriptor:
        """Factory for Element104"""
        return MinecraftBlockDescriptor("minecraft:element_104", True)

    @staticmethod
    def Element105() -> MinecraftBlockDescriptor:
        """Factory for Element105"""
        return MinecraftBlockDescriptor("minecraft:element_105", True)

    @staticmethod
    def Element106() -> MinecraftBlockDescriptor:
        """Factory for Element106"""
        return MinecraftBlockDescriptor("minecraft:element_106", True)

    @staticmethod
    def Element107() -> MinecraftBlockDescriptor:
        """Factory for Element107"""
        return MinecraftBlockDescriptor("minecraft:element_107", True)

    @staticmethod
    def Element108() -> MinecraftBlockDescriptor:
        """Factory for Element108"""
        return MinecraftBlockDescriptor("minecraft:element_108", True)

    @staticmethod
    def Element109() -> MinecraftBlockDescriptor:
        """Factory for Element109"""
        return MinecraftBlockDescriptor("minecraft:element_109", True)

    @staticmethod
    def Element11() -> MinecraftBlockDescriptor:
        """Factory for Element11"""
        return MinecraftBlockDescriptor("minecraft:element_11", True)

    @staticmethod
    def Element110() -> MinecraftBlockDescriptor:
        """Factory for Element110"""
        return MinecraftBlockDescriptor("minecraft:element_110", True)

    @staticmethod
    def Element111() -> MinecraftBlockDescriptor:
        """Factory for Element111"""
        return MinecraftBlockDescriptor("minecraft:element_111", True)

    @staticmethod
    def Element112() -> MinecraftBlockDescriptor:
        """Factory for Element112"""
        return MinecraftBlockDescriptor("minecraft:element_112", True)

    @staticmethod
    def Element113() -> MinecraftBlockDescriptor:
        """Factory for Element113"""
        return MinecraftBlockDescriptor("minecraft:element_113", True)

    @staticmethod
    def Element114() -> MinecraftBlockDescriptor:
        """Factory for Element114"""
        return MinecraftBlockDescriptor("minecraft:element_114", True)

    @staticmethod
    def Element115() -> MinecraftBlockDescriptor:
        """Factory for Element115"""
        return MinecraftBlockDescriptor("minecraft:element_115", True)

    @staticmethod
    def Element116() -> MinecraftBlockDescriptor:
        """Factory for Element116"""
        return MinecraftBlockDescriptor("minecraft:element_116", True)

    @staticmethod
    def Element117() -> MinecraftBlockDescriptor:
        """Factory for Element117"""
        return MinecraftBlockDescriptor("minecraft:element_117", True)

    @staticmethod
    def Element118() -> MinecraftBlockDescriptor:
        """Factory for Element118"""
        return MinecraftBlockDescriptor("minecraft:element_118", True)

    @staticmethod
    def Element12() -> MinecraftBlockDescriptor:
        """Factory for Element12"""
        return MinecraftBlockDescriptor("minecraft:element_12", True)

    @staticmethod
    def Element13() -> MinecraftBlockDescriptor:
        """Factory for Element13"""
        return MinecraftBlockDescriptor("minecraft:element_13", True)

    @staticmethod
    def Element14() -> MinecraftBlockDescriptor:
        """Factory for Element14"""
        return MinecraftBlockDescriptor("minecraft:element_14", True)

    @staticmethod
    def Element15() -> MinecraftBlockDescriptor:
        """Factory for Element15"""
        return MinecraftBlockDescriptor("minecraft:element_15", True)

    @staticmethod
    def Element16() -> MinecraftBlockDescriptor:
        """Factory for Element16"""
        return MinecraftBlockDescriptor("minecraft:element_16", True)

    @staticmethod
    def Element17() -> MinecraftBlockDescriptor:
        """Factory for Element17"""
        return MinecraftBlockDescriptor("minecraft:element_17", True)

    @staticmethod
    def Element18() -> MinecraftBlockDescriptor:
        """Factory for Element18"""
        return MinecraftBlockDescriptor("minecraft:element_18", True)

    @staticmethod
    def Element19() -> MinecraftBlockDescriptor:
        """Factory for Element19"""
        return MinecraftBlockDescriptor("minecraft:element_19", True)

    @staticmethod
    def Element2() -> MinecraftBlockDescriptor:
        """Factory for Element2"""
        return MinecraftBlockDescriptor("minecraft:element_2", True)

    @staticmethod
    def Element20() -> MinecraftBlockDescriptor:
        """Factory for Element20"""
        return MinecraftBlockDescriptor("minecraft:element_20", True)

    @staticmethod
    def Element21() -> MinecraftBlockDescriptor:
        """Factory for Element21"""
        return MinecraftBlockDescriptor("minecraft:element_21", True)

    @staticmethod
    def Element22() -> MinecraftBlockDescriptor:
        """Factory for Element22"""
        return MinecraftBlockDescriptor("minecraft:element_22", True)

    @staticmethod
    def Element23() -> MinecraftBlockDescriptor:
        """Factory for Element23"""
        return MinecraftBlockDescriptor("minecraft:element_23", True)

    @staticmethod
    def Element24() -> MinecraftBlockDescriptor:
        """Factory for Element24"""
        return MinecraftBlockDescriptor("minecraft:element_24", True)

    @staticmethod
    def Element25() -> MinecraftBlockDescriptor:
        """Factory for Element25"""
        return MinecraftBlockDescriptor("minecraft:element_25", True)

    @staticmethod
    def Element26() -> MinecraftBlockDescriptor:
        """Factory for Element26"""
        return MinecraftBlockDescriptor("minecraft:element_26", True)

    @staticmethod
    def Element27() -> MinecraftBlockDescriptor:
        """Factory for Element27"""
        return MinecraftBlockDescriptor("minecraft:element_27", True)

    @staticmethod
    def Element28() -> MinecraftBlockDescriptor:
        """Factory for Element28"""
        return MinecraftBlockDescriptor("minecraft:element_28", True)

    @staticmethod
    def Element29() -> MinecraftBlockDescriptor:
        """Factory for Element29"""
        return MinecraftBlockDescriptor("minecraft:element_29", True)

    @staticmethod
    def Element3() -> MinecraftBlockDescriptor:
        """Factory for Element3"""
        return MinecraftBlockDescriptor("minecraft:element_3", True)

    @staticmethod
    def Element30() -> MinecraftBlockDescriptor:
        """Factory for Element30"""
        return MinecraftBlockDescriptor("minecraft:element_30", True)

    @staticmethod
    def Element31() -> MinecraftBlockDescriptor:
        """Factory for Element31"""
        return MinecraftBlockDescriptor("minecraft:element_31", True)

    @staticmethod
    def Element32() -> MinecraftBlockDescriptor:
        """Factory for Element32"""
        return MinecraftBlockDescriptor("minecraft:element_32", True)

    @staticmethod
    def Element33() -> MinecraftBlockDescriptor:
        """Factory for Element33"""
        return MinecraftBlockDescriptor("minecraft:element_33", True)

    @staticmethod
    def Element34() -> MinecraftBlockDescriptor:
        """Factory for Element34"""
        return MinecraftBlockDescriptor("minecraft:element_34", True)

    @staticmethod
    def Element35() -> MinecraftBlockDescriptor:
        """Factory for Element35"""
        return MinecraftBlockDescriptor("minecraft:element_35", True)

    @staticmethod
    def Element36() -> MinecraftBlockDescriptor:
        """Factory for Element36"""
        return MinecraftBlockDescriptor("minecraft:element_36", True)

    @staticmethod
    def Element37() -> MinecraftBlockDescriptor:
        """Factory for Element37"""
        return MinecraftBlockDescriptor("minecraft:element_37", True)

    @staticmethod
    def Element38() -> MinecraftBlockDescriptor:
        """Factory for Element38"""
        return MinecraftBlockDescriptor("minecraft:element_38", True)

    @staticmethod
    def Element39() -> MinecraftBlockDescriptor:
        """Factory for Element39"""
        return MinecraftBlockDescriptor("minecraft:element_39", True)

    @staticmethod
    def Element4() -> MinecraftBlockDescriptor:
        """Factory for Element4"""
        return MinecraftBlockDescriptor("minecraft:element_4", True)

    @staticmethod
    def Element40() -> MinecraftBlockDescriptor:
        """Factory for Element40"""
        return MinecraftBlockDescriptor("minecraft:element_40", True)

    @staticmethod
    def Element41() -> MinecraftBlockDescriptor:
        """Factory for Element41"""
        return MinecraftBlockDescriptor("minecraft:element_41", True)

    @staticmethod
    def Element42() -> MinecraftBlockDescriptor:
        """Factory for Element42"""
        return MinecraftBlockDescriptor("minecraft:element_42", True)

    @staticmethod
    def Element43() -> MinecraftBlockDescriptor:
        """Factory for Element43"""
        return MinecraftBlockDescriptor("minecraft:element_43", True)

    @staticmethod
    def Element44() -> MinecraftBlockDescriptor:
        """Factory for Element44"""
        return MinecraftBlockDescriptor("minecraft:element_44", True)

    @staticmethod
    def Element45() -> MinecraftBlockDescriptor:
        """Factory for Element45"""
        return MinecraftBlockDescriptor("minecraft:element_45", True)

    @staticmethod
    def Element46() -> MinecraftBlockDescriptor:
        """Factory for Element46"""
        return MinecraftBlockDescriptor("minecraft:element_46", True)

    @staticmethod
    def Element47() -> MinecraftBlockDescriptor:
        """Factory for Element47"""
        return MinecraftBlockDescriptor("minecraft:element_47", True)

    @staticmethod
    def Element48() -> MinecraftBlockDescriptor:
        """Factory for Element48"""
        return MinecraftBlockDescriptor("minecraft:element_48", True)

    @staticmethod
    def Element49() -> MinecraftBlockDescriptor:
        """Factory for Element49"""
        return MinecraftBlockDescriptor("minecraft:element_49", True)

    @staticmethod
    def Element5() -> MinecraftBlockDescriptor:
        """Factory for Element5"""
        return MinecraftBlockDescriptor("minecraft:element_5", True)

    @staticmethod
    def Element50() -> MinecraftBlockDescriptor:
        """Factory for Element50"""
        return MinecraftBlockDescriptor("minecraft:element_50", True)

    @staticmethod
    def Element51() -> MinecraftBlockDescriptor:
        """Factory for Element51"""
        return MinecraftBlockDescriptor("minecraft:element_51", True)

    @staticmethod
    def Element52() -> MinecraftBlockDescriptor:
        """Factory for Element52"""
        return MinecraftBlockDescriptor("minecraft:element_52", True)

    @staticmethod
    def Element53() -> MinecraftBlockDescriptor:
        """Factory for Element53"""
        return MinecraftBlockDescriptor("minecraft:element_53", True)

    @staticmethod
    def Element54() -> MinecraftBlockDescriptor:
        """Factory for Element54"""
        return MinecraftBlockDescriptor("minecraft:element_54", True)

    @staticmethod
    def Element55() -> MinecraftBlockDescriptor:
        """Factory for Element55"""
        return MinecraftBlockDescriptor("minecraft:element_55", True)

    @staticmethod
    def Element56() -> MinecraftBlockDescriptor:
        """Factory for Element56"""
        return MinecraftBlockDescriptor("minecraft:element_56", True)

    @staticmethod
    def Element57() -> MinecraftBlockDescriptor:
        """Factory for Element57"""
        return MinecraftBlockDescriptor("minecraft:element_57", True)

    @staticmethod
    def Element58() -> MinecraftBlockDescriptor:
        """Factory for Element58"""
        return MinecraftBlockDescriptor("minecraft:element_58", True)

    @staticmethod
    def Element59() -> MinecraftBlockDescriptor:
        """Factory for Element59"""
        return MinecraftBlockDescriptor("minecraft:element_59", True)

    @staticmethod
    def Element6() -> MinecraftBlockDescriptor:
        """Factory for Element6"""
        return MinecraftBlockDescriptor("minecraft:element_6", True)

    @staticmethod
    def Element60() -> MinecraftBlockDescriptor:
        """Factory for Element60"""
        return MinecraftBlockDescriptor("minecraft:element_60", True)

    @staticmethod
    def Element61() -> MinecraftBlockDescriptor:
        """Factory for Element61"""
        return MinecraftBlockDescriptor("minecraft:element_61", True)

    @staticmethod
    def Element62() -> MinecraftBlockDescriptor:
        """Factory for Element62"""
        return MinecraftBlockDescriptor("minecraft:element_62", True)

    @staticmethod
    def Element63() -> MinecraftBlockDescriptor:
        """Factory for Element63"""
        return MinecraftBlockDescriptor("minecraft:element_63", True)

    @staticmethod
    def Element64() -> MinecraftBlockDescriptor:
        """Factory for Element64"""
        return MinecraftBlockDescriptor("minecraft:element_64", True)

    @staticmethod
    def Element65() -> MinecraftBlockDescriptor:
        """Factory for Element65"""
        return MinecraftBlockDescriptor("minecraft:element_65", True)

    @staticmethod
    def Element66() -> MinecraftBlockDescriptor:
        """Factory for Element66"""
        return MinecraftBlockDescriptor("minecraft:element_66", True)

    @staticmethod
    def Element67() -> MinecraftBlockDescriptor:
        """Factory for Element67"""
        return MinecraftBlockDescriptor("minecraft:element_67", True)

    @staticmethod
    def Element68() -> MinecraftBlockDescriptor:
        """Factory for Element68"""
        return MinecraftBlockDescriptor("minecraft:element_68", True)

    @staticmethod
    def Element69() -> MinecraftBlockDescriptor:
        """Factory for Element69"""
        return MinecraftBlockDescriptor("minecraft:element_69", True)

    @staticmethod
    def Element7() -> MinecraftBlockDescriptor:
        """Factory for Element7"""
        return MinecraftBlockDescriptor("minecraft:element_7", True)

    @staticmethod
    def Element70() -> MinecraftBlockDescriptor:
        """Factory for Element70"""
        return MinecraftBlockDescriptor("minecraft:element_70", True)

    @staticmethod
    def Element71() -> MinecraftBlockDescriptor:
        """Factory for Element71"""
        return MinecraftBlockDescriptor("minecraft:element_71", True)

    @staticmethod
    def Element72() -> MinecraftBlockDescriptor:
        """Factory for Element72"""
        return MinecraftBlockDescriptor("minecraft:element_72", True)

    @staticmethod
    def Element73() -> MinecraftBlockDescriptor:
        """Factory for Element73"""
        return MinecraftBlockDescriptor("minecraft:element_73", True)

    @staticmethod
    def Element74() -> MinecraftBlockDescriptor:
        """Factory for Element74"""
        return MinecraftBlockDescriptor("minecraft:element_74", True)

    @staticmethod
    def Element75() -> MinecraftBlockDescriptor:
        """Factory for Element75"""
        return MinecraftBlockDescriptor("minecraft:element_75", True)

    @staticmethod
    def Element76() -> MinecraftBlockDescriptor:
        """Factory for Element76"""
        return MinecraftBlockDescriptor("minecraft:element_76", True)

    @staticmethod
    def Element77() -> MinecraftBlockDescriptor:
        """Factory for Element77"""
        return MinecraftBlockDescriptor("minecraft:element_77", True)

    @staticmethod
    def Element78() -> MinecraftBlockDescriptor:
        """Factory for Element78"""
        return MinecraftBlockDescriptor("minecraft:element_78", True)

    @staticmethod
    def Element79() -> MinecraftBlockDescriptor:
        """Factory for Element79"""
        return MinecraftBlockDescriptor("minecraft:element_79", True)

    @staticmethod
    def Element8() -> MinecraftBlockDescriptor:
        """Factory for Element8"""
        return MinecraftBlockDescriptor("minecraft:element_8", True)

    @staticmethod
    def Element80() -> MinecraftBlockDescriptor:
        """Factory for Element80"""
        return MinecraftBlockDescriptor("minecraft:element_80", True)

    @staticmethod
    def Element81() -> MinecraftBlockDescriptor:
        """Factory for Element81"""
        return MinecraftBlockDescriptor("minecraft:element_81", True)

    @staticmethod
    def Element82() -> MinecraftBlockDescriptor:
        """Factory for Element82"""
        return MinecraftBlockDescriptor("minecraft:element_82", True)

    @staticmethod
    def Element83() -> MinecraftBlockDescriptor:
        """Factory for Element83"""
        return MinecraftBlockDescriptor("minecraft:element_83", True)

    @staticmethod
    def Element84() -> MinecraftBlockDescriptor:
        """Factory for Element84"""
        return MinecraftBlockDescriptor("minecraft:element_84", True)

    @staticmethod
    def Element85() -> MinecraftBlockDescriptor:
        """Factory for Element85"""
        return MinecraftBlockDescriptor("minecraft:element_85", True)

    @staticmethod
    def Element86() -> MinecraftBlockDescriptor:
        """Factory for Element86"""
        return MinecraftBlockDescriptor("minecraft:element_86", True)

    @staticmethod
    def Element87() -> MinecraftBlockDescriptor:
        """Factory for Element87"""
        return MinecraftBlockDescriptor("minecraft:element_87", True)

    @staticmethod
    def Element88() -> MinecraftBlockDescriptor:
        """Factory for Element88"""
        return MinecraftBlockDescriptor("minecraft:element_88", True)

    @staticmethod
    def Element89() -> MinecraftBlockDescriptor:
        """Factory for Element89"""
        return MinecraftBlockDescriptor("minecraft:element_89", True)

    @staticmethod
    def Element9() -> MinecraftBlockDescriptor:
        """Factory for Element9"""
        return MinecraftBlockDescriptor("minecraft:element_9", True)

    @staticmethod
    def Element90() -> MinecraftBlockDescriptor:
        """Factory for Element90"""
        return MinecraftBlockDescriptor("minecraft:element_90", True)

    @staticmethod
    def Element91() -> MinecraftBlockDescriptor:
        """Factory for Element91"""
        return MinecraftBlockDescriptor("minecraft:element_91", True)

    @staticmethod
    def Element92() -> MinecraftBlockDescriptor:
        """Factory for Element92"""
        return MinecraftBlockDescriptor("minecraft:element_92", True)

    @staticmethod
    def Element93() -> MinecraftBlockDescriptor:
        """Factory for Element93"""
        return MinecraftBlockDescriptor("minecraft:element_93", True)

    @staticmethod
    def Element94() -> MinecraftBlockDescriptor:
        """Factory for Element94"""
        return MinecraftBlockDescriptor("minecraft:element_94", True)

    @staticmethod
    def Element95() -> MinecraftBlockDescriptor:
        """Factory for Element95"""
        return MinecraftBlockDescriptor("minecraft:element_95", True)

    @staticmethod
    def Element96() -> MinecraftBlockDescriptor:
        """Factory for Element96"""
        return MinecraftBlockDescriptor("minecraft:element_96", True)

    @staticmethod
    def Element97() -> MinecraftBlockDescriptor:
        """Factory for Element97"""
        return MinecraftBlockDescriptor("minecraft:element_97", True)

    @staticmethod
    def Element98() -> MinecraftBlockDescriptor:
        """Factory for Element98"""
        return MinecraftBlockDescriptor("minecraft:element_98", True)

    @staticmethod
    def Element99() -> MinecraftBlockDescriptor:
        """Factory for Element99"""
        return MinecraftBlockDescriptor("minecraft:element_99", True)

    @staticmethod
    def ElementConstructor(direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for ElementConstructor"""
        return MinecraftBlockDescriptor("minecraft:element_constructor", True, {_BlockStateKeys.Direction: direction})

    @staticmethod
    def EmeraldBlock() -> MinecraftBlockDescriptor:
        """Factory for EmeraldBlock"""
        return MinecraftBlockDescriptor("minecraft:emerald_block", True)

    @staticmethod
    def EmeraldOre() -> MinecraftBlockDescriptor:
        """Factory for EmeraldOre"""
        return MinecraftBlockDescriptor("minecraft:emerald_ore", True)

    @staticmethod
    def EnchantingTable() -> MinecraftBlockDescriptor:
        """Factory for EnchantingTable"""
        return MinecraftBlockDescriptor("minecraft:enchanting_table", True)

    @staticmethod
    def EndBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for EndBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:end_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def EndBricks() -> MinecraftBlockDescriptor:
        """Factory for EndBricks"""
        return MinecraftBlockDescriptor("minecraft:end_bricks", True)

    @staticmethod
    def EndPortal() -> MinecraftBlockDescriptor:
        """Factory for EndPortal"""
        return MinecraftBlockDescriptor("minecraft:end_portal", True)

    @staticmethod
    def EndPortalFrame(end_portal_eye_bit: EndPortalEyeBit, minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for EndPortalFrame"""
        return MinecraftBlockDescriptor(
            "minecraft:end_portal_frame", True,
            {
                _BlockStateKeys.EndPortalEyeBit: end_portal_eye_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def EndRod(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for EndRod"""
        return MinecraftBlockDescriptor("minecraft:end_rod", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def EndStone() -> MinecraftBlockDescriptor:
        """Factory for EndStone"""
        return MinecraftBlockDescriptor("minecraft:end_stone", True)

    @staticmethod
    def EndStoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for EndStoneBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:end_stone_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def EndStoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for EndStoneBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:end_stone_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def EndStoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for EndStoneBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:end_stone_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def EnderChest(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for EnderChest"""
        return MinecraftBlockDescriptor(
            "minecraft:ender_chest", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def ExposedChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for ExposedChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:exposed_chiseled_copper", True)

    @staticmethod
    def ExposedCopper() -> MinecraftBlockDescriptor:
        """Factory for ExposedCopper"""
        return MinecraftBlockDescriptor("minecraft:exposed_copper", True)

    @staticmethod
    def ExposedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for ExposedCopperBulb"""
        return MinecraftBlockDescriptor(
            "minecraft:exposed_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def ExposedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for ExposedCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:exposed_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def ExposedCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for ExposedCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:exposed_copper_grate", True)

    @staticmethod
    def ExposedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for ExposedCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:exposed_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def ExposedCutCopper() -> MinecraftBlockDescriptor:
        """Factory for ExposedCutCopper"""
        return MinecraftBlockDescriptor("minecraft:exposed_cut_copper", True)

    @staticmethod
    def ExposedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for ExposedCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:exposed_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def ExposedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for ExposedCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:exposed_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def ExposedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for ExposedDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:exposed_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def Farmland(moisturized_amount: MoisturizedAmount) -> MinecraftBlockDescriptor:
        """Factory for Farmland"""
        return MinecraftBlockDescriptor("minecraft:farmland", True, {_BlockStateKeys.MoisturizedAmount: moisturized_amount})

    @staticmethod
    def FenceGate(in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit) -> MinecraftBlockDescriptor:
        """Factory for FenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def Fern() -> MinecraftBlockDescriptor:
        """Factory for Fern"""
        return MinecraftBlockDescriptor("minecraft:fern", True)

    @staticmethod
    def Fire(age: Age) -> MinecraftBlockDescriptor:
        """Factory for Fire"""
        return MinecraftBlockDescriptor("minecraft:fire", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def FireCoral() -> MinecraftBlockDescriptor:
        """Factory for FireCoral"""
        return MinecraftBlockDescriptor("minecraft:fire_coral", True)

    @staticmethod
    def FireCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for FireCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:fire_coral_block", True)

    @staticmethod
    def FireCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for FireCoralFan"""
        return MinecraftBlockDescriptor("minecraft:fire_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def FireCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for FireCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:fire_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def FireflyBush() -> MinecraftBlockDescriptor:
        """Factory for FireflyBush"""
        return MinecraftBlockDescriptor("minecraft:firefly_bush", True)

    @staticmethod
    def FletchingTable() -> MinecraftBlockDescriptor:
        """Factory for FletchingTable"""
        return MinecraftBlockDescriptor("minecraft:fletching_table", True)

    @staticmethod
    def FlowerPot(update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for FlowerPot"""
        return MinecraftBlockDescriptor("minecraft:flower_pot", True, {_BlockStateKeys.UpdateBit: update_bit})

    @staticmethod
    def FloweringAzalea() -> MinecraftBlockDescriptor:
        """Factory for FloweringAzalea"""
        return MinecraftBlockDescriptor("minecraft:flowering_azalea", True)

    @staticmethod
    def FlowingLava(liquid_depth: LiquidDepth) -> MinecraftBlockDescriptor:
        """Factory for FlowingLava"""
        return MinecraftBlockDescriptor("minecraft:flowing_lava", True, {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def FlowingWater(liquid_depth: LiquidDepth) -> MinecraftBlockDescriptor:
        """Factory for FlowingWater"""
        return MinecraftBlockDescriptor("minecraft:flowing_water", True, {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def Frame(
        facing_direction: FacingDirection, item_frame_map_bit: ItemFrameMapBit, item_frame_photo_bit: ItemFramePhotoBit
    ) -> MinecraftBlockDescriptor:
        """Factory for Frame"""
        return MinecraftBlockDescriptor(
            "minecraft:frame", True,
            {
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.ItemFrameMapBit: item_frame_map_bit,
                _BlockStateKeys.ItemFramePhotoBit: item_frame_photo_bit,
            },
        )

    @staticmethod
    def FrogSpawn() -> MinecraftBlockDescriptor:
        """Factory for FrogSpawn"""
        return MinecraftBlockDescriptor("minecraft:frog_spawn", True)

    @staticmethod
    def FrostedIce(age: Age) -> MinecraftBlockDescriptor:
        """Factory for FrostedIce"""
        return MinecraftBlockDescriptor("minecraft:frosted_ice", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def Furnace(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Furnace"""
        return MinecraftBlockDescriptor("minecraft:furnace", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def GildedBlackstone() -> MinecraftBlockDescriptor:
        """Factory for GildedBlackstone"""
        return MinecraftBlockDescriptor("minecraft:gilded_blackstone", True)

    @staticmethod
    def Glass() -> MinecraftBlockDescriptor:
        """Factory for Glass"""
        return MinecraftBlockDescriptor("minecraft:glass", True)

    @staticmethod
    def GlassPane() -> MinecraftBlockDescriptor:
        """Factory for GlassPane"""
        return MinecraftBlockDescriptor("minecraft:glass_pane", True)

    @staticmethod
    def GlowFrame(
        facing_direction: FacingDirection, item_frame_map_bit: ItemFrameMapBit, item_frame_photo_bit: ItemFramePhotoBit
    ) -> MinecraftBlockDescriptor:
        """Factory for GlowFrame"""
        return MinecraftBlockDescriptor(
            "minecraft:glow_frame", True,
            {
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.ItemFrameMapBit: item_frame_map_bit,
                _BlockStateKeys.ItemFramePhotoBit: item_frame_photo_bit,
            },
        )

    @staticmethod
    def GlowLichen(multi_face_direction_bits: MultiFaceDirectionBits) -> MinecraftBlockDescriptor:
        """Factory for GlowLichen"""
        return MinecraftBlockDescriptor("minecraft:glow_lichen", True, {_BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits})

    @staticmethod
    def Glowstone() -> MinecraftBlockDescriptor:
        """Factory for Glowstone"""
        return MinecraftBlockDescriptor("minecraft:glowstone", True)

    @staticmethod
    def GoldBlock() -> MinecraftBlockDescriptor:
        """Factory for GoldBlock"""
        return MinecraftBlockDescriptor("minecraft:gold_block", True)

    @staticmethod
    def GoldOre() -> MinecraftBlockDescriptor:
        """Factory for GoldOre"""
        return MinecraftBlockDescriptor("minecraft:gold_ore", True)

    @staticmethod
    def GoldenRail(rail_data_bit: RailDataBit, rail_direction: RailDirection) -> MinecraftBlockDescriptor:
        """Factory for GoldenRail"""
        return MinecraftBlockDescriptor(
            "minecraft:golden_rail", True, {_BlockStateKeys.RailDataBit: rail_data_bit, _BlockStateKeys.RailDirection: rail_direction}
        )

    @staticmethod
    def Granite() -> MinecraftBlockDescriptor:
        """Factory for Granite"""
        return MinecraftBlockDescriptor("minecraft:granite", True)

    @staticmethod
    def GraniteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for GraniteDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:granite_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def GraniteSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for GraniteSlab"""
        return MinecraftBlockDescriptor("minecraft:granite_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def GraniteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for GraniteStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:granite_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def GraniteWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for GraniteWall"""
        return MinecraftBlockDescriptor(
            "minecraft:granite_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def GrassBlock() -> MinecraftBlockDescriptor:
        """Factory for GrassBlock"""
        return MinecraftBlockDescriptor("minecraft:grass_block", True)

    @staticmethod
    def GrassPath() -> MinecraftBlockDescriptor:
        """Factory for GrassPath"""
        return MinecraftBlockDescriptor("minecraft:grass_path", True)

    @staticmethod
    def Gravel() -> MinecraftBlockDescriptor:
        """Factory for Gravel"""
        return MinecraftBlockDescriptor("minecraft:gravel", True)

    @staticmethod
    def GrayCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for GrayCandle"""
        return MinecraftBlockDescriptor("minecraft:gray_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def GrayCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for GrayCandleCake"""
        return MinecraftBlockDescriptor("minecraft:gray_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def GrayCarpet() -> MinecraftBlockDescriptor:
        """Factory for GrayCarpet"""
        return MinecraftBlockDescriptor("minecraft:gray_carpet", True)

    @staticmethod
    def GrayConcrete() -> MinecraftBlockDescriptor:
        """Factory for GrayConcrete"""
        return MinecraftBlockDescriptor("minecraft:gray_concrete", True)

    @staticmethod
    def GrayConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for GrayConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:gray_concrete_powder", True)

    @staticmethod
    def GrayGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for GrayGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:gray_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def GrayShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for GrayShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:gray_shulker_box", True)

    @staticmethod
    def GrayStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for GrayStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:gray_stained_glass", True)

    @staticmethod
    def GrayStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for GrayStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:gray_stained_glass_pane", True)

    @staticmethod
    def GrayTerracotta() -> MinecraftBlockDescriptor:
        """Factory for GrayTerracotta"""
        return MinecraftBlockDescriptor("minecraft:gray_terracotta", True)

    @staticmethod
    def GrayWool() -> MinecraftBlockDescriptor:
        """Factory for GrayWool"""
        return MinecraftBlockDescriptor("minecraft:gray_wool", True)

    @staticmethod
    def GreenCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for GreenCandle"""
        return MinecraftBlockDescriptor("minecraft:green_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def GreenCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for GreenCandleCake"""
        return MinecraftBlockDescriptor("minecraft:green_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def GreenCarpet() -> MinecraftBlockDescriptor:
        """Factory for GreenCarpet"""
        return MinecraftBlockDescriptor("minecraft:green_carpet", True)

    @staticmethod
    def GreenConcrete() -> MinecraftBlockDescriptor:
        """Factory for GreenConcrete"""
        return MinecraftBlockDescriptor("minecraft:green_concrete", True)

    @staticmethod
    def GreenConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for GreenConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:green_concrete_powder", True)

    @staticmethod
    def GreenGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for GreenGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:green_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def GreenShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for GreenShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:green_shulker_box", True)

    @staticmethod
    def GreenStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for GreenStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:green_stained_glass", True)

    @staticmethod
    def GreenStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for GreenStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:green_stained_glass_pane", True)

    @staticmethod
    def GreenTerracotta() -> MinecraftBlockDescriptor:
        """Factory for GreenTerracotta"""
        return MinecraftBlockDescriptor("minecraft:green_terracotta", True)

    @staticmethod
    def GreenWool() -> MinecraftBlockDescriptor:
        """Factory for GreenWool"""
        return MinecraftBlockDescriptor("minecraft:green_wool", True)

    @staticmethod
    def Grindstone(attachment: Attachment, direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for Grindstone"""
        return MinecraftBlockDescriptor(
            "minecraft:grindstone", True, {_BlockStateKeys.Attachment: attachment, _BlockStateKeys.Direction: direction}
        )

    @staticmethod
    def HangingRoots() -> MinecraftBlockDescriptor:
        """Factory for HangingRoots"""
        return MinecraftBlockDescriptor("minecraft:hanging_roots", True)

    @staticmethod
    def HardBlackStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardBlackStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_black_stained_glass", True)

    @staticmethod
    def HardBlackStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardBlackStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_black_stained_glass_pane", True)

    @staticmethod
    def HardBlueStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardBlueStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_blue_stained_glass", True)

    @staticmethod
    def HardBlueStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardBlueStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_blue_stained_glass_pane", True)

    @staticmethod
    def HardBrownStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardBrownStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_brown_stained_glass", True)

    @staticmethod
    def HardBrownStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardBrownStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_brown_stained_glass_pane", True)

    @staticmethod
    def HardCyanStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardCyanStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_cyan_stained_glass", True)

    @staticmethod
    def HardCyanStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardCyanStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_cyan_stained_glass_pane", True)

    @staticmethod
    def HardGlass() -> MinecraftBlockDescriptor:
        """Factory for HardGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_glass", True)

    @staticmethod
    def HardGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_glass_pane", True)

    @staticmethod
    def HardGrayStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardGrayStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_gray_stained_glass", True)

    @staticmethod
    def HardGrayStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardGrayStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_gray_stained_glass_pane", True)

    @staticmethod
    def HardGreenStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardGreenStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_green_stained_glass", True)

    @staticmethod
    def HardGreenStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardGreenStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_green_stained_glass_pane", True)

    @staticmethod
    def HardLightBlueStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardLightBlueStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_light_blue_stained_glass", True)

    @staticmethod
    def HardLightBlueStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardLightBlueStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_light_blue_stained_glass_pane", True)

    @staticmethod
    def HardLightGrayStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardLightGrayStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_light_gray_stained_glass", True)

    @staticmethod
    def HardLightGrayStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardLightGrayStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_light_gray_stained_glass_pane", True)

    @staticmethod
    def HardLimeStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardLimeStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_lime_stained_glass", True)

    @staticmethod
    def HardLimeStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardLimeStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_lime_stained_glass_pane", True)

    @staticmethod
    def HardMagentaStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardMagentaStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_magenta_stained_glass", True)

    @staticmethod
    def HardMagentaStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardMagentaStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_magenta_stained_glass_pane", True)

    @staticmethod
    def HardOrangeStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardOrangeStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_orange_stained_glass", True)

    @staticmethod
    def HardOrangeStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardOrangeStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_orange_stained_glass_pane", True)

    @staticmethod
    def HardPinkStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardPinkStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_pink_stained_glass", True)

    @staticmethod
    def HardPinkStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardPinkStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_pink_stained_glass_pane", True)

    @staticmethod
    def HardPurpleStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardPurpleStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_purple_stained_glass", True)

    @staticmethod
    def HardPurpleStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardPurpleStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_purple_stained_glass_pane", True)

    @staticmethod
    def HardRedStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardRedStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_red_stained_glass", True)

    @staticmethod
    def HardRedStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardRedStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_red_stained_glass_pane", True)

    @staticmethod
    def HardWhiteStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardWhiteStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_white_stained_glass", True)

    @staticmethod
    def HardWhiteStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardWhiteStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_white_stained_glass_pane", True)

    @staticmethod
    def HardYellowStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for HardYellowStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:hard_yellow_stained_glass", True)

    @staticmethod
    def HardYellowStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for HardYellowStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:hard_yellow_stained_glass_pane", True)

    @staticmethod
    def HardenedClay() -> MinecraftBlockDescriptor:
        """Factory for HardenedClay"""
        return MinecraftBlockDescriptor("minecraft:hardened_clay", True)

    @staticmethod
    def HayBlock(deprecated: Deprecated, pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for HayBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:hay_block", True, {_BlockStateKeys.Deprecated: deprecated, _BlockStateKeys.PillarAxis: pillar_axis}
        )

    @staticmethod
    def HeavyCore() -> MinecraftBlockDescriptor:
        """Factory for HeavyCore"""
        return MinecraftBlockDescriptor("minecraft:heavy_core", True)

    @staticmethod
    def HeavyWeightedPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for HeavyWeightedPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:heavy_weighted_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def HoneyBlock() -> MinecraftBlockDescriptor:
        """Factory for HoneyBlock"""
        return MinecraftBlockDescriptor("minecraft:honey_block", True)

    @staticmethod
    def HoneycombBlock() -> MinecraftBlockDescriptor:
        """Factory for HoneycombBlock"""
        return MinecraftBlockDescriptor("minecraft:honeycomb_block", True)

    @staticmethod
    def Hopper(facing_direction: FacingDirection, toggle_bit: ToggleBit) -> MinecraftBlockDescriptor:
        """Factory for Hopper"""
        return MinecraftBlockDescriptor(
            "minecraft:hopper", True, {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.ToggleBit: toggle_bit}
        )

    @staticmethod
    def HornCoral() -> MinecraftBlockDescriptor:
        """Factory for HornCoral"""
        return MinecraftBlockDescriptor("minecraft:horn_coral", True)

    @staticmethod
    def HornCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for HornCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:horn_coral_block", True)

    @staticmethod
    def HornCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for HornCoralFan"""
        return MinecraftBlockDescriptor("minecraft:horn_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def HornCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for HornCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:horn_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def Ice() -> MinecraftBlockDescriptor:
        """Factory for Ice"""
        return MinecraftBlockDescriptor("minecraft:ice", True)

    @staticmethod
    def InfestedChiseledStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for InfestedChiseledStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:infested_chiseled_stone_bricks", True)

    @staticmethod
    def InfestedCobblestone() -> MinecraftBlockDescriptor:
        """Factory for InfestedCobblestone"""
        return MinecraftBlockDescriptor("minecraft:infested_cobblestone", True)

    @staticmethod
    def InfestedCrackedStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for InfestedCrackedStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:infested_cracked_stone_bricks", True)

    @staticmethod
    def InfestedDeepslate(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for InfestedDeepslate"""
        return MinecraftBlockDescriptor("minecraft:infested_deepslate", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def InfestedMossyStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for InfestedMossyStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:infested_mossy_stone_bricks", True)

    @staticmethod
    def InfestedStone() -> MinecraftBlockDescriptor:
        """Factory for InfestedStone"""
        return MinecraftBlockDescriptor("minecraft:infested_stone", True)

    @staticmethod
    def InfestedStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for InfestedStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:infested_stone_bricks", True)

    @staticmethod
    def IronBars() -> MinecraftBlockDescriptor:
        """Factory for IronBars"""
        return MinecraftBlockDescriptor("minecraft:iron_bars", True)

    @staticmethod
    def IronBlock() -> MinecraftBlockDescriptor:
        """Factory for IronBlock"""
        return MinecraftBlockDescriptor("minecraft:iron_block", True)

    @staticmethod
    def IronDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for IronDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:iron_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def IronOre() -> MinecraftBlockDescriptor:
        """Factory for IronOre"""
        return MinecraftBlockDescriptor("minecraft:iron_ore", True)

    @staticmethod
    def IronTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for IronTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:iron_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def Jigsaw(facing_direction: FacingDirection, rotation: Rotation) -> MinecraftBlockDescriptor:
        """Factory for Jigsaw"""
        return MinecraftBlockDescriptor(
            "minecraft:jigsaw", True, {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.Rotation: rotation}
        )

    @staticmethod
    def Jukebox() -> MinecraftBlockDescriptor:
        """Factory for Jukebox"""
        return MinecraftBlockDescriptor("minecraft:jukebox", True)

    @staticmethod
    def JungleButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for JungleButton"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def JungleDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for JungleDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def JungleDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for JungleDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:jungle_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def JungleFence() -> MinecraftBlockDescriptor:
        """Factory for JungleFence"""
        return MinecraftBlockDescriptor("minecraft:jungle_fence", True)

    @staticmethod
    def JungleFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for JungleFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def JungleHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for JungleHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def JungleLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for JungleLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def JungleLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for JungleLog"""
        return MinecraftBlockDescriptor("minecraft:jungle_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def JunglePlanks() -> MinecraftBlockDescriptor:
        """Factory for JunglePlanks"""
        return MinecraftBlockDescriptor("minecraft:jungle_planks", True)

    @staticmethod
    def JunglePressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for JunglePressurePlate"""
        return MinecraftBlockDescriptor("minecraft:jungle_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def JungleSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for JungleSapling"""
        return MinecraftBlockDescriptor("minecraft:jungle_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def JungleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for JungleSlab"""
        return MinecraftBlockDescriptor("minecraft:jungle_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def JungleStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for JungleStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def JungleStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for JungleStandingSign"""
        return MinecraftBlockDescriptor("minecraft:jungle_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def JungleTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for JungleTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:jungle_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def JungleWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for JungleWallSign"""
        return MinecraftBlockDescriptor("minecraft:jungle_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def JungleWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for JungleWood"""
        return MinecraftBlockDescriptor("minecraft:jungle_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Kelp(kelp_age: KelpAge) -> MinecraftBlockDescriptor:
        """Factory for Kelp"""
        return MinecraftBlockDescriptor("minecraft:kelp", True, {_BlockStateKeys.KelpAge: kelp_age})

    @staticmethod
    def LabTable(direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for LabTable"""
        return MinecraftBlockDescriptor("minecraft:lab_table", True, {_BlockStateKeys.Direction: direction})

    @staticmethod
    def Ladder(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for Ladder"""
        return MinecraftBlockDescriptor("minecraft:ladder", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Lantern(hanging: Hanging) -> MinecraftBlockDescriptor:
        """Factory for Lantern"""
        return MinecraftBlockDescriptor("minecraft:lantern", True, {_BlockStateKeys.Hanging: hanging})

    @staticmethod
    def LapisBlock() -> MinecraftBlockDescriptor:
        """Factory for LapisBlock"""
        return MinecraftBlockDescriptor("minecraft:lapis_block", True)

    @staticmethod
    def LapisOre() -> MinecraftBlockDescriptor:
        """Factory for LapisOre"""
        return MinecraftBlockDescriptor("minecraft:lapis_ore", True)

    @staticmethod
    def LargeAmethystBud(minecraft_block_face: BlockFace) -> MinecraftBlockDescriptor:
        """Factory for LargeAmethystBud"""
        return MinecraftBlockDescriptor("minecraft:large_amethyst_bud", True, {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def LargeFern(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for LargeFern"""
        return MinecraftBlockDescriptor("minecraft:large_fern", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def Lava(liquid_depth: LiquidDepth) -> MinecraftBlockDescriptor:
        """Factory for Lava"""
        return MinecraftBlockDescriptor("minecraft:lava", True, {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def LeafLitter(growth: Growth, minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for LeafLitter"""
        return MinecraftBlockDescriptor(
            "minecraft:leaf_litter", True,
            {_BlockStateKeys.Growth: growth, _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
        )

    @staticmethod
    def Lectern(minecraft_cardinal_direction: CardinalDirection, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for Lectern"""
        return MinecraftBlockDescriptor(
            "minecraft:lectern", True,
            {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction, _BlockStateKeys.PoweredBit: powered_bit},
        )

    @staticmethod
    def Lever(lever_direction: LeverDirection, open_bit: OpenBit) -> MinecraftBlockDescriptor:
        """Factory for Lever"""
        return MinecraftBlockDescriptor(
            "minecraft:lever", True, {_BlockStateKeys.LeverDirection: lever_direction, _BlockStateKeys.OpenBit: open_bit}
        )

    @staticmethod
    def LightBlock0() -> MinecraftBlockDescriptor:
        """Factory for LightBlock0"""
        return MinecraftBlockDescriptor("minecraft:light_block_0", True)

    @staticmethod
    def LightBlock1() -> MinecraftBlockDescriptor:
        """Factory for LightBlock1"""
        return MinecraftBlockDescriptor("minecraft:light_block_1", True)

    @staticmethod
    def LightBlock10() -> MinecraftBlockDescriptor:
        """Factory for LightBlock10"""
        return MinecraftBlockDescriptor("minecraft:light_block_10", True)

    @staticmethod
    def LightBlock11() -> MinecraftBlockDescriptor:
        """Factory for LightBlock11"""
        return MinecraftBlockDescriptor("minecraft:light_block_11", True)

    @staticmethod
    def LightBlock12() -> MinecraftBlockDescriptor:
        """Factory for LightBlock12"""
        return MinecraftBlockDescriptor("minecraft:light_block_12", True)

    @staticmethod
    def LightBlock13() -> MinecraftBlockDescriptor:
        """Factory for LightBlock13"""
        return MinecraftBlockDescriptor("minecraft:light_block_13", True)

    @staticmethod
    def LightBlock14() -> MinecraftBlockDescriptor:
        """Factory for LightBlock14"""
        return MinecraftBlockDescriptor("minecraft:light_block_14", True)

    @staticmethod
    def LightBlock15() -> MinecraftBlockDescriptor:
        """Factory for LightBlock15"""
        return MinecraftBlockDescriptor("minecraft:light_block_15", True)

    @staticmethod
    def LightBlock2() -> MinecraftBlockDescriptor:
        """Factory for LightBlock2"""
        return MinecraftBlockDescriptor("minecraft:light_block_2", True)

    @staticmethod
    def LightBlock3() -> MinecraftBlockDescriptor:
        """Factory for LightBlock3"""
        return MinecraftBlockDescriptor("minecraft:light_block_3", True)

    @staticmethod
    def LightBlock4() -> MinecraftBlockDescriptor:
        """Factory for LightBlock4"""
        return MinecraftBlockDescriptor("minecraft:light_block_4", True)

    @staticmethod
    def LightBlock5() -> MinecraftBlockDescriptor:
        """Factory for LightBlock5"""
        return MinecraftBlockDescriptor("minecraft:light_block_5", True)

    @staticmethod
    def LightBlock6() -> MinecraftBlockDescriptor:
        """Factory for LightBlock6"""
        return MinecraftBlockDescriptor("minecraft:light_block_6", True)

    @staticmethod
    def LightBlock7() -> MinecraftBlockDescriptor:
        """Factory for LightBlock7"""
        return MinecraftBlockDescriptor("minecraft:light_block_7", True)

    @staticmethod
    def LightBlock8() -> MinecraftBlockDescriptor:
        """Factory for LightBlock8"""
        return MinecraftBlockDescriptor("minecraft:light_block_8", True)

    @staticmethod
    def LightBlock9() -> MinecraftBlockDescriptor:
        """Factory for LightBlock9"""
        return MinecraftBlockDescriptor("minecraft:light_block_9", True)

    @staticmethod
    def LightBlueCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for LightBlueCandle"""
        return MinecraftBlockDescriptor("minecraft:light_blue_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def LightBlueCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for LightBlueCandleCake"""
        return MinecraftBlockDescriptor("minecraft:light_blue_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def LightBlueCarpet() -> MinecraftBlockDescriptor:
        """Factory for LightBlueCarpet"""
        return MinecraftBlockDescriptor("minecraft:light_blue_carpet", True)

    @staticmethod
    def LightBlueConcrete() -> MinecraftBlockDescriptor:
        """Factory for LightBlueConcrete"""
        return MinecraftBlockDescriptor("minecraft:light_blue_concrete", True)

    @staticmethod
    def LightBlueConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for LightBlueConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:light_blue_concrete_powder", True)

    @staticmethod
    def LightBlueGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for LightBlueGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:light_blue_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def LightBlueShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for LightBlueShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:light_blue_shulker_box", True)

    @staticmethod
    def LightBlueStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for LightBlueStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:light_blue_stained_glass", True)

    @staticmethod
    def LightBlueStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for LightBlueStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:light_blue_stained_glass_pane", True)

    @staticmethod
    def LightBlueTerracotta() -> MinecraftBlockDescriptor:
        """Factory for LightBlueTerracotta"""
        return MinecraftBlockDescriptor("minecraft:light_blue_terracotta", True)

    @staticmethod
    def LightBlueWool() -> MinecraftBlockDescriptor:
        """Factory for LightBlueWool"""
        return MinecraftBlockDescriptor("minecraft:light_blue_wool", True)

    @staticmethod
    def LightGrayCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for LightGrayCandle"""
        return MinecraftBlockDescriptor("minecraft:light_gray_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def LightGrayCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for LightGrayCandleCake"""
        return MinecraftBlockDescriptor("minecraft:light_gray_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def LightGrayCarpet() -> MinecraftBlockDescriptor:
        """Factory for LightGrayCarpet"""
        return MinecraftBlockDescriptor("minecraft:light_gray_carpet", True)

    @staticmethod
    def LightGrayConcrete() -> MinecraftBlockDescriptor:
        """Factory for LightGrayConcrete"""
        return MinecraftBlockDescriptor("minecraft:light_gray_concrete", True)

    @staticmethod
    def LightGrayConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for LightGrayConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:light_gray_concrete_powder", True)

    @staticmethod
    def LightGrayShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for LightGrayShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:light_gray_shulker_box", True)

    @staticmethod
    def LightGrayStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for LightGrayStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:light_gray_stained_glass", True)

    @staticmethod
    def LightGrayStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for LightGrayStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:light_gray_stained_glass_pane", True)

    @staticmethod
    def LightGrayTerracotta() -> MinecraftBlockDescriptor:
        """Factory for LightGrayTerracotta"""
        return MinecraftBlockDescriptor("minecraft:light_gray_terracotta", True)

    @staticmethod
    def LightGrayWool() -> MinecraftBlockDescriptor:
        """Factory for LightGrayWool"""
        return MinecraftBlockDescriptor("minecraft:light_gray_wool", True)

    @staticmethod
    def LightWeightedPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for LightWeightedPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:light_weighted_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def LightningRod(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for LightningRod"""
        return MinecraftBlockDescriptor("minecraft:lightning_rod", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Lilac(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for Lilac"""
        return MinecraftBlockDescriptor("minecraft:lilac", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def LilyOfTheValley() -> MinecraftBlockDescriptor:
        """Factory for LilyOfTheValley"""
        return MinecraftBlockDescriptor("minecraft:lily_of_the_valley", True)

    @staticmethod
    def LimeCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for LimeCandle"""
        return MinecraftBlockDescriptor("minecraft:lime_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def LimeCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for LimeCandleCake"""
        return MinecraftBlockDescriptor("minecraft:lime_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def LimeCarpet() -> MinecraftBlockDescriptor:
        """Factory for LimeCarpet"""
        return MinecraftBlockDescriptor("minecraft:lime_carpet", True)

    @staticmethod
    def LimeConcrete() -> MinecraftBlockDescriptor:
        """Factory for LimeConcrete"""
        return MinecraftBlockDescriptor("minecraft:lime_concrete", True)

    @staticmethod
    def LimeConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for LimeConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:lime_concrete_powder", True)

    @staticmethod
    def LimeGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for LimeGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:lime_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def LimeShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for LimeShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:lime_shulker_box", True)

    @staticmethod
    def LimeStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for LimeStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:lime_stained_glass", True)

    @staticmethod
    def LimeStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for LimeStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:lime_stained_glass_pane", True)

    @staticmethod
    def LimeTerracotta() -> MinecraftBlockDescriptor:
        """Factory for LimeTerracotta"""
        return MinecraftBlockDescriptor("minecraft:lime_terracotta", True)

    @staticmethod
    def LimeWool() -> MinecraftBlockDescriptor:
        """Factory for LimeWool"""
        return MinecraftBlockDescriptor("minecraft:lime_wool", True)

    @staticmethod
    def LitBlastFurnace(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for LitBlastFurnace"""
        return MinecraftBlockDescriptor(
            "minecraft:lit_blast_furnace", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def LitDeepslateRedstoneOre() -> MinecraftBlockDescriptor:
        """Factory for LitDeepslateRedstoneOre"""
        return MinecraftBlockDescriptor("minecraft:lit_deepslate_redstone_ore", True)

    @staticmethod
    def LitFurnace(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for LitFurnace"""
        return MinecraftBlockDescriptor(
            "minecraft:lit_furnace", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def LitPumpkin(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for LitPumpkin"""
        return MinecraftBlockDescriptor(
            "minecraft:lit_pumpkin", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def LitRedstoneLamp() -> MinecraftBlockDescriptor:
        """Factory for LitRedstoneLamp"""
        return MinecraftBlockDescriptor("minecraft:lit_redstone_lamp", True)

    @staticmethod
    def LitRedstoneOre() -> MinecraftBlockDescriptor:
        """Factory for LitRedstoneOre"""
        return MinecraftBlockDescriptor("minecraft:lit_redstone_ore", True)

    @staticmethod
    def LitSmoker(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for LitSmoker"""
        return MinecraftBlockDescriptor("minecraft:lit_smoker", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def Lodestone() -> MinecraftBlockDescriptor:
        """Factory for Lodestone"""
        return MinecraftBlockDescriptor("minecraft:lodestone", True)

    @staticmethod
    def Loom(direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for Loom"""
        return MinecraftBlockDescriptor("minecraft:loom", True, {_BlockStateKeys.Direction: direction})

    @staticmethod
    def MagentaCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for MagentaCandle"""
        return MinecraftBlockDescriptor("minecraft:magenta_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def MagentaCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for MagentaCandleCake"""
        return MinecraftBlockDescriptor("minecraft:magenta_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def MagentaCarpet() -> MinecraftBlockDescriptor:
        """Factory for MagentaCarpet"""
        return MinecraftBlockDescriptor("minecraft:magenta_carpet", True)

    @staticmethod
    def MagentaConcrete() -> MinecraftBlockDescriptor:
        """Factory for MagentaConcrete"""
        return MinecraftBlockDescriptor("minecraft:magenta_concrete", True)

    @staticmethod
    def MagentaConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for MagentaConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:magenta_concrete_powder", True)

    @staticmethod
    def MagentaGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for MagentaGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:magenta_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def MagentaShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for MagentaShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:magenta_shulker_box", True)

    @staticmethod
    def MagentaStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for MagentaStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:magenta_stained_glass", True)

    @staticmethod
    def MagentaStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for MagentaStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:magenta_stained_glass_pane", True)

    @staticmethod
    def MagentaTerracotta() -> MinecraftBlockDescriptor:
        """Factory for MagentaTerracotta"""
        return MinecraftBlockDescriptor("minecraft:magenta_terracotta", True)

    @staticmethod
    def MagentaWool() -> MinecraftBlockDescriptor:
        """Factory for MagentaWool"""
        return MinecraftBlockDescriptor("minecraft:magenta_wool", True)

    @staticmethod
    def Magma() -> MinecraftBlockDescriptor:
        """Factory for Magma"""
        return MinecraftBlockDescriptor("minecraft:magma", True)

    @staticmethod
    def MangroveButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for MangroveButton"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def MangroveDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for MangroveDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def MangroveDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MangroveDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:mangrove_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def MangroveFence() -> MinecraftBlockDescriptor:
        """Factory for MangroveFence"""
        return MinecraftBlockDescriptor("minecraft:mangrove_fence", True)

    @staticmethod
    def MangroveFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for MangroveFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def MangroveHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for MangroveHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def MangroveLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for MangroveLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def MangroveLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for MangroveLog"""
        return MinecraftBlockDescriptor("minecraft:mangrove_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def MangrovePlanks() -> MinecraftBlockDescriptor:
        """Factory for MangrovePlanks"""
        return MinecraftBlockDescriptor("minecraft:mangrove_planks", True)

    @staticmethod
    def MangrovePressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for MangrovePressurePlate"""
        return MinecraftBlockDescriptor("minecraft:mangrove_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def MangrovePropagule(hanging: Hanging, propagule_stage: PropaguleStage) -> MinecraftBlockDescriptor:
        """Factory for MangrovePropagule"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_propagule", True, {_BlockStateKeys.Hanging: hanging, _BlockStateKeys.PropaguleStage: propagule_stage}
        )

    @staticmethod
    def MangroveRoots() -> MinecraftBlockDescriptor:
        """Factory for MangroveRoots"""
        return MinecraftBlockDescriptor("minecraft:mangrove_roots", True)

    @staticmethod
    def MangroveSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MangroveSlab"""
        return MinecraftBlockDescriptor("minecraft:mangrove_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def MangroveStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for MangroveStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MangroveStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for MangroveStandingSign"""
        return MinecraftBlockDescriptor("minecraft:mangrove_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def MangroveTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for MangroveTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:mangrove_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def MangroveWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for MangroveWallSign"""
        return MinecraftBlockDescriptor("minecraft:mangrove_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def MangroveWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for MangroveWood"""
        return MinecraftBlockDescriptor("minecraft:mangrove_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def MaterialReducer(direction: Direction) -> MinecraftBlockDescriptor:
        """Factory for MaterialReducer"""
        return MinecraftBlockDescriptor("minecraft:material_reducer", True, {_BlockStateKeys.Direction: direction})

    @staticmethod
    def MediumAmethystBud(minecraft_block_face: BlockFace) -> MinecraftBlockDescriptor:
        """Factory for MediumAmethystBud"""
        return MinecraftBlockDescriptor("minecraft:medium_amethyst_bud", True, {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def MelonBlock() -> MinecraftBlockDescriptor:
        """Factory for MelonBlock"""
        return MinecraftBlockDescriptor("minecraft:melon_block", True)

    @staticmethod
    def MelonStem(facing_direction: FacingDirection, growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for MelonStem"""
        return MinecraftBlockDescriptor(
            "minecraft:melon_stem", True, {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.Growth: growth}
        )

    @staticmethod
    def MobSpawner() -> MinecraftBlockDescriptor:
        """Factory for MobSpawner"""
        return MinecraftBlockDescriptor("minecraft:mob_spawner", True)

    @staticmethod
    def MossBlock() -> MinecraftBlockDescriptor:
        """Factory for MossBlock"""
        return MinecraftBlockDescriptor("minecraft:moss_block", True)

    @staticmethod
    def MossCarpet() -> MinecraftBlockDescriptor:
        """Factory for MossCarpet"""
        return MinecraftBlockDescriptor("minecraft:moss_carpet", True)

    @staticmethod
    def MossyCobblestone() -> MinecraftBlockDescriptor:
        """Factory for MossyCobblestone"""
        return MinecraftBlockDescriptor("minecraft:mossy_cobblestone", True)

    @staticmethod
    def MossyCobblestoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MossyCobblestoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_cobblestone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyCobblestoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MossyCobblestoneSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_cobblestone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyCobblestoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for MossyCobblestoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_cobblestone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MossyCobblestoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for MossyCobblestoneWall"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_cobblestone_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def MossyStoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MossyStoneBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_stone_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyStoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MossyStoneBrickSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_stone_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyStoneBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for MossyStoneBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_stone_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MossyStoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for MossyStoneBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:mossy_stone_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def MossyStoneBricks() -> MinecraftBlockDescriptor:
        """Factory for MossyStoneBricks"""
        return MinecraftBlockDescriptor("minecraft:mossy_stone_bricks", True)

    @staticmethod
    def Mud() -> MinecraftBlockDescriptor:
        """Factory for Mud"""
        return MinecraftBlockDescriptor("minecraft:mud", True)

    @staticmethod
    def MudBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MudBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:mud_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MudBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for MudBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:mud_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def MudBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for MudBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:mud_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MudBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for MudBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:mud_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def MudBricks() -> MinecraftBlockDescriptor:
        """Factory for MudBricks"""
        return MinecraftBlockDescriptor("minecraft:mud_bricks", True)

    @staticmethod
    def MuddyMangroveRoots(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for MuddyMangroveRoots"""
        return MinecraftBlockDescriptor("minecraft:muddy_mangrove_roots", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def MushroomStem(huge_mushroom_bits: HugeMushroomBits) -> MinecraftBlockDescriptor:
        """Factory for MushroomStem"""
        return MinecraftBlockDescriptor("minecraft:mushroom_stem", True, {_BlockStateKeys.HugeMushroomBits: huge_mushroom_bits})

    @staticmethod
    def Mycelium() -> MinecraftBlockDescriptor:
        """Factory for Mycelium"""
        return MinecraftBlockDescriptor("minecraft:mycelium", True)

    @staticmethod
    def NetherBrick() -> MinecraftBlockDescriptor:
        """Factory for NetherBrick"""
        return MinecraftBlockDescriptor("minecraft:nether_brick", True)

    @staticmethod
    def NetherBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for NetherBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:nether_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def NetherBrickFence() -> MinecraftBlockDescriptor:
        """Factory for NetherBrickFence"""
        return MinecraftBlockDescriptor("minecraft:nether_brick_fence", True)

    @staticmethod
    def NetherBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for NetherBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:nether_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def NetherBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for NetherBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:nether_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def NetherBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for NetherBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:nether_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def NetherGoldOre() -> MinecraftBlockDescriptor:
        """Factory for NetherGoldOre"""
        return MinecraftBlockDescriptor("minecraft:nether_gold_ore", True)

    @staticmethod
    def NetherSprouts() -> MinecraftBlockDescriptor:
        """Factory for NetherSprouts"""
        return MinecraftBlockDescriptor("minecraft:nether_sprouts", True)

    @staticmethod
    def NetherWart(age: Age) -> MinecraftBlockDescriptor:
        """Factory for NetherWart"""
        return MinecraftBlockDescriptor("minecraft:nether_wart", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def NetherWartBlock() -> MinecraftBlockDescriptor:
        """Factory for NetherWartBlock"""
        return MinecraftBlockDescriptor("minecraft:nether_wart_block", True)

    @staticmethod
    def NetheriteBlock() -> MinecraftBlockDescriptor:
        """Factory for NetheriteBlock"""
        return MinecraftBlockDescriptor("minecraft:netherite_block", True)

    @staticmethod
    def Netherrack() -> MinecraftBlockDescriptor:
        """Factory for Netherrack"""
        return MinecraftBlockDescriptor("minecraft:netherrack", True)

    @staticmethod
    def NormalStoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for NormalStoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:normal_stone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def NormalStoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for NormalStoneSlab"""
        return MinecraftBlockDescriptor("minecraft:normal_stone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def NormalStoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for NormalStoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:normal_stone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def Noteblock() -> MinecraftBlockDescriptor:
        """Factory for Noteblock"""
        return MinecraftBlockDescriptor("minecraft:noteblock", True)

    @staticmethod
    def OakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for OakDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:oak_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def OakFence() -> MinecraftBlockDescriptor:
        """Factory for OakFence"""
        return MinecraftBlockDescriptor("minecraft:oak_fence", True)

    @staticmethod
    def OakHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for OakHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:oak_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def OakLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for OakLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:oak_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def OakLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for OakLog"""
        return MinecraftBlockDescriptor("minecraft:oak_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def OakPlanks() -> MinecraftBlockDescriptor:
        """Factory for OakPlanks"""
        return MinecraftBlockDescriptor("minecraft:oak_planks", True)

    @staticmethod
    def OakSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for OakSapling"""
        return MinecraftBlockDescriptor("minecraft:oak_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def OakSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for OakSlab"""
        return MinecraftBlockDescriptor("minecraft:oak_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def OakStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for OakStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:oak_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def OakWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for OakWood"""
        return MinecraftBlockDescriptor("minecraft:oak_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Observer(facing_direction: FacingDirection, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for Observer"""
        return MinecraftBlockDescriptor(
            "minecraft:observer", True,
            {_BlockStateKeys.MinecraftFacingDirection: facing_direction, _BlockStateKeys.PoweredBit: powered_bit},
        )

    @staticmethod
    def Obsidian() -> MinecraftBlockDescriptor:
        """Factory for Obsidian"""
        return MinecraftBlockDescriptor("minecraft:obsidian", True)

    @staticmethod
    def OchreFroglight(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for OchreFroglight"""
        return MinecraftBlockDescriptor("minecraft:ochre_froglight", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def OpenEyeblossom() -> MinecraftBlockDescriptor:
        """Factory for OpenEyeblossom"""
        return MinecraftBlockDescriptor("minecraft:open_eyeblossom", True)

    @staticmethod
    def OrangeCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for OrangeCandle"""
        return MinecraftBlockDescriptor("minecraft:orange_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def OrangeCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for OrangeCandleCake"""
        return MinecraftBlockDescriptor("minecraft:orange_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def OrangeCarpet() -> MinecraftBlockDescriptor:
        """Factory for OrangeCarpet"""
        return MinecraftBlockDescriptor("minecraft:orange_carpet", True)

    @staticmethod
    def OrangeConcrete() -> MinecraftBlockDescriptor:
        """Factory for OrangeConcrete"""
        return MinecraftBlockDescriptor("minecraft:orange_concrete", True)

    @staticmethod
    def OrangeConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for OrangeConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:orange_concrete_powder", True)

    @staticmethod
    def OrangeGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for OrangeGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:orange_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def OrangeShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for OrangeShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:orange_shulker_box", True)

    @staticmethod
    def OrangeStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for OrangeStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:orange_stained_glass", True)

    @staticmethod
    def OrangeStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for OrangeStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:orange_stained_glass_pane", True)

    @staticmethod
    def OrangeTerracotta() -> MinecraftBlockDescriptor:
        """Factory for OrangeTerracotta"""
        return MinecraftBlockDescriptor("minecraft:orange_terracotta", True)

    @staticmethod
    def OrangeTulip() -> MinecraftBlockDescriptor:
        """Factory for OrangeTulip"""
        return MinecraftBlockDescriptor("minecraft:orange_tulip", True)

    @staticmethod
    def OrangeWool() -> MinecraftBlockDescriptor:
        """Factory for OrangeWool"""
        return MinecraftBlockDescriptor("minecraft:orange_wool", True)

    @staticmethod
    def OxeyeDaisy() -> MinecraftBlockDescriptor:
        """Factory for OxeyeDaisy"""
        return MinecraftBlockDescriptor("minecraft:oxeye_daisy", True)

    @staticmethod
    def OxidizedChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for OxidizedChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:oxidized_chiseled_copper", True)

    @staticmethod
    def OxidizedCopper() -> MinecraftBlockDescriptor:
        """Factory for OxidizedCopper"""
        return MinecraftBlockDescriptor("minecraft:oxidized_copper", True)

    @staticmethod
    def OxidizedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for OxidizedCopperBulb"""
        return MinecraftBlockDescriptor(
            "minecraft:oxidized_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def OxidizedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for OxidizedCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:oxidized_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def OxidizedCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for OxidizedCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:oxidized_copper_grate", True)

    @staticmethod
    def OxidizedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for OxidizedCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:oxidized_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def OxidizedCutCopper() -> MinecraftBlockDescriptor:
        """Factory for OxidizedCutCopper"""
        return MinecraftBlockDescriptor("minecraft:oxidized_cut_copper", True)

    @staticmethod
    def OxidizedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for OxidizedCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:oxidized_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def OxidizedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for OxidizedCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:oxidized_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def OxidizedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for OxidizedDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:oxidized_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PackedIce() -> MinecraftBlockDescriptor:
        """Factory for PackedIce"""
        return MinecraftBlockDescriptor("minecraft:packed_ice", True)

    @staticmethod
    def PackedMud() -> MinecraftBlockDescriptor:
        """Factory for PackedMud"""
        return MinecraftBlockDescriptor("minecraft:packed_mud", True)

    @staticmethod
    def PaleHangingMoss(tip: Tip) -> MinecraftBlockDescriptor:
        """Factory for PaleHangingMoss"""
        return MinecraftBlockDescriptor("minecraft:pale_hanging_moss", True, {_BlockStateKeys.Tip: tip})

    @staticmethod
    def PaleMossBlock() -> MinecraftBlockDescriptor:
        """Factory for PaleMossBlock"""
        return MinecraftBlockDescriptor("minecraft:pale_moss_block", True)

    @staticmethod
    def PaleMossCarpet(
        pale_moss_carpet_side_east: PaleMossCarpetSideEast,
        pale_moss_carpet_side_north: PaleMossCarpetSideNorth,
        pale_moss_carpet_side_south: PaleMossCarpetSideSouth,
        pale_moss_carpet_side_west: PaleMossCarpetSideWest,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PaleMossCarpet"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_moss_carpet", True,
            {
                _BlockStateKeys.PaleMossCarpetSideEast: pale_moss_carpet_side_east,
                _BlockStateKeys.PaleMossCarpetSideNorth: pale_moss_carpet_side_north,
                _BlockStateKeys.PaleMossCarpetSideSouth: pale_moss_carpet_side_south,
                _BlockStateKeys.PaleMossCarpetSideWest: pale_moss_carpet_side_west,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def PaleOakButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PaleOakButton"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def PaleOakDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PaleOakDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def PaleOakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PaleOakDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PaleOakFence() -> MinecraftBlockDescriptor:
        """Factory for PaleOakFence"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_fence", True)

    @staticmethod
    def PaleOakFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for PaleOakFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def PaleOakHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for PaleOakHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def PaleOakLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for PaleOakLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def PaleOakLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for PaleOakLog"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PaleOakPlanks() -> MinecraftBlockDescriptor:
        """Factory for PaleOakPlanks"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_planks", True)

    @staticmethod
    def PaleOakPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for PaleOakPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def PaleOakSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for PaleOakSapling"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def PaleOakSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PaleOakSlab"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PaleOakStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PaleOakStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PaleOakStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for PaleOakStandingSign"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def PaleOakTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for PaleOakTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:pale_oak_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def PaleOakWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PaleOakWallSign"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PaleOakWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for PaleOakWood"""
        return MinecraftBlockDescriptor("minecraft:pale_oak_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PearlescentFroglight(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for PearlescentFroglight"""
        return MinecraftBlockDescriptor("minecraft:pearlescent_froglight", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Peony(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for Peony"""
        return MinecraftBlockDescriptor("minecraft:peony", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def PetrifiedOakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PetrifiedOakDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:petrified_oak_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PetrifiedOakSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PetrifiedOakSlab"""
        return MinecraftBlockDescriptor("minecraft:petrified_oak_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PiglinHead(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PiglinHead"""
        return MinecraftBlockDescriptor("minecraft:piglin_head", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PinkCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for PinkCandle"""
        return MinecraftBlockDescriptor("minecraft:pink_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def PinkCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for PinkCandleCake"""
        return MinecraftBlockDescriptor("minecraft:pink_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def PinkCarpet() -> MinecraftBlockDescriptor:
        """Factory for PinkCarpet"""
        return MinecraftBlockDescriptor("minecraft:pink_carpet", True)

    @staticmethod
    def PinkConcrete() -> MinecraftBlockDescriptor:
        """Factory for PinkConcrete"""
        return MinecraftBlockDescriptor("minecraft:pink_concrete", True)

    @staticmethod
    def PinkConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for PinkConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:pink_concrete_powder", True)

    @staticmethod
    def PinkGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PinkGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:pink_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PinkPetals(growth: Growth, minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for PinkPetals"""
        return MinecraftBlockDescriptor(
            "minecraft:pink_petals", True,
            {_BlockStateKeys.Growth: growth, _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
        )

    @staticmethod
    def PinkShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for PinkShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:pink_shulker_box", True)

    @staticmethod
    def PinkStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for PinkStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:pink_stained_glass", True)

    @staticmethod
    def PinkStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for PinkStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:pink_stained_glass_pane", True)

    @staticmethod
    def PinkTerracotta() -> MinecraftBlockDescriptor:
        """Factory for PinkTerracotta"""
        return MinecraftBlockDescriptor("minecraft:pink_terracotta", True)

    @staticmethod
    def PinkTulip() -> MinecraftBlockDescriptor:
        """Factory for PinkTulip"""
        return MinecraftBlockDescriptor("minecraft:pink_tulip", True)

    @staticmethod
    def PinkWool() -> MinecraftBlockDescriptor:
        """Factory for PinkWool"""
        return MinecraftBlockDescriptor("minecraft:pink_wool", True)

    @staticmethod
    def Piston(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for Piston"""
        return MinecraftBlockDescriptor("minecraft:piston", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PistonArmCollision(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PistonArmCollision"""
        return MinecraftBlockDescriptor("minecraft:piston_arm_collision", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PitcherCrop(growth: Growth, upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for PitcherCrop"""
        return MinecraftBlockDescriptor(
            "minecraft:pitcher_crop", True, {_BlockStateKeys.Growth: growth, _BlockStateKeys.UpperBlockBit: upper_block_bit}
        )

    @staticmethod
    def PitcherPlant(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for PitcherPlant"""
        return MinecraftBlockDescriptor("minecraft:pitcher_plant", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def PlayerHead(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PlayerHead"""
        return MinecraftBlockDescriptor("minecraft:player_head", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Podzol() -> MinecraftBlockDescriptor:
        """Factory for Podzol"""
        return MinecraftBlockDescriptor("minecraft:podzol", True)

    @staticmethod
    def PointedDripstone(dripstone_thickness: DripstoneThickness, hanging: Hanging) -> MinecraftBlockDescriptor:
        """Factory for PointedDripstone"""
        return MinecraftBlockDescriptor(
            "minecraft:pointed_dripstone", True,
            {_BlockStateKeys.DripstoneThickness: dripstone_thickness, _BlockStateKeys.Hanging: hanging},
        )

    @staticmethod
    def PolishedAndesite() -> MinecraftBlockDescriptor:
        """Factory for PolishedAndesite"""
        return MinecraftBlockDescriptor("minecraft:polished_andesite", True)

    @staticmethod
    def PolishedAndesiteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedAndesiteDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_andesite_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedAndesiteSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedAndesiteSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_andesite_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedAndesiteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedAndesiteStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_andesite_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedBasalt(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for PolishedBasalt"""
        return MinecraftBlockDescriptor("minecraft:polished_basalt", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PolishedBlackstone() -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstone"""
        return MinecraftBlockDescriptor("minecraft:polished_blackstone", True)

    @staticmethod
    def PolishedBlackstoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneBrickSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstoneBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedBlackstoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def PolishedBlackstoneBricks() -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneBricks"""
        return MinecraftBlockDescriptor("minecraft:polished_blackstone_bricks", True)

    @staticmethod
    def PolishedBlackstoneButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneButton"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def PolishedBlackstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstonePressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstonePressurePlate"""
        return MinecraftBlockDescriptor("minecraft:polished_blackstone_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def PolishedBlackstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedBlackstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PolishedBlackstoneWall"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_blackstone_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def PolishedDeepslate() -> MinecraftBlockDescriptor:
        """Factory for PolishedDeepslate"""
        return MinecraftBlockDescriptor("minecraft:polished_deepslate", True)

    @staticmethod
    def PolishedDeepslateDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedDeepslateDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_deepslate_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDeepslateSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedDeepslateSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_deepslate_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDeepslateStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedDeepslateStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_deepslate_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedDeepslateWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PolishedDeepslateWall"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_deepslate_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def PolishedDiorite() -> MinecraftBlockDescriptor:
        """Factory for PolishedDiorite"""
        return MinecraftBlockDescriptor("minecraft:polished_diorite", True)

    @staticmethod
    def PolishedDioriteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedDioriteDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_diorite_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDioriteSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedDioriteSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_diorite_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDioriteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedDioriteStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_diorite_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedGranite() -> MinecraftBlockDescriptor:
        """Factory for PolishedGranite"""
        return MinecraftBlockDescriptor("minecraft:polished_granite", True)

    @staticmethod
    def PolishedGraniteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedGraniteDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_granite_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedGraniteSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedGraniteSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_granite_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedGraniteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedGraniteStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_granite_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedTuff() -> MinecraftBlockDescriptor:
        """Factory for PolishedTuff"""
        return MinecraftBlockDescriptor("minecraft:polished_tuff", True)

    @staticmethod
    def PolishedTuffDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedTuffDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_tuff_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedTuffSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PolishedTuffSlab"""
        return MinecraftBlockDescriptor("minecraft:polished_tuff_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PolishedTuffStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PolishedTuffStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_tuff_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedTuffWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PolishedTuffWall"""
        return MinecraftBlockDescriptor(
            "minecraft:polished_tuff_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Poppy() -> MinecraftBlockDescriptor:
        """Factory for Poppy"""
        return MinecraftBlockDescriptor("minecraft:poppy", True)

    @staticmethod
    def Portal(portal_axis: PortalAxis) -> MinecraftBlockDescriptor:
        """Factory for Portal"""
        return MinecraftBlockDescriptor("minecraft:portal", True, {_BlockStateKeys.PortalAxis: portal_axis})

    @staticmethod
    def Potatoes(growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for Potatoes"""
        return MinecraftBlockDescriptor("minecraft:potatoes", True, {_BlockStateKeys.Growth: growth})

    @staticmethod
    def PowderSnow() -> MinecraftBlockDescriptor:
        """Factory for PowderSnow"""
        return MinecraftBlockDescriptor("minecraft:powder_snow", True)

    @staticmethod
    def PoweredComparator(
        minecraft_cardinal_direction: CardinalDirection, output_lit_bit: OutputLitBit, output_subtract_bit: OutputSubtractBit
    ) -> MinecraftBlockDescriptor:
        """Factory for PoweredComparator"""
        return MinecraftBlockDescriptor(
            "minecraft:powered_comparator", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OutputLitBit: output_lit_bit,
                _BlockStateKeys.OutputSubtractBit: output_subtract_bit,
            },
        )

    @staticmethod
    def PoweredRepeater(minecraft_cardinal_direction: CardinalDirection, repeater_delay: RepeaterDelay) -> MinecraftBlockDescriptor:
        """Factory for PoweredRepeater"""
        return MinecraftBlockDescriptor(
            "minecraft:powered_repeater", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.RepeaterDelay: repeater_delay,
            },
        )

    @staticmethod
    def Prismarine() -> MinecraftBlockDescriptor:
        """Factory for Prismarine"""
        return MinecraftBlockDescriptor("minecraft:prismarine", True)

    @staticmethod
    def PrismarineBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PrismarineBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:prismarine_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PrismarineBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PrismarineBrickSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:prismarine_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PrismarineBricks() -> MinecraftBlockDescriptor:
        """Factory for PrismarineBricks"""
        return MinecraftBlockDescriptor("minecraft:prismarine_bricks", True)

    @staticmethod
    def PrismarineBricksStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PrismarineBricksStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:prismarine_bricks_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PrismarineDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PrismarineDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:prismarine_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PrismarineSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PrismarineSlab"""
        return MinecraftBlockDescriptor("minecraft:prismarine_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PrismarineStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PrismarineStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:prismarine_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PrismarineWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for PrismarineWall"""
        return MinecraftBlockDescriptor(
            "minecraft:prismarine_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Pumpkin(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Pumpkin"""
        return MinecraftBlockDescriptor("minecraft:pumpkin", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def PumpkinStem(facing_direction: FacingDirection, growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for PumpkinStem"""
        return MinecraftBlockDescriptor(
            "minecraft:pumpkin_stem", True, {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.Growth: growth}
        )

    @staticmethod
    def PurpleCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for PurpleCandle"""
        return MinecraftBlockDescriptor("minecraft:purple_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def PurpleCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for PurpleCandleCake"""
        return MinecraftBlockDescriptor("minecraft:purple_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def PurpleCarpet() -> MinecraftBlockDescriptor:
        """Factory for PurpleCarpet"""
        return MinecraftBlockDescriptor("minecraft:purple_carpet", True)

    @staticmethod
    def PurpleConcrete() -> MinecraftBlockDescriptor:
        """Factory for PurpleConcrete"""
        return MinecraftBlockDescriptor("minecraft:purple_concrete", True)

    @staticmethod
    def PurpleConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for PurpleConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:purple_concrete_powder", True)

    @staticmethod
    def PurpleGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for PurpleGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:purple_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PurpleShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for PurpleShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:purple_shulker_box", True)

    @staticmethod
    def PurpleStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for PurpleStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:purple_stained_glass", True)

    @staticmethod
    def PurpleStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for PurpleStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:purple_stained_glass_pane", True)

    @staticmethod
    def PurpleTerracotta() -> MinecraftBlockDescriptor:
        """Factory for PurpleTerracotta"""
        return MinecraftBlockDescriptor("minecraft:purple_terracotta", True)

    @staticmethod
    def PurpleWool() -> MinecraftBlockDescriptor:
        """Factory for PurpleWool"""
        return MinecraftBlockDescriptor("minecraft:purple_wool", True)

    @staticmethod
    def PurpurBlock(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for PurpurBlock"""
        return MinecraftBlockDescriptor("minecraft:purpur_block", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PurpurDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PurpurDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:purpur_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PurpurPillar(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for PurpurPillar"""
        return MinecraftBlockDescriptor("minecraft:purpur_pillar", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PurpurSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for PurpurSlab"""
        return MinecraftBlockDescriptor("minecraft:purpur_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PurpurStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for PurpurStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:purpur_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def QuartzBlock(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for QuartzBlock"""
        return MinecraftBlockDescriptor("minecraft:quartz_block", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def QuartzBricks() -> MinecraftBlockDescriptor:
        """Factory for QuartzBricks"""
        return MinecraftBlockDescriptor("minecraft:quartz_bricks", True)

    @staticmethod
    def QuartzDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for QuartzDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:quartz_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def QuartzOre() -> MinecraftBlockDescriptor:
        """Factory for QuartzOre"""
        return MinecraftBlockDescriptor("minecraft:quartz_ore", True)

    @staticmethod
    def QuartzPillar(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for QuartzPillar"""
        return MinecraftBlockDescriptor("minecraft:quartz_pillar", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def QuartzSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for QuartzSlab"""
        return MinecraftBlockDescriptor("minecraft:quartz_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def QuartzStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for QuartzStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:quartz_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def Rail(rail_direction: RailDirection) -> MinecraftBlockDescriptor:
        """Factory for Rail"""
        return MinecraftBlockDescriptor("minecraft:rail", True, {_BlockStateKeys.RailDirection: rail_direction})

    @staticmethod
    def RawCopperBlock() -> MinecraftBlockDescriptor:
        """Factory for RawCopperBlock"""
        return MinecraftBlockDescriptor("minecraft:raw_copper_block", True)

    @staticmethod
    def RawGoldBlock() -> MinecraftBlockDescriptor:
        """Factory for RawGoldBlock"""
        return MinecraftBlockDescriptor("minecraft:raw_gold_block", True)

    @staticmethod
    def RawIronBlock() -> MinecraftBlockDescriptor:
        """Factory for RawIronBlock"""
        return MinecraftBlockDescriptor("minecraft:raw_iron_block", True)

    @staticmethod
    def RedCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for RedCandle"""
        return MinecraftBlockDescriptor("minecraft:red_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def RedCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for RedCandleCake"""
        return MinecraftBlockDescriptor("minecraft:red_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def RedCarpet() -> MinecraftBlockDescriptor:
        """Factory for RedCarpet"""
        return MinecraftBlockDescriptor("minecraft:red_carpet", True)

    @staticmethod
    def RedConcrete() -> MinecraftBlockDescriptor:
        """Factory for RedConcrete"""
        return MinecraftBlockDescriptor("minecraft:red_concrete", True)

    @staticmethod
    def RedConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for RedConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:red_concrete_powder", True)

    @staticmethod
    def RedGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for RedGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:red_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def RedMushroom() -> MinecraftBlockDescriptor:
        """Factory for RedMushroom"""
        return MinecraftBlockDescriptor("minecraft:red_mushroom", True)

    @staticmethod
    def RedMushroomBlock(huge_mushroom_bits: HugeMushroomBits) -> MinecraftBlockDescriptor:
        """Factory for RedMushroomBlock"""
        return MinecraftBlockDescriptor("minecraft:red_mushroom_block", True, {_BlockStateKeys.HugeMushroomBits: huge_mushroom_bits})

    @staticmethod
    def RedNetherBrick() -> MinecraftBlockDescriptor:
        """Factory for RedNetherBrick"""
        return MinecraftBlockDescriptor("minecraft:red_nether_brick", True)

    @staticmethod
    def RedNetherBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for RedNetherBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:red_nether_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def RedNetherBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for RedNetherBrickSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:red_nether_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def RedNetherBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for RedNetherBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:red_nether_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def RedNetherBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for RedNetherBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:red_nether_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def RedSand() -> MinecraftBlockDescriptor:
        """Factory for RedSand"""
        return MinecraftBlockDescriptor("minecraft:red_sand", True)

    @staticmethod
    def RedSandstone() -> MinecraftBlockDescriptor:
        """Factory for RedSandstone"""
        return MinecraftBlockDescriptor("minecraft:red_sandstone", True)

    @staticmethod
    def RedSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for RedSandstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:red_sandstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def RedSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for RedSandstoneSlab"""
        return MinecraftBlockDescriptor("minecraft:red_sandstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def RedSandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for RedSandstoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:red_sandstone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def RedSandstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for RedSandstoneWall"""
        return MinecraftBlockDescriptor(
            "minecraft:red_sandstone_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def RedShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for RedShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:red_shulker_box", True)

    @staticmethod
    def RedStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for RedStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:red_stained_glass", True)

    @staticmethod
    def RedStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for RedStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:red_stained_glass_pane", True)

    @staticmethod
    def RedTerracotta() -> MinecraftBlockDescriptor:
        """Factory for RedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:red_terracotta", True)

    @staticmethod
    def RedTulip() -> MinecraftBlockDescriptor:
        """Factory for RedTulip"""
        return MinecraftBlockDescriptor("minecraft:red_tulip", True)

    @staticmethod
    def RedWool() -> MinecraftBlockDescriptor:
        """Factory for RedWool"""
        return MinecraftBlockDescriptor("minecraft:red_wool", True)

    @staticmethod
    def RedstoneBlock() -> MinecraftBlockDescriptor:
        """Factory for RedstoneBlock"""
        return MinecraftBlockDescriptor("minecraft:redstone_block", True)

    @staticmethod
    def RedstoneLamp() -> MinecraftBlockDescriptor:
        """Factory for RedstoneLamp"""
        return MinecraftBlockDescriptor("minecraft:redstone_lamp", True)

    @staticmethod
    def RedstoneOre() -> MinecraftBlockDescriptor:
        """Factory for RedstoneOre"""
        return MinecraftBlockDescriptor("minecraft:redstone_ore", True)

    @staticmethod
    def RedstoneTorch(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for RedstoneTorch"""
        return MinecraftBlockDescriptor("minecraft:redstone_torch", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def RedstoneWire(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for RedstoneWire"""
        return MinecraftBlockDescriptor("minecraft:redstone_wire", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def Reeds(age: Age) -> MinecraftBlockDescriptor:
        """Factory for Reeds"""
        return MinecraftBlockDescriptor("minecraft:reeds", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def ReinforcedDeepslate() -> MinecraftBlockDescriptor:
        """Factory for ReinforcedDeepslate"""
        return MinecraftBlockDescriptor("minecraft:reinforced_deepslate", True)

    @staticmethod
    def RepeatingCommandBlock(conditional_bit: ConditionalBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for RepeatingCommandBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:repeating_command_block", True,
            {_BlockStateKeys.ConditionalBit: conditional_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def ResinBlock() -> MinecraftBlockDescriptor:
        """Factory for ResinBlock"""
        return MinecraftBlockDescriptor("minecraft:resin_block", True)

    @staticmethod
    def ResinBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for ResinBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:resin_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def ResinBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for ResinBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:resin_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def ResinBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for ResinBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:resin_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def ResinBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for ResinBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:resin_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def ResinBricks() -> MinecraftBlockDescriptor:
        """Factory for ResinBricks"""
        return MinecraftBlockDescriptor("minecraft:resin_bricks", True)

    @staticmethod
    def ResinClump(multi_face_direction_bits: MultiFaceDirectionBits) -> MinecraftBlockDescriptor:
        """Factory for ResinClump"""
        return MinecraftBlockDescriptor("minecraft:resin_clump", True, {_BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits})

    @staticmethod
    def RespawnAnchor(respawn_anchor_charge: RespawnAnchorCharge) -> MinecraftBlockDescriptor:
        """Factory for RespawnAnchor"""
        return MinecraftBlockDescriptor("minecraft:respawn_anchor", True, {_BlockStateKeys.RespawnAnchorCharge: respawn_anchor_charge})

    @staticmethod
    def RoseBush(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for RoseBush"""
        return MinecraftBlockDescriptor("minecraft:rose_bush", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def Sand() -> MinecraftBlockDescriptor:
        """Factory for Sand"""
        return MinecraftBlockDescriptor("minecraft:sand", True)

    @staticmethod
    def Sandstone() -> MinecraftBlockDescriptor:
        """Factory for Sandstone"""
        return MinecraftBlockDescriptor("minecraft:sandstone", True)

    @staticmethod
    def SandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SandstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:sandstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SandstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SandstoneSlab"""
        return MinecraftBlockDescriptor("minecraft:sandstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for SandstoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:sandstone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SandstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for SandstoneWall"""
        return MinecraftBlockDescriptor(
            "minecraft:sandstone_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Scaffolding(stability: Stability, stability_check: StabilityCheck) -> MinecraftBlockDescriptor:
        """Factory for Scaffolding"""
        return MinecraftBlockDescriptor(
            "minecraft:scaffolding", True, {_BlockStateKeys.Stability: stability, _BlockStateKeys.StabilityCheck: stability_check}
        )

    @staticmethod
    def Sculk() -> MinecraftBlockDescriptor:
        """Factory for Sculk"""
        return MinecraftBlockDescriptor("minecraft:sculk", True)

    @staticmethod
    def SculkCatalyst(bloom: Bloom) -> MinecraftBlockDescriptor:
        """Factory for SculkCatalyst"""
        return MinecraftBlockDescriptor("minecraft:sculk_catalyst", True, {_BlockStateKeys.Bloom: bloom})

    @staticmethod
    def SculkSensor(sculk_sensor_phase: SculkSensorPhase) -> MinecraftBlockDescriptor:
        """Factory for SculkSensor"""
        return MinecraftBlockDescriptor("minecraft:sculk_sensor", True, {_BlockStateKeys.SculkSensorPhase: sculk_sensor_phase})

    @staticmethod
    def SculkShrieker(active: Active, can_summon: CanSummon) -> MinecraftBlockDescriptor:
        """Factory for SculkShrieker"""
        return MinecraftBlockDescriptor(
            "minecraft:sculk_shrieker", True, {_BlockStateKeys.Active: active, _BlockStateKeys.CanSummon: can_summon}
        )

    @staticmethod
    def SculkVein(multi_face_direction_bits: MultiFaceDirectionBits) -> MinecraftBlockDescriptor:
        """Factory for SculkVein"""
        return MinecraftBlockDescriptor("minecraft:sculk_vein", True, {_BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits})

    @staticmethod
    def SeaLantern() -> MinecraftBlockDescriptor:
        """Factory for SeaLantern"""
        return MinecraftBlockDescriptor("minecraft:sea_lantern", True)

    @staticmethod
    def SeaPickle(cluster_count: ClusterCount, dead_bit: DeadBit) -> MinecraftBlockDescriptor:
        """Factory for SeaPickle"""
        return MinecraftBlockDescriptor(
            "minecraft:sea_pickle", True, {_BlockStateKeys.ClusterCount: cluster_count, _BlockStateKeys.DeadBit: dead_bit}
        )

    @staticmethod
    def Seagrass(sea_grass_type: SeaGrassType) -> MinecraftBlockDescriptor:
        """Factory for Seagrass"""
        return MinecraftBlockDescriptor("minecraft:seagrass", True, {_BlockStateKeys.SeaGrassType: sea_grass_type})

    @staticmethod
    def ShortDryGrass() -> MinecraftBlockDescriptor:
        """Factory for ShortDryGrass"""
        return MinecraftBlockDescriptor("minecraft:short_dry_grass", True)

    @staticmethod
    def ShortGrass() -> MinecraftBlockDescriptor:
        """Factory for ShortGrass"""
        return MinecraftBlockDescriptor("minecraft:short_grass", True)

    @staticmethod
    def Shroomlight() -> MinecraftBlockDescriptor:
        """Factory for Shroomlight"""
        return MinecraftBlockDescriptor("minecraft:shroomlight", True)

    @staticmethod
    def SilverGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for SilverGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:silver_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def SkeletonSkull(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for SkeletonSkull"""
        return MinecraftBlockDescriptor("minecraft:skeleton_skull", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Slime() -> MinecraftBlockDescriptor:
        """Factory for Slime"""
        return MinecraftBlockDescriptor("minecraft:slime", True)

    @staticmethod
    def SmallAmethystBud(minecraft_block_face: BlockFace) -> MinecraftBlockDescriptor:
        """Factory for SmallAmethystBud"""
        return MinecraftBlockDescriptor("minecraft:small_amethyst_bud", True, {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def SmallDripleafBlock(minecraft_cardinal_direction: CardinalDirection, upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for SmallDripleafBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:small_dripleaf_block", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def SmithingTable() -> MinecraftBlockDescriptor:
        """Factory for SmithingTable"""
        return MinecraftBlockDescriptor("minecraft:smithing_table", True)

    @staticmethod
    def Smoker(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Smoker"""
        return MinecraftBlockDescriptor("minecraft:smoker", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def SmoothBasalt() -> MinecraftBlockDescriptor:
        """Factory for SmoothBasalt"""
        return MinecraftBlockDescriptor("minecraft:smooth_basalt", True)

    @staticmethod
    def SmoothQuartz(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for SmoothQuartz"""
        return MinecraftBlockDescriptor("minecraft:smooth_quartz", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def SmoothQuartzDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothQuartzDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_quartz_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothQuartzSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothQuartzSlab"""
        return MinecraftBlockDescriptor("minecraft:smooth_quartz_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SmoothQuartzStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for SmoothQuartzStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_quartz_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SmoothRedSandstone() -> MinecraftBlockDescriptor:
        """Factory for SmoothRedSandstone"""
        return MinecraftBlockDescriptor("minecraft:smooth_red_sandstone", True)

    @staticmethod
    def SmoothRedSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothRedSandstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_red_sandstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothRedSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothRedSandstoneSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_red_sandstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothRedSandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for SmoothRedSandstoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_red_sandstone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SmoothSandstone() -> MinecraftBlockDescriptor:
        """Factory for SmoothSandstone"""
        return MinecraftBlockDescriptor("minecraft:smooth_sandstone", True)

    @staticmethod
    def SmoothSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothSandstoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_sandstone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothSandstoneSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_sandstone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothSandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for SmoothSandstoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_sandstone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SmoothStone() -> MinecraftBlockDescriptor:
        """Factory for SmoothStone"""
        return MinecraftBlockDescriptor("minecraft:smooth_stone", True)

    @staticmethod
    def SmoothStoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothStoneDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:smooth_stone_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothStoneSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SmoothStoneSlab"""
        return MinecraftBlockDescriptor("minecraft:smooth_stone_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SnifferEgg(cracked_state: CrackedState) -> MinecraftBlockDescriptor:
        """Factory for SnifferEgg"""
        return MinecraftBlockDescriptor("minecraft:sniffer_egg", True, {_BlockStateKeys.CrackedState: cracked_state})

    @staticmethod
    def Snow() -> MinecraftBlockDescriptor:
        """Factory for Snow"""
        return MinecraftBlockDescriptor("minecraft:snow", True)

    @staticmethod
    def SnowLayer(covered_bit: CoveredBit, height: Height) -> MinecraftBlockDescriptor:
        """Factory for SnowLayer"""
        return MinecraftBlockDescriptor("minecraft:snow_layer", True, {_BlockStateKeys.CoveredBit: covered_bit, _BlockStateKeys.Height: height})

    @staticmethod
    def SoulCampfire(extinguished: Extinguished, minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for SoulCampfire"""
        return MinecraftBlockDescriptor(
            "minecraft:soul_campfire", True,
            {
                _BlockStateKeys.Extinguished: extinguished,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def SoulFire(age: Age) -> MinecraftBlockDescriptor:
        """Factory for SoulFire"""
        return MinecraftBlockDescriptor("minecraft:soul_fire", True, {_BlockStateKeys.Age: age})

    @staticmethod
    def SoulLantern(hanging: Hanging) -> MinecraftBlockDescriptor:
        """Factory for SoulLantern"""
        return MinecraftBlockDescriptor("minecraft:soul_lantern", True, {_BlockStateKeys.Hanging: hanging})

    @staticmethod
    def SoulSand() -> MinecraftBlockDescriptor:
        """Factory for SoulSand"""
        return MinecraftBlockDescriptor("minecraft:soul_sand", True)

    @staticmethod
    def SoulSoil() -> MinecraftBlockDescriptor:
        """Factory for SoulSoil"""
        return MinecraftBlockDescriptor("minecraft:soul_soil", True)

    @staticmethod
    def SoulTorch(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for SoulTorch"""
        return MinecraftBlockDescriptor("minecraft:soul_torch", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def Sponge() -> MinecraftBlockDescriptor:
        """Factory for Sponge"""
        return MinecraftBlockDescriptor("minecraft:sponge", True)

    @staticmethod
    def SporeBlossom() -> MinecraftBlockDescriptor:
        """Factory for SporeBlossom"""
        return MinecraftBlockDescriptor("minecraft:spore_blossom", True)

    @staticmethod
    def SpruceButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for SpruceButton"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def SpruceDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for SpruceDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def SpruceDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SpruceDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:spruce_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SpruceFence() -> MinecraftBlockDescriptor:
        """Factory for SpruceFence"""
        return MinecraftBlockDescriptor("minecraft:spruce_fence", True)

    @staticmethod
    def SpruceFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for SpruceFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def SpruceHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for SpruceHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def SpruceLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> MinecraftBlockDescriptor:
        """Factory for SpruceLeaves"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_leaves", True, {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def SpruceLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for SpruceLog"""
        return MinecraftBlockDescriptor("minecraft:spruce_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def SprucePlanks() -> MinecraftBlockDescriptor:
        """Factory for SprucePlanks"""
        return MinecraftBlockDescriptor("minecraft:spruce_planks", True)

    @staticmethod
    def SprucePressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for SprucePressurePlate"""
        return MinecraftBlockDescriptor("minecraft:spruce_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def SpruceSapling(age_bit: AgeBit) -> MinecraftBlockDescriptor:
        """Factory for SpruceSapling"""
        return MinecraftBlockDescriptor("minecraft:spruce_sapling", True, {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def SpruceSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for SpruceSlab"""
        return MinecraftBlockDescriptor("minecraft:spruce_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SpruceStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for SpruceStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SpruceStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for SpruceStandingSign"""
        return MinecraftBlockDescriptor("minecraft:spruce_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def SpruceTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for SpruceTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:spruce_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def SpruceWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for SpruceWallSign"""
        return MinecraftBlockDescriptor("minecraft:spruce_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def SpruceWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for SpruceWood"""
        return MinecraftBlockDescriptor("minecraft:spruce_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StandingBanner(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for StandingBanner"""
        return MinecraftBlockDescriptor("minecraft:standing_banner", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def StandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for StandingSign"""
        return MinecraftBlockDescriptor("minecraft:standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def StickyPiston(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for StickyPiston"""
        return MinecraftBlockDescriptor("minecraft:sticky_piston", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def StickyPistonArmCollision(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for StickyPistonArmCollision"""
        return MinecraftBlockDescriptor("minecraft:sticky_piston_arm_collision", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Stone() -> MinecraftBlockDescriptor:
        """Factory for Stone"""
        return MinecraftBlockDescriptor("minecraft:stone", True)

    @staticmethod
    def StoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for StoneBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:stone_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def StoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for StoneBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:stone_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def StoneBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for StoneBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:stone_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def StoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for StoneBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:stone_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def StoneBricks() -> MinecraftBlockDescriptor:
        """Factory for StoneBricks"""
        return MinecraftBlockDescriptor("minecraft:stone_bricks", True)

    @staticmethod
    def StoneButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for StoneButton"""
        return MinecraftBlockDescriptor(
            "minecraft:stone_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def StonePressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for StonePressurePlate"""
        return MinecraftBlockDescriptor("minecraft:stone_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def StoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for StoneStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:stone_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def StonecutterBlock(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for StonecutterBlock"""
        return MinecraftBlockDescriptor(
            "minecraft:stonecutter_block", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def StrippedAcaciaLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedAcaciaLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_acacia_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedAcaciaWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedAcaciaWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_acacia_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedBambooBlock(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedBambooBlock"""
        return MinecraftBlockDescriptor("minecraft:stripped_bamboo_block", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedBirchLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedBirchLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_birch_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedBirchWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedBirchWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_birch_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCherryLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedCherryLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_cherry_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCherryWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedCherryWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_cherry_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCrimsonHyphae(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedCrimsonHyphae"""
        return MinecraftBlockDescriptor("minecraft:stripped_crimson_hyphae", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCrimsonStem(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedCrimsonStem"""
        return MinecraftBlockDescriptor("minecraft:stripped_crimson_stem", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedDarkOakLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedDarkOakLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_dark_oak_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedDarkOakWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedDarkOakWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_dark_oak_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedJungleLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedJungleLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_jungle_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedJungleWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedJungleWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_jungle_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedMangroveLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedMangroveLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_mangrove_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedMangroveWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedMangroveWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_mangrove_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedOakLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedOakLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_oak_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedOakWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedOakWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_oak_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedPaleOakLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedPaleOakLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_pale_oak_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedPaleOakWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedPaleOakWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_pale_oak_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedSpruceLog(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedSpruceLog"""
        return MinecraftBlockDescriptor("minecraft:stripped_spruce_log", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedSpruceWood(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedSpruceWood"""
        return MinecraftBlockDescriptor("minecraft:stripped_spruce_wood", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedWarpedHyphae(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedWarpedHyphae"""
        return MinecraftBlockDescriptor("minecraft:stripped_warped_hyphae", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedWarpedStem(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for StrippedWarpedStem"""
        return MinecraftBlockDescriptor("minecraft:stripped_warped_stem", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StructureBlock(structure_block_type: StructureBlockType) -> MinecraftBlockDescriptor:
        """Factory for StructureBlock"""
        return MinecraftBlockDescriptor("minecraft:structure_block", True, {_BlockStateKeys.StructureBlockType: structure_block_type})

    @staticmethod
    def StructureVoid() -> MinecraftBlockDescriptor:
        """Factory for StructureVoid"""
        return MinecraftBlockDescriptor("minecraft:structure_void", True)

    @staticmethod
    def Sunflower(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for Sunflower"""
        return MinecraftBlockDescriptor("minecraft:sunflower", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def SuspiciousGravel(brushed_progress: BrushedProgress, hanging: Hanging) -> MinecraftBlockDescriptor:
        """Factory for SuspiciousGravel"""
        return MinecraftBlockDescriptor(
            "minecraft:suspicious_gravel", True, {_BlockStateKeys.BrushedProgress: brushed_progress, _BlockStateKeys.Hanging: hanging}
        )

    @staticmethod
    def SuspiciousSand(brushed_progress: BrushedProgress, hanging: Hanging) -> MinecraftBlockDescriptor:
        """Factory for SuspiciousSand"""
        return MinecraftBlockDescriptor(
            "minecraft:suspicious_sand", True, {_BlockStateKeys.BrushedProgress: brushed_progress, _BlockStateKeys.Hanging: hanging}
        )

    @staticmethod
    def SweetBerryBush(growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for SweetBerryBush"""
        return MinecraftBlockDescriptor("minecraft:sweet_berry_bush", True, {_BlockStateKeys.Growth: growth})

    @staticmethod
    def TallDryGrass() -> MinecraftBlockDescriptor:
        """Factory for TallDryGrass"""
        return MinecraftBlockDescriptor("minecraft:tall_dry_grass", True)

    @staticmethod
    def TallGrass(upper_block_bit: UpperBlockBit) -> MinecraftBlockDescriptor:
        """Factory for TallGrass"""
        return MinecraftBlockDescriptor("minecraft:tall_grass", True, {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def Target() -> MinecraftBlockDescriptor:
        """Factory for Target"""
        return MinecraftBlockDescriptor("minecraft:target", True)

    @staticmethod
    def TintedGlass() -> MinecraftBlockDescriptor:
        """Factory for TintedGlass"""
        return MinecraftBlockDescriptor("minecraft:tinted_glass", True)

    @staticmethod
    def Tnt(explode_bit: ExplodeBit) -> MinecraftBlockDescriptor:
        """Factory for Tnt"""
        return MinecraftBlockDescriptor("minecraft:tnt", True, {_BlockStateKeys.ExplodeBit: explode_bit})

    @staticmethod
    def Torch(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for Torch"""
        return MinecraftBlockDescriptor("minecraft:torch", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def Torchflower() -> MinecraftBlockDescriptor:
        """Factory for Torchflower"""
        return MinecraftBlockDescriptor("minecraft:torchflower", True)

    @staticmethod
    def TorchflowerCrop(growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for TorchflowerCrop"""
        return MinecraftBlockDescriptor("minecraft:torchflower_crop", True, {_BlockStateKeys.Growth: growth})

    @staticmethod
    def Trapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for Trapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def TrappedChest(minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for TrappedChest"""
        return MinecraftBlockDescriptor(
            "minecraft:trapped_chest", True, {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def TrialSpawner(ominous: Ominous, trial_spawner_state: TrialSpawnerState) -> MinecraftBlockDescriptor:
        """Factory for TrialSpawner"""
        return MinecraftBlockDescriptor(
            "minecraft:trial_spawner", True, {_BlockStateKeys.Ominous: ominous, _BlockStateKeys.TrialSpawnerState: trial_spawner_state}
        )

    @staticmethod
    def TripWire(
        attached_bit: AttachedBit, disarmed_bit: DisarmedBit, powered_bit: PoweredBit, suspended_bit: SuspendedBit
    ) -> MinecraftBlockDescriptor:
        """Factory for TripWire"""
        return MinecraftBlockDescriptor(
            "minecraft:trip_wire", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.DisarmedBit: disarmed_bit,
                _BlockStateKeys.PoweredBit: powered_bit,
                _BlockStateKeys.SuspendedBit: suspended_bit,
            },
        )

    @staticmethod
    def TripwireHook(attached_bit: AttachedBit, direction: Direction, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for TripwireHook"""
        return MinecraftBlockDescriptor(
            "minecraft:tripwire_hook", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.PoweredBit: powered_bit,
            },
        )

    @staticmethod
    def TubeCoral() -> MinecraftBlockDescriptor:
        """Factory for TubeCoral"""
        return MinecraftBlockDescriptor("minecraft:tube_coral", True)

    @staticmethod
    def TubeCoralBlock() -> MinecraftBlockDescriptor:
        """Factory for TubeCoralBlock"""
        return MinecraftBlockDescriptor("minecraft:tube_coral_block", True)

    @staticmethod
    def TubeCoralFan(coral_fan_direction: CoralFanDirection) -> MinecraftBlockDescriptor:
        """Factory for TubeCoralFan"""
        return MinecraftBlockDescriptor("minecraft:tube_coral_fan", True, {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def TubeCoralWallFan(coral_direction: CoralDirection) -> MinecraftBlockDescriptor:
        """Factory for TubeCoralWallFan"""
        return MinecraftBlockDescriptor("minecraft:tube_coral_wall_fan", True, {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def Tuff() -> MinecraftBlockDescriptor:
        """Factory for Tuff"""
        return MinecraftBlockDescriptor("minecraft:tuff", True)

    @staticmethod
    def TuffBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for TuffBrickDoubleSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:tuff_brick_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def TuffBrickSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for TuffBrickSlab"""
        return MinecraftBlockDescriptor("minecraft:tuff_brick_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def TuffBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for TuffBrickStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:tuff_brick_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def TuffBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for TuffBrickWall"""
        return MinecraftBlockDescriptor(
            "minecraft:tuff_brick_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def TuffBricks() -> MinecraftBlockDescriptor:
        """Factory for TuffBricks"""
        return MinecraftBlockDescriptor("minecraft:tuff_bricks", True)

    @staticmethod
    def TuffDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for TuffDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:tuff_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def TuffSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for TuffSlab"""
        return MinecraftBlockDescriptor("minecraft:tuff_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def TuffStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for TuffStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:tuff_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def TuffWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for TuffWall"""
        return MinecraftBlockDescriptor(
            "minecraft:tuff_wall", True,
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def TurtleEgg(cracked_state: CrackedState, turtle_egg_count: TurtleEggCount) -> MinecraftBlockDescriptor:
        """Factory for TurtleEgg"""
        return MinecraftBlockDescriptor(
            "minecraft:turtle_egg", True,
            {_BlockStateKeys.CrackedState: cracked_state, _BlockStateKeys.TurtleEggCount: turtle_egg_count},
        )

    @staticmethod
    def TwistingVines(twisting_vines_age: TwistingVinesAge) -> MinecraftBlockDescriptor:
        """Factory for TwistingVines"""
        return MinecraftBlockDescriptor("minecraft:twisting_vines", True, {_BlockStateKeys.TwistingVinesAge: twisting_vines_age})

    @staticmethod
    def UnderwaterTnt(explode_bit: ExplodeBit) -> MinecraftBlockDescriptor:
        """Factory for UnderwaterTnt"""
        return MinecraftBlockDescriptor("minecraft:underwater_tnt", True, {_BlockStateKeys.ExplodeBit: explode_bit})

    @staticmethod
    def UnderwaterTorch(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for UnderwaterTorch"""
        return MinecraftBlockDescriptor("minecraft:underwater_torch", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def UndyedShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for UndyedShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:undyed_shulker_box", True)

    @staticmethod
    def Unknown() -> MinecraftBlockDescriptor:
        """Factory for Unknown"""
        return MinecraftBlockDescriptor("minecraft:unknown", True)

    @staticmethod
    def UnlitRedstoneTorch(torch_facing_direction: TorchFacingDirection) -> MinecraftBlockDescriptor:
        """Factory for UnlitRedstoneTorch"""
        return MinecraftBlockDescriptor("minecraft:unlit_redstone_torch", True, {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def UnpoweredComparator(
        minecraft_cardinal_direction: CardinalDirection, output_lit_bit: OutputLitBit, output_subtract_bit: OutputSubtractBit
    ) -> MinecraftBlockDescriptor:
        """Factory for UnpoweredComparator"""
        return MinecraftBlockDescriptor(
            "minecraft:unpowered_comparator", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OutputLitBit: output_lit_bit,
                _BlockStateKeys.OutputSubtractBit: output_subtract_bit,
            },
        )

    @staticmethod
    def UnpoweredRepeater(minecraft_cardinal_direction: CardinalDirection, repeater_delay: RepeaterDelay) -> MinecraftBlockDescriptor:
        """Factory for UnpoweredRepeater"""
        return MinecraftBlockDescriptor(
            "minecraft:unpowered_repeater", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.RepeaterDelay: repeater_delay,
            },
        )

    @staticmethod
    def Vault(minecraft_cardinal_direction: CardinalDirection, ominous: Ominous, vault_state: VaultState) -> MinecraftBlockDescriptor:
        """Factory for Vault"""
        return MinecraftBlockDescriptor(
            "minecraft:vault", True,
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.Ominous: ominous,
                _BlockStateKeys.VaultState: vault_state,
            },
        )

    @staticmethod
    def VerdantFroglight(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for VerdantFroglight"""
        return MinecraftBlockDescriptor("minecraft:verdant_froglight", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Vine(vine_direction_bits: VineDirectionBits) -> MinecraftBlockDescriptor:
        """Factory for Vine"""
        return MinecraftBlockDescriptor("minecraft:vine", True, {_BlockStateKeys.VineDirectionBits: vine_direction_bits})

    @staticmethod
    def WallBanner(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WallBanner"""
        return MinecraftBlockDescriptor("minecraft:wall_banner", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WallSign"""
        return MinecraftBlockDescriptor("minecraft:wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WarpedButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WarpedButton"""
        return MinecraftBlockDescriptor(
            "minecraft:warped_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def WarpedDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WarpedDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:warped_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WarpedDoubleSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WarpedDoubleSlab"""
        return MinecraftBlockDescriptor("minecraft:warped_double_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def WarpedFence() -> MinecraftBlockDescriptor:
        """Factory for WarpedFence"""
        return MinecraftBlockDescriptor("minecraft:warped_fence", True)

    @staticmethod
    def WarpedFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> MinecraftBlockDescriptor:
        """Factory for WarpedFenceGate"""
        return MinecraftBlockDescriptor(
            "minecraft:warped_fence_gate", True,
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def WarpedFungus() -> MinecraftBlockDescriptor:
        """Factory for WarpedFungus"""
        return MinecraftBlockDescriptor("minecraft:warped_fungus", True)

    @staticmethod
    def WarpedHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> MinecraftBlockDescriptor:
        """Factory for WarpedHangingSign"""
        return MinecraftBlockDescriptor(
            "minecraft:warped_hanging_sign", True,
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def WarpedHyphae(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for WarpedHyphae"""
        return MinecraftBlockDescriptor("minecraft:warped_hyphae", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def WarpedNylium() -> MinecraftBlockDescriptor:
        """Factory for WarpedNylium"""
        return MinecraftBlockDescriptor("minecraft:warped_nylium", True)

    @staticmethod
    def WarpedPlanks() -> MinecraftBlockDescriptor:
        """Factory for WarpedPlanks"""
        return MinecraftBlockDescriptor("minecraft:warped_planks", True)

    @staticmethod
    def WarpedPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for WarpedPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:warped_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def WarpedRoots() -> MinecraftBlockDescriptor:
        """Factory for WarpedRoots"""
        return MinecraftBlockDescriptor("minecraft:warped_roots", True)

    @staticmethod
    def WarpedSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WarpedSlab"""
        return MinecraftBlockDescriptor("minecraft:warped_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def WarpedStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for WarpedStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:warped_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WarpedStandingSign(ground_sign_direction: GroundSignDirection) -> MinecraftBlockDescriptor:
        """Factory for WarpedStandingSign"""
        return MinecraftBlockDescriptor("minecraft:warped_standing_sign", True, {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def WarpedStem(pillar_axis: PillarAxis) -> MinecraftBlockDescriptor:
        """Factory for WarpedStem"""
        return MinecraftBlockDescriptor("minecraft:warped_stem", True, {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def WarpedTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for WarpedTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:warped_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WarpedWallSign(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WarpedWallSign"""
        return MinecraftBlockDescriptor("minecraft:warped_wall_sign", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WarpedWartBlock() -> MinecraftBlockDescriptor:
        """Factory for WarpedWartBlock"""
        return MinecraftBlockDescriptor("minecraft:warped_wart_block", True)

    @staticmethod
    def Water(liquid_depth: LiquidDepth) -> MinecraftBlockDescriptor:
        """Factory for Water"""
        return MinecraftBlockDescriptor("minecraft:water", True, {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def Waterlily() -> MinecraftBlockDescriptor:
        """Factory for Waterlily"""
        return MinecraftBlockDescriptor("minecraft:waterlily", True)

    @staticmethod
    def WaxedChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_chiseled_copper", True)

    @staticmethod
    def WaxedCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_copper", True)

    @staticmethod
    def WaxedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedCopperBulb"""
        return MinecraftBlockDescriptor("minecraft:waxed_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit})

    @staticmethod
    def WaxedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WaxedCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for WaxedCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:waxed_copper_grate", True)

    @staticmethod
    def WaxedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedCutCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedCutCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_cut_copper", True)

    @staticmethod
    def WaxedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for WaxedCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedExposedChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_exposed_chiseled_copper", True)

    @staticmethod
    def WaxedExposedCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_exposed_copper", True)

    @staticmethod
    def WaxedExposedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCopperBulb"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_exposed_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WaxedExposedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_exposed_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedExposedCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:waxed_exposed_copper_grate", True)

    @staticmethod
    def WaxedExposedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_exposed_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedExposedCutCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCutCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_exposed_cut_copper", True)

    @staticmethod
    def WaxedExposedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_exposed_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedExposedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_exposed_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedExposedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedExposedDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_exposed_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedOxidizedChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_oxidized_chiseled_copper", True)

    @staticmethod
    def WaxedOxidizedCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_oxidized_copper", True)

    @staticmethod
    def WaxedOxidizedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCopperBulb"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_oxidized_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WaxedOxidizedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_oxidized_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedOxidizedCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:waxed_oxidized_copper_grate", True)

    @staticmethod
    def WaxedOxidizedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_oxidized_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedOxidizedCutCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCutCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_oxidized_cut_copper", True)

    @staticmethod
    def WaxedOxidizedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_oxidized_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedOxidizedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_oxidized_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedOxidizedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedOxidizedDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_oxidized_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedWeatheredChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_weathered_chiseled_copper", True)

    @staticmethod
    def WaxedWeatheredCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_weathered_copper", True)

    @staticmethod
    def WaxedWeatheredCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCopperBulb"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_weathered_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WaxedWeatheredCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_weathered_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedWeatheredCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:waxed_weathered_copper_grate", True)

    @staticmethod
    def WaxedWeatheredCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_weathered_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedWeatheredCutCopper() -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCutCopper"""
        return MinecraftBlockDescriptor("minecraft:waxed_weathered_cut_copper", True)

    @staticmethod
    def WaxedWeatheredCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_weathered_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedWeatheredCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_weathered_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedWeatheredDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WaxedWeatheredDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:waxed_weathered_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WeatheredChiseledCopper() -> MinecraftBlockDescriptor:
        """Factory for WeatheredChiseledCopper"""
        return MinecraftBlockDescriptor("minecraft:weathered_chiseled_copper", True)

    @staticmethod
    def WeatheredCopper() -> MinecraftBlockDescriptor:
        """Factory for WeatheredCopper"""
        return MinecraftBlockDescriptor("minecraft:weathered_copper", True)

    @staticmethod
    def WeatheredCopperBulb(lit: Lit, powered_bit: PoweredBit) -> MinecraftBlockDescriptor:
        """Factory for WeatheredCopperBulb"""
        return MinecraftBlockDescriptor(
            "minecraft:weathered_copper_bulb", True, {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WeatheredCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WeatheredCopperDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:weathered_copper_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WeatheredCopperGrate() -> MinecraftBlockDescriptor:
        """Factory for WeatheredCopperGrate"""
        return MinecraftBlockDescriptor("minecraft:weathered_copper_grate", True)

    @staticmethod
    def WeatheredCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> MinecraftBlockDescriptor:
        """Factory for WeatheredCopperTrapdoor"""
        return MinecraftBlockDescriptor(
            "minecraft:weathered_copper_trapdoor", True,
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WeatheredCutCopper() -> MinecraftBlockDescriptor:
        """Factory for WeatheredCutCopper"""
        return MinecraftBlockDescriptor("minecraft:weathered_cut_copper", True)

    @staticmethod
    def WeatheredCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WeatheredCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:weathered_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WeatheredCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> MinecraftBlockDescriptor:
        """Factory for WeatheredCutCopperStairs"""
        return MinecraftBlockDescriptor(
            "minecraft:weathered_cut_copper_stairs", True,
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WeatheredDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> MinecraftBlockDescriptor:
        """Factory for WeatheredDoubleCutCopperSlab"""
        return MinecraftBlockDescriptor(
            "minecraft:weathered_double_cut_copper_slab", True, {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def Web() -> MinecraftBlockDescriptor:
        """Factory for Web"""
        return MinecraftBlockDescriptor("minecraft:web", True)

    @staticmethod
    def WeepingVines(weeping_vines_age: WeepingVinesAge) -> MinecraftBlockDescriptor:
        """Factory for WeepingVines"""
        return MinecraftBlockDescriptor("minecraft:weeping_vines", True, {_BlockStateKeys.WeepingVinesAge: weeping_vines_age})

    @staticmethod
    def WetSponge() -> MinecraftBlockDescriptor:
        """Factory for WetSponge"""
        return MinecraftBlockDescriptor("minecraft:wet_sponge", True)

    @staticmethod
    def Wheat(growth: Growth) -> MinecraftBlockDescriptor:
        """Factory for Wheat"""
        return MinecraftBlockDescriptor("minecraft:wheat", True, {_BlockStateKeys.Growth: growth})

    @staticmethod
    def WhiteCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for WhiteCandle"""
        return MinecraftBlockDescriptor("minecraft:white_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def WhiteCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for WhiteCandleCake"""
        return MinecraftBlockDescriptor("minecraft:white_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def WhiteCarpet() -> MinecraftBlockDescriptor:
        """Factory for WhiteCarpet"""
        return MinecraftBlockDescriptor("minecraft:white_carpet", True)

    @staticmethod
    def WhiteConcrete() -> MinecraftBlockDescriptor:
        """Factory for WhiteConcrete"""
        return MinecraftBlockDescriptor("minecraft:white_concrete", True)

    @staticmethod
    def WhiteConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for WhiteConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:white_concrete_powder", True)

    @staticmethod
    def WhiteGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WhiteGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:white_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WhiteShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for WhiteShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:white_shulker_box", True)

    @staticmethod
    def WhiteStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for WhiteStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:white_stained_glass", True)

    @staticmethod
    def WhiteStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for WhiteStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:white_stained_glass_pane", True)

    @staticmethod
    def WhiteTerracotta() -> MinecraftBlockDescriptor:
        """Factory for WhiteTerracotta"""
        return MinecraftBlockDescriptor("minecraft:white_terracotta", True)

    @staticmethod
    def WhiteTulip() -> MinecraftBlockDescriptor:
        """Factory for WhiteTulip"""
        return MinecraftBlockDescriptor("minecraft:white_tulip", True)

    @staticmethod
    def WhiteWool() -> MinecraftBlockDescriptor:
        """Factory for WhiteWool"""
        return MinecraftBlockDescriptor("minecraft:white_wool", True)

    @staticmethod
    def Wildflowers(growth: Growth, minecraft_cardinal_direction: CardinalDirection) -> MinecraftBlockDescriptor:
        """Factory for Wildflowers"""
        return MinecraftBlockDescriptor(
            "minecraft:wildflowers", True,
            {_BlockStateKeys.Growth: growth, _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
        )

    @staticmethod
    def WitherRose() -> MinecraftBlockDescriptor:
        """Factory for WitherRose"""
        return MinecraftBlockDescriptor("minecraft:wither_rose", True)

    @staticmethod
    def WitherSkeletonSkull(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WitherSkeletonSkull"""
        return MinecraftBlockDescriptor("minecraft:wither_skeleton_skull", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WoodenButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for WoodenButton"""
        return MinecraftBlockDescriptor(
            "minecraft:wooden_button", True,
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def WoodenDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> MinecraftBlockDescriptor:
        """Factory for WoodenDoor"""
        return MinecraftBlockDescriptor(
            "minecraft:wooden_door", True,
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WoodenPressurePlate(redstone_signal: RedstoneSignal) -> MinecraftBlockDescriptor:
        """Factory for WoodenPressurePlate"""
        return MinecraftBlockDescriptor("minecraft:wooden_pressure_plate", True, {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def YellowCandle(candles: Candles, lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for YellowCandle"""
        return MinecraftBlockDescriptor("minecraft:yellow_candle", True, {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def YellowCandleCake(lit: Lit) -> MinecraftBlockDescriptor:
        """Factory for YellowCandleCake"""
        return MinecraftBlockDescriptor("minecraft:yellow_candle_cake", True, {_BlockStateKeys.Lit: lit})

    @staticmethod
    def YellowCarpet() -> MinecraftBlockDescriptor:
        """Factory for YellowCarpet"""
        return MinecraftBlockDescriptor("minecraft:yellow_carpet", True)

    @staticmethod
    def YellowConcrete() -> MinecraftBlockDescriptor:
        """Factory for YellowConcrete"""
        return MinecraftBlockDescriptor("minecraft:yellow_concrete", True)

    @staticmethod
    def YellowConcretePowder() -> MinecraftBlockDescriptor:
        """Factory for YellowConcretePowder"""
        return MinecraftBlockDescriptor("minecraft:yellow_concrete_powder", True)

    @staticmethod
    def YellowGlazedTerracotta(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for YellowGlazedTerracotta"""
        return MinecraftBlockDescriptor("minecraft:yellow_glazed_terracotta", True, {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def YellowShulkerBox() -> MinecraftBlockDescriptor:
        """Factory for YellowShulkerBox"""
        return MinecraftBlockDescriptor("minecraft:yellow_shulker_box", True)

    @staticmethod
    def YellowStainedGlass() -> MinecraftBlockDescriptor:
        """Factory for YellowStainedGlass"""
        return MinecraftBlockDescriptor("minecraft:yellow_stained_glass", True)

    @staticmethod
    def YellowStainedGlassPane() -> MinecraftBlockDescriptor:
        """Factory for YellowStainedGlassPane"""
        return MinecraftBlockDescriptor("minecraft:yellow_stained_glass_pane", True)

    @staticmethod
    def YellowTerracotta() -> MinecraftBlockDescriptor:
        """Factory for YellowTerracotta"""
        return MinecraftBlockDescriptor("minecraft:yellow_terracotta", True)

    @staticmethod
    def YellowWool() -> MinecraftBlockDescriptor:
        """Factory for YellowWool"""
        return MinecraftBlockDescriptor("minecraft:yellow_wool", True)

    @staticmethod
    def ZombieHead(facing_direction: FacingDirection) -> MinecraftBlockDescriptor:
        """Factory for ZombieHead"""
        return MinecraftBlockDescriptor("minecraft:zombie_head", True, {_BlockStateKeys.FacingDirection: facing_direction})
