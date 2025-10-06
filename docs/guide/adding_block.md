# Adding a Custom Block

This guide shows how to create an **Enchanting Plus Table** block with **Anvil**. It's written for **Anvil beginners** who already understand Minecraft concepts. Each step highlights what's **necessary** versus **optional**.

---

## Define the Block

```py title="blocks/enchanting_plus_table.py"
from anvil.api.blocks.blocks import Block

# Namespace is inferred from anvilconfig; only provide the short name here.
def enchanting_plus_table():
    block = Block("enchanting_plus_table")
    return block
```

!!! warning
    Declare a `Block` with a **unique name** (e.g., `"enchanting_plus_table"`). Namespace comes from **anvilconfig**.

---

## Server Description & States

```py title="server description"
from anvil.lib.enums import ItemCategory

# Show the block in the creative inventory (optional)
block.server.description.menu_category(ItemCategory.Construction)
block.server.description.add_state("is_awesome", (False, True))
```

!!! note
    Server‑side states are **optional**. If you don't define any, the block still exports and works.

---

## Components — Visuals & Basics

```py title="components: visuals & basics"
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockSelectionBox,
    BlockDisplayName,
    BlockMaterialInstance,
    BlockGeometry,
    BlockDestructibleByMining,
)

# Visuals (mandatory): geometry + at least one material instance
block.server.components.add(
    BlockCollisionBox((16, 12, 16), (0, 0, 0)),
    BlockSelectionBox((16, 12, 16), (0, 0, 0)),
    BlockDisplayName("Enchanting Plus Table"),
    BlockMaterialInstance().add_instance(block.name, "enchanting_plus_table"),
    BlockGeometry("enchanting_plus_table"),
    BlockDestructibleByMining(1.5),
)
```

!!! info "Blockbench references"
    The identifier passed to `BlockGeometry(...)` must map to a **Blockbench file** under `assets/blockbench`, and its **internal geometry/material names must match**. Mismatches raise an export error.

!!! failure
    **Visuals are mandatory.** Without a `BlockGeometry` and at least one material instance, the block won't export.

![Enchanting Plus Table Blockbench preview](/assets/enchanting_plus_table_blockbench.png)

---

## Crafting Recipe

```py title="crafting"
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.vanilla.items import MinecraftItemTypes
from anvil.api.vanilla.blocks import MinecraftBlockTypes

recipe = ShapedCraftingRecipe(block.name)
recipe.result(block.identifier, count=1)
recipe.ingredients([
    [MinecraftItemTypes.AmethystShard, MinecraftBlockTypes.EnchantingTable(), MinecraftItemTypes.AmethystShard],
    [MinecraftBlockTypes.GoldBlock(),    MinecraftBlockTypes.GoldBlock(),       MinecraftBlockTypes.GoldBlock()],
])
recipe.unlock_items([
    MinecraftItemTypes.AmethystShard,
    MinecraftBlockTypes.EnchantingTable(),
    MinecraftBlockTypes.GoldBlock(),
])
recipe.queue()
```

!!! note
    Recipes are **optional**. If omitted, the block can still be obtained via creative inventory or commands.

---

## Block Item

```py title="block item"
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemIcon, ItemMaxStackSize
from anvil.lib.enums import ItemCategory

item = block.item
item.server.description.category(ItemCategory.Construction)
item.server.components.add(
    ItemMaxStackSize(64),
    ItemIcon(item.name),
    ItemBlockPlacer(block.identifier),
    ItemDisplayName("Enchanting Plus Table"),
)
```

!!! tip
    The block's **item** is available as `block.item`. Accessing it auto‑creates a corresponding item.

---

## Queue the Block

```py title="finalize"
block.queue()
return block
```

!!! success
    **Queuing is mandatory.** If you don't call `block.queue()`, the framework will **not export** the block.
Queuing the block will also queue any associated item.

!!! tip "Queue groups"
    You can also group exports by calling `block.queue("group")` if you prefer a structured output directory.

---

## Full Example — Enchanting Plus Table

```py title="blocks/enchanting_plus_table.py"
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockSelectionBox,
    BlockDisplayName,
    BlockMaterialInstance,
    BlockGeometry,
    BlockDestructibleByMining,
)
from anvil.api.items.components import ItemBlockPlacer, ItemDisplayName, ItemIcon, ItemMaxStackSize
from anvil.api.items.crafting import ShapedCraftingRecipe
from anvil.api.vanilla.items import MinecraftItemTypes
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.lib.enums import ItemCategory


def enchanting_plus_table():
    block = Block("enchanting_plus_table")

    block.server.description.menu_category(ItemCategory.Construction)
    block.server.description.add_state("is_awesome", (False, True))

    # Visuals (mandatory)
    block.server.components.add(
        BlockCollisionBox((16, 12, 16), (0, 0, 0)),
        BlockSelectionBox((16, 12, 16), (0, 0, 0)),
        BlockDisplayName("Enchanting Plus Table"),
        BlockMaterialInstance().add_instance(block.name, "enchanting_plus_table"),
        BlockGeometry("enchanting_plus_table"),
        BlockDestructibleByMining(1.5),
    )

    # Crafting recipe (optional)
    recipe = ShapedCraftingRecipe(block.name)
    recipe.result(block.identifier, count=1)
    recipe.ingredients([
        [MinecraftItemTypes.AmethystShard, MinecraftBlockTypes.EnchantingTable(), MinecraftItemTypes.AmethystShard],
        [MinecraftBlockTypes.GoldBlock(),    MinecraftBlockTypes.GoldBlock(),       MinecraftBlockTypes.GoldBlock()],
    ])
    recipe.unlock_items([
        MinecraftItemTypes.AmethystShard,
        MinecraftBlockTypes.EnchantingTable(),
        MinecraftBlockTypes.GoldBlock(),
    ])
    recipe.queue()

    # Block item (optional)
    item = block.item
    item.server.description.category(ItemCategory.Construction)
    item.server.components.add(
        ItemMaxStackSize(64),
        ItemIcon(item.name),
        ItemBlockPlacer(block.identifier),
        ItemDisplayName("Enchanting Plus Table"),
    )

    # Finalize (mandatory)
    block.queue()
    return block


EnchantingPlusTable = enchanting_plus_table()
```

---
