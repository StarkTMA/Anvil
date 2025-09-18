import os
import uuid
from datetime import datetime

import click
import commentjson as json
import requests
from packaging.version import Version

from anvil.lib.config import Config, ConfigOption, ConfigSection
from anvil.lib.format_versions import MANIFEST_BUILD
from anvil.lib.lib import (APPDATA, DESKTOP, CreateDirectory, File, FileExists,
                           process_subcommand, validate_namespace_project_name)
from anvil.lib.templater import load_file

from .__version__ import __version__


class JsonSchemes:
    """Collection of static methods for generating various project templates and configurations."""
    
    @staticmethod
    def python():
        """Generates a Python template.
        
        Returns:
            str: The Python template content.
        """
        return load_file("python.txt")

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
            "package_json.txt", {"project_name": project_name, "version": version, "description": description, "author": author}, is_json=True
        )

    @staticmethod
    def vscode(path, wkspc, script_uuid):
        """Generates a VSCode configuration template.
        
        Args:
            path (str): The project path.
            wkspc (str): The workspace path.
            script_uuid (str): The script UUID.
            
        Returns:
            dict: The VSCode configuration data.
        """
        return load_file("vscode.txt", {"script_uuid": script_uuid, "wkspc": wkspc, "path": path}, is_json=True)

    @staticmethod
    def gitignore():
        """Generates a .gitignore template.
        
        Returns:
            str: The .gitignore template content.
        """
        return load_file("gitignore.txt")

    @staticmethod
    def code_workspace(name, path1, path2, preview=False):
        """Generates a VS Code workspace configuration.
        
        Args:
            name (str): The workspace name.
            path1 (str): The first path component.
            path2 (str): The second path component.
            preview (bool, optional): Whether this is for preview mode. Defaults to False.
            
        Returns:
            dict: The workspace configuration data.
        """
        return load_file(
            "code_workspace.txt",
            {
                "name": name,
                "path": os.path.join(path1, path2),
                "dev_res_path": os.path.join(
                    APPDATA,
                    "Local",
                    "Packages",
                    f"Microsoft.Minecraft{'WindowsBeta' if preview else 'UWP'}_8wekyb3d8bbwe",
                    "LocalState",
                    "games",
                    "com.mojang",
                    "development_resource_packs",
                ),
                "dev_beh_path": os.path.join(
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
            is_json=True,
        )

    @staticmethod
    def tsconfig(out_dir):
        return load_file("tsconfig.txt", {"out_dir": os.path.join(out_dir, "scripts")})

    @staticmethod
    def esbuild_config_js(outDir):
        return load_file(
            "esbuild.txt", {"out_dir": os.path.join(outDir, "scripts"), "minify": Config().get_option(ConfigSection.ANVIL, ConfigOption.MINIFY)}
        )

    @staticmethod
    def tsconstants(namespace: str, project_name: str):
        return load_file("tsconstants.txt", {"namespace": namespace, "project_name": project_name})


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
    config.add_option(ConfigSection.ANVIL, ConfigOption.ENTRY_POINT, "scripts/python/main.py")
    config.add_option(ConfigSection.ANVIL, ConfigOption.MINIFY, False)

    config.add_option(ConfigSection.BUILD, ConfigOption.RELEASE, "1.0.0")
    config.add_option(ConfigSection.BUILD, ConfigOption.RP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.BP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.PACK_UUID, str(uuid.uuid4()))
    config.add_option(ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, str(uuid.uuid4()))

    config.add_section(namespace)

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


def handle_script(config: Config, namespace: str, project_name: str, DEV_BEH_DIR, WORKING_DIR) -> None:
    click.echo("Initiating ScriptingAPI modules")
    install_dependencies = ["@minecraft/server", "@minecraft/server-ui", "typescript", "esbuild"]

    script_uuid = str(uuid.uuid4())
    config.add_option(ConfigSection.BUILD, ConfigOption.DATA_MODULE_UUID, script_uuid)
    config.add_option(ConfigSection.ANVIL, ConfigOption.JS_BUNDLE_SCRIPT, "node esbuild.js")

    File(
        "package.json",
        JsonSchemes.package_json(
            project_name,
            "1.0.0",
            config.get_option("package", "display_name") + " Essentials",
            config.get_option("package", "company"),
        ),
        "",
        "w",
        True,
    )
    File(
        "launch.json",
        JsonSchemes.vscode(
            os.path.join(DEV_BEH_DIR, f"BP_{config.get_option("anvil", "pascal_project_name")}", "scripts"),
            os.path.join(WORKING_DIR, "scripts", "javascript"),
            script_uuid,
        ),
        ".vscode",
        "w",
        False,
    )
    File("tsconfig.json", JsonSchemes.tsconfig(DEV_BEH_DIR), "", "w", False)
    File("esbuild.js", JsonSchemes.esbuild_config_js(DEV_BEH_DIR), "", "w", False)
    File("constants.ts", JsonSchemes.tsconstants(namespace, project_name), os.path.join("scripts", "javascript"), "w", False)
    File("main.ts", 'import { world, system } from "@minecraft/server";\n', os.path.join("scripts", "javascript"), "w", False)

    print(f"Installing npm packages... [{', '.join(install_dependencies)}]")
    process_subcommand(
        f"npm init -y && npm install {' '.join(install_dependencies)}",
        f"Unable to initiate npm packages [{', '.join(install_dependencies)}].",
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

    CreateDirectoriesFromTree(
        {
            project_name: {
                "assets": {
                    "bbmodels": {},
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
    )

    os.chdir(project_name)
    config.save()

    if scriptapi:
        handle_script(config, namespace, project_name, DEV_BEH_DIR, WORKING_DIR)

    File("main.py", JsonSchemes.python(), "scripts/python/", "w")
    File(".gitignore", JsonSchemes.gitignore(), "", "w")
    File("CHANGELOG.md", "", "", "w")
    File(
        f"{project_name}.code-workspace",
        JsonSchemes.code_workspace(config.get_option("package", "company"), WORKING_DIR, project_name, preview),
        DESKTOP,
        "w",
    )

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
