"""The `minecraft:recipe_shapeless`, also used by the stonecutter."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.items.crafting.recipe import _BaseRecipe, _item, _Recipe, _RecipeItem
from anvil.api.items.items import Item
from anvil.lib.format_versions import RECIPE_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import JsonObject, Length, json_field


class _ShapelessRecipe(_Recipe):
    """The `minecraft:recipe_shapeless` body."""

    __required__: ClassVar[tuple[str, ...]] = (
        "description",
        "tags",
        "ingredients",
        "result",
    )

    group: str | None = None
    ingredients: Annotated[list[_RecipeItem], Length(1, 9)] = json_field(
        default_factory=list
    )
    result: _RecipeItem | None = None

    def add_ingredient(self, ingredient: _RecipeItem) -> None:
        """Adds an ingredient."""
        self.ingredients.append(ingredient)

    def set_result(self, result: _RecipeItem) -> None:
        """Sets the item produced."""
        self.result = result


class _ShapelessRecipeFile(JsonObject):
    """The content of a shapeless recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_shapeless",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _ShapelessRecipe = json_field(
        key="minecraft:recipe_shapeless", default_factory=_ShapelessRecipe
    )


class ShapelessRecipe(_BaseRecipe):
    """A shapeless crafting recipe: ingredients placed anywhere on the crafting grid.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_shapeless)
    """

    _document = _ShapelessRecipeFile
    _object_type = "Shapeless Recipe"

    def __init__(self, name: str, tags: Sequence[str] = ("crafting_table",)) -> None:
        """Creates a shapeless recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            tags (Sequence[str], optional): The stations that use the recipe. Defaults to
                ("crafting_table",).
        """
        super().__init__(name, tags)

    def ingredients(
        self,
        items: Sequence[
            Item
            | str
            | Block
            | BlockDescriptor
            | str
            | tuple[Item | str | Block | BlockDescriptor, int]
            | None
        ],
    ) -> "ShapelessRecipe":
        """Adds the ingredients, at most 9. None entries are skipped.

        Args:
            items (Sequence[...]): The items, each an item or an `(item, data)` tuple.
        """
        for item in items:
            if item is not None:
                self._recipe.add_ingredient(_item(item))
        return self

    def result(
        self,
        item: Item | str | Block | BlockDescriptor,
        count: int = 1,
        data: int = 0,
    ) -> "ShapelessRecipe":
        """Sets the item produced.

        Args:
            item (Item | Block | BlockDescriptor | str): The item.
            count (int, optional): How many are produced. Defaults to 1.
            data (int, optional): The deprecated data value. Defaults to 0, left out.
        """
        self._recipe.set_result(_item(item, data, count))
        return self

    def queue(self) -> "ShapelessRecipe":
        return super().queue()


class StoneCutterRecipe(ShapelessRecipe):
    """A stonecutter recipe: a shapeless recipe with one ingredient, used by the stonecutter.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_shapeless)
    """

    _object_type = "Stone Cutter Recipe"

    def __init__(self, name: str, tags: Sequence[str] = ("stonecutter",)) -> None:
        """Creates a stonecutter recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            tags (Sequence[str], optional): The stations that use the recipe. Defaults to
                ("stonecutter",).
        """
        super().__init__(name, tags)

    def ingredient(
        self,
        item: Item | str | Block | BlockDescriptor,
        data: int = 0,
    ) -> "StoneCutterRecipe":
        """Sets the ingredient.

        Args:
            item (Item | Block | BlockDescriptor | str): The item.
            data (int, optional): The deprecated data value. Defaults to 0, left out.
        """
        self.ingredients([(item, data)])
        return self

    def queue(self) -> "StoneCutterRecipe":
        return super().queue()
