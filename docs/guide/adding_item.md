# Adding a Custom Item

This guide shows how to create an **Arcane User Guide** item with **Anvil**. It targets **Anvil beginners** who already understand Minecraft concepts. Each step highlights what's **necessary** versus **optional**.

Every snippet on this page is taken from a project that compiles. Component arguments are **keyword-only**: write `ItemMaxStackSize(value=1)`, not `ItemMaxStackSize(1)`.

---

## Define the Item

```py title="items/arcane_user_guide.py"
from anvil.api.items.items import Item

# Namespace is inferred from anvilconfig; only provide the short name here.
def arcane_user_guide():
    item = Item("arcane_user_guide")
    return item
```

!!! warning
    Declare an `Item` with a **unique name** (e.g., `"arcane_user_guide"`). Namespace comes from **anvilconfig**.

---

## Server Description

```py title="server description"
from anvil.lib.jsonmodel.enums import ItemCategory

# Optional: where it appears in the creative inventory
item.server.description.set_menu_category(ItemCategory.Items)
```

!!! note
    The category is **optional**. If omitted, the item still exports and can be obtained by commands or via recipes. `set_menu_category` also takes a `group` (an `ItemGroups` member or a catalog `tag.<namespace>:<name>` key) and `is_hidden_in_commands`.

---

## Components — Visuals & Basics

```py title="components: visuals & basics"
from anvil.api.items.components import ItemDisplayName, ItemIcon, ItemMaxStackSize
from anvil.api.pbr.texture_set import TextureComponents

item.server.components.add(
    ItemIcon(textures=TextureComponents(color=item.name)),
    ItemDisplayName(value="Arcane User Guide"),
    ItemMaxStackSize(value=1),
)
```

!!! info "Textures"
    `ItemIcon(textures=TextureComponents(color=<name>))` reads `assets/textures/items/<name>.png` (here `arcane_user_guide.png`). If the texture doesn't exist, export fails.

!!! tip "PBR Support"
    Add PBR maps the same way: `TextureComponents(color=item.name, normal="texture_normal", mer="texture_mer")`.

!!! tip "Localization"
    `ItemDisplayName` is optional: Anvil adds one keyed `item.<namespace>:<name>.name` when you leave it out. Every plain string passed to a display name becomes a localization key tracked in `localization.csv`. See [Localization](localization.md).

!!! failure
    An item needs **at least one component**, or the export fails.

---

## Interactions

```py title="interactions"
from anvil.api.items.components import ItemCooldown, ItemGlint, ItemUseModifiers

item.server.components.add(
    ItemCooldown(category=item.name, duration=1),  # separate cooldown channel per item name
    ItemUseModifiers(use_duration=700000, movement_modifier=0.4),
    ItemGlint(),  # cosmetic enchantment glint
)
```

!!! note
    All of the above are **optional**. Use them to control usability and flair.

---

## Crafting Recipe

```py title="crafting"
from anvil.api.items.crafting.shaped import ShapedCraftingRecipe
from anvil.api.vanilla.items import MinecraftItemTypes

recipe = ShapedCraftingRecipe(item.name)
recipe.result(item)
recipe.ingredients(
    [
        [MinecraftItemTypes.Book(), MinecraftItemTypes.Emerald()],
        [MinecraftItemTypes.LapisLazuli(), None],
    ]
)
recipe.queue()
```

!!! note
    Recipes are **optional**. If omitted, the item is still available via category or commands. More recipe types are in [Recipes and the item catalog](recipes.md).

---

## Item Client / Attachable (Optional)

```py title="item client"
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents

client = item.client
client.description.add_geometry("arcane_user_guide")
client.description.add_texture(
    blockbench="arcane_user_guide",
    component=TextureComponents(color="arcane_user_guide"),
)
client.description.animation(
    "arcane_user_guide", "first_person", condition=Query.IsFirstPerson()
)
client.description.animation(
    "arcane_user_guide", "third_person", condition=~Query.IsFirstPerson()
)
rc = client.description.render_controller("default")
rc.set_geometry("arcane_user_guide")
rc.add_texture("arcane_user_guide")
```

