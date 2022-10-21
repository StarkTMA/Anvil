from ast import Global
import commentjson as json
from urllib import request
import os
import sys
import numpy as np
import zipfile
import shutil
import csv
import random
import string
import uuid
import click
from datetime import datetime
from fnmatch import fnmatch
from typing import overload,NewType,Tuple
from collections import defaultdict, OrderedDict
from PIL import Image, ImageColor, ImageEnhance, ImageQt
import time
from pprint import pprint
from . __version__ import __version__
from .submodules.localization import *

FileExists = lambda path : os.path.exists(path)
MakePath = lambda *paths : os.path.normpath(os.path.join(*[ x for x in paths if type(x) is str ])).replace('\\','/')

APPDATA = os.getenv('APPDATA').rstrip('Roaming')
DESKTOP = MakePath(os.getenv('USERPROFILE'),'Desktop')
MOLANG_PREFIXES = ['q.','v.','c.','t.','query.','variable.','context.','temp.']

Seconds = NewType('Seconds',str)

class LootPoolType():
    Empty  = 'empty'
    Item = 'item'
    LootTable = 'loot_table'

class Population():
    Animal = 'animal'
    UnderwaterAnimal = 'underwater_animal'
    Monster = 'monster'
    Ambient = 'ambient'

class Difficulty():
    Peaceful = 'peaceful'
    Easy = 'easy'
    Normal = 'normal'
    Hard = 'hard' 

