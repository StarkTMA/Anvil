import json
import os
import uuid
from datetime import datetime

import click
import requests

from anvil.lib.config import Config, ConfigOption, ConfigSection
from anvil.lib.format_versions import (MANIFEST_BUILD, MODULE_MINECRAFT_SERVER,
                                       MODULE_MINECRAFT_SERVER_UI)
from anvil.lib.lib import (APPDATA, DESKTOP, CreateDirectory, File,
                           process_subcommand, validate_namespace_project_name)
from anvil.lib.logger import Logger


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

class JsonSchemes:
    
    @staticmethod
    def structure(project_name):
        return {
            project_name: {
                "behavior_packs": {},
                "resource_packs": {},
                "assets": {
                    "animations": {},
                    "javascript": {},
                    "marketing": {},
                    "models": {
                        "actors": {},
                        "blocks": {},
                    },
                    "particles": {},
                    "python": {},
                    "skins": {},
                    "sounds": {},
                    "structures": {},
                    "textures": {
                        "actors": {},
                        "environment": {},
                        "blocks": {},
                        "items": {},
                        "ui": {},
                        "particle": {},
                    },
                    "output": {},
                },
            }
        }

    @staticmethod
    def script():
        return "\n".join(
            [
                "from anvil import *",
                "",
                'if __name__ == "__main__":',
                "    ANVIL.compile()",
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
            "modules": [
                {"type": "data", "uuid": str(uuid.uuid4()), "version": version}
            ],
            "dependencies": [
                {
                    "uuid": rpuuid,
                    "version": version
                }
            ],
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
            m["dependencies"].append({
                "module_name": "@minecraft/server",
                "version": MODULE_MINECRAFT_SERVER,
            })
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
            "dependencies": [
                {
                    "uuid": bp_uuid,
                    "version": version
                }
            ],
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
    def code_workspace(name, path1, path2):
        return {
            "folders": [
                {"name": name, "path": os.path.join(path1, path2)},
            ]
        }

    @staticmethod
    def packagejson(project_name, version, description, author):
        return {
            "name": project_name,
            "version": version,
            "description": description,
            "main": "scripts/main.js",
            "scripts": {"test": 'echo "Error: no test specified" && exit 1'},
            "keywords": [],
            "author": author,
            "license": "ISC",
        }

    @staticmethod
    def tsconfig(pascal_project_name):
        return {
            "compilerOptions": {
                "target": "ESNext",
                "module": "es2020",
                "declaration": False,
                "outDir": f"behavior_packs/BP_{pascal_project_name}/scripts",
                "strict": True,
                "pretty": True,
                "esModuleInterop": True,
                "moduleResolution": "Node",
                "resolveJsonModule": True,
                "noUnusedLocals": True,
                "noUnusedParameters": True,
                "forceConsistentCasingInFileNames": True,
                "lib": [
                    "ESNext",
                    "dom",
                ],
            },
            "include": ["assets/javascript/**/*"],
            "exclude": ["node_modules"],
        }

    @staticmethod
    def vscode(pascal_project_name):
        return {
            "version": "0.3.0",
            "configurations": [
                {
                    "type": "minecraft-js",
                    "request": "attach",
                    "name": "Wait for Minecraft Debug Connections",
                    "mode": "listen",
                    "localRoot": f"${{workspaceFolder}}/behavior_packs/BP_{pascal_project_name}/scripts",
                    "port": 19144,
                }
            ],
        }


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
@click.option(
    "--addon",
    is_flag=True,
    default=False,
    show_default=True,
    help="Sets this package as an addon, comes with many restrictions.",
)
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

    Args:
        namespace (str): The namespace of the project.
        project_name (str): The name of the project.
        preview (bool, optional): Whether to generate the project in Minecraft Preview. Defaults to False.
        scriptapi (bool, optional): Whether to add dependencies support of ScriptAPI. Defaults to False.
        pbr (bool, optional): Whether to add capabilities support of Physically based rendering. Defaults to False.
        random_seed (bool, optional): Whether to add support of Random Seed Worlds. Defaults to False.

    """
    # Prints header
    logger = Logger()
    logger.header()

    validate_namespace_project_name(namespace, project_name, addon)

    display_name = project_name.title().replace("-", " ").replace("_", " ")
    # Prints message
    click.echo(f"Initiating {display_name}")

    # Setup the directory
    try:
        latest_build = json.loads(
            requests.get(
                f"https://raw.githubusercontent.com/Mojang/bedrock-samples/{'preview' if preview else 'main'}/version.json"
            ).text
        )["latest"]["version"]
    except:
        latest_build = MANIFEST_BUILD
    base_dir = os.path.join(
        APPDATA,
        "Local",
        "Packages",
        f"Microsoft.Minecraft{'WindowsBeta' if preview else 'UWP'}_8wekyb3d8bbwe",
        "LocalState",
        "games",
        "com.mojang",
        "minecraftWorlds",
    )
    os.chdir(base_dir)

    CreateDirectoriesFromTree(JsonSchemes.structure(project_name))
    os.chdir(project_name)

    # Init the config file
    config = Config()
    
    config.add_option(ConfigSection.MINECRAFT, ConfigOption.VANILLA_VERSION, latest_build)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.COMPANY, namespace.title())
    config.add_option(ConfigSection.PACKAGE, ConfigOption.NAMESPACE, namespace)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_NAME, project_name)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.DISPLAY_NAME, display_name)
    config.add_option(ConfigSection.PACKAGE, ConfigOption.PROJECT_DESCRIPTION, f"{display_name} Packs")
    config.add_option(ConfigSection.PACKAGE, ConfigOption.TARGET, "addon" if addon else "world")
    config.add_option(ConfigSection.PACKAGE, ConfigOption.EXPERIMENTAL, preview)

    config.add_option(ConfigSection.BUILD, ConfigOption.RELEASE, "1.0.0")
    config.add_option(ConfigSection.BUILD, ConfigOption.RP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.BP_UUID, [str(uuid.uuid4())])
    config.add_option(ConfigSection.BUILD, ConfigOption.PACK_UUID, str(uuid.uuid4()))

    config.add_option(ConfigSection.ANVIL, ConfigOption.DEBUG, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.SCRIPT_API, scriptapi)
    config.add_option(ConfigSection.ANVIL, ConfigOption.SCRIPT_UI, False)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PBR, pbr)
    config.add_option(ConfigSection.ANVIL, ConfigOption.RANDOM_SEED, random_seed)
    config.add_option(ConfigSection.ANVIL, ConfigOption.PASCAL_PROJECT_NAME, "".join(x[0] for x in project_name.split("_")).upper())
    config.add_option(ConfigSection.ANVIL, ConfigOption.LAST_CHECK, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    config.add_section(namespace)

    config.save()
    
    File(f"{project_name}.anvil.py", JsonSchemes.script(), "", "w")
    File(".gitignore", JsonSchemes.gitignore(), "", "w")
    File("CHANGELOG.md", "", "", "w")

    File(
        "en_US.lang",
        "\n".join(
            JsonSchemes.pack_name_lang(
                config.get_option("package", "display_name"),
                config.get_option("package", "project_description"),
            )
        ),
        os.path.join(
            "behavior_packs",
            "BP_" + config.get_option("anvil", "pascal_project_name"),
            "texts",
        ),
        "w",
    )
    File(
        "en_US.lang",
        "\n".join(
            JsonSchemes.pack_name_lang(
                config.get_option("package", "display_name"),
                config.get_option("package", "project_description"),
            )
        ),
        os.path.join(
            "resource_packs",
            "RP_" + config.get_option("anvil", "pascal_project_name"),
            "texts",
        ),
        "w",
    )
    File(
        "manifest.json",
        JsonSchemes.manifest_bp([1, 0, 0], config.get_option(ConfigSection.BUILD, ConfigOption.BP_UUID)[0], config.get_option(ConfigSection.BUILD, ConfigOption.RP_UUID)[0], config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY), scriptapi, False),
        os.path.join("behavior_packs", "BP_" + config.get_option(ConfigSection.ANVIL, ConfigOption.PASCAL_PROJECT_NAME)),
        "w",
    )
    File(
        "manifest.json",
        JsonSchemes.manifest_rp([1, 0, 0], config.get_option(ConfigSection.BUILD, ConfigOption.RP_UUID)[0], config.get_option(ConfigSection.BUILD, ConfigOption.BP_UUID)[0], config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY), pbr, addon),
        os.path.join("resource_packs", "RP_" + config.get_option(ConfigSection.ANVIL, ConfigOption.PASCAL_PROJECT_NAME)),
        "w",
    )
    File(
        "manifest.json",
        JsonSchemes.manifest_world(
            [1, 0, 0], config.get_option(ConfigSection.BUILD, ConfigOption.PACK_UUID), config.get_option(ConfigSection.PACKAGE, ConfigOption.COMPANY), random_seed
        ),
        "",
        "w",
    )

    File(
        "world_behavior_packs.json",
        JsonSchemes.world_packs(config.get_option("build", "bp_uuid"), [1, 0, 0]),
        "",
        "w",
    )
    File(
        "world_resource_packs.json",
        JsonSchemes.world_packs(config.get_option("build", "rp_uuid"), [1, 0, 0]),
        "",
        "w",
    )

    File(
        f"{project_name}.code-workspace",
        JsonSchemes.code_workspace(config.get_option("package", "company"), base_dir, project_name),
        DESKTOP,
        "w",
    )

    if scriptapi:
        click.echo("Initiating ScriptingAPI modules")
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
        File("tsconfig.json", JsonSchemes.tsconfig(config.get_option("anvil", "pascal_project_name")), "", "w", False)
        File("launch.json", JsonSchemes.vscode(config.get_option("anvil", "pascal_project_name")), ".vscode", "w", False)

    config.save()

    process_subcommand(
        f"start {os.path.join(DESKTOP, f'{project_name}.code-workspace')}", "Unable to start the project vscode workspace"
    )
