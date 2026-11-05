"""The resource pack's `sounds.json`: the sounds played by block, entity, individual and
interactive events."""

from typing import Annotated

from anvil.api.blocks.blocks_json import BlocksJSONObject
from anvil.api.logic.molang import Molang
from anvil.api.sounds.server_sound_definitions import MusicInfo
from anvil.api.sounds.sound_definitions import SoundDefinition, _SoundDescription
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import (
    JsonFile,
    JsonObject,
    Keyed,
    NonNegative,
    Positive,
    json_field,
)
from anvil.lib.jsonmodel.enums import (
    BlockInteractiveSoundEvent,
    BlockSoundEvent,
    EntitySoundEvent,
    SoundCategory,
)
from anvil.lib.translator import AnvilTranslator

_DEFAULT_PITCH = (0.8, 1.2)


class _SoundEventSound(JsonObject):
    """The sound an event plays.

    Args:
        event (str): The event name.
        sound (str): The sound name, as in the sound definitions.
        pitch (float | tuple[float, float], optional): The pitch, or a random pitch range.
        volume (float, optional): The volume.
    """

    event: str = json_field(exclude=True)
    sound: str = json_field()
    pitch: Annotated[float, Positive] | tuple[float, float] | None = None
    volume: Annotated[float, NonNegative] | None = None


class _SoundEvents(JsonObject):
    """The sounds of a block or an entity, and of each of their events."""

    events: Annotated[list[_SoundEventSound], Keyed("event")] = json_field(
        default_factory=list, omit_default=True
    )

    def add_event(self, event: _SoundEventSound) -> None:
        """Sets an event's sound, in place of an earlier one."""
        self.events = [x for x in self.events if x.event != event.event] + [event]


class _BlockSounds(_SoundEvents):
    """The sounds of one block.

    Args:
        block (str): The block identifier.
    """

    block: str = json_field(exclude=True)


class _EntityVariant(_SoundEvents):
    """The sounds of one variant of an entity.

    Args:
        variant (str): The value of the variant key.
    """

    variant: str = json_field(exclude=True)


class _EntityVariants(JsonObject):
    """The `variants` of an entity's sounds: a key, and the sounds of each of its values."""

    key: Molang | str = json_field()
    map: Annotated[list[_EntityVariant], Keyed("variant")] = json_field(
        default_factory=list
    )

    def variant(self, variant: str) -> _EntityVariant:
        """The sounds of a variant, added when it has none yet."""
        for existing in self.map:
            if existing.variant == variant:
                return existing
        self.map.append(_EntityVariant(variant=variant))
        return self.map[-1]


class _EntitySounds(_SoundEvents):
    """The sounds of one entity.

    Args:
        entity (str): The entity identifier.
    """

    entity: str = json_field(exclude=True)
    variants: _EntityVariants | None = None

    def set_variant_key(self, key: Molang | str) -> None:
        """Sets the key the variants are picked by. Changing it keeps the variants."""
        if self.variants is None:
            self.variants = _EntityVariants(key=key)
        else:
            self.variants.key = key


class _EntitySoundsSection(JsonObject):
    """The `entity_sounds` of `sounds.json`."""

    entities: Annotated[list[_EntitySounds], Keyed("entity")] = json_field(
        default_factory=list, omit_default=True
    )

    def entity(self, entity: str) -> _EntitySounds:
        """The sounds of an entity, added when it has none yet."""
        for existing in self.entities:
            if existing.entity == entity:
                return existing
        self.entities.append(_EntitySounds(entity=entity))
        return self.entities[-1]


class _BlockSoundsSection(JsonObject):
    """A list of block sounds, written as one object keyed by block."""

    block_sounds: Annotated[list[_BlockSounds], Keyed("block")] = json_field(
        default_factory=list, omit_default=True
    )

    def block(self, block: str) -> _BlockSounds:
        """The sounds of a block, added when it has none yet."""
        for existing in self.block_sounds:
            if existing.block == block:
                return existing
        self.block_sounds.append(_BlockSounds(block=block))
        return self.block_sounds[-1]


