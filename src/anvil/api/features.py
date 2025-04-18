import json
import os
from enum import StrEnum

from griffe import Logger
from PIL import Image, ImageDraw, ImageFont

from anvil import ANVIL, CONFIG
from anvil.api.enums import (AimAssistTargetMode, CameraPresets,
                             FogCameraLocation, LootPoolType, PotionId,
                             RawTextConstructor, RenderDistanceType,
                             SmeltingTags)
from anvil.api.types import Identifier
from anvil.lib.lib import CopyFiles, File, FileExists, clamp
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes, MinecraftDescription


# Dialogue ------------------------------------------------
class _DialogueButton:
    """Handles dialogue buttons.

    Attributes:
        button_name (str): The name of the button.
        _commands (list[str], optional): A list of commands for the button. Defaults to empty list.
    """

    def __init__(self, button_name: str, *commands: str):
        """Initializes a _DialogueButton instance.

        Args:
            button_name (str): The name of the button.
            *commands (str): The commands for the button.
        """
        self._button_name = button_name
        self._commands = [f"/{command}" if not str(command).startswith("/") else command for command in commands]

    def _export(self):
        """Returns the dialogue button.

        Returns:
            dict: The dialogue button.
        """
        return JsonSchemes.dialogue_button(self._button_name, self._commands)


class _DialogueScene:
    """Handles dialogue scenes.

    Attributes:
        scene_tag (str): The tag of the scene.
        _buttons (list[_DialogueButton], optional): A list of dialogue buttons. Defaults to empty list.
        _on_open_commands (list[str], optional): A list of commands to be executed when the scene opens. Defaults to empty list.
        _on_close_commands (list[str], optional): A list of commands to be executed when the scene closes. Defaults to empty list.
        _npc_name (str, optional): The name of the NPC for the scene. Defaults to None.
        _text (str, optional): The text for the scene. Defaults to None.
    """

    def __init__(self, scene_tag: str):
        """Initializes a _DialogueScene instance.

        Args:
            scene_tag (str): The tag of the scene.
        """
        self._scene_tag = f"{CONFIG.NAMESPACE}:{scene_tag}"
        self._buttons: list[_DialogueButton] = []
        self._on_open_commands = []
        self._on_close_commands = []
        self._npc_name = None
        self._text = None

    @property
    def identifier(self):
        return self._scene_tag

    def properties(self, npc_name: str, text: str = ""):
        """Sets the properties for the dialogue scene.

        Args:
            npc_name (str): The name of the NPC.
            text (str, optional): The text for the scene. Defaults to ''.

        Returns:
            _DialogueScene: The dialogue scene instance.
        """
        self._npc_name: str = RawTextConstructor().text(npc_name)
        if not text is None:
            self._text: str = RawTextConstructor().translate(text)
        return self

    def button(self, button_name: str, *commands: str):
        """Adds a button to the dialogue scene.

        Args:
            button_name (str): The name of the button.
            *commands (str): The commands for the button.

        Returns:
            _DialogueScene: The dialogue scene instance.
        """
        if len(self._buttons) >= 6:
            CONFIG.Logger.dialogue_max_buttons(self._scene_tag, len(self._buttons))
        # Buttons cannot be translated
        button = _DialogueButton(button_name, *commands)
        self._buttons.append(button)
        return self

    def on_open_commands(self, *commands: str):
        """Sets the commands to be executed when the scene opens.

        Args:
            *commands (str): The commands to be executed.

        Returns:
            _DialogueScene: The dialogue scene instance.
        """
        self._on_open_commands = commands
        return self

    def on_close_commands(self, *commands: str):
        """Sets the commands to be executed when the scene closes.

        Args:
            *commands (str): The commands to be executed.

        Returns:
            _DialogueScene: The dialogue scene instance.
        """
        self._on_close_commands = commands
        return self

    def _export(self):
        """Returns the dialogue scene.

        Returns:
            dict: The dialogue scene.
        """
        return JsonSchemes.dialogue_scene(
            self._scene_tag,
            self._npc_name.__str__(),
            self._text.__str__(),
            ["/" + cmd.__str__() for cmd in self._on_open_commands],
            ["/" + cmd.__str__() for cmd in self._on_close_commands],
            [button._export() for button in self._buttons],
        )


class Dialogue(AddonObject):
    _extension = ".dialogue.json"
    _path = os.path.join(CONFIG.BP_PATH, "dialogue")

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._dialogues = JsonSchemes.dialogues()
        self._scenes = []

    def add_scene(self, scene_tag: str):
        scene = _DialogueScene(scene_tag)
        self._scenes.append(scene)
        return scene

    def queue(self, directory: str = None):
        for scene in self._scenes:
            self._dialogues["minecraft:npc_dialogue"]["scenes"].append(scene._export())
        self.content(self._dialogues)
        return super().queue(directory)


