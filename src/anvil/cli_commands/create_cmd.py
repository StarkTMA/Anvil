import os
import uuid
from datetime import datetime

import click
from click_aliases import ClickAliasedGroup

from anvil.lib.config import Config, ConfigOption, ConfigSection
from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import (
    DESKTOP,
    PREVIEW_COM_MOJANG,
    RELEASE_COM_MOJANG,
    AnvilDisplay,
    AnvilIO,
    AnvilValidator,
    Directory,
    process_subcommand,
)
from anvil.lib.templater import load_file

from ..__version__ import __version__


class JsonSchemes:
    """Collection of static methods for generating various project templates and configurations."""

    @staticmethod
    def python():
        """Generates a Python template.

        Returns:
            str: The Python template content.
        """
        return load_file("python.jsont")

    @staticmethod
    def package_json(project_name, version, description, author):
        """Generates a package.json template.

        Args:
            project_name (str): The name of the project.
            version (str): The version of the project.
            description (str): The project description.
            author (str): The project author.

        Returns:
            dict: The package.json template data.
        """
        return load_file(
            "package_json.jsont",
            {
                "project_name": project_name,
                "version": version,
                "description": description,
                "author": author,
            },
            is_json=True,
        )

    @staticmethod
    def vscode(path, wkspc, script_uuid, project_name):
        """Generates a VSCode configuration template.

        Args:
            path (str): The project path.
            wkspc (str): The workspace path.
            script_uuid (str): The script UUID.
            project_name (str): The project name.

        Returns:
            dict: The VSCode configuration data.
        """
        return load_file(
            "vscode.jsont",
            {
                "script_uuid": script_uuid,
                "wkspc": wkspc,
                "path": path,
                "project_name": project_name,
            },
            is_json=True,
        )

    @staticmethod
    def gitignore():
        """Generates a .gitignore template.

        Returns:
            str: The .gitignore template content.
        """
        return load_file("gitignore.jsont")

    @staticmethod
    def code_workspace(name, path, preview=False):
        """Generates a VS Code workspace configuration.

        Args:
            name (str): The workspace name.
            path1 (str): The first path component.
            path2 (str): The second path component.
            preview (bool, optional): Whether this is for preview mode. Defaults to False.

        Returns:
            dict: The workspace configuration data.
        """
        DEV_RES_DIR = os.path.join(RELEASE_COM_MOJANG, "development_resource_packs")
        DEV_BEH_DIR = os.path.join(RELEASE_COM_MOJANG, "development_behavior_packs")

        DEV_PREV_RES_DIR = os.path.join(
            PREVIEW_COM_MOJANG, "development_resource_packs"
        )
        DEV_PREV_BEH_DIR = os.path.join(
            PREVIEW_COM_MOJANG, "development_behavior_packs"
        )

        return load_file(
            "code_workspace.jsont",
            {
                "name": name,
                "path": path,
                "dev_res_path": DEV_RES_DIR,
                "dev_beh_path": DEV_BEH_DIR,
                "dev_prev_res_path": DEV_PREV_RES_DIR,
                "dev_prev_beh_path": DEV_PREV_BEH_DIR,
            },
            is_json=True,
        )

    @staticmethod
    def tsconfig(out_dir):
        return load_file(
            "tsconfig.jsont",
            {"out_dir": os.path.join(out_dir, "scripts")},
            is_json=True,
        )

    @staticmethod
    def esbuild_config_js(outDir, minify: bool = False):
        return load_file(
            "esbuild.jsont",
            {
                "out_dir": outDir,
                "minify": minify,
            },
        )

    @staticmethod
    def tsconstants(namespace: str, project_name: str):
        return load_file(
            "tsconstants.jsont", {"namespace": namespace, "project_name": project_name}
        )


