"""The behavior pack's server sound definitions: music information and duration of
sounds, for the server."""

from dataclasses import dataclass
from typing import Annotated, Any, ClassVar

from anvil.api.core.enums import DurationInfoMode
from anvil.api.core.types import JsonSchema
from anvil.lib.config import Pack
from anvil.lib.format_versions import SERVER_SOUND_DEFINITIONS_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, NonNegative, json_field


@dataclass(kw_only=True)
class MusicInfo:
    """The server-side information of a sound, registered with `server_sound=` on the
    sound methods. Experimental, from Minecraft 26.40.

    Args:
        genres (list[str], optional): The music genres.
        moods (list[str], optional): The music moods.
        artist (str, optional): The artist.
        title (str, optional): The title.
        duration (float, optional): The length of the sound, in seconds.
        duration_tracking (DurationInfoMode, optional): How the duration is tracked.
            Defaults to game time.
        tags (list[str], optional): Tags of the sound.
    """

    genres: list[str] | None = None
    moods: list[str] | None = None
    artist: str | None = None
    title: str | None = None
    duration: float | None = None
    duration_tracking: DurationInfoMode = DurationInfoMode.GameTime
    tags: list[str] | None = None


class _ServerMusicInfo(JsonObject):
    """The `music_info` of a server sound. Unset keys are left out."""

    genres: list[str] = json_field(default_factory=list, omit_default=True)
    moods: list[str] = json_field(default_factory=list, omit_default=True)
    artist: str | None = None
    title: str | None = None


class _ServerDurationInfo(JsonObject):
    """The `duration_info` of a server sound."""

    tracking: DurationInfoMode = json_field()
    duration: Annotated[float, NonNegative] = json_field()


class _ServerSound(JsonObject):
    """One server sound, written as `{identifier: {...}}`.

    Args:
        identifier (str): The sound name, as in the resource pack's sound definitions.
    """

    identifier: str = json_field(exclude=True)
    music_info: _ServerMusicInfo | None = None
    duration_info: _ServerDurationInfo | None = None
    tags: list[str] = json_field(default_factory=list, omit_default=True)

    @classmethod
    def from_music_info(cls, identifier: str, info: MusicInfo) -> "_ServerSound":
        """The server sound of a `MusicInfo`."""
        music = _ServerMusicInfo(
            genres=list(info.genres or []),
            moods=list(info.moods or []),
            artist=info.artist,
            title=info.title,
        )
        return cls(
            identifier=identifier,
            music_info=music if music.__json__() else None,
            duration_info=(
                None
                if info.duration is None
                else _ServerDurationInfo(
                    tracking=info.duration_tracking, duration=info.duration
                )
            ),
            tags=list(info.tags or []),
        )

    def __json__(self) -> Any:
        return {self.identifier: JsonObject.__json__(self)}

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        body = JsonObject.__schema_body__.__func__(cls, definitions)
        return {
            "type": "object",
            "minProperties": 1,
            "maxProperties": 1,
            "additionalProperties": body,
        }


class _ServerSoundDefinitionsFile(JsonObject):
    """The content of the behavior pack's `sounds/sound_definitions.json`."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:server_sound_definitions",
    )

    format_version: str = json_field(
        default=SERVER_SOUND_DEFINITIONS_VERSION, init=False
    )
    definitions: list[_ServerSound] = json_field(
        key="minecraft:server_sound_definitions", default_factory=list
    )

    def add_definition(self, sound: _ServerSound) -> None:
        """Adds a server sound."""
        self.definitions.append(sound)


class ServerSoundDefinition(JsonFile):
    """The behavior pack's server sound definitions (experimental, from Minecraft 26.40):
    duration, music information and tags of sounds the resource pack defines.

    Server sounds are registered through `server_sound=` on `SoundDefinition.sound_reference`
    and the methods that call it (`MusicDefinition.music_definition`, the
    `SoundEvent.add_*_event` methods), so a server sound always has its client sound.
    """

    _document = _ServerSoundDefinitionsFile
    _instance = None
    _pack = Pack.BP
    _folder = "sounds"
    _object_type = "Server Sound Definitions"

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

    def server_sound_reference(
        self, sound_identifier: str, music_info: MusicInfo
    ) -> "ServerSoundDefinition":
        """Registers the server information of a sound the resource pack defines.

        Args:
            sound_identifier (str): The sound name, `<namespace>:<sound_reference>`.
            music_info (MusicInfo): The duration, music information and tags.
        """
        self._content.add_definition(
            _ServerSound.from_music_info(sound_identifier, music_info)
        )
        return self

    def queue(self) -> "ServerSoundDefinition":
        """Queues the server sound definitions, when there is any."""
        if not self._content.definitions:
            return self
        return super().queue("")

    def __export__(self) -> None:
        if not self._content.definitions:
            return None
        return super().__export__()