# Fog -----------------------------------------------------
class _FogDistance:
    """
    Class to handle fog distances based on camera location, color, and other parameters. Allows for setting fog color,
    distance, and transition.

    Attributes:
        _camera_location (FogCameraLocation): Specifies the location of the camera.
        _distance (dict): A dictionary containing the fog properties related to the camera location.
    """

    def __init__(self, camera_location: FogCameraLocation = FogCameraLocation.Air) -> None:
        """
        Initialize the _FogDistance instance.

        Args:
            camera_location (FogCameraLocation, optional): Enum specifying the location of the camera. Defaults to FogCameraLocation.Air.
        """
        self._camera_location = camera_location.value
        self._distance = {self._camera_location: {}}

    def color(self, color: str):
        """
        Set the color of the fog.

        Args:
            color (str | hex): The color to set the fog.

        Returns:
            _FogDistance: Returns self for chaining.
        """
        self._distance[self._camera_location]["fog_color"] = color
        return self

    def distance(
        self,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
    ):
        """
        Set the starting and ending distance of the fog along with the render distance type.

        Args:
            fog_start (int): The starting distance of the fog.
            fog_end (int): The ending distance of the fog.
            render_distance_type (RenderDistanceType, optional): The type of render distance. Defaults to RenderDistanceType.Render.

        Raises:
            CONFIG.Logger.fog_start_end: If fog_end is less than or equal to fog_start.

        Returns:
            _FogDistance: Returns self for chaining.
        """
        if fog_start >= fog_end:
            raise CONFIG.Logger.fog_start_end(fog_start, fog_end)

        self._distance[self._camera_location]["fog_start"] = fog_start
        self._distance[self._camera_location]["fog_end"] = fog_end
        self._distance[self._camera_location]["render_distance_type"] = render_distance_type.value
        return self

    def transition_fog(
        self,
        color: str,
        fog_start: int,
        fog_end: int,
        render_distance_type: RenderDistanceType = RenderDistanceType.Render,
    ):
        """
        Set the color, starting and ending distance of the fog for transitioning along with the render distance type.

        Args:
            color (str): The color to set the fog.
            fog_start (int): The starting distance of the fog.
            fog_end (int): The ending distance of the fog.
            render_distance_type (RenderDistanceType, optional): The type of render distance. Defaults to RenderDistanceType.Render.

        Raises:
            CONFIG.Logger.fog_start_end: If fog_end is less than or equal to fog_start.

        Returns:
            _FogDistance: Returns self for chaining.
        """
        if fog_start >= fog_end:
            raise CONFIG.Logger.fog_start_end(fog_start, fog_end)
        self._distance[self._camera_location]["color"] = color
        self._distance[self._camera_location]["fog_start"] = fog_start
        self._distance[self._camera_location]["fog_end"] = fog_end
        self._distance[self._camera_location]["render_distance_type"] = render_distance_type.value
        return self

    def _export(self):
        """
        Return the instance's distance data.

        Returns:
            dict: The distance data of the instance.
        """
        return self._distance


