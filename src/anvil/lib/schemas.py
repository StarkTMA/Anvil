from __future__ import annotations

import os
import uuid
from typing import Any, Dict, List, Mapping

from anvil import CONFIG
from anvil.lib.config import ConfigPackageTarget
from anvil.lib.format_versions import *
from anvil.lib.lib import File, salt_from_str
from anvil.lib.types import Identifier
from packaging.version import Version


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
    def bp_animation(identifier, animation_short_name, loop):
        return {
            f"animation.{identifier.replace(':', '.')}.{animation_short_name}": {
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
    def animation_controller(identifier, controller_shortname):
        return {
            f"controller.animation.{identifier.replace(':', '.')}.{controller_shortname}": {
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
    def render_controller(identifier, controller_name):
        return {
            f"controller.render.{identifier.replace(':', '.')}.{controller_name}": {
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
    def camera_preset(identifier, inherit_from):
        return {
            "format_version": CAMERA_PRESET_VERSION,
            "minecraft:camera_preset": {
                "identifier": identifier,
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
    def smelting_recipe(identifier: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_furnace": {
                "tags": tags,
                "description": {"identifier": identifier},
            },
        }

    @staticmethod
    def smithing_table_recipe(identifier: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_smithing_transform": {
                "description": {"identifier": identifier},
                "tags": tags,
            },
        }

    @staticmethod
    def smithing_table_trim_recipe(identifier: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_smithing_trim": {
                "description": {"identifier": identifier},
                "tags": tags,
            },
        }

    @staticmethod
    def shapeless_crafting_recipe(identifier: str, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_shapeless": {
                "description": {"identifier": identifier},
                "tags": tags,
                "ingredients": [],
            },
        }

    @staticmethod
    def shaped_crafting_recipe(identifier: str, assume_symmetry: bool, tags: list[str]):
        return {
            "format_version": RECIPE_JSON_FORMAT_VERSION,
            "minecraft:recipe_shaped": {
                "description": {"identifier": identifier},
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
                "identifier": identifier,
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
    def jigsaw_template_pools(identifier: str, fallback_identifier: str | None):
        return {
            "format_version": "1.21.20",
            "minecraft:template_pool": {
                "description": {"identifier": identifier},
                "elements": [],
                "fallback": fallback_identifier if fallback_identifier else {},
            },
        }

    @staticmethod
    def jigsaw_structure_set(identifier: str, separation: int, spacing: int, spread_type, placement_type):
        return {
            "format_version": JIGSAW_VERSION,
            "minecraft:structure_set": {
                "description": {"identifier": identifier},
                "placement": {
                    "type": "minecraft:random_spread",  # placement_type
                    "salt": salt_from_str(identifier),
                    "separation": separation,
                    "spacing": spacing,
                    "spread_type": spread_type,
                },
                "structures": [],
            },
        }

    @staticmethod
    def texture_set():
        return {"format_version": PBR_SETTINGS_VERSION, "minecraft:texture_set": {}}


class AddonDescriptor:
    """An object representing an addon descriptor with validation for names and namespaces."""

    _object_type = "addon_descriptor"

    def _validate_name(self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = False) -> tuple[str, str]:
        """Validates the name of the Minecraft object.

        Parameters:
            name (str): The name of the Minecraft object.
        """
        object_name: str
        object_namespace: str

        if ":" in name:
            object_namespace, object_name = name.split(":", 1)
        else:
            object_namespace = "minecraft" if is_vanilla else CONFIG.NAMESPACE
            object_name = name

        if not str(object_name)[0].isalpha():
            raise ValueError(f"Names cannot start with a digit. {self._object_type}[{name}]")

        if not str(object_namespace)[0].isalpha():
            raise ValueError(f"Namespaces cannot start with a digit. {self._object_type}[{name}]")

        if CONFIG._TARGET == ConfigPackageTarget.ADDON and is_vanilla and not is_vanilla_allowed:
            raise RuntimeError(
                f"Overriding vanilla features is not allowed for packages of type '{CONFIG._TARGET}'. {self._object_type}[{name}]"
            )

        if is_vanilla and object_namespace != "minecraft":
            raise ValueError(f"Invalid namespace '{object_namespace}' overriding Vanilla for. {self._object_type}[{name}]")

        return object_name, object_namespace

    def __init__(self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = False) -> None:
        """
        Constructs all the necessary attributes for the AddonObject object.

        Parameters:
            name (str): The name of the addon object.
        """

        self._is_vanilla = is_vanilla
        self._name, self._namespace = self._validate_name(name, is_vanilla, is_vanilla_allowed)
        self._display_name = self._name.replace("_", " ").title()

    @property
    def identifier(self) -> Identifier:
        """
        Returns the identifier of the addon object in the format 'namespace:name'.

        Returns:
            str: The identifier of the addon object.
        """
        return f"{self._namespace}:{self._name}"

    @property
    def name(self) -> str:
        """
        Returns the name of the addon object.

        Returns:
            str: The name of the addon object.
        """
        return self._name

    def __str__(self):
        return self.identifier


# For the description property of json files
class MinecraftDescription(AddonDescriptor):
    """Handles Minecraft descriptions.

    Attributes:
        name (str): The name of the Minecraft object.
        is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
    """

    def __init__(self, name, is_vanilla=False):
        super().__init__(name, is_vanilla)
        self._description: dict = JsonSchemes.description(self._namespace, self._name)

    def _export(self) -> dict:
        """Returns the description of the Minecraft object.

        Returns:
            dict: The description
        """
        return self._description


class AddonObject(AddonDescriptor):
    """
    An object representing an addon with functionality to modify its content, queue it for processing, and export it.

    Attributes:
        name (str): The name of the addon object.
        is_vanilla (bool): Indicates if the object is from vanilla Minecraft.
        object_type (str, optional): The type of the addon object.
    """

    _extension = ".json"
    _path = ""
    _object_type = "addon_object"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """
        Constructs all the necessary attributes for the AddonObject object.

        Parameters:
            name (str): The name of the addon object.
        """
        super().__init__(name, is_vanilla)

        self._directory = ""
        self._content = {}
        self._shorten = True

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
            raise ValueError(
                f"Relative file path [{path}] has [{len(path)}] characters, but cannot be more than [80] characters."
            )

        if self._shorten and type(self._content) is dict:
            self._content = _shorten_dict(self._content)

        self._content = _replace_backslashes(self._content)
        File(f"{self._name}{self._extension}", self._content, self._path, "w")


class MinecraftAddonObject(AddonDescriptor):
    def __init__(self, name, is_vanilla=False, is_vanilla_allowed=False):
        super().__init__(name, is_vanilla, is_vanilla_allowed)


class MinecraftEntityDescriptor(MinecraftAddonObject):
    _object_type = "Entity Descriptor"

    def __init__(self, name, is_vanilla=False, allow_runtime: bool = True, is_vanilla_allowed=True):
        super().__init__(name, is_vanilla, is_vanilla_allowed)
        self._allow_runtime = allow_runtime


class MinecraftBlockDescriptor(AddonDescriptor):
    _object_type = "Block Descriptor"

    def __init__(
        self,
        name,
        is_vanilla=False,
        states: Mapping[str, str | int | float | bool] = None,
        tags: set[str] = None,
        is_vanilla_allowed=True,
    ) -> None:
        super().__init__(name, is_vanilla, is_vanilla_allowed)
        self._states = states if states is not None else {}
        self._tags = tags if tags is not None else set()

    @property
    def tags(self) -> set[str]:
        """Returns the tags associated with the block."""
        return self._tags

    @property
    def states(self) -> str:
        """Returns a string representation of the block states."""
        if len(self._states.keys()) > 0:
            return "{" + ", ".join(f"{k}={v}" for k, v in self._states.items()) + "}"
        return ""

    def __str__(self) -> Identifier:
        if self.states != "":
            return f"{self.identifier} [{self.states}]"
        return self.identifier


class MinecraftItemDescriptor(AddonDescriptor):
    _object_type = "Item Descriptor"

    def __init__(self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = True) -> None:
        super().__init__(name, is_vanilla, is_vanilla_allowed)

    def __str__(self) -> Identifier:
        return self.identifier


class EntityDescriptor(MinecraftEntityDescriptor):
    def __init__(self, name: str, is_vanilla: bool = False, allow_runtime: bool = True) -> None:
        super().__init__(name, is_vanilla, allow_runtime, False)


class BlockDescriptor(MinecraftBlockDescriptor):
    def __init__(
        self, name: str, is_vanilla: bool = False, states: Mapping[str, str | int | float | bool] = None, tags: set[str] = None
    ) -> None:
        super().__init__(name, is_vanilla, states, tags, False)


class ItemDescriptor(MinecraftItemDescriptor):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name, is_vanilla, False)


class _BaseComponent(AddonDescriptor):
    _object_type = "Base Component"

    def _require_components(self, *components: "_BaseComponent") -> None:
        self._dependencies.extend(components)

    def _add_clashes(self, *components: "_BaseComponent") -> None:
        self._clashes.extend(components)

    def _enforce_version(self, current: str, minimum: str) -> None:
        if Version(current) < Version(minimum):
            raise ValueError(f"{self.identifier} requires ≥ {minimum} (got {current}).")

    def _add_field(self, key: str, value: Any) -> None:
        self._component[key] = value

    def _set_value(self, value: Dict[str, Any]) -> None:
        self._component = value

    def _get_field(self, key: str, default: Any) -> Any:
        return self._component.get(key, default)

    def _add_dict(self, value: Dict[str, Any]) -> None:
        self._component.update(value)

    def __init__(self, component_name, is_vanilla: bool = True) -> None:
        super().__init__(component_name, is_vanilla, True)
        self._dependencies: List["_BaseComponent"] = []
        self._clashes: List["_BaseComponent"] = []
        self._component: Dict[str, Any] = {}

    def __iter__(self):
        """Iterates over the component's fields."""
        return iter({self.identifier: self._component}.items())


class CustomComponent(_BaseComponent):
    """A custom component that can be used to extend the functionality of Minecraft objects.

    Attributes:
        component_name (str): The name of the component.
    """

    def __init__(self, component_name: str) -> None:
        """
        Constructs all the necessary attributes for the CustomComponent object.

        Parameters:
            component_name (str): The name of the custom component.
        """
        super().__init__(component_name, False)
