import os

from anvil import ANVIL, CONFIG
from anvil.api.items.items import Item
from anvil.lib.enums import ItemCategory, RecipeUnlockContext, SmeltingTags
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import Identifier


class CraftingItemCatalog(AddonObject):
    _instance = None
    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "item_catalog")

    def __new__(cls, *Parameters, **kwParameters):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("crafting_item_catalog")
        self.content(JsonSchemes.crafting_items_catalog())
        self._initialized = True

    def add_group(
        self, category_name: ItemCategory, group_name: str, group_icon: Item, items_list: list[Item] = []
    ) -> "CraftingItemCatalog":
        """
        Adds a group to an existing category.

        Parameters:
            category_name (str): The category name to update.
            group_name (str): The group name to add.
            group_icon (Item): The item to use as the icon for the group.
            items_list (list[Item], optional): List of items to add to the group. Defaults to an empty list.
        """
        group_id = f"{CONFIG.NAMESPACE}:{group_name.replace(" ", "_").lower()}"
        ANVIL.definitions.register_lang(group_id, group_name)

        group = {
            "group_identifier": {
                "icon": group_icon.identifier,
                "name": group_id,
            },
            "items": [item.identifier for item in items_list],
        }

        for cat in self._content["minecraft:crafting_items_catalog"]["categories"]:
            if cat.get("category_name") == str(category_name):
                groups = cat.setdefault("groups", [])
                for existing_group in groups:
                    if existing_group["group_identifier"]["name"] == group_id:
                        existing_group.setdefault("items", []).extend([item.identifier for item in items_list])
                    break
                else:
                    groups.append(group)
                break
        else:
            self._content["minecraft:crafting_items_catalog"]["categories"].append(
                {
                    "category_name": str(category_name),
                    "groups": [group],
                }
            )
        return self

    def add_loose_items(self, category_name: ItemCategory, items: list[Item]) -> "CraftingItemCatalog":
        """Adds loose items to a category.

        Parameters:
            category_name (ItemCategory): The category name to update.
            items (list[Item]): List of items to add to the category.

        Returns:
            CraftingItemCatalog: The current instance of CraftingItemCatalog.
        """
        for cat in self._content["minecraft:crafting_items_catalog"]["categories"]:
            if cat.get("category_name") == str(category_name):
                cat.setdefault("loose_items", []).extend(items)
                break
        else:
            self._content["minecraft:crafting_items_catalog"]["categories"].append(
                {
                    "category_name": str(category_name),
                    "loose_items": items,
                }
            )
        return self

    def queue(self):
        return super().queue()


class SmeltingRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")
    _object_type = "Smelting Recipe"

    def __init__(self, name: str, *tags: SmeltingTags):
        super().__init__(name)
        self._tags = tags
        self.content(JsonSchemes.smelting_recipe(self.identifier, tags))

    def input(self, identifier: Identifier):
        self._content["minecraft:recipe_furnace"]["input"] = {"item": identifier}
        return self

    def output(self, identifier: Identifier):
        self._content["minecraft:recipe_furnace"]["output"] = identifier
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_furnace"]["priority"] = priority
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content["minecraft:recipe_furnace"]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Identifier]):
        self._content["minecraft:recipe_furnace"]["unlock"] = [{"item": [str(item)]} for item in unlock_items]
        return self

    def queue(self):
        return super().queue()


class SmithingRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")
    _object_type = "Smithing Recipe"

    def __init__(self, name: str):
        self._name = name
        self.content(JsonSchemes.smithing_table_recipe(self.identifier, ["smithing_table"]))
        super().__init__(name)

    def base(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["base"] = identifier
        return self

    def addition(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["addition"] = identifier
        return self

    def result(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["result"] = identifier
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_smithing_transform"]["priority"] = priority
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content["minecraft:recipe_smithing_transform"]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Identifier]):
        self._content["minecraft:recipe_smithing_transform"]["unlock"] = [{"item": [str(item)]} for item in unlock_items]
        return self

    def queue(self):
        return super().queue()


class ShapelessRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")
    _object_type = "Shapeless Recipe"

    def __init__(self, name: str):
        super().__init__(name)
        self.content(JsonSchemes.shapeless_crafting_recipe(self.identifier, ["crafting_table"]))

    def ingredients(self, items: list[tuple[Identifier, int]]):
        if len(items) > 9:
            raise ValueError(f"Too many items in shapeless recipe, maximum is 9. {self._object_type}[{self._name}]")

        for i, item in enumerate(items):
            if not item is None:
                if not isinstance(item, tuple):
                    data = {"item": str(item)}
                else:
                    data = {"item": str(item[0]), "data": item[1]}
                self._content["minecraft:recipe_shapeless"]["ingredients"].append(data)
        return self

    def result(self, item: Item | Identifier, count: int = 1, data: int = 0):
        self._content["minecraft:recipe_shapeless"]["result"] = {
            "item": str(item),
            "count": count,
            "data": data if data != 0 else {},
        }
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_shapeless"]["priority"] = priority
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content["minecraft:recipe_shapeless"]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Identifier]):
        self._content["minecraft:recipe_shapeless"]["unlock"] = [{"item": [str(item)]} for item in unlock_items]
        return self

    def queue(self):
        return super().queue()