class _IndividualEventSounds(JsonObject):
    """The `individual_event_sounds` of `sounds.json`: sounds played by event name."""

    events: Annotated[list[_SoundEventSound], Keyed("event")] = json_field(
        default_factory=list, omit_default=True
    )

    def add_event(self, event: _SoundEventSound) -> None:
        """Sets an event's sound, in place of an earlier one."""
        self.events = [x for x in self.events if x.event != event.event] + [event]


class _IndividualNamedSounds(JsonObject):
    """The `individual_named_sounds` of `sounds.json`: sounds played by name, such as
    biome ambient sounds."""

    sounds: Annotated[list[_SoundEventSound], Keyed("event")] = json_field(
        default_factory=list, omit_default=True
    )

    def add_sound(self, sound: _SoundEventSound) -> None:
        """Sets a named sound, in place of an earlier one."""
        self.sounds = [x for x in self.sounds if x.event != sound.event] + [sound]


class _SoundsFile(JsonObject):
    """The content of `sounds.json`. Empty sections are left out."""

    block_sounds: Annotated[list[_BlockSounds], Keyed("block")] = json_field(
        default_factory=list, omit_default=True
    )
    entity_sounds: _EntitySoundsSection = json_field(
        default_factory=_EntitySoundsSection
    )
    individual_event_sounds: _IndividualEventSounds = json_field(
        default_factory=_IndividualEventSounds
    )
    individual_named_sounds: _IndividualNamedSounds = json_field(
        default_factory=_IndividualNamedSounds
    )
    interactive_sounds: _BlockSoundsSection = json_field(
        default_factory=_BlockSoundsSection
    )

    def block(self, block: str) -> _BlockSounds:
        """The sounds of a block, added when it has none yet."""
        for existing in self.block_sounds:
            if existing.block == block:
                return existing
        self.block_sounds.append(_BlockSounds(block=block))
        return self.block_sounds[-1]


