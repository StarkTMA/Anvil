# Adding a Custom Item

This guide shows how to create an **Arcane User Guide** item with **Anvil**. It targets **Anvil beginners** who already understand Minecraft concepts. Each step highlights what's **necessary** versus **optional**.

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
from anvil.lib.enums import ItemCategory

# Optional: where it appears in the creative inventory
item.server.description.category(ItemCategory.Items)
```

!!! note
    The category is **optional**. If omitted, the item still exports and can be obtained by commands or via recipes.

---

## Components — Visuals & Basics

```py title="components: visuals & basics"
from anvil.api.items.components import (
    ItemDisplayName,
    ItemIcon,
    ItemMaxStackSize,
)

item.server.components.add(
    ItemIcon(item.name),                  # references a texture named like the item
    ItemDisplayName("Arcane User Guide"),
    ItemMaxStackSize(1),
)
```

!!! info "Textures"
    `ItemIcon(<name>)` looks up a **texture** with the same identifier under your assets/textures/items (e.g., `arcane_user_guide`). If the texture doesn't exist, export will fail.

!!! tip "Localization"
    Every plain string passed to any anvil component (e.g., `ItemDisplayName("Arcane User Guide")`) is automatically converted to a localization key and tracked via an XLSX file in your project root.

---

## Interactions

```py title="interactions"
from anvil.api.items.components import (
    ItemCooldown,
    ItemUseModifiers,
    ItemGlint,
)

item.server.components.add(
    ItemCooldown(item.name, 1),      # separate cooldown channel per-item-name
    ItemUseModifiers(700000, 0.4),   # use duration & movement factor
    ItemGlint(True),                 # cosmetic enchantment glint
)
```

!!! note
    All of the above are **optional**. Use them to control usability and flair.

---

## Crafting Recipe

```py title="crafting"
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.vanilla.items import MinecraftItemTypes

recipe = ShapedCraftingRecipe(item.name)
recipe.result(item.identifier)
recipe.ingredients([
    [MinecraftItemTypes.Book,        MinecraftItemTypes.Emerald],
    [MinecraftItemTypes.LapisLazuli, None],
])
recipe.queue()
```

!!! note
    Recipes are **optional**. If omitted, the item is still available via category or commands.

---

## Attachable (Optional)

```py title="attachable: minimal setup"
att = item.attachable
```

!!! tip
    The item's **attachable** is available as `item.attachable`. Accessing it auto‑creates a corresponding attachable.

!!! info "Same API as entities"
    From here, **everything works exactly like the entity client**: add textures/materials, render controllers, animations, animation controllers, particles, and sounds. Reuse the patterns from your **Adding a Custom Entity** tutorial for attachables.

---

## Queue the Item

```py title="finalize"
item.queue()
return item
```

!!! success
    **Queuing is mandatory.** If you don't call `item.queue()`, the framework will **not export** the item.
    Queuing the item will also queue any associated attachable.

!!! tip "Queue groups"
    You can group exports with `item.queue("group")` just like blocks and entities.

---

## Full Example — Arcane User Guide

```py title="items/arcane_user_guide.py"
from anvil.api.items.items import Item
from anvil.api.items.components import (
    ItemCooldown,
    ItemDisplayName,
    ItemIcon,
    ItemMaxStackSize,
    ItemUseModifiers,
    ItemGlint,
)
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.vanilla.items import MinecraftItemTypes
from anvil.lib.enums import ItemCategory

# Import the attachable helper from wherever you store it
from items.arcane_user_guide import user_guide_attachable  # adjust path to your layout


def arcane_user_guide():
    item = Item("arcane_user_guide")

    # Optional: creative category
    item.server.description.category(ItemCategory.Items)

    # Visuals & basics (recommended)
    item.server.components.add(
        ItemIcon(item.name),
        ItemDisplayName("Arcane User Guide"),
        ItemMaxStackSize(1),
    )

    # Interaction polish (optional)
    item.server.components.add(
        ItemCooldown(item.name, 1),
        ItemUseModifiers(700000, 0.4),
        ItemGlint(True),
    )

    # Attachable (optional) — paged book behavior
    user_guide_attachable(item)

    # Crafting (optional)
    recipe = ShapedCraftingRecipe(item.name)
    recipe.result(item.identifier)
    recipe.ingredients([
        [MinecraftItemTypes.Book,        MinecraftItemTypes.Emerald],
        [MinecraftItemTypes.LapisLazuli, None],
    ])
    recipe.queue()

    # Finalize (mandatory)
    item.queue()
    return item


ArcaneUserGuide = arcane_user_guide()
```

---

## Multi‑Variant Items (Leveraging Python)

```py title="items/enchanted_tomes.py"
from anvil.api.items.items import Item
from anvil.api.items.components import ItemIcon, ItemDisplayName, ItemMaxStackSize
from anvil.api.items.crafting import CraftingItemCatalog
from anvil.lib.enums import ItemCategory


def enchanted_tomes():
    names = {"tome_air": "Tome of Air", "tome_fire": "Tome of Fire"}
    items = []
    for key, display in names.items():
        it = Item(key)
        it.server.description.category(ItemCategory.Items)
        it.server.components.add(
            ItemIcon("enchanted_tomes"),
            ItemDisplayName(display),
            ItemMaxStackSize(1),
        )
        it.queue()
        items.append(it)

    # Optional: group in the creative catalog
    catalog = CraftingItemCatalog()
    catalog.add_group(
        ItemCategory.Items,
        "Enchanted Tomes",
        items[0],  # icon source block/item
        items,
    )
    catalog.queue()
    return items
```

!!! note
    `CraftingItemCatalog` lets you group related items in the creative/in‑game catalogs. Entirely **optional**.
