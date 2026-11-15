"""The resource pack's `sounds/sound_definitions.json`: the sound files each sound
identifier plays."""

from pathlib import Path, PurePosixPath
from typing import Annotated, Any, ClassVar

from anvil.api.sounds.server_sound_definitions import MusicInfo, ServerSoundDefinition
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import SOUND_DEFINITIONS_VERSION
from anvil.lib.jsonmodel import (
    JsonFile,
    JsonObject,
    Keyed,
    NonNegative,
    Positive,
    json_field,
)
from anvil.lib.jsonmodel.enums import SoundCategory
from anvil.lib.lib import Directory
from anvil.lib.reports import ReportType
from anvil.lib.translator import AnvilTranslator


class _Sound(JsonObject):
    """One sound file of a sound definition. Written as its path alone when nothing else is
    set.

    Args:
        name (str): The path of the file in the resource pack, without extension.
        source (Path): The folder the `.ogg` file is copied from.
    """

    name: str = json_field()
    source: Path = json_field(exclude=True)
    volume: Annotated[float, NonNegative] = json_field(default=1, omit_default=True)
    pitch: Annotated[float, Positive] = json_field(default=1, omit_default=True)
    weight: Annotated[int, NonNegative] = json_field(default=1, omit_default=True)
    is3D: bool | None = None
    stream: bool | None = None

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        return payload["name"] if list(payload) == ["name"] else payload

    @classmethod
    def __schema_body__(cls, definitions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return {"anyOf": [{"type": "string"}, schema]}


class _SoundDescription(JsonObject):
    """A sound definition: a sound name and the files it plays one of. Made by
    `SoundDefinition.sound_reference`; add its files with `add_sound`.

    Args:
        identifier (str): The sound name, `<namespace>:<sound_reference>`.
        category (SoundCategory): The volume slider the sound follows.
    """

    identifier: str = json_field(exclude=True)
    category: SoundCategory = json_field()
    use_legacy_max_distance: bool = json_field(
        default=False, omit_default=True, key="__use_legacy_max_distance"
    )
    max_distance: Annotated[float, NonNegative] | None = None
    min_distance: Annotated[float, NonNegative] | None = None
    subtitle: str | None = None
    sounds: list[_Sound] = json_field(default_factory=list)

    def add_sound(
        self,
        sound_name: str,
        volume: float = 1,
        weight: int = 1,
        pitch: float = 1,
        is_3d: bool | None = None,
        stream: bool | None = None,
    ) -> "_SoundDescription":
        """Adds a sound file, `assets/sounds/<sound_name>.ogg`.

        Args:
            sound_name (str): The path of the file in `assets/sounds`, without extension.
            volume (float, optional): The volume. Defaults to 1.
            weight (int, optional): How likely the file is picked. Defaults to 1.
            pitch (float, optional): The pitch. Defaults to 1.
            is_3d (bool, optional): If the sound fades with distance. Game default true.
            stream (bool, optional): Streams the file instead of loading it. Game default false.

        Raises:
            FileNotFoundError: When the `.ogg` file does not exist.
        """
        *folders, file = PurePosixPath(sound_name).parts
        source = Path("assets", "sounds", *folders)
        if not (source / f"{file}.ogg").exists():
            raise FileNotFoundError(
                f"{file}.ogg not found in {source}. Please ensure the file exists."
            )
        self.sounds.append(
            _Sound(
                name=PurePosixPath(
                    "sounds", CONFIG.NAMESPACE, *folders, file
                ).as_posix(),
                source=source,
                volume=volume,
                pitch=pitch,
                weight=weight,
                is3D=is_3d,
                stream=stream,
            )
        )
        CONFIG.Report.add_report(
            ReportType.SOUND, col0=self.identifier, col1=file, vanilla=False
        )
        return self


class _SoundDefinitionsFile(JsonObject):
    """The content of `sounds/sound_definitions.json`."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "sound_definitions")

    format_version: str = json_field(default=SOUND_DEFINITIONS_VERSION, init=False)
    sound_definitions: Annotated[list[_SoundDescription], Keyed("identifier")] = (
        json_field(default_factory=list)
    )

    def add_sound_definition(self, sound: _SoundDescription) -> None:
        """Adds a sound definition, in place of an earlier one with the same name."""
        self.sound_definitions = [
            x for x in self.sound_definitions if x.identifier != sound.identifier
        ] + [sound]


class SoundDefinition(JsonFile[_SoundDefinitionsFile]):
    """The sound definitions of the resource pack, `sounds/sound_definitions.json`: each
    sound name and the files it plays. There is one per pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/addcustomsounds)
    """

    _instance = None
    _pack = Pack.RP
    _folder = "sounds"
    _object_type = "Sound Definitions"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("sound_definitions")
        self._initialized = True

    def sound_reference(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str | None = None,
        server_sound: "MusicInfo | None" = None,
    ) -> _SoundDescription:
        """Defines a sound. A sound defined again replaces the first definition.

        Args:
            sound_reference (str): The sound name, written as `<namespace>:<sound_reference>`.
            category (SoundCategory): The volume slider the sound follows.
            use_legacy_max_distance (bool, optional): Uses the old distance falloff.
                Defaults to False.
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            subtitle (str, optional): The subtitle text, or a `subtitle.` localization key.
            server_sound (MusicInfo, optional): Also registers the sound in the behavior
                pack's server sound definitions.

        Returns:
            _SoundDescription: The sound definition; add its files with `add_sound`.
        """
        if subtitle is not None and not subtitle.startswith("subtitle."):
            key = f"subtitle.{sound_reference}"
            AnvilTranslator().add_localization_entry(key, subtitle)
            subtitle = key

        sound = _SoundDescription(
            identifier=f"{CONFIG.NAMESPACE}:{sound_reference}",
            category=category,
            use_legacy_max_distance=use_legacy_max_distance,
            max_distance=max_distance,
            min_distance=min_distance,
            subtitle=subtitle,
        )
        self._document.add_sound_definition(sound)

        if server_sound is not None:
            ServerSoundDefinition().server_sound_reference(
                sound.identifier, server_sound
            )
        return sound

    def queue(self) -> "SoundDefinition":
        """Queues the sound definitions for export."""
        return super().queue("")

    def __export__(self) -> None:
        """Copies the sound files and writes the definitions, when there is any."""
        if not self._document.sound_definitions:
            return None
        for definition in self._document.sound_definitions:
            for sound in definition.sounds:
                path = PurePosixPath(sound.name)
                Directory.copy_files(
                    sound.source, CONFIG.RP_PATH / path.parent, f"{path.name}.ogg"
                )
        return super().__export__()
