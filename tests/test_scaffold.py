"""Tests for the project scaffolding files (anvil/lib/scaffold.py) and the world template
manifest and pack lists (anvil/api/core/manifest.py)."""

from anvil.__version__ import __version__
from anvil.api.core.manifest import world_packs, world_template_manifest
from anvil.lib import config, scaffold
from anvil.lib.config import CONFIG
from anvil.lib.lib import AnvilIO


def _json(document):
    return AnvilIO._normalize_json_like(document)


def test_world_template_manifest():
    manifest = _json(world_template_manifest((1, 2, 3), "module-uuid"))
    assert manifest["format_version"] == 2
    assert manifest["header"]["version"] == [1, 2, 3]
    assert manifest["header"]["uuid"] == CONFIG._PACK_UUID
    assert manifest["header"]["lock_template_options"] is True
    assert "allow_random_seed" not in manifest["header"]
    assert manifest["modules"] == [
        {"type": "world_template", "uuid": "module-uuid", "version": [1, 2, 3]}
    ]
    assert manifest["metadata"] == {"authors": [CONFIG.COMPANY]}


def test_world_template_manifest_random_seed():
    with config.override(_RANDOM_SEED=True):
        manifest = _json(world_template_manifest((1, 0, 0), "module-uuid"))
    assert manifest["header"]["allow_random_seed"] is True


def test_world_packs_is_a_list():
    assert _json(world_packs((1, 0, 0), ["uuid-a", "uuid-b"])) == [
        {"pack_id": "uuid-a", "version": [1, 0, 0]},
        {"pack_id": "uuid-b", "version": [1, 0, 0]},
    ]


def test_package_json():
    result = scaffold.package_json("my_project", "1.0.0", "My description", "Author")
    assert result["name"] == "my_project"
    assert result["version"] == "1.0.0"
    assert result["description"] == "My description"
    assert result["author"] == "Author"
    assert result["scripts"] == {
        "build": "node esbuild.js",
        "test": "npx tsc --noemit",
    }


def test_tsconfig_and_vscode_paths_use_forward_slashes():
    assert scaffold.tsconfig("C:\\packs\\BP")["compilerOptions"]["outDir"].endswith(
        "BP/scripts"
    )
    launch = scaffold.vscode_launch("out/scripts", "src/js", "script-uuid", "demo")
    configuration = launch["configurations"][0]
    assert configuration["name"] == "Debug demo"
    assert configuration["targetModuleUuid"] == "script-uuid"
    assert configuration["sourceMapRoot"] == "out/scripts"


def test_code_workspace_lists_project_pack_folders():
    folders = scaffold.code_workspace(
        "demo", "work/demo", dev_res_path="dev/RP", dev_beh_path="dev/BP"
    )["folders"]
    assert folders == [
        {"name": "demo", "path": "work/demo"},
        {"name": "Dev Resource Packs", "path": "dev/RP/RP_demo"},
        {"name": "Dev behavior Packs", "path": "dev/BP/BP_demo"},
    ]


def test_code_workspace_defaults_to_game_folders():
    folders = scaffold.code_workspace("demo", "work/demo")["folders"]
    assert folders[1]["path"].endswith("development_resource_packs/RP_demo")
    assert folders[2]["path"].endswith("development_behavior_packs/BP_demo")


def test_text_files():
    constants = scaffold.ts_constants()
    assert isinstance(constants, str)
    assert 'import config from "../../anvilconfig.json";' in constants
    assert "export const NAMESPACE = config.package.namespace;" in constants
    assert "export const PROJECT_NAME = config.package.project_name;" in constants
    assert "ANVIL.compile(" in scaffold.main_py()
    assert "__pycache__/" in scaffold.gitignore()
    esbuild = scaffold.esbuild_js()
    assert "anvilconfig.json" in esbuild and "tsconfig" in esbuild


def test_github_release_workflow():
    workflow = scaffold.github_release_workflow("test_project")
    assert workflow.startswith("name: Release test_project\n")
    assert '"mcanvil==$ANVIL_VERSION"' in workflow
    assert '.get("anvil_version")' in workflow
    assert f'or "{__version__}"' in workflow
    assert "${{ github.ref }}" in workflow
    assert "--tech-notes" in workflow
    assert ".pdf" in workflow
    assert 'newline="\\n"' in workflow
    assert "softprops/action-gh-release@v2" in workflow
