import os

from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG
from anvil.lib.enums import (
    BlockInteractiveSoundEvent,
    BlockSoundEvent,
    EntitySoundEvent,
    MusicCategory,
    SoundCategory,
)
from anvil.lib.lib import CopyFiles, FileExists
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import Identifier


class _SoundDescription:
    """Represents a sound description for Minecraft addon sound definitions.

    Manages the configuration and properties of individual sound effects,
    including volume, distance, and 3D positioning parameters.
    """

    def __init__(
        self,
        sound_reference: str,
        category: SoundCategory,
        use_legacy_max_distance: bool = False,
        max_distance: float = 0,
        min_distance: float = 9999,
    ) -> None:
        """Initializes a _SoundDescription instance.

        Parameters:
            sound_reference (str): The definition of the sound.
            category (SoundCategory): The category of the sound.
            use_legacy_max_distance (bool, optional): Use legacy max distance if True. Defaults to False.
            max_distance (int, optional): The maximum distance for the sound. Defaults to 0.
            min_distance (int, optional): The minimum distance for the sound. Defaults to 9999.
        """
        self._category = category
        self._sound_reference = sound_reference
        self._sound_definition = f"{CONFIG.NAMESPACE}:{sound_reference}"
        self._sound = JsonSchemes.sound(self._sound_definition, self._category)

        if use_legacy_max_distance != False:
            self._sound[self._sound_definition].update(
                {"__use_legacy_max_distance": use_legacy_max_distance}
            )
        if max_distance != 0:
            self._sound[self._sound_definition]["max_distance"] = max_distance
        if min_distance != 9999:
            self._sound[self._sound_definition]["min_distance"] = min_distance
        self._sounds = []

    def add_sound(
        self,
        sound_name: str,
        volume: int = 1,
        weight: int = 1,
        pitch: int = 1,
        is_3d: bool = None,
        stream: bool = None,
    ):
        """Adds a sound to the _SoundDescription instance.

        Parameters:
            sound_name (str): The name of the sound.
            volume (int, optional): The volume of the sound. Defaults to 1.
            weight (int, optional): The weight of the sound. Defaults to 1.
            pitch (int, optional): The pitch of the sound. Defaults to 1.
            is_3d (bool, optional): If the sound is 3D. Defaults to None.
            stream (bool, optional): If the sound is streamed. Defaults to None.
            load_on_low_memory (bool, optional): If the sound is loaded on low memory. Defaults to False.
        """
        dirs = sound_name.split("/")
        source_path = os.path.join("assets", "sounds", *dirs[:-1])
        target_path = os.path.join("sounds", CONFIG.NAMESPACE, *dirs[:-1])
        sound_name = dirs[-1]
        if not FileExists(os.path.join(source_path, f"{sound_name}.ogg")):
            raise FileNotFoundError(
                f"{sound_name}.ogg not found in {source_path}. Please ensure the file exists."
            )

        sound_dict = {
            "name": os.path.join(target_path, sound_name),
            "source": source_path,
            "target": target_path,
        }
        if pitch != 1:
            sound_dict.update({"pitch": pitch})
        if not is_3d is None:
            sound_dict.update({"is3D": is_3d})
        if not stream is None:
            sound_dict.update({"stream": stream})
        if volume != 1:
            sound_dict.update({"volume": volume})
        if weight != 1:
            sound_dict.update({"weight": weight})
        if len(sound_dict.keys()) == 1:
            sound_dict = os.path.join("sounds", target_path, sound_name)
        self._sounds.append(sound_dict)

        CONFIG.Report.add_report(
            ReportType.SOUND,
            col0=self._sound_definition,
            col1=sound_name,
            vanilla=False,
        )
        return self

    @property
    def identifier(self):
        """Gets the sound definition identifier.

        Returns:
            str: The sound definition identifier.
        """
        return self._sound_definition

    @property
    def _export(self):
        """Returns the sound description.

        Returns:
            dict: The sound description
        """
        for sound in self._sounds:
            sound_name = (sound["name"] if "name" in sound else sound).split("\\")[-1]
            CopyFiles(
                sound["source"],
                os.path.join(
                    CONFIG.RP_PATH,
                    sound["target"],
                ),
                f"{sound_name}.ogg",
            )
            del sound["source"]
            del sound["target"]
            if len(sound.keys()) == 1:
                sound = sound["name"]
            self._sound[self._sound_definition]["sounds"].append(sound)
        return self._sound


