"""A collection of useful functions and classes used throughout the program."""
import json as json
import logging
import math
import os
import shutil
import string
import subprocess
import sys
import types
import zipfile
from collections import defaultdict
from configparser import ConfigParser
from datetime import datetime
from enum import Enum, StrEnum
from typing import Any, NewType, Tuple
from uuid import uuid4

import click
import commentjson as commentjson
import requests
from click import style
from halo import Halo
from PIL import Image, ImageDraw, ImageFont

from .__version__ import __version__

Color = NewType("Color", [tuple[int, int, int] | tuple[int, int, int, int] | str])
Seconds = NewType("Seconds", float)
Molang = NewType("Molang", str)
coordinate = NewType("coordinate", [float | str])
coordinates = NewType("tuple(x, y, z)", tuple[coordinate, coordinate, coordinate])
position = NewType("tuple(x, y, z)", tuple[coordinate, coordinate, coordinate])
rotation = NewType("tuple(ry,rx)", tuple[coordinate, coordinate])
level = NewType("tuple(lm,l)", tuple[float, float])
Component = NewType("Component", str)
Identifier = NewType("Identifier", str)
event = NewType("Event", str)
tick = NewType("Tick", int)
_range = NewType("[range]", str)
inf = 99999999999

APPDATA: str = os.getenv("APPDATA").rstrip("Roaming")  # type: ignore
DESKTOP: str = os.path.join(os.getenv("USERPROFILE"), "Desktop")  # type: ignore
MOLANG_PREFIXES = ("q.", "v.", "c.", "t.", "query.", "variable.", "context.", "temp.")

MANIFEST_BUILD: list[int] = [1, 20, 40]  # The build version of the manifest.
BLOCK_SERVER_VERSION: str = "1.20.30"  # The version of the block server.
ENTITY_SERVER_VERSION: str = "1.20.50"  # The version of the entity server.
ENTITY_CLIENT_VERSION: str = "1.10.0"  # The version of the entity client.
BP_ANIMATION_VERSION: str = "1.10.0"  # The version of the behavior pack animation.
RP_ANIMATION_VERSION: str = "1.8.0"  # The version of the resource pack animation.
ANIMATION_CONTROLLERS_VERSION: str = "1.10.0"  # The version of the animation controllers.
SPAWN_RULES_VERSION: str = "1.8.0"  # The version of the spawn rules.
GEOMETRY_VERSION: str = "1.12.0"  # The version of the geometry.
RENDER_CONTROLLER_VERSION: str = "1.10.0"  # The version of the render controller.
SOUND_DEFINITIONS_VERSION: str = "1.20.20"  # The version of the sound definitions.
DIALOGUE_VERSION: str = "1.18.0"  # The version of the dialogue.
FOG_VERSION: str = "1.16.100"  # The version of the fog.
MATERIALS_VERSION: str = "1.0.0"  # The version of the materials.
ITEM_SERVER_VERSION: str = "1.20.50"  # The version of the item server.
GLOBAL_LIGHTING = [1, 0, 0]
CAMERA_PRESET_VERSION = "1.19.50"  # The version of the camera presets.

MODULE_MINECRAFT_SERVER: str = "1.6.0"  # The version of the Minecraft server module.
MODULE_MINECRAFT_SERVER_UI: str = "1.1.0"  # The version of the Minecraft UI module.
MODULE_MINECRAFT_SERVER_EDITOR: str = "0.1.0"  # The version of the Minecraft UI module.
MODULE_MINECRAFT_SERVER_GAMETEST: str = "1.0.0"  # The version of the Minecraft UI module.

# --------------------------------------------------------------------------


class Arguments(StrEnum):
    """Enumeration for the different types of arguments."""

    def __str__(self) -> str:
        return self.value


