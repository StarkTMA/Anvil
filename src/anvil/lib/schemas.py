from __future__ import annotations

import json
import os
import traceback
import uuid
from typing import Dict, Mapping

from anvil.lib.config import CONFIG, ConfigPackageTarget
from anvil.lib.format_versions import *
from anvil.lib.lib import APPDATA, File, salt_from_str
from anvil.lib.templater import load_file
from anvil.lib.types import Identifier


class JsonSchemes:
    """A class used to read and write to the json_schemes.json file."""

    @staticmethod
    def pack_name_lang(name, description):
        return load_file(
            "pack_name_lang.jsont", {"name": name, "description": description}
        ).splitlines()

    @staticmethod
    def skin_pack_name_lang(name, display_name):
        return load_file(
            "skin_pack_name_lang.jsont", {"name": name, "display_name": display_name}
        ).splitlines()

    @staticmethod
    def esbuild_config_js(outDir, minify):
        return load_file(
            "esbuild.jsont",
            {"out_dir": os.path.join(outDir, "scripts"), "minify": json.dumps(minify)},
            is_json=False,
        )

    @staticmethod
    def manifest_bp(version):
        config = CONFIG
        m = load_file(
            "manifest_bp.jsont",
            {
                "bp_uuid": config._BP_UUID[0],
                "version": version,
                "engine_version": [int(i) for i in MANIFEST_BUILD.split(".")],
                "data_module_uuid": config._DATA_MODULE_UUID,
                "rp_uuid": config._RP_UUID[0],
                "company": config.COMPANY,
            },
            is_json=True,
        )

        if config._SCRIPT_API:
            m["modules"].append(
                {
                    "uuid": config._SCRIPT_MODULE_UUID,
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
            if config._SCRIPT_UI:
                m["dependencies"].append(
                    {
                        "module_name": "@minecraft/server-ui",
                        "version": MODULE_MINECRAFT_SERVER_UI,
                    }
                )
        if config._TARGET == "addon":
            m["header"]["pack_scope"] = "world"
            m["metadata"]["product_type"] = "addon"
        return m

    @staticmethod
    def manifest_rp(version):
        config = CONFIG
        m = load_file(
            "manifest_rp.jsont",
            {
                "rp_uuid": config._RP_UUID[0],
                "version": version,
                "engine_version": [int(i) for i in MANIFEST_BUILD.split(".")],
                "resource_module_uuid": str(uuid.uuid4()),
                "bp_uuid": config._BP_UUID[0],
                "company": config.COMPANY,
            },
            is_json=True,
        )
        if config._PBR:
            m.update({"capabilities": ["pbr"]})
        if config._TARGET == "addon":
            m["header"]["pack_scope"] = "world"
            m["metadata"]["product_type"] = "addon"
        return m

    @staticmethod
    def manifest_world(version):
        config = CONFIG
        m = load_file(
            "manifest_rp.jsont",
            {
                "world_uuid": config._PACK_UUID,
                "version": version,
                "engine_version": [int(i) for i in MANIFEST_BUILD.split(".")],
                "world_module_uuid": str(uuid.uuid4()),
                "company": config.COMPANY,
            },
            is_json=True,
        )

        if config._RANDOM_SEED:
            m["header"]["allow_random_seed"] = True

        return m

    @staticmethod
    def world_packs(version, pack_ids):
        return [{"pack_id": pack, "version": version} for pack in pack_ids]

    @staticmethod
    def skin_pack(serialize_name):
        return load_file(
            "skin_pack.jsont", {"serialize_name": serialize_name}, is_json=True
        )

    @staticmethod
    def skin_json(filename: str, is_slim: bool, free: bool):
        return load_file(
            "skin_json.jsont",
            {
                "filename": filename,
                "geo_type": "customSlim" if is_slim else "custom",
                "paid": "free" if free else "paid",
            },
            is_json=True,
        )

    @staticmethod
    def manifest_skins(version):
        return load_file(
            "manifest_skins.jsont",
            {
                "skin_uuid": str(uuid.uuid4()),
                "version": version,
                "skin_module_uuid": str(uuid.uuid4()),
            },
            is_json=True,
        )

    @staticmethod
    def description(namespace, identifier):
        return {"description": {"identifier": f"{namespace}:{identifier}"}}

    @staticmethod
    def item_texture(resource_pack_name):
        return load_file(
            "item_texture.jsont",
            {"resource_pack_name": resource_pack_name},
            is_json=True,
        )

    @staticmethod
    def sound_definitions():
        return load_file(
            "sound_definitions.jsont",
            {"format_version": SOUND_DEFINITIONS_VERSION},
            is_json=True,
        )

    @staticmethod
    def music_definitions():
        return load_file("music_definitions.jsont", is_json=True)

    @staticmethod
    def sound(name, category):
        return {name: {"category": category, "sounds": []}}

    @staticmethod
    def materials() -> Dict:
        return load_file(
            "materials.jsont", {"version": MATERIALS_VERSION}, is_json=True
        )

    @staticmethod
    def languages() -> Dict:
        return load_file("languages.jsont", is_json=True)

    @staticmethod
    def client_description():
        return {
            "materials": {"default": "entity_alphatest"},
            "scripts": {
                "pre_animation": [],
                "initialize": [],
                "animate": [],
                "parent_setup": [],
            },
            "textures": {},
            "geometry": {},
            "particle_effects": {},
            "sound_effects": {},
            "render_controllers": [],
        }

    @staticmethod
    def entity_client():
        return load_file(
            "entity_client.jsont",
            {"format_version": ENTITY_CLIENT_VERSION},
            is_json=True,
        )

    @staticmethod
    def entity_server():
        return load_file(
            "entity_server.jsont",
            {"format_version": ENTITY_SERVER_VERSION},
            is_json=True,
        )

    @staticmethod
    def animations_bp():
        return load_file(
            "animations_bp.jsont",
            {"format_version": BP_ANIMATION_VERSION},
            is_json=True,
        )

    @staticmethod
    def bp_animation(identifier, animation_short_name, loop):
        return {
            f"animation.{identifier.replace(':', '.')}.{animation_short_name}": {
                "loop": loop,
                "timeline": {},
            }
        }

    @staticmethod
    def animations_rp():
        return load_file(
            "animations_rp.jsont",
            {"format_version": RP_ANIMATION_VERSION},
            is_json=True,
        )

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
        return load_file(
            "animation_controllers.jsont",
            {"format_version": ANIMATION_CONTROLLERS_VERSION},
            is_json=True,
        )

    @staticmethod
    def geometry(
        model_name: str,
        texture_size: list[int],
        visible_box: list[int],
        visible_offset: list[int],
    ):
        config = CONFIG
        return load_file(
            "geometry.jsont",
            {
                "format_version": GEOMETRY_VERSION,
                "namespace": config.NAMESPACE,
                "model_name": model_name,
                "texture_width": texture_size[0],
                "texture_height": texture_size[1],
                "visible_bounds_width": visible_box[0],
                "visible_bounds_height": visible_box[1],
                "visible_bounds_offset": visible_offset,
            },
            is_json=True,
        )

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
        return load_file(
            "render_controllers.jsont",
            {"format_version": RENDER_CONTROLLER_VERSION},
            is_json=True,
        )

    @staticmethod
    def attachable():
        return load_file(
            "attachable.jsont", {"format_version": ENTITY_CLIENT_VERSION}, is_json=True
        )

    @staticmethod
    def spawn_rules():
        return load_file(
            "spawn_rules.jsont", {"format_version": SPAWN_RULES_VERSION}, is_json=True
        )

    @staticmethod
    def server_block():
        return load_file(
            "server_block.jsont", {"format_version": BLOCK_SERVER_VERSION}, is_json=True
        )

    @staticmethod
    def terrain_texture(resource_pack_name):
        return load_file(
            "terrain_texture.jsont",
            {"resource_pack_name": resource_pack_name},
            is_json=True,
        )

    @staticmethod
    def flipbook_textures():
        return load_file("flipbook_textures.jsont", is_json=True)

    @staticmethod
    def font(font_name, font_file):
        return load_file(
            "font.jsont", {"font_name": font_name, "font_file": font_file}, is_json=True
        )

    @staticmethod
    def fog():
        return load_file("fog.jsont", {"format_version": FOG_VERSION}, is_json=True)

    @staticmethod
    def dialogues():
        return load_file(
            "dialogues_json.jsont", {"format_version": DIALOGUE_VERSION}, is_json=True
        )

    @staticmethod
    def dialogue_scene(
        scene_tag, npc_name, text, on_open_commands, on_close_commands, buttons
    ):
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
        return load_file(
            "server_item.jsont", {"format_version": ITEM_SERVER_VERSION}, is_json=True
        )

    @staticmethod
    def camera_preset(identifier, inherit_from):
        return load_file(
            "camera_preset.jsont",
            {
                "format_version": CAMERA_PRESET_VERSION,
                "identifier": identifier,
                "inherit_from": inherit_from,
            },
            is_json=True,
        )

    @staticmethod
    def package_json(project_name, version, description, author):
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
    def tsconstants(namespace: str, project_name: str):
        return load_file(
            "tsconstants.jsont", {"namespace": namespace, "project_name": project_name}
        )

    @staticmethod
    def tsconfig(out_dir):
        return load_file(
            "tsconfig.jsont",
            {"out_dir": os.path.join(out_dir, "scripts")},
            is_json=True,
        )

    @staticmethod
    def blocks_json():
        return load_file(
            "blocks_json.jsont",
            {"format_version": BLOCK_JSON_FORMAT_VERSION},
            is_json=True,
        )

    @staticmethod
    def sounds_json():
        return load_file("sounds_json.jsont", is_json=True)

    @staticmethod
    def atmosphere_settings(identifier: str):
        return load_file(
            "atmosphere_settings.jsont",
            {"format_version": PBR_SETTINGS_VERSION, "identifier": identifier},
            is_json=True,
        )

    @staticmethod
    def fog_settings(identifier: str):
        return load_file(
            "fog_settings.jsont",
            {"format_version": FOG_VERSION, "identifier": identifier},
            is_json=True,
        )

    @staticmethod
    def shadow_settings():
        return load_file(
            "shadow_settings.jsont",
            {"format_version": PBR_SETTINGS_VERSION},
            is_json=True,
        )

    @staticmethod
    def water_settings(identifier: str):
        return load_file(
            "water_settings.jsont",
            {"format_version": PBR_SETTINGS_VERSION, "identifier": identifier},
            is_json=True,
        )

    @staticmethod
    def color_grading_settings(identifier: str):
        return load_file(
            "color_grading_settings.jsont",
            {"format_version": PBR_SETTINGS_VERSION, "identifier": identifier},
            is_json=True,
        )

    @staticmethod
    def lighting_settings(identifier: str):
        return load_file(
            "lighting_settings.jsont",
            {"format_version": PBR_SETTINGS_VERSION, "identifier": identifier},
            is_json=True,
        )

    @staticmethod
    def local_lighting():
        return load_file(
            "local_lighting.jsont",
            {"format_version": PBR_SETTINGS_VERSION},
            is_json=True,
        )

    @staticmethod
    def pbr_fallback_settings():
        return load_file(
            "pbr_fallback_settings.jsont",
            {"format_version": PBR_SETTINGS_VERSION},
            is_json=True,
        )

    @staticmethod
    def loot_table():
        return load_file("loot_table.jsont", is_json=True)

    @staticmethod
    def recipe_smelting(identifier: str, tags: list[str]):
        return load_file(
            "recipe_smelting.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
            },
            is_json=True,
        )

    @staticmethod
    def recipe_smithing_table(identifier: str, tags: list[str]):
        return load_file(
            "recipe_smithing_table.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
            },
            is_json=True,
        )

    @staticmethod
    def recipe_smithing_table_trim(identifier: str, tags: list[str]):
        return load_file(
            "recipe_smithing_table_trim.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
            },
            is_json=True,
        )

    @staticmethod
    def recipe_shapeless_crafting(identifier: str, tags: list[str]):
        return load_file(
            "recipe_shapeless_crafting.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
            },
            is_json=True,
        )

    @staticmethod
    def recipe_shaped_crafting(identifier: str, assume_symmetry: bool, tags: list[str]):
        return load_file(
            "recipe_shaped_crafting.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
                "assume_symmetry": assume_symmetry,
            },
            is_json=True,
        )

    @staticmethod
    def recipe_brewing_container(identifier: str, tags: list[str]):
        return load_file(
            "recipe_brewing_container.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
            },
            is_json=True,
        )

    @staticmethod
    def recipe_brewing_mix(identifier: str, tags: list[str]):
        return load_file(
            "recipe_brewing_mix.jsont",
            {
                "format_version": RECIPE_JSON_FORMAT_VERSION,
                "identifier": identifier,
                "tags": tags,
            },
            is_json=True,
        )

    @staticmethod
    def crafting_items_catalog():
        return load_file(
            "crafting_items_catalog.jsont",
            {"format_version": CRAFTING_ITEMS_CATALOG},
            is_json=True,
        )

    @staticmethod
    def aim_assist_preset(identifier: str):
        return load_file(
            "aim_assist_preset.jsont", {"identifier": identifier}, is_json=True
        )

    @staticmethod
    def aim_assist_categories():
        return load_file("aim_assist_categories.jsont", is_json=True)

    @staticmethod
    def jigsaw_structure_process(identifier: str):
        return load_file(
            "jigsaw_structure_process.jsont",
            {"format_version": JIGSAW_VERSION, "identifier": identifier},
            is_json=True,
        )

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
        return load_file(
            "jigsaw_structures.jsont",
            {
                "format_version": JIGSAW_VERSION,
                "identifier": identifier,
                "placement_step": placement_step,
                "start_pool_identifier": start_pool_identifier,
                "start_jigsaw_name": (
                    start_jigsaw_name if start_jigsaw_name is not None else {}
                ),
                "max_depth": max_depth,
                "start_height": start_height,
                "liquid_settings": liquid_settings,
            },
            is_json=True,
        )

    @staticmethod
    def jigsaw_template_pools(identifier: str, fallback_identifier: str | None):
        return load_file(
            "jigsaw_template_pools.jsont",
            {
                "format_version": JIGSAW_VERSION,
                "identifier": identifier,
                "fallback_identifier": (
                    fallback_identifier if fallback_identifier else {}
                ),
            },
            is_json=True,
        )

    @staticmethod
    def jigsaw_structure_set(
        identifier: str, separation: int, spacing: int, spread_type, placement_type
    ):
        return load_file(
            "jigsaw_structure_set.jsont",
            {
                "format_version": JIGSAW_VERSION,
                "identifier": identifier,
                "salt": salt_from_str(identifier),
                "separation": separation,
                "spacing": spacing,
                "spread_type": spread_type,
            },
            is_json=True,
        )

    @staticmethod
    def texture_set():
        return load_file(
            "texture_set.jsont",
            {
                "format_version": TEXTURE_SET_VERSION,
            },
            is_json=True,
        )

    @staticmethod
    def python():
        return load_file("python.jsont")

    @staticmethod
    def gitignore():
        return load_file("gitignore.jsont")

    @staticmethod
    def code_workspace(name, path1, path2, preview=False):
        return load_file(
            "code_workspace.jsont",
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
    def vscode(path, wkspc, script_uuid, project_name):
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
    def biome_server():
        return load_file(
            "biome_server.jsont", {"format_version": BIOME_SERVER_VERSION}, is_json=True
        )

    @staticmethod
    def biome_client():
        return load_file(
            "biome_client.jsont", {"format_version": BIOME_CLIENT_VERSION}, is_json=True
        )

    @staticmethod
    def block_culling_rules(identifier: Identifier):
        return load_file(
            "block_culling.jsont",
            {"format_version": BLOCK_CULLING_VERSION, "identifier": identifier},
            is_json=True,
        )


class AddonDescriptor:
    """An object representing an addon descriptor with validation for names and namespaces."""

    _object_type = "addon_descriptor"

    def _validate_name(
        self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = False
    ) -> tuple[str, str]:
        """Validates the name of the Minecraft object.

        Parameters:
            name (str): The name of the Minecraft object.
            is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
            is_vanilla_allowed (bool, optional): If overriding vanilla objects is allowed, used for vanilla definitions. Defaults to False.
        """
        object_name: str
        object_namespace: str

        if ":" in name:
            object_namespace, object_name = name.split(":", 1)
        else:
            object_namespace = "minecraft" if is_vanilla else CONFIG.NAMESPACE
            object_name = name

        if str(object_name)[0].isdigit():
            raise ValueError(
                f"Names cannot start with a digit. {object_name} at {self._object_type}[{name}]"
            )

        if not str(object_namespace)[0].isalpha():
            raise ValueError(
                f"Namespaces cannot start with a digit. {self._object_type}[{name}]"
            )

        if (
            CONFIG._TARGET == ConfigPackageTarget.ADDON
            and is_vanilla
            and not is_vanilla_allowed
        ):
            raise RuntimeError(
                f"Overriding vanilla features is not allowed for packages of type '{CONFIG._TARGET}'. {self._object_type}[{name}]"
            )

        if is_vanilla and object_namespace != "minecraft":
            raise ValueError(
                f"Invalid namespace '{object_namespace}' overriding Vanilla component with a different namespace. {self._object_type}[{name}]"
            )

        return object_name, object_namespace

    def __init__(
        self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = False
    ) -> None:
        """
        Constructs all the necessary attributes for the AddonObject object.

        Parameters:
            name (str): The name of the addon object.
            is_vanilla (bool, optional): If the object is from vanilla Minecraft. Defaults to False.
            is_vanilla_allowed (bool, optional): If overriding vanilla objects is allowed. Defaults to False.
        """

        self._is_vanilla = is_vanilla
        self._name, self._namespace = self._validate_name(
            str(name), is_vanilla, is_vanilla_allowed
        )
        self._data = None
        self._display_name = self._name.replace("_", " ").title()
        self._created_from = traceback.format_stack()[:-1]

    @property
    def identifier(self) -> Identifier:
        """
        Returns the identifier of the addon object in the format 'namespace:name'.

        Returns:
            str: The identifier of the addon object.
        """
        if self._data:
            return f"{self._namespace}:{self._name}:{self._data}"
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

    def set_identifier_data(self, data: str):
        """
        Sets the data of the addon object.

        Parameters:
            data (any): The data to be set for the addon object.
        """
        self._data = data
        return self


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
    _config = CONFIG

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

    def content(self, content) -> AddonObject:
        """
        Sets the content of the addon object and returns the object.

        Parameters:
            content (any): The content to be set for the addon object.

        Returns:
            self: The instance of the current AddonObject.
        """
        self._content = content
        return self

    def queue(self, directory: str | None = None) -> AddonObject:
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
                    if (v != {} and v != [] and v != None)
                    or str(k).startswith("minecraft:")
                    or v == {"do_not_shorten": True}
                }

            elif isinstance(d, list):
                return [v for v in map(_shorten_dict, d) if v != []]

            return d

        def _replace_backslashes(obj):
            if isinstance(obj, str):
                return (
                    obj.replace('"/n"', '"\\n"').replace("/n", "\n").replace("\\", "/")
                )
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

        self._states = {}
        if states:
            for k, v in states.items():
                if v is not None:
                    self._states[str(k)] = str(v)
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
        if self.states or self._tags:
            return {
                "name": self.identifier,
                "states": self.states if self.states else {},
                "tags": self.tags if self.tags else {},
            }
        return self.identifier