class SoundEvent(JsonFile[_SoundsFile]):
    """The sound events of the resource pack, `sounds.json`: the sounds blocks and entities
    play for each event, and sounds played by name. There is one per pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/addcustomsounds)
    """

    _instance = None
    _pack = Pack.RP
    _object_type = "Sound Events"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("sounds")
        self._initialized = True
        self._changed = False

    @staticmethod
    def _sound(
        event: str,
        sound_reference: str,
        pitch: float | tuple[float, float] | None,
        volume: float | None,
    ) -> _SoundEventSound:
        return _SoundEventSound(
            event=event,
            sound=f"{CONFIG.NAMESPACE}:{sound_reference}",
            pitch=pitch,
            volume=volume,
        )

    def add_entity_event(
        self,
        entity: str,
        sound_reference: str,
        sound_event: EntitySoundEvent,
        category: SoundCategory,
        volume: float = 1.0,
        pitch: float | tuple[float, float] = _DEFAULT_PITCH,
        max_distance: float | None = None,
        min_distance: float | None = None,
        variant_query: Molang | str | None = None,
        variant_map: str | None = None,
        subtitle: str | None = None,
        server_sound: MusicInfo | None = None,
    ) -> _SoundDescription:
        """Plays a sound for an entity's event, and defines the sound.

        Args:
            entity (str): The entity identifier.
            sound_reference (str): The sound name, written as `<namespace>:<sound_reference>`.
            sound_event (EntitySoundEvent): The event.
            category (SoundCategory): The volume slider the sound follows.
            volume (float, optional): The volume. Defaults to 1.
            pitch (float | tuple[float, float], optional): The pitch, or a random pitch
                range. Defaults to (0.8, 1.2).
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            variant_query (Molang | str, optional): The key the entity's sound variants are
                picked by. With `variant_map`, the sound plays for that variant only.
            variant_map (str, optional): The value of `variant_query` the sound is for.
            subtitle (str, optional): The subtitle text.
            server_sound (MusicInfo, optional): Also registers the sound in the behavior
                pack's (experimental) server sound definitions.

        Returns:
            _SoundDescription: The sound definition; add its files with `add_sound`.
        """
        self._changed = True
        sounds = self._document.entity_sounds.entity(str(entity))
        event = self._sound(sound_event, sound_reference, pitch, volume)
        if variant_query is not None:
            if variant_map is None:
                raise ValueError(
                    f"A sound variant needs the variant it is for (variant_map). Entity [{entity}]"
                )
            sounds.set_variant_key(variant_query)
            sounds.variants.variant(variant_map).add_event(event)
        else:
            sounds.add_event(event)

        key = f"subtitle.entity.{entity}.{sound_event}"
        if subtitle is not None:
            AnvilTranslator().add_localization_entry(key, subtitle)

        return SoundDefinition().sound_reference(
            sound_reference,
            category,
            max_distance=max_distance,
            min_distance=min_distance,
            subtitle=key if subtitle is not None else None,
            server_sound=server_sound,
        )

    def add_block_event(
        self,
        block: str,
        sound_reference: str,
        sound_event: BlockSoundEvent,
        volume: float = 1.0,
        pitch: float | tuple[float, float] = _DEFAULT_PITCH,
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str | None = None,
        server_sound: MusicInfo | None = None,
    ) -> _SoundDescription:
        """Plays a sound for a block's event, adds the block to `blocks.json`, and defines
        the sound.

        Args:
            block (str): The block identifier.
            sound_reference (str): The sound name, written as `<namespace>:<sound_reference>`.
            sound_event (BlockSoundEvent): The event.
            volume (float, optional): The volume. Defaults to 1.
            pitch (float | tuple[float, float], optional): The pitch, or a random pitch
                range. Defaults to (0.8, 1.2).
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            subtitle (str, optional): The subtitle text.
            server_sound (MusicInfo, optional): Also registers the sound in the behavior
                pack's (experimental) server sound definitions.

        Returns:
            _SoundDescription: The sound definition; add its files with `add_sound`.
        """
        self._changed = True
        self._document.block(str(block)).add_event(
            self._sound(sound_event, sound_reference, pitch, volume)
        )
        BlocksJSONObject().add_block(block)
        return self._block_sound(
            block,
            sound_reference,
            sound_event,
            max_distance,
            min_distance,
            subtitle,
            server_sound,
        )

    def add_block_interactive_event(
        self,
        block: str,
        sound_reference: str,
        sound_event: BlockInteractiveSoundEvent,
        volume: float = 1.0,
        pitch: float | tuple[float, float] = _DEFAULT_PITCH,
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str | None = None,
        server_sound: MusicInfo | None = None,
    ) -> _SoundDescription:
        """Plays a sound when an entity interacts with a block, such as stepping on it, adds
        the block to `blocks.json`, and defines the sound.

        Args:
            block (str): The block identifier.
            sound_reference (str): The sound name, written as `<namespace>:<sound_reference>`.
            sound_event (BlockInteractiveSoundEvent): The event.
            volume (float, optional): The volume. Defaults to 1.
            pitch (float | tuple[float, float], optional): The pitch, or a random pitch
                range. Defaults to (0.8, 1.2).
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            subtitle (str, optional): The subtitle text.
            server_sound (MusicInfo, optional): Also registers the sound in the behavior
                pack's (experimental) server sound definitions.

        Returns:
            _SoundDescription: The sound definition; add its files with `add_sound`.
        """
        self._changed = True
        self._document.interactive_sounds.block(str(block)).add_event(
            self._sound(sound_event, sound_reference, pitch, volume)
        )
        BlocksJSONObject().add_block(block)
        return self._block_sound(
            block,
            sound_reference,
            sound_event,
            max_distance,
            min_distance,
            subtitle,
            server_sound,
        )

    def _block_sound(
        self,
        block: str,
        sound_reference: str,
        sound_event: str,
        max_distance: float | None,
        min_distance: float | None,
        subtitle: str | None,
        server_sound: MusicInfo | None,
    ) -> _SoundDescription:
        key = f"subtitle.block.{block}.{sound_event}"
        if subtitle is not None:
            AnvilTranslator().add_localization_entry(key, subtitle)
        return SoundDefinition().sound_reference(
            sound_reference,
            SoundCategory.Block,
            max_distance=max_distance,
            min_distance=min_distance,
            subtitle=key if subtitle is not None else None,
            server_sound=server_sound,
        )

    def add_individual_event(
        self,
        sound_reference: str,
        category: SoundCategory,
        volume: float = 1.0,
        pitch: float | tuple[float, float] = _DEFAULT_PITCH,
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str | None = None,
        server_sound: MusicInfo | None = None,
    ) -> _SoundDescription:
        """Plays a sound for the event named `sound_reference`, and defines the sound.

        Args:
            sound_reference (str): The event name, and the sound name written as
                `<namespace>:<sound_reference>`.
            category (SoundCategory): The volume slider the sound follows.
            volume (float, optional): The volume. Defaults to 1.
            pitch (float | tuple[float, float], optional): The pitch, or a random pitch
                range. Game default (0.8, 1.2).
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.
            subtitle (str, optional): The subtitle text.
            server_sound (MusicInfo, optional): Also registers the sound in the behavior
                pack's (experimental) server sound definitions.

        Returns:
            _SoundDescription: The sound definition; add its files with `add_sound`.
        """
        self._changed = True
        self._document.individual_event_sounds.add_event(
            self._sound(
                sound_reference,
                sound_reference,
                None if pitch == _DEFAULT_PITCH else pitch,
                volume,
            )
        )

        key = f"subtitle.individual.{sound_reference}"
        if subtitle is not None:
            AnvilTranslator().add_localization_entry(key, subtitle)

        return SoundDefinition().sound_reference(
            sound_reference,
            category,
            max_distance=max_distance,
            min_distance=min_distance,
            subtitle=key if subtitle is not None else None,
            server_sound=server_sound,
        )

    def add_individual_named_sound(
        self,
        sound_reference: str,
        category: SoundCategory = SoundCategory.Ambient,
        volume: float = 1.0,
        pitch: float | tuple[float, float] = _DEFAULT_PITCH,
        max_distance: float | None = None,
        min_distance: float | None = None,
    ) -> _SoundDescription:
        """Registers a sound in `individual_named_sounds`, and defines it. Client biome
        ambient sounds (`minecraft:ambient_sounds`) must be defined here.

        Args:
            sound_reference (str): The name, and the sound name written as
                `<namespace>:<sound_reference>`.
            category (SoundCategory, optional): The volume slider the sound follows.
                Defaults to Ambient.
            volume (float, optional): The volume. Defaults to 1.
            pitch (float | tuple[float, float], optional): The pitch, or a random pitch
                range. Game default (0.8, 1.2).
            max_distance (float, optional): The distance the sound is no longer heard at.
            min_distance (float, optional): The distance the sound starts to fade at.

        Returns:
            _SoundDescription: The sound definition; add its files with `add_sound`.
        """
        self._changed = True
        self._document.individual_named_sounds.add_sound(
            self._sound(
                sound_reference,
                sound_reference,
                None if pitch == _DEFAULT_PITCH else pitch,
                volume,
            )
        )
        return SoundDefinition().sound_reference(
            sound_reference,
            category,
            max_distance=max_distance,
            min_distance=min_distance,
        )

    def queue(self) -> "SoundEvent":
        """Queues `sounds.json` for export, when a sound event was added."""
        if not self._changed:
            return self
        return super().queue()
