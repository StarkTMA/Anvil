"""Anvil's enums: targets, slots, block traits and states, JSON UI values and more."""

from enum import StrEnum


class Target(StrEnum):
    """
    Enumeration for the types of targets that can be selected in Minecraft.
    """

    P = "@p"
    R = "@r"
    A = "@a"
    E = "@e"
    S = "@s"
    C = "@c"
    V = "@v"
    Initiator = "@initiator"
    N = "@n"


class FogCameraLocation(StrEnum):
    """
    Enumeration for the different locations of the fog camera in the game.
    """

    Air = "air"
    Lava = "lava"
    Lava_resistance = "lava_resistance"
    Powder_snow = "powder_snow"
    Water = "water"
    Weather = "weather"


class RenderDistanceType(StrEnum):
    """
    Enumeration for the different types of render distances in the game.
    """

    Render = "render"
    Fixed = "fixed"


class LootPoolType(StrEnum):
    """
    Enumeration for the different types of loot pools.
    """

    Empty = "empty"
    Item = "item"
    LootTable = "loot_table"


class Slots(StrEnum):
    """
    Enumeration for the different types of inventory slots in the game.
    """

    Mainhand = "slot.weapon.mainhand"
    Offhand = "slot.weapon.offhand"
    Head = "slot.armor.head"
    Chest = "slot.armor.chest"
    Legs = "slot.armor.legs"
    Feet = "slot.armor.feet"
    Hotbar = "slot.hotbar"
    Inventory = "slot.inventory"
    Enderchest = "slot.enderchest"
    Saddle = "slot.saddle"
    Armor = "slot.armor"
    EquippedChest = "slot.chest"
    Equippable = "slot.equippable"
    Container = "slots.container"
    Body = "slot.armor.body"


class Dimension(StrEnum):
    """
    Enumeration for the different dimensions in the game.
    """

    Nether = "minecraft:nether"
    Overworld = "minecraft:overworld"
    TheEnd = "minecraft:the_end"


class Difficulty(StrEnum):
    """
    Enumeration for the different levels of game difficulty.
    """

    Peaceful = "peaceful"
    Easy = "easy"
    Normal = "normal"
    Hard = "hard"
    Hardcore = "hardcore"


class DamageCause(StrEnum):
    """
    Enumeration for the different causes of damage in the game.
    """

    All = "all"
    Anvil = "anvil"
    EntityAttack = "entity_attack"
    BlockExplosion = "block_explosion"
    Contact = "contact"
    Drowning = "drowning"
    EntityExplosion = "entity_explosion"
    Fall = "fall"
    FallingBlock = "falling_block"
    Fatal = "fatal"
    Fire = "fire"
    Firetick = "firetick"
    FlyIntoWall = "fly_into_wall"
    Lava = "lava"
    Magic = "magic"
    Nothing = "none"
    Override = "override"
    Piston = "piston"
    Projectile = "projectile"
    SonicBoom = "sonic_boom"
    Stalactite = "stalactite"
    Stalagmite = "stalagmite"
    Starve = "starve"
    Suffocation = "suffocation"
    SelfDestruct = "self_destruct"
    Thorns = "thorns"
    Void = "void"
    Wither = "wither"


class Anchor(StrEnum):
    """
    Enumeration representing the two anchor points that can be used in Minecraft: the feet and the eyes.
    """

    Feet = "feet"
    Eyes = "eyes"


class CameraPresets(StrEnum):
    ControlSchemeCamera = "minecraft:control_scheme_camera"
    FirstPerson = "minecraft:first_person"
    FixedBoom = "minecraft:fixed_boom"
    FollowOrbit = "minecraft:follow_orbit"
    Free = "minecraft:free"
    ThirdPerson = "minecraft:third_person"
    ThirdPersonFront = "minecraft:third_person_front"


class ControlSchemes(StrEnum):
    """
    Enumeration representing the different control schemes in Minecraft Bedrock.
    """

    CameraRelative = "camera_relative"
    CameraRelativeStrafe = "camera_relative_strafe"
    PlayerRelative = "player_relative"
    PlayerRelativeStrafe = "player_relative_strafe"
    LockedPlayerRelativeStrafe = "locked_player_relative_strafe"


class Population(StrEnum):
    """
    Enumeration for the different types of in-game populations.
    """

    Ambient = "ambient"
    Animal = "animal"
    Cat = "cat"
    Monster = "monster"
    Pillager = "pillager"
    WaterAnimal = "water_animal"


class PlacementDirectionTrait(StrEnum):
    CardinalDirection = "minecraft:cardinal_direction"
    FacingDirection = "minecraft:facing_direction"
    CornerAndCardinalDirection = "minecraft:corner_and_cardinal_direction"
    SixteenWayRotation = "minecraft:sixteen_way_rotation"


class PlacementPositionTrait(StrEnum):
    BlockFace = "minecraft:block_face"
    VerticalHalf = "minecraft:vertical_half"
    CornerAndCardinal = "minecraft:corner_and_cardinal"


class ConnectionTrait(StrEnum):
    CardinalConnections = "minecraft:cardinal_connections"


class CardinalConnectionStates(StrEnum):
    """
    Enumeration representing the connected faces of a block in Minecraft, used for blocks that can connect to adjacent blocks (e.g., fences, walls).
    """

    North = "minecraft:connection_north"
    South = "minecraft:connection_south"
    East = "minecraft:connection_east"
    West = "minecraft:connection_west"


class BlockCornerState(StrEnum):
    Corner = "minecraft:corner"


class MultiblockPartState(StrEnum):
    Part = "minecraft:multi_block_part"


