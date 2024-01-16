import os

from PIL import Image, ImageDraw, ImageFont

from anvil import CONFIG
from anvil.api.enums import CameraPresets, FogCameraLocation, LootPoolType, RawTextConstructor, RenderDistanceType
from anvil.api.types import Identifier
from anvil.lib.lib import CopyFiles, Defaults, File, FileExists, clamp
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

    @property
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
    _path = os.path.join(CONFIG.BP_PATH, "loot_tables", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME)

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
        return os.path.join("loot_tables", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, self._directory, self._name + self._extension)

    def queue(self, directory: str = ""):
        for pool in self._pools:
            self._content["pools"].append(pool._export())
        self.content(self._content)
        self._directory = directory
        return super().queue(directory=directory)


# Recipe --------------------------------------------------
# Legacy code, must improve
class Recipe(AddonObject):
    _extension = ".recipe.json"
    _path = os.path.join(CONFIG.BP_PATH, "recipes")

    class _Crafting:
        class _Shapeless:
            def __init__(
                self,
                parent,
                identifier,
                output_item_id: str,
                data: int = 0,
                count: int = 1,
            ):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 9
                self._ingredients = []
                self._default = Defaults(
                    "recipe_shapeless",
                    self._identifier,
                    output_item_id,
                    data,
                    count,
                    CONFIG.NAMESPACE,
                )

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                item_id = str(item_id)
                if self._item_count == 0:
                    raise RuntimeError(f"The recipe {self._parent._name} has more than 9 items")
                if item_id not in [item["item"] for item in self._ingredients]:
                    self._ingredients.append({"item": item_id, "data": data, "count": count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default["minecraft:recipe_shapeless"]["ingredients"] = self._ingredients
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _Shaped:
            def __init__(self, parent: "Recipe", identifier, output_item_id, data, count, recipe_exactly):
                self._parent = parent
                self._identifier = identifier
                self._recipe_exactly = recipe_exactly
                self._keys = "abcdefghijklmnopqrstuvwxyz"
                self._items = {}
                self._pattern = ["   ", "   ", "   "]
                self._key = {}
                self._default = Defaults(
                    "recipe_shaped",
                    self._identifier,
                    output_item_id,
                    data,
                    count,
                    CONFIG.NAMESPACE,
                )
                self._grid = [[" " for i in range(3)] for j in range(3)]

            def item_0_0(self, item_identifier: str = " ", data: int = 0):
                self._grid[0][0] = {"item": item_identifier, "data": data}
                return self

            def item_0_1(self, item_identifier: str = " ", data: int = 0):
                self._grid[0][1] = {"item": item_identifier, "data": data}
                return self

            def item_0_2(self, item_identifier: str = " ", data: int = 0):
                self._grid[0][2] = {"item": item_identifier, "data": data}
                return self

            def item_1_0(self, item_identifier: str = " ", data: int = 0):
                self._grid[1][0] = {"item": item_identifier, "data": data}
                return self

            def item_1_1(self, item_identifier: str = " ", data: int = 0):
                self._grid[1][1] = {"item": item_identifier, "data": data}
                return self

            def item_1_2(self, item_identifier: str = " ", data: int = 0):
                self._grid[1][2] = {"item": item_identifier, "data": data}
                return self

            def item_2_0(self, item_identifier: str = " ", data: int = 0):
                self._grid[2][0] = {"item": item_identifier, "data": data}
                return self

            def item_2_1(self, item_identifier: str = " ", data: int = 0):
                self._grid[2][1] = {"item": item_identifier, "data": data}
                return self

            def item_2_2(self, item_identifier: str = " ", data: int = 0):
                self._grid[2][2] = {"item": item_identifier, "data": data}
                return self

            def queue(self):
                for i in range(0, 3):  # Row
                    for j in range(0, 3):  # Column
                        current_item = str(self._grid[i][j]["item"]) if type(self._grid[i][j]) is dict else " "
                        current_data = self._grid[i][j]["data"] if type(self._grid[i][j]) is dict else 0
                        current_key = self._keys[0]
                        if current_item != " ":
                            if current_item not in self._items:
                                self._items.update(
                                    {
                                        current_item: {
                                            "key": current_key,
                                            "data": current_data,
                                        }
                                    }
                                )
                                self._pattern[i] = self._pattern[i][:j] + current_key + self._pattern[i][j + 1 : :]
                                self._keys = self._keys[1::]
                                self._key.update(
                                    {
                                        current_key: {
                                            "item": current_item,
                                            "data": current_data,
                                        }
                                    }
                                )
                            elif current_data != self._items[current_item]["data"]:
                                self._items.update(
                                    {
                                        current_item: {
                                            "key": current_key,
                                            "data": current_data,
                                        }
                                    }
                                )
                                self._pattern[i] = self._pattern[i][:j] + current_key + self._pattern[i][j + 1 : :]
                                self._keys = self._keys[1::]
                                self._key.update(
                                    {
                                        current_key: {
                                            "item": current_item,
                                            "data": current_data,
                                        }
                                    }
                                )
                            else:
                                self._pattern[i] = (
                                    self._pattern[i][:j] + self._items[current_item]["key"] + self._pattern[i][j + 1 : :]
                                )
                if not self._recipe_exactly:
                    for i in range(len(self._pattern[0])):
                        if self._pattern[0].endswith(" ") and self._pattern[1].endswith(" ") and self._pattern[2].endswith(" "):
                            for j in range(len(self._pattern)):
                                self._pattern[j] = self._pattern[j].removesuffix(" ")

                        if (
                            self._pattern[0].startswith(" ")
                            and self._pattern[1].startswith(" ")
                            and self._pattern[2].startswith(" ")
                        ):
                            for j in range(len(self._pattern)):
                                self._pattern[j] = self._pattern[j].removeprefix(" ")

                    for i in range(len(self._pattern)):
                        if len(self._pattern) > 0:
                            if self._pattern[-1] == (" " * len(self._pattern[-1])):
                                self._pattern.pop(-1)
                        if len(self._pattern) > 0:
                            if self._pattern[0] == (" " * len(self._pattern[0])):
                                self._pattern.pop(0)

                self._default["minecraft:recipe_shaped"]["pattern"] = self._pattern
                self._default["minecraft:recipe_shaped"]["key"] = self._key
                self._parent.content(self._default)
                self._parent._export()

        class _Stonecutter:
            def __init__(
                self,
                parent,
                identifier,
                output_item_id: str,
                data: int = 0,
                count: int = 1,
            ):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 1
                self._ingredients = []
                self._default = Defaults(
                    "recipe_stonecutter",
                    self._identifier,
                    output_item_id,
                    data,
                    count,
                    CONFIG.NAMESPACE,
                )

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    raise RuntimeError(f"The recipe {self._parent._name} has more than 9 items")
                if item_id not in [item["item"] for item in self._ingredients]:
                    self._ingredients.append({"item": item_id, "data": data, "count": count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default["minecraft:recipe_shapeless"]["ingredients"] = self._ingredients
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _Stonecutter:
            def __init__(
                self,
                parent,
                identifier,
                output_item_id: str,
                data: int = 0,
                count: int = 1,
            ):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 1
                self._ingredients = []
                self._default = Defaults(
                    "recipe_stonecutter",
                    self._identifier,
                    output_item_id,
                    data,
                    count,
                    CONFIG.NAMESPACE,
                )

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    raise RuntimeError(f"The recipe {self._parent._name} can only take 1 item")
                self._ingredients.append({"item": item_id, "data": data, "count": count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default["minecraft:recipe_shapeless"]["ingredients"] = self._ingredients
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        class _SmithingTable:
            def __init__(
                self,
                parent,
                identifier,
                output_item_id: str,
                data: int = 0,
                count: int = 1,
            ):
                self._parent = parent
                self._identifier = identifier
                self._item_count = 1
                self._ingredients = []
                self._default = Defaults(
                    "recipe_smithing_table",
                    self._identifier,
                    output_item_id,
                    data,
                    count,
                    CONFIG.NAMESPACE,
                )

            def add_item(self, item_id: str, data: int = 0, count: int = 1):
                if self._item_count == 0:
                    raise RuntimeError(f"The recipe {self._parent._name} can only take 1 item")
                self._ingredients.append({"item": item_id, "data": data, "count": count})
                self._item_count -= 1
                return self

            def queue(self):
                self._default["minecraft:recipe_shapeless"]["ingredients"].extend(self._ingredients)
                self._parent.content(self._default)
                self._parent.queue()
                self._parent._export()

        def __init__(self, parent: "Recipe", identifier):
            self._parent = parent
            self._identifier = identifier

        def shapeless(self, output_item_id: str, data: int = 0, count: int = 1):
            return self._Shapeless(self._parent, self._identifier, output_item_id, data, count)

        def shaped(
            self,
            output_item_id: str,
            data: int = 0,
            count: int = 1,
            recipe_exactly: bool = False,
        ):
            return self._Shaped(
                self._parent,
                self._identifier,
                output_item_id,
                data,
                count,
                recipe_exactly,
            )

        def stonecutter(self, output_item_id: str, data: int = 0, count: int = 1):
            return self._Stonecutter(self._parent, self._identifier, output_item_id, data, count)

        def smithing_table(self, output_item_id: str, data: int = 0, count: int = 1):
            return self._SmithingTable(self._parent, self._identifier, output_item_id, data, count)

    class _Smelting:
        def __init__(self, parent, identifier):
            self._parent = parent
            self._identifier = identifier
            self._tags = []
            self._output = " "
            self._input = " "

        def output(self, output_item_id: str, data: int = 0, count: int = 1):
            self._output = f"{output_item_id}:{data}"
            return self

        def input(self, input_item_id: str, data: int = 0, count: int = 1):
            self._input = f"{input_item_id}:{data}"
            return self

        @property
        def furnace(self):
            self._tags.append("furnace")
            return self

        @property
        def blast_furnace(self):
            self._tags.append("blast_furnace")
            return self

        @property
        def smoker(self):
            self._tags.append("smoker")
            return self

        @property
        def campfire(self):
            self._tags.append("campfire")
            self._tags.append("soul_campfire")
            return self

        def queue(self):
            if self._output == " ":
                raise RuntimeError("Recipe missing output item")
            if self._input == " ":
                raise RuntimeError("Recipe missing input item")
            self._tags = list(set(self._tags))
            self._default = Defaults(
                "recipe_furnace",
                self._identifier,
                self._output,
                self._input,
                self._tags,
            )
            self._parent.content(self._default)
            self._parent.queue()
            self._parent._export()

    def __init__(self, name: str):
        self._name = name
        self._content = ""
        super().__init__(name)

    def crafting(self, identifier: str):
        return self._Crafting(self, identifier)

    def smelting(self, identifier: str):
        return self._Smelting(self, identifier)

    def queue(self, directory: str = ""):
        return super().queue(directory)


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
        self._content = ""
        self._use_vanilla_texture = use_vanilla_texture

    def queue(self):
        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self._name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self._name}",
        )

        return super().queue("particles")

    def _export(self):
        if self._content != "":
            super()._export()
        if not self._use_vanilla_texture:
            if FileExists(os.path.join("assets", "particles", f"{self._name}.png")):
                CopyFiles(
                    os.path.join("assets", "particles"),
                    os.path.join(CONFIG.RP_PATH, "textures", CONFIG.NAMESPACE, CONFIG.PROJECT_NAME, "particle"),
                    f"{self._name}.png",
                )
            else:
                CONFIG.Logger.file_exist_error(f"{self._name}.png", os.path.join("assets", "particles"))

        if FileExists(os.path.join("assets", "particles", f"{self._name}.particle.json")):
            CopyFiles(
                os.path.join("assets", "particles"),
                os.path.join(CONFIG.RP_PATH, "particles"),
                f"{self._name}.particle.json",
            )
        else:
            CONFIG.Logger.file_exist_error(f"{self._name}.particle.json", os.path.join("assets", "particles"))


# Camera Presets ------------------------------------------
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
        self._camera_preset["minecraft:camera_preset"]["listener"] = value
        return self

    @property
    def queue(self):
        """Queues the camera preset to be exported."""
        self.content(self._camera_preset)
        return super().queue()

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
        CONFIG._queue(self)

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
