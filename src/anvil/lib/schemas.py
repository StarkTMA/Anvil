import os
import random
import uuid
from typing import Any

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
    def manifest_bp(version):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": CONFIG._BP_UUID[0],
                "version": version,
                "min_engine_version": [int(i) for i in MANIFEST_BUILD.split(".")],
            },
            "modules": [{"type": "data", "uuid": CONFIG._DATA_MODULE_UUID, "version": version}],
            "dependencies": [{"uuid": CONFIG._RP_UUID[0], "version": version}],
            "metadata": {"authors": [CONFIG.COMPANY]},
        }
        if CONFIG._SCRIPT_API:
            m["modules"].append(
                {
                    "uuid": CONFIG._SCRIPT_MODULE_UUID,
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
            if CONFIG._SCRIPT_UI:
                m["dependencies"].append(
                    {
                        "module_name": "@minecraft/server-ui",
                        "version": MODULE_MINECRAFT_SERVER_UI,
                    }
                )
        if CONFIG._TARGET == "addon":
            m["header"]["pack_scope"] = "world"
            m["metadata"]["product_type"] = "addon"
        return m

    @staticmethod
    def manifest_rp(version):
        m = {
            "format_version": 2,
            "header": {
                "description": "pack.description",
                "name": "pack.name",
                "uuid": CONFIG._RP_UUID[0],
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
            "dependencies": [{"uuid": CONFIG._BP_UUID[0], "version": version}],
            "metadata": {"authors": [CONFIG.COMPANY]},
        }
        if CONFIG._PBR:
            m.update({"capabilities": ["pbr"]})
        if CONFIG._TARGET == "addon":
            m["header"]["pack_scope"] = "world"
            m["metadata"]["product_type"] = "addon"
        return m

    @staticmethod
    def manifest_world(version):
        m = {
            "format_version": 2,
            "header": {
                "name": "pack.name",
                "description": "pack.description",
                "version": version,
                "uuid": CONFIG._PACK_UUID,
                # "platform_locked": False,
                "lock_template_options": True,
                "base_game_version": [int(i) for i in MANIFEST_BUILD.split(".")],
            },
            "modules": [
                {
                    "type": "world_template",
                    "uuid": str(uuid.uuid4()),
                    "version": version,
                }
            ],
            "metadata": {"authors": [CONFIG.COMPANY]},
        }

        if CONFIG._RANDOM_SEED:
            m["header"]["allow_random_seed"] = True

        return m

    @staticmethod
    def world_packs(version, pack_id):
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
    def geometry(model_name: str, texture_size: list[int], visible_box: list[int], visible_offset: list[int]):
        return {
            "format_version": GEOMETRY_VERSION,
            "minecraft:geometry": [
                {
                    "description": {
                        "identifier": f"geometry.{CONFIG.NAMESPACE}.{model_name}",
                        "texture_width": texture_size[0],
                        "texture_height": texture_size[1],
                        "visible_bounds_width": visible_box[0],
                        "visible_bounds_height": visible_box[1],
                        "visible_bounds_offset": visible_offset,
                    },
                    "bones": [],
                }
            ],
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

    @staticmethod
    def sounds():
        return {
            "individual_event_sounds": {},
            "block_sounds": {},
            "entity_sounds": {"entities": {}},
            "interactive_sounds": {},
        }

    @staticmethod
    def atmosphere_settings(identifier: str):
        return {
            "format_version": PBR_SETTINGS_VERSION,
            "minecraft:atmosphere_settings": {
                "identifier": identifier,
            },
        }

    @staticmethod
    def fog_settings(identifier: str):
        return {
            "format_version": FOG_VERSION,
            "minecraft:fog_settings": {
                "identifier": identifier,
                "volumetric": {},
            },
        }

    @staticmethod
    def shadow_settings():
        return {"format_version": PBR_SETTINGS_VERSION, "minecraft:shadow_settings": {}}

    @staticmethod
    def water_settings(identifier: str):
        return {
            "format_version": PBR_SETTINGS_VERSION,
            "minecraft:water_settings": {
                "description": {"identifier": identifier},
            },
        }

    @staticmethod
    def color_grading_settings(identifier: str):
        return {
            "format_version": PBR_SETTINGS_VERSION,
            "minecraft:color_grading_settings": {"description": {"identifier": identifier}, "color_grading": {}},
        }

    @staticmethod
    def client_biome(biome_identifier: str):
        return {
            "format_version": PBR_SETTINGS_VERSION,
            "minecraft:client_biome": {"description": {"identifier": biome_identifier}, "components": {}},
        }

    @staticmethod
    def lighting_settings(identifier: str):
        return {
            "format_version": PBR_SETTINGS_VERSION,
            "minecraft:lighting_settings": {"description": {"identifier": identifier}, "directional_lights": {}},
        }

    @staticmethod
    def point_lights():
        return {"format_version": PBR_SETTINGS_VERSION, "minecraft:point_light_settings": {"colors": {}}}

    @staticmethod
    def pbr_fallback_settings():
        return {
            "format_version": PBR_SETTINGS_VERSION,
            "minecraft:pbr_fallback_settings": {},
        }

    @staticmethod
    def loot_table():
        return {"pools": []}

    @staticmethod
    def smelting_recipe(namespace: str, name: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_furnace": {
                "tags": tags,
                "description": {"identifier": f"{namespace}:{name}"},
            },
        }

    @staticmethod
    def smithing_table_recipe(namespace: str, name: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_smithing_transform": {
                "description": {"identifier": f"{namespace}:{name}"},
                "tags": tags,
            },
        }

    @staticmethod
    def smithing_table_trim_recipe(namespace: str, name: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_smithing_trim": {
                "description": {"identifier": f"{namespace}:{name}"},
                "tags": tags,
            },
        }

    @staticmethod
    def shapeless_crafting_recipe(namespace: str, name: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_shapeless": {
                "description": {"identifier": f"{namespace}:{name}"},
                "tags": tags,
                "ingredients": [],
            },
        }

    @staticmethod
    def shaped_crafting_recipe(namespace: str, name: str, assume_symmetry: bool, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_shaped": {
                "description": {"identifier": f"{namespace}:{name}"},
                "tags": tags,
                "assume_symmetry": assume_symmetry,
                "pattern": [],
                "key": {},
            },
        }

    @staticmethod
    def tsconstants(namespace: str, project_name: str):
        file = []
        file.append(f'export const NAMESPACE = "{namespace}"')
        file.append(f'export const PROJECT_NAME = "{project_name}"')

        return "\n".join(file)

    @staticmethod
    def crafting_items_catalog():
        return {
            "format_version": CRAFTING_ITEMS_CATALOG,
            "minecraft:crafting_items_catalog": {"categories": []},
        }

    @staticmethod
    def aim_assist_preset(identifier: str):
        return {
            "minecraft:aim_assist_preset": {
                "identifier": f"{CONFIG.NAMESPACE}:{identifier}",
                "item_settings": {},
                "default_item_settings": "default",
                "hand_settings": "default",
                "exclusion_list": {},
                "liquid_targeting_list": {},
            }
        }

    @staticmethod
    def aim_assist_categories():
        return {"minecraft:aim_assist_categories": {"categories": []}}

    @staticmethod
    def jigsaw_structure_process(identifier: str):
        return {
            "format_version": JIGSAW_VERSION,
            "minecraft:processor_list": {
                "description": {"identifier": identifier},
                "processors": [],
            },
        }

    @staticmethod
    def jigsaw_structures(
        identifier: str,
        placement_step: str,
        start_pool_identifier: str,
        start_jigsaw_name: str | None,
        max_depth: int,
        start_height,
        liquid_settings,
    ):
        return {
            "format_version": JIGSAW_VERSION,
            "minecraft:jigsaw": {
                "description": {"identifier": identifier},
                "biome_filters": [],
                "step": placement_step,
                "start_pool": start_pool_identifier,
                "start_jigsaw_name": start_jigsaw_name if start_jigsaw_name is not None else {},
                "max_depth": max_depth,
                "start_height": start_height,
                "pool_aliases": [],
                "liquid_settings": liquid_settings,
            },
        }

    @staticmethod
    def jigsaw_template_pools(identifier: str, fallback_identifier: str):
        return {
            "format_version": "1.21.20",
            "minecraft:template_pool": {
                "description": {"identifier": identifier},
                "elements": [],
                "fallback": fallback_identifier,
            },
        }

    @staticmethod
    def jigsaw_structure_set(identifier: str, separation: int, spacing: int):
        return {
            "format_version": JIGSAW_VERSION,
            "minecraft:structure_set": {
                "description": {"identifier": identifier},
                "placement": {
                    "type": "minecraft:random_spread",
                    "salt": random.randint(0, 1000000),
                    "separation": separation,
                    "spacing": spacing,
                    "spread_type": "linear",
                },
                "structures": [],
            },
        }

    @staticmethod
    def texture_set():
        return {"format_version": PBR_SETTINGS_VERSION, "minecraft:texture_set": {}}


