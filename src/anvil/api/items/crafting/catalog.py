"""The crafting item catalog: the groups and items added to the creative inventory and
the recipe book."""

from typing import ClassVar, Sequence

from anvil.api.blocks.blocks import Block
from anvil.api.core.enums import ItemCategory
from anvil.api.items.items import Item
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import CRAFTING_ITEMS_CATALOG
from anvil.lib.jsonmodel import JsonFile, JsonObject, json_field
from anvil.lib.schemas import MinecraftBlockDescriptor, MinecraftItemDescriptor
from anvil.lib.translator import AnvilTranslator


class _CatalogGroupIdentifier(JsonObject):
    """The `group_identifier` of a catalog group: its name and icon."""

    __required__: ClassVar[tuple[str, ...]] = ("name",)

    icon: str | None = None
    name: str = json_field()


class _CatalogGroup(JsonObject):
    """A group of a catalog category. Without a `group_identifier`, its items are loose."""

    group_identifier: _CatalogGroupIdentifier | None = None
    items: list[str] = json_field(default_factory=list)

    def add_items(self, items: Sequence[str]) -> None:
        """Adds items at the end of the group."""
        self.items.extend(items)


class _CatalogCategory(JsonObject):
    """A category of the catalog, with the groups added to it."""

    __required__: ClassVar[tuple[str, ...]] = ("category_name",)

    category_name: ItemCategory = json_field()
    groups: list[_CatalogGroup] = json_field(default_factory=list)

    def group(self, name: str) -> _CatalogGroup | None:
        """The named group, or None."""
        for group in self.groups:
            if group.group_identifier and group.group_identifier.name == name:
                return group
        return None

    def add_group(self, group: _CatalogGroup) -> None:
        """Adds a group at the end of the category."""
        self.groups.append(group)


class _CraftingItemsCatalog(JsonObject):
    """The `minecraft:crafting_items_catalog` object."""

    categories: list[_CatalogCategory] = json_field(default_factory=list)

    def category(self, category: ItemCategory) -> _CatalogCategory:
        """The category, added when it is not in the catalog yet."""
        for existing in self.categories:
            if existing.category_name == category:
                return existing
        added = _CatalogCategory(category_name=category)
        self.categories.append(added)
        return added


class _CraftingItemsCatalogFile(JsonObject):
    """The content of `item_catalog/crafting_item_catalog.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:crafting_items_catalog",
    )

    format_version: str = json_field(default=CRAFTING_ITEMS_CATALOG, init=False)
    catalog: _CraftingItemsCatalog = json_field(
        key="minecraft:crafting_items_catalog", default_factory=_CraftingItemsCatalog
    )


class CraftingItemCatalog(JsonFile):
    """The crafting item catalog: the groups and items added to the creative inventory and
    the recipe book. Additions go at the end of their category.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/craftingitemcatalogdocumentation)
    """

    _document = _CraftingItemsCatalogFile
    _instance = None
    _extension = ".json"
    _pack = Pack.BP
    _folder = "item_catalog"
    _object_type = "Crafting Item Catalog"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CraftingItemCatalog, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("crafting_item_catalog")
        self._initialized = True

    def add_group(
        self,
        category: ItemCategory,
        name: str,
        icon: MinecraftItemDescriptor | MinecraftBlockDescriptor,
        items: Sequence[Item | Block] = (),
    ) -> "CraftingItemCatalog":
        """Adds a group to a category, or adds the items to the group when it is already
        there. The items' menu category is set to the category and group.

        Args:
            category (ItemCategory): The category to add the group to.
            name (str): The group's display name, localized as `tag.<namespace>:<name>`.
            icon (MinecraftItemDescriptor | MinecraftBlockDescriptor): The item shown as the
                group's icon.
            items (Sequence[Item | Block], optional): The items of the group.

        Returns:
            CraftingItemCatalog: The current instance of CraftingItemCatalog.
        """
        localized_key = f"tag.{CONFIG.NAMESPACE}:{name.replace(" ", "_").lower()}"
        AnvilTranslator().add_localization_entry(localized_key, name)

        for item in items:
            item.server.description.menu_category(
                category=category, group=localized_key
            )

        identifiers = [str(item.identifier) for item in items]
        target = self._content.catalog.category(category)
        group = target.group(localized_key)
        if group is None:
            target.add_group(
                _CatalogGroup(
                    group_identifier=_CatalogGroupIdentifier(
                        icon=str(icon.identifier), name=localized_key
                    ),
                    items=identifiers,
                )
            )
        else:
            group.add_items(identifiers)
        return self

    def add_loose_items(
        self,
        category: ItemCategory,
        items: Sequence[Item | Block],
    ) -> "CraftingItemCatalog":
        """Adds items to a category outside of any collapsible group. The items' menu
        category is set to the category.

        Args:
            category (ItemCategory): The category to add the items to.
            items (Sequence[Item | Block]): The items to add.

        Returns:
            CraftingItemCatalog: The current instance of CraftingItemCatalog.
        """
        for item in items:
            item.server.description.menu_category(category=category)

        self._content.catalog.category(category).add_group(
            _CatalogGroup(items=[str(item.identifier) for item in items])
        )
        return self

    def queue(self) -> "CraftingItemCatalog":
        """Queues the catalog for export."""
        return super().queue()