class CardinalDirectionsValues(StrEnum):
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class FacingDirectionValues(StrEnum):
    Up = "up"
    Down = "down"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    EAST = "east"


class VerticalHalfValues(StrEnum):
    TOP = "top"
    BOTTOM = "bottom"


class BlockCornerValues(StrEnum):
    """
    Enumeration representing the corner and cardinal directions for block placement in Minecraft.
    """

    InnerLeft = "inner_left"
    InnerRight = "inner_right"
    OuterLeft = "outer_left"
    OuterRight = "outer_right"
    None_ = "none"


class BlockFaceValues(StrEnum):
    """
    Enumeration representing the different faces of a block in Minecraft.
    """

    Up = "up"
    Down = "down"
    North = "north"
    South = "south"
    East = "east"
    West = "west"
    Side = "side"
    All = "all"


_CARDINAL_FACES = [
    BlockFaceValues.North,
    BlockFaceValues.South,
    BlockFaceValues.East,
    BlockFaceValues.West,
]
_ALL_FACES = [
    BlockFaceValues.North,
    BlockFaceValues.South,
    BlockFaceValues.East,
    BlockFaceValues.West,
    BlockFaceValues.Up,
    BlockFaceValues.Down,
]


def expand_block_face_sides(faces: list[BlockFaceValues]) -> list[BlockFaceValues]:
    """Expand ``BlockFaceValues.Side`` and ``BlockFaceValues.All`` into explicit face lists.

    ``Side`` expands to the four cardinal directions (North, South, East, West).
    ``All`` expands to all six faces.
    The input list is not mutated; a new list is returned.
    """
    has_all = BlockFaceValues.All in faces
    has_side = BlockFaceValues.Side in faces

    if not has_all and not has_side:
        return list(faces)

    if has_all:
        faces.remove(BlockFaceValues.All)
    if has_side:
        faces.remove(BlockFaceValues.Side)

    if has_all:
        faces.extend(_ALL_FACES)
    else:
        faces.extend(_CARDINAL_FACES)
    return faces


class BlockMaterial(StrEnum):
    """
    Enumeration representing the different types of rendering methods a block can use in Minecraft.

    Opaque:	Used for a regular block texture without an alpha layer. Does not allow for transparency or translucency
    DoubleSided:	Used for completely disabling backface culling.
    Blend:	Used for a block like stained glass. Allows for transparency and translucency (slightly transparent textures).
    AlphaTest:	Used for a block like the monster spawner. Does not allow for translucency, only fully opaque or fully transparent textures. Also disabled backface culling.
    AlphaTestSingleSided: Used for a block like the (unstained) glass. Does not allow for translucency, only fully opaque or fully transparent textures. Also enables backface culling.
    BlendToOpaque:	Will blend like stained glass in the near render and turn opaque on the far render.
    AlphaTestToOpaque: Used for a block like the leaves. Does not allow for translucency, only fully opaque or fully transparent textures in the near render and turn only opaque on the far render. Also disabled backface culling.
    AlphaTestSingleSidedToOpaque:	Used for a block like the sugar cane. Does not allow for translucency, only fully opaque or fully transparent textures in the near render and turn only opaque on the far render. Also enables backface culling.
    """

    Opaque = "opaque"
    DoubleSided = "double_sided"
    Blend = "blend"
    AlphaTest = "alpha_test"
    AlphaTestSingleSided = "alpha_test_single_sided"
    BlendToOpaque = "blend_to_opaque"
    AlphaTestToOpaque = "alpha_test_to_opaque"
    AlphaTestSingleSidedToOpaque = "alpha_test_single_sided_to_opaque"
    AlphaMaskedTint = "alpha_masked_tint"


class ItemCategory(StrEnum):
    """
    Enumeration representing the categories of blocks and items that can be used in Minecraft.
    """

    Construction = "construction"
    Equipment = "equipment"
    Items = "items"
    Nature = "nature"


