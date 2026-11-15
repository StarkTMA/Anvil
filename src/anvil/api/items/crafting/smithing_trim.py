"""The `minecraft:recipe_smithing_trim`."""

from collections.abc import Sequence
from typing import ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.items.crafting.recipe import _BaseRecipe, _Recipe, _RecipeItem
from anvil.api.items.items import Item
from anvil.lib.format_versions import RECIPE_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import JsonObject, json_field


class _SmithingTrimRecipe(_Recipe):
    """The `minecraft:recipe_smithing_trim` body."""

    __required__: ClassVar[tuple[str, ...]] = (
        "description",
        "tags",
        "template",
        "base",
        "addition",
    )

    template: str | _RecipeItem | None = None
    base: str | _RecipeItem | None = None
    addition: str | _RecipeItem | None = None

    def set_template(self, item: str | _RecipeItem) -> None:
        """Sets the trim template, an item or a tag."""
        self.template = item

    def set_base(self, item: str | _RecipeItem) -> None:
        """Sets the armor trimmed, an item or a tag."""
        self.base = item

    def set_addition(self, item: str | _RecipeItem) -> None:
        """Sets the trim material, an item or a tag."""
        self.addition = item


class _SmithingTrimRecipeFile(JsonObject):
    """The content of a smithing trim recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_smithing_trim",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _SmithingTrimRecipe = json_field(
        key="minecraft:recipe_smithing_trim", default_factory=_SmithingTrimRecipe
    )


def _item_or_tag(
    item: Item | str | Block | BlockDescriptor | None,
    tag: str | None,
) -> str | _RecipeItem:
    if (item is None) == (tag is None):
        raise ValueError("Give exactly one of item or tag.")
    return str(item) if tag is None else _RecipeItem(tag=tag)


class SmithingTrimRecipe(_BaseRecipe[_SmithingTrimRecipeFile]):
    """A smithing table trim recipe: armor decorated with a trim template and a material.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_smithing_trim)
    """

    _object_type = "Smithing Trim Recipe"

    def __init__(self, name: str, tags: Sequence[str] = ("smithing_table",)) -> None:
        """Creates a smithing trim recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            tags (Sequence[str], optional): The stations that use the recipe. Defaults to
                ("smithing_table",).
        """
        super().__init__(name, tags)

    def template(
        self,
        item: Item | str | Block | BlockDescriptor | None = None,
        tag: str | None = None,
    ) -> "SmithingTrimRecipe":
        """Sets the trim template: an item, or any item of a tag.

        Args:
            item (Item | Block | BlockDescriptor | str, optional): The item.
            tag (str, optional): The item tag, such as `minecraft:trim_templates`.
        """
        self._recipe.set_template(_item_or_tag(item, tag))
        return self

    def base(
        self,
        item: Item | str | Block | BlockDescriptor | None = None,
        tag: str | None = None,
    ) -> "SmithingTrimRecipe":
        """Sets the armor trimmed: an item, or any item of a tag.

        Args:
            item (Item | Block | BlockDescriptor | str, optional): The item.
            tag (str, optional): The item tag, such as `minecraft:trimmable_armors`.
        """
        self._recipe.set_base(_item_or_tag(item, tag))
        return self

    def addition(
        self,
        item: Item | str | Block | BlockDescriptor | None = None,
        tag: str | None = None,
    ) -> "SmithingTrimRecipe":
        """Sets the trim material: an item, or any item of a tag.

        Args:
            item (Item | Block | BlockDescriptor | str, optional): The item.
            tag (str, optional): The item tag, such as `minecraft:trim_materials`.
        """
        self._recipe.set_addition(_item_or_tag(item, tag))
        return self

    def queue(self) -> "SmithingTrimRecipe":
        return super().queue()