class AddonObject:
    """
    An object representing an addon with functionality to modify its content, queue it for processing, and export it.

    Attributes:
        name (str): The name of the addon object.
    """

    _extension = ".json"
    _path = ""

    def __init__(self, name: str) -> None:
        """
        Constructs all the necessary attributes for the AddonObject object.

        Parameters:
            name (str): The name of the addon object.
            path (str): The path of the addon object.
        """
        self._shorten = True
        self._name = name
        self._content = {}
        self._directory = ""
        self._is_vanilla = False
        CONFIG.Logger.object_initiated(self._name)

    @property
    def identifier(self) -> str:
        """
        Returns the identifier of the addon object in the format 'namespace:name'.

        Returns:
            str: The identifier of the addon object.
        """
        return f"{'minecraft' if  self._is_vanilla else CONFIG.NAMESPACE}:{self._name}"

    @property
    def do_not_shorten(self):
        """
        Setter property that disables shortening of `dict` when exporting.
        """
        self._shorten = False

    def content(self, content):
        """
        Sets the content of the addon object and returns the object.

        Parameters:
            content (any): The content to be set for the addon object.

        Returns:
            self: The instance of the current AddonObject.
        """
        self._content = content
        return self

    def queue(self, directory: str | None = None):
        """
        Queues the addon object for processing and logs the event.

        Parameters:
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
                    k: (v if v != {"do_not_shorten": True} else {})
                    for k, v in ((k, _shorten_dict(v)) for k, v in d.items())
                    if (v != {} and v != []) or str(k).startswith("minecraft:") or v == {"do_not_shorten": True}
                }

            elif isinstance(d, list):
                return [v for v in map(_shorten_dict, d) if v != []]

            return d

        def _replace_backslashes(obj):
            if isinstance(obj, str):
                return obj.replace('"/n"', '"\\n"').replace("/n", "\n").replace("\\", "/")
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

        Parameters:
            name (str): The name of the Minecraft object.
        """
        if ":" in name:
            CONFIG.Logger.namespaces_not_allowed(name)

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes a MinecraftDescription instance.

        Parameters:
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

    def _export(self) -> dict:
        """Returns the description of the Minecraft object.

        Returns:
            dict: The description
        """
        return self._description