def FileExists(path) -> bool:
    """Checks if a file exists.

    Args:
        path (_type_): The path to the file.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(path)


def normalize_180(angle: float | str) -> float:
    """Normalizes an angle between -180 and 180.

    Args:
        angle (float): The angle to be normalized.

    Returns:
        float: The normalized angle.
    """
    if isinstance(angle, float):
        return round((angle + 540) % 360 - 180)
    else:
        return angle


def clamp(value: float, _min: float, _max: float) -> float:
    """
    Clamps a value between a minimum and maximum limit.

    Args:
        value (float): The value to be clamped.
        _min (float): The lower limit.
        _max (float): The upper limit.

    Returns:
        float: The clamped value.
    """
    return max(min(_max, value), _min)


def frange(start: int, stop: int, num: float = 1):
    """
    Generate a list of interpolated values between start and stop.

    Args:
        start (int): The starting value.
        stop (int): The ending value.
        num (float, optional): The number of values to generate. Defaults to 1.

    Returns:
        list: A list of interpolated values between start and stop.
    """
    step = (stop - start) / (num - 1)
    values = [round(start + i * step, 2) for i in range(num)]
    return values


def process_color(color: Color, add_alpha: bool = False) -> str | list[float]:
    if isinstance(color, tuple):
        if len(color) not in [3, 4]:
            raise ValueError("Color tuple must have 3 or 4 elements.")
        if len(color) == 3 and add_alpha:
            color = (*color, 255)
        return (clamp(c, 0.0, 255.0) for c in color)
    elif isinstance(color, str):
        if color[0] != "#" or len(color) not in [7, 9]:
            raise ValueError(
                "Invalid color string. Must be a hexadecimal string of 7 (RGB) or 9 (RGBA) characters including '#'."
            )
        if len(color) == 7 and add_alpha:
            color += "ff"
        return color
    else:
        raise TypeError("Color must be either a tuple of 3 or 4 integers or a hexadecimal string.")


class FillMode(Arguments):
    Replace = "replace"
    Outline = "outline"
    Hollow = "hollow"
    Destroy = "destroy"
    Keep = "keep"


class MusicRepeatMode(Arguments):
    Once = "play_once"
    Loop = "loop"


class LootPoolType(Arguments):
    """
    Enumeration for the different types of loot pools.
    """

    Empty = "empty"
    Item = "item"
    LootTable = "loot_table"


class Population(Arguments):
    """
    Enumeration for the different types of in-game populations.
    """

    Animal = "animal"
    UnderwaterAnimal = "underwater_animal"
    Monster = "monster"
    Ambient = "ambient"


class Difficulty(Arguments):
    """
    Enumeration for the different levels of game difficulty.
    """

    Peaceful = "peaceful"
    Easy = "easy"
    Normal = "normal"
    Hard = "hard"


class SoundCategory(Arguments):
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


class MusicCategory(Arguments):
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


class DamageCause(Arguments):
    """
    Enumeration for the different causes of damage in the game.
    """

    All = "all"
    Anvil = "anvil"
    EntityAttack = "entity_attack"
    Block_explosion = "block_explosion"
    Contact = "contact"
    Drowning = "drowning"
    Entity_explosion = "entity_explosion"
    Fall = "fall"
    Falling_block = "falling_block"
    Fatal = "fatal"
    Fire = "fire"
    Firetick = "firetick"
    Fly_into_wall = "fly_into_wall"
    Lava = "lava"
    Magic = "magic"
    Nothing = "none"
    Override = "override"
    Piston = "piston"
    Projectile = "projectile"
    Sonic_boom = "sonic_boom"
    Stalactite = "stalactite"
    Stalagmite = "stalagmite"
    Starve = "starve"
    Suffocation = "suffocation"
    Suicide = "suicide"
    Thorns = "thorns"
    Void = "void"
    Wither = "wither"


class Effects(Arguments):
    """
    Enumeration for the different types of effects in the game.
    """

    Hunger = "hunger"
    JumpBoost = "jump"
    Saturation = "saturation"
    Regeneration = "regeneration"
    Speed = "speed"
    Strength = "strength"
    Slowness = "slowness"
    Weakness = "weakness"
    Levitation = "levitation"
    Wither = "wither"
    Poison = "poison"
    Absorption = "absorption"
    Invisibility = "invisibility"
    SlowFalling = "slow_falling"


class Gamemodes(Arguments):
    """
    Enumeration for the different types of game modes.
    """

    Adventure = "adventure"
    Creative = "creative"
    Default = "default"
    Survival = "survival"
    Spectator = "spectator"

    A = Adventure
    C = Creative
    D = Default
    S = Survival


class Style(Arguments):
    """
    Enumeration for the different styles of text in the game.
    """

    Black: str = "§0"
    DarkBlue: str = "§1"
    DarkGreen: str = "§2"
    DarkAqua: str = "§3"
    DarkRed: str = "§4"
    DarkPurple: str = "§5"
    Gold: str = "§6"
    Gray: str = "§7"
    DarkGray: str = "§8"
    Blue: str = "§9"
    Green: str = "§a"
    Aqua: str = "§b"
    Red: str = "§c"
    Purple: str = "§d"
    Yellow: str = "§e"
    White: str = "§f"
    MineconGold: str = "§g"
    Obfuscated: str = "§k"
    Bold: str = "§l"
    Italic: str = "§o"
    Reset: str = "§r"


class FogCameraLocation(Arguments):
    """
    Enumeration for the different locations of the fog camera in the game.
    """

    Air = "air"
    Lava = "lava"
    Lava_resistance = "lava_resistance"
    Powder_snow = "powder_snow"
    Water = "water"
    Weather = "weather"


class RenderDistanceType(Arguments):
    """
    Enumeration for the different types of render distances in the game.
    """

    Render = "render"
    Fixed = "fixed"


class Dimension(Arguments):
    """
    Enumeration for the different dimensions in the game.
    """

    Overworld = "overworld"
    Nether = "nether"
    End = "the_end"


class Operator(Arguments):
    """
    Enumeration for the different types of mathematical operators.
    """

    Less = "<"
    LessEqual = "<="
    Equals = "="
    Greater = ">"
    GreaterEqual = ">="


class ScoreboardOperation(Arguments):
    """
    Enumeration for the different operations that can be performed on a scoreboard.
    """

    Addition = "+="
    Subtraction = "-="
    Multiplication = "*="
    Division = "/="
    Modulus = "%="
    Assign = "="
    Min = "<"
    Max = ">"
    Swaps = "><"


class Slots(Arguments):
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


class Target(Arguments):
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


class Anchor(Arguments):
    """
    Enumeration representing the two anchor points that can be used in Minecraft: the feet and the eyes.
    """

    Feet = "feet"
    Eyes = "eyes"


class BlockCategory(Arguments):
    """
    Enumeration representing the categories of blocks that can be used in Minecraft.
    """

    Construction = "construction"
    Nature = "nature"
    Equipment = "equipment"
    Items = "items"
    none = "none"


class BlockMaterial(Arguments):
    """
    Enumeration representing the different types of rendering methods a block can use in Minecraft.
    """

    Opaque = "opaque"
    DoubleSided = "double_sided"
    Blend = "blend"
    AlphaTest = "alpha_test"


class BlockFaces(Arguments):
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


class CameraShakeType(Arguments):
    """
    Enumeration representing the types of camera shakes that can occur in Minecraft.
    """

    positional = "positional"
    rotational = "rotational"


class MaskMode(Arguments):
    """
    Enumeration representing the different mask modes that can be applied in Minecraft.
    """

    replace = "replace"
    masked = "masked"


class CloneMode(Arguments):
    """
    Enumeration representing the different modes that can be used when cloning in Minecraft.
    """

    force = "force"
    move = "move"
    normal = "normal"


class WeatherSet(Arguments):
    """
    Enumeration representing the different types of weather that can be set in Minecraft.
    """

    Clear = "clear"
    Rain = "rain"
    Thunder = "thunder"


class FilterSubject(Arguments):
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


class FilterOperation(Arguments):
    """
    Enumeration representing the different operations that can be used in filters in Minecraft.
    """

    Less = "<"
    LessEqual = "<="
    Greater = ">"
    GreaterEqual = ">="
    Equals = "equals"
    Not = "not"


class FilterEquipmentDomain(Arguments):
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


class MaterialStates(Arguments):
    """
    Enumeration representing the different states a material can be in Minecraft.
    """

    EnableStencilTest = "EnableStencilTest"
    StencilWrite = "StencilWrite"
    InvertCulling = "InvertCulling"
    DisableCulling = "DisableCulling"
    DisableDepthWrite = "DisableDepthWrite"
    Blending = "Blending"


class MaterialDefinitions(Arguments):
    """
    Enumeration representing the different definitions that can be set for a material in Minecraft.
    """

    Fancy = "FANCY"
    USE_OVERLAY = "USE_OVERLAY"
    USE_COLOR_MASK = "USE_COLOR_MASK"
    MULTI_COLOR_TINT = "MULTI_COLOR_TINT"
    COLOR_BASED = "COLOR_BASED"
    USE_UV_ANIM = "USE_UV_ANIM"
    TINTED = "TINTED"
    USE_COLOR_BLEND = "USE_COLOR_BLEND"
    MULTIPLICATIVE_TINT = "MULTIPLICATIVE_TINT"
    MULTIPLICATIVE_TINT_COLOR = "MULTIPLICATIVE_TINT_COLOR"


class MaterialFunc(Arguments):
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


class MaterialOperation(Arguments):
    """
    Enumeration representing the different operations that can be set for a material in Minecraft.
    """

    Keep = "Keep"
    Replace = "Replace"


class InputPermissions(Arguments):
    """
    Enumeration representing the different input permissions that can be set for a player in Minecraft.
    """

    Camera = "camera"
    Movement = "movement"


class EntitySoundEvent(Arguments):
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


class CameraPresets(Arguments):
    FirstPerson = "minecraft:first_person"
    ThirdPerson = "minecraft:third_person"
    ThirdPersonFront = "minecraft:third_person_front"
    Free = "minecraft:free"


class CameraEasing(Arguments):
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


class TimeSpec(Arguments):
    DAY = "day"
    SUNRISE = "sunrise"
    NOON = "noon"
    SUNSET = "sunset"
    NIGHT = "night"
    MIDNIGHT = "midnight"


class Biomes(Arguments):
    BEACH = "beach"
    DESERT = "desert"
    EXTREME_HILLS = "extreme_hills"
    FLAT = "flat"
    FOREST = "forest"
    ICE = "ice"
    JUNGLE = "jungle"
    MESA = "mesa"
    MUSHROOM_ISLAND = "mushroom_island"
    OCEAN = "ocean"
    PLAIN = "plain"
    RIVER = "river"
    SAVANNA = "savanna"
    STONE_BEACH = "stone_beach"
    SWAMP = "swamp"
    TAIGA = "taiga"
    THE_END = "the_end"
    THE_NETHER = "the_nether"


class ReportType(Arguments):
    SOUND = "sound"
    ENTITY = "entity"
    ATTACHABLE = "attachable"
    ITEM = "item"
    BLOCK = "block"
    PARTICLE = "particle"


class Selector:
    """
    A class used to construct a target selector for Minecraft commands. The class offers various methods to set target
    parameters such as its type, name, count, coordinates, distance, volume, scores, rotation, permissions, and gamemode.
    """

    def __init__(self, target: Target = Target.S) -> None:
        """
        Initializes a Selector object.

        Args:
            target (Target, optional): The target type. Defaults to Target.S (self).
        """
        self.target = target
        self.arguments = []

    def _args(self, **args):
        for key, value in args.items():
            if not value is None and {key: value} not in self.arguments:
                self.arguments.append({key: value})
        return self

    def type(self, *types: str | Identifier):
        """Sets the type of the target."""
        for type in types:
            self._args(type=type)
        return self

    def name(self, name: str):
        """Sets the name of the target.

        Args:
            name (str): The name of the target.

        """
        self._args(name=f'"{name}"')
        return self

    def family(self, family: str):
        """Sets the family of the target.

        Args:
            family (str): The family of the target.

        """
        self._args(family=family)
        return self

    def count(self, count: int):
        """Sets the count of the target.

        Args:
            count (int): The number of targets to select.

        """
        self._args(c=count)
        return self

    def coordinates(self, *, x: coordinate = None, y: coordinate = None, z: coordinate = None):
        """Sets the coordinates of the target.

        Args:
            x (coordinate, optional): The x coordinate. Defaults to None.
            y (coordinate, optional): The y coordinate. Defaults to None.
            z (coordinate, optional): The z coordinate. Defaults to None.

        """
        self._args(x=x, y=y, z=z)
        return self

    def distance(self, *, r: coordinate = None, rm: coordinate = None):
        """Sets the distance of the target.

        Args:
            r (coordinate, optional): The maximum distance. Defaults to None.
            rm (coordinate, optional): The minimum distance. Defaults to None.

        """
        self._args(r=r, rm=rm)
        return self

    def volume(self, *, dx: float = None, dy: float = None, dz: float = None):
        """Sets the volume of the target.

        Args:
            dx (float, optional): The x volume. Defaults to None.
            dy (float, optional): The y volume. Defaults to None.
            dz (float, optional): The z volume. Defaults to None.

        """
        self._args(dx=dx, dy=dy, dz=dz)
        return self

    def scores(self, **scores):
        """Sets the scores of the target.

        Example:
            >>> selector.scores(score1=1, score2=2, score3=3)
        """
        score_values = {}
        for score, value in scores.items():
            score_values.update({score: value})
        self._args(scores=score_values)
        return self

    def tag(self, *tags: str):
        """Sets the tags of the target.

        Example:
            >>> selector.tag("tag1", "!tag2")
        """
        for tag in tags:
            self._args(tag=tag)
        return self

    def rotation(
        self,
        *,
        ry: float = None,
        rym: float = None,
        rx: float = None,
        rxm: float = None,
    ):
        """Sets the rotation of the target.

        Args:
            ry (float, optional): The maximum yaw. Defaults to None.
            rym (float, optional): The minimum yaw. Defaults to None.
            rx (float, optional): The maximum pitch. Defaults to None.
            rxm (float, optional): The minimum pitch. Defaults to None.

        """
        self._args(
            ry=normalize_180(round(ry, 2)) if not ry is None else ry,
            rym=normalize_180(round(rym, 2)) if not rym is None else rym,
            rx=clamp(round(rx, 2), -90, 90) if not rx is None else rx,
            rxm=clamp(round(rxm, 2), -90, 90) if not rxm is None else rxm,
        )
        return self

    def has_permission(self, *, camera: bool = None, movement: bool = None):
        """Selects targets that have the specified permissions.

        Args:
            camera (bool, optional): Defaults to None.
            movement (bool, optional): Defaults to None.

        """
        permission = {}
        if not camera is None:
            permission.update({"camera": "enabled" if camera else "disabled"})
        if not movement is None:
            permission.update({"movement": "enabled" if movement else "disabled"})

        self._args(haspermission=permission)
        return self

    def has_item(
        self,
        *,
        item: str | Identifier,
        data: int = -1,
        quantity: int = None,
        location: Slots = None,
        slot: int = None,
    ):
        """Selects targets that have the specified item.

        Args:
            item (str | Identifier): The item to check for.
            data (int, optional): The data value of the item. Defaults to -1.
            quantity (int, optional): The quantity of the item. Defaults to None.
            location (Slots, optional): The location of the item. Defaults to None.
            slot (int, optional): The slot of the item. Defaults to None.

        """
        test_item = {
            "item": item,
            "data": data if data != -1 else None,
            "quantity": quantity,
            "location": location,
            "slot": slot,
        }
        self._args(hasitem=test_item)
        return self

    def gamemode(self, gamemode: Gamemodes):
        """Selects targets that have the specified gamemode.

        Args:
            gamemode (Gamemodes): The gamemode to check for.

        """
        self._args(m=gamemode)
        return self

    def __str__(self) -> str:
        """Returns the target selector as a string."""
        if len(self.arguments) > 0:
            args = []
            for i in self.arguments:
                for key, value in i.items():
                    values = value
                    if type(value) is dict:
                        values = f"{{{', '.join(f'{k} = {v}' for k, v in value.items() if not v is None)}}}"
                    args.append(f"{key} = {values}")

            self.target = f"{self.target} [{', '.join(args)}]"
        return self.target


class BlockDescriptor(dict):
    """
    A class that inherits from Python's built-in dict class. It is used to create a descriptor for a block in Minecraft
    with its name, tags, and states.
    """

    def __init__(self, name: str, tags: "Molang", **states):
        """
        Initializes a BlockDescriptor object.

        Args:
            name (str): The name of the block.
            tags (Molang): The tags of the block.
            **states: The states of the block.
        """
        super().__init__(name=name, tags=tags, states=states)


class Vibrations(Arguments):
    EntityInteract = "entity_interact"
    Shear = "shear"
    none = "none"


class ControlFlags(Arguments):
    Move = "move"
    Look = "look"

# Legacy code, will be removed in the future.
def Defaults(type, *args):
    """

    Args:
        type (_type_): _description_

    Returns:
        _type_: _description_
    """
    match type:
        case "recipe_shaped":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shaped": {
                    "tags": ["crafting_table"],
                    "pattern": [],
                    "key": {},
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_shapeless":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": ["crafting_table"],
                    "ingredients": [],
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_stonecutter":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": ["stonecutter"],
                    "ingredients": [],
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_smithing_table":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": ["smithing_table"],
                    "ingredients": [{"item": "minecraft:netherite_ingot", "count": 1}],
                    "result": {"item": args[1], "data": args[2], "count": args[3]},
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "recipe_furnace":
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_furnace": {
                    "tags": args[3],
                    "output": args[1],
                    "input": args[2],
                    "description": {"identifier": f"{args[4]}:{args[0]}"},
                },
            }
        case "spawn_rules":
            return {
                "format_version": "1.8.0",
                "minecraft:spawn_rules": {
                    "description": {
                        "identifier": f"{args[0]}:{args[1]}",
                        "population_control": "ambient",
                    },
                    "conditions": [],
                },
            }
        case "loot_table":
            return {"pools": []}


def RemoveDirectory(path: str) -> None:
    """
    Removes a directory and all its contents.

    Args:
        path (str): The path to the directory to be removed.
    """
    shutil.rmtree(f"./{path}", ignore_errors=True)


def RemoveFile(path: str) -> None:
    """
    Removes a file.

    Args:
        path (str): The path to the file to be removed.
    """
    os.remove(path)


def CopyFiles(old_dir: str, new_dir: str, target_file: str, rename: str = None) -> None:
    """
    Copies a file from one directory to another.

    Args:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
        target_file (str): The name of the file to be copied.
        rename (str, optional): The new name for the copied file. Defaults to None.
    """
    CreateDirectory(new_dir)
    if rename is None:
        shutil.copyfile(os.path.join(old_dir, target_file), os.path.join(new_dir, target_file))
    else:
        shutil.copyfile(os.path.join(old_dir, target_file), os.path.join(new_dir, rename))


def CopyFolder(old_dir: str, new_dir: str) -> None:
    """
    Copies a folder and all its contents to a new location.

    Args:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
    """
    CreateDirectory(new_dir)
    shutil.copytree(os.path.realpath(old_dir), os.path.realpath(new_dir), dirs_exist_ok=True)


def zipit(zip_name, dir_list: dict) -> None:
    """
    Create a ZIP archive containing multiple directories and files.

    Args:
        zip_name: The name of the ZIP archive.
        dir_list (dict): A dictionary where the keys are source directories and the values are target directories.

    Note:
        The target directories represent the structure inside the ZIP archive.
    """

    def zipdir(ziph: zipfile.ZipFile, source, target):
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                for file in files:
                    ziph.write(
                        os.path.join(root, file),
                        os.path.join(
                            target,
                            os.path.relpath(os.path.join(root, file), os.path.join(source, ".")),
                        ),
                    )
        else:
            ziph.write(
                source,
                os.path.relpath(os.path.join(target, source), os.path.join(source, "..")),
            )

    zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
    for source, target in dir_list.items():
        zipdir(zipf, source, target)
    zipf.close()


def CreateDirectory(path: str) -> None:
    """
    Creates a new directory.

    Args:
        path (str): The path to the new directory.
    """
    this_path = os.path.join("./", path.lstrip("/"))
    os.makedirs(this_path, exist_ok=True)


class _Config:
    """A class used to read and write to the config.ini file."""

    def __init__(self) -> None:
        """Initializes a Config object."""
        with open("anvilconfig.json", "r") as f:
            self._config = json.loads(f.read())

    def save(self):
        """Saves the anvilconfig.json file."""
        with open("anvilconfig.json", "w") as f:
            f.write(json.dumps(self._config, indent=4))

    def add_section(self, section: str) -> None:
        """Adds a section to the anvilconfig.json file.

        Args:
            section (str): The section to add.
        """
        self._config[section] = {}

    def has_section(self, section: str) -> bool:
        """Checks if a section exists in the anvilconfig.json file.

        Args:
            section (str): The section to check.

        Returns:
            bool: True if the section exists, False otherwise.
        """
        return section in self._config

    def add_option(self, section: str, option: str, value):
        """Sets a value in the anvilconfig.json file.

        Args:
            section (str): The section to set the value in.
            option (str): The option to set the value in.
            value (Any): The value to set.
        """
        if not self.has_section(section):
            self.add_section(section)

        self._config[section][option] = value
        self.save()

    def has_option(self, section: str, option: str) -> bool:
        """Checks if an option exists in the anvilconfig.json file.

        Args:
            section (str): The section to check the option in.
            option (str): The option to check.

        Returns:
            bool: True if the option exists, False otherwise.
        """
        return option in self._config[section]

    def get_option(self, section, option) -> str:
        """Gets a value from the anvilconfig.json file.

        Args:
            section (str): The section to get the value from.
            option (str): The option to get the value from.

        Returns:
            str: The value of the option.
        """
        return self._config[section][option]


class _Logger:
    """A class used to log messages to the console and to a log file."""

    @staticmethod
    def Red(text: str):
        return style(text, "red")

    @staticmethod
    def Yellow(text: str):
        return style(text, "yellow")

    @staticmethod
    def Green(text: str):
        return style(text, "green")

    @staticmethod
    def Cyan(text: str):
        return style(text, "cyan")

    def __init__(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename="anvil.log",
            filemode="w",
        )
        self.logger = logging.getLogger()

    # Console header
    @staticmethod
    def header():
        click.clear()
        click.echo(
            "\n".join(
                [
                    f"{_Logger.Cyan('Anvil')} - by Yasser A. Benfoughal.",
                    f"Version {_Logger.Cyan(__version__)}.",
                    f"Copyright © {datetime.now().year} {_Logger.Red('StarkTMA')}.",
                    "All rights reserved.",
                    "",
                    "",
                ]
            )
        )

    # ------------------------------------------------------------------------
    # Addon Objects
    # ------------------------------------------------------------------------
    # Info
    def object_initiated(self, name: str):
        self.logger.info(f"Object initiated: {name}.")

    # Info
    def object_queued(self, name: str):
        self.logger.info(f"Object queued: {name}.")

    # Info
    def object_exported(self, name: str):
        self.logger.info(f"Object exported: {name}.")

    # Info
    def new_minecraft_build(self, old, new):
        m = f"A newer vanilla packages were found. Updating from {old} to {new}"
        self.logger.info(m)
        click.echo(m)

    # Info
    def minecraft_build_up_to_date(self):
        m = "Packages up to date"
        self.logger.info(m)
        click.echo(m)

    # Error
    def score_error(self, score):
        m = f"{[_Logger.Red('ERROR')]}: Score objective must be 16 characters, Error at {score}"
        self.logger.error(m)
        raise ValueError(m)

    # Error
    def not_compiled(self):
        m = 'Code must be compiled before packaging, make sure to run "ANVIL.compile"'
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Info
    def packaging_zip(self):
        m = "Packaging submission .zip"
        self.logger.info(m)
        click.echo(_Logger.Cyan(m))

    # Info
    def packaging_mcaddon(self):
        m = "Packaging .mcaddon"
        self.logger.info(m)

    # Info
    def packaging_mcworld(self):
        m = "Packaging .mcworld"
        self.logger.info(m)

    # Warn
    def file_exist_warning(self, filename):
        m = f"{filename} does not exist. This will cause validator fails."
        self.logger.warn(m)
        click.echo(_Logger.Yellow("[WARNING]: " + m))

    # Error
    def file_exist_error(self, filename, directory):
        m = f'{filename} could not be found at "{directory}".'
        self.logger.error(m)
        raise FileNotFoundError(_Logger.Red("[ERROR]: " + m))

    # Error
    def path_length_error(self, path):
        m = f"Relative file path [{path}] has [{len(path)}] characters, but cannot be more than [80] characters."
        self.logger.error(m)
        raise FileNotFoundError(_Logger.Red("[ERROR]: " + m))

    # Error
    def component_version_error(self, component, current_version, target_version):
        m = f"The component [{component}] cannot be used with a format version below {target_version}. Current version is {current_version}."
        self.logger.error(m)
        raise FileNotFoundError(_Logger.Red("[ERROR]: " + m))

    # Error
    def runtime_entity_error(self, entity):
        m = f"Runtime Identifier type must be a [Vanilla.Entities] type. Error at {entity}."
        self.logger.error(m)
        raise TypeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def runtime_entity_not_allowed(self, entity):
        m = f"Entity [{entity}] does not allow runtime identifier usage."
        self.logger.error(m)
        raise TypeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def unsupported_font_size(self):
        m = f"Font character_size must be a multiple of 16."
        self.logger.error(m)
        raise ValueError(_Logger.Red("[ERROR]: " + m))

    # Error
    def unsupported_block_type(self, block):
        m = f"block must be  of a [Blocks] or [str] type. Error at {block}."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def namespace_not_in_geo(self, geo_file, geo_namespace):
        m = f"The geometry file {geo_file}.geo.json doesn't contain a geometry called {geo_namespace}"
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def multiple_rotations(self):
        m = f"Multiple rotation arguments were used. A maximum of 1 is allowed."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Warn
    def missing_state(self, target, controller, state):
        m = f'{target} {controller} is missing the animation state "{state}".'
        self.logger.warn(m)
        click.echo(_Logger.Yellow("[WARNING]: " + m))

    # Error
    def dialogue_max_buttons(self, scene_tag, buttons_len):
        m = f"The Dialogue scene {scene_tag} has {buttons_len} buttons, The maximum allowed is 6."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def fog_start_end(self, fog_start, fog_end):
        m = f"fog_end: [{fog_end}] must be greater than fog_start: [{fog_start}]."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def unsupported_model_type(self, model):
        m = f"model must be of a [entity], [attachables] or [blocks] type. Error at {model}."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def no_geo_found(self, geo):
        m = f"The Geometry file {geo} does not have any geometry."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def no_anim_found(self, anim):
        m = f"The Animation file {anim} does not have any animations."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def client_type_unsupported(self, type, entity):
        m = f"{type} is not a supported Actor Type, error at {entity}."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def namespaces_not_allowed(self, name):
        m = f"Identifiers are not valid name formats, error at {name}."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Info
    def project_missing_config(self):
        m = f"The project require missing configuration. Please fill in the following options:"
        self.logger.info(m)
        click.echo(_Logger.Cyan("[Info]: " + m))

    # Info
    def config_added_option(self, section: str, option: str):
        m = f"{option} was added to {section}"
        self.logger.info(m)
        click.echo(_Logger.Cyan("[Info]: " + m))

    # Info
    def config_option_changeable(self, *options: str):
        m = f"The options {options} can be changed from the config file at any time, recompilation will be required."
        self.logger.info(m)
        click.echo(_Logger.Cyan("[Info]: " + m))

    # Error
    @staticmethod
    def namespace_too_long(namespace):
        m = f"Namespace must be 8 characters or less. {namespace} is {len(namespace)} characters long."
        # self.logger.error(m)
        raise ValueError(_Logger.Red("[ERROR]: " + m))

    # Error
    @staticmethod
    def reserved_namespace(namespace):
        m = f"{namespace} is a reserved namespace and cannot be used."
        # self.logger.error(m)
        raise ValueError(_Logger.Red("[ERROR]: " + m))

    # Error
    @staticmethod
    def unique_namespace(namespace):
        m = f"Every namespace must be unique to the pack. it should be {namespace}."
        # self.logger.error(m)
        raise ValueError(_Logger.Red("[ERROR]: " + m))

    # Error
    @staticmethod
    def project_name_too_long(self, project_name):
        m = f"Project name must be 16 characters or less. {project_name} is {len(project_name)} characters long."
        # self.logger.error(m)
        raise ValueError(_Logger.Red("[ERROR]: " + m))

    # Error
    def missing_animation(self, animation_path, animation):
        m = f"{animation_path} is missing the animation {animation}"
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def entity_missing_texture(self, entity):
        m = f"{entity} has no textures added."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def block_missing_texture(self, block):
        m = f"{block} has no default material instance added."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # Error
    def block_missing_geometry(self, block):
        m = f"{block} has no default geometry added."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))

    # ===================================
    def missing_render_controller(self, entity):
        return f'{Message.ERROR}: {style(entity, "green")} missing a render_controller.'

    def lang_error(self, text):
        return f'{Message.ERROR}: Invalid localized string at {style(text, "green")}'

    def sound_category_error(self):
        return f"{Message.ERROR}: Invalid sound category."

    def music_category_error(self):
        return f"{Message.ERROR}: Invalid music category."

    def damage_cause_error(self):
        return f"{Message.ERROR}: Invalid damage cause."

    def function_error(self, type, function):
        return f"{Message.ERROR}: ANVIL.{type}() accepts Function objects only, Error at {function}"

    # General
    def check_update(self):
        return style("Checking for updates...", "green")

    def anvil_type_error(self, type):
        return f"{Message.ERROR}:  {type} Is not a valid Anvil Type."

    def execution_time(self, time):
        return f'Execution starts at: {style(time, "cyan")}'

    def compiling(self, filename):
        return f'{style("[Compiling]", "cyan")}: {style(filename, "green")}               ' + "\033[A"

    def compilation_time(self, time):
        return f'{style("[Compilation Time]", "cyan")}: {style(time, "green") if time < 15 else style(time, "red")} s.               '

    def translating(self, filename):
        return f'{style("[Translating]", "cyan")}: {style(filename, "green")}               ' + "\033[A"

    def translation_time(self, time):
        return f'{style("[Translation Time]", "cyan")}: {style(time, "green")} s.               '

    def exporting(self, filename):
        return f'{style("[Exporting]", "green")}: {style(filename, "green")}               ' + "\033[A"

    # Molang
    def molang_only(self, command):
        return f'{Message.ERROR}: Molang operations only, Error at "{style(command, "green")}".'

    # Error
    def digits_not_allowed(self, identifier):
        m = f"Names starting with a digit are not allowed {identifier}."
        self.logger.error(m)
        raise RuntimeError(_Logger.Red("[ERROR]: " + m))


class _JsonSchemes:
    """A class used to read and write to the json_schemes.json file."""

    @staticmethod
    def structure(project_name):
        return {
            project_name: {
                "behavior_packs": {},
                "resource_packs": {},
                "assets": {
                    "skins": {},
                    "animations": {},
                    "models": {
                        "entity": {},
                        "attachables": {},
                        "blocks": {},
                    },
                    "particles": {},
                    "sounds": {},
                    "structures": {},
                    "marketing": {},
                    "textures": {
                        "attachables": {},
                        "environment": {},
                        "blocks": {},
                        "items": {},
                        "entity": {},
                        "ui": {},
                        "particle": {},
                    },
                    "output": {},
                    "javascript": {},
                    "anvilscripts": {},
                },
            }
        }

    @staticmethod
    def script():
        return "\n".join(
            [
                "from anvil import *",
                'if __name__ == "__main__":',
                "    ANVIL.compile()",
                "    #ANVIL.package()",
            ]
        )

    @staticmethod
    def gitignore():
        return "\n".join(
            [
                "#Anvil",
                "assets/vanilla/",
                "# Byte-compiled / optimized / DLL files",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "# C extensions",
                "*.so",
                "# Distribution / packaging",
                ".Python",
                "build/",
                "develop-eggs/",
                "dist/",
                "downloads/",
                "eggs/",
                ".eggs/",
                "lib/",
                "lib64/",
                "parts/",
                "sdist/",
                "var/",
                "wheels/",
                "pip-wheel-metadata/",
                "share/python-wheels/",
                "*.egg-info/",
                ".installed.cfg",
                "*.egg",
                "MANIFEST",
                "# Environments",
                ".env",
                ".venv",
                "env/",
                "venv/",
                "ENV/",
                "env.bak/",
                "venv.bak/",
                "# Typescript/Javascript",
                "node_modules/",
            ]
        )

    @staticmethod
    def pack_name_lang(name, description):
        return [f"pack.name={name}", f"pack.description={description}"]

    @staticmethod
    def skin_pack_name_lang(name, display_name):
        return [f"skinpack.{name}={display_name}"]

    @staticmethod
    def manifest_bp(version, uuid1, has_script: bool, server_ui: bool):
        v = list(map(int, version.split(".")))
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": uuid1[0],
                "version": v,
                "min_engine_version": MANIFEST_BUILD,
            },
            "modules": [{"type": "data", "uuid": str(uuid4()), "version": v}],
        }
        if has_script:
            m["modules"].append(
                {
                    "uuid": str(uuid4()),
                    "version": v,
                    "type": "script",
                    "language": "javascript",
                    "entry": "scripts/main.js",
                }
            )
            m.update(
                {
                    "dependencies": [
                        {
                            "module_name": "@minecraft/server",
                            "version": MODULE_MINECRAFT_SERVER,
                        }
                    ]
                }
            )
            if server_ui:
                m["dependencies"].append(
                    {
                        "module_name": "@minecraft/server-ui",
                        "version": MODULE_MINECRAFT_SERVER_UI,
                    }
                )
        return m

    @staticmethod
    def manifest_rp(version, uuid1, has_pbr):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": uuid1[0],
                "version": version,
                "min_engine_version": MANIFEST_BUILD,
            },
            "modules": [
                {
                    "type": "resources",
                    "uuid": str(uuid4()),
                    "version": version,
                }
            ],
        }
        if has_pbr:
            m.update({"capabilities": ["pbr"]})
        return m

    @staticmethod
    def manifest_world(version, uuid1, author, seed):
        return {
            "format_version": 2,
            "header": {
                "name": "pack.name",
                "description": "pack.description",
                "version": version,
                "uuid": uuid1,
                # "platform_locked": False,
                "lock_template_options": True,
                "base_game_version": MANIFEST_BUILD,
                "allow_random_seed": seed,
            },
            "modules": [
                {
                    "type": "world_template",
                    "uuid": str(uuid4()),
                    "version": version,
                }
            ],
            "metadata": {"authors": [author]},
        }

    @staticmethod
    def world_packs(pack_id, version):
        return [{"pack_id": i, "version": version} for i in pack_id]

    @staticmethod
    def code_workspace(name, path1, path2):
        return {
            "folders": [
                {"name": name, "path": os.path.join(path1, path2)},
            ]
        }

    @staticmethod
    def packagejson(project_name, version, description, author):
        return {
            "name": project_name,
            "version": version,
            "description": description,
            "main": "scripts/main.js",
            "scripts": {"test": 'echo "Error: no test specified" && exit 1'},
            "keywords": [],
            "author": author,
            "license": "ISC",
        }

    @staticmethod
    def skins_json(serialize_name):
        return {
            "serialize_name": serialize_name,
            "localization_name": serialize_name,
            "skins": [],
        }

    @staticmethod
    def manifest_skins(version):
        return {
            "format_version": 1,
            "header": {
                "name": "pack.name",
                "uuid": str(uuid4()),
                "version": version,
            },
            "modules": [
                {
                    "type": "skin_pack",
                    "uuid": str(uuid4()),
                    "version": version,
                }
            ],
        }

    @staticmethod
    def description(namespace, identifier):
        return {"description": {"identifier": f"{namespace}:{identifier}"}}

    @staticmethod
    def item_texture(resource_pack_name):
        return {
            "resource_pack_name": resource_pack_name,
            "texture_name": "atlas.items",
            "texture_data": {},
        }

    @staticmethod
    def sound_definitions():
        return {
            "format_version": SOUND_DEFINITIONS_VERSION,
            "sound_definitions": {},
        }

    @staticmethod
    def music_definitions():
        return {}

    @staticmethod
    def sound(name, category):
        return {name: {"category": category, "sounds": []}}

    @staticmethod
    def materials():
        return {"materials": {"version": MATERIALS_VERSION}}

    @staticmethod
    def languages():
        return [
            "en_US",
            "en_GB",
            "de_DE",
            "es_ES",
            "es_MX",
            "fr_FR",
            "fr_CA",
            "it_IT",
            "pt_BR",
            "pt_PT",
            "ru_RU",
            "zh_CN",
            "zh_TW",
            "nl_NL",
            "bg_BG",
            "cs_CZ",
            "da_DK",
            "el_GR",
            "fi_FI",
            "hu_HU",
            "id_ID",
            "nb_NO",
            "pl_PL",
            "sk_SK",
            "sv_SE",
            "tr_TR",
            "uk_UA",
        ]

    @staticmethod
    def client_description():
        return {
            "materials": {"default": "entity_alphatest"},
            "scripts": {"pre_animation": [], "initialize": [], "animate": []},
            "textures": {},
            "geometry": {},
            "particle_effects": {},
            "sound_effects": {},
            "render_controllers": [],
        }

    @staticmethod
    def client_entity():
        return {
            "format_version": ENTITY_CLIENT_VERSION,
            "minecraft:client_entity": {},
        }

    @staticmethod
    def server_entity():
        return {
            "format_version": ENTITY_SERVER_VERSION,
            "minecraft:entity": {
                "component_groups": {},
                "components": {},
                "events": {},
            },
        }

    @staticmethod
    def bp_animations():
        return {"format_version": BP_ANIMATION_VERSION, "animations": {}}

    @staticmethod
    def bp_animation(animation_name, part, animation_type, loop):
        return {
            f"animation.{animation_name}.{part}.{animation_type}": {
                "loop": loop,
                "timeline": {},
            }
        }

    @staticmethod
    def rp_animations():
        return {"format_version": RP_ANIMATION_VERSION, "animations": {}}

    @staticmethod
    def animation_controller_state(state):
        return {
            state: {
                "on_entry": [],
                "on_exit": [],
                "animations": [],
                "transitions": [],
            }
        }

    @staticmethod
    def animation_controller(controller_name, part, animation_type):
        return {
            f"controller.animation.{controller_name}.{part}.{animation_type}": {
                "initial_state": "default",
                "states": {},
            }
        }

    @staticmethod
    def animation_controllers():
        return {
            "format_version": ANIMATION_CONTROLLERS_VERSION,
            "animation_controllers": {},
        }

    @staticmethod
    def geometry():
        return {
            "format_version": GEOMETRY_VERSION,
            "minecraft:geometry": [],
        }

    @staticmethod
    def render_controller(controller_name, part, controller_type):
        return {
            f"controller.render.{controller_name}.{part}.{controller_type}": {
                "arrays": {"textures": {}, "geometries": {}},
                "materials": [],
                "geometry": {},
                "textures": [],
                "part_visibility": [],
            }
        }

    @staticmethod
    def render_controllers():
        return {
            "format_version": RENDER_CONTROLLER_VERSION,
            "render_controllers": {},
        }

    @staticmethod
    def attachable():
        return {"format_version": ENTITY_CLIENT_VERSION, "minecraft:attachable": {}}

    @staticmethod
    def spawn_rules():
        return {
            "format_version": SPAWN_RULES_VERSION,
            "minecraft:spawn_rules": {"conditions": []},
        }

    @staticmethod
    def server_block():
        return {
            "format_version": BLOCK_SERVER_VERSION,
            "minecraft:block": {
                "description": {},
                "components": {},
                "permutations": [],
            },
        }

    @staticmethod
    def terrain_texture(resource_pack_name):
        return {
            "num_mip_levels": 4,
            "padding": 8,
            "resource_pack_name": resource_pack_name,
            "texture_data": {},
            "texture_name": "atlas.terrain",
        }

    @staticmethod
    def flipbook_textures():
        return []

    @staticmethod
    def font(font_name, font_file):
        return {
            "version": 1,
            "fonts": [
                {
                    "font_format": "ttf",
                    "font_name": font_name,
                    "version": 1,
                    "font_file": f"font/{font_file}",
                    "lowPerformanceCompatible": False,
                }
            ],
        }

    @staticmethod
    def fog():
        return {
            "format_version": FOG_VERSION,
            "minecraft:fog_settings": {
                "distance": {},
                "volumetric": {},
            },
        }

    @staticmethod
    def dialogues():
        return {
            "format_version": DIALOGUE_VERSION,
            "minecraft:npc_dialogue": {"scenes": []},
        }

    @staticmethod
    def dialogue_scene(scene_tag, npc_name, text, on_open_commands, on_close_commands, buttons):
        return {
            "scene_tag": scene_tag,
            "npc_name": npc_name,
            "text": text,
            "on_open_commands": on_open_commands,
            "on_close_commands": on_close_commands,
            "buttons": buttons,
        }

    @staticmethod
    def dialogue_button(name, commands):
        return {"name": name, "commands": commands}

    @staticmethod
    def server_item():
        return {
            "format_version": ITEM_SERVER_VERSION,
            "minecraft:item": {"components": {}},
        }

    @staticmethod
    def camera_preset(namespace, name, inherit_from):
        return {
            "format_version": CAMERA_PRESET_VERSION,
            "minecraft:camera_preset": {
                "identifier": f"{namespace}:{name}",
                "inherit_from": inherit_from,
            },
        }

    @staticmethod
    def tsconfig(pascal_project_name):
        return {
            "compilerOptions": {
                "target": "ESNext",
                "module": "es2020",
                "declaration": False,
                "outDir": f"behavior_packs/BP_{pascal_project_name}/scripts",
                "strict": True,
                "pretty": True,
                "esModuleInterop": True,
                "moduleResolution": "Node",
                "resolveJsonModule": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "forceConsistentCasingInFileNames": True,
                "lib": [
                    "ESNext",
                    "dom",
                ],
            },
            "include": ["assets/javascript/**/*"],
            "exclude": ["node_modules"],
        }

    @staticmethod
    def vscode(pascal_project_name):
        return {
            "version": "0.3.0",
            "configurations": [
                {
                    "type": "minecraft-js",
                    "request": "attach",
                    "name": "Wait for Minecraft Debug Connections",
                    "mode": "listen",
                    "localRoot": f"${{workspaceFolder}}/behavior_packs/BP_{pascal_project_name}/scripts",
                    "port": 19144,
                }
            ],
        }

    # ---------------------------
    @staticmethod
    def sounds():
        return {
            "individual_event_sounds": {},
            "block_sounds": {},
            "entity_sounds": {"entities": {}},
            "interactive_sounds": {},
        }

    @staticmethod
    def directional_lights():
        return {
            "format_version": GLOBAL_LIGHTING,
            "directional_lights": {},
            "pbr": {},
        }

    @staticmethod
    def atmospherics():
        return {
            "horizon_blend_stops": {},
        }


def File(name: str, content: str | dict, directory: str, mode: str, skip_tag: bool = False, *args) -> None:
    """
    Create or modify a file with the given content.

    Args:
        name (str): The name of the file.
        content: The content of the file.
        directory (str): The directory path where the file should be created or modified.
        mode (str): The file mode, either "w" (write) or "a" (append).
        skip_tag (bool, optional): Whether to skip adding the file metadata tag. Defaults to False.
        *args: Additional arguments.

    Note:
        The file content is converted to the appropriate format based on the file extension.
    """
    CreateDirectory(directory)
    type = name.split(".")[-1]
    out_content = ""
    file_content = content
    stamp = f"Generated with Anvil@starktma_lg {__version__}"
    time = datetime.now(datetime.now().astimezone().tzinfo).strftime("%d-%m-%Y %H:%M:%S %z")
    # copyright=f'Property of {COMPANY}'
    copyright = ""
    path = os.path.normpath(os.path.join(directory, name))
    if mode == "w":
        match type:
            case "json" | "material" | "code-workspace":
                out_content = f"//Filename: {name}\n//{stamp}\n//{time}\n//{copyright}\n\n"
                file_content = json.dumps(content, sort_keys=False, indent=4, ensure_ascii=False)
            case "py" | "mcfunction":
                out_content = f"#Filename: {name}\n#{stamp}\n#{time}\n#{copyright}\n\n"
            case "lang":
                out_content = f"##Filename: {name}\n##{stamp}\n##{time}\n##{copyright}\n\n"
    if skip_tag:
        out_content = file_content
    else:
        out_content += file_content

    prev = ""

    if FileExists(path):
        with open(path, "r", encoding="utf-8") as file:
            prev = file.read()

    if prev.split("\n")[6::] != file_content.split("\n"):
        with open(path, mode, encoding="utf-8") as file:
            file.write(out_content)


def process_subcommand(command: str, error_handle: str = "Error"):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{error_handle}: {e}")


def validate_namespace_project_name(namespace: str, project_name: str):
    display_name = project_name.title().replace("-", " ").replace("_", " ")
    pascal_project_name = "".join(x for x in display_name if x.isupper())

    if namespace == "minecraft":
        _Logger.reserved_namespace(namespace)
    
    if len(namespace) > 8:
        _Logger.namespace_too_long(namespace)
    
    if not namespace.endswith(f"_{pascal_project_name.lower()}"):
        _Logger.unique_namespace(f"{namespace}_{pascal_project_name.lower()}")

    if len(project_name) > 16:
        _Logger.project_name_too_long(namespace)
    