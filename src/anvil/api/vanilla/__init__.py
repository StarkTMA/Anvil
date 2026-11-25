"""Vanilla data from Mojang/bedrock-samples v1.26.60.5.

Import everything vanilla from here, e.g. `from anvil.api.vanilla import MinecraftItemTypes`.
"""

from .biomes import MinecraftBiomeTags, MinecraftBiomeTypes
from .blocks import MinecraftBlockTags, vanilla_block_ids
from .effects import (
    MinecraftEffects,
    MinecraftPotionEffectTypes,
    MinecraftPotionLiquidTypes,
)
from .enchantments import MinecraftEnchantments
from .entities import vanilla_entities_ids
from .factories import minecraft_blocks as MinecraftBlockTypes
from .factories import minecraft_entities as MinecraftEntityTypes
from .factories import minecraft_items as MinecraftItemTypes
from .features import MinecraftStructureTypes
from .items import MinecraftItemTags, vanilla_items_ids

__all__ = [
    "MinecraftBiomeTags",
    "MinecraftBiomeTypes",
    "MinecraftBlockTags",
    "MinecraftBlockTypes",
    "MinecraftEffects",
    "MinecraftEnchantments",
    "MinecraftEntityTypes",
    "MinecraftItemTags",
    "MinecraftItemTypes",
    "MinecraftPotionEffectTypes",
    "MinecraftPotionLiquidTypes",
    "MinecraftStructureTypes",
    "vanilla_block_ids",
    "vanilla_entities_ids",
    "vanilla_items_ids",
]