class ItemGroups(StrEnum):
    Anvil = "minecraft:itemGroup.name.anvil"
    Arrow = "minecraft:itemGroup.name.arrow"
    Axe = "minecraft:itemGroup.name.axe"
    Banner = "minecraft:itemGroup.name.banner"
    BannerPattern = "minecraft:itemGroup.name.banner_pattern"
    Bed = "minecraft:itemGroup.name.bed"
    Boat = "minecraft:itemGroup.name.boat"
    Boots = "minecraft:itemGroup.name.boots"
    Buttons = "minecraft:itemGroup.name.buttons"
    Candles = "minecraft:itemGroup.name.candles"
    Chalkboard = "minecraft:itemGroup.name.chalkboard"
    Chest = "minecraft:itemGroup.name.chest"
    ChestBoat = "minecraft:itemGroup.name.chestboat"
    Chestplate = "minecraft:itemGroup.name.chestplate"
    Concrete = "minecraft:itemGroup.name.concrete"
    ConcretePowder = "minecraft:itemGroup.name.concretePowder"
    CookedFood = "minecraft:itemGroup.name.cookedFood"
    Copper = "minecraft:itemGroup.name.copper"
    Coral = "minecraft:itemGroup.name.coral"
    CoralDecorations = "minecraft:itemGroup.name.coral_decorations"
    Crop = "minecraft:itemGroup.name.crop"
    Door = "minecraft:itemGroup.name.door"
    Dye = "minecraft:itemGroup.name.dye"
    EnchantedBook = "minecraft:itemGroup.name.enchantedBook"
    Fence = "minecraft:itemGroup.name.fence"
    FenceGate = "minecraft:itemGroup.name.fenceGate"
    Firework = "minecraft:itemGroup.name.firework"
    FireworkStars = "minecraft:itemGroup.name.fireworkStars"
    Flower = "minecraft:itemGroup.name.flower"
    Glass = "minecraft:itemGroup.name.glass"
    GlassPane = "minecraft:itemGroup.name.glassPane"
    GlazedTerracotta = "minecraft:itemGroup.name.glazedTerracotta"
    GoatHorn = "minecraft:itemGroup.name.goatHorn"
    Grass = "minecraft:itemGroup.name.grass"
    HangingSign = "minecraft:itemGroup.name.hanging_sign"
    Helmet = "minecraft:itemGroup.name.helmet"
    Hoe = "minecraft:itemGroup.name.hoe"
    HorseArmor = "minecraft:itemGroup.name.horseArmor"
    Leaves = "minecraft:itemGroup.name.leaves"
    Leggings = "minecraft:itemGroup.name.leggings"
    LingeringPotion = "minecraft:itemGroup.name.lingeringPotion"
    Log = "minecraft:itemGroup.name.log"
    Minecart = "minecraft:itemGroup.name.minecart"
    MiscFood = "minecraft:itemGroup.name.miscFood"
    MobEgg = "minecraft:itemGroup.name.mobEgg"
    MonsterStoneEgg = "minecraft:itemGroup.name.monsterStoneEgg"
    Mushroom = "minecraft:itemGroup.name.mushroom"
    NetherWartBlock = "minecraft:itemGroup.name.netherWartBlock"
    Ore = "minecraft:itemGroup.name.ore"
    Permission = "minecraft:itemGroup.name.permission"
    Pickaxe = "minecraft:itemGroup.name.pickaxe"
    Planks = "minecraft:itemGroup.name.planks"
    Potion = "minecraft:itemGroup.name.potion"
    PotterySherds = "minecraft:itemGroup.name.potterySherds"
    PressurePlate = "minecraft:itemGroup.name.pressurePlate"
    Rail = "minecraft:itemGroup.name.rail"
    RawFood = "minecraft:itemGroup.name.rawFood"
    Record = "minecraft:itemGroup.name.record"
    Sandstone = "minecraft:itemGroup.name.sandstone"
    Sapling = "minecraft:itemGroup.name.sapling"
    Sculk = "minecraft:itemGroup.name.sculk"
    Seed = "minecraft:itemGroup.name.seed"
    Shovel = "minecraft:itemGroup.name.shovel"
    ShulkerBox = "minecraft:itemGroup.name.shulkerBox"
    Sign = "minecraft:itemGroup.name.sign"
    Skull = "minecraft:itemGroup.name.skull"
    Slab = "minecraft:itemGroup.name.slab"
    SmithingTemplates = "minecraft:itemGroup.name.smithing_templates"
    SplashPotion = "minecraft:itemGroup.name.splashPotion"
    StainedClay = "minecraft:itemGroup.name.stainedClay"
    Stairs = "minecraft:itemGroup.name.stairs"
    Stone = "minecraft:itemGroup.name.stone"
    StoneBrick = "minecraft:itemGroup.name.stoneBrick"
    Sword = "minecraft:itemGroup.name.sword"
    Trapdoor = "minecraft:itemGroup.name.trapdoor"
    Walls = "minecraft:itemGroup.name.walls"
    Wood = "minecraft:itemGroup.name.wood"
    Wool = "minecraft:itemGroup.name.wool"
    WoolCarpet = "minecraft:itemGroup.name.woolCarpet"


class Weather(StrEnum):
    """
    Enumeration representing the different types of weather that can be set in Minecraft.
    """

    Clear = "clear"
    Rain = "rain"
    Thunder = "thunder"


class FilterSubject(StrEnum):
    """
    Enumeration representing the different subjects that can be used in filters in Minecraft.
    """

    Block = "block"
    Damager = "damager"
    Other = "other"
    Parent = "parent"
    Player = "player"
    Self = "self"
    Target = "target"
    Baby = "baby"
    Holder = "holder"
    Item = "item"


class FilterOperation(StrEnum):
    """
    Enumeration representing the different operations that can be used in filters in Minecraft.
    """

    Less = "<"
    LessEqual = "<="
    Greater = ">"
    GreaterEqual = ">="
    Equals = "equals"
    Not = "not"


class FilterEquipmentDomain(StrEnum):
    """
    Enumeration representing the different equipment domains that can be used in filters in Minecraft.
    """

    Any = "any"
    Armor = "armor"
    Feet = "feet"
    Hand = "hand"
    Head = "head"
    Inventory = "inventory"
    Leg = "leg"
    Torso = "torso"


class Vibrations(StrEnum):
    EntityInteract = "entity_interact"
    EntityAct = "entity_act"
    EntityDie = "entity_die"
    Shear = "shear"
    none = "none"


class ControlFlags(StrEnum):
    Move = "move"
    Look = "look"
    Jump = "jump"


class MaterialStates(StrEnum):
    """
    Enumeration representing the different states a material can be in Minecraft.
    """

    EnableStencilTest = "EnableStencilTest"
    StencilWrite = "StencilWrite"
    InvertCulling = "InvertCulling"
    DisableCulling = "DisableCulling"
    DisableDepthWrite = "DisableDepthWrite"
    Blending = "Blending"
    DisableAlphaWrite = "DisableAlphaWrite"
    DisableColorWrite = "DisableColorWrite"
    EnableAlphaToCoverage = "EnableAlphaToCoverage"