class SoundDefinition(AddonObject):
    """Singleton for handling sound definitions.

    Attributes:
        _sounds (list[_SoundDescription], optional): A list of sound descriptions. Defaults to empty list.
    """

    _instance = None
    _path = os.path.join(CONFIG.RP_PATH, "sounds")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("sound_definitions")
        self.content(JsonSchemes.sound_definitions())
        self._sounds: list[_SoundDescription] = []
        self._initialized = True

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
            _SoundDescription: The created sound description instance.
        """
        sound = _SoundDescription(
            sound_reference,
            category,
            use_legacy_max_distance,
            max_distance=max_distance,
            min_distance=min_distance,
        )
        self._sounds.append(sound)
        return sound

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
    """Singleton for handling music definitions.

    Attributes:
        _extensions (dict): The file extensions for the music definition.
        _sounds (list[_SoundDescription], optional): A list of sound descriptions. Defaults to empty list.
    """

    _instance = None
    _path = os.path.join(CONFIG.RP_PATH, "sounds")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("music_definitions")
        self.content(JsonSchemes.music_definitions())
        self._initialized = True

    def music_definition(
        self,
        music_reference: MusicCategory | str,
        min_delay: int = 60,
        max_delay: int = 180,
    ):
        """Defines a music for the MusicDefinition instance.

        Parameters:
            music_category (MusicCategory): The category of the music.
            min_delay (int, optional): The minimum delay for the music. Defaults to 60.
            max_delay (int, optional): The maximum delay for the music. Defaults to 180.

        Returns:
            _SoundDescription: The created sound description instance.
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
        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            f"music.{music_reference}", SoundCategory.Music
        )

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
    """Singleton for handling sound events for entities and individual sounds.

    Manages the creation and configuration of sound events that can be
    triggered by entities or as standalone sounds in the game.
    """

    _instance = None
    _path = os.path.join(CONFIG.RP_PATH)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Only initialize once
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("sounds")
        self.content(JsonSchemes.sounds_json())
        self._initialized = True

    def add_entity_event(
        self,
        entity_identifier: Identifier,
        sound_identifier: str,
        sound_event: EntitySoundEvent,
        category: SoundCategory,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float = 0,
        min_distance: float = 9999,
        variant_query: Molang = None,
        variant_map: str = None,
    ):
        self._content["entity_sounds"]["entities"].setdefault(
            entity_identifier,
            {"events": {}, "variants": {"key": {}, "map": {}}},
        )
        if variant_query is not None:
            self._content["entity_sounds"]["entities"][entity_identifier]["variants"][
                "key"
            ] = variant_query
            self._content["entity_sounds"]["entities"][entity_identifier]["variants"][
                "map"
            ][variant_map] = {
                "sound": f"{CONFIG.NAMESPACE}:{sound_identifier}",
                "pitch": pitch,
                "volume": volume,
            }
        else:
            self._content["entity_sounds"]["entities"][entity_identifier]["events"][
                sound_event.value
            ] = {
                "sound": f"{CONFIG.NAMESPACE}:{sound_identifier}",
                "pitch": pitch,
                "volume": volume,
            }

        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            sound_identifier,
            category,
            max_distance=max_distance,
            min_distance=min_distance,
        )

    def add_block_event(
        self,
        block_identifier: Identifier,
        sound_identifier: str,
        sound_event: BlockSoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float = 0,
        min_distance: float = 9999,
    ):
        self._content["block_sounds"].setdefault(
            block_identifier,
            {"events": {}},
        )
        self._content["block_sounds"][block_identifier]["events"][sound_event] = {
            "sound": f"{CONFIG.NAMESPACE}:{sound_identifier}",
            "pitch": pitch,
            "volume": volume,
        }

        BlocksJSONObject().add_block(block_identifier)

        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            sound_identifier,
            SoundCategory.Block,
            max_distance=max_distance,
            min_distance=min_distance,
        )

    def add_block_interactive_event(
        self,
        block_identifier: Identifier,
        sound_identifier: str,
        sound_event: BlockInteractiveSoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float = 0,
        min_distance: float = 9999,
    ):
        self._content["interactive_sounds"]["block_sounds"].setdefault(
            block_identifier,
            {"events": {}},
        )
        self._content["interactive_sounds"]["block_sounds"][block_identifier]["events"][
            sound_event
        ] = {
            "sound": f"{CONFIG.NAMESPACE}:{sound_identifier}",
            "pitch": pitch,
            "volume": volume,
        }

        BlocksJSONObject().add_block(block_identifier)

        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            sound_identifier,
            SoundCategory.Block,
            max_distance=max_distance,
            min_distance=min_distance,
        )

    def add_individual_event(
        self,
        sound_identifier: str,
        category: SoundCategory,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float = 0,
        min_distance: float = 9999,
    ):
        self._content["individual_event_sounds"]["events"][sound_identifier] = {
            "sound": sound_identifier,
            "pitch": pitch if pitch != (0.8, 1.2) else {},
            "volume": volume,
        }

        sound_definition_object = SoundDefinition()
        return sound_definition_object.sound_reference(
            sound_identifier,
            category,
            max_distance,
            min_distance,
        )

    def queue(self):
        return super().queue()


class BlocksJSONObject(AddonObject):
    _instance = None
    _extension = ".json"
    _path = CONFIG.RP_PATH

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("blocks")
        self.content(JsonSchemes.blocks_json())
        self._initialized = True

    def add_block(self, block: Identifier):
        self._content.update({str(block): {"sound": str(block)}})

    def queue(self):
        return super().queue()
