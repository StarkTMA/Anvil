"""Tests for the typed feature and feature rule files."""

import pytest

from anvil.api.core.enums import BlockFaceValues, FeatureRulePlacementPass
from anvil.api.core.filters import Filter
from anvil.api.features import (
    AggregateFeature,
    CoordinateRange,
    Feature,
    FeatureRule,
    GeodeFeature,
    GrowingPlantFeature,
    MultiBlockFeature,
    OreFeature,
    ScatterFeature,
    SearchFeature,
    SingleBlockFeature,
    SnapToSurfaceFeature,
    StructureTemplateFeature,
    TreeFeature,
    WeightedRandomFeature,
)
from anvil.lib.lib import AnvilIO
from anvil.lib.schemas import MinecraftBlockDescriptor

jsonschema = pytest.importorskip("jsonschema")


def _json(value):
    return AnvilIO._normalize_json_like(value)


def _check(feature):
    schema = type(feature).__schema__()
    jsonschema.Draft202012Validator.check_schema(schema)
    exported = _json(feature._content)
    jsonschema.validate(exported, schema, cls=jsonschema.Draft202012Validator)
    return exported


def _body(feature):
    exported = _check(feature)
    key = next(key for key in exported if key != "format_version")
    return exported[key]


def test_feature_base_cannot_be_created():
    with pytest.raises(TypeError):
        Feature("nothing")


def test_single_block_feature():
    feature = SingleBlockFeature("flower", randomize_rotation=True)
    feature.place_block("minecraft:poppy").place_block(
        MinecraftBlockDescriptor("minecraft:dandelion", True, states={"a": 1}), 3
    )
    feature.may_replace(["minecraft:air"])
    feature.may_attach_to(BlockFaceValues.Down, ["minecraft:grass_block"])
    feature.may_attach_to(BlockFaceValues.Side, ["minecraft:stone"], auto_rotate=None)
    feature.may_not_attach_to("diagonal", ["minecraft:water"])

    body = _body(feature)
    assert body["description"] == {"identifier": "test:flower"}
    assert body["places_block"] == [
        {"block": "minecraft:poppy", "weight": 1.0},
        {"block": {"name": "minecraft:dandelion", "states": {"a": 1}}, "weight": 3},
    ]
    assert body["may_attach_to"] == {
        "bottom": ["minecraft:grass_block"],
        "sides": ["minecraft:stone"],
        "min_sides_must_attach": 1,
        "auto_rotate": False,
    }
    assert body["may_not_attach_to"] == {"diagonal": ["minecraft:water"]}
    assert body["enforce_placement_rules"] is False
    assert body["randomize_rotation"] is True


def test_single_block_feature_needs_a_block():
    with pytest.raises(ValueError):
        _json(SingleBlockFeature("empty")._content)


def test_scatter_feature_and_rule_distribution():
    flower = SingleBlockFeature("flower").place_block("minecraft:poppy")
    spread = CoordinateRange("uniform", (-4, 4))
    scatter = ScatterFeature("flowers", flower).distribution(
        "math.random_integer(1, 3)", None, spread, 0, spread, "xzy"
    )
    assert _body(scatter) == {
        "description": {"identifier": "test:flowers"},
        "places_feature": "test:flower",
        "project_input_to_floor": False,
        "distribution": {
            "iterations": "math.random_integer(1, 3)",
            "coordinate_eval_order": "xzy",
            "x": {"distribution": "uniform", "extent": [-4, 4]},
            "y": 0,
            "z": {"distribution": "uniform", "extent": [-4, 4]},
        },
    }

    rule = FeatureRule("flowers_rule", scatter, FeatureRulePlacementPass.SurfacePass)
    rule.biome_filter([Filter.has_biome_tag("plains")])
    rule.distribution(
        1,
        (1, 4),
        CoordinateRange("fixed_grid", (0, 15), step_size=4),
        "q.heightmap(v.worldx, v.worldz)",
        0,
    )
    exported = _check(rule)
    rules = exported["minecraft:feature_rules"]
    assert rules["description"] == {
        "identifier": "test:flowers_rule",
        "places_feature": "test:flowers",
    }
    assert rules["conditions"]["placement_pass"] == "surface_pass"
    assert rules["conditions"]["minecraft:biome_filter"][0]["test"] == "has_biome_tag"
    assert rules["distribution"]["scatter_chance"] == {"numerator": 1, "denominator": 4}
    assert rules["distribution"]["x"]["step_size"] == 4


