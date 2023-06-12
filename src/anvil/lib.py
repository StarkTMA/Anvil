import csv
import json as json
import logging
import math
import os
import random
import shutil
import string
import sys
import time
import zipfile
from collections import OrderedDict, defaultdict
from configparser import ConfigParser
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NewType, Tuple, Type, Union, overload
from urllib import request
from uuid import uuid4

import click
import commentjson as commentjson
from click import style
from PIL import Image, ImageColor, ImageDraw, ImageEnhance, ImageFont, ImageQt

from .__version__ import __version__

Seconds = NewType("Seconds", str)
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
def FileExists(path):
    return os.path.exists(path)


# A function that checks if a file or directory exists at the specified path.


def normalize_180(angle):
    return (angle + 540) % 360 - 180


# A function that normalizes an angle to the range [-180, 180].


APPDATA: str = os.getenv("APPDATA").rstrip("Roaming")
# The path to the AppData directory.

DESKTOP: str = os.path.join(os.getenv("USERPROFILE"), "Desktop")
# The path to the desktop directory.

MOLANG_PREFIXES: tuple[str, ...] = (
    "q.",
    "v.",
    "c.",
    "t.",
    "query.",
    "variable.",
    "context.",
    "temp.",
)
# A tuple of prefixes commonly used in MoLang expressions.


MANIFEST_BUILD: list[int] = [1, 19, 70]  # The build version of the manifest.
BLOCK_SERVER_VERSION: str = "1.19.70"  # The version of the block server.
ENTITY_SERVER_VERSION: str = "1.19.0"  # The version of the entity server.
ENTITY_CLIENT_VERSION: str = "1.10.0"  # The version of the entity client.
# The version of the behavior pack animation.
BP_ANIMATION_VERSION: str = "1.10.0"
# The version of the resource pack animation.
RP_ANIMATION_VERSION: str = "1.8.0"
ANIMATION_CONTROLLERS_VERSION: str = "1.10.0"  # The version of the animation controllers.

SPAWN_RULES_VERSION: str = "1.8.0"  # The version of the spawn rules.
GEOMETRY_VERSION: str = "1.12.0"  # The version of the geometry.
# The version of the render controller.
RENDER_CONTROLLER_VERSION: str = "1.10.0"
# The version of the sound definitions.
SOUND_DEFINITIONS_VERSION: str = "1.14.0"
DIALOGUE_VERSION: str = "1.18.0"  # The version of the dialogue.
FOG_VERSION: str = "1.16.100"  # The version of the fog.
MATERIALS_VERSION: str = "1.0.0"  # The version of the materials.
ITEM_SERVER_VERSION: str = "1.20.0"  # The version of the item server.
# The version of the Minecraft server module.
MODULE_MINECRAFT_SERVER: str = "1.1.0"


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


class LootPoolType:
    """
    Enumeration for the different types of loot pools.
    """

    Empty = "empty"
    Item = "item"
    LootTable = "loot_table"


class Population:
    """
    Enumeration for the different types of in-game populations.
    """

    Animal = "animal"
    UnderwaterAnimal = "underwater_animal"
    Monster = "monster"
    Ambient = "ambient"


class Difficulty:
    """
    Enumeration for the different levels of game difficulty.
    """

    Peaceful = "peaceful"
    Easy = "easy"
    Normal = "normal"
    Hard = "hard"


class SoundCategory:
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


class MusicCategory:
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


class DamageCause:
    """
    Enumeration for the different causes of damage in the game.
    """

    All = "all"
    Anvil = "anvil"
    Attack = "attack"
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


class Effects:
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


class Gamemodes:
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


class Style:
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


class FogCameraLocation:
    """
    Enumeration for the different locations of the fog camera in the game.
    """

    Air = "air"
    Lava = "lava"
    Lava_resistance = "lava_resistance"
    Powder_snow = "powder_snow"
    Water = "water"
    Weather = "weather"


class RenderDistanceType:
    """
    Enumeration for the different types of render distances in the game.
    """

    Render = "render"
    Fixed = "fixed"


class Dimension:
    """
    Enumeration for the different dimensions in the game.
    """

    Overworld = "overworld"
    Nether = "nether"
    End = "the_end"


class Operator:
    """
    Enumeration for the different types of mathematical operators.
    """

    Less = "<"
    LessEqual = "<="
    Equals = "="
    Greater = ">"
    GreaterEqual = ">="


class ScoreboardOperation:
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


class Slots:
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


