import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

import click

from anvil.lib import scaffold
from anvil.lib.config import (
    Config,
    ConfigOption,
    ConfigSection,
    validate_namespace_project_name,
)
from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import (
    DESKTOP,
    OUTPUT,
    PREVIEW_COM_MOJANG,
    RELEASE_COM_MOJANG,
    AnvilDisplay,
    AnvilIO,
    AnvilValidator,
    Directory,
    process_subcommand,
)


def handle_configuration(
    namespace: str,
    project_name: str,
    display_name: str,
    preview: bool,
    scriptapi: bool,
    addon: bool,
):
    config = Config(allow_missing=True)

    config.add_option(ConfigSection.PACKAGE, ConfigOption.NAMESPACE, namespace)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME, project_name)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.COMPANY, namespace.title())
    config.add_option(ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME, display_name)
    config.add_option(
        ConfigSection.PACKAGE, ConfigOption.PROJECT_DESCRIPTION, f"{display_name} Packs"
    )
    config.add_option(
        ConfigSection.PACKAGE,
        ConfigOption.BEHAVIOUR_DESCRIPTION,
        f"{display_name} behavior Pack",
    )
    config.add_option(
        ConfigSection.PACKAGE,
        ConfigOption.RESOURCE_DESCRIPTION,
        f"{display_name} Resource Pack",
    )
    config.add_option(
        ConfigSection.PACKAGE, ConfigOption.TARGET, "addon" if addon else "world"
    )

    config.add_option(ConfigSection.MANIFEST, ConfigOption.RELEASE, "1.0.0")
    config.add_option(ConfigSection.MANIFEST, ConfigOption.RP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.MANIFEST, ConfigOption.BP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.MANIFEST, ConfigOption.PACK_UUID, str(uuid.uuid4()))
    config.add_option(
        ConfigSection.MANIFEST, ConfigOption.DATA_MODULE_UUID, str(uuid.uuid4())
    )
    config.add_option(
        ConfigSection.MANIFEST, ConfigOption.RESOURCE_MODULE_UUID, str(uuid.uuid4())
    )

    config.add_option(ConfigSection.FEATURES, ConfigOption.SCRIPT_API, scriptapi)
    config.add_option(ConfigSection.FEATURES, ConfigOption.SCRIPT_UI, scriptapi)
    config.add_option(ConfigSection.FEATURES, ConfigOption.PBR, False)
    config.add_option(ConfigSection.FEATURES, ConfigOption.RANDOM_SEED, False)
    config.add_option(ConfigSection.FEATURES, ConfigOption.EXPERIMENTAL, False)

    config.add_option(ConfigSection.BUILD, ConfigOption.PREVIEW, preview)
    config.add_option(
        ConfigSection.BUILD, ConfigOption.ENTRY_POINT, "scripts/python/main.py"
    )
    config.add_option(ConfigSection.BUILD, ConfigOption.MINIFY, False)
    config.add_option(ConfigSection.BUILD, ConfigOption.ADD_STAMP, True)
    config.add_option(
        ConfigSection.BUILD,
        ConfigOption.LOCAL_EXPORT,
        sys.platform != "win32",
    )

    config.add_option(
        ConfigSection.ANVIL,
        ConfigOption.LAST_CHECK,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    config.add_option(ConfigSection.ANVIL, ConfigOption.VANILLA_VERSION, MANIFEST_BUILD)

    return config


def create_directories_from_tree(tree: dict) -> None:
    """
    Recursively creates directories based on the structure of a tree.

    Args:
        tree (dict): The tree structure representing the directories.

    Returns:
        None
    """

    def find_key(tree: dict, path: Path, a: list) -> list:
        """
        Recursively finds keys in the tree structure.

        Args:
            tree (dict): The tree structure.
            path (Path): The current path.
            a (list): The list to store the found keys.

        Returns:
            list: The list of found keys.
        """
        for key, value in tree.items():
            if isinstance(value, dict):
                find_key(value, path / key, a)
            if value == {}:
                a.append(path / key)
        return a

    directories = find_key(tree, Path(), a=[])
    for directory in directories:
        Directory.create(directory)


def handle_script(
    config: Config,
    namespace: str,
    project_name: str,
    DEV_BEH_DIR: Path,
    WORKING_DIR: Path,
    vscode: bool,
) -> None:
    click.echo("Initiating ScriptingAPI modules")
    install_dependencies = [
        "@minecraft/server",
        "@minecraft/server-ui",
        "@minecraft/vanilla-data",
        "@starktma/minecraft-utils",
        "esbuild",
    ]

    script_uuid = str(uuid.uuid4())
    config.add_option(
        ConfigSection.MANIFEST, ConfigOption.DATA_MODULE_UUID, script_uuid
    )
    config.add_option(
        ConfigSection.BUILD, ConfigOption.JS_BUNDLE_SCRIPT, "node esbuild.js"
    )
    DEV_BEH_DIR = (
        DEV_BEH_DIR
        / f"BP_{config.get_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME)}"
    )

    AnvilIO.file(
        "package.json",
        scaffold.package_json(
            project_name,
            "1.0.0",
            str(config.get_option(ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME))
            + " Essentials",
            config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY),
        ),
        "",
        "w",
    )
    AnvilIO.file("tsconfig.json", scaffold.tsconfig(DEV_BEH_DIR), "", "w")
    AnvilIO.file(
        "esbuild.js",
        scaffold.esbuild_js(),
        "",
        "w",
    )
    AnvilIO.file(
        "constants.ts",
        scaffold.ts_constants(namespace, project_name),
        Path("scripts", "javascript"),
        "w",
    )
    AnvilIO.file(
        "main.ts",
        'import { world, system } from "@minecraft/server";\n',
        Path("scripts", "javascript"),
        "w",
    )
    if vscode:
        AnvilIO.file(
            "launch.json",
            scaffold.vscode_launch(
                DEV_BEH_DIR / "scripts",
                WORKING_DIR / "scripts" / "javascript",
                script_uuid,
                project_name,
            ),
            ".vscode",
            "w",
        )

    click.echo(f"Installing npm packages... [{', '.join(install_dependencies)}]")
    process_subcommand(
        f"npm init -y && npm install {' '.join(install_dependencies)}",
        f"Unable to initiate npm packages [{', '.join(install_dependencies)}].",
    )


