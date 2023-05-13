import csv
import math
import os
import random
import shutil
import string
import sys
import time
import uuid
import zipfile
from collections import OrderedDict, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Tuple, Type, overload, Union
from urllib import request

import click
import commentjson as commentjson
import json as json
from PIL import Image, ImageColor, ImageDraw, ImageEnhance, ImageFont, ImageQt

from .__version__ import __version__
from .api import CONFIG
from .api.localization import *

FileExists = lambda path: os.path.exists(path)
MakePath = lambda *paths: os.path.normpath(os.path.join(*[x for x in paths if type(x) is str])).replace("\\", "/")
normalize_180 = lambda angle : (angle + 540) % 360 - 180

APPDATA = os.getenv("APPDATA").rstrip("Roaming")
DESKTOP = MakePath(os.getenv("USERPROFILE"), "Desktop")
MOLANG_PREFIXES = ("q.", "v.", "c.", "t.", "query.", "variable.", "context.", "temp.")

MANIFEST_BUILD = [1, 19, 70]
BLOCK_SERVER_VERSION = "1.19.70"
ENTITY_SERVER_VERSION = "1.19.0"
ENTITY_CLIENT_VERSION = "1.10.0"
BP_ANIMATION_VERSION = "1.10.0"
RP_ANIMATION_VERSION = "1.8.0"
ANIMATION_CONTROLLERS_VERSION = "1.10.0"
SPAWN_RULES_VERSION = "1.8.0"
GEOMETRY_VERSION = "1.12.0"
RENDER_CONTROLLER_VERSION = "1.10.0"
SOUND_DEFINITIONS_VERSION = "1.14.0"
DIALOGUE_VERSION = "1.18.0"
FOG_VERSION = "1.16.100"
MATERIALS_VERSION = "1.0.0"
ITEM_SERVER_VERSION = "1.20.0"

def clamp(value, _min, _max):
    return max(min(_max, value), _min)

class LootPoolType:
    Empty = "empty"
    Item = "item"
    LootTable = "loot_table"

class Population:
    Animal = "animal"
    UnderwaterAnimal = "underwater_animal"
    Monster = "monster"
    Ambient = "ambient"

class Difficulty:
    Peaceful = "peaceful"
    Easy = "easy"
    Normal = "normal"
    Hard = "hard"

class SoundCategory:
    list = ["ambient", "block", "player", "neutral", "hostile", "music", "record", "ui"]

    Ambient = "ambient"
    Block = "block"
    Player = "player"
    Neutral = "neutral"
    Hostile = "hostile"
    Music = "music"
    Record = "record"
    UI = "ui"

class MusicCategory:
    list = [
        "creative",
        "credits",
        "crimson_forest",
        "dripstone_caves",
        "end",
        "endboss",
        "frozen_peaks",
        "game",
        "grove",
        "hell",
        "jagged_peaks",
        "lush_caves",
        "meadow",
        "menu",
        "nether",
        "snowy_slopes",
        "soulsand_valley",
        "stony_peaks",
        "water",
    ]
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
    list = [
        "all",
        "anvil",
        "attack",
        "block_explosion",
        "contact",
        "drowning",
        "entity_explosion",
        "fall",
        "falling_block",
        "fatal",
        "fire",
        "firetick",
        "fly_into_wall",
        "lava",
        "magic",
        "none",
        "override",
        "piston",
        "projectile",
        "sonic_boom",
        "stalactite",
        "stalagmite",
        "starve",
        "suffocation",
        "suicide",
        "thorns",
        "void",
        "wither",
    ]
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

class Target:
    list = ["block", "damager", "other", "parent", "player", "self", "target"]
    Block = "block"
    Damager = "damager"
    Other = "other"
    Parent = "parent"
    Player = "player"
    Self = "self"
    Target = "target"

class Effects:
    Hunger = 'hunger'
    JumpBoost = 'jump'
    Saturation = 'saturation'
    Regeneration = 'regeneration'
    Speed = 'speed'
    Strength = 'strength'
    Slowness = 'slowness'
    Weakness = 'weakness'
    Levitation = 'levitation'
    Regeneration = 'regeneration'
    Wither = 'wither'
    Poison = 'poison'
    Absorption = 'absorption'

class Gamemodes:
    Adventure = 'adventure'
    Creative = 'creative'
    Default = 'default'
    Survival = 'survival'
    Spectator = 'spectator'
    
    A = Adventure
    C = Creative
    D = Default
    S = Survival