class Target:
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

    def type(self, *types: str):
        for type in types:
            self._args(type=type)
        return self

    def name(self, name: str):
        self._args(name=f'"{name}"')
        return self

    def family(self, family: str):
        self._args(family=family)
        return self

    def count(self, count: int):
        self._args(c=count)
        return self

    def coordinates(
        self, *, x: coordinate = None, y: coordinate = None, z: coordinate = None
    ):
        self._args(x=x, y=y, z=z)
        return self

    def distance(self, *, r: coordinate = None, rm: coordinate = None):
        self._args(r=r, rm=rm)
        return self

    def volume(
        self, *, dx: coordinate = None, dy: coordinate = None, dz: coordinate = None
    ):
        self._args(dx=dx, dy=dy, dz=dz)
        return self

    def scores(self, **scores):
        score_values = {}
        for score, value in scores.items():
            score_values.update({score: value})
        self._args(scores=score_values)
        return self

    def tag(self, *tags: str):
        for tag in tags:
            self._args(tag=tag)
        return self

    def rotation(
        self,
        *,
        ry: rotation = None,
        rym: rotation = None,
        rx: rotation = None,
        rxm: rotation = None,
    ):
        self._args(
            ry=normalize_180(round(ry, 2)) if not ry is None else ry,
            rym=normalize_180(round(rym, 2)) if not rym is None else rym,
            rx=clamp(round(rx, 2), -90, 90) if not rx is None else rx,
            rxm=clamp(round(rxm, 2), -90, 90) if not rxm is None else rxm,
        )
        return self

    def has_permission(self, *, camera: bool = None, movement: bool = None):
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
        item,
        data: int = -1,
        quantity: int = None,
        location: Slots = None,
        slot: int = None,
    ):
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
        self._args(m=gamemode)
        return self

    def __str__(self):
        if len(self.arguments) > 0:
            args = []
            for i in self.arguments:
                for key, value in i.items():
                    values = value
                    if type(value) is dict:
                        values = f"{{{', '.join(f'{k} = {v}' for k, v in value.items() if not v is None)}}}"
                    args.append(f"{key} = {values}")

            self.target += f"[{', '.join(args)}]"
        return self.target


class Anchor:
    """
    Enumeration representing the two anchor points that can be used in Minecraft: the feet and the eyes.
    """

    Feet = "feet"
    Eyes = "eyes"


class BlockCategory:
    """
    Enumeration representing the categories of blocks that can be used in Minecraft.
    """

    Construction = "construction"
    Nature = "nature"
    Equipment = "equipment"
    Items = "items"
    none = "none"


class BlockMaterial:
    """
    Enumeration representing the different types of rendering methods a block can use in Minecraft.
    """

    Opaque = "opaque"
    DoubleSided = "double_sided"
    Blend = "blend"
    AlphaTest = "alpha_test"


class BlockFaces:
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


class CameraShakeType:
    """
    Enumeration representing the types of camera shakes that can occur in Minecraft.
    """

    positional = "positional"
    rotational = "rotational"


class MaskMode:
    """
    Enumeration representing the different mask modes that can be applied in Minecraft.
    """

    replace = "replace"
    masked = "masked"


class CloneMode:
    """
    Enumeration representing the different modes that can be used when cloning in Minecraft.
    """

    force = "force"
    move = "move"
    normal = "normal"


class WeatherSet:
    """
    Enumeration representing the different types of weather that can be set in Minecraft.
    """

    Clear = "clear"
    Rain = "rain"
    Thunder = "thunder"


class FilterSubject:
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


class FilterOperation:
    """
    Enumeration representing the different operations that can be used in filters in Minecraft.
    """

    Less = "<"
    LessEqual = "<="
    Greater = ">"
    GreaterEqual = ">="
    Equals = "equals"
    Not = "not"


class FilterEquipmentDomain:
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


# Materials classes
class MaterialStates:
    """
    Enumeration representing the different states a material can be in Minecraft.
    """

    EnableStencilTest = "EnableStencilTest"
    StencilWrite = "StencilWrite"
    InvertCulling = "InvertCulling"
    DisableCulling = "DisableCulling"
    DisableDepthWrite = "DisableDepthWrite"


class MaterialDefinitions:
    """
    Enumeration representing the different definitions that can be set for a material in Minecraft.
    """

    Fancy = "FANCY"
    USE_OVERLAY = "USE_OVERLAY"
    USE_COLOR_MASK = "USE_COLOR_MASK"
    MULTI_COLOR_TINT = "MULTI_COLOR_TINT"
    COLOR_BASED = "COLOR_BASED"


class MaterialFunc:
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


class MaterialOperation:
    """
    Enumeration representing the different operations that can be set for a material in Minecraft.
    """

    Keep = "Keep"
    Replace = "Replace"


