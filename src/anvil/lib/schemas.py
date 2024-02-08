import os
import uuid

from anvil import CONFIG
from anvil.lib.format_versions import *
from anvil.lib.lib import File


class JsonSchemes:
    """A class used to read and write to the json_schemes.json file."""

    @staticmethod
    def pack_name_lang(name, description):
        return [f"pack.name={name}", f"pack.description={description}"]

    @staticmethod
    def skin_pack_name_lang(name, display_name):
        return [f"skinpack.{name}={display_name}"]

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
    def skins_json(serialize_name):
        return {
            "serialize_name": serialize_name,
            "localization_name": serialize_name,
            "skins": [],
        }

    @staticmethod
    def skin_json(filename: str, is_slim: bool, free: bool):
        return {
            "localization_name": filename,
            "geometry": f"geometry.humanoid.{ 'customSlim' if is_slim else 'custom'}",
            "texture": f"{filename}.png",
            "type": "free" if free else "paid",
        }

    @staticmethod
    def manifest_skins(version):
        return {
            "format_version": 1,
            "header": {
                "name": "pack.name",
                "uuid": str(uuid.uuid4()),
                "version": version,
            },
            "modules": [
                {
                    "type": "skin_pack",
                    "uuid": str(uuid.uuid4()),
                    "version": version,
                }
            ],
        }

    @staticmethod
    def description(namespace, identifier):
        return {"description": {"identifier": f"{namespace}:{identifier}"}}

    @staticmethod
    def item_texture(resource_pack_name):
        return {
            "resource_pack_name": resource_pack_name,
            "texture_name": "atlas.items",
            "texture_data": {},
        }

    @staticmethod
    def sound_definitions():
        return {
            "format_version": SOUND_DEFINITIONS_VERSION,
            "sound_definitions": {},
        }

    @staticmethod
    def music_definitions():
        return {}

    @staticmethod
    def sound(name, category):
        return {name: {"category": category, "sounds": []}}

    @staticmethod
    def materials():
        return {"materials": {"version": MATERIALS_VERSION}}

    @staticmethod
    def languages():
        return [
            "en_US",
            "en_GB",
            "de_DE",
            "es_ES",
            "es_MX",
            "fr_FR",
            "fr_CA",
            "it_IT",
            "pt_BR",
            "pt_PT",
            "ru_RU",
            "zh_CN",
            "zh_TW",
            "nl_NL",
            "bg_BG",
            "cs_CZ",
            "da_DK",
            "el_GR",
            "fi_FI",
            "hu_HU",
            "id_ID",
            "nb_NO",
            "pl_PL",
            "sk_SK",
            "sv_SE",
            "tr_TR",
            "uk_UA",
        ]

    @staticmethod
    def client_description():
        return {
            "materials": {"default": "entity_alphatest"},
            "scripts": {"pre_animation": [], "initialize": [], "animate": []},
            "textures": {},
            "geometry": {},
            "particle_effects": {},
            "sound_effects": {},
            "render_controllers": [],
        }

    @staticmethod
    def client_entity():
        return {
            "format_version": ENTITY_CLIENT_VERSION,
            "minecraft:client_entity": {},
        }

    @staticmethod
    def server_entity():
        return {
            "format_version": ENTITY_SERVER_VERSION,
            "minecraft:entity": {
                "component_groups": {},
                "components": {},
                "events": {},
            },
        }

    @staticmethod
    def bp_animations():
        return {"format_version": BP_ANIMATION_VERSION, "animations": {}}

    @staticmethod
    def bp_animation(animation_name, part, animation_type, loop):
        return {
            f"animation.{animation_name}.{part}.{animation_type}": {
                "loop": loop,
                "timeline": {},
            }
        }

    @staticmethod
    def rp_animations():
        return {"format_version": RP_ANIMATION_VERSION, "animations": {}}

    @staticmethod
    def animation_controller_state(state):
        return {
            state: {
                "on_entry": [],
                "on_exit": [],
                "animations": [],
                "transitions": [],
            }
        }

    @staticmethod
    def animation_controller(controller_name, part, animation_type):
        return {
            f"controller.animation.{controller_name}.{part}.{animation_type}": {
                "initial_state": "default",
                "states": {},
            }
        }

    @staticmethod
    def animation_controllers():
        return {
            "format_version": ANIMATION_CONTROLLERS_VERSION,
            "animation_controllers": {},
        }

    @staticmethod
    def geometry():
        return {
            "format_version": GEOMETRY_VERSION,
            "minecraft:geometry": [],
        }

    @staticmethod
    def render_controller(controller_name, part, controller_type):
        return {
            f"controller.render.{controller_name}.{part}.{controller_type}": {
                "arrays": {"textures": {}, "geometries": {}},
                "materials": [],
                "geometry": {},
                "textures": [],
                "part_visibility": [],
            }
        }

    @staticmethod
    def render_controllers():
        return {
            "format_version": RENDER_CONTROLLER_VERSION,
            "render_controllers": {},
        }

    @staticmethod
    def attachable():
        return {"format_version": ENTITY_CLIENT_VERSION, "minecraft:attachable": {}}

    @staticmethod
    def spawn_rules():
        return {
            "format_version": SPAWN_RULES_VERSION,
            "minecraft:spawn_rules": {"conditions": []},
        }

    @staticmethod
    def server_block():
        return {
            "format_version": BLOCK_SERVER_VERSION,
            "minecraft:block": {
                "description": {},
                "components": {},
                "permutations": [],
            },
        }

    @staticmethod
    def terrain_texture(resource_pack_name):
        return {
            "num_mip_levels": 4,
            "padding": 8,
            "resource_pack_name": resource_pack_name,
            "texture_data": {},
            "texture_name": "atlas.terrain",
        }

    @staticmethod
    def flipbook_textures():
        return []

    @staticmethod
    def font(font_name, font_file):
        return {
            "version": 1,
            "fonts": [
                {
                    "font_format": "ttf",
                    "font_name": font_name,
                    "version": 1,
                    "font_file": f"font/{font_file}",
                    "lowPerformanceCompatible": False,
                }
            ],
        }

    @staticmethod
    def fog():
        return {
            "format_version": FOG_VERSION,
            "minecraft:fog_settings": {
                "distance": {},
                "volumetric": {},
            },
        }

    @staticmethod
    def dialogues():
        return {
            "format_version": DIALOGUE_VERSION,
            "minecraft:npc_dialogue": {"scenes": []},
        }

    @staticmethod
    def dialogue_scene(scene_tag, npc_name, text, on_open_commands, on_close_commands, buttons):
        return {
            "scene_tag": scene_tag,
            "npc_name": npc_name,
            "text": text,
            "on_open_commands": on_open_commands,
            "on_close_commands": on_close_commands,
            "buttons": buttons,
        }

    @staticmethod
    def dialogue_button(name, commands):
        return {"name": name, "commands": commands}

    @staticmethod
    def server_item():
        return {
            "format_version": ITEM_SERVER_VERSION,
            "minecraft:item": {"components": {}},
        }

    @staticmethod
    def camera_preset(namespace, name, inherit_from):
        return {
            "format_version": CAMERA_PRESET_VERSION,
            "minecraft:camera_preset": {
                "identifier": f"{namespace}:{name}",
                "inherit_from": inherit_from,
            },
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

    @staticmethod
    def blocks():
        return {
            "format_version": [int(i) for i in BLOCK_JSON_FORMAT_VERSION.split(".")],
        }

    # ---------------------------
    @staticmethod
    def sounds():
        return {
            "individual_event_sounds": {},
            "block_sounds": {},
            "entity_sounds": {"entities": {}},
            "interactive_sounds": {},
        }

    @staticmethod
    def directional_lights():
        return {
            "format_version": GLOBAL_LIGHTING.split("."),
            "directional_lights": {},
            "pbr": {},
        }

    @staticmethod
    def atmospherics():
        return {
            "horizon_blend_stops": {},
        }

    @staticmethod
    def loot_table():
        return {"pools": []}


class AddonObject:
    """
    An object representing an addon with functionality to modify its content, queue it for processing, and export it.

    Attributes:
        _extension (dict): A mapping of file extension types with the different namespace formats.
        _name (str): The name of the addon object.
        _path (str): The path of the addon object.
        _content (dict): The content of the addon object.
        _directory (str): The directory where the addon object is located.
        _shorten (bool): A flag indicating whether the content should be shortened.
    """

    _extension = ".json"
    _path = ""

    def __init__(self, name: str) -> None:
        """
        Constructs all the necessary attributes for the AddonObject object.

        Args:
            name (str): The name of the addon object.
            path (str): The path of the addon object.
        """
        self._shorten = True
        self._name = name
        self._content = {}
        self._directory = ""
        CONFIG.Logger.object_initiated(self._name)

    @property
    def do_not_shorten(self):
        """
        Setter property that disables shortening of `dict` when exporting.
        """
        self._shorten = False

    def content(self, content):
        """
        Sets the content of the addon object and returns the object.

        Args:
            content (any): The content to be set for the addon object.

        Returns:
            self: The instance of the current AddonObject.
        """
        self._content = content
        return self

    def queue(self, directory: str | None = None):
        """
        Queues the addon object for processing and logs the event.

        Args:
            directory (str, optional): The directory of the addon object.

        Returns:
            self: The instance of the current AddonObject.
        """
        from anvil import ANVIL

        self._directory = directory if not directory is None else ""
        self._path = os.path.join(self._path, self._directory)
        CONFIG.Logger.object_queued(self._name)
        ANVIL._queue(self)
        return self

    def _export(self):
        """
        Exports the addon object after potentially shortening its content and replacing backslashes.
        Logs the event and writes the object to a file.
        """

        def _shorten_dict(d):
            if isinstance(d, dict):
                return {
                    k: v
                    for k, v in ((k, _shorten_dict(v)) for k, v in d.items())
                    if v != {} and v != [] or str(k).startswith("minecraft:")
                }

            elif isinstance(d, list):
                return [v for v in map(_shorten_dict, d) if v != []]

            return d

        def _replace_backslashes(obj):
            if isinstance(obj, str):
                return obj.replace("\\", "/").replace('"/n"', '"\\n"').replace("/n", "\n")
            elif isinstance(obj, list):
                return [_replace_backslashes(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: _replace_backslashes(value) for key, value in obj.items()}
            else:
                return obj

        path = self._path.removeprefix(CONFIG.RP_PATH).removeprefix(CONFIG.BP_PATH)
        path = os.path.join(path, f"{self._name}{self._extension}")
        if len(path) > 80:
            CONFIG.Logger.path_length_error(path)

        if self._shorten and type(self._content) is dict:
            self._content = _shorten_dict(self._content)

        self._content = _replace_backslashes(self._content)
        CONFIG.Logger.object_exported(self._name)
        File(f"{self._name}{self._extension}", self._content, self._path, "w")


class MinecraftDescription:
    """Handles Minecraft descriptions.

    Attributes:
        name (str): The name of the Minecraft object.
        is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
    """

    def _validate_name(self, name: str):
        """Validates the name of the Minecraft object.

        Args:
            name (str): The name of the Minecraft object.
        """
        if ":" in name:
            CONFIG.Logger.namespaces_not_allowed(name)

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes a MinecraftDescription instance.

        Args:
            name (str): The name of the Minecraft object.
            is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
        """
        self._validate_name(name)
        self._name = name
        self._is_vanilla = is_vanilla
        self._namespace = "minecraft" if is_vanilla else CONFIG.NAMESPACE
        self._description: dict = JsonSchemes.description(self._namespace, self._name)

    @property
    def identifier(self) -> str:
        """Formulates the identifier for the Minecraft object.

        Returns:
            str: The identifier in the format 'namespace_format:name'
        """
        return f"{self._namespace}:{self._name}"

    @property
    def name(self) -> str:
        """Returns the name of the Minecraft object.

        Returns:
            str: The name
        """
        return self._name

    @property
    def is_vanilla(self) -> bool:
        """Returns if the Minecraft object is from vanilla Minecraft.

        Returns:
            bool: If the object is from vanilla Minecraft
        """
        return self._is_vanilla

    @property
    def to_dict(self) -> dict:
        """Returns the description of the Minecraft object.

        Returns:
            dict: The description
        """
        return self._description
