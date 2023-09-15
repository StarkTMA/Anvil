import json
import os
from datetime import datetime
from uuid import uuid4

import click
from github import Github

from .lib import (APPDATA, DESKTOP, CreateDirectory, File, _Config,
                  _JsonSchemes, _Logger)


def CreateDirectoriesFromTree(tree: dict) -> None:
    """
    Recursively creates directories based on the structure of a tree.

    Args:
        tree (dict): The tree structure representing the directories.

    Returns:
        None
    """

    def find_key(tree: dict, path: str, a: list) -> list:
        """
        Recursively finds keys in the tree structure.

        Args:
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
@click.option(
    "--preview",
    is_flag=True,
    default=False,
    show_default=True,
    help="Generates the project in Minecraft Preview com.mojang instead of release.",
)
@click.option(
    "--fullns",
    is_flag=True,
    default=False,
    show_default=True,
    help="Sets the Project namespace to the full namespace.project_name.",
)
@click.option(
    "--scriptapi",
    is_flag=True,
    default=False,
    show_default=True,
    help="Adds dependencies support of ScriptAPI.",
)
@click.option(
    "--pbr",
    is_flag=True,
    default=False,
    show_default=True,
    help="Adds capabilities support of Physically based rendering.",
)
def create(
    namespace: str,
    project_name: str,
    preview: bool = False,
    fullns: bool = False,
    scriptapi: bool = False,
    pbr: bool = False,
) -> None:
    """
    Create an Anvil project.

    Args:
        namespace (str): The namespace of the project.
        project_name (str): The name of the project.
        preview (bool, optional): Whether to generate the project in Minecraft Preview. Defaults to False.
        fullns (bool, optional): Whether to set the project namespace to the full namespace.project_name. Defaults to False.
        scriptapi (bool, optional): Whether to add dependencies support of ScriptAPI. Defaults to False.
        pbr (bool, optional): Whether to add capabilities support of Physically based rendering. Defaults to False.

    Returns:
        None
    """
    # Prints header
    _Logger.header()

    # Checks for Value Errors
    if len(namespace) > 8:
        _Logger.namespace_too_long(namespace)
        
    if namespace == "minecraft":
        _Logger.namespace_too_long(namespace)
    
    if len(project_name) > 16:
        _Logger.project_name_too_long(namespace)

    # Prints message
    click.echo(f'Initiating {project_name.title().replace("-", " ").replace("_", " ")}')

    # Setup the directory
    github = Github().get_repo("Mojang/bedrock-samples")
    if preview:
        target = "Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe"
        latest_build = json.loads(
            github.get_contents("version.json", "preview").decoded_content.decode()
        )["latest"]["version"]
    else:
        target = "Microsoft.MinecraftUWP_8wekyb3d8bbwe"
        latest_build = json.loads(
            github.get_contents("version.json", "main").decoded_content.decode()
        )["latest"]["version"]
    base_dir = os.path.join(
        APPDATA,
        "Local",
        "Packages",
        target,
        "LocalState",
        "games",
        "com.mojang",
        "minecraftWorlds",
    )
    os.chdir(base_dir)

    # Init the config file
    Config = _Config()
    Config.set("MINECRAFT", "vanilla_version", latest_build)
    Config.set("PACKAGE", "company", namespace.title())
    Config.set("PACKAGE", "namespace", namespace)
    Config.set("PACKAGE", "project_name", project_name)
    Config.set(
        "PACKAGE",
        "display_name",
        project_name.title().replace("-", " ").replace("_", " "),
    )
    Config.set(
        "PACKAGE",
        "project_description",
        f"{Config.get('PACKAGE', 'display_name')} Essentials",
    )

    Config.set("BUILD", "release", "1.0.0")
    Config.set("BUILD", "rp_uuid", str(uuid4()))
    Config.set("BUILD", "bp_uuid", str(uuid4()))
    Config.set("BUILD", "pack_uuid", str(uuid4()))

    Config.set("ANVIL", "debug", 0)
    Config.set("ANVIL", "scriptapi", int(scriptapi))
    Config.set("ANVIL", "pbr", int(pbr))
    Config.set("ANVIL", "namespace_format", int(fullns))
    Config.set(
        "ANVIL",
        "pascal_project_name",
        "".join(x for x in Config.get("PACKAGE", "display_name") if x.isupper()),
    )
    Config.set("ANVIL", "last_check", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    CreateDirectoriesFromTree(_JsonSchemes.structure(project_name))
    os.chdir(project_name)

    File(f"{project_name}.anvil.py", _JsonSchemes.script(), "", "w")
    File(".gitignore", _JsonSchemes.gitignore(), "", "w")
    File("CHANGELOG.md", "", "", "w")

    File(
        "en_US.lang",
        "\n".join(
            _JsonSchemes.pack_name_lang(
                Config.get("PACKAGE", "display_name"),
                Config.get("PACKAGE", "project_description"),
            )
        ),
        os.path.join(
            "behavior_packs",
            "BP_" + Config.get("ANVIL", "pascal_project_name"),
            "texts",
        ),
        "w",
    )
    File(
        "en_US.lang",
        "\n".join(
            _JsonSchemes.pack_name_lang(
                Config.get("PACKAGE", "display_name"),
                Config.get("PACKAGE", "project_description"),
            )
        ),
        os.path.join(
            "resource_packs",
            "RP_" + Config.get("ANVIL", "pascal_project_name"),
            "texts",
        ),
        "w",
    )
    File(
        "manifest.json",
        _JsonSchemes.manifest_bp([1, 0, 0], Config.get("BUILD", "bp_uuid"), scriptapi),
        os.path.join(
            "behavior_packs", "BP_" + Config.get("ANVIL", "pascal_project_name")
        ),
        "w",
    )
    File(
        "manifest.json",
        _JsonSchemes.manifest_rp([1, 0, 0], Config.get("BUILD", "rp_uuid"), pbr),
        os.path.join(
            "resource_packs", "RP_" + Config.get("ANVIL", "pascal_project_name")
        ),
        "w",
    )
    File(
        "manifest.json",
        _JsonSchemes.manifest_world(
            [1, 0, 0],
            Config.get("BUILD", "pack_uuid"),
            Config.get("PACKAGE", "company"),
        ),
        "",
        "w",
    )

    File(
        "world_behavior_packs.json",
        _JsonSchemes.world_packs(Config.get("BUILD", "bp_uuid"), [1, 0, 0]),
        "",
        "w",
    )
    File(
        "world_resource_packs.json",
        _JsonSchemes.world_packs(Config.get("BUILD", "rp_uuid"), [1, 0, 0]),
        "",
        "w",
    )

    File(
        f"{project_name}.code-workspace",
        _JsonSchemes.code_workspace(
            Config.get("PACKAGE", "company"), base_dir, project_name
        ),
        DESKTOP,
        "w",
    )

    if scriptapi:
        click.echo("Initiating ScriptingAPI modules")
        File(
            "index.js",
            "",
            os.path.join(
                "behavior_packs",
                "BP_" + Config.get("ANVIL", "pascal_project_name"),
                "scripts",
            ),
            "w",
        )
        File(
            "package.json",
            _JsonSchemes.packagejson(
                project_name,
                "1.0.0",
                Config.get("PACKAGE", "display_name") + " Essentials",
                Config.get("PACKAGE", "company"),
            ),
            "",
            "w",
            True,
        )

        # os.system('npm install -g typescript')
        os.system("npm install @minecraft/server")
        os.system("npm install @minecraft/server-ui")

    Config.save()
    # os.system(f'start {os.path.join(base_dir,project_name)}')
    os.system(f"start {os.path.join(DESKTOP, f'{project_name}.code-workspace')}")
