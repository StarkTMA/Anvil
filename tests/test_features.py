import json
import pytest


def test_multi_block_feature(tmp_path, monkeypatch):
    config_file = tmp_path / "anvilconfig.json"
    config_file.write_text(
        json.dumps(
            {
                "package": {
                    "namespace": "test",
                    "project_name": "test",
                    "company": "test",
                    "display_name": "Test Project",
                    "project_description": "Test Description",
                    "behavior_description": "Test BP",
                    "resource_description": "Test RP",
                }
            }
        )
    )
    monkeypatch.chdir(tmp_path)

    from anvil.lib.config import CONFIG

    old_instance = CONFIG._instance
    CONFIG._instance = (
        None  # Reset singleton so it picks up the current dir's anvilconfig.json
    )

    try:
        from anvil.api.features import MultiBlockFeature

        feature = MultiBlockFeature(
            name="test:horizontal_log_feature",
            places_block="test:horizontal_log",
            randomize_rotation=True,
            enforce_placement_rules=True,
        )
        feature.may_replace(["minecraft:air", "minecraft:grass", "minecraft:dirt"])

        content = feature._content["minecraft:multi_block_feature"]
        assert content["description"]["identifier"] == "test:horizontal_log_feature"
        assert content["places_block"] == "test:horizontal_log"
        assert content["randomize_rotation"] is True
        assert content["enforce_placement_rules"] is True
        assert content["may_replace"] == [
            "minecraft:air",
            "minecraft:grass",
            "minecraft:dirt",
        ]
    finally:
        CONFIG._instance = old_instance


def test_tree_feature(tmp_path, monkeypatch):
    config_file = tmp_path / "anvilconfig.json"
    config_file.write_text(
        json.dumps(
            {
                "package": {
                    "namespace": "test",
                    "project_name": "test",
                    "company": "test",
                    "display_name": "Test Project",
                    "project_description": "Test Description",
                    "behavior_description": "Test BP",
                    "resource_description": "Test RP",
                }
            }
        )
    )
    monkeypatch.chdir(tmp_path)

    from anvil.lib.config import CONFIG

    old_instance = CONFIG._instance
    CONFIG._instance = None

    try:
        from anvil.api.features import TreeFeature

        tree = TreeFeature("test_tree")
        tree.may_grow_on(["minecraft:dirt", "minecraft:grass_block"])
        tree.may_replace(["minecraft:air", "minecraft:leaves"])
        tree.may_grow_through(["minecraft:dirt"])
        tree.trunk(
            trunk_block="test:custom_log",
            trunk_height=(4, 7),
        )
        tree.canopy(
            leaf_block="test:custom_leaves",
            canopy_offset_min=-3,
            canopy_offset_max=0,
            variation_chance=[(1, 2), (1, 1)],
        )

        content = tree._content["minecraft:tree_feature"]
        assert content["description"]["identifier"] == str(tree.identifier)
        assert content["may_grow_on"] == ["minecraft:dirt", "minecraft:grass_block"]
        assert content["may_replace"] == ["minecraft:air", "minecraft:leaves"]
        assert content["may_grow_through"] == ["minecraft:dirt"]
        assert content["trunk"]["trunk_block"] == "test:custom_log"
        assert content["canopy"]["leaf_block"] == "test:custom_leaves"
    finally:
        CONFIG._instance = old_instance


