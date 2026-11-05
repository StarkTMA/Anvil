"""The files `anvil init` and the build write next to a project's code: the npm, TypeScript,
esbuild, VS Code and GitHub workflow files, the Python entry point and `.gitignore`. JSON
files are returned as dicts, the others as text."""

from pathlib import Path

from anvil.__version__ import __version__
from anvil.lib.lib import PREVIEW_COM_MOJANG, RELEASE_COM_MOJANG

__all__ = [
    "code_workspace",
    "esbuild_js",
    "github_release_workflow",
    "gitignore",
    "main_py",
    "package_json",
    "ts_constants",
    "tsconfig",
    "vscode_launch",
]


def package_json(
    project_name: str, version: str, description: str, author: str
) -> dict:
    """The project's `package.json`.

    Args:
        project_name (str): The npm package name.
        version (str): The package version.
        description (str): The package description.
        author (str): The package author.
    """
    return {
        "name": project_name,
        "version": version,
        "description": description,
        "type": "module",
        "scripts": {"build": "node esbuild.js", "test": "npx tsc --noemit"},
        "keywords": [],
        "author": author,
        "license": "ISC",
    }


def tsconfig(out_dir: str | Path) -> dict:
    """The project's `tsconfig.json`.

    Args:
        out_dir (str | Path): The behavior pack folder. Scripts compile to its `scripts`
            folder.
    """
    return {
        "compilerOptions": {
            "target": "ESNext",
            "module": "es2020",
            "declaration": False,
            "outDir": (Path(out_dir) / "scripts").as_posix(),
            "rootDir": "./scripts/javascript",
            "strict": True,
            "pretty": True,
            "esModuleInterop": True,
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "forceConsistentCasingInFileNames": True,
            "lib": ["ESNext", "DOM"],
        },
        "include": ["scripts/javascript/**/*"],
        "exclude": ["node_modules"],
    }


def vscode_launch(
    source_map_root: str | Path,
    local_root: str | Path,
    script_uuid: str,
    project_name: str,
) -> dict:
    """The `.vscode/launch.json` that attaches the Minecraft script debugger.

    Args:
        source_map_root (str | Path): The folder of the compiled scripts and their source
            maps.
        local_root (str | Path): The folder of the TypeScript sources.
        script_uuid (str): The UUID of the behavior pack's script module.
        project_name (str): The project name, shown in the debug configuration.
    """
    return {
        "version": "0.3.0",
        "configurations": [
            {
                "type": "minecraft-js",
                "request": "attach",
                "name": f"Debug {project_name}",
                "mode": "listen",
                "targetModuleUuid": script_uuid,
                "localRoot": Path(local_root).as_posix(),
                "sourceMapRoot": Path(source_map_root).as_posix(),
                "generatedSourceRoot": Path(source_map_root).as_posix(),
                "port": 19144,
            }
        ],
    }


def code_workspace(
    name: str,
    path: str | Path,
    preview: bool = False,
    dev_res_path: str | Path | None = None,
    dev_beh_path: str | Path | None = None,
) -> dict:
    """The project's VS Code workspace: the project folder and the development pack folders
    of Minecraft and Minecraft Preview.

    Args:
        name (str): The name of the project folder in the workspace.
        path (str | Path): The project folder.
        preview (bool, optional): Whether the development packs are Minecraft Preview's.
        dev_res_path (str | Path, optional): The development resource packs folder, when it
            is not the game's.
        dev_beh_path (str | Path, optional): The development behavior packs folder, when it
            is not the game's.
    """
    com_mojang = PREVIEW_COM_MOJANG if preview else RELEASE_COM_MOJANG
    folders = [
        (name, path),
        (
            "Dev Resource Packs",
            dev_res_path or com_mojang / "development_resource_packs",
        ),
        (
            "Dev behavior Packs",
            dev_beh_path or com_mojang / "development_behavior_packs",
        ),
        (
            "Dev Preview Resource Packs",
            PREVIEW_COM_MOJANG / "development_resource_packs",
        ),
        (
            "Dev Preview behavior Packs",
            PREVIEW_COM_MOJANG / "development_behavior_packs",
        ),
    ]
    return {
        "folders": [
            {"name": folder, "path": Path(location).as_posix()}
            for folder, location in folders
        ]
    }


