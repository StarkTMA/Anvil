"""The `minecraft:recipe_smithing_transform`."""

from typing import ClassVar, Sequence

from anvil.api.items.crafting.recipe import _BaseRecipe, _Recipe
from anvil.lib.format_versions import RECIPE_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import JsonObject, json_field
from anvil.lib.schemas import MinecraftBlockDescriptor, MinecraftItemDescriptor


class _SmithingTransformRecipe(_Recipe):
    """The `minecraft:recipe_smithing_transform` body."""

    __required__: ClassVar[tuple[str, ...]] = (
        "description",
        "tags",
        "template",
        "base",
        "addition",
        "result",
    )

    template: str | None = None
    base: str | None = None
    addition: str | None = None
    result: str | None = None

    def set_template(self, item: str) -> None:
        """Sets the smithing template item."""
        self.template = item

    def set_base(self, item: str) -> None:
        """Sets the item transformed."""
        self.base = item

    def set_addition(self, item: str) -> None:
        """Sets the material added."""
        self.addition = item

    def set_result(self, item: str) -> None:
        """Sets the item produced."""
        self.result = item


class _SmithingTransformRecipeFile(JsonObject):
    """The content of a smithing transform recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_smithing_transform",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _SmithingTransformRecipe = json_field(
        key="minecraft:recipe_smithing_transform",
        default_factory=_SmithingTransformRecipe,
    )


class SmithingRecipe(_BaseRecipe):
    """A smithing table transform recipe: a base item upgraded with a template and a material.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_smithing_transform)
    """

    _document = _SmithingTransformRecipeFile
    _object_type = "Smithing Recipe"

    def __init__(self, name: str, tags: Sequence[str] = ("smithing_table",)) -> None:
        """Creates a smithing transform recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            tags (Sequence[str], optional): The stations that use the recipe. Defaults to
                ("smithing_table",).
        """
        super().__init__(name, tags)

    def template(
        self, identifier: MinecraftItemDescriptor | MinecraftBlockDescriptor | str
    ) -> "SmithingRecipe":
        """Sets the smithing template item.

        Args:
            identifier (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
        """
        self._recipe.set_template(str(identifier))
        return self

    def base(
        self, identifier: MinecraftItemDescriptor | MinecraftBlockDescriptor | str
    ) -> "SmithingRecipe":
        """Sets the item transformed.

        Args:
            identifier (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
        """
        self._recipe.set_base(str(identifier))
        return self

    def addition(
        self, identifier: MinecraftItemDescriptor | MinecraftBlockDescriptor | str
    ) -> "SmithingRecipe":
        """Sets the material added.

        Args:
            identifier (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
        """
        self._recipe.set_addition(str(identifier))
        return self

    def result(
        self, identifier: MinecraftItemDescriptor | MinecraftBlockDescriptor | str
    ) -> "SmithingRecipe":
        """Sets the item produced.

        Args:
            identifier (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
        """
        self._recipe.set_result(str(identifier))
        return self

    def queue(self) -> "SmithingRecipe":
        return super().queue()
