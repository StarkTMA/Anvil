"""Tests for cross-platform support and local_export flag."""
import json
import os
import sys
import pytest
from unittest.mock import patch

from anvil.lib.config import _AnvilConfig, Config, ConfigOption, ConfigSection
from anvil.cli_commands.clear_cmd import get_project_dev_pack_paths
from anvil.cli_commands.init_cmd import handle_configuration
from anvil.api.core.core import clean_old_dev
from anvil.lib.lib import RELEASE_COM_MOJANG, PREVIEW_COM_MOJANG, validate_platform


@pytest.fixture(autouse=True)
def reset_anvil_config():
    """Reset the _AnvilConfig singleton before and after each test."""
    _AnvilConfig._instance = None
    yield
    _AnvilConfig._instance = None


@pytest.fixture
def make_project(tmp_path, monkeypatch):
    """Factory fixture to create an anvilconfig.json in tmp_path."""
    def _create(local_export=None, preview=False):
        data = {
            "package": {
                "namespace": "test_ns",
                "project_name": "test_proj",
                "company": "TestCo",
                "display_name": "Test Project",
                "project_description": "desc",
                "behavior_description": "bp",
                "resource_description": "rp",
                "target": "world",
            },
            "build": {
                "release": "1.0.0",
                "rp_uuid": ["00000000-0000-0000-0000-000000000001"],
                "bp_uuid": ["00000000-0000-0000-0000-000000000002"],
                "pack_uuid": "00000000-0000-0000-0000-000000000003",
                "data_module_uuid": "00000000-0000-0000-0000-000000000004",
            },
            "anvil": {
                "debug": False,
                "scriptapi": False,
                "scriptui": False,
                "pbr": False,
                "random_seed": False,
                "pascal_project_name": "TP",
                "last_check": "2099-01-01 00:00:00",
                "experimental": False,
                "preview": preview,
                "entry_point": "scripts/python/main.py",
                "minify": False,
                "add_stamp": True,
            },
            "minecraft": {
                "vanilla_version": "1.21.0",
            },
        }
        if local_export is not None:
            data["anvil"]["local_export"] = local_export

        cfg_path = tmp_path / "anvilconfig.json"
        cfg_path.write_text(json.dumps(data, indent=4))
        monkeypatch.chdir(tmp_path)
        return tmp_path

    return _create


def test_validate_platform():
    """Only Windows, macOS, and Linux are supported."""
    with patch("sys.platform", "win32"):
        validate_platform()
    with patch("sys.platform", "darwin"):
        validate_platform()
    with patch("sys.platform", "linux"):
        validate_platform()
    with patch("sys.platform", "linux2"):
        validate_platform()

    with patch("sys.platform", "android"):
        with pytest.raises(OSError, match="only supports Windows, macOS, and Linux"):
            validate_platform()
    with patch("sys.platform", "freebsd"):
        with pytest.raises(OSError, match="only supports Windows, macOS, and Linux"):
            validate_platform()


def test_windows_local_export_false_defaults_to_mojang(make_project, monkeypatch):
    """On Windows when local_export is false, export to default com.mojang paths."""
    make_project(local_export=False, preview=False)
    monkeypatch.setattr(sys, "platform", "win32")

    with patch("anvil.lib.lib.AnvilValidator.validate_namespace_project_name"):
        cfg = _AnvilConfig()
        expected_rp = os.path.join(RELEASE_COM_MOJANG, "development_resource_packs", "RP_test_proj")
        expected_bp = os.path.join(RELEASE_COM_MOJANG, "development_behavior_packs", "BP_test_proj")
        assert cfg.RP_PATH == expected_rp
        assert cfg.BP_PATH == expected_bp
        assert cfg._LOCAL_EXPORT is False


def test_windows_preview_effective_only_with_default_paths(make_project, monkeypatch):
    """On Windows without local_export, preview chooses PREVIEW_COM_MOJANG."""
    make_project(local_export=False, preview=True)
    monkeypatch.setattr(sys, "platform", "win32")

    with patch("anvil.lib.lib.AnvilValidator.validate_namespace_project_name"):
        cfg = _AnvilConfig()
        expected_rp = os.path.join(PREVIEW_COM_MOJANG, "development_resource_packs", "RP_test_proj")
        expected_bp = os.path.join(PREVIEW_COM_MOJANG, "development_behavior_packs", "BP_test_proj")
        assert cfg.RP_PATH == expected_rp
        assert cfg.BP_PATH == expected_bp


def test_windows_local_export_true_exports_to_output(make_project, monkeypatch):
    """On Windows when local_export is true, export to output/com.mojang folder."""
    make_project(local_export=True, preview=True)
    monkeypatch.setattr(sys, "platform", "win32")

    with patch("anvil.lib.lib.AnvilValidator.validate_namespace_project_name"):
        cfg = _AnvilConfig()
        expected_mojang = os.path.join(os.path.abspath("output"), "com.mojang")
        assert cfg.RP_PATH == os.path.join(
            expected_mojang, "development_resource_packs", "RP_test_proj"
        )
        assert cfg.BP_PATH == os.path.join(
            expected_mojang, "development_behavior_packs", "BP_test_proj"
        )
        assert cfg._WORLD_PATH == os.path.join(
            expected_mojang, "minecraftWorlds", "test_proj"
        )
        assert cfg._LOCAL_EXPORT is True