class MaterialDefinitions(StrEnum):
    """
    Enumeration representing the different definitions that can be set for a material in Minecraft.
    """

    FANCY = "FANCY"
    USE_OVERLAY = "USE_OVERLAY"
    USE_COLOR_MASK = "USE_COLOR_MASK"
    MULTI_COLOR_TINT = "MULTI_COLOR_TINT"
    COLOR_BASED = "COLOR_BASED"
    USE_UV_ANIM = "USE_UV_ANIM"
    TINTED = "TINTED"
    USE_COLOR_BLEND = "USE_COLOR_BLEND"
    MULTIPLICATIVE_TINT = "MULTIPLICATIVE_TINT"
    MULTIPLICATIVE_TINT_COLOR = "MULTIPLICATIVE_TINT_COLOR"
    USE_MULTITEXTURE = "USE_MULTITEXTURE"
    ALPHA_TEST = "ALPHA_TEST"
    LINE_STRIP = "LINE_STRIP"
    USE_EMISSIVE = "USE_EMISSIVE"
    NO_TEXTURE = "NO_TEXTURE"
    ITEM_IN_HAND = "ITEM_IN_HAND"
    GLINT = "GLINT"
    USE_ONLY_EMISSIVE = "USE_ONLY_EMISSIVE"
    USE_MASK = "USE_MASK"


class MaterialFunc(StrEnum):
    """
    Enumeration representing the different functions that can be set for a material in Minecraft.
    """

    Always = "Always"
    Equal = "Equal"
    NotEqual = "NotEqual"
    Less = "Less"
    Greater = "Greater"
    GreaterEqual = "GreaterEqual"
    LessEqual = "LessEqual"


class MaterialOperation(StrEnum):
    """
    Enumeration representing the different operations that can be set for a material in Minecraft.
    """

    Keep = "Keep"
    Replace = "Replace"


class SoundCategory(StrEnum):
    """
    Enumeration for the different categories of sounds in the game.
    """

    Ambient = "ambient"
    Block = "block"
    Player = "player"
    Neutral = "neutral"
    Hostile = "hostile"
    Music = "music"
    Record = "record"
    UI = "ui"


class DurationInfoMode(StrEnum):
    """
    Enumeration for how a server-side sound definition's duration is tracked.
    """

    GameTime = "game_time"
    RealTime = "real_time"


class EntitySoundEvent(StrEnum):
    Ambient = "ambient"
    Hurt = "hurt"
    Death = "death"
    Takeoff = "takeoff"
    AmbientTame = "ambient.tame"
    Purr = "purr"
    Purreow = "purreow"
    Eat = "eat"
    Step = "step"
    Plop = "plop"
    Fuse = "fuse"
    Breathe = "breathe"
    Attack = "attack"
    Splash = "splash"
    Swim = "swim"
    AmbientInWater = "ambient.in.water"
    HurtInWater = "hurt.in.water"
    DeathInWater = "death.in.water"
    Jump = "jump"
    Mad = "mad"
    Stare = "stare"
    Flap = "flap"
    Fizz = "fizz"
    Sniff = "sniff"
    Screech = "screech"
    Sleep = "sleep"
    Spit = "spit"
    Scream = "scream"
    Warn = "warn"
    Shoot = "shoot"
    GuardianFlop = "guardian.flop"
    Flop = "flop"
    CastSpell = "cast.spell"
    PrepareAttack = "prepare.attack"
    PrepareSummon = "prepare.summon"
    PrepareWololo = "prepare.wololo"
    AmbientInRaid = "ambient.in.raid"
    Celebrate = "celebrate"
    Fang = "fang"
    Charge = "charge"
    Armor = "armor"
    AddChest = "add.chest"
    Saddle = "saddle"
    Land = "land"
    Throw = "throw"
    AttackStrong = "attack.strong"
    Roar = "roar"
    Stun = "stun"
    Thunder = "thunder"
    Explode = "explode"
    Fly = "fly"
    ImitateBlaze = "imitate.blaze"
    ImitateCaveSpider = "imitate.cave_spider"
    ImitateCreeper = "imitate.creeper"
    ImitateElderGuardian = "imitate.elder_guardian"
    ImitateEnderDragon = "imitate.ender_dragon"
    ImitateEnderman = "imitate.enderman"
    ImitateEndermite = "imitate.endermite"
    ImitateEvocationIllager = "imitate.evocation_illager"
    ImitateGhast = "imitate.ghast"
    ImitateHusk = "imitate.husk"
    ImitateIllusionIllager = "imitate.illusion_illager"
    ImitateMagmaCube = "imitate.magma_cube"
    ImitatePolarBear = "imitate.polar_bear"
    ImitatePanda = "imitate.panda"
    ImitateShulker = "imitate.shulker"
    ImitateSilverfish = "imitate.silverfish"
    ImitateSkeleton = "imitate.skeleton"
    ImitateSlime = "imitate.slime"
    ImitateSpider = "imitate.spider"
    ImitateStray = "imitate.stray"
    ImitateVex = "imitate.vex"
    ImitateVindicationIllager = "imitate.vindication_illager"
    ImitateWitch = "imitate.witch"
    ImitateWither = "imitate.wither"
    ImitateWitherSkeleton = "imitate.wither_skeleton"
    ImitateWolf = "imitate.wolf"
    ImitateZombie = "imitate.zombie"
    ImitateDrowned = "imitate.drowned"
    ImitateZombiePigman = "imitate.zombie_pigman"
    ImitateZombieVillager = "imitate.zombie_villager"
    Swoop = "swoop"
    Boost = "boost"
    DeathToZombie = "death.to.zombie"
    AttackNodamage = "attack.nodamage"
    ElderguardianCurse = "elderguardian.curse"
    AmbientBaby = "ambient.baby"
    MobWarning = "mob.warning"
    AmbientAggressive = "ambient.aggressive"
    AmbientWorried = "ambient.worried"
    Presneeze = "presneeze"
    Sneeze = "sneeze"
    CantBreed = "cant_breed"
    ShulkerOpen = "shulker.open"
    ShulkerClose = "shulker.close"
    HurtBaby = "hurt.baby"
    DeathBaby = "death.baby"
    StepBaby = "step.baby"
    Born = "born"
    SquishBig = "squish.big"
    SquishSmall = "squish.small"
    Haggle = "haggle"
    HaggleYes = "haggle.yes"
    HaggleNo = "haggle.no"
    Disappeared = "disappeared"
    Drink = "drink"
    Reappeared = "reappeared"
    DeathMinVolume = "death.min.volume"
    DeathMidVolume = "death.mid.volume"
    Spawn = "spawn"
    BreakBlock = "break.block"
    Shake = "shake"
    Growl = "growl"
    Whine = "whine"
    Pant = "pant"