class InputPermissions:
    """
    Enumeration representing the different input permissions that can be set for a player in Minecraft.
    """

    Camera = "camera"
    Movement = "movement"


def Defaults(type, *args):
    match type:
        case "rp_item_v1":
            return {
                "format_version": "1.10.0",
                "minecraft:item": {
                    "description": {
                        "identifier": f"{args[0]}:{args[1]}",
                        "category": "Nature",
                    },
                    "components": {
                        "minecraft:icon": f"{args[1]}",
                        "minecraft:render_offsets": "apple",
                    },
                },
            }
        case "bp_item_v1":
            return {
                "format_version": "1.10.0",
                "minecraft:item": {
                    "description": {
                        "identifier": f"{args[0]}:{args[1]}",
                    },
                    "components": {"minecraft:use_animation": "none"},
                },
            }
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
        case "music_definitions":
            return {}
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
        shutil.copyfile(
            os.path.join(old_dir, target_file), os.path.join(new_dir, target_file)
        )
    else:
        shutil.copyfile(
            os.path.join(old_dir, target_file), os.path.join(new_dir, rename)
        )


def CopyFolder(old_dir: str, new_dir: str) -> None:
    """
    Copies a folder and all its contents to a new location.

    Args:
        old_dir (str): The path to the source directory.
        new_dir (str): The path to the destination directory.
    """
    CreateDirectory(new_dir)
    shutil.copytree(
        os.path.realpath(old_dir), os.path.realpath(new_dir), dirs_exist_ok=True
    )


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
                            os.path.relpath(
                                os.path.join(root, file), os.path.join(source, ".")
                            ),
                        ),
                    )
        else:
            ziph.write(
                source,
                os.path.relpath(
                    os.path.join(target, source), os.path.join(source, "..")
                ),
            )

    zipf = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
    for source, target in dir_list.items():
        zipdir(zipf, source, target)
    zipf.close()


# ------------------------------------------------------------------------
# Control classes
# ------------------------------------------------------------------------


class _Config:
    def __init__(self) -> None:
        self._config = ConfigParser()
        self._config.read("config.ini")

    def save(self):
        with open("config.ini", "w") as f:
            self._config.write(f)

    def set(self, section, option, value):
        if not self._config.has_section(section):
            self._config.add_section(section)

        self._config[section][option] = str(value)
        self.save()

    def has_option(self, section, option):
        return option in self._config[section]

    def has_section(self, section):
        return section in self._config

    def get(self, section, option):
        return self._config[section][option]


class _Logger:
    Red = lambda text: style(text, "red")
    Yellow = lambda text: style(text, "yellow")
    Green = lambda text: style(text, "green")
    Cyan = lambda text: style(text, "cyan")

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
                    f"{_Logger.Cyan('Anvil')} - by Yasser A. Benfoguhal.",
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
        click.echo(_Logger.Cyan(m))

    # Info
    def packaging_mcworld(self):
        m = "Packaging .mcworld"
        self.logger.info(m)
        click.echo(_Logger.Cyan(m))

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





    # Actor Client
    def client_type_unsupported(self, type, entity):
        return f"{Message.ERROR}: {type} is an unsupported Actor Type, at {entity}."

    # Entity Client
    def missing_texture(self, entity):
        return f'{Message.ERROR}: {style(entity, "green")} missing a texture.'

    def missing_render_controller(self, entity):
        return f'{Message.ERROR}: {style(entity, "green")} missing a render_controller.'

    def missing_animation(self, NAMESPACE, entity, animation):
        return f'{Message.ERROR}: The animation file {style(f"{entity}.animation.json", "green")} doesn\'t contain an animation called {style(NAMESPACE, "green")}.'

    def lang_error(self, text):
        return f'{Message.ERROR}: Invalid localized string at {style(text, "green")}'

    def sound_category_error(self):
        return f"{Message.ERROR}: Invalid sound category."

    def music_category_error(self):
        return f"{Message.ERROR}: Invalid music category."

    def damage_cause_error(self):
        return f"{Message.ERROR}: Invalid damage cause."

    # Entity Server
    def missing_state(self, identifier, controller, state):
        return f'{Message.WARNING}: {style(identifier, "green")} - {controller} - Missing state "{style(state, "green")}".'

    def function_error(self, type, function):
        return f"{Message.ERROR}: ANVIL.{type}() accepts Function objects only, Error at {function}"

    # Dialogues
    def dialogue_max_buttons(self, scene_tag, buttons_len):
        return f"{Message.ERROR}: The Dialogue scene {scene_tag} has {buttons_len} buttons, The maximum allowed is 6."

    # General
    def check_update(self):
        return style("Checking for updates...", "green")

    def anvil_type_error(self, type):
        return f"{Message.ERROR}:  {type} Is not a valid Anvil Type."

    def execution_time(self, time):
        return f'Execution starts at: {style(time, "cyan")}'

    def compiling(self, filename):
        return (
            f'{style("[Compiling]", "cyan")}: {style(filename, "green")}               '
            + "\033[A"
        )

    def compilation_time(self, time):
        return f'{style("[Compilation Time]", "cyan")}: {style(time, "green") if time < 15 else style(time, "red")} s.               '

    def translating(self, filename):
        return (
            f'{style("[Translating]", "cyan")}: {style(filename, "green")}               '
            + "\033[A"
        )

    def translation_time(self, time):
        return f'{style("[Translation Time]", "cyan")}: {style(time, "green")} s.               '

    def exporting(self, filename):
        return (
            f'{style("[Exporting]", "green")}: {style(filename, "green")}               '
            + "\033[A"
        )

    def unsupported_font_size(self):
        return f"{Message.ERROR}: character_size must be a multiple of 16."

    # Identifiers
    def namespaces_not_allowed(self, identifier):
        return (
            f'{Message.ERROR}: Namespaces are not allowed. {style(identifier, "green")}'
        )

    # Molang
    def molang_only(self, command):
        return f'{Message.ERROR}: Molang operations only, Error at "{style(command, "green")}".'


