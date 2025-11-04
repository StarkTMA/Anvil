import os

from anvil.lib.config import CONFIG
from anvil.lib.enums import RawTextConstructor
from anvil.lib.schemas import AddonObject, JsonSchemes


class _DialogueButton:
    """Handles dialogue buttons.

    Attributes:
        button_name (str): The name of the button.
        _commands (list[str], optional): A list of commands for the button. Defaults to empty list.
    """

    def __init__(self, button_name: str, *commands: str):
        """Initializes a _DialogueButton instance.

        Parameters:
            button_name (str): The name of the button.
            *commands (str): The commands for the button.
        """
        self._button_name = button_name
        self._commands = [
            f"/{command}" if not str(command).startswith("/") else command
            for command in commands
        ]

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

        Parameters:
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

        Parameters:
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

        Parameters:
            button_name (str): The name of the button.
            *commands (str): The commands for the button.

        Returns:
            _DialogueScene: The dialogue scene instance.
        """
        if len(self._buttons) >= 6:
            raise RuntimeError(
                f"The Dialogue scene {self._scene_tag} has {len(self._buttons)} buttons, The maximum allowed is 6."
            )
        # Buttons cannot be translated
        button = _DialogueButton(button_name, *commands)
        self._buttons.append(button)
        return self

    def on_open_commands(self, *commands: str):
        """Sets the commands to be executed when the scene opens.

        Parameters:
            *commands (str): The commands to be executed.

        Returns:
            _DialogueScene: The dialogue scene instance.
        """
        self._on_open_commands = commands
        return self

    def on_close_commands(self, *commands: str):
        """Sets the commands to be executed when the scene closes.

        Parameters:
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
    _object_type = "Dialogue"

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