class Vanilla():
    #Updated on 21-10-2022
    # Latest Updated release: 1.19.31
    # Latest Updated preview: 1.19.50.21
    class Entities():
        _list = [
            "armor_stand", "arrow", "axolotl", "bat", "bee",
            "blaze", "cat", "cave_spider", "chicken", "cow",
            "creeper", "dolphin", "donkey", "drowned", "elder_guardian",
            "ender_dragon", "enderman", "endermite", "evocation_illager",
            "fish", "fox", "ghast", "glow_squid", "goat", "guardian",
            "hoglin", "horse", "husk", "iron_golem", "llama",
            "magma_cube", "mooshroom", "mule", "npc", "ocelot",
            "panda", "parrot", "phantom", "pig", "piglin_brute",
            "piglin", "pillager", "player", "polar_bear", "pufferfish",
            "rabbit", "ravager", "salmon", "sheep", "shulker", "silverfish",
            "skeleton_horse", "skeleton", "slime", "snow_golem",
            "spider", "squid", "stray", "strider", "tropicalfish",
            "turtle", "vex", "villager_v2", "vindicator", "wandering_trader",
            "witch", 'wither_skull', 'wither_skull_dangerous', "wither_skeleton", "wither", "wolf", "zoglin",
            "zombie_horse", "zombie_pigman", "zombie_villager_v2", "zombie", 
            'boat', 'snowball', 'fishing_hook', 'fireball', 'llama_spit', 'thrown_trident'
        ]
        ArmorStand="armor_stand"
        Arrow="arrow"
        Axolotl="axolotl"
        Bat="bat"
        Bee="bee"
        Blaze="blaze"
        Cat="cat"
        CaveSpider="cave_spider"
        Chicken="chicken"
        Cow="cow"
        Creeper="creeper"
        Dolphin="dolphin"
        Donkey="donkey"
        Drowned="drowned"
        ElderGuardian="elder_guardian"
        EnderDragon="ender_dragon"
        Enderman="enderman"
        Endermite="endermite"
        EvocationIllager="evocation_illager"
        Fish="fish"
        FishingHook = 'fishing_hook'
        Fireball = 'fireball'
        Fox="fox"
        Ghast="ghast"
        GlowSquid="glow_squid"
        Goat="goat"
        Guardian="guardian"
        Hoglin="hoglin"
        Horse="horse"
        Husk="husk"
        IronGolem="iron_golem"
        Llama="llama"
        LlamaSpit = 'llama_spit'
        MagmaCube="magma_cube"
        Mooshroom="mooshroom"
        Mule="mule"
        Npc="npc"
        Ocelot="ocelot"
        Panda="panda"
        Parrot="parrot"
        Phantom="phantom"
        Pig="pig"
        PiglinBrute="piglin_brute"
        Piglin="piglin"
        Pillager="pillager"
        Player="player"
        PolarBear="polar_bear"
        Pufferfish="pufferfish"
        Rabbit="rabbit"
        Ravager="ravager"
        Salmon="salmon"
        Sheep="sheep"
        Shulker="shulker"
        Silverfish="silverfish"
        SkeletonHorse="skeleton_horse"
        Skeleton="skeleton"
        Slime="slime"
        SnowGolem="snow_golem"
        Spider="spider"
        Squid="squid"
        Stray="stray"
        Strider="strider"
        Tropicalfish="tropicalfish"
        ThrownTrident = 'thrown_trident'
        Turtle="turtle"
        Vex="vex"
        Villager="villager_v2"
        Vindicator="vindicator"
        WanderingTrader="wandering_trader"
        Witch="witch"
        WitherSkull="wither_skull"
        WitherSkullDangeroud="wither_skull_dangerous"
        WitherSkeleton="wither_skeleton"
        Wither="wither"
        Wolf="wolf"
        Zoglin="zoglin"
        ZombieHorse="zombie_horse"
        ZombiePigman="zombie_pigman"
        ZombieVillager="zombie_villager_v2"
        Zombie="zombie"
        Boat ="boat"
        Snowball ="snowball"
        # 1.19.0
        #Updated on 11-07-2022
        _list.append('warden')
        Warden="warden"
        # 1.19.50.21
        #Updated on 21-10-2022
        _list.append('camel')
        Camel="camel"

    class BlocksItems:
        _list = {
        # Planks
        "minecraft:oak_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Planks",
            "icon_path": "icons/oak_planks.png",
            "identifier": "minecraft:planks"
        },
        "minecraft:spruce_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Planks",
            "icon_path": "icons/spruce_planks.png",
            "identifier": "minecraft:planks"
        },
        "minecraft:birch_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Planks",
            "icon_path": "icons/birch_planks.png",
            "identifier": "minecraft:planks"
        },
        "minecraft:jungle_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Planks",
            "icon_path": "icons/jungle_planks.png",
            "identifier": "minecraft:planks"
        },
        "minecraft:acacia_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Acacia Planks",
            "icon_path": "icons/acacia_planks.png",
            "identifier": "minecraft:planks"
        },
        "minecraft:dark_oak_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Dark Oak Planks",
            "icon_path": "icons/dark_oak_planks.png",
            "identifier": "minecraft:planks"
        },
        "minecraft:mangrove_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Mangrove Planks",
            "icon_path": "icons/mangrove_planks.png",
            "identifier": "minecraft:mangrove_planks"
        },
        "minecraft:crimson_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Planks",
            "icon_path": "icons/crimson_planks.png",
            "identifier": "minecraft:crimson_planks"
        },
        "minecraft:warped_planks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Planks",
            "icon_path": "icons/warped_planks.png",
            "identifier": "minecraft:warped_planks"
        },
        # Walls
        "minecraft:cobblestone_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobblestone Wall",
            "icon_path": "icons/cobblestone_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:mossy_cobblestone_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Mossy Cobblestone Wall",
            "icon_path": "icons/mossy_cobblestone_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:granite_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Granite Wall",
            "icon_path": "icons/granite_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:diorite_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Diorite Wall",
            "icon_path": "icons/diorite_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:andesite_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Andesite Wall",
            "icon_path": "icons/andesite_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:sandstone_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Sandstone Wall",
            "icon_path": "icons/sandstone_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:red_sandstone_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Red Sandstone Wall",
            "icon_path": "icons/red_sandstone_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:stone_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Stone Brick Wall",
            "icon_path": "icons/stone_brick_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:mossy_stone_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Mossy Stone Brick Wall",
            "icon_path": "icons/mossy_stone_brick_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Brick Wall",
            "icon_path": "icons/brick_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:nether_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 9,
            "display_name": "Nether Brick Wall",
            "icon_path": "icons/nether_brick_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:red_nether_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 13,
            "display_name": "Red Nether Brick Wall",
            "icon_path": "icons/red_nether_brick_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:end_stone_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 10,
            "display_name": "End Stone Brick Wall",
            "icon_path": "icons/end_stone_brick_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:prismarine_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Prismarine Wall",
            "icon_path": "icons/prismarine_wall.png",
            "identifier": "minecraft:cobblestone_wall"
        },
        "minecraft:blackstone_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Blackstone Wall",
            "icon_path": "icons/blackstone_wall.png",
            "identifier": "minecraft:blackstone_wall"
        },
        "minecraft:polished_blackstone_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Wall",
            "icon_path": "icons/polished_blackstone_wall.png",
            "identifier": "minecraft:polished_blackstone_wall"
        },
        "minecraft:polished_blackstone_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Brick Wall",
            "icon_path": "icons/polished_blackstone_brick_wall.png",
            "identifier": "minecraft:polished_blackstone_brick_wall"
        },
        "minecraft:cobbled_deepslate_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobbled Deepslate Wall",
            "icon_path": "icons/cobbled_deepslate_wall.png",
            "identifier": "minecraft:cobbled_deepslate_wall"
        },
        "minecraft:deepslate_tile_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Tile Wall",
            "icon_path": "icons/deepslate_tile_wall.png",
            "identifier": "minecraft:deepslate_tile_wall"
        },
        "minecraft:polished_deepslate_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Deepslate Wall",
            "icon_path": "icons/polished_deepslate_wall.png",
            "identifier": "minecraft:polished_deepslate_wall"
        },
        "minecraft:deepslate_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Brick Wall",
            "icon_path": "icons/deepslate_brick_wall.png",
            "identifier": "minecraft:deepslate_brick_wall"
        },
        "minecraft:mud_brick_wall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mud Brick Wall",
            "icon_path": "icons/mud_brick_wall.png",
            "identifier": "minecraft:mud_brick_wall"
        },
        # Fences
        "minecraft:oak_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Fence",
            "icon_path": "icons/oak_fence.png",
            "identifier": "minecraft:fence"
        },
        "minecraft:spruce_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Fence",
            "icon_path": "icons/spruce_fence.png",
            "identifier": "minecraft:fence"
        },
        "minecraft:birch_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Fence",
            "icon_path": "icons/birch_fence.png",
            "identifier": "minecraft:fence"
        },
        "minecraft:jungle_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Fence",
            "icon_path": "icons/jungle_fence.png",
            "identifier": "minecraft:fence"
        },
        "minecraft:acacia_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Acacia Fence",
            "icon_path": "icons/acacia_fence.png",
            "identifier": "minecraft:fence"
        },
        "minecraft:dark_oak_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Dark Oak Fence",
            "icon_path": "icons/dark_oak_fence.png",
            "identifier": "minecraft:fence"
        },
        "minecraft:mangrove_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Mangrove Fence",
            "icon_path": "icons/mangrove_fence.png",
            "identifier": "minecraft:mangrove_fence"
        },
        "minecraft:nether_brick_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Brick Fence",
            "icon_path": "icons/nether_brick_fence.png",
            "identifier": "minecraft:nether_brick_fence"
        },
        "minecraft:crimson_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Fence",
            "icon_path": "icons/crimson_fence.png",
            "identifier": "minecraft:crimson_fence"
        },
        "minecraft:warped_fence": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Fence",
            "icon_path": "icons/warped_fence.png",
            "identifier": "minecraft:warped_fence"
        },
        # Fence Gates
        "minecraft:oak_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Fence Gate",
            "icon_path": "icons/oak_fence_gate.png",
            "identifier": "minecraft:fence_gate"
        },
        "minecraft:spruce_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Fence Gate",
            "icon_path": "icons/spruce_fence_gate.png",
            "identifier": "minecraft:spruce_fence_gate"
        },
        "minecraft:birch_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Fence Gate",
            "icon_path": "icons/birch_fence_gate.png",
            "identifier": "minecraft:birch_fence_gate"
        },
        "minecraft:jungle_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Fence Gate",
            "icon_path": "icons/jungle_fence_gate.png",
            "identifier": "minecraft:jungle_fence_gate"
        },
        "minecraft:acacia_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Fence Gate",
            "icon_path": "icons/acacia_fence_gate.png",
            "identifier": "minecraft:acacia_fence_gate"
        },
        "minecraft:dark_oak_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Fence Gate",
            "icon_path": "icons/dark_oak_fence_gate.png",
            "identifier": "minecraft:dark_oak_fence_gate"
        },
        "minecraft:mangrove_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Fence Gate",
            "icon_path": "icons/mangrove_fence_gate.png",
            "identifier": "minecraft:mangrove_fence_gate"
        },
        "minecraft:crimson_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Fence Gate",
            "icon_path": "icons/crimson_fence_gate.png",
            "identifier": "minecraft:crimson_fence_gate"
        },
        "minecraft:warped_fence_gate": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Fence Gate",
            "icon_path": "icons/warped_fence_gate.png",
            "identifier": "minecraft:warped_fence_gate"
        },
        # Stairs
        "minecraft:stone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Stairs",
            "icon_path": "icons/stone_stairs.png",
            "identifier": "minecraft:normal_stone_stairs"
        },
        "minecraft:cobblestone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobblestone Stairs",
            "icon_path": "icons/cobblestone_stairs.png",
            "identifier": "minecraft:stone_stairs"
        },
        "minecraft:mossy_cobblestone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mossy Cobblestone Stairs",
            "icon_path": "icons/mossy_cobblestone_stairs.png",
            "identifier": "minecraft:mossy_cobblestone_stairs"
        },
        "minecraft:oak_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Wood Stairs",
            "icon_path": "icons/oak_stairs.png",
            "identifier": "minecraft:oak_stairs"
        },
        "minecraft:spruce_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Wood Stairs",
            "icon_path": "icons/spruce_stairs.png",
            "identifier": "minecraft:spruce_stairs"
        },
        "minecraft:birch_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Wood Stairs",
            "icon_path": "icons/birch_stairs.png",
            "identifier": "minecraft:birch_stairs"
        },
        "minecraft:jungle_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Wood Stairs",
            "icon_path": "icons/jungle_stairs.png",
            "identifier": "minecraft:jungle_stairs"
        },
        "minecraft:acacia_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Wood Stairs",
            "icon_path": "icons/acacia_stairs.png",
            "identifier": "minecraft:acacia_stairs"
        },
        "minecraft:dark_oak_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Wood Stairs",
            "icon_path": "icons/dark_oak_stairs.png",
            "identifier": "minecraft:dark_oak_stairs"
        },
        "minecraft:mangrove_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Stairs",
            "icon_path": "icons/mangrove_stairs.png",
            "identifier": "minecraft:mangrove_stairs"
        },
        "minecraft:stone_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Brick Stairs",
            "icon_path": "icons/stone_brick_stairs.png",
            "identifier": "minecraft:stone_brick_stairs"
        },
        "minecraft:mossy_stone_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mossy Stone Brick Stairs",
            "icon_path": "icons/mossy_stone_brick_stairs.png",
            "identifier": "minecraft:mossy_stone_brick_stairs"
        },
        "minecraft:sandstone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sandstone Stairs",
            "icon_path": "icons/sandstone_stairs.png",
            "identifier": "minecraft:sandstone_stairs"
        },
        "minecraft:smooth_sandstone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Smooth Sandstone Stairs",
            "icon_path": "icons/smooth_sandstone_stairs.png",
            "identifier": "minecraft:smooth_sandstone_stairs"
        },
        "minecraft:red_sandstone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Sandstone Stairs",
            "icon_path": "icons/red_sandstone_stairs.png",
            "identifier": "minecraft:red_sandstone_stairs"
        },
        "minecraft:smooth_red_sandstone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Smooth Red Sandstone Stairs",
            "icon_path": "icons/smooth_red_sandstone_stairs.png",
            "identifier": "minecraft:smooth_red_sandstone_stairs"
        },
        "minecraft:granite_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Granite Stairs",
            "icon_path": "icons/granite_stairs.png",
            "identifier": "minecraft:granite_stairs"
        },
        "minecraft:polished_granite_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Granite Stairs",
            "icon_path": "icons/polished_granite_stairs.png",
            "identifier": "minecraft:polished_granite_stairs"
        },
        "minecraft:diorite_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diorite Stairs",
            "icon_path": "icons/diorite_stairs.png",
            "identifier": "minecraft:diorite_stairs"
        },
        "minecraft:polished_diorite_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Diorite Stairs",
            "icon_path": "icons/polished_diorite_stairs.png",
            "identifier": "minecraft:polished_diorite_stairs"
        },
        "minecraft:andesite_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Andesite Stairs",
            "icon_path": "icons/andesite_stairs.png",
            "identifier": "minecraft:andesite_stairs"
        },
        "minecraft:polished_andesite_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Andesite Stairs",
            "icon_path": "icons/polished_andesite_stairs.png",
            "identifier": "minecraft:polished_andesite_stairs"
        },
        "minecraft:brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brick Stairs",
            "icon_path": "icons/brick_stairs.png",
            "identifier": "minecraft:brick_stairs"
        },
        "minecraft:nether_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Brick Stairs",
            "icon_path": "icons/nether_brick_stairs.png",
            "identifier": "minecraft:nether_brick_stairs"
        },
        "minecraft:red_nether_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Red Nether Brick Stairs",
            "icon_path": "icons/red_nether_brick_stairs.png",
            "identifier": "minecraft:red_nether_brick_stairs"
        },
        "minecraft:end_stone_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Stone Brick Stairs",
            "icon_path": "icons/end_stone_brick_stairs.png",
            "identifier": "minecraft:end_brick_stairs"
        },
        "minecraft:quartz_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Quartz Stairs",
            "icon_path": "icons/quartz_stairs.png",
            "identifier": "minecraft:quartz_stairs"
        },
        "minecraft:smooth_quartz_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Smooth Quartz Stairs",
            "icon_path": "icons/smooth_quartz_stairs.png",
            "identifier": "minecraft:smooth_quartz_stairs"
        },
        "minecraft:purpur_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Purpur Stairs",
            "icon_path": "icons/purpur_stairs.png",
            "identifier": "minecraft:purpur_stairs"
        },
        "minecraft:prismarine_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Prismarine Stairs",
            "icon_path": "icons/prismarine_stairs.png",
            "identifier": "minecraft:prismarine_stairs"
        },
        "minecraft:dark_prismarine_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Prismarine Stairs",
            "icon_path": "icons/dark_prismarine_stairs.png",
            "identifier": "minecraft:dark_prismarine_stairs"
        },
        "minecraft:prismarine_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Prismarine Brick Stairs",
            "icon_path": "icons/prismarine_brick_stairs.png",
            "identifier": "minecraft:prismarine_bricks_stairs"
        },
        "minecraft:crimson_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Stairs",
            "icon_path": "icons/crimson_stairs.png",
            "identifier": "minecraft:crimson_stairs"
        },
        "minecraft:warped_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Stairs",
            "icon_path": "icons/warped_stairs.png",
            "identifier": "minecraft:warped_stairs"
        },
        "minecraft:blackstone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Blackstone Stairs",
            "icon_path": "icons/blackstone_stairs.png",
            "identifier": "minecraft:blackstone_stairs"
        },
        "minecraft:polished_blackstone_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Stairs",
            "icon_path": "icons/polished_blackstone_stairs.png",
            "identifier": "minecraft:polished_blackstone_stairs"
        },
        "minecraft:polished_blackstone_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Brick Stairs",
            "icon_path": "icons/polished_blackstone_brick_stairs.png",
            "identifier": "minecraft:polished_blackstone_brick_stairs"
        },
        "minecraft:cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cut Copper Stairs",
            "icon_path": "icons/cut_copper_stairs.png",
            "identifier": "minecraft:cut_copper_stairs"
        },
        "minecraft:exposed_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Exposed Cut Copper Stairs",
            "icon_path": "icons/exposed_cut_copper_stairs.png",
            "identifier": "minecraft:exposed_cut_copper_stairs"
        },
        "minecraft:weathered_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Weathered Cut Copper Stairs",
            "icon_path": "icons/weathered_cut_copper_stairs.png",
            "identifier": "minecraft:weathered_cut_copper_stairs"
        },
        "minecraft:oxidized_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oxidized Cut Copper Stairs",
            "icon_path": "icons/oxidized_cut_copper_stairs.png",
            "identifier": "minecraft:oxidized_cut_copper_stairs"
        },
        "minecraft:waxed_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Cut Copper Stairs",
            "icon_path": "icons/waxed_cut_copper_stairs.png",
            "identifier": "minecraft:waxed_cut_copper_stairs"
        },
        "minecraft:waxed_exposed_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Exposed Cut Copper Stairs",
            "icon_path": "icons/waxed_exposed_cut_copper_stairs.png",
            "identifier": "minecraft:waxed_exposed_cut_copper_stairs"
        },
        "minecraft:waxed_weathered_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Weathered Cut Copper Stairs",
            "icon_path": "icons/waxed_weathered_cut_copper_stairs.png",
            "identifier": "minecraft:waxed_weathered_cut_copper_stairs"
        },
        "minecraft:waxed_oxidized_cut_copper_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Oxidized Cut Copper Stairs",
            "icon_path": "icons/waxed_oxidized_cut_copper_stairs.png",
            "identifier": "minecraft:waxed_oxidized_cut_copper_stairs"
        },
        "minecraft:cobbled_deepslate_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobbled Deepslate Stairs",
            "icon_path": "icons/cobbled_deepslate_stairs.png",
            "identifier": "minecraft:cobbled_deepslate_stairs"
        },
        "minecraft:deepslate_tile_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Tile Stairs",
            "icon_path": "icons/deepslate_tile_stairs.png",
            "identifier": "minecraft:deepslate_tile_stairs"
        },
        "minecraft:polished_deepslate_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Deepslate Stairs",
            "icon_path": "icons/polished_deepslate_stairs.png",
            "identifier": "minecraft:polished_deepslate_stairs"
        },
        "minecraft:deepslate_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Brick Stairs",
            "icon_path": "icons/deepslate_brick_stairs.png",
            "identifier": "minecraft:deepslate_brick_stairs"
        },
        "minecraft:mud_brick_stairs": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mud Brick Stairs",
            "icon_path": "icons/mud_brick_stairs.png",
            "identifier": "minecraft:mud_brick_stairs"
        },
        # Doors
        "minecraft:oak_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Door",
            "icon_path": "icons/oak_door.png",
            "identifier": "minecraft:wooden_door"
        },
        "minecraft:spruce_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Door",
            "icon_path": "icons/spruce_door.png",
            "identifier": "minecraft:spruce_door"
        },
        "minecraft:birch_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Door",
            "icon_path": "icons/birch_door.png",
            "identifier": "minecraft:birch_door"
        },
        "minecraft:jungle_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Door",
            "icon_path": "icons/jungle_door.png",
            "identifier": "minecraft:jungle_door"
        },
        "minecraft:acacia_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Door",
            "icon_path": "icons/acacia_door.png",
            "identifier": "minecraft:acacia_door"
        },
        "minecraft:dark_oak_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Door",
            "icon_path": "icons/dark_oak_door.png",
            "identifier": "minecraft:dark_oak_door"
        },
        "minecraft:mangrove_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Door",
            "icon_path": "icons/mangrove_door.png",
            "identifier": "minecraft:mangrove_door"
        },
        "minecraft:iron_door": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Door",
            "icon_path": "icons/iron_door.png",
            "identifier": "minecraft:iron_door"
        },
        "minecraft:crimson_door": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Door",
            "icon_path": "icons/crimson_door.png",
            "identifier": "minecraft:crimson_door"
        },
        "minecraft:warped_door": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Door",
            "icon_path": "icons/warped_door.png",
            "identifier": "minecraft:warped_door"
        },
        # Trapsdoors
        "minecraft:oak_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Trapdoor",
            "icon_path": "icons/oak_trapdoor.png",
            "identifier": "minecraft:trapdoor"
        },
        "minecraft:spruce_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Trapdoor",
            "icon_path": "icons/spruce_trapdoor.png",
            "identifier": "minecraft:spruce_trapdoor"
        },
        "minecraft:birch_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Trapdoor",
            "icon_path": "icons/birch_trapdoor.png",
            "identifier": "minecraft:birch_trapdoor"
        },
        "minecraft:jungle_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Trapdoor",
            "icon_path": "icons/jungle_trapdoor.png",
            "identifier": "minecraft:jungle_trapdoor"
        },
        "minecraft:acacia_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Trapdoor",
            "icon_path": "icons/acacia_trapdoor.png",
            "identifier": "minecraft:acacia_trapdoor"
        },
        "minecraft:dark_oak_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Trapdoor",
            "icon_path": "icons/dark_oak_trapdoor.png",
            "identifier": "minecraft:dark_oak_trapdoor"
        },
        "minecraft:mangrove_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Trapdoor",
            "icon_path": "icons/mangrove_trapdoor.png",
            "identifier": "minecraft:mangrove_trapdoor"
        },
        "minecraft:iron_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Trapdoor",
            "icon_path": "icons/iron_trapdoor.png",
            "identifier": "minecraft:iron_trapdoor"
        },
        "minecraft:crimson_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Trapdoor",
            "icon_path": "icons/crimson_trapdoor.png",
            "identifier": "minecraft:crimson_trapdoor"
        },
        "minecraft:warped_trapdoor": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Trapdoor",
            "icon_path": "icons/warped_trapdoor.png",
            "identifier": "minecraft:warped_trapdoor"
        },
        #
        "minecraft:iron_bars": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Bars",
            "icon_path": "icons/iron_bars.png",
            "identifier": "minecraft:iron_bars"
        },
        # Glass
        "minecraft:glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glass",
            "icon_path": "icons/glass.png",
            "identifier": "minecraft:glass"
        },
        "minecraft:white_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Stained Glass",
            "icon_path": "icons/white_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:gray_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Stained Glass",
            "icon_path": "icons/gray_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:light_gray_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Stained Glass",
            "icon_path": "icons/light_gray_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:black_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Stained Glass",
            "icon_path": "icons/black_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:brown_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Stained Glass",
            "icon_path": "icons/brown_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:red_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Stained Glass",
            "icon_path": "icons/red_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:orange_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Stained Glass",
            "icon_path": "icons/orange_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:yellow_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Stained Glass",
            "icon_path": "icons/yellow_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:lime_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Stained Glass",
            "icon_path": "icons/lime_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:green_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Stained Glass",
            "icon_path": "icons/green_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:cyan_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Stained Glass",
            "icon_path": "icons/cyan_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:light_blue_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Stained Glass",
            "icon_path": "icons/light_blue_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:blue_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Stained Glass",
            "icon_path": "icons/blue_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:purple_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Stained Glass",
            "icon_path": "icons/purple_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:magenta_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Stained Glass",
            "icon_path": "icons/magenta_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:pink_stained_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Stained Glass",
            "icon_path": "icons/pink_stained_glass.png",
            "identifier": "minecraft:stained_glass"
        },
        "minecraft:tinted_glass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tinted Glass",
            "icon_path": "icons/tinted_glass.png",
            "identifier": "minecraft:tinted_glass"
        },
        "minecraft:glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glass Pane",
            "icon_path": "icons/glass_pane.png",
            "identifier": "minecraft:glass_pane"
        },
        "minecraft:white_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Stained Glass Pane",
            "icon_path": "icons/white_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:gray_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Stained Glass Pane",
            "icon_path": "icons/gray_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:light_gray_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Stained Glass Pane",
            "icon_path": "icons/light_gray_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:black_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Stained Glass Pane",
            "icon_path": "icons/black_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:brown_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Stained Glass Pane",
            "icon_path": "icons/brown_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:red_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Stained Glass Pane",
            "icon_path": "icons/red_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:orange_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Stained Glass Pane",
            "icon_path": "icons/orange_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:yellow_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Stained Glass Pane",
            "icon_path": "icons/yellow_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:lime_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Stained Glass Pane",
            "icon_path": "icons/lime_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:green_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Stained Glass Pane",
            "icon_path": "icons/green_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:cyan_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Stained Glass Pane",
            "icon_path": "icons/cyan_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:light_blue_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Stained Glass Pane",
            "icon_path": "icons/light_blue_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:blue_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Stained Glass Pane",
            "icon_path": "icons/blue_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:purple_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Stained Glass Pane",
            "icon_path": "icons/purple_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:magenta_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Stained Glass Pane",
            "icon_path": "icons/magenta_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        "minecraft:pink_stained_glass_pane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Stained Glass Pane",
            "icon_path": "icons/pink_stained_glass_pane.png",
            "identifier": "minecraft:stained_glass_pane"
        },
        # Climbing
        "minecraft:ladder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ladder",
            "icon_path": "icons/ladder.png",
            "identifier": "minecraft:ladder"
        },
        "minecraft:scaffolding": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Scaffolding",
            "icon_path": "icons/scaffolding.png",
            "identifier": "minecraft:scaffolding"
        },
        # Slabs
        "minecraft:stone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Stone Slab",
            "icon_path": "icons/stone_slab.png",
            "identifier": "minecraft:stone_slab4"
        },
        "minecraft:smooth_stone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Smooth Stone Slab",
            "icon_path": "icons/smooth_stone_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:cobblestone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Cobblestone Slab",
            "icon_path": "icons/cobblestone_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:mossy_cobblestone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Mossy Cobblestone Slab",
            "icon_path": "icons/mossy_cobblestone_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:oak_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Wood Slab",
            "icon_path": "icons/oak_slab.png",
            "identifier": "minecraft:wooden_slab"
        },
        "minecraft:spruce_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Wood Slab",
            "icon_path": "icons/spruce_slab.png",
            "identifier": "minecraft:wooden_slab"
        },
        "minecraft:birch_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Wood Slab",
            "icon_path": "icons/birch_slab.png",
            "identifier": "minecraft:wooden_slab"
        },
        "minecraft:jungle_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Wood Slab",
            "icon_path": "icons/jungle_slab.png",
            "identifier": "minecraft:wooden_slab"
        },
        "minecraft:acacia_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Acacia Wood Slab",
            "icon_path": "icons/acacia_slab.png",
            "identifier": "minecraft:wooden_slab"
        },
        "minecraft:dark_oak_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Dark Oak Wood Slab",
            "icon_path": "icons/dark_oak_slab.png",
            "identifier": "minecraft:wooden_slab"
        },
        "minecraft:mangrove_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Mangrove Slab",
            "icon_path": "icons/mangrove_slab.png",
            "identifier": "minecraft:mangrove_slab"
        },
        "minecraft:stone_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Stone Brick Slab",
            "icon_path": "icons/stone_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:mossy_stone_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mossy Stone Brick Slab",
            "icon_path": "icons/mossy_stone_slab.png",
            "identifier": "minecraft:stone_slab4"
        },
        "minecraft:sandstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Sandstone Slab",
            "icon_path": "icons/sandstone_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:cut_sandstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Cut Sandstone Slab",
            "icon_path": "icons/cut_sandstone_slab.png",
            "identifier": "minecraft:stone_slab4"
        },
        "minecraft:smooth_sandstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Smooth Sandstone Slab",
            "icon_path": "icons/smooth_sandstone_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:red_sandstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Sandstone Slab",
            "icon_path": "icons/red_sandstone_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:cut_red_sandstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Cut Red Sandstone Slab",
            "icon_path": "icons/cut_red_sandstone_slab.png",
            "identifier": "minecraft:stone_slab4"
        },
        "minecraft:smooth_red_sandstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Smooth Red Sandstone Slab",
            "icon_path": "icons/smooth_red_sandstone_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:granite_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Granite Slab",
            "icon_path": "icons/granite_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:polished_granite_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Polished Granite Slab",
            "icon_path": "icons/polished_granite_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:diorite_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Diorite Slab",
            "icon_path": "icons/diorite_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:polished_diorite_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Polished Diorite Slab",
            "icon_path": "icons/polished_diorite_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:andesite_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Andesite Slab",
            "icon_path": "icons/andesite_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:polished_andesite_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Polished Andesite Slab",
            "icon_path": "icons/polished_andesite_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Brick Slab",
            "icon_path": "icons/brick_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:nether_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 7,
            "display_name": "Nether Brick Slab",
            "icon_path": "icons/nether_brick_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:red_nether_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 7,
            "display_name": "Red Nether Brick Slab",
            "icon_path": "icons/red_nether_brick_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:end_stone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Stone Brick Slab",
            "icon_path": "icons/end_stone_slab.png",
            "identifier": "minecraft:stone_slab3"
        },
        "minecraft:quartz_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 6,
            "display_name": "Quartz Slab",
            "icon_path": "icons/quartz_slab.png",
            "identifier": "minecraft:stone_slab"
        },
        "minecraft:smooth_quartz_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 1,
            "display_name": "Smooth Quartz Slab",
            "icon_path": "icons/smooth_quartz_slab.png",
            "identifier": "minecraft:stone_slab4"
        },
        "minecraft:purpur_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 1,
            "display_name": "Purpur Slab",
            "icon_path": "icons/purpur_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:prismarine_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Prismarine Slab",
            "icon_path": "icons/prismarine_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:dark_prismarine_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Dark Prismarine Slab",
            "icon_path": "icons/dark_prismarine_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:prismarine_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Prismarine Brick Slab",
            "icon_path": "icons/prismarine_brick_slab.png",
            "identifier": "minecraft:stone_slab2"
        },
        "minecraft:crimson_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Slab",
            "icon_path": "icons/crimson_slab.png",
            "identifier": "minecraft:crimson_slab"
        },
        "minecraft:warped_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Slab",
            "icon_path": "icons/warped_slab.png",
            "identifier": "minecraft:warped_slab"
        },
        "minecraft:blackstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Blackstone Slab",
            "icon_path": "icons/blackstone_slab.png",
            "identifier": "minecraft:blackstone_slab"
        },
        "minecraft:polished_blackstone_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Slab",
            "icon_path": "icons/polished_blackstone_slab.png",
            "identifier": "minecraft:polished_blackstone_slab"
        },
        "minecraft:polished_blackstone_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Brick Slab",
            "icon_path": "icons/polished_blackstone_brick_slab.png",
            "identifier": "minecraft:polished_blackstone_brick_slab"
        },
        "minecraft:cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cut Copper Slab",
            "icon_path": "icons/cut_copper_slab.png",
            "identifier": "minecraft:cut_copper_slab"
        },
        "minecraft:exposed_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Exposed Cut Copper Slab",
            "icon_path": "icons/exposed_cut_copper_slab.png",
            "identifier": "minecraft:exposed_cut_copper_slab"
        },
        "minecraft:weathered_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Weathered Cut Copper Slab",
            "icon_path": "icons/weathered_cut_copper_slab.png",
            "identifier": "minecraft:weathered_cut_copper_slab"
        },
        "minecraft:oxidized_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oxidized Cut Copper Slab",
            "icon_path": "icons/oxidized_cut_copper_slab.png",
            "identifier": "minecraft:oxidized_cut_copper_slab"
        },
        "minecraft:waxed_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Cut Copper Slab",
            "icon_path": "icons/waxed_cut_copper_slab.png",
            "identifier": "minecraft:waxed_cut_copper_slab"
        },
        "minecraft:waxed_exposed_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Exposed Cut Copper Slab",
            "icon_path": "icons/waxed_exposed_cut_copper_slab.png",
            "identifier": "minecraft:waxed_exposed_cut_copper_slab"
        },
        "minecraft:waxed_weathered_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Weathered Cut Copper Slab",
            "icon_path": "icons/waxed_weathered_cut_copper_slab.png",
            "identifier": "minecraft:waxed_weathered_cut_copper_slab"
        },
        "minecraft:waxed_oxidized_cut_copper_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Oxidized Cut Copper Slab",
            "icon_path": "icons/waxed_oxidized_cut_copper_slab.png",
            "identifier": "minecraft:waxed_oxidized_cut_copper_slab"
        },
        "minecraft:cobbled_deepslate_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobbled Deepslate Slab",
            "icon_path": "icons/cobbled_deepslate_slab.png",
            "identifier": "minecraft:cobbled_deepslate_slab"
        },
        "minecraft:polished_deepslate_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Deepslate Slab",
            "icon_path": "icons/polished_deepslate_slab.png",
            "identifier": "minecraft:polished_deepslate_slab"
        },
        "minecraft:deepslate_tile_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Tile Slab",
            "icon_path": "icons/deepslate_tile_slab.png",
            "identifier": "minecraft:deepslate_tile_slab"
        },
        "minecraft:deepslate_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Brick Slab",
            "icon_path": "icons/deepslate_brick_slab.png",
            "identifier": "minecraft:deepslate_brick_slab"
        },
        "minecraft:mud_brick_slab": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Mud Brick Slab",
            "icon_path": "icons/mud_brick_slab.png",
            "identifier": "minecraft:mud_brick_slab"
        },
        # Bricks
        "minecraft:bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bricks",
            "icon_path": "icons/bricks.png",
            "identifier": "minecraft:brick_block"
        },
        "minecraft:chiseled_nether_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Chiseled Nether Bricks",
            "icon_path": "icons/chiseled_nether_bricks.png",
            "identifier": "minecraft:chiseled_nether_bricks"
        },
        "minecraft:cracked_nether_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Cracked Nether Bricks",
            "icon_path": "icons/cracked_nether_bricks.png",
            "identifier": "minecraft:cracked_nether_bricks"
        },
        "minecraft:quartz_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Quartz Bricks",
            "icon_path": "icons/quartz_bricks.png",
            "identifier": "minecraft:quartz_bricks"
        },
        "minecraft:stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Bricks",
            "icon_path": "icons/stone_bricks.png",
            "identifier": "minecraft:stonebrick"
        },
        "minecraft:mossy_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Mossy Stone Bricks",
            "icon_path": "icons/mossy_stone_bricks.png",
            "identifier": "minecraft:stonebrick"
        },
        "minecraft:cracked_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Cracked Stone Bricks",
            "icon_path": "icons/cracked_stone_bricks.png",
            "identifier": "minecraft:stonebrick"
        },
        "minecraft:chiseled_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Chiseled Stone Bricks",
            "icon_path": "icons/chiseled_stone_bricks.png",
            "identifier": "minecraft:stonebrick"
        },
        "minecraft:end_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Stone Bricks",
            "icon_path": "icons/end_stone_bricks.png",
            "identifier": "minecraft:end_bricks"
        },
        "minecraft:prismarine_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Prismarine Bricks",
            "icon_path": "icons/prismarine_bricks.png",
            "identifier": "minecraft:prismarine"
        },
        "minecraft:polished_blackstone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Bricks",
            "icon_path": "icons/polished_blackstone_bricks.png",
            "identifier": "minecraft:polished_blackstone_bricks"
        },
        "minecraft:cracked_polished_blackstone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Cracked Polished Blackstone Bricks",
            "icon_path": "icons/cracked_polished_blackstone_bricks.png",
            "identifier": "minecraft:cracked_polished_blackstone_bricks"
        },
        "minecraft:gilded_blackstone": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Gilded Blackstone",
            "icon_path": "icons/gilded_blackstone.png",
            "identifier": "minecraft:gilded_blackstone"
        },
        "minecraft:chiseled_polished_blackstone": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Chiseled Polished Blackstone",
            "icon_path": "icons/chiseled_polished_blackstone.png",
            "identifier": "minecraft:chiseled_polished_blackstone"
        },
        "minecraft:deepslate_tiles": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Tiles",
            "icon_path": "icons/deepslate_tiles.png",
            "identifier": "minecraft:deepslate_tiles"
        },
        "minecraft:cracked_deepslate_tiles": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cracked Deepslate Tiles",
            "icon_path": "icons/cracked_deepslate_tiles.png",
            "identifier": "minecraft:cracked_deepslate_tiles"
        },
        "minecraft:deepslate_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Bricks",
            "icon_path": "icons/deepslate_bricks.png",
            "identifier": "minecraft:deepslate_bricks"
        },
        "minecraft:cracked_deepslate_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cracked Deepslate Bricks",
            "icon_path": "icons/cracked_deepslate_bricks.png",
            "identifier": "minecraft:cracked_deepslate_bricks"
        },
        "minecraft:chiseled_deepslate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chiseled Deepslate",
            "icon_path": "icons/chiseled_deepslate.png",
            "identifier": "minecraft:chiseled_deepslate"
        },
        # Cobblestone
        "minecraft:cobblestone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobblestone",
            "icon_path": "icons/cobblestone.png",
            "identifier": "minecraft:cobblestone"
        },
        "minecraft:mossy_cobblestone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Moss Stone",
            "icon_path": "icons/mossy_cobblestone.png",
            "identifier": "minecraft:mossy_cobblestone"
        },
        "minecraft:cobbled_deepslate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobbled Deepslate",
            "icon_path": "icons/cobbled_deepslate.png",
            "identifier": "minecraft:cobbled_deepslate"
        },
        # Stone
        "minecraft:smooth_stone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Smooth Stone",
            "icon_path": "icons/smooth_stone.png",
            "identifier": "minecraft:smooth_stone"
        },
        "minecraft:sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sandstone",
            "icon_path": "icons/sandstone.png",
            "identifier": "minecraft:sandstone"
        },
        "minecraft:chiseled_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Chiseled Sandstone",
            "icon_path": "icons/chiseled_sandstone.png",
            "identifier": "minecraft:sandstone"
        },
        "minecraft:cut_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Cut Sandstone",
            "icon_path": "icons/cut_sandstone.png",
            "identifier": "minecraft:sandstone"
        },
        "minecraft:smooth_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Smooth Sandstone",
            "icon_path": "icons/smooth_sandstone.png",
            "identifier": "minecraft:sandstone"
        },
        "minecraft:red_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Sandstone",
            "icon_path": "icons/red_sandstone.png",
            "identifier": "minecraft:red_sandstone"
        },
        "minecraft:chiseled_red_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Chiseled Red Sandstone",
            "icon_path": "icons/chiseled_red_sandstone.png",
            "identifier": "minecraft:red_sandstone"
        },
        "minecraft:cut_red_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Cut Red Sandstone",
            "icon_path": "icons/cut_red_sandstone.png",
            "identifier": "minecraft:red_sandstone"
        },
        "minecraft:smooth_red_sandstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Smooth Red Sandstone",
            "icon_path": "icons/smooth_red_sandstone.png",
            "identifier": "minecraft:red_sandstone"
        },
        "minecraft:coal_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Coal",
            "icon_path": "icons/coal_block.png",
            "identifier": "minecraft:coal_block"
        },
        "minecraft:dried_kelp_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dried Kelp Block",
            "icon_path": "icons/dried_kelp_block.png",
            "identifier": "minecraft:dried_kelp_block"
        },
        "minecraft:gold_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gold Block",
            "icon_path": "icons/gold_block.png",
            "identifier": "minecraft:gold_block"
        },
        "minecraft:iron_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Block",
            "icon_path": "icons/iron_block.png",
            "identifier": "minecraft:iron_block"
        },
        "minecraft:copper_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Copper",
            "icon_path": "icons/copper_block.png",
            "identifier": "minecraft:copper_block"
        },
        "minecraft:exposed_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Exposed Copper",
            "icon_path": "icons/exposed_copper.png",
            "identifier": "minecraft:exposed_copper"
        },
        "minecraft:weathered_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Weathered Copper",
            "icon_path": "icons/weathered_copper.png",
            "identifier": "minecraft:weathered_copper"
        },
        "minecraft:oxidized_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oxidized Copper",
            "icon_path": "icons/oxidized_copper.png",
            "identifier": "minecraft:oxidized_copper"
        },
        "minecraft:waxed_copper_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Block of Copper",
            "icon_path": "icons/waxed_copper_block.png",
            "identifier": "minecraft:waxed_copper"
        },
        "minecraft:waxed_exposed_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Exposed Copper",
            "icon_path": "icons/waxed_exposed_copper.png",
            "identifier": "minecraft:waxed_exposed_copper"
        },
        "minecraft:waxed_weathered_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Weathered Copper",
            "icon_path": "icons/waxed_weathered_copper.png",
            "identifier": "minecraft:waxed_weathered_copper"
        },
        "minecraft:waxed_oxidized_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Oxidized Copper",
            "icon_path": "icons/waxed_oxidized_copper.png",
            "identifier": "minecraft:waxed_oxidized_copper"
        },
        "minecraft:cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cut Copper",
            "icon_path": "icons/cut_copper.png",
            "identifier": "minecraft:cut_copper"
        },
        "minecraft:exposed_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Exposed Cut Copper",
            "icon_path": "icons/exposed_cut_copper.png",
            "identifier": "minecraft:exposed_cut_copper"
        },
        "minecraft:weathered_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Weathered Cut Copper",
            "icon_path": "icons/weathered_cut_copper.png",
            "identifier": "minecraft:weathered_cut_copper"
        },
        "minecraft:oxidized_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oxidized Cut Copper",
            "icon_path": "icons/oxidized_cut_copper.png",
            "identifier": "minecraft:oxidized_cut_copper"
        },
        "minecraft:waxed_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Cut Copper",
            "icon_path": "icons/waxed_cut_copper.png",
            "identifier": "minecraft:waxed_cut_copper"
        },
        "minecraft:waxed_exposed_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Exposed Cut Copper",
            "icon_path": "icons/waxed_exposed_cut_copper.png",
            "identifier": "minecraft:waxed_exposed_cut_copper"
        },
        "minecraft:waxed_weathered_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Weathered Cut Copper",
            "icon_path": "icons/waxed_weathered_cut_copper.png",
            "identifier": "minecraft:waxed_weathered_cut_copper"
        },
        "minecraft:waxed_oxidized_cut_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Waxed Oxidized Cut Copper",
            "icon_path": "icons/waxed_oxidized_cut_copper.png",
            "identifier": "minecraft:waxed_oxidized_cut_copper"
        },
        "minecraft:emerald_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Emerald Block",
            "icon_path": "icons/emerald_block.png",
            "identifier": "minecraft:emerald_block"
        },
        "minecraft:diamond_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Block",
            "icon_path": "icons/diamond_block.png",
            "identifier": "minecraft:diamond_block"
        },
        "minecraft:lapis_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Lapis Lazuli",
            "icon_path": "icons/lapis_block.png",
            "identifier": "minecraft:lapis_block"
        },
        "minecraft:raw_iron_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Raw Iron",
            "icon_path": "icons/raw_iron_block.png",
            "identifier": "minecraft:raw_iron_block"
        },
        "minecraft:raw_copper_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Raw Copper",
            "icon_path": "icons/raw_copper_block.png",
            "identifier": "minecraft:raw_copper_block"
        },
        "minecraft:raw_gold_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Raw Gold",
            "icon_path": "icons/raw_gold_block.png",
            "identifier": "minecraft:raw_gold_block"
        },
        "minecraft:quartz_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Quartz Block",
            "icon_path": "icons/quartz_block.png",
            "identifier": "minecraft:quartz_block"
        },
        "minecraft:quartz_pillar": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 2,
            "display_name": "Pillar Quartz Block",
            "icon_path": "icons/quartz_pillar.png",
            "identifier": "minecraft:quartz_block"
        },
        "minecraft:chiseled_quartz_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 1,
            "display_name": "Chiseled Quartz Block",
            "icon_path": "icons/chiseled_quartz_block.png",
            "identifier": "minecraft:quartz_block"
        },
        "minecraft:smooth_quartz": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 3,
            "display_name": "Smooth Quartz",
            "icon_path": "icons/smooth_quartz.png",
            "identifier": "minecraft:quartz_block"
        },
        "minecraft:prismarine": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Prismarine",
            "icon_path": "icons/prismarine.png",
            "identifier": "minecraft:prismarine"
        },
        "minecraft:dark_prismarine": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Dark Prismarine",
            "icon_path": "icons/dark_prismarine.png",
            "identifier": "minecraft:prismarine"
        },
        "minecraft:slime_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Slime Block",
            "icon_path": "icons/slime_block.png",
            "identifier": "minecraft:slime"
        },
        "minecraft:honey_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Honey Block",
            "icon_path": "icons/honey_block.png",
            "identifier": "minecraft:honey_block"
        },
        "minecraft:honeycomb_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Honeycomb Block",
            "icon_path": "icons/honeycomb_block.png",
            "identifier": "minecraft:honeycomb_block"
        },
        "minecraft:hay_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Hay Bale",
            "icon_path": "icons/hay_block.png",
            "identifier": "minecraft:hay_block"
        },
        "minecraft:bone_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bone Block",
            "icon_path": "icons/bone_block.png",
            "identifier": "minecraft:bone_block"
        },
        "minecraft:nether_brick_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Brick Block",
            "icon_path": "icons/nether_brick.png",
            "identifier": "minecraft:nether_brick"
        },
        "minecraft:red_nether_brick": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Red Nether Brick",
            "icon_path": "icons/red_nether_bricks.png",
            "identifier": "minecraft:red_nether_brick"
        },
        "minecraft:netherite_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Block",
            "icon_path": "icons/netherite_block.png",
            "identifier": "minecraft:netherite_block"
        },
        "minecraft:lodestone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lodestone",
            "icon_path": "icons/lodestone.png",
            "identifier": "minecraft:lodestone"
        },
        # Wool
        "minecraft:white_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Wool",
            "icon_path": "icons/white_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:light_gray_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Wool",
            "icon_path": "icons/light_gray_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:gray_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Wool",
            "icon_path": "icons/gray_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:black_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Wool",
            "icon_path": "icons/black_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:brown_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Wool",
            "icon_path": "icons/brown_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:red_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Wool",
            "icon_path": "icons/red_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:orange_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Wool",
            "icon_path": "icons/orange_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:yellow_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Wool",
            "icon_path": "icons/yellow_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:lime_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Wool",
            "icon_path": "icons/lime_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:green_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Wool",
            "icon_path": "icons/green_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:cyan_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Wool",
            "icon_path": "icons/cyan_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:light_blue_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Wool",
            "icon_path": "icons/light_blue_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:blue_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Wool",
            "icon_path": "icons/blue_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:purple_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Wool",
            "icon_path": "icons/purple_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:magenta_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Wool",
            "icon_path": "icons/magenta_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:pink_wool": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Wool",
            "icon_path": "icons/pink_wool.png",
            "identifier": "minecraft:wool"
        },
        "minecraft:white_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Carpet",
            "icon_path": "icons/white_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:light_gray_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Carpet",
            "icon_path": "icons/light_gray_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:gray_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Carpet",
            "icon_path": "icons/gray_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:black_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Carpet",
            "icon_path": "icons/black_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:brown_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Carpet",
            "icon_path": "icons/brown_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:red_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Carpet",
            "icon_path": "icons/red_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:orange_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Carpet",
            "icon_path": "icons/orange_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:yellow_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Carpet",
            "icon_path": "icons/yellow_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:lime_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Carpet",
            "icon_path": "icons/lime_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:green_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Carpet",
            "icon_path": "icons/green_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:cyan_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Carpet",
            "icon_path": "icons/cyan_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:light_blue_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Carpet",
            "icon_path": "icons/light_blue_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:blue_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Carpet",
            "icon_path": "icons/blue_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:purple_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Carpet",
            "icon_path": "icons/purple_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:magenta_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Carpet",
            "icon_path": "icons/magenta_carpet.png",
            "identifier": "minecraft:carpet"
        },
        "minecraft:pink_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Carpet",
            "icon_path": "icons/pink_carpet.png",
            "identifier": "minecraft:carpet"
        },
        # Concrete
        "minecraft:white_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Concrete Powder",
            "icon_path": "icons/white_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:light_gray_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Concrete Powder",
            "icon_path": "icons/light_gray_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:gray_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Concrete Powder",
            "icon_path": "icons/gray_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:black_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Concrete Powder",
            "icon_path": "icons/black_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:brown_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Concrete Powder",
            "icon_path": "icons/brown_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:red_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Concrete Powder",
            "icon_path": "icons/red_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:orange_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Concrete Powder",
            "icon_path": "icons/orange_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:yellow_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Concrete Powder",
            "icon_path": "icons/yellow_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:lime_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Concrete Powder",
            "icon_path": "icons/lime_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:green_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Concrete Powder",
            "icon_path": "icons/green_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:cyan_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Concrete Powder",
            "icon_path": "icons/cyan_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:light_blue_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Concrete Powder",
            "icon_path": "icons/light_blue_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:blue_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Concrete Powder",
            "icon_path": "icons/blue_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:purple_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Concrete Powder",
            "icon_path": "icons/purple_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:magenta_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Concrete Powder",
            "icon_path": "icons/magenta_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },
        "minecraft:pink_concrete_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Concrete Powder",
            "icon_path": "icons/pink_concrete_powder.png",
            "identifier": "minecraft:concrete_powder"
        },

        "minecraft:white_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Concrete",
            "icon_path": "icons/white_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:light_gray_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Concrete",
            "icon_path": "icons/light_gray_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:gray_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Concrete",
            "icon_path": "icons/gray_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:black_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Concrete",
            "icon_path": "icons/black_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:brown_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Concrete",
            "icon_path": "icons/brown_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:red_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Concrete",
            "icon_path": "icons/red_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:orange_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Concrete",
            "icon_path": "icons/orange_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:yellow_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Concrete",
            "icon_path": "icons/yellow_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:lime_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Concrete",
            "icon_path": "icons/lime_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:green_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Concrete",
            "icon_path": "icons/green_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:cyan_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Concrete",
            "icon_path": "icons/cyan_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:light_blue_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Concrete",
            "icon_path": "icons/light_blue_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:blue_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Concrete",
            "icon_path": "icons/blue_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:purple_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Concrete",
            "icon_path": "icons/purple_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:magenta_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Concrete",
            "icon_path": "icons/magenta_concrete.png",
            "identifier": "minecraft:concrete"
        },
        "minecraft:pink_concrete": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Concrete",
            "icon_path": "icons/pink_concrete.png",
            "identifier": "minecraft:concrete"
        },
        # Terracotta
        "minecraft:clay": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Clay",
            "icon_path": "icons/clay.png",
            "identifier": "minecraft:clay"
        },
        "minecraft:terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Terracotta",
            "icon_path": "icons/terracotta.png",
            "identifier": "minecraft:hardened_clay"
        },
        "minecraft:white_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Terracotta",
            "icon_path": "icons/white_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:light_gray_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Terracotta",
            "icon_path": "icons/light_gray_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:gray_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Terracotta",
            "icon_path": "icons/gray_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:black_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Terracotta",
            "icon_path": "icons/black_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:brown_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Terracotta",
            "icon_path": "icons/brown_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:red_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Terracotta",
            "icon_path": "icons/red_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:orange_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Terracotta",
            "icon_path": "icons/orange_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:yellow_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Terracotta",
            "icon_path": "icons/yellow_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:lime_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Terracotta",
            "icon_path": "icons/lime_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:green_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Terracotta",
            "icon_path": "icons/green_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:cyan_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Terracotta",
            "icon_path": "icons/cyan_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:light_blue_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Terracotta",
            "icon_path": "icons/light_blue_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:blue_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Terracotta",
            "icon_path": "icons/blue_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:purple_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Terracotta",
            "icon_path": "icons/purple_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:magenta_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Terracotta",
            "icon_path": "icons/magenta_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:pink_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Terracotta",
            "icon_path": "icons/pink_terracotta.png",
            "identifier": "minecraft:stained_hardened_clay"
        },
        "minecraft:white_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Glazed Terracotta",
            "icon_path": "icons/white_glazed_terracotta.png",
            "identifier": "minecraft:white_glazed_terracotta"
        },
        "minecraft:light_gray_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Gray Glazed Terracotta",
            "icon_path": "icons/light_gray_glazed_terracotta.png",
            "identifier": "minecraft:silver_glazed_terracotta"
        },
        "minecraft:gray_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gray Glazed Terracotta",
            "icon_path": "icons/gray_glazed_terracotta.png",
            "identifier": "minecraft:gray_glazed_terracotta"
        },
        "minecraft:black_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Black Glazed Terracotta",
            "icon_path": "icons/black_glazed_terracotta.png",
            "identifier": "minecraft:black_glazed_terracotta"
        },
        "minecraft:brown_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brown Glazed Terracotta",
            "icon_path": "icons/brown_glazed_terracotta.png",
            "identifier": "minecraft:brown_glazed_terracotta"
        },
        "minecraft:red_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Glazed Terracotta",
            "icon_path": "icons/red_glazed_terracotta.png",
            "identifier": "minecraft:red_glazed_terracotta"
        },
        "minecraft:orange_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Orange Glazed Terracotta",
            "icon_path": "icons/orange_glazed_terracotta.png",
            "identifier": "minecraft:orange_glazed_terracotta"
        },
        "minecraft:yellow_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Yellow Glazed Terracotta",
            "icon_path": "icons/yellow_glazed_terracotta.png",
            "identifier": "minecraft:yellow_glazed_terracotta"
        },
        "minecraft:lime_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lime Glazed Terracotta",
            "icon_path": "icons/lime_glazed_terracotta.png",
            "identifier": "minecraft:lime_glazed_terracotta"
        },
        "minecraft:green_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Green Glazed Terracotta",
            "icon_path": "icons/green_glazed_terracotta.png",
            "identifier": "minecraft:green_glazed_terracotta"
        },
        "minecraft:cyan_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cyan Glazed Terracotta",
            "icon_path": "icons/cyan_glazed_terracotta.png",
            "identifier": "minecraft:cyan_glazed_terracotta"
        },
        "minecraft:light_blue_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Blue Glazed Terracotta",
            "icon_path": "icons/light_blue_glazed_terracotta.png",
            "identifier": "minecraft:light_blue_glazed_terracotta"
        },
        "minecraft:blue_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blue Glazed Terracotta",
            "icon_path": "icons/blue_glazed_terracotta.png",
            "identifier": "minecraft:blue_glazed_terracotta"
        },
        "minecraft:purple_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Purple Glazed Terracotta",
            "icon_path": "icons/purple_glazed_terracotta.png",
            "identifier": "minecraft:purple_glazed_terracotta"
        },
        "minecraft:magenta_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Magenta Glazed Terracotta",
            "icon_path": "icons/magenta_glazed_terracotta.png",
            "identifier": "minecraft:magenta_glazed_terracotta"
        },
        "minecraft:pink_glazed_terracotta": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pink Glazed Terracotta",
            "icon_path": "icons/pink_glazed_terracotta.png",
            "identifier": "minecraft:pink_glazed_terracotta"
        },
        #
        "minecraft:purpur_block": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Purpur Block",
            "icon_path": "icons/purpur_block.png",
            "identifier": "minecraft:purpur_block"
        },
        "minecraft:purpur_pillar": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 2,
            "display_name": "Purpur Pillar",
            "icon_path": "icons/purpur_pillar.png",
            "identifier": "minecraft:purpur_block"
        },
        "minecraft:packed_mud": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Packed Mud",
            "icon_path": "icons/packed_mud.png",
            "identifier": "minecraft:packed_mud"
        },
        "minecraft:mud_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Mud Bricks",
            "icon_path": "icons/mud_bricks.png",
            "identifier": "minecraft:mud_bricks"
        },
        "minecraft:nether_wart_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Wart Block",
            "icon_path": "icons/nether_wart_block.png",
            "identifier": "minecraft:nether_wart_block"
        },
        "minecraft:warped_wart_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Wart Block",
            "icon_path": "icons/warped_wart_block.png",
            "identifier": "minecraft:warped_wart_block"
        },
        "minecraft:shroomlight": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Shroomlight",
            "icon_path": "icons/shroomlight.png",
            "identifier": "minecraft:shroomlight"
        },
        "minecraft:crimson_nylium": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Nylium",
            "icon_path": "icons/crimson_nylium.png",
            "identifier": "minecraft:crimson_nylium"
        },
        "minecraft:warped_nylium": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Nylium",
            "icon_path": "icons/warped_nylium.png",
            "identifier": "minecraft:warped_nylium"
        },
        "minecraft:basalt": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Basalt",
            "icon_path": "icons/basalt.png",
            "identifier": "minecraft:basalt"
        },
        "minecraft:polished_basalt": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Basalt",
            "icon_path": "icons/polished_basalt.png",
            "identifier": "minecraft:polished_basalt"
        },
        "minecraft:smooth_basalt": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Smooth Basalt",
            "icon_path": "icons/smooth_basalt.png",
            "identifier": "minecraft:smooth_basalt"
        },
        "minecraft:soul_soil": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Soul Soil",
            "icon_path": "icons/soul_soil.png",
            "identifier": "minecraft:soul_soil"
        },
        "minecraft:dirt": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dirt",
            "icon_path": "icons/dirt.png",
            "identifier": "minecraft:dirt"
        },
        "minecraft:coarse_dirt": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Coarse Dirt",
            "icon_path": "icons/coarse_dirt.png",
            "identifier": "minecraft:dirt"
        },
        "minecraft:farmland": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Farmland",
            "icon_path": "icons/farmland.png",
            "identifier": "minecraft:farmland"
        },
        "minecraft:grass_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Grass",
            "icon_path": "icons/grass.png",
            "identifier": "minecraft:grass"
        },
        "minecraft:grass_path": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dirt Path",
            "icon_path": "icons/grass_path.png",
            "identifier": "minecraft:grass_path"
        },
        "minecraft:podzol": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Podzol",
            "icon_path": "icons/podzol.png",
            "identifier": "minecraft:podzol"
        },
        "minecraft:mycelium": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mycelium",
            "icon_path": "icons/mycelium.png",
            "identifier": "minecraft:mycelium"
        },
        "minecraft:mud": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mud",
            "icon_path": "icons/mud.png",
            "identifier": "minecraft:mud"
        },
        "minecraft:stone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone",
            "icon_path": "icons/stone.png",
            "identifier": "minecraft:stone"
        },
        # Ores
        "minecraft:iron_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Ore",
            "icon_path": "icons/iron_ore.png",
            "identifier": "minecraft:iron_ore"
        },
        "minecraft:gold_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gold Ore",
            "icon_path": "icons/gold_ore.png",
            "identifier": "minecraft:gold_ore"
        },
        "minecraft:diamond_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Ore",
            "icon_path": "icons/diamond_ore.png",
            "identifier": "minecraft:diamond_ore"
        },
        "minecraft:lapis_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lapis Lazuli Ore",
            "icon_path": "icons/lapis_ore.png",
            "identifier": "minecraft:lapis_ore"
        },
        "minecraft:redstone_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Redstone Ore",
            "icon_path": "icons/redstone_ore.png",
            "identifier": "minecraft:redstone_ore"
        },
        "minecraft:coal_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Coal Ore",
            "icon_path": "icons/coal_ore.png",
            "identifier": "minecraft:coal_ore"
        },
        "minecraft:copper_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Copper Ore",
            "icon_path": "icons/copper_ore.png",
            "identifier": "minecraft:copper_ore"
        },
        "minecraft:emerald_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Emerald Ore",
            "icon_path": "icons/emerald_ore.png",
            "identifier": "minecraft:emerald_ore"
        },
        "minecraft:nether_quartz_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Quartz Ore",
            "icon_path": "icons/nether_quartz_ore.png",
            "identifier": "minecraft:quartz_ore"
        },
        "minecraft:nether_gold_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Gold Ore",
            "icon_path": "icons/nether_gold_ore.png",
            "identifier": "minecraft:nether_gold_ore"
        },
        "minecraft:ancient_debris": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Ancient Debris",
            "icon_path": "icons/ancient_debris.png",
            "identifier": "minecraft:ancient_debris"
        },
        "minecraft:deepslate_iron_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Iron Ore",
            "icon_path": "icons/deepslate_iron_ore.png",
            "identifier": "minecraft:deepslate_iron_ore"
        },
        "minecraft:deepslate_gold_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Gold Ore",
            "icon_path": "icons/deepslate_gold_ore.png",
            "identifier": "minecraft:deepslate_gold_ore"
        },
        "minecraft:deepslate_diamond_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Diamond Ore",
            "icon_path": "icons/deepslate_diamond_ore.png",
            "identifier": "minecraft:deepslate_diamond_ore"
        },
        "minecraft:deepslate_lapis_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Lapis Ore",
            "icon_path": "icons/deepslate_lapis_ore.png",
            "identifier": "minecraft:deepslate_lapis_ore"
        },
        "minecraft:deepslate_redstone_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Redstone Ore",
            "icon_path": "icons/deepslate_redstone_ore.png",
            "identifier": "minecraft:deepslate_redstone_ore"
        },
        "minecraft:deepslate_emerald_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Emerald Ore",
            "icon_path": "icons/deepslate_emerald_ore.png",
            "identifier": "minecraft:deepslate_emerald_ore"
        },
        "minecraft:deepslate_coal_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Coal Ore",
            "icon_path": "icons/deepslate_coal_ore.png",
            "identifier": "minecraft:deepslate_coal_ore"
        },
        "minecraft:deepslate_copper_ore": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate Copper Ore",
            "icon_path": "icons/deepslate_copper_ore.png",
            "identifier": "minecraft:deepslate_copper_ore"
        },
        # Stone
        "minecraft:gravel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gravel",
            "icon_path": "icons/gravel.png",
            "identifier": "minecraft:gravel"
        },
        "minecraft:granite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Granite",
            "icon_path": "icons/granite.png",
            "identifier": "minecraft:stone"
        },
        "minecraft:diorite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Diorite",
            "icon_path": "icons/diorite.png",
            "identifier": "minecraft:stone"
        },
        "minecraft:andesite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Andesite",
            "icon_path": "icons/andesite.png",
            "identifier": "minecraft:stone"
        },
        "minecraft:blackstone": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Blackstone",
            "icon_path": "icons/blackstone.png",
            "identifier": "minecraft:blackstone"
        },
        "minecraft:deepslate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Deepslate",
            "icon_path": "icons/deepslate.png",
            "identifier": "minecraft:deepslate"
        },
        "minecraft:polished_granite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Polished Granite",
            "icon_path": "icons/polished_granite.png",
            "identifier": "minecraft:stone"
        },
        "minecraft:polished_diorite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Polished Diorite",
            "icon_path": "icons/polished_diorite.png",
            "identifier": "minecraft:stone"
        },
        "minecraft:polished_andesite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Polished Andesite",
            "icon_path": "icons/polished_andesite.png",
            "identifier": "minecraft:stone"
        },
        "minecraft:polished_blackstone": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone",
            "icon_path": "icons/polished_blackstone.png",
            "identifier": "minecraft:polished_blackstone"
        },
        "minecraft:polished_deepslate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polished Deepslate",
            "icon_path": "icons/polished_deepslate.png",
            "identifier": "minecraft:polished_deepslate"
        },
        "minecraft:sand": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sand",
            "icon_path": "icons/sand.png",
            "identifier": "minecraft:sand"
        },
        "minecraft:red_sand": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Red Sand",
            "icon_path": "icons/red_sand.png",
            "identifier": "minecraft:sand"
        },
        "minecraft:cactus": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cactus",
            "icon_path": "icons/cactus.png",
            "identifier": "minecraft:cactus"
        },
        # Log
        "minecraft:oak_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Log",
            "icon_path": "icons/oak_log.png",
            "identifier": "minecraft:log"
        },
        "minecraft:stripped_oak_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Oak Log",
            "icon_path": "icons/stripped_oak_log.png",
            "identifier": "minecraft:stripped_oak_log"
        },
        "minecraft:spruce_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Log",
            "icon_path": "icons/spruce_log.png",
            "identifier": "minecraft:log"
        },
        "minecraft:stripped_spruce_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Spruce Log",
            "icon_path": "icons/stripped_spruce_log.png",
            "identifier": "minecraft:stripped_spruce_log"
        },
        "minecraft:birch_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Log",
            "icon_path": "icons/birch_log.png",
            "identifier": "minecraft:log"
        },
        "minecraft:stripped_birch_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Birch Log",
            "icon_path": "icons/stripped_birch_log.png",
            "identifier": "minecraft:stripped_birch_log"
        },
        "minecraft:jungle_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Log",
            "icon_path": "icons/jungle_log.png",
            "identifier": "minecraft:log"
        },
        "minecraft:stripped_jungle_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Jungle Log",
            "icon_path": "icons/stripped_jungle_log.png",
            "identifier": "minecraft:stripped_jungle_log"
        },
        "minecraft:acacia_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Log",
            "icon_path": "icons/acacia_log.png",
            "identifier": "minecraft:log2"
        },
        "minecraft:stripped_acacia_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Acacia Log",
            "icon_path": "icons/stripped_acacia_log.png",
            "identifier": "minecraft:stripped_acacia_log"
        },
        "minecraft:dark_oak_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Dark Oak Log",
            "icon_path": "icons/dark_oak_log.png",
            "identifier": "minecraft:log2"
        },
        "minecraft:stripped_dark_oak_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Dark Oak Log",
            "icon_path": "icons/stripped_dark_oak_log.png",
            "identifier": "minecraft:stripped_dark_oak_log"
        },
        "minecraft:mangrove_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Log",
            "icon_path": "icons/mangrove_log.png",
            "identifier": "minecraft:mangrove_log"
        },
        "minecraft:stripped_mangrove_log": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Mangrove Log",
            "icon_path": "icons/stripped_mangrove_log.png",
            "identifier": "minecraft:stripped_mangrove_log"
        },
        "minecraft:crimson_stem": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Stem",
            "icon_path": "icons/crimson_stem.png",
            "identifier": "minecraft:crimson_stem"
        },
        "minecraft:stripped_crimson_stem": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Stripped Crimson Stem",
            "icon_path": "icons/stripped_crimson_stem.png",
            "identifier": "minecraft:stripped_crimson_stem"
        },
        "minecraft:warped_stem": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Stem",
            "icon_path": "icons/warped_stem.png",
            "identifier": "minecraft:warped_stem"
        },
        "minecraft:stripped_warped_stem": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Stripped Warped Stem",
            "icon_path": "icons/stripped_warped_stem.png",
            "identifier": "minecraft:stripped_warped_stem"
        },
        "minecraft:oak_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Wood",
            "icon_path": "icons/oak_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:stripped_oak_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Stripped Oak Wood",
            "icon_path": "icons/stripped_oak_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:spruce_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Wood",
            "icon_path": "icons/spruce_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:stripped_spruce_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Stripped Spruce Wood",
            "icon_path": "icons/stripped_spruce_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:birch_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Wood",
            "icon_path": "icons/birch_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:stripped_birch_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Stripped Birch Wood",
            "icon_path": "icons/stripped_birch_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:jungle_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Wood",
            "icon_path": "icons/jungle_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:stripped_jungle_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Stripped Jungle Wood",
            "icon_path": "icons/stripped_jungle_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:acacia_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Acacia Wood",
            "icon_path": "icons/acacia_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:stripped_acacia_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Stripped Acacia Wood",
            "icon_path": "icons/stripped_acacia_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:dark_oak_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Dark Oak Wood",
            "icon_path": "icons/dark_oak_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:mangrove_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Wood",
            "icon_path": "icons/mangrove_wood.png",
            "identifier": "minecraft:mangrove_wood"
        },
        "minecraft:stripped_mangrove_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stripped Mangrove",
            "icon_path": "icons/stripped_mangrove_wood.png",
            "identifier": "minecraft:stripped_mangrove_wood"
        },
        "minecraft:stripped_dark_oak_wood": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Stripped Dark Oak Wood",
            "icon_path": "icons/stripped_dark_oak_wood.png",
            "identifier": "minecraft:wood"
        },
        "minecraft:crimson_hyphae": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Hyphae",
            "icon_path": "icons/crimson_hyphae.png",
            "identifier": "minecraft:crimson_hyphae"
        },
        "minecraft:stripped_crimson_hyphae": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Stripped Crimson Hyphae",
            "icon_path": "icons/stripped_crimson_hyphae.png",
            "identifier": "minecraft:stripped_crimson_hyphae"
        },
        "minecraft:warped_hyphae": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Hyphae",
            "icon_path": "icons/warped_hyphae.png",
            "identifier": "minecraft:warped_hyphae"
        },
        "minecraft:stripped_warped_hyphae": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Stripped Warped Hyphae",
            "icon_path": "icons/stripped_warped_hyphae.png",
            "identifier": "minecraft:stripped_warped_hyphae"
        },
        # leaves
        "minecraft:oak_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Leaves",
            "icon_path": "icons/oak_leaves.png",
            "identifier": "minecraft:leaves"
        },
        "minecraft:spruce_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Leaves",
            "icon_path": "icons/spruce_leaves.png",
            "identifier": "minecraft:leaves"
        },
        "minecraft:birch_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Leaves",
            "icon_path": "icons/birch_leaves.png",
            "identifier": "minecraft:leaves"
        },
        "minecraft:jungle_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Leaves",
            "icon_path": "icons/jungle_leaves.png",
            "identifier": "minecraft:leaves"
        },
        "minecraft:acacia_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Leaves",
            "icon_path": "icons/acacia_leaves.png",
            "identifier": "minecraft:leaves2"
        },
        "minecraft:dark_oak_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Dark Oak Leaves",
            "icon_path": "icons/dark_oak_leaves.png",
            "identifier": "minecraft:leaves2"
        },
        "minecraft:mangrove_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Leaves",
            "icon_path": "icons/mangrove_leaves.png",
            "identifier": "minecraft:mangrove_leaves"
        },
        "minecraft:azalea_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Azalea Leaves",
            "icon_path": "icons/azalea_leaves.png",
            "identifier": "minecraft:azalea_leaves"
        },
        "minecraft:flowering_azalea_leaves": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Flowering Azalea Leaves",
            "icon_path": "icons/azalea_leaves_flowered.png",
            "identifier": "minecraft:azalea_leaves_flowered"
        },
        # Saplings
        "minecraft:oak_sapling": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Sapling",
            "icon_path": "icons/oak_sapling.png",
            "identifier": "minecraft:sapling"
        },
        "minecraft:spruce_sapling": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Spruce Sapling",
            "icon_path": "icons/spruce_sapling.png",
            "identifier": "minecraft:sapling"
        },
        "minecraft:birch_sapling": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Birch Sapling",
            "icon_path": "icons/birch_sapling.png",
            "identifier": "minecraft:sapling"
        },
        "minecraft:jungle_sapling": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Jungle Sapling",
            "icon_path": "icons/jungle_sapling.png",
            "identifier": "minecraft:sapling"
        },
        "minecraft:acacia_sapling": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Acacia Sapling",
            "icon_path": "icons/acacia_sapling.png",
            "identifier": "minecraft:sapling"
        },
        "minecraft:dark_oak_sapling": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Dark Oak Sapling",
            "icon_path": "icons/dark_oak_sapling.png",
            "identifier": "minecraft:sapling"
        },
        "minecraft:mangrove_propagule": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Mangrove Propagule",
            "icon_path": "icons/mangrove_propagule.png",
            "identifier": "minecraft:mangrove_propagule"
        },
        #
        "minecraft:bee_nest": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bee Nest",
            "icon_path": "icons/bee_nest.png",
            "identifier": "minecraft:bee_nest"
        },
        # Plants
        "minecraft:wheat_seeds": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wheat Seeds",
            "icon_path": "icons/wheat_seeds.png",
            "identifier": "minecraft:wheat_seeds"
        },
        "minecraft:pumpkin_seeds": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pumpkin Seeds",
            "icon_path": "icons/pumpkin_seeds.png",
            "identifier": "minecraft:pumpkin_seeds"
        },
        "minecraft:melon_seeds": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Melon Seeds",
            "icon_path": "icons/melon_seeds.png",
            "identifier": "minecraft:melon_seeds"
        },
        "minecraft:beetroot_seeds": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Beetroot Seeds",
            "icon_path": "icons/beetroot_seeds.png",
            "identifier": "minecraft:beetroot_seeds"
        },
        "minecraft:wheat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wheat",
            "icon_path": "icons/wheat.png",
            "identifier": "minecraft:wheat"
        },
        "minecraft:beetroot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Beetroot",
            "icon_path": "icons/beetroot.png",
            "identifier": "minecraft:beetroot"
        },
        "minecraft:potato": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Potato",
            "icon_path": "icons/potato.png",
            "identifier": "minecraft:potato"
        },
        "minecraft:poisonous_potato": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Poisonous Potato",
            "icon_path": "icons/poisonous_potato.png",
            "identifier": "minecraft:poisonous_potato"
        },
        "minecraft:carrot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Carrot",
            "icon_path": "icons/carrot.png",
            "identifier": "minecraft:carrot"
        },
        "minecraft:golden_carrot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Carrot",
            "icon_path": "icons/golden_carrot.png",
            "identifier": "minecraft:golden_carrot"
        },
        "minecraft:apple": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Apple",
            "icon_path": "icons/apple.png",
            "identifier": "minecraft:apple"
        },
        "minecraft:golden_apple": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Apple",
            "icon_path": "icons/golden_apple.png",
            "identifier": "minecraft:golden_apple"
        },
        "minecraft:enchanted_golden_apple": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Enchanted Golden Apple",
            "icon_path": "icons/enchanted_golden_apple.png",
            "identifier": "minecraft:enchanted_golden_apple"
        },
        "minecraft:melon": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Melon",
            "icon_path": "icons/melon.png",
            "identifier": "minecraft:melon_block"
        },
        "minecraft:melon_slice": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Melon",
            "icon_path": "icons/melon_slice.png",
            "identifier": "minecraft:melon_slice"
        },
        "minecraft:glistering_melon_slice": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glistering Melon Slice",
            "icon_path": "icons/glistering_melon_slice.png",
            "identifier": "minecraft:glistering_melon_slice"
        },
        "minecraft:sweet_berries": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sweet Berries",
            "icon_path": "icons/sweet_berries.png",
            "identifier": "minecraft:sweet_berries"
        },
        "minecraft:glow_berries": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glow Berries",
            "icon_path": "icons/glow_berries.png",
            "identifier": "minecraft:glow_berries"
        },
        "minecraft:pumpkin": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pumpkin",
            "icon_path": "icons/pumpkin.png",
            "identifier": "minecraft:pumpkin"
        },
        "minecraft:carved_pumpkin": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Carved Pumpkin",
            "icon_path": "icons/carved_pumpkin.png",
            "identifier": "minecraft:carved_pumpkin"
        },
        "minecraft:jack_o_lantern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jack o'Lantern",
            "icon_path": "icons/jack_o_lantern.png",
            "identifier": "minecraft:lit_pumpkin"
        },
        "minecraft:honeycomb": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Honeycomb",
            "icon_path": "icons/honeycomb.png",
            "identifier": "minecraft:honeycomb"
        },
        "minecraft:fern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Fern",
            "icon_path": "icons/fern.png",
            "identifier": "minecraft:tallgrass"
        },
        "minecraft:large_fern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Large Fern",
            "icon_path": "icons/large_fern.png",
            "identifier": "minecraft:double_plant"
        },
        "minecraft:grass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Grass",
            "icon_path": "icons/grass.png",
            "identifier": "minecraft:tallgrass"
        },
        "minecraft:tall_grass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Double Tallgrass",
            "icon_path": "icons/tall_grass.png",
            "identifier": "minecraft:double_plant"
        },
        "minecraft:nether_sprouts": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Sprouts",
            "icon_path": "icons/nether_sprouts.png",
            "identifier": "minecraft:nether_sprouts"
        },
        "minecraft:fire_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Fire Coral",
            "icon_path": "icons/fire_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:brain_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Brain Coral",
            "icon_path": "icons/brain_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:bubble_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Bubble Coral",
            "icon_path": "icons/bubble_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:tube_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tube Coral",
            "icon_path": "icons/tube_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:horn_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Horn Coral",
            "icon_path": "icons/horn_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:dead_fire_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Dead Fire Coral",
            "icon_path": "icons/dead_fire_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:dead_brain_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Dead Brain Coral",
            "icon_path": "icons/dead_brain_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:dead_bubble_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Dead Bubble Coral",
            "icon_path": "icons/dead_bubble_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:dead_tube_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Dead Tube Coral",
            "icon_path": "icons/dead_tube_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:dead_horn_coral": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Dead Horn Coral",
            "icon_path": "icons/dead_horn_coral.png",
            "identifier": "minecraft:coral"
        },
        "minecraft:fire_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Fire Coral Fan",
            "icon_path": "icons/fire_coral_fan.png",
            "identifier": "minecraft:coral_fan"
        },
        "minecraft:brain_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Brain Coral Fan",
            "icon_path": "icons/brain_coral_fan.png",
            "identifier": "minecraft:coral_fan"
        },
        "minecraft:bubble_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Bubble Coral Fan",
            "icon_path": "icons/bubble_coral_fan.png",
            "identifier": "minecraft:coral_fan"
        },
        "minecraft:tube_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tube Coral Fan",
            "icon_path": "icons/tube_coral_fan.png",
            "identifier": "minecraft:coral_fan"
        },
        "minecraft:horn_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Horn Coral Fan",
            "icon_path": "icons/horn_coral_fan.png",
            "identifier": "minecraft:coral_fan"
        },
        "minecraft:dead_fire_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Dead Fire Coral Fan",
            "icon_path": "icons/dead_fire_coral_fan.png",
            "identifier": "minecraft:coral_fan_dead"
        },
        "minecraft:dead_brain_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Dead Brain Coral Fan",
            "icon_path": "icons/dead_brain_coral_fan.png",
            "identifier": "minecraft:coral_fan_dead"
        },
        "minecraft:dead_bubble_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Dead Bubble Coral Fan",
            "icon_path": "icons/dead_bubble_coral_fan.png",
            "identifier": "minecraft:coral_fan_dead"
        },
        "minecraft:dead_tube_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dead Tube Coral Fan",
            "icon_path": "icons/dead_tube_coral_fan.png",
            "identifier": "minecraft:coral_fan_dead"
        },
        "minecraft:dead_horn_coral_fan": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Dead Horn Coral Fan",
            "icon_path": "icons/dead_horn_coral_fan.png",
            "identifier": "minecraft:coral_fan_dead"
        },
        "minecraft:kelp": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Kelp",
            "icon_path": "icons/kelp.png",
            "identifier": "minecraft:kelp"
        },
        "minecraft:seagrass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sea Grass",
            "icon_path": "icons/seagrass.png",
            "identifier": "minecraft:seagrass"
        },
        "minecraft:crimson_roots": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Roots",
            "icon_path": "icons/crimson_roots.png",
            "identifier": "minecraft:crimson_roots"
        },
        "minecraft:warped_roots": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Roots",
            "icon_path": "icons/warped_roots.png",
            "identifier": "minecraft:warped_roots"
        },
        "minecraft:dandelion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dandelion",
            "icon_path": "icons/dandelion.png",
            "identifier": "minecraft:yellow_flower"
        },
        "minecraft:poppy": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Poppy",
            "icon_path": "icons/poppy.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:blue_orchid": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Blue Orchid",
            "icon_path": "icons/blue_orchid.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:allium": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Allium",
            "icon_path": "icons/allium.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:azure_bluet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Azure Bluet",
            "icon_path": "icons/azure_bluet.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:red_tulip": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Red Tulip",
            "icon_path": "icons/red_tulip.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:orange_tulip": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Orange Tulip",
            "icon_path": "icons/orange_tulip.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:white_tulip": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "White Tulip",
            "icon_path": "icons/white_tulip.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:pink_tulip": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Pink Tulip",
            "icon_path": "icons/pink_tulip.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:oxeye_daisy": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Oxeye Daisy",
            "icon_path": "icons/oxeye_daisy.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:cornflower": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cornflower",
            "icon_path": "icons/cornflower.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:lily_of_the_valley": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Lily of the Valley",
            "icon_path": "icons/lily_of_the_valley.png",
            "identifier": "minecraft:red_flower"
        },
        "minecraft:sunflower": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sunflower",
            "icon_path": "icons/sunflower.png",
            "identifier": "minecraft:double_plant"
        },
        "minecraft:lilac": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Lilac",
            "icon_path": "icons/lilac.png",
            "identifier": "minecraft:double_plant"
        },
        "minecraft:rose_bush": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Rose Bush",
            "icon_path": "icons/rose_bush.png",
            "identifier": "minecraft:double_plant"
        },
        "minecraft:peony": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Peony",
            "icon_path": "icons/peony.png",
            "identifier": "minecraft:double_plant"
        },
        "minecraft:wither_rose": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wither Rose",
            "icon_path": "icons/wither_rose.png",
            "identifier": "minecraft:wither_rose"
        },
        # Dyes
        "minecraft:white_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Dye",
            "icon_path": "icons/white_dye.png",
            "identifier": "minecraft:white_dye"
        },
        "minecraft:light_gray_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Gray Dye",
            "icon_path": "icons/light_gray_dye.png",
            "identifier": "minecraft:light_gray_dye"
        },
        "minecraft:gray_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gray Dye",
            "icon_path": "icons/gray_dye.png",
            "identifier": "minecraft:gray_dye"
        },
        "minecraft:brown_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brown Dye",
            "icon_path": "icons/brown_dye.png",
            "identifier": "minecraft:brown_dye"
        },
        "minecraft:black_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Black Dye",
            "icon_path": "icons/black_dye.png",
            "identifier": "minecraft:black_dye"
        },
        "minecraft:red_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Dye",
            "icon_path": "icons/red_dye.png",
            "identifier": "minecraft:red_dye"
        },
        "minecraft:orange_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Orange Dye",
            "icon_path": "icons/orange_dye.png",
            "identifier": "minecraft:orange_dye"
        },
        "minecraft:yellow_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Yellow Dye",
            "icon_path": "icons/yellow_dye.png",
            "identifier": "minecraft:yellow_dye"
        },
        "minecraft:lime_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lime Dye",
            "icon_path": "icons/lime_dye.png",
            "identifier": "minecraft:lime_dye"
        },
        "minecraft:green_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Green Dye",
            "icon_path": "icons/green_dye.png",
            "identifier": "minecraft:green_dye"
        },
        "minecraft:cyan_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cyan Dye",
            "icon_path": "icons/cyan_dye.png",
            "identifier": "minecraft:cyan_dye"
        },
        "minecraft:light_blue_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Blue Dye",
            "icon_path": "icons/light_blue_dye.png",
            "identifier": "minecraft:light_blue_dye"
        },
        "minecraft:blue_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blue Dye",
            "icon_path": "icons/blue_dye.png",
            "identifier": "minecraft:blue_dye"
        },
        "minecraft:purple_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Purple Dye",
            "icon_path": "icons/purple_dye.png",
            "identifier": "minecraft:purple_dye"
        },
        "minecraft:magenta_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Magenta Dye",
            "icon_path": "icons/magenta_dye.png",
            "identifier": "minecraft:magenta_dye"
        },
        "minecraft:pink_dye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pink Dye",
            "icon_path": "icons/pink_dye.png",
            "identifier": "minecraft:pink_dye"
        },
        "minecraft:ink_sac": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ink Sack",
            "icon_path": "icons/ink_sac.png",
            "identifier": "minecraft:ink_sac"
        },
        "minecraft:glow_ink_sac": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glow Ink Sac",
            "icon_path": "icons/glow_ink_sac.png",
            "identifier": "minecraft:glow_ink_sac"
        },
        "minecraft:cocoa_beans": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cocoa Beans",
            "icon_path": "icons/cocoa_beans.png",
            "identifier": "minecraft:cocoa_beans"
        },
        "minecraft:lapis_lazuli": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lapis Lazuli",
            "icon_path": "icons/lapis_lazuli.png",
            "identifier": "minecraft:lapis_lazuli"
        },
        "minecraft:bone_meal": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bone Meal",
            "icon_path": "icons/bone_meal.png",
            "identifier": "minecraft:bone_meal"
        },
        #
        "minecraft:vine": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Vines",
            "icon_path": "icons/vine.png",
            "identifier": "minecraft:vine"
        },
        "minecraft:weeping_vines": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Weeping Vines",
            "icon_path": "icons/weeping_vines.png",
            "identifier": "minecraft:weeping_vines"
        },
        "minecraft:twisting_vines": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Twisting Vines",
            "icon_path": "icons/twisting_vines.png",
            "identifier": "minecraft:twisting_vines"
        },
        "minecraft:lily_pad": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lily Pad",
            "icon_path": "icons/lily_pad.png",
            "identifier": "minecraft:waterlily"
        },
        "minecraft:dead_bush": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dead Bush",
            "icon_path": "icons/dead_bush.png",
            "identifier": "minecraft:deadbush"
        },
        "minecraft:bamboo": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bamboo",
            "icon_path": "icons/bamboo.png",
            "identifier": "minecraft:bamboo"
        },
        #
        "minecraft:snow_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Snow Block",
            "icon_path": "icons/snow_block.png",
            "identifier": "minecraft:snow"
        },
        "minecraft:ice": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ice",
            "icon_path": "icons/ice.png",
            "identifier": "minecraft:ice"
        },
        "minecraft:packed_ice": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Packed Ice",
            "icon_path": "icons/packed_ice.png",
            "identifier": "minecraft:packed_ice"
        },
        "minecraft:blue_ice": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blue Ice",
            "icon_path": "icons/blue_ice.png",
            "identifier": "minecraft:blue_ice"
        },
        "minecraft:snow_layer": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Top Snow",
            "icon_path": "icons/snow.png",
            "identifier": "minecraft:snow_layer"
        },
        "minecraft:pointed_dripstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pointed Dripstone",
            "icon_path": "icons/pointed_dripstone.png",
            "identifier": "minecraft:pointed_dripstone"
        },
        "minecraft:dripstone_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dripstone Block",
            "icon_path": "icons/dripstone_block.png",
            "identifier": "minecraft:dripstone_block"
        },
        "minecraft:moss_carpet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Moss Carpet",
            "icon_path": "icons/moss_carpet.png",
            "identifier": "minecraft:moss_carpet"
        },
        "minecraft:moss_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Moss Block",
            "icon_path": "icons/moss_block.png",
            "identifier": "minecraft:moss_block"
        },
        "minecraft:rooted_dirt": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rooted Dirt",
            "icon_path": "icons/rooted_dirt.png",
            "identifier": "minecraft:dirt_with_roots"
        },
        "minecraft:hanging_roots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Hanging Roots",
            "icon_path": "icons/hanging_roots.png",
            "identifier": "minecraft:hanging_roots"
        },
        "minecraft:mangrove_roots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Roots",
            "icon_path": "icons/mangrove_roots.png",
            "identifier": "minecraft:mangrove_roots"
        },
        "minecraft:muddy_mangrove_roots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Muddy Mangrove Roots",
            "icon_path": "icons/muddy_mangrove_roots.png",
            "identifier": "minecraft:muddy_mangrove_roots"
        },
        "minecraft:big_dripleaf": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Big Dripleaf",
            "icon_path": "icons/big_dripleaf.png",
            "identifier": "minecraft:big_dripleaf"
        },
        "minecraft:small_dripleaf": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Small Dripleaf",
            "icon_path": "icons/small_dripleaf.png",
            "identifier": "minecraft:small_dripleaf_block"
        },
        "minecraft:spore_blossom": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spore Blossom",
            "icon_path": "icons/spore_blossom.png",
            "identifier": "minecraft:spore_blossom"
        },
        "minecraft:azalea": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Azalea",
            "icon_path": "icons/azalea.png",
            "identifier": "minecraft:azalea"
        },
        "minecraft:flowering_azalea": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Flowering Azalea",
            "icon_path": "icons/flowering_azalea.png",
            "identifier": "minecraft:flowering_azalea"
        },
        "minecraft:glow_lichen": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glow Lichen",
            "icon_path": "icons/glow_lichen.png",
            "identifier": "minecraft:glow_lichen"
        },
        "minecraft:amethyst_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Block of Amethyst",
            "icon_path": "icons/amethyst_block.png",
            "identifier": "minecraft:amethyst_block"
        },
        "minecraft:budding_amethyst": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Budding Amethyst",
            "icon_path": "icons/budding_amethyst.png",
            "identifier": "minecraft:budding_amethyst"
        },
        "minecraft:amethyst_cluster": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Amethyst Cluster",
            "icon_path": "icons/amethyst_cluster.png",
            "identifier": "minecraft:amethyst_cluster"
        },
        "minecraft:large_amethyst_bud": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Large Amethyst Bud",
            "icon_path": "icons/large_amethyst_bud.png",
            "identifier": "minecraft:large_amethyst_bud"
        },
        "minecraft:medium_amethyst_bud": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Medium Amethyst Bud",
            "icon_path": "icons/medium_amethyst_bud.png",
            "identifier": "minecraft:medium_amethyst_bud"
        },
        "minecraft:small_amethyst_bud": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Small Amethyst Bud",
            "icon_path": "icons/small_amethyst_bud.png",
            "identifier": "minecraft:small_amethyst_bud"
        },
        "minecraft:tuff": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tuff",
            "icon_path": "icons/tuff.png",
            "identifier": "minecraft:tuff"
        },
        "minecraft:calcite": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Calcite",
            "icon_path": "icons/calcite.png",
            "identifier": "minecraft:calcite"
        },
        # Food
        "minecraft:chicken": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Chicken",
            "icon_path": "icons/chicken.png",
            "identifier": "minecraft:chicken"
        },
        "minecraft:porkchop": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Porkchop",
            "icon_path": "icons/porkchop.png",
            "identifier": "minecraft:porkchop"
        },
        "minecraft:beef": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Beef",
            "icon_path": "icons/beef.png",
            "identifier": "minecraft:beef"
        },
        "minecraft:mutton": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Mutton",
            "icon_path": "icons/mutton.png",
            "identifier": "minecraft:mutton"
        },
        "minecraft:rabbit": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Rabbit",
            "icon_path": "icons/rabbit.png",
            "identifier": "minecraft:rabbit"
        },
        "minecraft:cod": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cod",
            "icon_path": "icons/cod.png",
            "identifier": "minecraft:cod"
        },
        "minecraft:salmon": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Salmon",
            "icon_path": "icons/salmon.png",
            "identifier": "minecraft:salmon"
        },
        "minecraft:tropical_fish": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tropical Fish",
            "icon_path": "icons/tropical_fish.png",
            "identifier": "minecraft:tropical_fish"
        },
        "minecraft:pufferfish": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pufferfish",
            "icon_path": "icons/pufferfish.png",
            "identifier": "minecraft:pufferfish"
        },
        "minecraft:brown_mushroom": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brown Mushroom",
            "icon_path": "icons/brown_mushroom.png",
            "identifier": "minecraft:brown_mushroom"
        },
        "minecraft:red_mushroom": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Mushroom",
            "icon_path": "icons/red_mushroom.png",
            "identifier": "minecraft:red_mushroom"
        },
        "minecraft:crimson_fungus": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Fungus",
            "icon_path": "icons/crimson_fungus.png",
            "identifier": "minecraft:crimson_fungus"
        },
        "minecraft:warped_fungus": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Fungus",
            "icon_path": "icons/warped_fungus.png",
            "identifier": "minecraft:warped_fungus"
        },
        "minecraft:brown_mushroom_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Brown Mushroom Block",
            "icon_path": "icons/brown_mushroom_block.png",
            "identifier": "minecraft:brown_mushroom_block"
        },
        "minecraft:red_mushroom_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Mushroom Block",
            "icon_path": "icons/red_mushroom_block.png",
            "identifier": "minecraft:red_mushroom_block"
        },
        "minecraft:mushroom_stem": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Mushroom Stem",
            "icon_path": "icons/mushroom_stem.png",
            "identifier": "minecraft:brown_mushroom_block"
        },
        "minecraft:mushroom": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mushroom",
            "icon_path": "icons/mushroom.png",
            "identifier": "minecraft:brown_mushroom_block"
        },
        "minecraft:egg": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Egg",
            "icon_path": "icons/egg.png",
            "identifier": "minecraft:egg"
        },
        "minecraft:sugar_cane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sugar Canes",
            "icon_path": "icons/sugar_cane.png",
            "identifier": "minecraft:sugar_cane"
        },
        "minecraft:sugar": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sugar",
            "icon_path": "icons/sugar.png",
            "identifier": "minecraft:sugar"
        },
        "minecraft:rotten_flesh": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rotten Flesh",
            "icon_path": "icons/rotten_flesh.png",
            "identifier": "minecraft:rotten_flesh"
        },
        "minecraft:bone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bone",
            "icon_path": "icons/bone.png",
            "identifier": "minecraft:bone"
        },
        "minecraft:cobweb": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cobweb",
            "icon_path": "icons/cobweb.png",
            "identifier": "minecraft:web"
        },
        "minecraft:spider_eye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spider Eye",
            "icon_path": "icons/spider_eye.png",
            "identifier": "minecraft:spider_eye"
        },
        "minecraft:spawner": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Monster Spawner",
            "icon_path": "icons/spawner.png",
            "identifier": "minecraft:mob_spawner"
        },
        "minecraft:infested_stone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Infested Stone",
            "icon_path": "icons/infested_stone.png",
            "identifier": "minecraft:monster_egg"
        },
        "minecraft:infested_cobblestone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Infested Cobblestone",
            "icon_path": "icons/infested_cobblestone.png",
            "identifier": "minecraft:monster_egg"
        },
        "minecraft:infested_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Infested Stone Brick",
            "icon_path": "icons/infested_stone_bricks.png",
            "identifier": "minecraft:monster_egg"
        },
        "minecraft:infested_mossy_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Infested Mossy Stone Brick",
            "icon_path": "icons/infested_mossy_stone_bricks.png",
            "identifier": "minecraft:monster_egg"
        },
        "minecraft:infested_cracked_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Infested Cracked Stone Brick",
            "icon_path": "icons/infested_cracked_stone_bricks.png",
            "identifier": "minecraft:monster_egg"
        },
        "minecraft:infested_chiseled_stone_bricks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Infested Chiseled Stone Brick",
            "icon_path": "icons/infested_chiseled_stone_bricks.png",
            "identifier": "minecraft:monster_egg"
        },
        "minecraft:infested_deepslate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Infested Deepslate",
            "icon_path": "icons/infested_deepslate.png",
            "identifier": "minecraft:infested_deepslate"
        },
        "minecraft:dragon_egg": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Dragon Egg",
            "icon_path": "icons/dragon_egg.png",
            "identifier": "minecraft:dragon_egg"
        },
        "minecraft:turtle_egg": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sea Turtle Egg",
            "icon_path": "icons/turtle_egg.png",
            "identifier": "minecraft:turtle_egg"
        },
        "minecraft:frog_spawn": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Frogspawn",
            "icon_path": "icons/frog_spawn.png",
            "identifier": "minecraft:frog_spawn"
        },
        "minecraft:pearlescent_froglight": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pearlescent Froglight",
            "icon_path": "icons/pearlescent_froglight.png",
            "identifier": "minecraft:pearlescent_froglight"
        },
        "minecraft:verdant_froglight": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Verdant Froglight",
            "icon_path": "icons/verdant_froglight.png",
            "identifier": "minecraft:verdant_froglight"
        },
        "minecraft:ochre_froglight": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ochre Froglight",
            "icon_path": "icons/ochre_froglight.png",
            "identifier": "minecraft:ochre_froglight"
        },
        # Spawn Eggs
        "minecraft:chicken_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chicken Spawn Egg",
            "icon_path": "icons/chicken_spawn_egg.png",
            "identifier": "minecraft:chicken_spawn_egg"
        },
        "minecraft:bee_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bee Spawn Egg",
            "icon_path": "icons/bee_spawn_egg.png",
            "identifier": "minecraft:bee_spawn_egg"
        },
        "minecraft:cow_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cow Spawn Egg",
            "icon_path": "icons/cow_spawn_egg.png",
            "identifier": "minecraft:cow_spawn_egg"
        },
        "minecraft:pig_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pig Spawn Egg",
            "icon_path": "icons/pig_spawn_egg.png",
            "identifier": "minecraft:pig_spawn_egg"
        },
        "minecraft:sheep_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sheep Spawn Egg",
            "icon_path": "icons/sheep_spawn_egg.png",
            "identifier": "minecraft:sheep_spawn_egg"
        },
        "minecraft:wolf_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wolf Spawn Egg",
            "icon_path": "icons/wolf_spawn_egg.png",
            "identifier": "minecraft:wolf_spawn_egg"
        },
        "minecraft:polar_bear_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Polar Bear Spawn Egg",
            "icon_path": "icons/polar_bear_spawn_egg.png",
            "identifier": "minecraft:polar_bear_spawn_egg"
        },
        "minecraft:ocelot_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ocelot Spawn Egg",
            "icon_path": "icons/ocelot_spawn_egg.png",
            "identifier": "minecraft:ocelot_spawn_egg"
        },
        "minecraft:cat_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cat Spawn Egg",
            "icon_path": "icons/cat_spawn_egg.png",
            "identifier": "minecraft:cat_spawn_egg"
        },
        "minecraft:mooshroom_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mooshroom Spawn Egg",
            "icon_path": "icons/mooshroom_spawn_egg.png",
            "identifier": "minecraft:mooshroom_spawn_egg"
        },
        "minecraft:bat_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bat Spawn Egg",
            "icon_path": "icons/bat_spawn_egg.png",
            "identifier": "minecraft:bat_spawn_egg"
        },
        "minecraft:parrot_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Parrot Spawn Egg",
            "icon_path": "icons/parrot_spawn_egg.png",
            "identifier": "minecraft:parrot_spawn_egg"
        },
        "minecraft:rabbit_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rabbit Spawn Egg",
            "icon_path": "icons/rabbit_spawn_egg.png",
            "identifier": "minecraft:rabbit_spawn_egg"
        },
        "minecraft:llama_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Llama Spawn Egg",
            "icon_path": "icons/llama_spawn_egg.png",
            "identifier": "minecraft:llama_spawn_egg"
        },
        "minecraft:horse_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Horse Spawn Egg",
            "icon_path": "icons/horse_spawn_egg.png",
            "identifier": "minecraft:horse_spawn_egg"
        },
        "minecraft:donkey_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Donkey Spawn Egg",
            "icon_path": "icons/donkey_spawn_egg.png",
            "identifier": "minecraft:donkey_spawn_egg"
        },
        "minecraft:mule_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mule Spawn Egg",
            "icon_path": "icons/mule_spawn_egg.png",
            "identifier": "minecraft:mule_spawn_egg"
        },
        "minecraft:skeleton_horse_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Skeleton Horse Spawn Egg",
            "icon_path": "icons/skeleton_horse_spawn_egg.png",
            "identifier": "minecraft:skeleton_horse_spawn_egg"
        },
        "minecraft:zombie_horse_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Zombie Horse Spawn Egg",
            "icon_path": "icons/zombie_horse_spawn_egg.png",
            "identifier": "minecraft:zombie_horse_spawn_egg"
        },
        "minecraft:tropical_fish_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tropical Fish Spawn Egg",
            "icon_path": "icons/tropical_fish_spawn_egg.png",
            "identifier": "minecraft:tropical_fish_spawn_egg"
        },
        "minecraft:cod_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cod Spawn Egg",
            "icon_path": "icons/cod_spawn_egg.png",
            "identifier": "minecraft:cod_spawn_egg"
        },
        "minecraft:pufferfish_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pufferfish Spawn Egg",
            "icon_path": "icons/pufferfish_spawn_egg.png",
            "identifier": "minecraft:pufferfish_spawn_egg"
        },
        "minecraft:salmon_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Salmon Spawn Egg",
            "icon_path": "icons/salmon_spawn_egg.png",
            "identifier": "minecraft:salmon_spawn_egg"
        },
        "minecraft:dolphin_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dolphin Spawn Egg",
            "icon_path": "icons/dolphin_spawn_egg.png",
            "identifier": "minecraft:dolphin_spawn_egg"
        },
        "minecraft:turtle_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Turtle Spawn Egg",
            "icon_path": "icons/turtle_spawn_egg.png",
            "identifier": "minecraft:turtle_spawn_egg"
        },
        "minecraft:panda_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Panda Spawn Egg",
            "icon_path": "icons/panda_spawn_egg.png",
            "identifier": "minecraft:panda_spawn_egg"
        },
        "minecraft:fox_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Fox Spawn Egg",
            "icon_path": "icons/fox_spawn_egg.png",
            "identifier": "minecraft:fox_spawn_egg"
        },
        "minecraft:creeper_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Creeper Spawn Egg",
            "icon_path": "icons/creeper_spawn_egg.png",
            "identifier": "minecraft:creeper_spawn_egg"
        },
        "minecraft:enderman_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Enderman Spawn Egg",
            "icon_path": "icons/enderman_spawn_egg.png",
            "identifier": "minecraft:enderman_spawn_egg"
        },
        "minecraft:silverfish_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Silverfish Spawn Egg",
            "icon_path": "icons/silverfish_spawn_egg.png",
            "identifier": "minecraft:silverfish_spawn_egg"
        },
        "minecraft:skeleton_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Skeleton Spawn Egg",
            "icon_path": "icons/skeleton_spawn_egg.png",
            "identifier": "minecraft:skeleton_spawn_egg"
        },
        "minecraft:wither_skeleton_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wither Skeleton Spawn Egg",
            "icon_path": "icons/wither_skeleton_spawn_egg.png",
            "identifier": "minecraft:wither_skeleton_spawn_egg"
        },
        "minecraft:stray_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stray Spawn Egg",
            "icon_path": "icons/stray_spawn_egg.png",
            "identifier": "minecraft:stray_spawn_egg"
        },
        "minecraft:slime_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Slime Spawn Egg",
            "icon_path": "icons/slime_spawn_egg.png",
            "identifier": "minecraft:slime_spawn_egg"
        },
        "minecraft:spider_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spider Spawn Egg",
            "icon_path": "icons/spider_spawn_egg.png",
            "identifier": "minecraft:spider_spawn_egg"
        },
        "minecraft:zombie_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Zombie Spawn Egg",
            "icon_path": "icons/zombie_spawn_egg.png",
            "identifier": "minecraft:zombie_spawn_egg"
        },
        "minecraft:zombified_piglin_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Zombified Piglin Spawn Egg",
            "icon_path": "icons/zombified_piglin_spawn_egg.png",
            "identifier": "minecraft:zombie_pigman_spawn_egg"
        },
        "minecraft:husk_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Husk Spawn Egg",
            "icon_path": "icons/husk_spawn_egg.png",
            "identifier": "minecraft:husk_spawn_egg"
        },
        "minecraft:drowned_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Drowned Spawn Egg",
            "icon_path": "icons/drowned_spawn_egg.png",
            "identifier": "minecraft:drowned_spawn_egg"
        },
        "minecraft:squid_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Squid Spawn Egg",
            "icon_path": "icons/squid_spawn_egg.png",
            "identifier": "minecraft:squid_spawn_egg"
        },
        "minecraft:glow_squid_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glow Squid Spawn Egg",
            "icon_path": "icons/glow_squid_spawn_egg.png",
            "identifier": "minecraft:glow_squid_spawn_egg"
        },
        "minecraft:cave_spider_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cave Spider Spawn Egg",
            "icon_path": "icons/cave_spider_spawn_egg.png",
            "identifier": "minecraft:cave_spider_spawn_egg"
        },
        "minecraft:witch_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Witch Spawn Egg",
            "icon_path": "icons/witch_spawn_egg.png",
            "identifier": "minecraft:witch_spawn_egg"
        },
        "minecraft:guardian_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Guardian Spawn Egg",
            "icon_path": "icons/guardian_spawn_egg.png",
            "identifier": "minecraft:guardian_spawn_egg"
        },
        "minecraft:elder_guardian_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Elder Guardian Spawn Egg",
            "icon_path": "icons/elder_guardian_spawn_egg.png",
            "identifier": "minecraft:elder_guardian_spawn_egg"
        },
        "minecraft:endermite_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Endermite Spawn Egg",
            "icon_path": "icons/endermite_spawn_egg.png",
            "identifier": "minecraft:endermite_spawn_egg"
        },
        "minecraft:magma_cube_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Magma Cube Spawn Egg",
            "icon_path": "icons/magma_cube_spawn_egg.png",
            "identifier": "minecraft:magma_cube_spawn_egg"
        },
        "minecraft:strider_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Strider Spawn Egg",
            "icon_path": "icons/strider_spawn_egg.png",
            "identifier": "minecraft:strider_spawn_egg"
        },
        "minecraft:hoglin_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Hoglin Spawn Egg",
            "icon_path": "icons/hoglin_spawn_egg.png",
            "identifier": "minecraft:hoglin_spawn_egg"
        },
        "minecraft:piglin_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Piglin Spawn Egg",
            "icon_path": "icons/piglin_spawn_egg.png",
            "identifier": "minecraft:piglin_spawn_egg"
        },
        "minecraft:zoglin_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Zoglin Spawn Egg",
            "icon_path": "icons/zoglin_spawn_egg.png",
            "identifier": "minecraft:zoglin_spawn_egg"
        },
        "minecraft:piglin_brute_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Piglin Brute Spawn Egg",
            "icon_path": "icons/piglin_brute_spawn_egg.png",
            "identifier": "minecraft:piglin_brute_spawn_egg"
        },
        "minecraft:goat_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Goat Spawn Egg",
            "icon_path": "icons/goat_spawn_egg.png",
            "identifier": "minecraft:goat_spawn_egg"
        },
        "minecraft:axolotl_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Axolotl Spawn Egg",
            "icon_path": "icons/axolotl_spawn_egg.png",
            "identifier": "minecraft:axolotl_spawn_egg"
        },
        "minecraft:warden_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Warden Spawn Egg",
            "icon_path": "icons/warden_spawn_egg.png",
            "identifier": "minecraft:warden_spawn_egg"
        },
        "minecraft:allay_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Allay Spawn Egg",
            "icon_path": "icons/allay_spawn_egg.png",
            "identifier": "minecraft:allay_spawn_egg"
        },
        "minecraft:frog_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Frog Spawn Egg",
            "icon_path": "icons/frog_spawn_egg.png",
            "identifier": "minecraft:frog_spawn_egg"
        },
        "minecraft:tadpole_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tadpole Spawn Egg",
            "icon_path": "icons/tadpole_spawn_egg.png",
            "identifier": "minecraft:tadpole_spawn_egg"
        },
        "minecraft:ghast_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ghast Spawn Egg",
            "icon_path": "icons/ghast_spawn_egg.png",
            "identifier": "minecraft:ghast_spawn_egg"
        },
        "minecraft:blaze_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blaze Spawn Egg",
            "icon_path": "icons/blaze_spawn_egg.png",
            "identifier": "minecraft:blaze_spawn_egg"
        },
        "minecraft:shulker_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Shulker Spawn Egg",
            "icon_path": "icons/shulker_spawn_egg.png",
            "identifier": "minecraft:shulker_spawn_egg"
        },
        "minecraft:vindicator_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Vindicator Spawn Egg",
            "icon_path": "icons/vindicator_spawn_egg.png",
            "identifier": "minecraft:vindicator_spawn_egg"
        },
        "minecraft:evoker_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Evoker Spawn Egg",
            "icon_path": "icons/evoker_spawn_egg.png",
            "identifier": "minecraft:evoker_spawn_egg"
        },
        "minecraft:vex_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Vex Spawn Egg",
            "icon_path": "icons/vex_spawn_egg.png",
            "identifier": "minecraft:vex_spawn_egg"
        },
        "minecraft:villager_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Villager Spawn Egg",
            "icon_path": "icons/villager_spawn_egg.png",
            "identifier": "minecraft:villager_spawn_egg"
        },
        "minecraft:wandering_trader_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wandering Trader Spawn Egg",
            "icon_path": "icons/wandering_trader_spawn_egg.png",
            "identifier": "minecraft:wandering_trader_spawn_egg"
        },
        "minecraft:zombie_villager_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Zombie Villager Spawn Egg",
            "icon_path": "icons/zombie_villager_spawn_egg.png",
            "identifier": "minecraft:zombie_villager_spawn_egg"
        },
        "minecraft:phantom_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Phantom Spawn Egg",
            "icon_path": "icons/phantom_spawn_egg.png",
            "identifier": "minecraft:phantom_spawn_egg"
        },
        "minecraft:pillager_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pillager Spawn Egg",
            "icon_path": "icons/pillager_spawn_egg.png",
            "identifier": "minecraft:pillager_spawn_egg"
        },
        "minecraft:ravager_spawn_egg": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ravager Spawn Egg",
            "icon_path": "icons/ravager_spawn_egg.png",
            "identifier": "minecraft:ravager_spawn_egg"
        },
        # Blocks
        "minecraft:obsidian": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Obsidian",
            "icon_path": "icons/obsidian.png",
            "identifier": "minecraft:obsidian"
        },
        "minecraft:crying_obsidian": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crying Obsidian",
            "icon_path": "icons/crying_obsidian.png",
            "identifier": "minecraft:crying_obsidian"
        },
        "minecraft:bedrock": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bedrock",
            "icon_path": "icons/bedrock.png",
            "identifier": "minecraft:bedrock"
        },
        "minecraft:soul_sand": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Soul Sand",
            "icon_path": "icons/soul_sand.png",
            "identifier": "minecraft:soul_sand"
        },
        "minecraft:netherrack": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherrack",
            "icon_path": "icons/netherrack.png",
            "identifier": "minecraft:netherrack"
        },
        "minecraft:magma_block": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Magma Block",
            "icon_path": "icons/magma_block.png",
            "identifier": "minecraft:magma"
        },
        "minecraft:nether_wart": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Wart",
            "icon_path": "icons/nether_wart.png",
            "identifier": "minecraft:nether_wart"
        },
        "minecraft:end_stone": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Stone",
            "icon_path": "icons/end_stone.png",
            "identifier": "minecraft:end_stone"
        },
        "minecraft:chorus_flower": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Chorus Flower",
            "icon_path": "icons/chorus_flower.png",
            "identifier": "minecraft:chorus_flower"
        },
        "minecraft:chorus_plant": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Chorus Plant",
            "icon_path": "icons/chorus_plant.png",
            "identifier": "minecraft:chorus_plant"
        },
        "minecraft:chorus_fruit": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Chorus Fruit",
            "icon_path": "icons/chorus_fruit.png",
            "identifier": "minecraft:chorus_fruit"
        },
        "minecraft:popped_chorus_fruit": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Popped Chorus Fruit",
            "icon_path": "icons/popped_chorus_fruit.png",
            "identifier": "minecraft:popped_chorus_fruit"
        },
        "minecraft:sponge": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sponge",
            "icon_path": "icons/sponge.png",
            "identifier": "minecraft:sponge"
        },
        "minecraft:wet_sponge": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Wet Sponge",
            "icon_path": "icons/wet_sponge.png",
            "identifier": "minecraft:sponge"
        },
        # Coral
        "minecraft:tube_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tube Coral Block",
            "icon_path": "icons/tube_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:brain_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Brain Coral Block",
            "icon_path": "icons/brain_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:bubble_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Bubble Coral Block",
            "icon_path": "icons/bubble_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:fire_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Fire Coral Block",
            "icon_path": "icons/fire_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:horn_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Horn Coral block",
            "icon_path": "icons/horn_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:dead_tube_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Dead Tube Coral Block",
            "icon_path": "icons/dead_tube_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:dead_brain_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Dead Brain Coral Block",
            "icon_path": "icons/dead_brain_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:dead_bubble_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Dead Bubble Coral Block",
            "icon_path": "icons/dead_bubble_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:dead_fire_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Dead Fire Coral Block",
            "icon_path": "icons/dead_fire_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:dead_horn_coral_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Dead Horn Coral Block",
            "icon_path": "icons/dead_horn_coral_block.png",
            "identifier": "minecraft:coral_block"
        },
        "minecraft:sculk": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sculk",
            "icon_path": "icons/sculk.png",
            "identifier": "minecraft:sculk"
        },
        "minecraft:sculk_vein": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sculk Vein",
            "icon_path": "icons/sculk_vein.png",
            "identifier": "minecraft:sculk_vein"
        },
        "minecraft:sculk_catalyst": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sculk Catalyst",
            "icon_path": "icons/sculk_catalyst.png",
            "identifier": "minecraft:sculk_catalyst"
        },
        "minecraft:sculk_shrieker": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sculk Shrieker",
            "icon_path": "icons/sculk_shrieker.png",
            "identifier": "minecraft:sculk_shrieker"
        },
        "minecraft:sculk_sensor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sculk Sensor",
            "icon_path": "icons/sculk_sensor.png",
            "identifier": "minecraft:sculk_sensor"
        },
        "minecraft:reinforced_deepslate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Reinforced Deepslate",
            "icon_path": "icons/reinforced_deepslate.png",
            "identifier": "minecraft:reinforced_deepslate"
        },
        # Armor
        "minecraft:leather_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Leather Cap",
            "icon_path": "icons/leather_helmet.png",
            "identifier": "minecraft:leather_helmet"
        },
        "minecraft:chainmail_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chainmail Helmet",
            "icon_path": "icons/chainmail_helmet.png",
            "identifier": "minecraft:chainmail_helmet"
        },
        "minecraft:iron_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Helmet",
            "icon_path": "icons/iron_helmet.png",
            "identifier": "minecraft:iron_helmet"
        },
        "minecraft:golden_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Helmet",
            "icon_path": "icons/golden_helmet.png",
            "identifier": "minecraft:golden_helmet"
        },
        "minecraft:diamond_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Helmet",
            "icon_path": "icons/diamond_helmet.png",
            "identifier": "minecraft:diamond_helmet"
        },
        "minecraft:netherite_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Helmet",
            "icon_path": "icons/netherite_helmet.png",
            "identifier": "minecraft:netherite_helmet"
        },
        "minecraft:leather_chestplate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Leather Tunic",
            "icon_path": "icons/leather_chestplate.png",
            "identifier": "minecraft:leather_chestplate"
        },
        "minecraft:chainmail_chestplate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chainmail Chestplate",
            "icon_path": "icons/chainmail_chestplate.png",
            "identifier": "minecraft:chainmail_chestplate"
        },
        "minecraft:iron_chestplate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Chestplate",
            "icon_path": "icons/iron_chestplate.png",
            "identifier": "minecraft:iron_chestplate"
        },
        "minecraft:golden_chestplate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Chestplate",
            "icon_path": "icons/golden_chestplate.png",
            "identifier": "minecraft:golden_chestplate"
        },
        "minecraft:diamond_chestplate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Chestplate",
            "icon_path": "icons/diamond_chestplate.png",
            "identifier": "minecraft:diamond_chestplate"
        },
        "minecraft:netherite_chestplate": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Chestplate",
            "icon_path": "icons/netherite_chestplate.png",
            "identifier": "minecraft:netherite_chestplate"
        },
        "minecraft:leather_leggings": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Leather Pants",
            "icon_path": "icons/leather_leggings.png",
            "identifier": "minecraft:leather_leggings"
        },
        "minecraft:chainmail_leggings": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chainmail Leggings",
            "icon_path": "icons/chainmail_leggings.png",
            "identifier": "minecraft:chainmail_leggings"
        },
        "minecraft:iron_leggings": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Leggings",
            "icon_path": "icons/iron_leggings.png",
            "identifier": "minecraft:iron_leggings"
        },
        "minecraft:golden_leggings": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Leggings",
            "icon_path": "icons/golden_leggings.png",
            "identifier": "minecraft:golden_leggings"
        },
        "minecraft:diamond_leggings": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Leggings",
            "icon_path": "icons/diamond_leggings.png",
            "identifier": "minecraft:diamond_leggings"
        },
        "minecraft:netherite_leggings": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Leggings",
            "icon_path": "icons/netherite_leggings.png",
            "identifier": "minecraft:netherite_leggings"
        },
        "minecraft:leather_boots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Leather Boots",
            "icon_path": "icons/leather_boots.png",
            "identifier": "minecraft:leather_boots"
        },
        "minecraft:chainmail_boots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chainmail Boots",
            "icon_path": "icons/chainmail_boots.png",
            "identifier": "minecraft:chainmail_boots"
        },
        "minecraft:iron_boots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Boots",
            "icon_path": "icons/iron_boots.png",
            "identifier": "minecraft:iron_boots"
        },
        "minecraft:golden_boots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Boots",
            "icon_path": "icons/golden_boots.png",
            "identifier": "minecraft:golden_boots"
        },
        "minecraft:diamond_boots": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Boots",
            "icon_path": "icons/diamond_boots.png",
            "identifier": "minecraft:diamond_boots"
        },
        "minecraft:netherite_boots": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Boots",
            "icon_path": "icons/netherite_boots.png",
            "identifier": "minecraft:netherite_boots"
        },
        # Tools
        "minecraft:wooden_sword": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Sword",
            "icon_path": "icons/wooden_sword.png",
            "identifier": "minecraft:wooden_sword"
        },
        "minecraft:stone_sword": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Sword",
            "icon_path": "icons/stone_sword.png",
            "identifier": "minecraft:stone_sword"
        },
        "minecraft:iron_sword": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Sword",
            "icon_path": "icons/iron_sword.png",
            "identifier": "minecraft:iron_sword"
        },
        "minecraft:golden_sword": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Sword",
            "icon_path": "icons/golden_sword.png",
            "identifier": "minecraft:golden_sword"
        },
        "minecraft:diamond_sword": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Sword",
            "icon_path": "icons/diamond_sword.png",
            "identifier": "minecraft:diamond_sword"
        },
        "minecraft:netherite_sword": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Sword",
            "icon_path": "icons/netherite_sword.png",
            "identifier": "minecraft:netherite_sword"
        },
        "minecraft:wooden_axe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Axe",
            "icon_path": "icons/wooden_axe.png",
            "identifier": "minecraft:wooden_axe"
        },
        "minecraft:stone_axe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Axe",
            "icon_path": "icons/stone_axe.png",
            "identifier": "minecraft:stone_axe"
        },
        "minecraft:iron_axe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Axe",
            "icon_path": "icons/iron_axe.png",
            "identifier": "minecraft:iron_axe"
        },
        "minecraft:golden_axe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Axe",
            "icon_path": "icons/golden_axe.png",
            "identifier": "minecraft:golden_axe"
        },
        "minecraft:diamond_axe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Axe",
            "icon_path": "icons/diamond_axe.png",
            "identifier": "minecraft:diamond_axe"
        },
        "minecraft:netherite_axe": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Axe",
            "icon_path": "icons/netherite_axe.png",
            "identifier": "minecraft:netherite_axe"
        },
        "minecraft:wooden_pickaxe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Pickaxe",
            "icon_path": "icons/wooden_pickaxe.png",
            "identifier": "minecraft:wooden_pickaxe"
        },
        "minecraft:stone_pickaxe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Pickaxe",
            "icon_path": "icons/stone_pickaxe.png",
            "identifier": "minecraft:stone_pickaxe"
        },
        "minecraft:iron_pickaxe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Pickaxe",
            "icon_path": "icons/iron_pickaxe.png",
            "identifier": "minecraft:iron_pickaxe"
        },
        "minecraft:golden_pickaxe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Pickaxe",
            "icon_path": "icons/golden_pickaxe.png",
            "identifier": "minecraft:golden_pickaxe"
        },
        "minecraft:diamond_pickaxe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Pickaxe",
            "icon_path": "icons/diamond_pickaxe.png",
            "identifier": "minecraft:diamond_pickaxe"
        },
        "minecraft:netherite_pickaxe": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Pickaxe",
            "icon_path": "icons/netherite_pickaxe.png",
            "identifier": "minecraft:netherite_pickaxe"
        },
        "minecraft:wooden_shovel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Shovel",
            "icon_path": "icons/wooden_shovel.png",
            "identifier": "minecraft:wooden_shovel"
        },
        "minecraft:stone_shovel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Shovel",
            "icon_path": "icons/stone_shovel.png",
            "identifier": "minecraft:stone_shovel"
        },
        "minecraft:iron_shovel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Shovel",
            "icon_path": "icons/iron_shovel.png",
            "identifier": "minecraft:iron_shovel"
        },
        "minecraft:golden_shovel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Shovel",
            "icon_path": "icons/golden_shovel.png",
            "identifier": "minecraft:golden_shovel"
        },
        "minecraft:diamond_shovel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Shovel",
            "icon_path": "icons/diamond_shovel.png",
            "identifier": "minecraft:diamond_shovel"
        },
        "minecraft:netherite_shovel": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Shovel",
            "icon_path": "icons/netherite_shovel.png",
            "identifier": "minecraft:netherite_shovel"
        },
        "minecraft:wooden_hoe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Hoe",
            "icon_path": "icons/wooden_hoe.png",
            "identifier": "minecraft:wooden_hoe"
        },
        "minecraft:stone_hoe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Hoe",
            "icon_path": "icons/stone_hoe.png",
            "identifier": "minecraft:stone_hoe"
        },
        "minecraft:iron_hoe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Hoe",
            "icon_path": "icons/iron_hoe.png",
            "identifier": "minecraft:iron_hoe"
        },
        "minecraft:golden_hoe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Hoe",
            "icon_path": "icons/golden_hoe.png",
            "identifier": "minecraft:golden_hoe"
        },
        "minecraft:diamond_hoe": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Hoe",
            "icon_path": "icons/diamond_hoe.png",
            "identifier": "minecraft:diamond_hoe"
        },
        "minecraft:netherite_hoe": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Hoe",
            "icon_path": "icons/netherite_hoe.png",
            "identifier": "minecraft:netherite_hoe"
        },
        "minecraft:bow": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bow",
            "icon_path": "icons/bow.png",
            "identifier": "minecraft:bow"
        },
        "minecraft:crossbow": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Crossbow",
            "icon_path": "icons/crossbow.png",
            "identifier": "minecraft:crossbow"
        },
        # arrows
        "minecraft:arrow": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Arrow",
            "icon_path": "icons/arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:night_vision_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Arrow of Night Vision (0:22)",
            "icon_path": "icons/night_vision_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:night_vision_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Arrow of Night Vision (1:00)",
            "icon_path": "icons/night_vision_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:invisibility_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Arrow of invisibility (0:22)",
            "icon_path": "icons/invisibility_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:invisibility_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Arrow of invisibility (1:00)",
            "icon_path": "icons/invisibility_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:leaping_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Arrow of Leaping I (0:22)",
            "icon_path": "icons/leaping_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:leaping_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Arrow of Leaping I (1:00)",
            "icon_path": "icons/leaping_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:leaping_2_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Arrow of Leaping II (0:11)",
            "icon_path": "icons/leaping_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:fire_resistance_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Arrow of ire Resistance (0:22)",
            "icon_path": "icons/fire_resistance_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:fire_resistance_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Arrow of Fire Resistance (1:00)",
            "icon_path": "icons/fire_resistance_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:speed_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Arrow of Speed I (0:22)",
            "icon_path": "icons/speed_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:speed_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 16,
            "display_name": "Arrow of Speed I (1:00)",
            "icon_path": "icons/speed_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:speed_2_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 17,
            "display_name": "Arrow of Speed I (0:11)",
            "icon_path": "icons/speed_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:slowness_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 18,
            "display_name": "Arrow of Slowness (0:11)",
            "icon_path": "icons/slowness_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:slowness_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 19,
            "display_name": "Arrow of Slowness (0:30)",
            "icon_path": "icons/slowness_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:water_breathing_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 20,
            "display_name": "Arrow of Water Breathing (0:22)",
            "icon_path": "icons/water_breathing_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:water_breathing_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 21,
            "display_name": "Arrow of Water Breathing (1:00)",
            "icon_path": "icons/water_breathing_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:healing_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 22,
            "display_name": "Arrow of Healing I",
            "icon_path": "icons/healing_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:healing_arrow_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 23,
            "display_name": "Arrow of Healing II",
            "icon_path": "icons/healing_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:harming_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 24,
            "display_name": "Arrow of Harming I",
            "icon_path": "icons/harming_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:harming_arrow_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 25,
            "display_name": "Arrow of Harming II",
            "icon_path": "icons/harming_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:poison_arrow_0.05": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 26,
            "display_name": "Arrow of Poison (0:05)",
            "icon_path": "icons/poison_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:poison_arrow_0.15": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 27,
            "display_name": "Arrow of Poison (0:15)",
            "icon_path": "icons/poison_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:poison_2_arrow_0.02": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 28,
            "display_name": "Arrow of Poison II (0:02)",
            "icon_path": "icons/poison_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:regeneration_arrow_0.05": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 29,
            "display_name": "Arrow of Regeneration (0:05)",
            "icon_path": "icons/regeneration_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:regeneration_arrow_0.15": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 30,
            "display_name": "Arrow of Regeneration (0:15)",
            "icon_path": "icons/regeneration_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:regeneration_2_arrow_0.02": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 31,
            "display_name": "Arrow of Regeneration II (0:02)",
            "icon_path": "icons/regeneration_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:strength_arrow_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 32,
            "display_name": "Arrow of Strength (0:22)",
            "icon_path": "icons/strength_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:strength_arrow_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 33,
            "display_name": "Arrow of Strength (1:00)",
            "icon_path": "icons/strength_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:strength_2_arrow_0.11": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 33,
            "display_name": "Arrow of Strength II (0:11)",
            "icon_path": "icons/strength_arrow.png",
            "identifier": "minecraft:arrow"
        },

        "minecraft:weakness_arrow_0.11": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 34,
            "display_name": "Arrow of Weakness (0:11)",
            "icon_path": "icons/weakness_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:weakness_arrow_0.30": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 35,
            "display_name": "Arrow of Weakness (0:30)",
            "icon_path": "icons/weakness_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:decay_arrow_0.05": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 36,
            "display_name": "Arrow of Decay (0:05)",
            "icon_path": "icons/decay_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:turtle_master_arrow_0.02": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 37,
            "display_name": "Arrow of Turtle Master (0:02)",
            "icon_path": "icons/turtle_master_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:turtle_master_arrow_0.05": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 38,
            "display_name": "Arrow of Turtle Master (0:05)",
            "icon_path": "icons/turtle_master_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:turtle_master_2_arrow_0.02": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 39,
            "display_name": "Arrow of Turtle Master II (0:02)",
            "icon_path": "icons/turtle_master_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:slow_falling_arrow_0.11": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 40,
            "display_name": "Arrow of Slow Falling II (0:11)",
            "icon_path": "icons/slow_falling_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:slow_falling_arrow_0.30": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 41,
            "display_name": "Arrow of Slow Falling II (0:30)",
            "icon_path": "icons/slow_falling_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:slowness_arrow_0.02": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 42,
            "display_name": "Arrow of Slowness (0:02)",
            "icon_path": "icons/slowness_arrow.png",
            "identifier": "minecraft:arrow"
        },
        "minecraft:shield": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Shield",
            "icon_path": "icons/shield.png",
            "identifier": "minecraft:shield"
        },
        # Food
        "minecraft:cooked_chicken": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cooked Chicken",
            "icon_path": "icons/cooked_chicken.png",
            "identifier": "minecraft:cooked_chicken"
        },
        "minecraft:cooked_porkchop": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cooked Porkchop",
            "icon_path": "icons/cooked_porkchop.png",
            "identifier": "minecraft:cooked_porkchop"
        },
        "minecraft:cooked_beef": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Steak",
            "icon_path": "icons/cooked_beef.png",
            "identifier": "minecraft:cooked_beef"
        },
        "minecraft:cooked_mutton": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cooked Mutton",
            "icon_path": "icons/cooked_mutton.png",
            "identifier": "minecraft:cooked_mutton"
        },
        "minecraft:cooked_rabbit": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cooked Rabbit",
            "icon_path": "icons/cooked_rabbit.png",
            "identifier": "minecraft:cooked_rabbit"
        },
        "minecraft:cooked_cod": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cooked Cod",
            "icon_path": "icons/cooked_cod.png",
            "identifier": "minecraft:cooked_cod"
        },
        "minecraft:cooked_salmon": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cooked Salmon",
            "icon_path": "icons/cooked_salmon.png",
            "identifier": "minecraft:cooked_salmon"
        },
        "minecraft:bread": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bread",
            "icon_path": "icons/bread.png",
            "identifier": "minecraft:bread"
        },
        "minecraft:mushroom_stew": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mushroom Stew",
            "icon_path": "icons/mushroom_stew.png",
            "identifier": "minecraft:mushroom_stew"
        },
        "minecraft:beetroot_soup": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Beetroot Soup",
            "icon_path": "icons/beetroot_soup.png",
            "identifier": "minecraft:beetroot_soup"
        },
        "minecraft:rabbit_stew": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rabbit Stew",
            "icon_path": "icons/rabbit_stew.png",
            "identifier": "minecraft:rabbit_stew"
        },
        "minecraft:baked_potato": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Baked Potato",
            "icon_path": "icons/baked_potato.png",
            "identifier": "minecraft:baked_potato"
        },
        "minecraft:cookie": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cookie",
            "icon_path": "icons/cookie.png",
            "identifier": "minecraft:cookie"
        },
        "minecraft:pumpkin_pie": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pumpkin Pie",
            "icon_path": "icons/pumpkin_pie.png",
            "identifier": "minecraft:pumpkin_pie"
        },
        "minecraft:cake": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cake",
            "icon_path": "icons/cake.png",
            "identifier": "minecraft:cake"
        },
        "minecraft:dried_kelp": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dried Kelp",
            "icon_path": "icons/dried_kelp.png",
            "identifier": "minecraft:dried_kelp"
        },
        # Tools
        "minecraft:fishing_rod": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Fishing Rod",
            "icon_path": "icons/fishing_rod.png",
            "identifier": "minecraft:fishing_rod"
        },
        "minecraft:carrot_on_a_stick": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Carrot on a Stick",
            "icon_path": "icons/carrot_on_a_stick.png",
            "identifier": "minecraft:carrot_on_a_stick"
        },
        "minecraft:warped_fungus_on_a_stick": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Fungus on a Stick",
            "icon_path": "icons/warped_fungus_on_a_stick.png",
            "identifier": "minecraft:warped_fungus_on_a_stick"
        },
        "minecraft:snowball": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Snowball",
            "icon_path": "icons/snowball.png",
            "identifier": "minecraft:snowball"
        },
        "minecraft:shears": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Shears",
            "icon_path": "icons/shears.png",
            "identifier": "minecraft:shears"
        },
        "minecraft:flint_and_steel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Flint and Steel",
            "icon_path": "icons/flint_and_steel.png",
            "identifier": "minecraft:flint_and_steel"
        },
        "minecraft:lead": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lead",
            "icon_path": "icons/lead.png",
            "identifier": "minecraft:lead"
        },
        "minecraft:clock": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Clock",
            "icon_path": "icons/clock.png",
            "identifier": "minecraft:clock"
        },
        "minecraft:compass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Compass",
            "icon_path": "icons/compass.png",
            "identifier": "minecraft:compass"
        },
        "minecraft:recovery_compass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "recovery_compass",
            "icon_path": "icons/recovery_compass.png",
            "identifier": "minecraft:recovery_compass"
        },
        "minecraft:map": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Empty Map",
            "icon_path": "icons/map.png",
            "identifier": "minecraft:empty_map"
        },
        "minecraft:locator_map": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Empty Locator Map",
            "icon_path": "icons/map.png",
            "identifier": "minecraft:empty_map"
        },
        "minecraft:saddle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Saddle",
            "icon_path": "icons/saddle.png",
            "identifier": "minecraft:saddle"
        },
        "minecraft:goat_horn_ponder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Goat Horn (Ponder)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_sing": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Goat Horn (Sing)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_seek": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Goat Horn (Seek)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_feel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Goat Horn (Feel)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_admire": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Goat Horn (Admire)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_call": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Goat Horn (Call)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_yearn": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Goat Horn (Yearn)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:goat_horn_resist": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Goat Horn (Resist)",
            "icon_path": "icons/goat_horn.png",
            "identifier": "minecraft:goat_horn"
        },
        "minecraft:leather_horse_armor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Leather Horse Armor",
            "icon_path": "icons/leather_horse_armor.png",
            "identifier": "minecraft:leather_horse_armor"
        },
        "minecraft:iron_horse_armor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Horse Armor",
            "icon_path": "icons/iron_horse_armor.png",
            "identifier": "minecraft:iron_horse_armor"
        },
        "minecraft:golden_horse_armor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Golden Horse Armor",
            "icon_path": "icons/golden_horse_armor.png",
            "identifier": "minecraft:golden_horse_armor"
        },
        "minecraft:diamond_horse_armor": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond Horse Armor",
            "icon_path": "icons/diamond_horse_armor.png",
            "identifier": "minecraft:diamond_horse_armor"
        },
        "minecraft:trident": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Trident",
            "icon_path": "icons/trident.png",
            "identifier": "minecraft:trident"
        },
        "minecraft:turtle_helmet": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Turtle Shell",
            "icon_path": "icons/turtle_helmet.png",
            "identifier": "minecraft:turtle_helmet"
        },
        "minecraft:elytra": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Elytra",
            "icon_path": "icons/elytra.png",
            "identifier": "minecraft:elytra"
        },
        "minecraft:totem_of_undying": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Totem of Undying",
            "icon_path": "icons/totem_of_undying.png",
            "identifier": "minecraft:totem_of_undying"
        },
        "minecraft:glass_bottle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glass Bottle",
            "icon_path": "icons/glass_bottle.png",
            "identifier": "minecraft:glass_bottle"
        },
        "minecraft:experience_bottle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bottle o' Enchanting",
            "icon_path": "icons/experience_bottle.png",
            "identifier": "minecraft:experience_bottle"
        },
        # Potions
        "minecraft:water_bottle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Water Bottle",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:mundane_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Mundane Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:long_mundane_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Long Mundane Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:thick_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Thick Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:awkward_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Awkward Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:night_vision_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Potion of Night Vision (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:night_vision_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Potion of Night Vision (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:invisibility_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Potion of Invisibility (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:invisibility_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Potion of Invisibility (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:leaping_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Potion of Leaping (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:leaping_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Potion of Leaping (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:leaping_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Potion of Leaping II (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:fire_resistance_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Potion of Fire Resistance (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:fire_resistance_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Potion of Fire Resistance (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:swiftness_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Potion of Swiftness (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:swiftness_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Potion of Swiftness (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:swiftness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 16,
            "display_name": "Potion of Swiftness II (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:slowness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 17,
            "display_name": "Potion of Slowness (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:slowness_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 18,
            "display_name": "Potion of Slowness (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:water_breathing_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 19,
            "display_name": "Potion of Water Breathing (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:water_breathing_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 20,
            "display_name": "Potion of Water Breathing (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:healing_potion_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 21,
            "display_name": "Potion of Healing I",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:healing_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 22,
            "display_name": "Potion of Healing II",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:harming_potion_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 23,
            "display_name": "Potion of Harming I",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:harming_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 24,
            "display_name": "Potion of Harming II",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:poison_potion_0.45": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 25,
            "display_name": "Potion of Poison (0:45)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:poison_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 26,
            "display_name": "Potion of Poison (2:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:poison_potion_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 27,
            "display_name": "Potion of Poison II (0:22)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:regeneration_potion_0.45": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 28,
            "display_name": "Potion of Regeneration (0:45)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:regeneration_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 29,
            "display_name": "Potion of Regeneration (2:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:regeneration_potion_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 30,
            "display_name": "Potion of Regeneration II (0:22)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:strength_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 31,
            "display_name": "Potion of Strength (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:strength_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 32,
            "display_name": "Potion of Strength (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:strength_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 33,
            "display_name": "Potion of Strength (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:weakness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 34,
            "display_name": "Potion of Weakness (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:weakness_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 35,
            "display_name": "Potion of Weakness (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:decay_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 36,
            "display_name": "Potion of Decay (0:40)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:turtle_master_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 37,
            "display_name": "Potion of Turtle Master (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:turtle_master_potion_0.4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 38,
            "display_name": "Potion of Turtle Master (0:40)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:turtle_master_2_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 39,
            "display_name": "Potion of Turtle Master II (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:slow_falling_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 40,
            "display_name": "Potion of Slow Falling (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:slow_falling_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 41,
            "display_name": "Potion of Slow Falling (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:slowness_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 42,
            "display_name": "Potion of Slowness II (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:potion"
        },
        "minecraft:splash_water_bottle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Splash Water Bottle",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_mundane_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Splash Mundane Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_long_mundane_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Splash Long Mundane Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_thick_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Splash Thick Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_awkward_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Splash Awkward Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_night_vision_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Splash Potion of Night Vision (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_night_vision_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Splash Potion of Night Vision (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_invisibility_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Splash Potion of Invisibility (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_invisibility_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Splash Potion of Invisibility (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_leaping_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Splash Potion of Leaping (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_leaping_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Splash Potion of Leaping (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_leaping_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Splash Potion of Leaping II (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_fire_resistance_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Splash Potion of Fire Resistance (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_fire_resistance_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Splash Potion of Fire Resistance (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_swiftness_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Splash Potion of Swiftness (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_swiftness_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Splash Potion of Swiftness (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_swiftness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 16,
            "display_name": "Splash Potion of Swiftness II (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_slowness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 17,
            "display_name": "Splash Potion of Slowness (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_slowness_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 18,
            "display_name": "Splash Potion of Slowness (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_water_breathing_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 19,
            "display_name": "Splash Potion of Water Breathing (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_water_breathing_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 20,
            "display_name": "Splash Potion of Water Breathing (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_healing_potion_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 21,
            "display_name": "Splash Potion of Healing I",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_healing_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 22,
            "display_name": "Splash Potion of Healing II",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_harming_potion_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 23,
            "display_name": "Splash Potion of Harming I",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_harming_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 24,
            "display_name": "Splash Potion of Harming II",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_poison_potion_0.45": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 25,
            "display_name": "Splash Potion of Poison (0:45)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_poison_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 26,
            "display_name": "Splash Potion of Poison (2:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_poison_potion_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 27,
            "display_name": "Splash Potion of Poison II (0:22)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_regeneration_potion_0.45": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 28,
            "display_name": "Splash Potion of Regeneration (0:45)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_regeneration_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 29,
            "display_name": "Splash Potion of Regeneration (2:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_regeneration_potion_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 30,
            "display_name": "Splash Potion of Regeneration II (0:22)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_strength_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 31,
            "display_name": "Splash Potion of Strength (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_strength_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 32,
            "display_name": "Splash Potion of Strength (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_strength_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 33,
            "display_name": "Splash Potion of Strength (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_weakness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 34,
            "display_name": "Splash Potion of Weakness (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_weakness_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 35,
            "display_name": "Splash Potion of Weakness (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_decay_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 36,
            "display_name": "Splash Potion of Decay (0:40)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_turtle_master_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 37,
            "display_name": "Splash Potion of Turtle Master (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_turtle_master_potion_0.4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 38,
            "display_name": "Splash Potion of Turtle Master (0:40)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_turtle_master_2_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 39,
            "display_name": "Splash Potion of Turtle Master II (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_slow_falling_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 40,
            "display_name": "Splash Potion of Slow Falling (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_slow_falling_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 41,
            "display_name": "Splash Potion of Slow Falling (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:splash_slowness_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 42,
            "display_name": "Splash Potion of Slowness II (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:splash_potion"
        },
        "minecraft:lingering_water_bottle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lingering Water Bottle",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_mundane_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Lingering Mundane Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_long_mundane_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Lingering Long Mundane Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_thick_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Lingering Thick Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_awkward_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Lingering Awkward Potion",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_night_vision_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lingering Potion of Night Vision (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_night_vision_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Lingering Potion of Night Vision (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_invisibility_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Lingering Potion of Invisibility (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_invisibility_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Lingering Potion of Invisibility (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_leaping_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Lingering Potion of Leaping (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_leaping_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Lingering Potion of Leaping (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_leaping_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Lingering Potion of Leaping II (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_fire_resistance_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Lingering Potion of Fire Resistance (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_fire_resistance_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Lingering Potion of Fire Resistance (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_swiftness_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Lingering Potion of Swiftness (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_swiftness_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Lingering Potion of Swiftness (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_swiftness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 16,
            "display_name": "Lingering Potion of Swiftness II (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_slowness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 17,
            "display_name": "Lingering Potion of Slowness (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_slowness_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 18,
            "display_name": "Lingering Potion of Slowness (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_water_breathing_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 19,
            "display_name": "Lingering Potion of Water Breathing (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_water_breathing_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 20,
            "display_name": "Lingering Potion of Water Breathing (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_healing_potion_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 21,
            "display_name": "Lingering Potion of Healing I",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_healing_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 22,
            "display_name": "Lingering Potion of Healing II",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_harming_potion_1": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 23,
            "display_name": "Lingering Potion of Harming I",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_harming_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 24,
            "display_name": "Lingering Potion of Harming II",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_poison_potion_0.45": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 25,
            "display_name": "Lingering Potion of Poison (0:45)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_poison_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 26,
            "display_name": "Lingering Potion of Poison (2:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_poison_potion_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 27,
            "display_name": "Lingering Potion of Poison II (0:22)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_regeneration_potion_0.45": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 28,
            "display_name": "Lingering Potion of Regeneration (0:45)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_regeneration_potion_2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 29,
            "display_name": "Lingering Potion of Regeneration (2:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_regeneration_potion_0.22": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 30,
            "display_name": "Lingering Potion of Regeneration II (0:22)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_strength_potion_3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 31,
            "display_name": "Lingering Potion of Strength (3:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_strength_potion_8": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 32,
            "display_name": "Lingering Potion of Strength (8:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_strength_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 33,
            "display_name": "Lingering Potion of Strength (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_weakness_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 34,
            "display_name": "Lingering Potion of Weakness (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_weakness_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 35,
            "display_name": "Lingering Potion of Weakness (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_decay_potion": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 36,
            "display_name": "Lingering Potion of Decay (0:40)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_turtle_master_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 37,
            "display_name": "Lingering Potion of Turtle Master (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_turtle_master_potion_0.4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 38,
            "display_name": "Lingering Potion of Turtle Master (0:40)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_turtle_master_2_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 39,
            "display_name": "Lingering Potion of Turtle Master II (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_slow_falling_potion_1.3": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 40,
            "display_name": "Lingering Potion of Slow Falling (1:30)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_slow_falling_potion_4": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 41,
            "display_name": "Lingering Potion of Slow Falling (4:00)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        "minecraft:lingering_slowness_potion_0.2": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 42,
            "display_name": "Lingering Potion of Slowness II (0:20)",
            "icon_path": "icons/potion.png",
            "identifier": "minecraft:lingering_potion"
        },
        #
        "minecraft:spyglass": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spyglass",
            "icon_path": "icons/spyglass.png",
            "identifier": "minecraft:spyglass"
        },
        "minecraft:stick": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stick",
            "icon_path": "icons/stick.png",
            "identifier": "minecraft:stick"
        },
        "minecraft:white_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Bed",
            "icon_path": "icons/white_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:light_gray_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Bed",
            "icon_path": "icons/light_gray_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:gray_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Bed",
            "icon_path": "icons/gray_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:black_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Bed",
            "icon_path": "icons/black_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:brown_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Bed",
            "icon_path": "icons/brown_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:red_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Bed",
            "icon_path": "icons/red_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:orange_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Bed",
            "icon_path": "icons/orange_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:yellow_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Bed",
            "icon_path": "icons/yellow_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:lime_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Bed",
            "icon_path": "icons/lime_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:green_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Bed",
            "icon_path": "icons/green_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:cyan_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Bed",
            "icon_path": "icons/cyan_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:light_blue_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Bed",
            "icon_path": "icons/light_blue_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:blue_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Bed",
            "icon_path": "icons/blue_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:purple_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Bed",
            "icon_path": "icons/purple_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:magenta_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Bed",
            "icon_path": "icons/magenta_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:pink_bed": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Bed",
            "icon_path": "icons/pink_bed.png",
            "identifier": "minecraft:bed"
        },
        "minecraft:torch": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Torch",
            "icon_path": "icons/torch.png",
            "identifier": "minecraft:torch"
        },
        "minecraft:soul_torch": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Soul Torch",
            "icon_path": "icons/soul_torch.png",
            "identifier": "minecraft:soul_torch"
        },
        "minecraft:sea_pickle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sea Pickle",
            "icon_path": "icons/sea_pickle.png",
            "identifier": "minecraft:sea_pickle"
        },
        "minecraft:lantern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lantern",
            "icon_path": "icons/lantern.png",
            "identifier": "minecraft:lantern"
        },
        "minecraft:soul_lantern": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Soul Lantern",
            "icon_path": "icons/soul_lantern.png",
            "identifier": "minecraft:soul_lantern"
        },
        "minecraft:candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Candle",
            "icon_path": "icons/candle.png",
            "identifier": "minecraft:candle"
        },
        "minecraft:white_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Candle",
            "icon_path": "icons/white_candle.png",
            "identifier": "minecraft:white_candle"
        },
        "minecraft:orange_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Orange Candle",
            "icon_path": "icons/orange_candle.png",
            "identifier": "minecraft:orange_candle"
        },
        "minecraft:magenta_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Magenta Candle",
            "icon_path": "icons/magenta_candle.png",
            "identifier": "minecraft:magenta_candle"
        },
        "minecraft:light_blue_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Blue Candle",
            "icon_path": "icons/light_blue_candle.png",
            "identifier": "minecraft:light_blue_candle"
        },
        "minecraft:yellow_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Yellow Candle",
            "icon_path": "icons/yellow_candle.png",
            "identifier": "minecraft:yellow_candle"
        },
        "minecraft:lime_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lime Candle",
            "icon_path": "icons/lime_candle.png",
            "identifier": "minecraft:lime_candle"
        },
        "minecraft:pink_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pink Candle",
            "icon_path": "icons/pink_candle.png",
            "identifier": "minecraft:pink_candle"
        },
        "minecraft:gray_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gray Candle",
            "icon_path": "icons/gray_candle.png",
            "identifier": "minecraft:gray_candle"
        },
        "minecraft:light_gray_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Gray Candle",
            "icon_path": "icons/light_gray_candle.png",
            "identifier": "minecraft:light_gray_candle"
        },
        "minecraft:cyan_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cyan Candle",
            "icon_path": "icons/cyan_candle.png",
            "identifier": "minecraft:cyan_candle"
        },
        "minecraft:purple_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Purple Candle",
            "icon_path": "icons/purple_candle.png",
            "identifier": "minecraft:purple_candle"
        },
        "minecraft:blue_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blue Candle",
            "icon_path": "icons/blue_candle.png",
            "identifier": "minecraft:blue_candle"
        },
        "minecraft:brown_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brown Candle",
            "icon_path": "icons/brown_candle.png",
            "identifier": "minecraft:brown_candle"
        },
        "minecraft:green_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Green Candle",
            "icon_path": "icons/green_candle.png",
            "identifier": "minecraft:green_candle"
        },
        "minecraft:red_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Red Candle",
            "icon_path": "icons/red_candle.png",
            "identifier": "minecraft:red_candle"
        },
        "minecraft:black_candle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Black Candle",
            "icon_path": "icons/black_candle.png",
            "identifier": "minecraft:black_candle"
        },
        "minecraft:crafting_table": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Crafting Table",
            "icon_path": "icons/crafting_table.png",
            "identifier": "minecraft:crafting_table"
        },
        "minecraft:cartography_table": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cartography Table",
            "icon_path": "icons/cartography_table.png",
            "identifier": "minecraft:cartography_table"
        },
        "minecraft:fletching_table": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Fletching Table",
            "icon_path": "icons/fletching_table.png",
            "identifier": "minecraft:fletching_table"
        },
        "minecraft:smithing_table": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Smithing Table",
            "icon_path": "icons/smithing_table.png",
            "identifier": "minecraft:smithing_table"
        },
        "minecraft:beehive": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Beehive",
            "icon_path": "icons/beehive.png",
            "identifier": "minecraft:beehive"
        },
        "minecraft:campfire": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Campfire",
            "icon_path": "icons/campfire.png",
            "identifier": "minecraft:campfire"
        },
        "minecraft:soul_campfire": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Soul Campfire",
            "icon_path": "icons/soul_campfire.png",
            "identifier": "minecraft:soul_campfire"
        },
        "minecraft:furnace": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Furnace",
            "icon_path": "icons/furnace.png",
            "identifier": "minecraft:furnace"
        },
        "minecraft:blast_furnace": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blast Furnace",
            "icon_path": "icons/blast_furnace.png",
            "identifier": "minecraft:blast_furnace"
        },
        "minecraft:smoker": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Smoker",
            "icon_path": "icons/smoker.png",
            "identifier": "minecraft:smoker"
        },
        "minecraft:respawn_anchor": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Respawn Anchor",
            "icon_path": "icons/respawn_anchor.png",
            "identifier": "minecraft:respawn_anchor"
        },
        "minecraft:brewing_stand": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brewing Stand",
            "icon_path": "icons/brewing_stand.png",
            "identifier": "minecraft:brewing_stand"
        },
        "minecraft:anvil": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Anvil",
            "icon_path": "icons/anvil.png",
            "identifier": "minecraft:anvil"
        },
        "minecraft:slighlty_damaged_anvil": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Slightly Damaged Anvil",
            "icon_path": "icons/slighlty_damaged_anvil.png",
            "identifier": "minecraft:anvil"
        },
        "minecraft:very_damaged_anvil": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Very Damaged Anvil",
            "icon_path": "icons/very_damaged_anvil.png",
            "identifier": "minecraft:anvil"
        },
        "minecraft:grindstone": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Grindstone",
            "icon_path": "icons/grindstone.png",
            "identifier": "minecraft:grindstone"
        },
        "minecraft:enchanting_table": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Enchantment Table",
            "icon_path": "icons/enchanting_table.png",
            "identifier": "minecraft:enchanting_table"
        },
        "minecraft:bookshelf": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bookshelf",
            "icon_path": "icons/bookshelf.png",
            "identifier": "minecraft:bookshelf"
        },
        "minecraft:lectern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lectern",
            "icon_path": "icons/lectern.png",
            "identifier": "minecraft:lectern"
        },
        "minecraft:cauldron": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cauldron",
            "icon_path": "icons/cauldron.png",
            "identifier": "minecraft:cauldron"
        },
        "minecraft:composter": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Composter",
            "icon_path": "icons/composter.png",
            "identifier": "minecraft:composter"
        },
        "minecraft:chest": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chest",
            "icon_path": "icons/chest.png",
            "identifier": "minecraft:chest"
        },
        "minecraft:trapped_chest": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Trapped Chest",
            "icon_path": "icons/trapped_chest.png",
            "identifier": "minecraft:trapped_chest"
        },
        "minecraft:ender_chest": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Ender Chest",
            "icon_path": "icons/ender_chest.png",
            "identifier": "minecraft:ender_chest"
        },
        "minecraft:barrel": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Barrel",
            "icon_path": "icons/barrel.png",
            "identifier": "minecraft:barrel"
        },
        "minecraft:shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Shulker Box",
            "icon_path": "icons/shulker_box.png",
            "identifier": "minecraft:undyed_shulker_box"
        },
        "minecraft:white_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "White Shulker Box",
            "icon_path": "icons/white_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:gray_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Gray Shulker Box",
            "icon_path": "icons/gray_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:light_gray_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Light Gray Shulker Box",
            "icon_path": "icons/light_gray_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:black_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Black Shulker Box",
            "icon_path": "icons/black_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:brown_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Brown Shulker Box",
            "icon_path": "icons/brown_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:red_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Red Shulker Box",
            "icon_path": "icons/red_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:orange_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Orange Shulker Box",
            "icon_path": "icons/orange_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:yellow_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Yellow Shulker Box",
            "icon_path": "icons/yellow_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:lime_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Lime Shulker Box",
            "icon_path": "icons/lime_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:green_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Green Shulker Box",
            "icon_path": "icons/green_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:cyan_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Cyan Shulker Box",
            "icon_path": "icons/cyan_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:light_blue_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Light Blue Shulker Box",
            "icon_path": "icons/light_blue_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:blue_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Blue Shulker Box",
            "icon_path": "icons/blue_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:purple_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Purple Shulker Box",
            "icon_path": "icons/purple_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:magenta_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Magenta Shulker Box",
            "icon_path": "icons/magenta_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:pink_shulker_box": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Pink Shulker Box",
            "icon_path": "icons/pink_shulker_box.png",
            "identifier": "minecraft:shulker_box"
        },
        "minecraft:armor_stand": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Armor Stand",
            "icon_path": "icons/armor_stand.png",
            "identifier": "minecraft:armor_stand"
        },
        "minecraft:note_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Note Block",
            "icon_path": "icons/note_block.png",
            "identifier": "minecraft:noteblock"
        },
        "minecraft:jukebox": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jukebox",
            "icon_path": "icons/jukebox.png",
            "identifier": "minecraft:jukebox"
        },
        "minecraft:music_disc_13": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "13 Disc",
            "icon_path": "icons/music_disc_13.png",
            "identifier": "minecraft:music_disc_13"
        },
        "minecraft:music_disc_cat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cat Disc",
            "icon_path": "icons/music_disc_cat.png",
            "identifier": "minecraft:music_disc_cat"
        },
        "minecraft:music_disc_blocks": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blocks Disc",
            "icon_path": "icons/music_disc_blocks.png",
            "identifier": "minecraft:music_disc_blocks"
        },
        "minecraft:music_disc_chirp": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chirp Disc",
            "icon_path": "icons/music_disc_chirp.png",
            "identifier": "minecraft:music_disc_chirp"
        },
        "minecraft:music_disc_far": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Far Disc",
            "icon_path": "icons/music_disc_far.png",
            "identifier": "minecraft:music_disc_far"
        },
        "minecraft:music_disc_mall": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mall Disc",
            "icon_path": "icons/music_disc_mall.png",
            "identifier": "minecraft:music_disc_mall"
        },
        "minecraft:music_disc_mellohi": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mellohi Disc",
            "icon_path": "icons/music_disc_mellohi.png",
            "identifier": "minecraft:music_disc_mellohi"
        },
        "minecraft:music_disc_stal": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stal Disc",
            "icon_path": "icons/music_disc_stal.png",
            "identifier": "minecraft:music_disc_stal"
        },
        "minecraft:music_disc_strad": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Strad Disc",
            "icon_path": "icons/music_disc_strad.png",
            "identifier": "minecraft:music_disc_strad"
        },
        "minecraft:music_disc_ward": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ward Disc",
            "icon_path": "icons/music_disc_ward.png",
            "identifier": "minecraft:music_disc_ward"
        },
        "minecraft:music_disc_11": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "11 Disc",
            "icon_path": "icons/music_disc_11.png",
            "identifier": "minecraft:music_disc_11"
        },
        "minecraft:music_disc_wait": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wait Disc",
            "icon_path": "icons/music_disc_wait.png",
            "identifier": "minecraft:music_disc_wait"
        },
        "minecraft:music_disc_otherside": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Otherside Disc",
            "icon_path": "icons/music_disc_otherside.png",
            "identifier": "minecraft:music_disc_otherside"
        },
        "minecraft:music_disc_5": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "5 Disc",
            "icon_path": "icons/music_disc_5.png",
            "identifier": "minecraft:music_disc_5"
        },
        "minecraft:music_disc_pigstep": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pigstep Disc",
            "icon_path": "icons/music_disc_pigstep.png",
            "identifier": "minecraft:music_disc_pigstep"
        },
        "minecraft:disc_fragment_5": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Disc Fragment 5",
            "icon_path": "icons/disc_fragment_5.png",
            "identifier": "minecraft:disc_fragment_5"
        },
        "minecraft:glowstone_dust": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Glowstone Dust",
            "icon_path": "icons/glowstone_dust.png",
            "identifier": "minecraft:glowstone_dust"
        },
        "minecraft:glowstone": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Glowstone",
            "icon_path": "icons/glowstone.png",
            "identifier": "minecraft:glowstone"
        },
        "minecraft:redstone_lamp": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Redstone Lamp",
            "icon_path": "icons/redstone_lamp.png",
            "identifier": "minecraft:redstone_lamp"
        },
        "minecraft:sea_lantern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Sea Lantern",
            "icon_path": "icons/sea_lantern.png",
            "identifier": "minecraft:sea_lantern"
        },
        "minecraft:oak_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Sign",
            "icon_path": "icons/oak_sign.png",
            "identifier": "minecraft:oak_sign"
        },
        "minecraft:spruce_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Sign",
            "icon_path": "icons/spruce_sign.png",
            "identifier": "minecraft:spruce_sign"
        },
        "minecraft:birch_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Sign",
            "icon_path": "icons/birch_sign.png",
            "identifier": "minecraft:birch_sign"
        },
        "minecraft:jungle_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Sign",
            "icon_path": "icons/jungle_sign.png",
            "identifier": "minecraft:jungle_sign"
        },
        "minecraft:acacia_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Sign",
            "icon_path": "icons/acacia_sign.png",
            "identifier": "minecraft:acacia_sign"
        },
        "minecraft:dark_oak_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Sign",
            "icon_path": "icons/dark_oak_sign.png",
            "identifier": "minecraft:dark_oak_sign"
        },
        "minecraft:mangrove_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Sign",
            "icon_path": "icons/mangrove_sign.png",
            "identifier": "minecraft:mangrove_sign"
        },
        "minecraft:crimson_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Sign",
            "icon_path": "icons/crimson_sign.png",
            "identifier": "minecraft:crimson_sign"
        },
        "minecraft:warped_sign": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Sign",
            "icon_path": "icons/warped_sign.png",
            "identifier": "minecraft:warped_sign"
        },
        "minecraft:painting": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Painting",
            "icon_path": "icons/painting.png",
            "identifier": "minecraft:painting"
        },
        "minecraft:item_frame": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Item Frame",
            "icon_path": "icons/item_frame.png",
            "identifier": "minecraft:frame"
        },
        "minecraft:glow_item_frame": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Glow Item Frame",
            "icon_path": "icons/glow_item_frame.png",
            "identifier": "minecraft:glow_frame"
        },
        "minecraft:honey_bottle": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Honey Bottle",
            "icon_path": "icons/honey_bottle.png",
            "identifier": "minecraft:honey_bottle"
        },
        "minecraft:flower_pot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Flower Pot",
            "icon_path": "icons/flower_pot.png",
            "identifier": "minecraft:flower_pot"
        },
        "minecraft:bowl": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bowl",
            "icon_path": "icons/bowl.png",
            "identifier": "minecraft:bowl"
        },
        "minecraft:bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bucket",
            "icon_path": "icons/bucket.png",
            "identifier": "minecraft:bucket"
        },
        "minecraft:milk_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Milk Bucket",
            "icon_path": "icons/milk_bucket.png",
            "identifier": "minecraft:milk_bucket"
        },
        "minecraft:water_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Water Bucket",
            "icon_path": "icons/water_bucket.png",
            "identifier": "minecraft:water_bucket"
        },
        "minecraft:lava_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lava Bucket",
            "icon_path": "icons/lava_bucket.png",
            "identifier": "minecraft:lava_bucket"
        },
        "minecraft:cod_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Cod Bucket",
            "icon_path": "icons/cod_bucket.png",
            "identifier": "minecraft:cod_bucket"
        },
        "minecraft:salmon_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Salmon Bucket",
            "icon_path": "icons/salmon_bucket.png",
            "identifier": "minecraft:salmon_bucket"
        },
        "minecraft:tropical_fish_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tropical Fish Bucket",
            "icon_path": "icons/tropical_fish_bucket.png",
            "identifier": "minecraft:tropical_fish_bucket"
        },
        "minecraft:pufferfish_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Pufferfish Bucket",
            "icon_path": "icons/pufferfish_bucket.png",
            "identifier": "minecraft:pufferfish_bucket"
        },
        "minecraft:powder_snow_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Powder Snow Bucket",
            "icon_path": "icons/powder_snow_bucket.png",
            "identifier": "minecraft:powder_snow_bucket"
        },
        "minecraft:axolotl_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bucket of Axolotl",
            "icon_path": "icons/axolotl_bucket.png",
            "identifier": "minecraft:axolotl_bucket"
        },
        "minecraft:tadpole_bucket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bucket of Tadpole",
            "icon_path": "icons/tadpole_bucket.png",
            "identifier": "minecraft:tadpole_bucket"
        },
        "minecraft:player_head": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Player Head",
            "icon_path": "icons/player_head.png",
            "identifier": "minecraft:skull"
        },
        "minecraft:zombie_head": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Zombie Head",
            "icon_path": "icons/zombie_head.png",
            "identifier": "minecraft:skull"
        },
        "minecraft:creeper_head": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Creeper Head",
            "icon_path": "icons/creeper_head.png",
            "identifier": "minecraft:skull"
        },
        "minecraft:dragon_head": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 5,
            "display_name": "Ender Dragon Head",
            "icon_path": "icons/dragon_head.png",
            "identifier": "minecraft:skull"
        },
        "minecraft:skeleton_skull": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Skeleton Skull",
            "icon_path": "icons/skeleton_skull.png",
            "identifier": "minecraft:skull"
        },
        "minecraft:wither_skeleton_skull": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Wither Skeleton Skull",
            "icon_path": "icons/wither_skeleton_skull.png",
            "identifier": "minecraft:skull"
        },
        "minecraft:beacon": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Beacon",
            "icon_path": "icons/beacon.png",
            "identifier": "minecraft:beacon"
        },
        "minecraft:bell": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bell",
            "icon_path": "icons/bell.png",
            "identifier": "minecraft:bell"
        },
        "minecraft:conduit": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Conduit",
            "icon_path": "icons/conduit.png",
            "identifier": "minecraft:conduit"
        },
        "minecraft:stonecutter": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stonecutter",
            "icon_path": "icons/stonecutter.png",
            "identifier": "minecraft:stonecutter_block"
        },
        "minecraft:end_portal_frame": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Portal Frame",
            "icon_path": "icons/end_portal_frame.png",
            "identifier": "minecraft:end_portal_frame"
        },
        "minecraft:coal": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Coal",
            "icon_path": "icons/coal.png",
            "identifier": "minecraft:coal"
        },
        "minecraft:charcoal": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Charcoal",
            "icon_path": "icons/charcoal.png",
            "identifier": "minecraft:charcoal"
        },
        "minecraft:diamond": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Diamond",
            "icon_path": "icons/diamond.png",
            "identifier": "minecraft:diamond"
        },
        "minecraft:iron_nugget": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Nugget",
            "icon_path": "icons/iron_nugget.png",
            "identifier": "minecraft:iron_nugget"
        },
        "minecraft:raw_iron": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Iron",
            "icon_path": "icons/raw_iron.png",
            "identifier": "minecraft:raw_iron"
        },
        "minecraft:raw_gold": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Gold",
            "icon_path": "icons/raw_gold.png",
            "identifier": "minecraft:raw_gold"
        },
        "minecraft:raw_copper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Raw Copper",
            "icon_path": "icons/raw_copper.png",
            "identifier": "minecraft:raw_copper"
        },
        "minecraft:copper_ingot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Copper Ingot",
            "icon_path": "icons/copper_ingot.png",
            "identifier": "minecraft:copper_ingot"
        },
        "minecraft:iron_ingot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Iron Ingot",
            "icon_path": "icons/iron_ingot.png",
            "identifier": "minecraft:iron_ingot"
        },
        "minecraft:netherite_scrap": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Scrap",
            "icon_path": "icons/netherite_scrap.png",
            "identifier": "minecraft:netherite_scrap"
        },
        "minecraft:netherite_ingot": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Netherite Ingot",
            "icon_path": "icons/netherite_ingot.png",
            "identifier": "minecraft:netherite_ingot"
        },
        "minecraft:gold_nugget": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gold Nugget",
            "icon_path": "icons/gold_nugget.png",
            "identifier": "minecraft:gold_nugget"
        },
        "minecraft:gold_ingot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gold Ingot",
            "icon_path": "icons/gold_ingot.png",
            "identifier": "minecraft:gold_ingot"
        },
        "minecraft:emerald": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Emerald",
            "icon_path": "icons/emerald.png",
            "identifier": "minecraft:emerald"
        },
        "minecraft:quartz": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Quartz",
            "icon_path": "icons/quartz.png",
            "identifier": "minecraft:quartz"
        },
        "minecraft:clay_ball": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Clay",
            "icon_path": "icons/clay_ball.png",
            "identifier": "minecraft:clay_ball"
        },
        "minecraft:brick": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Brick",
            "icon_path": "icons/brick.png",
            "identifier": "minecraft:brick"
        },
        "minecraft:netherbrick": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Brick",
            "icon_path": "icons/netherbrick.png",
            "identifier": "minecraft:netherbrick"
        },
        "minecraft:prismarine_shard": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Prismarine Shard",
            "icon_path": "icons/prismarine_shard.png",
            "identifier": "minecraft:prismarine_shard"
        },
        "minecraft:amethyst_shard": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Amethyst Shard",
            "icon_path": "icons/amethyst_shard.png",
            "identifier": "minecraft:amethyst_shard"
        },
        "minecraft:prismarine_crystals": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Prismarine Crystals",
            "icon_path": "icons/prismarine_crystals.png",
            "identifier": "minecraft:prismarine_crystals"
        },
        "minecraft:nautilus_shell": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Nautilus Shell",
            "icon_path": "icons/nautilus_shell.png",
            "identifier": "minecraft:nautilus_shell"
        },
        "minecraft:heart_of_the_sea": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Heart of the Sea",
            "icon_path": "icons/heart_of_the_sea.png",
            "identifier": "minecraft:heart_of_the_sea"
        },
        "minecraft:scute": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Scute",
            "icon_path": "icons/scute.png",
            "identifier": "minecraft:scute"
        },
        "minecraft:phantom_membrane": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Phantom Membrane",
            "icon_path": "icons/phantom_membrane.png",
            "identifier": "minecraft:phantom_membrane"
        },
        "minecraft:string": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "String",
            "icon_path": "icons/string.png",
            "identifier": "minecraft:string"
        },
        "minecraft:feather": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Feather",
            "icon_path": "icons/feather.png",
            "identifier": "minecraft:feather"
        },
        "minecraft:flint": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Flint",
            "icon_path": "icons/flint.png",
            "identifier": "minecraft:flint"
        },
        "minecraft:gunpowder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Gunpowder",
            "icon_path": "icons/gunpowder.png",
            "identifier": "minecraft:gunpowder"
        },
        "minecraft:leather": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Leather",
            "icon_path": "icons/leather.png",
            "identifier": "minecraft:leather"
        },
        "minecraft:rabbit_hide": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rabbit Hide",
            "icon_path": "icons/rabbit_hide.png",
            "identifier": "minecraft:rabbit_hide"
        },
        "minecraft:rabbit_foot": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rabbit's Foot",
            "icon_path": "icons/rabbit_foot.png",
            "identifier": "minecraft:rabbit_foot"
        },
        "minecraft:fire_charge": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Fire Charge",
            "icon_path": "icons/fire_charge.png",
            "identifier": "minecraft:fire_charge"
        },
        "minecraft:blaze_rod": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blaze Rod",
            "icon_path": "icons/blaze_rod.png",
            "identifier": "minecraft:blaze_rod"
        },
        "minecraft:blaze_powder": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Blaze Powder",
            "icon_path": "icons/blaze_powder.png",
            "identifier": "minecraft:blaze_powder"
        },
        "minecraft:magma_cream": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Magma Cream",
            "icon_path": "icons/magma_cream.png",
            "identifier": "minecraft:magma_cream"
        },
        "minecraft:fermented_spider_eye": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Fermented Spider Eye",
            "icon_path": "icons/fermented_spider_eye.png",
            "identifier": "minecraft:fermented_spider_eye"
        },
        "minecraft:echo_shard": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Echo Shard",
            "icon_path": "icons/echo_shard.png",
            "identifier": "minecraft:echo_shard"
        },
        "minecraft:dragon_breath": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Dragon's Breath",
            "icon_path": "icons/dragon_breath.png",
            "identifier": "minecraft:dragon_breath"
        },
        "minecraft:shulker_shell": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Shulker Shell",
            "icon_path": "icons/shulker_shell.png",
            "identifier": "minecraft:shulker_shell"
        },
        "minecraft:ghast_tear": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Ghast Tear",
            "icon_path": "icons/ghast_tear.png",
            "identifier": "minecraft:ghast_tear"
        },
        "minecraft:slime_ball": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Slimeball",
            "icon_path": "icons/slime_ball.png",
            "identifier": "minecraft:slime_ball"
        },
        "minecraft:ender_pearl": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Ender Pearl",
            "icon_path": "icons/ender_pearl.png",
            "identifier": "minecraft:ender_pearl"
        },
        "minecraft:ender_eye": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "Eye of Ender",
            "icon_path": "icons/ender_eye.png",
            "identifier": "minecraft:ender_eye"
        },
        "minecraft:nether_star": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Star",
            "icon_path": "icons/nether_star.png",
            "identifier": "minecraft:nether_star"
        },
        "minecraft:end_rod": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Rod",
            "icon_path": "icons/end_rod.png",
            "identifier": "minecraft:end_rod"
        },
        "minecraft:lightning_rod": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lightning Rod",
            "icon_path": "icons/lightning_rod.png",
            "identifier": "minecraft:lightning_rod"
        },
        "minecraft:end_crystal": {
            "creative": False,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Crystal",
            "icon_path": "icons/end_crystal.png",
            "identifier": "minecraft:end_crystal"
        },
        "minecraft:paper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Paper",
            "icon_path": "icons/paper.png",
            "identifier": "minecraft:paper"
        },
        "minecraft:book": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Book",
            "icon_path": "icons/book.png",
            "identifier": "minecraft:book"
        },
        "minecraft:writable_book": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Book and Quill",
            "icon_path": "icons/writable_book.png",
            "identifier": "minecraft:writable_book"
        },
        "minecraft:enchanted_book": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Enchanted Book",
            "icon_path": "icons/enchanted_book.png",
            "identifier": "minecraft:enchanted_book"
        },
        # Boats
        "minecraft:oak_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Boat",
            "icon_path": "icons/oak_boat.png",
            "identifier": "minecraft:oak_boat"
        },
        "minecraft:spruce_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Boat",
            "icon_path": "icons/spruce_boat.png",
            "identifier": "minecraft:spruce_boat"
        },
        "minecraft:birch_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Boat",
            "icon_path": "icons/birch_boat.png",
            "identifier": "minecraft:birch_boat"
        },
        "minecraft:jungle_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Boat",
            "icon_path": "icons/jungle_boat.png",
            "identifier": "minecraft:jungle_boat"
        },
        "minecraft:acacia_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Boat",
            "icon_path": "icons/acacia_boat.png",
            "identifier": "minecraft:acacia_boat"
        },
        "minecraft:dark_oak_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Boat",
            "icon_path": "icons/dark_oak_boat.png",
            "identifier": "minecraft:dark_oak_boat"
        },
        "minecraft:mangrove_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Boat",
            "icon_path": "icons/mangrove_boat.png",
            "identifier": "minecraft:mangrove_boat"
        },
        "minecraft:oak_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Boat with Chest",
            "icon_path": "icons/oak_chest_boat.png",
            "identifier": "minecraft:oak_chest_boat"
        },
        "minecraft:spruce_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Boat with Chest",
            "icon_path": "icons/spruce_chest_boat.png",
            "identifier": "minecraft:spruce_chest_boat"
        },
        "minecraft:birch_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Boat with Chest",
            "icon_path": "icons/birch_chest_boat.png",
            "identifier": "minecraft:birch_chest_boat"
        },
        "minecraft:jungle_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Boat with Chest",
            "icon_path": "icons/jungle_chest_boat.png",
            "identifier": "minecraft:jungle_chest_boat"
        },
        "minecraft:acacia_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Boat with Chest",
            "icon_path": "icons/acacia_chest_boat.png",
            "identifier": "minecraft:acacia_chest_boat"
        },
        "minecraft:dark_oak_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Boat with Chest",
            "icon_path": "icons/dark_oak_chest_boat.png",
            "identifier": "minecraft:dark_oak_chest_boat"
        },
        "minecraft:mangrove_chest_boat": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Boat with Chest",
            "icon_path": "icons/mangrove_chest_boat.png",
            "identifier": "minecraft:mangrove_chest_boat"
        },
        "minecraft:rail": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Rail",
            "icon_path": "icons/rail.png",
            "identifier": "minecraft:rail"
        },
        "minecraft:powered_rail": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Powered Rail",
            "icon_path": "icons/powered_rail.png",
            "identifier": "minecraft:golden_rail"
        },
        "minecraft:detector_rail": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Detector Rail",
            "icon_path": "icons/detector_rail.png",
            "identifier": "minecraft:detector_rail"
        },
        "minecraft:activator_rail": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Activator Rail",
            "icon_path": "icons/activator_rail.png",
            "identifier": "minecraft:activator_rail"
        },
        "minecraft:minecart": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Minecart",
            "icon_path": "icons/minecart.png",
            "identifier": "minecraft:minecart"
        },
        "minecraft:chest_minecart": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Minecart with Chest",
            "icon_path": "icons/chest_minecart.png",
            "identifier": "minecraft:chest_minecart"
        },
        "minecraft:hopper_minecart": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Minecart with Hopper",
            "icon_path": "icons/hopper_minecart.png",
            "identifier": "minecraft:hopper_minecart"
        },
        "minecraft:tnt_minecart": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Minecart with TNT",
            "icon_path": "icons/tnt_minecart.png",
            "identifier": "minecraft:tnt_minecart"
        },
        "minecraft:redstone_block": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Redstone Block",
            "icon_path": "icons/redstone_block.png",
            "identifier": "minecraft:redstone_block"
        },
        "minecraft:redstone_torch": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Redstone Torch",
            "icon_path": "icons/redstone_torch.png",
            "identifier": "minecraft:redstone_torch"
        },
        "minecraft:lever": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Lever",
            "icon_path": "icons/lever.png",
            "identifier": "minecraft:lever"
        },
        "minecraft:oak_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Wooden Button",
            "icon_path": "icons/oak_button.png",
            "identifier": "minecraft:wooden_button"
        },
        "minecraft:spruce_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Button",
            "icon_path": "icons/spruce_button.png",
            "identifier": "minecraft:spruce_button"
        },
        "minecraft:birch_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Button",
            "icon_path": "icons/birch_button.png",
            "identifier": "minecraft:birch_button"
        },
        "minecraft:jungle_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Button",
            "icon_path": "icons/jungle_button.png",
            "identifier": "minecraft:jungle_button"
        },
        "minecraft:acacia_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Button",
            "icon_path": "icons/acacia_button.png",
            "identifier": "minecraft:acacia_button"
        },
        "minecraft:dark_oak_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Button",
            "icon_path": "icons/dark_oak_button.png",
            "identifier": "minecraft:dark_oak_button"
        },
        "minecraft:mangrove_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Button",
            "icon_path": "icons/mangrove_button.png",
            "identifier": "minecraft:mangrove_button"
        },
        "minecraft:stone_button": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Button",
            "icon_path": "icons/stone_button.png",
            "identifier": "minecraft:stone_button"
        },
        "minecraft:crimson_button": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Button",
            "icon_path": "icons/crimson_button.png",
            "identifier": "minecraft:crimson_button"
        },
        "minecraft:warped_button": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Button",
            "icon_path": "icons/warped_button.png",
            "identifier": "minecraft:warped_button"
        },
        "minecraft:polished_blackstone_button": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Button",
            "icon_path": "icons/polished_blackstone_button.png",
            "identifier": "minecraft:polished_blackstone_button"
        },
        "minecraft:tripwire_hook": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Tripwire Hook",
            "icon_path": "icons/tripwire_hook.png",
            "identifier": "minecraft:tripwire_hook"
        },
        "minecraft:oak_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Oak Pressure Plate",
            "icon_path": "icons/oak_pressure_plate.png",
            "identifier": "minecraft:wooden_pressure_plate"
        },
        "minecraft:spruce_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Spruce Pressure Plate",
            "icon_path": "icons/spruce_pressure_plate.png",
            "identifier": "minecraft:spruce_pressure_plate"
        },
        "minecraft:birch_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Birch Pressure Plate",
            "icon_path": "icons/birch_pressure_plate.png",
            "identifier": "minecraft:birch_pressure_plate"
        },
        "minecraft:jungle_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jungle Pressure Plate",
            "icon_path": "icons/jungle_pressure_plate.png",
            "identifier": "minecraft:jungle_pressure_plate"
        },
        "minecraft:acacia_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Acacia Pressure Plate",
            "icon_path": "icons/acacia_pressure_plate.png",
            "identifier": "minecraft:acacia_pressure_plate"
        },
        "minecraft:dark_oak_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Dark Oak Pressure Plate",
            "icon_path": "icons/dark_oak_pressure_plate.png",
            "identifier": "minecraft:dark_oak_pressure_plate"
        },
        "minecraft:mangrove_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Mangrove Pressure Plate",
            "icon_path": "icons/mangrove_pressure_plate.png",
            "identifier": "minecraft:mangrove_pressure_plate"
        },
        "minecraft:crimson_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Crimson Pressure Plate",
            "icon_path": "icons/crimson_pressure_plate.png",
            "identifier": "minecraft:crimson_pressure_plate"
        },
        "minecraft:warped_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Warped Pressure Plate",
            "icon_path": "icons/warped_pressure_plate.png",
            "identifier": "minecraft:warped_pressure_plate"
        },
        "minecraft:stone_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Stone Pressure Plate",
            "icon_path": "icons/stone_pressure_plate.png",
            "identifier": "minecraft:stone_pressure_plate"
        },
        "minecraft:light_weighted_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light Weighted Pressure Plate",
            "icon_path": "icons/light_weighted_pressure_plate.png",
            "identifier": "minecraft:light_weighted_pressure_plate"
        },
        "minecraft:heavy_weighted_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Heavy Weighted Pressure Plate",
            "icon_path": "icons/heavy_weighted_pressure_plate.png",
            "identifier": "minecraft:heavy_weighted_pressure_plate"
        },
        "minecraft:polished_blackstone_pressure_plate": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Polished Blackstone Pressure Plate",
            "icon_path": "icons/polished_blackstone_pressure_plate.png",
            "identifier": "minecraft:polished_blackstone_pressure_plate"
        },
        "minecraft:observer": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Observer",
            "icon_path": "icons/observer.png",
            "identifier": "minecraft:observer"
        },
        "minecraft:daylight_detector": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Daylight Sensor",
            "icon_path": "icons/daylight_detector.png",
            "identifier": "minecraft:daylight_detector"
        },
        "minecraft:repeater": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Redstone Repeater",
            "icon_path": "icons/repeater.png",
            "identifier": "minecraft:repeater"
        },
        "minecraft:comparator": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Redstone Comparator",
            "icon_path": "icons/comparator.png",
            "identifier": "minecraft:comparator"
        },
        "minecraft:hopper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Hopper",
            "icon_path": "icons/hopper.png",
            "identifier": "minecraft:hopper"
        },
        "minecraft:dropper": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Dropper",
            "icon_path": "icons/dropper.png",
            "identifier": "minecraft:dropper"
        },
        "minecraft:dispenser": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Dispenser",
            "icon_path": "icons/dispenser.png",
            "identifier": "minecraft:dispenser"
        },
        "minecraft:piston": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Piston",
            "icon_path": "icons/piston.png",
            "identifier": "minecraft:piston"
        },
        "minecraft:sticky_piston": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Sticky Piston",
            "icon_path": "icons/sticky_piston.png",
            "identifier": "minecraft:sticky_piston"
        },
        "minecraft:tnt": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "TNT",
            "icon_path": "icons/tnt.png",
            "identifier": "minecraft:tnt"
        },
        "minecraft:name_tag": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Name Tag",
            "icon_path": "icons/name_tag.png",
            "identifier": "minecraft:name_tag"
        },
        "minecraft:loom": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Loom",
            "icon_path": "icons/loom.png",
            "identifier": "minecraft:loom"
        },
        "minecraft:black_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Black Banner",
            "icon_path": "icons/black_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:gray_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 8,
            "display_name": "Gray Banner",
            "icon_path": "icons/gray_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:light_gray_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 7,
            "display_name": "Light Gray Banner",
            "icon_path": "icons/light_gray_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:white_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "White Banner",
            "icon_path": "icons/white_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:light_blue_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 12,
            "display_name": "Light Blue Banner",
            "icon_path": "icons/light_blue_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:orange_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 14,
            "display_name": "Orange Banner",
            "icon_path": "icons/orange_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:red_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 1,
            "display_name": "Red Banner",
            "icon_path": "icons/red_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:blue_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 4,
            "display_name": "Blue Banner",
            "icon_path": "icons/blue_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:purple_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 5,
            "display_name": "Purple Banner",
            "icon_path": "icons/purple_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:magenta_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 13,
            "display_name": "Magenta Banner",
            "icon_path": "icons/magenta_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:pink_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 9,
            "display_name": "Pink Banner",
            "icon_path": "icons/pink_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:brown_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 3,
            "display_name": "Brown Banner",
            "icon_path": "icons/brown_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:yellow_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 11,
            "display_name": "Yellow Banner",
            "icon_path": "icons/yellow_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:lime_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 10,
            "display_name": "Lime Banner",
            "icon_path": "icons/lime_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:green_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 2,
            "display_name": "Green Banner",
            "icon_path": "icons/green_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:cyan_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 6,
            "display_name": "Cyan Banner",
            "icon_path": "icons/cyan_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:illager_banner": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 15,
            "display_name": "Illager Banner (Unobtainable w/o NBT Edit)",
            "icon_path": "icons/illager_banner.png",
            "identifier": "minecraft:banner"
        },
        "minecraft:bordure_indented_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Bordure Indented Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:bordure_indented_banner_pattern"
        },
        "minecraft:creeper_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Creeper Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:creeper_banner_pattern"
        },
        "minecraft:field_masoned_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Field Masoned Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:field_masoned_banner_pattern"
        },
        "minecraft:flower_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Flower Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:flower_banner_pattern"
        },
        "minecraft:globe_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Globe Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:banner_pattern"
        },
        "minecraft:mojang_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Thing Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:mojang_banner_pattern"
        },
        "minecraft:piglin_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Piglin Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:piglin_banner_pattern"
        },
        "minecraft:skull_banner_pattern": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Skull Banner Pattern",
            "icon_path": "icons/banner_pattern.png",
            "identifier": "minecraft:skull_banner_pattern"
        },
        "minecraft:firework_rocket": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Firework Rocket",
            "icon_path": "icons/firework_rocket.png",
            "identifier": "minecraft:firework_rocket"
        },
        "minecraft:firework_star": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Firework Star",
            "icon_path": "icons/firework_star.png",
            "identifier": "minecraft:firework_star"
        },
        "minecraft:chain": {
            "creative": False,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Chain",
            "icon_path": "icons/chain.png",
            "identifier": "minecraft:chain"
        },
        "minecraft:target": {
            "creative": False,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Target",
            "icon_path": "icons/target.png",
            "identifier": "minecraft:target"
        },
        # creative
        "minecraft:air": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Air",
            "icon_path": "icons/air.png",
            "identifier": "minecraft:air"
        },
        "minecraft:allow": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Allow",
            "icon_path": "icons/allow.png",
            "identifier": "minecraft:allow"
        },
        "minecraft:barrier": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Barrier",
            "icon_path": "icons/barrier.png",
            "identifier": "minecraft:barrier"
        },
        "minecraft:command_block": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Command Block",
            "icon_path": "icons/command_block.png",
            "identifier": "minecraft:command_block"
        },
        "minecraft:chain_command_block": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Chain Command Block",
            "icon_path": "icons/chain_command_block.png",
            "identifier": "minecraft:chain_command_block"
        },
        "minecraft:repeating_command_block": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Repeating Command Block",
            "icon_path": "icons/repeating_command_block.png",
            "identifier": "minecraft:repeating_command_block"
        },
        "minecraft:command_block_minecart": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Minecart with Command Block",
            "icon_path": "icons/command_block_minecart.png",
            "identifier": "minecraft:command_block_minecart"
        },
        "minecraft:structure_block": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Structure Block",
            "icon_path": "icons/structure_block.png",
            "identifier": "minecraft:structure_block"
        },
        "minecraft:structure_void": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Structure Void",
            "icon_path": "icons/structure_void.png",
            "identifier": "minecraft:structure_void"
        },
        "minecraft:jigsaw": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Jigsaw Block",
            "icon_path": "icons/jigsaw.png",
            "identifier": "minecraft:jigsaw"
        },
        "minecraft:light": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Light",
            "icon_path": "icons/light.png",
            "identifier": "minecraft:light_block"
        },
        "minecraft:suspicious_stew": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Suspicious Stew",
            "icon_path": "icons/suspicious_stew.png",
            "identifier": "minecraft:suspicious_stew"
        },
        "minecraft:filled_map": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Map",
            "icon_path": "icons/filled_map.png",
            "identifier": "minecraft:filled_map"
        },
        "minecraft:frosted_ice": {
            "creative": True,
            "experimental": False,
            "dimension": "overworld",
            "data": 0,
            "display_name": "Frosted Ice",
            "icon_path": "icons/frosted_ice.png",
            "identifier": "minecraft:frosted_ice"
        },
        "minecraft:portal": {
            "creative": True,
            "experimental": False,
            "dimension": "nether",
            "data": 0,
            "display_name": "Nether Portal (Unobtainable w/o NBT Edit)",
            "icon_path": "icons/portal.png",
            "identifier": "minecraft:portal"
        },
        "minecraft:end_portal": {
            "creative": True,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Portal (Unobtainable w/o NBT Edit)",
            "icon_path": "icons/end_portal.png",
            "identifier": "minecraft:end_portal"
        },
        "minecraft:end_gateway": {
            "creative": True,
            "experimental": False,
            "dimension": "end",
            "data": 0,
            "display_name": "End Gateway (Unobtainable w/o NBT Edit)",
            "icon_path": "icons/end_gateway.png",
            "identifier": "minecraft:end_gateway"
        }
    }
        # 1.19.50.21
        #Updated on 21-10-2022
        _list.update({
            # Wood
            "minecraft:bamboo_planks": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Planks",
                "icon_path": "icons/bamboo_planks.png",
                "identifier": "minecraft:bamboo_planks"
            },
            "minecraft:bamboo_mosaic": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Mosaic",
                "icon_path": "icons/bamboo_mosaic.png",
                "identifier": "minecraft:bamboo_mosaic"
            },
            "minecraft:bamboo_fence": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Fence",
                "icon_path": "icons/bamboo_fence.png",
                "identifier": "minecraft:bamboo_fence"
            },
            "minecraft:bamboo_fence_gate": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Fence Gate",
                "icon_path": "icons/bamboo_fence_gate.png",
                "identifier": "minecraft:bamboo_fence_gate"
            },
            "minecraft:bamboo_stairs": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Stairs",
                "icon_path": "icons/bamboo_stairs.png",
                "identifier": "minecraft:bamboo_stairs"
            },
            "minecraft:bamboo_door": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Door",
                "icon_path": "icons/bamboo_door.png",
                "identifier": "minecraft:bamboo_door"
            },
            "minecraft:bamboo_trapdoor": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Trapdoor",
                "icon_path": "icons/bamboo_trapdoor.png",
                "identifier": "minecraft:bamboo_trapdoor"
            },
            "minecraft:bamboo_slab": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Slab",
                "icon_path": "icons/bamboo_slab.png",
                "identifier": "minecraft:bamboo_slab"
            },
            "minecraft:bamboo_mosaic_slab": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Mosaic Slab",
                "icon_path": "icons/bamboo_mosaic_slab.png",
                "identifier": "minecraft:bamboo_mosaic_slab"
            },
            "minecraft:bamboo_mosaic_stairs": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Mosaic Stairs",
                "icon_path": "icons/bamboo_mosaic_stairs.png",
                "identifier": "minecraft:bamboo_mosaic_stairs"
            },
            "minecraft:bamboo_boat": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Boat",
                "icon_path": "icons/bamboo_boat.png",
                "identifier": "minecraft:bamboo_boat"
            },
            "minecraft:bamboo_chest_boat": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Chest Boat",
                "icon_path": "icons/bamboo_chest_boat.png",
                "identifier": "minecraft:bamboo_chest_boat"
            },
            "minecraft:bamboo_button": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Button",
                "icon_path": "icons/bamboo_button.png",
                "identifier": "minecraft:bamboo_button"
            },
            "minecraft:bamboo_pressure_plate": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Pressure Plate",
                "icon_path": "icons/bamboo_pressure_plate.png",
                "identifier": "minecraft:bamboo_pressure_plate"
            },
            "minecraft:bamboo_sign": {
                "creative": False,
                "experimental": True,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Sign",
                "icon_path": "icons/bamboo_sign.png",
                "identifier": "minecraft:bamboo_sign"
            },
            # Spawn Egg
            "minecraft:camel_spawn_egg": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Camel Spawn Egg",
                "icon_path": "icons/camel_spawn_egg.png",
                "identifier": "minecraft:camel_spawn_egg"
            },
            # Bookshelf
            "minecraft:chiseled_bookshelf": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Chiseled Bookshelf",
                "icon_path": "icons/chiseled_bookshelf.png",
                "identifier": "minecraft:chiseled_bookshelf"
            },
            # Hanging Signs
            "minecraft:bamboo_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Hanging Sign",
                "icon_path": "icons/bamboo_hanging_sign.png",
                "identifier": "minecraft:bamboo_hanging_sign"
            },
            "minecraft:mangrove_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Mangrove Hanging Sign",
                "icon_path": "icons/mangrove_hanging_sign.png",
                "identifier": "minecraft:mangrove_hanging_sign"
            },
            "minecraft:warped_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Bamboo Hanging Sign",
                "icon_path": "icons/warped_hanging_sign.png",
                "identifier": "minecraft:warped_hanging_sign"
            },
            "minecraft:crimson_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Crimson Hanging Sign",
                "icon_path": "icons/crimson_hanging_sign.png",
                "identifier": "minecraft:crimson_hanging_sign"
            },
            "minecraft:dark_oak_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Dark Oak Hanging Sign",
                "icon_path": "icons/dark_oak_hanging_sign.png",
                "identifier": "minecraft:dark_oak_hanging_sign"
            },
            "minecraft:acacia_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Acasia Hanging Sign",
                "icon_path": "icons/acacia_hanging_sign.png",
                "identifier": "minecraft:acacia_hanging_sign"
            },
            "minecraft:jungle_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Jungle Hanging Sign",
                "icon_path": "icons/jungle_hanging_sign.png",
                "identifier": "minecraft:jungle_hanging_sign"
            },
            "minecraft:birch_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Birch Hanging Sign",
                "icon_path": "icons/birch_hanging_sign.png",
                "identifier": "minecraft:birch_hanging_sign"
            },
            "minecraft:spruce_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Spruce Hanging Sign",
                "icon_path": "icons/spruce_hanging_sign.png",
                "identifier": "minecraft:spruce_hanging_sign"
            },
            "minecraft:oak_hanging_sign": {
                "creative": True,
                "experimental": False,
                "dimension": "overworld",
                "data": 0,
                "display_name": "Oak Hanging Sign",
                "icon_path": "icons/oak_hanging_sign.png",
                "identifier": "minecraft:oak_hanging_sign"
            }
        })

