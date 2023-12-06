import json
import os
from datetime import datetime
from uuid import uuid4

import click
from github import Github

from .lib import (APPDATA, DESKTOP, MANIFEST_BUILD, CreateDirectory, File,
                  _Config, _JsonSchemes, _Logger, process_subcommand, requests,
                  validate_namespace_project_name)


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
@click.option(
    "--random_seed",
    is_flag=True,
    default=False,
    show_default=True,
    help="Adds support of Random Seed Worlds.",
)
def create(
    namespace: str,
    project_name: str,
    preview: bool = False,
    fullns: bool = False,
    scriptapi: bool = False,
    pbr: bool = False,
    random_seed: bool = False,
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
        random_seed (bool, optional): Whether to add support of Random Seed Worlds. Defaults to False.

    """
    # Prints header
    _Logger.header()

    validate_namespace_project_name(namespace, project_name)
    
    display_name = project_name.title().replace("-", " ").replace("_", " ")
    # Prints message
    click.echo(f'Initiating {display_name}')

    # Setup the directory
    try:
        latest_build = json.loads(requests.get(f"https://raw.githubusercontent.com/Mojang/bedrock-samples/{'preview' if preview else 'main'}/version.json").text)["latest"]["version"]
    except:
        latest_build = ".".join(str(i) for i in MANIFEST_BUILD)
    base_dir = os.path.join(APPDATA, "Local", "Packages", f"Microsoft.Minecraft{'WindowsBeta' if preview else 'UWP'}_8wekyb3d8bbwe", "LocalState", "games", "com.mojang", "minecraftWorlds")
    os.chdir(base_dir)

    # Init the config file
    Config = _Config()
    Config.add_option("minecraft", "vanilla_version", latest_build)
    Config.add_option("package", "company", namespace.title())
    Config.add_option("package", "namespace", namespace)
    Config.add_option("package", "project_name", project_name)
    Config.add_option("package", "display_name", display_name)
    Config.add_option("package", "project_description", f"{display_name} Packs")

    Config.add_option("build", "release", [1, 0, 0])
    Config.add_option("build", "rp_uuid", [str(uuid4())])
    Config.add_option("build", "bp_uuid", [str(uuid4())])
    Config.add_option("build", "pack_uuid", str(uuid4()))

    Config.add_option("anvil", "debug", False)
    Config.add_option("anvil", "scriptapi", scriptapi)
    Config.add_option("anvil", "scriptui", False)
    Config.add_option("anvil", "pbr", pbr)
    Config.add_option("anvil", "random_seed", random_seed)
    Config.add_option("anvil", "namespace_format", fullns)
    Config.add_option("anvil", "pascal_project_name", "".join(x for x in display_name if x.isupper()))
    Config.add_option("anvil", "last_check", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    Config.add_section(namespace)
    
    CreateDirectoriesFromTree(_JsonSchemes.structure(project_name))
    os.chdir(project_name)

    File(f"{project_name}.anvil.py", _JsonSchemes.script(), "", "w")
    File(".gitignore", _JsonSchemes.gitignore(), "", "w")
    File("CHANGELOG.md", "", "", "w")

    File(
        "en_US.lang",
        "\n".join(
            _JsonSchemes.pack_name_lang(
                Config.get_option("package", "display_name"),
                Config.get_option("package", "project_description"),
            )
        ),
        os.path.join(
            "behavior_packs",
            "BP_" + Config.get_option("anvil", "pascal_project_name"),
            "texts",
        ),
        "w",
    )
    File(
        "en_US.lang",
        "\n".join(
            _JsonSchemes.pack_name_lang(
                Config.get_option("package", "display_name"),
                Config.get_option("package", "project_description"),
            )
        ),
        os.path.join(
            "resource_packs",
            "RP_" + Config.get_option("anvil", "pascal_project_name"),
            "texts",
        ),
        "w",
    )
    File(
        "manifest.json",
        _JsonSchemes.manifest_bp([1, 0, 0], Config.get_option("build", "bp_uuid"), scriptapi, False),
        os.path.join(
            "behavior_packs", "BP_" + Config.get_option("anvil", "pascal_project_name")
        ),
        "w",
    )
    File(
        "manifest.json",
        _JsonSchemes.manifest_rp([1, 0, 0], Config.get_option("build", "rp_uuid"), pbr),
        os.path.join(
            "resource_packs", "RP_" + Config.get_option("anvil", "pascal_project_name")
        ),
        "w",
    )
    File(
        "manifest.json",
        _JsonSchemes.manifest_world(
            [1, 0, 0],
            Config.get_option("build", "pack_uuid"),
            Config.get_option("package", "company"),
            random_seed
        ),
        "",
        "w",
    )

    File(
        "world_behavior_packs.json",
        _JsonSchemes.world_packs(Config.get_option("build", "bp_uuid"), [1, 0, 0]),
        "",
        "w",
    )
    File(
        "world_resource_packs.json",
        _JsonSchemes.world_packs(Config.get_option("build", "rp_uuid"), [1, 0, 0]),
        "",
        "w",
    )

    File(
        f"{project_name}.code-workspace",
        _JsonSchemes.code_workspace(
            Config.get_option("package", "company"), base_dir, project_name
        ),
        DESKTOP,
        "w",
    )

    if scriptapi:
        click.echo("Initiating ScriptingAPI modules")
        File(
            "package.json",
            _JsonSchemes.packagejson(
                project_name,
                "1.0.0",
                Config.get_option("package", "display_name") + " Essentials",
                Config.get_option("package", "company"),
            ),
            "",
            "w",
            True,
        )
        File("tsconfig.json", _JsonSchemes.tsconfig(Config.get_option("anvil", "pascal_project_name")), "", "w", False)
        File("launch.json", _JsonSchemes.vscode(Config.get_option("anvil", "pascal_project_name")), ".vscode", "w", False)

        # os.system('npm install -g typescript')
        # os.system("npm i @minecraft/server")
        # os.system("npm i @minecraft/server-ui")

    Config.save()
    # os.system(f'start {os.path.join(base_dir,project_name)}')
    process_subcommand(f"start {os.path.join(DESKTOP, f'{project_name}.code-workspace')}", "Unable to start the project vscode workspace")