def test_scatter_feature_needs_a_distribution():
    with pytest.raises(ValueError):
        _json(ScatterFeature("flowers", "test:flower")._content)


def test_coordinate_range_grid_options_need_a_grid():
    with pytest.raises(ValueError):
        _json(CoordinateRange("uniform", (0, 15), step_size=4))
    with pytest.raises(ValueError):
        _json(CoordinateRange("sideways", (0, 15)))


def test_scatter_chance_denominator_must_be_positive():
    rule = FeatureRule("rule", "test:flower", FeatureRulePlacementPass.FirstPass)
    rule.distribution(1, (1, 0), 0, 0, 0)
    with pytest.raises(ValueError):
        _json(rule._content)


def test_feature_lists():
    aggregate = (
        AggregateFeature("both").features(["test:a", "test:b"]).early_out("none")
    )
    assert _body(aggregate)["features"] == ["test:a", "test:b"]
    with pytest.raises(ValueError):
        _json(AggregateFeature("none")._content)

    weighted = (
        WeightedRandomFeature("pick").add_feature("test:a", 2).features([("test:b", 1)])
    )
    assert _body(weighted)["features"] == [["test:a", 2], ["test:b", 1]]


def test_values_raise_instead_of_being_clamped():
    with pytest.raises(ValueError):
        _json(OreFeature("ore", 0)._content)
    with pytest.raises(ValueError):
        _json(SnapToSurfaceFeature("snap", "test:a", 8, surface="sideways")._content)


def test_ore_and_search_features():
    ore = OreFeature("ore", 8).add_replace_rule(
        "minecraft:coal_ore", ["minecraft:stone"]
    )
    assert _body(ore)["replace_rules"] == [
        {"places_block": "minecraft:coal_ore", "may_replace": ["minecraft:stone"]}
    ]

    search = SearchFeature("search", "test:a", "+y", (0, 0, 0), (0, 8, 0))
    assert _body(search)["search_volume"] == {"min": [0, 0, 0], "max": [0, 8, 0]}
    search.search_volume((0, 9, 0), (0, 8, 0))
    with pytest.raises(ValueError):
        _json(search._content)


def test_structure_template_constraints_are_kept_when_empty():
    feature = StructureTemplateFeature("hut", "test:hut", 4, "random")
    feature.grounded().unburied().leveled().block_allowlist(["minecraft:air"])
    assert _body(feature)["constraints"] == {
        "grounded": {},
        "unburied": {},
        "leveled": {},
        "block_intersection": {"block_allowlist": ["minecraft:air"]},
    }


def test_multi_block_and_growing_plant():
    feature = MultiBlockFeature("log", "test:horizontal_log", True, True)
    feature.may_replace(["minecraft:air"])
    assert _body(feature) == {
        "description": {"identifier": "test:log"},
        "places_block": "test:horizontal_log",
        "enforce_placement_rules": True,
        "randomize_rotation": True,
        "may_replace": ["minecraft:air"],
    }

    vine = GrowingPlantFeature("vine", "DOWN", age=(17, 26))
    vine.add_height((1, 13), 2).add_body_block("minecraft:cave_vines", 4)
    vine.add_head_block("minecraft:cave_vines", 4)
    body = _body(vine)
    assert body["height_distribution"] == [[{"range_min": 1, "range_max": 13}, 2]]
    assert body["age"] == {"range_min": 17, "range_max": 26}


def test_geode_ranges_raise():
    options = dict(
        filler="minecraft:air",
        inner_layer="minecraft:amethyst_block",
        alternate_inner_layer="minecraft:budding_amethyst",
        middle_layer="minecraft:calcite",
        outer_layer="minecraft:smooth_basalt",
        min_outer_wall_distance=4,
        max_outer_wall_distance=7,
        min_distribution_points=3,
        max_distribution_points=5,
        min_point_offset=1,
        max_point_offset=3,
        max_radius=16,
        crack_point_offset=2,
        generate_crack_chance=0.95,
        base_crack_size=2,
        noise_multiplier=0.025,
        use_potential_placements_chance=0.35,
        use_alternate_layer0_chance=0.083,
        placements_require_layer0_alternate=True,
        invalid_blocks_threshold=1,
    )
    assert _body(GeodeFeature("geode", **options))["max_radius"] == 16
    with pytest.raises(ValueError):
        _json(GeodeFeature("bad", **(options | {"generate_crack_chance": 2}))._content)


