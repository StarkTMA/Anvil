from enum import StrEnum
from typing import Literal, TypedDict, Unpack

from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.lib.jsonmodel import Identifier

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

def AcaciaButton(
    **states: Unpack[AcaciaButtonStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaDoor(**states: Unpack[AcaciaDoorStates]) -> Identifier | BlockDescriptor: ...
def AcaciaDoubleSlab(
    **states: Unpack[AcaciaDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaFence(
    **states: Unpack[AcaciaFenceStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaFenceGate(
    **states: Unpack[AcaciaFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaHangingSign(
    **states: Unpack[AcaciaHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaLeaves(
    **states: Unpack[AcaciaLeavesStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaLog(**states: Unpack[AcaciaLogStates]) -> Identifier | BlockDescriptor: ...
def AcaciaPlanks() -> Identifier: ...
def AcaciaPressurePlate(
    **states: Unpack[AcaciaPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaSapling(
    **states: Unpack[AcaciaSaplingStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaShelf(
    **states: Unpack[AcaciaShelfStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaSlab(**states: Unpack[AcaciaSlabStates]) -> Identifier | BlockDescriptor: ...
def AcaciaStairs(
    **states: Unpack[AcaciaStairsStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaStandingSign(
    **states: Unpack[AcaciaStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaTrapdoor(
    **states: Unpack[AcaciaTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaWallSign(
    **states: Unpack[AcaciaWallSignStates],
) -> Identifier | BlockDescriptor: ...
def AcaciaWood(**states: Unpack[AcaciaWoodStates]) -> Identifier | BlockDescriptor: ...
def ActivatorRail(
    **states: Unpack[ActivatorRailStates],
) -> Identifier | BlockDescriptor: ...
def Air() -> Identifier: ...
def Allium() -> Identifier: ...
def Allow() -> Identifier: ...
def AmethystBlock() -> Identifier: ...
def AmethystCluster(
    **states: Unpack[AmethystClusterStates],
) -> Identifier | BlockDescriptor: ...
def AncientDebris() -> Identifier: ...
def Andesite() -> Identifier: ...
def AndesiteDoubleSlab(
    **states: Unpack[AndesiteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def AndesiteSlab(
    **states: Unpack[AndesiteSlabStates],
) -> Identifier | BlockDescriptor: ...
def AndesiteStairs(
    **states: Unpack[AndesiteStairsStates],
) -> Identifier | BlockDescriptor: ...
def AndesiteWall(
    **states: Unpack[AndesiteWallStates],
) -> Identifier | BlockDescriptor: ...
def Anvil(**states: Unpack[AnvilStates]) -> Identifier | BlockDescriptor: ...
def Azalea() -> Identifier: ...
def AzaleaLeaves(
    **states: Unpack[AzaleaLeavesStates],
) -> Identifier | BlockDescriptor: ...
def AzaleaLeavesFlowered(
    **states: Unpack[AzaleaLeavesFloweredStates],
) -> Identifier | BlockDescriptor: ...
def AzureBluet() -> Identifier: ...
def Bamboo(**states: Unpack[BambooStates]) -> Identifier | BlockDescriptor: ...
def BambooBlock(
    **states: Unpack[BambooBlockStates],
) -> Identifier | BlockDescriptor: ...
def BambooButton(
    **states: Unpack[BambooButtonStates],
) -> Identifier | BlockDescriptor: ...
def BambooDoor(**states: Unpack[BambooDoorStates]) -> Identifier | BlockDescriptor: ...
def BambooDoubleSlab(
    **states: Unpack[BambooDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BambooFence(
    **states: Unpack[BambooFenceStates],
) -> Identifier | BlockDescriptor: ...
def BambooFenceGate(
    **states: Unpack[BambooFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def BambooHangingSign(
    **states: Unpack[BambooHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def BambooMosaic() -> Identifier: ...
def BambooMosaicDoubleSlab(
    **states: Unpack[BambooMosaicDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BambooMosaicSlab(
    **states: Unpack[BambooMosaicSlabStates],
) -> Identifier | BlockDescriptor: ...
def BambooMosaicStairs(
    **states: Unpack[BambooMosaicStairsStates],
) -> Identifier | BlockDescriptor: ...
def BambooPlanks() -> Identifier: ...
def BambooPressurePlate(
    **states: Unpack[BambooPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def BambooSapling(
    **states: Unpack[BambooSaplingStates],
) -> Identifier | BlockDescriptor: ...
def BambooShelf(
    **states: Unpack[BambooShelfStates],
) -> Identifier | BlockDescriptor: ...
def BambooSlab(**states: Unpack[BambooSlabStates]) -> Identifier | BlockDescriptor: ...
def BambooStairs(
    **states: Unpack[BambooStairsStates],
) -> Identifier | BlockDescriptor: ...
def BambooStandingSign(
    **states: Unpack[BambooStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def BambooTrapdoor(
    **states: Unpack[BambooTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def BambooWallSign(
    **states: Unpack[BambooWallSignStates],
) -> Identifier | BlockDescriptor: ...
def Barrel(**states: Unpack[BarrelStates]) -> Identifier | BlockDescriptor: ...
def Barrier() -> Identifier: ...
def Basalt(**states: Unpack[BasaltStates]) -> Identifier | BlockDescriptor: ...
def Beacon() -> Identifier: ...
def Bed(**states: Unpack[BedStates]) -> Identifier | BlockDescriptor: ...
def Bedrock(**states: Unpack[BedrockStates]) -> Identifier | BlockDescriptor: ...
def BeeNest(**states: Unpack[BeeNestStates]) -> Identifier | BlockDescriptor: ...
def Beehive(**states: Unpack[BeehiveStates]) -> Identifier | BlockDescriptor: ...
def Beetroot(**states: Unpack[BeetrootStates]) -> Identifier | BlockDescriptor: ...
def Bell(**states: Unpack[BellStates]) -> Identifier | BlockDescriptor: ...
def BigDripleaf(
    **states: Unpack[BigDripleafStates],
) -> Identifier | BlockDescriptor: ...
def BirchButton(
    **states: Unpack[BirchButtonStates],
) -> Identifier | BlockDescriptor: ...
def BirchDoor(**states: Unpack[BirchDoorStates]) -> Identifier | BlockDescriptor: ...
def BirchDoubleSlab(
    **states: Unpack[BirchDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BirchFence(**states: Unpack[BirchFenceStates]) -> Identifier | BlockDescriptor: ...
def BirchFenceGate(
    **states: Unpack[BirchFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def BirchHangingSign(
    **states: Unpack[BirchHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def BirchLeaves(
    **states: Unpack[BirchLeavesStates],
) -> Identifier | BlockDescriptor: ...
def BirchLog(**states: Unpack[BirchLogStates]) -> Identifier | BlockDescriptor: ...
def BirchPlanks() -> Identifier: ...
def BirchPressurePlate(
    **states: Unpack[BirchPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def BirchSapling(
    **states: Unpack[BirchSaplingStates],
) -> Identifier | BlockDescriptor: ...
def BirchShelf(**states: Unpack[BirchShelfStates]) -> Identifier | BlockDescriptor: ...
def BirchSlab(**states: Unpack[BirchSlabStates]) -> Identifier | BlockDescriptor: ...
def BirchStairs(
    **states: Unpack[BirchStairsStates],
) -> Identifier | BlockDescriptor: ...
def BirchStandingSign(
    **states: Unpack[BirchStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def BirchTrapdoor(
    **states: Unpack[BirchTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def BirchWallSign(
    **states: Unpack[BirchWallSignStates],
) -> Identifier | BlockDescriptor: ...
def BirchWood(**states: Unpack[BirchWoodStates]) -> Identifier | BlockDescriptor: ...
def BlackCandle(
    **states: Unpack[BlackCandleStates],
) -> Identifier | BlockDescriptor: ...
def BlackCandleCake(
    **states: Unpack[BlackCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def BlackCarpet() -> Identifier: ...
def BlackConcrete() -> Identifier: ...
def BlackConcreteDoubleSlab(
    **states: Unpack[BlackConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlackConcretePowder() -> Identifier: ...
def BlackConcreteSlab(
    **states: Unpack[BlackConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlackConcreteStairs(
    **states: Unpack[BlackConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def BlackGlazedTerracotta(
    **states: Unpack[BlackGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def BlackShulkerBox() -> Identifier: ...
def BlackStainedGlass() -> Identifier: ...
def BlackStainedGlassPane(
    **states: Unpack[BlackStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def BlackTerracotta() -> Identifier: ...
def BlackWool() -> Identifier: ...
def BlackWoolDoubleSlab(
    **states: Unpack[BlackWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlackWoolSlab(
    **states: Unpack[BlackWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlackWoolStairs(
    **states: Unpack[BlackWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def Blackstone() -> Identifier: ...
def BlackstoneDoubleSlab(
    **states: Unpack[BlackstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlackstoneSlab(
    **states: Unpack[BlackstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlackstoneStairs(
    **states: Unpack[BlackstoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def BlackstoneWall(
    **states: Unpack[BlackstoneWallStates],
) -> Identifier | BlockDescriptor: ...
def BlastFurnace(
    **states: Unpack[BlastFurnaceStates],
) -> Identifier | BlockDescriptor: ...
def BlueCandle(**states: Unpack[BlueCandleStates]) -> Identifier | BlockDescriptor: ...
def BlueCandleCake(
    **states: Unpack[BlueCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def BlueCarpet() -> Identifier: ...
def BlueConcrete() -> Identifier: ...
def BlueConcreteDoubleSlab(
    **states: Unpack[BlueConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlueConcretePowder() -> Identifier: ...
def BlueConcreteSlab(
    **states: Unpack[BlueConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlueConcreteStairs(
    **states: Unpack[BlueConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def BlueGlazedTerracotta(
    **states: Unpack[BlueGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def BlueIce() -> Identifier: ...
def BlueOrchid() -> Identifier: ...
def BlueShulkerBox() -> Identifier: ...
def BlueStainedGlass() -> Identifier: ...
def BlueStainedGlassPane(
    **states: Unpack[BlueStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def BlueTerracotta() -> Identifier: ...
def BlueWool() -> Identifier: ...
def BlueWoolDoubleSlab(
    **states: Unpack[BlueWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlueWoolSlab(
    **states: Unpack[BlueWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def BlueWoolStairs(
    **states: Unpack[BlueWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def BoneBlock(**states: Unpack[BoneBlockStates]) -> Identifier | BlockDescriptor: ...
def Bookshelf() -> Identifier: ...
def BorderBlock(
    **states: Unpack[BorderBlockStates],
) -> Identifier | BlockDescriptor: ...
def BrainCoral() -> Identifier: ...
def BrainCoralBlock() -> Identifier: ...
def BrainCoralFan(
    **states: Unpack[BrainCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def BrainCoralWallFan(
    **states: Unpack[BrainCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def BrewingStand(
    **states: Unpack[BrewingStandStates],
) -> Identifier | BlockDescriptor: ...
def BrickBlock() -> Identifier: ...
def BrickDoubleSlab(
    **states: Unpack[BrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BrickSlab(**states: Unpack[BrickSlabStates]) -> Identifier | BlockDescriptor: ...
def BrickStairs(
    **states: Unpack[BrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def BrickWall(**states: Unpack[BrickWallStates]) -> Identifier | BlockDescriptor: ...
def BrownCandle(
    **states: Unpack[BrownCandleStates],
) -> Identifier | BlockDescriptor: ...
def BrownCandleCake(
    **states: Unpack[BrownCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def BrownCarpet() -> Identifier: ...
def BrownConcrete() -> Identifier: ...
def BrownConcreteDoubleSlab(
    **states: Unpack[BrownConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BrownConcretePowder() -> Identifier: ...
def BrownConcreteSlab(
    **states: Unpack[BrownConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def BrownConcreteStairs(
    **states: Unpack[BrownConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def BrownGlazedTerracotta(
    **states: Unpack[BrownGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def BrownMushroom() -> Identifier: ...
def BrownMushroomBlock(
    **states: Unpack[BrownMushroomBlockStates],
) -> Identifier | BlockDescriptor: ...
def BrownShulkerBox() -> Identifier: ...
def BrownStainedGlass() -> Identifier: ...
def BrownStainedGlassPane(
    **states: Unpack[BrownStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def BrownTerracotta() -> Identifier: ...
def BrownWool() -> Identifier: ...
def BrownWoolDoubleSlab(
    **states: Unpack[BrownWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def BrownWoolSlab(
    **states: Unpack[BrownWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def BrownWoolStairs(
    **states: Unpack[BrownWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def BubbleColumn(
    **states: Unpack[BubbleColumnStates],
) -> Identifier | BlockDescriptor: ...
def BubbleCoral() -> Identifier: ...
def BubbleCoralBlock() -> Identifier: ...
def BubbleCoralFan(
    **states: Unpack[BubbleCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def BubbleCoralWallFan(
    **states: Unpack[BubbleCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def BuddingAmethyst() -> Identifier: ...
def Bush() -> Identifier: ...
def Cactus(**states: Unpack[CactusStates]) -> Identifier | BlockDescriptor: ...
def CactusFlower() -> Identifier: ...
def Cake(**states: Unpack[CakeStates]) -> Identifier | BlockDescriptor: ...
def Calcite() -> Identifier: ...
def CalibratedSculkSensor(
    **states: Unpack[CalibratedSculkSensorStates],
) -> Identifier | BlockDescriptor: ...
def Camera() -> Identifier: ...
def Campfire(**states: Unpack[CampfireStates]) -> Identifier | BlockDescriptor: ...
def Candle(**states: Unpack[CandleStates]) -> Identifier | BlockDescriptor: ...
def CandleCake(**states: Unpack[CandleCakeStates]) -> Identifier | BlockDescriptor: ...
def Carrots(**states: Unpack[CarrotsStates]) -> Identifier | BlockDescriptor: ...
def CartographyTable() -> Identifier: ...
def CarvedPumpkin(
    **states: Unpack[CarvedPumpkinStates],
) -> Identifier | BlockDescriptor: ...
def Cauldron(**states: Unpack[CauldronStates]) -> Identifier | BlockDescriptor: ...
def CaveVines(**states: Unpack[CaveVinesStates]) -> Identifier | BlockDescriptor: ...
def CaveVinesBodyWithBerries(
    **states: Unpack[CaveVinesBodyWithBerriesStates],
) -> Identifier | BlockDescriptor: ...
def CaveVinesHeadWithBerries(
    **states: Unpack[CaveVinesHeadWithBerriesStates],
) -> Identifier | BlockDescriptor: ...
def ChainCommandBlock(
    **states: Unpack[ChainCommandBlockStates],
) -> Identifier | BlockDescriptor: ...
def ChemicalHeat() -> Identifier: ...
def CherryButton(
    **states: Unpack[CherryButtonStates],
) -> Identifier | BlockDescriptor: ...
def CherryDoor(**states: Unpack[CherryDoorStates]) -> Identifier | BlockDescriptor: ...
def CherryDoubleSlab(
    **states: Unpack[CherryDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CherryFence(
    **states: Unpack[CherryFenceStates],
) -> Identifier | BlockDescriptor: ...
def CherryFenceGate(
    **states: Unpack[CherryFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def CherryHangingSign(
    **states: Unpack[CherryHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def CherryLeaves(
    **states: Unpack[CherryLeavesStates],
) -> Identifier | BlockDescriptor: ...
def CherryLog(**states: Unpack[CherryLogStates]) -> Identifier | BlockDescriptor: ...
def CherryPlanks() -> Identifier: ...
def CherryPressurePlate(
    **states: Unpack[CherryPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def CherrySapling(
    **states: Unpack[CherrySaplingStates],
) -> Identifier | BlockDescriptor: ...
def CherryShelf(
    **states: Unpack[CherryShelfStates],
) -> Identifier | BlockDescriptor: ...
def CherrySlab(**states: Unpack[CherrySlabStates]) -> Identifier | BlockDescriptor: ...
def CherryStairs(
    **states: Unpack[CherryStairsStates],
) -> Identifier | BlockDescriptor: ...
def CherryStandingSign(
    **states: Unpack[CherryStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def CherryTrapdoor(
    **states: Unpack[CherryTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def CherryWallSign(
    **states: Unpack[CherryWallSignStates],
) -> Identifier | BlockDescriptor: ...
def CherryWood(**states: Unpack[CherryWoodStates]) -> Identifier | BlockDescriptor: ...
def Chest(**states: Unpack[ChestStates]) -> Identifier | BlockDescriptor: ...
def ChippedAnvil(
    **states: Unpack[ChippedAnvilStates],
) -> Identifier | BlockDescriptor: ...
def ChiseledBookshelf(
    **states: Unpack[ChiseledBookshelfStates],
) -> Identifier | BlockDescriptor: ...
def ChiseledCinnabar() -> Identifier: ...
def ChiseledCopper() -> Identifier: ...
def ChiseledDeepslate() -> Identifier: ...
def ChiseledNetherBricks() -> Identifier: ...
def ChiseledPolishedBlackstone() -> Identifier: ...
def ChiseledQuartzBlock(
    **states: Unpack[ChiseledQuartzBlockStates],
) -> Identifier | BlockDescriptor: ...
def ChiseledRedSandstone() -> Identifier: ...
def ChiseledResinBricks() -> Identifier: ...
def ChiseledSandstone() -> Identifier: ...
def ChiseledStoneBricks() -> Identifier: ...
def ChiseledSulfur() -> Identifier: ...
def ChiseledTuff() -> Identifier: ...
def ChiseledTuffBricks() -> Identifier: ...
def ChorusFlower(
    **states: Unpack[ChorusFlowerStates],
) -> Identifier | BlockDescriptor: ...
def ChorusPlant() -> Identifier: ...
def Cinnabar() -> Identifier: ...
def CinnabarBrickDoubleSlab(
    **states: Unpack[CinnabarBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarBrickSlab(
    **states: Unpack[CinnabarBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarBrickStairs(
    **states: Unpack[CinnabarBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarBrickWall(
    **states: Unpack[CinnabarBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarBricks() -> Identifier: ...
def CinnabarDoubleSlab(
    **states: Unpack[CinnabarDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarSlab(
    **states: Unpack[CinnabarSlabStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarStairs(
    **states: Unpack[CinnabarStairsStates],
) -> Identifier | BlockDescriptor: ...
def CinnabarWall(
    **states: Unpack[CinnabarWallStates],
) -> Identifier | BlockDescriptor: ...
def Clay() -> Identifier: ...
def ClosedEyeblossom() -> Identifier: ...
def CoalBlock() -> Identifier: ...
def CoalOre() -> Identifier: ...
def CoarseDirt() -> Identifier: ...
def CobbledDeepslate() -> Identifier: ...
def CobbledDeepslateDoubleSlab(
    **states: Unpack[CobbledDeepslateDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CobbledDeepslateSlab(
    **states: Unpack[CobbledDeepslateSlabStates],
) -> Identifier | BlockDescriptor: ...
def CobbledDeepslateStairs(
    **states: Unpack[CobbledDeepslateStairsStates],
) -> Identifier | BlockDescriptor: ...
def CobbledDeepslateWall(
    **states: Unpack[CobbledDeepslateWallStates],
) -> Identifier | BlockDescriptor: ...
def Cobblestone() -> Identifier: ...
def CobblestoneDoubleSlab(
    **states: Unpack[CobblestoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CobblestoneSlab(
    **states: Unpack[CobblestoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def CobblestoneWall(
    **states: Unpack[CobblestoneWallStates],
) -> Identifier | BlockDescriptor: ...
def Cocoa(**states: Unpack[CocoaStates]) -> Identifier | BlockDescriptor: ...
def ColoredTorchBlue(
    **states: Unpack[ColoredTorchBlueStates],
) -> Identifier | BlockDescriptor: ...
def ColoredTorchGreen(
    **states: Unpack[ColoredTorchGreenStates],
) -> Identifier | BlockDescriptor: ...
def ColoredTorchPurple(
    **states: Unpack[ColoredTorchPurpleStates],
) -> Identifier | BlockDescriptor: ...
def ColoredTorchRed(
    **states: Unpack[ColoredTorchRedStates],
) -> Identifier | BlockDescriptor: ...
def CommandBlock(
    **states: Unpack[CommandBlockStates],
) -> Identifier | BlockDescriptor: ...
def Composter(**states: Unpack[ComposterStates]) -> Identifier | BlockDescriptor: ...
def CompoundCreator(
    **states: Unpack[CompoundCreatorStates],
) -> Identifier | BlockDescriptor: ...
def Conduit() -> Identifier: ...
def CopperBars(**states: Unpack[CopperBarsStates]) -> Identifier | BlockDescriptor: ...
def CopperBlock() -> Identifier: ...
def CopperBulb(**states: Unpack[CopperBulbStates]) -> Identifier | BlockDescriptor: ...
def CopperChain(
    **states: Unpack[CopperChainStates],
) -> Identifier | BlockDescriptor: ...
def CopperChest(
    **states: Unpack[CopperChestStates],
) -> Identifier | BlockDescriptor: ...
def CopperDoor(**states: Unpack[CopperDoorStates]) -> Identifier | BlockDescriptor: ...
def CopperGolemStatue(
    **states: Unpack[CopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def CopperGrate() -> Identifier: ...
def CopperLantern(
    **states: Unpack[CopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def CopperOre() -> Identifier: ...
def CopperTorch(
    **states: Unpack[CopperTorchStates],
) -> Identifier | BlockDescriptor: ...
def CopperTrapdoor(
    **states: Unpack[CopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def Cornflower() -> Identifier: ...
def CrackedDeepslateBricks() -> Identifier: ...
def CrackedDeepslateTiles() -> Identifier: ...
def CrackedNetherBricks() -> Identifier: ...
def CrackedPolishedBlackstoneBricks() -> Identifier: ...
def CrackedStoneBricks() -> Identifier: ...
def Crafter(**states: Unpack[CrafterStates]) -> Identifier | BlockDescriptor: ...
def CraftingTable() -> Identifier: ...
def CreakingHeart(
    **states: Unpack[CreakingHeartStates],
) -> Identifier | BlockDescriptor: ...
def CreeperHead(
    **states: Unpack[CreeperHeadStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonButton(
    **states: Unpack[CrimsonButtonStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonDoor(
    **states: Unpack[CrimsonDoorStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonDoubleSlab(
    **states: Unpack[CrimsonDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonFence(
    **states: Unpack[CrimsonFenceStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonFenceGate(
    **states: Unpack[CrimsonFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonFungus() -> Identifier: ...
def CrimsonHangingSign(
    **states: Unpack[CrimsonHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonHyphae(
    **states: Unpack[CrimsonHyphaeStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonNylium() -> Identifier: ...
def CrimsonPlanks() -> Identifier: ...
def CrimsonPressurePlate(
    **states: Unpack[CrimsonPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonRoots() -> Identifier: ...
def CrimsonShelf(
    **states: Unpack[CrimsonShelfStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonSlab(
    **states: Unpack[CrimsonSlabStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonStairs(
    **states: Unpack[CrimsonStairsStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonStandingSign(
    **states: Unpack[CrimsonStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonStem(
    **states: Unpack[CrimsonStemStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonTrapdoor(
    **states: Unpack[CrimsonTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def CrimsonWallSign(
    **states: Unpack[CrimsonWallSignStates],
) -> Identifier | BlockDescriptor: ...
def CryingObsidian() -> Identifier: ...
def CutCopper() -> Identifier: ...
def CutCopperSlab(
    **states: Unpack[CutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def CutCopperStairs(
    **states: Unpack[CutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def CutRedSandstone() -> Identifier: ...
def CutRedSandstoneDoubleSlab(
    **states: Unpack[CutRedSandstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CutRedSandstoneSlab(
    **states: Unpack[CutRedSandstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def CutSandstone() -> Identifier: ...
def CutSandstoneDoubleSlab(
    **states: Unpack[CutSandstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CutSandstoneSlab(
    **states: Unpack[CutSandstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def CyanCandle(**states: Unpack[CyanCandleStates]) -> Identifier | BlockDescriptor: ...
def CyanCandleCake(
    **states: Unpack[CyanCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def CyanCarpet() -> Identifier: ...
def CyanConcrete() -> Identifier: ...
def CyanConcreteDoubleSlab(
    **states: Unpack[CyanConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CyanConcretePowder() -> Identifier: ...
def CyanConcreteSlab(
    **states: Unpack[CyanConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def CyanConcreteStairs(
    **states: Unpack[CyanConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def CyanGlazedTerracotta(
    **states: Unpack[CyanGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def CyanShulkerBox() -> Identifier: ...
def CyanStainedGlass() -> Identifier: ...
def CyanStainedGlassPane(
    **states: Unpack[CyanStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def CyanTerracotta() -> Identifier: ...
def CyanWool() -> Identifier: ...
def CyanWoolDoubleSlab(
    **states: Unpack[CyanWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def CyanWoolSlab(
    **states: Unpack[CyanWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def CyanWoolStairs(
    **states: Unpack[CyanWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def DamagedAnvil(
    **states: Unpack[DamagedAnvilStates],
) -> Identifier | BlockDescriptor: ...
def Dandelion() -> Identifier: ...
def DarkOakButton(
    **states: Unpack[DarkOakButtonStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakDoor(
    **states: Unpack[DarkOakDoorStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakDoubleSlab(
    **states: Unpack[DarkOakDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakFence(
    **states: Unpack[DarkOakFenceStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakFenceGate(
    **states: Unpack[DarkOakFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakHangingSign(
    **states: Unpack[DarkOakHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakLeaves(
    **states: Unpack[DarkOakLeavesStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakLog(**states: Unpack[DarkOakLogStates]) -> Identifier | BlockDescriptor: ...
def DarkOakPlanks() -> Identifier: ...
def DarkOakPressurePlate(
    **states: Unpack[DarkOakPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakSapling(
    **states: Unpack[DarkOakSaplingStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakShelf(
    **states: Unpack[DarkOakShelfStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakSlab(
    **states: Unpack[DarkOakSlabStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakStairs(
    **states: Unpack[DarkOakStairsStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakTrapdoor(
    **states: Unpack[DarkOakTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def DarkOakWood(
    **states: Unpack[DarkOakWoodStates],
) -> Identifier | BlockDescriptor: ...
def DarkPrismarine() -> Identifier: ...
def DarkPrismarineDoubleSlab(
    **states: Unpack[DarkPrismarineDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def DarkPrismarineSlab(
    **states: Unpack[DarkPrismarineSlabStates],
) -> Identifier | BlockDescriptor: ...
def DarkPrismarineStairs(
    **states: Unpack[DarkPrismarineStairsStates],
) -> Identifier | BlockDescriptor: ...
def DarkoakStandingSign(
    **states: Unpack[DarkoakStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def DarkoakWallSign(
    **states: Unpack[DarkoakWallSignStates],
) -> Identifier | BlockDescriptor: ...
def DaylightDetector(
    **states: Unpack[DaylightDetectorStates],
) -> Identifier | BlockDescriptor: ...
def DaylightDetectorInverted(
    **states: Unpack[DaylightDetectorInvertedStates],
) -> Identifier | BlockDescriptor: ...
def DeadBrainCoral() -> Identifier: ...
def DeadBrainCoralBlock() -> Identifier: ...
def DeadBrainCoralFan(
    **states: Unpack[DeadBrainCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadBrainCoralWallFan(
    **states: Unpack[DeadBrainCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadBubbleCoral() -> Identifier: ...
def DeadBubbleCoralBlock() -> Identifier: ...
def DeadBubbleCoralFan(
    **states: Unpack[DeadBubbleCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadBubbleCoralWallFan(
    **states: Unpack[DeadBubbleCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadFireCoral() -> Identifier: ...
def DeadFireCoralBlock() -> Identifier: ...
def DeadFireCoralFan(
    **states: Unpack[DeadFireCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadFireCoralWallFan(
    **states: Unpack[DeadFireCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadHornCoral() -> Identifier: ...
def DeadHornCoralBlock() -> Identifier: ...
def DeadHornCoralFan(
    **states: Unpack[DeadHornCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadHornCoralWallFan(
    **states: Unpack[DeadHornCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadTubeCoral() -> Identifier: ...
def DeadTubeCoralBlock() -> Identifier: ...
def DeadTubeCoralFan(
    **states: Unpack[DeadTubeCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def DeadTubeCoralWallFan(
    **states: Unpack[DeadTubeCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def Deadbush() -> Identifier: ...
def DecoratedPot(
    **states: Unpack[DecoratedPotStates],
) -> Identifier | BlockDescriptor: ...
def Deepslate(**states: Unpack[DeepslateStates]) -> Identifier | BlockDescriptor: ...
def DeepslateBrickDoubleSlab(
    **states: Unpack[DeepslateBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateBrickSlab(
    **states: Unpack[DeepslateBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateBrickStairs(
    **states: Unpack[DeepslateBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateBrickWall(
    **states: Unpack[DeepslateBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateBricks() -> Identifier: ...
def DeepslateCoalOre() -> Identifier: ...
def DeepslateCopperOre() -> Identifier: ...
def DeepslateDiamondOre() -> Identifier: ...
def DeepslateEmeraldOre() -> Identifier: ...
def DeepslateGoldOre() -> Identifier: ...
def DeepslateIronOre() -> Identifier: ...
def DeepslateLapisOre() -> Identifier: ...
def DeepslateRedstoneOre() -> Identifier: ...
def DeepslateTileDoubleSlab(
    **states: Unpack[DeepslateTileDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateTileSlab(
    **states: Unpack[DeepslateTileSlabStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateTileStairs(
    **states: Unpack[DeepslateTileStairsStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateTileWall(
    **states: Unpack[DeepslateTileWallStates],
) -> Identifier | BlockDescriptor: ...
def DeepslateTiles() -> Identifier: ...
def Deny() -> Identifier: ...
def DetectorRail(
    **states: Unpack[DetectorRailStates],
) -> Identifier | BlockDescriptor: ...
def DiamondBlock() -> Identifier: ...
def DiamondOre() -> Identifier: ...
def Diorite() -> Identifier: ...
def DioriteDoubleSlab(
    **states: Unpack[DioriteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def DioriteSlab(
    **states: Unpack[DioriteSlabStates],
) -> Identifier | BlockDescriptor: ...
def DioriteStairs(
    **states: Unpack[DioriteStairsStates],
) -> Identifier | BlockDescriptor: ...
def DioriteWall(
    **states: Unpack[DioriteWallStates],
) -> Identifier | BlockDescriptor: ...
def Dirt() -> Identifier: ...
def DirtWithRoots() -> Identifier: ...
def Dispenser(**states: Unpack[DispenserStates]) -> Identifier | BlockDescriptor: ...
def DoubleCutCopperSlab(
    **states: Unpack[DoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def DragonEgg() -> Identifier: ...
def DragonHead(**states: Unpack[DragonHeadStates]) -> Identifier | BlockDescriptor: ...
def DriedGhast(**states: Unpack[DriedGhastStates]) -> Identifier | BlockDescriptor: ...
def DriedKelpBlock() -> Identifier: ...
def DripstoneBlock() -> Identifier: ...
def Dropper(**states: Unpack[DropperStates]) -> Identifier | BlockDescriptor: ...
def Element0() -> Identifier: ...
def Element1() -> Identifier: ...
def Element10() -> Identifier: ...
def Element100() -> Identifier: ...
def Element101() -> Identifier: ...
def Element102() -> Identifier: ...
def Element103() -> Identifier: ...
def Element104() -> Identifier: ...
def Element105() -> Identifier: ...
def Element106() -> Identifier: ...
def Element107() -> Identifier: ...
def Element108() -> Identifier: ...
def Element109() -> Identifier: ...
def Element11() -> Identifier: ...
def Element110() -> Identifier: ...
def Element111() -> Identifier: ...
def Element112() -> Identifier: ...
def Element113() -> Identifier: ...
def Element114() -> Identifier: ...
def Element115() -> Identifier: ...
def Element116() -> Identifier: ...
def Element117() -> Identifier: ...
def Element118() -> Identifier: ...
def Element12() -> Identifier: ...
def Element13() -> Identifier: ...
def Element14() -> Identifier: ...
def Element15() -> Identifier: ...
def Element16() -> Identifier: ...
def Element17() -> Identifier: ...
def Element18() -> Identifier: ...
def Element19() -> Identifier: ...
def Element2() -> Identifier: ...
def Element20() -> Identifier: ...
def Element21() -> Identifier: ...
def Element22() -> Identifier: ...
def Element23() -> Identifier: ...
def Element24() -> Identifier: ...
def Element25() -> Identifier: ...
def Element26() -> Identifier: ...
def Element27() -> Identifier: ...
def Element28() -> Identifier: ...
def Element29() -> Identifier: ...
def Element3() -> Identifier: ...
def Element30() -> Identifier: ...
def Element31() -> Identifier: ...
def Element32() -> Identifier: ...
def Element33() -> Identifier: ...
def Element34() -> Identifier: ...
def Element35() -> Identifier: ...
def Element36() -> Identifier: ...
def Element37() -> Identifier: ...
def Element38() -> Identifier: ...
def Element39() -> Identifier: ...
def Element4() -> Identifier: ...
def Element40() -> Identifier: ...
def Element41() -> Identifier: ...
def Element42() -> Identifier: ...
def Element43() -> Identifier: ...
def Element44() -> Identifier: ...
def Element45() -> Identifier: ...
def Element46() -> Identifier: ...
def Element47() -> Identifier: ...
def Element48() -> Identifier: ...
def Element49() -> Identifier: ...
def Element5() -> Identifier: ...
def Element50() -> Identifier: ...
def Element51() -> Identifier: ...
def Element52() -> Identifier: ...
def Element53() -> Identifier: ...
def Element54() -> Identifier: ...
def Element55() -> Identifier: ...
def Element56() -> Identifier: ...
def Element57() -> Identifier: ...
def Element58() -> Identifier: ...
def Element59() -> Identifier: ...
def Element6() -> Identifier: ...
def Element60() -> Identifier: ...
def Element61() -> Identifier: ...
def Element62() -> Identifier: ...
def Element63() -> Identifier: ...
def Element64() -> Identifier: ...
def Element65() -> Identifier: ...
def Element66() -> Identifier: ...
def Element67() -> Identifier: ...
def Element68() -> Identifier: ...
def Element69() -> Identifier: ...
def Element7() -> Identifier: ...
def Element70() -> Identifier: ...
def Element71() -> Identifier: ...
def Element72() -> Identifier: ...
def Element73() -> Identifier: ...
def Element74() -> Identifier: ...
def Element75() -> Identifier: ...
def Element76() -> Identifier: ...
def Element77() -> Identifier: ...
def Element78() -> Identifier: ...
def Element79() -> Identifier: ...
def Element8() -> Identifier: ...
def Element80() -> Identifier: ...
def Element81() -> Identifier: ...
def Element82() -> Identifier: ...
def Element83() -> Identifier: ...
def Element84() -> Identifier: ...
def Element85() -> Identifier: ...
def Element86() -> Identifier: ...
def Element87() -> Identifier: ...
def Element88() -> Identifier: ...
def Element89() -> Identifier: ...
def Element9() -> Identifier: ...
def Element90() -> Identifier: ...
def Element91() -> Identifier: ...
def Element92() -> Identifier: ...
def Element93() -> Identifier: ...
def Element94() -> Identifier: ...
def Element95() -> Identifier: ...
def Element96() -> Identifier: ...
def Element97() -> Identifier: ...
def Element98() -> Identifier: ...
def Element99() -> Identifier: ...
def ElementConstructor(
    **states: Unpack[ElementConstructorStates],
) -> Identifier | BlockDescriptor: ...
def EmeraldBlock() -> Identifier: ...
def EmeraldOre() -> Identifier: ...
def EnchantingTable() -> Identifier: ...
def EndBrickStairs(
    **states: Unpack[EndBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def EndBricks() -> Identifier: ...
def EndPortal() -> Identifier: ...
def EndPortalFrame(
    **states: Unpack[EndPortalFrameStates],
) -> Identifier | BlockDescriptor: ...
def EndRod(**states: Unpack[EndRodStates]) -> Identifier | BlockDescriptor: ...
def EndStone() -> Identifier: ...
def EndStoneBrickDoubleSlab(
    **states: Unpack[EndStoneBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def EndStoneBrickSlab(
    **states: Unpack[EndStoneBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def EndStoneBrickWall(
    **states: Unpack[EndStoneBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def EnderChest(**states: Unpack[EnderChestStates]) -> Identifier | BlockDescriptor: ...
def ExposedChiseledCopper() -> Identifier: ...
def ExposedCopper() -> Identifier: ...
def ExposedCopperBars(
    **states: Unpack[ExposedCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperBulb(
    **states: Unpack[ExposedCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperChain(
    **states: Unpack[ExposedCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperChest(
    **states: Unpack[ExposedCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperDoor(
    **states: Unpack[ExposedCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperGolemStatue(
    **states: Unpack[ExposedCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperGrate() -> Identifier: ...
def ExposedCopperLantern(
    **states: Unpack[ExposedCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCopperTrapdoor(
    **states: Unpack[ExposedCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCutCopper() -> Identifier: ...
def ExposedCutCopperSlab(
    **states: Unpack[ExposedCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def ExposedCutCopperStairs(
    **states: Unpack[ExposedCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def ExposedDoubleCutCopperSlab(
    **states: Unpack[ExposedDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def ExposedLightningRod(
    **states: Unpack[ExposedLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def Farmland(**states: Unpack[FarmlandStates]) -> Identifier | BlockDescriptor: ...
def FenceGate(**states: Unpack[FenceGateStates]) -> Identifier | BlockDescriptor: ...
def Fern() -> Identifier: ...
def Fire(**states: Unpack[FireStates]) -> Identifier | BlockDescriptor: ...
def FireCoral() -> Identifier: ...
def FireCoralBlock() -> Identifier: ...
def FireCoralFan(
    **states: Unpack[FireCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def FireCoralWallFan(
    **states: Unpack[FireCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def FireflyBush() -> Identifier: ...
def FletchingTable() -> Identifier: ...
def FlowerPot(**states: Unpack[FlowerPotStates]) -> Identifier | BlockDescriptor: ...
def FloweringAzalea() -> Identifier: ...
def FlowingLava(
    **states: Unpack[FlowingLavaStates],
) -> Identifier | BlockDescriptor: ...
def FlowingWater(
    **states: Unpack[FlowingWaterStates],
) -> Identifier | BlockDescriptor: ...
def Frame(**states: Unpack[FrameStates]) -> Identifier | BlockDescriptor: ...
def FrogSpawn() -> Identifier: ...
def FrostedIce(**states: Unpack[FrostedIceStates]) -> Identifier | BlockDescriptor: ...
def Furnace(**states: Unpack[FurnaceStates]) -> Identifier | BlockDescriptor: ...
def GildedBlackstone() -> Identifier: ...
def Glass() -> Identifier: ...
def GlassPane(**states: Unpack[GlassPaneStates]) -> Identifier | BlockDescriptor: ...
def GlowFrame(**states: Unpack[GlowFrameStates]) -> Identifier | BlockDescriptor: ...
def GlowLichen(**states: Unpack[GlowLichenStates]) -> Identifier | BlockDescriptor: ...
def Glowstone() -> Identifier: ...
def GoldBlock() -> Identifier: ...
def GoldOre() -> Identifier: ...
def GoldenDandelion() -> Identifier: ...
def GoldenRail(**states: Unpack[GoldenRailStates]) -> Identifier | BlockDescriptor: ...
def Granite() -> Identifier: ...
def GraniteDoubleSlab(
    **states: Unpack[GraniteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def GraniteSlab(
    **states: Unpack[GraniteSlabStates],
) -> Identifier | BlockDescriptor: ...
def GraniteStairs(
    **states: Unpack[GraniteStairsStates],
) -> Identifier | BlockDescriptor: ...
def GraniteWall(
    **states: Unpack[GraniteWallStates],
) -> Identifier | BlockDescriptor: ...
def GrassBlock() -> Identifier: ...
def GrassPath() -> Identifier: ...
def Gravel() -> Identifier: ...
def GrayCandle(**states: Unpack[GrayCandleStates]) -> Identifier | BlockDescriptor: ...
def GrayCandleCake(
    **states: Unpack[GrayCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def GrayCarpet() -> Identifier: ...
def GrayConcrete() -> Identifier: ...
def GrayConcreteDoubleSlab(
    **states: Unpack[GrayConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def GrayConcretePowder() -> Identifier: ...
def GrayConcreteSlab(
    **states: Unpack[GrayConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def GrayConcreteStairs(
    **states: Unpack[GrayConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def GrayGlazedTerracotta(
    **states: Unpack[GrayGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def GrayShulkerBox() -> Identifier: ...
def GrayStainedGlass() -> Identifier: ...
def GrayStainedGlassPane(
    **states: Unpack[GrayStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def GrayTerracotta() -> Identifier: ...
def GrayWool() -> Identifier: ...
def GrayWoolDoubleSlab(
    **states: Unpack[GrayWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def GrayWoolSlab(
    **states: Unpack[GrayWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def GrayWoolStairs(
    **states: Unpack[GrayWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def GreenCandle(
    **states: Unpack[GreenCandleStates],
) -> Identifier | BlockDescriptor: ...
def GreenCandleCake(
    **states: Unpack[GreenCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def GreenCarpet() -> Identifier: ...
def GreenConcrete() -> Identifier: ...
def GreenConcreteDoubleSlab(
    **states: Unpack[GreenConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def GreenConcretePowder() -> Identifier: ...
def GreenConcreteSlab(
    **states: Unpack[GreenConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def GreenConcreteStairs(
    **states: Unpack[GreenConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def GreenGlazedTerracotta(
    **states: Unpack[GreenGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def GreenShulkerBox() -> Identifier: ...
def GreenStainedGlass() -> Identifier: ...
def GreenStainedGlassPane(
    **states: Unpack[GreenStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def GreenTerracotta() -> Identifier: ...
def GreenWool() -> Identifier: ...
def GreenWoolDoubleSlab(
    **states: Unpack[GreenWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def GreenWoolSlab(
    **states: Unpack[GreenWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def GreenWoolStairs(
    **states: Unpack[GreenWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def Grindstone(**states: Unpack[GrindstoneStates]) -> Identifier | BlockDescriptor: ...
def HangingRoots() -> Identifier: ...
def HardBlackStainedGlass() -> Identifier: ...
def HardBlackStainedGlassPane(
    **states: Unpack[HardBlackStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardBlueStainedGlass() -> Identifier: ...
def HardBlueStainedGlassPane(
    **states: Unpack[HardBlueStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardBrownStainedGlass() -> Identifier: ...
def HardBrownStainedGlassPane(
    **states: Unpack[HardBrownStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardCyanStainedGlass() -> Identifier: ...
def HardCyanStainedGlassPane(
    **states: Unpack[HardCyanStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardGlass() -> Identifier: ...
def HardGlassPane(
    **states: Unpack[HardGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardGrayStainedGlass() -> Identifier: ...
def HardGrayStainedGlassPane(
    **states: Unpack[HardGrayStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardGreenStainedGlass() -> Identifier: ...
def HardGreenStainedGlassPane(
    **states: Unpack[HardGreenStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardLightBlueStainedGlass() -> Identifier: ...
def HardLightBlueStainedGlassPane(
    **states: Unpack[HardLightBlueStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardLightGrayStainedGlass() -> Identifier: ...
def HardLightGrayStainedGlassPane(
    **states: Unpack[HardLightGrayStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardLimeStainedGlass() -> Identifier: ...
def HardLimeStainedGlassPane(
    **states: Unpack[HardLimeStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardMagentaStainedGlass() -> Identifier: ...
def HardMagentaStainedGlassPane(
    **states: Unpack[HardMagentaStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardOrangeStainedGlass() -> Identifier: ...
def HardOrangeStainedGlassPane(
    **states: Unpack[HardOrangeStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardPinkStainedGlass() -> Identifier: ...
def HardPinkStainedGlassPane(
    **states: Unpack[HardPinkStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardPurpleStainedGlass() -> Identifier: ...
def HardPurpleStainedGlassPane(
    **states: Unpack[HardPurpleStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardRedStainedGlass() -> Identifier: ...
def HardRedStainedGlassPane(
    **states: Unpack[HardRedStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardWhiteStainedGlass() -> Identifier: ...
def HardWhiteStainedGlassPane(
    **states: Unpack[HardWhiteStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardYellowStainedGlass() -> Identifier: ...
def HardYellowStainedGlassPane(
    **states: Unpack[HardYellowStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def HardenedClay() -> Identifier: ...
def HayBlock(**states: Unpack[HayBlockStates]) -> Identifier | BlockDescriptor: ...
def HeavyCore() -> Identifier: ...
def HeavyWeightedPressurePlate(
    **states: Unpack[HeavyWeightedPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def HoneyBlock() -> Identifier: ...
def HoneycombBlock() -> Identifier: ...
def Hopper(**states: Unpack[HopperStates]) -> Identifier | BlockDescriptor: ...
def HornCoral() -> Identifier: ...
def HornCoralBlock() -> Identifier: ...
def HornCoralFan(
    **states: Unpack[HornCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def HornCoralWallFan(
    **states: Unpack[HornCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def Ice() -> Identifier: ...
def InfestedChiseledStoneBricks() -> Identifier: ...
def InfestedCobblestone() -> Identifier: ...
def InfestedCrackedStoneBricks() -> Identifier: ...
def InfestedDeepslate(
    **states: Unpack[InfestedDeepslateStates],
) -> Identifier | BlockDescriptor: ...
def InfestedMossyStoneBricks() -> Identifier: ...
def InfestedStone() -> Identifier: ...
def InfestedStoneBricks() -> Identifier: ...
def IronBars(**states: Unpack[IronBarsStates]) -> Identifier | BlockDescriptor: ...
def IronBlock() -> Identifier: ...
def IronChain(**states: Unpack[IronChainStates]) -> Identifier | BlockDescriptor: ...
def IronDoor(**states: Unpack[IronDoorStates]) -> Identifier | BlockDescriptor: ...
def IronOre() -> Identifier: ...
def IronTrapdoor(
    **states: Unpack[IronTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def Jigsaw(**states: Unpack[JigsawStates]) -> Identifier | BlockDescriptor: ...
def Jukebox() -> Identifier: ...
def JungleButton(
    **states: Unpack[JungleButtonStates],
) -> Identifier | BlockDescriptor: ...
def JungleDoor(**states: Unpack[JungleDoorStates]) -> Identifier | BlockDescriptor: ...
def JungleDoubleSlab(
    **states: Unpack[JungleDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def JungleFence(
    **states: Unpack[JungleFenceStates],
) -> Identifier | BlockDescriptor: ...
def JungleFenceGate(
    **states: Unpack[JungleFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def JungleHangingSign(
    **states: Unpack[JungleHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def JungleLeaves(
    **states: Unpack[JungleLeavesStates],
) -> Identifier | BlockDescriptor: ...
def JungleLog(**states: Unpack[JungleLogStates]) -> Identifier | BlockDescriptor: ...
def JunglePlanks() -> Identifier: ...
def JunglePressurePlate(
    **states: Unpack[JunglePressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def JungleSapling(
    **states: Unpack[JungleSaplingStates],
) -> Identifier | BlockDescriptor: ...
def JungleShelf(
    **states: Unpack[JungleShelfStates],
) -> Identifier | BlockDescriptor: ...
def JungleSlab(**states: Unpack[JungleSlabStates]) -> Identifier | BlockDescriptor: ...
def JungleStairs(
    **states: Unpack[JungleStairsStates],
) -> Identifier | BlockDescriptor: ...
def JungleStandingSign(
    **states: Unpack[JungleStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def JungleTrapdoor(
    **states: Unpack[JungleTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def JungleWallSign(
    **states: Unpack[JungleWallSignStates],
) -> Identifier | BlockDescriptor: ...
def JungleWood(**states: Unpack[JungleWoodStates]) -> Identifier | BlockDescriptor: ...
def Kelp(**states: Unpack[KelpStates]) -> Identifier | BlockDescriptor: ...
def LabTable(**states: Unpack[LabTableStates]) -> Identifier | BlockDescriptor: ...
def Ladder(**states: Unpack[LadderStates]) -> Identifier | BlockDescriptor: ...
def Lantern(**states: Unpack[LanternStates]) -> Identifier | BlockDescriptor: ...
def LapisBlock() -> Identifier: ...
def LapisOre() -> Identifier: ...
def LargeAmethystBud(
    **states: Unpack[LargeAmethystBudStates],
) -> Identifier | BlockDescriptor: ...
def LargeFern(**states: Unpack[LargeFernStates]) -> Identifier | BlockDescriptor: ...
def Lava(**states: Unpack[LavaStates]) -> Identifier | BlockDescriptor: ...
def LeafLitter(**states: Unpack[LeafLitterStates]) -> Identifier | BlockDescriptor: ...
def Lectern(**states: Unpack[LecternStates]) -> Identifier | BlockDescriptor: ...
def Lever(**states: Unpack[LeverStates]) -> Identifier | BlockDescriptor: ...
def LightBlock0() -> Identifier: ...
def LightBlock1() -> Identifier: ...
def LightBlock10() -> Identifier: ...
def LightBlock11() -> Identifier: ...
def LightBlock12() -> Identifier: ...
def LightBlock13() -> Identifier: ...
def LightBlock14() -> Identifier: ...
def LightBlock15() -> Identifier: ...
def LightBlock2() -> Identifier: ...
def LightBlock3() -> Identifier: ...
def LightBlock4() -> Identifier: ...
def LightBlock5() -> Identifier: ...
def LightBlock6() -> Identifier: ...
def LightBlock7() -> Identifier: ...
def LightBlock8() -> Identifier: ...
def LightBlock9() -> Identifier: ...
def LightBlueCandle(
    **states: Unpack[LightBlueCandleStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueCandleCake(
    **states: Unpack[LightBlueCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueCarpet() -> Identifier: ...
def LightBlueConcrete() -> Identifier: ...
def LightBlueConcreteDoubleSlab(
    **states: Unpack[LightBlueConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueConcretePowder() -> Identifier: ...
def LightBlueConcreteSlab(
    **states: Unpack[LightBlueConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueConcreteStairs(
    **states: Unpack[LightBlueConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueGlazedTerracotta(
    **states: Unpack[LightBlueGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueShulkerBox() -> Identifier: ...
def LightBlueStainedGlass() -> Identifier: ...
def LightBlueStainedGlassPane(
    **states: Unpack[LightBlueStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueTerracotta() -> Identifier: ...
def LightBlueWool() -> Identifier: ...
def LightBlueWoolDoubleSlab(
    **states: Unpack[LightBlueWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueWoolSlab(
    **states: Unpack[LightBlueWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightBlueWoolStairs(
    **states: Unpack[LightBlueWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayCandle(
    **states: Unpack[LightGrayCandleStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayCandleCake(
    **states: Unpack[LightGrayCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayCarpet() -> Identifier: ...
def LightGrayConcrete() -> Identifier: ...
def LightGrayConcreteDoubleSlab(
    **states: Unpack[LightGrayConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayConcretePowder() -> Identifier: ...
def LightGrayConcreteSlab(
    **states: Unpack[LightGrayConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayConcreteStairs(
    **states: Unpack[LightGrayConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayShulkerBox() -> Identifier: ...
def LightGrayStainedGlass() -> Identifier: ...
def LightGrayStainedGlassPane(
    **states: Unpack[LightGrayStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayTerracotta() -> Identifier: ...
def LightGrayWool() -> Identifier: ...
def LightGrayWoolDoubleSlab(
    **states: Unpack[LightGrayWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayWoolSlab(
    **states: Unpack[LightGrayWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def LightGrayWoolStairs(
    **states: Unpack[LightGrayWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def LightWeightedPressurePlate(
    **states: Unpack[LightWeightedPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def LightningRod(
    **states: Unpack[LightningRodStates],
) -> Identifier | BlockDescriptor: ...
def Lilac(**states: Unpack[LilacStates]) -> Identifier | BlockDescriptor: ...
def LilyOfTheValley() -> Identifier: ...
def LimeCandle(**states: Unpack[LimeCandleStates]) -> Identifier | BlockDescriptor: ...
def LimeCandleCake(
    **states: Unpack[LimeCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def LimeCarpet() -> Identifier: ...
def LimeConcrete() -> Identifier: ...
def LimeConcreteDoubleSlab(
    **states: Unpack[LimeConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def LimeConcretePowder() -> Identifier: ...
def LimeConcreteSlab(
    **states: Unpack[LimeConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def LimeConcreteStairs(
    **states: Unpack[LimeConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def LimeGlazedTerracotta(
    **states: Unpack[LimeGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def LimeShulkerBox() -> Identifier: ...
def LimeStainedGlass() -> Identifier: ...
def LimeStainedGlassPane(
    **states: Unpack[LimeStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def LimeTerracotta() -> Identifier: ...
def LimeWool() -> Identifier: ...
def LimeWoolDoubleSlab(
    **states: Unpack[LimeWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def LimeWoolSlab(
    **states: Unpack[LimeWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def LimeWoolStairs(
    **states: Unpack[LimeWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def LitBlastFurnace(
    **states: Unpack[LitBlastFurnaceStates],
) -> Identifier | BlockDescriptor: ...
def LitDeepslateRedstoneOre() -> Identifier: ...
def LitFurnace(**states: Unpack[LitFurnaceStates]) -> Identifier | BlockDescriptor: ...
def LitPumpkin(**states: Unpack[LitPumpkinStates]) -> Identifier | BlockDescriptor: ...
def LitRedstoneLamp() -> Identifier: ...
def LitRedstoneOre() -> Identifier: ...
def LitSmoker(**states: Unpack[LitSmokerStates]) -> Identifier | BlockDescriptor: ...
def Lodestone() -> Identifier: ...
def Loom(**states: Unpack[LoomStates]) -> Identifier | BlockDescriptor: ...
def MagentaCandle(
    **states: Unpack[MagentaCandleStates],
) -> Identifier | BlockDescriptor: ...
def MagentaCandleCake(
    **states: Unpack[MagentaCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def MagentaCarpet() -> Identifier: ...
def MagentaConcrete() -> Identifier: ...
def MagentaConcreteDoubleSlab(
    **states: Unpack[MagentaConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def MagentaConcretePowder() -> Identifier: ...
def MagentaConcreteSlab(
    **states: Unpack[MagentaConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def MagentaConcreteStairs(
    **states: Unpack[MagentaConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def MagentaGlazedTerracotta(
    **states: Unpack[MagentaGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def MagentaShulkerBox() -> Identifier: ...
def MagentaStainedGlass() -> Identifier: ...
def MagentaStainedGlassPane(
    **states: Unpack[MagentaStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def MagentaTerracotta() -> Identifier: ...
def MagentaWool() -> Identifier: ...
def MagentaWoolDoubleSlab(
    **states: Unpack[MagentaWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def MagentaWoolSlab(
    **states: Unpack[MagentaWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def MagentaWoolStairs(
    **states: Unpack[MagentaWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def Magma() -> Identifier: ...
def MangroveButton(
    **states: Unpack[MangroveButtonStates],
) -> Identifier | BlockDescriptor: ...
def MangroveDoor(
    **states: Unpack[MangroveDoorStates],
) -> Identifier | BlockDescriptor: ...
def MangroveDoubleSlab(
    **states: Unpack[MangroveDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def MangroveFence(
    **states: Unpack[MangroveFenceStates],
) -> Identifier | BlockDescriptor: ...
def MangroveFenceGate(
    **states: Unpack[MangroveFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def MangroveHangingSign(
    **states: Unpack[MangroveHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def MangroveLeaves(
    **states: Unpack[MangroveLeavesStates],
) -> Identifier | BlockDescriptor: ...
def MangroveLog(
    **states: Unpack[MangroveLogStates],
) -> Identifier | BlockDescriptor: ...
def MangrovePlanks() -> Identifier: ...
def MangrovePressurePlate(
    **states: Unpack[MangrovePressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def MangrovePropagule(
    **states: Unpack[MangrovePropaguleStates],
) -> Identifier | BlockDescriptor: ...
def MangroveRoots() -> Identifier: ...
def MangroveShelf(
    **states: Unpack[MangroveShelfStates],
) -> Identifier | BlockDescriptor: ...
def MangroveSlab(
    **states: Unpack[MangroveSlabStates],
) -> Identifier | BlockDescriptor: ...
def MangroveStairs(
    **states: Unpack[MangroveStairsStates],
) -> Identifier | BlockDescriptor: ...
def MangroveStandingSign(
    **states: Unpack[MangroveStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def MangroveTrapdoor(
    **states: Unpack[MangroveTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def MangroveWallSign(
    **states: Unpack[MangroveWallSignStates],
) -> Identifier | BlockDescriptor: ...
def MangroveWood(
    **states: Unpack[MangroveWoodStates],
) -> Identifier | BlockDescriptor: ...
def MaterialReducer(
    **states: Unpack[MaterialReducerStates],
) -> Identifier | BlockDescriptor: ...
def MediumAmethystBud(
    **states: Unpack[MediumAmethystBudStates],
) -> Identifier | BlockDescriptor: ...
def MelonBlock() -> Identifier: ...
def MelonStem(**states: Unpack[MelonStemStates]) -> Identifier | BlockDescriptor: ...
def MobSpawner() -> Identifier: ...
def MossBlock() -> Identifier: ...
def MossCarpet() -> Identifier: ...
def MossyCobblestone() -> Identifier: ...
def MossyCobblestoneDoubleSlab(
    **states: Unpack[MossyCobblestoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def MossyCobblestoneSlab(
    **states: Unpack[MossyCobblestoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def MossyCobblestoneStairs(
    **states: Unpack[MossyCobblestoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def MossyCobblestoneWall(
    **states: Unpack[MossyCobblestoneWallStates],
) -> Identifier | BlockDescriptor: ...
def MossyStoneBrickDoubleSlab(
    **states: Unpack[MossyStoneBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def MossyStoneBrickSlab(
    **states: Unpack[MossyStoneBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def MossyStoneBrickStairs(
    **states: Unpack[MossyStoneBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def MossyStoneBrickWall(
    **states: Unpack[MossyStoneBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def MossyStoneBricks() -> Identifier: ...
def Mud() -> Identifier: ...
def MudBrickDoubleSlab(
    **states: Unpack[MudBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def MudBrickSlab(
    **states: Unpack[MudBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def MudBrickStairs(
    **states: Unpack[MudBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def MudBrickWall(
    **states: Unpack[MudBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def MudBricks() -> Identifier: ...
def MuddyMangroveRoots(
    **states: Unpack[MuddyMangroveRootsStates],
) -> Identifier | BlockDescriptor: ...
def MushroomStem(
    **states: Unpack[MushroomStemStates],
) -> Identifier | BlockDescriptor: ...
def Mycelium() -> Identifier: ...
def NetherBrick() -> Identifier: ...
def NetherBrickDoubleSlab(
    **states: Unpack[NetherBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def NetherBrickFence(
    **states: Unpack[NetherBrickFenceStates],
) -> Identifier | BlockDescriptor: ...
def NetherBrickSlab(
    **states: Unpack[NetherBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def NetherBrickStairs(
    **states: Unpack[NetherBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def NetherBrickWall(
    **states: Unpack[NetherBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def NetherGoldOre() -> Identifier: ...
def NetherSprouts() -> Identifier: ...
def NetherWart(**states: Unpack[NetherWartStates]) -> Identifier | BlockDescriptor: ...
def NetherWartBlock() -> Identifier: ...
def NetheriteBlock() -> Identifier: ...
def Netherrack() -> Identifier: ...
def NormalStoneDoubleSlab(
    **states: Unpack[NormalStoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def NormalStoneSlab(
    **states: Unpack[NormalStoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def NormalStoneStairs(
    **states: Unpack[NormalStoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def Noteblock() -> Identifier: ...
def OakDoubleSlab(
    **states: Unpack[OakDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def OakFence(**states: Unpack[OakFenceStates]) -> Identifier | BlockDescriptor: ...
def OakHangingSign(
    **states: Unpack[OakHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def OakLeaves(**states: Unpack[OakLeavesStates]) -> Identifier | BlockDescriptor: ...
def OakLog(**states: Unpack[OakLogStates]) -> Identifier | BlockDescriptor: ...
def OakPlanks() -> Identifier: ...
def OakSapling(**states: Unpack[OakSaplingStates]) -> Identifier | BlockDescriptor: ...
def OakShelf(**states: Unpack[OakShelfStates]) -> Identifier | BlockDescriptor: ...
def OakSlab(**states: Unpack[OakSlabStates]) -> Identifier | BlockDescriptor: ...
def OakStairs(**states: Unpack[OakStairsStates]) -> Identifier | BlockDescriptor: ...
def OakWood(**states: Unpack[OakWoodStates]) -> Identifier | BlockDescriptor: ...
def Observer(**states: Unpack[ObserverStates]) -> Identifier | BlockDescriptor: ...
def Obsidian() -> Identifier: ...
def OchreFroglight(
    **states: Unpack[OchreFroglightStates],
) -> Identifier | BlockDescriptor: ...
def OpenEyeblossom() -> Identifier: ...
def OrangeCandle(
    **states: Unpack[OrangeCandleStates],
) -> Identifier | BlockDescriptor: ...
def OrangeCandleCake(
    **states: Unpack[OrangeCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def OrangeCarpet() -> Identifier: ...
def OrangeConcrete() -> Identifier: ...
def OrangeConcreteDoubleSlab(
    **states: Unpack[OrangeConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def OrangeConcretePowder() -> Identifier: ...
def OrangeConcreteSlab(
    **states: Unpack[OrangeConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def OrangeConcreteStairs(
    **states: Unpack[OrangeConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def OrangeGlazedTerracotta(
    **states: Unpack[OrangeGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def OrangePoplarLeaves(
    **states: Unpack[OrangePoplarLeavesStates],
) -> Identifier | BlockDescriptor: ...
def OrangeShulkerBox() -> Identifier: ...
def OrangeStainedGlass() -> Identifier: ...
def OrangeStainedGlassPane(
    **states: Unpack[OrangeStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def OrangeTerracotta() -> Identifier: ...
def OrangeTulip() -> Identifier: ...
def OrangeWool() -> Identifier: ...
def OrangeWoolDoubleSlab(
    **states: Unpack[OrangeWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def OrangeWoolSlab(
    **states: Unpack[OrangeWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def OrangeWoolStairs(
    **states: Unpack[OrangeWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def OxeyeDaisy() -> Identifier: ...
def OxidizedChiseledCopper() -> Identifier: ...
def OxidizedCopper() -> Identifier: ...
def OxidizedCopperBars(
    **states: Unpack[OxidizedCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperBulb(
    **states: Unpack[OxidizedCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperChain(
    **states: Unpack[OxidizedCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperChest(
    **states: Unpack[OxidizedCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperDoor(
    **states: Unpack[OxidizedCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperGolemStatue(
    **states: Unpack[OxidizedCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperGrate() -> Identifier: ...
def OxidizedCopperLantern(
    **states: Unpack[OxidizedCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCopperTrapdoor(
    **states: Unpack[OxidizedCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCutCopper() -> Identifier: ...
def OxidizedCutCopperSlab(
    **states: Unpack[OxidizedCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedCutCopperStairs(
    **states: Unpack[OxidizedCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedDoubleCutCopperSlab(
    **states: Unpack[OxidizedDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def OxidizedLightningRod(
    **states: Unpack[OxidizedLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def PackedIce() -> Identifier: ...
def PackedMud() -> Identifier: ...
def PaleHangingMoss(
    **states: Unpack[PaleHangingMossStates],
) -> Identifier | BlockDescriptor: ...
def PaleMossBlock() -> Identifier: ...
def PaleMossCarpet(
    **states: Unpack[PaleMossCarpetStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakButton(
    **states: Unpack[PaleOakButtonStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakDoor(
    **states: Unpack[PaleOakDoorStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakDoubleSlab(
    **states: Unpack[PaleOakDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakFence(
    **states: Unpack[PaleOakFenceStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakFenceGate(
    **states: Unpack[PaleOakFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakHangingSign(
    **states: Unpack[PaleOakHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakLeaves(
    **states: Unpack[PaleOakLeavesStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakLog(**states: Unpack[PaleOakLogStates]) -> Identifier | BlockDescriptor: ...
def PaleOakPlanks() -> Identifier: ...
def PaleOakPressurePlate(
    **states: Unpack[PaleOakPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakSapling(
    **states: Unpack[PaleOakSaplingStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakShelf(
    **states: Unpack[PaleOakShelfStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakSlab(
    **states: Unpack[PaleOakSlabStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakStairs(
    **states: Unpack[PaleOakStairsStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakStandingSign(
    **states: Unpack[PaleOakStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakTrapdoor(
    **states: Unpack[PaleOakTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakWallSign(
    **states: Unpack[PaleOakWallSignStates],
) -> Identifier | BlockDescriptor: ...
def PaleOakWood(
    **states: Unpack[PaleOakWoodStates],
) -> Identifier | BlockDescriptor: ...
def PearlescentFroglight(
    **states: Unpack[PearlescentFroglightStates],
) -> Identifier | BlockDescriptor: ...
def Peony(**states: Unpack[PeonyStates]) -> Identifier | BlockDescriptor: ...
def PetrifiedOakDoubleSlab(
    **states: Unpack[PetrifiedOakDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PetrifiedOakSlab(
    **states: Unpack[PetrifiedOakSlabStates],
) -> Identifier | BlockDescriptor: ...
def PiglinHead(**states: Unpack[PiglinHeadStates]) -> Identifier | BlockDescriptor: ...
def PinkCandle(**states: Unpack[PinkCandleStates]) -> Identifier | BlockDescriptor: ...
def PinkCandleCake(
    **states: Unpack[PinkCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def PinkCarpet() -> Identifier: ...
def PinkConcrete() -> Identifier: ...
def PinkConcreteDoubleSlab(
    **states: Unpack[PinkConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PinkConcretePowder() -> Identifier: ...
def PinkConcreteSlab(
    **states: Unpack[PinkConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def PinkConcreteStairs(
    **states: Unpack[PinkConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def PinkGlazedTerracotta(
    **states: Unpack[PinkGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def PinkPetals(**states: Unpack[PinkPetalsStates]) -> Identifier | BlockDescriptor: ...
def PinkShulkerBox() -> Identifier: ...
def PinkStainedGlass() -> Identifier: ...
def PinkStainedGlassPane(
    **states: Unpack[PinkStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def PinkTerracotta() -> Identifier: ...
def PinkTulip() -> Identifier: ...
def PinkWool() -> Identifier: ...
def PinkWoolDoubleSlab(
    **states: Unpack[PinkWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PinkWoolSlab(
    **states: Unpack[PinkWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def PinkWoolStairs(
    **states: Unpack[PinkWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def Piston(**states: Unpack[PistonStates]) -> Identifier | BlockDescriptor: ...
def PistonArmCollision(
    **states: Unpack[PistonArmCollisionStates],
) -> Identifier | BlockDescriptor: ...
def PitcherCrop(
    **states: Unpack[PitcherCropStates],
) -> Identifier | BlockDescriptor: ...
def PitcherPlant(
    **states: Unpack[PitcherPlantStates],
) -> Identifier | BlockDescriptor: ...
def PlayerHead(**states: Unpack[PlayerHeadStates]) -> Identifier | BlockDescriptor: ...
def Podzol() -> Identifier: ...
def PointedDripstone(
    **states: Unpack[PointedDripstoneStates],
) -> Identifier | BlockDescriptor: ...
def PolishedAndesite() -> Identifier: ...
def PolishedAndesiteDoubleSlab(
    **states: Unpack[PolishedAndesiteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedAndesiteSlab(
    **states: Unpack[PolishedAndesiteSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedAndesiteStairs(
    **states: Unpack[PolishedAndesiteStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBasalt(
    **states: Unpack[PolishedBasaltStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstone() -> Identifier: ...
def PolishedBlackstoneBrickDoubleSlab(
    **states: Unpack[PolishedBlackstoneBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneBrickSlab(
    **states: Unpack[PolishedBlackstoneBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneBrickStairs(
    **states: Unpack[PolishedBlackstoneBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneBrickWall(
    **states: Unpack[PolishedBlackstoneBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneBricks() -> Identifier: ...
def PolishedBlackstoneButton(
    **states: Unpack[PolishedBlackstoneButtonStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneDoubleSlab(
    **states: Unpack[PolishedBlackstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstonePressurePlate(
    **states: Unpack[PolishedBlackstonePressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneSlab(
    **states: Unpack[PolishedBlackstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneStairs(
    **states: Unpack[PolishedBlackstoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedBlackstoneWall(
    **states: Unpack[PolishedBlackstoneWallStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCinnabar() -> Identifier: ...
def PolishedCinnabarDoubleSlab(
    **states: Unpack[PolishedCinnabarDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCinnabarSlab(
    **states: Unpack[PolishedCinnabarSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCinnabarStairs(
    **states: Unpack[PolishedCinnabarStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedCinnabarWall(
    **states: Unpack[PolishedCinnabarWallStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDeepslate() -> Identifier: ...
def PolishedDeepslateDoubleSlab(
    **states: Unpack[PolishedDeepslateDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDeepslateSlab(
    **states: Unpack[PolishedDeepslateSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDeepslateStairs(
    **states: Unpack[PolishedDeepslateStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDeepslateWall(
    **states: Unpack[PolishedDeepslateWallStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDiorite() -> Identifier: ...
def PolishedDioriteDoubleSlab(
    **states: Unpack[PolishedDioriteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDioriteSlab(
    **states: Unpack[PolishedDioriteSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedDioriteStairs(
    **states: Unpack[PolishedDioriteStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedGranite() -> Identifier: ...
def PolishedGraniteDoubleSlab(
    **states: Unpack[PolishedGraniteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedGraniteSlab(
    **states: Unpack[PolishedGraniteSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedGraniteStairs(
    **states: Unpack[PolishedGraniteStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedSulfur() -> Identifier: ...
def PolishedSulfurDoubleSlab(
    **states: Unpack[PolishedSulfurDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedSulfurSlab(
    **states: Unpack[PolishedSulfurSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedSulfurStairs(
    **states: Unpack[PolishedSulfurStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedSulfurWall(
    **states: Unpack[PolishedSulfurWallStates],
) -> Identifier | BlockDescriptor: ...
def PolishedTuff() -> Identifier: ...
def PolishedTuffDoubleSlab(
    **states: Unpack[PolishedTuffDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedTuffSlab(
    **states: Unpack[PolishedTuffSlabStates],
) -> Identifier | BlockDescriptor: ...
def PolishedTuffStairs(
    **states: Unpack[PolishedTuffStairsStates],
) -> Identifier | BlockDescriptor: ...
def PolishedTuffWall(
    **states: Unpack[PolishedTuffWallStates],
) -> Identifier | BlockDescriptor: ...
def PoplarButton(
    **states: Unpack[PoplarButtonStates],
) -> Identifier | BlockDescriptor: ...
def PoplarDoor(**states: Unpack[PoplarDoorStates]) -> Identifier | BlockDescriptor: ...
def PoplarDoubleSlab(
    **states: Unpack[PoplarDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PoplarFence(
    **states: Unpack[PoplarFenceStates],
) -> Identifier | BlockDescriptor: ...
def PoplarFenceGate(
    **states: Unpack[PoplarFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def PoplarHangingSign(
    **states: Unpack[PoplarHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def PoplarLog(**states: Unpack[PoplarLogStates]) -> Identifier | BlockDescriptor: ...
def PoplarPlanks() -> Identifier: ...
def PoplarPressurePlate(
    **states: Unpack[PoplarPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def PoplarSapling(
    **states: Unpack[PoplarSaplingStates],
) -> Identifier | BlockDescriptor: ...
def PoplarShelf(
    **states: Unpack[PoplarShelfStates],
) -> Identifier | BlockDescriptor: ...
def PoplarSlab(**states: Unpack[PoplarSlabStates]) -> Identifier | BlockDescriptor: ...
def PoplarStairs(
    **states: Unpack[PoplarStairsStates],
) -> Identifier | BlockDescriptor: ...
def PoplarStandingSign(
    **states: Unpack[PoplarStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def PoplarTrapdoor(
    **states: Unpack[PoplarTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def PoplarWallSign(
    **states: Unpack[PoplarWallSignStates],
) -> Identifier | BlockDescriptor: ...
def PoplarWood(**states: Unpack[PoplarWoodStates]) -> Identifier | BlockDescriptor: ...
def Poppy() -> Identifier: ...
def Portal(**states: Unpack[PortalStates]) -> Identifier | BlockDescriptor: ...
def Potatoes(**states: Unpack[PotatoesStates]) -> Identifier | BlockDescriptor: ...
def PotentSulfur(
    **states: Unpack[PotentSulfurStates],
) -> Identifier | BlockDescriptor: ...
def PowderSnow() -> Identifier: ...
def PoweredComparator(
    **states: Unpack[PoweredComparatorStates],
) -> Identifier | BlockDescriptor: ...
def PoweredRepeater(
    **states: Unpack[PoweredRepeaterStates],
) -> Identifier | BlockDescriptor: ...
def Prismarine() -> Identifier: ...
def PrismarineBrickDoubleSlab(
    **states: Unpack[PrismarineBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PrismarineBrickSlab(
    **states: Unpack[PrismarineBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def PrismarineBricks() -> Identifier: ...
def PrismarineBricksStairs(
    **states: Unpack[PrismarineBricksStairsStates],
) -> Identifier | BlockDescriptor: ...
def PrismarineDoubleSlab(
    **states: Unpack[PrismarineDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PrismarineSlab(
    **states: Unpack[PrismarineSlabStates],
) -> Identifier | BlockDescriptor: ...
def PrismarineStairs(
    **states: Unpack[PrismarineStairsStates],
) -> Identifier | BlockDescriptor: ...
def PrismarineWall(
    **states: Unpack[PrismarineWallStates],
) -> Identifier | BlockDescriptor: ...
def Pumpkin(**states: Unpack[PumpkinStates]) -> Identifier | BlockDescriptor: ...
def PumpkinStem(
    **states: Unpack[PumpkinStemStates],
) -> Identifier | BlockDescriptor: ...
def PurpleCandle(
    **states: Unpack[PurpleCandleStates],
) -> Identifier | BlockDescriptor: ...
def PurpleCandleCake(
    **states: Unpack[PurpleCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def PurpleCarpet() -> Identifier: ...
def PurpleConcrete() -> Identifier: ...
def PurpleConcreteDoubleSlab(
    **states: Unpack[PurpleConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PurpleConcretePowder() -> Identifier: ...
def PurpleConcreteSlab(
    **states: Unpack[PurpleConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def PurpleConcreteStairs(
    **states: Unpack[PurpleConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def PurpleGlazedTerracotta(
    **states: Unpack[PurpleGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def PurpleShulkerBox() -> Identifier: ...
def PurpleStainedGlass() -> Identifier: ...
def PurpleStainedGlassPane(
    **states: Unpack[PurpleStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def PurpleTerracotta() -> Identifier: ...
def PurpleWool() -> Identifier: ...
def PurpleWoolDoubleSlab(
    **states: Unpack[PurpleWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PurpleWoolSlab(
    **states: Unpack[PurpleWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def PurpleWoolStairs(
    **states: Unpack[PurpleWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def PurpurBlock(
    **states: Unpack[PurpurBlockStates],
) -> Identifier | BlockDescriptor: ...
def PurpurDoubleSlab(
    **states: Unpack[PurpurDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def PurpurPillar(
    **states: Unpack[PurpurPillarStates],
) -> Identifier | BlockDescriptor: ...
def PurpurSlab(**states: Unpack[PurpurSlabStates]) -> Identifier | BlockDescriptor: ...
def PurpurStairs(
    **states: Unpack[PurpurStairsStates],
) -> Identifier | BlockDescriptor: ...
def QuartzBlock(
    **states: Unpack[QuartzBlockStates],
) -> Identifier | BlockDescriptor: ...
def QuartzBricks() -> Identifier: ...
def QuartzDoubleSlab(
    **states: Unpack[QuartzDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def QuartzOre() -> Identifier: ...
def QuartzPillar(
    **states: Unpack[QuartzPillarStates],
) -> Identifier | BlockDescriptor: ...
def QuartzSlab(**states: Unpack[QuartzSlabStates]) -> Identifier | BlockDescriptor: ...
def QuartzStairs(
    **states: Unpack[QuartzStairsStates],
) -> Identifier | BlockDescriptor: ...
def Rail(**states: Unpack[RailStates]) -> Identifier | BlockDescriptor: ...
def RawCopperBlock() -> Identifier: ...
def RawGoldBlock() -> Identifier: ...
def RawIronBlock() -> Identifier: ...
def RedCandle(**states: Unpack[RedCandleStates]) -> Identifier | BlockDescriptor: ...
def RedCandleCake(
    **states: Unpack[RedCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def RedCarpet() -> Identifier: ...
def RedConcrete() -> Identifier: ...
def RedConcreteDoubleSlab(
    **states: Unpack[RedConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedConcretePowder() -> Identifier: ...
def RedConcreteSlab(
    **states: Unpack[RedConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedConcreteStairs(
    **states: Unpack[RedConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def RedGlazedTerracotta(
    **states: Unpack[RedGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def RedMushroom() -> Identifier: ...
def RedMushroomBlock(
    **states: Unpack[RedMushroomBlockStates],
) -> Identifier | BlockDescriptor: ...
def RedNetherBrick() -> Identifier: ...
def RedNetherBrickDoubleSlab(
    **states: Unpack[RedNetherBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedNetherBrickSlab(
    **states: Unpack[RedNetherBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedNetherBrickStairs(
    **states: Unpack[RedNetherBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def RedNetherBrickWall(
    **states: Unpack[RedNetherBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def RedPoplarLeaves(
    **states: Unpack[RedPoplarLeavesStates],
) -> Identifier | BlockDescriptor: ...
def RedSand() -> Identifier: ...
def RedSandstone() -> Identifier: ...
def RedSandstoneDoubleSlab(
    **states: Unpack[RedSandstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedSandstoneSlab(
    **states: Unpack[RedSandstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedSandstoneStairs(
    **states: Unpack[RedSandstoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def RedSandstoneWall(
    **states: Unpack[RedSandstoneWallStates],
) -> Identifier | BlockDescriptor: ...
def RedShrub() -> Identifier: ...
def RedShulkerBox() -> Identifier: ...
def RedStainedGlass() -> Identifier: ...
def RedStainedGlassPane(
    **states: Unpack[RedStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def RedTerracotta() -> Identifier: ...
def RedTulip() -> Identifier: ...
def RedWool() -> Identifier: ...
def RedWoolDoubleSlab(
    **states: Unpack[RedWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedWoolSlab(
    **states: Unpack[RedWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def RedWoolStairs(
    **states: Unpack[RedWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def RedstoneBlock() -> Identifier: ...
def RedstoneLamp() -> Identifier: ...
def RedstoneOre() -> Identifier: ...
def RedstoneTorch(
    **states: Unpack[RedstoneTorchStates],
) -> Identifier | BlockDescriptor: ...
def RedstoneWire(
    **states: Unpack[RedstoneWireStates],
) -> Identifier | BlockDescriptor: ...
def Reeds(**states: Unpack[ReedsStates]) -> Identifier | BlockDescriptor: ...
def ReinforcedDeepslate() -> Identifier: ...
def RepeatingCommandBlock(
    **states: Unpack[RepeatingCommandBlockStates],
) -> Identifier | BlockDescriptor: ...
def ResinBlock() -> Identifier: ...
def ResinBrickDoubleSlab(
    **states: Unpack[ResinBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def ResinBrickSlab(
    **states: Unpack[ResinBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def ResinBrickStairs(
    **states: Unpack[ResinBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def ResinBrickWall(
    **states: Unpack[ResinBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def ResinBricks() -> Identifier: ...
def ResinClump(**states: Unpack[ResinClumpStates]) -> Identifier | BlockDescriptor: ...
def RespawnAnchor(
    **states: Unpack[RespawnAnchorStates],
) -> Identifier | BlockDescriptor: ...
def RoseBush(**states: Unpack[RoseBushStates]) -> Identifier | BlockDescriptor: ...
def Sand() -> Identifier: ...
def Sandstone() -> Identifier: ...
def SandstoneDoubleSlab(
    **states: Unpack[SandstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SandstoneSlab(
    **states: Unpack[SandstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def SandstoneStairs(
    **states: Unpack[SandstoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def SandstoneWall(
    **states: Unpack[SandstoneWallStates],
) -> Identifier | BlockDescriptor: ...
def Scaffolding(
    **states: Unpack[ScaffoldingStates],
) -> Identifier | BlockDescriptor: ...
def Sculk() -> Identifier: ...
def SculkCatalyst(
    **states: Unpack[SculkCatalystStates],
) -> Identifier | BlockDescriptor: ...
def SculkSensor(
    **states: Unpack[SculkSensorStates],
) -> Identifier | BlockDescriptor: ...
def SculkShrieker(
    **states: Unpack[SculkShriekerStates],
) -> Identifier | BlockDescriptor: ...
def SculkVein(**states: Unpack[SculkVeinStates]) -> Identifier | BlockDescriptor: ...
def SeaLantern() -> Identifier: ...
def SeaPickle(**states: Unpack[SeaPickleStates]) -> Identifier | BlockDescriptor: ...
def Seagrass(**states: Unpack[SeagrassStates]) -> Identifier | BlockDescriptor: ...
def ShelfMushroom(
    **states: Unpack[ShelfMushroomStates],
) -> Identifier | BlockDescriptor: ...
def ShortDryGrass() -> Identifier: ...
def ShortGrass() -> Identifier: ...
def Shroomlight() -> Identifier: ...
def SilverGlazedTerracotta(
    **states: Unpack[SilverGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def SkeletonSkull(
    **states: Unpack[SkeletonSkullStates],
) -> Identifier | BlockDescriptor: ...
def Slime() -> Identifier: ...
def SmallAmethystBud(
    **states: Unpack[SmallAmethystBudStates],
) -> Identifier | BlockDescriptor: ...
def SmallDripleafBlock(
    **states: Unpack[SmallDripleafBlockStates],
) -> Identifier | BlockDescriptor: ...
def SmithingTable() -> Identifier: ...
def Smoker(**states: Unpack[SmokerStates]) -> Identifier | BlockDescriptor: ...
def SmoothBasalt() -> Identifier: ...
def SmoothQuartz(
    **states: Unpack[SmoothQuartzStates],
) -> Identifier | BlockDescriptor: ...
def SmoothQuartzDoubleSlab(
    **states: Unpack[SmoothQuartzDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothQuartzSlab(
    **states: Unpack[SmoothQuartzSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothQuartzStairs(
    **states: Unpack[SmoothQuartzStairsStates],
) -> Identifier | BlockDescriptor: ...
def SmoothRedSandstone() -> Identifier: ...
def SmoothRedSandstoneDoubleSlab(
    **states: Unpack[SmoothRedSandstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothRedSandstoneSlab(
    **states: Unpack[SmoothRedSandstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothRedSandstoneStairs(
    **states: Unpack[SmoothRedSandstoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def SmoothSandstone() -> Identifier: ...
def SmoothSandstoneDoubleSlab(
    **states: Unpack[SmoothSandstoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothSandstoneSlab(
    **states: Unpack[SmoothSandstoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothSandstoneStairs(
    **states: Unpack[SmoothSandstoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def SmoothStone() -> Identifier: ...
def SmoothStoneDoubleSlab(
    **states: Unpack[SmoothStoneDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SmoothStoneSlab(
    **states: Unpack[SmoothStoneSlabStates],
) -> Identifier | BlockDescriptor: ...
def SnifferEgg(**states: Unpack[SnifferEggStates]) -> Identifier | BlockDescriptor: ...
def Snow() -> Identifier: ...
def SnowLayer(**states: Unpack[SnowLayerStates]) -> Identifier | BlockDescriptor: ...
def SoulCampfire(
    **states: Unpack[SoulCampfireStates],
) -> Identifier | BlockDescriptor: ...
def SoulFire(**states: Unpack[SoulFireStates]) -> Identifier | BlockDescriptor: ...
def SoulLantern(
    **states: Unpack[SoulLanternStates],
) -> Identifier | BlockDescriptor: ...
def SoulSand() -> Identifier: ...
def SoulSoil() -> Identifier: ...
def SoulTorch(**states: Unpack[SoulTorchStates]) -> Identifier | BlockDescriptor: ...
def Sponge() -> Identifier: ...
def SporeBlossom() -> Identifier: ...
def SpruceButton(
    **states: Unpack[SpruceButtonStates],
) -> Identifier | BlockDescriptor: ...
def SpruceDoor(**states: Unpack[SpruceDoorStates]) -> Identifier | BlockDescriptor: ...
def SpruceDoubleSlab(
    **states: Unpack[SpruceDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SpruceFence(
    **states: Unpack[SpruceFenceStates],
) -> Identifier | BlockDescriptor: ...
def SpruceFenceGate(
    **states: Unpack[SpruceFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def SpruceHangingSign(
    **states: Unpack[SpruceHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def SpruceLeaves(
    **states: Unpack[SpruceLeavesStates],
) -> Identifier | BlockDescriptor: ...
def SpruceLog(**states: Unpack[SpruceLogStates]) -> Identifier | BlockDescriptor: ...
def SprucePlanks() -> Identifier: ...
def SprucePressurePlate(
    **states: Unpack[SprucePressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def SpruceSapling(
    **states: Unpack[SpruceSaplingStates],
) -> Identifier | BlockDescriptor: ...
def SpruceShelf(
    **states: Unpack[SpruceShelfStates],
) -> Identifier | BlockDescriptor: ...
def SpruceSlab(**states: Unpack[SpruceSlabStates]) -> Identifier | BlockDescriptor: ...
def SpruceStairs(
    **states: Unpack[SpruceStairsStates],
) -> Identifier | BlockDescriptor: ...
def SpruceStandingSign(
    **states: Unpack[SpruceStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def SpruceTrapdoor(
    **states: Unpack[SpruceTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def SpruceWallSign(
    **states: Unpack[SpruceWallSignStates],
) -> Identifier | BlockDescriptor: ...
def SpruceWood(**states: Unpack[SpruceWoodStates]) -> Identifier | BlockDescriptor: ...
def StandingBanner(
    **states: Unpack[StandingBannerStates],
) -> Identifier | BlockDescriptor: ...
def StandingSign(
    **states: Unpack[StandingSignStates],
) -> Identifier | BlockDescriptor: ...
def StickyPiston(
    **states: Unpack[StickyPistonStates],
) -> Identifier | BlockDescriptor: ...
def StickyPistonArmCollision(
    **states: Unpack[StickyPistonArmCollisionStates],
) -> Identifier | BlockDescriptor: ...
def Stone() -> Identifier: ...
def StoneBrickDoubleSlab(
    **states: Unpack[StoneBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def StoneBrickSlab(
    **states: Unpack[StoneBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def StoneBrickStairs(
    **states: Unpack[StoneBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def StoneBrickWall(
    **states: Unpack[StoneBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def StoneBricks() -> Identifier: ...
def StoneButton(
    **states: Unpack[StoneButtonStates],
) -> Identifier | BlockDescriptor: ...
def StonePressurePlate(
    **states: Unpack[StonePressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def StoneStairs(
    **states: Unpack[StoneStairsStates],
) -> Identifier | BlockDescriptor: ...
def StonecutterBlock(
    **states: Unpack[StonecutterBlockStates],
) -> Identifier | BlockDescriptor: ...
def StrawBed(**states: Unpack[StrawBedStates]) -> Identifier | BlockDescriptor: ...
def StrippedAcaciaLog(
    **states: Unpack[StrippedAcaciaLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedAcaciaWood(
    **states: Unpack[StrippedAcaciaWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedBambooBlock(
    **states: Unpack[StrippedBambooBlockStates],
) -> Identifier | BlockDescriptor: ...
def StrippedBirchLog(
    **states: Unpack[StrippedBirchLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedBirchWood(
    **states: Unpack[StrippedBirchWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedCherryLog(
    **states: Unpack[StrippedCherryLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedCherryWood(
    **states: Unpack[StrippedCherryWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedCrimsonHyphae(
    **states: Unpack[StrippedCrimsonHyphaeStates],
) -> Identifier | BlockDescriptor: ...
def StrippedCrimsonStem(
    **states: Unpack[StrippedCrimsonStemStates],
) -> Identifier | BlockDescriptor: ...
def StrippedDarkOakLog(
    **states: Unpack[StrippedDarkOakLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedDarkOakWood(
    **states: Unpack[StrippedDarkOakWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedJungleLog(
    **states: Unpack[StrippedJungleLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedJungleWood(
    **states: Unpack[StrippedJungleWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedMangroveLog(
    **states: Unpack[StrippedMangroveLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedMangroveWood(
    **states: Unpack[StrippedMangroveWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedOakLog(
    **states: Unpack[StrippedOakLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedOakWood(
    **states: Unpack[StrippedOakWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedPaleOakLog(
    **states: Unpack[StrippedPaleOakLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedPaleOakWood(
    **states: Unpack[StrippedPaleOakWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedPoplarLog(
    **states: Unpack[StrippedPoplarLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedPoplarWood(
    **states: Unpack[StrippedPoplarWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedSpruceLog(
    **states: Unpack[StrippedSpruceLogStates],
) -> Identifier | BlockDescriptor: ...
def StrippedSpruceWood(
    **states: Unpack[StrippedSpruceWoodStates],
) -> Identifier | BlockDescriptor: ...
def StrippedWarpedHyphae(
    **states: Unpack[StrippedWarpedHyphaeStates],
) -> Identifier | BlockDescriptor: ...
def StrippedWarpedStem(
    **states: Unpack[StrippedWarpedStemStates],
) -> Identifier | BlockDescriptor: ...
def StructureBlock(
    **states: Unpack[StructureBlockStates],
) -> Identifier | BlockDescriptor: ...
def StructureVoid() -> Identifier: ...
def Sulfur() -> Identifier: ...
def SulfurBrickDoubleSlab(
    **states: Unpack[SulfurBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SulfurBrickSlab(
    **states: Unpack[SulfurBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def SulfurBrickStairs(
    **states: Unpack[SulfurBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def SulfurBrickWall(
    **states: Unpack[SulfurBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def SulfurBricks() -> Identifier: ...
def SulfurDoubleSlab(
    **states: Unpack[SulfurDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def SulfurSlab(**states: Unpack[SulfurSlabStates]) -> Identifier | BlockDescriptor: ...
def SulfurSpike(
    **states: Unpack[SulfurSpikeStates],
) -> Identifier | BlockDescriptor: ...
def SulfurStairs(
    **states: Unpack[SulfurStairsStates],
) -> Identifier | BlockDescriptor: ...
def SulfurWall(**states: Unpack[SulfurWallStates]) -> Identifier | BlockDescriptor: ...
def Sunflower(**states: Unpack[SunflowerStates]) -> Identifier | BlockDescriptor: ...
def SuspiciousGravel(
    **states: Unpack[SuspiciousGravelStates],
) -> Identifier | BlockDescriptor: ...
def SuspiciousSand(
    **states: Unpack[SuspiciousSandStates],
) -> Identifier | BlockDescriptor: ...
def SweetBerryBush(
    **states: Unpack[SweetBerryBushStates],
) -> Identifier | BlockDescriptor: ...
def TallDryGrass() -> Identifier: ...
def TallGrass(**states: Unpack[TallGrassStates]) -> Identifier | BlockDescriptor: ...
def Target() -> Identifier: ...
def TintedGlass() -> Identifier: ...
def Tnt(**states: Unpack[TntStates]) -> Identifier | BlockDescriptor: ...
def Torch(**states: Unpack[TorchStates]) -> Identifier | BlockDescriptor: ...
def Torchflower() -> Identifier: ...
def TorchflowerCrop(
    **states: Unpack[TorchflowerCropStates],
) -> Identifier | BlockDescriptor: ...
def Trapdoor(**states: Unpack[TrapdoorStates]) -> Identifier | BlockDescriptor: ...
def TrappedChest(
    **states: Unpack[TrappedChestStates],
) -> Identifier | BlockDescriptor: ...
def TrialSpawner(
    **states: Unpack[TrialSpawnerStates],
) -> Identifier | BlockDescriptor: ...
def TripWire(**states: Unpack[TripWireStates]) -> Identifier | BlockDescriptor: ...
def TripwireHook(
    **states: Unpack[TripwireHookStates],
) -> Identifier | BlockDescriptor: ...
def TubeCoral() -> Identifier: ...
def TubeCoralBlock() -> Identifier: ...
def TubeCoralFan(
    **states: Unpack[TubeCoralFanStates],
) -> Identifier | BlockDescriptor: ...
def TubeCoralWallFan(
    **states: Unpack[TubeCoralWallFanStates],
) -> Identifier | BlockDescriptor: ...
def Tuff() -> Identifier: ...
def TuffBrickDoubleSlab(
    **states: Unpack[TuffBrickDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def TuffBrickSlab(
    **states: Unpack[TuffBrickSlabStates],
) -> Identifier | BlockDescriptor: ...
def TuffBrickStairs(
    **states: Unpack[TuffBrickStairsStates],
) -> Identifier | BlockDescriptor: ...
def TuffBrickWall(
    **states: Unpack[TuffBrickWallStates],
) -> Identifier | BlockDescriptor: ...
def TuffBricks() -> Identifier: ...
def TuffDoubleSlab(
    **states: Unpack[TuffDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def TuffSlab(**states: Unpack[TuffSlabStates]) -> Identifier | BlockDescriptor: ...
def TuffStairs(**states: Unpack[TuffStairsStates]) -> Identifier | BlockDescriptor: ...
def TuffWall(**states: Unpack[TuffWallStates]) -> Identifier | BlockDescriptor: ...
def TurtleEgg(**states: Unpack[TurtleEggStates]) -> Identifier | BlockDescriptor: ...
def TwistingVines(
    **states: Unpack[TwistingVinesStates],
) -> Identifier | BlockDescriptor: ...
def UnderwaterTnt(
    **states: Unpack[UnderwaterTntStates],
) -> Identifier | BlockDescriptor: ...
def UnderwaterTorch(
    **states: Unpack[UnderwaterTorchStates],
) -> Identifier | BlockDescriptor: ...
def UndyedShulkerBox() -> Identifier: ...
def Unknown() -> Identifier: ...
def UnlitRedstoneTorch(
    **states: Unpack[UnlitRedstoneTorchStates],
) -> Identifier | BlockDescriptor: ...
def UnpoweredComparator(
    **states: Unpack[UnpoweredComparatorStates],
) -> Identifier | BlockDescriptor: ...
def UnpoweredRepeater(
    **states: Unpack[UnpoweredRepeaterStates],
) -> Identifier | BlockDescriptor: ...
def Vault(**states: Unpack[VaultStates]) -> Identifier | BlockDescriptor: ...
def VerdantFroglight(
    **states: Unpack[VerdantFroglightStates],
) -> Identifier | BlockDescriptor: ...
def Vine(**states: Unpack[VineStates]) -> Identifier | BlockDescriptor: ...
def WallBanner(**states: Unpack[WallBannerStates]) -> Identifier | BlockDescriptor: ...
def WallSign(**states: Unpack[WallSignStates]) -> Identifier | BlockDescriptor: ...
def WarpedButton(
    **states: Unpack[WarpedButtonStates],
) -> Identifier | BlockDescriptor: ...
def WarpedDoor(**states: Unpack[WarpedDoorStates]) -> Identifier | BlockDescriptor: ...
def WarpedDoubleSlab(
    **states: Unpack[WarpedDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def WarpedFence(
    **states: Unpack[WarpedFenceStates],
) -> Identifier | BlockDescriptor: ...
def WarpedFenceGate(
    **states: Unpack[WarpedFenceGateStates],
) -> Identifier | BlockDescriptor: ...
def WarpedFungus() -> Identifier: ...
def WarpedHangingSign(
    **states: Unpack[WarpedHangingSignStates],
) -> Identifier | BlockDescriptor: ...
def WarpedHyphae(
    **states: Unpack[WarpedHyphaeStates],
) -> Identifier | BlockDescriptor: ...
def WarpedNylium() -> Identifier: ...
def WarpedPlanks() -> Identifier: ...
def WarpedPressurePlate(
    **states: Unpack[WarpedPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def WarpedRoots() -> Identifier: ...
def WarpedShelf(
    **states: Unpack[WarpedShelfStates],
) -> Identifier | BlockDescriptor: ...
def WarpedSlab(**states: Unpack[WarpedSlabStates]) -> Identifier | BlockDescriptor: ...
def WarpedStairs(
    **states: Unpack[WarpedStairsStates],
) -> Identifier | BlockDescriptor: ...
def WarpedStandingSign(
    **states: Unpack[WarpedStandingSignStates],
) -> Identifier | BlockDescriptor: ...
def WarpedStem(**states: Unpack[WarpedStemStates]) -> Identifier | BlockDescriptor: ...
def WarpedTrapdoor(
    **states: Unpack[WarpedTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def WarpedWallSign(
    **states: Unpack[WarpedWallSignStates],
) -> Identifier | BlockDescriptor: ...
def WarpedWartBlock() -> Identifier: ...
def Water(**states: Unpack[WaterStates]) -> Identifier | BlockDescriptor: ...
def Waterlily() -> Identifier: ...
def WaxedChiseledCopper() -> Identifier: ...
def WaxedCopper() -> Identifier: ...
def WaxedCopperBars(
    **states: Unpack[WaxedCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperBulb(
    **states: Unpack[WaxedCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperChain(
    **states: Unpack[WaxedCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperChest(
    **states: Unpack[WaxedCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperDoor(
    **states: Unpack[WaxedCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperGolemStatue(
    **states: Unpack[WaxedCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperGrate() -> Identifier: ...
def WaxedCopperLantern(
    **states: Unpack[WaxedCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCopperTrapdoor(
    **states: Unpack[WaxedCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCutCopper() -> Identifier: ...
def WaxedCutCopperSlab(
    **states: Unpack[WaxedCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedCutCopperStairs(
    **states: Unpack[WaxedCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedDoubleCutCopperSlab(
    **states: Unpack[WaxedDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedChiseledCopper() -> Identifier: ...
def WaxedExposedCopper() -> Identifier: ...
def WaxedExposedCopperBars(
    **states: Unpack[WaxedExposedCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperBulb(
    **states: Unpack[WaxedExposedCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperChain(
    **states: Unpack[WaxedExposedCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperChest(
    **states: Unpack[WaxedExposedCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperDoor(
    **states: Unpack[WaxedExposedCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperGolemStatue(
    **states: Unpack[WaxedExposedCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperGrate() -> Identifier: ...
def WaxedExposedCopperLantern(
    **states: Unpack[WaxedExposedCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCopperTrapdoor(
    **states: Unpack[WaxedExposedCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCutCopper() -> Identifier: ...
def WaxedExposedCutCopperSlab(
    **states: Unpack[WaxedExposedCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedCutCopperStairs(
    **states: Unpack[WaxedExposedCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedDoubleCutCopperSlab(
    **states: Unpack[WaxedExposedDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedExposedLightningRod(
    **states: Unpack[WaxedExposedLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def WaxedLightningRod(
    **states: Unpack[WaxedLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedChiseledCopper() -> Identifier: ...
def WaxedOxidizedCopper() -> Identifier: ...
def WaxedOxidizedCopperBars(
    **states: Unpack[WaxedOxidizedCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperBulb(
    **states: Unpack[WaxedOxidizedCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperChain(
    **states: Unpack[WaxedOxidizedCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperChest(
    **states: Unpack[WaxedOxidizedCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperDoor(
    **states: Unpack[WaxedOxidizedCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperGolemStatue(
    **states: Unpack[WaxedOxidizedCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperGrate() -> Identifier: ...
def WaxedOxidizedCopperLantern(
    **states: Unpack[WaxedOxidizedCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCopperTrapdoor(
    **states: Unpack[WaxedOxidizedCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCutCopper() -> Identifier: ...
def WaxedOxidizedCutCopperSlab(
    **states: Unpack[WaxedOxidizedCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedCutCopperStairs(
    **states: Unpack[WaxedOxidizedCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedDoubleCutCopperSlab(
    **states: Unpack[WaxedOxidizedDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedOxidizedLightningRod(
    **states: Unpack[WaxedOxidizedLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredChiseledCopper() -> Identifier: ...
def WaxedWeatheredCopper() -> Identifier: ...
def WaxedWeatheredCopperBars(
    **states: Unpack[WaxedWeatheredCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperBulb(
    **states: Unpack[WaxedWeatheredCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperChain(
    **states: Unpack[WaxedWeatheredCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperChest(
    **states: Unpack[WaxedWeatheredCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperDoor(
    **states: Unpack[WaxedWeatheredCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperGolemStatue(
    **states: Unpack[WaxedWeatheredCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperGrate() -> Identifier: ...
def WaxedWeatheredCopperLantern(
    **states: Unpack[WaxedWeatheredCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCopperTrapdoor(
    **states: Unpack[WaxedWeatheredCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCutCopper() -> Identifier: ...
def WaxedWeatheredCutCopperSlab(
    **states: Unpack[WaxedWeatheredCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredCutCopperStairs(
    **states: Unpack[WaxedWeatheredCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredDoubleCutCopperSlab(
    **states: Unpack[WaxedWeatheredDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WaxedWeatheredLightningRod(
    **states: Unpack[WaxedWeatheredLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredChiseledCopper() -> Identifier: ...
def WeatheredCopper() -> Identifier: ...
def WeatheredCopperBars(
    **states: Unpack[WeatheredCopperBarsStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperBulb(
    **states: Unpack[WeatheredCopperBulbStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperChain(
    **states: Unpack[WeatheredCopperChainStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperChest(
    **states: Unpack[WeatheredCopperChestStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperDoor(
    **states: Unpack[WeatheredCopperDoorStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperGolemStatue(
    **states: Unpack[WeatheredCopperGolemStatueStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperGrate() -> Identifier: ...
def WeatheredCopperLantern(
    **states: Unpack[WeatheredCopperLanternStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCopperTrapdoor(
    **states: Unpack[WeatheredCopperTrapdoorStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCutCopper() -> Identifier: ...
def WeatheredCutCopperSlab(
    **states: Unpack[WeatheredCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredCutCopperStairs(
    **states: Unpack[WeatheredCutCopperStairsStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredDoubleCutCopperSlab(
    **states: Unpack[WeatheredDoubleCutCopperSlabStates],
) -> Identifier | BlockDescriptor: ...
def WeatheredLightningRod(
    **states: Unpack[WeatheredLightningRodStates],
) -> Identifier | BlockDescriptor: ...
def Web() -> Identifier: ...
def WeepingVines(
    **states: Unpack[WeepingVinesStates],
) -> Identifier | BlockDescriptor: ...
def WetSponge() -> Identifier: ...
def Wheat(**states: Unpack[WheatStates]) -> Identifier | BlockDescriptor: ...
def WhiteCandle(
    **states: Unpack[WhiteCandleStates],
) -> Identifier | BlockDescriptor: ...
def WhiteCandleCake(
    **states: Unpack[WhiteCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def WhiteCarpet() -> Identifier: ...
def WhiteConcrete() -> Identifier: ...
def WhiteConcreteDoubleSlab(
    **states: Unpack[WhiteConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def WhiteConcretePowder() -> Identifier: ...
def WhiteConcreteSlab(
    **states: Unpack[WhiteConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def WhiteConcreteStairs(
    **states: Unpack[WhiteConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def WhiteGlazedTerracotta(
    **states: Unpack[WhiteGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def WhiteShulkerBox() -> Identifier: ...
def WhiteStainedGlass() -> Identifier: ...
def WhiteStainedGlassPane(
    **states: Unpack[WhiteStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def WhiteTerracotta() -> Identifier: ...
def WhiteTulip() -> Identifier: ...
def WhiteWool() -> Identifier: ...
def WhiteWoolDoubleSlab(
    **states: Unpack[WhiteWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def WhiteWoolSlab(
    **states: Unpack[WhiteWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def WhiteWoolStairs(
    **states: Unpack[WhiteWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def Wildflowers(
    **states: Unpack[WildflowersStates],
) -> Identifier | BlockDescriptor: ...
def WitherRose() -> Identifier: ...
def WitherSkeletonSkull(
    **states: Unpack[WitherSkeletonSkullStates],
) -> Identifier | BlockDescriptor: ...
def WoodenButton(
    **states: Unpack[WoodenButtonStates],
) -> Identifier | BlockDescriptor: ...
def WoodenDoor(**states: Unpack[WoodenDoorStates]) -> Identifier | BlockDescriptor: ...
def WoodenPressurePlate(
    **states: Unpack[WoodenPressurePlateStates],
) -> Identifier | BlockDescriptor: ...
def YellowCandle(
    **states: Unpack[YellowCandleStates],
) -> Identifier | BlockDescriptor: ...
def YellowCandleCake(
    **states: Unpack[YellowCandleCakeStates],
) -> Identifier | BlockDescriptor: ...
def YellowCarpet() -> Identifier: ...
def YellowConcrete() -> Identifier: ...
def YellowConcreteDoubleSlab(
    **states: Unpack[YellowConcreteDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def YellowConcretePowder() -> Identifier: ...
def YellowConcreteSlab(
    **states: Unpack[YellowConcreteSlabStates],
) -> Identifier | BlockDescriptor: ...
def YellowConcreteStairs(
    **states: Unpack[YellowConcreteStairsStates],
) -> Identifier | BlockDescriptor: ...
def YellowGlazedTerracotta(
    **states: Unpack[YellowGlazedTerracottaStates],
) -> Identifier | BlockDescriptor: ...
def YellowPoplarLeaves(
    **states: Unpack[YellowPoplarLeavesStates],
) -> Identifier | BlockDescriptor: ...
def YellowShulkerBox() -> Identifier: ...
def YellowStainedGlass() -> Identifier: ...
def YellowStainedGlassPane(
    **states: Unpack[YellowStainedGlassPaneStates],
) -> Identifier | BlockDescriptor: ...
def YellowTerracotta() -> Identifier: ...
def YellowWool() -> Identifier: ...
def YellowWoolDoubleSlab(
    **states: Unpack[YellowWoolDoubleSlabStates],
) -> Identifier | BlockDescriptor: ...
def YellowWoolSlab(
    **states: Unpack[YellowWoolSlabStates],
) -> Identifier | BlockDescriptor: ...
def YellowWoolStairs(
    **states: Unpack[YellowWoolStairsStates],
) -> Identifier | BlockDescriptor: ...
def ZombieHead(**states: Unpack[ZombieHeadStates]) -> Identifier | BlockDescriptor: ...
