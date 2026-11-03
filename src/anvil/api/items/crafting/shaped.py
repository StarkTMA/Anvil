"""The `minecraft:recipe_shaped`."""

from typing import Annotated, ClassVar, Sequence

from anvil.api.items.crafting.recipe import _BaseRecipe, _item, _Recipe, _RecipeItem
from anvil.lib.format_versions import RECIPE_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import JsonObject, Keyed, Length, json_field
from anvil.lib.schemas import MinecraftBlockDescriptor, MinecraftItemDescriptor


class _ShapedKey(_RecipeItem):
    """An entry of a shaped recipe's `key`: the item a pattern symbol stands for."""

    symbol: str = json_field(exclude=True)


class _ShapedRecipe(_Recipe):
    """The `minecraft:recipe_shaped` body."""

    __required__: ClassVar[tuple[str, ...]] = (
        "description",
        "tags",
        "pattern",
        "key",
        "result",
    )

    assume_symmetry: bool | None = None
    group: str | None = None
    pattern: Annotated[list[Annotated[str, Length(1, 3)]], Length(1, 3)] = json_field(
        default_factory=list
    )
    key: Annotated[list[_ShapedKey], Keyed("symbol")] = json_field(default_factory=list)
    result: _RecipeItem | None = None

    def set_assume_symmetry(self, assume_symmetry: bool) -> None:
        """Sets whether the mirrored pattern also crafts the result."""
        self.assume_symmetry = assume_symmetry

    def set_pattern(self, pattern: list[str], key: list[_ShapedKey]) -> None:
        """Sets the pattern and the items its symbols stand for."""
        self.pattern = pattern
        self.key = key

    def set_result(self, result: _RecipeItem) -> None:
        """Sets the item produced."""
        self.result = result

    def __validate__(self) -> None:
        super().__validate__()
        symbols = {entry.symbol for entry in self.key}
        for row in self.pattern:
            for symbol in row:
                if symbol != " " and symbol not in symbols:
                    raise ValueError(
                        f"The pattern symbol '{symbol}' is not in the key."
                    )


class _ShapedRecipeFile(JsonObject):
    """The content of a shaped recipe file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:recipe_shaped",
    )

    format_version: str = json_field(default=RECIPE_JSON_FORMAT_VERSION, init=False)
    recipe: _ShapedRecipe = json_field(
        key="minecraft:recipe_shaped", default_factory=_ShapedRecipe
    )


_KEY_SYMBOLS = "abcdefghi"


class ShapedCraftingRecipe(_BaseRecipe):
    """A shaped crafting recipe: ingredients placed in a pattern on the crafting grid.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/recipe_shaped)
    """

    _document = _ShapedRecipeFile
    _object_type = "Shaped Crafting Recipe"

    def __init__(
        self,
        name: str,
        assume_symmetry: bool = True,
        tags: Sequence[str] = ("crafting_table",),
    ) -> None:
        """Creates a shaped recipe.

        Args:
            name (str): The name of the recipe, also its file name.
            assume_symmetry (bool, optional): Whether the mirrored pattern also crafts the
                result. Defaults to True.
            tags (Sequence[str], optional): The stations that use the recipe. Defaults to
                ("crafting_table",).
        """
        super().__init__(name, tags)
        self._recipe.set_assume_symmetry(assume_symmetry)

    def ingredients(
        self,
        items: Sequence[
            Sequence[
                MinecraftItemDescriptor
                | MinecraftBlockDescriptor
                | str
                | tuple[MinecraftItemDescriptor | MinecraftBlockDescriptor | str, int]
                | None
            ]
        ],
        keep_empty_slots: bool = False,
    ) -> "ShapedCraftingRecipe":
        """Sets the grid: up to 3 rows of up to 3 items, None for an empty slot. Each
        different item gets its own pattern symbol.

        Args:
            items (Sequence[Sequence[...]]): The rows, each item an item or an
                `(item, data)` tuple.
            keep_empty_slots (bool, optional): Keeps the empty rows and columns around the
                items. Defaults to False.

        Raises:
            ValueError: When there are more than 3 rows or 3 items in a row.
        """
        if len(items) > 3 or any(len(row) > 3 for row in items):
            raise ValueError(
                f"A shaped recipe has at most 3 rows of 3 items. {self._object_type}[{self.identifier}]"
            )

        key: list[_ShapedKey] = []
        pattern = ["   ", "   ", "   "]
        for i, row in enumerate(items):
            for j, item in enumerate(row):
                if item is None:
                    continue
                ingredient = _item(item)
                symbol = next(
                    (
                        entry.symbol
                        for entry in key
                        if (entry.item, entry.data)
                        == (ingredient.item, ingredient.data)
                    ),
                    None,
                )
                if symbol is None:
                    symbol = _KEY_SYMBOLS[len(key)]
                    key.append(
                        _ShapedKey(
                            symbol=symbol, item=ingredient.item, data=ingredient.data
                        )
                    )
                pattern[i] = pattern[i][:j] + symbol + pattern[i][j + 1 :]

        if not keep_empty_slots:
            while pattern and pattern[0] == "   ":
                pattern.pop(0)
            while pattern and pattern[-1] == "   ":
                pattern.pop(-1)
            while pattern and all(row[0] == " " for row in pattern):
                pattern = [row[1:] for row in pattern]
            while pattern and all(row[-1] == " " for row in pattern):
                pattern = [row[:-1] for row in pattern]

        self._recipe.set_pattern(pattern, key)
        return self

    def result(
        self,
        item: MinecraftItemDescriptor | MinecraftBlockDescriptor | str,
        count: int = 1,
        data: int = 0,
    ) -> "ShapedCraftingRecipe":
        """Sets the item produced.

        Args:
            item (MinecraftItemDescriptor | MinecraftBlockDescriptor | str): The item.
            count (int, optional): How many are produced. Defaults to 1.
            data (int, optional): The deprecated data value. Defaults to 0, left out.
        """
        self._recipe.set_result(_item(item, data, count))
        return self

    def queue(self) -> "ShapedCraftingRecipe":
        return super().queue()
