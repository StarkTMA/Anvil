"""Tests for the typed recipe files and the crafting item catalog."""

from types import SimpleNamespace

import pytest

from anvil.api.items.crafting import (
    CraftingItemCatalog,
    PotionBrewingRecipe,
    PotionMixingRecipe,
    ShapedCraftingRecipe,
    ShapelessRecipe,
    SmeltingRecipe,
    SmithingRecipe,
    SmithingTrimRecipe,
    StoneCutterRecipe,
)
from anvil.lib import config
from anvil.lib.jsonmodel.enums import ItemCategory, RecipeUnlockContext, SmeltingTags
from anvil.lib.lib import AnvilIO
from anvil.lib.translator import AnvilTranslator

jsonschema = pytest.importorskip("jsonschema")


@pytest.fixture(autouse=True)
def project(monkeypatch):
    monkeypatch.setattr(CraftingItemCatalog, "_instance", None)
    monkeypatch.setattr(AnvilTranslator, "add_localization_entry", lambda *a: None)
    with config.override(NAMESPACE="testns", PROJECT_NAME="proj"):
        yield


def _check(file):
    schema = type(file).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = AnvilIO._normalize_json_like(file._document)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


def _body(file, key):
    exported = _check(file)
    assert "format_version" in exported
    return exported[key]


def test_shaped_recipe_builds_pattern_and_key():
    recipe = ShapedCraftingRecipe("door")
    recipe.ingredients(
        [["a:plank", "a:plank"], ["a:plank", None], ["a:stick", "a:stick"]]
    )
    recipe.result("testns:door", 3)
    recipe.unlock_context(RecipeUnlockContext.AlwaysUnlocked)
    assert _body(recipe, "minecraft:recipe_shaped") == {
        "description": {"identifier": "testns:door"},
        "tags": ["crafting_table"],
        "assume_symmetry": True,
        "pattern": ["aa", "a ", "bb"],
        "key": {"a": {"item": "a:plank"}, "b": {"item": "a:stick"}},
        "result": {"item": "testns:door", "count": 3},
        "unlock": {"context": "AlwaysUnlocked"},
    }


def test_shaped_recipe_trims_empty_rows_and_columns():
    recipe = ShapedCraftingRecipe("pad").result("testns:pad")
    recipe.ingredients([[None, "a:x"], [None, "a:y"]])
    assert _body(recipe, "minecraft:recipe_shaped")["pattern"] == ["a", "b"]


def test_shaped_recipe_refuses_a_bigger_grid():
    with pytest.raises(ValueError):
        ShapedCraftingRecipe("big").ingredients([["a:x"]] * 4)
    with pytest.raises(ValueError):
        ShapedCraftingRecipe("wide").ingredients([["a:x"] * 4])


def test_shaped_recipe_needs_a_pattern():
    recipe = ShapedCraftingRecipe("empty").result("testns:x")
    with pytest.raises(ValueError):
        recipe._document.__json__()


def test_shapeless_recipe_with_data_and_unlock_items():
    recipe = ShapelessRecipe("button").ingredients([("a:plank", 2), "a:stone", None])
    recipe.result("testns:button", 1, data=4)
    recipe.unlock_items(["a:plank"]).priority(1)
    assert _body(recipe, "minecraft:recipe_shapeless") == {
        "description": {"identifier": "testns:button"},
        "tags": ["crafting_table"],
        "ingredients": [{"item": "a:plank", "data": 2}, {"item": "a:stone"}],
        "result": {"item": "testns:button", "count": 1, "data": 4},
        "unlock": [{"item": "a:plank"}],
        "priority": 1,
    }


def test_shapeless_recipe_refuses_ten_ingredients():
    recipe = ShapelessRecipe("many").ingredients(["a:x"] * 10).result("testns:x")
    with pytest.raises(ValueError):
        recipe._document.__json__()