class SoundCategory():
    list = ['ambient', 'block', 'player', 'neutral', 'hostile', 'music', 'record', 'ui']
    
    Ambient = 'ambient'
    Block = 'block'
    Player = 'player'
    Neutral = 'neutral'
    Hostile = 'hostile'
    Music = 'music'
    Record = 'record'
    UI = 'ui'
class MusicCategory():
    list = ['creative', 'credits', 'crimson_forest', 'dripstone_caves', 'end', 'endboss', 'frozen_peaks', 'game', 'grove', 'hell', 'jagged_peaks', 'lush_caves', 'meadow', 'menu', 'nether', 'snowy_slopes', 'soulsand_valley', 'stony_peaks', 'water' ]
    Creative = 'creative'
    Credits = 'credits'
    Crimson_forest = 'crimson_forest'
    Dripstone_caves = 'dripstone_caves'
    End = 'end'
    Endboss = 'endboss'
    Frozen_peaks = 'frozen_peaks'
    Game = 'game'
    Grove = 'grove'
    Hell = 'hell'
    Jagged_peaks = 'jagged_peaks'
    Lush_caves = 'lush_caves'
    Meadow = 'meadow'
    Menu = 'menu'
    Nether = 'nether'
    Snowy_slopes = 'snowy_slopes'
    Soulsand_valley = 'soulsand_valley'
    Stony_peaks = 'stony_peaks'
    Water = 'water'
