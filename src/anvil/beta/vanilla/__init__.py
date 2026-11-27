"""Experimental vanilla content, only valid with `features.experimental`.

Import everything from here, e.g. `from anvil.beta.vanilla import MinecraftItemTypes`.
"""

from .biomes import MinecraftBiomeTypes
from .blocks import MinecraftBlockTypes, vanilla_block_ids
from .effects import MinecraftEffects
from .entities import MinecraftEntityTypes, vanilla_entities_ids
from .items import MinecraftItemTags, MinecraftItemTypes, vanilla_items_ids

__all__ = [
    "MinecraftBiomeTypes",
    "MinecraftBlockTypes",
    "MinecraftEffects",
    "MinecraftEntityTypes",
    "MinecraftItemTags",
    "MinecraftItemTypes",
    "vanilla_block_ids",
    "vanilla_entities_ids",
    "vanilla_items_ids",
]
