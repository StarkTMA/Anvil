import os
from enum import StrEnum

from anvil import CONFIG
from anvil.api.logic.molang import Molang
from anvil.lib.enums import EntitySoundEvent, MusicCategory, SoundCategory
from anvil.lib.lib import CopyFiles, FileExists
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import Identifier


class SoundDescription:
    def __init__(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: float = 0,
        min_distance: float = 9999,
    ) -> None:
        """Initializes a SoundDescription instance.

        Parameters:
            sound_reference (str): The definition of the sound.
            category (SoundCategory): The category of the sound.
            use_legacy_max_distance (bool, optional): Use legacy max distance if True. Defaults to False.
            max_distance (int, optional): The maximum distance for the sound. Defaults to 0.
            min_distance (int, optional): The minimum distance for the sound. Defaults to 9999.
        """
        self._category = category.value
        self._sound_reference = sound_reference
        self._sound_definition = f"{CONFIG.NAMESPACE}:{sound_reference}"
        self._sound = JsonSchemes.sound(self._sound_definition, self._category)

        if use_legacy_max_distance != False:
            self._sound[self._sound_definition].update({"__use_legacy_max_distance": use_legacy_max_distance})
        if max_distance != 0:
            self._sound[self._sound_definition].update({"max_distance": max_distance})
        if min_distance != 9999:
            self._sound[self._sound_definition].update({"min_distance": min_distance})
        self._sounds = []

    def add_sound(
        self,
        sound_name,
        volume: int = 1,
        weight: int = 1,
        pitch: int = [1, 1],
        is_3d: bool = None,
        stream: bool = None,
        load_on_low_memory: bool = False,
    ):
        """Adds a sound to the SoundDescription instance.

        Parameters:
            sound_name (str): The name of the sound.
            volume (int, optional): The volume of the sound. Defaults to 1.
            weight (int, optional): The weight of the sound. Defaults to 1.
            pitch (list[int], optional): The pitch of the sound. Defaults to [1, 1].
            is_3d (bool, optional): If the sound is 3D. Defaults to None.
            stream (bool, optional): If the sound is streamed. Defaults to None.
            load_on_low_memory (bool, optional): If the sound is loaded on low memory. Defaults to False.
        """
        parent_dir = self._sound_reference.split(".")[0]
        if not FileExists(os.path.join("assets", "sounds", parent_dir, f"{sound_name}.ogg")):
            raise FileNotFoundError(f"{sound_name}.ogg not found in {os.path.join('assets', 'sounds', parent_dir)}. Please ensure the file exists.")

        self._sound_name = sound_name
        splits = self._sound_definition.removeprefix(f"{CONFIG.NAMESPACE}:").split(".")
        self._path = CONFIG.NAMESPACE
        for i in range(len(splits) - 1):
            self._path = os.path.join(self._path, splits[i])
        sound = {"name": os.path.join("sounds", self._path, self._sound_name), "load_on_low_memory": load_on_low_memory}
        if pitch != [1, 1]:
            sound.update({"pitch": pitch})
        if not is_3d is None:
            sound.update({"is3D": is_3d})
        if not stream is None:
            sound.update({"stream": stream})
        if volume != 1:
            sound.update({"volume": volume})
        if weight != 1:
            sound.update({"weight": weight})
        self._sounds.append(sound)

        CONFIG.Report.add_report(ReportType.SOUND, col0=self._sound_definition, col1=self._sound_name, vanilla=False)
        return self

    @property
    def identifier(self):
        return self._sound_definition

    @property
    def _export(self):
        """Returns the sound description.

        Returns:
            dict: The sound description
        """
        parent_dir = self._sound_reference.split(".")[0]
        for sound in self._sounds:
            s = sound["name"].split("\\")[-1]
            CopyFiles(
                os.path.join("assets", "sounds", parent_dir),
                os.path.join(
                    CONFIG.RP_PATH,
                    "sounds",
                    self._path,
                ),
                f"{s}.ogg",
            )
        self._sound[self._sound_definition]["sounds"] = self._sounds
        return self._sound


