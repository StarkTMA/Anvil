from anvil.api.blocks.blocks_json import BlocksJSONObject
from anvil.api.sounds import SoundEvent
from anvil.lib.jsonmodel import Identifier
from anvil.lib.jsonmodel.enums import (
    BlockInteractiveSoundEvent,
    BlockSoundEvent,
    BlockSoundGroup,
)

__all__ = ["BlockClient"]


class BlockClient:
    """The client side of a block: its sounds. Blocks have no client file, their sounds are
    written to `blocks.json` and `sounds.json`."""

    _object_type = "Block Client"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates the client side of a block.

        Args:
            name (str): The block's name.
            is_vanilla (bool, optional): If the block is a vanilla one. Defaults to False.
        """
        self.identifier = Identifier.parse(
            name, vanilla=is_vanilla, object_type=self._object_type
        )

    @property
    def name(self) -> str:
        """The block's name, without its namespace."""
        return self.identifier.name

    def sound_group(self, group: BlockSoundGroup | str) -> "BlockClient":
        """Gives the block the sounds of a vanilla sound group, like oak planks have the `wood`
        group's: breaking, placing, walking, and the clicks of doors, buttons and plates. It
        needs no sound files. To make your own sounds for the block, use `block_sound`.

        Args:
            group (BlockSoundGroup | str): The group, like `BlockSoundGroup.Wood`.
        """
        BlocksJSONObject().add_block(self.identifier, group)
        return self

    def block_sound(
        self,
        sound_reference: str,
        sound_event: BlockSoundEvent | BlockInteractiveSoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float | None = None,
        min_distance: float | None = None,
        subtitle: str | None = None,
    ):
        """Gives the block a sound of its own for one of its sound events, registered in
        `sounds.json`. The sound file is `sound_reference`.

        Args:
            sound_reference (str): The sound definition's name.
            sound_event (BlockSoundEvent | BlockInteractiveSoundEvent): The event it plays on.
            volume (float, optional): Defaults to 1.0.
            pitch (tuple[float, float], optional): The pitch range. Defaults to (0.8, 1.2).
            max_distance (float, optional): Where the sound fades out.
            min_distance (float, optional): Where the sound starts to fade.
            subtitle (str, optional): The subtitle shown.

        Raises:
            TypeError: When the event is not a block sound event.
        """
        sound_event_obj = SoundEvent()
        if isinstance(sound_event, BlockSoundEvent):
            sound_def = sound_event_obj.add_block_event(
                self.identifier,
                sound_reference,
                sound_event,
                volume,
                pitch,
                max_distance,
                min_distance,
                subtitle,
            )
            return sound_def
        elif isinstance(sound_event, BlockInteractiveSoundEvent):
            sound_def = sound_event_obj.add_block_interactive_event(
                self.identifier,
                sound_reference,
                sound_event,
                volume,
                pitch,
                max_distance,
                min_distance,
                subtitle,
            )
            return sound_def
        else:
            raise TypeError("Invalid sound event type.")

    def queue(self) -> "BlockClient":
        """Blocks have no client file, so there is nothing to queue."""
        return self
