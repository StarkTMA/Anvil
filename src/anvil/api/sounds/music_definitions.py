"""The resource pack's `sounds/music_definitions.json`: the music played in each
situation."""

from typing import Annotated, Any

from anvil.api.core.enums import MusicCategory, SoundCategory
from anvil.api.core.types import JsonSchema
from anvil.api.sounds.server_sound_definitions import MusicInfo
from anvil.api.sounds.sound_definitions import SoundDefinition, _SoundDescription
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject, Keyed, NonNegative, json_field


class _Music(JsonObject):
    """The music of one music category.

    Args:
        category (str): The music category.
        event_name (str): The sound played.
        min_delay (int): The shortest wait between two tracks, in seconds.
        max_delay (int): The longest wait between two tracks, in seconds.
    """

    category: str = json_field(exclude=True)
    event_name: str = json_field()
    max_delay: Annotated[int, NonNegative] = json_field()
    min_delay: Annotated[int, NonNegative] = json_field()

    def __validate__(self) -> None:
        if self.min_delay > self.max_delay:
            raise ValueError(
                f"Music '{self.category}' has a min_delay larger than its max_delay."
            )


class _MusicDefinitionsFile(JsonObject):
    """The content of `sounds/music_definitions.json`: the music of each category."""

    music: Annotated[list[_Music], Keyed("category")] = json_field(default_factory=list)

    def add_music(self, music: _Music) -> None:
        """Adds a category's music, in place of an earlier one."""
        self.music = [x for x in self.music if x.category != music.category] + [music]

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        payload.update(payload.pop("music", {}))
        return payload

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        music = schema["properties"].pop("music")
        schema.pop("required", None)
        schema["additionalProperties"] = music["additionalProperties"]
        return schema


class MusicDefinition(JsonFile):
    """The music definitions of the resource pack, `sounds/music_definitions.json`: the
    music played for each music category. There is one per pack.
    """

    _document = _MusicDefinitionsFile
    _instance = None
    _pack = Pack.RP
    _folder = "sounds"
    _object_type = "Music Definitions"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("music_definitions")
        self._initialized = True

    def music_definition(
        self,
        music_reference: MusicCategory | str,
        min_delay: int = 60,
        max_delay: int = 180,
        server_sound: MusicInfo | None = None,
    ) -> _SoundDescription:
        """Defines the music of a music category, played as the sound
        `<namespace>:music.<music_reference>`.

        Args:
            music_reference (MusicCategory | str): The music category.
            min_delay (int, optional): The shortest wait between two tracks, in seconds.
                Defaults to 60.
            max_delay (int, optional): The longest wait between two tracks, in seconds.
                Defaults to 180.
            server_sound (MusicInfo, optional): Also registers the music in the behavior
                pack's (experimental) server sound definitions.

        Returns:
            _SoundDescription: The music's sound definition; add its files with `add_sound`.
        """
        self._content.add_music(
            _Music(
                category=str(music_reference),
                event_name=f"{CONFIG.NAMESPACE}:music.{music_reference}",
                max_delay=max_delay,
                min_delay=min_delay,
            )
        )
        return SoundDefinition().sound_reference(
            f"music.{music_reference}", SoundCategory.Music, server_sound=server_sound
        )

    def queue(self) -> "MusicDefinition":
        """Queues the music definitions for export."""
        return super().queue("")

    def __export__(self) -> None:
        if not self._content.music:
            return None
        return super().__export__()
