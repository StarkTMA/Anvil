# Adding a Custom Block

This guide shows how to create an **Enchanting Plus Table** block with **Anvil**. It's written for **Anvil beginners** who already understand Minecraft concepts. Each step highlights what's **necessary** versus **optional**.

Every snippet on this page is taken from a project that compiles. Component arguments are **keyword-only**: write `BlockDestructibleByMining(seconds_to_destroy=1.5)`, not `BlockDestructibleByMining(1.5)`.

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
from anvil.lib.jsonmodel.enums import ItemCategory

# Show the block in the creative inventory (optional)
block.server.description.set_menu_category(ItemCategory.Construction)
block.server.description.add_state("is_awesome", (False, True))
```

!!! note
    Server‑side states are **optional**. If you don't define any, the block still exports and works. A state name without a namespace gets the project's (`tut:is_awesome`). States, permutations and traits are covered in [Block states, permutations and traits](block_states.md).

---

## Components — Visuals & Basics

```py title="components: visuals & basics"
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockDestructibleByMining,
    BlockGeometry,
    BlockMaterialInstance,
    BlockSelectionBox,
    InstanceSpec,
    InstanceVariant,
)

# Visuals (mandatory): geometry + at least one material instance
block.server.components.add(
    BlockCollisionBox(origin=(-8, 0, -8), size=(16, 12, 16)),
    BlockSelectionBox(origin=(-8, 0, -8), size=(16, 12, 16)),
    BlockMaterialInstance().add_instance(
        spec=InstanceSpec(
            blockbench="enchanting_plus_table",
            variations=[InstanceVariant(color="enchanting_plus_table")],
        )
    ),
    BlockGeometry(blockbench="enchanting_plus_table"),
    BlockDestructibleByMining(seconds_to_destroy=1.5),
)
```

!!! info "Blockbench references"
    `BlockGeometry(blockbench=...)` and `InstanceSpec(blockbench=...)` name a **Blockbench file** under `assets/bbmodels`. Its model identifier must equal the file name, and the texture named in `InstanceVariant(color=...)` must exist inside that file. Mismatches raise an export error.

!!! info "Blockbench collections"
    If your `.bbmodel` contains exported Blockbench collections, you can reference a specific part with `BlockGeometry(blockbench="my_model", collection="bottom")`. Anvil exports that collection as its own geometry and references it as `geometry.<namespace>.my_model.bottom`.

!!! tip "PBR Support"
    `InstanceVariant` takes the same arguments as `TextureComponents`: `InstanceVariant(color="block", normal="block_normal", mer="block_mer")` enables normal maps and metalness/emissive/roughness channels. See the [PBR guide](pbr.md).

!!! tip "Display name"
    Anvil adds a `BlockDisplayName` for you, keyed `tile.<namespace>:<name>.name` in `localization.csv`. Add `BlockDisplayName(value="Enchanting Plus Table")` yourself only to override the generated text.

!!! failure
    **Visuals are mandatory.** Without a `BlockGeometry` and at least one material instance, the block won't export.

---

## Block Sounds

```py title="block sounds"
from anvil.lib.jsonmodel.enums import BlockSoundGroup

block.client.sound_group(BlockSoundGroup.Wood)
```

!!! note
    A sound group reuses the sounds of a vanilla block and needs no sound files. Custom block sounds are covered in [Particles and sounds](particles_and_sounds.md).

---

## Crafting Recipe

```py title="crafting"
from anvil.api.items.crafting.shaped import ShapedCraftingRecipe
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.api.vanilla.items import MinecraftItemTypes

recipe = ShapedCraftingRecipe(block.name)
recipe.result(block)
recipe.ingredients(
    [
        [
            MinecraftItemTypes.AmethystShard(),
            MinecraftBlockTypes.EnchantingTable(),
            MinecraftItemTypes.AmethystShard(),
        ],
        [
            MinecraftBlockTypes.GoldBlock(),
            MinecraftBlockTypes.GoldBlock(),
            MinecraftBlockTypes.GoldBlock(),
        ],
    ]
)
recipe.unlock_items([MinecraftBlockTypes.EnchantingTable()])
recipe.queue()
```

!!! note
    Recipes are **optional**. If omitted, the block can still be obtained via creative inventory or commands. More recipe types are in [Recipes and the item catalog](recipes.md).

---

## Block Item

```py title="block item"
from anvil.lib.jsonmodel.enums import ItemCategory
from anvil.api.items.components import ItemIcon, ItemMaxStackSize
from anvil.api.pbr.texture_set import TextureComponents