class SoundDefinition(AddonObject):
    """Handles sound definitions.

    Attributes:
        _sounds (list[SoundDescription], optional): A list of sound descriptions. Defaults to empty list.
    """

    _path = os.path.join(CONFIG.RP_PATH, "sounds")

    def __init__(self) -> None:
        """Initializes a SoundDefinition instance."""
        super().__init__("sound_definitions")
        self.content(JsonSchemes.sound_definitions())
        self._sounds: list[SoundDescription] = []

    def sound_reference(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: float = 0,
        min_distance: float = 9999,
    ):
        """Defines a sound for the SoundDefinition instance.

        Parameters:
            sound_reference (str): The sound_reference of the sound.
            category (SoundCategory): The category of the sound.
            use_legacy_max_distance (bool, optional): Use legacy max distance if True. Defaults to False.
            max_distance (int, optional): The maximum distance for the sound. Defaults to 0.
            min_distance (int, optional): The minimum distance for the sound. Defaults to 9999.

        Returns:
            SoundDescription: The created sound description instance.
        """
        sound = SoundDescription(
            sound_reference,
            category,
            use_legacy_max_distance,
            max_distance,
            min_distance,
        )
        self._sounds.append(sound)
        return sound

    @property
    def queue(self):
        """Returns the queue for the sound definition.

        Returns:
            queue: The queue for the sound definition.
        """
        return super().queue("")

    def _export(self):
        """Returns the sound definition.

        Returns:
            dict: The sound definition.
        """
        for sound in self._sounds:
            self._content["sound_definitions"].update(sound._export)
        return super()._export()


class MusicDefinition(AddonObject):
    """Handles music definitions.

    Attributes:
        _extensions (dict): The file extensions for the music definition.
        _sounds (list[SoundDescription], optional): A list of sound descriptions. Defaults to empty list.
    """

    _path = os.path.join(CONFIG.RP_PATH, "sounds")

    def __init__(self) -> None:
        """Initializes a MusicDefinition instance."""
        super().__init__("music_definitions")
        self.content(JsonSchemes.music_definitions())

    def music_definition(self, music_reference: MusicCategory | str, min_delay: int = 60, max_delay: int = 180):
        """Defines a music for the MusicDefinition instance.

        Parameters:
            music_category (MusicCategory): The category of the music.
            min_delay (int, optional): The minimum delay for the music. Defaults to 60.
            max_delay (int, optional): The maximum delay for the music. Defaults to 180.

        Returns:
            SoundDescription: The created sound description instance.
        """
        self._content.update(
            {
                music_reference: {
                    "event_name": music_reference,
                    "max_delay": max_delay,
                    "min_delay": min_delay,
                }
            }
        )

    @property
    def queue(self):
        """Returns the queue for the music definition.

        Returns:
            queue: The queue for the music definition.
        """
        return super().queue("")

    def _export(self):
        """Returns the music definition.

        Returns:
            dict: The music definition.
        """
        return super()._export()


class SoundEvent(AddonObject):
    """Handles sound events."""

    _path = os.path.join(CONFIG.RP_PATH)

    def __init__(self) -> None:
        """Initializes a SoundEvent instance."""
        super().__init__("sounds")
        self.content(JsonSchemes.sounds())

    def add_entity_event(
        self,
        entity_identifier: Identifier,
        sound_identifier: str,
        sound_event: EntitySoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        variant_query: Molang = None,
        variant_map: str = None,
    ):
        """Adds an entity event to the SoundEvent instance.

        Parameters:
            entity_identifier (Identifier): The identifier of the entity.
            sound_event (EntitySoundEvent): The sound event for the entity.
            sound_identifier (str): The identifier of the sound.
            volume (float, optional): The volume of the event. Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch of the event. Defaults to (0.8, 1.2).
            variant_query (Molang, optional): The variant query for the event. Defaults to None.
            variant_map (str, optional): The variant map for the event. Defaults to None.
        """

        self._content["entity_sounds"]["entities"].setdefault(
            entity_identifier, {entity_identifier: {"events": {}}, "variants": {"key": "", "map": {}}}
        )
        if variant_query is not None:
            self._content["entity_sounds"]["entities"][entity_identifier]["variants"]["key"] = variant_query
            self._content["entity_sounds"]["entities"][entity_identifier]["variants"]["map"][variant_map] = {
                "sound": f"{CONFIG.NAMESPACE}:{sound_identifier}",
                "pitch": pitch if pitch != (0.8, 1.2) else {},
                "volume": volume,
            }
        else:
            self._content["entity_sounds"]["entities"][entity_identifier]["events"][sound_event.value] = {
                "sound": f"{CONFIG.NAMESPACE}:{sound_identifier}",
                "pitch": pitch if pitch != (0.8, 1.2) else {},
                "volume": volume,
            }


    def add_individual_event(
        self,
        sound_identifier: str,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
    ):
        """Adds an individual event to the SoundEvent instance.

        Parameters:
            sound_identifier (str): The identifier of the sound.
            volume (float, optional): The volume of the event. Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch of the event. Defaults to (0.8, 1.2).
        """
        self._content["individual_event_sounds"]["events"][sound_identifier] = {
            "sound": sound_identifier,
            "pitch": pitch if pitch != (0.8, 1.2) else {},
            "volume": volume,
        }

    @property
    def queue(self):
        """Returns the queue for the sound event.

        Returns:
            queue: The queue for the sound event.
        """
        return super().queue()
