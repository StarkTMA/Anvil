"""The behavior pack's `animations/<entity>.animation.json`: timelines of commands, events
and Molang an entity runs."""

from typing import TYPE_CHECKING, Annotated, ClassVar

from anvil.api.logic.molang import Molang
from anvil.lib.config import Pack
from anvil.lib.format_versions import BP_ANIMATION_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    JsonFile,
    JsonObject,
    JsonValue,
    Keyed,
    NonNegative,
    json_field,
)
from anvil.lib.jsonmodel.enums import Target

if TYPE_CHECKING:
    from anvil.api.actors.server import _EntityServerDescription


# region Parts


def _bp_command(command: str) -> str:
    """A behavior pack command as written: an `@s` event as is, Molang ending with `;`, and
    a slash command starting with `/`."""
    if not isinstance(command, str):
        raise TypeError(f"Expected a command, event or Molang string. [{command}]")
    if command.startswith(Target.S.value):
        return command
    if any(command.startswith(prefix) for prefix in Molang.prefixes):
        return f"{command};"
    return f"/{command}"


class _BPTimelineEntry(JsonValue):
    """What an animation runs at one time."""

    time: float = json_field(exclude=True, positional=True)
    commands: list[str] = json_field(default_factory=list)


class _BPAnimation(JsonObject):
    """A behavior pack animation, `animation.<namespace>.<entity>.<name>`: commands, events
    and Molang run along a timeline. The entity's description lists it by its short name.
    Unset keys are left out.
    """

    name: str = json_field(exclude=True, positional=True)
    owner: Identifier = json_field(exclude=True)
    """The entity identifier."""
    animate: bool = json_field(default=False, exclude=True)
    """Runs all the time, or while `condition` is true."""
    condition: str | None = json_field(default=None, exclude=True)

    loop: bool = False
    animation_length: Annotated[float, NonNegative] | None = None
    anim_time_update: str | None = None
    timeline: Annotated[list[_BPTimelineEntry], Keyed("time")] = json_field(
        default_factory=list
    )

    @property
    def identifier(self) -> str:
        """The animation's identifier, `animation.<namespace>.<entity>.<name>`."""
        return f"animation.{self.owner.replace(':', '.')}.{self.name}"

    def _set_animate(self, condition: str | Molang | None = None) -> None:
        """Runs it all the time, or while the condition is true."""
        self.animate = True
        self.condition = None if condition is None else str(condition)

    def add_timeline(self, timestamp: float, commands: list[str]) -> "_BPAnimation":
        """Runs commands, events (`@s <event>`) or Molang at a time. Makes the animation
        last until just after it, at least 0.05 seconds, unless it already lasts longer.

        Args:
            timestamp (float): The time, in seconds.
            commands (list[str]): What runs.
        """
        if not isinstance(commands, list):
            raise TypeError("Animation timeline expected a list of strings.")
        length = 0.05 if self.animation_length is None else self.animation_length
        self.animation_length = timestamp + 0.05 if length <= timestamp else length
        entry = next((e for e in self.timeline if e.time == timestamp), None)
        if entry is None:
            entry = _BPTimelineEntry(timestamp)
            self.timeline.append(entry)
        entry.commands.extend(_bp_command(command) for command in commands)
        return self

    def set_animation_length(self, animation_length: float) -> "_BPAnimation":
        """Sets how long the animation lasts, in seconds."""
        self.animation_length = animation_length
        return self

    def set_anim_time_update(self, anim_time_update: str) -> "_BPAnimation":
        """Sets how the animation time moves each frame, Molang."""
        self.anim_time_update = anim_time_update
        return self


# endregion


# region File


class _BPAnimationsFile(JsonObject):
    """The content of a behavior pack `.animation.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "animations")

    format_version: str = json_field(default=BP_ANIMATION_VERSION, init=False)
    animations: Annotated[list[_BPAnimation], Keyed("identifier")] = json_field(
        default_factory=list
    )


class BPAnimations(JsonFile):
    """The behavior pack animations of an entity, written when it has any. The entity's
    description holds them (`entity.server.description.animation()` adds them); the
    file writes them.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/animations/animationsoverview)
    """

    _document = _BPAnimationsFile
    _extension = ".animation.json"
    _pack = Pack.BP
    _folder = "animations"
    _object_type = "Behavior Pack Animation"

    def __init__(self, source: "_EntityServerDescription") -> None:
        """Creates the animations file of an entity.

        Args:
            source (_EntityServerDescription): The entity's description, which holds the
                animations.
        """
        super().__init__(source.identifier, source.identifier.is_vanilla)
        self._source = source

    def queue(self, directory: str | None = None) -> "BPAnimations | None":
        """Queues the animations for export, when the entity has any."""
        self._content = self._document(
            animations=[
                e for e in self._source._animations if isinstance(e, _BPAnimation)
            ]
        )
        if self._content.animations:
            return super().queue(directory=directory)
        return None


# endregion