class Fog(AddonObject):
    """A class representing a Fog."""

    _extension = ".fog.json"
    _path = os.path.join(CONFIG.RP_PATH, "fogs")

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Initializes a Fog instance.

        Args:
            name (str): The name of the fog.
            is_vanilla (bool, optional): Whether the fog is a vanilla fog. Defaults to False.
        """
        super().__init__(name)
        self._name = name
        self._description = MinecraftDescription(self._name, is_vanilla)
        self._fog = JsonSchemes.fog()
        self._locations: list[_FogDistance] = []
        self._volumes = []

    def add_distance_location(self, camera_location: FogCameraLocation = FogCameraLocation.Air):
        """Adds a distance location to the fog.

        Args:
            camera_location (FogCameraLocation, optional): The camera location of the fog. Defaults to FogCameraLocation.Air.
        """
        self._locations.append(_FogDistance(camera_location))
        return self._locations[-1]

    def add_volume(self):
        pass

    @property
    def identifier(self):
        return self._description.identifier

    def queue(self):
        """Queues the fog to be exported."""
        for location in self._locations:
            self._fog["minecraft:fog_settings"]["distance"].update(location._export())
        self._fog["minecraft:fog_settings"].update(self._description.to_dict)
        self.content(self._fog)
        return super().queue()

    def __str__(self) -> str:
        return self._description.identifier


# Loot Table ----------------------------------------------
# Legacy code, must improve
class _LootPool:
    class _entry:
        class _Functions:
            def __init__(self) -> None:
                pass

            def SetBookContent(self, author: str, title: str, *pages: str):
                self._func = {
                    "author": author,
                    "title": title,
                    "pages": [str(p) for p in pages],
                    "function": "set_book_contents",
                }
                return self

            def SetName(self, name: str):
                self._func = {"function": "set_name", "name": name}
                return self

            def SetLore(self, *lore: str):
                self._func = {"function": "set_lore", "lore": [lore]}
                return self

            def SpecificEnchants(self, *enchants: tuple[str, int]):
                self._func = {
                    "function": "specific_enchants",
                    "enchants": [{"id": enchant[0], "level": enchant[1]} for enchant in enchants],
                }
                return self

            def SetDamage(self, damage: tuple[float, float]):
                self._func = {
                    "function": "set_damage",
                    "damage": {
                        "min": clamp(damage[0], 0, 1),
                        "max": clamp(damage[1], 0, 1),
                    },
                }
                return self

            def SetCount(self, count: int | tuple[int, int]):
                if type(count) is tuple:
                    self._func = {
                        "function": "set_count",
                        "count": {"min": count[0], "max": count[1]},
                    }
                elif type(count) is int:
                    self._func = {"function": "set_count", "count": count}
                return self

            def SetData(self, data: int | tuple[int, int]):
                if type(data) is tuple:
                    self._func = {
                        "function": "set_data",
                        "data": {"min": data[0], "max": data[1]},
                    }
                elif type(data) is int:
                    self._func = {"function": "set_data", "data": data}
                return self

            def EnchantRandomly(self):
                self._func = {"function": "enchant_randomly"}
                return self

            def SetPotion(self, id: PotionId):
                self._func = {"function": "set_potion", "id": id}
                return self

            def _export(self):
                return self._func

        def __init__(
            self,
            name: str,
            count: int = 1,
            weight: int = 1,
            entry_type: LootPoolType = LootPoolType.Item,
        ) -> None:
            self._entry = {
                "type": entry_type.value,
                "name": name,
                "count": count,
                "weight": weight,
            }
            self._functions = []

        def quality(self, quality: int):
            self._entry.update({"quality": quality})

        @property
        def functions(self):
            function = self._Functions()
            self._functions.append(function)
            return function

        def _export(self):
            for function in self._functions:
                if "functions" not in self._entry:
                    self._entry.update({"functions": []})
                self._entry["functions"].append(function._export())
            return self._entry

    def __init__(
        self,
        rolls: int | list[int, int] = 1,
        loot_type: LootPoolType = LootPoolType.Item,
    ):
        self._pool = {}
        self._entries = []
        if type(rolls) is int:
            self._pool.update({"rolls": rolls})
        elif type(rolls) is tuple:
            self._pool.update({"rolls": {rolls[0], rolls[1]}})
        self._pool.update({"type": loot_type.value})

    def tiers(self, bonus_chance: int = 0, bonus_rolls: int = 0, initial_range: int = 0):
        self._pool.update({"tiers": {}})
        if bonus_chance != 0:
            self._pool["tiers"].update({"bonus_chance": bonus_chance})
        if bonus_rolls != 0:
            self._pool["tiers"].update({"bonus_rolls": bonus_rolls})
        if initial_range != 0:
            self._pool["tiers"].update({"initial_range": initial_range})

    def entry(
        self,
        name: str,
        count: int = 1,
        weight: int = 1,
        entry_type: LootPoolType = LootPoolType.Item,
    ):
        entry = self._entry(str(name), count, weight, entry_type)
        self._entries.append(entry)
        return entry

    def _export(self):
        for entry in self._entries:
            if "entries" not in self._pool:
                self._pool.update({"entries": []})
            self._pool["entries"].append(entry._export())
        return self._pool


class LootTable(AddonObject):
    """A class representing a LootTable."""

    _extension = ".loot_table.json"
    _path = os.path.join(CONFIG.BP_PATH, "loot_tables", CONFIG.NAMESPACE)

    def __init__(self, name: str):
        """Initializes a LootTable instance.

        Args:
            name (str): The name of the LootTable.
        """
        super().__init__(name)
        self._content = JsonSchemes.loot_table()
        self._pools = []

    def pool(
        self,
        rolls: int | list[int, int] = 1,
        loot_type: LootPoolType = LootPoolType.Item,
    ):
        pool = _LootPool(rolls, loot_type)
        self._pools.append(pool)
        return pool

    @property
    def path(self):
        return os.path.join("loot_tables", CONFIG.NAMESPACE, self._directory, self._name + self._extension)

    def queue(self, directory: str = ""):
        for pool in self._pools:
            self._content["pools"].append(pool._export())
        self.content(self._content)
        self._directory = directory
        return super().queue(directory=directory)


# Recipes -------------------------------------------------
class SmeltingRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")

    def __init__(self, name: str, *tags: SmeltingTags):
        self._name = name
        self._tags = tags
        super().__init__(name)
        self.content(JsonSchemes.smelting_recipe(CONFIG.NAMESPACE, name, tags))

    def input(self, identifier: Identifier):
        self._content["minecraft:recipe_furnace"]["input"] = {"item": identifier}
        return self

    def output(self, identifier: Identifier):
        self._content["minecraft:recipe_furnace"]["output"] = identifier
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_furnace"]["priority"] = priority
        return self

    def queue(self):
        return super().queue()


class SmithingRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")

    def __init__(self, name: str):
        self._name = name
        self.content(JsonSchemes.smithing_table_recipe(CONFIG.NAMESPACE, name, ["smithing_table"]))
        super().__init__(name)

    def base(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["base"] = identifier
        return self

    def addition(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["addition"] = identifier
        return self

    def result(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["result"] = identifier
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_smithing_transform"]["priority"] = priority
        return self

    def queue(self):
        return super().queue()


class ShapelessRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")

    def __init__(self, name: str):
        super().__init__(name)
        self.content(JsonSchemes.shapeless_crafting_recipe(CONFIG.NAMESPACE, name, ["crafting_table"]))

    def ingredients(self, items: list[tuple[Identifier, int]]):
        if len(items) > 9:
            CONFIG.Logger.recipe_max_items(self._name)

        for i, item in enumerate(items):
            if not item is None:
                if not isinstance(item, tuple):
                    data = {"item": str(item)}
                else:
                    data = {"item": str(item[0]), "data": item[1]}
                self._content["minecraft:recipe_shapeless"]["ingredients"].append(data)
        return self

    def result(self, identifier: Identifier, count: int = 1, data: int = 0):
        self._content["minecraft:recipe_shapeless"]["result"] = {
            "item": identifier,
            "count": count,
            "data": data if data != 0 else {},
        }
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_shapeless"]["priority"] = priority
        return self

    def queue(self):
        return super().queue()


class StoneCutterRecipe(ShapelessRecipe):
    def __init__(self, name: str):
        super().__init__(name)
        self.content(JsonSchemes.shapeless_crafting_recipe(CONFIG.NAMESPACE, name, ["stonecutter"]))

    def ingredient(self, identifier: Identifier, data: int = 0):
        return super().ingredient([(identifier, data)])

    def queue(self):
        return super().queue()


class ShapedCraftingRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")

    def __init__(self, name: str, assume_symmetry: bool = True):
        self._name = name
        self._recipe_exactly = False
        super().__init__(name)
        self.content(JsonSchemes.shaped_crafting_recipe(CONFIG.NAMESPACE, name, assume_symmetry, ["crafting_table"]))

    def ingredients(self, items: list[list[tuple[str, int]]], keep_empty_slots: bool = False) -> None:
        max_items = 9
        if len(items) > max_items:
            CONFIG.Logger.recipe_max_items(self._name)

        keys = "abcdefghijklmnopqrstuvwxyz"
        pattern = ["   ", "   ", "   "]
        added_items = {}

        for i, row in enumerate(items):
            for j, item in enumerate(row):
                if not item is None:
                    if not isinstance(item, tuple):
                        data = {"item": str(item)}
                    else:
                        data = {"item": str(item[0]), "data": item[1]}

                    key = next((k for k, v in added_items.items() if v == data), None)
                    if key is None:
                        key = keys[len(added_items)]
                        added_items[key] = data

                    pattern[i] = pattern[i][:j] + key + pattern[i][j + 1 :]

        self._content["minecraft:recipe_shaped"]["key"] = added_items

        if not keep_empty_slots:
            while pattern and pattern[0] == "   ":
                pattern.pop(0)
            while pattern and pattern[-1] == "   ":
                pattern.pop(-1)

            while all(row[0] == " " for row in pattern):
                pattern = [row[1:] for row in pattern]
            while all(row[-1] == " " for row in pattern):
                pattern = [row[:-1] for row in pattern]

        self._content["minecraft:recipe_shaped"]["pattern"] = pattern
        return self

    def result(self, identifier: Identifier, count: int = 1, data: int = 0):
        self._content["minecraft:recipe_shaped"]["result"] = {
            "item": str(identifier),
            "count": count,
            "data": data if data != 0 else {},
        }
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_shaped"]["priority"] = priority
        return self

    def queue(self):
        return super().queue()


class SmithingTrimRecipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")

    def __init__(self, name: str):
        self._name = name
        self.content(JsonSchemes.smithing_table_trim_recipe(CONFIG.NAMESPACE, name, ["smithing_table"]))
        super().__init__(name)

    def base(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["base"] = identifier
        return self

    def addition(self, identifier: Identifier):
        self._content["minecraft:recipe_smithing_transform"]["addition"] = identifier
        return self

    def priority(self, priority: int):
        self._content["minecraft:recipe_smithing_transform"]["priority"] = priority
        return self

    def queue(self):
        return super().queue()


# Function ------------------------------------------------
class Function(AddonObject):
    _extension = ".mcfunction"
    _path = os.path.join(CONFIG.BP_PATH, "functions", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME)

    _ticking: list["Function"] = set()
    _setup: list["Function"] = set()
    _function_limit: int = 10000

    def __init__(self, name: str) -> None:
        """Inintializes the Function class.
        The function is limited to 10000 commands. If you exceed this limit, the function will be split into multiple functions.

        Args:
            name (str): The name of the function.
        """
        super().__init__(name)
        self._function: list[str] = []
        self._sub_functions: list[Function] = [self]

    def add(self, *commands: str):
        """Adds a command to the function."""
        if len(self._sub_functions[-1]._function) >= self._function_limit - len(commands) - 1:
            self._sub_functions.append(Function(f"{self._name}_{len(self._sub_functions)}"))
        self._sub_functions[-1]._function.extend([str(func) for func in commands])
        return self

    @property
    def path(self):
        """Gets the path of the function. To use this properly, the function must be queued."""
        return os.path.join(self._directory, self._name)

    @property
    def execute(self):
        """Returns the execute command of the function."""
        return f"function {self.path}"

    @property
    def tick(self):
        """Adds the function to the tick.json file."""
        Function._ticking.add(self)
        return self

    @property
    def add_to_setup(self):
        """Adds the function to the setup function. Meaning this will run when your execute your setup function."""
        Function._setup.add(self)
        return self

    def queue(self, directory: str = None):
        """Queues the function to be exported.

        Args:
            directory (str, optional): The directory to queue the function to. Defaults to None."""

        self._directory = directory
        return super().queue(self._directory)

    def __len__(self):
        """Returns the number of commands in the function."""
        return len(self._function)

    def _export(self):
        """Exports the function to the file system."""
        for function in self._sub_functions[1:]:
            function.content("\n".join(function._function)).queue(self._directory)
        self.content("\n".join(self._function))
        if len(self._function) > 0:
            return super()._export()


class _Tick(AddonObject):
    """Handles tick functions for the addon.

    Attributes:
        _functions (list): Stores all the tick functions.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "functions")

    def __init__(self) -> None:
        """Initializes a _Tick instance."""
        super().__init__("tick")
        self._functions = []
        self.do_not_shorten

    def add_function(self, *functions: "Function"):
        """Adds the provided functions to the tick function list.

        Args:
            functions (Function): Functions to add to the list.
        """
        self._functions.extend([f.path for f in functions])
        return self

    @property
    def queue(self):
        """Generates the content and queues the functions.

        Returns:
            object: The parent's queue method result.
        """
        self.content({"values": self._functions})
        return super().queue()