class StoneCutterRecipe(ShapelessRecipe):
    _object_type = "Stone Cutter Recipe"

    def __init__(self, name: str):
        super().__init__(name)
        self.content(JsonSchemes.shapeless_crafting_recipe(self.identifier, ["stonecutter"]))

    def ingredient(self, item: Item | Identifier, data: int = 0):
        return super().ingredient([(item, data)])

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content["minecraft:recipe_shapeless"]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Item]):
        self._content["minecraft:recipe_shapeless"]["unlock"] = [{"item": [str(item)]} for item in unlock_items]
        return self

    def queue(self):
        return super().queue()


class ShapedCraftingRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")
    _object_type = "Shaped Crafting Recipe"

    def __init__(self, name: str, assume_symmetry: bool = True):
        self._recipe_exactly = False
        super().__init__(name)
        self.content(JsonSchemes.shaped_crafting_recipe(self.identifier, assume_symmetry, ["crafting_table"]))

    def ingredients(self, items: list[list[tuple[Item | Identifier, int]]], keep_empty_slots: bool = False) -> None:
        max_items = 9
        if len(items) > max_items:
            raise ValueError(
                f"Too many items in shaped recipe, maximum is {max_items}. {self._object_type}[{self.identifier}]"
            )

        keys = "abcdefghijklmnopqrstuvwxyz"
        pattern = ["   ", "   ", "   "]
        added_items = {}

        for i, row in enumerate(items):
            for j, item in enumerate(row):
                if not item is None:
                    if not isinstance(item, tuple):
                        data = {"item": str(item)}
                    else:
                        data = {"item": str(item[0]), "data": item[1]}

                    key = next((k for k, v in added_items.items() if v == data), None)
                    if key is None:
                        key = keys[len(added_items)]
                        added_items[key] = data

                    pattern[i] = pattern[i][:j] + key + pattern[i][j + 1 :]

        self._content["minecraft:recipe_shaped"]["key"] = added_items

        if not keep_empty_slots:
            while pattern and pattern[0] == "   ":
                pattern.pop(0)
            while pattern and pattern[-1] == "   ":
                pattern.pop(-1)

            while all(row[0] == " " for row in pattern):
                pattern = [row[1:] for row in pattern]
            while all(row[-1] == " " for row in pattern):
                pattern = [row[:-1] for row in pattern]

        self._content["minecraft:recipe_shaped"]["pattern"] = pattern
        return self

    def result(self, item: Item | Identifier, count: int = 1, data: int = 0):
        self._content["minecraft:recipe_shaped"]["result"] = {
            "item": str(item),
            "count": count,
            "data": data if data != 0 else {},
        }
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_shaped"]["priority"] = priority
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content["minecraft:recipe_shaped"]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Item | Identifier]):
        self._content["minecraft:recipe_shaped"]["unlock"] = [{"item": str(item)} for item in unlock_items]
        return self

    def queue(self):
        return super().queue()


class SmithingTrimRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")
    _object_type = "Smithing Trim Recipe"

    def __init__(self, name: str):
        self._name = name
        self.content(JsonSchemes.smithing_table_trim_recipe(self.identifier, ["smithing_table"]))
        super().__init__(name)

    def base(self, item: Item | Identifier):
        self._content["minecraft:recipe_smithing_transform"]["base"] = item
        return self

    def addition(self, item: Item | Identifier):
        self._content["minecraft:recipe_smithing_transform"]["addition"] = item
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_smithing_transform"]["priority"] = priority
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content["minecraft:recipe_smithing_trim"]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Item | Identifier]):
        self._content["minecraft:recipe_smithing_trim"]["unlock"] = [{"item": [str(item)]} for item in unlock_items]
        return self

    def queue(self):
        return super().queue()
