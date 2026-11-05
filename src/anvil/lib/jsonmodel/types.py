"""Anvil's type aliases and the Literal value sets of components and files."""

from typing import Literal

from .enums import Slots

type Vector2D = tuple[float, float]
type Vector3D = tuple[float, float, float]
type Vector4D = tuple[float, float, float, float]

type Vector3DInt = tuple[int, int, int]
type Vector4DInt = tuple[int, int, int, int]

type RGB = Vector3D
type RGBA = Vector4D
type RGB255 = Vector3DInt
type RGBA255 = Vector4DInt
type HexRGB = str
type HexRGBA = str
type Color = RGB | RGBA | RGB255 | RGBA255 | HexRGB | HexRGBA


InstrumentSound = Literal[
    "note.harp",
    "note.bd",
    "note.snare",
    "note.hat",
    "note.bassattack",
    "note.flute",
    "note.bell",
    "note.guitar",
    "note.chime",
    "note.xylophone",
    "note.iron_xylophone",
    "note.cow_bell",
    "note.didgeridoo",
    "note.bit",
    "note.banjo",
    "note.pling",
    "note.trumpet",
    "note.trumpet_exposed",
    "note.trumpet_weathered",
    "note.trumpet_oxidized",
    "note.zombie",
    "note.skeleton",
    "note.creeper",
    "note.enderdragon",
    "note.witherskeleton",
    "note.piglin",
    "note.none",
]


BiomeNoiseType = Literal[
    "beach",
    "deep_ocean",
    "default",
    "default_mutated",
    "extreme",
    "highlands",
    "less_extreme",
    "lowlands",
    "mountains",
    "mushroom",
    "ocean",
    "river",
    "stone_beach",
    "swamp",
    "taiga",
]

BiomeNoiseGradientBuilderType = Literal[
    "minecraft:capped",
    "minecraft:frozen_ocean",
    "minecraft:mesa",
    "minecraft:noise_gradient",
    "minecraft:overworld",
    "minecraft:swamp",
    "minecraft:the_end",
]

BiomeVillageTypes = Literal["default", "desert", "ice", "savanna", "taiga"]

BiomeClimateCategory = Literal["medium", "warm", "lukewarm", "cold", "frozen"]

FoliageColorMap = Literal[
    "birch",
    "dry_foliage",
    "evergreen",
    "foliage",
    "mangrove_swamp_foliage",
    "swamp_foliage",
]

GrassColorMap = Literal["grass", "swamp_grass"]


BlockDefaultGeometry = Literal[
    "minecraft:geometry.full_block",
    "minecraft:geometry.full_block_v1",
    "minecraft:geometry.cross",
]

BlockCullingLayer = Literal[
    "minecraft:culling_layer.undefined", "minecraft:culling_layer.leaves"
]

BlockConnectionSource = Literal["all", "only_fences", "none"]

BlockPrecipitationBehavior = Literal[
    "obstruct_rain", "obstruct_rain_accumulate_snow", "none", "snowlogging"
]

BlockChestObstructionRule = Literal["always", "never", "shape"]

BlockSupportShape = Literal["fence", "stair"]

BlockLavaFlammable = Literal["always", "never"]

BlockSticky = Literal["none", "same"]

BlockMovementType = Literal["push_pull", "push", "popped", "immovable"]

TintMethod = Literal[
    "none",
    "default_foliage",
    "birch_foliage",
    "evergreen_foliage",
    "dry_foliage",
    "grass",
    "water",
]

Rarity = Literal["common", "uncommon", "rare", "epic"]
SpawnCategory = Literal[
    "creature",
    "monster",
    "ambient",
    "axolotls",
    "water_creature",
    "water_ambient",
    "underground_water_creature",
    "misc",
]

ItemUseAnimations = Literal[
    "eat",
    "drink",
    "block",
    "bow",
    "splash",
    "linger",
    "camera",
    "crossbow",
    "none",
    "brush",
    "spear",
    "spyglass",
]

ItemCooldownType = Literal["attack", "use"]

ItemStartUsing = Literal["always", "if_first"]

ItemPlantAtFace = Literal["UP", "DOWN", "NORTH", "SOUTH", "EAST", "WEST"]

ItemWearableSlots = Literal[
    Slots.Body,
    Slots.Chest,
    Slots.Feet,
    Slots.Head,
    Slots.Legs,
    Slots.Mainhand,
    Slots.Offhand,
]


MobEvent = Literal[
    "minecraft:pillager_patrols_event",
    "minecraft:wandering_trader_event",
    "minecraft:ender_dragon_event",
]


TextureFilter = Literal[
    "Point", "Bilinear", "Trilinear", "MipMapBilinear", "TexelAA", "PCF"
]
TextureWrap = Literal["Repeat", "Clamp"]