class Style:
    Black : str = '§0'
    DarkBlue : str = '§1'
    DarkGreen : str = '§2'
    DarkAqua : str = '§3'
    DarkRed : str = '§4'
    DarkPurple : str = '§5'
    Gold : str = '§6'
    Gray : str = '§7'
    DarkGray : str = '§8'
    Blue : str = '§9'
    Green : str = '§a'
    Aqua : str = '§b'
    Red : str = '§c'
    Purple : str = '§d'
    Yellow : str = '§e'
    White : str = '§f'
    MineconGold : str = '§g'
    Obfuscated : str = '§k'
    Bold : str = '§l'
    Italic : str = '§o'
    Reset : str = '§r'

class FogCameraLocation:
    Air = 'air'
    Lava = 'lava'
    Lava_resistance = 'lava_resistance'
    Powder_snow = 'powder_snow'
    Water = 'water'
    Weather = 'weather'

class RenderDistanceType:
    Render = 'render'
    Fixed = 'fixed'

class Dimension:
    Overworld = 'overworld'
    Nether = 'nether'
    End = 'the_end'

class Operator:
    Less = '<'
    LessEqual = '<='
    Equals = '='
    Greater = '>'
    GreaterEqual = '>='

class ScoreboardOperation:
    Addition = '+='
    Subtraction = '-='
    Multiplication = '*='
    Division = '/='
    Modulus = '%='
    Assign = '='
    Min = '<'
    Max = '>'
    Swaps  = '><'

class Slots:
    Mainhand = 'slot.weapon.mainhand'
    Offhand = 'slot.weapon.offhand'
    Head = 'slot.armor.head'
    Chest = 'slot.armor.chest'
    Legs = 'slot.armor.legs'
    Feet = 'slot.armor.feet'
    Hotbar = 'slot.hotbar'
    Inventory = 'slot.inventory'
    Enderchest = 'slot.enderchest'
    Saddle = 'slot.saddle'
    Armor = 'slot.armor'
    Chest = 'slot.chest'
    Equippable = 'slot.equippable'
    Container = 'slots.container'

class Target():
    P = '@p'
    R = '@r'
    A = '@a'
    E = '@e'
    S = '@s'
    C = '@c'
    V = '@v'
    Initiator = '@initiator'

class Selector():
    def __init__(self, target: Target = Target.S) -> None:
        self.target = target
        self.arguments = []
        
    def _args(self, **args):
        for key, value in args.items():
            if not value is None and {key : value} not in self.arguments:
                self.arguments.append({key : value}) 
        return self
        
    def type(self, *types : str):
        for type in types:
            self._args(type = type)
        return self

    def name(self, name : str):
        self._args(name = name)
        return self

    def family(self, family : str):
        self._args(family = family)
        return self

    def count(self, count : int):
        self._args(c = count)
        return self

    def coordinates(self, *, x : coordinate = None, y : coordinate = None, z : coordinate = None):
        self._args(x=x, y=y, z=z)
        return self

    def distance(self, *, r : coordinate = None, rm : coordinate = None):
        self._args(r=r, rm=rm)
        return self

    def volume(self, *, dx : coordinate = None, dy : coordinate = None, dz : coordinate = None):
        self._args(dx=dx, dy=dy, dz=dz)
        return self

    def scores(self, **scores):
        score_values = {}
        for score, value in scores.items():
            score_values.update({
                score: value
            })
        self._args(scores = score_values)
        return self
    
    def tag(self, *tags : str):
        for tag in tags:
            self._args(tag = tag)
        return self

    def rotation(self, *, ry : rotation = None, rym : rotation = None, rx : rotation = None, rxm : rotation = None):
        self._args(
            ry=normalize_180(round(ry, 2)) if not ry is None else ry,
            rym=normalize_180(round(rym, 2)) if not rym is None else rym,
            rx=clamp(round(rx, 2), -90, 90) if not rx is None else rx,
            rxm=clamp(round(rxm, 2), -90, 90) if not rxm is None else rxm,
        )
        return self

    def haspermission(self, *, camera : bool = None, movement : bool = None):
        permission = {}
        if not camera is None:
            permission.update({"camera": "enabled" if camera else "disabled"})
        if not movement is None:
            permission.update({"movement": "enabled" if movement else "disabled"})

        self._args(haspermission = permission)
        return self

    def hasitem(self, *, item, data : int = -1, quantity : int = None, location : Slots = None, slot : int = None):
        testitem = {
            'item' : item,
            "data": data if data != -1 else None,
            "quantity": quantity,
            "location": location,
            "slot": slot
        }
        self._args(hasitem = testitem)
        return self
    
    def gamemode(self, gamemode : Gamemodes):
        self._args(m = gamemode)
        return self

    def __str__(self):
        if len(self.arguments) > 0:
            args = []
            for i in self.arguments:
                for key, value in i.items():
                    values = value
                    if type(value) is dict:
                        values = f"{{{', '.join(f'{k} = {v}' for k, v in value.items() if not v is None)}}}"
                    args.append(f'{key} = {values}')

            self.target += f"[{', '.join(args)}]"
        return self.target

