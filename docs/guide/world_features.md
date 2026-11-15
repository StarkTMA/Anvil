# Generating Features

This tutorial fills the **Ember Fields** biome from [Creating a biome](custom_biome.md) with an **ore**, scattered **lanterns** and **trees**. World generation has two halves: a **feature** describes what to place, and a **feature rule** describes where and how often. Scatter features sit in between to repeat another feature.

Every snippet compiles as written.

---

## Ore

```py title="worldgen/ember_features.py"
from anvil.lib.jsonmodel.enums import FeatureRulePlacementPass
from anvil.api.core.filters import Filter
from anvil.api.features.feature import CoordinateRange
from anvil.api.features.feature_rule import FeatureRule
from anvil.api.features.ore import OreFeature
from anvil.api.vanilla.blocks import MinecraftBlockTypes

in_ember_fields = Filter.has_biome_tag("ember_fields")

ore = OreFeature("ember_ore", count=9, discard_chance_on_air_exposure=0.3)
ore.add_replace_rule(
    MinecraftBlockTypes.Magma(),
    [MinecraftBlockTypes.Basalt(), MinecraftBlockTypes.Blackstone()],
)
ore.queue()
FeatureRule("ember_ore", ore, FeatureRulePlacementPass.UndergroundPass).biome_filter(
    in_ember_fields
).distribution(
    iterations=12,
    scatter_chance=None,
    x=CoordinateRange("uniform", (0, 16)),
    y=CoordinateRange("uniform", (-20, 40)),
    z=CoordinateRange("uniform", (0, 16)),
).queue()
```

```json
"minecraft:feature_rules": {
  "description": {"identifier": "tut:ember_ore", "places_feature": "tut:ember_ore"},
  "conditions": {"placement_pass": "underground_pass", "minecraft:biome_filter": {"test": "has_biome_tag", "value": "ember_fields"}},
  "distribution": {
    "iterations": 12,
    "x": {"distribution": "uniform", "extent": [0, 16]},
    "y": {"distribution": "uniform", "extent": [-20, 40]},
    "z": {"distribution": "uniform", "extent": [0, 16]}
  }
}
```

- `OreFeature(name, count)` places a vein of `count` blocks; each replace rule says which block is placed into which blocks.
- `FeatureRule(name, feature, placement_pass)` runs the feature per chunk. `distribution(iterations, scatter_chance, x, y, z)` says how many tries and where: a number, a Molang string or a `CoordinateRange(distribution, extent)`.
- A biome filter is a `Filter`, the same ones spawn rules use.

---

## Scattered Blocks

A single-block feature places one block with attachment rules. A scatter feature repeats it, and the feature rule places the scatter.

```py title="lanterns"
from anvil.lib.jsonmodel.enums import BlockFaceValues
from anvil.api.features.scatter import ScatterFeature
from anvil.api.features.single_block import SingleBlockFeature

lantern = SingleBlockFeature("ember_lantern", enforce_placement_rules=True)
lantern.place_block("tut:brass_lantern")
lantern.may_attach_to(
    BlockFaceValues.Down, [MinecraftBlockTypes.Basalt(), MinecraftBlockTypes.Blackstone()]
)
lantern.queue()

lanterns = ScatterFeature("ember_lanterns", lantern, project_input_to_floor=True)
lanterns.distribution(
    iterations=3,
    scatter_chance=(1, 6),
    x=CoordinateRange("uniform", (0, 16)),
    y=64,
    z=CoordinateRange("uniform", (0, 16)),
)
lanterns.queue()
FeatureRule(
    "ember_lanterns", lanterns, FeatureRulePlacementPass.SurfacePass
).biome_filter(in_ember_fields).distribution(
    iterations=1, scatter_chance=None, x=0, y="query.heightmap(0, 0)", z=0
).queue()
```

```json
"minecraft:scatter_feature": {
  "description": {"identifier": "tut:ember_lanterns"},
  "places_feature": "tut:ember_lantern",
  "project_input_to_floor": true,
  "distribution": {
    "iterations": 3,
    "scatter_chance": {"numerator": 1, "denominator": 6},
    "x": {"distribution": "uniform", "extent": [0, 16]},
    "y": 64,
    "z": {"distribution": "uniform", "extent": [0, 16]}
  }
}
```

!!! note
    `scatter_chance` is a percentage, a `(numerator, denominator)` fraction or a Molang string; `None` means always. `project_input_to_floor` drops the scatter's start position to the ground, so the lanterns land on the surface wherever `y=64` was.

!!! tip "Custom blocks in features"
    A feature takes your blocks as `"namespace:name"` strings or as `block.descriptor(lit=True)` with state values.

---

## Trees