def test_tree_feature_trunk_types(tmp_path, monkeypatch):
    config_file = tmp_path / "anvilconfig.json"
    config_file.write_text(
        json.dumps(
            {
                "package": {
                    "namespace": "test",
                    "project_name": "test",
                    "company": "test",
                    "display_name": "Test Project",
                    "project_description": "Test Description",
                    "behavior_description": "Test BP",
                    "resource_description": "Test RP",
                }
            }
        )
    )
    monkeypatch.chdir(tmp_path)

    from anvil.lib.config import CONFIG

    old_instance = CONFIG._instance
    CONFIG._instance = None

    try:
        from anvil.api.features import TreeFeature

        # 1. trunk with tuple range and can_be_submerged
        tree1 = TreeFeature("t1").trunk(
            trunk_block="minecraft:oak_log",
            trunk_height=(4, 7),
            height_modifier=(0, 2),
            can_be_submerged=1,
        )
        assert tree1._content["minecraft:tree_feature"]["trunk"] == {
            "trunk_block": "minecraft:oak_log",
            "trunk_height": {"range_min": 4, "range_max": 7},
            "height_modifier": {"range_min": 0, "range_max": 2},
            "can_be_submerged": {"max_depth": 1},
        }

        # 2. fancy_trunk with strict plain arguments
        tree2 = TreeFeature("t2").fancy_trunk(
            trunk_block="minecraft:oak_log",
            base_height=5,
            height_variance=12,
            height_scale=0.618,
            trunk_width=1,
            width_scale=1.0,
            foliage_altitude_factor=0.3,
            branch_slope=0.381,
            branch_density=1.0,
            branch_min_altitude_factor=0.2,
        )
        assert tree2._content["minecraft:tree_feature"]["fancy_trunk"] == {
            "trunk_block": "minecraft:oak_log",
            "trunk_height": {"base": 5, "variance": 12, "scale": 0.618},
            "trunk_width": 1,
            "width_scale": 1.0,
            "foliage_altitude_factor": 0.3,
            "branches": {"slope": 0.381, "density": 1.0, "min_altitude_factor": 0.2},
        }

        # 3. acacia_trunk with strict plain arguments
        tree3 = TreeFeature("t3").acacia_trunk(
            trunk_block="minecraft:acacia_log",
            trunk_width=1,
            base_height=4,
            height_intervals=[2],
            min_height_for_canopy=3,
            allow_diagonal_growth=True,
            lean_height=(2, 3),
            lean_steps=(3, 4),
            lean_length=(1, 2),
        )
        assert tree3._content["minecraft:tree_feature"]["acacia_trunk"] == {
            "trunk_block": "minecraft:acacia_log",
            "trunk_width": 1,
            "trunk_height": {"base": 4, "intervals": [2], "min_height_for_canopy": 3},
            "trunk_lean": {
                "allow_diagonal_growth": True,
                "lean_height": {"range_min": 2, "range_max": 3},
                "lean_steps": {"range_min": 3, "range_max": 4},
                "lean_length": {"range_min": 1, "range_max": 2},
            },
            "branches": {
                "branch_chance": 0.0,
                "branch_length": {"range_min": 1, "range_max": 4},
                "branch_position": {"range_min": 1, "range_max": 3},
            },
        }

        # 4. cherry_trunk with strict plain arguments
        tree4 = TreeFeature("t4").cherry_trunk(
            trunk_block="minecraft:cherry_log",
            base_height=7,
            height_intervals=[1],
            one_branch_weight=10,
            two_branches_weight=10,
            two_branches_and_trunk_weight=10,
            branch_horizontal_length=(2, 4),
            branch_start_offset_from_top=(-4, -3),
            branch_end_offset_from_top=(-1, 0),
        )
        assert tree4._content["minecraft:tree_feature"]["cherry_trunk"] == {
            "trunk_block": "minecraft:cherry_log",
            "trunk_height": {"base": 7, "intervals": [1]},
            "branches": {
                "tree_type_weights": {
                    "one_branch": 10,
                    "two_branches": 10,
                    "two_branches_and_trunk": 10,
                },
                "branch_horizontal_length": {"range_min": 2, "range_max": 4},
                "branch_start_offset_from_top": {"range_min": -4, "range_max": -3},
                "branch_end_offset_from_top": {"range_min": -1, "range_max": 0},
            },
        }

        # 5. fallen_trunk with tuple ranges
        tree5 = TreeFeature("t5").fallen_trunk(
            trunk_block="minecraft:birch_log",
            log_length=(5, 8),
            stump_height=(1, 2),
            height_modifier=(0, 1),
            log_decoration_feature="minecraft:optional_log_mushrooms_feature",
        )
        assert tree5._content["minecraft:tree_feature"]["fallen_trunk"] == {
            "trunk_block": "minecraft:birch_log",
            "log_length": {"range_min": 5, "range_max": 8},
            "stump_height": {"range_min": 1, "range_max": 2},
            "height_modifier": {"range_min": 0, "range_max": 1},
            "log_decoration_feature": "minecraft:optional_log_mushrooms_feature",
        }

        # 6. mangrove_trunk with strict plain arguments
        tree6 = TreeFeature("t6").mangrove_trunk(
            trunk_block="minecraft:mangrove_log",
            trunk_width=1,
            base_height=2,
            height_rand_a=1,
            height_rand_b=4,
            branch_chance=100.0,
            branch_length=(0, 1),
            branch_steps=(1, 4),
        )
        assert tree6._content["minecraft:tree_feature"]["mangrove_trunk"] == {
            "trunk_block": "minecraft:mangrove_log",
            "trunk_width": 1,
            "trunk_height": {"base": 2, "height_rand_a": 1, "height_rand_b": 4},
            "branches": {
                "branch_chance": 100.0,
                "branch_length": {"range_min": 0, "range_max": 1},
                "branch_steps": {"range_min": 1, "range_max": 4},
            },
        }

        # 7. mega_trunk with strict plain arguments
        tree7 = TreeFeature("t7").mega_trunk(
            trunk_block="minecraft:jungle_log",
            trunk_width=2,
            base_height=10,
            height_intervals=[3, 20],
            height_modifier=(0, 2),
            branch_length=5,
        )
        assert tree7._content["minecraft:tree_feature"]["mega_trunk"] == {
            "trunk_block": "minecraft:jungle_log",
            "trunk_width": 2,
            "trunk_height": {"base": 10, "intervals": [3, 20]},
            "height_modifier": {"range_min": 0, "range_max": 2},
            "branches": {
                "branch_length": 5,
            },
        }

        # 8. poplar_trunk with tuple ranges
        tree8 = TreeFeature("t8").poplar_trunk(
            trunk_block="minecraft:birch_log",
            trunk_height=(8, 12),
            remaining_trunk_height_above_branches=2,
            amount_of_foliage_support_branches=3,
            height_modifier=(0, 1),
        )
        assert tree8._content["minecraft:tree_feature"]["poplar_trunk"] == {
            "trunk_block": "minecraft:birch_log",
            "trunk_height": {"range_min": 8, "range_max": 12},
            "remaining_trunk_height_above_branches": {"range_min": 2, "range_max": 2},
            "amount_of_foliage_support_branches": 3,
            "height_modifier": {"range_min": 0, "range_max": 1},
        }
    finally:
        CONFIG._instance = old_instance