class BlockSoundEvent(StrEnum):
    BreakPot = "break_pot"
    Break = "break"
    ButtonClickOff = "button.click_off"
    ButtonClickOn = "button.click_on"
    Default = "default"
    DoorClose = "door.close"
    DoorOpen = "door.open"
    Fall = "fall"
    FenceGateClose = "fence_gate.close"
    FenceGateOpen = "fence_gate.open"
    Hit = "hit"
    ItemUseOn = "item.use.on"
    Place = "place"
    PowerOff = "power.off"
    PowerOn = "power.on"
    PressurePlateClickOff = "pressure_plate.click_off"
    PressurePlateClickOn = "pressure_plate.click_on"
    ShatterPot = "shatter_pot"
    Step = "step"
    TrapdoorClose = "trapdoor.close"
    TrapdoorOpen = "trapdoor.open"


class BlockInteractiveSoundEvent(StrEnum):
    Default = "default"
    Fall = "fall"
    Jump = "jump"
    Land = "land"
    Step = "step"


class BlockSoundGroup(StrEnum):
    """The vanilla block sound groups, the ones `blocks.json` gives vanilla blocks (oak planks use
    `Wood`). They hold every sound event of a block: break, place, step, door and button clicks.
    """

    AmethystBlock = "amethyst_block"
    AmethystCluster = "amethyst_cluster"
    AncientDebris = "ancient_debris"
    Anvil = "anvil"
    Azalea = "azalea"
    AzaleaLeaves = "azalea_leaves"
    Bamboo = "bamboo"
    BambooSapling = "bamboo_sapling"
    BambooWood = "bamboo_wood"
    BambooWoodHangingSign = "bamboo_wood_hanging_sign"
    Basalt = "basalt"
    BigDripleaf = "big_dripleaf"
    BoneBlock = "bone_block"
    CactusFlower = "cactus_flower"
    Calcite = "calcite"
    Candle = "candle"
    CaveVines = "cave_vines"
    Chain = "chain"
    CherryLeaves = "cherry_leaves"
    CherryWood = "cherry_wood"
    CherryWoodHangingSign = "cherry_wood_hanging_sign"
    ChiseledBookshelf = "chiseled_bookshelf"
    Cinnabar = "cinnabar"
    Cloth = "cloth"
    Comparator = "comparator"
    Copper = "copper"
    CopperBulb = "copper_bulb"
    CopperChest = "copper_chest"
    CopperChestOxidized = "copper_chest_oxidized"
    CopperChestWeathered = "copper_chest_weathered"
    CopperGolemStatue = "copper_golem_statue"
    CopperGrate = "copper_grate"
    Coral = "coral"
    CreakingHeart = "creaking_heart"
    Deadbush = "deadbush"
    DecoratedPot = "decorated_pot"
    Deepslate = "deepslate"
    DeepslateBricks = "deepslate_bricks"
    DirtWithRoots = "dirt_with_roots"
    DriedGhast = "dried_ghast"
    DripstoneBlock = "dripstone_block"
    Eyeblossom = "eyeblossom"
    FireflyBush = "firefly_bush"
    FrogSpawn = "frog_spawn"
    Froglight = "froglight"
    Fungus = "fungus"
    Glass = "glass"
    GlowLichen = "glow_lichen"
    Grass = "grass"
    Gravel = "gravel"
    HangingRoots = "hanging_roots"
    HangingSign = "hanging_sign"
    HeavyCore = "heavy_core"
    HoneyBlock = "honey_block"
    Iron = "iron"
    Itemframe = "itemframe"
    Ladder = "ladder"
    Lantern = "lantern"
    LargeAmethystBud = "large_amethyst_bud"
    LeafLitter = "leaf_litter"
    Lever = "lever"
    Lodestone = "lodestone"
    MangroveRoots = "mangrove_roots"
    MediumAmethystBud = "medium_amethyst_bud"
    Metal = "metal"
    MobSpawner = "mob_spawner"
    MossBlock = "moss_block"
    MossCarpet = "moss_carpet"
    Mud = "mud"
    MudBricks = "mud_bricks"
    MuddyMangroveRoots = "muddy_mangrove_roots"
    NetherBrick = "nether_brick"
    NetherGoldOre = "nether_gold_ore"
    NetherSprouts = "nether_sprouts"
    NetherWart = "nether_wart"
    NetherWood = "nether_wood"
    NetherWoodHangingSign = "nether_wood_hanging_sign"
    Netherite = "netherite"
    Netherrack = "netherrack"
    Normal = "normal"
    Nylium = "nylium"
    PackedMud = "packed_mud"
    PaleHangingMoss = "pale_hanging_moss"
    PinkPetals = "pink_petals"
    PointedDripstone = "pointed_dripstone"
    PolishedTuff = "polished_tuff"
    PoplarLeaves = "poplar_leaves"
    PotentSulfur = "potent_sulfur"
    PowderSnow = "powder_snow"
    RedShrub = "red_shrub"
    Resin = "resin"
    ResinBrick = "resin_brick"
    Roots = "roots"
    Sand = "sand"
    Scaffolding = "scaffolding"
    Sculk = "sculk"
    SculkCatalyst = "sculk_catalyst"
    SculkSensor = "sculk_sensor"
    SculkShrieker = "sculk_shrieker"
    SculkVein = "sculk_vein"
    Shelf = "shelf"
    ShelfMushroom = "shelf_mushroom"
    Shroomlight = "shroomlight"
    Slime = "slime"
    SmallAmethystBud = "small_amethyst_bud"
    Snow = "snow"
    SoulSand = "soul_sand"
    SoulSoil = "soul_soil"
    Sponge = "sponge"
    SporeBlossom = "spore_blossom"
    Stem = "stem"
    Stone = "stone"
    StrawBed = "straw_bed"
    Sulfur = "sulfur"
    SulfurSpike = "sulfur_spike"
    SuspiciousGravel = "suspicious_gravel"
    SuspiciousSand = "suspicious_sand"
    SweetBerryBush = "sweet_berry_bush"
    Terracotta = "terracotta"
    TrialSpawner = "trial_spawner"
    Tuff = "tuff"
    TuffBricks = "tuff_bricks"
    TurtleEgg = "turtle_egg"
    Vault = "vault"
    Vines = "vines"
    Web = "web"
    WeepingVines = "weeping_vines"
    WetSponge = "wet_sponge"
    Wood = "wood"