def handle_configuration(
    namespace: str,
    project_name: str,
    display_name: str,
    preview: bool,
    scriptapi: bool,
    addon: bool,
):
    config = Config()

    config.add_option(
        ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, MANIFEST_BUILD
    )

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

    config.add_option(ConfigSection.ANVIL, ConfigOption.DEBUG, False)
    config.add_option(
        ConfigSection.ANVIL,
        ConfigOption.PASCAL_PROJECT_NAME,
        "".join(x[0] for x in project_name.split("_")).upper(),
    )
    config.add_option(
        ConfigSection.ANVIL,
        ConfigOption.LAST_CHECK,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    config.add_option(ConfigSection.ANVIL, ConfigOption.SCRIPT_API, scriptapi)
    config.add_option(ConfigSection.ANVIL, ConfigOption.SCRIPT_UI, scriptapi)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PBR, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.RANDOM_SEED, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.EXPERIMENTAL, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PREVIEW, preview)
    config.add_option(
        ConfigSection.ANVIL, ConfigOption.ENTRY_POINT, "scripts/python/main.py"
    )
    config.add_option(ConfigSection.ANVIL, ConfigOption.MINIFY, False)

    config.add_option(ConfigSection.BUILD, ConfigOption.RELEASE, "1.0.0")
    config.add_option(ConfigSection.BUILD, ConfigOption.RP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.BP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.PACK_UUID, str(uuid.uuid4()))
    config.add_option(
        ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, str(uuid.uuid4())
    )

    config.add_section(namespace)

    return config


def create_directories_from_tree(tree: dict) -> None:
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
        Directory.create(directory)


def handle_script(
    config: Config,
    namespace: str,
    project_name: str,
    DEV_BEH_DIR: str,
    WORKING_DIR: str,
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
    config.add_option(ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, script_uuid)
    config.add_option(
        ConfigSection.ANVIL, ConfigOption.JS_BUNDLE_SCRIPT, "node esbuild.js"
    )
    DEV_BEH_DIR = os.path.join(
        DEV_BEH_DIR,
        f"BP_{config.get_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME)}",
    )

    AnvilIO.file(
        "package.json",
        JsonSchemes.package_json(
            project_name,
            "1.0.0",
            str(config.get_option(ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME))
            + " Essentials",
            config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY),
        ),
        "",
        "w",
        True,
    )
    AnvilIO.file("tsconfig.json", JsonSchemes.tsconfig(DEV_BEH_DIR), "", "w", False)
    AnvilIO.file(
        "esbuild.js",
        JsonSchemes.esbuild_config_js(
            os.path.join(DEV_BEH_DIR, "scripts"),
            bool(config.get_option(ConfigSection.ANVIL, ConfigOption.MINIFY)),
        ),
        "",
        "w",
        False,
    )
    AnvilIO.file(
        "constants.ts",
        JsonSchemes.tsconstants(namespace, project_name),
        os.path.join("scripts", "javascript"),
        "w",
        False,
    )
    AnvilIO.file(
        "main.ts",
        'import { world, system } from "@minecraft/server";\n',
        os.path.join("scripts", "javascript"),
        "w",
        False,
    )
    if vscode:
        AnvilIO.file(
            "launch.json",
            JsonSchemes.vscode(
                os.path.join(DEV_BEH_DIR, "scripts"),
                os.path.join(WORKING_DIR, "scripts", "javascript"),
                script_uuid,
                project_name,
            ),
            ".vscode",
            "w",
            False,
        )

    print(f"Installing npm packages... [{', '.join(install_dependencies)}]")
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
    AnvilValidator.validate_namespace_project_name(namespace, project_name, addon)
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
    WORKING_DIR = os.getcwd()
    COM_MOJANG = PREVIEW_COM_MOJANG if preview else RELEASE_COM_MOJANG
    DEV_RES_DIR = os.path.join(COM_MOJANG, "development_resource_packs")
    DEV_BEH_DIR = os.path.join(COM_MOJANG, "development_behavior_packs")
    AnvilIO.file("main.py", JsonSchemes.python(), "scripts/python/", "w")
    AnvilIO.file(".gitignore", JsonSchemes.gitignore(), "", "w")
    AnvilIO.file("CHANGELOG.md", "", "", "w")
    if scriptapi:
        handle_script(config, namespace, project_name, DEV_BEH_DIR, WORKING_DIR, vscode)
    if vscode:
        AnvilIO.file(
            f"{project_name}.code-workspace",
            JsonSchemes.code_workspace(
                config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY),
                WORKING_DIR,
                preview,
            ),
            DESKTOP,
            "w",
        )
        process_subcommand(
            f"start {os.path.join(DESKTOP, f'{project_name}.code-workspace')}",
            "Unable to start the project vscode workspace",
        )
    AnvilValidator.check_new_versions()
