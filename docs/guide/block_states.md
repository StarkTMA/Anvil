# Block States, Permutations and Traits

This tutorial builds a **Brass Lantern** that can be lit, faces the direction it was placed in, only sits on stone, and ticks. It shows how a block changes with its **states**, how **permutations** swap components, how **traits** give the game-managed states, and how a **custom component** carries parameters to your scripts. Read [Adding a Custom Block](adding_block.md) first.

The whole example compiles as written.

---

## States and Traits

```py title="blocks/brass_lantern.py"
from anvil.api.blocks.blocks import Block
from anvil.lib.jsonmodel.enums import ItemCategory, ItemGroups, PlacementDirectionTrait

block = Block("brass_lantern")
description = block.server.description

description.set_menu_category(ItemCategory.Items, ItemGroups.Copper)
description.add_state("lit", (False, True))
description.traits.set_placement_direction(
    traits=[PlacementDirectionTrait.CardinalDirection]
)
```

- `add_state(name, values)` declares a state you control (up to 16 values). The name gets the project namespace: `tut:lit`.
- A **trait** adds states the game sets on placement. `set_placement_direction` gives `minecraft:cardinal_direction` (or `facing_direction`), `set_placement_position` gives `block_face` and `vertical_half`, `set_connection` the connection sides and `set_multi_block(direction, part_count)` the multi-block part.

```json
"description": {
  "identifier": "tut:brass_lantern",
  "states": {"tut:lit": [false, true]},
  "menu_category": {"category": "items", "group": "minecraft:itemGroup.name.copper"},
  "traits": {"minecraft:placement_direction": {"enabled_states": ["minecraft:cardinal_direction"]}}
}
```

---

## Root Components

```py title="root components"
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockDestructibleByMining,
    BlockGeometry,
    BlockMaterialInstance,
    BlockPlacementFilter,
    BlockSelectionBox,
    BlockTick,
    InstanceSpec,
    InstanceVariant,
)
from anvil.lib.jsonmodel.enums import BlockFaceValues
from anvil.api.vanilla.blocks import MinecraftBlockTypes

block.server.components.add(
    BlockGeometry(blockbench="brass_lantern"),
    BlockMaterialInstance().add_instance(
        spec=InstanceSpec(
            blockbench="brass_lantern",
            variations=[InstanceVariant(color="brass_lantern")],
        )
    ),
    BlockCollisionBox(origin=(-4, 0, -4), size=(8, 10, 8)),
    BlockSelectionBox(origin=(-4, 0, -4), size=(8, 10, 8)),
    BlockDestructibleByMining(seconds_to_destroy=0.5),
    BlockPlacementFilter().add_condition(
        allowed_faces=[BlockFaceValues.Up],
        block_filter=[MinecraftBlockTypes.Stone(), MinecraftBlockTypes.Cobblestone()],
    ),
    BlockTick(interval_range=(40, 80), looping=True),
)
```

!!! note
    `BlockPlacementFilter` limits where the block can be placed: here only on the top face of stone or cobblestone. `BlockTick` calls the `onTick` hook of the block's custom components every 40 to 80 ticks.

---

## Permutations

A permutation is a Molang condition and the components that apply while it is true. Components in a permutation **replace** the root component with the same identifier.

```py title="permutations"
from anvil.api.blocks.components import BlockLightEmission
from anvil.api.logic.molang import Query

block.server.permutation(Query.BlockState("lit")).add(
    BlockLightEmission(value=12),
    BlockMaterialInstance().add_instance(
        spec=InstanceSpec(
            blockbench="brass_lantern",
            variations=[InstanceVariant(color="brass_lantern_lit")],
        )
    ),
)
block.server.permutation(
    Query.BlockState(PlacementDirectionTrait.CardinalDirection) == "north"
).add(BlockGeometry(blockbench="brass_lantern").set_n_way_visual_rotation(y="180"))
```

```json
"permutations": [
  {
    "condition": "q.block_state('tut:lit')",
    "components": {
      "minecraft:light_emission": 12,
      "minecraft:material_instances": {"*": {"texture": "tut:brass_lantern_lit"}}
    }
  },
  {
    "condition": "(q.block_state('minecraft:cardinal_direction') == 'north')",
    "components": {
      "minecraft:geometry": {"n_way_visual_rotation": {"y": "180"}, "identifier": "geometry.tut.brass_lantern"}
    }
  }
]
```

!!! tip "State names in Molang"
    `Query.BlockState("lit")` resolves the bare name to the block's own state. Pass a trait enum member for the game's states.

!!! tip "Rotation without permutations"
    `BlockGeometry(...).set_n_way_visual_rotation(y="q.block_state('minecraft:cardinal_direction') == 'north' ? 180 : 0")` rotates the model from Molang, so one geometry component can replace four permutations.

---

## Custom Component With Parameters

Custom components carry data from Python to the Script API. Fields are declared like any dataclass field; Anvil validates them at export.