class MusicCategory(StrEnum):
    """
    Enumeration for the different categories of music in the game.
    """

    Creative = "creative"
    Credits = "credits"
    Crimson_forest = "crimson_forest"
    Dripstone_caves = "dripstone_caves"
    End = "end"
    Endboss = "endboss"
    Frozen_peaks = "frozen_peaks"
    Game = "game"
    Grove = "grove"
    Hell = "hell"
    Jagged_peaks = "jagged_peaks"
    Lush_caves = "lush_caves"
    Meadow = "meadow"
    Menu = "menu"
    Nether = "nether"
    Snowy_slopes = "snowy_slopes"
    Soulsand_valley = "soulsand_valley"
    Stony_peaks = "stony_peaks"
    Water = "water"


class SmeltingTags(StrEnum):
    FURNACE = "furnace"
    BLAST_FURNACE = "blast_furnace"
    SMOKER = "smoker"
    CAMPFIRE = "campfire"
    SOUL_CAMPFIRE = "soul_campfire"


class ContainerType(StrEnum):
    Horse = "horse"
    MinecartChest = "minecart_chest"
    ChestBoat = "chest_boat"
    MinecartHopper = "minecart_hopper"
    Inventory = "inventory"
    Container = "container"
    Hopper = "hopper"


class EnchantsSlots(StrEnum):
    """
    Enumeration of enchantment slots available in Minecraft.

    This enum defines all possible equipment slots that can receive enchantments,
    organized by equipment type and usage category.

    Armor Slots:
        ArmorHead: Helmet slot enchantments
        ArmorTorso: Chestplate slot enchantments
        ArmorLegs: Leggings slot enchantments
        ArmorFeet: Boots slot enchantments
        GArmor: General armor enchantments (applicable to any armor piece)

    Weapon Slots:
        Sword: Sword-specific enchantments
        Bow: Bow-specific enchantments
        Spear: Spear/trident enchantments
        Crossbow: Crossbow-specific enchantments
        MeleeSpear: Melee trident enchantments

    Tool Slots:
        GTool: General tool enchantments (applicable to multiple tool types)
        Hoe: Hoe-specific enchantments
        Shears: Shears-specific enchantments
        Flintandsteel: Flint and steel enchantments
        Shield: Shield-specific enchantments

    Digging Tools:
        GDigging: General digging tool enchantments
        Axe: Axe-specific enchantments
        Pickaxe: Pickaxe-specific enchantments
        Shovel: Shovel-specific enchantments

    Special Items:
        FishingRod: Fishing rod enchantments
        CarrotStick: Carrot on a stick enchantments
        Elytra: Elytra wing enchantments
        CosmeticHead: Cosmetic head item enchantments
    """

    ArmorHead = "armor_head"
    ArmorTorso = "armor_torso"
    ArmorLegs = "armor_legs"
    ArmorFeet = "armor_feet"
    GArmor = "g_armor"
    Sword = "sword"
    Bow = "bow"
    Spear = "spear"
    Crossbow = "crossbow"
    MeleeSpear = "melee_spear"
    GTool = "g_tool"
    Hoe = "hoe"
    Shears = "shears"
    Flintandsteel = "flintsteel"
    Shield = "shield"
    GDigging = "g_digging"
    Axe = "axe"
    Pickaxe = "pickaxe"
    Shovel = "shovel"
    FishingRod = "fishing_rod"
    CarrotStick = "carrot_stick"
    Elytra = "elytra"
    CosmeticHead = "cosmetic_head"


class ExplosionParticleEffect(StrEnum):
    Explosion = "explosion"
    WindBurst = "wind_burst"
    BreezeWindBurst = "breeze_wind_burst"


