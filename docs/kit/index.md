# Kit

`anvil.kit` holds ready-made content built on top of the [API](../api/index.md): call one function and get a complete, working feature such as a full wood set.

!!! warning "Stability"
    The kit is opinionated and may change between minor versions of Anvil: names, parameters and the content it generates can all change. Pin your Anvil version if you depend on a kit's exact output.

    The [API](../api/index.md) (`anvil.api`) is the stable layer. If you need full control or long-term stability, build on the API directly and use the kit as a reference.

## Optional dependencies

Some kits need packages that a plain `pip install mcanvil` doesn't include. Install them through the matching extra:

| Kit | Extra | Install |
| --- | --- | --- |
| `anvil.kit.world.ldtk` | `ldtk` (Amulet) | `pip install mcanvil[ldtk]` |

Importing a kit without its extra raises an `ImportError` naming the command to run.

## Available kits

### Blocks

- **`anvil.kit.blocks.wood_set`**: a complete wood set (planks, logs, wood, slabs, stairs, fences, gates, doors, trapdoors, buttons, pressure plates, signs (standing and wall in one block), hanging signs, boats and chest boats) with recipes, vanilla wood tags, fuel values, creative inventory placement and the TypeScript components they need.

```python
from anvil.kit.blocks.wood_set import WoodBlock, create_wood_set

create_wood_set("rotten")                                    # everything
create_wood_set("rotten", WoodBlock.DOOR)                    # everything but doors
create_wood_set("rotten", own_creative_group=True)           # in its own creative group
```

### World

- **`anvil.kit.world.potionsAPI`**: potion variants (drinkable, splash, lingering) and brewing recipes.
- **`anvil.kit.world.ldtk`**: builds a Minecraft world from an [LDtk](https://ldtk.io) map. Needs the `ldtk` extra.

### Actors

- **`anvil.kit.actors.components`**: a custom projectile item component.
- **`anvil.kit.actors.materials`**: an entity outline material.
