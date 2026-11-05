# Recipes and the Item Catalog

This tutorial defines two materials, **Ember Dust** and **Ember Crystal**, and every recipe type Anvil exports: **shapeless**, **shaped**, **smelting** and **stonecutter**, then groups the items in the creative inventory with the **crafting item catalog**.

Every snippet compiles as written.

---

## The Items

```py title="recipes/ember_recipes.py"
from anvil.lib.jsonmodel.enums import ItemCategory
from anvil.api.items.components import ItemDisplayName, ItemIcon, ItemMaxStackSize
from anvil.api.items.items import Item
from anvil.api.pbr.texture_set import TextureComponents


def simple_item(name: str, display: str) -> Item:
    item = Item(name)
    item.server.description.set_menu_category(ItemCategory.Items)
    item.server.components.add(
        ItemIcon(textures=TextureComponents(color=name)),
        ItemDisplayName(value=display),
        ItemMaxStackSize(value=64),
    )
    return item.queue()


dust = simple_item("ember_dust", "Ember Dust")
crystal = simple_item("ember_crystal", "Ember Crystal")
```

!!! tip
    `queue()` returns the object, so a helper can create, queue and return an item in one expression. Items, blocks, vanilla `MinecraftItemTypes.X()` and `MinecraftBlockTypes.X()` descriptors and plain `"namespace:name"` strings are all accepted wherever a recipe wants an item.

---

## Shapeless

```py title="shapeless"
from anvil.api.items.crafting.shapeless import ShapelessRecipe
from anvil.api.vanilla.items import MinecraftItemTypes

ShapelessRecipe("ember_dust").ingredients(
    [MinecraftItemTypes.BlazePowder(), (MinecraftItemTypes.Gunpowder(), 2)]
).result(dust, count=3).unlock_items([MinecraftItemTypes.BlazePowder()]).queue()
```

An `(item, count)` tuple asks for several of one ingredient. `unlock_items` lists the items that reveal the recipe in the recipe book; `unlock_context(RecipeUnlockContext.AlwaysUnlocked)` is the alternative.

---

## Shaped

```py title="shaped"
from anvil.api.items.crafting.shaped import ShapedCraftingRecipe

ShapedCraftingRecipe("ember_crystal").ingredients(
    [
        [None, dust, None],
        [dust, MinecraftItemTypes.AmethystShard(), dust],
        [None, dust, None],
    ]
).result(crystal).unlock_items([dust]).queue()
```

```json
"minecraft:recipe_shaped": {
  "description": {"identifier": "tut:ember_crystal"},
  "tags": ["crafting_table"],
  "unlock": [{"item": "tut:ember_dust"}],
  "assume_symmetry": true,
  "pattern": [" a ", "aba", " a "],
  "key": {"a": {"item": "tut:ember_dust"}, "b": {"item": "minecraft:amethyst_shard"}},
  "result": {"item": "tut:ember_crystal", "count": 1}
}
```

The grid is a list of rows; `None` is an empty slot. Anvil assigns the pattern keys. Pass `assume_symmetry=False` to the constructor when the mirrored pattern must not match.

---

## Smelting and Stonecutting

```py title="furnace and stonecutter"
from anvil.lib.jsonmodel.enums import SmeltingTags
from anvil.api.items.crafting.furnace import SmeltingRecipe
from anvil.api.items.crafting.shapeless import StoneCutterRecipe
from anvil.api.vanilla.blocks import MinecraftBlockTypes

SmeltingRecipe(
    "ember_dust_from_crystal", [SmeltingTags.FURNACE, SmeltingTags.BLAST_FURNACE]
).input(crystal).output(dust).queue()

StoneCutterRecipe("ember_crystal_from_block").ingredient(
    MinecraftBlockTypes.AmethystBlock()
).result(crystal, count=4).queue()
```

!!! note
    Smelting recipes list the blocks they work in: `FURNACE`, `BLAST_FURNACE`, `SMOKER`, `CAMPFIRE` and `SOUL_CAMPFIRE`. Smithing recipes live in `anvil.api.items.crafting.smithing_transform` and `smithing_trim`, brewing in `brewing`.

---

## Crafting Item Catalog

```py title="catalog"
from anvil.api.items.crafting.catalog import CraftingItemCatalog

catalog = CraftingItemCatalog()
catalog.add_group(ItemCategory.Items, "Ember Materials", dust, [dust, crystal])
catalog.queue()
```

```json
"minecraft:crafting_items_catalog": {
  "categories": [
    {
      "category_name": "items",
      "groups": [{"group_identifier": {"icon": "tut:ember_dust", "name": "tag.tut:ember_materials"}, "items": ["tut:ember_dust", "tut:ember_crystal"]}]
    }
  ]
}
```

- `add_group(category, name, icon, items)` creates a named group; the name becomes a localized `tag.<namespace>:<name>` key.
- `add_loose_items(category, items)` adds items to a tab without a group.
- `CraftingItemCatalog()` is a single shared file, so groups can be added from several modules.

!!! tip "Menu category versus catalog"
    `set_menu_category(ItemCategory.Items, ItemGroups.Copper)` on the item or block description puts it in a **vanilla** group. The catalog is for **your own** groups. You can also pass the catalog's `tag.<namespace>:<name>` string as the group of `set_menu_category`.

---

## Full Example

```py title="recipes/ember_recipes.py"
from anvil.lib.jsonmodel.enums import ItemCategory, SmeltingTags
from anvil.api.items.components import ItemDisplayName, ItemIcon, ItemMaxStackSize
from anvil.api.items.crafting.catalog import CraftingItemCatalog
from anvil.api.items.crafting.furnace import SmeltingRecipe
from anvil.api.items.crafting.shaped import ShapedCraftingRecipe
from anvil.api.items.crafting.shapeless import ShapelessRecipe, StoneCutterRecipe
from anvil.api.items.items import Item
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.api.vanilla.items import MinecraftItemTypes


def simple_item(name: str, display: str) -> Item:
    item = Item(name)
    item.server.description.set_menu_category(ItemCategory.Items)
    item.server.components.add(
        ItemIcon(textures=TextureComponents(color=name)),
        ItemDisplayName(value=display),
        ItemMaxStackSize(value=64),
    )
    return item.queue()


def ember_recipes():
    dust = simple_item("ember_dust", "Ember Dust")
    crystal = simple_item("ember_crystal", "Ember Crystal")

    ShapelessRecipe("ember_dust").ingredients(
        [MinecraftItemTypes.BlazePowder(), (MinecraftItemTypes.Gunpowder(), 2)]
    ).result(dust, count=3).unlock_items([MinecraftItemTypes.BlazePowder()]).queue()

    ShapedCraftingRecipe("ember_crystal").ingredients(
        [
            [None, dust, None],
            [dust, MinecraftItemTypes.AmethystShard(), dust],
            [None, dust, None],
        ]
    ).result(crystal).unlock_items([dust]).queue()

    SmeltingRecipe(
        "ember_dust_from_crystal", [SmeltingTags.FURNACE, SmeltingTags.BLAST_FURNACE]
    ).input(crystal).output(dust).queue()

    StoneCutterRecipe("ember_crystal_from_block").ingredient(
        MinecraftBlockTypes.AmethystBlock()
    ).result(crystal, count=4).queue()

    catalog = CraftingItemCatalog()
    catalog.add_group(ItemCategory.Items, "Ember Materials", dust, [dust, crystal])
    catalog.queue()


ember_recipes()
```
