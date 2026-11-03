"""The `minecraft:recipe_furnace`."""

from typing import Annotated, ClassVar, Sequence

from anvil.api.core.enums import SmeltingTags
from anvil.api.items.crafting.recipe import _BaseRecipe, _Recipe
from anvil.lib.format_versions import RECIPE_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import ItemObject, JsonObject, json_field
from anvil.lib.schemas import MinecraftBlockDescriptor, MinecraftItemDescriptor


class _FurnaceRecipe(_Recipe):
    """The `minecraft:recipe_furnace` body."""

    input: Annotated[str, ItemObject] | None = None
    output: str | None = None

    def set_input(self, item: str) -> None:
        """Sets the item smelted."""
        self.input = item

    def set_output(self, item: str) -> None:
        """Sets the item produced."""
        self.output = item


class _FurnaceRecipeFile(JsonObject):
    """The content of a furnace recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_furnace",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _FurnaceRecipe = json_field(
        key="minecraft:recipe_furnace", default_factory=_FurnaceRecipe
    )


class SmeltingRecipe(_BaseRecipe):
    """A furnace recipe: an item smelted in furnaces, smokers, blast furnaces or campfires.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_furnace)
    """

    _document = _FurnaceRecipeFile
    _object_type = "Smelting Recipe"

    def __init__(self, name: str, tags: Sequence[SmeltingTags]) -> None:
        """Creates a furnace recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            tags (Sequence[SmeltingTags]): The stations that smelt the item.
        """
        super().__init__(name, tags)

    def input(
        self, identifier: MinecraftItemDescriptor | MinecraftBlockDescriptor | str
    ) -> "SmeltingRecipe":
        """Sets the item smelted.

        Args:
            identifier (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
        """
        self._recipe.set_input(str(identifier))
        return self

    def output(
        self, identifier: MinecraftItemDescriptor | MinecraftBlockDescriptor | str
    ) -> "SmeltingRecipe":
        """Sets the item produced.

        Args:
            identifier (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
        """
        self._recipe.set_output(str(identifier))
        return self

    def queue(self) -> "SmeltingRecipe":
        return super().queue()
