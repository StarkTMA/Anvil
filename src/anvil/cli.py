import os
import uuid
from datetime import datetime

import click
import commentjson as json
import requests
from packaging.version import Version

from anvil.lib.config import Config, ConfigOption, ConfigSection
from anvil.lib.format_versions import (MANIFEST_BUILD, MODULE_MINECRAFT_SERVER,
                                       MODULE_MINECRAFT_SERVER_UI)
from anvil.lib.lib import (APPDATA, DESKTOP, CreateDirectory, File, FileExists,
                           process_subcommand, validate_namespace_project_name)

from .__version__ import __version__


class JsonSchemes:
    @staticmethod
    def structure(project_name):
        return {
            project_name: {
                "assets": {
                    "models": {},
                    "textures": {"environment": {}, "items": {}, "ui": {}},
                    "sounds": {},
                    "particles": {},
                    "skins": {},
                },
                "scripts": {"javascript": {}, "python": {}},
                "world": {"structures": {}},
                "marketing": {},
                "output": {},
            }
        }

    @staticmethod
    def script():
        return "\n".join(
            [
                "from anvil import *",
                "",
                'if __name__ == "__main__":',
                "    ANVIL.compile(extract_world=None)",
                "    #ANVIL.package()",
            ]
        )

    @staticmethod
    def gitignore():
        return "\n".join(
            [
                "#Anvil",
                "assets/cache/",
                "# Byte-compiled / optimized / DLL files",
                "__pycache__/",
                "*.py[cod]",
                "*$py.class",
                "# C extensions",
                "*.so",
                "# Distribution / packaging",
                ".Python",
                "build/",
                "develop-eggs/",
                "dist/",
                "downloads/",
                "eggs/",
                ".eggs/",
                "lib/",
                "lib64/",
                "parts/",
                "sdist/",
                "var/",
                "wheels/",
                "pip-wheel-metadata/",
                "share/python-wheels/",
                "*.egg-info/",
                ".installed.cfg",
                "*.egg",
                "MANIFEST",
                "# Environments",
                ".env",
                ".venv",
                "env/",
                "venv/",
                "ENV/",
                "env.bak/",
                "venv.bak/",
                "# Typescript/Javascript",
                "node_modules/",
            ]
        )

    @staticmethod
    def pack_name_lang(name, description):
        return [f"pack.name={name}", f"pack.description={description}"]

    @staticmethod
    def manifest_bp(version, uuid1, rpuuid, author, has_script: bool, server_ui: bool):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": uuid1,
                "version": version,
                "min_engine_version": [int(i) for i in MANIFEST_BUILD.split(".")],
            },
            "modules": [{"type": "data", "uuid": str(uuid.uuid4()), "version": version}],
            "dependencies": [{"uuid": rpuuid, "version": version}],
            "metadata": {"authors": [author]},
        }
        if has_script:
            m["modules"].append(
                {
                    "uuid": str(uuid.uuid4()),
                    "version": version,
                    "type": "script",
                    "language": "javascript",
                    "entry": "scripts/main.js",
                }
            )
            m["dependencies"].append(
                {
                    "module_name": "@minecraft/server",
                    "version": MODULE_MINECRAFT_SERVER,
                }
            )
            if server_ui:
                m["dependencies"].append(
                    {
                        "module_name": "@minecraft/server-ui",
                        "version": MODULE_MINECRAFT_SERVER_UI,
                    }
                )
        return m

    @staticmethod
    def manifest_rp(version, uuid1, bp_uuid, author, has_pbr, addon):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": uuid1,
                "version": version,
                "min_engine_version": [int(i) for i in MANIFEST_BUILD.split(".")],
            },
            "modules": [
                {
                    "type": "resources",
                    "uuid": str(uuid.uuid4()),
                    "version": version,
                }
            ],
            "dependencies": [{"uuid": bp_uuid, "version": version}],
            "metadata": {"authors": [author]},
        }
        if has_pbr:
            m.update({"capabilities": ["pbr"]})
        if addon:
            m["header"]["pack_scope"] = "world"
            m["metadata"]["product_type"] = "addon"
        return m

    @staticmethod
    def manifest_world(version, uuid1, author, seed):
        return {
            "format_version": 2,
            "header": {
                "name": "pack.name",
                "description": "pack.description",
                "version": version,
                "uuid": uuid1,
                # "platform_locked": False,
                "lock_template_options": True,
                "base_game_version": [int(i) for i in MANIFEST_BUILD.split(".")],
                "allow_random_seed": seed,
            },
            "modules": [
                {
                    "type": "world_template",
                    "uuid": str(uuid.uuid4()),
                    "version": version,
                }
            ],
            "metadata": {"authors": [author]},
        }

    @staticmethod
    def world_packs(pack_id, version):
        return [{"pack_id": i, "version": version} for i in pack_id]

    @staticmethod
    def code_workspace(name, path1, path2, preview=False):
        return {
            "folders": [
                {"name": name, "path": os.path.join(path1, path2)},
                {
                    "name": "Dev Resource Packs",
                    "path": os.path.join(
                        APPDATA,
                        "Local",
                        "Packages",
                        f"Microsoft.Minecraft{'WindowsBeta' if preview else 'UWP'}_8wekyb3d8bbwe",
                        "LocalState",
                        "games",
                        "com.mojang",
                        "development_resource_packs",
                    ),
                },
                {
                    "name": "Dev behavior Packs",
                    "path": os.path.join(
                        APPDATA,
                        "Local",
                        "Packages",
                        f"Microsoft.Minecraft{'WindowsBeta' if preview else 'UWP'}_8wekyb3d8bbwe",
                        "LocalState",
                        "games",
                        "com.mojang",
                        "development_behavior_packs",
                    ),
                },
            ]
        }

    @staticmethod
    def vscode(path):
        return {
            "version": "0.3.0",
            "configurations": [
                {
                    "type": "minecraft-js",
                    "request": "attach",
                    "name": "Wait for Minecraft Debug Connections",
                    "mode": "listen",
                    "localRoot": path,
                    "port": 19144,
                }
            ],
        }

    @staticmethod
    def packagejson(project_name, version, description, author):
        return {
            "name": project_name,
            "version": version,
            "description": description,
            "type": "module",
            "keywords": [],
            "author": author,
            "license": "ISC",
        }

    @staticmethod
    def tsconfig(out_dir):
        return {
            "compilerOptions": {
                "target": "ESNext",
                "module": "es2020",
                "declaration": False,
                "outDir": os.path.join(out_dir, "scripts"),
                "strict": True,
                "pretty": True,
                "esModuleInterop": True,
                "moduleResolution": "Node",
                "resolveJsonModule": True,
                "forceConsistentCasingInFileNames": True,
                "lib": ["ESNext"],
            },
            "include": ["scripts/javascript/**/*"],
            "exclude": ["node_modules"],
        }

    @staticmethod
    def tsconstants(namespace: str, project_name: str):
        file = []
        file.append(f'export const NAMESPACE = "{namespace}"')
        file.append(f'export const PROJECT_NAME = "{project_name}"')

        return "\n".join(file)

    @staticmethod
    def esbuild_config_js(outDir):
        return "\n".join(
            [
                "import esbuild from 'esbuild';",
                f"const outDir = '{os.path.join(outDir, 'scripts')}';",
                "esbuild",
                "    .build({",
                '        entryPoints: ["scripts/javascript/main.ts"],',
                "        bundle: true,",
                '        format: "esm",',
                "        sourcemap: true,",
                "        minify: true,",
                "        external: [",
                "            '@minecraft/server',",
                "            '@minecraft/server-ui',",
                "        ],",
                "    })",
                "    .catch(() => process.exit(1));",
            ]
        )