item = block.item
item.server.description.set_menu_category(ItemCategory.Construction)
item.server.components.add(
    ItemMaxStackSize(value=64),
    ItemIcon(textures=TextureComponents(color=item.name)),
)
```

!!! tip
    The block's **item** is available as `block.item`. Accessing it creates an `Item` with the block's name, and `block.queue()` queues it too. The icon is read from `assets/textures/items/enchanting_plus_table.png`. Add `ItemBlockPlacer(block=block)` when the item should place the block itself instead of relying on the game's default block item.

---

## Queue the Block

```py title="finalize"
block.queue()
return block
```

!!! success
    **Queuing is mandatory.** If you don't call `block.queue()`, the framework will **not export** the block.
    Queuing the block also queues its client file and its item.

---

## Full Example — Enchanting Plus Table

```py title="blocks/enchanting_plus_table.py"
from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockDestructibleByMining,
    BlockGeometry,
    BlockMaterialInstance,
    BlockSelectionBox,
    InstanceSpec,
    InstanceVariant,
)
from anvil.lib.jsonmodel.enums import BlockSoundGroup, ItemCategory
from anvil.api.items.components import ItemIcon, ItemMaxStackSize
from anvil.api.items.crafting.shaped import ShapedCraftingRecipe
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.api.vanilla.items import MinecraftItemTypes


def enchanting_plus_table():
    block = Block("enchanting_plus_table")

    block.server.description.set_menu_category(ItemCategory.Construction)
    block.server.description.add_state("is_awesome", (False, True))

    # Visuals (mandatory)
    block.server.components.add(
        BlockCollisionBox(origin=(-8, 0, -8), size=(16, 12, 16)),
        BlockSelectionBox(origin=(-8, 0, -8), size=(16, 12, 16)),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench="enchanting_plus_table",
                variations=[InstanceVariant(color="enchanting_plus_table")],
            )
        ),
        BlockGeometry(blockbench="enchanting_plus_table"),
        BlockDestructibleByMining(seconds_to_destroy=1.5),
    )
    block.client.sound_group(BlockSoundGroup.Wood)

    # Crafting recipe (optional)
    recipe = ShapedCraftingRecipe(block.name)
    recipe.result(block)
    recipe.ingredients(
        [
            [
                MinecraftItemTypes.AmethystShard(),
                MinecraftBlockTypes.EnchantingTable(),
                MinecraftItemTypes.AmethystShard(),
            ],
            [
                MinecraftBlockTypes.GoldBlock(),
                MinecraftBlockTypes.GoldBlock(),
                MinecraftBlockTypes.GoldBlock(),
            ],
        ]
    )
    recipe.unlock_items([MinecraftBlockTypes.EnchantingTable()])
    recipe.queue()

    # Block item (optional)
    item = block.item
    item.server.description.set_menu_category(ItemCategory.Construction)
    item.server.components.add(
        ItemMaxStackSize(value=64),
        ItemIcon(textures=TextureComponents(color=item.name)),
    )

    # Finalize (mandatory)
    block.queue()
    return block


EnchantingPlusTable = enchanting_plus_table()
```

---

## Advanced Features

### Custom Ticking

Use `BlockTick` to make your block run a `tick` custom component event periodically or randomly.

```python
from anvil.api.blocks.components import BlockTick

block.server.components.add(BlockTick(interval_range=(10, 20), looping=True))
```

### Custom Components

For more complex logic, attach **Custom Components**. These are scripts that run in the game and can interact with the world.

```python
from anvil.api.blocks.components import BlockCustomComponent


class MyBlockLogic(BlockCustomComponent):
    identifier = "my_block_logic"


block.server.components.add(MyBlockLogic())
```

See the [Custom Components Guide](custom_components.md) for parameters and the TypeScript side.

### States, Permutations and Traits

Make the block change with its state (a lit lantern, a rotated model) in [Block states, permutations and traits](block_states.md).

### World Generation

To make your block generate naturally in the world, see [Generating features](world_features.md).
