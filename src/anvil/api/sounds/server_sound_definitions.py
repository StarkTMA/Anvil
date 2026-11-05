"""The behavior pack's server sound definitions: music information and duration of
sounds, for the server."""

import re
from dataclasses import dataclass
from typing import Annotated, ClassVar

from anvil.lib.config import Pack
from anvil.lib.format_versions import SERVER_SOUND_DEFINITIONS_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, NonNegative, Pairs, json_field
from anvil.lib.jsonmodel.enums import DurationInfoMode

_NO_SPACE = re.compile(r"^\S+$")


@dataclass(kw_only=True)
class MusicInfo:
    """The server-side information of a sound, registered with `server_sound=` on the
    sound methods.

    Args:
        genres (list[str], optional): Free-form genre labels.
        moods (list[str], optional): Free-form mood labels.
        artist (str, optional): The artist, as display text or a translation key.
        title (str, optional): The title, as display text or a translation key.
        duration (float, optional): The length of the sound, in seconds. When set, the
            server tracks the sound's lifetime.
        duration_tracking (DurationInfoMode, optional): How the duration drains: by game
            ticks or by wall-clock time. Defaults to game time.
        tags (list[tuple[str, str | list[str]]], optional): Pack-defined `(name, value)`
            tags, the value a string or a list of strings. Names and values have no
            whitespace, and each name is used once.
        broadcast_range (float, optional): A broadcast play of the sound reaches players
            within this many blocks, capped by their view distance.
    """

    genres: list[str] | None = None
    moods: list[str] | None = None
    artist: str | None = None
    title: str | None = None
    duration: float | None = None
    duration_tracking: DurationInfoMode = DurationInfoMode.GameTime
    tags: list[tuple[str, str | list[str]]] | None = None
    broadcast_range: float | None = None


class _ServerMusicInfo(JsonObject):
    """The `music_info` of a server sound. Unset keys are left out."""

    genres: list[str] = json_field(default_factory=list, omit_default=True)
    moods: list[str] = json_field(default_factory=list, omit_default=True)
    artist: str | None = None
    title: str | None = None


class _ServerDurationInfo(JsonObject):
    """The `duration_info` of a server sound: the server tracks the sound's lifetime."""

    mode: DurationInfoMode = json_field()
    seconds: Annotated[float, NonNegative] = json_field()


class _ServerSound(JsonObject):
    """One server sound definition."""

    __required__: ClassVar[tuple[str, ...]] = ("sound_event_name",)

    sound_event_name: str = json_field()
    duration_info: _ServerDurationInfo | None = None
    music_info: _ServerMusicInfo | None = None
    tags: Annotated[list[tuple[str, str | list[str]]], Pairs] = json_field(
        default_factory=list, omit_default=True
    )
    broadcast_range: Annotated[float, NonNegative] | None = None

    @classmethod
    def from_music_info(cls, sound_event_name: str, info: MusicInfo) -> "_ServerSound":
        """The server sound of a `MusicInfo`."""
        music = _ServerMusicInfo(
            genres=list(info.genres or []),
            moods=list(info.moods or []),
            artist=info.artist,
            title=info.title,
        )
        return cls(
            sound_event_name=sound_event_name,
            duration_info=(
                None
                if info.duration is None
                else _ServerDurationInfo(
                    mode=info.duration_tracking, seconds=info.duration
                )
            ),
            music_info=music if music.__json__() else None,
            tags=list(info.tags or []),
            broadcast_range=info.broadcast_range,
        )

    def __validate__(self) -> None:
        names = [name for name, _ in self.tags]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(
                f"Server sound '{self.sound_event_name}': tags {duplicates} are set more "
                "than once."
            )
        words = [self.sound_event_name, *names]
        for _, value in self.tags:
            words += [value] if isinstance(value, str) else value
        for word in words:
            if not _NO_SPACE.match(word):
                raise ValueError(
                    f"Server sound '{self.sound_event_name}': '{word}' must be one word "
                    "with no whitespace."
                )


class _ServerSoundDefinitionsFile(JsonObject):
    """The content of the behavior pack's `sounds/sound_definitions.json`: a list of server
    sound definitions."""

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


class ServerSoundDefinition(JsonFile[_ServerSoundDefinitionsFile]):
    """The behavior pack's server sound definitions:
    duration, music information and tags of sounds the resource pack defines.

    Server sounds are registered through `server_sound=` on `SoundDefinition.sound_reference`
    and the methods that call it (`MusicDefinition.music_definition`, the
    `SoundEvent.add_*_event` methods), so a server sound always has its client sound.
    """

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
        self._document.add_definition(
            _ServerSound.from_music_info(sound_identifier, music_info)
        )
        return self

    def queue(self) -> "ServerSoundDefinition":
        """Queues the server sound definitions, when there is any."""
        if not self._document.definitions:
            return self
        return super().queue("")

    def __export__(self) -> None:
        if not self._document.definitions:
            return None
        return super().__export__()
