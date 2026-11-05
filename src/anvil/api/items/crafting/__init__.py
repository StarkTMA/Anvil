"""Recipes and the crafting item catalog.

Each recipe type writes one typed document. Its file class builds it, and values are checked
when the file is exported.
"""

from anvil.lib.jsonmodel.enums import ItemCategory, RecipeUnlockContext

from .brewing import PotionBrewingRecipe, PotionMixingRecipe
from .catalog import CraftingItemCatalog
from .furnace import SmeltingRecipe
from .shaped import ShapedCraftingRecipe
from .shapeless import ShapelessRecipe, StoneCutterRecipe
from .smithing_transform import SmithingRecipe
from .smithing_trim import SmithingTrimRecipe

__all__ = [
    "CraftingItemCatalog",
    "ItemCategory",
    "PotionBrewingRecipe",
    "PotionMixingRecipe",
    "RecipeUnlockContext",
    "ShapedCraftingRecipe",
    "ShapelessRecipe",
    "SmeltingRecipe",
    "SmithingRecipe",
    "SmithingTrimRecipe",
    "StoneCutterRecipe",
]