# Particle ------------------------------------------------
class Particle(AddonObject):
    _extension = ".particle.json"
    _path = os.path.join(CONFIG.BP_PATH, "particles")

    def __init__(self, particle_name, use_vanilla_texture: bool = False):
        super().__init__(particle_name)
        self._name = particle_name
        self._use_vanilla_texture = use_vanilla_texture

        if not FileExists(os.path.join("assets", "particles", f"{self._name}.particle.json")):
            CONFIG.Logger.file_exist_error(f"{self._name}.particle.json", os.path.join("assets", "particles"))

        with open(os.path.join("assets", "particles", f"{self._name}.particle.json"), "r") as file:
            self._content = json.loads(file.read())
            if self._content["particle_effect"]["description"]["identifier"] != f"{CONFIG.NAMESPACE}:{self._name}":
                CONFIG.Logger.namespace_not_valid(self._content["particle_effect"]["description"]["identifier"])

    def queue(self):
        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self._name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self._name}",
        )

        return super().queue("particles")

    def _export(self):
        if not self._use_vanilla_texture:
            texture_path = self._content["particle_effect"]["description"]["basic_render_parameters"]["texture"]
            texture_name = texture_path.split("/")[-1]
            self._content["particle_effect"]["description"]["basic_render_parameters"]["texture"] = os.path.join(
                CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "particle", texture_name
            )

            if not FileExists(os.path.join("assets", "particles", f"{texture_name}.png")):
                CONFIG.Logger.file_exist_error(f"{texture_name}.png", os.path.join("assets", "particles"))

            CopyFiles(
                os.path.join("assets", "particles"),
                os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "particle"),
                f"{texture_name}.png",
            )

        CopyFiles(
            os.path.join("assets", "particles"),
            os.path.join(CONFIG.RP_PATH, "particles"),
            f"{self._name}.particle.json",
        )