class DamageCause():
    list = ['all', 'anvil', 'attack', 'block_explosion', 'contact', 'drowning', 'entity_explosion', 'fall', 'falling_block', 'fatal', 'fire', 'fire_tick', 'fly_into_wall', 'lava', 'magic', 'none', 'override', 'piston', 'projectile', 'sonic_boom', 'stalactite', 'stalagmite', 'starve', 'suffocation', 'suicide', 'thorns', 'void', 'wither',]
    All = 'all'
    Anvil = 'anvil'
    Attack = 'attack'
    Block_explosion = 'block_explosion'
    Contact = 'contact'
    Drowning = 'drowning'
    Entity_explosion = 'entity_explosion'
    Fall = 'fall'
    Falling_block = 'falling_block'
    Fatal = 'fatal'
    Fire = 'fire'
    Fire_tick = 'fire_tick'
    Fly_into_wall = 'fly_into_wall'
    Lava = 'lava'
    Magic = 'magic'
    Nothing = 'none'
    Override = 'override'
    Piston = 'piston'
    Projectile = 'projectile'
    Sonic_boom = 'sonic_boom'
    Stalactite = 'stalactite'
    Stalagmite = 'stalagmite'
    Starve = 'starve'
    Suffocation = 'suffocation'
    Suicide = 'suicide'
    Thorns = 'thorns'
    Void = 'void'
    Wither = 'wither'