!!! tip
    The item's **attachable** is its client, available as `item.client`. Accessing it creates the attachable; it is only exported when you used it.

!!! info "Same API as entities"
    From here, **everything works exactly like the entity client**: textures, materials, render controllers, animations, animation controllers, particles and sounds. See [Animating an entity](entity_animations.md) and, for armor, [Wearables and attachables](wearables.md).

---

## Queue the Item

```py title="finalize"
item.queue()
return item
```

!!! success
    **Queuing is mandatory.** If you don't call `item.queue()`, the framework will **not export** the item.
    Queuing the item also queues its attachable, when one was created.

---

## Full Example — Arcane User Guide

```py title="items/arcane_user_guide.py"
from anvil.lib.jsonmodel.enums import ItemCategory
from anvil.api.items.components import (
    ItemCooldown,
    ItemDisplayName,
    ItemGlint,
    ItemIcon,
    ItemMaxStackSize,
    ItemUseModifiers,
)
from anvil.api.items.crafting.shaped import ShapedCraftingRecipe
from anvil.api.items.items import Item
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.items import MinecraftItemTypes


def arcane_user_guide():
    item = Item("arcane_user_guide")

    item.server.description.set_menu_category(ItemCategory.Items)

    # Visuals & basics (mandatory)
    item.server.components.add(
        ItemIcon(textures=TextureComponents(color=item.name)),
        ItemDisplayName(value="Arcane User Guide"),
        ItemMaxStackSize(value=1),
    )

    # Interactions (optional)
    item.server.components.add(
        ItemCooldown(category=item.name, duration=1),
        ItemUseModifiers(use_duration=700000, movement_modifier=0.4),
        ItemGlint(),
    )

    # Crafting recipe (optional)
    recipe = ShapedCraftingRecipe(item.name)
    recipe.result(item)
    recipe.ingredients(
        [
            [MinecraftItemTypes.Book(), MinecraftItemTypes.Emerald()],
            [MinecraftItemTypes.LapisLazuli(), None],
        ]
    )
    recipe.queue()

    # Item client / attachable (optional)
    client = item.client
    client.description.add_geometry("arcane_user_guide")
    client.description.add_texture(
        blockbench="arcane_user_guide",
        component=TextureComponents(color="arcane_user_guide"),
    )
    client.description.animation(
        "arcane_user_guide", "first_person", condition=Query.IsFirstPerson()
    )
    client.description.animation(
        "arcane_user_guide", "third_person", condition=~Query.IsFirstPerson()
    )
    rc = client.description.render_controller("default")
    rc.set_geometry("arcane_user_guide")
    rc.add_texture("arcane_user_guide")

    # Finalize (mandatory)
    item.queue()
    return item


ArcaneUserGuide = arcane_user_guide()
```

---

## Multi‑Variant Items (Leveraging Python)

```py title="items/enchanted_tomes.py"
from anvil.lib.jsonmodel.enums import ItemCategory
from anvil.api.items.components import ItemDisplayName, ItemIcon, ItemMaxStackSize
from anvil.api.items.crafting.catalog import CraftingItemCatalog
from anvil.api.items.items import Item
from anvil.api.pbr.texture_set import TextureComponents


def enchanted_tomes():
    names = {"tome_air": "Tome of Air", "tome_fire": "Tome of Fire"}
    items = []
    for key, display in names.items():
        tome = Item(key)
        tome.server.description.set_menu_category(ItemCategory.Items)
        tome.server.components.add(
            ItemIcon(textures=TextureComponents(color=key)),
            ItemDisplayName(value=display),
            ItemMaxStackSize(value=1),
        )
        tome.queue()
        items.append(tome)

    # Optional: group in the creative catalog
    catalog = CraftingItemCatalog()
    catalog.add_group(ItemCategory.Items, "Enchanted Tomes", items[0], items)
    catalog.queue()
    return items


EnchantedTomes = enchanted_tomes()
```

!!! note
    `CraftingItemCatalog` groups related items in the creative inventory. The third argument is the item or block whose icon the group shows. Entirely **optional**.
