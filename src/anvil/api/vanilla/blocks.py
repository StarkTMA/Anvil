from enum import StrEnum
from typing import Literal, TypeAlias

from anvil.lib.types import BlockDescriptor

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
    def AcaciaButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for AcaciaButton"""
        return BlockDescriptor(
            "minecraft:acacia_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def AcaciaDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for AcaciaDoor"""
        return BlockDescriptor(
            "minecraft:acacia_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def AcaciaDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for AcaciaDoubleSlab"""
        return BlockDescriptor("minecraft:acacia_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AcaciaFence() -> BlockDescriptor:
        """Factory for AcaciaFence"""
        return BlockDescriptor("minecraft:acacia_fence")

    @staticmethod
    def AcaciaFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for AcaciaFenceGate"""
        return BlockDescriptor(
            "minecraft:acacia_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def AcaciaHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for AcaciaHangingSign"""
        return BlockDescriptor(
            "minecraft:acacia_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def AcaciaLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for AcaciaLeaves"""
        return BlockDescriptor(
            "minecraft:acacia_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def AcaciaLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for AcaciaLog"""
        return BlockDescriptor("minecraft:acacia_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def AcaciaPlanks() -> BlockDescriptor:
        """Factory for AcaciaPlanks"""
        return BlockDescriptor("minecraft:acacia_planks")

    @staticmethod
    def AcaciaPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for AcaciaPressurePlate"""
        return BlockDescriptor("minecraft:acacia_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def AcaciaSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for AcaciaSapling"""
        return BlockDescriptor("minecraft:acacia_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def AcaciaSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for AcaciaSlab"""
        return BlockDescriptor("minecraft:acacia_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AcaciaStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for AcaciaStairs"""
        return BlockDescriptor(
            "minecraft:acacia_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def AcaciaStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for AcaciaStandingSign"""
        return BlockDescriptor("minecraft:acacia_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def AcaciaTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for AcaciaTrapdoor"""
        return BlockDescriptor(
            "minecraft:acacia_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def AcaciaWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for AcaciaWallSign"""
        return BlockDescriptor("minecraft:acacia_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def AcaciaWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for AcaciaWood"""
        return BlockDescriptor("minecraft:acacia_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def ActivatorRail(rail_data_bit: RailDataBit, rail_direction: RailDirection) -> BlockDescriptor:
        """Factory for ActivatorRail"""
        return BlockDescriptor(
            "minecraft:activator_rail",
            {_BlockStateKeys.RailDataBit: rail_data_bit, _BlockStateKeys.RailDirection: rail_direction},
        )

    @staticmethod
    def Air() -> BlockDescriptor:
        """Factory for Air"""
        return BlockDescriptor("minecraft:air")

    @staticmethod
    def Allium() -> BlockDescriptor:
        """Factory for Allium"""
        return BlockDescriptor("minecraft:allium")

    @staticmethod
    def Allow() -> BlockDescriptor:
        """Factory for Allow"""
        return BlockDescriptor("minecraft:allow")

    @staticmethod
    def AmethystBlock() -> BlockDescriptor:
        """Factory for AmethystBlock"""
        return BlockDescriptor("minecraft:amethyst_block")

    @staticmethod
    def AmethystCluster(minecraft_block_face: BlockFace) -> BlockDescriptor:
        """Factory for AmethystCluster"""
        return BlockDescriptor("minecraft:amethyst_cluster", {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def AncientDebris() -> BlockDescriptor:
        """Factory for AncientDebris"""
        return BlockDescriptor("minecraft:ancient_debris")

    @staticmethod
    def Andesite() -> BlockDescriptor:
        """Factory for Andesite"""
        return BlockDescriptor("minecraft:andesite")

    @staticmethod
    def AndesiteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for AndesiteDoubleSlab"""
        return BlockDescriptor("minecraft:andesite_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AndesiteSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for AndesiteSlab"""
        return BlockDescriptor("minecraft:andesite_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def AndesiteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for AndesiteStairs"""
        return BlockDescriptor(
            "minecraft:andesite_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def AndesiteWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for AndesiteWall"""
        return BlockDescriptor(
            "minecraft:andesite_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Anvil(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Anvil"""
        return BlockDescriptor("minecraft:anvil", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def Azalea() -> BlockDescriptor:
        """Factory for Azalea"""
        return BlockDescriptor("minecraft:azalea")

    @staticmethod
    def AzaleaLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for AzaleaLeaves"""
        return BlockDescriptor(
            "minecraft:azalea_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def AzaleaLeavesFlowered(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for AzaleaLeavesFlowered"""
        return BlockDescriptor(
            "minecraft:azalea_leaves_flowered",
            {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit},
        )

    @staticmethod
    def AzureBluet() -> BlockDescriptor:
        """Factory for AzureBluet"""
        return BlockDescriptor("minecraft:azure_bluet")

    @staticmethod
    def Bamboo(
        age_bit: AgeBit, bamboo_leaf_size: BambooLeafSize, bamboo_stalk_thickness: BambooStalkThickness
    ) -> BlockDescriptor:
        """Factory for Bamboo"""
        return BlockDescriptor(
            "minecraft:bamboo",
            {
                _BlockStateKeys.AgeBit: age_bit,
                _BlockStateKeys.BambooLeafSize: bamboo_leaf_size,
                _BlockStateKeys.BambooStalkThickness: bamboo_stalk_thickness,
            },
        )

    @staticmethod
    def BambooBlock(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for BambooBlock"""
        return BlockDescriptor("minecraft:bamboo_block", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def BambooButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BambooButton"""
        return BlockDescriptor(
            "minecraft:bamboo_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def BambooDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for BambooDoor"""
        return BlockDescriptor(
            "minecraft:bamboo_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def BambooDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BambooDoubleSlab"""
        return BlockDescriptor("minecraft:bamboo_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BambooFence() -> BlockDescriptor:
        """Factory for BambooFence"""
        return BlockDescriptor("minecraft:bamboo_fence")

    @staticmethod
    def BambooFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for BambooFenceGate"""
        return BlockDescriptor(
            "minecraft:bamboo_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def BambooHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for BambooHangingSign"""
        return BlockDescriptor(
            "minecraft:bamboo_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def BambooMosaic() -> BlockDescriptor:
        """Factory for BambooMosaic"""
        return BlockDescriptor("minecraft:bamboo_mosaic")

    @staticmethod
    def BambooMosaicDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BambooMosaicDoubleSlab"""
        return BlockDescriptor(
            "minecraft:bamboo_mosaic_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def BambooMosaicSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BambooMosaicSlab"""
        return BlockDescriptor("minecraft:bamboo_mosaic_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BambooMosaicStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for BambooMosaicStairs"""
        return BlockDescriptor(
            "minecraft:bamboo_mosaic_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BambooPlanks() -> BlockDescriptor:
        """Factory for BambooPlanks"""
        return BlockDescriptor("minecraft:bamboo_planks")

    @staticmethod
    def BambooPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for BambooPressurePlate"""
        return BlockDescriptor("minecraft:bamboo_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def BambooSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for BambooSapling"""
        return BlockDescriptor("minecraft:bamboo_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def BambooSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BambooSlab"""
        return BlockDescriptor("minecraft:bamboo_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BambooStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for BambooStairs"""
        return BlockDescriptor(
            "minecraft:bamboo_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BambooStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for BambooStandingSign"""
        return BlockDescriptor("minecraft:bamboo_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def BambooTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for BambooTrapdoor"""
        return BlockDescriptor(
            "minecraft:bamboo_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def BambooWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BambooWallSign"""
        return BlockDescriptor("minecraft:bamboo_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Barrel(facing_direction: FacingDirection, open_bit: OpenBit) -> BlockDescriptor:
        """Factory for Barrel"""
        return BlockDescriptor(
            "minecraft:barrel", {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.OpenBit: open_bit}
        )

    @staticmethod
    def Barrier() -> BlockDescriptor:
        """Factory for Barrier"""
        return BlockDescriptor("minecraft:barrier")

    @staticmethod
    def Basalt(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for Basalt"""
        return BlockDescriptor("minecraft:basalt", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Beacon() -> BlockDescriptor:
        """Factory for Beacon"""
        return BlockDescriptor("minecraft:beacon")

    @staticmethod
    def Bed(direction: Direction, head_piece_bit: HeadPieceBit, occupied_bit: OccupiedBit) -> BlockDescriptor:
        """Factory for Bed"""
        return BlockDescriptor(
            "minecraft:bed",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.HeadPieceBit: head_piece_bit,
                _BlockStateKeys.OccupiedBit: occupied_bit,
            },
        )

    @staticmethod
    def Bedrock(infiniburn_bit: InfiniburnBit) -> BlockDescriptor:
        """Factory for Bedrock"""
        return BlockDescriptor("minecraft:bedrock", {_BlockStateKeys.InfiniburnBit: infiniburn_bit})

    @staticmethod
    def BeeNest(direction: Direction, honey_level: HoneyLevel) -> BlockDescriptor:
        """Factory for BeeNest"""
        return BlockDescriptor(
            "minecraft:bee_nest", {_BlockStateKeys.Direction: direction, _BlockStateKeys.HoneyLevel: honey_level}
        )

    @staticmethod
    def Beehive(direction: Direction, honey_level: HoneyLevel) -> BlockDescriptor:
        """Factory for Beehive"""
        return BlockDescriptor(
            "minecraft:beehive", {_BlockStateKeys.Direction: direction, _BlockStateKeys.HoneyLevel: honey_level}
        )

    @staticmethod
    def Beetroot(growth: Growth) -> BlockDescriptor:
        """Factory for Beetroot"""
        return BlockDescriptor("minecraft:beetroot", {_BlockStateKeys.Growth: growth})

    @staticmethod
    def Bell(attachment: Attachment, direction: Direction, toggle_bit: ToggleBit) -> BlockDescriptor:
        """Factory for Bell"""
        return BlockDescriptor(
            "minecraft:bell",
            {_BlockStateKeys.Attachment: attachment, _BlockStateKeys.Direction: direction, _BlockStateKeys.ToggleBit: toggle_bit},
        )

    @staticmethod
    def BigDripleaf(
        big_dripleaf_head: BigDripleafHead, big_dripleaf_tilt: BigDripleafTilt, minecraft_cardinal_direction: CardinalDirection
    ) -> BlockDescriptor:
        """Factory for BigDripleaf"""
        return BlockDescriptor(
            "minecraft:big_dripleaf",
            {
                _BlockStateKeys.BigDripleafHead: big_dripleaf_head,
                _BlockStateKeys.BigDripleafTilt: big_dripleaf_tilt,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def BirchButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BirchButton"""
        return BlockDescriptor(
            "minecraft:birch_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def BirchDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for BirchDoor"""
        return BlockDescriptor(
            "minecraft:birch_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def BirchDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BirchDoubleSlab"""
        return BlockDescriptor("minecraft:birch_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BirchFence() -> BlockDescriptor:
        """Factory for BirchFence"""
        return BlockDescriptor("minecraft:birch_fence")

    @staticmethod
    def BirchFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for BirchFenceGate"""
        return BlockDescriptor(
            "minecraft:birch_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def BirchHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for BirchHangingSign"""
        return BlockDescriptor(
            "minecraft:birch_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def BirchLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for BirchLeaves"""
        return BlockDescriptor(
            "minecraft:birch_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def BirchLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for BirchLog"""
        return BlockDescriptor("minecraft:birch_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def BirchPlanks() -> BlockDescriptor:
        """Factory for BirchPlanks"""
        return BlockDescriptor("minecraft:birch_planks")

    @staticmethod
    def BirchPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for BirchPressurePlate"""
        return BlockDescriptor("minecraft:birch_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def BirchSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for BirchSapling"""
        return BlockDescriptor("minecraft:birch_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def BirchSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BirchSlab"""
        return BlockDescriptor("minecraft:birch_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BirchStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for BirchStairs"""
        return BlockDescriptor(
            "minecraft:birch_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BirchStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for BirchStandingSign"""
        return BlockDescriptor("minecraft:birch_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def BirchTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for BirchTrapdoor"""
        return BlockDescriptor(
            "minecraft:birch_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def BirchWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BirchWallSign"""
        return BlockDescriptor("minecraft:birch_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BirchWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for BirchWood"""
        return BlockDescriptor("minecraft:birch_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def BlackCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for BlackCandle"""
        return BlockDescriptor("minecraft:black_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def BlackCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for BlackCandleCake"""
        return BlockDescriptor("minecraft:black_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def BlackCarpet() -> BlockDescriptor:
        """Factory for BlackCarpet"""
        return BlockDescriptor("minecraft:black_carpet")

    @staticmethod
    def BlackConcrete() -> BlockDescriptor:
        """Factory for BlackConcrete"""
        return BlockDescriptor("minecraft:black_concrete")

    @staticmethod
    def BlackConcretePowder() -> BlockDescriptor:
        """Factory for BlackConcretePowder"""
        return BlockDescriptor("minecraft:black_concrete_powder")

    @staticmethod
    def BlackGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BlackGlazedTerracotta"""
        return BlockDescriptor("minecraft:black_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BlackShulkerBox() -> BlockDescriptor:
        """Factory for BlackShulkerBox"""
        return BlockDescriptor("minecraft:black_shulker_box")

    @staticmethod
    def BlackStainedGlass() -> BlockDescriptor:
        """Factory for BlackStainedGlass"""
        return BlockDescriptor("minecraft:black_stained_glass")

    @staticmethod
    def BlackStainedGlassPane() -> BlockDescriptor:
        """Factory for BlackStainedGlassPane"""
        return BlockDescriptor("minecraft:black_stained_glass_pane")

    @staticmethod
    def BlackTerracotta() -> BlockDescriptor:
        """Factory for BlackTerracotta"""
        return BlockDescriptor("minecraft:black_terracotta")

    @staticmethod
    def BlackWool() -> BlockDescriptor:
        """Factory for BlackWool"""
        return BlockDescriptor("minecraft:black_wool")

    @staticmethod
    def Blackstone() -> BlockDescriptor:
        """Factory for Blackstone"""
        return BlockDescriptor("minecraft:blackstone")

    @staticmethod
    def BlackstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BlackstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:blackstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def BlackstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BlackstoneSlab"""
        return BlockDescriptor("minecraft:blackstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BlackstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for BlackstoneStairs"""
        return BlockDescriptor(
            "minecraft:blackstone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BlackstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for BlackstoneWall"""
        return BlockDescriptor(
            "minecraft:blackstone_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def BlastFurnace(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for BlastFurnace"""
        return BlockDescriptor(
            "minecraft:blast_furnace", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def BlueCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for BlueCandle"""
        return BlockDescriptor("minecraft:blue_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def BlueCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for BlueCandleCake"""
        return BlockDescriptor("minecraft:blue_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def BlueCarpet() -> BlockDescriptor:
        """Factory for BlueCarpet"""
        return BlockDescriptor("minecraft:blue_carpet")

    @staticmethod
    def BlueConcrete() -> BlockDescriptor:
        """Factory for BlueConcrete"""
        return BlockDescriptor("minecraft:blue_concrete")

    @staticmethod
    def BlueConcretePowder() -> BlockDescriptor:
        """Factory for BlueConcretePowder"""
        return BlockDescriptor("minecraft:blue_concrete_powder")

    @staticmethod
    def BlueGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BlueGlazedTerracotta"""
        return BlockDescriptor("minecraft:blue_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BlueIce() -> BlockDescriptor:
        """Factory for BlueIce"""
        return BlockDescriptor("minecraft:blue_ice")

    @staticmethod
    def BlueOrchid() -> BlockDescriptor:
        """Factory for BlueOrchid"""
        return BlockDescriptor("minecraft:blue_orchid")

    @staticmethod
    def BlueShulkerBox() -> BlockDescriptor:
        """Factory for BlueShulkerBox"""
        return BlockDescriptor("minecraft:blue_shulker_box")

    @staticmethod
    def BlueStainedGlass() -> BlockDescriptor:
        """Factory for BlueStainedGlass"""
        return BlockDescriptor("minecraft:blue_stained_glass")

    @staticmethod
    def BlueStainedGlassPane() -> BlockDescriptor:
        """Factory for BlueStainedGlassPane"""
        return BlockDescriptor("minecraft:blue_stained_glass_pane")

    @staticmethod
    def BlueTerracotta() -> BlockDescriptor:
        """Factory for BlueTerracotta"""
        return BlockDescriptor("minecraft:blue_terracotta")

    @staticmethod
    def BlueWool() -> BlockDescriptor:
        """Factory for BlueWool"""
        return BlockDescriptor("minecraft:blue_wool")

    @staticmethod
    def BoneBlock(deprecated: Deprecated, pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for BoneBlock"""
        return BlockDescriptor(
            "minecraft:bone_block", {_BlockStateKeys.Deprecated: deprecated, _BlockStateKeys.PillarAxis: pillar_axis}
        )

    @staticmethod
    def Bookshelf() -> BlockDescriptor:
        """Factory for Bookshelf"""
        return BlockDescriptor("minecraft:bookshelf")

    @staticmethod
    def BorderBlock(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for BorderBlock"""
        return BlockDescriptor(
            "minecraft:border_block",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def BrainCoral() -> BlockDescriptor:
        """Factory for BrainCoral"""
        return BlockDescriptor("minecraft:brain_coral")

    @staticmethod
    def BrainCoralBlock() -> BlockDescriptor:
        """Factory for BrainCoralBlock"""
        return BlockDescriptor("minecraft:brain_coral_block")

    @staticmethod
    def BrainCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for BrainCoralFan"""
        return BlockDescriptor("minecraft:brain_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def BrainCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for BrainCoralWallFan"""
        return BlockDescriptor("minecraft:brain_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def BrewingStand(
        brewing_stand_slot_a_bit: BrewingStandSlotABit,
        brewing_stand_slot_b_bit: BrewingStandSlotBBit,
        brewing_stand_slot_c_bit: BrewingStandSlotCBit,
    ) -> BlockDescriptor:
        """Factory for BrewingStand"""
        return BlockDescriptor(
            "minecraft:brewing_stand",
            {
                _BlockStateKeys.BrewingStandSlotABit: brewing_stand_slot_a_bit,
                _BlockStateKeys.BrewingStandSlotBBit: brewing_stand_slot_b_bit,
                _BlockStateKeys.BrewingStandSlotCBit: brewing_stand_slot_c_bit,
            },
        )

    @staticmethod
    def BrickBlock() -> BlockDescriptor:
        """Factory for BrickBlock"""
        return BlockDescriptor("minecraft:brick_block")

    @staticmethod
    def BrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BrickDoubleSlab"""
        return BlockDescriptor("minecraft:brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for BrickSlab"""
        return BlockDescriptor("minecraft:brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def BrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for BrickStairs"""
        return BlockDescriptor(
            "minecraft:brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def BrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for BrickWall"""
        return BlockDescriptor(
            "minecraft:brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def BrownCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for BrownCandle"""
        return BlockDescriptor("minecraft:brown_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def BrownCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for BrownCandleCake"""
        return BlockDescriptor("minecraft:brown_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def BrownCarpet() -> BlockDescriptor:
        """Factory for BrownCarpet"""
        return BlockDescriptor("minecraft:brown_carpet")

    @staticmethod
    def BrownConcrete() -> BlockDescriptor:
        """Factory for BrownConcrete"""
        return BlockDescriptor("minecraft:brown_concrete")

    @staticmethod
    def BrownConcretePowder() -> BlockDescriptor:
        """Factory for BrownConcretePowder"""
        return BlockDescriptor("minecraft:brown_concrete_powder")

    @staticmethod
    def BrownGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for BrownGlazedTerracotta"""
        return BlockDescriptor("minecraft:brown_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def BrownMushroom() -> BlockDescriptor:
        """Factory for BrownMushroom"""
        return BlockDescriptor("minecraft:brown_mushroom")

    @staticmethod
    def BrownMushroomBlock(huge_mushroom_bits: HugeMushroomBits) -> BlockDescriptor:
        """Factory for BrownMushroomBlock"""
        return BlockDescriptor("minecraft:brown_mushroom_block", {_BlockStateKeys.HugeMushroomBits: huge_mushroom_bits})

    @staticmethod
    def BrownShulkerBox() -> BlockDescriptor:
        """Factory for BrownShulkerBox"""
        return BlockDescriptor("minecraft:brown_shulker_box")

    @staticmethod
    def BrownStainedGlass() -> BlockDescriptor:
        """Factory for BrownStainedGlass"""
        return BlockDescriptor("minecraft:brown_stained_glass")

    @staticmethod
    def BrownStainedGlassPane() -> BlockDescriptor:
        """Factory for BrownStainedGlassPane"""
        return BlockDescriptor("minecraft:brown_stained_glass_pane")

    @staticmethod
    def BrownTerracotta() -> BlockDescriptor:
        """Factory for BrownTerracotta"""
        return BlockDescriptor("minecraft:brown_terracotta")

    @staticmethod
    def BrownWool() -> BlockDescriptor:
        """Factory for BrownWool"""
        return BlockDescriptor("minecraft:brown_wool")

    @staticmethod
    def BubbleColumn(drag_down: DragDown) -> BlockDescriptor:
        """Factory for BubbleColumn"""
        return BlockDescriptor("minecraft:bubble_column", {_BlockStateKeys.DragDown: drag_down})

    @staticmethod
    def BubbleCoral() -> BlockDescriptor:
        """Factory for BubbleCoral"""
        return BlockDescriptor("minecraft:bubble_coral")

    @staticmethod
    def BubbleCoralBlock() -> BlockDescriptor:
        """Factory for BubbleCoralBlock"""
        return BlockDescriptor("minecraft:bubble_coral_block")

    @staticmethod
    def BubbleCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for BubbleCoralFan"""
        return BlockDescriptor("minecraft:bubble_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def BubbleCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for BubbleCoralWallFan"""
        return BlockDescriptor("minecraft:bubble_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def BuddingAmethyst() -> BlockDescriptor:
        """Factory for BuddingAmethyst"""
        return BlockDescriptor("minecraft:budding_amethyst")

    @staticmethod
    def Bush() -> BlockDescriptor:
        """Factory for Bush"""
        return BlockDescriptor("minecraft:bush")

    @staticmethod
    def Cactus(age: Age) -> BlockDescriptor:
        """Factory for Cactus"""
        return BlockDescriptor("minecraft:cactus", {_BlockStateKeys.Age: age})

    @staticmethod
    def CactusFlower() -> BlockDescriptor:
        """Factory for CactusFlower"""
        return BlockDescriptor("minecraft:cactus_flower")

    @staticmethod
    def Cake(bite_counter: BiteCounter) -> BlockDescriptor:
        """Factory for Cake"""
        return BlockDescriptor("minecraft:cake", {_BlockStateKeys.BiteCounter: bite_counter})

    @staticmethod
    def Calcite() -> BlockDescriptor:
        """Factory for Calcite"""
        return BlockDescriptor("minecraft:calcite")

    @staticmethod
    def CalibratedSculkSensor(
        minecraft_cardinal_direction: CardinalDirection, sculk_sensor_phase: SculkSensorPhase
    ) -> BlockDescriptor:
        """Factory for CalibratedSculkSensor"""
        return BlockDescriptor(
            "minecraft:calibrated_sculk_sensor",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.SculkSensorPhase: sculk_sensor_phase,
            },
        )

    @staticmethod
    def Camera() -> BlockDescriptor:
        """Factory for Camera"""
        return BlockDescriptor("minecraft:camera")

    @staticmethod
    def Campfire(extinguished: Extinguished, minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Campfire"""
        return BlockDescriptor(
            "minecraft:campfire",
            {
                _BlockStateKeys.Extinguished: extinguished,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def Candle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for Candle"""
        return BlockDescriptor("minecraft:candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def CandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for CandleCake"""
        return BlockDescriptor("minecraft:candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def Carrots(growth: Growth) -> BlockDescriptor:
        """Factory for Carrots"""
        return BlockDescriptor("minecraft:carrots", {_BlockStateKeys.Growth: growth})

    @staticmethod
    def CartographyTable() -> BlockDescriptor:
        """Factory for CartographyTable"""
        return BlockDescriptor("minecraft:cartography_table")

    @staticmethod
    def CarvedPumpkin(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for CarvedPumpkin"""
        return BlockDescriptor(
            "minecraft:carved_pumpkin", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def Cauldron(cauldron_liquid: CauldronLiquid, fill_level: FillLevel) -> BlockDescriptor:
        """Factory for Cauldron"""
        return BlockDescriptor(
            "minecraft:cauldron", {_BlockStateKeys.CauldronLiquid: cauldron_liquid, _BlockStateKeys.FillLevel: fill_level}
        )

    @staticmethod
    def CaveVines(growing_plant_age: GrowingPlantAge) -> BlockDescriptor:
        """Factory for CaveVines"""
        return BlockDescriptor("minecraft:cave_vines", {_BlockStateKeys.GrowingPlantAge: growing_plant_age})

    @staticmethod
    def CaveVinesBodyWithBerries(growing_plant_age: GrowingPlantAge) -> BlockDescriptor:
        """Factory for CaveVinesBodyWithBerries"""
        return BlockDescriptor("minecraft:cave_vines_body_with_berries", {_BlockStateKeys.GrowingPlantAge: growing_plant_age})

    @staticmethod
    def CaveVinesHeadWithBerries(growing_plant_age: GrowingPlantAge) -> BlockDescriptor:
        """Factory for CaveVinesHeadWithBerries"""
        return BlockDescriptor("minecraft:cave_vines_head_with_berries", {_BlockStateKeys.GrowingPlantAge: growing_plant_age})

    @staticmethod
    def Chain(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for Chain"""
        return BlockDescriptor("minecraft:chain", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def ChainCommandBlock(conditional_bit: ConditionalBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for ChainCommandBlock"""
        return BlockDescriptor(
            "minecraft:chain_command_block",
            {_BlockStateKeys.ConditionalBit: conditional_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def ChemicalHeat() -> BlockDescriptor:
        """Factory for ChemicalHeat"""
        return BlockDescriptor("minecraft:chemical_heat")

    @staticmethod
    def CherryButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CherryButton"""
        return BlockDescriptor(
            "minecraft:cherry_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def CherryDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for CherryDoor"""
        return BlockDescriptor(
            "minecraft:cherry_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def CherryDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CherryDoubleSlab"""
        return BlockDescriptor("minecraft:cherry_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CherryFence() -> BlockDescriptor:
        """Factory for CherryFence"""
        return BlockDescriptor("minecraft:cherry_fence")

    @staticmethod
    def CherryFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for CherryFenceGate"""
        return BlockDescriptor(
            "minecraft:cherry_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def CherryHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for CherryHangingSign"""
        return BlockDescriptor(
            "minecraft:cherry_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def CherryLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for CherryLeaves"""
        return BlockDescriptor(
            "minecraft:cherry_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def CherryLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for CherryLog"""
        return BlockDescriptor("minecraft:cherry_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def CherryPlanks() -> BlockDescriptor:
        """Factory for CherryPlanks"""
        return BlockDescriptor("minecraft:cherry_planks")

    @staticmethod
    def CherryPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for CherryPressurePlate"""
        return BlockDescriptor("minecraft:cherry_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def CherrySapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for CherrySapling"""
        return BlockDescriptor("minecraft:cherry_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def CherrySlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CherrySlab"""
        return BlockDescriptor("minecraft:cherry_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CherryStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for CherryStairs"""
        return BlockDescriptor(
            "minecraft:cherry_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CherryStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for CherryStandingSign"""
        return BlockDescriptor("minecraft:cherry_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def CherryTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for CherryTrapdoor"""
        return BlockDescriptor(
            "minecraft:cherry_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def CherryWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CherryWallSign"""
        return BlockDescriptor("minecraft:cherry_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CherryWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for CherryWood"""
        return BlockDescriptor("minecraft:cherry_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Chest(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Chest"""
        return BlockDescriptor("minecraft:chest", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def ChippedAnvil(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for ChippedAnvil"""
        return BlockDescriptor(
            "minecraft:chipped_anvil", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def ChiseledBookshelf(books_stored: BooksStored, direction: Direction) -> BlockDescriptor:
        """Factory for ChiseledBookshelf"""
        return BlockDescriptor(
            "minecraft:chiseled_bookshelf", {_BlockStateKeys.BooksStored: books_stored, _BlockStateKeys.Direction: direction}
        )

    @staticmethod
    def ChiseledCopper() -> BlockDescriptor:
        """Factory for ChiseledCopper"""
        return BlockDescriptor("minecraft:chiseled_copper")

    @staticmethod
    def ChiseledDeepslate() -> BlockDescriptor:
        """Factory for ChiseledDeepslate"""
        return BlockDescriptor("minecraft:chiseled_deepslate")

    @staticmethod
    def ChiseledNetherBricks() -> BlockDescriptor:
        """Factory for ChiseledNetherBricks"""
        return BlockDescriptor("minecraft:chiseled_nether_bricks")

    @staticmethod
    def ChiseledPolishedBlackstone() -> BlockDescriptor:
        """Factory for ChiseledPolishedBlackstone"""
        return BlockDescriptor("minecraft:chiseled_polished_blackstone")

    @staticmethod
    def ChiseledQuartzBlock(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for ChiseledQuartzBlock"""
        return BlockDescriptor("minecraft:chiseled_quartz_block", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def ChiseledRedSandstone() -> BlockDescriptor:
        """Factory for ChiseledRedSandstone"""
        return BlockDescriptor("minecraft:chiseled_red_sandstone")

    @staticmethod
    def ChiseledResinBricks() -> BlockDescriptor:
        """Factory for ChiseledResinBricks"""
        return BlockDescriptor("minecraft:chiseled_resin_bricks")

    @staticmethod
    def ChiseledSandstone() -> BlockDescriptor:
        """Factory for ChiseledSandstone"""
        return BlockDescriptor("minecraft:chiseled_sandstone")

    @staticmethod
    def ChiseledStoneBricks() -> BlockDescriptor:
        """Factory for ChiseledStoneBricks"""
        return BlockDescriptor("minecraft:chiseled_stone_bricks")

    @staticmethod
    def ChiseledTuff() -> BlockDescriptor:
        """Factory for ChiseledTuff"""
        return BlockDescriptor("minecraft:chiseled_tuff")

    @staticmethod
    def ChiseledTuffBricks() -> BlockDescriptor:
        """Factory for ChiseledTuffBricks"""
        return BlockDescriptor("minecraft:chiseled_tuff_bricks")

    @staticmethod
    def ChorusFlower(age: Age) -> BlockDescriptor:
        """Factory for ChorusFlower"""
        return BlockDescriptor("minecraft:chorus_flower", {_BlockStateKeys.Age: age})

    @staticmethod
    def ChorusPlant() -> BlockDescriptor:
        """Factory for ChorusPlant"""
        return BlockDescriptor("minecraft:chorus_plant")

    @staticmethod
    def Clay() -> BlockDescriptor:
        """Factory for Clay"""
        return BlockDescriptor("minecraft:clay")

    @staticmethod
    def ClosedEyeblossom() -> BlockDescriptor:
        """Factory for ClosedEyeblossom"""
        return BlockDescriptor("minecraft:closed_eyeblossom")

    @staticmethod
    def CoalBlock() -> BlockDescriptor:
        """Factory for CoalBlock"""
        return BlockDescriptor("minecraft:coal_block")

    @staticmethod
    def CoalOre() -> BlockDescriptor:
        """Factory for CoalOre"""
        return BlockDescriptor("minecraft:coal_ore")

    @staticmethod
    def CoarseDirt() -> BlockDescriptor:
        """Factory for CoarseDirt"""
        return BlockDescriptor("minecraft:coarse_dirt")

    @staticmethod
    def CobbledDeepslate() -> BlockDescriptor:
        """Factory for CobbledDeepslate"""
        return BlockDescriptor("minecraft:cobbled_deepslate")

    @staticmethod
    def CobbledDeepslateDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CobbledDeepslateDoubleSlab"""
        return BlockDescriptor(
            "minecraft:cobbled_deepslate_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CobbledDeepslateSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CobbledDeepslateSlab"""
        return BlockDescriptor(
            "minecraft:cobbled_deepslate_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CobbledDeepslateStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for CobbledDeepslateStairs"""
        return BlockDescriptor(
            "minecraft:cobbled_deepslate_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CobbledDeepslateWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for CobbledDeepslateWall"""
        return BlockDescriptor(
            "minecraft:cobbled_deepslate_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Cobblestone() -> BlockDescriptor:
        """Factory for Cobblestone"""
        return BlockDescriptor("minecraft:cobblestone")

    @staticmethod
    def CobblestoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CobblestoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:cobblestone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CobblestoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CobblestoneSlab"""
        return BlockDescriptor("minecraft:cobblestone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CobblestoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for CobblestoneWall"""
        return BlockDescriptor(
            "minecraft:cobblestone_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Cocoa(age: Age, direction: Direction) -> BlockDescriptor:
        """Factory for Cocoa"""
        return BlockDescriptor("minecraft:cocoa", {_BlockStateKeys.Age: age, _BlockStateKeys.Direction: direction})

    @staticmethod
    def ColoredTorchBlue(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for ColoredTorchBlue"""
        return BlockDescriptor("minecraft:colored_torch_blue", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def ColoredTorchGreen(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for ColoredTorchGreen"""
        return BlockDescriptor("minecraft:colored_torch_green", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def ColoredTorchPurple(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for ColoredTorchPurple"""
        return BlockDescriptor("minecraft:colored_torch_purple", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def ColoredTorchRed(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for ColoredTorchRed"""
        return BlockDescriptor("minecraft:colored_torch_red", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def CommandBlock(conditional_bit: ConditionalBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CommandBlock"""
        return BlockDescriptor(
            "minecraft:command_block",
            {_BlockStateKeys.ConditionalBit: conditional_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def Composter(composter_fill_level: ComposterFillLevel) -> BlockDescriptor:
        """Factory for Composter"""
        return BlockDescriptor("minecraft:composter", {_BlockStateKeys.ComposterFillLevel: composter_fill_level})

    @staticmethod
    def CompoundCreator(direction: Direction) -> BlockDescriptor:
        """Factory for CompoundCreator"""
        return BlockDescriptor("minecraft:compound_creator", {_BlockStateKeys.Direction: direction})

    @staticmethod
    def Conduit() -> BlockDescriptor:
        """Factory for Conduit"""
        return BlockDescriptor("minecraft:conduit")

    @staticmethod
    def CopperBlock() -> BlockDescriptor:
        """Factory for CopperBlock"""
        return BlockDescriptor("minecraft:copper_block")

    @staticmethod
    def CopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for CopperBulb"""
        return BlockDescriptor("minecraft:copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit})

    @staticmethod
    def CopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for CopperDoor"""
        return BlockDescriptor(
            "minecraft:copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def CopperGrate() -> BlockDescriptor:
        """Factory for CopperGrate"""
        return BlockDescriptor("minecraft:copper_grate")

    @staticmethod
    def CopperOre() -> BlockDescriptor:
        """Factory for CopperOre"""
        return BlockDescriptor("minecraft:copper_ore")

    @staticmethod
    def CopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for CopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def Cornflower() -> BlockDescriptor:
        """Factory for Cornflower"""
        return BlockDescriptor("minecraft:cornflower")

    @staticmethod
    def CrackedDeepslateBricks() -> BlockDescriptor:
        """Factory for CrackedDeepslateBricks"""
        return BlockDescriptor("minecraft:cracked_deepslate_bricks")

    @staticmethod
    def CrackedDeepslateTiles() -> BlockDescriptor:
        """Factory for CrackedDeepslateTiles"""
        return BlockDescriptor("minecraft:cracked_deepslate_tiles")

    @staticmethod
    def CrackedNetherBricks() -> BlockDescriptor:
        """Factory for CrackedNetherBricks"""
        return BlockDescriptor("minecraft:cracked_nether_bricks")

    @staticmethod
    def CrackedPolishedBlackstoneBricks() -> BlockDescriptor:
        """Factory for CrackedPolishedBlackstoneBricks"""
        return BlockDescriptor("minecraft:cracked_polished_blackstone_bricks")

    @staticmethod
    def CrackedStoneBricks() -> BlockDescriptor:
        """Factory for CrackedStoneBricks"""
        return BlockDescriptor("minecraft:cracked_stone_bricks")

    @staticmethod
    def Crafter(crafting: Crafting, orientation: Orientation, triggered_bit: TriggeredBit) -> BlockDescriptor:
        """Factory for Crafter"""
        return BlockDescriptor(
            "minecraft:crafter",
            {
                _BlockStateKeys.Crafting: crafting,
                _BlockStateKeys.Orientation: orientation,
                _BlockStateKeys.TriggeredBit: triggered_bit,
            },
        )

    @staticmethod
    def CraftingTable() -> BlockDescriptor:
        """Factory for CraftingTable"""
        return BlockDescriptor("minecraft:crafting_table")

    @staticmethod
    def CreakingHeart(creaking_heart_state: CreakingHeartState, natural: Natural, pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for CreakingHeart"""
        return BlockDescriptor(
            "minecraft:creaking_heart",
            {
                _BlockStateKeys.CreakingHeartState: creaking_heart_state,
                _BlockStateKeys.Natural: natural,
                _BlockStateKeys.PillarAxis: pillar_axis,
            },
        )

    @staticmethod
    def CreeperHead(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CreeperHead"""
        return BlockDescriptor("minecraft:creeper_head", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CrimsonButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CrimsonButton"""
        return BlockDescriptor(
            "minecraft:crimson_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def CrimsonDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for CrimsonDoor"""
        return BlockDescriptor(
            "minecraft:crimson_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def CrimsonDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CrimsonDoubleSlab"""
        return BlockDescriptor("minecraft:crimson_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CrimsonFence() -> BlockDescriptor:
        """Factory for CrimsonFence"""
        return BlockDescriptor("minecraft:crimson_fence")

    @staticmethod
    def CrimsonFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for CrimsonFenceGate"""
        return BlockDescriptor(
            "minecraft:crimson_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def CrimsonFungus() -> BlockDescriptor:
        """Factory for CrimsonFungus"""
        return BlockDescriptor("minecraft:crimson_fungus")

    @staticmethod
    def CrimsonHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for CrimsonHangingSign"""
        return BlockDescriptor(
            "minecraft:crimson_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def CrimsonHyphae(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for CrimsonHyphae"""
        return BlockDescriptor("minecraft:crimson_hyphae", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def CrimsonNylium() -> BlockDescriptor:
        """Factory for CrimsonNylium"""
        return BlockDescriptor("minecraft:crimson_nylium")

    @staticmethod
    def CrimsonPlanks() -> BlockDescriptor:
        """Factory for CrimsonPlanks"""
        return BlockDescriptor("minecraft:crimson_planks")

    @staticmethod
    def CrimsonPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for CrimsonPressurePlate"""
        return BlockDescriptor("minecraft:crimson_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def CrimsonRoots() -> BlockDescriptor:
        """Factory for CrimsonRoots"""
        return BlockDescriptor("minecraft:crimson_roots")

    @staticmethod
    def CrimsonSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CrimsonSlab"""
        return BlockDescriptor("minecraft:crimson_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CrimsonStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for CrimsonStairs"""
        return BlockDescriptor(
            "minecraft:crimson_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CrimsonStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for CrimsonStandingSign"""
        return BlockDescriptor("minecraft:crimson_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def CrimsonStem(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for CrimsonStem"""
        return BlockDescriptor("minecraft:crimson_stem", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def CrimsonTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for CrimsonTrapdoor"""
        return BlockDescriptor(
            "minecraft:crimson_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def CrimsonWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CrimsonWallSign"""
        return BlockDescriptor("minecraft:crimson_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CryingObsidian() -> BlockDescriptor:
        """Factory for CryingObsidian"""
        return BlockDescriptor("minecraft:crying_obsidian")

    @staticmethod
    def CutCopper() -> BlockDescriptor:
        """Factory for CutCopper"""
        return BlockDescriptor("minecraft:cut_copper")

    @staticmethod
    def CutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CutCopperSlab"""
        return BlockDescriptor("minecraft:cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for CutCopperStairs"""
        return BlockDescriptor(
            "minecraft:cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def CutRedSandstone() -> BlockDescriptor:
        """Factory for CutRedSandstone"""
        return BlockDescriptor("minecraft:cut_red_sandstone")

    @staticmethod
    def CutRedSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CutRedSandstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:cut_red_sandstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CutRedSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CutRedSandstoneSlab"""
        return BlockDescriptor(
            "minecraft:cut_red_sandstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CutSandstone() -> BlockDescriptor:
        """Factory for CutSandstone"""
        return BlockDescriptor("minecraft:cut_sandstone")

    @staticmethod
    def CutSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CutSandstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:cut_sandstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def CutSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for CutSandstoneSlab"""
        return BlockDescriptor("minecraft:cut_sandstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def CyanCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for CyanCandle"""
        return BlockDescriptor("minecraft:cyan_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def CyanCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for CyanCandleCake"""
        return BlockDescriptor("minecraft:cyan_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def CyanCarpet() -> BlockDescriptor:
        """Factory for CyanCarpet"""
        return BlockDescriptor("minecraft:cyan_carpet")

    @staticmethod
    def CyanConcrete() -> BlockDescriptor:
        """Factory for CyanConcrete"""
        return BlockDescriptor("minecraft:cyan_concrete")

    @staticmethod
    def CyanConcretePowder() -> BlockDescriptor:
        """Factory for CyanConcretePowder"""
        return BlockDescriptor("minecraft:cyan_concrete_powder")

    @staticmethod
    def CyanGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for CyanGlazedTerracotta"""
        return BlockDescriptor("minecraft:cyan_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def CyanShulkerBox() -> BlockDescriptor:
        """Factory for CyanShulkerBox"""
        return BlockDescriptor("minecraft:cyan_shulker_box")

    @staticmethod
    def CyanStainedGlass() -> BlockDescriptor:
        """Factory for CyanStainedGlass"""
        return BlockDescriptor("minecraft:cyan_stained_glass")

    @staticmethod
    def CyanStainedGlassPane() -> BlockDescriptor:
        """Factory for CyanStainedGlassPane"""
        return BlockDescriptor("minecraft:cyan_stained_glass_pane")

    @staticmethod
    def CyanTerracotta() -> BlockDescriptor:
        """Factory for CyanTerracotta"""
        return BlockDescriptor("minecraft:cyan_terracotta")

    @staticmethod
    def CyanWool() -> BlockDescriptor:
        """Factory for CyanWool"""
        return BlockDescriptor("minecraft:cyan_wool")

    @staticmethod
    def DamagedAnvil(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for DamagedAnvil"""
        return BlockDescriptor(
            "minecraft:damaged_anvil", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def Dandelion() -> BlockDescriptor:
        """Factory for Dandelion"""
        return BlockDescriptor("minecraft:dandelion")

    @staticmethod
    def DarkOakButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for DarkOakButton"""
        return BlockDescriptor(
            "minecraft:dark_oak_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def DarkOakDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for DarkOakDoor"""
        return BlockDescriptor(
            "minecraft:dark_oak_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def DarkOakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DarkOakDoubleSlab"""
        return BlockDescriptor("minecraft:dark_oak_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DarkOakFence() -> BlockDescriptor:
        """Factory for DarkOakFence"""
        return BlockDescriptor("minecraft:dark_oak_fence")

    @staticmethod
    def DarkOakFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for DarkOakFenceGate"""
        return BlockDescriptor(
            "minecraft:dark_oak_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def DarkOakHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for DarkOakHangingSign"""
        return BlockDescriptor(
            "minecraft:dark_oak_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def DarkOakLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for DarkOakLeaves"""
        return BlockDescriptor(
            "minecraft:dark_oak_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def DarkOakLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for DarkOakLog"""
        return BlockDescriptor("minecraft:dark_oak_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def DarkOakPlanks() -> BlockDescriptor:
        """Factory for DarkOakPlanks"""
        return BlockDescriptor("minecraft:dark_oak_planks")

    @staticmethod
    def DarkOakPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for DarkOakPressurePlate"""
        return BlockDescriptor("minecraft:dark_oak_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def DarkOakSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for DarkOakSapling"""
        return BlockDescriptor("minecraft:dark_oak_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def DarkOakSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DarkOakSlab"""
        return BlockDescriptor("minecraft:dark_oak_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DarkOakStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for DarkOakStairs"""
        return BlockDescriptor(
            "minecraft:dark_oak_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DarkOakTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for DarkOakTrapdoor"""
        return BlockDescriptor(
            "minecraft:dark_oak_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def DarkOakWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for DarkOakWood"""
        return BlockDescriptor("minecraft:dark_oak_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def DarkPrismarine() -> BlockDescriptor:
        """Factory for DarkPrismarine"""
        return BlockDescriptor("minecraft:dark_prismarine")

    @staticmethod
    def DarkPrismarineDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DarkPrismarineDoubleSlab"""
        return BlockDescriptor(
            "minecraft:dark_prismarine_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DarkPrismarineSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DarkPrismarineSlab"""
        return BlockDescriptor("minecraft:dark_prismarine_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DarkPrismarineStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for DarkPrismarineStairs"""
        return BlockDescriptor(
            "minecraft:dark_prismarine_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DarkoakStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for DarkoakStandingSign"""
        return BlockDescriptor("minecraft:darkoak_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def DarkoakWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for DarkoakWallSign"""
        return BlockDescriptor("minecraft:darkoak_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def DaylightDetector(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for DaylightDetector"""
        return BlockDescriptor("minecraft:daylight_detector", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def DaylightDetectorInverted(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for DaylightDetectorInverted"""
        return BlockDescriptor("minecraft:daylight_detector_inverted", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def DeadBrainCoral() -> BlockDescriptor:
        """Factory for DeadBrainCoral"""
        return BlockDescriptor("minecraft:dead_brain_coral")

    @staticmethod
    def DeadBrainCoralBlock() -> BlockDescriptor:
        """Factory for DeadBrainCoralBlock"""
        return BlockDescriptor("minecraft:dead_brain_coral_block")

    @staticmethod
    def DeadBrainCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for DeadBrainCoralFan"""
        return BlockDescriptor("minecraft:dead_brain_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadBrainCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for DeadBrainCoralWallFan"""
        return BlockDescriptor("minecraft:dead_brain_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadBubbleCoral() -> BlockDescriptor:
        """Factory for DeadBubbleCoral"""
        return BlockDescriptor("minecraft:dead_bubble_coral")

    @staticmethod
    def DeadBubbleCoralBlock() -> BlockDescriptor:
        """Factory for DeadBubbleCoralBlock"""
        return BlockDescriptor("minecraft:dead_bubble_coral_block")

    @staticmethod
    def DeadBubbleCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for DeadBubbleCoralFan"""
        return BlockDescriptor("minecraft:dead_bubble_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadBubbleCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for DeadBubbleCoralWallFan"""
        return BlockDescriptor("minecraft:dead_bubble_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadFireCoral() -> BlockDescriptor:
        """Factory for DeadFireCoral"""
        return BlockDescriptor("minecraft:dead_fire_coral")

    @staticmethod
    def DeadFireCoralBlock() -> BlockDescriptor:
        """Factory for DeadFireCoralBlock"""
        return BlockDescriptor("minecraft:dead_fire_coral_block")

    @staticmethod
    def DeadFireCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for DeadFireCoralFan"""
        return BlockDescriptor("minecraft:dead_fire_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadFireCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for DeadFireCoralWallFan"""
        return BlockDescriptor("minecraft:dead_fire_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadHornCoral() -> BlockDescriptor:
        """Factory for DeadHornCoral"""
        return BlockDescriptor("minecraft:dead_horn_coral")

    @staticmethod
    def DeadHornCoralBlock() -> BlockDescriptor:
        """Factory for DeadHornCoralBlock"""
        return BlockDescriptor("minecraft:dead_horn_coral_block")

    @staticmethod
    def DeadHornCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for DeadHornCoralFan"""
        return BlockDescriptor("minecraft:dead_horn_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadHornCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for DeadHornCoralWallFan"""
        return BlockDescriptor("minecraft:dead_horn_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def DeadTubeCoral() -> BlockDescriptor:
        """Factory for DeadTubeCoral"""
        return BlockDescriptor("minecraft:dead_tube_coral")

    @staticmethod
    def DeadTubeCoralBlock() -> BlockDescriptor:
        """Factory for DeadTubeCoralBlock"""
        return BlockDescriptor("minecraft:dead_tube_coral_block")

    @staticmethod
    def DeadTubeCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for DeadTubeCoralFan"""
        return BlockDescriptor("minecraft:dead_tube_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def DeadTubeCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for DeadTubeCoralWallFan"""
        return BlockDescriptor("minecraft:dead_tube_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def Deadbush() -> BlockDescriptor:
        """Factory for Deadbush"""
        return BlockDescriptor("minecraft:deadbush")

    @staticmethod
    def DecoratedPot(direction: Direction) -> BlockDescriptor:
        """Factory for DecoratedPot"""
        return BlockDescriptor("minecraft:decorated_pot", {_BlockStateKeys.Direction: direction})

    @staticmethod
    def Deepslate(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for Deepslate"""
        return BlockDescriptor("minecraft:deepslate", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def DeepslateBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DeepslateBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:deepslate_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DeepslateBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DeepslateBrickSlab"""
        return BlockDescriptor("minecraft:deepslate_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DeepslateBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for DeepslateBrickStairs"""
        return BlockDescriptor(
            "minecraft:deepslate_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DeepslateBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for DeepslateBrickWall"""
        return BlockDescriptor(
            "minecraft:deepslate_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def DeepslateBricks() -> BlockDescriptor:
        """Factory for DeepslateBricks"""
        return BlockDescriptor("minecraft:deepslate_bricks")

    @staticmethod
    def DeepslateCoalOre() -> BlockDescriptor:
        """Factory for DeepslateCoalOre"""
        return BlockDescriptor("minecraft:deepslate_coal_ore")

    @staticmethod
    def DeepslateCopperOre() -> BlockDescriptor:
        """Factory for DeepslateCopperOre"""
        return BlockDescriptor("minecraft:deepslate_copper_ore")

    @staticmethod
    def DeepslateDiamondOre() -> BlockDescriptor:
        """Factory for DeepslateDiamondOre"""
        return BlockDescriptor("minecraft:deepslate_diamond_ore")

    @staticmethod
    def DeepslateEmeraldOre() -> BlockDescriptor:
        """Factory for DeepslateEmeraldOre"""
        return BlockDescriptor("minecraft:deepslate_emerald_ore")

    @staticmethod
    def DeepslateGoldOre() -> BlockDescriptor:
        """Factory for DeepslateGoldOre"""
        return BlockDescriptor("minecraft:deepslate_gold_ore")

    @staticmethod
    def DeepslateIronOre() -> BlockDescriptor:
        """Factory for DeepslateIronOre"""
        return BlockDescriptor("minecraft:deepslate_iron_ore")

    @staticmethod
    def DeepslateLapisOre() -> BlockDescriptor:
        """Factory for DeepslateLapisOre"""
        return BlockDescriptor("minecraft:deepslate_lapis_ore")

    @staticmethod
    def DeepslateRedstoneOre() -> BlockDescriptor:
        """Factory for DeepslateRedstoneOre"""
        return BlockDescriptor("minecraft:deepslate_redstone_ore")

    @staticmethod
    def DeepslateTileDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DeepslateTileDoubleSlab"""
        return BlockDescriptor(
            "minecraft:deepslate_tile_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DeepslateTileSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DeepslateTileSlab"""
        return BlockDescriptor("minecraft:deepslate_tile_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DeepslateTileStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for DeepslateTileStairs"""
        return BlockDescriptor(
            "minecraft:deepslate_tile_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DeepslateTileWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for DeepslateTileWall"""
        return BlockDescriptor(
            "minecraft:deepslate_tile_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def DeepslateTiles() -> BlockDescriptor:
        """Factory for DeepslateTiles"""
        return BlockDescriptor("minecraft:deepslate_tiles")

    @staticmethod
    def Deny() -> BlockDescriptor:
        """Factory for Deny"""
        return BlockDescriptor("minecraft:deny")

    @staticmethod
    def DetectorRail(rail_data_bit: RailDataBit, rail_direction: RailDirection) -> BlockDescriptor:
        """Factory for DetectorRail"""
        return BlockDescriptor(
            "minecraft:detector_rail", {_BlockStateKeys.RailDataBit: rail_data_bit, _BlockStateKeys.RailDirection: rail_direction}
        )

    @staticmethod
    def DiamondBlock() -> BlockDescriptor:
        """Factory for DiamondBlock"""
        return BlockDescriptor("minecraft:diamond_block")

    @staticmethod
    def DiamondOre() -> BlockDescriptor:
        """Factory for DiamondOre"""
        return BlockDescriptor("minecraft:diamond_ore")

    @staticmethod
    def Diorite() -> BlockDescriptor:
        """Factory for Diorite"""
        return BlockDescriptor("minecraft:diorite")

    @staticmethod
    def DioriteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DioriteDoubleSlab"""
        return BlockDescriptor("minecraft:diorite_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DioriteSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DioriteSlab"""
        return BlockDescriptor("minecraft:diorite_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def DioriteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for DioriteStairs"""
        return BlockDescriptor(
            "minecraft:diorite_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def DioriteWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for DioriteWall"""
        return BlockDescriptor(
            "minecraft:diorite_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Dirt() -> BlockDescriptor:
        """Factory for Dirt"""
        return BlockDescriptor("minecraft:dirt")

    @staticmethod
    def DirtWithRoots() -> BlockDescriptor:
        """Factory for DirtWithRoots"""
        return BlockDescriptor("minecraft:dirt_with_roots")

    @staticmethod
    def Dispenser(facing_direction: FacingDirection, triggered_bit: TriggeredBit) -> BlockDescriptor:
        """Factory for Dispenser"""
        return BlockDescriptor(
            "minecraft:dispenser",
            {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.TriggeredBit: triggered_bit},
        )

    @staticmethod
    def DoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for DoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def DragonEgg() -> BlockDescriptor:
        """Factory for DragonEgg"""
        return BlockDescriptor("minecraft:dragon_egg")

    @staticmethod
    def DragonHead(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for DragonHead"""
        return BlockDescriptor("minecraft:dragon_head", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def DriedGhast(minecraft_cardinal_direction: CardinalDirection, rehydration_level: RehydrationLevel) -> BlockDescriptor:
        """Factory for DriedGhast"""
        return BlockDescriptor(
            "minecraft:dried_ghast",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.RehydrationLevel: rehydration_level,
            },
        )

    @staticmethod
    def DriedKelpBlock() -> BlockDescriptor:
        """Factory for DriedKelpBlock"""
        return BlockDescriptor("minecraft:dried_kelp_block")

    @staticmethod
    def DripstoneBlock() -> BlockDescriptor:
        """Factory for DripstoneBlock"""
        return BlockDescriptor("minecraft:dripstone_block")

    @staticmethod
    def Dropper(facing_direction: FacingDirection, triggered_bit: TriggeredBit) -> BlockDescriptor:
        """Factory for Dropper"""
        return BlockDescriptor(
            "minecraft:dropper", {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.TriggeredBit: triggered_bit}
        )

    @staticmethod
    def Element0() -> BlockDescriptor:
        """Factory for Element0"""
        return BlockDescriptor("minecraft:element_0")

    @staticmethod
    def Element1() -> BlockDescriptor:
        """Factory for Element1"""
        return BlockDescriptor("minecraft:element_1")

    @staticmethod
    def Element10() -> BlockDescriptor:
        """Factory for Element10"""
        return BlockDescriptor("minecraft:element_10")

    @staticmethod
    def Element100() -> BlockDescriptor:
        """Factory for Element100"""
        return BlockDescriptor("minecraft:element_100")

    @staticmethod
    def Element101() -> BlockDescriptor:
        """Factory for Element101"""
        return BlockDescriptor("minecraft:element_101")

    @staticmethod
    def Element102() -> BlockDescriptor:
        """Factory for Element102"""
        return BlockDescriptor("minecraft:element_102")

    @staticmethod
    def Element103() -> BlockDescriptor:
        """Factory for Element103"""
        return BlockDescriptor("minecraft:element_103")

    @staticmethod
    def Element104() -> BlockDescriptor:
        """Factory for Element104"""
        return BlockDescriptor("minecraft:element_104")

    @staticmethod
    def Element105() -> BlockDescriptor:
        """Factory for Element105"""
        return BlockDescriptor("minecraft:element_105")

    @staticmethod
    def Element106() -> BlockDescriptor:
        """Factory for Element106"""
        return BlockDescriptor("minecraft:element_106")

    @staticmethod
    def Element107() -> BlockDescriptor:
        """Factory for Element107"""
        return BlockDescriptor("minecraft:element_107")

    @staticmethod
    def Element108() -> BlockDescriptor:
        """Factory for Element108"""
        return BlockDescriptor("minecraft:element_108")

    @staticmethod
    def Element109() -> BlockDescriptor:
        """Factory for Element109"""
        return BlockDescriptor("minecraft:element_109")

    @staticmethod
    def Element11() -> BlockDescriptor:
        """Factory for Element11"""
        return BlockDescriptor("minecraft:element_11")

    @staticmethod
    def Element110() -> BlockDescriptor:
        """Factory for Element110"""
        return BlockDescriptor("minecraft:element_110")

    @staticmethod
    def Element111() -> BlockDescriptor:
        """Factory for Element111"""
        return BlockDescriptor("minecraft:element_111")

    @staticmethod
    def Element112() -> BlockDescriptor:
        """Factory for Element112"""
        return BlockDescriptor("minecraft:element_112")

    @staticmethod
    def Element113() -> BlockDescriptor:
        """Factory for Element113"""
        return BlockDescriptor("minecraft:element_113")

    @staticmethod
    def Element114() -> BlockDescriptor:
        """Factory for Element114"""
        return BlockDescriptor("minecraft:element_114")

    @staticmethod
    def Element115() -> BlockDescriptor:
        """Factory for Element115"""
        return BlockDescriptor("minecraft:element_115")

    @staticmethod
    def Element116() -> BlockDescriptor:
        """Factory for Element116"""
        return BlockDescriptor("minecraft:element_116")

    @staticmethod
    def Element117() -> BlockDescriptor:
        """Factory for Element117"""
        return BlockDescriptor("minecraft:element_117")

    @staticmethod
    def Element118() -> BlockDescriptor:
        """Factory for Element118"""
        return BlockDescriptor("minecraft:element_118")

    @staticmethod
    def Element12() -> BlockDescriptor:
        """Factory for Element12"""
        return BlockDescriptor("minecraft:element_12")

    @staticmethod
    def Element13() -> BlockDescriptor:
        """Factory for Element13"""
        return BlockDescriptor("minecraft:element_13")

    @staticmethod
    def Element14() -> BlockDescriptor:
        """Factory for Element14"""
        return BlockDescriptor("minecraft:element_14")

    @staticmethod
    def Element15() -> BlockDescriptor:
        """Factory for Element15"""
        return BlockDescriptor("minecraft:element_15")

    @staticmethod
    def Element16() -> BlockDescriptor:
        """Factory for Element16"""
        return BlockDescriptor("minecraft:element_16")

    @staticmethod
    def Element17() -> BlockDescriptor:
        """Factory for Element17"""
        return BlockDescriptor("minecraft:element_17")

    @staticmethod
    def Element18() -> BlockDescriptor:
        """Factory for Element18"""
        return BlockDescriptor("minecraft:element_18")

    @staticmethod
    def Element19() -> BlockDescriptor:
        """Factory for Element19"""
        return BlockDescriptor("minecraft:element_19")

    @staticmethod
    def Element2() -> BlockDescriptor:
        """Factory for Element2"""
        return BlockDescriptor("minecraft:element_2")

    @staticmethod
    def Element20() -> BlockDescriptor:
        """Factory for Element20"""
        return BlockDescriptor("minecraft:element_20")

    @staticmethod
    def Element21() -> BlockDescriptor:
        """Factory for Element21"""
        return BlockDescriptor("minecraft:element_21")

    @staticmethod
    def Element22() -> BlockDescriptor:
        """Factory for Element22"""
        return BlockDescriptor("minecraft:element_22")

    @staticmethod
    def Element23() -> BlockDescriptor:
        """Factory for Element23"""
        return BlockDescriptor("minecraft:element_23")

    @staticmethod
    def Element24() -> BlockDescriptor:
        """Factory for Element24"""
        return BlockDescriptor("minecraft:element_24")

    @staticmethod
    def Element25() -> BlockDescriptor:
        """Factory for Element25"""
        return BlockDescriptor("minecraft:element_25")

    @staticmethod
    def Element26() -> BlockDescriptor:
        """Factory for Element26"""
        return BlockDescriptor("minecraft:element_26")

    @staticmethod
    def Element27() -> BlockDescriptor:
        """Factory for Element27"""
        return BlockDescriptor("minecraft:element_27")

    @staticmethod
    def Element28() -> BlockDescriptor:
        """Factory for Element28"""
        return BlockDescriptor("minecraft:element_28")

    @staticmethod
    def Element29() -> BlockDescriptor:
        """Factory for Element29"""
        return BlockDescriptor("minecraft:element_29")

    @staticmethod
    def Element3() -> BlockDescriptor:
        """Factory for Element3"""
        return BlockDescriptor("minecraft:element_3")

    @staticmethod
    def Element30() -> BlockDescriptor:
        """Factory for Element30"""
        return BlockDescriptor("minecraft:element_30")

    @staticmethod
    def Element31() -> BlockDescriptor:
        """Factory for Element31"""
        return BlockDescriptor("minecraft:element_31")

    @staticmethod
    def Element32() -> BlockDescriptor:
        """Factory for Element32"""
        return BlockDescriptor("minecraft:element_32")

    @staticmethod
    def Element33() -> BlockDescriptor:
        """Factory for Element33"""
        return BlockDescriptor("minecraft:element_33")

    @staticmethod
    def Element34() -> BlockDescriptor:
        """Factory for Element34"""
        return BlockDescriptor("minecraft:element_34")

    @staticmethod
    def Element35() -> BlockDescriptor:
        """Factory for Element35"""
        return BlockDescriptor("minecraft:element_35")

    @staticmethod
    def Element36() -> BlockDescriptor:
        """Factory for Element36"""
        return BlockDescriptor("minecraft:element_36")

    @staticmethod
    def Element37() -> BlockDescriptor:
        """Factory for Element37"""
        return BlockDescriptor("minecraft:element_37")

    @staticmethod
    def Element38() -> BlockDescriptor:
        """Factory for Element38"""
        return BlockDescriptor("minecraft:element_38")

    @staticmethod
    def Element39() -> BlockDescriptor:
        """Factory for Element39"""
        return BlockDescriptor("minecraft:element_39")

    @staticmethod
    def Element4() -> BlockDescriptor:
        """Factory for Element4"""
        return BlockDescriptor("minecraft:element_4")

    @staticmethod
    def Element40() -> BlockDescriptor:
        """Factory for Element40"""
        return BlockDescriptor("minecraft:element_40")

    @staticmethod
    def Element41() -> BlockDescriptor:
        """Factory for Element41"""
        return BlockDescriptor("minecraft:element_41")

    @staticmethod
    def Element42() -> BlockDescriptor:
        """Factory for Element42"""
        return BlockDescriptor("minecraft:element_42")

    @staticmethod
    def Element43() -> BlockDescriptor:
        """Factory for Element43"""
        return BlockDescriptor("minecraft:element_43")

    @staticmethod
    def Element44() -> BlockDescriptor:
        """Factory for Element44"""
        return BlockDescriptor("minecraft:element_44")

    @staticmethod
    def Element45() -> BlockDescriptor:
        """Factory for Element45"""
        return BlockDescriptor("minecraft:element_45")

    @staticmethod
    def Element46() -> BlockDescriptor:
        """Factory for Element46"""
        return BlockDescriptor("minecraft:element_46")

    @staticmethod
    def Element47() -> BlockDescriptor:
        """Factory for Element47"""
        return BlockDescriptor("minecraft:element_47")

    @staticmethod
    def Element48() -> BlockDescriptor:
        """Factory for Element48"""
        return BlockDescriptor("minecraft:element_48")

    @staticmethod
    def Element49() -> BlockDescriptor:
        """Factory for Element49"""
        return BlockDescriptor("minecraft:element_49")

    @staticmethod
    def Element5() -> BlockDescriptor:
        """Factory for Element5"""
        return BlockDescriptor("minecraft:element_5")

    @staticmethod
    def Element50() -> BlockDescriptor:
        """Factory for Element50"""
        return BlockDescriptor("minecraft:element_50")

    @staticmethod
    def Element51() -> BlockDescriptor:
        """Factory for Element51"""
        return BlockDescriptor("minecraft:element_51")

    @staticmethod
    def Element52() -> BlockDescriptor:
        """Factory for Element52"""
        return BlockDescriptor("minecraft:element_52")

    @staticmethod
    def Element53() -> BlockDescriptor:
        """Factory for Element53"""
        return BlockDescriptor("minecraft:element_53")

    @staticmethod
    def Element54() -> BlockDescriptor:
        """Factory for Element54"""
        return BlockDescriptor("minecraft:element_54")

    @staticmethod
    def Element55() -> BlockDescriptor:
        """Factory for Element55"""
        return BlockDescriptor("minecraft:element_55")

    @staticmethod
    def Element56() -> BlockDescriptor:
        """Factory for Element56"""
        return BlockDescriptor("minecraft:element_56")

    @staticmethod
    def Element57() -> BlockDescriptor:
        """Factory for Element57"""
        return BlockDescriptor("minecraft:element_57")

    @staticmethod
    def Element58() -> BlockDescriptor:
        """Factory for Element58"""
        return BlockDescriptor("minecraft:element_58")

    @staticmethod
    def Element59() -> BlockDescriptor:
        """Factory for Element59"""
        return BlockDescriptor("minecraft:element_59")

    @staticmethod
    def Element6() -> BlockDescriptor:
        """Factory for Element6"""
        return BlockDescriptor("minecraft:element_6")

    @staticmethod
    def Element60() -> BlockDescriptor:
        """Factory for Element60"""
        return BlockDescriptor("minecraft:element_60")

    @staticmethod
    def Element61() -> BlockDescriptor:
        """Factory for Element61"""
        return BlockDescriptor("minecraft:element_61")

    @staticmethod
    def Element62() -> BlockDescriptor:
        """Factory for Element62"""
        return BlockDescriptor("minecraft:element_62")

    @staticmethod
    def Element63() -> BlockDescriptor:
        """Factory for Element63"""
        return BlockDescriptor("minecraft:element_63")

    @staticmethod
    def Element64() -> BlockDescriptor:
        """Factory for Element64"""
        return BlockDescriptor("minecraft:element_64")

    @staticmethod
    def Element65() -> BlockDescriptor:
        """Factory for Element65"""
        return BlockDescriptor("minecraft:element_65")

    @staticmethod
    def Element66() -> BlockDescriptor:
        """Factory for Element66"""
        return BlockDescriptor("minecraft:element_66")

    @staticmethod
    def Element67() -> BlockDescriptor:
        """Factory for Element67"""
        return BlockDescriptor("minecraft:element_67")

    @staticmethod
    def Element68() -> BlockDescriptor:
        """Factory for Element68"""
        return BlockDescriptor("minecraft:element_68")

    @staticmethod
    def Element69() -> BlockDescriptor:
        """Factory for Element69"""
        return BlockDescriptor("minecraft:element_69")

    @staticmethod
    def Element7() -> BlockDescriptor:
        """Factory for Element7"""
        return BlockDescriptor("minecraft:element_7")

    @staticmethod
    def Element70() -> BlockDescriptor:
        """Factory for Element70"""
        return BlockDescriptor("minecraft:element_70")

    @staticmethod
    def Element71() -> BlockDescriptor:
        """Factory for Element71"""
        return BlockDescriptor("minecraft:element_71")

    @staticmethod
    def Element72() -> BlockDescriptor:
        """Factory for Element72"""
        return BlockDescriptor("minecraft:element_72")

    @staticmethod
    def Element73() -> BlockDescriptor:
        """Factory for Element73"""
        return BlockDescriptor("minecraft:element_73")

    @staticmethod
    def Element74() -> BlockDescriptor:
        """Factory for Element74"""
        return BlockDescriptor("minecraft:element_74")

    @staticmethod
    def Element75() -> BlockDescriptor:
        """Factory for Element75"""
        return BlockDescriptor("minecraft:element_75")

    @staticmethod
    def Element76() -> BlockDescriptor:
        """Factory for Element76"""
        return BlockDescriptor("minecraft:element_76")

    @staticmethod
    def Element77() -> BlockDescriptor:
        """Factory for Element77"""
        return BlockDescriptor("minecraft:element_77")

    @staticmethod
    def Element78() -> BlockDescriptor:
        """Factory for Element78"""
        return BlockDescriptor("minecraft:element_78")

    @staticmethod
    def Element79() -> BlockDescriptor:
        """Factory for Element79"""
        return BlockDescriptor("minecraft:element_79")

    @staticmethod
    def Element8() -> BlockDescriptor:
        """Factory for Element8"""
        return BlockDescriptor("minecraft:element_8")

    @staticmethod
    def Element80() -> BlockDescriptor:
        """Factory for Element80"""
        return BlockDescriptor("minecraft:element_80")

    @staticmethod
    def Element81() -> BlockDescriptor:
        """Factory for Element81"""
        return BlockDescriptor("minecraft:element_81")

    @staticmethod
    def Element82() -> BlockDescriptor:
        """Factory for Element82"""
        return BlockDescriptor("minecraft:element_82")

    @staticmethod
    def Element83() -> BlockDescriptor:
        """Factory for Element83"""
        return BlockDescriptor("minecraft:element_83")

    @staticmethod
    def Element84() -> BlockDescriptor:
        """Factory for Element84"""
        return BlockDescriptor("minecraft:element_84")

    @staticmethod
    def Element85() -> BlockDescriptor:
        """Factory for Element85"""
        return BlockDescriptor("minecraft:element_85")

    @staticmethod
    def Element86() -> BlockDescriptor:
        """Factory for Element86"""
        return BlockDescriptor("minecraft:element_86")

    @staticmethod
    def Element87() -> BlockDescriptor:
        """Factory for Element87"""
        return BlockDescriptor("minecraft:element_87")

    @staticmethod
    def Element88() -> BlockDescriptor:
        """Factory for Element88"""
        return BlockDescriptor("minecraft:element_88")

    @staticmethod
    def Element89() -> BlockDescriptor:
        """Factory for Element89"""
        return BlockDescriptor("minecraft:element_89")

    @staticmethod
    def Element9() -> BlockDescriptor:
        """Factory for Element9"""
        return BlockDescriptor("minecraft:element_9")

    @staticmethod
    def Element90() -> BlockDescriptor:
        """Factory for Element90"""
        return BlockDescriptor("minecraft:element_90")

    @staticmethod
    def Element91() -> BlockDescriptor:
        """Factory for Element91"""
        return BlockDescriptor("minecraft:element_91")

    @staticmethod
    def Element92() -> BlockDescriptor:
        """Factory for Element92"""
        return BlockDescriptor("minecraft:element_92")

    @staticmethod
    def Element93() -> BlockDescriptor:
        """Factory for Element93"""
        return BlockDescriptor("minecraft:element_93")

    @staticmethod
    def Element94() -> BlockDescriptor:
        """Factory for Element94"""
        return BlockDescriptor("minecraft:element_94")

    @staticmethod
    def Element95() -> BlockDescriptor:
        """Factory for Element95"""
        return BlockDescriptor("minecraft:element_95")

    @staticmethod
    def Element96() -> BlockDescriptor:
        """Factory for Element96"""
        return BlockDescriptor("minecraft:element_96")

    @staticmethod
    def Element97() -> BlockDescriptor:
        """Factory for Element97"""
        return BlockDescriptor("minecraft:element_97")

    @staticmethod
    def Element98() -> BlockDescriptor:
        """Factory for Element98"""
        return BlockDescriptor("minecraft:element_98")

    @staticmethod
    def Element99() -> BlockDescriptor:
        """Factory for Element99"""
        return BlockDescriptor("minecraft:element_99")

    @staticmethod
    def ElementConstructor(direction: Direction) -> BlockDescriptor:
        """Factory for ElementConstructor"""
        return BlockDescriptor("minecraft:element_constructor", {_BlockStateKeys.Direction: direction})

    @staticmethod
    def EmeraldBlock() -> BlockDescriptor:
        """Factory for EmeraldBlock"""
        return BlockDescriptor("minecraft:emerald_block")

    @staticmethod
    def EmeraldOre() -> BlockDescriptor:
        """Factory for EmeraldOre"""
        return BlockDescriptor("minecraft:emerald_ore")

    @staticmethod
    def EnchantingTable() -> BlockDescriptor:
        """Factory for EnchantingTable"""
        return BlockDescriptor("minecraft:enchanting_table")

    @staticmethod
    def EndBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for EndBrickStairs"""
        return BlockDescriptor(
            "minecraft:end_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def EndBricks() -> BlockDescriptor:
        """Factory for EndBricks"""
        return BlockDescriptor("minecraft:end_bricks")

    @staticmethod
    def EndPortal() -> BlockDescriptor:
        """Factory for EndPortal"""
        return BlockDescriptor("minecraft:end_portal")

    @staticmethod
    def EndPortalFrame(end_portal_eye_bit: EndPortalEyeBit, minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for EndPortalFrame"""
        return BlockDescriptor(
            "minecraft:end_portal_frame",
            {
                _BlockStateKeys.EndPortalEyeBit: end_portal_eye_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def EndRod(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for EndRod"""
        return BlockDescriptor("minecraft:end_rod", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def EndStone() -> BlockDescriptor:
        """Factory for EndStone"""
        return BlockDescriptor("minecraft:end_stone")

    @staticmethod
    def EndStoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for EndStoneBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:end_stone_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def EndStoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for EndStoneBrickSlab"""
        return BlockDescriptor("minecraft:end_stone_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def EndStoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for EndStoneBrickWall"""
        return BlockDescriptor(
            "minecraft:end_stone_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def EnderChest(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for EnderChest"""
        return BlockDescriptor(
            "minecraft:ender_chest", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def ExposedChiseledCopper() -> BlockDescriptor:
        """Factory for ExposedChiseledCopper"""
        return BlockDescriptor("minecraft:exposed_chiseled_copper")

    @staticmethod
    def ExposedCopper() -> BlockDescriptor:
        """Factory for ExposedCopper"""
        return BlockDescriptor("minecraft:exposed_copper")

    @staticmethod
    def ExposedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for ExposedCopperBulb"""
        return BlockDescriptor(
            "minecraft:exposed_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def ExposedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for ExposedCopperDoor"""
        return BlockDescriptor(
            "minecraft:exposed_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def ExposedCopperGrate() -> BlockDescriptor:
        """Factory for ExposedCopperGrate"""
        return BlockDescriptor("minecraft:exposed_copper_grate")

    @staticmethod
    def ExposedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for ExposedCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:exposed_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def ExposedCutCopper() -> BlockDescriptor:
        """Factory for ExposedCutCopper"""
        return BlockDescriptor("minecraft:exposed_cut_copper")

    @staticmethod
    def ExposedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for ExposedCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:exposed_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def ExposedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for ExposedCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:exposed_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def ExposedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for ExposedDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:exposed_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def Farmland(moisturized_amount: MoisturizedAmount) -> BlockDescriptor:
        """Factory for Farmland"""
        return BlockDescriptor("minecraft:farmland", {_BlockStateKeys.MoisturizedAmount: moisturized_amount})

    @staticmethod
    def FenceGate(in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit) -> BlockDescriptor:
        """Factory for FenceGate"""
        return BlockDescriptor(
            "minecraft:fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def Fern() -> BlockDescriptor:
        """Factory for Fern"""
        return BlockDescriptor("minecraft:fern")

    @staticmethod
    def Fire(age: Age) -> BlockDescriptor:
        """Factory for Fire"""
        return BlockDescriptor("minecraft:fire", {_BlockStateKeys.Age: age})

    @staticmethod
    def FireCoral() -> BlockDescriptor:
        """Factory for FireCoral"""
        return BlockDescriptor("minecraft:fire_coral")

    @staticmethod
    def FireCoralBlock() -> BlockDescriptor:
        """Factory for FireCoralBlock"""
        return BlockDescriptor("minecraft:fire_coral_block")

    @staticmethod
    def FireCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for FireCoralFan"""
        return BlockDescriptor("minecraft:fire_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def FireCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for FireCoralWallFan"""
        return BlockDescriptor("minecraft:fire_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def FireflyBush() -> BlockDescriptor:
        """Factory for FireflyBush"""
        return BlockDescriptor("minecraft:firefly_bush")

    @staticmethod
    def FletchingTable() -> BlockDescriptor:
        """Factory for FletchingTable"""
        return BlockDescriptor("minecraft:fletching_table")

    @staticmethod
    def FlowerPot(update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for FlowerPot"""
        return BlockDescriptor("minecraft:flower_pot", {_BlockStateKeys.UpdateBit: update_bit})

    @staticmethod
    def FloweringAzalea() -> BlockDescriptor:
        """Factory for FloweringAzalea"""
        return BlockDescriptor("minecraft:flowering_azalea")

    @staticmethod
    def FlowingLava(liquid_depth: LiquidDepth) -> BlockDescriptor:
        """Factory for FlowingLava"""
        return BlockDescriptor("minecraft:flowing_lava", {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def FlowingWater(liquid_depth: LiquidDepth) -> BlockDescriptor:
        """Factory for FlowingWater"""
        return BlockDescriptor("minecraft:flowing_water", {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def Frame(
        facing_direction: FacingDirection, item_frame_map_bit: ItemFrameMapBit, item_frame_photo_bit: ItemFramePhotoBit
    ) -> BlockDescriptor:
        """Factory for Frame"""
        return BlockDescriptor(
            "minecraft:frame",
            {
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.ItemFrameMapBit: item_frame_map_bit,
                _BlockStateKeys.ItemFramePhotoBit: item_frame_photo_bit,
            },
        )

    @staticmethod
    def FrogSpawn() -> BlockDescriptor:
        """Factory for FrogSpawn"""
        return BlockDescriptor("minecraft:frog_spawn")

    @staticmethod
    def FrostedIce(age: Age) -> BlockDescriptor:
        """Factory for FrostedIce"""
        return BlockDescriptor("minecraft:frosted_ice", {_BlockStateKeys.Age: age})

    @staticmethod
    def Furnace(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Furnace"""
        return BlockDescriptor("minecraft:furnace", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def GildedBlackstone() -> BlockDescriptor:
        """Factory for GildedBlackstone"""
        return BlockDescriptor("minecraft:gilded_blackstone")

    @staticmethod
    def Glass() -> BlockDescriptor:
        """Factory for Glass"""
        return BlockDescriptor("minecraft:glass")

    @staticmethod
    def GlassPane() -> BlockDescriptor:
        """Factory for GlassPane"""
        return BlockDescriptor("minecraft:glass_pane")

    @staticmethod
    def GlowFrame(
        facing_direction: FacingDirection, item_frame_map_bit: ItemFrameMapBit, item_frame_photo_bit: ItemFramePhotoBit
    ) -> BlockDescriptor:
        """Factory for GlowFrame"""
        return BlockDescriptor(
            "minecraft:glow_frame",
            {
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.ItemFrameMapBit: item_frame_map_bit,
                _BlockStateKeys.ItemFramePhotoBit: item_frame_photo_bit,
            },
        )

    @staticmethod
    def GlowLichen(multi_face_direction_bits: MultiFaceDirectionBits) -> BlockDescriptor:
        """Factory for GlowLichen"""
        return BlockDescriptor("minecraft:glow_lichen", {_BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits})

    @staticmethod
    def Glowstone() -> BlockDescriptor:
        """Factory for Glowstone"""
        return BlockDescriptor("minecraft:glowstone")

    @staticmethod
    def GoldBlock() -> BlockDescriptor:
        """Factory for GoldBlock"""
        return BlockDescriptor("minecraft:gold_block")

    @staticmethod
    def GoldOre() -> BlockDescriptor:
        """Factory for GoldOre"""
        return BlockDescriptor("minecraft:gold_ore")

    @staticmethod
    def GoldenRail(rail_data_bit: RailDataBit, rail_direction: RailDirection) -> BlockDescriptor:
        """Factory for GoldenRail"""
        return BlockDescriptor(
            "minecraft:golden_rail", {_BlockStateKeys.RailDataBit: rail_data_bit, _BlockStateKeys.RailDirection: rail_direction}
        )

    @staticmethod
    def Granite() -> BlockDescriptor:
        """Factory for Granite"""
        return BlockDescriptor("minecraft:granite")

    @staticmethod
    def GraniteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for GraniteDoubleSlab"""
        return BlockDescriptor("minecraft:granite_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def GraniteSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for GraniteSlab"""
        return BlockDescriptor("minecraft:granite_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def GraniteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for GraniteStairs"""
        return BlockDescriptor(
            "minecraft:granite_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def GraniteWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for GraniteWall"""
        return BlockDescriptor(
            "minecraft:granite_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def GrassBlock() -> BlockDescriptor:
        """Factory for GrassBlock"""
        return BlockDescriptor("minecraft:grass_block")

    @staticmethod
    def GrassPath() -> BlockDescriptor:
        """Factory for GrassPath"""
        return BlockDescriptor("minecraft:grass_path")

    @staticmethod
    def Gravel() -> BlockDescriptor:
        """Factory for Gravel"""
        return BlockDescriptor("minecraft:gravel")

    @staticmethod
    def GrayCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for GrayCandle"""
        return BlockDescriptor("minecraft:gray_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def GrayCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for GrayCandleCake"""
        return BlockDescriptor("minecraft:gray_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def GrayCarpet() -> BlockDescriptor:
        """Factory for GrayCarpet"""
        return BlockDescriptor("minecraft:gray_carpet")

    @staticmethod
    def GrayConcrete() -> BlockDescriptor:
        """Factory for GrayConcrete"""
        return BlockDescriptor("minecraft:gray_concrete")

    @staticmethod
    def GrayConcretePowder() -> BlockDescriptor:
        """Factory for GrayConcretePowder"""
        return BlockDescriptor("minecraft:gray_concrete_powder")

    @staticmethod
    def GrayGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for GrayGlazedTerracotta"""
        return BlockDescriptor("minecraft:gray_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def GrayShulkerBox() -> BlockDescriptor:
        """Factory for GrayShulkerBox"""
        return BlockDescriptor("minecraft:gray_shulker_box")

    @staticmethod
    def GrayStainedGlass() -> BlockDescriptor:
        """Factory for GrayStainedGlass"""
        return BlockDescriptor("minecraft:gray_stained_glass")

    @staticmethod
    def GrayStainedGlassPane() -> BlockDescriptor:
        """Factory for GrayStainedGlassPane"""
        return BlockDescriptor("minecraft:gray_stained_glass_pane")

    @staticmethod
    def GrayTerracotta() -> BlockDescriptor:
        """Factory for GrayTerracotta"""
        return BlockDescriptor("minecraft:gray_terracotta")

    @staticmethod
    def GrayWool() -> BlockDescriptor:
        """Factory for GrayWool"""
        return BlockDescriptor("minecraft:gray_wool")

    @staticmethod
    def GreenCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for GreenCandle"""
        return BlockDescriptor("minecraft:green_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def GreenCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for GreenCandleCake"""
        return BlockDescriptor("minecraft:green_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def GreenCarpet() -> BlockDescriptor:
        """Factory for GreenCarpet"""
        return BlockDescriptor("minecraft:green_carpet")

    @staticmethod
    def GreenConcrete() -> BlockDescriptor:
        """Factory for GreenConcrete"""
        return BlockDescriptor("minecraft:green_concrete")

    @staticmethod
    def GreenConcretePowder() -> BlockDescriptor:
        """Factory for GreenConcretePowder"""
        return BlockDescriptor("minecraft:green_concrete_powder")

    @staticmethod
    def GreenGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for GreenGlazedTerracotta"""
        return BlockDescriptor("minecraft:green_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def GreenShulkerBox() -> BlockDescriptor:
        """Factory for GreenShulkerBox"""
        return BlockDescriptor("minecraft:green_shulker_box")

    @staticmethod
    def GreenStainedGlass() -> BlockDescriptor:
        """Factory for GreenStainedGlass"""
        return BlockDescriptor("minecraft:green_stained_glass")

    @staticmethod
    def GreenStainedGlassPane() -> BlockDescriptor:
        """Factory for GreenStainedGlassPane"""
        return BlockDescriptor("minecraft:green_stained_glass_pane")

    @staticmethod
    def GreenTerracotta() -> BlockDescriptor:
        """Factory for GreenTerracotta"""
        return BlockDescriptor("minecraft:green_terracotta")

    @staticmethod
    def GreenWool() -> BlockDescriptor:
        """Factory for GreenWool"""
        return BlockDescriptor("minecraft:green_wool")

    @staticmethod
    def Grindstone(attachment: Attachment, direction: Direction) -> BlockDescriptor:
        """Factory for Grindstone"""
        return BlockDescriptor(
            "minecraft:grindstone", {_BlockStateKeys.Attachment: attachment, _BlockStateKeys.Direction: direction}
        )

    @staticmethod
    def HangingRoots() -> BlockDescriptor:
        """Factory for HangingRoots"""
        return BlockDescriptor("minecraft:hanging_roots")

    @staticmethod
    def HardBlackStainedGlass() -> BlockDescriptor:
        """Factory for HardBlackStainedGlass"""
        return BlockDescriptor("minecraft:hard_black_stained_glass")

    @staticmethod
    def HardBlackStainedGlassPane() -> BlockDescriptor:
        """Factory for HardBlackStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_black_stained_glass_pane")

    @staticmethod
    def HardBlueStainedGlass() -> BlockDescriptor:
        """Factory for HardBlueStainedGlass"""
        return BlockDescriptor("minecraft:hard_blue_stained_glass")

    @staticmethod
    def HardBlueStainedGlassPane() -> BlockDescriptor:
        """Factory for HardBlueStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_blue_stained_glass_pane")

    @staticmethod
    def HardBrownStainedGlass() -> BlockDescriptor:
        """Factory for HardBrownStainedGlass"""
        return BlockDescriptor("minecraft:hard_brown_stained_glass")

    @staticmethod
    def HardBrownStainedGlassPane() -> BlockDescriptor:
        """Factory for HardBrownStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_brown_stained_glass_pane")

    @staticmethod
    def HardCyanStainedGlass() -> BlockDescriptor:
        """Factory for HardCyanStainedGlass"""
        return BlockDescriptor("minecraft:hard_cyan_stained_glass")

    @staticmethod
    def HardCyanStainedGlassPane() -> BlockDescriptor:
        """Factory for HardCyanStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_cyan_stained_glass_pane")

    @staticmethod
    def HardGlass() -> BlockDescriptor:
        """Factory for HardGlass"""
        return BlockDescriptor("minecraft:hard_glass")

    @staticmethod
    def HardGlassPane() -> BlockDescriptor:
        """Factory for HardGlassPane"""
        return BlockDescriptor("minecraft:hard_glass_pane")

    @staticmethod
    def HardGrayStainedGlass() -> BlockDescriptor:
        """Factory for HardGrayStainedGlass"""
        return BlockDescriptor("minecraft:hard_gray_stained_glass")

    @staticmethod
    def HardGrayStainedGlassPane() -> BlockDescriptor:
        """Factory for HardGrayStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_gray_stained_glass_pane")

    @staticmethod
    def HardGreenStainedGlass() -> BlockDescriptor:
        """Factory for HardGreenStainedGlass"""
        return BlockDescriptor("minecraft:hard_green_stained_glass")

    @staticmethod
    def HardGreenStainedGlassPane() -> BlockDescriptor:
        """Factory for HardGreenStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_green_stained_glass_pane")

    @staticmethod
    def HardLightBlueStainedGlass() -> BlockDescriptor:
        """Factory for HardLightBlueStainedGlass"""
        return BlockDescriptor("minecraft:hard_light_blue_stained_glass")

    @staticmethod
    def HardLightBlueStainedGlassPane() -> BlockDescriptor:
        """Factory for HardLightBlueStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_light_blue_stained_glass_pane")

    @staticmethod
    def HardLightGrayStainedGlass() -> BlockDescriptor:
        """Factory for HardLightGrayStainedGlass"""
        return BlockDescriptor("minecraft:hard_light_gray_stained_glass")

    @staticmethod
    def HardLightGrayStainedGlassPane() -> BlockDescriptor:
        """Factory for HardLightGrayStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_light_gray_stained_glass_pane")

    @staticmethod
    def HardLimeStainedGlass() -> BlockDescriptor:
        """Factory for HardLimeStainedGlass"""
        return BlockDescriptor("minecraft:hard_lime_stained_glass")

    @staticmethod
    def HardLimeStainedGlassPane() -> BlockDescriptor:
        """Factory for HardLimeStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_lime_stained_glass_pane")

    @staticmethod
    def HardMagentaStainedGlass() -> BlockDescriptor:
        """Factory for HardMagentaStainedGlass"""
        return BlockDescriptor("minecraft:hard_magenta_stained_glass")

    @staticmethod
    def HardMagentaStainedGlassPane() -> BlockDescriptor:
        """Factory for HardMagentaStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_magenta_stained_glass_pane")

    @staticmethod
    def HardOrangeStainedGlass() -> BlockDescriptor:
        """Factory for HardOrangeStainedGlass"""
        return BlockDescriptor("minecraft:hard_orange_stained_glass")

    @staticmethod
    def HardOrangeStainedGlassPane() -> BlockDescriptor:
        """Factory for HardOrangeStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_orange_stained_glass_pane")

    @staticmethod
    def HardPinkStainedGlass() -> BlockDescriptor:
        """Factory for HardPinkStainedGlass"""
        return BlockDescriptor("minecraft:hard_pink_stained_glass")

    @staticmethod
    def HardPinkStainedGlassPane() -> BlockDescriptor:
        """Factory for HardPinkStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_pink_stained_glass_pane")

    @staticmethod
    def HardPurpleStainedGlass() -> BlockDescriptor:
        """Factory for HardPurpleStainedGlass"""
        return BlockDescriptor("minecraft:hard_purple_stained_glass")

    @staticmethod
    def HardPurpleStainedGlassPane() -> BlockDescriptor:
        """Factory for HardPurpleStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_purple_stained_glass_pane")

    @staticmethod
    def HardRedStainedGlass() -> BlockDescriptor:
        """Factory for HardRedStainedGlass"""
        return BlockDescriptor("minecraft:hard_red_stained_glass")

    @staticmethod
    def HardRedStainedGlassPane() -> BlockDescriptor:
        """Factory for HardRedStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_red_stained_glass_pane")

    @staticmethod
    def HardWhiteStainedGlass() -> BlockDescriptor:
        """Factory for HardWhiteStainedGlass"""
        return BlockDescriptor("minecraft:hard_white_stained_glass")

    @staticmethod
    def HardWhiteStainedGlassPane() -> BlockDescriptor:
        """Factory for HardWhiteStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_white_stained_glass_pane")

    @staticmethod
    def HardYellowStainedGlass() -> BlockDescriptor:
        """Factory for HardYellowStainedGlass"""
        return BlockDescriptor("minecraft:hard_yellow_stained_glass")

    @staticmethod
    def HardYellowStainedGlassPane() -> BlockDescriptor:
        """Factory for HardYellowStainedGlassPane"""
        return BlockDescriptor("minecraft:hard_yellow_stained_glass_pane")

    @staticmethod
    def HardenedClay() -> BlockDescriptor:
        """Factory for HardenedClay"""
        return BlockDescriptor("minecraft:hardened_clay")

    @staticmethod
    def HayBlock(deprecated: Deprecated, pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for HayBlock"""
        return BlockDescriptor(
            "minecraft:hay_block", {_BlockStateKeys.Deprecated: deprecated, _BlockStateKeys.PillarAxis: pillar_axis}
        )

    @staticmethod
    def HeavyCore() -> BlockDescriptor:
        """Factory for HeavyCore"""
        return BlockDescriptor("minecraft:heavy_core")

    @staticmethod
    def HeavyWeightedPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for HeavyWeightedPressurePlate"""
        return BlockDescriptor("minecraft:heavy_weighted_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def HoneyBlock() -> BlockDescriptor:
        """Factory for HoneyBlock"""
        return BlockDescriptor("minecraft:honey_block")

    @staticmethod
    def HoneycombBlock() -> BlockDescriptor:
        """Factory for HoneycombBlock"""
        return BlockDescriptor("minecraft:honeycomb_block")

    @staticmethod
    def Hopper(facing_direction: FacingDirection, toggle_bit: ToggleBit) -> BlockDescriptor:
        """Factory for Hopper"""
        return BlockDescriptor(
            "minecraft:hopper", {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.ToggleBit: toggle_bit}
        )

    @staticmethod
    def HornCoral() -> BlockDescriptor:
        """Factory for HornCoral"""
        return BlockDescriptor("minecraft:horn_coral")

    @staticmethod
    def HornCoralBlock() -> BlockDescriptor:
        """Factory for HornCoralBlock"""
        return BlockDescriptor("minecraft:horn_coral_block")

    @staticmethod
    def HornCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for HornCoralFan"""
        return BlockDescriptor("minecraft:horn_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def HornCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for HornCoralWallFan"""
        return BlockDescriptor("minecraft:horn_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def Ice() -> BlockDescriptor:
        """Factory for Ice"""
        return BlockDescriptor("minecraft:ice")

    @staticmethod
    def InfestedChiseledStoneBricks() -> BlockDescriptor:
        """Factory for InfestedChiseledStoneBricks"""
        return BlockDescriptor("minecraft:infested_chiseled_stone_bricks")

    @staticmethod
    def InfestedCobblestone() -> BlockDescriptor:
        """Factory for InfestedCobblestone"""
        return BlockDescriptor("minecraft:infested_cobblestone")

    @staticmethod
    def InfestedCrackedStoneBricks() -> BlockDescriptor:
        """Factory for InfestedCrackedStoneBricks"""
        return BlockDescriptor("minecraft:infested_cracked_stone_bricks")

    @staticmethod
    def InfestedDeepslate(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for InfestedDeepslate"""
        return BlockDescriptor("minecraft:infested_deepslate", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def InfestedMossyStoneBricks() -> BlockDescriptor:
        """Factory for InfestedMossyStoneBricks"""
        return BlockDescriptor("minecraft:infested_mossy_stone_bricks")

    @staticmethod
    def InfestedStone() -> BlockDescriptor:
        """Factory for InfestedStone"""
        return BlockDescriptor("minecraft:infested_stone")

    @staticmethod
    def InfestedStoneBricks() -> BlockDescriptor:
        """Factory for InfestedStoneBricks"""
        return BlockDescriptor("minecraft:infested_stone_bricks")

    @staticmethod
    def IronBars() -> BlockDescriptor:
        """Factory for IronBars"""
        return BlockDescriptor("minecraft:iron_bars")

    @staticmethod
    def IronBlock() -> BlockDescriptor:
        """Factory for IronBlock"""
        return BlockDescriptor("minecraft:iron_block")

    @staticmethod
    def IronDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for IronDoor"""
        return BlockDescriptor(
            "minecraft:iron_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def IronOre() -> BlockDescriptor:
        """Factory for IronOre"""
        return BlockDescriptor("minecraft:iron_ore")

    @staticmethod
    def IronTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for IronTrapdoor"""
        return BlockDescriptor(
            "minecraft:iron_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def Jigsaw(facing_direction: FacingDirection, rotation: Rotation) -> BlockDescriptor:
        """Factory for Jigsaw"""
        return BlockDescriptor(
            "minecraft:jigsaw", {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.Rotation: rotation}
        )

    @staticmethod
    def Jukebox() -> BlockDescriptor:
        """Factory for Jukebox"""
        return BlockDescriptor("minecraft:jukebox")

    @staticmethod
    def JungleButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for JungleButton"""
        return BlockDescriptor(
            "minecraft:jungle_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def JungleDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for JungleDoor"""
        return BlockDescriptor(
            "minecraft:jungle_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def JungleDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for JungleDoubleSlab"""
        return BlockDescriptor("minecraft:jungle_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def JungleFence() -> BlockDescriptor:
        """Factory for JungleFence"""
        return BlockDescriptor("minecraft:jungle_fence")

    @staticmethod
    def JungleFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for JungleFenceGate"""
        return BlockDescriptor(
            "minecraft:jungle_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def JungleHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for JungleHangingSign"""
        return BlockDescriptor(
            "minecraft:jungle_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def JungleLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for JungleLeaves"""
        return BlockDescriptor(
            "minecraft:jungle_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def JungleLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for JungleLog"""
        return BlockDescriptor("minecraft:jungle_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def JunglePlanks() -> BlockDescriptor:
        """Factory for JunglePlanks"""
        return BlockDescriptor("minecraft:jungle_planks")

    @staticmethod
    def JunglePressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for JunglePressurePlate"""
        return BlockDescriptor("minecraft:jungle_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def JungleSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for JungleSapling"""
        return BlockDescriptor("minecraft:jungle_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def JungleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for JungleSlab"""
        return BlockDescriptor("minecraft:jungle_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def JungleStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for JungleStairs"""
        return BlockDescriptor(
            "minecraft:jungle_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def JungleStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for JungleStandingSign"""
        return BlockDescriptor("minecraft:jungle_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def JungleTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for JungleTrapdoor"""
        return BlockDescriptor(
            "minecraft:jungle_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def JungleWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for JungleWallSign"""
        return BlockDescriptor("minecraft:jungle_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def JungleWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for JungleWood"""
        return BlockDescriptor("minecraft:jungle_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Kelp(kelp_age: KelpAge) -> BlockDescriptor:
        """Factory for Kelp"""
        return BlockDescriptor("minecraft:kelp", {_BlockStateKeys.KelpAge: kelp_age})

    @staticmethod
    def LabTable(direction: Direction) -> BlockDescriptor:
        """Factory for LabTable"""
        return BlockDescriptor("minecraft:lab_table", {_BlockStateKeys.Direction: direction})

    @staticmethod
    def Ladder(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for Ladder"""
        return BlockDescriptor("minecraft:ladder", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Lantern(hanging: Hanging) -> BlockDescriptor:
        """Factory for Lantern"""
        return BlockDescriptor("minecraft:lantern", {_BlockStateKeys.Hanging: hanging})

    @staticmethod
    def LapisBlock() -> BlockDescriptor:
        """Factory for LapisBlock"""
        return BlockDescriptor("minecraft:lapis_block")

    @staticmethod
    def LapisOre() -> BlockDescriptor:
        """Factory for LapisOre"""
        return BlockDescriptor("minecraft:lapis_ore")

    @staticmethod
    def LargeAmethystBud(minecraft_block_face: BlockFace) -> BlockDescriptor:
        """Factory for LargeAmethystBud"""
        return BlockDescriptor("minecraft:large_amethyst_bud", {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def LargeFern(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for LargeFern"""
        return BlockDescriptor("minecraft:large_fern", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def Lava(liquid_depth: LiquidDepth) -> BlockDescriptor:
        """Factory for Lava"""
        return BlockDescriptor("minecraft:lava", {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def LeafLitter(growth: Growth, minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for LeafLitter"""
        return BlockDescriptor(
            "minecraft:leaf_litter",
            {_BlockStateKeys.Growth: growth, _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
        )

    @staticmethod
    def Lectern(minecraft_cardinal_direction: CardinalDirection, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for Lectern"""
        return BlockDescriptor(
            "minecraft:lectern",
            {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction, _BlockStateKeys.PoweredBit: powered_bit},
        )

    @staticmethod
    def Lever(lever_direction: LeverDirection, open_bit: OpenBit) -> BlockDescriptor:
        """Factory for Lever"""
        return BlockDescriptor(
            "minecraft:lever", {_BlockStateKeys.LeverDirection: lever_direction, _BlockStateKeys.OpenBit: open_bit}
        )

    @staticmethod
    def LightBlock0() -> BlockDescriptor:
        """Factory for LightBlock0"""
        return BlockDescriptor("minecraft:light_block_0")

    @staticmethod
    def LightBlock1() -> BlockDescriptor:
        """Factory for LightBlock1"""
        return BlockDescriptor("minecraft:light_block_1")

    @staticmethod
    def LightBlock10() -> BlockDescriptor:
        """Factory for LightBlock10"""
        return BlockDescriptor("minecraft:light_block_10")

    @staticmethod
    def LightBlock11() -> BlockDescriptor:
        """Factory for LightBlock11"""
        return BlockDescriptor("minecraft:light_block_11")

    @staticmethod
    def LightBlock12() -> BlockDescriptor:
        """Factory for LightBlock12"""
        return BlockDescriptor("minecraft:light_block_12")

    @staticmethod
    def LightBlock13() -> BlockDescriptor:
        """Factory for LightBlock13"""
        return BlockDescriptor("minecraft:light_block_13")

    @staticmethod
    def LightBlock14() -> BlockDescriptor:
        """Factory for LightBlock14"""
        return BlockDescriptor("minecraft:light_block_14")

    @staticmethod
    def LightBlock15() -> BlockDescriptor:
        """Factory for LightBlock15"""
        return BlockDescriptor("minecraft:light_block_15")

    @staticmethod
    def LightBlock2() -> BlockDescriptor:
        """Factory for LightBlock2"""
        return BlockDescriptor("minecraft:light_block_2")

    @staticmethod
    def LightBlock3() -> BlockDescriptor:
        """Factory for LightBlock3"""
        return BlockDescriptor("minecraft:light_block_3")

    @staticmethod
    def LightBlock4() -> BlockDescriptor:
        """Factory for LightBlock4"""
        return BlockDescriptor("minecraft:light_block_4")

    @staticmethod
    def LightBlock5() -> BlockDescriptor:
        """Factory for LightBlock5"""
        return BlockDescriptor("minecraft:light_block_5")

    @staticmethod
    def LightBlock6() -> BlockDescriptor:
        """Factory for LightBlock6"""
        return BlockDescriptor("minecraft:light_block_6")

    @staticmethod
    def LightBlock7() -> BlockDescriptor:
        """Factory for LightBlock7"""
        return BlockDescriptor("minecraft:light_block_7")

    @staticmethod
    def LightBlock8() -> BlockDescriptor:
        """Factory for LightBlock8"""
        return BlockDescriptor("minecraft:light_block_8")

    @staticmethod
    def LightBlock9() -> BlockDescriptor:
        """Factory for LightBlock9"""
        return BlockDescriptor("minecraft:light_block_9")

    @staticmethod
    def LightBlueCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for LightBlueCandle"""
        return BlockDescriptor("minecraft:light_blue_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def LightBlueCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for LightBlueCandleCake"""
        return BlockDescriptor("minecraft:light_blue_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def LightBlueCarpet() -> BlockDescriptor:
        """Factory for LightBlueCarpet"""
        return BlockDescriptor("minecraft:light_blue_carpet")

    @staticmethod
    def LightBlueConcrete() -> BlockDescriptor:
        """Factory for LightBlueConcrete"""
        return BlockDescriptor("minecraft:light_blue_concrete")

    @staticmethod
    def LightBlueConcretePowder() -> BlockDescriptor:
        """Factory for LightBlueConcretePowder"""
        return BlockDescriptor("minecraft:light_blue_concrete_powder")

    @staticmethod
    def LightBlueGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for LightBlueGlazedTerracotta"""
        return BlockDescriptor("minecraft:light_blue_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def LightBlueShulkerBox() -> BlockDescriptor:
        """Factory for LightBlueShulkerBox"""
        return BlockDescriptor("minecraft:light_blue_shulker_box")

    @staticmethod
    def LightBlueStainedGlass() -> BlockDescriptor:
        """Factory for LightBlueStainedGlass"""
        return BlockDescriptor("minecraft:light_blue_stained_glass")

    @staticmethod
    def LightBlueStainedGlassPane() -> BlockDescriptor:
        """Factory for LightBlueStainedGlassPane"""
        return BlockDescriptor("minecraft:light_blue_stained_glass_pane")

    @staticmethod
    def LightBlueTerracotta() -> BlockDescriptor:
        """Factory for LightBlueTerracotta"""
        return BlockDescriptor("minecraft:light_blue_terracotta")

    @staticmethod
    def LightBlueWool() -> BlockDescriptor:
        """Factory for LightBlueWool"""
        return BlockDescriptor("minecraft:light_blue_wool")

    @staticmethod
    def LightGrayCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for LightGrayCandle"""
        return BlockDescriptor("minecraft:light_gray_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def LightGrayCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for LightGrayCandleCake"""
        return BlockDescriptor("minecraft:light_gray_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def LightGrayCarpet() -> BlockDescriptor:
        """Factory for LightGrayCarpet"""
        return BlockDescriptor("minecraft:light_gray_carpet")

    @staticmethod
    def LightGrayConcrete() -> BlockDescriptor:
        """Factory for LightGrayConcrete"""
        return BlockDescriptor("minecraft:light_gray_concrete")

    @staticmethod
    def LightGrayConcretePowder() -> BlockDescriptor:
        """Factory for LightGrayConcretePowder"""
        return BlockDescriptor("minecraft:light_gray_concrete_powder")

    @staticmethod
    def LightGrayShulkerBox() -> BlockDescriptor:
        """Factory for LightGrayShulkerBox"""
        return BlockDescriptor("minecraft:light_gray_shulker_box")

    @staticmethod
    def LightGrayStainedGlass() -> BlockDescriptor:
        """Factory for LightGrayStainedGlass"""
        return BlockDescriptor("minecraft:light_gray_stained_glass")

    @staticmethod
    def LightGrayStainedGlassPane() -> BlockDescriptor:
        """Factory for LightGrayStainedGlassPane"""
        return BlockDescriptor("minecraft:light_gray_stained_glass_pane")

    @staticmethod
    def LightGrayTerracotta() -> BlockDescriptor:
        """Factory for LightGrayTerracotta"""
        return BlockDescriptor("minecraft:light_gray_terracotta")

    @staticmethod
    def LightGrayWool() -> BlockDescriptor:
        """Factory for LightGrayWool"""
        return BlockDescriptor("minecraft:light_gray_wool")

    @staticmethod
    def LightWeightedPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for LightWeightedPressurePlate"""
        return BlockDescriptor("minecraft:light_weighted_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def LightningRod(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for LightningRod"""
        return BlockDescriptor("minecraft:lightning_rod", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Lilac(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for Lilac"""
        return BlockDescriptor("minecraft:lilac", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def LilyOfTheValley() -> BlockDescriptor:
        """Factory for LilyOfTheValley"""
        return BlockDescriptor("minecraft:lily_of_the_valley")

    @staticmethod
    def LimeCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for LimeCandle"""
        return BlockDescriptor("minecraft:lime_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def LimeCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for LimeCandleCake"""
        return BlockDescriptor("minecraft:lime_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def LimeCarpet() -> BlockDescriptor:
        """Factory for LimeCarpet"""
        return BlockDescriptor("minecraft:lime_carpet")

    @staticmethod
    def LimeConcrete() -> BlockDescriptor:
        """Factory for LimeConcrete"""
        return BlockDescriptor("minecraft:lime_concrete")

    @staticmethod
    def LimeConcretePowder() -> BlockDescriptor:
        """Factory for LimeConcretePowder"""
        return BlockDescriptor("minecraft:lime_concrete_powder")

    @staticmethod
    def LimeGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for LimeGlazedTerracotta"""
        return BlockDescriptor("minecraft:lime_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def LimeShulkerBox() -> BlockDescriptor:
        """Factory for LimeShulkerBox"""
        return BlockDescriptor("minecraft:lime_shulker_box")

    @staticmethod
    def LimeStainedGlass() -> BlockDescriptor:
        """Factory for LimeStainedGlass"""
        return BlockDescriptor("minecraft:lime_stained_glass")

    @staticmethod
    def LimeStainedGlassPane() -> BlockDescriptor:
        """Factory for LimeStainedGlassPane"""
        return BlockDescriptor("minecraft:lime_stained_glass_pane")

    @staticmethod
    def LimeTerracotta() -> BlockDescriptor:
        """Factory for LimeTerracotta"""
        return BlockDescriptor("minecraft:lime_terracotta")

    @staticmethod
    def LimeWool() -> BlockDescriptor:
        """Factory for LimeWool"""
        return BlockDescriptor("minecraft:lime_wool")

    @staticmethod
    def LitBlastFurnace(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for LitBlastFurnace"""
        return BlockDescriptor(
            "minecraft:lit_blast_furnace", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def LitDeepslateRedstoneOre() -> BlockDescriptor:
        """Factory for LitDeepslateRedstoneOre"""
        return BlockDescriptor("minecraft:lit_deepslate_redstone_ore")

    @staticmethod
    def LitFurnace(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for LitFurnace"""
        return BlockDescriptor(
            "minecraft:lit_furnace", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def LitPumpkin(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for LitPumpkin"""
        return BlockDescriptor(
            "minecraft:lit_pumpkin", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def LitRedstoneLamp() -> BlockDescriptor:
        """Factory for LitRedstoneLamp"""
        return BlockDescriptor("minecraft:lit_redstone_lamp")

    @staticmethod
    def LitRedstoneOre() -> BlockDescriptor:
        """Factory for LitRedstoneOre"""
        return BlockDescriptor("minecraft:lit_redstone_ore")

    @staticmethod
    def LitSmoker(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for LitSmoker"""
        return BlockDescriptor("minecraft:lit_smoker", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def Lodestone() -> BlockDescriptor:
        """Factory for Lodestone"""
        return BlockDescriptor("minecraft:lodestone")

    @staticmethod
    def Loom(direction: Direction) -> BlockDescriptor:
        """Factory for Loom"""
        return BlockDescriptor("minecraft:loom", {_BlockStateKeys.Direction: direction})

    @staticmethod
    def MagentaCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for MagentaCandle"""
        return BlockDescriptor("minecraft:magenta_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def MagentaCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for MagentaCandleCake"""
        return BlockDescriptor("minecraft:magenta_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def MagentaCarpet() -> BlockDescriptor:
        """Factory for MagentaCarpet"""
        return BlockDescriptor("minecraft:magenta_carpet")

    @staticmethod
    def MagentaConcrete() -> BlockDescriptor:
        """Factory for MagentaConcrete"""
        return BlockDescriptor("minecraft:magenta_concrete")

    @staticmethod
    def MagentaConcretePowder() -> BlockDescriptor:
        """Factory for MagentaConcretePowder"""
        return BlockDescriptor("minecraft:magenta_concrete_powder")

    @staticmethod
    def MagentaGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for MagentaGlazedTerracotta"""
        return BlockDescriptor("minecraft:magenta_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def MagentaShulkerBox() -> BlockDescriptor:
        """Factory for MagentaShulkerBox"""
        return BlockDescriptor("minecraft:magenta_shulker_box")

    @staticmethod
    def MagentaStainedGlass() -> BlockDescriptor:
        """Factory for MagentaStainedGlass"""
        return BlockDescriptor("minecraft:magenta_stained_glass")

    @staticmethod
    def MagentaStainedGlassPane() -> BlockDescriptor:
        """Factory for MagentaStainedGlassPane"""
        return BlockDescriptor("minecraft:magenta_stained_glass_pane")

    @staticmethod
    def MagentaTerracotta() -> BlockDescriptor:
        """Factory for MagentaTerracotta"""
        return BlockDescriptor("minecraft:magenta_terracotta")

    @staticmethod
    def MagentaWool() -> BlockDescriptor:
        """Factory for MagentaWool"""
        return BlockDescriptor("minecraft:magenta_wool")

    @staticmethod
    def Magma() -> BlockDescriptor:
        """Factory for Magma"""
        return BlockDescriptor("minecraft:magma")

    @staticmethod
    def MangroveButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for MangroveButton"""
        return BlockDescriptor(
            "minecraft:mangrove_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def MangroveDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for MangroveDoor"""
        return BlockDescriptor(
            "minecraft:mangrove_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def MangroveDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MangroveDoubleSlab"""
        return BlockDescriptor("minecraft:mangrove_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def MangroveFence() -> BlockDescriptor:
        """Factory for MangroveFence"""
        return BlockDescriptor("minecraft:mangrove_fence")

    @staticmethod
    def MangroveFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for MangroveFenceGate"""
        return BlockDescriptor(
            "minecraft:mangrove_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def MangroveHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for MangroveHangingSign"""
        return BlockDescriptor(
            "minecraft:mangrove_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def MangroveLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for MangroveLeaves"""
        return BlockDescriptor(
            "minecraft:mangrove_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def MangroveLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for MangroveLog"""
        return BlockDescriptor("minecraft:mangrove_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def MangrovePlanks() -> BlockDescriptor:
        """Factory for MangrovePlanks"""
        return BlockDescriptor("minecraft:mangrove_planks")

    @staticmethod
    def MangrovePressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for MangrovePressurePlate"""
        return BlockDescriptor("minecraft:mangrove_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def MangrovePropagule(hanging: Hanging, propagule_stage: PropaguleStage) -> BlockDescriptor:
        """Factory for MangrovePropagule"""
        return BlockDescriptor(
            "minecraft:mangrove_propagule", {_BlockStateKeys.Hanging: hanging, _BlockStateKeys.PropaguleStage: propagule_stage}
        )

    @staticmethod
    def MangroveRoots() -> BlockDescriptor:
        """Factory for MangroveRoots"""
        return BlockDescriptor("minecraft:mangrove_roots")

    @staticmethod
    def MangroveSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MangroveSlab"""
        return BlockDescriptor("minecraft:mangrove_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def MangroveStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for MangroveStairs"""
        return BlockDescriptor(
            "minecraft:mangrove_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MangroveStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for MangroveStandingSign"""
        return BlockDescriptor("minecraft:mangrove_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def MangroveTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for MangroveTrapdoor"""
        return BlockDescriptor(
            "minecraft:mangrove_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def MangroveWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for MangroveWallSign"""
        return BlockDescriptor("minecraft:mangrove_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def MangroveWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for MangroveWood"""
        return BlockDescriptor("minecraft:mangrove_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def MaterialReducer(direction: Direction) -> BlockDescriptor:
        """Factory for MaterialReducer"""
        return BlockDescriptor("minecraft:material_reducer", {_BlockStateKeys.Direction: direction})

    @staticmethod
    def MediumAmethystBud(minecraft_block_face: BlockFace) -> BlockDescriptor:
        """Factory for MediumAmethystBud"""
        return BlockDescriptor("minecraft:medium_amethyst_bud", {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def MelonBlock() -> BlockDescriptor:
        """Factory for MelonBlock"""
        return BlockDescriptor("minecraft:melon_block")

    @staticmethod
    def MelonStem(facing_direction: FacingDirection, growth: Growth) -> BlockDescriptor:
        """Factory for MelonStem"""
        return BlockDescriptor(
            "minecraft:melon_stem", {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.Growth: growth}
        )

    @staticmethod
    def MobSpawner() -> BlockDescriptor:
        """Factory for MobSpawner"""
        return BlockDescriptor("minecraft:mob_spawner")

    @staticmethod
    def MossBlock() -> BlockDescriptor:
        """Factory for MossBlock"""
        return BlockDescriptor("minecraft:moss_block")

    @staticmethod
    def MossCarpet() -> BlockDescriptor:
        """Factory for MossCarpet"""
        return BlockDescriptor("minecraft:moss_carpet")

    @staticmethod
    def MossyCobblestone() -> BlockDescriptor:
        """Factory for MossyCobblestone"""
        return BlockDescriptor("minecraft:mossy_cobblestone")

    @staticmethod
    def MossyCobblestoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MossyCobblestoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:mossy_cobblestone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyCobblestoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MossyCobblestoneSlab"""
        return BlockDescriptor(
            "minecraft:mossy_cobblestone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyCobblestoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for MossyCobblestoneStairs"""
        return BlockDescriptor(
            "minecraft:mossy_cobblestone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MossyCobblestoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for MossyCobblestoneWall"""
        return BlockDescriptor(
            "minecraft:mossy_cobblestone_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def MossyStoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MossyStoneBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:mossy_stone_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyStoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MossyStoneBrickSlab"""
        return BlockDescriptor(
            "minecraft:mossy_stone_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MossyStoneBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for MossyStoneBrickStairs"""
        return BlockDescriptor(
            "minecraft:mossy_stone_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MossyStoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for MossyStoneBrickWall"""
        return BlockDescriptor(
            "minecraft:mossy_stone_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def MossyStoneBricks() -> BlockDescriptor:
        """Factory for MossyStoneBricks"""
        return BlockDescriptor("minecraft:mossy_stone_bricks")

    @staticmethod
    def Mud() -> BlockDescriptor:
        """Factory for Mud"""
        return BlockDescriptor("minecraft:mud")

    @staticmethod
    def MudBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MudBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:mud_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def MudBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for MudBrickSlab"""
        return BlockDescriptor("minecraft:mud_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def MudBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for MudBrickStairs"""
        return BlockDescriptor(
            "minecraft:mud_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def MudBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for MudBrickWall"""
        return BlockDescriptor(
            "minecraft:mud_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def MudBricks() -> BlockDescriptor:
        """Factory for MudBricks"""
        return BlockDescriptor("minecraft:mud_bricks")

    @staticmethod
    def MuddyMangroveRoots(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for MuddyMangroveRoots"""
        return BlockDescriptor("minecraft:muddy_mangrove_roots", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def MushroomStem(huge_mushroom_bits: HugeMushroomBits) -> BlockDescriptor:
        """Factory for MushroomStem"""
        return BlockDescriptor("minecraft:mushroom_stem", {_BlockStateKeys.HugeMushroomBits: huge_mushroom_bits})

    @staticmethod
    def Mycelium() -> BlockDescriptor:
        """Factory for Mycelium"""
        return BlockDescriptor("minecraft:mycelium")

    @staticmethod
    def NetherBrick() -> BlockDescriptor:
        """Factory for NetherBrick"""
        return BlockDescriptor("minecraft:nether_brick")

    @staticmethod
    def NetherBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for NetherBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:nether_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def NetherBrickFence() -> BlockDescriptor:
        """Factory for NetherBrickFence"""
        return BlockDescriptor("minecraft:nether_brick_fence")

    @staticmethod
    def NetherBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for NetherBrickSlab"""
        return BlockDescriptor("minecraft:nether_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def NetherBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for NetherBrickStairs"""
        return BlockDescriptor(
            "minecraft:nether_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def NetherBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for NetherBrickWall"""
        return BlockDescriptor(
            "minecraft:nether_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def NetherGoldOre() -> BlockDescriptor:
        """Factory for NetherGoldOre"""
        return BlockDescriptor("minecraft:nether_gold_ore")

    @staticmethod
    def NetherSprouts() -> BlockDescriptor:
        """Factory for NetherSprouts"""
        return BlockDescriptor("minecraft:nether_sprouts")

    @staticmethod
    def NetherWart(age: Age) -> BlockDescriptor:
        """Factory for NetherWart"""
        return BlockDescriptor("minecraft:nether_wart", {_BlockStateKeys.Age: age})

    @staticmethod
    def NetherWartBlock() -> BlockDescriptor:
        """Factory for NetherWartBlock"""
        return BlockDescriptor("minecraft:nether_wart_block")

    @staticmethod
    def NetheriteBlock() -> BlockDescriptor:
        """Factory for NetheriteBlock"""
        return BlockDescriptor("minecraft:netherite_block")

    @staticmethod
    def Netherrack() -> BlockDescriptor:
        """Factory for Netherrack"""
        return BlockDescriptor("minecraft:netherrack")

    @staticmethod
    def NormalStoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for NormalStoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:normal_stone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def NormalStoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for NormalStoneSlab"""
        return BlockDescriptor("minecraft:normal_stone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def NormalStoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for NormalStoneStairs"""
        return BlockDescriptor(
            "minecraft:normal_stone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def Noteblock() -> BlockDescriptor:
        """Factory for Noteblock"""
        return BlockDescriptor("minecraft:noteblock")

    @staticmethod
    def OakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for OakDoubleSlab"""
        return BlockDescriptor("minecraft:oak_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def OakFence() -> BlockDescriptor:
        """Factory for OakFence"""
        return BlockDescriptor("minecraft:oak_fence")

    @staticmethod
    def OakHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for OakHangingSign"""
        return BlockDescriptor(
            "minecraft:oak_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def OakLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for OakLeaves"""
        return BlockDescriptor(
            "minecraft:oak_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def OakLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for OakLog"""
        return BlockDescriptor("minecraft:oak_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def OakPlanks() -> BlockDescriptor:
        """Factory for OakPlanks"""
        return BlockDescriptor("minecraft:oak_planks")

    @staticmethod
    def OakSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for OakSapling"""
        return BlockDescriptor("minecraft:oak_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def OakSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for OakSlab"""
        return BlockDescriptor("minecraft:oak_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def OakStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for OakStairs"""
        return BlockDescriptor(
            "minecraft:oak_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def OakWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for OakWood"""
        return BlockDescriptor("minecraft:oak_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Observer(facing_direction: FacingDirection, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for Observer"""
        return BlockDescriptor(
            "minecraft:observer",
            {_BlockStateKeys.MinecraftFacingDirection: facing_direction, _BlockStateKeys.PoweredBit: powered_bit},
        )

    @staticmethod
    def Obsidian() -> BlockDescriptor:
        """Factory for Obsidian"""
        return BlockDescriptor("minecraft:obsidian")

    @staticmethod
    def OchreFroglight(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for OchreFroglight"""
        return BlockDescriptor("minecraft:ochre_froglight", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def OpenEyeblossom() -> BlockDescriptor:
        """Factory for OpenEyeblossom"""
        return BlockDescriptor("minecraft:open_eyeblossom")

    @staticmethod
    def OrangeCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for OrangeCandle"""
        return BlockDescriptor("minecraft:orange_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def OrangeCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for OrangeCandleCake"""
        return BlockDescriptor("minecraft:orange_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def OrangeCarpet() -> BlockDescriptor:
        """Factory for OrangeCarpet"""
        return BlockDescriptor("minecraft:orange_carpet")

    @staticmethod
    def OrangeConcrete() -> BlockDescriptor:
        """Factory for OrangeConcrete"""
        return BlockDescriptor("minecraft:orange_concrete")

    @staticmethod
    def OrangeConcretePowder() -> BlockDescriptor:
        """Factory for OrangeConcretePowder"""
        return BlockDescriptor("minecraft:orange_concrete_powder")

    @staticmethod
    def OrangeGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for OrangeGlazedTerracotta"""
        return BlockDescriptor("minecraft:orange_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def OrangeShulkerBox() -> BlockDescriptor:
        """Factory for OrangeShulkerBox"""
        return BlockDescriptor("minecraft:orange_shulker_box")

    @staticmethod
    def OrangeStainedGlass() -> BlockDescriptor:
        """Factory for OrangeStainedGlass"""
        return BlockDescriptor("minecraft:orange_stained_glass")

    @staticmethod
    def OrangeStainedGlassPane() -> BlockDescriptor:
        """Factory for OrangeStainedGlassPane"""
        return BlockDescriptor("minecraft:orange_stained_glass_pane")

    @staticmethod
    def OrangeTerracotta() -> BlockDescriptor:
        """Factory for OrangeTerracotta"""
        return BlockDescriptor("minecraft:orange_terracotta")

    @staticmethod
    def OrangeTulip() -> BlockDescriptor:
        """Factory for OrangeTulip"""
        return BlockDescriptor("minecraft:orange_tulip")

    @staticmethod
    def OrangeWool() -> BlockDescriptor:
        """Factory for OrangeWool"""
        return BlockDescriptor("minecraft:orange_wool")

    @staticmethod
    def OxeyeDaisy() -> BlockDescriptor:
        """Factory for OxeyeDaisy"""
        return BlockDescriptor("minecraft:oxeye_daisy")

    @staticmethod
    def OxidizedChiseledCopper() -> BlockDescriptor:
        """Factory for OxidizedChiseledCopper"""
        return BlockDescriptor("minecraft:oxidized_chiseled_copper")

    @staticmethod
    def OxidizedCopper() -> BlockDescriptor:
        """Factory for OxidizedCopper"""
        return BlockDescriptor("minecraft:oxidized_copper")

    @staticmethod
    def OxidizedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for OxidizedCopperBulb"""
        return BlockDescriptor(
            "minecraft:oxidized_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def OxidizedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for OxidizedCopperDoor"""
        return BlockDescriptor(
            "minecraft:oxidized_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def OxidizedCopperGrate() -> BlockDescriptor:
        """Factory for OxidizedCopperGrate"""
        return BlockDescriptor("minecraft:oxidized_copper_grate")

    @staticmethod
    def OxidizedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for OxidizedCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:oxidized_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def OxidizedCutCopper() -> BlockDescriptor:
        """Factory for OxidizedCutCopper"""
        return BlockDescriptor("minecraft:oxidized_cut_copper")

    @staticmethod
    def OxidizedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for OxidizedCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:oxidized_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def OxidizedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for OxidizedCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:oxidized_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def OxidizedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for OxidizedDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:oxidized_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PackedIce() -> BlockDescriptor:
        """Factory for PackedIce"""
        return BlockDescriptor("minecraft:packed_ice")

    @staticmethod
    def PackedMud() -> BlockDescriptor:
        """Factory for PackedMud"""
        return BlockDescriptor("minecraft:packed_mud")

    @staticmethod
    def PaleHangingMoss(tip: Tip) -> BlockDescriptor:
        """Factory for PaleHangingMoss"""
        return BlockDescriptor("minecraft:pale_hanging_moss", {_BlockStateKeys.Tip: tip})

    @staticmethod
    def PaleMossBlock() -> BlockDescriptor:
        """Factory for PaleMossBlock"""
        return BlockDescriptor("minecraft:pale_moss_block")

    @staticmethod
    def PaleMossCarpet(
        pale_moss_carpet_side_east: PaleMossCarpetSideEast,
        pale_moss_carpet_side_north: PaleMossCarpetSideNorth,
        pale_moss_carpet_side_south: PaleMossCarpetSideSouth,
        pale_moss_carpet_side_west: PaleMossCarpetSideWest,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for PaleMossCarpet"""
        return BlockDescriptor(
            "minecraft:pale_moss_carpet",
            {
                _BlockStateKeys.PaleMossCarpetSideEast: pale_moss_carpet_side_east,
                _BlockStateKeys.PaleMossCarpetSideNorth: pale_moss_carpet_side_north,
                _BlockStateKeys.PaleMossCarpetSideSouth: pale_moss_carpet_side_south,
                _BlockStateKeys.PaleMossCarpetSideWest: pale_moss_carpet_side_west,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def PaleOakButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PaleOakButton"""
        return BlockDescriptor(
            "minecraft:pale_oak_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def PaleOakDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for PaleOakDoor"""
        return BlockDescriptor(
            "minecraft:pale_oak_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def PaleOakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PaleOakDoubleSlab"""
        return BlockDescriptor("minecraft:pale_oak_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PaleOakFence() -> BlockDescriptor:
        """Factory for PaleOakFence"""
        return BlockDescriptor("minecraft:pale_oak_fence")

    @staticmethod
    def PaleOakFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for PaleOakFenceGate"""
        return BlockDescriptor(
            "minecraft:pale_oak_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def PaleOakHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for PaleOakHangingSign"""
        return BlockDescriptor(
            "minecraft:pale_oak_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def PaleOakLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for PaleOakLeaves"""
        return BlockDescriptor(
            "minecraft:pale_oak_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def PaleOakLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for PaleOakLog"""
        return BlockDescriptor("minecraft:pale_oak_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PaleOakPlanks() -> BlockDescriptor:
        """Factory for PaleOakPlanks"""
        return BlockDescriptor("minecraft:pale_oak_planks")

    @staticmethod
    def PaleOakPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for PaleOakPressurePlate"""
        return BlockDescriptor("minecraft:pale_oak_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def PaleOakSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for PaleOakSapling"""
        return BlockDescriptor("minecraft:pale_oak_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def PaleOakSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PaleOakSlab"""
        return BlockDescriptor("minecraft:pale_oak_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PaleOakStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PaleOakStairs"""
        return BlockDescriptor(
            "minecraft:pale_oak_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PaleOakStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for PaleOakStandingSign"""
        return BlockDescriptor("minecraft:pale_oak_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def PaleOakTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for PaleOakTrapdoor"""
        return BlockDescriptor(
            "minecraft:pale_oak_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def PaleOakWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PaleOakWallSign"""
        return BlockDescriptor("minecraft:pale_oak_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PaleOakWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for PaleOakWood"""
        return BlockDescriptor("minecraft:pale_oak_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PearlescentFroglight(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for PearlescentFroglight"""
        return BlockDescriptor("minecraft:pearlescent_froglight", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Peony(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for Peony"""
        return BlockDescriptor("minecraft:peony", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def PetrifiedOakDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PetrifiedOakDoubleSlab"""
        return BlockDescriptor(
            "minecraft:petrified_oak_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PetrifiedOakSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PetrifiedOakSlab"""
        return BlockDescriptor("minecraft:petrified_oak_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PiglinHead(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PiglinHead"""
        return BlockDescriptor("minecraft:piglin_head", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PinkCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for PinkCandle"""
        return BlockDescriptor("minecraft:pink_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def PinkCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for PinkCandleCake"""
        return BlockDescriptor("minecraft:pink_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def PinkCarpet() -> BlockDescriptor:
        """Factory for PinkCarpet"""
        return BlockDescriptor("minecraft:pink_carpet")

    @staticmethod
    def PinkConcrete() -> BlockDescriptor:
        """Factory for PinkConcrete"""
        return BlockDescriptor("minecraft:pink_concrete")

    @staticmethod
    def PinkConcretePowder() -> BlockDescriptor:
        """Factory for PinkConcretePowder"""
        return BlockDescriptor("minecraft:pink_concrete_powder")

    @staticmethod
    def PinkGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PinkGlazedTerracotta"""
        return BlockDescriptor("minecraft:pink_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PinkPetals(growth: Growth, minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for PinkPetals"""
        return BlockDescriptor(
            "minecraft:pink_petals",
            {_BlockStateKeys.Growth: growth, _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
        )

    @staticmethod
    def PinkShulkerBox() -> BlockDescriptor:
        """Factory for PinkShulkerBox"""
        return BlockDescriptor("minecraft:pink_shulker_box")

    @staticmethod
    def PinkStainedGlass() -> BlockDescriptor:
        """Factory for PinkStainedGlass"""
        return BlockDescriptor("minecraft:pink_stained_glass")

    @staticmethod
    def PinkStainedGlassPane() -> BlockDescriptor:
        """Factory for PinkStainedGlassPane"""
        return BlockDescriptor("minecraft:pink_stained_glass_pane")

    @staticmethod
    def PinkTerracotta() -> BlockDescriptor:
        """Factory for PinkTerracotta"""
        return BlockDescriptor("minecraft:pink_terracotta")

    @staticmethod
    def PinkTulip() -> BlockDescriptor:
        """Factory for PinkTulip"""
        return BlockDescriptor("minecraft:pink_tulip")

    @staticmethod
    def PinkWool() -> BlockDescriptor:
        """Factory for PinkWool"""
        return BlockDescriptor("minecraft:pink_wool")

    @staticmethod
    def Piston(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for Piston"""
        return BlockDescriptor("minecraft:piston", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PistonArmCollision(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PistonArmCollision"""
        return BlockDescriptor("minecraft:piston_arm_collision", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PitcherCrop(growth: Growth, upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for PitcherCrop"""
        return BlockDescriptor(
            "minecraft:pitcher_crop", {_BlockStateKeys.Growth: growth, _BlockStateKeys.UpperBlockBit: upper_block_bit}
        )

    @staticmethod
    def PitcherPlant(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for PitcherPlant"""
        return BlockDescriptor("minecraft:pitcher_plant", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def PlayerHead(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PlayerHead"""
        return BlockDescriptor("minecraft:player_head", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Podzol() -> BlockDescriptor:
        """Factory for Podzol"""
        return BlockDescriptor("minecraft:podzol")

    @staticmethod
    def PointedDripstone(dripstone_thickness: DripstoneThickness, hanging: Hanging) -> BlockDescriptor:
        """Factory for PointedDripstone"""
        return BlockDescriptor(
            "minecraft:pointed_dripstone",
            {_BlockStateKeys.DripstoneThickness: dripstone_thickness, _BlockStateKeys.Hanging: hanging},
        )

    @staticmethod
    def PolishedAndesite() -> BlockDescriptor:
        """Factory for PolishedAndesite"""
        return BlockDescriptor("minecraft:polished_andesite")

    @staticmethod
    def PolishedAndesiteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedAndesiteDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_andesite_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedAndesiteSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedAndesiteSlab"""
        return BlockDescriptor(
            "minecraft:polished_andesite_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedAndesiteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedAndesiteStairs"""
        return BlockDescriptor(
            "minecraft:polished_andesite_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedBasalt(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for PolishedBasalt"""
        return BlockDescriptor("minecraft:polished_basalt", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PolishedBlackstone() -> BlockDescriptor:
        """Factory for PolishedBlackstone"""
        return BlockDescriptor("minecraft:polished_blackstone")

    @staticmethod
    def PolishedBlackstoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedBlackstoneBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedBlackstoneBrickSlab"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstoneBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedBlackstoneBrickStairs"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedBlackstoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for PolishedBlackstoneBrickWall"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def PolishedBlackstoneBricks() -> BlockDescriptor:
        """Factory for PolishedBlackstoneBricks"""
        return BlockDescriptor("minecraft:polished_blackstone_bricks")

    @staticmethod
    def PolishedBlackstoneButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PolishedBlackstoneButton"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def PolishedBlackstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedBlackstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstonePressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for PolishedBlackstonePressurePlate"""
        return BlockDescriptor("minecraft:polished_blackstone_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def PolishedBlackstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedBlackstoneSlab"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedBlackstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedBlackstoneStairs"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedBlackstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for PolishedBlackstoneWall"""
        return BlockDescriptor(
            "minecraft:polished_blackstone_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def PolishedDeepslate() -> BlockDescriptor:
        """Factory for PolishedDeepslate"""
        return BlockDescriptor("minecraft:polished_deepslate")

    @staticmethod
    def PolishedDeepslateDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedDeepslateDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_deepslate_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDeepslateSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedDeepslateSlab"""
        return BlockDescriptor(
            "minecraft:polished_deepslate_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDeepslateStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedDeepslateStairs"""
        return BlockDescriptor(
            "minecraft:polished_deepslate_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedDeepslateWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for PolishedDeepslateWall"""
        return BlockDescriptor(
            "minecraft:polished_deepslate_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def PolishedDiorite() -> BlockDescriptor:
        """Factory for PolishedDiorite"""
        return BlockDescriptor("minecraft:polished_diorite")

    @staticmethod
    def PolishedDioriteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedDioriteDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_diorite_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDioriteSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedDioriteSlab"""
        return BlockDescriptor(
            "minecraft:polished_diorite_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedDioriteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedDioriteStairs"""
        return BlockDescriptor(
            "minecraft:polished_diorite_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedGranite() -> BlockDescriptor:
        """Factory for PolishedGranite"""
        return BlockDescriptor("minecraft:polished_granite")

    @staticmethod
    def PolishedGraniteDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedGraniteDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_granite_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedGraniteSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedGraniteSlab"""
        return BlockDescriptor(
            "minecraft:polished_granite_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedGraniteStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedGraniteStairs"""
        return BlockDescriptor(
            "minecraft:polished_granite_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedTuff() -> BlockDescriptor:
        """Factory for PolishedTuff"""
        return BlockDescriptor("minecraft:polished_tuff")

    @staticmethod
    def PolishedTuffDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedTuffDoubleSlab"""
        return BlockDescriptor(
            "minecraft:polished_tuff_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PolishedTuffSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PolishedTuffSlab"""
        return BlockDescriptor("minecraft:polished_tuff_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PolishedTuffStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PolishedTuffStairs"""
        return BlockDescriptor(
            "minecraft:polished_tuff_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PolishedTuffWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for PolishedTuffWall"""
        return BlockDescriptor(
            "minecraft:polished_tuff_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Poppy() -> BlockDescriptor:
        """Factory for Poppy"""
        return BlockDescriptor("minecraft:poppy")

    @staticmethod
    def Portal(portal_axis: PortalAxis) -> BlockDescriptor:
        """Factory for Portal"""
        return BlockDescriptor("minecraft:portal", {_BlockStateKeys.PortalAxis: portal_axis})

    @staticmethod
    def Potatoes(growth: Growth) -> BlockDescriptor:
        """Factory for Potatoes"""
        return BlockDescriptor("minecraft:potatoes", {_BlockStateKeys.Growth: growth})

    @staticmethod
    def PowderSnow() -> BlockDescriptor:
        """Factory for PowderSnow"""
        return BlockDescriptor("minecraft:powder_snow")

    @staticmethod
    def PoweredComparator(
        minecraft_cardinal_direction: CardinalDirection, output_lit_bit: OutputLitBit, output_subtract_bit: OutputSubtractBit
    ) -> BlockDescriptor:
        """Factory for PoweredComparator"""
        return BlockDescriptor(
            "minecraft:powered_comparator",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OutputLitBit: output_lit_bit,
                _BlockStateKeys.OutputSubtractBit: output_subtract_bit,
            },
        )

    @staticmethod
    def PoweredRepeater(minecraft_cardinal_direction: CardinalDirection, repeater_delay: RepeaterDelay) -> BlockDescriptor:
        """Factory for PoweredRepeater"""
        return BlockDescriptor(
            "minecraft:powered_repeater",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.RepeaterDelay: repeater_delay,
            },
        )

    @staticmethod
    def Prismarine() -> BlockDescriptor:
        """Factory for Prismarine"""
        return BlockDescriptor("minecraft:prismarine")

    @staticmethod
    def PrismarineBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PrismarineBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:prismarine_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PrismarineBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PrismarineBrickSlab"""
        return BlockDescriptor(
            "minecraft:prismarine_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PrismarineBricks() -> BlockDescriptor:
        """Factory for PrismarineBricks"""
        return BlockDescriptor("minecraft:prismarine_bricks")

    @staticmethod
    def PrismarineBricksStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PrismarineBricksStairs"""
        return BlockDescriptor(
            "minecraft:prismarine_bricks_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PrismarineDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PrismarineDoubleSlab"""
        return BlockDescriptor(
            "minecraft:prismarine_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def PrismarineSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PrismarineSlab"""
        return BlockDescriptor("minecraft:prismarine_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PrismarineStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PrismarineStairs"""
        return BlockDescriptor(
            "minecraft:prismarine_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def PrismarineWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for PrismarineWall"""
        return BlockDescriptor(
            "minecraft:prismarine_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Pumpkin(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Pumpkin"""
        return BlockDescriptor("minecraft:pumpkin", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def PumpkinStem(facing_direction: FacingDirection, growth: Growth) -> BlockDescriptor:
        """Factory for PumpkinStem"""
        return BlockDescriptor(
            "minecraft:pumpkin_stem", {_BlockStateKeys.FacingDirection: facing_direction, _BlockStateKeys.Growth: growth}
        )

    @staticmethod
    def PurpleCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for PurpleCandle"""
        return BlockDescriptor("minecraft:purple_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def PurpleCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for PurpleCandleCake"""
        return BlockDescriptor("minecraft:purple_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def PurpleCarpet() -> BlockDescriptor:
        """Factory for PurpleCarpet"""
        return BlockDescriptor("minecraft:purple_carpet")

    @staticmethod
    def PurpleConcrete() -> BlockDescriptor:
        """Factory for PurpleConcrete"""
        return BlockDescriptor("minecraft:purple_concrete")

    @staticmethod
    def PurpleConcretePowder() -> BlockDescriptor:
        """Factory for PurpleConcretePowder"""
        return BlockDescriptor("minecraft:purple_concrete_powder")

    @staticmethod
    def PurpleGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for PurpleGlazedTerracotta"""
        return BlockDescriptor("minecraft:purple_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def PurpleShulkerBox() -> BlockDescriptor:
        """Factory for PurpleShulkerBox"""
        return BlockDescriptor("minecraft:purple_shulker_box")

    @staticmethod
    def PurpleStainedGlass() -> BlockDescriptor:
        """Factory for PurpleStainedGlass"""
        return BlockDescriptor("minecraft:purple_stained_glass")

    @staticmethod
    def PurpleStainedGlassPane() -> BlockDescriptor:
        """Factory for PurpleStainedGlassPane"""
        return BlockDescriptor("minecraft:purple_stained_glass_pane")

    @staticmethod
    def PurpleTerracotta() -> BlockDescriptor:
        """Factory for PurpleTerracotta"""
        return BlockDescriptor("minecraft:purple_terracotta")

    @staticmethod
    def PurpleWool() -> BlockDescriptor:
        """Factory for PurpleWool"""
        return BlockDescriptor("minecraft:purple_wool")

    @staticmethod
    def PurpurBlock(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for PurpurBlock"""
        return BlockDescriptor("minecraft:purpur_block", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PurpurDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PurpurDoubleSlab"""
        return BlockDescriptor("minecraft:purpur_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PurpurPillar(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for PurpurPillar"""
        return BlockDescriptor("minecraft:purpur_pillar", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def PurpurSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for PurpurSlab"""
        return BlockDescriptor("minecraft:purpur_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def PurpurStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for PurpurStairs"""
        return BlockDescriptor(
            "minecraft:purpur_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def QuartzBlock(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for QuartzBlock"""
        return BlockDescriptor("minecraft:quartz_block", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def QuartzBricks() -> BlockDescriptor:
        """Factory for QuartzBricks"""
        return BlockDescriptor("minecraft:quartz_bricks")

    @staticmethod
    def QuartzDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for QuartzDoubleSlab"""
        return BlockDescriptor("minecraft:quartz_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def QuartzOre() -> BlockDescriptor:
        """Factory for QuartzOre"""
        return BlockDescriptor("minecraft:quartz_ore")

    @staticmethod
    def QuartzPillar(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for QuartzPillar"""
        return BlockDescriptor("minecraft:quartz_pillar", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def QuartzSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for QuartzSlab"""
        return BlockDescriptor("minecraft:quartz_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def QuartzStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for QuartzStairs"""
        return BlockDescriptor(
            "minecraft:quartz_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def Rail(rail_direction: RailDirection) -> BlockDescriptor:
        """Factory for Rail"""
        return BlockDescriptor("minecraft:rail", {_BlockStateKeys.RailDirection: rail_direction})

    @staticmethod
    def RawCopperBlock() -> BlockDescriptor:
        """Factory for RawCopperBlock"""
        return BlockDescriptor("minecraft:raw_copper_block")

    @staticmethod
    def RawGoldBlock() -> BlockDescriptor:
        """Factory for RawGoldBlock"""
        return BlockDescriptor("minecraft:raw_gold_block")

    @staticmethod
    def RawIronBlock() -> BlockDescriptor:
        """Factory for RawIronBlock"""
        return BlockDescriptor("minecraft:raw_iron_block")

    @staticmethod
    def RedCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for RedCandle"""
        return BlockDescriptor("minecraft:red_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def RedCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for RedCandleCake"""
        return BlockDescriptor("minecraft:red_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def RedCarpet() -> BlockDescriptor:
        """Factory for RedCarpet"""
        return BlockDescriptor("minecraft:red_carpet")

    @staticmethod
    def RedConcrete() -> BlockDescriptor:
        """Factory for RedConcrete"""
        return BlockDescriptor("minecraft:red_concrete")

    @staticmethod
    def RedConcretePowder() -> BlockDescriptor:
        """Factory for RedConcretePowder"""
        return BlockDescriptor("minecraft:red_concrete_powder")

    @staticmethod
    def RedGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for RedGlazedTerracotta"""
        return BlockDescriptor("minecraft:red_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def RedMushroom() -> BlockDescriptor:
        """Factory for RedMushroom"""
        return BlockDescriptor("minecraft:red_mushroom")

    @staticmethod
    def RedMushroomBlock(huge_mushroom_bits: HugeMushroomBits) -> BlockDescriptor:
        """Factory for RedMushroomBlock"""
        return BlockDescriptor("minecraft:red_mushroom_block", {_BlockStateKeys.HugeMushroomBits: huge_mushroom_bits})

    @staticmethod
    def RedNetherBrick() -> BlockDescriptor:
        """Factory for RedNetherBrick"""
        return BlockDescriptor("minecraft:red_nether_brick")

    @staticmethod
    def RedNetherBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for RedNetherBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:red_nether_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def RedNetherBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for RedNetherBrickSlab"""
        return BlockDescriptor(
            "minecraft:red_nether_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def RedNetherBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for RedNetherBrickStairs"""
        return BlockDescriptor(
            "minecraft:red_nether_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def RedNetherBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for RedNetherBrickWall"""
        return BlockDescriptor(
            "minecraft:red_nether_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def RedSand() -> BlockDescriptor:
        """Factory for RedSand"""
        return BlockDescriptor("minecraft:red_sand")

    @staticmethod
    def RedSandstone() -> BlockDescriptor:
        """Factory for RedSandstone"""
        return BlockDescriptor("minecraft:red_sandstone")

    @staticmethod
    def RedSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for RedSandstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:red_sandstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def RedSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for RedSandstoneSlab"""
        return BlockDescriptor("minecraft:red_sandstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def RedSandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for RedSandstoneStairs"""
        return BlockDescriptor(
            "minecraft:red_sandstone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def RedSandstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for RedSandstoneWall"""
        return BlockDescriptor(
            "minecraft:red_sandstone_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def RedShulkerBox() -> BlockDescriptor:
        """Factory for RedShulkerBox"""
        return BlockDescriptor("minecraft:red_shulker_box")

    @staticmethod
    def RedStainedGlass() -> BlockDescriptor:
        """Factory for RedStainedGlass"""
        return BlockDescriptor("minecraft:red_stained_glass")

    @staticmethod
    def RedStainedGlassPane() -> BlockDescriptor:
        """Factory for RedStainedGlassPane"""
        return BlockDescriptor("minecraft:red_stained_glass_pane")

    @staticmethod
    def RedTerracotta() -> BlockDescriptor:
        """Factory for RedTerracotta"""
        return BlockDescriptor("minecraft:red_terracotta")

    @staticmethod
    def RedTulip() -> BlockDescriptor:
        """Factory for RedTulip"""
        return BlockDescriptor("minecraft:red_tulip")

    @staticmethod
    def RedWool() -> BlockDescriptor:
        """Factory for RedWool"""
        return BlockDescriptor("minecraft:red_wool")

    @staticmethod
    def RedstoneBlock() -> BlockDescriptor:
        """Factory for RedstoneBlock"""
        return BlockDescriptor("minecraft:redstone_block")

    @staticmethod
    def RedstoneLamp() -> BlockDescriptor:
        """Factory for RedstoneLamp"""
        return BlockDescriptor("minecraft:redstone_lamp")

    @staticmethod
    def RedstoneOre() -> BlockDescriptor:
        """Factory for RedstoneOre"""
        return BlockDescriptor("minecraft:redstone_ore")

    @staticmethod
    def RedstoneTorch(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for RedstoneTorch"""
        return BlockDescriptor("minecraft:redstone_torch", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def RedstoneWire(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for RedstoneWire"""
        return BlockDescriptor("minecraft:redstone_wire", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def Reeds(age: Age) -> BlockDescriptor:
        """Factory for Reeds"""
        return BlockDescriptor("minecraft:reeds", {_BlockStateKeys.Age: age})

    @staticmethod
    def ReinforcedDeepslate() -> BlockDescriptor:
        """Factory for ReinforcedDeepslate"""
        return BlockDescriptor("minecraft:reinforced_deepslate")

    @staticmethod
    def RepeatingCommandBlock(conditional_bit: ConditionalBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for RepeatingCommandBlock"""
        return BlockDescriptor(
            "minecraft:repeating_command_block",
            {_BlockStateKeys.ConditionalBit: conditional_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def ResinBlock() -> BlockDescriptor:
        """Factory for ResinBlock"""
        return BlockDescriptor("minecraft:resin_block")

    @staticmethod
    def ResinBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for ResinBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:resin_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def ResinBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for ResinBrickSlab"""
        return BlockDescriptor("minecraft:resin_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def ResinBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for ResinBrickStairs"""
        return BlockDescriptor(
            "minecraft:resin_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def ResinBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for ResinBrickWall"""
        return BlockDescriptor(
            "minecraft:resin_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def ResinBricks() -> BlockDescriptor:
        """Factory for ResinBricks"""
        return BlockDescriptor("minecraft:resin_bricks")

    @staticmethod
    def ResinClump(multi_face_direction_bits: MultiFaceDirectionBits) -> BlockDescriptor:
        """Factory for ResinClump"""
        return BlockDescriptor("minecraft:resin_clump", {_BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits})

    @staticmethod
    def RespawnAnchor(respawn_anchor_charge: RespawnAnchorCharge) -> BlockDescriptor:
        """Factory for RespawnAnchor"""
        return BlockDescriptor("minecraft:respawn_anchor", {_BlockStateKeys.RespawnAnchorCharge: respawn_anchor_charge})

    @staticmethod
    def RoseBush(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for RoseBush"""
        return BlockDescriptor("minecraft:rose_bush", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def Sand() -> BlockDescriptor:
        """Factory for Sand"""
        return BlockDescriptor("minecraft:sand")

    @staticmethod
    def Sandstone() -> BlockDescriptor:
        """Factory for Sandstone"""
        return BlockDescriptor("minecraft:sandstone")

    @staticmethod
    def SandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SandstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:sandstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SandstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SandstoneSlab"""
        return BlockDescriptor("minecraft:sandstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for SandstoneStairs"""
        return BlockDescriptor(
            "minecraft:sandstone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SandstoneWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for SandstoneWall"""
        return BlockDescriptor(
            "minecraft:sandstone_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def Scaffolding(stability: Stability, stability_check: StabilityCheck) -> BlockDescriptor:
        """Factory for Scaffolding"""
        return BlockDescriptor(
            "minecraft:scaffolding", {_BlockStateKeys.Stability: stability, _BlockStateKeys.StabilityCheck: stability_check}
        )

    @staticmethod
    def Sculk() -> BlockDescriptor:
        """Factory for Sculk"""
        return BlockDescriptor("minecraft:sculk")

    @staticmethod
    def SculkCatalyst(bloom: Bloom) -> BlockDescriptor:
        """Factory for SculkCatalyst"""
        return BlockDescriptor("minecraft:sculk_catalyst", {_BlockStateKeys.Bloom: bloom})

    @staticmethod
    def SculkSensor(sculk_sensor_phase: SculkSensorPhase) -> BlockDescriptor:
        """Factory for SculkSensor"""
        return BlockDescriptor("minecraft:sculk_sensor", {_BlockStateKeys.SculkSensorPhase: sculk_sensor_phase})

    @staticmethod
    def SculkShrieker(active: Active, can_summon: CanSummon) -> BlockDescriptor:
        """Factory for SculkShrieker"""
        return BlockDescriptor(
            "minecraft:sculk_shrieker", {_BlockStateKeys.Active: active, _BlockStateKeys.CanSummon: can_summon}
        )

    @staticmethod
    def SculkVein(multi_face_direction_bits: MultiFaceDirectionBits) -> BlockDescriptor:
        """Factory for SculkVein"""
        return BlockDescriptor("minecraft:sculk_vein", {_BlockStateKeys.MultiFaceDirectionBits: multi_face_direction_bits})

    @staticmethod
    def SeaLantern() -> BlockDescriptor:
        """Factory for SeaLantern"""
        return BlockDescriptor("minecraft:sea_lantern")

    @staticmethod
    def SeaPickle(cluster_count: ClusterCount, dead_bit: DeadBit) -> BlockDescriptor:
        """Factory for SeaPickle"""
        return BlockDescriptor(
            "minecraft:sea_pickle", {_BlockStateKeys.ClusterCount: cluster_count, _BlockStateKeys.DeadBit: dead_bit}
        )

    @staticmethod
    def Seagrass(sea_grass_type: SeaGrassType) -> BlockDescriptor:
        """Factory for Seagrass"""
        return BlockDescriptor("minecraft:seagrass", {_BlockStateKeys.SeaGrassType: sea_grass_type})

    @staticmethod
    def ShortDryGrass() -> BlockDescriptor:
        """Factory for ShortDryGrass"""
        return BlockDescriptor("minecraft:short_dry_grass")

    @staticmethod
    def ShortGrass() -> BlockDescriptor:
        """Factory for ShortGrass"""
        return BlockDescriptor("minecraft:short_grass")

    @staticmethod
    def Shroomlight() -> BlockDescriptor:
        """Factory for Shroomlight"""
        return BlockDescriptor("minecraft:shroomlight")

    @staticmethod
    def SilverGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for SilverGlazedTerracotta"""
        return BlockDescriptor("minecraft:silver_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def SkeletonSkull(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for SkeletonSkull"""
        return BlockDescriptor("minecraft:skeleton_skull", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Slime() -> BlockDescriptor:
        """Factory for Slime"""
        return BlockDescriptor("minecraft:slime")

    @staticmethod
    def SmallAmethystBud(minecraft_block_face: BlockFace) -> BlockDescriptor:
        """Factory for SmallAmethystBud"""
        return BlockDescriptor("minecraft:small_amethyst_bud", {_BlockStateKeys.MinecraftBlockFace: minecraft_block_face})

    @staticmethod
    def SmallDripleafBlock(minecraft_cardinal_direction: CardinalDirection, upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for SmallDripleafBlock"""
        return BlockDescriptor(
            "minecraft:small_dripleaf_block",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def SmithingTable() -> BlockDescriptor:
        """Factory for SmithingTable"""
        return BlockDescriptor("minecraft:smithing_table")

    @staticmethod
    def Smoker(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Smoker"""
        return BlockDescriptor("minecraft:smoker", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction})

    @staticmethod
    def SmoothBasalt() -> BlockDescriptor:
        """Factory for SmoothBasalt"""
        return BlockDescriptor("minecraft:smooth_basalt")

    @staticmethod
    def SmoothQuartz(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for SmoothQuartz"""
        return BlockDescriptor("minecraft:smooth_quartz", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def SmoothQuartzDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothQuartzDoubleSlab"""
        return BlockDescriptor(
            "minecraft:smooth_quartz_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothQuartzSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothQuartzSlab"""
        return BlockDescriptor("minecraft:smooth_quartz_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SmoothQuartzStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for SmoothQuartzStairs"""
        return BlockDescriptor(
            "minecraft:smooth_quartz_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SmoothRedSandstone() -> BlockDescriptor:
        """Factory for SmoothRedSandstone"""
        return BlockDescriptor("minecraft:smooth_red_sandstone")

    @staticmethod
    def SmoothRedSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothRedSandstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:smooth_red_sandstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothRedSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothRedSandstoneSlab"""
        return BlockDescriptor(
            "minecraft:smooth_red_sandstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothRedSandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for SmoothRedSandstoneStairs"""
        return BlockDescriptor(
            "minecraft:smooth_red_sandstone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SmoothSandstone() -> BlockDescriptor:
        """Factory for SmoothSandstone"""
        return BlockDescriptor("minecraft:smooth_sandstone")

    @staticmethod
    def SmoothSandstoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothSandstoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:smooth_sandstone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothSandstoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothSandstoneSlab"""
        return BlockDescriptor(
            "minecraft:smooth_sandstone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothSandstoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for SmoothSandstoneStairs"""
        return BlockDescriptor(
            "minecraft:smooth_sandstone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SmoothStone() -> BlockDescriptor:
        """Factory for SmoothStone"""
        return BlockDescriptor("minecraft:smooth_stone")

    @staticmethod
    def SmoothStoneDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothStoneDoubleSlab"""
        return BlockDescriptor(
            "minecraft:smooth_stone_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def SmoothStoneSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SmoothStoneSlab"""
        return BlockDescriptor("minecraft:smooth_stone_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SnifferEgg(cracked_state: CrackedState) -> BlockDescriptor:
        """Factory for SnifferEgg"""
        return BlockDescriptor("minecraft:sniffer_egg", {_BlockStateKeys.CrackedState: cracked_state})

    @staticmethod
    def Snow() -> BlockDescriptor:
        """Factory for Snow"""
        return BlockDescriptor("minecraft:snow")

    @staticmethod
    def SnowLayer(covered_bit: CoveredBit, height: Height) -> BlockDescriptor:
        """Factory for SnowLayer"""
        return BlockDescriptor("minecraft:snow_layer", {_BlockStateKeys.CoveredBit: covered_bit, _BlockStateKeys.Height: height})

    @staticmethod
    def SoulCampfire(extinguished: Extinguished, minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for SoulCampfire"""
        return BlockDescriptor(
            "minecraft:soul_campfire",
            {
                _BlockStateKeys.Extinguished: extinguished,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
            },
        )

    @staticmethod
    def SoulFire(age: Age) -> BlockDescriptor:
        """Factory for SoulFire"""
        return BlockDescriptor("minecraft:soul_fire", {_BlockStateKeys.Age: age})

    @staticmethod
    def SoulLantern(hanging: Hanging) -> BlockDescriptor:
        """Factory for SoulLantern"""
        return BlockDescriptor("minecraft:soul_lantern", {_BlockStateKeys.Hanging: hanging})

    @staticmethod
    def SoulSand() -> BlockDescriptor:
        """Factory for SoulSand"""
        return BlockDescriptor("minecraft:soul_sand")

    @staticmethod
    def SoulSoil() -> BlockDescriptor:
        """Factory for SoulSoil"""
        return BlockDescriptor("minecraft:soul_soil")

    @staticmethod
    def SoulTorch(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for SoulTorch"""
        return BlockDescriptor("minecraft:soul_torch", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def Sponge() -> BlockDescriptor:
        """Factory for Sponge"""
        return BlockDescriptor("minecraft:sponge")

    @staticmethod
    def SporeBlossom() -> BlockDescriptor:
        """Factory for SporeBlossom"""
        return BlockDescriptor("minecraft:spore_blossom")

    @staticmethod
    def SpruceButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for SpruceButton"""
        return BlockDescriptor(
            "minecraft:spruce_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def SpruceDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for SpruceDoor"""
        return BlockDescriptor(
            "minecraft:spruce_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def SpruceDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SpruceDoubleSlab"""
        return BlockDescriptor("minecraft:spruce_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SpruceFence() -> BlockDescriptor:
        """Factory for SpruceFence"""
        return BlockDescriptor("minecraft:spruce_fence")

    @staticmethod
    def SpruceFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for SpruceFenceGate"""
        return BlockDescriptor(
            "minecraft:spruce_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def SpruceHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for SpruceHangingSign"""
        return BlockDescriptor(
            "minecraft:spruce_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def SpruceLeaves(persistent_bit: PersistentBit, update_bit: UpdateBit) -> BlockDescriptor:
        """Factory for SpruceLeaves"""
        return BlockDescriptor(
            "minecraft:spruce_leaves", {_BlockStateKeys.PersistentBit: persistent_bit, _BlockStateKeys.UpdateBit: update_bit}
        )

    @staticmethod
    def SpruceLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for SpruceLog"""
        return BlockDescriptor("minecraft:spruce_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def SprucePlanks() -> BlockDescriptor:
        """Factory for SprucePlanks"""
        return BlockDescriptor("minecraft:spruce_planks")

    @staticmethod
    def SprucePressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for SprucePressurePlate"""
        return BlockDescriptor("minecraft:spruce_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def SpruceSapling(age_bit: AgeBit) -> BlockDescriptor:
        """Factory for SpruceSapling"""
        return BlockDescriptor("minecraft:spruce_sapling", {_BlockStateKeys.AgeBit: age_bit})

    @staticmethod
    def SpruceSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for SpruceSlab"""
        return BlockDescriptor("minecraft:spruce_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def SpruceStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for SpruceStairs"""
        return BlockDescriptor(
            "minecraft:spruce_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def SpruceStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for SpruceStandingSign"""
        return BlockDescriptor("minecraft:spruce_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def SpruceTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for SpruceTrapdoor"""
        return BlockDescriptor(
            "minecraft:spruce_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def SpruceWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for SpruceWallSign"""
        return BlockDescriptor("minecraft:spruce_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def SpruceWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for SpruceWood"""
        return BlockDescriptor("minecraft:spruce_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StandingBanner(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for StandingBanner"""
        return BlockDescriptor("minecraft:standing_banner", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def StandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for StandingSign"""
        return BlockDescriptor("minecraft:standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def StickyPiston(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for StickyPiston"""
        return BlockDescriptor("minecraft:sticky_piston", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def StickyPistonArmCollision(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for StickyPistonArmCollision"""
        return BlockDescriptor("minecraft:sticky_piston_arm_collision", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def Stone() -> BlockDescriptor:
        """Factory for Stone"""
        return BlockDescriptor("minecraft:stone")

    @staticmethod
    def StoneBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for StoneBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:stone_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def StoneBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for StoneBrickSlab"""
        return BlockDescriptor("minecraft:stone_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def StoneBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for StoneBrickStairs"""
        return BlockDescriptor(
            "minecraft:stone_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def StoneBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for StoneBrickWall"""
        return BlockDescriptor(
            "minecraft:stone_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def StoneBricks() -> BlockDescriptor:
        """Factory for StoneBricks"""
        return BlockDescriptor("minecraft:stone_bricks")

    @staticmethod
    def StoneButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for StoneButton"""
        return BlockDescriptor(
            "minecraft:stone_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def StonePressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for StonePressurePlate"""
        return BlockDescriptor("minecraft:stone_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def StoneStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for StoneStairs"""
        return BlockDescriptor(
            "minecraft:stone_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def StonecutterBlock(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for StonecutterBlock"""
        return BlockDescriptor(
            "minecraft:stonecutter_block", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def StrippedAcaciaLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedAcaciaLog"""
        return BlockDescriptor("minecraft:stripped_acacia_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedAcaciaWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedAcaciaWood"""
        return BlockDescriptor("minecraft:stripped_acacia_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedBambooBlock(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedBambooBlock"""
        return BlockDescriptor("minecraft:stripped_bamboo_block", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedBirchLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedBirchLog"""
        return BlockDescriptor("minecraft:stripped_birch_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedBirchWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedBirchWood"""
        return BlockDescriptor("minecraft:stripped_birch_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCherryLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedCherryLog"""
        return BlockDescriptor("minecraft:stripped_cherry_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCherryWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedCherryWood"""
        return BlockDescriptor("minecraft:stripped_cherry_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCrimsonHyphae(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedCrimsonHyphae"""
        return BlockDescriptor("minecraft:stripped_crimson_hyphae", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedCrimsonStem(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedCrimsonStem"""
        return BlockDescriptor("minecraft:stripped_crimson_stem", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedDarkOakLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedDarkOakLog"""
        return BlockDescriptor("minecraft:stripped_dark_oak_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedDarkOakWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedDarkOakWood"""
        return BlockDescriptor("minecraft:stripped_dark_oak_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedJungleLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedJungleLog"""
        return BlockDescriptor("minecraft:stripped_jungle_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedJungleWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedJungleWood"""
        return BlockDescriptor("minecraft:stripped_jungle_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedMangroveLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedMangroveLog"""
        return BlockDescriptor("minecraft:stripped_mangrove_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedMangroveWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedMangroveWood"""
        return BlockDescriptor("minecraft:stripped_mangrove_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedOakLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedOakLog"""
        return BlockDescriptor("minecraft:stripped_oak_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedOakWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedOakWood"""
        return BlockDescriptor("minecraft:stripped_oak_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedPaleOakLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedPaleOakLog"""
        return BlockDescriptor("minecraft:stripped_pale_oak_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedPaleOakWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedPaleOakWood"""
        return BlockDescriptor("minecraft:stripped_pale_oak_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedSpruceLog(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedSpruceLog"""
        return BlockDescriptor("minecraft:stripped_spruce_log", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedSpruceWood(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedSpruceWood"""
        return BlockDescriptor("minecraft:stripped_spruce_wood", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedWarpedHyphae(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedWarpedHyphae"""
        return BlockDescriptor("minecraft:stripped_warped_hyphae", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StrippedWarpedStem(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for StrippedWarpedStem"""
        return BlockDescriptor("minecraft:stripped_warped_stem", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def StructureBlock(structure_block_type: StructureBlockType) -> BlockDescriptor:
        """Factory for StructureBlock"""
        return BlockDescriptor("minecraft:structure_block", {_BlockStateKeys.StructureBlockType: structure_block_type})

    @staticmethod
    def StructureVoid() -> BlockDescriptor:
        """Factory for StructureVoid"""
        return BlockDescriptor("minecraft:structure_void")

    @staticmethod
    def Sunflower(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for Sunflower"""
        return BlockDescriptor("minecraft:sunflower", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def SuspiciousGravel(brushed_progress: BrushedProgress, hanging: Hanging) -> BlockDescriptor:
        """Factory for SuspiciousGravel"""
        return BlockDescriptor(
            "minecraft:suspicious_gravel", {_BlockStateKeys.BrushedProgress: brushed_progress, _BlockStateKeys.Hanging: hanging}
        )

    @staticmethod
    def SuspiciousSand(brushed_progress: BrushedProgress, hanging: Hanging) -> BlockDescriptor:
        """Factory for SuspiciousSand"""
        return BlockDescriptor(
            "minecraft:suspicious_sand", {_BlockStateKeys.BrushedProgress: brushed_progress, _BlockStateKeys.Hanging: hanging}
        )

    @staticmethod
    def SweetBerryBush(growth: Growth) -> BlockDescriptor:
        """Factory for SweetBerryBush"""
        return BlockDescriptor("minecraft:sweet_berry_bush", {_BlockStateKeys.Growth: growth})

    @staticmethod
    def TallDryGrass() -> BlockDescriptor:
        """Factory for TallDryGrass"""
        return BlockDescriptor("minecraft:tall_dry_grass")

    @staticmethod
    def TallGrass(upper_block_bit: UpperBlockBit) -> BlockDescriptor:
        """Factory for TallGrass"""
        return BlockDescriptor("minecraft:tall_grass", {_BlockStateKeys.UpperBlockBit: upper_block_bit})

    @staticmethod
    def Target() -> BlockDescriptor:
        """Factory for Target"""
        return BlockDescriptor("minecraft:target")

    @staticmethod
    def TintedGlass() -> BlockDescriptor:
        """Factory for TintedGlass"""
        return BlockDescriptor("minecraft:tinted_glass")

    @staticmethod
    def Tnt(explode_bit: ExplodeBit) -> BlockDescriptor:
        """Factory for Tnt"""
        return BlockDescriptor("minecraft:tnt", {_BlockStateKeys.ExplodeBit: explode_bit})

    @staticmethod
    def Torch(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for Torch"""
        return BlockDescriptor("minecraft:torch", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def Torchflower() -> BlockDescriptor:
        """Factory for Torchflower"""
        return BlockDescriptor("minecraft:torchflower")

    @staticmethod
    def TorchflowerCrop(growth: Growth) -> BlockDescriptor:
        """Factory for TorchflowerCrop"""
        return BlockDescriptor("minecraft:torchflower_crop", {_BlockStateKeys.Growth: growth})

    @staticmethod
    def Trapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for Trapdoor"""
        return BlockDescriptor(
            "minecraft:trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def TrappedChest(minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for TrappedChest"""
        return BlockDescriptor(
            "minecraft:trapped_chest", {_BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction}
        )

    @staticmethod
    def TrialSpawner(ominous: Ominous, trial_spawner_state: TrialSpawnerState) -> BlockDescriptor:
        """Factory for TrialSpawner"""
        return BlockDescriptor(
            "minecraft:trial_spawner", {_BlockStateKeys.Ominous: ominous, _BlockStateKeys.TrialSpawnerState: trial_spawner_state}
        )

    @staticmethod
    def TripWire(
        attached_bit: AttachedBit, disarmed_bit: DisarmedBit, powered_bit: PoweredBit, suspended_bit: SuspendedBit
    ) -> BlockDescriptor:
        """Factory for TripWire"""
        return BlockDescriptor(
            "minecraft:trip_wire",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.DisarmedBit: disarmed_bit,
                _BlockStateKeys.PoweredBit: powered_bit,
                _BlockStateKeys.SuspendedBit: suspended_bit,
            },
        )

    @staticmethod
    def TripwireHook(attached_bit: AttachedBit, direction: Direction, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for TripwireHook"""
        return BlockDescriptor(
            "minecraft:tripwire_hook",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.PoweredBit: powered_bit,
            },
        )

    @staticmethod
    def TubeCoral() -> BlockDescriptor:
        """Factory for TubeCoral"""
        return BlockDescriptor("minecraft:tube_coral")

    @staticmethod
    def TubeCoralBlock() -> BlockDescriptor:
        """Factory for TubeCoralBlock"""
        return BlockDescriptor("minecraft:tube_coral_block")

    @staticmethod
    def TubeCoralFan(coral_fan_direction: CoralFanDirection) -> BlockDescriptor:
        """Factory for TubeCoralFan"""
        return BlockDescriptor("minecraft:tube_coral_fan", {_BlockStateKeys.CoralFanDirection: coral_fan_direction})

    @staticmethod
    def TubeCoralWallFan(coral_direction: CoralDirection) -> BlockDescriptor:
        """Factory for TubeCoralWallFan"""
        return BlockDescriptor("minecraft:tube_coral_wall_fan", {_BlockStateKeys.CoralDirection: coral_direction})

    @staticmethod
    def Tuff() -> BlockDescriptor:
        """Factory for Tuff"""
        return BlockDescriptor("minecraft:tuff")

    @staticmethod
    def TuffBrickDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for TuffBrickDoubleSlab"""
        return BlockDescriptor(
            "minecraft:tuff_brick_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def TuffBrickSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for TuffBrickSlab"""
        return BlockDescriptor("minecraft:tuff_brick_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def TuffBrickStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for TuffBrickStairs"""
        return BlockDescriptor(
            "minecraft:tuff_brick_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def TuffBrickWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for TuffBrickWall"""
        return BlockDescriptor(
            "minecraft:tuff_brick_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def TuffBricks() -> BlockDescriptor:
        """Factory for TuffBricks"""
        return BlockDescriptor("minecraft:tuff_bricks")

    @staticmethod
    def TuffDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for TuffDoubleSlab"""
        return BlockDescriptor("minecraft:tuff_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def TuffSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for TuffSlab"""
        return BlockDescriptor("minecraft:tuff_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def TuffStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for TuffStairs"""
        return BlockDescriptor(
            "minecraft:tuff_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def TuffWall(
        wall_connection_type_east: WallConnectionTypeEast,
        wall_connection_type_north: WallConnectionTypeNorth,
        wall_connection_type_south: WallConnectionTypeSouth,
        wall_connection_type_west: WallConnectionTypeWest,
        wall_post_bit: WallPostBit,
    ) -> BlockDescriptor:
        """Factory for TuffWall"""
        return BlockDescriptor(
            "minecraft:tuff_wall",
            {
                _BlockStateKeys.WallConnectionTypeEast: wall_connection_type_east,
                _BlockStateKeys.WallConnectionTypeNorth: wall_connection_type_north,
                _BlockStateKeys.WallConnectionTypeSouth: wall_connection_type_south,
                _BlockStateKeys.WallConnectionTypeWest: wall_connection_type_west,
                _BlockStateKeys.WallPostBit: wall_post_bit,
            },
        )

    @staticmethod
    def TurtleEgg(cracked_state: CrackedState, turtle_egg_count: TurtleEggCount) -> BlockDescriptor:
        """Factory for TurtleEgg"""
        return BlockDescriptor(
            "minecraft:turtle_egg",
            {_BlockStateKeys.CrackedState: cracked_state, _BlockStateKeys.TurtleEggCount: turtle_egg_count},
        )

    @staticmethod
    def TwistingVines(twisting_vines_age: TwistingVinesAge) -> BlockDescriptor:
        """Factory for TwistingVines"""
        return BlockDescriptor("minecraft:twisting_vines", {_BlockStateKeys.TwistingVinesAge: twisting_vines_age})

    @staticmethod
    def UnderwaterTnt(explode_bit: ExplodeBit) -> BlockDescriptor:
        """Factory for UnderwaterTnt"""
        return BlockDescriptor("minecraft:underwater_tnt", {_BlockStateKeys.ExplodeBit: explode_bit})

    @staticmethod
    def UnderwaterTorch(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for UnderwaterTorch"""
        return BlockDescriptor("minecraft:underwater_torch", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def UndyedShulkerBox() -> BlockDescriptor:
        """Factory for UndyedShulkerBox"""
        return BlockDescriptor("minecraft:undyed_shulker_box")

    @staticmethod
    def Unknown() -> BlockDescriptor:
        """Factory for Unknown"""
        return BlockDescriptor("minecraft:unknown")

    @staticmethod
    def UnlitRedstoneTorch(torch_facing_direction: TorchFacingDirection) -> BlockDescriptor:
        """Factory for UnlitRedstoneTorch"""
        return BlockDescriptor("minecraft:unlit_redstone_torch", {_BlockStateKeys.TorchFacingDirection: torch_facing_direction})

    @staticmethod
    def UnpoweredComparator(
        minecraft_cardinal_direction: CardinalDirection, output_lit_bit: OutputLitBit, output_subtract_bit: OutputSubtractBit
    ) -> BlockDescriptor:
        """Factory for UnpoweredComparator"""
        return BlockDescriptor(
            "minecraft:unpowered_comparator",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OutputLitBit: output_lit_bit,
                _BlockStateKeys.OutputSubtractBit: output_subtract_bit,
            },
        )

    @staticmethod
    def UnpoweredRepeater(minecraft_cardinal_direction: CardinalDirection, repeater_delay: RepeaterDelay) -> BlockDescriptor:
        """Factory for UnpoweredRepeater"""
        return BlockDescriptor(
            "minecraft:unpowered_repeater",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.RepeaterDelay: repeater_delay,
            },
        )

    @staticmethod
    def Vault(minecraft_cardinal_direction: CardinalDirection, ominous: Ominous, vault_state: VaultState) -> BlockDescriptor:
        """Factory for Vault"""
        return BlockDescriptor(
            "minecraft:vault",
            {
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.Ominous: ominous,
                _BlockStateKeys.VaultState: vault_state,
            },
        )

    @staticmethod
    def VerdantFroglight(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for VerdantFroglight"""
        return BlockDescriptor("minecraft:verdant_froglight", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def Vine(vine_direction_bits: VineDirectionBits) -> BlockDescriptor:
        """Factory for Vine"""
        return BlockDescriptor("minecraft:vine", {_BlockStateKeys.VineDirectionBits: vine_direction_bits})

    @staticmethod
    def WallBanner(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WallBanner"""
        return BlockDescriptor("minecraft:wall_banner", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WallSign"""
        return BlockDescriptor("minecraft:wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WarpedButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WarpedButton"""
        return BlockDescriptor(
            "minecraft:warped_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def WarpedDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WarpedDoor"""
        return BlockDescriptor(
            "minecraft:warped_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WarpedDoubleSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WarpedDoubleSlab"""
        return BlockDescriptor("minecraft:warped_double_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def WarpedFence() -> BlockDescriptor:
        """Factory for WarpedFence"""
        return BlockDescriptor("minecraft:warped_fence")

    @staticmethod
    def WarpedFenceGate(
        in_wall_bit: InWallBit, minecraft_cardinal_direction: CardinalDirection, open_bit: OpenBit
    ) -> BlockDescriptor:
        """Factory for WarpedFenceGate"""
        return BlockDescriptor(
            "minecraft:warped_fence_gate",
            {
                _BlockStateKeys.InWallBit: in_wall_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
            },
        )

    @staticmethod
    def WarpedFungus() -> BlockDescriptor:
        """Factory for WarpedFungus"""
        return BlockDescriptor("minecraft:warped_fungus")

    @staticmethod
    def WarpedHangingSign(
        attached_bit: AttachedBit, facing_direction: FacingDirection, ground_sign_direction: GroundSignDirection, hanging: Hanging
    ) -> BlockDescriptor:
        """Factory for WarpedHangingSign"""
        return BlockDescriptor(
            "minecraft:warped_hanging_sign",
            {
                _BlockStateKeys.AttachedBit: attached_bit,
                _BlockStateKeys.FacingDirection: facing_direction,
                _BlockStateKeys.GroundSignDirection: ground_sign_direction,
                _BlockStateKeys.Hanging: hanging,
            },
        )

    @staticmethod
    def WarpedHyphae(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for WarpedHyphae"""
        return BlockDescriptor("minecraft:warped_hyphae", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def WarpedNylium() -> BlockDescriptor:
        """Factory for WarpedNylium"""
        return BlockDescriptor("minecraft:warped_nylium")

    @staticmethod
    def WarpedPlanks() -> BlockDescriptor:
        """Factory for WarpedPlanks"""
        return BlockDescriptor("minecraft:warped_planks")

    @staticmethod
    def WarpedPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for WarpedPressurePlate"""
        return BlockDescriptor("minecraft:warped_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def WarpedRoots() -> BlockDescriptor:
        """Factory for WarpedRoots"""
        return BlockDescriptor("minecraft:warped_roots")

    @staticmethod
    def WarpedSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WarpedSlab"""
        return BlockDescriptor("minecraft:warped_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half})

    @staticmethod
    def WarpedStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for WarpedStairs"""
        return BlockDescriptor(
            "minecraft:warped_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WarpedStandingSign(ground_sign_direction: GroundSignDirection) -> BlockDescriptor:
        """Factory for WarpedStandingSign"""
        return BlockDescriptor("minecraft:warped_standing_sign", {_BlockStateKeys.GroundSignDirection: ground_sign_direction})

    @staticmethod
    def WarpedStem(pillar_axis: PillarAxis) -> BlockDescriptor:
        """Factory for WarpedStem"""
        return BlockDescriptor("minecraft:warped_stem", {_BlockStateKeys.PillarAxis: pillar_axis})

    @staticmethod
    def WarpedTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for WarpedTrapdoor"""
        return BlockDescriptor(
            "minecraft:warped_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WarpedWallSign(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WarpedWallSign"""
        return BlockDescriptor("minecraft:warped_wall_sign", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WarpedWartBlock() -> BlockDescriptor:
        """Factory for WarpedWartBlock"""
        return BlockDescriptor("minecraft:warped_wart_block")

    @staticmethod
    def Water(liquid_depth: LiquidDepth) -> BlockDescriptor:
        """Factory for Water"""
        return BlockDescriptor("minecraft:water", {_BlockStateKeys.LiquidDepth: liquid_depth})

    @staticmethod
    def Waterlily() -> BlockDescriptor:
        """Factory for Waterlily"""
        return BlockDescriptor("minecraft:waterlily")

    @staticmethod
    def WaxedChiseledCopper() -> BlockDescriptor:
        """Factory for WaxedChiseledCopper"""
        return BlockDescriptor("minecraft:waxed_chiseled_copper")

    @staticmethod
    def WaxedCopper() -> BlockDescriptor:
        """Factory for WaxedCopper"""
        return BlockDescriptor("minecraft:waxed_copper")

    @staticmethod
    def WaxedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for WaxedCopperBulb"""
        return BlockDescriptor("minecraft:waxed_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit})

    @staticmethod
    def WaxedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WaxedCopperDoor"""
        return BlockDescriptor(
            "minecraft:waxed_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedCopperGrate() -> BlockDescriptor:
        """Factory for WaxedCopperGrate"""
        return BlockDescriptor("minecraft:waxed_copper_grate")

    @staticmethod
    def WaxedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for WaxedCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:waxed_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedCutCopper() -> BlockDescriptor:
        """Factory for WaxedCutCopper"""
        return BlockDescriptor("minecraft:waxed_cut_copper")

    @staticmethod
    def WaxedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for WaxedCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:waxed_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedExposedChiseledCopper() -> BlockDescriptor:
        """Factory for WaxedExposedChiseledCopper"""
        return BlockDescriptor("minecraft:waxed_exposed_chiseled_copper")

    @staticmethod
    def WaxedExposedCopper() -> BlockDescriptor:
        """Factory for WaxedExposedCopper"""
        return BlockDescriptor("minecraft:waxed_exposed_copper")

    @staticmethod
    def WaxedExposedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for WaxedExposedCopperBulb"""
        return BlockDescriptor(
            "minecraft:waxed_exposed_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WaxedExposedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WaxedExposedCopperDoor"""
        return BlockDescriptor(
            "minecraft:waxed_exposed_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedExposedCopperGrate() -> BlockDescriptor:
        """Factory for WaxedExposedCopperGrate"""
        return BlockDescriptor("minecraft:waxed_exposed_copper_grate")

    @staticmethod
    def WaxedExposedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for WaxedExposedCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:waxed_exposed_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedExposedCutCopper() -> BlockDescriptor:
        """Factory for WaxedExposedCutCopper"""
        return BlockDescriptor("minecraft:waxed_exposed_cut_copper")

    @staticmethod
    def WaxedExposedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedExposedCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_exposed_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedExposedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for WaxedExposedCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:waxed_exposed_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedExposedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedExposedDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_exposed_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedOxidizedChiseledCopper() -> BlockDescriptor:
        """Factory for WaxedOxidizedChiseledCopper"""
        return BlockDescriptor("minecraft:waxed_oxidized_chiseled_copper")

    @staticmethod
    def WaxedOxidizedCopper() -> BlockDescriptor:
        """Factory for WaxedOxidizedCopper"""
        return BlockDescriptor("minecraft:waxed_oxidized_copper")

    @staticmethod
    def WaxedOxidizedCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for WaxedOxidizedCopperBulb"""
        return BlockDescriptor(
            "minecraft:waxed_oxidized_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WaxedOxidizedCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WaxedOxidizedCopperDoor"""
        return BlockDescriptor(
            "minecraft:waxed_oxidized_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedOxidizedCopperGrate() -> BlockDescriptor:
        """Factory for WaxedOxidizedCopperGrate"""
        return BlockDescriptor("minecraft:waxed_oxidized_copper_grate")

    @staticmethod
    def WaxedOxidizedCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for WaxedOxidizedCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:waxed_oxidized_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedOxidizedCutCopper() -> BlockDescriptor:
        """Factory for WaxedOxidizedCutCopper"""
        return BlockDescriptor("minecraft:waxed_oxidized_cut_copper")

    @staticmethod
    def WaxedOxidizedCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedOxidizedCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_oxidized_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedOxidizedCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for WaxedOxidizedCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:waxed_oxidized_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedOxidizedDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedOxidizedDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_oxidized_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedWeatheredChiseledCopper() -> BlockDescriptor:
        """Factory for WaxedWeatheredChiseledCopper"""
        return BlockDescriptor("minecraft:waxed_weathered_chiseled_copper")

    @staticmethod
    def WaxedWeatheredCopper() -> BlockDescriptor:
        """Factory for WaxedWeatheredCopper"""
        return BlockDescriptor("minecraft:waxed_weathered_copper")

    @staticmethod
    def WaxedWeatheredCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for WaxedWeatheredCopperBulb"""
        return BlockDescriptor(
            "minecraft:waxed_weathered_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WaxedWeatheredCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WaxedWeatheredCopperDoor"""
        return BlockDescriptor(
            "minecraft:waxed_weathered_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WaxedWeatheredCopperGrate() -> BlockDescriptor:
        """Factory for WaxedWeatheredCopperGrate"""
        return BlockDescriptor("minecraft:waxed_weathered_copper_grate")

    @staticmethod
    def WaxedWeatheredCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for WaxedWeatheredCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:waxed_weathered_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WaxedWeatheredCutCopper() -> BlockDescriptor:
        """Factory for WaxedWeatheredCutCopper"""
        return BlockDescriptor("minecraft:waxed_weathered_cut_copper")

    @staticmethod
    def WaxedWeatheredCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedWeatheredCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_weathered_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WaxedWeatheredCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for WaxedWeatheredCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:waxed_weathered_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WaxedWeatheredDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WaxedWeatheredDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:waxed_weathered_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WeatheredChiseledCopper() -> BlockDescriptor:
        """Factory for WeatheredChiseledCopper"""
        return BlockDescriptor("minecraft:weathered_chiseled_copper")

    @staticmethod
    def WeatheredCopper() -> BlockDescriptor:
        """Factory for WeatheredCopper"""
        return BlockDescriptor("minecraft:weathered_copper")

    @staticmethod
    def WeatheredCopperBulb(lit: Lit, powered_bit: PoweredBit) -> BlockDescriptor:
        """Factory for WeatheredCopperBulb"""
        return BlockDescriptor(
            "minecraft:weathered_copper_bulb", {_BlockStateKeys.Lit: lit, _BlockStateKeys.PoweredBit: powered_bit}
        )

    @staticmethod
    def WeatheredCopperDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WeatheredCopperDoor"""
        return BlockDescriptor(
            "minecraft:weathered_copper_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WeatheredCopperGrate() -> BlockDescriptor:
        """Factory for WeatheredCopperGrate"""
        return BlockDescriptor("minecraft:weathered_copper_grate")

    @staticmethod
    def WeatheredCopperTrapdoor(direction: Direction, open_bit: OpenBit, upside_down_bit: UpsideDownBit) -> BlockDescriptor:
        """Factory for WeatheredCopperTrapdoor"""
        return BlockDescriptor(
            "minecraft:weathered_copper_trapdoor",
            {
                _BlockStateKeys.Direction: direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpsideDownBit: upside_down_bit,
            },
        )

    @staticmethod
    def WeatheredCutCopper() -> BlockDescriptor:
        """Factory for WeatheredCutCopper"""
        return BlockDescriptor("minecraft:weathered_cut_copper")

    @staticmethod
    def WeatheredCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WeatheredCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:weathered_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def WeatheredCutCopperStairs(upside_down_bit: UpsideDownBit, weirdo_direction: WeirdoDirection) -> BlockDescriptor:
        """Factory for WeatheredCutCopperStairs"""
        return BlockDescriptor(
            "minecraft:weathered_cut_copper_stairs",
            {_BlockStateKeys.UpsideDownBit: upside_down_bit, _BlockStateKeys.WeirdoDirection: weirdo_direction},
        )

    @staticmethod
    def WeatheredDoubleCutCopperSlab(minecraft_vertical_half: VerticalHalf) -> BlockDescriptor:
        """Factory for WeatheredDoubleCutCopperSlab"""
        return BlockDescriptor(
            "minecraft:weathered_double_cut_copper_slab", {_BlockStateKeys.MinecraftVerticalHalf: minecraft_vertical_half}
        )

    @staticmethod
    def Web() -> BlockDescriptor:
        """Factory for Web"""
        return BlockDescriptor("minecraft:web")

    @staticmethod
    def WeepingVines(weeping_vines_age: WeepingVinesAge) -> BlockDescriptor:
        """Factory for WeepingVines"""
        return BlockDescriptor("minecraft:weeping_vines", {_BlockStateKeys.WeepingVinesAge: weeping_vines_age})

    @staticmethod
    def WetSponge() -> BlockDescriptor:
        """Factory for WetSponge"""
        return BlockDescriptor("minecraft:wet_sponge")

    @staticmethod
    def Wheat(growth: Growth) -> BlockDescriptor:
        """Factory for Wheat"""
        return BlockDescriptor("minecraft:wheat", {_BlockStateKeys.Growth: growth})

    @staticmethod
    def WhiteCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for WhiteCandle"""
        return BlockDescriptor("minecraft:white_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def WhiteCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for WhiteCandleCake"""
        return BlockDescriptor("minecraft:white_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def WhiteCarpet() -> BlockDescriptor:
        """Factory for WhiteCarpet"""
        return BlockDescriptor("minecraft:white_carpet")

    @staticmethod
    def WhiteConcrete() -> BlockDescriptor:
        """Factory for WhiteConcrete"""
        return BlockDescriptor("minecraft:white_concrete")

    @staticmethod
    def WhiteConcretePowder() -> BlockDescriptor:
        """Factory for WhiteConcretePowder"""
        return BlockDescriptor("minecraft:white_concrete_powder")

    @staticmethod
    def WhiteGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WhiteGlazedTerracotta"""
        return BlockDescriptor("minecraft:white_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WhiteShulkerBox() -> BlockDescriptor:
        """Factory for WhiteShulkerBox"""
        return BlockDescriptor("minecraft:white_shulker_box")

    @staticmethod
    def WhiteStainedGlass() -> BlockDescriptor:
        """Factory for WhiteStainedGlass"""
        return BlockDescriptor("minecraft:white_stained_glass")

    @staticmethod
    def WhiteStainedGlassPane() -> BlockDescriptor:
        """Factory for WhiteStainedGlassPane"""
        return BlockDescriptor("minecraft:white_stained_glass_pane")

    @staticmethod
    def WhiteTerracotta() -> BlockDescriptor:
        """Factory for WhiteTerracotta"""
        return BlockDescriptor("minecraft:white_terracotta")

    @staticmethod
    def WhiteTulip() -> BlockDescriptor:
        """Factory for WhiteTulip"""
        return BlockDescriptor("minecraft:white_tulip")

    @staticmethod
    def WhiteWool() -> BlockDescriptor:
        """Factory for WhiteWool"""
        return BlockDescriptor("minecraft:white_wool")

    @staticmethod
    def Wildflowers(growth: Growth, minecraft_cardinal_direction: CardinalDirection) -> BlockDescriptor:
        """Factory for Wildflowers"""
        return BlockDescriptor(
            "minecraft:wildflowers",
            {_BlockStateKeys.Growth: growth, _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction},
        )

    @staticmethod
    def WitherRose() -> BlockDescriptor:
        """Factory for WitherRose"""
        return BlockDescriptor("minecraft:wither_rose")

    @staticmethod
    def WitherSkeletonSkull(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WitherSkeletonSkull"""
        return BlockDescriptor("minecraft:wither_skeleton_skull", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def WoodenButton(button_pressed_bit: ButtonPressedBit, facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for WoodenButton"""
        return BlockDescriptor(
            "minecraft:wooden_button",
            {_BlockStateKeys.ButtonPressedBit: button_pressed_bit, _BlockStateKeys.FacingDirection: facing_direction},
        )

    @staticmethod
    def WoodenDoor(
        door_hinge_bit: DoorHingeBit,
        minecraft_cardinal_direction: CardinalDirection,
        open_bit: OpenBit,
        upper_block_bit: UpperBlockBit,
    ) -> BlockDescriptor:
        """Factory for WoodenDoor"""
        return BlockDescriptor(
            "minecraft:wooden_door",
            {
                _BlockStateKeys.DoorHingeBit: door_hinge_bit,
                _BlockStateKeys.MinecraftCardinalDirection: minecraft_cardinal_direction,
                _BlockStateKeys.OpenBit: open_bit,
                _BlockStateKeys.UpperBlockBit: upper_block_bit,
            },
        )

    @staticmethod
    def WoodenPressurePlate(redstone_signal: RedstoneSignal) -> BlockDescriptor:
        """Factory for WoodenPressurePlate"""
        return BlockDescriptor("minecraft:wooden_pressure_plate", {_BlockStateKeys.RedstoneSignal: redstone_signal})

    @staticmethod
    def YellowCandle(candles: Candles, lit: Lit) -> BlockDescriptor:
        """Factory for YellowCandle"""
        return BlockDescriptor("minecraft:yellow_candle", {_BlockStateKeys.Candles: candles, _BlockStateKeys.Lit: lit})

    @staticmethod
    def YellowCandleCake(lit: Lit) -> BlockDescriptor:
        """Factory for YellowCandleCake"""
        return BlockDescriptor("minecraft:yellow_candle_cake", {_BlockStateKeys.Lit: lit})

    @staticmethod
    def YellowCarpet() -> BlockDescriptor:
        """Factory for YellowCarpet"""
        return BlockDescriptor("minecraft:yellow_carpet")

    @staticmethod
    def YellowConcrete() -> BlockDescriptor:
        """Factory for YellowConcrete"""
        return BlockDescriptor("minecraft:yellow_concrete")

    @staticmethod
    def YellowConcretePowder() -> BlockDescriptor:
        """Factory for YellowConcretePowder"""
        return BlockDescriptor("minecraft:yellow_concrete_powder")

    @staticmethod
    def YellowGlazedTerracotta(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for YellowGlazedTerracotta"""
        return BlockDescriptor("minecraft:yellow_glazed_terracotta", {_BlockStateKeys.FacingDirection: facing_direction})

    @staticmethod
    def YellowShulkerBox() -> BlockDescriptor:
        """Factory for YellowShulkerBox"""
        return BlockDescriptor("minecraft:yellow_shulker_box")

    @staticmethod
    def YellowStainedGlass() -> BlockDescriptor:
        """Factory for YellowStainedGlass"""
        return BlockDescriptor("minecraft:yellow_stained_glass")

    @staticmethod
    def YellowStainedGlassPane() -> BlockDescriptor:
        """Factory for YellowStainedGlassPane"""
        return BlockDescriptor("minecraft:yellow_stained_glass_pane")

    @staticmethod
    def YellowTerracotta() -> BlockDescriptor:
        """Factory for YellowTerracotta"""
        return BlockDescriptor("minecraft:yellow_terracotta")

    @staticmethod
    def YellowWool() -> BlockDescriptor:
        """Factory for YellowWool"""
        return BlockDescriptor("minecraft:yellow_wool")

    @staticmethod
    def ZombieHead(facing_direction: FacingDirection) -> BlockDescriptor:
        """Factory for ZombieHead"""
        return BlockDescriptor("minecraft:zombie_head", {_BlockStateKeys.FacingDirection: facing_direction})