class Target():
    list = ['block', 'damager', 'other', 'parent', 'player', 'self', 'target']
    Block = 'block'
    Damager = 'damager'
    Other = 'other'
    Parent = 'parent'
    Player = 'player'
    Self = 'self'
    Target = 'target'  

def Schemes(type, *args):
    MANIFEST_BUILD = [1, 18, 0]
    ENTITY_SERVER_VERSION = '1.16.0'
    ENTITY_CLIENT_VERSION = '1.10.0'
    BP_ANIMATION_VERSION = '1.10.0'
    ANIMATION_CONTROLLERS_VERSION = '1.10.0'
    SPAWN_RULES_VERSION = '1.8.0'
    GEOMETRY_VERSION = '1.12.0'
    RENDER_CONTROLLER_VERSION = '1.10.0'
    SOUND_DEFINITIONS_VERSION = '1.14.0'
    match type:
        case 'structure':
            return {
                args[0]: {
                    "behavior_packs": {},
                    "resource_packs": {},
                    "assets": {
                        "skins":{},
                        "animations": {},
                        "models": {
                            "entity":{},
                            'attachables':{}
                        },
                        "particles": {},
                        "sounds": {},
                        "structures": {},
                        "marketing":{},
                        "textures": {
                            "attachables":{},
                            "blocks": {},
                            "items": {},
                            "entity": {},
                            'ui':{},
                            'particle':{}
                        },
                        "vanilla": {},
                    }
                }
            }
        case 'script':
            return \
                'from anvil import *\n\n\n\n'\
                'if __name__ == "__main__":\n\n\n'\
                f'    ANVIL.compile\n'\
                f'    #Uncomment package when you\'re ready to submit it. Pass True as the argument to clear all assets when packaging\n'\
                f'    #ANVIL.package()\n'
        case 'config':
            return {
                'COMPANY': args[1].title(),
                'NAMESPACE': args[0],
                'PROJECT_NAME': args[2],
                'DISPLAY_NAME': args[3].replace('_', ' ').replace('-', ' ').title(),
                'PROJECT_DESCRIPTION': f'{args[4].replace("_", " ").replace("-", " ").title()}',
                'VANILLA_VERSION': args[5],
                'LAST_CHECK': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'NAMESPACE_FORMAT': int(args[6]),
                'BUILD': args[7]
            }
        case 'code-workspace':
            return {
            	"folders": [
            		{
                        "name": "Assets",
            			"path": MakePath(args[0],args[1],'assets')
            		},
            		{
                        "name": "Resource Packs",
            			"path": MakePath(args[0],args[1],'resource_packs')
            		},
            		{
                        "name": "Behavior Packs",
            			"path": MakePath(args[0],args[1],'behavior_packs')
            		},
            		{
                        "name":"General",
            			"path": MakePath(args[0],args[1])
            		}
            	]
            }
        
        case 'description': 
            return {
                'description': {
                    'identifier': f'{args[0]}:{args[1]}'
            }
        }
        case 'client_description':
            return {
                'materials': {
                    'default': 'entity_alphatest'
                },
                'scripts':{
                    'pre_animation':[],
                    'initialize': [],
                    'animate':[]
                },
                'textures': {},
                'geometry': {},
                'particle_effects': {},
                'sound_effects': {},
                'render_controllers': []
            }
        case 'server_entity':
            return {
                'format_version': ENTITY_SERVER_VERSION,
                'minecraft:entity': {
                    'component_groups':{},
                    'components':{},
                    'events':{}
                }
            }
        case 'client_entity':
            return {
                'format_version': ENTITY_CLIENT_VERSION,
                'minecraft:client_entity': {}
            }
        case 'bp_animations':
            return {
                "format_version": BP_ANIMATION_VERSION,
                "animations": {}
            }     
        case 'bp_animation':
            return {
                f'animation.{args[0]}.{args[1]}.{args[2]}': {
                    'loop': args[3],
                    'timeline': {}
                }
            }
        case 'animation_controllers':
            return {
                'format_version': ANIMATION_CONTROLLERS_VERSION,
                'animation_controllers': {}
            }
        case 'animation_controller':
            return {
                f'controller.animation.{args[0]}.{args[1]}.{args[2]}': {
                    'initial_state': 'default', 'states': {}
                }
            }
        case 'animation_controller_state':
            return {
                args[0]:{
                    'on_entry':[],
                    'on_exit':[],
                    'animations':[],
                    'transitions':[],
                }
            }
        case 'geometry':
            return {
                'format_version': GEOMETRY_VERSION, 
                'minecraft:geometry': [
                    {
                        'description': {
                            'identifier': f'geometry.{args[0]}.{args[1]}'
                        }, 
                        "bones": [args[2]]
                    }
                ]
            }
        case 'render_controllers':
            return {
                'format_version': RENDER_CONTROLLER_VERSION,
                'render_controllers': {}
            }
        case 'render_controller':
            return {
                    f'controller.render.{args[0]}.{args[1]}.{args[2]}': {
                    'arrays': {
                        'textures':{},
                        'geometries': {}
                    },
                    'materials': [{'*': 'Material.default'}],
                    'geometry': {},
                    'textures': [],
                    'part_visibility': [
                        {'*': True}
                    ]
                }
            }
        case 'item_texture':
            return {
                'resource_pack_name': args[0],
                'texture_name': 'atlas.items',
                'texture_data': {}
            }
        case 'terrain_textures':
            return {
               "num_mip_levels" : 4,
               "padding" : 8,
               "resource_pack_name" : args[0],
               "texture_data" : {},
               "texture_name" : "atlas.terrain"
            }
        case 'flipbook_textures':
            return []
            
        case 'attachable':
            return {
                "format_version": ENTITY_CLIENT_VERSION,
                "minecraft:attachable": {}
            }
        
        case 'spawn_rules':
            return {
                'format_version': SPAWN_RULES_VERSION,
                'minecraft:spawn_rules': {
                    'conditions': []
                }
            }
        case 'language':
            return \
                f'pack.name={args[0]}\n'\
                f'pack.description={args[1]}\n\n'
        case 'manifest_bp':
            return {
                "format_version": 2,
                "header": {"description": "pack.description", "name": "pack.name", "uuid": str(uuid.uuid4()), "version": [1, 0, 0], "min_engine_version": MANIFEST_BUILD},
                "modules": [
                    {
                        "type": "data",
                        "uuid": str(uuid.uuid4()),
                        "version": [1, 0, 0]
                    }
                ]
            }
        case 'manifest_rp':
            return {
                "format_version": 2,
                "header": {"description": "pack.description", "name": "pack.name", "uuid": str(uuid.uuid4()), "version": [1, 0, 0], "min_engine_version": MANIFEST_BUILD},
                "modules": [
                    {
                        "type": "resources",
                        "uuid": str(uuid.uuid4()),
                        "version": [1, 0, 0]
                    }
                ]
            }
        case 'manifest_skins':
            return {
                "format_version": 1,
                "header": {
                    "name": "pack.name",
                    "uuid": str(uuid.uuid4()),
                    "version": [1, 0, 0]
                },
                "modules": [
                    {
                        "type": "skin_pack",
                        "uuid": str(uuid.uuid4()),
                        "version": [1, 0, 0]
                    }
                ]
            }
        case 'skins':
            return {
                "serialize_name": args[0],
                "localization_name": args[0],
                "skins": args[1]
            }
        case 'skin_language':
            return \
                f'skinpack.{args[0]}={args[1]}\n'\
        
        case 'world_packs':
            return [
                {
                    "pack_id": args[0],
                    "version": args[1]
                }
            ]
        case 'manifest_world':
            return {
                "format_version": 2,
                "header": {
                    "name": "pack.name",
                    "description": "pack.description",
                    "version": [1, 0, 0],
                    "uuid": str(uuid.uuid4()),
                    "lock_template_options": True,
                    "base_game_version": MANIFEST_BUILD
                },
                "modules": [
                    {
                        "type": "world_template",
                        "uuid": str(uuid.uuid4()),
                        "version": [1, 0, 0]
                    }
                ],
                "metadata" : {
                    "authors" : args[0]
                }
            }
        case 'sound_definitions':
            return {
                "format_version": SOUND_DEFINITIONS_VERSION,
                "sound_definitions": {}
            }
        case 'music_definitions':
            return {
            }
        case 'sound':
            return {
                args[0]: {
                    'category': args[1],
                    'sounds': []
                }
            }

        case 'blocks':
            return {}
        
