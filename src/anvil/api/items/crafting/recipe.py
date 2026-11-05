"""The parts every recipe type shares, and the base of the recipe file classes.

Each recipe type has its own module with a body (`_XRecipe`), the document written to the
file (`_XRecipeFile`) and the file class you create and build."""

from collections.abc import Sequence
from typing import Annotated, ClassVar

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.items.items import Item
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import (
    Identifier,
    JsonFile,
    JsonObject,
    NonNegative,
    Positive,
    Wrapped,
    json_field,
)
from anvil.lib.jsonmodel.enums import RecipeUnlockContext


class _RecipeItem(JsonObject):
    """An item of a recipe: an item, or any item of a tag."""

    item: str | None = None
    tag: str | None = None
    data: Annotated[int, NonNegative] | None = None
    count: Annotated[int, Positive] | None = None

    def __validate__(self) -> None:
        if (self.item is None) == (self.tag is None):
            raise ValueError("A recipe item needs exactly one of item or tag.")


class _RecipeUnlock(JsonObject):
    """An unlock condition: an item the player obtains, or a context."""

    item: str | None = None
    context: RecipeUnlockContext | None = None

    def __validate__(self) -> None:
        if (self.item is None) == (self.context is None):
            raise ValueError("A recipe unlock needs exactly one of item or context.")


def _item(item: object, data: int = 0, count: int | None = None) -> _RecipeItem:
    """A recipe item from an identifier, a descriptor or an `(item, data)` tuple."""
    if isinstance(item, tuple):
        item, data = item
    return _RecipeItem(item=str(item), data=data or None, count=count)


class _Recipe(JsonObject, abstract=True):
    """The parts every recipe type has: its identifier, tags, priority and unlocking."""

    __required__: ClassVar[tuple[str, ...]] = ("description", "tags")

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    tags: list[str] = json_field(default_factory=list)
    priority: int | None = None
    unlock: list[_RecipeUnlock] | _RecipeUnlock | None = None

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`."""
        self.description = identifier

    def set_tags(self, tags: Sequence[str]) -> None:
        """Sets the crafting stations that use the recipe."""
        self.tags = [str(tag) for tag in tags]

    def set_priority(self, priority: int) -> None:
        """Sets the priority of the recipe when several recipes match."""
        self.priority = priority

    def set_unlock(self, unlock: list[_RecipeUnlock] | _RecipeUnlock) -> None:
        """Sets what unlocks the recipe in the recipe book."""
        self.unlock = unlock

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The recipe has no identifier.")


class _BaseRecipe[D: JsonObject](JsonFile[D]):
    """The base of the recipe file classes."""

    _extension = ".recipe.json"
    _pack = Pack.BP
    _folder = "recipes"
    _object_type = "Base Recipe"

    def __init__(self, name: str, tags: Sequence[str]) -> None:
        super().__init__(name)
        self._recipe.set_description(self.identifier)
        self._recipe.set_tags(tags)

    @property
    def _recipe(self) -> _Recipe:
        """The recipe body in the file."""
        return self._document.recipe

    def priority(self, priority: int) -> "_BaseRecipe":
        """Sets the priority of the recipe when several recipes match.

        Args:
            priority (int): The priority, lower values first.
        """
        self._recipe.set_priority(priority)
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext) -> "_BaseRecipe":
        """Unlocks the recipe in the recipe book in a context.

        Args:
            unlock_context (RecipeUnlockContext): The context.
        """
        self._recipe.set_unlock(_RecipeUnlock(context=unlock_context))
        return self

    def unlock_items(
        self,
        unlock_items: Sequence[Item | str | Block | BlockDescriptor],
    ) -> "_BaseRecipe":
        """Unlocks the recipe in the recipe book when the player gets one of the items.

        Args:
            unlock_items (Sequence[Item | Block | BlockDescriptor | str]):
                The items.
        """
        self._recipe.set_unlock(
            [_RecipeUnlock(item=str(item)) for item in unlock_items]
        )
        return self

    def queue(self) -> "_BaseRecipe":
        """Queues the recipe for export."""
        return super().queue()
