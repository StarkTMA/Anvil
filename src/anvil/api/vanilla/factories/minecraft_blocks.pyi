from enum import StrEnum
from typing import Literal, TypedDict, Unpack

from anvil.lib.schemas import MinecraftBlockDescriptor

class BlockStateKeys(StrEnum):
    """Every vanilla block state name."""

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
    MinecraftConnectionDown = "minecraft:connection_down"
    MinecraftConnectionEast = "minecraft:connection_east"
    MinecraftConnectionNorth = "minecraft:connection_north"
    MinecraftConnectionSouth = "minecraft:connection_south"
    MinecraftConnectionUp = "minecraft:connection_up"
    MinecraftConnectionWest = "minecraft:connection_west"
    MinecraftCorner = "minecraft:corner"
    MinecraftFacingDirection = "minecraft:facing_direction"
    MinecraftMultiBlockPart = "minecraft:multi_block_part"
    MinecraftSixteenWayRotation = "minecraft:sixteen_way_rotation"
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
    PotentSulfurState = "potent_sulfur_state"
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

class AcaciaButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class AcaciaDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class AcaciaDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class AcaciaFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class AcaciaFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class AcaciaHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class AcaciaLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class AcaciaLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class AcaciaPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class AcaciaSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class AcaciaShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class AcaciaSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class AcaciaStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class AcaciaStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class AcaciaTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class AcaciaWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class AcaciaWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class ActivatorRailStates(TypedDict, total=False):
    rail_data_bit: bool | None
    rail_direction: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None

class AmethystClusterStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class AndesiteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class AndesiteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class AndesiteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class AndesiteWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class AnvilStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class AzaleaLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class AzaleaLeavesFloweredStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class BambooStates(TypedDict, total=False):
    age_bit: bool | None
    bamboo_leaf_size: Literal["no_leaves", "small_leaves", "large_leaves"] | None
    bamboo_stalk_thickness: Literal["thin", "thick"] | None

class BambooBlockStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class BambooButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BambooDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class BambooDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BambooFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class BambooFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class BambooHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class BambooMosaicDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BambooMosaicSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BambooMosaicStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BambooPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class BambooSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class BambooShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class BambooSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BambooStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BambooStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class BambooTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class BambooWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BarrelStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    open_bit: bool | None

class BasaltStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class BedStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    head_piece_bit: bool | None
    occupied_bit: bool | None

class BedrockStates(TypedDict, total=False):
    infiniburn_bit: bool | None

class BeeNestStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    honey_level: Literal[0, 1, 2, 3, 4, 5] | None

class BeehiveStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    honey_level: Literal[0, 1, 2, 3, 4, 5] | None

class BeetrootStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class BellStates(TypedDict, total=False):
    attachment: Literal["standing", "hanging", "side", "multiple"] | None
    direction: Literal[0, 1, 2, 3] | None
    toggle_bit: bool | None

class BigDripleafStates(TypedDict, total=False):
    big_dripleaf_head: bool | None
    big_dripleaf_tilt: Literal["none", "unstable", "partial_tilt", "full_tilt"] | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class BirchButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BirchDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class BirchDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BirchFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class BirchFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class BirchHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class BirchLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class BirchLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class BirchPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class BirchSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class BirchShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class BirchSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BirchStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BirchStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class BirchTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class BirchWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BirchWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class BlackCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class BlackCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class BlackConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlackConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlackConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BlackGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BlackStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class BlackWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlackWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlackWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BlackstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlackstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlackstoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BlackstoneWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class BlastFurnaceStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class BlueCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class BlueCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class BlueConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlueConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlueConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BlueGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BlueStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class BlueWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlueWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BlueWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BoneBlockStates(TypedDict, total=False):
    deprecated: Literal[0, 1, 2, 3] | None
    pillar_axis: Literal["y", "x", "z"] | None

class BorderBlockStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class BrainCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class BrainCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class BrewingStandStates(TypedDict, total=False):
    brewing_stand_slot_a_bit: bool | None
    brewing_stand_slot_b_bit: bool | None
    brewing_stand_slot_c_bit: bool | None

class BrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class BrownCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class BrownCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class BrownConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BrownConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BrownConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BrownGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class BrownMushroomBlockStates(TypedDict, total=False):
    huge_mushroom_bits: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class BrownStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class BrownWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BrownWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class BrownWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class BubbleColumnStates(TypedDict, total=False):
    drag_down: bool | None

class BubbleCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class BubbleCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class CactusStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class CakeStates(TypedDict, total=False):
    bite_counter: Literal[0, 1, 2, 3, 4, 5, 6] | None

class CalibratedSculkSensorStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    sculk_sensor_phase: Literal[0, 1, 2] | None

class CampfireStates(TypedDict, total=False):
    extinguished: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class CandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class CandleCakeStates(TypedDict, total=False):
    lit: bool | None

class CarrotsStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class CarvedPumpkinStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class CauldronStates(TypedDict, total=False):
    cauldron_liquid: Literal["water", "lava", "powder_snow"] | None
    fill_level: Literal[0, 1, 2, 3, 4, 5, 6] | None

class CaveVinesStates(TypedDict, total=False):
    growing_plant_age: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ]
        | None
    )

class CaveVinesBodyWithBerriesStates(TypedDict, total=False):
    growing_plant_age: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ]
        | None
    )

class CaveVinesHeadWithBerriesStates(TypedDict, total=False):
    growing_plant_age: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ]
        | None
    )

class ChainCommandBlockStates(TypedDict, total=False):
    conditional_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CherryButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CherryDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class CherryDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CherryFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class CherryFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class CherryHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class CherryLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class CherryLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class CherryPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class CherrySaplingStates(TypedDict, total=False):
    age_bit: bool | None

class CherryShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class CherrySlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CherryStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CherryStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class CherryTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class CherryWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CherryWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class ChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class ChippedAnvilStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class ChiseledBookshelfStates(TypedDict, total=False):
    books_stored: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
        ]
        | None
    )
    direction: Literal[0, 1, 2, 3] | None

class ChiseledQuartzBlockStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class ChorusFlowerStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class CinnabarBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CinnabarBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CinnabarBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CinnabarBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class CinnabarDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CinnabarSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CinnabarStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CinnabarWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class CobbledDeepslateDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CobbledDeepslateSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CobbledDeepslateStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CobbledDeepslateWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class CobblestoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CobblestoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CobblestoneWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class CocoaStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    direction: Literal[0, 1, 2, 3] | None

class ColoredTorchBlueStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class ColoredTorchGreenStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class ColoredTorchPurpleStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class ColoredTorchRedStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class CommandBlockStates(TypedDict, total=False):
    conditional_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class ComposterStates(TypedDict, total=False):
    composter_fill_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8] | None

class CompoundCreatorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None

class CopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class CopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class CopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class CopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class CopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class CopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class CopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class CopperTorchStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class CopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class CrafterStates(TypedDict, total=False):
    crafting: bool | None
    orientation: (
        Literal[
            "down_east",
            "down_north",
            "down_south",
            "down_west",
            "up_east",
            "up_north",
            "up_south",
            "up_west",
            "west_up",
            "east_up",
            "north_up",
            "south_up",
        ]
        | None
    )
    triggered_bit: bool | None

class CreakingHeartStates(TypedDict, total=False):
    creaking_heart_state: Literal["uprooted", "dormant", "awake"] | None
    natural: bool | None
    pillar_axis: Literal["y", "x", "z"] | None

class CreeperHeadStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CrimsonButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CrimsonDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class CrimsonDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CrimsonFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class CrimsonFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class CrimsonHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class CrimsonHyphaeStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class CrimsonPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class CrimsonShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class CrimsonSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CrimsonStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CrimsonStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class CrimsonStemStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class CrimsonTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class CrimsonWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CutRedSandstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CutRedSandstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CutSandstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CutSandstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CyanCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class CyanCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class CyanConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CyanConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CyanConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class CyanGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class CyanStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class CyanWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CyanWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class CyanWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class DamagedAnvilStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class DarkOakButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class DarkOakDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class DarkOakDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DarkOakFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class DarkOakFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class DarkOakHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class DarkOakLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class DarkOakLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class DarkOakPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class DarkOakSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class DarkOakShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class DarkOakSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DarkOakStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class DarkOakTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class DarkOakWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class DarkPrismarineDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DarkPrismarineSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DarkPrismarineStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class DarkoakStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class DarkoakWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class DaylightDetectorStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class DaylightDetectorInvertedStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class DeadBrainCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class DeadBrainCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class DeadBubbleCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class DeadBubbleCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class DeadFireCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class DeadFireCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class DeadHornCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class DeadHornCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class DeadTubeCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class DeadTubeCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class DecoratedPotStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None

class DeepslateStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class DeepslateBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DeepslateBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DeepslateBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class DeepslateBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class DeepslateTileDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DeepslateTileSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DeepslateTileStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class DeepslateTileWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class DetectorRailStates(TypedDict, total=False):
    rail_data_bit: bool | None
    rail_direction: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None

class DioriteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DioriteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DioriteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class DioriteWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class DispenserStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    triggered_bit: bool | None

class DoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class DragonHeadStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class DriedGhastStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    rehydration_level: Literal[0, 1, 2, 3] | None

class DropperStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    triggered_bit: bool | None

class ElementConstructorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None

class EndBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class EndPortalFrameStates(TypedDict, total=False):
    end_portal_eye_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class EndRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class EndStoneBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class EndStoneBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class EndStoneBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class EnderChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class ExposedCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class ExposedCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class ExposedCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class ExposedCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class ExposedCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class ExposedCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class ExposedCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class ExposedCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class ExposedCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class ExposedCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class ExposedDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class ExposedLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class FarmlandStates(TypedDict, total=False):
    moisturized_amount: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class FenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class FireStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class FireCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class FireCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class FlowerPotStates(TypedDict, total=False):
    update_bit: bool | None

class FlowingLavaStates(TypedDict, total=False):
    liquid_depth: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class FlowingWaterStates(TypedDict, total=False):
    liquid_depth: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class FrameStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    item_frame_map_bit: bool | None
    item_frame_photo_bit: bool | None

class FrostedIceStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class FurnaceStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class GlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class GlowFrameStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    item_frame_map_bit: bool | None
    item_frame_photo_bit: bool | None

class GlowLichenStates(TypedDict, total=False):
    multi_face_direction_bits: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
        ]
        | None
    )

class GoldenRailStates(TypedDict, total=False):
    rail_data_bit: bool | None
    rail_direction: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None

class GraniteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GraniteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GraniteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class GraniteWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class GrayCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class GrayCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class GrayConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GrayConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GrayConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class GrayGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class GrayStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class GrayWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GrayWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GrayWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class GreenCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class GreenCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class GreenConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GreenConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GreenConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class GreenGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class GreenStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class GreenWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GreenWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class GreenWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class GrindstoneStates(TypedDict, total=False):
    attachment: Literal["standing", "hanging", "side", "multiple"] | None
    direction: Literal[0, 1, 2, 3] | None

class HardBlackStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardBlueStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardBrownStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardCyanStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardGrayStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardGreenStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardLightBlueStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardLightGrayStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardLimeStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardMagentaStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardOrangeStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardPinkStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardPurpleStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardRedStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardWhiteStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HardYellowStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class HayBlockStates(TypedDict, total=False):
    deprecated: Literal[0, 1, 2, 3] | None
    pillar_axis: Literal["y", "x", "z"] | None

class HeavyWeightedPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class HopperStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    toggle_bit: bool | None

class HornCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class HornCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class InfestedDeepslateStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class IronBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class IronChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class IronDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class IronTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class JigsawStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    rotation: Literal[0, 1, 2, 3] | None

class JungleButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class JungleDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class JungleDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class JungleFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class JungleFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class JungleHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class JungleLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class JungleLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class JunglePressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class JungleSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class JungleShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class JungleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class JungleStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class JungleStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class JungleTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class JungleWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class JungleWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class KelpStates(TypedDict, total=False):
    kelp_age: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ]
        | None
    )

class LabTableStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None

class LadderStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class LanternStates(TypedDict, total=False):
    hanging: bool | None

class LargeAmethystBudStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class LargeFernStates(TypedDict, total=False):
    upper_block_bit: bool | None

class LavaStates(TypedDict, total=False):
    liquid_depth: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class LeafLitterStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class LecternStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None

class LeverStates(TypedDict, total=False):
    lever_direction: (
        Literal[
            "down_east_west",
            "east",
            "west",
            "south",
            "north",
            "up_north_south",
            "up_east_west",
            "down_north_south",
        ]
        | None
    )
    open_bit: bool | None

class LightBlueCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class LightBlueCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class LightBlueConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightBlueConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightBlueConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class LightBlueGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class LightBlueStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class LightBlueWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightBlueWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightBlueWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class LightGrayCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class LightGrayCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class LightGrayConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightGrayConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightGrayConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class LightGrayStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class LightGrayWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightGrayWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LightGrayWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class LightWeightedPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class LightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class LilacStates(TypedDict, total=False):
    upper_block_bit: bool | None

class LimeCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class LimeCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class LimeConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LimeConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LimeConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class LimeGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class LimeStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class LimeWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LimeWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class LimeWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class LitBlastFurnaceStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class LitFurnaceStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class LitPumpkinStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class LitSmokerStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class LoomStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None

class MagentaCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class MagentaCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class MagentaConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MagentaConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MagentaConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class MagentaGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class MagentaStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class MagentaWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MagentaWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MagentaWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class MangroveButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class MangroveDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class MangroveDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MangroveFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class MangroveFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class MangroveHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class MangroveLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class MangroveLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class MangrovePressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class MangrovePropaguleStates(TypedDict, total=False):
    hanging: bool | None
    propagule_stage: Literal[0, 1, 2, 3, 4] | None

class MangroveShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class MangroveSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MangroveStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class MangroveStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class MangroveTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class MangroveWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class MangroveWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class MaterialReducerStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None

class MediumAmethystBudStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class MelonStemStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class MossyCobblestoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MossyCobblestoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MossyCobblestoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class MossyCobblestoneWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class MossyStoneBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MossyStoneBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MossyStoneBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class MossyStoneBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class MudBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MudBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class MudBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class MudBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class MuddyMangroveRootsStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class MushroomStemStates(TypedDict, total=False):
    huge_mushroom_bits: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class NetherBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class NetherBrickFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class NetherBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class NetherBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class NetherBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class NetherWartStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class NormalStoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class NormalStoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class NormalStoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class OakDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OakFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class OakHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class OakLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class OakLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class OakSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class OakShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class OakSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OakStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class OakWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class ObserverStates(TypedDict, total=False):
    minecraft_facing_direction: (
        Literal["down", "up", "north", "south", "west", "east"] | None
    )
    powered_bit: bool | None

class OchreFroglightStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class OrangeCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class OrangeCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class OrangeConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OrangeConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OrangeConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class OrangeGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class OrangePoplarLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class OrangeStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class OrangeWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OrangeWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OrangeWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class OxidizedCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class OxidizedCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class OxidizedCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class OxidizedCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class OxidizedCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class OxidizedCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class OxidizedCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class OxidizedCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class OxidizedCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OxidizedCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class OxidizedDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class OxidizedLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class PaleHangingMossStates(TypedDict, total=False):
    tip: bool | None

class PaleMossCarpetStates(TypedDict, total=False):
    pale_moss_carpet_side_east: Literal["none", "short", "tall"] | None
    pale_moss_carpet_side_north: Literal["none", "short", "tall"] | None
    pale_moss_carpet_side_south: Literal["none", "short", "tall"] | None
    pale_moss_carpet_side_west: Literal["none", "short", "tall"] | None
    upper_block_bit: bool | None

class PaleOakButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PaleOakDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class PaleOakDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PaleOakFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class PaleOakFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class PaleOakHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class PaleOakLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class PaleOakLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PaleOakPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class PaleOakSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class PaleOakShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class PaleOakSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PaleOakStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PaleOakStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class PaleOakTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class PaleOakWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PaleOakWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PearlescentFroglightStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PeonyStates(TypedDict, total=False):
    upper_block_bit: bool | None

class PetrifiedOakDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PetrifiedOakSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PiglinHeadStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PinkCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class PinkCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class PinkConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PinkConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PinkConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PinkGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PinkPetalsStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class PinkStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class PinkWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PinkWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PinkWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PistonStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PistonArmCollisionStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PitcherCropStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    upper_block_bit: bool | None

class PitcherPlantStates(TypedDict, total=False):
    upper_block_bit: bool | None

class PlayerHeadStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PointedDripstoneStates(TypedDict, total=False):
    dripstone_thickness: Literal["tip", "frustum", "middle", "base", "merge"] | None
    hanging: bool | None

class PolishedAndesiteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedAndesiteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedAndesiteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedBasaltStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PolishedBlackstoneBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedBlackstoneBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedBlackstoneBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedBlackstoneBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedBlackstoneButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PolishedBlackstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedBlackstonePressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class PolishedBlackstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedBlackstoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedBlackstoneWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedCinnabarDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedCinnabarSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedCinnabarStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedCinnabarWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedDeepslateDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedDeepslateSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedDeepslateStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedDeepslateWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedDioriteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedDioriteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedDioriteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedGraniteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedGraniteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedGraniteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedSulfurDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedSulfurSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedSulfurStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedSulfurWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PolishedTuffDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedTuffSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PolishedTuffStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PolishedTuffWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PoplarButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PoplarDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class PoplarDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PoplarFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class PoplarFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class PoplarHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class PoplarLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PoplarPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class PoplarSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class PoplarShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class PoplarSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PoplarStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PoplarStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class PoplarTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class PoplarWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PoplarWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PortalStates(TypedDict, total=False):
    portal_axis: Literal["unknown", "x", "z"] | None

class PotatoesStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class PotentSulfurStates(TypedDict, total=False):
    potent_sulfur_state: (
        Literal["dry", "wet", "dormant", "erupting", "continuous"] | None
    )

class PoweredComparatorStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    output_lit_bit: bool | None
    output_subtract_bit: bool | None

class PoweredRepeaterStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    repeater_delay: Literal[0, 1, 2, 3] | None

class PrismarineBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PrismarineBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PrismarineBricksStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PrismarineDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PrismarineSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PrismarineStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PrismarineWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class PumpkinStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class PumpkinStemStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class PurpleCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class PurpleCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class PurpleConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PurpleConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PurpleConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PurpleGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class PurpleStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class PurpleWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PurpleWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PurpleWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class PurpurBlockStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PurpurDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PurpurPillarStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class PurpurSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class PurpurStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class QuartzBlockStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class QuartzDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class QuartzPillarStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class QuartzSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class QuartzStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class RailStates(TypedDict, total=False):
    rail_direction: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | None

class RedCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class RedCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class RedConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class RedGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class RedMushroomBlockStates(TypedDict, total=False):
    huge_mushroom_bits: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class RedNetherBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedNetherBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedNetherBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class RedNetherBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class RedPoplarLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class RedSandstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedSandstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedSandstoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class RedSandstoneWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class RedStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class RedWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class RedWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class RedstoneTorchStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class RedstoneWireStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class ReedsStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class RepeatingCommandBlockStates(TypedDict, total=False):
    conditional_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class ResinBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class ResinBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class ResinBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class ResinBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class ResinClumpStates(TypedDict, total=False):
    multi_face_direction_bits: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
        ]
        | None
    )

class RespawnAnchorStates(TypedDict, total=False):
    respawn_anchor_charge: Literal[0, 1, 2, 3, 4] | None

class RoseBushStates(TypedDict, total=False):
    upper_block_bit: bool | None

class SandstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SandstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SandstoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SandstoneWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class ScaffoldingStates(TypedDict, total=False):
    stability: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    stability_check: bool | None

class SculkCatalystStates(TypedDict, total=False):
    bloom: bool | None

class SculkSensorStates(TypedDict, total=False):
    sculk_sensor_phase: Literal[0, 1, 2] | None

class SculkShriekerStates(TypedDict, total=False):
    active: bool | None
    can_summon: bool | None

class SculkVeinStates(TypedDict, total=False):
    multi_face_direction_bits: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
        ]
        | None
    )

class SeaPickleStates(TypedDict, total=False):
    cluster_count: Literal[0, 1, 2, 3] | None
    dead_bit: bool | None

class SeagrassStates(TypedDict, total=False):
    sea_grass_type: Literal["default", "double_top", "double_bot"] | None

class ShelfMushroomStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class SilverGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class SkeletonSkullStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class SmallAmethystBudStates(TypedDict, total=False):
    minecraft_block_face: Literal["down", "up", "north", "south", "west", "east"] | None

class SmallDripleafBlockStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    upper_block_bit: bool | None

class SmokerStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class SmoothQuartzStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class SmoothQuartzDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothQuartzSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothQuartzStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SmoothRedSandstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothRedSandstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothRedSandstoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SmoothSandstoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothSandstoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothSandstoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SmoothStoneDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SmoothStoneSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SnifferEggStates(TypedDict, total=False):
    cracked_state: Literal["no_cracks", "cracked", "max_cracked"] | None

class SnowLayerStates(TypedDict, total=False):
    covered_bit: bool | None
    height: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class SoulCampfireStates(TypedDict, total=False):
    extinguished: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class SoulFireStates(TypedDict, total=False):
    age: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class SoulLanternStates(TypedDict, total=False):
    hanging: bool | None

class SoulTorchStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class SpruceButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class SpruceDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class SpruceDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SpruceFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class SpruceFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class SpruceHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class SpruceLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class SpruceLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class SprucePressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class SpruceSaplingStates(TypedDict, total=False):
    age_bit: bool | None

class SpruceShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class SpruceSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SpruceStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SpruceStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class SpruceTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class SpruceWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class SpruceWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StandingBannerStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class StandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class StickyPistonStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class StickyPistonArmCollisionStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class StoneBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class StoneBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class StoneBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class StoneBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class StoneButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class StonePressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class StoneStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class StonecutterBlockStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class StrawBedStates(TypedDict, total=False):
    head_piece_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    occupied_bit: bool | None

class StrippedAcaciaLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedAcaciaWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedBambooBlockStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedBirchLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedBirchWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedCherryLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedCherryWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedCrimsonHyphaeStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedCrimsonStemStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedDarkOakLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedDarkOakWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedJungleLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedJungleWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedMangroveLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedMangroveWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedOakLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedOakWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedPaleOakLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedPaleOakWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedPoplarLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedPoplarWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedSpruceLogStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedSpruceWoodStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedWarpedHyphaeStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StrippedWarpedStemStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class StructureBlockStates(TypedDict, total=False):
    structure_block_type: (
        Literal["data", "save", "load", "corner", "invalid", "export"] | None
    )

class SulfurBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SulfurBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SulfurBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SulfurBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class SulfurDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SulfurSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class SulfurSpikeStates(TypedDict, total=False):
    dripstone_thickness: Literal["tip", "frustum", "middle", "base", "merge"] | None
    hanging: bool | None

class SulfurStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class SulfurWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class SunflowerStates(TypedDict, total=False):
    upper_block_bit: bool | None

class SuspiciousGravelStates(TypedDict, total=False):
    brushed_progress: Literal[0, 1, 2, 3] | None
    hanging: bool | None

class SuspiciousSandStates(TypedDict, total=False):
    brushed_progress: Literal[0, 1, 2, 3] | None
    hanging: bool | None

class SweetBerryBushStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class TallGrassStates(TypedDict, total=False):
    upper_block_bit: bool | None

class TntStates(TypedDict, total=False):
    explode_bit: bool | None

class TorchStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class TorchflowerCropStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class TrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class TrappedChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class TrialSpawnerStates(TypedDict, total=False):
    ominous: bool | None
    trial_spawner_state: Literal[0, 1, 2, 3, 4, 5] | None

class TripWireStates(TypedDict, total=False):
    attached_bit: bool | None
    disarmed_bit: bool | None
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None
    powered_bit: bool | None
    suspended_bit: bool | None

class TripwireHookStates(TypedDict, total=False):
    attached_bit: bool | None
    direction: Literal[0, 1, 2, 3] | None
    powered_bit: bool | None

class TubeCoralFanStates(TypedDict, total=False):
    coral_fan_direction: Literal[0, 1] | None

class TubeCoralWallFanStates(TypedDict, total=False):
    coral_direction: Literal[0, 1, 2, 3] | None

class TuffBrickDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class TuffBrickSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class TuffBrickStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class TuffBrickWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class TuffDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class TuffSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class TuffStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class TuffWallStates(TypedDict, total=False):
    wall_connection_type_east: Literal["none", "short", "tall"] | None
    wall_connection_type_north: Literal["none", "short", "tall"] | None
    wall_connection_type_south: Literal["none", "short", "tall"] | None
    wall_connection_type_west: Literal["none", "short", "tall"] | None
    wall_post_bit: bool | None

class TurtleEggStates(TypedDict, total=False):
    cracked_state: Literal["no_cracks", "cracked", "max_cracked"] | None
    turtle_egg_count: Literal["one_egg", "two_egg", "three_egg", "four_egg"] | None

class TwistingVinesStates(TypedDict, total=False):
    twisting_vines_age: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ]
        | None
    )

class UnderwaterTntStates(TypedDict, total=False):
    explode_bit: bool | None

class UnderwaterTorchStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class UnlitRedstoneTorchStates(TypedDict, total=False):
    torch_facing_direction: (
        Literal["unknown", "west", "east", "north", "south", "top"] | None
    )

class UnpoweredComparatorStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    output_lit_bit: bool | None
    output_subtract_bit: bool | None

class UnpoweredRepeaterStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    repeater_delay: Literal[0, 1, 2, 3] | None

class VaultStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    ominous: bool | None
    vault_state: Literal["inactive", "active", "unlocking", "ejecting"] | None

class VerdantFroglightStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class VineStates(TypedDict, total=False):
    vine_direction_bits: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class WallBannerStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WarpedButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WarpedDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WarpedDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WarpedFenceStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WarpedFenceGateStates(TypedDict, total=False):
    in_wall_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None

class WarpedHangingSignStates(TypedDict, total=False):
    attached_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )
    hanging: bool | None

class WarpedHyphaeStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WarpedPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class WarpedShelfStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    powered_bit: bool | None
    powered_shelf_type: Literal[0, 1, 2, 3] | None

class WarpedSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WarpedStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WarpedStandingSignStates(TypedDict, total=False):
    ground_sign_direction: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class WarpedStemStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WarpedTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class WarpedWallSignStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WaterStates(TypedDict, total=False):
    liquid_depth: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None

class WaxedCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WaxedCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class WaxedCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WaxedCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WaxedCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class WaxedCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class WaxedCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WaxedDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedExposedCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WaxedExposedCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class WaxedExposedCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WaxedExposedCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedExposedCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WaxedExposedCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedExposedCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class WaxedExposedCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class WaxedExposedCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedExposedCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WaxedExposedDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedExposedLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class WaxedLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class WaxedOxidizedCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WaxedOxidizedCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class WaxedOxidizedCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WaxedOxidizedCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedOxidizedCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WaxedOxidizedCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedOxidizedCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class WaxedOxidizedCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class WaxedOxidizedCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedOxidizedCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WaxedOxidizedDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedOxidizedLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class WaxedWeatheredCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WaxedWeatheredCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class WaxedWeatheredCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WaxedWeatheredCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedWeatheredCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WaxedWeatheredCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WaxedWeatheredCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class WaxedWeatheredCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class WaxedWeatheredCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedWeatheredCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WaxedWeatheredDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WaxedWeatheredLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class WeatheredCopperBarsStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WeatheredCopperBulbStates(TypedDict, total=False):
    lit: bool | None
    powered_bit: bool | None

class WeatheredCopperChainStates(TypedDict, total=False):
    pillar_axis: Literal["y", "x", "z"] | None

class WeatheredCopperChestStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WeatheredCopperDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WeatheredCopperGolemStatueStates(TypedDict, total=False):
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WeatheredCopperLanternStates(TypedDict, total=False):
    hanging: bool | None

class WeatheredCopperTrapdoorStates(TypedDict, total=False):
    direction: Literal[0, 1, 2, 3] | None
    open_bit: bool | None
    upside_down_bit: bool | None

class WeatheredCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WeatheredCutCopperStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WeatheredDoubleCutCopperSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WeatheredLightningRodStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None
    powered_bit: bool | None

class WeepingVinesStates(TypedDict, total=False):
    weeping_vines_age: (
        Literal[
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
        ]
        | None
    )

class WheatStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None

class WhiteCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class WhiteCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class WhiteConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WhiteConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WhiteConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WhiteGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WhiteStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class WhiteWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WhiteWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class WhiteWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class WildflowersStates(TypedDict, total=False):
    growth: Literal[0, 1, 2, 3, 4, 5, 6, 7] | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None

class WitherSkeletonSkullStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WoodenButtonStates(TypedDict, total=False):
    button_pressed_bit: bool | None
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class WoodenDoorStates(TypedDict, total=False):
    door_hinge_bit: bool | None
    minecraft_cardinal_direction: Literal["south", "west", "north", "east"] | None
    open_bit: bool | None
    upper_block_bit: bool | None

class WoodenPressurePlateStates(TypedDict, total=False):
    redstone_signal: (
        Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] | None
    )

class YellowCandleStates(TypedDict, total=False):
    candles: Literal[0, 1, 2, 3] | None
    lit: bool | None

class YellowCandleCakeStates(TypedDict, total=False):
    lit: bool | None

class YellowConcreteDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class YellowConcreteSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class YellowConcreteStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class YellowGlazedTerracottaStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

class YellowPoplarLeavesStates(TypedDict, total=False):
    persistent_bit: bool | None
    update_bit: bool | None

class YellowStainedGlassPaneStates(TypedDict, total=False):
    minecraft_connection_east: bool | None
    minecraft_connection_north: bool | None
    minecraft_connection_south: bool | None
    minecraft_connection_west: bool | None

class YellowWoolDoubleSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class YellowWoolSlabStates(TypedDict, total=False):
    minecraft_vertical_half: Literal["bottom", "top"] | None

class YellowWoolStairsStates(TypedDict, total=False):
    minecraft_corner: (
        Literal["none", "inner_left", "inner_right", "outer_left", "outer_right"] | None
    )
    upside_down_bit: bool | None
    weirdo_direction: Literal[0, 1, 2, 3] | None

class ZombieHeadStates(TypedDict, total=False):
    facing_direction: Literal[0, 1, 2, 3, 4, 5] | None