@click.command(help="Initiate an Anvil project")
@click.argument("namespace")
@click.argument("project_name")
@click.option(
    "--preview",
    is_flag=True,
    default=False,
    show_default=True,
    help="Generates the project in Minecraft Preview com.mojang.",
)
@click.option(
    "--scriptapi",
    is_flag=True,
    default=False,
    show_default=True,
    help="Adds dependencies support of ScriptAPI.",
)
@click.option(
    "--addon",
    is_flag=True,
    default=False,
    show_default=True,
    help="Sets this package as an addon, comes with many restrictions.",
)
@click.option(
    "--vscode",
    is_flag=True,
    default=False,
    show_default=True,
    help="Adds support for Visual Studio Code.",
)
def init(
    namespace: str,
    project_name: str,
    preview: bool = False,
    scriptapi: bool = False,
    addon: bool = False,
    vscode: bool = False,
) -> None:
    validate_namespace_project_name(namespace, project_name, addon)
    display_name = project_name.title().replace("-", " ").replace("_", " ")
    AnvilDisplay.copyright()
    click.echo(f"Initiating {display_name}")
    config = handle_configuration(
        namespace, project_name, display_name, preview, scriptapi, addon
    )
    create_directories_from_tree(
        {
            project_name: {
                "assets": {
                    "structures": {},
                    "bbmodels": {},
                    "textures": {
                        "environment": {},
                        "items": {},
                        "ui": {},
                    },
                    "sounds": {},
                    "particles": {},
                    "skins": {},
                },
                "scripts": {"javascript": {}, "python": {}},
                "world": {},
                "marketing": {},
                "output": {},
            }
        }
    )
    os.chdir(project_name)
    config.save()
    WORKING_DIR = Path.cwd()
    local_export = (
        bool(config.get_option(ConfigSection.BUILD, ConfigOption.LOCAL_EXPORT))
        if config.has_option(ConfigSection.BUILD, ConfigOption.LOCAL_EXPORT)
        else (sys.platform != "win32")
    )
    if local_export or sys.platform != "win32":
        COM_MOJANG = WORKING_DIR / OUTPUT / "com.mojang"
    else:
        COM_MOJANG = PREVIEW_COM_MOJANG if preview else RELEASE_COM_MOJANG

    DEV_RES_DIR = COM_MOJANG / "development_resource_packs"
    DEV_BEH_DIR = COM_MOJANG / "development_behavior_packs"

    AnvilIO.file("main.py", scaffold.main_py(), Path("scripts", "python"), "w")
    AnvilIO.file(".gitignore", scaffold.gitignore(), "", "w")
    AnvilIO.file(
        "release.yml",
        scaffold.github_release_workflow(project_name),
        Path(".github", "workflows"),
        "w",
    )
    AnvilIO.file("CHANGELOG.md", "", "", "w")
    if scriptapi:
        handle_script(config, namespace, project_name, DEV_BEH_DIR, WORKING_DIR, vscode)
    if vscode:
        workspace_file = f"{project_name}.code-workspace"
        workspace_dir = DESKTOP if DESKTOP.is_dir() else WORKING_DIR
        AnvilIO.file(
            workspace_file,
            scaffold.code_workspace(
                config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY),
                WORKING_DIR,
                preview,
                dev_res_path=DEV_RES_DIR,
                dev_beh_path=DEV_BEH_DIR,
            ),
            workspace_dir,
            "w",
        )
        workspace_full_path = workspace_dir / workspace_file
        if sys.platform == "win32":
            process_subcommand(
                f'start "" "{workspace_full_path}"',
                "Unable to start the project vscode workspace",
            )
        elif sys.platform == "darwin":
            process_subcommand(
                f'open "{workspace_full_path}"',
                "Unable to start the project vscode workspace",
            )
        else:
            process_subcommand(
                f'xdg-open "{workspace_full_path}"',
                "Unable to start the project vscode workspace",
            )
    AnvilValidator.check_new_versions()