# Camera Presets ------------------------------------------


class AimAssistPreset(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "Camera", "Presets")

    def __init__(self, identifier: str):
        super().__init__(identifier)
        self.content(JsonSchemes.aim_assist_preset(identifier))

    @property
    def identifier(self):
        return self._content["minecraft:aim_assist_preset"]["identifier"]

    def item_settings(self, settings: dict):
        self._preset["minecraft:aim_assist_preset"]["item_settings"] = settings
        return self

    def default_item_settings(self, setting: str):
        self._preset["minecraft:aim_assist_preset"]["default_item_settings"] = setting
        return self

    def hand_settings(self, setting: str):
        self._preset["minecraft:aim_assist_preset"]["hand_settings"] = setting
        return self

    def exclusion_list(self, exclusions: dict):
        self._preset["minecraft:aim_assist_preset"]["exclusion_list"] = exclusions
        return self

    def liquid_targeting_list(self, targets: dict):
        self._preset["minecraft:aim_assist_preset"]["liquid_targeting_list"] = targets
        return self

    def _export(self):
        return self._preset

    def queue(self, directory: str = None):
        self.content(self._preset)
        return super().queue(directory)


class AimAssistCategory:
    def __init__(self, name: str):
        self._category = {"name": name, "priorities": {}}

    def entity_default(self, value: int):
        self._category["entity_default"] = value
        return self

    def block_default(self, value: int):
        self._category["block_default"] = value
        return self

    def block_priority(self, block: str, priority: int):
        if "blocks" not in self._category["priorities"]:
            self._category["priorities"]["blocks"] = {}
        self._category["priorities"]["blocks"][block] = priority
        return self

    def entity_priority(self, entity: str, priority: int):
        if "entities" not in self._category["priorities"]:
            self._category["priorities"]["entities"] = {}
        self._category["priorities"]["entities"][entity] = priority
        return self

    def export(self):
        return self._category