def test_tree_feature():
    tree = TreeFeature("tree")
    tree.may_grow_on(["minecraft:dirt"]).may_replace(["minecraft:air"])
    tree.trunk(
        "test:log", trunk_height=(4, 7), height_modifier=(0, 2), can_be_submerged=1
    )
    tree.trunk_decoration((1, 4), "minecraft:vine", 2, "down")
    tree.canopy(
        "test:leaves",
        canopy_offset_min=-3,
        canopy_offset_max=0,
        variation_chance=[(1, 2), 1.0],
    )
    body = _body(tree)
    assert body["trunk"] == {
        "trunk_block": "test:log",
        "trunk_height": {"range_min": 4, "range_max": 7},
        "height_modifier": {"range_min": 0, "range_max": 2},
        "can_be_submerged": {"max_depth": 1},
        "trunk_decoration": {
            "decoration_chance": {"numerator": 1, "denominator": 4},
            "decoration_block": "minecraft:vine",
            "num_steps": 2,
            "step_direction": "down",
        },
    }
    assert body["canopy"] == {
        "canopy_offset": {"min": -3, "max": 0},
        "variation_chance": [{"numerator": 1, "denominator": 2}, 1.0],
        "leaf_block": "test:leaves",
    }


def test_tree_has_one_trunk_and_needs_one():
    with pytest.raises(ValueError):
        _json(TreeFeature("bare")._content)
    tree = TreeFeature("tree").trunk("test:log").fancy_trunk("test:log")
    body = _body(tree)
    assert "trunk" not in body and "fancy_trunk" in body


def test_tree_branch_canopies_follow_the_trunk_in_any_order():
    tree = TreeFeature("cherry")
    tree.cherry_canopy("test:leaves", height=5)
    tree.cherry_trunk("test:log")
    tree.branch_fancy_canopy("test:leaves", height=2)
    body = _body(tree)
    branch_canopy = body["cherry_trunk"]["branches"]["branch_canopy"]
    assert branch_canopy["cherry_canopy"]["height"] == {"range_min": 5, "range_max": 5}
    assert branch_canopy["fancy_canopy"]["height"] == 2
    assert body["cherry_canopy"] == branch_canopy["cherry_canopy"]


@pytest.mark.parametrize(
    "build",
    [
        lambda tree: tree.acacia_trunk("test:log", height_intervals=[2]).acacia_canopy(
            "test:leaves"
        ),
        lambda tree: tree.fallen_trunk("test:log", stump_height=1),
        lambda tree: tree.mangrove_trunk("test:log")
        .mangrove_canopy(["test:leaves", ("test:flowers", 2)])
        .mangrove_roots("test:roots", above_root_chance=(1, 2)),
        lambda tree: tree.mega_trunk(
            "test:log", branch_altitude_factor=(0.2, 0.5)
        ).mega_canopy("test:leaves"),
        lambda tree: tree.poplar_trunk("test:log").poplar_canopy(
            "test:leaves", radius=[(2, 1)]
        ),
        lambda tree: tree.trunk("test:log", 5).roofed_canopy("test:leaves"),
        lambda tree: tree.trunk("test:log").spruce_canopy("test:leaves"),
        lambda tree: tree.trunk("test:log").pine_canopy("test:leaves"),
        lambda tree: tree.trunk("test:log").mega_pine_canopy("test:leaves"),
        lambda tree: tree.trunk("test:log").random_spread_canopy(["test:leaves"]),
    ],
)
def test_tree_trunks_and_canopies_match_the_schema(build):
    tree = TreeFeature("tree")
    build(tree)
    _check(tree)


def test_tree_cherry_trunk_base_must_be_two():
    tree = TreeFeature("tree").cherry_trunk("test:log", base_height=1)
    with pytest.raises(ValueError):
        _json(tree._content)