def Defaults(type, *args):
    match type:
        case 'animation_controllers_rp':
            return {
                'format_version': '1.10.0',
                'animation_controllers': {}
            }
        case 'animation':
            return {
                "format_version": "1.10.0",
                "animations": {}
            }
        case 'rp_item_v1':
            return {
                'format_version': '1.10.0',
                'minecraft:item': {
                    'description': {
                        'identifier': f"{args[0]}:{args[1]}",
                        'category': 'Nature'
                    },
                    'components': {
                        'minecraft:icon': f'{args[1]}',
                        'minecraft:render_offsets': 'apple'
                    }
                }
            }
        case 'bp_item_v1':
            return {
                'format_version': '1.10.0',
                'minecraft:item': {
                    'description': {
                        'identifier': f"{args[0]}:{args[1]}",
                    },
                    'components': {}
                }
            }
        case 'bp_block_v1':
            return {
                'format_version': '1.10.0',
                'minecraft:block': {
                    'description': {
                        'identifier': f"{args[0]}:{args[1]}",
                        'is_experimental': False,
                        'register_to_creative_menu': True
                    },
                    'components': {}
                }
            }
        case 'recipe_shaped':
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shaped": {
                    "tags": [
                        "crafting_table"
                    ],
                    "pattern": [],
                    "key": {},
                    "result": {
                        'item': args[1],
                        'data': args[2],
                        'count': args[3]
                    },
                    "description": {
                        "identifier": f'{args[0]}'
                    }
                }
            }
        case 'recipe_shapeless':
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": [
                        "crafting_table"
                    ],
                    "ingredients": [],
                    "result": {
                        'item': args[1],
                        'data': args[2],
                        'count': args[3]
                    },
                    "description": {
                        "identifier": f'{args[0]}'
                    }
                }
            }
        case 'recipe_stonecutter':
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": [
                        "stonecutter"
                    ],
                    "ingredients": [],
                    "result": {
                        'item': args[1],
                        'data': args[2],
                        'count': args[3]
                    },
                    "description": {
                        "identifier": f'{args[0]}'
                    }
                }
            }
        case 'recipe_smithing_table':
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_shapeless": {
                    "tags": [
                        "smithing_table"
                    ],
                    "ingredients": [
                        {'item': 'minecraft:netherite_ingot', 'count': 1}
                    ],
                    "result": {
                        'item': args[1],
                        'data': args[2],
                        'count': args[3]
                    },
                    "description": {
                        "identifier": f'{args[0]}'
                    }
                }
            }
        case 'recipe_furnace':
            return {
                "format_version": "1.16.0",
                "minecraft:recipe_furnace": {
                    "tags": args[3],
                    "output": args[1],
                    "input": args[2],
                    "description": {
                        "identifier": f'{args[0]}'
                    }
                }
            }
        case 'spawn_rules':
            return {
                'format_version': '1.8.0',
                'minecraft:spawn_rules': {
                    'description': {
                        'identifier': f'{args[0]}:{args[1]}',
                        'population_control': 'ambient'
                    },
                    'conditions': []
                }
            }
        case 'materials':
            return {
                "materials": {
                    "version": "1.0.0"
                }
            }
        case 'music_definitions':
            return {}
        case 'language':
            return \
                f'pack.name={args[0]}\n'\
                f'pack.description={args[1]}\n\n'
        case 'manifest_bp':
            return {
                "format_version": 2,
                "header": {"description": "pack.description", "name": "pack.name", "uuid": str(uuid.uuid4()), "version": [1, 0, 0], "min_engine_version": [1, 18, 0]},
                "modules": [{"description": "pack.description", "type": "data", "uuid": str(uuid.uuid4()), "version": [1, 0, 0]}]
            }
        case 'manifest_rp':
            return {
                "format_version": 2,
                "header": {"description": "pack.description", "name": "pack.name", "uuid": str(uuid.uuid4()), "version": [1, 0, 0], "min_engine_version": [1, 16, 220]},
                "modules": [{"description": "pack.description", "type": "resources", "uuid": str(uuid.uuid4()), "version": [1, 0, 0]}]
            }
        case 'languages':
            return [
                'en_US',
                'en_GB',
                'de_DE',
                'es_ES',
                'es_MX',
                'fr_FR',
                'fr_CA',
                'it_IT',
                'pt_BR',
                'pt_PT',
                'ru_RU',
                'zh_CN',
                'zh_TW',
                'nl_NL',
                'bg_BG',
                'cs_CZ',
                'da_DK',
                'el_GR',
                'fi_FI',
                'hu_HU',
                'id_ID',
                'nb_NO',
                'pl_PL',
                'sk_SK',
                'sv_SE',
                'tr_TR',
                'uk_UA'
            ]
        case 'blocks':
            return {
                'format_version': '1.10.0'
            }
        case 'terrain_texture':
            return {
                'resource_pack_name': args[0],
                'texture_name': 'atlas.terrain',
                'padding': 8,
                'num_mip_levels': 4,
                'texture_data': {
                }
            }
        case 'loot_table':
            return {
                'pools': [
                ]
            }
        case 'dialogue':
            return {
                'format_version': '1.18.0',
                'minecraft:npc_dialogue': {
                    'scenes': []
                }
            }
        case 'sounds':
            return {
                "entity_sounds": {
                    "entities": {
                    }
                }
            }      
        case 'world_packs':
            return [
                {
                    "pack_id": args[0],
                    "version": args[1]
                }
            ]
        case 'script':
            return \
                'from anvil import *\n\n\n\n'\
                'if __name__ == "__main__":\n\n\n'\
                f'    ANVIL.compile\n'\
                f'    #Uncomment package when you\'re ready to submit it. Pass True as the argument to clear all assets when packaging\n'\
                f'    #ANVIL.package()\n'
        case 'settings':
            return \
                '# This is the wrong script to run\n'\
                '# Use this script to edit projects settings\n'\
                'from os import path\n\n'\
                'BASE_DIR = path.dirname(path.realpath(__file__))\n'
        case 'config':
            return {
                "COMPANY": args[1].title(),
                "NAMESPACE": args[0],
                "PROJECT_NAME": args[2],
                "DISPLAY_NAME": args[3].replace('_', ' ').replace('-', ' ').title(),
                "PROJECT_DESCRIPTION": f'{args[4].replace("_", " ").replace("-", " ").title()}',
                "VANILLA_VERSION": args[5],
                "LAST_CHECK": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        case 'structure':
            return {
                args[0]: {
                    "behavior_packs": {
                        f"BP_{args[0]}": {
                            "texts": {}
                        }
                    },
                    "resource_packs": {
                        f"RP_{args[0]}": {
                            "texts": {}
                        }
                    },
                    "assets": {
                        "animations": {},
                        "blocks": {},
                        "cache":{},
                        "geometries": {},
                        "items": {},
                        "particles": {},
                        "sounds": {},
                        "structures": {},
                        "textures": {},
                        "vanilla": {},
                        "marketing":{}
                    }
                }
            }
        case 'code-workspace':
            return {
            	"folders": [
            		{
            			"path": f"{args[0]}/{args[1]}"
            		},
            		{
            			"name": "BP.zip",
            			"uri": f"zip:{args[0]}/{args[1]}/assets/vanilla/BP.zip"
            		},
            		{
            			"name": "RP.zip",
            			"uri": f"zip:{args[0]}/{args[1]}/assets/vanilla/RP.zip"
            		}
            	],
            	"settings": {
            		"docwriter.style": "JSDoc"
            	}
            }
        case 'entity_rp':
            return {
                'format_version': '1.10.0',
                'minecraft:client_entity': {
                    'description': {
                        'identifier': f'{args[0]}:{args[1]}',
                        'materials': {
                            'default': 'entity_alphatest'
                        },
                        'scripts':{},
                        'textures': {},
                        'geometry': {},
                        'render_controllers': []
                    }
                }
            }
        case 'entity_bp':
            return {
                'format_version': '1.16.0',
                'minecraft:entity': {}
            }
        case 'render_controller':
            return{
                'format_version': '1.10.0',
                'render_controllers': {}
            }


def RawText(text: str):
    snake_case_name = text.lower().replace(' ', '_').replace('\n', '%1')
    display_name = text.replace('_', ' ').title()
    return snake_case_name, display_name


def random_character_generator(length: int):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def CreateImage(name: str, width: int, height: int, color, directory=''):
    img = Image.new('RGBA', (width, height), color=color)
    img.save(f'{directory}/{name}.png')


def GetColors(image):
    original = Image.open(image)
    reduced = original.convert('P', palette=Image.WEB)
    palette = reduced.getpalette()
    palette = [palette[3*n:3*n+3] for n in range(256)]
    color_count = [(n, palette[m]) for n, m in reduced.getcolors()]
    most = '#{0:02x}{1:02x}{2:02x}'.format(
        color_count[0][1][0], color_count[0][1][1], color_count[0][1][2])
    least = '#{0:02x}{1:02x}{2:02x}'.format(
        color_count[-1][1][0], color_count[-1][1][1], color_count[-1][1][2])
    return most, least


def RaiseError(text):
    raise SystemExit(text)


def CheckAvailability(file, type, folder):
    if FileExists(f'{folder}/{file}') is False:
        RaiseError(MISSING_FILE(type, file, folder))


def CreateDirectoriesFromTree(tree):
    def find_key(tree, path, a):
        for key, value in tree.items():
            if isinstance(value, dict):
                find_key(value, f'{path}/{key}', a)
            if value == {}:
                a.append(f'{path}/{key}')
        return a
    directories = find_key(tree, '', a=[])
    for dir in directories:
        CreateDirectory(dir)


def ShortenDict(d):
    if isinstance(d, dict):
        return {
            k: v for k, v in ((k, ShortenDict(v)) for k, v in d.items())
            if v != {} and v != [] or str(k).startswith('minecraft:')
        }

    elif isinstance(d, list):
        return [v for v in map(ShortenDict, d) if v != []]

    return d


def CreateTreeFromPath(path):
    def get_path(my_list):
        if len(my_list) > 0 and my_list[0] != '':
            return {my_list[0]: get_path(my_list[1::])}
        else:
            return {}
    my_list = path.split('/')
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
    return '/'.join(path)


def RemoveDirectory(path):
    shutil.rmtree(f'./{path}', ignore_errors=True)


def RemoveFile(path):
    os.remove(path)


def CreateDirectory(path:str):
    this_path = os.path.join('./',path.lstrip('/'))
    os.makedirs(this_path, exist_ok=True)


def MoveFiles(old_dir: str, new_dir: str, file_name: str):
    CreateDirectory(new_dir)
    os.replace(f'{old_dir}/{file_name}', f'{new_dir}/{file_name}')


def CopyFiles(old_dir: str, new_dir: str, file_name: str):
    CreateDirectory(new_dir)
    
    shutil.copyfile(MakePath(old_dir,file_name), MakePath(new_dir,file_name))


def CopyFolder(old_dir: str, new_dir: str):
    CreateDirectory(new_dir)
    shutil.copytree(os.path.realpath(old_dir), os.path.realpath(new_dir),dirs_exist_ok=True)


def File(name: str, content, directory: str, mode: str,*args):
    CreateDirectory(directory)
    type = name.split('.')[-1]
    out_content = ''
    file_content = content
    stamp = f'Generated with Anvil@StarkTMA {__version__}'
    time = datetime.now(datetime.now().astimezone().tzinfo).strftime("%d-%m-%Y %H:%M:%S %z")
    #copyright=f'Property of {COMPANY}'
    copyright=''
    path = os.path.normpath(os.path.join(directory,name))
    if mode == 'w':
        match type:
            case 'json' | 'material' | 'code-workspace':
                out_content = f'//{stamp}\n//{time}\n//{copyright}\n\n'
                file_content = json.dumps(content, sort_keys=False, indent=4)
            case 'py' | 'mcfunction':
                out_content = f'#{stamp}\n#{time}\n#{copyright}\n\n'
            case 'lang':
                out_content = f'##{stamp}\n##{time}\n##{copyright}\n\n'

    out_content += file_content
    prev = ''
    if FileExists(path):
        with open(path, 'r', encoding='utf-8') as file:
            prev = file.read()
    if prev.split('\n')[4::] != file_content.split('\n'):
        with open(path, mode, encoding='utf-8') as file:
            file.write(out_content)


def DownloadFile(url: str, save_path: str, content_type: str):
    def report_hook(count, block_size, total_size):
        progress = 100.0 * count * block_size / total_size
        # Converting  from B to MB
        downloaded = round((count * block_size)*pow(10,-6),1)
        total = round(total_size*pow(10,-6),1)
        bar = int((downloaded/total)*20)
        if progress <= 100:
            click.echo(f'\rDownloading: ', nl=False)
            click.echo(click.style("━" * bar,fg='bright_magenta'),nl=False)
            click.echo(click.style(f'╸',fg='bright_magenta'),nl=False)
            click.echo(click.style("━" * (20-bar),fg='bright_black'),nl=False)
            click.echo(click.style(f'  {downloaded}/{total} MB',fg='green'),nl=False)
        else:
            click.echo(f'\rDownloading: ', nl=False)
            click.echo(click.style("━" * 20,fg='bright_green'),nl=False)
            click.echo(click.style(f'╸',fg='bright_green'))
    request.urlretrieve(url, save_path, reporthook=report_hook)


def header():
    os.system('cls')
    click.echo(MODULE)
    click.echo(VERSION(__version__))
    click.echo(COPYRIGHT(datetime.now().year))