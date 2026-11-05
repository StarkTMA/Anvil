from typing import Annotated, ClassVar

from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import DIALOGUE_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, Length, json_field
from anvil.lib.translator import AnvilTranslator

__all__ = ["Dialogue"]


class _DialogueTranslation(JsonObject):
    """A `rawtext` entry that shows a localized string."""

    translate: str = json_field()


class _DialogueText(JsonObject):
    """A `rawtext` message, used for names and text so they are localized."""

    rawtext: list[_DialogueTranslation] = json_field(default_factory=list)

    @classmethod
    def localized(cls, kind: str, text: str) -> "_DialogueText":
        """Adds `text` to the language file and returns a message that shows it.

        Args:
            kind (str): What the text is, part of its localization key (`npc_name`, `text`
                or `button`).
            text (str): The text, in the default language.
        """
        translator = AnvilTranslator()
        key = translator.localize(
            text, f"dialogue.{CONFIG.NAMESPACE}:{CONFIG.PROJECT_NAME}.{kind}"
        )

        return cls(rawtext=[_DialogueTranslation(translate=key)])


class _DialogueButton(JsonObject):
    """A button of a dialogue scene and the commands it runs."""

    __required__: ClassVar[tuple[str, ...]] = ("name", "commands")

    name: _DialogueText = json_field()
    commands: list[str] = json_field(default_factory=list)


class _DialogueScene(JsonObject):
    """A dialogue scene, opened in game with `/dialogue open` and its scene tag."""

    __required__: ClassVar[tuple[str, ...]] = ("scene_tag",)

    scene_tag: str = json_field()
    npc_name: _DialogueText | None = None
    text: _DialogueText | None = None
    on_open_commands: list[str] = json_field(default_factory=list)
    on_close_commands: list[str] = json_field(default_factory=list)
    buttons: Annotated[list[_DialogueButton], Length(maximum=6)] = json_field(
        default_factory=list
    )

    @property
    def identifier(self) -> str:
        """The scene tag, as `/dialogue open` takes it."""
        return self.scene_tag

    def properties(self, npc_name: str, text: str) -> "_DialogueScene":
        """Sets the NPC name and the text of the scene. Both are localized.

        Args:
            npc_name (str): The name of the NPC.
            text (str): The text of the scene.

        Returns:
            _DialogueScene: Self, to chain more settings.
        """
        self.npc_name = _DialogueText.localized("npc_name", npc_name)
        self.text = _DialogueText.localized("text", text)
        return self

    def button(self, button_name: str, commands: list[str]) -> "_DialogueScene":
        """Adds a button. A scene has at most 6.

        Args:
            button_name (str): The button text. It is localized.
            commands (list[str]): The commands the button runs. A leading `/` is added
                when missing.

        Returns:
            _DialogueScene: Self, to chain more settings.
        """
        self.buttons.append(
            _DialogueButton(
                name=_DialogueText.localized("button", button_name),
                commands=[
                    command if str(command).startswith("/") else f"/{command}"
                    for command in commands
                ],
            )
        )
        return self

    def set_on_open_commands(self, commands: list[str]) -> "_DialogueScene":
        """Sets the commands that run when the scene opens.

        Args:
            commands (list[str]): The commands.

        Returns:
            _DialogueScene: Self, to chain more settings.
        """
        self.on_open_commands = list(commands)
        return self

    def set_on_close_commands(self, commands: list[str]) -> "_DialogueScene":
        """Sets the commands that run when the scene closes.

        Args:
            commands (list[str]): The commands.

        Returns:
            _DialogueScene: Self, to chain more settings.
        """
        self.on_close_commands = list(commands)
        return self


class _NpcDialogue(JsonObject):
    """The `minecraft:npc_dialogue` object."""

    scenes: list[_DialogueScene] = json_field(default_factory=list)

    def add_scene(self, scene_tag: str) -> _DialogueScene:
        """Adds a scene and returns it."""
        scene = _DialogueScene(scene_tag=scene_tag)
        self.scenes.append(scene)
        return scene


class _DialogueFile(JsonObject):
    """The content of `dialogue/<name>.dialogue.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:npc_dialogue",
    )

    format_version: str = json_field(default=DIALOGUE_VERSION, init=False)
    npc_dialogue: _NpcDialogue = json_field(
        key="minecraft:npc_dialogue", default_factory=_NpcDialogue
    )


class Dialogue(JsonFile[_DialogueFile]):
    """NPC dialogue scenes: text, an NPC name, buttons and the commands they run. A scene
    opens in game with `/dialogue open <npc> <player> <scene tag>`.

    ```python
    dialogue = Dialogue("intro")
    scene = dialogue.add_scene("intro")
    scene.properties("Ducky", "Hello new friend")
    scene.button("Bye", ["say Goodbye"])
    dialogue.queue()
    ```

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/npcdialogue)
    """

    _extension = ".dialogue.json"
    _pack = Pack.BP
    _folder = "dialogue"
    _object_type = "Dialogue"

    def __init__(self, name: str) -> None:
        """Initializes a dialogue file.

        Args:
            name (str): The file name.
        """
        super().__init__(name)

    def add_scene(self, scene: str) -> _DialogueScene:
        """Adds a scene. Its tag is `<namespace>:<scene>`.

        Args:
            scene (str): The scene name.

        Returns:
            _DialogueScene: The scene, to set its text, buttons and commands.
        """
        return self._document.npc_dialogue.add_scene(f"{CONFIG.NAMESPACE}:{scene}")

    def queue(self) -> "Dialogue":
        """Queues the dialogue file for export."""
        return super().queue()