class _JsonSchemes:
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
                    "vanilla": {},
                    "output": {},
                },
            }
        }

    @staticmethod
    def script():
        return "\n".join(
            [
                "from anvil import *",
                'if __name__ == "__main__":',
                "    ANVIL.compile",
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
            ]
        )

    @staticmethod
    def pack_name_lang(name, description):
        return [f"pack.name={name}", f"pack.description={description}"]

    @staticmethod
    def skin_pack_name_lang(name, display_name):
        return [f"skinpack.{name}={display_name}"]

    @staticmethod
    def manifest_bp(version, uuid1, has_script):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": uuid1,
                "version": version,
                "min_engine_version": MANIFEST_BUILD,
            },
            "modules": [{"type": "data", "uuid": str(uuid4()), "version": version}],
        }
        if has_script:
            m["modules"].append(
                {
                    "uuid": str(uuid4()),
                    "version": version,
                    "type": "script",
                    "language": "javascript",
                    "entry": "scripts/index.js",
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
        return m

    @staticmethod
    def manifest_rp(version, uuid1, has_pbr):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": uuid1,
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
            m.update({"dependencies": ["pbr"]})
        return m

    @staticmethod
    def manifest_world(version, uuid1, author):
        return {
            "format_version": 2,
            "header": {
                "name": "pack.name",
                "description": "pack.description",
                "version": version,
                "uuid": uuid1,
                "lock_template_options": True,
                "base_game_version": MANIFEST_BUILD,
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
        return [{"pack_id": pack_id, "version": version}]

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
            "main": "index.js",
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
    def description(identifier1, identifier2):
        return {"description": {"identifier": f"{identifier1}:{identifier2}"}}

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
    def dialogue_scene(
        scene_tag, npc_name, text, on_open_commands, on_close_commands, buttons
    ):
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


def CreateDirectory(path: str) -> None:
    """
    Creates a new directory.

    Args:
        path (str): The path to the new directory.
    """
    this_path = os.path.join("./", path.lstrip("/"))
    os.makedirs(this_path, exist_ok=True)


def File(
    name: str, content: str, directory: str, mode: str, skip_tag: bool = False, *args
) -> None:
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
    stamp = f"Generated with Anvil@StarkTMA {__version__}"
    time = datetime.now(datetime.now().astimezone().tzinfo).strftime(
        "%d-%m-%Y %H:%M:%S %z"
    )
    # copyright=f'Property of {COMPANY}'
    copyright = ""
    path = os.path.normpath(os.path.join(directory, name))
    if mode == "w":
        match type:
            case "json" | "material" | "code-workspace":
                out_content = (
                    f"//Filename: {name}\n//{stamp}\n//{time}\n//{copyright}\n\n"
                )
                file_content = json.dumps(
                    content, sort_keys=False, indent=4, ensure_ascii=False
                )
            case "py" | "mcfunction":
                out_content = f"#Filename: {name}\n#{stamp}\n#{time}\n#{copyright}\n\n"
            case "lang":
                out_content = (
                    f"##Filename: {name}\n##{stamp}\n##{time}\n##{copyright}\n\n"
                )
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