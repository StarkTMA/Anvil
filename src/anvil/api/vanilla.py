import os
from ast import Interactive
from enum import Enum

import commentjson as json
import requests

from anvil import ANVIL, CONFIG
from anvil.api.enums import Dimension
from anvil.lib.lib import File, FileExists

ENTITY_LIST: dict[str, "Entities.VanillaEntity"] = {}
ITEMS_LIST = []
BLOCK_LIST = []


class Entities:
    class VanillaEntity():
        def __init__(self, name : str, is_mob: bool = True, is_vanilla: bool = True, allow_runtime: bool = True) -> None:
            super().__init__()
            ENTITY_LIST[name] = self
            self.is_mob = is_mob
            self.namespace = 'minecraft' if is_vanilla else CONFIG.NAMESPACE
            self.name = name
            self.allow_runtime = allow_runtime
            self._github_name = name

        def _set_github_name(self, name):
            self._github_name = name

        def get_vanilla_resource(self):
            cache_path = os.path.join("assets", "cache", f"{self.name}.entity.json")
            data = {}
            if FileExists(cache_path):
                with open(cache_path, "r") as file:
                    data = json.loads(file.read())
            else:
                retrieve = requests.get(
                    f"https://raw.githubusercontent.com/Mojang/bedrock-samples/main/resource_pack/entity/{self._github_name}.entity.json"
                )
                data = json.loads(retrieve.text)
                File(f"{self.name}.entity.json", data, os.path.join("assets", "cache"), "w", True)
                
            return data

        @property
        def identifier(self):
            return self.namespace + ':' + self.name
        
        def __str__(self) -> str:
            return self.name
        
        def __eq__(self, __value: object) -> bool:
            return __value == (self.namespace + ':' + self.name)

        def __iter__(self):
            yield self.name
    
    # Added in 1.21.51
    Creaking = VanillaEntity("creaking")
    # Added in 1.21.30
    WindChargeParticle = VanillaEntity("wind_charge_particle")
    # Added in 1.21
    Bogged = VanillaEntity("bogged")
    Breeze = VanillaEntity("breeze")
    
    # Added in 1.20.80
    Armadillo = VanillaEntity("armadillo")

    Agent = VanillaEntity("agent", False)
    Allay = VanillaEntity("allay")
    ArmorStand = VanillaEntity("armor_stand", False)._set_github_name("armor_stand.v1.0")
    Arrow = VanillaEntity("arrow", False)
    Axolotl = VanillaEntity("axolotl")
    Bat = VanillaEntity("bat")
    Bed = VanillaEntity("bed", False)
    Bee = VanillaEntity("bee")
    Blaze = VanillaEntity("blaze")._set_github_name("blaze.v1.0")
    Boat = VanillaEntity("boat", False)
    Camel = VanillaEntity("camel")
    Cat = VanillaEntity("cat")
    CaveSpider = VanillaEntity("cave_spider")._set_github_name("cave_spider.v1.0")
    ChestBoat = VanillaEntity("chest_boat", False)
    ChestMinecart = VanillaEntity("chest_minecart", False)._set_github_name("chest_minecart.v1.0")
    Chicken = VanillaEntity("chicken")._set_github_name("chicken.v1.0")
    Cod = VanillaEntity("cod")
    CommandBlockMinecart = VanillaEntity("command_block_minecart", False)._set_github_name("command_block_minecart.v1.0")
    Cow = VanillaEntity("cow")._set_github_name("cow.v1.0")
    Creeper = VanillaEntity("creeper")._set_github_name("creeper.v1.0")
    DecoratedPot = VanillaEntity("decorated_pot", False)
    Dolphin = VanillaEntity("dolphin")
    Donkey = VanillaEntity("donkey")._set_github_name("donkey_v3")
    DragonFireball = VanillaEntity("dragon_fireball", False)
    Drowned = VanillaEntity("drowned")._set_github_name("drowned.v1.0")
    Egg = VanillaEntity("egg", False)
    ElderGuardian = VanillaEntity("elder_guardian")
    EnderCrystal = VanillaEntity("ender_crystal", False)
    EnderDragon = VanillaEntity("ender_dragon")
    EnderEye = VanillaEntity("ender_eye", False)
    EnderPearl = VanillaEntity("ender_pearl", False)
    Enderman = VanillaEntity("enderman")._set_github_name("enderman.v1.0")
    Endermite = VanillaEntity("endermite")
    EvocationFangs = VanillaEntity("evocation_fangs", False)
    EvocationIllager = VanillaEntity("evocation_illager")._set_github_name("evocation_illager.v1.0")
    ExperienceBottle = VanillaEntity("experience_bottle", False)
    ExperienceOrb = VanillaEntity("experience_orb", False)
    Fireball = VanillaEntity("fireball")
    FireworkRocket = VanillaEntity("firework_rocket", False)
    FishingHook = VanillaEntity("fishing_hook")
    Fox = VanillaEntity("fox")
    Frog = VanillaEntity("frog")
    Ghast = VanillaEntity("ghast")
    GlowSquid = VanillaEntity("glow_squid")
    Goat = VanillaEntity("goat")
    Guardian = VanillaEntity("guardian")
    Hoglin = VanillaEntity("hoglin")
    HopperMinecart = VanillaEntity("hopper_minecart", False)._set_github_name("hopper_minecart.v1.0")
    Horse = VanillaEntity("horse")._set_github_name("horse_v3")
    Husk = VanillaEntity("husk")._set_github_name("husk.v1.0")
    IronGolem = VanillaEntity("iron_golem")
    LeashKnot = VanillaEntity("leash_knot", False)
    LingeringPotion = VanillaEntity("lingering_potion", False)
    Llama = VanillaEntity("llama")._set_github_name("llama.v1.0")
    LlamaSpit = VanillaEntity("llama_spit")
    MagmaCube = VanillaEntity("magma_cube")
    Minecart = VanillaEntity("minecart", False)._set_github_name("minecart.v1.0")
    Mooshroom = VanillaEntity("mooshroom")._set_github_name("mooshroom.v1.0")
    Mule = VanillaEntity("mule")._set_github_name("mule_v3")
    Npc = VanillaEntity("npc")
    Ocelot = VanillaEntity("ocelot")._set_github_name("ocelot.v1.0")
    Panda = VanillaEntity("panda")
    Parrot = VanillaEntity("parrot")
    Phantom = VanillaEntity("phantom")
    Pig = VanillaEntity("pig")._set_github_name("pig.v1.0")
    Piglin = VanillaEntity("piglin")
    PiglinBrute = VanillaEntity("piglin_brute")
    Pillager = VanillaEntity("pillager")
    Player = VanillaEntity("player")
    PolarBear = VanillaEntity("polar_bear")
    Pufferfish = VanillaEntity("pufferfish")._set_github_name("pufferfish.v1.0")
    Rabbit = VanillaEntity("rabbit")._set_github_name("rabbit.v1.0")
    Ravager = VanillaEntity("ravager")
    Salmon = VanillaEntity("salmon")
    Sheep = VanillaEntity("sheep")._set_github_name("sheep.v1.0")
    Shulker = VanillaEntity("shulker")._set_github_name("shulker.v1.0")
    ShulkerBullet = VanillaEntity("shulker_bullet")
    Silverfish = VanillaEntity("silverfish")
    Skeleton = VanillaEntity("skeleton")._set_github_name("skeleton.v1.0")
    SkeletonHorse = VanillaEntity("skeleton_horse")._set_github_name("skeleton_horse_v3")
    Skull = VanillaEntity("skull", False)
    Slime = VanillaEntity("slime")
    SmallFireball = VanillaEntity("small_fireball")
    Sniffer = VanillaEntity("sniffer")
    Snowball = VanillaEntity("snowball", False)
    SnowGolem = VanillaEntity("snow_golem")._set_github_name("snow_golem.v1.0")
    Spider = VanillaEntity("spider")._set_github_name("spider.v1.0")
    SplashPotion = VanillaEntity("splash_potion", False)
    Squid = VanillaEntity("squid")
    Stray = VanillaEntity("stray")._set_github_name("stray.v1.0")
    Strider = VanillaEntity("strider")
    Tadpole = VanillaEntity("tadpole")
    ThrownTrident = VanillaEntity("thrown_trident")
    TntMinecart = VanillaEntity("tnt_minecart", False)._set_github_name("tnt_minecart.v1.0")
    TraderLlama = VanillaEntity("trader_llama")
    TripodCamera = VanillaEntity("tripod_camera", False)
    Tropicalfish = VanillaEntity("tropicalfish")
    Turtle = VanillaEntity("turtle")
    Vex = VanillaEntity("vex")._set_github_name("vex.v1.0")
    Villager = VanillaEntity("villager_v2")
    Vindicator = VanillaEntity("vindicator")._set_github_name("vindicator.v1.0")
    WanderingTrader = VanillaEntity("wandering_trader")
    Warden = VanillaEntity("warden")
    Witch = VanillaEntity("witch")._set_github_name("witch.v1.0")
    Wither = VanillaEntity("wither")._set_github_name("wither.v1.0")
    WitherSkeleton = VanillaEntity("wither_skeleton")._set_github_name("wither_skeleton.v1.0")
    WitherSkull = VanillaEntity("wither_skull")
    WitherSkullDangeroud = VanillaEntity("wither_skull_dangerous")
    Wolf = VanillaEntity("wolf")
    Zoglin = VanillaEntity("zoglin")
    Zombie = VanillaEntity("zombie")._set_github_name("zombie.v1.0")
    ZombieHorse = VanillaEntity("zombie_horse")._set_github_name("zombie_horse_v3")
    ZombieVillager = VanillaEntity("zombie_villager_v2")