class AimAssistCategories(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "Camera", "Presets")

    def __init__(self):
        super().__init__("categories")
        self.content(JsonSchemes.aim_assist_categories())
        self._categories: list[AimAssistCategory] = []

    def add_category(self, category_name: str):
        category = AimAssistCategory(category_name)
        self._categories.append(category)
        return category

    def _export(self):
        for category in self._categories:
            self._content["minecraft:aim_assist_categories"]["categories"].append(category.export())
        return self._content

    def queue(self):
        return super().queue()


class CameraPreset(AddonObject):
    """A class representing a CameraPreset."""

    _extension = ".camera.json"
    _path = os.path.join(CONFIG.BP_PATH, "cameras", "presets")

    def __init__(self, name: str, inherit_from: CameraPresets) -> None:
        """Initializes a CameraPreset instance.

        Args:
            name (str): The name of the camera preset.
            is_vanilla (bool, optional): Whether the camera preset is a vanilla camera preset. Defaults to False.
        """
        super().__init__(name)
        self._name = name
        self._inherit = inherit_from.value if isinstance(inherit_from, CameraPresets) else str(inherit_from)
        self._camera_preset = JsonSchemes.camera_preset(CONFIG.NAMESPACE, name, self._inherit)
        self._replace_reticle = False

    def position(self, x: float = 0, y: float = 0, z: float = 0):
        """Sets the position of the camera preset.

        Args:
            x (float): The x position of the camera preset.
            y (float): The y position of the camera preset.
            z (float): The z position of the camera preset.
        """
        if x != 0:
            self._camera_preset["minecraft:camera_preset"]["pos_x"] = x
        if y != 0:
            self._camera_preset["minecraft:camera_preset"]["pos_y"] = y
        if z != 0:
            self._camera_preset["minecraft:camera_preset"]["pos_z"] = z
        return self

    def rotation(self, x: float = 0, y: float = 0):
        """Sets the rotation of the camera preset.

        Args:
            x (float): The x rotation of the camera preset.
            y (float): The y rotation of the camera preset.
        """
        if x != 0:
            self._camera_preset["minecraft:camera_preset"]["rot_x"] = x
        if y != 0:
            self._camera_preset["minecraft:camera_preset"]["rot_y"] = y
        return self

    def player_effects(self, value: bool):
        """Sets whether the player effects are enabled.

        Args:
            value (bool): Whether the player effects are enabled.
        """
        self._camera_preset["minecraft:camera_preset"]["player_effects"] = value
        return self

    def listener(self, value: bool):
        """Sets whether the listener is enabled.

        Args:
            value (bool): Whether the listener is enabled.
        """
        if value:
            self._camera_preset["minecraft:camera_preset"]["listener"] = "player"
        return self

    def extend_player_rendering(self, value: bool = True):
        """Sets whether the player rendering is extended.

        Args:
            value (bool): Whether the player rendering is extended.
        """
        if self._inherit == CameraPresets.Free:
            if value == False:
                self._camera_preset["minecraft:camera_preset"]["extend_player_rendering"] = False
        else:
            CONFIG.Logger.extend_player_rendering_not_free(self._name)
        return self

    def view_offset(self, x_offset: float, y_offset: float):
        self._camera_preset["minecraft:camera_preset"]["view_offset"] = [x_offset, y_offset]
        return self

    def entity_offset(self, x_offset: float, y_offset: float, z_offset: float):
        self._camera_preset["minecraft:camera_preset"]["entity_offset"] = [x_offset, y_offset, z_offset]
        return self

    def radius(self, radius: float):
        self._camera_preset["minecraft:camera_preset"]["radius"] = clamp(radius, 0.1, 100)
        return self

    def aim_assist(
        self,
        preset: AimAssistPreset,
        target_mode: AimAssistTargetMode = AimAssistTargetMode.Distance,
        angle: list[float] = [30, 30],
        distance: float = 8,
        replace_reticle: bool = False,
    ):
        self._camera_preset["minecraft:camera_preset"]["aim_assist"] = {
            "preset": preset.identifier,
            "target_mode": target_mode.value,
            "angle": [min(angle), max(angle)],
            "distance": clamp(distance, 1, 16),
        }

        if replace_reticle:
            self._replace_reticle = True
        return self

    def focus_target(
        self,
        rotation_speed: float = 0.0,
        snap_to_target: bool = False,
        horizontal_rotation_limit: list[float] = [0, 360],
        vertical_rotation_limit: list[float] = [0, 180],
        continue_targeting: bool = False,
        tracking_radius: float = 50.0,
    ):
        self._camera_preset["minecraft:camera_preset"]["rotation_speed"] = max(0.0, rotation_speed)
        self._camera_preset["minecraft:camera_preset"]["snap_to_target"] = snap_to_target

        self._camera_preset["minecraft:camera_preset"]["horizontal_rotation_limit"] = [
            max(horizontal_rotation_limit[0], 0),
            min(horizontal_rotation_limit[1], 360),
        ]
        self._camera_preset["minecraft:camera_preset"]["vertical_rotation_limit"] = [
            max(vertical_rotation_limit[0], 0),
            min(vertical_rotation_limit[1], 180),
        ]
        self._camera_preset["minecraft:camera_preset"]["continue_targeting"] = continue_targeting
        self._camera_preset["minecraft:camera_preset"]["tracking_radius"] = tracking_radius
        return self

    def queue(self):
        """Queues the camera preset to be exported."""
        self.content(self._camera_preset)
        return super().queue()

    def _export(self):
        if self._replace_reticle:
            if FileExists(os.path.join("assets", "textures", "ui", "aimassist_block_highlight.png")):
                CopyFiles(
                    os.path.join("assets", "textures", "ui"),
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "aimassist_block_highlight.png",
                )
            if FileExists(os.path.join("assets", "textures", "ui", "aimassist_entity_highlight.png")):
                CopyFiles(
                    os.path.join("assets", "textures", "ui"),
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "aimassist_entity_highlight.png",
                )

        return super()._export()

    def __str__(self) -> str:
        return f"{CONFIG.NAMESPACE}:{self._name}"