class DamageSensor(StrEnum):
    Yes = "yes"
    No = "no"
    NoButSideEffectsApply = "no_but_side_effects_apply"
    NoButEntityEffectsApply = "no_but_entity_effects_apply"


class LineOfSightObstructionType(StrEnum):
    Outline = "outline"
    Collision = "collision"
    CollisionForCamera = "collision_for_camera"


class LookAtLocation(StrEnum):
    Head = "head"
    Body = "body"
    Feet = "feet"


class LootedAtSetTarget(StrEnum):
    Never = "never"
    OnceAndStopScanning = "once_and_stop_scanning"
    OnceAndKeepScanning = "once_and_keep_scanning"


class AimAssistTargetMode(StrEnum):
    Distance = "distance"
    Angle = "angle"


class BlockLiquidDetectionTouching(StrEnum):
    Blocking = "blocking"
    Broken = "broken"
    Popped = "popped"
    NoReaction = "no_reaction"


class InputModes(StrEnum):
    KeyboardAndMouse = "keyboard_and_mouse"
    Touch = "touch"
    Gamepad = "gamepad"
    MotionController = "motion_controller"


class RecipeUnlockContext(StrEnum):
    AlwaysUnlocked = "AlwaysUnlocked"
    PlayerInWater = "PlayerInWater"
    PlayerHasManyItems = "PlayerHasManyItems"


class RideableDismountMode(StrEnum):
    """
    Enumeration for the different modes of dismounting a rideable entity in Minecraft.
    """

    Default = "default"
    OnTopCenter = "on_top_center"
    LookDirection = "look_direction"


class LeashSpringType(StrEnum):
    """
    Enumeration for the different types of leash springs in Minecraft.

    Bouncy: Simulates a highly elastic spring that never reaches an equilibrium if the leashed entity is suspended mid-air.
    Dampened: Simulates a dampened spring attached to the front of the leashed entity's collision. It reaches an equilibrium if the entity is suspended mid-air and aligns with the movement direction.
    QuadDampened: Simulates four dampened springs connected to the center of each side of the entities' collisions. It reaches an equilibrium if the entity is suspended mid-air and gradually aligns with the leash holder over time.
    """

    Bouncy = "bouncy"
    Dampened = "dampened"
    QuadDampened = "quad_dampened"


class ExplorationMapDestinations(StrEnum):
    BuriedTreasure = "buriedtreasure"
    EndCity = "endcity"
    Fortress = "fortress"
    Mansion = "mansion"
    Mineshaft = "mineshaft"
    Monument = "monument"
    PillagerOutpost = "pillageroutpost"
    Ruins = "ruins"
    Shipwreck = "shipwreck"
    Stronghold = "stronghold"
    Temple = "temple"
    Village = "village"


class PlayerAbilities(StrEnum):
    FlySpeed = "flySpeed"
    Flying = "flying"
    Instabuild = "instabuild"
    Invulnerable = "invulnerable"
    Lightning = "lightning"
    Mayfly = "mayfly"
    Mute = "mute"
    Noclip = "noclip"
    VerticalFlySpeed = "verticalFlySpeed"
    WalkSpeed = "walkSpeed"
    Worldbuilder = "worldbuilder"


class FeatureRulePlacementPass(StrEnum):
    """
    Enumeration for the different feature rule placement passes in Minecraft.

    """

    PregenerationPass = "pregeneration_pass"
    FirstPass = "first_pass"
    BeforeUndergroundPass = "before_underground_pass"
    UndergroundPass = "underground_pass"
    AfterUndergroundPass = "after_underground_pass"
    BeforeSurfacePass = "before_surface_pass"
    SurfacePass = "surface_pass"
    AfterSurfacePass = "after_surface_pass"
    BeforeSkyPass = "before_sky_pass"
    SkyPass = "sky_pass"
    AfterSkyPass = "after_sky_pass"
    FinalPass = "final_pass"


# region JSON UI


class UIBindingType(StrEnum):
    """Enumeration of UI binding types for data connections.

    Binding types determine how UI elements connect to data sources
    and how they respond to data changes.

    Attributes:
        View: Binds to view-level data (element properties)
        Global: Binds to global game data
        Collection: Binds to collection data (arrays, lists)
        CollectionDetails: Binds to specific collection item details
        NONE: No binding applied
    """

    View = "view"
    Global = "global"
    Collection = "collection"
    CollectionDetails = "collection_details"
    NONE = "none"


class UIElementType(StrEnum):
    """Enumeration of UI element types.

    Defines the different types of UI elements that can be created
    within the framework.

    Attributes:
        Image: Image element for displaying textures
        Panel: Container element for grouping other elements
        Label: Text display element
        Screen: Top-level screen container
        Factory: Dynamic element generator
        StackPanel: Container that arranges children in a stack
        Grid: Container that arranges children in a grid layout
        Custom: Custom renderer element
        Button: Interactive button element
        CollectionPanel: A stack panel for collections that does not stack its children
        InputPanel: A panel that accepts input
        Toggle: A toggle with a checked and an unchecked state
        Dropdown: A toggle that opens a dropdown
        Slider: A range input
        SliderBox: The handle of a slider
        EditBox: A text field
        ScrollView: A scrolling panel
        ScrollbarTrack: The track of a scrollbar
        ScrollbarBox: The handle of a scrollbar
        SelectionWheel: A selection wheel
    """

    Image = "image"
    Panel = "panel"
    Label = "label"
    Screen = "screen"
    Factory = "factory"
    StackPanel = "stack_panel"
    Grid = "grid"
    Custom = "custom"
    Button = "button"
    CollectionPanel = "collection_panel"
    InputPanel = "input_panel"
    Toggle = "toggle"
    Dropdown = "dropdown"
    Slider = "slider"
    SliderBox = "slider_box"
    EditBox = "edit_box"
    ScrollView = "scroll_view"
    ScrollbarTrack = "scrollbar_track"
    ScrollbarBox = "scrollbar_box"
    SelectionWheel = "selection_wheel"


