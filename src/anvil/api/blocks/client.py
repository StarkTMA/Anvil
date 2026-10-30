from anvil.api.core.core import BlocksJSONObject, SoundEvent
from anvil.api.core.enums import (
    BlockInteractiveSoundEvent,
    BlockSoundEvent,
    BlockSoundGroup,
)
from anvil.lib.schemas import AddonObject

__all__ = ["BlockClient"]


class BlockClient(AddonObject):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        super().__init__(name, is_vanilla)

    def sound_group(self, group: BlockSoundGroup | str) -> "BlockClient":
        """Gives the block the sounds of a vanilla sound group, like oak planks have the `wood`
        group's: breaking, placing, walking, and the clicks of doors, buttons and plates. It
        needs no sound files. To make your own sounds for the block, use `block_sound`.

        Parameters:
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
        max_distance: float = 0,
        min_distance: float = 9999,
        subtitle: str = None,
    ):
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
        return self