# Structure -----------------------------------------------
class Structure:
    """A class representing a Structure."""

    def __init__(self, structure_name: str):
        """Initializes a Structure instance.

        Args:
            structure_name (str): The name of the structure.
        """
        self._structure_name = structure_name
        if not FileExists(os.path.join("assets", "structures", f"{self._structure_name}.mcstructure")):
            CONFIG.Logger.file_exist_error(f"{self._structure_name}.mcstructure", os.path.join("assets", "structures"))

    @property
    def queue(self):
        """Queues the structure to be exported."""
        ANVIL._queue(self)

    @property
    def identifier(self) -> Identifier:
        """Returns the identifier of the structure."""
        return f"{CONFIG.NAMESPACE}:{self._structure_name}"

    def _export(self):
        """Exports the structure to the file system."""
        CopyFiles(
            os.path.join("assets", "structures"),
            os.path.join(
                CONFIG.BP_PATH,
                "structures",
                CONFIG.NAMESPACE,
            ),
            f"{self._structure_name}.mcstructure",
        )


# Font ----------------------------------------------------
class Fonts:
    """A class representing a Fonts."""

    def __init__(self, font_name: str, character_size: int = 32) -> None:
        """Initializes a Fonts instance.

        Args:
            font_name (str): The name of the font.
            character_size (int, optional): The size of the character. Defaults to 32.
        """
        if character_size % 16 != 0:
            CONFIG.Logger.unsupported_font_size()
        font_size = round(character_size * 0.8)

        try:
            self.font = ImageFont.truetype(f"assets/textures/ui/{font_name}.ttf", font_size)
        except FileNotFoundError:
            self.font = ImageFont.truetype(f"assets/textures/ui/{font_name}.otf", font_size)
        except:
            self.font = ImageFont.truetype(f"{font_name}.ttf", font_size)

        self.character_size = character_size
        self._path = os.path.join(CONFIG.RP_PATH, "font")

    def generate_font(self):
        """Generates a default8 font image"""

        font_size = round(self.character_size * 0.8)
        image_size = self.character_size * 16

        image = Image.new("RGBA", (image_size, image_size))
        backup_font = ImageFont.truetype("arial.ttf", font_size)

        ascii = "ÀÁÂÈÉÊÍÓÔÕÚßãõǧÎ¹ŒœŞşŴŵŽê§©      !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~⌂"
        extended_ascii = "ÇüéâäàåçêëèïîìÄÅÉ§ÆôöòûùÿÖÜ¢£¥₧ƒáíóúñÑªº¿⌐¬½¼¡«»░▒▓│┤╡╢╖╕╣║╗╝╜╛┐└┴├├─┼╞╟╚╔╩╦╠═╬╧╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀αßΓπΣσµτΦΘΩδ∞φε∩≡±≥≤⌠⌡÷≈°∙·√ⁿ²■	"
        default8 = ascii + extended_ascii

        offset = [0, 0]

        img_draw = ImageDraw.Draw(image)
        for i in default8:
            font_target = self.font if i in ascii else backup_font

            bbox = font_target.getbbox(i)

            char_height = bbox[3] - bbox[1]

            x = offset[0] * self.character_size - bbox[0]
            y = offset[1] * self.character_size

            img_draw.text((x, y), i, fill=(255, 255, 255), font=font_target)

            offset[0] += 1
            if offset[0] >= 16:
                offset[0] = 0
                offset[1] += 1

            image.save(os.path.join("assets", "textures", "ui", "default8.png"))

        return self

    def generate_numbers_particle(self):
        """Generates a numbers particle from 0 to 999."""
        img_path = os.path.join("assets", "particles", "numbers.png")
        particle_path = os.path.join("assets", "particles", "numbers.particle.json")

        max_size = int(self.font.getlength("999"))
        image_size = (max_size * 10, self.character_size * 100)

        if not FileExists(img_path):
            image = Image.new("RGBA", image_size)
            offset = [0, 0]

            img_draw = ImageDraw.Draw(image)
            for i in range(0, 1000):
                bbox = self.font.getbbox(str(i))

                x = offset[0] * max_size
                y = offset[1] * self.character_size

                img_draw.text((x, y), str(i), fill=(255, 255, 255), font=self.font)

                offset[0] += 1
                if offset[0] >= 10:
                    offset[0] = 0
                    offset[1] += 1

                image.save(img_path)

        # if not FileExists(particle_path):
        #    File(
        #        "numbers.particle.json",
        #        {
        #            "format_version": "1.10.0",
        #            "particle_effect": {
        #                "description": {
        #                    "identifier": f"{CONFIG.NAMESPACE}:numbers",
        #                    "basic_render_parameters": {"material": "particles_alpha", "texture": "textures/particle/numbers"},
        #                },
        #                "components": {
        #                    "minecraft:emitter_local_space": {"position": True, "rotation": True, "velocity": True},
        #                    "minecraft:emitter_rate_steady": {"spawn_rate": 10, "max_particles": 1},
        #                    "minecraft:emitter_lifetime_looping": {"active_time": 1},
        #                    "minecraft:particle_lifetime_expression": {"max_lifetime": 0.75},
        #                    "minecraft:emitter_shape_point": {"offset": [0, 0, 0]},
        #                    "minecraft:particle_initial_speed": 0,
        #                    "minecraft:particle_motion_dynamic": {"linear_drag_coefficient": 1},
        #                    "minecraft:particle_appearance_billboard": {
        #                        "size": [0.18, 0.1],
        #                        "facing_camera_mode": "rotate_xyz",
        #                        "direction": {"mode": "custom", "custom_direction": [0, 0, -1]},
        #                        "uv": {
        #                            "texture_width": image_size[0],
        #                            "texture_height": image_size[1],
        #                            "uv": ["v.number_x_uv", "v.number_y_uv"],
        #                            "uv_size": [image_size[0] // 10, image_size[1] // 100],
        #                        },
        #                    },
        #                },
        #            },
        #        },
        #        os.path.join("assets", "particles"),
        #        "w",
        #    )

        return self

    @property
    def queue(self):
        """Queues the font to be exported."""
        for file in ["glyph_E1.png", "default8.png"]:
            if FileExists(os.path.join("assets", "textures", "ui", file)):
                CopyFiles(os.path.join("assets", "textures", "ui"), self._path, file)


