"""Tests for anvil/lib/schemas.py — JsonSchemes structural assertions.

These tests verify that key schema methods produce the expected JSON structure.
They use monkeypatching to avoid spinning up the full _AnvilConfig singleton.
"""
import json
import uuid
import pytest
from unittest.mock import MagicMock, patch


# ---------------------------------------------------------------------------
# Fixture: mock CONFIG for all tests in this module
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    cfg = MagicMock()
    cfg._BP_UUID = [str(uuid.uuid4())]
    cfg._RP_UUID = [str(uuid.uuid4())]
    cfg._PACK_UUID = str(uuid.uuid4())
    cfg._DATA_MODULE_UUID = str(uuid.uuid4())
    cfg._SCRIPT_MODULE_UUID = str(uuid.uuid4())
    cfg._RELEASE = "1.0.0"
    cfg._PREVIEW = False
    cfg._RANDOM_SEED = False
    cfg._MINIFY = False
    cfg._TARGET = "world"
    cfg.NAMESPACE = "test"
    cfg.PROJECT_NAME = "test_project"
    cfg.COMPANY = "TestCo"
    cfg.DISPLAY_NAME = "Test Project"
    cfg.PROJECT_DESCRIPTION = "A test"
    cfg.BEHAVIOUR_DESCRIPTION = "BP test"
    cfg.RESOURCE_DESCRIPTION = "RP test"
    cfg._PASCAL_PROJECT_NAME = "TP"
    cfg._EXPERIMENTAL = False
    cfg._SCRIPT_API = False
    cfg._SCRIPT_UI = False
    cfg.PBR = False

    monkeypatch.setattr("anvil.lib.schemas.CONFIG", cfg)
    return cfg


# ---------------------------------------------------------------------------
# manifest_bp
# ---------------------------------------------------------------------------

class TestManifestBP:
    def test_has_format_version(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_bp([1, 0, 0])
        assert "format_version" in result

    def test_has_header(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_bp([1, 0, 0])
        assert "header" in result

    def test_has_modules(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_bp([1, 0, 0])
        assert "modules" in result

    def test_header_uuid_is_string(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_bp([1, 0, 0])
        assert isinstance(result["header"]["uuid"], str)


# ---------------------------------------------------------------------------
# manifest_rp
# ---------------------------------------------------------------------------

class TestManifestRP:
    def test_has_format_version(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_rp([1, 0, 0])
        assert "format_version" in result

    def test_has_header(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_rp([1, 0, 0])
        assert "header" in result

    def test_header_uuid_is_string(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_rp([1, 0, 0])
        assert isinstance(result["header"]["uuid"], str)


# ---------------------------------------------------------------------------
# manifest_world
# ---------------------------------------------------------------------------

class TestManifestWorld:
    def test_has_format_version(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_world([1, 0, 0])
        assert "format_version" in result

    def test_has_header(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_world([1, 0, 0])
        assert "header" in result

    def test_random_seed_absent_by_default(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_world([1, 0, 0])
        assert result.get("header", {}).get("allow_random_seed") is None

    def test_random_seed_when_enabled(self, mock_config):
        mock_config._RANDOM_SEED = True
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.manifest_world([1, 0, 0])
        assert result["header"]["allow_random_seed"] is True


# ---------------------------------------------------------------------------
# world_packs
# ---------------------------------------------------------------------------

class TestWorldPacks:
    def test_returns_list(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.world_packs([1, 0, 0], ["uuid-1", "uuid-2"])
        assert isinstance(result, list)
        assert len(result) == 2

    def test_contains_pack_ids(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.world_packs([1, 0, 0], ["uuid-a"])
        assert result[0]["pack_id"] == "uuid-a"
        assert result[0]["version"] == [1, 0, 0]


# ---------------------------------------------------------------------------
# pack_name_lang
# ---------------------------------------------------------------------------

class TestPackNameLang:
    def test_returns_list_of_strings(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.pack_name_lang("MyPack", "A great pack")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_contains_name(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.pack_name_lang("MyPack", "A great pack")
        combined = "\n".join(result)
        assert "MyPack" in combined


# ---------------------------------------------------------------------------
# github_release_workflow (already tested in test_workflow.py — extra coverage)
# ---------------------------------------------------------------------------

class TestGithubReleaseWorkflow:
    def test_contains_project_name(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.github_release_workflow("my_proj", "My Project")
        assert "my_proj" in result

    def test_contains_release_action(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.github_release_workflow("my_proj", "My Project")
        assert "softprops/action-gh-release" in result

    def test_is_string(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.github_release_workflow("my_proj", "My Project")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# description helper
# ---------------------------------------------------------------------------

class TestDescription:
    def test_correct_identifier(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.description("stark", "my_entity")
        assert result == {"description": {"identifier": "stark:my_entity"}}


# ---------------------------------------------------------------------------
# esbuild_config_js
# ---------------------------------------------------------------------------

class TestEsbuildConfigJs:
    def test_returns_string(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.esbuild_config_js("C:/some/path", False)
        assert isinstance(result, str)

    def test_contains_esbuild_import(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.esbuild_config_js("C:/some/path", False)
        assert "esbuild" in result

    def test_contains_anvilconfig_loading(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.esbuild_config_js("C:/some/path", False)
        assert "anvilconfig.json" in result
        assert "anvilConfig" in result

    def test_contains_tsconfig_handling(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.esbuild_config_js("C:/some/path", False)
        assert "tsconfig" in result


# ---------------------------------------------------------------------------
# package_json
# ---------------------------------------------------------------------------

class TestPackageJson:
    def test_returns_dict(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.package_json("my_project", "1.0.0", "My description", "Author")
        assert isinstance(result, dict)

    def test_contains_project_metadata(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.package_json("my_project", "1.0.0", "My description", "Author")
        assert result["name"] == "my_project"
        assert result["version"] == "1.0.0"
        assert result["description"] == "My description"
        assert result["author"] == "Author"

    def test_contains_scripts(self):
        from anvil.lib.schemas import JsonSchemes
        result = JsonSchemes.package_json("my_project", "1.0.0", "My description", "Author")
        assert "scripts" in result
        assert result["scripts"]["build"] == "node esbuild.js"
        assert result["scripts"]["test"] == "npx tsc --noemit"

