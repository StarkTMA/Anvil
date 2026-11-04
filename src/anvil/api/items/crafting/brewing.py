"""The brewing recipes: `minecraft:recipe_brewing_container` and `minecraft:recipe_brewing_mix`."""

from collections.abc import Sequence
from typing import ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.items.crafting.recipe import _BaseRecipe, _Recipe
from anvil.api.items.items import Item
from anvil.lib.format_versions import RECIPE_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import JsonObject, json_field


class _BrewingRecipe(_Recipe):
    """The body of a brewing recipe: an input potion and a reagent make an output."""

    __required__: ClassVar[tuple[str, ...]] = (
        "description",
        "tags",
        "input",
        "reagent",
        "output",
    )

    input: str | None = None
    reagent: str | None = None
    output: str | None = None

    def set_recipe(self, input: str, reagent: str, output: str) -> None:
        """Sets the input potion, the reagent and the output potion."""
        self.input = input
        self.reagent = reagent
        self.output = output


class _BrewingContainerRecipeFile(JsonObject):
    """The content of a brewing container recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_brewing_container",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _BrewingRecipe = json_field(
        key="minecraft:recipe_brewing_container", default_factory=_BrewingRecipe
    )


class _BrewingMixRecipeFile(JsonObject):
    """The content of a brewing mix recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_brewing_mix",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _BrewingRecipe = json_field(
        key="minecraft:recipe_brewing_mix", default_factory=_BrewingRecipe
    )


class _PotionRecipe(_BaseRecipe):
    """The base of the brewing recipe file classes."""

    def __init__(self, name: str, tags: Sequence[str] = ("brewing_stand",)) -> None:
        """Creates a brewing recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            tags (Sequence[str], optional): The stations that use the recipe. Defaults to
                ("brewing_stand",).
        """
        super().__init__(name, tags)

    def recipe(
        self,
        item: Item | str | Block | BlockDescriptor,
        reagent: Item | str | Block | BlockDescriptor,
        output: Item | str | Block | BlockDescriptor,
    ) -> "_PotionRecipe":
        """Sets the brewing.

        Args:
            item (Item | Block | BlockDescriptor | str): The input potion.
            reagent (Item | Block | BlockDescriptor | str): The item
                brewed with the input potion.
            output (Item | Block | BlockDescriptor | str): The output
                potion.
        """
        self._recipe.set_recipe(str(item), str(reagent), str(output))
        return self


class PotionBrewingRecipe(_PotionRecipe):
    """A brewing container recipe: changes the potion container, such as a potion into a
    splash potion.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/minecraftrecipe_potionbrewing)
    """

    _document = _BrewingContainerRecipeFile
    _object_type = "Potion Brewing Recipe"

    def queue(self) -> "PotionBrewingRecipe":
        return super().queue()


class PotionMixingRecipe(_PotionRecipe):
    """A brewing mix recipe: changes the potion type, such as awkward into strength.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_brewing_mix)
    """

    _document = _BrewingMixRecipeFile
    _object_type = "Potion Mixing Recipe"

    def queue(self) -> "PotionMixingRecipe":
        return super().queue()