def AcaciaButton(**states: Unpack[AcaciaButtonStates]) -> MinecraftBlockDescriptor: ...
def AcaciaDoor(**states: Unpack[AcaciaDoorStates]) -> MinecraftBlockDescriptor: ...
def AcaciaDoubleSlab(
    **states: Unpack[AcaciaDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaFence(**states: Unpack[AcaciaFenceStates]) -> MinecraftBlockDescriptor: ...
def AcaciaFenceGate(
    **states: Unpack[AcaciaFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaHangingSign(
    **states: Unpack[AcaciaHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaLeaves(**states: Unpack[AcaciaLeavesStates]) -> MinecraftBlockDescriptor: ...
def AcaciaLog(**states: Unpack[AcaciaLogStates]) -> MinecraftBlockDescriptor: ...
def AcaciaPlanks() -> MinecraftBlockDescriptor: ...
def AcaciaPressurePlate(
    **states: Unpack[AcaciaPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaSapling(
    **states: Unpack[AcaciaSaplingStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaShelf(**states: Unpack[AcaciaShelfStates]) -> MinecraftBlockDescriptor: ...
def AcaciaSlab(**states: Unpack[AcaciaSlabStates]) -> MinecraftBlockDescriptor: ...
def AcaciaStairs(**states: Unpack[AcaciaStairsStates]) -> MinecraftBlockDescriptor: ...
def AcaciaStandingSign(
    **states: Unpack[AcaciaStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaTrapdoor(
    **states: Unpack[AcaciaTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaWallSign(
    **states: Unpack[AcaciaWallSignStates],
) -> MinecraftBlockDescriptor: ...
def AcaciaWood(**states: Unpack[AcaciaWoodStates]) -> MinecraftBlockDescriptor: ...
def ActivatorRail(
    **states: Unpack[ActivatorRailStates],
) -> MinecraftBlockDescriptor: ...
def Air() -> MinecraftBlockDescriptor: ...
def Allium() -> MinecraftBlockDescriptor: ...
def Allow() -> MinecraftBlockDescriptor: ...
def AmethystBlock() -> MinecraftBlockDescriptor: ...
def AmethystCluster(
    **states: Unpack[AmethystClusterStates],
) -> MinecraftBlockDescriptor: ...
def AncientDebris() -> MinecraftBlockDescriptor: ...
def Andesite() -> MinecraftBlockDescriptor: ...
def AndesiteDoubleSlab(
    **states: Unpack[AndesiteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def AndesiteSlab(**states: Unpack[AndesiteSlabStates]) -> MinecraftBlockDescriptor: ...
def AndesiteStairs(
    **states: Unpack[AndesiteStairsStates],
) -> MinecraftBlockDescriptor: ...
def AndesiteWall(**states: Unpack[AndesiteWallStates]) -> MinecraftBlockDescriptor: ...
def Anvil(**states: Unpack[AnvilStates]) -> MinecraftBlockDescriptor: ...
def Azalea() -> MinecraftBlockDescriptor: ...
def AzaleaLeaves(**states: Unpack[AzaleaLeavesStates]) -> MinecraftBlockDescriptor: ...
def AzaleaLeavesFlowered(
    **states: Unpack[AzaleaLeavesFloweredStates],
) -> MinecraftBlockDescriptor: ...
def AzureBluet() -> MinecraftBlockDescriptor: ...
def Bamboo(**states: Unpack[BambooStates]) -> MinecraftBlockDescriptor: ...
def BambooBlock(**states: Unpack[BambooBlockStates]) -> MinecraftBlockDescriptor: ...
def BambooButton(**states: Unpack[BambooButtonStates]) -> MinecraftBlockDescriptor: ...
def BambooDoor(**states: Unpack[BambooDoorStates]) -> MinecraftBlockDescriptor: ...
def BambooDoubleSlab(
    **states: Unpack[BambooDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BambooFence(**states: Unpack[BambooFenceStates]) -> MinecraftBlockDescriptor: ...
def BambooFenceGate(
    **states: Unpack[BambooFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def BambooHangingSign(
    **states: Unpack[BambooHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def BambooMosaic() -> MinecraftBlockDescriptor: ...
def BambooMosaicDoubleSlab(
    **states: Unpack[BambooMosaicDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BambooMosaicSlab(
    **states: Unpack[BambooMosaicSlabStates],
) -> MinecraftBlockDescriptor: ...
def BambooMosaicStairs(
    **states: Unpack[BambooMosaicStairsStates],
) -> MinecraftBlockDescriptor: ...
def BambooPlanks() -> MinecraftBlockDescriptor: ...
def BambooPressurePlate(
    **states: Unpack[BambooPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def BambooSapling(
    **states: Unpack[BambooSaplingStates],
) -> MinecraftBlockDescriptor: ...
def BambooShelf(**states: Unpack[BambooShelfStates]) -> MinecraftBlockDescriptor: ...
def BambooSlab(**states: Unpack[BambooSlabStates]) -> MinecraftBlockDescriptor: ...
def BambooStairs(**states: Unpack[BambooStairsStates]) -> MinecraftBlockDescriptor: ...
def BambooStandingSign(
    **states: Unpack[BambooStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def BambooTrapdoor(
    **states: Unpack[BambooTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def BambooWallSign(
    **states: Unpack[BambooWallSignStates],
) -> MinecraftBlockDescriptor: ...
def Barrel(**states: Unpack[BarrelStates]) -> MinecraftBlockDescriptor: ...
def Barrier() -> MinecraftBlockDescriptor: ...
def Basalt(**states: Unpack[BasaltStates]) -> MinecraftBlockDescriptor: ...
def Beacon() -> MinecraftBlockDescriptor: ...
def Bed(**states: Unpack[BedStates]) -> MinecraftBlockDescriptor: ...
def Bedrock(**states: Unpack[BedrockStates]) -> MinecraftBlockDescriptor: ...
def BeeNest(**states: Unpack[BeeNestStates]) -> MinecraftBlockDescriptor: ...
def Beehive(**states: Unpack[BeehiveStates]) -> MinecraftBlockDescriptor: ...
def Beetroot(**states: Unpack[BeetrootStates]) -> MinecraftBlockDescriptor: ...
def Bell(**states: Unpack[BellStates]) -> MinecraftBlockDescriptor: ...
def BigDripleaf(**states: Unpack[BigDripleafStates]) -> MinecraftBlockDescriptor: ...
def BirchButton(**states: Unpack[BirchButtonStates]) -> MinecraftBlockDescriptor: ...
def BirchDoor(**states: Unpack[BirchDoorStates]) -> MinecraftBlockDescriptor: ...
def BirchDoubleSlab(
    **states: Unpack[BirchDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BirchFence(**states: Unpack[BirchFenceStates]) -> MinecraftBlockDescriptor: ...
def BirchFenceGate(
    **states: Unpack[BirchFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def BirchHangingSign(
    **states: Unpack[BirchHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def BirchLeaves(**states: Unpack[BirchLeavesStates]) -> MinecraftBlockDescriptor: ...
def BirchLog(**states: Unpack[BirchLogStates]) -> MinecraftBlockDescriptor: ...
def BirchPlanks() -> MinecraftBlockDescriptor: ...
def BirchPressurePlate(
    **states: Unpack[BirchPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def BirchSapling(**states: Unpack[BirchSaplingStates]) -> MinecraftBlockDescriptor: ...
def BirchShelf(**states: Unpack[BirchShelfStates]) -> MinecraftBlockDescriptor: ...
def BirchSlab(**states: Unpack[BirchSlabStates]) -> MinecraftBlockDescriptor: ...
def BirchStairs(**states: Unpack[BirchStairsStates]) -> MinecraftBlockDescriptor: ...
def BirchStandingSign(
    **states: Unpack[BirchStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def BirchTrapdoor(
    **states: Unpack[BirchTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def BirchWallSign(
    **states: Unpack[BirchWallSignStates],
) -> MinecraftBlockDescriptor: ...
def BirchWood(**states: Unpack[BirchWoodStates]) -> MinecraftBlockDescriptor: ...
def BlackCandle(**states: Unpack[BlackCandleStates]) -> MinecraftBlockDescriptor: ...
def BlackCandleCake(
    **states: Unpack[BlackCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def BlackCarpet() -> MinecraftBlockDescriptor: ...
def BlackConcrete() -> MinecraftBlockDescriptor: ...
def BlackConcreteDoubleSlab(
    **states: Unpack[BlackConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlackConcretePowder() -> MinecraftBlockDescriptor: ...
def BlackConcreteSlab(
    **states: Unpack[BlackConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlackConcreteStairs(
    **states: Unpack[BlackConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def BlackGlazedTerracotta(
    **states: Unpack[BlackGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def BlackShulkerBox() -> MinecraftBlockDescriptor: ...
def BlackStainedGlass() -> MinecraftBlockDescriptor: ...
def BlackStainedGlassPane(
    **states: Unpack[BlackStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def BlackTerracotta() -> MinecraftBlockDescriptor: ...
def BlackWool() -> MinecraftBlockDescriptor: ...
def BlackWoolDoubleSlab(
    **states: Unpack[BlackWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlackWoolSlab(
    **states: Unpack[BlackWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlackWoolStairs(
    **states: Unpack[BlackWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def Blackstone() -> MinecraftBlockDescriptor: ...
def BlackstoneDoubleSlab(
    **states: Unpack[BlackstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlackstoneSlab(
    **states: Unpack[BlackstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlackstoneStairs(
    **states: Unpack[BlackstoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def BlackstoneWall(
    **states: Unpack[BlackstoneWallStates],
) -> MinecraftBlockDescriptor: ...
def BlastFurnace(**states: Unpack[BlastFurnaceStates]) -> MinecraftBlockDescriptor: ...
def BlueCandle(**states: Unpack[BlueCandleStates]) -> MinecraftBlockDescriptor: ...
def BlueCandleCake(
    **states: Unpack[BlueCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def BlueCarpet() -> MinecraftBlockDescriptor: ...
def BlueConcrete() -> MinecraftBlockDescriptor: ...
def BlueConcreteDoubleSlab(
    **states: Unpack[BlueConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlueConcretePowder() -> MinecraftBlockDescriptor: ...
def BlueConcreteSlab(
    **states: Unpack[BlueConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlueConcreteStairs(
    **states: Unpack[BlueConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def BlueGlazedTerracotta(
    **states: Unpack[BlueGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def BlueIce() -> MinecraftBlockDescriptor: ...
def BlueOrchid() -> MinecraftBlockDescriptor: ...
def BlueShulkerBox() -> MinecraftBlockDescriptor: ...
def BlueStainedGlass() -> MinecraftBlockDescriptor: ...
def BlueStainedGlassPane(
    **states: Unpack[BlueStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def BlueTerracotta() -> MinecraftBlockDescriptor: ...
def BlueWool() -> MinecraftBlockDescriptor: ...
def BlueWoolDoubleSlab(
    **states: Unpack[BlueWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BlueWoolSlab(**states: Unpack[BlueWoolSlabStates]) -> MinecraftBlockDescriptor: ...
def BlueWoolStairs(
    **states: Unpack[BlueWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def BoneBlock(**states: Unpack[BoneBlockStates]) -> MinecraftBlockDescriptor: ...
def Bookshelf() -> MinecraftBlockDescriptor: ...
def BorderBlock(**states: Unpack[BorderBlockStates]) -> MinecraftBlockDescriptor: ...
def BrainCoral() -> MinecraftBlockDescriptor: ...
def BrainCoralBlock() -> MinecraftBlockDescriptor: ...
def BrainCoralFan(
    **states: Unpack[BrainCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def BrainCoralWallFan(
    **states: Unpack[BrainCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def BrewingStand(**states: Unpack[BrewingStandStates]) -> MinecraftBlockDescriptor: ...
def BrickBlock() -> MinecraftBlockDescriptor: ...
def BrickDoubleSlab(
    **states: Unpack[BrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BrickSlab(**states: Unpack[BrickSlabStates]) -> MinecraftBlockDescriptor: ...
def BrickStairs(**states: Unpack[BrickStairsStates]) -> MinecraftBlockDescriptor: ...
def BrickWall(**states: Unpack[BrickWallStates]) -> MinecraftBlockDescriptor: ...
def BrownCandle(**states: Unpack[BrownCandleStates]) -> MinecraftBlockDescriptor: ...
def BrownCandleCake(
    **states: Unpack[BrownCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def BrownCarpet() -> MinecraftBlockDescriptor: ...
def BrownConcrete() -> MinecraftBlockDescriptor: ...
def BrownConcreteDoubleSlab(
    **states: Unpack[BrownConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BrownConcretePowder() -> MinecraftBlockDescriptor: ...
def BrownConcreteSlab(
    **states: Unpack[BrownConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def BrownConcreteStairs(
    **states: Unpack[BrownConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def BrownGlazedTerracotta(
    **states: Unpack[BrownGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def BrownMushroom() -> MinecraftBlockDescriptor: ...
def BrownMushroomBlock(
    **states: Unpack[BrownMushroomBlockStates],
) -> MinecraftBlockDescriptor: ...
def BrownShulkerBox() -> MinecraftBlockDescriptor: ...
def BrownStainedGlass() -> MinecraftBlockDescriptor: ...
def BrownStainedGlassPane(
    **states: Unpack[BrownStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def BrownTerracotta() -> MinecraftBlockDescriptor: ...
def BrownWool() -> MinecraftBlockDescriptor: ...
def BrownWoolDoubleSlab(
    **states: Unpack[BrownWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def BrownWoolSlab(
    **states: Unpack[BrownWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def BrownWoolStairs(
    **states: Unpack[BrownWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def BubbleColumn(**states: Unpack[BubbleColumnStates]) -> MinecraftBlockDescriptor: ...
def BubbleCoral() -> MinecraftBlockDescriptor: ...
def BubbleCoralBlock() -> MinecraftBlockDescriptor: ...
def BubbleCoralFan(
    **states: Unpack[BubbleCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def BubbleCoralWallFan(
    **states: Unpack[BubbleCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def BuddingAmethyst() -> MinecraftBlockDescriptor: ...
def Bush() -> MinecraftBlockDescriptor: ...
def Cactus(**states: Unpack[CactusStates]) -> MinecraftBlockDescriptor: ...
def CactusFlower() -> MinecraftBlockDescriptor: ...
def Cake(**states: Unpack[CakeStates]) -> MinecraftBlockDescriptor: ...
def Calcite() -> MinecraftBlockDescriptor: ...
def CalibratedSculkSensor(
    **states: Unpack[CalibratedSculkSensorStates],
) -> MinecraftBlockDescriptor: ...
def Camera() -> MinecraftBlockDescriptor: ...
def Campfire(**states: Unpack[CampfireStates]) -> MinecraftBlockDescriptor: ...
def Candle(**states: Unpack[CandleStates]) -> MinecraftBlockDescriptor: ...
def CandleCake(**states: Unpack[CandleCakeStates]) -> MinecraftBlockDescriptor: ...
def Carrots(**states: Unpack[CarrotsStates]) -> MinecraftBlockDescriptor: ...
def CartographyTable() -> MinecraftBlockDescriptor: ...
def CarvedPumpkin(
    **states: Unpack[CarvedPumpkinStates],
) -> MinecraftBlockDescriptor: ...
def Cauldron(**states: Unpack[CauldronStates]) -> MinecraftBlockDescriptor: ...
def CaveVines(**states: Unpack[CaveVinesStates]) -> MinecraftBlockDescriptor: ...
def CaveVinesBodyWithBerries(
    **states: Unpack[CaveVinesBodyWithBerriesStates],
) -> MinecraftBlockDescriptor: ...
def CaveVinesHeadWithBerries(
    **states: Unpack[CaveVinesHeadWithBerriesStates],
) -> MinecraftBlockDescriptor: ...
def ChainCommandBlock(
    **states: Unpack[ChainCommandBlockStates],
) -> MinecraftBlockDescriptor: ...
def ChemicalHeat() -> MinecraftBlockDescriptor: ...
def CherryButton(**states: Unpack[CherryButtonStates]) -> MinecraftBlockDescriptor: ...
def CherryDoor(**states: Unpack[CherryDoorStates]) -> MinecraftBlockDescriptor: ...
def CherryDoubleSlab(
    **states: Unpack[CherryDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CherryFence(**states: Unpack[CherryFenceStates]) -> MinecraftBlockDescriptor: ...
def CherryFenceGate(
    **states: Unpack[CherryFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def CherryHangingSign(
    **states: Unpack[CherryHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def CherryLeaves(**states: Unpack[CherryLeavesStates]) -> MinecraftBlockDescriptor: ...
def CherryLog(**states: Unpack[CherryLogStates]) -> MinecraftBlockDescriptor: ...
def CherryPlanks() -> MinecraftBlockDescriptor: ...
def CherryPressurePlate(
    **states: Unpack[CherryPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def CherrySapling(
    **states: Unpack[CherrySaplingStates],
) -> MinecraftBlockDescriptor: ...
def CherryShelf(**states: Unpack[CherryShelfStates]) -> MinecraftBlockDescriptor: ...
def CherrySlab(**states: Unpack[CherrySlabStates]) -> MinecraftBlockDescriptor: ...
def CherryStairs(**states: Unpack[CherryStairsStates]) -> MinecraftBlockDescriptor: ...
def CherryStandingSign(
    **states: Unpack[CherryStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def CherryTrapdoor(
    **states: Unpack[CherryTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def CherryWallSign(
    **states: Unpack[CherryWallSignStates],
) -> MinecraftBlockDescriptor: ...
def CherryWood(**states: Unpack[CherryWoodStates]) -> MinecraftBlockDescriptor: ...
def Chest(**states: Unpack[ChestStates]) -> MinecraftBlockDescriptor: ...
def ChippedAnvil(**states: Unpack[ChippedAnvilStates]) -> MinecraftBlockDescriptor: ...
def ChiseledBookshelf(
    **states: Unpack[ChiseledBookshelfStates],
) -> MinecraftBlockDescriptor: ...
def ChiseledCinnabar() -> MinecraftBlockDescriptor: ...
def ChiseledCopper() -> MinecraftBlockDescriptor: ...
def ChiseledDeepslate() -> MinecraftBlockDescriptor: ...
def ChiseledNetherBricks() -> MinecraftBlockDescriptor: ...
def ChiseledPolishedBlackstone() -> MinecraftBlockDescriptor: ...
def ChiseledQuartzBlock(
    **states: Unpack[ChiseledQuartzBlockStates],
) -> MinecraftBlockDescriptor: ...
def ChiseledRedSandstone() -> MinecraftBlockDescriptor: ...
def ChiseledResinBricks() -> MinecraftBlockDescriptor: ...
def ChiseledSandstone() -> MinecraftBlockDescriptor: ...
def ChiseledStoneBricks() -> MinecraftBlockDescriptor: ...
def ChiseledSulfur() -> MinecraftBlockDescriptor: ...
def ChiseledTuff() -> MinecraftBlockDescriptor: ...
def ChiseledTuffBricks() -> MinecraftBlockDescriptor: ...
def ChorusFlower(**states: Unpack[ChorusFlowerStates]) -> MinecraftBlockDescriptor: ...
def ChorusPlant() -> MinecraftBlockDescriptor: ...
def Cinnabar() -> MinecraftBlockDescriptor: ...
def CinnabarBrickDoubleSlab(
    **states: Unpack[CinnabarBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CinnabarBrickSlab(
    **states: Unpack[CinnabarBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def CinnabarBrickStairs(
    **states: Unpack[CinnabarBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def CinnabarBrickWall(
    **states: Unpack[CinnabarBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def CinnabarBricks() -> MinecraftBlockDescriptor: ...
def CinnabarDoubleSlab(
    **states: Unpack[CinnabarDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CinnabarSlab(**states: Unpack[CinnabarSlabStates]) -> MinecraftBlockDescriptor: ...
def CinnabarStairs(
    **states: Unpack[CinnabarStairsStates],
) -> MinecraftBlockDescriptor: ...
def CinnabarWall(**states: Unpack[CinnabarWallStates]) -> MinecraftBlockDescriptor: ...
def Clay() -> MinecraftBlockDescriptor: ...
def ClosedEyeblossom() -> MinecraftBlockDescriptor: ...
def CoalBlock() -> MinecraftBlockDescriptor: ...
def CoalOre() -> MinecraftBlockDescriptor: ...
def CoarseDirt() -> MinecraftBlockDescriptor: ...
def CobbledDeepslate() -> MinecraftBlockDescriptor: ...
def CobbledDeepslateDoubleSlab(
    **states: Unpack[CobbledDeepslateDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CobbledDeepslateSlab(
    **states: Unpack[CobbledDeepslateSlabStates],
) -> MinecraftBlockDescriptor: ...
def CobbledDeepslateStairs(
    **states: Unpack[CobbledDeepslateStairsStates],
) -> MinecraftBlockDescriptor: ...
def CobbledDeepslateWall(
    **states: Unpack[CobbledDeepslateWallStates],
) -> MinecraftBlockDescriptor: ...
def Cobblestone() -> MinecraftBlockDescriptor: ...
def CobblestoneDoubleSlab(
    **states: Unpack[CobblestoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CobblestoneSlab(
    **states: Unpack[CobblestoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def CobblestoneWall(
    **states: Unpack[CobblestoneWallStates],
) -> MinecraftBlockDescriptor: ...
def Cocoa(**states: Unpack[CocoaStates]) -> MinecraftBlockDescriptor: ...
def ColoredTorchBlue(
    **states: Unpack[ColoredTorchBlueStates],
) -> MinecraftBlockDescriptor: ...
def ColoredTorchGreen(
    **states: Unpack[ColoredTorchGreenStates],
) -> MinecraftBlockDescriptor: ...
def ColoredTorchPurple(
    **states: Unpack[ColoredTorchPurpleStates],
) -> MinecraftBlockDescriptor: ...
def ColoredTorchRed(
    **states: Unpack[ColoredTorchRedStates],
) -> MinecraftBlockDescriptor: ...
def CommandBlock(**states: Unpack[CommandBlockStates]) -> MinecraftBlockDescriptor: ...
def Composter(**states: Unpack[ComposterStates]) -> MinecraftBlockDescriptor: ...
def CompoundCreator(
    **states: Unpack[CompoundCreatorStates],
) -> MinecraftBlockDescriptor: ...
def Conduit() -> MinecraftBlockDescriptor: ...
def CopperBars(**states: Unpack[CopperBarsStates]) -> MinecraftBlockDescriptor: ...
def CopperBlock() -> MinecraftBlockDescriptor: ...
def CopperBulb(**states: Unpack[CopperBulbStates]) -> MinecraftBlockDescriptor: ...
def CopperChain(**states: Unpack[CopperChainStates]) -> MinecraftBlockDescriptor: ...
def CopperChest(**states: Unpack[CopperChestStates]) -> MinecraftBlockDescriptor: ...
def CopperDoor(**states: Unpack[CopperDoorStates]) -> MinecraftBlockDescriptor: ...
def CopperGolemStatue(
    **states: Unpack[CopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def CopperGrate() -> MinecraftBlockDescriptor: ...
def CopperLantern(
    **states: Unpack[CopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def CopperOre() -> MinecraftBlockDescriptor: ...
def CopperTorch(**states: Unpack[CopperTorchStates]) -> MinecraftBlockDescriptor: ...
def CopperTrapdoor(
    **states: Unpack[CopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def Cornflower() -> MinecraftBlockDescriptor: ...
def CrackedDeepslateBricks() -> MinecraftBlockDescriptor: ...
def CrackedDeepslateTiles() -> MinecraftBlockDescriptor: ...
def CrackedNetherBricks() -> MinecraftBlockDescriptor: ...
def CrackedPolishedBlackstoneBricks() -> MinecraftBlockDescriptor: ...
def CrackedStoneBricks() -> MinecraftBlockDescriptor: ...
def Crafter(**states: Unpack[CrafterStates]) -> MinecraftBlockDescriptor: ...
def CraftingTable() -> MinecraftBlockDescriptor: ...
def CreakingHeart(
    **states: Unpack[CreakingHeartStates],
) -> MinecraftBlockDescriptor: ...
def CreeperHead(**states: Unpack[CreeperHeadStates]) -> MinecraftBlockDescriptor: ...
def CrimsonButton(
    **states: Unpack[CrimsonButtonStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonDoor(**states: Unpack[CrimsonDoorStates]) -> MinecraftBlockDescriptor: ...
def CrimsonDoubleSlab(
    **states: Unpack[CrimsonDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonFence(**states: Unpack[CrimsonFenceStates]) -> MinecraftBlockDescriptor: ...
def CrimsonFenceGate(
    **states: Unpack[CrimsonFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonFungus() -> MinecraftBlockDescriptor: ...
def CrimsonHangingSign(
    **states: Unpack[CrimsonHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonHyphae(
    **states: Unpack[CrimsonHyphaeStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonNylium() -> MinecraftBlockDescriptor: ...
def CrimsonPlanks() -> MinecraftBlockDescriptor: ...
def CrimsonPressurePlate(
    **states: Unpack[CrimsonPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonRoots() -> MinecraftBlockDescriptor: ...
def CrimsonShelf(**states: Unpack[CrimsonShelfStates]) -> MinecraftBlockDescriptor: ...
def CrimsonSlab(**states: Unpack[CrimsonSlabStates]) -> MinecraftBlockDescriptor: ...
def CrimsonStairs(
    **states: Unpack[CrimsonStairsStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonStandingSign(
    **states: Unpack[CrimsonStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonStem(**states: Unpack[CrimsonStemStates]) -> MinecraftBlockDescriptor: ...
def CrimsonTrapdoor(
    **states: Unpack[CrimsonTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def CrimsonWallSign(
    **states: Unpack[CrimsonWallSignStates],
) -> MinecraftBlockDescriptor: ...
def CryingObsidian() -> MinecraftBlockDescriptor: ...
def CutCopper() -> MinecraftBlockDescriptor: ...
def CutCopperSlab(
    **states: Unpack[CutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def CutCopperStairs(
    **states: Unpack[CutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def CutRedSandstone() -> MinecraftBlockDescriptor: ...
def CutRedSandstoneDoubleSlab(
    **states: Unpack[CutRedSandstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CutRedSandstoneSlab(
    **states: Unpack[CutRedSandstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def CutSandstone() -> MinecraftBlockDescriptor: ...
def CutSandstoneDoubleSlab(
    **states: Unpack[CutSandstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CutSandstoneSlab(
    **states: Unpack[CutSandstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def CyanCandle(**states: Unpack[CyanCandleStates]) -> MinecraftBlockDescriptor: ...
def CyanCandleCake(
    **states: Unpack[CyanCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def CyanCarpet() -> MinecraftBlockDescriptor: ...
def CyanConcrete() -> MinecraftBlockDescriptor: ...
def CyanConcreteDoubleSlab(
    **states: Unpack[CyanConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CyanConcretePowder() -> MinecraftBlockDescriptor: ...
def CyanConcreteSlab(
    **states: Unpack[CyanConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def CyanConcreteStairs(
    **states: Unpack[CyanConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def CyanGlazedTerracotta(
    **states: Unpack[CyanGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def CyanShulkerBox() -> MinecraftBlockDescriptor: ...
def CyanStainedGlass() -> MinecraftBlockDescriptor: ...
def CyanStainedGlassPane(
    **states: Unpack[CyanStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def CyanTerracotta() -> MinecraftBlockDescriptor: ...
def CyanWool() -> MinecraftBlockDescriptor: ...
def CyanWoolDoubleSlab(
    **states: Unpack[CyanWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def CyanWoolSlab(**states: Unpack[CyanWoolSlabStates]) -> MinecraftBlockDescriptor: ...
def CyanWoolStairs(
    **states: Unpack[CyanWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def DamagedAnvil(**states: Unpack[DamagedAnvilStates]) -> MinecraftBlockDescriptor: ...
def Dandelion() -> MinecraftBlockDescriptor: ...
def DarkOakButton(
    **states: Unpack[DarkOakButtonStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakDoor(**states: Unpack[DarkOakDoorStates]) -> MinecraftBlockDescriptor: ...
def DarkOakDoubleSlab(
    **states: Unpack[DarkOakDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakFence(**states: Unpack[DarkOakFenceStates]) -> MinecraftBlockDescriptor: ...
def DarkOakFenceGate(
    **states: Unpack[DarkOakFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakHangingSign(
    **states: Unpack[DarkOakHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakLeaves(
    **states: Unpack[DarkOakLeavesStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakLog(**states: Unpack[DarkOakLogStates]) -> MinecraftBlockDescriptor: ...
def DarkOakPlanks() -> MinecraftBlockDescriptor: ...
def DarkOakPressurePlate(
    **states: Unpack[DarkOakPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakSapling(
    **states: Unpack[DarkOakSaplingStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakShelf(**states: Unpack[DarkOakShelfStates]) -> MinecraftBlockDescriptor: ...
def DarkOakSlab(**states: Unpack[DarkOakSlabStates]) -> MinecraftBlockDescriptor: ...
def DarkOakStairs(
    **states: Unpack[DarkOakStairsStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakTrapdoor(
    **states: Unpack[DarkOakTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def DarkOakWood(**states: Unpack[DarkOakWoodStates]) -> MinecraftBlockDescriptor: ...
def DarkPrismarine() -> MinecraftBlockDescriptor: ...
def DarkPrismarineDoubleSlab(
    **states: Unpack[DarkPrismarineDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def DarkPrismarineSlab(
    **states: Unpack[DarkPrismarineSlabStates],
) -> MinecraftBlockDescriptor: ...
def DarkPrismarineStairs(
    **states: Unpack[DarkPrismarineStairsStates],
) -> MinecraftBlockDescriptor: ...
def DarkoakStandingSign(
    **states: Unpack[DarkoakStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def DarkoakWallSign(
    **states: Unpack[DarkoakWallSignStates],
) -> MinecraftBlockDescriptor: ...
def DaylightDetector(
    **states: Unpack[DaylightDetectorStates],
) -> MinecraftBlockDescriptor: ...
def DaylightDetectorInverted(
    **states: Unpack[DaylightDetectorInvertedStates],
) -> MinecraftBlockDescriptor: ...
def DeadBrainCoral() -> MinecraftBlockDescriptor: ...
def DeadBrainCoralBlock() -> MinecraftBlockDescriptor: ...
def DeadBrainCoralFan(
    **states: Unpack[DeadBrainCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadBrainCoralWallFan(
    **states: Unpack[DeadBrainCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadBubbleCoral() -> MinecraftBlockDescriptor: ...
def DeadBubbleCoralBlock() -> MinecraftBlockDescriptor: ...
def DeadBubbleCoralFan(
    **states: Unpack[DeadBubbleCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadBubbleCoralWallFan(
    **states: Unpack[DeadBubbleCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadFireCoral() -> MinecraftBlockDescriptor: ...
def DeadFireCoralBlock() -> MinecraftBlockDescriptor: ...
def DeadFireCoralFan(
    **states: Unpack[DeadFireCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadFireCoralWallFan(
    **states: Unpack[DeadFireCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadHornCoral() -> MinecraftBlockDescriptor: ...
def DeadHornCoralBlock() -> MinecraftBlockDescriptor: ...
def DeadHornCoralFan(
    **states: Unpack[DeadHornCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadHornCoralWallFan(
    **states: Unpack[DeadHornCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadTubeCoral() -> MinecraftBlockDescriptor: ...
def DeadTubeCoralBlock() -> MinecraftBlockDescriptor: ...
def DeadTubeCoralFan(
    **states: Unpack[DeadTubeCoralFanStates],
) -> MinecraftBlockDescriptor: ...
def DeadTubeCoralWallFan(
    **states: Unpack[DeadTubeCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def Deadbush() -> MinecraftBlockDescriptor: ...
def DecoratedPot(**states: Unpack[DecoratedPotStates]) -> MinecraftBlockDescriptor: ...
def Deepslate(**states: Unpack[DeepslateStates]) -> MinecraftBlockDescriptor: ...
def DeepslateBrickDoubleSlab(
    **states: Unpack[DeepslateBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateBrickSlab(
    **states: Unpack[DeepslateBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateBrickStairs(
    **states: Unpack[DeepslateBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateBrickWall(
    **states: Unpack[DeepslateBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateBricks() -> MinecraftBlockDescriptor: ...
def DeepslateCoalOre() -> MinecraftBlockDescriptor: ...
def DeepslateCopperOre() -> MinecraftBlockDescriptor: ...
def DeepslateDiamondOre() -> MinecraftBlockDescriptor: ...
def DeepslateEmeraldOre() -> MinecraftBlockDescriptor: ...
def DeepslateGoldOre() -> MinecraftBlockDescriptor: ...
def DeepslateIronOre() -> MinecraftBlockDescriptor: ...
def DeepslateLapisOre() -> MinecraftBlockDescriptor: ...
def DeepslateRedstoneOre() -> MinecraftBlockDescriptor: ...
def DeepslateTileDoubleSlab(
    **states: Unpack[DeepslateTileDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateTileSlab(
    **states: Unpack[DeepslateTileSlabStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateTileStairs(
    **states: Unpack[DeepslateTileStairsStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateTileWall(
    **states: Unpack[DeepslateTileWallStates],
) -> MinecraftBlockDescriptor: ...
def DeepslateTiles() -> MinecraftBlockDescriptor: ...
def Deny() -> MinecraftBlockDescriptor: ...
def DetectorRail(**states: Unpack[DetectorRailStates]) -> MinecraftBlockDescriptor: ...
def DiamondBlock() -> MinecraftBlockDescriptor: ...
def DiamondOre() -> MinecraftBlockDescriptor: ...
def Diorite() -> MinecraftBlockDescriptor: ...
def DioriteDoubleSlab(
    **states: Unpack[DioriteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def DioriteSlab(**states: Unpack[DioriteSlabStates]) -> MinecraftBlockDescriptor: ...
def DioriteStairs(
    **states: Unpack[DioriteStairsStates],
) -> MinecraftBlockDescriptor: ...
def DioriteWall(**states: Unpack[DioriteWallStates]) -> MinecraftBlockDescriptor: ...
def Dirt() -> MinecraftBlockDescriptor: ...
def DirtWithRoots() -> MinecraftBlockDescriptor: ...
def Dispenser(**states: Unpack[DispenserStates]) -> MinecraftBlockDescriptor: ...
def DoubleCutCopperSlab(
    **states: Unpack[DoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def DragonEgg() -> MinecraftBlockDescriptor: ...
def DragonHead(**states: Unpack[DragonHeadStates]) -> MinecraftBlockDescriptor: ...
def DriedGhast(**states: Unpack[DriedGhastStates]) -> MinecraftBlockDescriptor: ...
def DriedKelpBlock() -> MinecraftBlockDescriptor: ...
def DripstoneBlock() -> MinecraftBlockDescriptor: ...
def Dropper(**states: Unpack[DropperStates]) -> MinecraftBlockDescriptor: ...
def Element0() -> MinecraftBlockDescriptor: ...
def Element1() -> MinecraftBlockDescriptor: ...
def Element10() -> MinecraftBlockDescriptor: ...
def Element100() -> MinecraftBlockDescriptor: ...
def Element101() -> MinecraftBlockDescriptor: ...
def Element102() -> MinecraftBlockDescriptor: ...
def Element103() -> MinecraftBlockDescriptor: ...
def Element104() -> MinecraftBlockDescriptor: ...
def Element105() -> MinecraftBlockDescriptor: ...
def Element106() -> MinecraftBlockDescriptor: ...
def Element107() -> MinecraftBlockDescriptor: ...
def Element108() -> MinecraftBlockDescriptor: ...
def Element109() -> MinecraftBlockDescriptor: ...
def Element11() -> MinecraftBlockDescriptor: ...
def Element110() -> MinecraftBlockDescriptor: ...
def Element111() -> MinecraftBlockDescriptor: ...
def Element112() -> MinecraftBlockDescriptor: ...
def Element113() -> MinecraftBlockDescriptor: ...
def Element114() -> MinecraftBlockDescriptor: ...
def Element115() -> MinecraftBlockDescriptor: ...
def Element116() -> MinecraftBlockDescriptor: ...
def Element117() -> MinecraftBlockDescriptor: ...
def Element118() -> MinecraftBlockDescriptor: ...
def Element12() -> MinecraftBlockDescriptor: ...
def Element13() -> MinecraftBlockDescriptor: ...
def Element14() -> MinecraftBlockDescriptor: ...
def Element15() -> MinecraftBlockDescriptor: ...
def Element16() -> MinecraftBlockDescriptor: ...
def Element17() -> MinecraftBlockDescriptor: ...
def Element18() -> MinecraftBlockDescriptor: ...
def Element19() -> MinecraftBlockDescriptor: ...
def Element2() -> MinecraftBlockDescriptor: ...
def Element20() -> MinecraftBlockDescriptor: ...
def Element21() -> MinecraftBlockDescriptor: ...
def Element22() -> MinecraftBlockDescriptor: ...
def Element23() -> MinecraftBlockDescriptor: ...
def Element24() -> MinecraftBlockDescriptor: ...
def Element25() -> MinecraftBlockDescriptor: ...
def Element26() -> MinecraftBlockDescriptor: ...
def Element27() -> MinecraftBlockDescriptor: ...
def Element28() -> MinecraftBlockDescriptor: ...
def Element29() -> MinecraftBlockDescriptor: ...
def Element3() -> MinecraftBlockDescriptor: ...
def Element30() -> MinecraftBlockDescriptor: ...
def Element31() -> MinecraftBlockDescriptor: ...
def Element32() -> MinecraftBlockDescriptor: ...
def Element33() -> MinecraftBlockDescriptor: ...
def Element34() -> MinecraftBlockDescriptor: ...
def Element35() -> MinecraftBlockDescriptor: ...
def Element36() -> MinecraftBlockDescriptor: ...
def Element37() -> MinecraftBlockDescriptor: ...
def Element38() -> MinecraftBlockDescriptor: ...
def Element39() -> MinecraftBlockDescriptor: ...
def Element4() -> MinecraftBlockDescriptor: ...
def Element40() -> MinecraftBlockDescriptor: ...
def Element41() -> MinecraftBlockDescriptor: ...
def Element42() -> MinecraftBlockDescriptor: ...
def Element43() -> MinecraftBlockDescriptor: ...
def Element44() -> MinecraftBlockDescriptor: ...
def Element45() -> MinecraftBlockDescriptor: ...
def Element46() -> MinecraftBlockDescriptor: ...
def Element47() -> MinecraftBlockDescriptor: ...
def Element48() -> MinecraftBlockDescriptor: ...
def Element49() -> MinecraftBlockDescriptor: ...
def Element5() -> MinecraftBlockDescriptor: ...
def Element50() -> MinecraftBlockDescriptor: ...
def Element51() -> MinecraftBlockDescriptor: ...
def Element52() -> MinecraftBlockDescriptor: ...
def Element53() -> MinecraftBlockDescriptor: ...
def Element54() -> MinecraftBlockDescriptor: ...
def Element55() -> MinecraftBlockDescriptor: ...
def Element56() -> MinecraftBlockDescriptor: ...
def Element57() -> MinecraftBlockDescriptor: ...
def Element58() -> MinecraftBlockDescriptor: ...
def Element59() -> MinecraftBlockDescriptor: ...
def Element6() -> MinecraftBlockDescriptor: ...
def Element60() -> MinecraftBlockDescriptor: ...
def Element61() -> MinecraftBlockDescriptor: ...
def Element62() -> MinecraftBlockDescriptor: ...
def Element63() -> MinecraftBlockDescriptor: ...
def Element64() -> MinecraftBlockDescriptor: ...
def Element65() -> MinecraftBlockDescriptor: ...
def Element66() -> MinecraftBlockDescriptor: ...
def Element67() -> MinecraftBlockDescriptor: ...
def Element68() -> MinecraftBlockDescriptor: ...
def Element69() -> MinecraftBlockDescriptor: ...
def Element7() -> MinecraftBlockDescriptor: ...
def Element70() -> MinecraftBlockDescriptor: ...
def Element71() -> MinecraftBlockDescriptor: ...
def Element72() -> MinecraftBlockDescriptor: ...
def Element73() -> MinecraftBlockDescriptor: ...
def Element74() -> MinecraftBlockDescriptor: ...
def Element75() -> MinecraftBlockDescriptor: ...
def Element76() -> MinecraftBlockDescriptor: ...
def Element77() -> MinecraftBlockDescriptor: ...
def Element78() -> MinecraftBlockDescriptor: ...
def Element79() -> MinecraftBlockDescriptor: ...
def Element8() -> MinecraftBlockDescriptor: ...
def Element80() -> MinecraftBlockDescriptor: ...
def Element81() -> MinecraftBlockDescriptor: ...
def Element82() -> MinecraftBlockDescriptor: ...
def Element83() -> MinecraftBlockDescriptor: ...
def Element84() -> MinecraftBlockDescriptor: ...
def Element85() -> MinecraftBlockDescriptor: ...
def Element86() -> MinecraftBlockDescriptor: ...
def Element87() -> MinecraftBlockDescriptor: ...
def Element88() -> MinecraftBlockDescriptor: ...
def Element89() -> MinecraftBlockDescriptor: ...
def Element9() -> MinecraftBlockDescriptor: ...
def Element90() -> MinecraftBlockDescriptor: ...
def Element91() -> MinecraftBlockDescriptor: ...
def Element92() -> MinecraftBlockDescriptor: ...
def Element93() -> MinecraftBlockDescriptor: ...
def Element94() -> MinecraftBlockDescriptor: ...
def Element95() -> MinecraftBlockDescriptor: ...
def Element96() -> MinecraftBlockDescriptor: ...
def Element97() -> MinecraftBlockDescriptor: ...
def Element98() -> MinecraftBlockDescriptor: ...
def Element99() -> MinecraftBlockDescriptor: ...
def ElementConstructor(
    **states: Unpack[ElementConstructorStates],
) -> MinecraftBlockDescriptor: ...
def EmeraldBlock() -> MinecraftBlockDescriptor: ...
def EmeraldOre() -> MinecraftBlockDescriptor: ...
def EnchantingTable() -> MinecraftBlockDescriptor: ...
def EndBrickStairs(
    **states: Unpack[EndBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def EndBricks() -> MinecraftBlockDescriptor: ...
def EndPortal() -> MinecraftBlockDescriptor: ...
def EndPortalFrame(
    **states: Unpack[EndPortalFrameStates],
) -> MinecraftBlockDescriptor: ...
def EndRod(**states: Unpack[EndRodStates]) -> MinecraftBlockDescriptor: ...
def EndStone() -> MinecraftBlockDescriptor: ...
def EndStoneBrickDoubleSlab(
    **states: Unpack[EndStoneBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def EndStoneBrickSlab(
    **states: Unpack[EndStoneBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def EndStoneBrickWall(
    **states: Unpack[EndStoneBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def EnderChest(**states: Unpack[EnderChestStates]) -> MinecraftBlockDescriptor: ...
def ExposedChiseledCopper() -> MinecraftBlockDescriptor: ...
def ExposedCopper() -> MinecraftBlockDescriptor: ...
def ExposedCopperBars(
    **states: Unpack[ExposedCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperBulb(
    **states: Unpack[ExposedCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperChain(
    **states: Unpack[ExposedCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperChest(
    **states: Unpack[ExposedCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperDoor(
    **states: Unpack[ExposedCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperGolemStatue(
    **states: Unpack[ExposedCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperGrate() -> MinecraftBlockDescriptor: ...
def ExposedCopperLantern(
    **states: Unpack[ExposedCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCopperTrapdoor(
    **states: Unpack[ExposedCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCutCopper() -> MinecraftBlockDescriptor: ...
def ExposedCutCopperSlab(
    **states: Unpack[ExposedCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def ExposedCutCopperStairs(
    **states: Unpack[ExposedCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def ExposedDoubleCutCopperSlab(
    **states: Unpack[ExposedDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def ExposedLightningRod(
    **states: Unpack[ExposedLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def Farmland(**states: Unpack[FarmlandStates]) -> MinecraftBlockDescriptor: ...
def FenceGate(**states: Unpack[FenceGateStates]) -> MinecraftBlockDescriptor: ...
def Fern() -> MinecraftBlockDescriptor: ...
def Fire(**states: Unpack[FireStates]) -> MinecraftBlockDescriptor: ...
def FireCoral() -> MinecraftBlockDescriptor: ...
def FireCoralBlock() -> MinecraftBlockDescriptor: ...
def FireCoralFan(**states: Unpack[FireCoralFanStates]) -> MinecraftBlockDescriptor: ...
def FireCoralWallFan(
    **states: Unpack[FireCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def FireflyBush() -> MinecraftBlockDescriptor: ...
def FletchingTable() -> MinecraftBlockDescriptor: ...
def FlowerPot(**states: Unpack[FlowerPotStates]) -> MinecraftBlockDescriptor: ...
def FloweringAzalea() -> MinecraftBlockDescriptor: ...
def FlowingLava(**states: Unpack[FlowingLavaStates]) -> MinecraftBlockDescriptor: ...
def FlowingWater(**states: Unpack[FlowingWaterStates]) -> MinecraftBlockDescriptor: ...
def Frame(**states: Unpack[FrameStates]) -> MinecraftBlockDescriptor: ...
def FrogSpawn() -> MinecraftBlockDescriptor: ...
def FrostedIce(**states: Unpack[FrostedIceStates]) -> MinecraftBlockDescriptor: ...
def Furnace(**states: Unpack[FurnaceStates]) -> MinecraftBlockDescriptor: ...
def GildedBlackstone() -> MinecraftBlockDescriptor: ...
def Glass() -> MinecraftBlockDescriptor: ...
def GlassPane(**states: Unpack[GlassPaneStates]) -> MinecraftBlockDescriptor: ...
def GlowFrame(**states: Unpack[GlowFrameStates]) -> MinecraftBlockDescriptor: ...
def GlowLichen(**states: Unpack[GlowLichenStates]) -> MinecraftBlockDescriptor: ...
def Glowstone() -> MinecraftBlockDescriptor: ...
def GoldBlock() -> MinecraftBlockDescriptor: ...
def GoldOre() -> MinecraftBlockDescriptor: ...
def GoldenDandelion() -> MinecraftBlockDescriptor: ...
def GoldenRail(**states: Unpack[GoldenRailStates]) -> MinecraftBlockDescriptor: ...
def Granite() -> MinecraftBlockDescriptor: ...
def GraniteDoubleSlab(
    **states: Unpack[GraniteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def GraniteSlab(**states: Unpack[GraniteSlabStates]) -> MinecraftBlockDescriptor: ...
def GraniteStairs(
    **states: Unpack[GraniteStairsStates],
) -> MinecraftBlockDescriptor: ...
def GraniteWall(**states: Unpack[GraniteWallStates]) -> MinecraftBlockDescriptor: ...
def GrassBlock() -> MinecraftBlockDescriptor: ...
def GrassPath() -> MinecraftBlockDescriptor: ...
def Gravel() -> MinecraftBlockDescriptor: ...
def GrayCandle(**states: Unpack[GrayCandleStates]) -> MinecraftBlockDescriptor: ...
def GrayCandleCake(
    **states: Unpack[GrayCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def GrayCarpet() -> MinecraftBlockDescriptor: ...
def GrayConcrete() -> MinecraftBlockDescriptor: ...
def GrayConcreteDoubleSlab(
    **states: Unpack[GrayConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def GrayConcretePowder() -> MinecraftBlockDescriptor: ...
def GrayConcreteSlab(
    **states: Unpack[GrayConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def GrayConcreteStairs(
    **states: Unpack[GrayConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def GrayGlazedTerracotta(
    **states: Unpack[GrayGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def GrayShulkerBox() -> MinecraftBlockDescriptor: ...
def GrayStainedGlass() -> MinecraftBlockDescriptor: ...
def GrayStainedGlassPane(
    **states: Unpack[GrayStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def GrayTerracotta() -> MinecraftBlockDescriptor: ...
def GrayWool() -> MinecraftBlockDescriptor: ...
def GrayWoolDoubleSlab(
    **states: Unpack[GrayWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def GrayWoolSlab(**states: Unpack[GrayWoolSlabStates]) -> MinecraftBlockDescriptor: ...
def GrayWoolStairs(
    **states: Unpack[GrayWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def GreenCandle(**states: Unpack[GreenCandleStates]) -> MinecraftBlockDescriptor: ...
def GreenCandleCake(
    **states: Unpack[GreenCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def GreenCarpet() -> MinecraftBlockDescriptor: ...
def GreenConcrete() -> MinecraftBlockDescriptor: ...
def GreenConcreteDoubleSlab(
    **states: Unpack[GreenConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def GreenConcretePowder() -> MinecraftBlockDescriptor: ...
def GreenConcreteSlab(
    **states: Unpack[GreenConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def GreenConcreteStairs(
    **states: Unpack[GreenConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def GreenGlazedTerracotta(
    **states: Unpack[GreenGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def GreenShulkerBox() -> MinecraftBlockDescriptor: ...
def GreenStainedGlass() -> MinecraftBlockDescriptor: ...
def GreenStainedGlassPane(
    **states: Unpack[GreenStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def GreenTerracotta() -> MinecraftBlockDescriptor: ...
def GreenWool() -> MinecraftBlockDescriptor: ...
def GreenWoolDoubleSlab(
    **states: Unpack[GreenWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def GreenWoolSlab(
    **states: Unpack[GreenWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def GreenWoolStairs(
    **states: Unpack[GreenWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def Grindstone(**states: Unpack[GrindstoneStates]) -> MinecraftBlockDescriptor: ...
def HangingRoots() -> MinecraftBlockDescriptor: ...
def HardBlackStainedGlass() -> MinecraftBlockDescriptor: ...
def HardBlackStainedGlassPane(
    **states: Unpack[HardBlackStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardBlueStainedGlass() -> MinecraftBlockDescriptor: ...
def HardBlueStainedGlassPane(
    **states: Unpack[HardBlueStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardBrownStainedGlass() -> MinecraftBlockDescriptor: ...
def HardBrownStainedGlassPane(
    **states: Unpack[HardBrownStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardCyanStainedGlass() -> MinecraftBlockDescriptor: ...
def HardCyanStainedGlassPane(
    **states: Unpack[HardCyanStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardGlass() -> MinecraftBlockDescriptor: ...
def HardGlassPane(
    **states: Unpack[HardGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardGrayStainedGlass() -> MinecraftBlockDescriptor: ...
def HardGrayStainedGlassPane(
    **states: Unpack[HardGrayStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardGreenStainedGlass() -> MinecraftBlockDescriptor: ...
def HardGreenStainedGlassPane(
    **states: Unpack[HardGreenStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardLightBlueStainedGlass() -> MinecraftBlockDescriptor: ...
def HardLightBlueStainedGlassPane(
    **states: Unpack[HardLightBlueStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardLightGrayStainedGlass() -> MinecraftBlockDescriptor: ...
def HardLightGrayStainedGlassPane(
    **states: Unpack[HardLightGrayStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardLimeStainedGlass() -> MinecraftBlockDescriptor: ...
def HardLimeStainedGlassPane(
    **states: Unpack[HardLimeStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardMagentaStainedGlass() -> MinecraftBlockDescriptor: ...
def HardMagentaStainedGlassPane(
    **states: Unpack[HardMagentaStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardOrangeStainedGlass() -> MinecraftBlockDescriptor: ...
def HardOrangeStainedGlassPane(
    **states: Unpack[HardOrangeStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardPinkStainedGlass() -> MinecraftBlockDescriptor: ...
def HardPinkStainedGlassPane(
    **states: Unpack[HardPinkStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardPurpleStainedGlass() -> MinecraftBlockDescriptor: ...
def HardPurpleStainedGlassPane(
    **states: Unpack[HardPurpleStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardRedStainedGlass() -> MinecraftBlockDescriptor: ...
def HardRedStainedGlassPane(
    **states: Unpack[HardRedStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardWhiteStainedGlass() -> MinecraftBlockDescriptor: ...
def HardWhiteStainedGlassPane(
    **states: Unpack[HardWhiteStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardYellowStainedGlass() -> MinecraftBlockDescriptor: ...
def HardYellowStainedGlassPane(
    **states: Unpack[HardYellowStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def HardenedClay() -> MinecraftBlockDescriptor: ...
def HayBlock(**states: Unpack[HayBlockStates]) -> MinecraftBlockDescriptor: ...
def HeavyCore() -> MinecraftBlockDescriptor: ...
def HeavyWeightedPressurePlate(
    **states: Unpack[HeavyWeightedPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def HoneyBlock() -> MinecraftBlockDescriptor: ...
def HoneycombBlock() -> MinecraftBlockDescriptor: ...
def Hopper(**states: Unpack[HopperStates]) -> MinecraftBlockDescriptor: ...
def HornCoral() -> MinecraftBlockDescriptor: ...
def HornCoralBlock() -> MinecraftBlockDescriptor: ...
def HornCoralFan(**states: Unpack[HornCoralFanStates]) -> MinecraftBlockDescriptor: ...
def HornCoralWallFan(
    **states: Unpack[HornCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def Ice() -> MinecraftBlockDescriptor: ...
def InfestedChiseledStoneBricks() -> MinecraftBlockDescriptor: ...
def InfestedCobblestone() -> MinecraftBlockDescriptor: ...
def InfestedCrackedStoneBricks() -> MinecraftBlockDescriptor: ...
def InfestedDeepslate(
    **states: Unpack[InfestedDeepslateStates],
) -> MinecraftBlockDescriptor: ...
def InfestedMossyStoneBricks() -> MinecraftBlockDescriptor: ...
def InfestedStone() -> MinecraftBlockDescriptor: ...
def InfestedStoneBricks() -> MinecraftBlockDescriptor: ...
def IronBars(**states: Unpack[IronBarsStates]) -> MinecraftBlockDescriptor: ...
def IronBlock() -> MinecraftBlockDescriptor: ...
def IronChain(**states: Unpack[IronChainStates]) -> MinecraftBlockDescriptor: ...
def IronDoor(**states: Unpack[IronDoorStates]) -> MinecraftBlockDescriptor: ...
def IronOre() -> MinecraftBlockDescriptor: ...
def IronTrapdoor(**states: Unpack[IronTrapdoorStates]) -> MinecraftBlockDescriptor: ...
def Jigsaw(**states: Unpack[JigsawStates]) -> MinecraftBlockDescriptor: ...
def Jukebox() -> MinecraftBlockDescriptor: ...
def JungleButton(**states: Unpack[JungleButtonStates]) -> MinecraftBlockDescriptor: ...
def JungleDoor(**states: Unpack[JungleDoorStates]) -> MinecraftBlockDescriptor: ...
def JungleDoubleSlab(
    **states: Unpack[JungleDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def JungleFence(**states: Unpack[JungleFenceStates]) -> MinecraftBlockDescriptor: ...
def JungleFenceGate(
    **states: Unpack[JungleFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def JungleHangingSign(
    **states: Unpack[JungleHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def JungleLeaves(**states: Unpack[JungleLeavesStates]) -> MinecraftBlockDescriptor: ...
def JungleLog(**states: Unpack[JungleLogStates]) -> MinecraftBlockDescriptor: ...
def JunglePlanks() -> MinecraftBlockDescriptor: ...
def JunglePressurePlate(
    **states: Unpack[JunglePressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def JungleSapling(
    **states: Unpack[JungleSaplingStates],
) -> MinecraftBlockDescriptor: ...
def JungleShelf(**states: Unpack[JungleShelfStates]) -> MinecraftBlockDescriptor: ...
def JungleSlab(**states: Unpack[JungleSlabStates]) -> MinecraftBlockDescriptor: ...
def JungleStairs(**states: Unpack[JungleStairsStates]) -> MinecraftBlockDescriptor: ...
def JungleStandingSign(
    **states: Unpack[JungleStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def JungleTrapdoor(
    **states: Unpack[JungleTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def JungleWallSign(
    **states: Unpack[JungleWallSignStates],
) -> MinecraftBlockDescriptor: ...
def JungleWood(**states: Unpack[JungleWoodStates]) -> MinecraftBlockDescriptor: ...
def Kelp(**states: Unpack[KelpStates]) -> MinecraftBlockDescriptor: ...
def LabTable(**states: Unpack[LabTableStates]) -> MinecraftBlockDescriptor: ...
def Ladder(**states: Unpack[LadderStates]) -> MinecraftBlockDescriptor: ...
def Lantern(**states: Unpack[LanternStates]) -> MinecraftBlockDescriptor: ...
def LapisBlock() -> MinecraftBlockDescriptor: ...
def LapisOre() -> MinecraftBlockDescriptor: ...
def LargeAmethystBud(
    **states: Unpack[LargeAmethystBudStates],
) -> MinecraftBlockDescriptor: ...
def LargeFern(**states: Unpack[LargeFernStates]) -> MinecraftBlockDescriptor: ...
def Lava(**states: Unpack[LavaStates]) -> MinecraftBlockDescriptor: ...
def LeafLitter(**states: Unpack[LeafLitterStates]) -> MinecraftBlockDescriptor: ...
def Lectern(**states: Unpack[LecternStates]) -> MinecraftBlockDescriptor: ...
def Lever(**states: Unpack[LeverStates]) -> MinecraftBlockDescriptor: ...
def LightBlock0() -> MinecraftBlockDescriptor: ...
def LightBlock1() -> MinecraftBlockDescriptor: ...
def LightBlock10() -> MinecraftBlockDescriptor: ...
def LightBlock11() -> MinecraftBlockDescriptor: ...
def LightBlock12() -> MinecraftBlockDescriptor: ...
def LightBlock13() -> MinecraftBlockDescriptor: ...
def LightBlock14() -> MinecraftBlockDescriptor: ...
def LightBlock15() -> MinecraftBlockDescriptor: ...
def LightBlock2() -> MinecraftBlockDescriptor: ...
def LightBlock3() -> MinecraftBlockDescriptor: ...
def LightBlock4() -> MinecraftBlockDescriptor: ...
def LightBlock5() -> MinecraftBlockDescriptor: ...
def LightBlock6() -> MinecraftBlockDescriptor: ...
def LightBlock7() -> MinecraftBlockDescriptor: ...
def LightBlock8() -> MinecraftBlockDescriptor: ...
def LightBlock9() -> MinecraftBlockDescriptor: ...
def LightBlueCandle(
    **states: Unpack[LightBlueCandleStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueCandleCake(
    **states: Unpack[LightBlueCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueCarpet() -> MinecraftBlockDescriptor: ...
def LightBlueConcrete() -> MinecraftBlockDescriptor: ...
def LightBlueConcreteDoubleSlab(
    **states: Unpack[LightBlueConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueConcretePowder() -> MinecraftBlockDescriptor: ...
def LightBlueConcreteSlab(
    **states: Unpack[LightBlueConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueConcreteStairs(
    **states: Unpack[LightBlueConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueGlazedTerracotta(
    **states: Unpack[LightBlueGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueShulkerBox() -> MinecraftBlockDescriptor: ...
def LightBlueStainedGlass() -> MinecraftBlockDescriptor: ...
def LightBlueStainedGlassPane(
    **states: Unpack[LightBlueStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueTerracotta() -> MinecraftBlockDescriptor: ...
def LightBlueWool() -> MinecraftBlockDescriptor: ...
def LightBlueWoolDoubleSlab(
    **states: Unpack[LightBlueWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueWoolSlab(
    **states: Unpack[LightBlueWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightBlueWoolStairs(
    **states: Unpack[LightBlueWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayCandle(
    **states: Unpack[LightGrayCandleStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayCandleCake(
    **states: Unpack[LightGrayCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayCarpet() -> MinecraftBlockDescriptor: ...
def LightGrayConcrete() -> MinecraftBlockDescriptor: ...
def LightGrayConcreteDoubleSlab(
    **states: Unpack[LightGrayConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayConcretePowder() -> MinecraftBlockDescriptor: ...
def LightGrayConcreteSlab(
    **states: Unpack[LightGrayConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayConcreteStairs(
    **states: Unpack[LightGrayConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayShulkerBox() -> MinecraftBlockDescriptor: ...
def LightGrayStainedGlass() -> MinecraftBlockDescriptor: ...
def LightGrayStainedGlassPane(
    **states: Unpack[LightGrayStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayTerracotta() -> MinecraftBlockDescriptor: ...
def LightGrayWool() -> MinecraftBlockDescriptor: ...
def LightGrayWoolDoubleSlab(
    **states: Unpack[LightGrayWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayWoolSlab(
    **states: Unpack[LightGrayWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def LightGrayWoolStairs(
    **states: Unpack[LightGrayWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def LightWeightedPressurePlate(
    **states: Unpack[LightWeightedPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def LightningRod(**states: Unpack[LightningRodStates]) -> MinecraftBlockDescriptor: ...
def Lilac(**states: Unpack[LilacStates]) -> MinecraftBlockDescriptor: ...
def LilyOfTheValley() -> MinecraftBlockDescriptor: ...
def LimeCandle(**states: Unpack[LimeCandleStates]) -> MinecraftBlockDescriptor: ...
def LimeCandleCake(
    **states: Unpack[LimeCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def LimeCarpet() -> MinecraftBlockDescriptor: ...
def LimeConcrete() -> MinecraftBlockDescriptor: ...
def LimeConcreteDoubleSlab(
    **states: Unpack[LimeConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def LimeConcretePowder() -> MinecraftBlockDescriptor: ...
def LimeConcreteSlab(
    **states: Unpack[LimeConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def LimeConcreteStairs(
    **states: Unpack[LimeConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def LimeGlazedTerracotta(
    **states: Unpack[LimeGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def LimeShulkerBox() -> MinecraftBlockDescriptor: ...
def LimeStainedGlass() -> MinecraftBlockDescriptor: ...
def LimeStainedGlassPane(
    **states: Unpack[LimeStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def LimeTerracotta() -> MinecraftBlockDescriptor: ...
def LimeWool() -> MinecraftBlockDescriptor: ...
def LimeWoolDoubleSlab(
    **states: Unpack[LimeWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def LimeWoolSlab(**states: Unpack[LimeWoolSlabStates]) -> MinecraftBlockDescriptor: ...
def LimeWoolStairs(
    **states: Unpack[LimeWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def LitBlastFurnace(
    **states: Unpack[LitBlastFurnaceStates],
) -> MinecraftBlockDescriptor: ...
def LitDeepslateRedstoneOre() -> MinecraftBlockDescriptor: ...
def LitFurnace(**states: Unpack[LitFurnaceStates]) -> MinecraftBlockDescriptor: ...
def LitPumpkin(**states: Unpack[LitPumpkinStates]) -> MinecraftBlockDescriptor: ...
def LitRedstoneLamp() -> MinecraftBlockDescriptor: ...
def LitRedstoneOre() -> MinecraftBlockDescriptor: ...
def LitSmoker(**states: Unpack[LitSmokerStates]) -> MinecraftBlockDescriptor: ...
def Lodestone() -> MinecraftBlockDescriptor: ...
def Loom(**states: Unpack[LoomStates]) -> MinecraftBlockDescriptor: ...
def MagentaCandle(
    **states: Unpack[MagentaCandleStates],
) -> MinecraftBlockDescriptor: ...
def MagentaCandleCake(
    **states: Unpack[MagentaCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def MagentaCarpet() -> MinecraftBlockDescriptor: ...
def MagentaConcrete() -> MinecraftBlockDescriptor: ...
def MagentaConcreteDoubleSlab(
    **states: Unpack[MagentaConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def MagentaConcretePowder() -> MinecraftBlockDescriptor: ...
def MagentaConcreteSlab(
    **states: Unpack[MagentaConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def MagentaConcreteStairs(
    **states: Unpack[MagentaConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def MagentaGlazedTerracotta(
    **states: Unpack[MagentaGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def MagentaShulkerBox() -> MinecraftBlockDescriptor: ...
def MagentaStainedGlass() -> MinecraftBlockDescriptor: ...
def MagentaStainedGlassPane(
    **states: Unpack[MagentaStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def MagentaTerracotta() -> MinecraftBlockDescriptor: ...
def MagentaWool() -> MinecraftBlockDescriptor: ...
def MagentaWoolDoubleSlab(
    **states: Unpack[MagentaWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def MagentaWoolSlab(
    **states: Unpack[MagentaWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def MagentaWoolStairs(
    **states: Unpack[MagentaWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def Magma() -> MinecraftBlockDescriptor: ...
def MangroveButton(
    **states: Unpack[MangroveButtonStates],
) -> MinecraftBlockDescriptor: ...
def MangroveDoor(**states: Unpack[MangroveDoorStates]) -> MinecraftBlockDescriptor: ...
def MangroveDoubleSlab(
    **states: Unpack[MangroveDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def MangroveFence(
    **states: Unpack[MangroveFenceStates],
) -> MinecraftBlockDescriptor: ...
def MangroveFenceGate(
    **states: Unpack[MangroveFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def MangroveHangingSign(
    **states: Unpack[MangroveHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def MangroveLeaves(
    **states: Unpack[MangroveLeavesStates],
) -> MinecraftBlockDescriptor: ...
def MangroveLog(**states: Unpack[MangroveLogStates]) -> MinecraftBlockDescriptor: ...
def MangrovePlanks() -> MinecraftBlockDescriptor: ...
def MangrovePressurePlate(
    **states: Unpack[MangrovePressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def MangrovePropagule(
    **states: Unpack[MangrovePropaguleStates],
) -> MinecraftBlockDescriptor: ...
def MangroveRoots() -> MinecraftBlockDescriptor: ...
def MangroveShelf(
    **states: Unpack[MangroveShelfStates],
) -> MinecraftBlockDescriptor: ...
def MangroveSlab(**states: Unpack[MangroveSlabStates]) -> MinecraftBlockDescriptor: ...
def MangroveStairs(
    **states: Unpack[MangroveStairsStates],
) -> MinecraftBlockDescriptor: ...
def MangroveStandingSign(
    **states: Unpack[MangroveStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def MangroveTrapdoor(
    **states: Unpack[MangroveTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def MangroveWallSign(
    **states: Unpack[MangroveWallSignStates],
) -> MinecraftBlockDescriptor: ...
def MangroveWood(**states: Unpack[MangroveWoodStates]) -> MinecraftBlockDescriptor: ...
def MaterialReducer(
    **states: Unpack[MaterialReducerStates],
) -> MinecraftBlockDescriptor: ...
def MediumAmethystBud(
    **states: Unpack[MediumAmethystBudStates],
) -> MinecraftBlockDescriptor: ...
def MelonBlock() -> MinecraftBlockDescriptor: ...
def MelonStem(**states: Unpack[MelonStemStates]) -> MinecraftBlockDescriptor: ...
def MobSpawner() -> MinecraftBlockDescriptor: ...
def MossBlock() -> MinecraftBlockDescriptor: ...
def MossCarpet() -> MinecraftBlockDescriptor: ...
def MossyCobblestone() -> MinecraftBlockDescriptor: ...
def MossyCobblestoneDoubleSlab(
    **states: Unpack[MossyCobblestoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def MossyCobblestoneSlab(
    **states: Unpack[MossyCobblestoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def MossyCobblestoneStairs(
    **states: Unpack[MossyCobblestoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def MossyCobblestoneWall(
    **states: Unpack[MossyCobblestoneWallStates],
) -> MinecraftBlockDescriptor: ...
def MossyStoneBrickDoubleSlab(
    **states: Unpack[MossyStoneBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def MossyStoneBrickSlab(
    **states: Unpack[MossyStoneBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def MossyStoneBrickStairs(
    **states: Unpack[MossyStoneBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def MossyStoneBrickWall(
    **states: Unpack[MossyStoneBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def MossyStoneBricks() -> MinecraftBlockDescriptor: ...
def Mud() -> MinecraftBlockDescriptor: ...
def MudBrickDoubleSlab(
    **states: Unpack[MudBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def MudBrickSlab(**states: Unpack[MudBrickSlabStates]) -> MinecraftBlockDescriptor: ...
def MudBrickStairs(
    **states: Unpack[MudBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def MudBrickWall(**states: Unpack[MudBrickWallStates]) -> MinecraftBlockDescriptor: ...
def MudBricks() -> MinecraftBlockDescriptor: ...
def MuddyMangroveRoots(
    **states: Unpack[MuddyMangroveRootsStates],
) -> MinecraftBlockDescriptor: ...
def MushroomStem(**states: Unpack[MushroomStemStates]) -> MinecraftBlockDescriptor: ...
def Mycelium() -> MinecraftBlockDescriptor: ...
def NetherBrick() -> MinecraftBlockDescriptor: ...
def NetherBrickDoubleSlab(
    **states: Unpack[NetherBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def NetherBrickFence(
    **states: Unpack[NetherBrickFenceStates],
) -> MinecraftBlockDescriptor: ...
def NetherBrickSlab(
    **states: Unpack[NetherBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def NetherBrickStairs(
    **states: Unpack[NetherBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def NetherBrickWall(
    **states: Unpack[NetherBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def NetherGoldOre() -> MinecraftBlockDescriptor: ...
def NetherSprouts() -> MinecraftBlockDescriptor: ...
def NetherWart(**states: Unpack[NetherWartStates]) -> MinecraftBlockDescriptor: ...
def NetherWartBlock() -> MinecraftBlockDescriptor: ...
def NetheriteBlock() -> MinecraftBlockDescriptor: ...
def Netherrack() -> MinecraftBlockDescriptor: ...
def NormalStoneDoubleSlab(
    **states: Unpack[NormalStoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def NormalStoneSlab(
    **states: Unpack[NormalStoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def NormalStoneStairs(
    **states: Unpack[NormalStoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def Noteblock() -> MinecraftBlockDescriptor: ...
def OakDoubleSlab(
    **states: Unpack[OakDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def OakFence(**states: Unpack[OakFenceStates]) -> MinecraftBlockDescriptor: ...
def OakHangingSign(
    **states: Unpack[OakHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def OakLeaves(**states: Unpack[OakLeavesStates]) -> MinecraftBlockDescriptor: ...
def OakLog(**states: Unpack[OakLogStates]) -> MinecraftBlockDescriptor: ...
def OakPlanks() -> MinecraftBlockDescriptor: ...
def OakSapling(**states: Unpack[OakSaplingStates]) -> MinecraftBlockDescriptor: ...
def OakShelf(**states: Unpack[OakShelfStates]) -> MinecraftBlockDescriptor: ...
def OakSlab(**states: Unpack[OakSlabStates]) -> MinecraftBlockDescriptor: ...
def OakStairs(**states: Unpack[OakStairsStates]) -> MinecraftBlockDescriptor: ...
def OakWood(**states: Unpack[OakWoodStates]) -> MinecraftBlockDescriptor: ...
def Observer(**states: Unpack[ObserverStates]) -> MinecraftBlockDescriptor: ...
def Obsidian() -> MinecraftBlockDescriptor: ...
def OchreFroglight(
    **states: Unpack[OchreFroglightStates],
) -> MinecraftBlockDescriptor: ...
def OpenEyeblossom() -> MinecraftBlockDescriptor: ...
def OrangeCandle(**states: Unpack[OrangeCandleStates]) -> MinecraftBlockDescriptor: ...
def OrangeCandleCake(
    **states: Unpack[OrangeCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def OrangeCarpet() -> MinecraftBlockDescriptor: ...
def OrangeConcrete() -> MinecraftBlockDescriptor: ...
def OrangeConcreteDoubleSlab(
    **states: Unpack[OrangeConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def OrangeConcretePowder() -> MinecraftBlockDescriptor: ...
def OrangeConcreteSlab(
    **states: Unpack[OrangeConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def OrangeConcreteStairs(
    **states: Unpack[OrangeConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def OrangeGlazedTerracotta(
    **states: Unpack[OrangeGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def OrangePoplarLeaves(
    **states: Unpack[OrangePoplarLeavesStates],
) -> MinecraftBlockDescriptor: ...
def OrangeShulkerBox() -> MinecraftBlockDescriptor: ...
def OrangeStainedGlass() -> MinecraftBlockDescriptor: ...
def OrangeStainedGlassPane(
    **states: Unpack[OrangeStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def OrangeTerracotta() -> MinecraftBlockDescriptor: ...
def OrangeTulip() -> MinecraftBlockDescriptor: ...
def OrangeWool() -> MinecraftBlockDescriptor: ...
def OrangeWoolDoubleSlab(
    **states: Unpack[OrangeWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def OrangeWoolSlab(
    **states: Unpack[OrangeWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def OrangeWoolStairs(
    **states: Unpack[OrangeWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def OxeyeDaisy() -> MinecraftBlockDescriptor: ...
def OxidizedChiseledCopper() -> MinecraftBlockDescriptor: ...
def OxidizedCopper() -> MinecraftBlockDescriptor: ...
def OxidizedCopperBars(
    **states: Unpack[OxidizedCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperBulb(
    **states: Unpack[OxidizedCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperChain(
    **states: Unpack[OxidizedCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperChest(
    **states: Unpack[OxidizedCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperDoor(
    **states: Unpack[OxidizedCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperGolemStatue(
    **states: Unpack[OxidizedCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperGrate() -> MinecraftBlockDescriptor: ...
def OxidizedCopperLantern(
    **states: Unpack[OxidizedCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCopperTrapdoor(
    **states: Unpack[OxidizedCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCutCopper() -> MinecraftBlockDescriptor: ...
def OxidizedCutCopperSlab(
    **states: Unpack[OxidizedCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedCutCopperStairs(
    **states: Unpack[OxidizedCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedDoubleCutCopperSlab(
    **states: Unpack[OxidizedDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def OxidizedLightningRod(
    **states: Unpack[OxidizedLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def PackedIce() -> MinecraftBlockDescriptor: ...
def PackedMud() -> MinecraftBlockDescriptor: ...
def PaleHangingMoss(
    **states: Unpack[PaleHangingMossStates],
) -> MinecraftBlockDescriptor: ...
def PaleMossBlock() -> MinecraftBlockDescriptor: ...
def PaleMossCarpet(
    **states: Unpack[PaleMossCarpetStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakButton(
    **states: Unpack[PaleOakButtonStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakDoor(**states: Unpack[PaleOakDoorStates]) -> MinecraftBlockDescriptor: ...
def PaleOakDoubleSlab(
    **states: Unpack[PaleOakDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakFence(**states: Unpack[PaleOakFenceStates]) -> MinecraftBlockDescriptor: ...
def PaleOakFenceGate(
    **states: Unpack[PaleOakFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakHangingSign(
    **states: Unpack[PaleOakHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakLeaves(
    **states: Unpack[PaleOakLeavesStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakLog(**states: Unpack[PaleOakLogStates]) -> MinecraftBlockDescriptor: ...
def PaleOakPlanks() -> MinecraftBlockDescriptor: ...
def PaleOakPressurePlate(
    **states: Unpack[PaleOakPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakSapling(
    **states: Unpack[PaleOakSaplingStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakShelf(**states: Unpack[PaleOakShelfStates]) -> MinecraftBlockDescriptor: ...
def PaleOakSlab(**states: Unpack[PaleOakSlabStates]) -> MinecraftBlockDescriptor: ...
def PaleOakStairs(
    **states: Unpack[PaleOakStairsStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakStandingSign(
    **states: Unpack[PaleOakStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakTrapdoor(
    **states: Unpack[PaleOakTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakWallSign(
    **states: Unpack[PaleOakWallSignStates],
) -> MinecraftBlockDescriptor: ...
def PaleOakWood(**states: Unpack[PaleOakWoodStates]) -> MinecraftBlockDescriptor: ...
def PearlescentFroglight(
    **states: Unpack[PearlescentFroglightStates],
) -> MinecraftBlockDescriptor: ...
def Peony(**states: Unpack[PeonyStates]) -> MinecraftBlockDescriptor: ...
def PetrifiedOakDoubleSlab(
    **states: Unpack[PetrifiedOakDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PetrifiedOakSlab(
    **states: Unpack[PetrifiedOakSlabStates],
) -> MinecraftBlockDescriptor: ...
def PiglinHead(**states: Unpack[PiglinHeadStates]) -> MinecraftBlockDescriptor: ...
def PinkCandle(**states: Unpack[PinkCandleStates]) -> MinecraftBlockDescriptor: ...
def PinkCandleCake(
    **states: Unpack[PinkCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def PinkCarpet() -> MinecraftBlockDescriptor: ...
def PinkConcrete() -> MinecraftBlockDescriptor: ...
def PinkConcreteDoubleSlab(
    **states: Unpack[PinkConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PinkConcretePowder() -> MinecraftBlockDescriptor: ...
def PinkConcreteSlab(
    **states: Unpack[PinkConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def PinkConcreteStairs(
    **states: Unpack[PinkConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def PinkGlazedTerracotta(
    **states: Unpack[PinkGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def PinkPetals(**states: Unpack[PinkPetalsStates]) -> MinecraftBlockDescriptor: ...
def PinkShulkerBox() -> MinecraftBlockDescriptor: ...
def PinkStainedGlass() -> MinecraftBlockDescriptor: ...
def PinkStainedGlassPane(
    **states: Unpack[PinkStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def PinkTerracotta() -> MinecraftBlockDescriptor: ...
def PinkTulip() -> MinecraftBlockDescriptor: ...
def PinkWool() -> MinecraftBlockDescriptor: ...
def PinkWoolDoubleSlab(
    **states: Unpack[PinkWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PinkWoolSlab(**states: Unpack[PinkWoolSlabStates]) -> MinecraftBlockDescriptor: ...
def PinkWoolStairs(
    **states: Unpack[PinkWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def Piston(**states: Unpack[PistonStates]) -> MinecraftBlockDescriptor: ...
def PistonArmCollision(
    **states: Unpack[PistonArmCollisionStates],
) -> MinecraftBlockDescriptor: ...
def PitcherCrop(**states: Unpack[PitcherCropStates]) -> MinecraftBlockDescriptor: ...
def PitcherPlant(**states: Unpack[PitcherPlantStates]) -> MinecraftBlockDescriptor: ...
def PlayerHead(**states: Unpack[PlayerHeadStates]) -> MinecraftBlockDescriptor: ...
def Podzol() -> MinecraftBlockDescriptor: ...
def PointedDripstone(
    **states: Unpack[PointedDripstoneStates],
) -> MinecraftBlockDescriptor: ...
def PolishedAndesite() -> MinecraftBlockDescriptor: ...
def PolishedAndesiteDoubleSlab(
    **states: Unpack[PolishedAndesiteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedAndesiteSlab(
    **states: Unpack[PolishedAndesiteSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedAndesiteStairs(
    **states: Unpack[PolishedAndesiteStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBasalt(
    **states: Unpack[PolishedBasaltStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstone() -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneBrickDoubleSlab(
    **states: Unpack[PolishedBlackstoneBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneBrickSlab(
    **states: Unpack[PolishedBlackstoneBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneBrickStairs(
    **states: Unpack[PolishedBlackstoneBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneBrickWall(
    **states: Unpack[PolishedBlackstoneBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneBricks() -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneButton(
    **states: Unpack[PolishedBlackstoneButtonStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneDoubleSlab(
    **states: Unpack[PolishedBlackstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstonePressurePlate(
    **states: Unpack[PolishedBlackstonePressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneSlab(
    **states: Unpack[PolishedBlackstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneStairs(
    **states: Unpack[PolishedBlackstoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedBlackstoneWall(
    **states: Unpack[PolishedBlackstoneWallStates],
) -> MinecraftBlockDescriptor: ...
def PolishedCinnabar() -> MinecraftBlockDescriptor: ...
def PolishedCinnabarDoubleSlab(
    **states: Unpack[PolishedCinnabarDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedCinnabarSlab(
    **states: Unpack[PolishedCinnabarSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedCinnabarStairs(
    **states: Unpack[PolishedCinnabarStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedCinnabarWall(
    **states: Unpack[PolishedCinnabarWallStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDeepslate() -> MinecraftBlockDescriptor: ...
def PolishedDeepslateDoubleSlab(
    **states: Unpack[PolishedDeepslateDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDeepslateSlab(
    **states: Unpack[PolishedDeepslateSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDeepslateStairs(
    **states: Unpack[PolishedDeepslateStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDeepslateWall(
    **states: Unpack[PolishedDeepslateWallStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDiorite() -> MinecraftBlockDescriptor: ...
def PolishedDioriteDoubleSlab(
    **states: Unpack[PolishedDioriteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDioriteSlab(
    **states: Unpack[PolishedDioriteSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedDioriteStairs(
    **states: Unpack[PolishedDioriteStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedGranite() -> MinecraftBlockDescriptor: ...
def PolishedGraniteDoubleSlab(
    **states: Unpack[PolishedGraniteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedGraniteSlab(
    **states: Unpack[PolishedGraniteSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedGraniteStairs(
    **states: Unpack[PolishedGraniteStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedSulfur() -> MinecraftBlockDescriptor: ...
def PolishedSulfurDoubleSlab(
    **states: Unpack[PolishedSulfurDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedSulfurSlab(
    **states: Unpack[PolishedSulfurSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedSulfurStairs(
    **states: Unpack[PolishedSulfurStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedSulfurWall(
    **states: Unpack[PolishedSulfurWallStates],
) -> MinecraftBlockDescriptor: ...
def PolishedTuff() -> MinecraftBlockDescriptor: ...
def PolishedTuffDoubleSlab(
    **states: Unpack[PolishedTuffDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedTuffSlab(
    **states: Unpack[PolishedTuffSlabStates],
) -> MinecraftBlockDescriptor: ...
def PolishedTuffStairs(
    **states: Unpack[PolishedTuffStairsStates],
) -> MinecraftBlockDescriptor: ...
def PolishedTuffWall(
    **states: Unpack[PolishedTuffWallStates],
) -> MinecraftBlockDescriptor: ...
def PoplarButton(**states: Unpack[PoplarButtonStates]) -> MinecraftBlockDescriptor: ...
def PoplarDoor(**states: Unpack[PoplarDoorStates]) -> MinecraftBlockDescriptor: ...
def PoplarDoubleSlab(
    **states: Unpack[PoplarDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PoplarFence(**states: Unpack[PoplarFenceStates]) -> MinecraftBlockDescriptor: ...
def PoplarFenceGate(
    **states: Unpack[PoplarFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def PoplarHangingSign(
    **states: Unpack[PoplarHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def PoplarLog(**states: Unpack[PoplarLogStates]) -> MinecraftBlockDescriptor: ...
def PoplarPlanks() -> MinecraftBlockDescriptor: ...
def PoplarPressurePlate(
    **states: Unpack[PoplarPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def PoplarSapling(
    **states: Unpack[PoplarSaplingStates],
) -> MinecraftBlockDescriptor: ...
def PoplarShelf(**states: Unpack[PoplarShelfStates]) -> MinecraftBlockDescriptor: ...
def PoplarSlab(**states: Unpack[PoplarSlabStates]) -> MinecraftBlockDescriptor: ...
def PoplarStairs(**states: Unpack[PoplarStairsStates]) -> MinecraftBlockDescriptor: ...
def PoplarStandingSign(
    **states: Unpack[PoplarStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def PoplarTrapdoor(
    **states: Unpack[PoplarTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def PoplarWallSign(
    **states: Unpack[PoplarWallSignStates],
) -> MinecraftBlockDescriptor: ...
def PoplarWood(**states: Unpack[PoplarWoodStates]) -> MinecraftBlockDescriptor: ...
def Poppy() -> MinecraftBlockDescriptor: ...
def Portal(**states: Unpack[PortalStates]) -> MinecraftBlockDescriptor: ...
def Potatoes(**states: Unpack[PotatoesStates]) -> MinecraftBlockDescriptor: ...
def PotentSulfur(**states: Unpack[PotentSulfurStates]) -> MinecraftBlockDescriptor: ...
def PowderSnow() -> MinecraftBlockDescriptor: ...
def PoweredComparator(
    **states: Unpack[PoweredComparatorStates],
) -> MinecraftBlockDescriptor: ...
def PoweredRepeater(
    **states: Unpack[PoweredRepeaterStates],
) -> MinecraftBlockDescriptor: ...
def Prismarine() -> MinecraftBlockDescriptor: ...
def PrismarineBrickDoubleSlab(
    **states: Unpack[PrismarineBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PrismarineBrickSlab(
    **states: Unpack[PrismarineBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def PrismarineBricks() -> MinecraftBlockDescriptor: ...
def PrismarineBricksStairs(
    **states: Unpack[PrismarineBricksStairsStates],
) -> MinecraftBlockDescriptor: ...
def PrismarineDoubleSlab(
    **states: Unpack[PrismarineDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PrismarineSlab(
    **states: Unpack[PrismarineSlabStates],
) -> MinecraftBlockDescriptor: ...
def PrismarineStairs(
    **states: Unpack[PrismarineStairsStates],
) -> MinecraftBlockDescriptor: ...
def PrismarineWall(
    **states: Unpack[PrismarineWallStates],
) -> MinecraftBlockDescriptor: ...
def Pumpkin(**states: Unpack[PumpkinStates]) -> MinecraftBlockDescriptor: ...
def PumpkinStem(**states: Unpack[PumpkinStemStates]) -> MinecraftBlockDescriptor: ...
def PurpleCandle(**states: Unpack[PurpleCandleStates]) -> MinecraftBlockDescriptor: ...
def PurpleCandleCake(
    **states: Unpack[PurpleCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def PurpleCarpet() -> MinecraftBlockDescriptor: ...
def PurpleConcrete() -> MinecraftBlockDescriptor: ...
def PurpleConcreteDoubleSlab(
    **states: Unpack[PurpleConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PurpleConcretePowder() -> MinecraftBlockDescriptor: ...
def PurpleConcreteSlab(
    **states: Unpack[PurpleConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def PurpleConcreteStairs(
    **states: Unpack[PurpleConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def PurpleGlazedTerracotta(
    **states: Unpack[PurpleGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def PurpleShulkerBox() -> MinecraftBlockDescriptor: ...
def PurpleStainedGlass() -> MinecraftBlockDescriptor: ...
def PurpleStainedGlassPane(
    **states: Unpack[PurpleStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def PurpleTerracotta() -> MinecraftBlockDescriptor: ...
def PurpleWool() -> MinecraftBlockDescriptor: ...
def PurpleWoolDoubleSlab(
    **states: Unpack[PurpleWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PurpleWoolSlab(
    **states: Unpack[PurpleWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def PurpleWoolStairs(
    **states: Unpack[PurpleWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def PurpurBlock(**states: Unpack[PurpurBlockStates]) -> MinecraftBlockDescriptor: ...
def PurpurDoubleSlab(
    **states: Unpack[PurpurDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def PurpurPillar(**states: Unpack[PurpurPillarStates]) -> MinecraftBlockDescriptor: ...
def PurpurSlab(**states: Unpack[PurpurSlabStates]) -> MinecraftBlockDescriptor: ...
def PurpurStairs(**states: Unpack[PurpurStairsStates]) -> MinecraftBlockDescriptor: ...
def QuartzBlock(**states: Unpack[QuartzBlockStates]) -> MinecraftBlockDescriptor: ...
def QuartzBricks() -> MinecraftBlockDescriptor: ...
def QuartzDoubleSlab(
    **states: Unpack[QuartzDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def QuartzOre() -> MinecraftBlockDescriptor: ...
def QuartzPillar(**states: Unpack[QuartzPillarStates]) -> MinecraftBlockDescriptor: ...
def QuartzSlab(**states: Unpack[QuartzSlabStates]) -> MinecraftBlockDescriptor: ...
def QuartzStairs(**states: Unpack[QuartzStairsStates]) -> MinecraftBlockDescriptor: ...
def Rail(**states: Unpack[RailStates]) -> MinecraftBlockDescriptor: ...
def RawCopperBlock() -> MinecraftBlockDescriptor: ...
def RawGoldBlock() -> MinecraftBlockDescriptor: ...
def RawIronBlock() -> MinecraftBlockDescriptor: ...
def RedCandle(**states: Unpack[RedCandleStates]) -> MinecraftBlockDescriptor: ...
def RedCandleCake(
    **states: Unpack[RedCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def RedCarpet() -> MinecraftBlockDescriptor: ...
def RedConcrete() -> MinecraftBlockDescriptor: ...
def RedConcreteDoubleSlab(
    **states: Unpack[RedConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedConcretePowder() -> MinecraftBlockDescriptor: ...
def RedConcreteSlab(
    **states: Unpack[RedConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedConcreteStairs(
    **states: Unpack[RedConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def RedGlazedTerracotta(
    **states: Unpack[RedGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def RedMushroom() -> MinecraftBlockDescriptor: ...
def RedMushroomBlock(
    **states: Unpack[RedMushroomBlockStates],
) -> MinecraftBlockDescriptor: ...
def RedNetherBrick() -> MinecraftBlockDescriptor: ...
def RedNetherBrickDoubleSlab(
    **states: Unpack[RedNetherBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedNetherBrickSlab(
    **states: Unpack[RedNetherBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedNetherBrickStairs(
    **states: Unpack[RedNetherBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def RedNetherBrickWall(
    **states: Unpack[RedNetherBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def RedPoplarLeaves(
    **states: Unpack[RedPoplarLeavesStates],
) -> MinecraftBlockDescriptor: ...
def RedSand() -> MinecraftBlockDescriptor: ...
def RedSandstone() -> MinecraftBlockDescriptor: ...
def RedSandstoneDoubleSlab(
    **states: Unpack[RedSandstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedSandstoneSlab(
    **states: Unpack[RedSandstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedSandstoneStairs(
    **states: Unpack[RedSandstoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def RedSandstoneWall(
    **states: Unpack[RedSandstoneWallStates],
) -> MinecraftBlockDescriptor: ...
def RedShrub() -> MinecraftBlockDescriptor: ...
def RedShulkerBox() -> MinecraftBlockDescriptor: ...
def RedStainedGlass() -> MinecraftBlockDescriptor: ...
def RedStainedGlassPane(
    **states: Unpack[RedStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def RedTerracotta() -> MinecraftBlockDescriptor: ...
def RedTulip() -> MinecraftBlockDescriptor: ...
def RedWool() -> MinecraftBlockDescriptor: ...
def RedWoolDoubleSlab(
    **states: Unpack[RedWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def RedWoolSlab(**states: Unpack[RedWoolSlabStates]) -> MinecraftBlockDescriptor: ...
def RedWoolStairs(
    **states: Unpack[RedWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def RedstoneBlock() -> MinecraftBlockDescriptor: ...
def RedstoneLamp() -> MinecraftBlockDescriptor: ...
def RedstoneOre() -> MinecraftBlockDescriptor: ...
def RedstoneTorch(
    **states: Unpack[RedstoneTorchStates],
) -> MinecraftBlockDescriptor: ...
def RedstoneWire(**states: Unpack[RedstoneWireStates]) -> MinecraftBlockDescriptor: ...
def Reeds(**states: Unpack[ReedsStates]) -> MinecraftBlockDescriptor: ...
def ReinforcedDeepslate() -> MinecraftBlockDescriptor: ...
def RepeatingCommandBlock(
    **states: Unpack[RepeatingCommandBlockStates],
) -> MinecraftBlockDescriptor: ...
def ResinBlock() -> MinecraftBlockDescriptor: ...
def ResinBrickDoubleSlab(
    **states: Unpack[ResinBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def ResinBrickSlab(
    **states: Unpack[ResinBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def ResinBrickStairs(
    **states: Unpack[ResinBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def ResinBrickWall(
    **states: Unpack[ResinBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def ResinBricks() -> MinecraftBlockDescriptor: ...
def ResinClump(**states: Unpack[ResinClumpStates]) -> MinecraftBlockDescriptor: ...
def RespawnAnchor(
    **states: Unpack[RespawnAnchorStates],
) -> MinecraftBlockDescriptor: ...
def RoseBush(**states: Unpack[RoseBushStates]) -> MinecraftBlockDescriptor: ...
def Sand() -> MinecraftBlockDescriptor: ...
def Sandstone() -> MinecraftBlockDescriptor: ...
def SandstoneDoubleSlab(
    **states: Unpack[SandstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SandstoneSlab(
    **states: Unpack[SandstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def SandstoneStairs(
    **states: Unpack[SandstoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def SandstoneWall(
    **states: Unpack[SandstoneWallStates],
) -> MinecraftBlockDescriptor: ...
def Scaffolding(**states: Unpack[ScaffoldingStates]) -> MinecraftBlockDescriptor: ...
def Sculk() -> MinecraftBlockDescriptor: ...
def SculkCatalyst(
    **states: Unpack[SculkCatalystStates],
) -> MinecraftBlockDescriptor: ...
def SculkSensor(**states: Unpack[SculkSensorStates]) -> MinecraftBlockDescriptor: ...
def SculkShrieker(
    **states: Unpack[SculkShriekerStates],
) -> MinecraftBlockDescriptor: ...
def SculkVein(**states: Unpack[SculkVeinStates]) -> MinecraftBlockDescriptor: ...
def SeaLantern() -> MinecraftBlockDescriptor: ...
def SeaPickle(**states: Unpack[SeaPickleStates]) -> MinecraftBlockDescriptor: ...
def Seagrass(**states: Unpack[SeagrassStates]) -> MinecraftBlockDescriptor: ...
def ShelfMushroom(
    **states: Unpack[ShelfMushroomStates],
) -> MinecraftBlockDescriptor: ...
def ShortDryGrass() -> MinecraftBlockDescriptor: ...
def ShortGrass() -> MinecraftBlockDescriptor: ...
def Shroomlight() -> MinecraftBlockDescriptor: ...
def SilverGlazedTerracotta(
    **states: Unpack[SilverGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def SkeletonSkull(
    **states: Unpack[SkeletonSkullStates],
) -> MinecraftBlockDescriptor: ...
def Slime() -> MinecraftBlockDescriptor: ...
def SmallAmethystBud(
    **states: Unpack[SmallAmethystBudStates],
) -> MinecraftBlockDescriptor: ...
def SmallDripleafBlock(
    **states: Unpack[SmallDripleafBlockStates],
) -> MinecraftBlockDescriptor: ...
def SmithingTable() -> MinecraftBlockDescriptor: ...
def Smoker(**states: Unpack[SmokerStates]) -> MinecraftBlockDescriptor: ...
def SmoothBasalt() -> MinecraftBlockDescriptor: ...
def SmoothQuartz(**states: Unpack[SmoothQuartzStates]) -> MinecraftBlockDescriptor: ...
def SmoothQuartzDoubleSlab(
    **states: Unpack[SmoothQuartzDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothQuartzSlab(
    **states: Unpack[SmoothQuartzSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothQuartzStairs(
    **states: Unpack[SmoothQuartzStairsStates],
) -> MinecraftBlockDescriptor: ...
def SmoothRedSandstone() -> MinecraftBlockDescriptor: ...
def SmoothRedSandstoneDoubleSlab(
    **states: Unpack[SmoothRedSandstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothRedSandstoneSlab(
    **states: Unpack[SmoothRedSandstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothRedSandstoneStairs(
    **states: Unpack[SmoothRedSandstoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def SmoothSandstone() -> MinecraftBlockDescriptor: ...
def SmoothSandstoneDoubleSlab(
    **states: Unpack[SmoothSandstoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothSandstoneSlab(
    **states: Unpack[SmoothSandstoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothSandstoneStairs(
    **states: Unpack[SmoothSandstoneStairsStates],
) -> MinecraftBlockDescriptor: ...
def SmoothStone() -> MinecraftBlockDescriptor: ...
def SmoothStoneDoubleSlab(
    **states: Unpack[SmoothStoneDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SmoothStoneSlab(
    **states: Unpack[SmoothStoneSlabStates],
) -> MinecraftBlockDescriptor: ...
def SnifferEgg(**states: Unpack[SnifferEggStates]) -> MinecraftBlockDescriptor: ...
def Snow() -> MinecraftBlockDescriptor: ...
def SnowLayer(**states: Unpack[SnowLayerStates]) -> MinecraftBlockDescriptor: ...
def SoulCampfire(**states: Unpack[SoulCampfireStates]) -> MinecraftBlockDescriptor: ...
def SoulFire(**states: Unpack[SoulFireStates]) -> MinecraftBlockDescriptor: ...
def SoulLantern(**states: Unpack[SoulLanternStates]) -> MinecraftBlockDescriptor: ...
def SoulSand() -> MinecraftBlockDescriptor: ...
def SoulSoil() -> MinecraftBlockDescriptor: ...
def SoulTorch(**states: Unpack[SoulTorchStates]) -> MinecraftBlockDescriptor: ...
def Sponge() -> MinecraftBlockDescriptor: ...
def SporeBlossom() -> MinecraftBlockDescriptor: ...
def SpruceButton(**states: Unpack[SpruceButtonStates]) -> MinecraftBlockDescriptor: ...
def SpruceDoor(**states: Unpack[SpruceDoorStates]) -> MinecraftBlockDescriptor: ...
def SpruceDoubleSlab(
    **states: Unpack[SpruceDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SpruceFence(**states: Unpack[SpruceFenceStates]) -> MinecraftBlockDescriptor: ...
def SpruceFenceGate(
    **states: Unpack[SpruceFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def SpruceHangingSign(
    **states: Unpack[SpruceHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def SpruceLeaves(**states: Unpack[SpruceLeavesStates]) -> MinecraftBlockDescriptor: ...
def SpruceLog(**states: Unpack[SpruceLogStates]) -> MinecraftBlockDescriptor: ...
def SprucePlanks() -> MinecraftBlockDescriptor: ...
def SprucePressurePlate(
    **states: Unpack[SprucePressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def SpruceSapling(
    **states: Unpack[SpruceSaplingStates],
) -> MinecraftBlockDescriptor: ...
def SpruceShelf(**states: Unpack[SpruceShelfStates]) -> MinecraftBlockDescriptor: ...
def SpruceSlab(**states: Unpack[SpruceSlabStates]) -> MinecraftBlockDescriptor: ...
def SpruceStairs(**states: Unpack[SpruceStairsStates]) -> MinecraftBlockDescriptor: ...
def SpruceStandingSign(
    **states: Unpack[SpruceStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def SpruceTrapdoor(
    **states: Unpack[SpruceTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def SpruceWallSign(
    **states: Unpack[SpruceWallSignStates],
) -> MinecraftBlockDescriptor: ...
def SpruceWood(**states: Unpack[SpruceWoodStates]) -> MinecraftBlockDescriptor: ...
def StandingBanner(
    **states: Unpack[StandingBannerStates],
) -> MinecraftBlockDescriptor: ...
def StandingSign(**states: Unpack[StandingSignStates]) -> MinecraftBlockDescriptor: ...
def StickyPiston(**states: Unpack[StickyPistonStates]) -> MinecraftBlockDescriptor: ...
def StickyPistonArmCollision(
    **states: Unpack[StickyPistonArmCollisionStates],
) -> MinecraftBlockDescriptor: ...
def Stone() -> MinecraftBlockDescriptor: ...
def StoneBrickDoubleSlab(
    **states: Unpack[StoneBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def StoneBrickSlab(
    **states: Unpack[StoneBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def StoneBrickStairs(
    **states: Unpack[StoneBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def StoneBrickWall(
    **states: Unpack[StoneBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def StoneBricks() -> MinecraftBlockDescriptor: ...
def StoneButton(**states: Unpack[StoneButtonStates]) -> MinecraftBlockDescriptor: ...
def StonePressurePlate(
    **states: Unpack[StonePressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def StoneStairs(**states: Unpack[StoneStairsStates]) -> MinecraftBlockDescriptor: ...
def StonecutterBlock(
    **states: Unpack[StonecutterBlockStates],
) -> MinecraftBlockDescriptor: ...
def StrawBed(**states: Unpack[StrawBedStates]) -> MinecraftBlockDescriptor: ...
def StrippedAcaciaLog(
    **states: Unpack[StrippedAcaciaLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedAcaciaWood(
    **states: Unpack[StrippedAcaciaWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedBambooBlock(
    **states: Unpack[StrippedBambooBlockStates],
) -> MinecraftBlockDescriptor: ...
def StrippedBirchLog(
    **states: Unpack[StrippedBirchLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedBirchWood(
    **states: Unpack[StrippedBirchWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedCherryLog(
    **states: Unpack[StrippedCherryLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedCherryWood(
    **states: Unpack[StrippedCherryWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedCrimsonHyphae(
    **states: Unpack[StrippedCrimsonHyphaeStates],
) -> MinecraftBlockDescriptor: ...
def StrippedCrimsonStem(
    **states: Unpack[StrippedCrimsonStemStates],
) -> MinecraftBlockDescriptor: ...
def StrippedDarkOakLog(
    **states: Unpack[StrippedDarkOakLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedDarkOakWood(
    **states: Unpack[StrippedDarkOakWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedJungleLog(
    **states: Unpack[StrippedJungleLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedJungleWood(
    **states: Unpack[StrippedJungleWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedMangroveLog(
    **states: Unpack[StrippedMangroveLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedMangroveWood(
    **states: Unpack[StrippedMangroveWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedOakLog(
    **states: Unpack[StrippedOakLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedOakWood(
    **states: Unpack[StrippedOakWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedPaleOakLog(
    **states: Unpack[StrippedPaleOakLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedPaleOakWood(
    **states: Unpack[StrippedPaleOakWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedPoplarLog(
    **states: Unpack[StrippedPoplarLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedPoplarWood(
    **states: Unpack[StrippedPoplarWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedSpruceLog(
    **states: Unpack[StrippedSpruceLogStates],
) -> MinecraftBlockDescriptor: ...
def StrippedSpruceWood(
    **states: Unpack[StrippedSpruceWoodStates],
) -> MinecraftBlockDescriptor: ...
def StrippedWarpedHyphae(
    **states: Unpack[StrippedWarpedHyphaeStates],
) -> MinecraftBlockDescriptor: ...
def StrippedWarpedStem(
    **states: Unpack[StrippedWarpedStemStates],
) -> MinecraftBlockDescriptor: ...
def StructureBlock(
    **states: Unpack[StructureBlockStates],
) -> MinecraftBlockDescriptor: ...
def StructureVoid() -> MinecraftBlockDescriptor: ...
def Sulfur() -> MinecraftBlockDescriptor: ...
def SulfurBrickDoubleSlab(
    **states: Unpack[SulfurBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SulfurBrickSlab(
    **states: Unpack[SulfurBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def SulfurBrickStairs(
    **states: Unpack[SulfurBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def SulfurBrickWall(
    **states: Unpack[SulfurBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def SulfurBricks() -> MinecraftBlockDescriptor: ...
def SulfurDoubleSlab(
    **states: Unpack[SulfurDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def SulfurSlab(**states: Unpack[SulfurSlabStates]) -> MinecraftBlockDescriptor: ...
def SulfurSpike(**states: Unpack[SulfurSpikeStates]) -> MinecraftBlockDescriptor: ...
def SulfurStairs(**states: Unpack[SulfurStairsStates]) -> MinecraftBlockDescriptor: ...
def SulfurWall(**states: Unpack[SulfurWallStates]) -> MinecraftBlockDescriptor: ...
def Sunflower(**states: Unpack[SunflowerStates]) -> MinecraftBlockDescriptor: ...
def SuspiciousGravel(
    **states: Unpack[SuspiciousGravelStates],
) -> MinecraftBlockDescriptor: ...
def SuspiciousSand(
    **states: Unpack[SuspiciousSandStates],
) -> MinecraftBlockDescriptor: ...
def SweetBerryBush(
    **states: Unpack[SweetBerryBushStates],
) -> MinecraftBlockDescriptor: ...
def TallDryGrass() -> MinecraftBlockDescriptor: ...
def TallGrass(**states: Unpack[TallGrassStates]) -> MinecraftBlockDescriptor: ...
def Target() -> MinecraftBlockDescriptor: ...
def TintedGlass() -> MinecraftBlockDescriptor: ...
def Tnt(**states: Unpack[TntStates]) -> MinecraftBlockDescriptor: ...
def Torch(**states: Unpack[TorchStates]) -> MinecraftBlockDescriptor: ...
def Torchflower() -> MinecraftBlockDescriptor: ...
def TorchflowerCrop(
    **states: Unpack[TorchflowerCropStates],
) -> MinecraftBlockDescriptor: ...
def Trapdoor(**states: Unpack[TrapdoorStates]) -> MinecraftBlockDescriptor: ...
def TrappedChest(**states: Unpack[TrappedChestStates]) -> MinecraftBlockDescriptor: ...
def TrialSpawner(**states: Unpack[TrialSpawnerStates]) -> MinecraftBlockDescriptor: ...
def TripWire(**states: Unpack[TripWireStates]) -> MinecraftBlockDescriptor: ...
def TripwireHook(**states: Unpack[TripwireHookStates]) -> MinecraftBlockDescriptor: ...
def TubeCoral() -> MinecraftBlockDescriptor: ...
def TubeCoralBlock() -> MinecraftBlockDescriptor: ...
def TubeCoralFan(**states: Unpack[TubeCoralFanStates]) -> MinecraftBlockDescriptor: ...
def TubeCoralWallFan(
    **states: Unpack[TubeCoralWallFanStates],
) -> MinecraftBlockDescriptor: ...
def Tuff() -> MinecraftBlockDescriptor: ...
def TuffBrickDoubleSlab(
    **states: Unpack[TuffBrickDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def TuffBrickSlab(
    **states: Unpack[TuffBrickSlabStates],
) -> MinecraftBlockDescriptor: ...
def TuffBrickStairs(
    **states: Unpack[TuffBrickStairsStates],
) -> MinecraftBlockDescriptor: ...
def TuffBrickWall(
    **states: Unpack[TuffBrickWallStates],
) -> MinecraftBlockDescriptor: ...
def TuffBricks() -> MinecraftBlockDescriptor: ...
def TuffDoubleSlab(
    **states: Unpack[TuffDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def TuffSlab(**states: Unpack[TuffSlabStates]) -> MinecraftBlockDescriptor: ...
def TuffStairs(**states: Unpack[TuffStairsStates]) -> MinecraftBlockDescriptor: ...
def TuffWall(**states: Unpack[TuffWallStates]) -> MinecraftBlockDescriptor: ...
def TurtleEgg(**states: Unpack[TurtleEggStates]) -> MinecraftBlockDescriptor: ...
def TwistingVines(
    **states: Unpack[TwistingVinesStates],
) -> MinecraftBlockDescriptor: ...
def UnderwaterTnt(
    **states: Unpack[UnderwaterTntStates],
) -> MinecraftBlockDescriptor: ...
def UnderwaterTorch(
    **states: Unpack[UnderwaterTorchStates],
) -> MinecraftBlockDescriptor: ...
def UndyedShulkerBox() -> MinecraftBlockDescriptor: ...
def Unknown() -> MinecraftBlockDescriptor: ...
def UnlitRedstoneTorch(
    **states: Unpack[UnlitRedstoneTorchStates],
) -> MinecraftBlockDescriptor: ...
def UnpoweredComparator(
    **states: Unpack[UnpoweredComparatorStates],
) -> MinecraftBlockDescriptor: ...
def UnpoweredRepeater(
    **states: Unpack[UnpoweredRepeaterStates],
) -> MinecraftBlockDescriptor: ...
def Vault(**states: Unpack[VaultStates]) -> MinecraftBlockDescriptor: ...
def VerdantFroglight(
    **states: Unpack[VerdantFroglightStates],
) -> MinecraftBlockDescriptor: ...
def Vine(**states: Unpack[VineStates]) -> MinecraftBlockDescriptor: ...
def WallBanner(**states: Unpack[WallBannerStates]) -> MinecraftBlockDescriptor: ...
def WallSign(**states: Unpack[WallSignStates]) -> MinecraftBlockDescriptor: ...
def WarpedButton(**states: Unpack[WarpedButtonStates]) -> MinecraftBlockDescriptor: ...
def WarpedDoor(**states: Unpack[WarpedDoorStates]) -> MinecraftBlockDescriptor: ...
def WarpedDoubleSlab(
    **states: Unpack[WarpedDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def WarpedFence(**states: Unpack[WarpedFenceStates]) -> MinecraftBlockDescriptor: ...
def WarpedFenceGate(
    **states: Unpack[WarpedFenceGateStates],
) -> MinecraftBlockDescriptor: ...
def WarpedFungus() -> MinecraftBlockDescriptor: ...
def WarpedHangingSign(
    **states: Unpack[WarpedHangingSignStates],
) -> MinecraftBlockDescriptor: ...
def WarpedHyphae(**states: Unpack[WarpedHyphaeStates]) -> MinecraftBlockDescriptor: ...
def WarpedNylium() -> MinecraftBlockDescriptor: ...
def WarpedPlanks() -> MinecraftBlockDescriptor: ...
def WarpedPressurePlate(
    **states: Unpack[WarpedPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def WarpedRoots() -> MinecraftBlockDescriptor: ...
def WarpedShelf(**states: Unpack[WarpedShelfStates]) -> MinecraftBlockDescriptor: ...
def WarpedSlab(**states: Unpack[WarpedSlabStates]) -> MinecraftBlockDescriptor: ...
def WarpedStairs(**states: Unpack[WarpedStairsStates]) -> MinecraftBlockDescriptor: ...
def WarpedStandingSign(
    **states: Unpack[WarpedStandingSignStates],
) -> MinecraftBlockDescriptor: ...
def WarpedStem(**states: Unpack[WarpedStemStates]) -> MinecraftBlockDescriptor: ...
def WarpedTrapdoor(
    **states: Unpack[WarpedTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def WarpedWallSign(
    **states: Unpack[WarpedWallSignStates],
) -> MinecraftBlockDescriptor: ...
def WarpedWartBlock() -> MinecraftBlockDescriptor: ...
def Water(**states: Unpack[WaterStates]) -> MinecraftBlockDescriptor: ...
def Waterlily() -> MinecraftBlockDescriptor: ...
def WaxedChiseledCopper() -> MinecraftBlockDescriptor: ...
def WaxedCopper() -> MinecraftBlockDescriptor: ...
def WaxedCopperBars(
    **states: Unpack[WaxedCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperBulb(
    **states: Unpack[WaxedCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperChain(
    **states: Unpack[WaxedCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperChest(
    **states: Unpack[WaxedCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperDoor(
    **states: Unpack[WaxedCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperGolemStatue(
    **states: Unpack[WaxedCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperGrate() -> MinecraftBlockDescriptor: ...
def WaxedCopperLantern(
    **states: Unpack[WaxedCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCopperTrapdoor(
    **states: Unpack[WaxedCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCutCopper() -> MinecraftBlockDescriptor: ...
def WaxedCutCopperSlab(
    **states: Unpack[WaxedCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedCutCopperStairs(
    **states: Unpack[WaxedCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedDoubleCutCopperSlab(
    **states: Unpack[WaxedDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedChiseledCopper() -> MinecraftBlockDescriptor: ...
def WaxedExposedCopper() -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperBars(
    **states: Unpack[WaxedExposedCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperBulb(
    **states: Unpack[WaxedExposedCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperChain(
    **states: Unpack[WaxedExposedCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperChest(
    **states: Unpack[WaxedExposedCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperDoor(
    **states: Unpack[WaxedExposedCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperGolemStatue(
    **states: Unpack[WaxedExposedCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperGrate() -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperLantern(
    **states: Unpack[WaxedExposedCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCopperTrapdoor(
    **states: Unpack[WaxedExposedCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCutCopper() -> MinecraftBlockDescriptor: ...
def WaxedExposedCutCopperSlab(
    **states: Unpack[WaxedExposedCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedCutCopperStairs(
    **states: Unpack[WaxedExposedCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedDoubleCutCopperSlab(
    **states: Unpack[WaxedExposedDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedExposedLightningRod(
    **states: Unpack[WaxedExposedLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def WaxedLightningRod(
    **states: Unpack[WaxedLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedChiseledCopper() -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopper() -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperBars(
    **states: Unpack[WaxedOxidizedCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperBulb(
    **states: Unpack[WaxedOxidizedCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperChain(
    **states: Unpack[WaxedOxidizedCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperChest(
    **states: Unpack[WaxedOxidizedCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperDoor(
    **states: Unpack[WaxedOxidizedCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperGolemStatue(
    **states: Unpack[WaxedOxidizedCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperGrate() -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperLantern(
    **states: Unpack[WaxedOxidizedCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCopperTrapdoor(
    **states: Unpack[WaxedOxidizedCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCutCopper() -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCutCopperSlab(
    **states: Unpack[WaxedOxidizedCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedCutCopperStairs(
    **states: Unpack[WaxedOxidizedCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedDoubleCutCopperSlab(
    **states: Unpack[WaxedOxidizedDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedOxidizedLightningRod(
    **states: Unpack[WaxedOxidizedLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredChiseledCopper() -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopper() -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperBars(
    **states: Unpack[WaxedWeatheredCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperBulb(
    **states: Unpack[WaxedWeatheredCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperChain(
    **states: Unpack[WaxedWeatheredCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperChest(
    **states: Unpack[WaxedWeatheredCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperDoor(
    **states: Unpack[WaxedWeatheredCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperGolemStatue(
    **states: Unpack[WaxedWeatheredCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperGrate() -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperLantern(
    **states: Unpack[WaxedWeatheredCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCopperTrapdoor(
    **states: Unpack[WaxedWeatheredCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCutCopper() -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCutCopperSlab(
    **states: Unpack[WaxedWeatheredCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredCutCopperStairs(
    **states: Unpack[WaxedWeatheredCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredDoubleCutCopperSlab(
    **states: Unpack[WaxedWeatheredDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WaxedWeatheredLightningRod(
    **states: Unpack[WaxedWeatheredLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredChiseledCopper() -> MinecraftBlockDescriptor: ...
def WeatheredCopper() -> MinecraftBlockDescriptor: ...
def WeatheredCopperBars(
    **states: Unpack[WeatheredCopperBarsStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperBulb(
    **states: Unpack[WeatheredCopperBulbStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperChain(
    **states: Unpack[WeatheredCopperChainStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperChest(
    **states: Unpack[WeatheredCopperChestStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperDoor(
    **states: Unpack[WeatheredCopperDoorStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperGolemStatue(
    **states: Unpack[WeatheredCopperGolemStatueStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperGrate() -> MinecraftBlockDescriptor: ...
def WeatheredCopperLantern(
    **states: Unpack[WeatheredCopperLanternStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCopperTrapdoor(
    **states: Unpack[WeatheredCopperTrapdoorStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCutCopper() -> MinecraftBlockDescriptor: ...
def WeatheredCutCopperSlab(
    **states: Unpack[WeatheredCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredCutCopperStairs(
    **states: Unpack[WeatheredCutCopperStairsStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredDoubleCutCopperSlab(
    **states: Unpack[WeatheredDoubleCutCopperSlabStates],
) -> MinecraftBlockDescriptor: ...
def WeatheredLightningRod(
    **states: Unpack[WeatheredLightningRodStates],
) -> MinecraftBlockDescriptor: ...
def Web() -> MinecraftBlockDescriptor: ...
def WeepingVines(**states: Unpack[WeepingVinesStates]) -> MinecraftBlockDescriptor: ...
def WetSponge() -> MinecraftBlockDescriptor: ...
def Wheat(**states: Unpack[WheatStates]) -> MinecraftBlockDescriptor: ...
def WhiteCandle(**states: Unpack[WhiteCandleStates]) -> MinecraftBlockDescriptor: ...
def WhiteCandleCake(
    **states: Unpack[WhiteCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def WhiteCarpet() -> MinecraftBlockDescriptor: ...
def WhiteConcrete() -> MinecraftBlockDescriptor: ...
def WhiteConcreteDoubleSlab(
    **states: Unpack[WhiteConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def WhiteConcretePowder() -> MinecraftBlockDescriptor: ...
def WhiteConcreteSlab(
    **states: Unpack[WhiteConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def WhiteConcreteStairs(
    **states: Unpack[WhiteConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def WhiteGlazedTerracotta(
    **states: Unpack[WhiteGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def WhiteShulkerBox() -> MinecraftBlockDescriptor: ...
def WhiteStainedGlass() -> MinecraftBlockDescriptor: ...
def WhiteStainedGlassPane(
    **states: Unpack[WhiteStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def WhiteTerracotta() -> MinecraftBlockDescriptor: ...
def WhiteTulip() -> MinecraftBlockDescriptor: ...
def WhiteWool() -> MinecraftBlockDescriptor: ...
def WhiteWoolDoubleSlab(
    **states: Unpack[WhiteWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def WhiteWoolSlab(
    **states: Unpack[WhiteWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def WhiteWoolStairs(
    **states: Unpack[WhiteWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def Wildflowers(**states: Unpack[WildflowersStates]) -> MinecraftBlockDescriptor: ...
def WitherRose() -> MinecraftBlockDescriptor: ...
def WitherSkeletonSkull(
    **states: Unpack[WitherSkeletonSkullStates],
) -> MinecraftBlockDescriptor: ...
def WoodenButton(**states: Unpack[WoodenButtonStates]) -> MinecraftBlockDescriptor: ...
def WoodenDoor(**states: Unpack[WoodenDoorStates]) -> MinecraftBlockDescriptor: ...
def WoodenPressurePlate(
    **states: Unpack[WoodenPressurePlateStates],
) -> MinecraftBlockDescriptor: ...
def YellowCandle(**states: Unpack[YellowCandleStates]) -> MinecraftBlockDescriptor: ...
def YellowCandleCake(
    **states: Unpack[YellowCandleCakeStates],
) -> MinecraftBlockDescriptor: ...
def YellowCarpet() -> MinecraftBlockDescriptor: ...
def YellowConcrete() -> MinecraftBlockDescriptor: ...
def YellowConcreteDoubleSlab(
    **states: Unpack[YellowConcreteDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def YellowConcretePowder() -> MinecraftBlockDescriptor: ...
def YellowConcreteSlab(
    **states: Unpack[YellowConcreteSlabStates],
) -> MinecraftBlockDescriptor: ...
def YellowConcreteStairs(
    **states: Unpack[YellowConcreteStairsStates],
) -> MinecraftBlockDescriptor: ...
def YellowGlazedTerracotta(
    **states: Unpack[YellowGlazedTerracottaStates],
) -> MinecraftBlockDescriptor: ...
def YellowPoplarLeaves(
    **states: Unpack[YellowPoplarLeavesStates],
) -> MinecraftBlockDescriptor: ...
def YellowShulkerBox() -> MinecraftBlockDescriptor: ...
def YellowStainedGlass() -> MinecraftBlockDescriptor: ...
def YellowStainedGlassPane(
    **states: Unpack[YellowStainedGlassPaneStates],
) -> MinecraftBlockDescriptor: ...
def YellowTerracotta() -> MinecraftBlockDescriptor: ...
def YellowWool() -> MinecraftBlockDescriptor: ...
def YellowWoolDoubleSlab(
    **states: Unpack[YellowWoolDoubleSlabStates],
) -> MinecraftBlockDescriptor: ...
def YellowWoolSlab(
    **states: Unpack[YellowWoolSlabStates],
) -> MinecraftBlockDescriptor: ...
def YellowWoolStairs(
    **states: Unpack[YellowWoolStairsStates],
) -> MinecraftBlockDescriptor: ...
def ZombieHead(**states: Unpack[ZombieHeadStates]) -> MinecraftBlockDescriptor: ...