def CreateDirectoriesFromTree(tree: dict) -> None:
    """
    Recursively creates directories based on the structure of a tree.

    Parameters:
        tree (dict): The tree structure representing the directories.

    Returns:
        None
    """

    def find_key(tree: dict, path: str, a: list) -> list:
        """
        Recursively finds keys in the tree structure.

        Parameters:
            tree (dict): The tree structure.
            path (str): The current path.
            a (list): The list to store the found keys.

        Returns:
            list: The list of found keys.
        """
        for key, value in tree.items():
            if isinstance(value, dict):
                find_key(value, f"{path}/{key}", a)
            if value == {}:
                a.append(f"{path}/{key}")
        return a

    directories = find_key(tree, "", a=[])
    for directory in directories:
        CreateDirectory(directory)


def handle_configuration(
    namespace: str, project_name: str, display_name: str, preview: bool, scriptapi: bool, pbr: bool, random_seed: bool, addon: bool
):
    config = Config()

    config.add_option(ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, MANIFEST_BUILD)

    config.add_option(ConfigSection.PACKAGE, ConfigOption.NAMESPACE, namespace)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME, project_name)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.COMPANY, namespace.title())
    config.add_option(ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME, display_name)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_DESCRIPTION, f"{display_name} Packs")
    config.add_option(ConfigSection.PACKAGE, ConfigOption.BEHAVIOUR_DESCRIPTION, f"{display_name} behavior Pack")
    config.add_option(ConfigSection.PACKAGE, ConfigOption.RESOURCE_DESCRIPTION, f"{display_name} Resource Pack")
    config.add_option(ConfigSection.PACKAGE, ConfigOption.TARGET, "addon" if addon else "world")

    config.add_option(ConfigSection.ANVIL, ConfigOption.DEBUG, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PASCAL_PROJECT_NAME, "".join(x[0] for x in project_name.split("_")).upper())
    config.add_option(ConfigSection.ANVIL, ConfigOption.LAST_CHECK, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    config.add_option(ConfigSection.ANVIL, ConfigOption.SCRIPT_API, scriptapi)
    config.add_option(ConfigSection.ANVIL, ConfigOption.SCRIPT_UI, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PBR, pbr)
    config.add_option(ConfigSection.ANVIL, ConfigOption.RANDOM_SEED, random_seed)
    config.add_option(ConfigSection.ANVIL, ConfigOption.EXPERIMENTAL, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PREVIEW, preview)
    config.add_option(ConfigSection.ANVIL, ConfigOption.ENTRY_POINT, "main.py")

    config.add_option(ConfigSection.BUILD, ConfigOption.RELEASE, "1.0.0")
    config.add_option(ConfigSection.BUILD, ConfigOption.RP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.BP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.PACK_UUID, str(uuid.uuid4()))
    config.add_option(ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, str(uuid.uuid4()))

    config.add_section(namespace)

    config.save()

    return config


def display_welcome_message(display_name: str) -> None:
    """
    Displays the welcome message for the Anvil CLI.

    Returns:
        None
    """
    click.clear()
    click.echo(
        "\n".join(
            [
                f"{click.style("Anvil", "cyan")} - by StarkTMA.",
                f"Version {click.style(__version__, "cyan")}.",
                f"Copyright © {datetime.now().year} {click.style("StarkTMA", "red")}.",
                "All rights reserved.",
                "",
                "",
            ]
        )
    )
    click.echo(f"Initiating {display_name}")


def check_version() -> None:
    """
    Checks the current version of Anvil and compares it with the latest version.

    Returns:
        None
    """
    try:
        latest_build: str = requests.get("https://raw.githubusercontent.com/StarkTMA/Anvil/main/src/anvil/__version__.py").split("=")[-1].strip()
    except:
        latest_build = __version__

    if Version(__version__) < Version(latest_build):
        click.echo(
            click.style(
                f"Anvil has been updated to version {latest_build}, please run `pip install --upgrade mcanvil` to update your project.",
                "yellow",
            )
        )


def handle_script(config: Config, namespace: str, project_name: str, DEV_BEH_DIR, DEV_RES_DIR) -> None:
    click.echo("Initiating ScriptingAPI modules")
    install_locally_modules = ["@minecraft/server", "@minecraft/server-ui", "@minecraft/vanilla-data"]
    install_global_modules = ["typescript", "esbuild"]

    config.add_option(ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, str(uuid.uuid4()))
    config.add_option(ConfigSection.ANVIL, ConfigOption.JS_BUNDLE_SCRIPT, "node esbuild.js")

    File(
        "package.json",
        JsonSchemes.packagejson(
            project_name,
            "1.0.0",
            config.get_option("package", "display_name") + " Essentials",
            config.get_option("package", "company"),
        ),
        "",
        "w",
        True,
    )
    File("tsconfig.json", JsonSchemes.tsconfig(DEV_BEH_DIR), "", "w", False)
    File("esbuild.js", JsonSchemes.esbuild_config_js(), "", "w", False)
    File(
        "launch.json",
        JsonSchemes.vscode(os.path.join(DEV_RES_DIR, f"BP_{config.get_option("anvil", "pascal_project_name")}", "scripts")),
        ".vscode",
        "w",
        False,
    )
    File("anvilconfig.ts", JsonSchemes.tsconstants(namespace, project_name), os.path.join("scripts", "javascript"), "w", False)
    File("main.ts", 'import * as mc from "@minecraft/server";\n', os.path.join("scripts", "javascript"), "w", False)

    print(f"Installing npm packages... [{', '.join(install_locally_modules + install_global_modules)}]")
    process_subcommand(
        f"npm init -y && npm install --save {', '.join(install_locally_modules)}",
        f"Unable to initiate npm packages [{', '.join(install_locally_modules)}].",
    )
    process_subcommand(
        f"npm init -y && npm install -g {', '.join(install_global_modules)}",
        f"Unable to initiate npm packages [{', '.join(install_global_modules)}].",
    )


@click.group()
def cli() -> None:
    """
    Main command line interface function.

    Returns:
        None
    """
    pass


@cli.command(help="Initiate an Anvil project")
@click.argument("namespace")
@click.argument("project_name")
@click.option("--preview", is_flag=True, default=False, show_default=True, help="Generates the project in Minecraft Preview com.mojang.")
@click.option("--scriptapi", is_flag=True, default=False, show_default=True, help="Adds dependencies support of ScriptAPI.")
@click.option("--pbr", is_flag=True, default=False, show_default=True, help="Adds capabilities support of Physically based rendering.")
@click.option("--random_seed", is_flag=True, default=False, show_default=True, help="Adds support of Random Seed Worlds.")
@click.option("--addon", is_flag=True, default=False, show_default=True, help="Sets this package as an addon, comes with many restrictions.")
def create(
    namespace: str,
    project_name: str,
    preview: bool = False,
    scriptapi: bool = False,
    pbr: bool = False,
    random_seed: bool = False,
    addon: bool = False,
) -> None:
    """
    Create an Anvil project.

    Parameters:
        namespace (str): The namespace of the project.
        project_name (str): The name of the project.
        preview (bool, optional): Whether to generate the project in Minecraft Preview. Defaults to False.
        scriptapi (bool, optional): Whether to add dependencies support of ScriptAPI. Defaults to False.
        pbr (bool, optional): Whether to add capabilities support of Physically based rendering. Defaults to False.
        random_seed (bool, optional): Whether to add support of Random Seed Worlds. Defaults to False.

    """

    validate_namespace_project_name(namespace, project_name, addon)
    display_name = project_name.title().replace("-", " ").replace("_", " ")
    display_welcome_message(display_name)

    config = handle_configuration(namespace, project_name, display_name, preview, scriptapi, pbr, random_seed, addon)

    WORKING_DIR = os.getcwd()
    MINECRAFT_BUILD = f"Microsoft.Minecraft" + "WindowsBeta" if preview else "UWP" + "_8wekyb3d8bbwe"
    APP_PACKAGES = os.path.join(APPDATA, "Local", "Packages")
    COM_MOJANG = os.path.join(APP_PACKAGES, MINECRAFT_BUILD, "LocalState", "games", "com.mojang")
    DEV_RES_DIR = os.path.join(COM_MOJANG, "development_resource_packs")
    DEV_BEH_DIR = os.path.join(COM_MOJANG, "development_behavior_packs")

    CreateDirectoriesFromTree(JsonSchemes.structure(project_name))

    os.chdir(project_name)

    File("main.py", JsonSchemes.script(), "scripts/python/", "w")
    File(".gitignore", JsonSchemes.gitignore(), "", "w")
    File("CHANGELOG.md", "", "", "w")
    File(
        f"{project_name}.code-workspace",
        JsonSchemes.code_workspace(config.get_option("package", "company"), WORKING_DIR, project_name, preview),
        DESKTOP,
        "w",
    )

    if scriptapi:
        handle_script(config, namespace, project_name, DEV_BEH_DIR, DEV_RES_DIR)

    config.save()

    process_subcommand(f"start {os.path.join(DESKTOP, f'{project_name}.code-workspace')}", "Unable to start the project vscode workspace")
    check_version()


@cli.command(help="Run an Anvil project")
def run() -> None:
    """
    Runs an Anvil Project
    """
    if not FileExists("anvilconfig.json"):
        click.echo("No valid Anvil project found, to create a new project run: `anvil create --help`")
    else:
        with open("./anvilconfig.json", "r") as file:
            data: dict = json.loads(file.read())
            entry_point = data.get(ConfigSection.ANVIL).get(ConfigOption.ENTRY_POINT)
            if not entry_point:
                click.echo("No entry point found in the Anvil project configuration.")
                return

        process_subcommand(f"py {os.path.join(*entry_point.split('/'))}", "Unable to run the anvil project.")