def ts_constants(namespace: str, project_name: str) -> str:
    """The `constants.ts` that gives the scripts the project's namespace and name."""
    return (
        f'export const NAMESPACE = "{namespace}"\n'
        f'export const PROJECT_NAME = "{project_name}"\n'
    )


def main_py() -> str:
    """The project's Python entry point, `scripts/python/main.py`."""
    return (
        "from anvil import *\n"
        "\n"
        'if __name__ == "__main__":\n'
        "    ANVIL.compile(extract_world=None)\n"
        "    # ANVIL.package()\n"
    )


def gitignore() -> str:
    """The project's `.gitignore`."""
    return _GITIGNORE


def esbuild_js() -> str:
    """The `esbuild.js` that bundles the TypeScript scripts. It reads `minify` and
    `scriptui` from `anvilconfig.json` and takes the output folder as `--outdir=`."""
    return _ESBUILD


def github_release_workflow(project_name: str) -> str:
    """The GitHub Actions workflow, `.github/workflows/release.yml`, that builds and
    releases the project when its version changes.

    Args:
        project_name (str): The project name, shown in the workflow name.
    """
    return (
        f"name: Release {project_name}\n"
        + _WORKFLOW_SETUP
        + f'          python -m pip install "mcanvil>={__version__}"\n'
        + _WORKFLOW_RELEASE
    )


# region Texts


_GITIGNORE = """\
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*.pyd
*.so
*$py.class

# Distribution / packaging
build/
dist/
.eggs/
pip-wheel-metadata/
*.egg-info/
*.egg
MANIFEST

# Unit test / coverage reports
htmlcov/
.coverage
.coverage.*
.cache
coverage.xml
*.py,cover
.pytest_cache/

# MkDocs output
site/

# Environments
.env
.venv
env/
venv/
ENV/

# Typescript/Javascript
node_modules/
package-lock.json

# Anvil
.vscode/
output/
TODO.md
.copilot-*
copilot-instructions.md
"""

_ESBUILD = """\
import esbuild from "esbuild";
import path from "path";
import { fileURLToPath } from "url";
import { mkdirSync, writeFileSync, readFileSync } from "fs";

// Read anvilconfig.json next to this file
const configPath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "anvilconfig.json");
const anvilConfig = JSON.parse(readFileSync(configPath, "utf8"));
const minify = anvilConfig.build?.minify ?? false;
const scriptui = anvilConfig.features?.scriptui ?? false;

// Resolve outDir exclusively from the --outdir argument
const outDir = process.argv
	.find((arg) => arg.startsWith("--outdir="))
	?.split("=")
	.slice(1)
	.join("=")
	.replace(/^["']|["']$/g, "");

if (!outDir) {
	console.error("Error: Missing required --outdir argument.");
	process.exit(1);
}

const tsconfigPath = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "tsconfig.json");

const removeFileSchemePlugin = {
	name: "remove-file-scheme",
	setup(build) {
		build.onEnd((result) => {
			if (!result.outputFiles?.length) return;

			for (const file of result.outputFiles) {
				if (!file.path.endsWith(".map")) continue;

				const map = JSON.parse(Buffer.from(file.contents).toString("utf8"));

				map.sources = map.sources.map((src) => {
					if (src.startsWith("file://")) {
						try {
							src = fileURLToPath(src);
						} catch {
							src = src.replace("file://", "");
						}
					}
					return src;
				});

				file.contents = Buffer.from(JSON.stringify(map));
			}
		});
	},
};

const minifyArg = process.argv.includes("--minify");

const external = ["@minecraft/server"];
if (scriptui) {
	external.push("@minecraft/server-ui");
}

const result = await esbuild.build({
	entryPoints: ["scripts/javascript/main.ts"],
	bundle: true,
	format: "esm",
	sourcemap: true,
	minify: minify || minifyArg,
	outdir: outDir,
	external: external,
	tsconfig: tsconfigPath,
	write: false,
	plugins: [removeFileSchemePlugin],
});

for (const f of result.outputFiles ?? []) {
	mkdirSync(path.dirname(f.path), { recursive: true });
	writeFileSync(f.path, f.contents);
}
"""