def test_stonecutter_recipe():
    recipe = StoneCutterRecipe("slab").ingredient("a:stone").result("testns:slab", 2)
    body = _body(recipe, "minecraft:recipe_shapeless")
    assert body["tags"] == ["stonecutter"]
    assert body["ingredients"] == [{"item": "a:stone"}]


def test_smelting_recipe():
    recipe = SmeltingRecipe("cooked", [SmeltingTags.FURNACE, SmeltingTags.SMOKER])
    recipe.input("a:raw").output("a:cooked")
    assert _body(recipe, "minecraft:recipe_furnace") == {
        "description": {"identifier": "testns:cooked"},
        "tags": ["furnace", "smoker"],
        "input": {"item": "a:raw"},
        "output": "a:cooked",
    }


def test_smithing_transform_recipe_has_a_template():
    recipe = SmithingRecipe("upgrade").template("a:template").base("a:sword")
    recipe.addition("a:ingot").result("a:better_sword")
    assert _body(recipe, "minecraft:recipe_smithing_transform") == {
        "description": {"identifier": "testns:upgrade"},
        "tags": ["smithing_table"],
        "template": "a:template",
        "base": "a:sword",
        "addition": "a:ingot",
        "result": "a:better_sword",
    }


def test_smithing_trim_recipe_writes_its_own_key_and_tags():
    recipe = SmithingTrimRecipe("trim").template(tag="minecraft:trim_templates")
    recipe.base(tag="minecraft:trimmable_armors").addition("a:gem")
    assert _body(recipe, "minecraft:recipe_smithing_trim") == {
        "description": {"identifier": "testns:trim"},
        "tags": ["smithing_table"],
        "template": {"tag": "minecraft:trim_templates"},
        "base": {"tag": "minecraft:trimmable_armors"},
        "addition": "a:gem",
    }
    with pytest.raises(ValueError):
        recipe.base("a:x", tag="a:y")


@pytest.mark.parametrize(
    "cls, key",
    [
        (PotionBrewingRecipe, "minecraft:recipe_brewing_container"),
        (PotionMixingRecipe, "minecraft:recipe_brewing_mix"),
    ],
)
def test_brewing_recipes(cls, key):
    recipe = cls("brew").recipe("a:potion", "a:dust", "a:splash")
    recipe.unlock_items(["a:dust"])
    assert _body(recipe, key) == {
        "description": {"identifier": "testns:brew"},
        "tags": ["brewing_stand"],
        "input": "a:potion",
        "reagent": "a:dust",
        "output": "a:splash",
        "unlock": [{"item": "a:dust"}],
    }


def _item(identifier):
    calls = []
    description = SimpleNamespace(set_menu_category=lambda **kw: calls.append(kw))
    return SimpleNamespace(
        identifier=identifier,
        server=SimpleNamespace(description=description),
        calls=calls,
    )


def test_catalog_groups_merge_and_loose_items():
    gem, ore, rod = _item("testns:gem"), _item("testns:ore"), _item("testns:rod")
    catalog = CraftingItemCatalog()
    catalog.add_group(ItemCategory.Items, "Gems", gem, [gem])
    catalog.add_group(ItemCategory.Items, "Gems", gem, [ore])
    catalog.add_loose_items(ItemCategory.Equipment, [rod])
    assert CraftingItemCatalog() is catalog
    assert gem.calls == [{"category": ItemCategory.Items, "group": "tag.testns:gems"}]
    assert rod.calls == [{"category": ItemCategory.Equipment}]
    assert _check(catalog) == {
        "format_version": "1.21.60",
        "minecraft:crafting_items_catalog": {
            "categories": [
                {
                    "category_name": "items",
                    "groups": [
                        {
                            "group_identifier": {
                                "icon": "testns:gem",
                                "name": "tag.testns:gems",
                            },
                            "items": ["testns:gem", "testns:ore"],
                        }
                    ],
                },
                {"category_name": "equipment", "groups": [{"items": ["testns:rod"]}]},
            ]
        },
    }