def test_non_windows_always_exports_to_output(make_project, monkeypatch):
    """On non-Windows, even if local_export is false or true, export to output/com.mojang folder."""
    # Test with local_export=False on Linux
    make_project(local_export=False, preview=True)
    monkeypatch.setattr(sys, "platform", "linux")

    with patch("anvil.lib.lib.AnvilValidator.validate_namespace_project_name"):
        cfg = _AnvilConfig()
        expected_mojang = os.path.join(os.path.abspath("output"), "com.mojang")
        assert cfg.RP_PATH == os.path.join(
            expected_mojang, "development_resource_packs", "RP_test_proj"
        )
        assert cfg.BP_PATH == os.path.join(
            expected_mojang, "development_behavior_packs", "BP_test_proj"
        )
        assert cfg._WORLD_PATH == os.path.join(
            expected_mojang, "minecraftWorlds", "test_proj"
        )
        assert cfg._LOCAL_EXPORT is True

    _AnvilConfig._instance = None

    # Test with local_export=True on macOS
    make_project(local_export=True, preview=False)
    monkeypatch.setattr(sys, "platform", "darwin")

    with patch("anvil.lib.lib.AnvilValidator.validate_namespace_project_name"):
        cfg2 = _AnvilConfig()
        assert cfg2.RP_PATH == os.path.join(
            expected_mojang, "development_resource_packs", "RP_test_proj"
        )
        assert cfg2.BP_PATH == os.path.join(
            expected_mojang, "development_behavior_packs", "BP_test_proj"
        )
        assert cfg2._WORLD_PATH == os.path.join(
            expected_mojang, "minecraftWorlds", "test_proj"
        )
        assert cfg2._LOCAL_EXPORT is True


def test_init_sets_local_export_based_on_platform(tmp_path, monkeypatch):
    """init_cmd sets local_export=False on Windows and True on non-Windows."""
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.chdir(tmp_path)
    cfg_win = handle_configuration("my_ns", "my_pack", "My Pack", False, False, False)
    assert cfg_win.get_option(ConfigSection.ANVIL, ConfigOption.LOCAL_EXPORT) is False

    _AnvilConfig._instance = None
    tmp_path_posix = tmp_path / "posix"
    tmp_path_posix.mkdir()
    monkeypatch.chdir(tmp_path_posix)
    monkeypatch.setattr(sys, "platform", "linux")
    cfg_posix = handle_configuration("my_ns", "my_pack", "My Pack", False, False, False)
    assert cfg_posix.get_option(ConfigSection.ANVIL, ConfigOption.LOCAL_EXPORT) is True


def test_clear_cmd_get_project_dev_pack_paths(make_project, monkeypatch):
    """clear_cmd respects local_export and platform."""
    # Windows with local_export=False -> com.mojang
    make_project(local_export=False, preview=False)
    monkeypatch.setattr(sys, "platform", "win32")
    cfg = Config()
    paths = get_project_dev_pack_paths(cfg)
    assert paths == [
        os.path.join(RELEASE_COM_MOJANG, "development_resource_packs", "RP_test_proj"),
        os.path.join(RELEASE_COM_MOJANG, "development_behavior_packs", "BP_test_proj"),
    ]

    # Windows with local_export=True -> output/com.mojang
    cfg.add_option(ConfigSection.ANVIL, ConfigOption.LOCAL_EXPORT, True)
    paths_local = get_project_dev_pack_paths(cfg)
    expected_mojang = os.path.join(os.path.abspath("output"), "com.mojang")
    assert paths_local == [
        os.path.join(expected_mojang, "development_resource_packs", "RP_test_proj"),
        os.path.join(expected_mojang, "development_behavior_packs", "BP_test_proj"),
    ]

    # Non-Windows -> output/com.mojang
    monkeypatch.setattr(sys, "platform", "darwin")
    paths_mac = get_project_dev_pack_paths(cfg)
    assert paths_mac == [
        os.path.join(expected_mojang, "development_resource_packs", "RP_test_proj"),
        os.path.join(expected_mojang, "development_behavior_packs", "BP_test_proj"),
    ]


def test_clean_old_dev_removes_configured_paths(make_project, tmp_path, monkeypatch):
    """clean_old_dev removes packs located at config.RP_PATH and config.BP_PATH."""
    make_project(local_export=True)
    monkeypatch.setattr(sys, "platform", "win32")
    with patch("anvil.lib.lib.AnvilValidator.validate_namespace_project_name"):
        cfg = _AnvilConfig()
        os.makedirs(cfg.RP_PATH, exist_ok=True)
        os.makedirs(cfg.BP_PATH, exist_ok=True)
        (tmp_path / "output" / "com.mojang" / "development_resource_packs" / "RP_test_proj" / "test.txt").write_text("rp content")
        (tmp_path / "output" / "com.mojang" / "development_behavior_packs" / "BP_test_proj" / "test.txt").write_text("bp content")

        assert os.path.isdir(cfg.RP_PATH)
        assert os.path.isdir(cfg.BP_PATH)

        clean_old_dev(cfg)

        assert not os.path.exists(cfg.RP_PATH)
        assert not os.path.exists(cfg.BP_PATH)
