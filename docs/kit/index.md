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

create_wood_set("rotten", tree=my_tree)                      # everything; saplings grow `my_tree`
create_wood_set("rotten", WoodBlock.SAPLING)                 # everything but saplings: no tree needed
create_wood_set("rotten", WoodBlock.DOOR, tree=my_tree)      # everything but doors
create_wood_set("rotten", own_creative_group=True, tree=my_tree)  # in its own creative group

wood = create_wood_set("rotten", tree=my_tree)
block, item = wood["planks"]                                # each part is a (block, item) pair
```

A set with saplings needs `tree`, the feature they grow into (a `Feature`, its identifier, or a function that builds it from the finished set: `tree=lambda wood: make_tree(wood["log"].block, wood["leaves"].block)`); the kit makes no trees. Build and queue it yourself: it can use the set's blocks by their identifiers (`<namespace>:<name>_log`, `<namespace>:<name>_leaves` with its `natural` state on).

### World

- **`anvil.kit.world.potionsAPI`**: potion variants (drinkable, splash, lingering) and brewing recipes.
- **`anvil.kit.world.ldtk`**: builds a Minecraft world from an [LDtk](https://ldtk.io) map. Needs the `ldtk` extra.

### Actors

- **`anvil.kit.actors.components`**: a custom projectile item component.
- **`anvil.kit.actors.materials`**: an entity outline material.

## The `WoodSet` class

`create_wood_set` covers the simple case. For anything more, build the set with the class:

```python
palm = (
    WoodSet("palm", exclude=WoodBlock.CHEST_BOAT)
    .tree(lambda wood: make_palm(wood["log"].block, wood["leaves"].block))
    .leaf_drop(coconut, 0.02)  # drops when the leaves are broken (no shears) or decay
    .build()
)
palm["planks"].block
```

- `tree` is a feature, its identifier, or a function receiving the set once its blocks exist.  Once built, `palm.tree_feature` is the resolved feature.
- `leaf_drop(item, chance, count=1)` takes an `Item` or an identifier like `minecraft:apple`.
