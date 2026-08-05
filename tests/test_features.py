import json
import pytest


def test_multi_block_feature(tmp_path, monkeypatch):
    config_file = tmp_path / "anvilconfig.json"
    config_file.write_text(json.dumps({
        "package": {
            "namespace": "test",
            "project_name": "test",
            "company": "test",
            "display_name": "Test Project",
            "project_description": "Test Description",
            "behavior_description": "Test BP",
            "resource_description": "Test RP",
        }
    }))
    monkeypatch.chdir(tmp_path)

    from anvil.lib.config import CONFIG
    old_instance = CONFIG._instance
    CONFIG._instance = None  # Reset singleton so it picks up the current dir's anvilconfig.json

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
        assert content["may_replace"] == ["minecraft:air", "minecraft:grass", "minecraft:dirt"]
    finally:
        CONFIG._instance = old_instance
