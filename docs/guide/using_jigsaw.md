# Using Jigsaw Structures

This guide explains how to generate complex, procedural structures using **Jigsaw Blocks**, similar to Minecraft's villages or bastions. We will stick to the patterns used in complex addon projects.

The system consists of three main parts:

1. **Processors**: Rules for how blocks behave during placement (e.g., ignoring air, replacing water).
2. **Template Pools**: Collections of structure files (`.mcstructure`) that can spawn.
3. **Structure Sets**: The top-level definition that controls where and how the structures generate in the world.

---

## 1. Processors

Processors allow you to modify blocks as they are placed. For example, you might want a path to replace grass but not air.

```python title="world/structures.py"
from anvil.api.world.structures import _JigsawStructureProcess
from anvil.api.vanilla.blocks import MinecraftBlockTypes

# Create a processor that prevents structure air from overwriting world blocks
# and ensures paths replace dirt correctly.
def create_path_processor():
    processor = _JigsawStructureProcess("ignore_air")

    # Don't replace existing blocks with Structure Void/Air
    processor.add_block_ignore_processor([MinecraftBlockTypes.Air()])

    # Rule: Turn Grass Path -> Dirt when placed on top of certain blocks
    processor.add_block_rule(MinecraftBlockTypes.GrassPath()).input_predicate.block_state_match(
        MinecraftBlockTypes.Dirt()
    )
    return processor

ignore_air = create_path_processor()
```

---

## 2. Template Pools

Pools are groups of structure elements. You often have a "start" pool and then subsequent pools like "corridors", "rooms", or "loot_rooms".

```python
from anvil.api.world.structures import JigsawStructureTemplatePool

pools = []

def dungeon_start_pool():
    # The name "dungeon_start" corresponds to the pool name referenced in Jigsaw blocks
    # Note: In the jigsaw block, you must use a unique NAMESPACE:POOL_NAME. Anvil will automaticall use the namespace of the addon.
    pool = JigsawStructureTemplatePool("dungeon_start")

    # Add an element pointing to world/structures/dungeon/start.mcstructure
    # We apply the processor we created earlier
    pool.add_structure_element("dungeon/start", ignore_air)

    pools.append(pool)
    return pool

def rooms_pool():
    pool = JigsawStructureTemplatePool("dungeon_rooms")

    # Add multiple variants with different weights
    pool.add_structure_element("dungeon/room_large", ignore_air, weight=10)
    pool.add_structure_element("dungeon/room_small", ignore_air, weight=5)

    pools.append(pool)
    return pool
```

---

## 3. Structure Sets

The **Structure Set** ties everything together. It defines the generation rules (biomes, spacing) and the starting point.

```python
from anvil.api.world.structures import JigsawStructureSet
from anvil.api.vanilla.biomes import MinecraftBiomeTags
from anvil.api.actors.components import Filter

def generate_dungeon():
    # 1. Initialize pools
    start = dungeon_start_pool()
    rooms_pool()

    # 2. Create the set
    # separation=4, spacing=10 means structures are 4-10 chunks apart
    dungeon_set = JigsawStructureSet("my_dungeon", separation=4)

    # 3. Add the main structure configuration
    main_structure = dungeon_set.add_jigsaw_structure(
        "my_dungeon_structure",
        start_pool=start,            # Start with this pool
        max_depth=4,                 # How far out to branch
        start_height=30,             # Y level (underground)
        placement_step="underground_structures",
        start_height_from_sea=False,
    )

    # 4. Add Biome Filters
    main_structure.add_biome_filters(
        Filter.any_of(
            Filter.has_biome_tag(MinecraftBiomeTags.Plains),
            Filter.has_biome_tag(MinecraftBiomeTags.Forest)
        )
    )

    # 6. Queue everything
    for pool in pools:
        pool.queue()
    dungeon_set.queue()
```

---

## Full Workflow

1.  **Design in Game**: Build your structures and save them with Jigsaw blocks.
    - Set the **Target Pool** in Jigsaw blocks to match your pool names (e.g., `my_namespace:dungeon_rooms`).
    - Save `.mcstructure` files to `world/structures/<category>/<name>.mcstructure`.
2.  **Define in Python**: Use the code above to register your pools and sets.
3.  **Run**: Anvil will export the structure set, which the game uses to generate your dungeon.

!!! tip "Linking Pools"
In your Jigsaw Block inside Minecraft: - **Target Pool**: `my_namespace:dungeon_rooms` (matches `JigsawStructureTemplatePool("dungeon_rooms")` + implicit namespace) - **Name**: `connector_a` (matches the name you connect to) - **Target Name**: `connector_a` (connection point on the other piece)