class Anchor:
    Feet = 'feet'
    Eyes = 'eyes'

class BlockCategory:
    Construction = "construction"
    Nature = "nature"
    Equipment = "equipment"
    Items = "items"
    none = "none"

class BlockMaterial:
    Opaque = 'opaque'
    DoubleSided = 'double_sided'
    Blend = 'blend'
    AlphaTest = 'alpha_test'

class BlockFaces:
    Up = "up"
    Down = "down"
    North = "north"
    South = "south"
    East = "east"
    West = "west"
    Side = "side"
    All = "all"

class BlockDescriptor(dict):
    def __init__(self, name: str, tags: Molang, **states):
        super().__init__(name = name, tags = tags, states = states)

class CameraShakeType():
    positional = 'positional'
    rotational = 'rotational'

class MaskMode():
    replace = 'replace'
    masked = 'masked'

class CloneMode():
    force = 'force'
    move = 'move'
    normal = 'normal'

class WeatherSet():
    Clear = 'clear'
    Rain = 'rain'
    Thunder = 'thunder'

class FilterSubject:
    Block = 'block'
    Damager = 'damager'
    Other = 'other'
    Parent = 'parent'
    Player = 'player'
    Self = 'self'
    Target = 'target'

class FilterOperation:
    Less = '<'
    LessEqual = '<='
    Greater = '>'
    GreaterEqual = '>='
    Equals = 'equals'
    Not = 'not'

class FilterEquipmentDomain:
    Any = 'any'
    Armor = 'armor'
    Feet = 'feet'
    Hand = 'hand'
    Head = 'head'
    Inventory = 'inventory'
    Leg = 'leg'
    Torso = 'torso'

class MaterialStates:
    EnableStencilTest = 'EnableStencilTest'
    StencilWrite = 'StencilWrite'
    InvertCulling = 'InvertCulling'
    DisableCulling = 'DisableCulling'
    DisableDepthWrite = 'DisableDepthWrite'

class MaterialDefinitions:
    Fancy = 'FANCY'
    USE_OVERLAY = 'USE_OVERLAY'
    USE_COLOR_MASK = 'USE_COLOR_MASK'
    MULTI_COLOR_TINT = 'MULTI_COLOR_TINT'
    COLOR_BASED = 'COLOR_BASED'
    
class MaterialFunc:
    Always = 'Always'
    Equal = 'Equal'
    NotEqual = 'NotEqual'
    Less = 'Less'
    Greater = 'Greater'
    GreaterEqual = 'GreaterEqual'
    LessEqual = 'LessEqual'

class MaterialOperation:
    Keep = 'Keep'
    Replace = 'Replace'

class Permission:
    Camera = 'camera'
    Movement = 'movement'

