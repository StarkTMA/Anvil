# Spawn Rules and Loot

This tutorial gives an **Ember Moth**, a small flying mob, natural **spawn rules** and a **loot table**. The moth is also used in [Particles and sounds](particles_and_sounds.md); the full entity is at the end of that page. Read [Adding a Custom Entity](adding_entity.md) first.

Every snippet compiles as written.

---

## A Flying Mob

```py title="entities/ember_moth.py"
from anvil.api.actors.components import (
    EntityAIRandomHover,
    EntityCollisionBox,
    EntityDespawn,
    EntityFireImmune,
    EntityFlyingSpeed,
    EntityHealth,
    EntityMovementBasic,
    EntityNavigationFly,
    EntityPhysics,
    EntityTypeFamily,
)
from anvil.api.actors.entity import Entity

entity = Entity("ember_moth")
server = entity.server

server.components.add(
    EntityCollisionBox(width=0.5, height=0.4),
    EntityPhysics(has_collision=True, has_gravity=False),
    EntityHealth(value=6, max=6),
    EntityTypeFamily(family=["ember_moth", "ambient", "mob"]),
    EntityFireImmune(),
    EntityFlyingSpeed(value=0.15),
    EntityMovementBasic(),
    EntityNavigationFly(can_path_from_air=True),
    EntityAIRandomHover(priority=1, hover_height=(2, 6), xz_dist=8, y_dist=6),
    EntityDespawn(despawn_from_distance=(32, 64)),
)
```

!!! note
    A flyer needs `has_gravity=False`, a flying speed, a fly navigation and a goal that moves it. `EntityDespawn` keeps the world from filling up with moths.

---

## Loot Table

```py title="loot table"
from anvil.api.actors.components import EntityLoot
from anvil.api.vanilla.items import MinecraftItemTypes
from anvil.api.world.loot_tables import LootTable


def ember_moth_loot():
    table = LootTable("ember_moth")
    pool = table.pool(rolls=1)
    pool.entry("tut:ember_dust", count=1, weight=4)
    pool.entry(MinecraftItemTypes.Gunpowder(), count=1, weight=1)
    pool.entry(None, weight=2)

    rare = table.pool(rolls=1)
    rare.conditions.killed_by_player().random_chance_with_looting(0.05, 0.02)
    rare.entry(MinecraftItemTypes.BlazePowder(), count=1)
    table.queue()
    return table


server.components.add(EntityLoot(table=ember_moth_loot()))
```

```json
{
  "pools": [
    {
      "rolls": 1,
      "entries": [
        {"type": "item", "name": "tut:ember_dust", "count": 1, "weight": 4},
        {"type": "item", "name": "minecraft:gunpowder", "count": 1, "weight": 1},
        {"type": "empty", "count": 1, "weight": 2}
      ]
    },
    {
      "rolls": 1,
      "conditions": [
        {"condition": "killed_by_player"},
        {"condition": "random_chance_with_looting", "chance": 0.05, "looting_multiplier": 0.02}
      ],
      "entries": [{"type": "item", "name": "minecraft:blaze_powder", "count": 1, "weight": 1}]
    }
  ]
}
```

- `table.pool(rolls)` adds a pool; `rolls` can be a `(min, max)` tuple.
- `pool.entry(item, count, weight)` takes an item, a block, a string identifier, another `LootTable` or `None` for an empty entry.
- `pool.conditions` has the loot conditions (`killed_by_player`, `random_chance`, `match_tool`, ...).
- `entry.functions` has the loot functions: `entry.functions.SetCount((2, 5))`, `.EnchantWithLevels((20, 30), treasure=True)`, `.SetName("...")` and so on.
- Blocks use the same tables: `BlockLootTable(value=table)`.

!!! tip "Where the file goes"
    The table exports to `loot_tables/<namespace>/ember_moth.loot_table.json`. `EntityLoot(table=...)` accepts the `LootTable` object or a path string.

---

## Spawn Rules

Every entity server has a spawn rule. Each `add_condition` starts a new condition block; a mob spawns when **all** parts of a block pass.

```py title="spawn rules"
from anvil.lib.jsonmodel.enums import Difficulty, Population
from anvil.api.core.filters import Filter
from anvil.api.vanilla.biomes import MinecraftBiomeTags
from anvil.api.vanilla.blocks import MinecraftBlockTypes

spawn = server.spawn_rule
spawn.description.set_population_control(Population.Ambient)
spawn.add_condition.spawns_on_surface().brightness_filter(0, 7).weight(8).herd(
    2, 5
).biome_filter(
    [
        Filter.any_of(
            [
                Filter.has_biome_tag(MinecraftBiomeTags.Savanna),
                Filter.has_biome_tag(MinecraftBiomeTags.Mesa),
            ]
        )
    ]
).spawns_above_block_filter([MinecraftBlockTypes.Magma()], distance=4)
spawn.add_condition.spawns_underground().difficulty_filter(
    Difficulty.Easy, Difficulty.Hard
).weight(2).biome_filter([Filter.has_biome_tag(MinecraftBiomeTags.Nether)])

entity.set_display_name("Ember Moth", "Ember Moth Egg").queue("ambient")
```

```json
"conditions": [
  {
    "minecraft:spawns_on_surface": {},
    "minecraft:brightness_filter": {"min": 0, "max": 7, "adjust_for_weather": true},
    "minecraft:weight": {"default": 8},
    "minecraft:herd": [{"min_size": 2, "max_size": 5}],
    "minecraft:biome_filter": [{"any_of": [{"test": "has_biome_tag", "value": "savanna"}, {"test": "has_biome_tag", "value": "mesa"}]}],
    "minecraft:spawns_above_block_filter": {"blocks": ["minecraft:magma"], "distance": 4}
  },
  {
    "minecraft:spawns_underground": {},
    "minecraft:difficulty_filter": {"min": "easy", "max": "hard"},
    "minecraft:weight": {"default": 2},
    "minecraft:biome_filter": [{"test": "has_biome_tag", "value": "nether"}]
  }
]
```

!!! note
    `biome_filter` takes a **list** of filters. The other builders are `height_filter`, `distance_filter`, `density_limit`, `delay_filter`, `spawns_on_block_filter`, `spawns_underwater`, `spawns_in_lava`, `permute_type`, `player_in_village_filter`, `world_age_filter` and `spawn_event`.

!!! tip "No natural spawning"
    Skip `spawn_rule` and call `entity.server.description.config(is_spawnable=False)` for a mob that only appears through commands or scripts.