_WORKFLOW_SETUP = """\

on:
  push:
  workflow_dispatch:

permissions:
  contents: write

concurrency:
  group: release-${{ github.ref }}
  cancel-in-progress: false

env:
  PYTHONUTF8: "1"

jobs:
  release:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    defaults:
      run:
        shell: bash

    steps:
      - name: Check out repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.13"

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "24"

      - name: Install build dependencies
        run: |
          python -m pip install --upgrade pip
"""

_WORKFLOW_RELEASE = """\
          if [ -f requirements.txt ]; then
            python -m pip install -r requirements.txt
          fi
          if [ -f package.json ]; then
            npm install
          fi

      - name: Enable local export
        run: |
          python - <<'PY'
          import json
          from pathlib import Path

          path = Path("anvilconfig.json")
          config = json.loads(path.read_text(encoding="utf-8"))
          config.setdefault("anvil", {})["local_export"] = True
          path.write_text(json.dumps(config, indent=4), encoding="utf-8")
          PY

      - name: Detect version bump
        id: version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_REPOSITORY: ${{ github.repository }}
        run: |
          python - <<'PY'
          import json, os, urllib.request, urllib.error
          from pathlib import Path

          config_path = Path("anvilconfig.json")
          if not config_path.exists():
              raise SystemExit("anvilconfig.json not found")

          config = json.loads(config_path.read_text(encoding="utf-8"))
          version = str(config["build"]["release"]).strip()
          target = str(config["package"].get("target", "world")).strip().lower()
          project_name = str(config["package"]["display_name"]).strip()

          if target not in ("addon", "world"):
              raise SystemExit(f"Unsupported package target: {target!r}")

          # A release is made only when the tag for this version does not exist yet.
          # Any API failure other than "not found" fails the job instead of guessing.
          repo = os.environ["GITHUB_REPOSITORY"]
          request = urllib.request.Request(
              f"https://api.github.com/repos/{repo}/releases/tags/v{version}",
              headers={
                  "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
                  "Accept": "application/vnd.github+json",
              },
          )
          try:
              urllib.request.urlopen(request).close()
              should_release = False
          except urllib.error.HTTPError as error:
              if error.code != 404:
                  raise
              should_release = True

          with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8", newline="\\n") as f:
              f.write(f"version={version}\\ntarget={target}\\nproject_name={project_name}\\nshould_release={'true' if should_release else 'false'}\\n")
          PY

      - name: Build and package
        if: steps.version.outputs.should_release == 'true'
        env:
          TARGET: ${{ steps.version.outputs.target }}
        run: |
          set -eo pipefail
          FLAGS="build"
          [ "$TARGET" == "addon" ] && FLAGS="$FLAGS --mcaddon"
          [ "$TARGET" == "world" ] && FLAGS="$FLAGS --mcworld"
          FLAGS="$FLAGS --zip --tech-notes"

          anvil $FLAGS

      - name: Collect artifacts
        if: steps.version.outputs.should_release == 'true'
        id: artifacts
        env:
          TARGET: ${{ steps.version.outputs.target }}
        run: |
          python - <<'PY'
          import os, subprocess
          from pathlib import Path

          target = os.environ["TARGET"]
          required = ".mcaddon" if target == "addon" else ".mcworld"
          files = sorted(
              p.as_posix()
              for p in Path("output").glob("*")
              if p.is_file() and p.suffix in [".mcaddon", ".mcworld", ".zip", ".pdf"]
          )
          if not any(f.endswith(required) for f in files):
              raise SystemExit(f"Build did not produce a {required} file in output/: {files}")

          with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8", newline="\\n") as f:
              f.write("files<<EOF\\n")
              for file in files:
                  f.write(f"{file}\\n")
              f.write("EOF\\n")

          notes = subprocess.check_output(["git", "log", "-1", "--pretty=%B"]).decode()
          Path("release-notes.md").write_text(notes, encoding="utf-8")
          PY

      - name: Create GitHub release
        if: steps.version.outputs.should_release == 'true'
        uses: softprops/action-gh-release@v2
        with:
          tag_name: v${{ steps.version.outputs.version }}
          target_commitish: ${{ github.sha }}
          name: ${{ steps.version.outputs.project_name }} v${{ steps.version.outputs.version }}
          body_path: release-notes.md
          fail_on_unmatched_files: true
          files: ${{ steps.artifacts.outputs.files }}
"""

# endregion