# Skin Packs
class SkinPack(AddonObject):
    _extension = ".json"
    _path = os.path.join("assets", "skins")

    def __init__(self) -> None:
        """Initializes a SkinPack instance."""
        super().__init__("skins")
        self._languages = []
        self._skins = []
        self.content(JsonSchemes.skins_json(CONFIG.PROJECT_NAME))

    def add_skin(
        self,
        filename: str,
        display_name: str,
        is_slim: bool = False,
        free: bool = False,
    ):
        """Adds a skin to the SkinPack.

        Args:
            filename (str): The filename of the skin.
            display_name (str): The display name of the skin.
            is_slim (bool, optional): Whether the skin is slim. Defaults to False.
            free (bool, optional): Whether the skin is free. Defaults to False.
        """
        if not FileExists(os.path.join(self._path, f"{filename}.png")):
            CONFIG.Logger.file_exist_error(f"{filename}.png", self._path)
        self._skins.append(JsonSchemes.skin_json(filename, is_slim, free))
        self._languages[f"skin.{CONFIG.PROJECT_NAME}.{filename}"] = display_name

    def _export(self):
        """Exports the SkinPack to the file system."""
        self._content["skins"] = self._skins
        l = JsonSchemes.skin_pack_name_lang(CONFIG.PROJECT_NAME, CONFIG.PROJECT_NAME + " Skin Pack")
        l.extend([f"{k}={v}" for k, v in self._languages.items()])

        File("languages.json", JsonSchemes.languages(), self._path, "w")
        File("manifest.json", JsonSchemes.manifest_skins(CONFIG._RELEASE), self._path, "w")
        File("en_US.lang", "\n".join(l), os.path.join(self._path, "texts"), "w")

        super()._export()