def Schemes(type, *args) -> dict:
    match type:
        # Anvil files
        case "structure":
            return {
                args[0]: {
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
                        'output':{}
                    },
                }
            }
        case "script":
            return (
                "from anvil import *\n\n\n\n"
                'if __name__ == "__main__":\n\n\n'
                f"    ANVIL.compile\n"
                f"    #Uncomment package when you're ready to submit it. Pass True as the argument to clear all assets when packaging\n"
                f"    #ANVIL.package()\n"
            )
        case "code-workspace":
            return {
                "folders": [
                    {"name": "Assets", "path": MakePath(args[0], args[1], "assets")},
                    {"name": args[2], "path": MakePath(args[0], args[1])}
                ]
            }
        case "gitignore":
            return """
#Anvil
assets/vanilla/

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/"""

        #Core
        case "manifest_bp":
            return {
                "format_version": 2,
                "header": {
                    "description": "pack.description",
                    "name": "pack.name",
                    "uuid": str(uuid.uuid4()),
                    "version": args[0],
                    "min_engine_version": MANIFEST_BUILD,
                },
                "modules": [
                    {"type": "data", "uuid": str(uuid.uuid4()), "version": args[0]}
                ]
            }
        case "manifest_rp":
            return {
                "format_version": 2,
                "header": {
                    "description": "pack.description",
                    "name": "pack.name",
                    "uuid": str(uuid.uuid4()),
                    "version": args[0],
                    "min_engine_version": MANIFEST_BUILD,
                },
                "modules": [
                    {
                        "type": "resources",
                        "uuid": str(uuid.uuid4()),
                        "version": args[0],
                    }
                ]
            }
        case "manifest_skins":
            return {
                "format_version": 1,
                "header": {
                    "name": "pack.name",
                    "uuid": str(uuid.uuid4()),
                    "version": args[0],
                },
                "modules": [
                    {
                        "type": "skin_pack",
                        "uuid": str(uuid.uuid4()),
                        "version": args[0],
                    }
                ]
            }
        case "manifest_world":
            return {
                "format_version": 2,
                "header": {
                    "name": "pack.name",
                    "description": "pack.description",
                    "version": args[0],
                    "uuid": str(uuid.uuid4()),
                    "lock_template_options": True,
                    "base_game_version": MANIFEST_BUILD,
                },
                "modules": [
                    {
                        "type": "world_template",
                        "uuid": str(uuid.uuid4()),
                        "version": args[0],
                    }
                ],
                "metadata": {
                    "authors": args[1]
                },
            }
        case "description":
            return {"description": {"identifier": f"{args[0]}:{args[1]}"}}
        case "item_texture":
            return {
                "resource_pack_name": args[0],
                "texture_name": "atlas.items",
                "texture_data": {},
            }
        case "language":
            return f"pack.name={args[0]}\n" f"pack.description={args[1]}\n\n"
        case "skins":
            return {
                "serialize_name": args[0],
                "localization_name": args[0],
                "skins": args[1],
            }
        case "skin_language":
            return f"skinpack.{args[0]}={args[1]}\n"
        case "world_packs":
            return [{"pack_id": args[0], "version": args[1]}]        
        case "sound_definitions":
            return {
                "format_version": SOUND_DEFINITIONS_VERSION,
                "sound_definitions": {},
            }
        case "music_definitions":
            return {}
        case "sound":
            return {args[0]: {"category": args[1], "sounds": []}}
        case "materials":
            return {"materials": {"version": MATERIALS_VERSION}}
        
        #Actors
        case "client_description":
            return {
                "materials": {"default": "entity_alphatest"},
                "scripts": {"pre_animation": [], "initialize": [], "animate": []},
                "textures": {},
                "geometry": {},
                "particle_effects": {},
                "sound_effects": {},
                "render_controllers": [],
            }
        case "client_entity":
            return {
                "format_version": ENTITY_CLIENT_VERSION,
                "minecraft:client_entity": {},
            }
        case "server_entity":
            return {
                "format_version": ENTITY_SERVER_VERSION,
                "minecraft:entity": {
                    "component_groups": {},
                    "components": {},
                    "events": {},
                },
            }
        case "bp_animations":
            return {"format_version": BP_ANIMATION_VERSION, "animations": {}}
        case "bp_animation":
            return {
                f"animation.{args[0]}.{args[1]}.{args[2]}": {
                    "loop": args[3],
                    "timeline": {},
                }
            }
        case "rp_animations":
            return {"format_version": RP_ANIMATION_VERSION, "animations": {}}
        case "animation_controller_state":
            return {
                args[0]: {
                    "on_entry": [],
                    "on_exit": [],
                    "animations": [],
                    "transitions": [],
                }
            }
        case "animation_controller":
            return {
                f"controller.animation.{args[0]}.{args[1]}.{args[2]}": {
                    "initial_state": "default",
                    "states": {},
                }
            }
        case "animation_controllers":
            return {
                "format_version": ANIMATION_CONTROLLERS_VERSION,
                "animation_controllers": {},
            }
        case "geometry":
            return {
                "format_version": GEOMETRY_VERSION,
                "minecraft:geometry": [
                    
                ],
            }
        case "render_controller":
            return {
                f"controller.render.{args[0]}.{args[1]}.{args[2]}": {
                    "arrays": {"textures": {}, "geometries": {}},
                    "materials": [],
                    "geometry": {},
                    "textures": [],
                    "part_visibility": [],
                }
            }
        case "render_controllers":
            return {
                "format_version": RENDER_CONTROLLER_VERSION,
                "render_controllers": {},
            }
        case "attachable":
            return {"format_version": ENTITY_CLIENT_VERSION, "minecraft:attachable": {}}
        case "spawn_rules":
            return {
                "format_version": SPAWN_RULES_VERSION,
                "minecraft:spawn_rules": {"conditions": []},
            }
        
        #Blocks
        case "server_block":
            return {
                "format_version": BLOCK_SERVER_VERSION, 
                "minecraft:block": {
                    "description": {}, 
                    "components": {},
                    "permutations": []
                }
            }
        case "terrain_texture":
            return {
                "num_mip_levels": 4,
                "padding": 8,
                "resource_pack_name": args[0],
                "texture_data": {},
                "texture_name": "atlas.terrain",
            }
        case "flipbook_textures":
            return []
        
        #Extra
        case "font":
            return {
              "version": 1,
              "fonts": [
                {
                  "font_format": "ttf",
                  "font_name": args[0],
                  "version": 1,
                  "font_file": f"font/{args[1]}",
                  "lowPerformanceCompatible": False
                }
              ]
            }
        case "fog":
            return {
                "format_version": FOG_VERSION,
                "minecraft:fog_settings": {
                    "distance": {},
                    "volumetric": {},
                },
            }
        case "dialogues":
            return {
                "format_version": DIALOGUE_VERSION,
                "minecraft:npc_dialogue": {"scenes": []},
            }
        case "dialogue_scene":
            return {
                "scene_tag": args[0],
                "npc_name": args[1],
                "text": args[2],
                "on_open_commands": args[3],
                "on_close_commands": args[4],
                "buttons": args[5],
            }
        case "dialogue_button":
            return {"name": args[0], "commands": args[1]}

        #Items
        case "server_item":
            return {
                "format_version": ITEM_SERVER_VERSION, 
                "minecraft:item": {
                    "description": {}, 
                    "components": {}
                }
            }