class UIAnchor(StrEnum):
    """Enumeration of anchor positions for UI element layout.

    Anchors determine how elements are positioned relative to their
    parent containers.

    Attributes:
        Center: Center position
        TopLeft: Top-left corner
        TopMiddle: Top center
        TopRight: Top-right corner
        LeftMiddle: Left center
        RightMiddle: Right center
        BottomLeft: Bottom-left corner
        BottomMiddle: Bottom center
        BottomRight: Bottom-right corner
    """

    Center = "center"
    TopLeft = "top_left"
    TopMiddle = "top_middle"
    TopRight = "top_right"
    LeftMiddle = "left_middle"
    RightMiddle = "right_middle"
    BottomLeft = "bottom_left"
    BottomMiddle = "bottom_middle"
    BottomRight = "bottom_right"


class UITextAlignment(StrEnum):
    """Enumeration of text alignment options.

    Defines how text content is aligned within text elements.

    Attributes:
        Center: Center-aligned text
        Left: Left-aligned text
        Right: Right-aligned text
    """

    Center = "center"
    Left = "left"
    Right = "right"


class UIAnimType(StrEnum):
    """Enumeration of animation types.

    Defines the different types of animations that can be applied
    to UI elements.

    Attributes:
        Alpha: Transparency/opacity animation
        Clip: Clipping animation
        Color: Color transition animation
        Flip_book: Frame-based flipbook animation
        Offset: Position offset animation
        Size: Size scaling animation
        UV: Texture coordinate animation
        Wait: Pause/delay animation
        Aseprite_flip_book: Aseprite-based flipbook animation
    """

    Alpha = "alpha"
    Clip = "clip"
    Color = "color"
    Flip_book = "flip_book"
    Offset = "offset"
    Size = "size"
    UV = "uv"
    Wait = "wait"
    Aseprite_flip_book = "aseprite_flip_book"


class UIEasing(StrEnum):
    """Enumeration of easing functions for animations.

    Easing functions control the rate of change in animations,
    providing smooth transitions and natural motion effects.

    Attributes:
        Linear: Constant rate of change
        Spring: Spring-like motion
        InQuad, OutQuad, InOutQuad: Quadratic easing variations
        InCubic, OutCubic, InOutCubic: Cubic easing variations
        InQuart, OutQuart, InOutQuart: Quartic easing variations
        InQuint, OutQuint, InOutQuint: Quintic easing variations
        InSine, OutSine, InOutSine: Sinusoidal easing variations
        InExpo, OutExpo, InOutExpo: Exponential easing variations
        InCirc, OutCirc, InOutCirc: Circular easing variations
        InBounce, OutBounce, InOutBounce: Bouncing easing variations
        InBack, OutBack, InOutBack: Back easing variations
        InElastic, OutElastic, InOutElastic: Elastic easing variations
    """

    Linear = "linear"
    Spring = "spring"
    InQuad = "in_quad"
    OutQuad = "out_quad"
    InOutQuad = "in_out_quad"
    InCubic = "in_cubic"
    OutCubic = "out_cubic"
    InOutCubic = "in_out_cubic"
    InQuart = "in_quart"
    OutQuart = "out_quart"
    InOutQuart = "in_out_quart"
    InQuint = "in_quint"
    OutQuint = "out_quint"
    InOutQuint = "in_out_quint"
    InSine = "in_sine"
    OutSine = "out_sine"
    InOutSine = "in_out_sine"
    InExpo = "in_expo"
    OutExpo = "out_expo"
    InOutExpo = "in_out_expo"
    InCirc = "in_circ"
    OutCirc = "out_circ"
    InOutCirc = "in_out_circ"
    InBounce = "in_bounce"
    OutBounce = "out_bounce"
    InOutBounce = "in_out_bounce"
    InBack = "in_back"
    OutBack = "out_back"
    InOutBack = "in_out_back"
    InElastic = "in_elastic"
    OutElastic = "out_elastic"
    InOutElastic = "in_out_elastic"


class UIElementTrigger(StrEnum):
    """Enumeration of trigger types for UI element activation.

    Defines when and how UI elements are triggered to appear or activate.

    Attributes:
        Title: Triggered by title/subtitle display
        Actionbar: Triggered by actionbar message display
        NONE: No trigger (always active or manually controlled)
    """

    Title = "title"
    Actionbar = "actionbar"
    NONE = "None"


class UIFontSize(StrEnum):
    """Enumeration of font size options.

    Defines the available font sizes for text elements.

    Attributes:
        Normal: Standard font size
        Small: Smaller font size
        Large: Larger font size
        ExtraLarge: Extra large font size
    """

    Normal = "normal"
    Small = "small"
    Large = "large"
    ExtraLarge = "extra_large"


# endregion
# region Kit


class SupportedBy(StrEnum):
    """Where the block holding up a supported block is."""

    Below = "below"
    """The block below."""
    BlockFace = "block_face"
    """The block it was placed against, read from `minecraft:block_face`."""
    Facing = "facing"
    """The block its `minecraft:cardinal_direction` points at."""
    Sign = "sign"
    """The block below when its `standing` state is on, otherwise the block its
    `minecraft:cardinal_direction` points at."""


# endregion