# Updated on 05-04-2023
# Latest Updated release: 1.19.81.01
class BlockStates:
    class VaultState(Enum):
        Active = "active"
        Ejecting = "ejecting"
        Interactive = "interactive"
        Unlocking = "unlocking"

    class TrialSpawnerState(Enum):
        ENUM5 = "5"
        ENUM4 = "4"
        ENUM3 = "3"
        ENUM2 = "2"
        ENUM1 = "1"
        ENUM0 = "0"

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

    class PropaguleStage(Enum):
        ENUM0 = "0"
        ENUM1 = "1"
        ENUM2 = "2"
        ENUM3 = "3"
        ENUM4 = "4"

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

        @property
        def identifier(self):
            return f'{self._namespace}:{self._name}'
        
        def __str__(self) -> str:
            return self.identifier
        
    # Waiting to be added
    # - Piglin Mob Head
    # Added in 1.21
    Mace = _basic_item("mace")
    OminousBottle = _basic_item("ominous_bottle")
    WindCharge = _basic_item("wind_charge")
    TrialKey = _basic_item("trial_key")
    OminousTrialKey = _basic_item("ominous_trial_key")
    BreezeRod = _basic_item("breeze_rod")
    TrialSpawner = _basic_item("trial_spawner")
    
    FlowPotteryShard = _basic_item("flow_pottery_shard")
    GusterPotteryShard = _basic_item("guster_pottery_shard")
    ScrapePotteryShard = _basic_item("scrape_pottery_shard")

    FlowBannerPattern = _basic_item('flow_banner_pattern')
    GlobeBannerPattern = _basic_item('globe_banner_pattern')
    GusterBannerPattern = _basic_item('guster_banner_pattern')

    BoltArmorTrim = _basic_item('bolt_armor_trim_smithing_template')
    FlowArmorTrim = _basic_item('flow_armor_trim_smithing_template')
    
    MusicDiscCreator = _basic_item('music_disc_creator')
    MusicDiscCreatorMusicBox = _basic_item('music_disc_creator_music_box')
    MusicDiscPrecipice = _basic_item('music_disc_precipice')

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
    EnderPearl = _basic_item("ender_pearl")
    GoldIngot = _basic_item("gold_ingot")
    BlazeRod = _basic_item("blaze_rod")
    BlazePowder = _basic_item("blaze_powder")
    IronIngot = _basic_item("iron_ingot")
    Diamond = _basic_item("diamond")
    Gunpowder = _basic_item("gunpowder")
    AcaciaBoat = _basic_item('acacia_boat')
    AcaciaChestBoat = _basic_item('acacia_chest_boat')
    AcaciaSign = _basic_item('acacia_sign')
    AllaySpawnEgg = _basic_item('allay_spawn_egg')
    AmethystShard = _basic_item('amethyst_shard')
    Apple = _basic_item('apple')
    ArmorStand = _basic_item('armor_stand')
    AxolotlBucket = _basic_item('axolotl_bucket')
    AxolotlSpawnEgg = _basic_item('axolotl_spawn_egg')
    BakedPotato = _basic_item('baked_potato')
    BambooRaftBoat = _basic_item('bamboo_raft_boat')
    BambooRaft = _basic_item('bamboo_raft')
    BambooSign = _basic_item('bamboo_sign')
    Banner = _basic_item('banner')
    BannerPattern = _basic_item('banner_pattern')
    BatSpawnEgg = _basic_item('bat_spawn_egg')
    BeeSpawnEgg = _basic_item('bee_spawn_egg')
    BeetrootSeeds = _basic_item('beetroot_seeds')
    BeetrootSoup = _basic_item('beetroot_soup')
    BirchBoat = _basic_item('birch_boat')
    BirchChestBoat = _basic_item('birch_chest_boat')
    BirchSign = _basic_item('birch_sign')
    BlackDye = _basic_item('black_dye')
    BlazeSpawnEgg = _basic_item('blaze_spawn_egg')
    BlueDye = _basic_item('blue_dye')
    BoneMeal = _basic_item('bone_meal')
    Book = _basic_item('book')
    BordureIndentedBannerPattern = _basic_item('bordure_indented_banner_pattern')
    Bow = _basic_item('bow')
    Bowl = _basic_item('bowl')
    Bread = _basic_item('bread')
    Brick = _basic_item('brick')
    BrownDye = _basic_item('brown_dye')
    Bucket = _basic_item('bucket')
    CamelSpawnEgg = _basic_item('camel_spawn_egg')
    Carpet = _basic_item('carpet')
    Carrot = _basic_item('carrot')
    CarrotOnAStick = _basic_item('carrot_on_a_stick')
    CatSpawnEgg = _basic_item('cat_spawn_egg')
    CaveSpiderSpawnEgg = _basic_item('cave_spider_spawn_egg')
    ChainmailBoots = _basic_item('chainmail_boots')
    ChainmailChestplate = _basic_item('chainmail_chestplate')
    ChainmailHelmet = _basic_item('chainmail_helmet')
    ChainmailLeggings = _basic_item('chainmail_leggings')
    Charcoal = _basic_item('charcoal')
    CherryBoat = _basic_item('cherry_boat')
    CherryChestBoat = _basic_item('cherry_chest_boat')
    ChestMinecart = _basic_item('chest_minecart')
    ChickenSpawnEgg = _basic_item('chicken_spawn_egg')
    ChorusFruit = _basic_item('chorus_fruit')
    Clock = _basic_item('clock')
    CocoaBeans = _basic_item('cocoa_beans')
    Cod = _basic_item('cod')
    CodBucket = _basic_item('cod_bucket')
    CodSpawnEgg = _basic_item('cod_spawn_egg')
    CommandBlockMinecart = _basic_item('command_block_minecart')
    Comparator = _basic_item('comparator')
    Compass = _basic_item('compass')
    CookedCod = _basic_item('cooked_cod')
    CookedMutton = _basic_item('cooked_mutton')
    CookedPorkchop = _basic_item('cooked_porkchop')
    CookedRabbit = _basic_item('cooked_rabbit')
    CookedSalmon = _basic_item('cooked_salmon')
    Cookie = _basic_item('cookie')
    CopperIngot = _basic_item('copper_ingot')
    Coral = _basic_item('coral')
    CowSpawnEgg = _basic_item('cow_spawn_egg')
    CreeperBannerPattern = _basic_item('creeper_banner_pattern')
    CreeperSpawnEgg = _basic_item('creeper_spawn_egg')
    CrimsonSign = _basic_item('crimson_sign')
    Crossbow = _basic_item('crossbow')
    CyanDye = _basic_item('cyan_dye')
    DarkOakBoat = _basic_item('dark_oak_boat')
    DarkOakChestBoat = _basic_item('dark_oak_chest_boat')
    DarkOakSign = _basic_item('dark_oak_sign')
    DiamondAxe = _basic_item('diamond_axe')
    DiamondBoots = _basic_item('diamond_boots')
    DiamondChestplate = _basic_item('diamond_chestplate')
    DiamondHelmet = _basic_item('diamond_helmet')
    DiamondHoe = _basic_item('diamond_hoe')
    DiamondHorseArmor = _basic_item('diamond_horse_armor')
    DiamondLeggings = _basic_item('diamond_leggings')
    DiamondPickaxe = _basic_item('diamond_pickaxe')
    DiamondShovel = _basic_item('diamond_shovel')
    DiamondSword = _basic_item('diamond_sword')
    DiscFragment5 = _basic_item('disc_fragment_5')
    DolphinSpawnEgg = _basic_item('dolphin_spawn_egg')
    DonkeySpawnEgg = _basic_item('donkey_spawn_egg')
    DragonBreath = _basic_item('dragon_breath')
    DriedKelp = _basic_item('dried_kelp')
    DrownedSpawnEgg = _basic_item('drowned_spawn_egg')
    EchoShard = _basic_item('echo_shard')
    ElderGuardianSpawnEgg = _basic_item('elder_guardian_spawn_egg')
    Elytra = _basic_item('elytra')
    Emerald = _basic_item('emerald')
    EmptyMap = _basic_item('empty_map')
    EnchantedBook = _basic_item('enchanted_book')
    EnchantedGoldenApple = _basic_item('enchanted_golden_apple')
    EndCrystal = _basic_item('end_crystal')
    EnderEye = _basic_item('ender_eye')
    EndermanSpawnEgg = _basic_item('enderman_spawn_egg')
    EndermiteSpawnEgg = _basic_item('endermite_spawn_egg')
    EvokerSpawnEgg = _basic_item('evoker_spawn_egg')
    ExperienceBottle = _basic_item('experience_bottle')
    Feather = _basic_item('feather')
    FermentedSpiderEye = _basic_item('fermented_spider_eye')
    FieldMasonedBannerPattern = _basic_item('field_masoned_banner_pattern')
    FilledMap = _basic_item('filled_map')
    FireCharge = _basic_item('fire_charge')
    FireworkRocket = _basic_item('firework_rocket')
    FireworkStar = _basic_item('firework_star')
    FishingRod = _basic_item('fishing_rod')
    FlintAndSteel = _basic_item('flint_and_steel')
    FlowerBannerPattern = _basic_item('flower_banner_pattern')
    FoxSpawnEgg = _basic_item('fox_spawn_egg')
    FrogSpawnEgg = _basic_item('frog_spawn_egg')
    GhastSpawnEgg = _basic_item('ghast_spawn_egg')
    GhastTear = _basic_item('ghast_tear')
    GlassBottle = _basic_item('glass_bottle')
    GlisteringMelonSlice = _basic_item('glistering_melon_slice')
    GlowBerries = _basic_item('glow_berries')
    GlowInkSac = _basic_item('glow_ink_sac')
    GlowSquidSpawnEgg = _basic_item('glow_squid_spawn_egg')
    GlowstoneDust = _basic_item('glowstone_dust')
    GoatHorn = _basic_item('goat_horn')
    GoatSpawnEgg = _basic_item('goat_spawn_egg')
    GoldenApple = _basic_item('golden_apple')
    GoldenAxe = _basic_item('golden_axe')
    GoldenBoots = _basic_item('golden_boots')
    GoldenCarrot = _basic_item('golden_carrot')
    GoldenChestplate = _basic_item('golden_chestplate')
    GoldenHelmet = _basic_item('golden_helmet')
    GoldenHoe = _basic_item('golden_hoe')
    GoldenHorseArmor = _basic_item('golden_horse_armor')
    GoldenLeggings = _basic_item('golden_leggings')
    GoldenPickaxe = _basic_item('golden_pickaxe')
    GoldenShovel = _basic_item('golden_shovel')
    GoldenSword = _basic_item('golden_sword')
    GrayDye = _basic_item('gray_dye')
    GreenDye = _basic_item('green_dye')
    GuardianSpawnEgg = _basic_item('guardian_spawn_egg')
    HeartOfTheSea = _basic_item('heart_of_the_sea')
    HoglinSpawnEgg = _basic_item('hoglin_spawn_egg')
    HoneyBottle = _basic_item('honey_bottle')
    Honeycomb = _basic_item('honeycomb')
    HopperMinecart = _basic_item('hopper_minecart')
    HorseSpawnEgg = _basic_item('horse_spawn_egg')
    HuskSpawnEgg = _basic_item('husk_spawn_egg')
    InkSac = _basic_item('ink_sac')
    IronAxe = _basic_item('iron_axe')
    IronBoots = _basic_item('iron_boots')
    IronChestplate = _basic_item('iron_chestplate')
    IronHelmet = _basic_item('iron_helmet')
    IronHoe = _basic_item('iron_hoe')
    IronHorseArmor = _basic_item('iron_horse_armor')
    IronLeggings = _basic_item('iron_leggings')
    IronPickaxe = _basic_item('iron_pickaxe')
    IronShovel = _basic_item('iron_shovel')
    IronSword = _basic_item('iron_sword')
    JungleBoat = _basic_item('jungle_boat')
    JungleChestBoat = _basic_item('jungle_chest_boat')
    JungleSign = _basic_item('jungle_sign')
    LapisLazuli = _basic_item('lapis_lazuli')
    LavaBucket = _basic_item('lava_bucket')
    Lead = _basic_item('lead')
    LeatherBoots = _basic_item('leather_boots')
    LeatherChestplate = _basic_item('leather_chestplate')
    LeatherHelmet = _basic_item('leather_helmet')
    LeatherHorseArmor = _basic_item('leather_horse_armor')
    LeatherLeggings = _basic_item('leather_leggings')
    LightBlueDye = _basic_item('light_blue_dye')
    LightGrayDye = _basic_item('light_gray_dye')
    LimeDye = _basic_item('lime_dye')
    LingeringPotion = _basic_item('lingering_potion')
    LlamaSpawnEgg = _basic_item('llama_spawn_egg')
    Log = _basic_item('log')
    Log2 = _basic_item('log2')
    MagentaDye = _basic_item('magenta_dye')
    MagmaCream = _basic_item('magma_cream')
    MagmaCubeSpawnEgg = _basic_item('magma_cube_spawn_egg')
    MangroveBoat = _basic_item('mangrove_boat')
    MangroveChestBoat = _basic_item('mangrove_chest_boat')
    MangroveSign = _basic_item('mangrove_sign')
    MelonSeeds = _basic_item('melon_seeds')
    MelonSlice = _basic_item('melon_slice')
    MilkBucket = _basic_item('milk_bucket')
    Minecart = _basic_item('minecart')
    MojangBannerPattern = _basic_item('mojang_banner_pattern')
    MooshroomSpawnEgg = _basic_item('mooshroom_spawn_egg')
    MuleSpawnEgg = _basic_item('mule_spawn_egg')
    MushroomStew = _basic_item('mushroom_stew')
    MusicDisc11 = _basic_item('music_disc_11')
    MusicDisc13 = _basic_item('music_disc_13')
    MusicDisc5 = _basic_item('music_disc_5')
    MusicDiscBlocks = _basic_item('music_disc_blocks')
    MusicDiscCat = _basic_item('music_disc_cat')
    MusicDiscChirp = _basic_item('music_disc_chirp')
    MusicDiscFar = _basic_item('music_disc_far')
    MusicDiscMall = _basic_item('music_disc_mall')
    MusicDiscMellohi = _basic_item('music_disc_mellohi')
    MusicDiscOtherside = _basic_item('music_disc_otherside')
    MusicDiscPigstep = _basic_item('music_disc_pigstep')
    MusicDiscStal = _basic_item('music_disc_stal')
    MusicDiscStrad = _basic_item('music_disc_strad')
    MusicDiscWait = _basic_item('music_disc_wait')
    MusicDiscWard = _basic_item('music_disc_ward')
    Mutton = _basic_item('mutton')
    NameTag = _basic_item('name_tag')
    NautilusShell = _basic_item('nautilus_shell')
    NetherStar = _basic_item('nether_star')
    Netherbrick = _basic_item('netherbrick')
    NetheriteAxe = _basic_item('netherite_axe')
    NetheriteBoots = _basic_item('netherite_boots')
    NetheriteChestplate = _basic_item('netherite_chestplate')
    NetheriteHelmet = _basic_item('netherite_helmet')
    NetheriteHoe = _basic_item('netherite_hoe')
    NetheriteIngot = _basic_item('netherite_ingot')
    NetheriteLeggings = _basic_item('netherite_leggings')
    NetheritePickaxe = _basic_item('netherite_pickaxe')
    NetheriteScrap = _basic_item('netherite_scrap')
    NetheriteShovel = _basic_item('netherite_shovel')
    NetheriteSword = _basic_item('netherite_sword')
    OakBoat = _basic_item('oak_boat')
    OakChestBoat = _basic_item('oak_chest_boat')
    OakSign = _basic_item('oak_sign')
    OcelotSpawnEgg = _basic_item('ocelot_spawn_egg')
    OrangeDye = _basic_item('orange_dye')
    Painting = _basic_item('painting')
    PandaSpawnEgg = _basic_item('panda_spawn_egg')
    Paper = _basic_item('paper')
    ParrotSpawnEgg = _basic_item('parrot_spawn_egg')
    PhantomMembrane = _basic_item('phantom_membrane')
    PhantomSpawnEgg = _basic_item('phantom_spawn_egg')
    PigSpawnEgg = _basic_item('pig_spawn_egg')
    PiglinBannerPattern = _basic_item('piglin_banner_pattern')
    PiglinBruteSpawnEgg = _basic_item('piglin_brute_spawn_egg')
    PiglinSpawnEgg = _basic_item('piglin_spawn_egg')
    PillagerSpawnEgg = _basic_item('pillager_spawn_egg')
    PinkDye = _basic_item('pink_dye')
    PoisonousPotato = _basic_item('poisonous_potato')
    PolarBearSpawnEgg = _basic_item('polar_bear_spawn_egg')
    PoppedChorusFruit = _basic_item('popped_chorus_fruit')
    Porkchop = _basic_item('porkchop')
    Potato = _basic_item('potato')
    Potion = _basic_item('potion')
    PowderSnowBucket = _basic_item('powder_snow_bucket')
    PrismarineCrystals = _basic_item('prismarine_crystals')
    PrismarineShard = _basic_item('prismarine_shard')
    Pufferfish = _basic_item('pufferfish')
    PufferfishBucket = _basic_item('pufferfish_bucket')
    PufferfishSpawnEgg = _basic_item('pufferfish_spawn_egg')
    PumpkinPie = _basic_item('pumpkin_pie')
    PumpkinSeeds = _basic_item('pumpkin_seeds')
    PurpleDye = _basic_item('purple_dye')
    Quartz = _basic_item('quartz')
    Rabbit = _basic_item('rabbit')
    RabbitHide = _basic_item('rabbit_hide')
    RabbitSpawnEgg = _basic_item('rabbit_spawn_egg')
    RabbitStew = _basic_item('rabbit_stew')
    RavagerSpawnEgg = _basic_item('ravager_spawn_egg')
    RawGold = _basic_item('raw_gold')
    RawIron = _basic_item('raw_iron')
    RecoveryCompass = _basic_item('recovery_compass')
    RedDye = _basic_item('red_dye')
    Repeater = _basic_item('repeater')
    Saddle = _basic_item('saddle')
    Salmon = _basic_item('salmon')
    SalmonBucket = _basic_item('salmon_bucket')
    SalmonSpawnEgg = _basic_item('salmon_spawn_egg')
    Scute = _basic_item('scute')
    Shears = _basic_item('shears')
    SheepSpawnEgg = _basic_item('sheep_spawn_egg')
    Shield = _basic_item('shield')
    ShulkerShell = _basic_item('shulker_shell')
    ShulkerSpawnEgg = _basic_item('shulker_spawn_egg')
    SilverfishSpawnEgg = _basic_item('silverfish_spawn_egg')
    SkeletonHorseSpawnEgg = _basic_item('skeleton_horse_spawn_egg')
    SkeletonSpawnEgg = _basic_item('skeleton_spawn_egg')
    SkullBannerPattern = _basic_item('skull_banner_pattern')
    SlimeBall = _basic_item('slime_ball')
    SlimeSpawnEgg = _basic_item('slime_spawn_egg')
    Snowball = _basic_item('snowball')
    SpiderEye = _basic_item('spider_eye')
    SpiderSpawnEgg = _basic_item('spider_spawn_egg')
    SplashPotion = _basic_item('splash_potion')
    SpruceBoat = _basic_item('spruce_boat')
    SpruceChestBoat = _basic_item('spruce_chest_boat')
    SpruceSign = _basic_item('spruce_sign')
    Spyglass = _basic_item('spyglass')
    SquidSpawnEgg = _basic_item('squid_spawn_egg')
    StainedGlass = _basic_item('stained_glass')
    StainedGlassPane = _basic_item('stained_glass_pane')
    StainedHardenedClay = _basic_item('stained_hardened_clay')
    Stick = _basic_item('stick')
    StoneAxe = _basic_item('stone_axe')
    StoneHoe = _basic_item('stone_hoe')
    StonePickaxe = _basic_item('stone_pickaxe')
    StoneShovel = _basic_item('stone_shovel')
    StoneSlab = _basic_item('stone_slab')
    StoneSlab2 = _basic_item('stone_slab2')
    StoneSlab3 = _basic_item('stone_slab3')
    StoneSlab4 = _basic_item('stone_slab4')
    StoneSword = _basic_item('stone_sword')
    StraySpawnEgg = _basic_item('stray_spawn_egg')
    StriderSpawnEgg = _basic_item('strider_spawn_egg')
    Sugar = _basic_item('sugar')
    SugarCane = _basic_item('sugar_cane')
    SuspiciousStew = _basic_item('suspicious_stew')
    SweetBerries = _basic_item('sweet_berries')
    TadpoleBucket = _basic_item('tadpole_bucket')
    TadpoleSpawnEgg = _basic_item('tadpole_spawn_egg')
    TntMinecart = _basic_item('tnt_minecart')
    TotemOfUndying = _basic_item('totem_of_undying')
    Trident = _basic_item('trident')
    TropicalFish = _basic_item('tropical_fish')
    TropicalFishBucket = _basic_item('tropical_fish_bucket')
    TropicalFishSpawnEgg = _basic_item('tropical_fish_spawn_egg')
    TurtleHelmet = _basic_item('turtle_helmet')
    TurtleSpawnEgg = _basic_item('turtle_spawn_egg')
    VexSpawnEgg = _basic_item('vex_spawn_egg')
    VillagerSpawnEgg = _basic_item('villager_spawn_egg')
    VindicatorSpawnEgg = _basic_item('vindicator_spawn_egg')
    WanderingTraderSpawnEgg = _basic_item('wandering_trader_spawn_egg')
    WardenSpawnEgg = _basic_item('warden_spawn_egg')
    WarpedFungusOnAStick = _basic_item('warped_fungus_on_a_stick')
    WarpedSign = _basic_item('warped_sign')
    WaterBucket = _basic_item('water_bucket')
    WheatSeeds = _basic_item('wheat_seeds')
    WhiteDye = _basic_item('white_dye')
    WitchSpawnEgg = _basic_item('witch_spawn_egg')
    WitherSkeletonSpawnEgg = _basic_item('wither_skeleton_spawn_egg')
    WolfSpawnEgg = _basic_item('wolf_spawn_egg')
    WoodenAxe = _basic_item('wooden_axe')
    WoodenHoe = _basic_item('wooden_hoe')
    WoodenPickaxe = _basic_item('wooden_pickaxe')
    WoodenShovel = _basic_item('wooden_shovel')
    WoodenSword = _basic_item('wooden_sword')
    Wool = _basic_item('wool')
    WritableBook = _basic_item('writable_book')
    WrittenBook = _basic_item('written_book')
    YellowDye = _basic_item('yellow_dye')
    ZoglinSpawnEgg = _basic_item('zoglin_spawn_egg')
    ZombieHorseSpawnEgg = _basic_item('zombie_horse_spawn_egg')
    ZombiePigmanSpawnEgg = _basic_item('zombie_pigman_spawn_egg')
    ZombieSpawnEgg = _basic_item('zombie_spawn_egg')
    ZombieVillagerSpawnEgg = _basic_item('zombie_villager_spawn_egg')
    Redstone = _basic_item('redstone')

    ArmadilloScute = _basic_item('armadillo_scute')
    WolfArmor = _basic_item('wolf_armor')


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
        
        @property
        def blockstate(self):
            return f'{self.identifier} [{", ".join([f'"{k[1:]}":"{v.value}"' for k, v in self.states])}]'
        
        def __str__(self):
            return self.identifier
    
    # Added in 1.12
    class Crafter(_MinecraftBlock):
        def __init__(self):
            super().__init__("crafter", True)

    class TrialSpawner(_MinecraftBlock):
        def __init__(self, ominous: bool = False, trial_spawner_state: 'BlockStates.TrialSpawnerState' = None):
            self._ominous = str(ominous)
            self._trial_spawner_state = trial_spawner_state
            super().__init__("trial_spawner", True)
    
    class Vault(_MinecraftBlock):
        def __init__(self, ominous: bool = False, vault_state: 'BlockStates.VaultState' = None, cardinal_direction: 'BlockStates.CardinalDirection' = None):
            self._ominous = str(ominous)
            self._vault_state = vault_state
            self._cardinal_direction = cardinal_direction
            super().__init__("trial_spawner", True)
    
    class HeavyCore(_MinecraftBlock):
        def __init__(self):
            super().__init__("heavy_core", True)
    
    class ChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("chiseled_copper", True)

    class CopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("copper_grate", True)

    class CopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("copper_bulb", True)

    class CopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("copper_door", True)

    class CopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("copper_trapdoor", True)

    class ExposedChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("exposed_chiseled_copper", True)

    class ExposedCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("exposed_copper_grate", True)

    class ExposedCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("exposed_copper_bulb", True)

    class ExposedCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("exposed_copper_door", True)

    class ExposedCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("exposed_copper_trapdoor", True)

    class OxidizedChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("oxidized_chiseled_copper", True)

    class OxidizedCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("oxidized_copper_grate", True)

    class OxidizedCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("oxidized_copper_bulb", True)

    class OxidizedCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("oxidized_copper_door", True)

    class OxidizedCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("oxidized_copper_trapdoor", True)

    class WaxedChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_chiseled_copper", True)

    class WaxedCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_copper_grate", True)

    class WaxedCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_copper_bulb", True)

    class WaxedCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_copper_door", True)

    class WaxedCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_copper_trapdoor", True)

    class WaxedExposedChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_exposed_chiseled_copper", True)

    class WaxedExposedCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_exposed_copper_grate", True)

    class WaxedExposedCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_exposed_copper_bulb", True)

    class WaxedExposedCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_exposed_copper_door", True)

    class WaxedExposedCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_exposed_copper_trapdoor", True)

    class WaxedOxidizedChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_oxidized_chiseled_copper", True)

    class WaxedOxidizedCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_oxidized_copper_grate", True)

    class WaxedOxidizedCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_oxidized_copper_bulb", True)

    class WaxedOxidizedCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_oxidized_copper_door", True)

    class WaxedOxidizedCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_oxidized_copper_trapdoor", True)

    class WeatheredChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("weathered_chiseled_copper", True)

    class WeatheredCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("weathered_copper_grate", True)

    class WeatheredCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("weathered_copper_bulb", True)

    class WeatheredCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("weathered_copper_door", True)

    class WeatheredCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("weathered_copper_trapdoor", True)

    class WaxedWeatheredChiseledCopper(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_weathered_chiseled_copper", True)

    class WaxedWeatheredCopperGrate(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_weathered_copper_grate", True)

    class WaxedWeatheredCopperBulb(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_weathered_copper_bulb", True)

    class WaxedWeatheredCopperDoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_weathered_copper_door", True)

    class WaxedWeatheredCopperTrapdoor(_MinecraftBlock):
        def __init__(self):
            super().__init__("waxed_weathered_copper_trapdoor", True)

    class ShortGrass(_MinecraftBlock):
        def __init__(self):
            super().__init__("short_grass", True)

    class Fern(_MinecraftBlock):
        def __init__(self):
            super().__init__("fern", True)

    class Sunflower(_MinecraftBlock):
        def __init__(self):
            super().__init__("sunflower", True)

    class Lilac(_MinecraftBlock):
        def __init__(self):
            super().__init__("lilac", True)

    class TallGrass(_MinecraftBlock):
        def __init__(self):
            super().__init__("tall_grass", True)

    class LargeFern(_MinecraftBlock):
        def __init__(self):
            super().__init__("large_fern", True)

    class RoseBush(_MinecraftBlock):
        def __init__(self):
            super().__init__("rose_bush", True)

    class Peony(_MinecraftBlock):
        def __init__(self):
            super().__init__("peony", True)

    class TubeCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("tube_coral_block", True)

    class BrainCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("brain_coral_block", True)

    class Bubble_CoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("bubble_coral_block", True)

    class FireCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("fire_coral_block", True)

    class HornCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("horn_coral_block", True)

    class DeadTubeCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_tube_coral_block", True)

    class DeadBrainCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_brain_coral_block", True)

    class DeadBubble_CoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_bubble_coral_block", True)

    class DeadFireCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_fire_coral_block", True)

    class DeadHornCoralBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_horn_coral_block", True)

    class SmoothStoneSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("smooth_stone_slab", True)

    class SandstoneSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("sandstone_slab", True)

    class PetrifiedOakSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("petrified_oak_slab", True)

    class CobblestoneSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("cobblestone_slab", True)

    class BrickSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("brick_slab", True)

    class StoneBrickSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("stone_brick_slab", True)

    class QuartzSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("quartz_slab", True)

    class NetherBrickSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("nether_brick_slab", True)

    # ------------------------------------------------------------------

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
        def __init__(self, cardinal_direction: 'BlockStates.CardinalDirection' = None):
            self._cardinal_direction = cardinal_direction
            super().__init__("anvil", True)

    class ChippedAnvil(_MinecraftBlock):
        def __init__(self, cardinal_direction: 'BlockStates.CardinalDirection' = None):
            self._cardinal_direction = cardinal_direction
            super().__init__("chipped_anvil", True)

    class DamagedAnvil(_MinecraftBlock):
        def __init__(self, cardinal_direction: 'BlockStates.CardinalDirection' = None):
            self._cardinal_direction = cardinal_direction
            super().__init__("damaged_anvil", True)

    class DeprecatedAnvil(_MinecraftBlock):
        def __init__(self, cardinal_direction: 'BlockStates.CardinalDirection' = None):
            self._cardinal_direction = cardinal_direction
            super().__init__("deprecated_anvil", True)

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

    class CompoundCreator(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None):
            self._direction = direction
            super().__init__("compound_creator", True)

    class MaterialReducer(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None):
            self._direction = direction
            super().__init__("material_reducer", True)

    class ElementConstructor(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None):
            self._direction = direction
            super().__init__("element_constructor", True)

    class LabTable(_MinecraftBlock):
        def __init__(self, direction:'BlockStates.Direction'=None):
            self._direction = direction
            super().__init__("lab_table", True)

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
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("cobblestone_wall", True)

    class MossyCobblestoneWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("mossy_cobblestone_wall", True)

    class GraniteWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("granite_wall", True)

    class DioriteWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("diorite_wall", True)

    class AndesiteWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("andesite_wall", True)

    class SandstoneWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("sandstone_wall", True)

    class BrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("brick_wall", True)

    class StoneBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("stone_brick_wall", True)

    class MossyStoneBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("mossy_stone_brick_wall", True)

    class NetherBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("nether_brick_wall", True)

    class EndStoneBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("end_stone_brick_wall", True)

    class PrismarineWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("prismarine_wall", True)

    class RedSandstoneWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("red_sandstone_wall", True)

    class RedNetherBrickWall(_MinecraftBlock):
        def __init__(self, wall_connection_type_east: 'BlockStates.WallConnectionTypeEast' = None,
                    wall_connection_type_north: 'BlockStates.WallConnectionTypeNorth' = None,
                    wall_connection_type_south: 'BlockStates.WallConnectionTypeSouth' = None,
                    wall_connection_type_west: 'BlockStates.WallConnectionTypeWest' = None,
                    wall_post_bit: 'BlockStates.WallPostBit' = None):
            self._wall_connection_type_east = wall_connection_type_east
            self._wall_connection_type_north = wall_connection_type_north
            self._wall_connection_type_south = wall_connection_type_south
            self._wall_connection_type_west = wall_connection_type_west
            self._wall_post_bit = wall_post_bit
            super().__init__("red_nether_brick_wall", True)


    class Cocoa(_MinecraftBlock):
        def __init__(self, age:'BlockStates.Age'=None, direction:'BlockStates.Direction'=None):
            self._age = age
            self._direction = direction
            super().__init__("cocoa", True)
    
    class ColoredTorchRed(_MinecraftBlock):
        def __init__(self, torch_facing_direction: 'BlockStates.TorchFacingDirection' = None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("colored_torch_red", True)

    class ColoredTorchGreen(_MinecraftBlock):
        def __init__(self, torch_facing_direction: 'BlockStates.TorchFacingDirection' = None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("colored_torch_green", True)

    class ColoredTorchBlue(_MinecraftBlock):
        def __init__(self, torch_facing_direction: 'BlockStates.TorchFacingDirection' = None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("colored_torch_blue", True)

    class ColoredTorchPurple(_MinecraftBlock):
        def __init__(self, torch_facing_direction: 'BlockStates.TorchFacingDirection' = None):
            self._torch_facing_direction = torch_facing_direction
            super().__init__("colored_torch_purple", True)

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

    class TubeCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("tube_coral_wall_fan", True)

    class BrainCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("brain_coral_wall_fan", True)

    class DeadTubeCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_tube_coral_wall_fan", True)

    class DeadBrainCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_brain_coral_wall_fan", True)

    class BubbleCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("bubble_coral_wall_fan", True)

    class FireCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("fire_coral_wall_fan", True)

    class DeadBubbleCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_bubble_coral_wall_fan", True)

    class DeadFireCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_fire_coral_wall_fan", True)

    class HornCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("horn_coral_wall_fan", True)

    class DeadHornCoralWallFan(_MinecraftBlock):
        def __init__(self):
            super().__init__("dead_horn_coral_wall_fan", True)

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
        def __init__(self):
            super().__init__("dirt", True)

    class CoarseDirt(_MinecraftBlock):
        def __init__(self):
            super().__init__("coarse_dirt", True)

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

    class SmoothStoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_stone_double_slab", True)

    class SandstoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("sandstone_double_slab", True)

    class OakDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("oak_double_slab", True)

    class CobblestoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("cobblestone_double_slab", True)

    class BrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("brick_double_slab", True)

    class StoneBrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("stone_brick_double_slab", True)

    class QuartzDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("quartz_double_slab", True)

    class NetherBrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("nether_brick_double_slab", True)

    class AcaciaDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("acacia_double_slab", True)

    class BirchDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("birch_double_slab", True)

    class DarkOakDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("dark_oak_double_slab", True)

    class JungleDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("jungle_double_slab", True)

    class OakDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("oak_double_slab", True)

    class SpruceDoubleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("spruce_double_slab", True)

    class RedSandstoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_sandstone_double_slab", True)

    class PurpurDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("purpur_double_slab", True)

    class PrismarineDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("prismarine_double_slab", True)

    class DarkPrismarineDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("dark_prismarine_double_slab", True)

    class PrismarineBrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("prismarine_brick_double_slab", True)

    class MossyCobblestoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("mossy_cobblestone_double_slab", True)

    class SmoothSandstoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_sandstone_double_slab", True)

    class RedNetherBrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_nether_brick_double_slab", True)

    class EndStoneBrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("end_stone_brick_double_slab", True)

    class SmoothRedSandstoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_red_sandstone_double_slab", True)

    class PolishedAndesiteDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("polished_andesite_double_slab", True)

    class AndesiteDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("andesite_double_slab", True)

    class DioriteDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("diorite_double_slab", True)

    class PolishedDioriteDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("polished_diorite_double_slab", True)

    class GraniteDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("granite_double_slab", True)

    class PolishedGraniteDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("polished_granite_double_slab", True)

    class MossyStoneBrickDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("mossy_stone_brick_double_slab", True)

    class SmoothQuartzDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_quartz_double_slab", True)

    class NormalStoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("normal_stone_double_slab", True)

    class CutSandstoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("cut_sandstone_double_slab", True)

    class CutRedSandstoneDoubleSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("cut_red_sandstone_double_slab", True)

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

    class GrassBlock(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("grass_block", True)

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

    class OakLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("oak_leaves", True)

    class SpruceLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("spruce_leaves", True)

    class BirchLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("birch_leaves", True)

    class JungleLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("jungle_leaves", True)

    class AcaciaLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("acacia_leaves", True)

    class DarkOakLeaves(_MinecraftBlock):
        def __init__(self, persistent_bit:'BlockStates.PersistentBit'=None, update_bit:'BlockStates.UpdateBit'=None):
            self._persistent_bit = persistent_bit
            self._update_bit = update_bit
            super().__init__("dark_oak_leaves", True)

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

    class LightBlock1(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_1", True)

    class LightBlock2(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_2", True)

    class LightBlock3(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_3", True)

    class LightBlock4(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_4", True)

    class LightBlock5(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_5", True)

    class LightBlock6(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_6", True)

    class LightBlock7(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_7", True)

    class LightBlock8(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_8", True)

    class LightBlock9(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_9", True)

    class LightBlock10(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_10", True)

    class LightBlock11(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_11", True)

    class LightBlock12(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_12", True)

    class LightBlock13(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_13", True)

    class LightBlock14(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_14", True)

    class LightBlock15(_MinecraftBlock):
        def __init__(self):
            super().__init__("light_block_15", True)

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
    
    class InfestedStone(_MinecraftBlock):
        def __init__(self):
            super().__init__("infested_stone", True)

    class InfestedCobblestone(_MinecraftBlock):
        def __init__(self):
            super().__init__("infested_cobblestone", True)

    class InfestedStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("infested_stone_bricks", True)

    class InfestedMossyStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("infested_mossy_stone_bricks", True)

    class InfestedCrackedStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("infested_cracked_stone_bricks", True)

    class InfestedChiseledStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("infested_chiseled_stone_bricks", True)

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
        def __init__(self):
            super().__init__("prismarine", True)

    class DarkPrismarine(_MinecraftBlock):
        def __init__(self):
            super().__init__("dark_prismarine", True)

    class PrismarineBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("prismarine_bricks", True)

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
        def __init__(self):
            super().__init__("purpur_block", True)

    class PurpurPillar(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("purpur_pillar", True)

    class DeprecatedPurpurBlock1(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("deprecated_purpur_block_1", True)

    class DeprecatedPurpurBlock2(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("deprecated_purpur_block_2", True)

    class PurpurStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("purpur_stairs", True)
    
    class QuartzBlock(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("quartz_block", True)

    class ChiseledQuartzBlock(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("chiseled_quartz_block", True)

    class QuartzPillar(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("quartz_pillar", True)

    class SmoothQuartz(_MinecraftBlock):
        def __init__(self, pillar_axis: 'BlockStates.PillarAxis' = None):
            self._pillar_axis = pillar_axis
            super().__init__("smooth_quartz", True)


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
        def __init__(self):
            super().__init__("red_sandstone", True)

    class ChiseledRedSandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("chiseled_red_sandstone", True)

    class CutRedSandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("cut_red_sandstone", True)

    class SmoothRedSandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_red_sandstone", True)


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
        def __init__(self):
            super().__init__("sand", True)

    class RedSand(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_sand", True)

    
    class Sandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("sandstone", True)

    class ChiseledSandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("chiseled_sandstone", True)

    class CutSandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("cut_sandstone", True)

    class SmoothSandstone(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_sandstone", True)

    class SandstoneStairs(_MinecraftBlock):
        def __init__(self, upside_down_bit:'BlockStates.UpsideDownBit'=None, weirdo_direction:'BlockStates.WeirdoDirection'=None):
            self._upside_down_bit = upside_down_bit
            self._weirdo_direction = weirdo_direction
            super().__init__("sandstone_stairs", True)

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
        def __init__(self):
            super().__init__("sponge", True)

    class WetSponge(_MinecraftBlock):
        def __init__(self):
            super().__init__("wet_sponge", True)

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

    class StoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("stone_bricks", True)

    class MossyStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("mossy_stone_bricks", True)

    class CrackedStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("cracked_stone_bricks", True)

    class ChiseledStoneBricks(_MinecraftBlock):
        def __init__(self):
            super().__init__("chiseled_stone_bricks", True)

    class Stonecutter(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("stonecutter", True)

    class StonecutterBlock(_MinecraftBlock):
        def __init__(self, facing_direction:'BlockStates.FacingDirection'=None):
            self._facing_direction = facing_direction
            super().__init__("stonecutter_block", True)

    class EndStoneBrickSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("end_stone_brick_slab", True)

    class SmoothRedSandstoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_red_sandstone_slab", True)

    class PolishedAndesiteSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("polished_andesite_slab", True)

    class AndesiteSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("andesite_slab", True)

    class DioriteSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("diorite_slab", True)

    class PolishedDioriteSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("polished_diorite_slab", True)

    class GraniteSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("granite_slab", True)

    class PolishedGraniteSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("polished_granite_slab", True)

    class RedSandstoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_sandstone_slab", True)

    class PurpurSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("purpur_slab", True)

    class PrismarineSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("prismarine_slab", True)

    class DarkPrismarineSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("dark_prismarine_slab", True)

    class PrismarineBrickSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("prismarine_brick_slab", True)

    class MossyCobblestoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("mossy_cobblestone_slab", True)

    class SmoothSandstoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_sandstone_slab", True)

    class RedNetherBrickSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_nether_brick_slab", True)

    class MossyStoneBrickSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("mossy_stone_brick_slab", True)

    class SmoothQuartzSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("smooth_quartz_slab", True)

    class NormalStoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("normal_stone_slab", True)

    class CutSandstoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("cut_sandstone_slab", True)

    class CutRedSandstoneSlab(_MinecraftBlock):
        def __init__(self):
            super().__init__("cut_red_sandstone_slab", True)

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

    class Target(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("target", True)

    class TintedGlass(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("tinted_glass", True)

    class Tnt(_MinecraftBlock):
        def __init__(self, explode_bit:'BlockStates.ExplodeBit'=None):
            self._explode_bit = explode_bit
            super().__init__("tnt", True)

    class UnderwaterTnt(_MinecraftBlock):
        def __init__(self, explode_bit:'BlockStates.ExplodeBit'=None):
            self._explode_bit = explode_bit
            super().__init__("underwater_tnt", True)

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

    class OakWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("oak_wood", True)
            
    class SpruceWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("spruce_wood", True)
            
    class BirchWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("birch_wood", True)
            
    class JungleWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("jungle_wood", True)
            
    class AcaciaWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("acacia_wood", True)
            
    class DarkOakWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("dark_oak_wood", True)
            
    class StrippedOakWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_oak_wood", True)
            
    class StrippedSpruceWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_spruce_wood", True)
            
    class StrippedBirchWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_birch_wood", True)
            
    class StrippedJungleWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_jungle_wood", True)
            
    class StrippedAcaciaWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_acacia_wood", True)
            
    class StrippedDarkOakWood(_MinecraftBlock):
        def __init__(self, pillar_axis:'BlockStates.PillarAxis'=None):
            self._pillar_axis = pillar_axis
            super().__init__("stripped_dark_oak_wood", True)

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

    class OakSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("oak_slab", True)

    class SpruceSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("spruce_slab", True)

    class BirchSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("birch_slab", True)

    class JungleSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("jungle_slab", True)

    class AcaciaSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("acacia_slab", True)

    class DarkOakSlab(_MinecraftBlock):
        def __init__(self, vertical_half:'BlockStates.VerticalHalf'=None):
            self._vertical_half = vertical_half
            super().__init__("dark_oak_slab", True)

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

    class Dandelion(_MinecraftBlock):
        def __init__(self, ):
            super().__init__("dandelion", True)

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
            
    class LightBlueTerracotta(_MinecraftBlock):
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
            
    class LightGrayTerracotta(_MinecraftBlock):
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
    class OakPlanks(_MinecraftBlock):
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

    # Added in 1.20.80
    #Saplings
    class OakSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("oak_sapling", True)

    class SpruceSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("spruce_sapling", True)

    class BirchSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("birch_sapling", True)

    class JungleSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("jungle_sapling", True)

    class AcaciaSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("acacia_sapling", True)

    class DarkOakSapling(_MinecraftBlock):
        def __init__(self, age_bit:'BlockStates.AgeBit'=None):
            self._age_bit = age_bit
            super().__init__("dark_oak_sapling", True)

    #Coral
    class TubeCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("tube_coral_fan", True)

    class BrainCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("brain_coral_fan", True)
    
    class BubbleCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("bubble_coral_fan", True)

    class FireCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("fire_coral_fan", True)

    class HornCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("horn_coral_fan", True)

    class DeadTubeCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("dead_tube_coral_fan", True)
    
    class DeadBrainCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("dead_brain_coral_fan", True)

    class DeadBubbleCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("dead_bubble_coral_fan", True)

    class DeadFireCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("dead_fire_coral_fan", True)

    class DeadHornCoralFan(_MinecraftBlock):
        def __init__(self, coral_fan_direction:'BlockStates.CoralFanDirection'=None):
            self._coral_fan_direction = coral_fan_direction
            super().__init__("dead_horn_coral_fan", True)

    class Poppy(_MinecraftBlock):
        def __init__(self):
            super().__init__("poppy", True)

    class BlueOrchid(_MinecraftBlock):
        def __init__(self):
            super().__init__("blue_orchid", True)

    class Allium(_MinecraftBlock):
        def __init__(self):
            super().__init__("allium", True)

    class AzureBluet(_MinecraftBlock):
        def __init__(self):
            super().__init__("azure_bluet", True)
            
    class RedTulip(_MinecraftBlock):
        def __init__(self):
            super().__init__("red_tulip", True)

    class OrangeTulip(_MinecraftBlock):
        def __init__(self):
            super().__init__("orange_tulip", True)

    class WhiteTulip(_MinecraftBlock):
        def __init__(self):
            super().__init__("white_tulip", True)

    class PinkTulip(_MinecraftBlock):
        def __init__(self):
            super().__init__("pink_tulip", True)

    class OxeyeDaisy(_MinecraftBlock):
        def __init__(self):
            super().__init__("oxeye_daisy", True)

    class Cornflower(_MinecraftBlock):
        def __init__(self):
            super().__init__("cornflower", True)

    class LilyOfTheValley(_MinecraftBlock):
        def __init__(self):
            super().__init__("lily_of_the_valley", True)

    # Added in 1.21.50
    class CreakingHeart(_MinecraftBlock):
        def __init__(self, active: bool = False, natural: bool = False, pillar_axis: BlockStates.PillarAxis = BlockStates.PillarAxis.Y):
            self._active = active
            self._natural = natural
            self._pillar_axis = pillar_axis
            super().__init__('creaking_hear', True)

    class ClosedEyeBlossom(_MinecraftBlock):
        def __init__(self):
            super().__init__('closed_eyeblossom', True)

    class OpenEyeBlossom(_MinecraftBlock):
        def __init__(self):
            super().__init__('open_eyeblossom', True)

    class PaleHangingMoss(_MinecraftBlock):
        def __init__(self, tip: bool = False):
            self._tip = tip
            super().__init__('pale_hanging_moss', True)

    class PaleMossBlock(_MinecraftBlock):
        def __init__(self):
            super().__init__('pale_moss_block', True)

    class PaleMossCarpet(_MinecraftBlock):
        def __init__(self):
            super().__init__('pale_moss_carpet', True)

    #To add Door, Fence, Fence Gate, Plank, Sign, Hanging Sign, Slab, Stairs, Trapdoor, Wood, Stripped Log, Stripped Wood, Button, Pressure Plate, Boat, Boat with Chest, Resin

# Take all the subclasses of Blocks and add them to BLOCK_LIST
for block in Blocks.__dict__.values():
    if isinstance(block, type) and issubclass(block, Blocks._MinecraftBlock) and block is not Blocks._MinecraftBlock:
        BLOCK_LIST.append(block())