def Defaults(type, *args):
    match type:
        case "animation_controllers_rp":
            return {"format_version": "1.10.0", "animation_controllers": {}}
        case "animation":
            return {"format_version": "1.10.0", "animations": {}}
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
                    "components": {
                        "minecraft:use_animation": "none"
                    },
                },
            }
        case "bp_block_v1":
            return {
                "format_version": "1.12.0",
                "minecraft:block": {
                    "description": {
                        "identifier": f"{args[0]}:{args[1]}",
                        "is_experimental": False,
                        "register_to_creative_menu": True
                    },
                    "components": {},
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
        case "language":
            return f"pack.name={args[0]}\n" f"pack.description={args[1]}\n\n"
        case "manifest_bp":
            return {
                "format_version": 2,
                "header": {
                    "description": "pack.description",
                    "name": "pack.name",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0],
                    "min_engine_version": [1, 18, 0],
                },
                "modules": [
                    {
                        "description": "pack.description",
                        "type": "data",
                        "uuid": str(uuid.uuid4()),
                        "version": [1, 0, 0],
                    }
                ],
            }
        case "manifest_rp":
            return {
                "format_version": 2,
                "header": {
                    "description": "pack.description",
                    "name": "pack.name",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0],
                    "min_engine_version": [1, 16, 220],
                },
                "modules": [
                    {
                        "description": "pack.description",
                        "type": "resources",
                        "uuid": str(uuid.uuid4()),
                        "version": [1, 0, 0],
                    }
                ],
            }
        case "languages":
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
        case "blocks":
            return {"format_version": "1.10.0"}
        case "terrain_texture":
            return {
                "resource_pack_name": args[0],
                "texture_name": "atlas.terrain",
                "padding": 8,
                "num_miplevels": 4,
                "texture_data": {},
            }
        case "loot_table":
            return {"pools": []}
        case "sounds":
            return {"entity_sounds": {"entities": {}}}
        case "world_packs":
            return [{"pack_id": args[0], "version": args[1]}]
        case "script":
            return (
                "from anvil import *\n\n\n\n"
                'if __name__ == "__main__":\n\n\n'
                f"    ANVIL.compile\n"
                f"    #Uncomment package when you're ready to submit it. Pass True as the argument to clear all assets when packaging\n"
                f"    #ANVIL.package()\n"
            )
        case "settings":
            return (
                "# This is the wrong script to run\n"
                "# Use this script to edit projects settings\n"
                "from os import path\n\n"
                "BASE_DIR = path.dirname(path.realpath(__file__))\n"
            )
        case "config":
            return {
                "COMPANY": args[1].title(),
                "NAMESPACE": args[0],
                "PROJECT_NAME": args[2],
                "DISPLAY_NAME": args[3].replace("_", " ").replace("-", " ").title(),
                "PROJECT_DESCRIPTION": f'{args[4].replace("_", " ").replace("-", " ").title()}',
                "VANILLA_VERSION": args[5],
                "LAST_CHECK": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        case "structure":
            return {
                args[0]: {
                    "behavior_packs": {f"BP_{args[0]}": {"texts": {}}},
                    "resource_packs": {f"RP_{args[0]}": {"texts": {}}},
                    "assets": {
                        "animations": {},
                        "blocks": {},
                        "cache": {},
                        "geometries": {},
                        "items": {},
                        "particles": {},
                        "sounds": {},
                        "structures": {},
                        "textures": {},
                        "vanilla": {},
                        "marketing": {},
                    },
                }
            }
        case "code-workspace":
            return {
                "folders": [
                    {"path": f"{args[0]}/{args[1]}"},
                    {
                        "name": "BP.zip",
                        "uri": f"zip:{args[0]}/{args[1]}/assets/vanilla/BP.zip",
                    },
                    {
                        "name": "RP.zip",
                        "uri": f"zip:{args[0]}/{args[1]}/assets/vanilla/RP.zip",
                    },
                ],
                "settings": {"docwriter.style": "JSDoc"},
            }
        case "entity_rp":
            return {
                "format_version": "1.10.0",
                "minecraft:client_entity": {
                    "description": {
                        "identifier": f"{args[0]}:{args[1]}",
                        "materials": {"default": "entity_alphatest"},
                        "scripts": {},
                        "textures": {},
                        "geometry": {},
                        "render_controllers": [],
                    }
                },
            }
        case "entity_bp":
            return {"format_version": "1.16.0", "minecraft:entity": {}}
        case "render_controller":
            return {"format_version": "1.10.0", "render_controllers": {}}


def RawText(text: str):
    snake_case_name = text.lower().replace(" ", "_").replace("\n", "%1")
    display_name = text.replace("_", " ").title()
    return snake_case_name, display_name


def random_character_generator(length: int):
    return "".join(random.choice(string.ascii_letters) for i in range(length))


def CreateImage(name: str, width: int, height: int, color, directory=""):
    img = Image.new("RGBA", (width, height), color=color)
    img.save(f"{directory}/{name}.png")


def GetColors(image):
    original = Image.open(image)
    reduced = original.convert("P", palette=Image.WEB)
    palette = reduced.getpalette()
    palette = [palette[3 * n : 3 * n + 3] for n in range(256)]
    color_count = [(n, palette[m]) for n, m in reduced.getcolors()]
    most = "#{0:02x}{1:02x}{2:02x}".format(
        color_count[0][1][0], color_count[0][1][1], color_count[0][1][2]
    )
    least = "#{0:02x}{1:02x}{2:02x}".format(
        color_count[-1][1][0], color_count[-1][1][1], color_count[-1][1][2]
    )
    return most, least


def RaiseError(text):
    raise SystemExit(text)


def CheckAvailability(file, type, folder):
    if FileExists(f"{folder}/{file}") is False:
        RaiseError(MISSING_FILE(type, file, folder))
        

def CreateDirectoriesFromTree(tree):
    def find_key(tree, path, a):
        for key, value in tree.items():
            if isinstance(value, dict):
                find_key(value, f"{path}/{key}", a)
            if value == {}:
                a.append(f"{path}/{key}")
        return a

    directories = find_key(tree, "", a=[])
    for dir in directories:
        CreateDirectory(dir)


def ShortenDict(d):
    if isinstance(d, dict):
        return {
            k: v
            for k, v in ((k, ShortenDict(v)) for k, v in d.items())
            if v != {} and v != [] or str(k).startswith("minecraft:")
        }

    elif isinstance(d, list):
        return [v for v in map(ShortenDict, d) if v != []]

    return d


def CreateTreeFromPath(path):
    def get_path(my_list):
        if len(my_list) > 0 and my_list[0] != "":
            return {my_list[0]: get_path(my_list[1::])}
        else:
            return {}

    my_list = path.split("/")
    tree = get_path(my_list)
    return tree


def GetPathFromTree(tree, keyword):
    def find_key(tree, keyword):
        for key, value in tree.items():
            if key == keyword:
                return [key]
            elif isinstance(value, dict):
                p = find_key(value, keyword)
                if p:
                    return [key] + p

    path = find_key(tree, keyword)
    return "/".join(path)


def RemoveDirectory(path):
    shutil.rmtree(f"./{path}", ignore_errors=True)


def RemoveFile(path):
    os.remove(path)


def CreateDirectory(path: str):
    this_path = os.path.join("./", path.lstrip("/"))
    os.makedirs(this_path, exist_ok=True)


def MoveFiles(old_dir: str, new_dir: str, file_name: str):
    CreateDirectory(new_dir)
    os.replace(f"{old_dir}/{file_name}", f"{new_dir}/{file_name}")


def CopyFiles(old_dir: str, new_dir: str, target_file: str, rename: str = None):
    CreateDirectory(new_dir)
    if rename is None:
        shutil.copyfile(MakePath(old_dir, target_file), MakePath(new_dir, target_file))
    else:
        shutil.copyfile(MakePath(old_dir, target_file), MakePath(new_dir, rename))


def CopyFolder(old_dir: str, new_dir: str):
    CreateDirectory(new_dir)
    shutil.copytree(
        os.path.realpath(old_dir), os.path.realpath(new_dir), dirs_exist_ok=True
    )


def File(name: str, content, directory: str, mode: str, *args):
    CreateDirectory(directory)
    type = name.split(".")[-1]
    out_content = ""
    file_content = content
    stamp = f"Generated with Anvil@StarkTMA {__version__}"
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

    out_content += file_content
    prev = ""
    
    if FileExists(path):
        with open(path, "r", encoding="utf-8") as file:
            prev = file.read()
    
    if prev.split("\n")[6::] != file_content.split("\n"):
        with open(path, mode, encoding="utf-8") as file:
            file.write(out_content)


def DownloadFile(url: str, save_path: str):
    def report_hook(count, block_size, total_size):
        progress = 100.0 * count * block_size / total_size
        # Converting  from B to MB
        downloaded = round((count * block_size) * pow(10, -6), 1)
        total = round(total_size * pow(10, -6), 1)
        bar = int((downloaded / total) * 20)
        if progress <= 100:
            click.echo(f"\rDownloading: ", nl=False)
            click.echo(click.style("━" * bar, fg="bright_magenta"), nl=False)
            click.echo(click.style(f"╸", fg="bright_magenta"), nl=False)
            click.echo(click.style("━" * (20 - bar), fg="bright_black"), nl=False)
            click.echo(click.style(f"  {downloaded}/{total} MB", fg="green"), nl=False)
        else:
            click.echo(f"\rDownloading: ", nl=False)
            click.echo(click.style("━" * 20, fg="bright_green"), nl=False)
            click.echo(click.style(f"╸", fg="bright_green"))

    request.urlretrieve(url, save_path, reporthook=report_hook)


def header():
    os.system("cls")
    click.echo(MODULE)
    click.echo(VERSION(__version__))
    click.echo(COPYRIGHT(datetime.now().year))



def frange(start: int, stop: int, num: float = 1):
    """
    Interpolate `num` values between `start` and `stop`.
    """
    step = (stop - start) / (num - 1)
    values = [round(start + i * step, 2) for i in range(num)]
    return values


def zipit(zip_name, dir_list:dict):
    def zipdir(ziph:zipfile.ZipFile, source, target):
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source):
                for file in files:
                    ziph.write(
                        os.path.join(root, file),
                        os.path.join(target,os.path.relpath(os.path.join(root, file), os.path.join(source, '.')))
                    )
        else:
            ziph.write(source,os.path.relpath(os.path.join(target,source), os.path.join(source, '..')))
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for source, target in dir_list.items():
        zipdir(zipf, source, target)
    zipf.close()