```py title="custom component"
from typing import Annotated

from anvil.api.blocks.components import BlockCustomComponent
from anvil.lib.jsonmodel import InRange, json_field


class LanternToggle(BlockCustomComponent):
    identifier = "lantern_toggle"

    cooldown_ticks: Annotated[int, InRange(0, 200)] = json_field(default=10)


block.server.components.add(LanternToggle(cooldown_ticks=20))
```

```json
"tut:lantern_toggle": {"cooldown_ticks": 20}
```

The TypeScript side reads `params.cooldown_ticks` in `onPlayerInteract` and sets the `tut:lit` state with `block.setPermutation(block.permutation.withState("tut:lit", true))`. See [Custom Components](custom_components.md).

---

## Sounds and the Item

```py title="sounds and item"
from anvil.lib.jsonmodel.enums import BlockSoundGroup
from anvil.api.items.components import ItemBlockPlacer, ItemIcon
from anvil.api.pbr.texture_set import TextureComponents

block.client.sound_group(BlockSoundGroup.Chain)

item = block.item
item.server.description.set_menu_category(ItemCategory.Items, ItemGroups.Copper)
item.server.components.add(
    ItemIcon(textures=TextureComponents(color="brass_lantern")),
    ItemBlockPlacer(block=block, replace_block_item=True),
)

block.queue()
```

!!! note
    `ItemBlockPlacer(block=block, replace_block_item=True)` makes the item the block's own item, so the icon from `assets/textures/items/brass_lantern.png` is what shows in the inventory.

---

## Full Example — Brass Lantern

```py title="blocks/brass_lantern.py"
from typing import Annotated

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockCollisionBox,
    BlockCustomComponent,
    BlockDestructibleByMining,
    BlockGeometry,
    BlockLightEmission,
    BlockMaterialInstance,
    BlockPlacementFilter,
    BlockSelectionBox,
    BlockTick,
    InstanceSpec,
    InstanceVariant,
)
from anvil.lib.jsonmodel.enums import (
    BlockFaceValues,
    BlockSoundGroup,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
)
from anvil.api.items.components import ItemBlockPlacer, ItemIcon
from anvil.api.logic.molang import Query
from anvil.api.pbr.texture_set import TextureComponents
from anvil.api.vanilla.blocks import MinecraftBlockTypes
from anvil.lib.jsonmodel import InRange, json_field


class LanternToggle(BlockCustomComponent):
    identifier = "lantern_toggle"

    cooldown_ticks: Annotated[int, InRange(0, 200)] = json_field(default=10)


def brass_lantern():
    block = Block("brass_lantern")
    description = block.server.description

    description.set_menu_category(ItemCategory.Items, ItemGroups.Copper)
    description.add_state("lit", (False, True))
    description.traits.set_placement_direction(
        traits=[PlacementDirectionTrait.CardinalDirection]
    )

    block.server.components.add(
        BlockGeometry(blockbench="brass_lantern"),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench="brass_lantern",
                variations=[InstanceVariant(color="brass_lantern")],
            )
        ),
        BlockCollisionBox(origin=(-4, 0, -4), size=(8, 10, 8)),
        BlockSelectionBox(origin=(-4, 0, -4), size=(8, 10, 8)),
        BlockDestructibleByMining(seconds_to_destroy=0.5),
        BlockPlacementFilter().add_condition(
            allowed_faces=[BlockFaceValues.Up],
            block_filter=[MinecraftBlockTypes.Stone(), MinecraftBlockTypes.Cobblestone()],
        ),
        BlockTick(interval_range=(40, 80), looping=True),
        LanternToggle(cooldown_ticks=20),
    )

    block.server.permutation(Query.BlockState("lit")).add(
        BlockLightEmission(value=12),
        BlockMaterialInstance().add_instance(
            spec=InstanceSpec(
                blockbench="brass_lantern",
                variations=[InstanceVariant(color="brass_lantern_lit")],
            )
        ),
    )
    block.server.permutation(
        Query.BlockState(PlacementDirectionTrait.CardinalDirection) == "north"
    ).add(BlockGeometry(blockbench="brass_lantern").set_n_way_visual_rotation(y="180"))

    block.client.sound_group(BlockSoundGroup.Chain)

    item = block.item
    item.server.description.set_menu_category(ItemCategory.Items, ItemGroups.Copper)
    item.server.components.add(
        ItemIcon(textures=TextureComponents(color="brass_lantern")),
        ItemBlockPlacer(block=block, replace_block_item=True),
    )

    block.queue()
    return block


BrassLantern = brass_lantern()
```

!!! tip "Blocks in other APIs"
    `block.descriptor(lit=True)` returns a `BlockDescriptor` with state values, accepted anywhere a vanilla `MinecraftBlockTypes.X()` is: loot tables, features, filters and recipes. To match blocks by tags only, write `BlockDescriptor(tags=Query.AllTags(["stone"]))`.