```py title="trees"
from anvil.api.features.tree import TreeFeature
from anvil.api.vanilla.biomes import MinecraftBiomeTags

tree = TreeFeature("ashen_tree")
tree.base_block(MinecraftBlockTypes.Dirt())
tree.may_grow_on([MinecraftBlockTypes.Basalt(), MinecraftBlockTypes.Dirt()])
tree.trunk(MinecraftBlockTypes.DarkOakLog(), trunk_height=(5, 9))
tree.spruce_canopy(MinecraftBlockTypes.DarkOakLeaves(), max_radius=(2, 4))
tree.queue()
FeatureRule("ashen_trees", tree, FeatureRulePlacementPass.SurfacePass).biome_filter(
    Filter.all_of([in_ember_fields, Filter.has_biome_tag(MinecraftBiomeTags.Overworld)])
).distribution(
    iterations=2,
    scatter_chance=(1, 4),
    x=CoordinateRange("uniform", (0, 16)),
    y="query.heightmap(variable.x, variable.z)",
    z=CoordinateRange("uniform", (0, 16)),
).queue()
```

A tree is one trunk builder (`trunk`, `fancy_trunk`, `mega_trunk`, `cherry_trunk`, `mangrove_trunk`...) plus one canopy builder (`canopy`, `spruce_canopy`, `fancy_canopy`, `mega_pine_canopy`...), with optional `trunk_decoration`, `canopy_decoration` and `mangrove_roots`.

!!! tip "Other features"
    `anvil.api.features` also has `AggregateFeature` (several features at one spot), `SequenceFeature`, `WeightedRandomFeature`, `SearchFeature`, `GeodeFeature`, `VegetationPatchFeature`, `StructureTemplateFeature` and more; they combine the same way. Jigsaw structures are in [Using Jigsaw](using_jigsaw.md).

---

## Full Example

```py title="worldgen/ember_features.py"
from anvil.lib.jsonmodel.enums import BlockFaceValues, FeatureRulePlacementPass
from anvil.api.core.filters import Filter
from anvil.api.features.feature import CoordinateRange
from anvil.api.features.feature_rule import FeatureRule
from anvil.api.features.ore import OreFeature
from anvil.api.features.scatter import ScatterFeature
from anvil.api.features.single_block import SingleBlockFeature
from anvil.api.features.tree import TreeFeature
from anvil.api.vanilla.biomes import MinecraftBiomeTags
from anvil.api.vanilla.blocks import MinecraftBlockTypes


def ember_features():
    in_ember_fields = Filter.has_biome_tag("ember_fields")

    ore = OreFeature("ember_ore", count=9, discard_chance_on_air_exposure=0.3)
    ore.add_replace_rule(
        MinecraftBlockTypes.Magma(),
        [MinecraftBlockTypes.Basalt(), MinecraftBlockTypes.Blackstone()],
    )
    ore.queue()
    FeatureRule("ember_ore", ore, FeatureRulePlacementPass.UndergroundPass).biome_filter(
        in_ember_fields
    ).distribution(
        iterations=12,
        scatter_chance=None,
        x=CoordinateRange("uniform", (0, 16)),
        y=CoordinateRange("uniform", (-20, 40)),
        z=CoordinateRange("uniform", (0, 16)),
    ).queue()

    lantern = SingleBlockFeature("ember_lantern", enforce_placement_rules=True)
    lantern.place_block("tut:brass_lantern")
    lantern.may_attach_to(
        BlockFaceValues.Down, [MinecraftBlockTypes.Basalt(), MinecraftBlockTypes.Blackstone()]
    )
    lantern.queue()

    lanterns = ScatterFeature("ember_lanterns", lantern, project_input_to_floor=True)
    lanterns.distribution(
        iterations=3,
        scatter_chance=(1, 6),
        x=CoordinateRange("uniform", (0, 16)),
        y=64,
        z=CoordinateRange("uniform", (0, 16)),
    )
    lanterns.queue()
    FeatureRule(
        "ember_lanterns", lanterns, FeatureRulePlacementPass.SurfacePass
    ).biome_filter(in_ember_fields).distribution(
        iterations=1, scatter_chance=None, x=0, y="query.heightmap(0, 0)", z=0
    ).queue()

    tree = TreeFeature("ashen_tree")
    tree.base_block(MinecraftBlockTypes.Dirt())
    tree.may_grow_on([MinecraftBlockTypes.Basalt(), MinecraftBlockTypes.Dirt()])
    tree.trunk(MinecraftBlockTypes.DarkOakLog(), trunk_height=(5, 9))
    tree.spruce_canopy(MinecraftBlockTypes.DarkOakLeaves(), max_radius=(2, 4))
    tree.queue()
    FeatureRule("ashen_trees", tree, FeatureRulePlacementPass.SurfacePass).biome_filter(
        Filter.all_of([in_ember_fields, Filter.has_biome_tag(MinecraftBiomeTags.Overworld)])
    ).distribution(
        iterations=2,
        scatter_chance=(1, 4),
        x=CoordinateRange("uniform", (0, 16)),
        y="query.heightmap(variable.x, variable.z)",
        z=CoordinateRange("uniform", (0, 16)),
    ).queue()


ember_features()
```