class MinecraftItemDescriptor(AddonDescriptor):
    _object_type = "Item Descriptor"

    def __init__(
        self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = True
    ) -> None:
        super().__init__(name, is_vanilla, is_vanilla_allowed)


class MinecraftBiomeDescriptor(AddonDescriptor):
    _object_type = "Biome Descriptor"

    def __init__(
        self, name: str, is_vanilla: bool = False, is_vanilla_allowed: bool = True
    ) -> None:
        super().__init__(name, is_vanilla, is_vanilla_allowed)

    def __str__(self) -> Identifier:
        return self.identifier


class MinecraftEntityDescriptor(MinecraftAddonObject):
    _object_type = "Entity Descriptor"

    def __init__(
        self,
        name,
        is_vanilla=False,
        allow_runtime: bool = True,
        is_vanilla_allowed=True,
    ):
        super().__init__(name, is_vanilla, is_vanilla_allowed)
        self._allow_runtime = allow_runtime


class EntityDescriptor(MinecraftEntityDescriptor):
    def __init__(
        self, name: str, is_vanilla: bool = False, allow_runtime: bool = True
    ) -> None:
        super().__init__(name, is_vanilla, allow_runtime, False)


class BlockDescriptor(MinecraftBlockDescriptor):
    def __init__(
        self,
        name: str,
        is_vanilla: bool = False,
        states: Mapping[str, str | int | float | bool] = None,
        tags: set[str] = None,
    ) -> None:
        super().__init__(name, is_vanilla, states, tags, False)


class ItemDescriptor(MinecraftItemDescriptor):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name, is_vanilla, False)


class BiomeDescriptor(MinecraftBiomeDescriptor):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name, is_vanilla, False)
