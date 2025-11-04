import os

from anvil.lib.config import CONFIG
from anvil.lib.enums import ItemCategory, RecipeUnlockContext, SmeltingTags
from anvil.lib.schemas import AddonObject, BlockDescriptor, ItemDescriptor, JsonSchemes
from anvil.lib.translator import AnvilTranslator
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
        self,
        category_name: ItemCategory,
        group_name: str,
        group_icon: ItemDescriptor | BlockDescriptor,
        items_list: list[ItemDescriptor | BlockDescriptor] = [],
    ) -> "CraftingItemCatalog":
        """
        Adds a group to an existing category.

        Parameters:
            category_name (str): The category name to update.
            group_name (str): The group name to add.
            group_icon (ItemDescriptor | BlockDescriptor): The item to use as the icon for the group.
            items_list (list[ItemDescriptor | BlockDescriptor], optional): List of items to add to the group. Defaults to an empty list.
        """
        localized_key = f"tag.{CONFIG.NAMESPACE}:{group_name.replace(" ", "_").lower()}"
        AnvilTranslator().add_localization_entry(localized_key, group_name)

        group = {
            "group_identifier": {
                "icon": group_icon.identifier,
                "name": localized_key,
            },
            "items": [item.identifier for item in items_list],
        }

        for cat in self._content["minecraft:crafting_items_catalog"]["categories"]:
            if cat.get("category_name") == str(category_name):
                if "groups" not in cat:
                    cat["groups"] = []
                for existing_group in cat["groups"]:
                    if existing_group["group_identifier"]["name"] == localized_key:
                        existing_group.setdefault(
                            "items", existing_group.get("items", [])
                        ).extend([item.identifier for item in items_list])
                    continue
                else:
                    cat["groups"].append(group)
                break
        else:
            self._content["minecraft:crafting_items_catalog"]["categories"].append(
                {
                    "category_name": str(category_name),
                    "groups": [group],
                }
            )
        return self

    def add_loose_items(
        self, category_name: ItemCategory, items: list[ItemDescriptor | BlockDescriptor]
    ) -> "CraftingItemCatalog":
        """Adds loose items to a category.

        Parameters:
            category_name (ItemCategory): The category name to update.
            items (list[ItemDescriptor | BlockDescriptor]): List of items to add to the category.

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


class _BaseRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")
    _object_type = "Base Recipe"
    _type = "minecraft:recipe_furnace"

    def __init__(self, name: str):
        super().__init__(name)

    def priority(self, priority: int):
        self._content[self._type]["priority"] = priority
        return self

    def unlock_context(self, unlock_context: RecipeUnlockContext):
        self._content[self._type]["unlock"] = {"context": unlock_context.value}
        return self

    def unlock_items(self, unlock_items: list[Identifier]):
        self._content[self._type]["unlock"] = [
            {"item": str(item)} for item in unlock_items
        ]
        return self

    def queue(self):
        return super().queue()


class SmeltingRecipe(_BaseRecipe):
    _object_type = "Smelting Recipe"
    _type = "minecraft:recipe_furnace"

    def __init__(self, name: str, tags: list[SmeltingTags]):
        super().__init__(name)
        self._tags = tags
        self.content(JsonSchemes.recipe_smelting(self.identifier, tags))

    def input(self, identifier: Identifier):
        self._content["minecraft:recipe_furnace"]["input"] = {"item": identifier}
        return self

    def output(self, identifier: Identifier):
        self._content["minecraft:recipe_furnace"]["output"] = identifier
        return self

    def queue(self):
        return super().queue()


class SmithingRecipe(_BaseRecipe):
    _object_type = "Smithing Recipe"
    _extension = ".recipe.json"

    def __init__(self, name: str, tags: list[str] = ["smithing_table"]):
        self._name = name
        self.content(JsonSchemes.recipe_smithing_table(self.identifier, tags))
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

    def queue(self):
        return super().queue()


class ShapelessRecipe(_BaseRecipe):
    _object_type = "Shapeless Recipe"
    _type = "minecraft:recipe_shapeless"

    def __init__(self, name: str, tags: list[str] = ["crafting_table"]):
        super().__init__(name)
        self.content(JsonSchemes.recipe_shapeless_crafting(self.identifier, tags))

    def ingredients(self, items: list[tuple[Identifier, int]]):
        if len(items) > 9:
            raise ValueError(
                f"Too many items in shapeless recipe, maximum is 9. {self._object_type}[{self._name}]"
            )

        for i, item in enumerate(items):
            if not item is None:
                if not isinstance(item, tuple):
                    data = {"item": str(item)}
                else:
                    data = {"item": str(item[0]), "data": item[1]}
                self._content["minecraft:recipe_shapeless"]["ingredients"].append(data)
        return self

    def result(
        self,
        item: ItemDescriptor | BlockDescriptor | Identifier,
        count: int = 1,
        data: int = 0,
    ):
        self._content["minecraft:recipe_shapeless"]["result"] = {
            "item": str(item),
            "count": count,
            "data": data if data != 0 else {},
        }
        return self

    def queue(self):
        return super().queue()


class StoneCutterRecipe(ShapelessRecipe):
    _object_type = "Stone Cutter Recipe"

    def __init__(self, name: str, tags: list[str] = ["stonecutter"]):
        super().__init__(name)
        self.content(JsonSchemes.recipe_shapeless_crafting(self.identifier, tags))

    def ingredient(
        self, item: ItemDescriptor | BlockDescriptor | Identifier, data: int = 0
    ):
        return super().ingredient([(item, data)])

    def queue(self):
        return super().queue()


class ShapedCraftingRecipe(_BaseRecipe):
    _object_type = "Shaped Crafting Recipe"
    _type = "minecraft:recipe_shaped"

    def __init__(
        self,
        name: str,
        assume_symmetry: bool = True,
        tags: list[str] = ["crafting_table"],
    ):
        self._recipe_exactly = False
        super().__init__(name)
        self.content(
            JsonSchemes.recipe_shaped_crafting(self.identifier, assume_symmetry, tags)
        )

    def ingredients(
        self,
        items: list[list[tuple[ItemDescriptor | BlockDescriptor | Identifier, int]]],
        keep_empty_slots: bool = False,
    ) -> None:
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

    def result(
        self,
        item: ItemDescriptor | BlockDescriptor | Identifier,
        count: int = 1,
        data: int = 0,
    ):
        self._content["minecraft:recipe_shaped"]["result"] = {
            "item": str(item),
            "count": count,
            "data": data if data != 0 else {},
        }
        return self

    def queue(self):
        return super().queue()


class SmithingTrimRecipe(_BaseRecipe):
    _object_type = "Smithing Trim Recipe"
    _extension = ".recipe.json"

    def __init__(self, name: str, tags: list[str] = ["smithing_table"]):
        self._name = name
        self.content(JsonSchemes.recipe_smithing_table_trim(self.identifier, tags))
        super().__init__(name)

    def base(self, item: ItemDescriptor | BlockDescriptor | Identifier):
        self._content["minecraft:recipe_smithing_transform"]["base"] = item
        return self

    def addition(self, item: ItemDescriptor | BlockDescriptor | Identifier):
        self._content["minecraft:recipe_smithing_transform"]["addition"] = item
        return self

    def queue(self):
        return super().queue()


class PotionBrewingRecipe(_BaseRecipe):
    _object_type = "Potion Brewing Recipe"
    _extension = ".recipe.json"
    _type = "minecraft:recipe_brewing_container"

    def __init__(self, name: str, tags: list[str] = ["brewing_stand"]):
        """Represents a Potion Brewing Container Recipe.

        Args:
            name (str): The name of the recipe.
            tags (list[str], optional): Tags associated with the recipe. Defaults to ["brewing_stand"].

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/minecraftrecipe_potionbrewing)
        """
        super().__init__(name)
        self.content(JsonSchemes.recipe_brewing_container(self.identifier, tags))

    def recipe(
        self,
        item: ItemDescriptor | BlockDescriptor | Identifier,
        reagent: ItemDescriptor | BlockDescriptor | Identifier,
        output: ItemDescriptor | BlockDescriptor | Identifier,
    ):
        """Sets the recipe for the potion brewing container.

        Args:
            item (ItemDescriptor | BlockDescriptor | Identifier): Input potion used in the brewing container recipe.
            reagent (ItemDescriptor | BlockDescriptor | Identifier): ItemDescriptor | BlockDescriptor used in the brewing container recipe with the input potio
            output (ItemDescriptor | BlockDescriptor | Identifier): Output potion from the brewing container recipe.

        Returns:
            PotionBrewingRecipe: The current instance of PotionBrewingRecipe.
        """
        self._content[self._type]["input"] = str(item)
        self._content[self._type]["reagent"] = str(reagent)
        self._content[self._type]["output"] = str(output)
        return self

    def queue(self):
        return super().queue()


class PotionMixingRecipe(_BaseRecipe):
    _object_type = "Potion Mixing Recipe"
    _extension = ".recipe.json"
    _type = "minecraft:recipe_brewing_mix"

    def __init__(self, name: str, tags: list[str] = ["brewing_stand"]):
        """Represents a Potion Mixing Recipe.

        Args:
            name (str): The name of the recipe.
            tags (list[str], optional): Tags associated with the recipe. Defaults to ["brewing_stand"].

        [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/recipereference/examples/recipedefinitions/minecraftrecipe_potionbrewingmix)
        """
        super().__init__(name)
        self.content(JsonSchemes.recipe_brewing_mix(self.identifier, tags))

    def recipe(
        self,
        item: ItemDescriptor | BlockDescriptor | Identifier,
        reagent: ItemDescriptor | BlockDescriptor | Identifier,
        output: ItemDescriptor | BlockDescriptor | Identifier,
    ):
        """Sets the recipe for the potion mixing.

        Args:
            item (ItemDescriptor | BlockDescriptor | Identifier): Input potion used in the mixing recipe.
            reagent (ItemDescriptor | BlockDescriptor | Identifier): ItemDescriptor | BlockDescriptor used in the mixing recipe with the input potion.
            output (ItemDescriptor | BlockDescriptor | Identifier): Output potion from the mixing recipe.

        Returns:
            PotionMixingRecipe: The current instance of PotionMixingRecipe.
        """
        self._content[self._type]["input"] = str(item)
        self._content[self._type]["reagent"] = str(reagent)
        self._content[self._type]["output"] = str(output)
        return self

    def queue(self):
        return super().queue()
