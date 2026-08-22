"""Tests for anvil/lib/config.py — Config CRUD operations."""
import json
import pytest
from anvil.lib.config import Config, ConfigSection, ConfigOption, ConfigPackageTarget


@pytest.fixture
def config_file(tmp_path):
    """Create a minimal anvilconfig.json and chdir to tmp_path."""
    data = {
        "package": {
            "namespace": "test",
            "project_name": "test_proj",
            "company": "TestCo",
            "display_name": "Test Project",
            "project_description": "desc",
            "behavior_description": "bp",
            "resource_description": "rp",
        }
    }
    cfg = tmp_path / "anvilconfig.json"
    cfg.write_text(json.dumps(data))
    return tmp_path


def test_config_loads(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    assert cfg.has_section(ConfigSection.PACKAGE)


def test_config_has_section_false(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    assert not cfg.has_section("nonexistent_section")


def test_config_add_and_get_option(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    cfg.add_option("package", "custom_key", "hello")
    assert cfg.has_option("package", "custom_key")
    assert cfg.get_option("package", "custom_key") == "hello"


def test_config_add_section(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    cfg.add_section("new_section")
    assert cfg.has_section("new_section")


def test_config_add_option_creates_section(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    cfg.add_option("brand_new", "key", 42)
    assert cfg.has_section("brand_new")
    assert cfg.get_option("brand_new", "key") == 42


def test_config_save_persists(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    cfg.add_option("package", "persisted", True)
    # Reload from disk
    cfg2 = Config()
    assert cfg2.get_option("package", "persisted") is True


def test_config_option_types(config_file, monkeypatch):
    monkeypatch.chdir(config_file)
    cfg = Config()
    cfg.add_option("test_types", "an_int", 99)
    cfg.add_option("test_types", "a_float", 3.14)
    cfg.add_option("test_types", "a_bool", False)
    cfg.add_option("test_types", "a_list", ["a", "b"])
    assert cfg.get_option("test_types", "an_int") == 99
    assert cfg.get_option("test_types", "a_float") == pytest.approx(3.14)
    assert cfg.get_option("test_types", "a_bool") is False
    assert cfg.get_option("test_types", "a_list") == ["a", "b"]


def test_config_missing_raises(tmp_path, monkeypatch):
    """Config without allow_missing=True should exit(1) if no anvilconfig.json."""
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        Config()


def test_config_allow_missing(tmp_path, monkeypatch):
    """Config(allow_missing=True) should not raise even with no anvilconfig.json."""
    monkeypatch.chdir(tmp_path)
    cfg = Config(allow_missing=True)
    assert not cfg.has_section("anything")


def test_config_package_target_enum():
    assert ConfigPackageTarget.WORLD == "world"
    assert ConfigPackageTarget.ADDON == "addon"
    assert "world" in list(ConfigPackageTarget)
    assert "addon" in list(ConfigPackageTarget)
