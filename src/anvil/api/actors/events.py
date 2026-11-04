"""The events of a server entity: what they add, remove, trigger and run, in sequences and
random picks."""

from typing import Annotated, Any, Self

from anvil.api.core.filters import Filter
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import JsonObject, JsonValue, Keyed, NonNegative, json_field
from anvil.lib.jsonmodel.enums import Vibrations

__all__ = ["_Event"]


# region Parts


class _ComponentGroups(JsonObject):
    """The component groups an event adds or removes."""

    component_groups: list[str] = json_field(default_factory=list)


class _PropertyValue(JsonValue):
    name: str = json_field(exclude=True, positional=True)
    value: bool | int | float | str = json_field(positional=True)


class _QueueCommand(JsonObject):
    command: list[str] = json_field(default_factory=list)


class _EmitVibration(JsonObject):
    vibration: Vibrations = json_field()


class _PlaySound(JsonObject):
    sound: str = json_field()


class _EmitParticle(JsonObject):
    particle: str = json_field()


class _HomeBlockEvent(JsonObject):
    event: str = json_field()


class _Unleash(JsonObject):
    unleash_self: bool | None = None
    unleash_others: bool | None = None


# endregion


class _EventNode(JsonObject, abstract=True):
    """An event, or an entry of a sequence or random pick. Unset keys are left out. Each
    builder returns the node, to chain."""

    add: _ComponentGroups | None = None
    remove: _ComponentGroups | None = None
    trigger: str | None = None
    set_property: Annotated[list[_PropertyValue], Keyed("name")] = json_field(
        default_factory=list, omit_default=True
    )
    queue_command: _QueueCommand | None = None
    emit_vibration: _EmitVibration | None = None
    play_sound: _PlaySound | None = None
    emit_particle: _EmitParticle | None = None
    execute_event_on_home_block: _HomeBlockEvent | None = None
    unleash: _Unleash | None = None

    def add_component_groups(self, component_groups: list[str]) -> Self:
        """Adds component groups to the entity.

        Args:
            component_groups (list[str]): The group names.
        """
        if not isinstance(component_groups, list):
            raise TypeError("Component groups must be provided as a list of strings.")
        if self.add is None:
            self.add = _ComponentGroups()
        self.add.component_groups.extend(component_groups)
        return self

    def remove_component_groups(self, component_groups: list[str]) -> Self:
        """Removes component groups from the entity.

        Args:
            component_groups (list[str]): The group names.
        """
        if not isinstance(component_groups, list):
            raise TypeError("Component groups must be provided as a list of strings.")
        if self.remove is None:
            self.remove = _ComponentGroups()
        self.remove.component_groups.extend(component_groups)
        return self

    def set_trigger(self, event: str) -> Self:
        """Runs another event. One per node; use sequences to run more.

        Args:
            event (str): The event name.
        """
        if self.trigger is not None:
            raise ValueError(
                "An event can only have one trigger. Use sequences instead."
            )
        self.trigger = event
        return self

    def add_property(self, property: str, value: bool | int | float | str) -> Self:
        """Sets an entity property of the project.

        Args:
            property (str): The property name, without namespace.
            value (bool | int | float | str): The value, or Molang.
        """
        name = f"{CONFIG.NAMESPACE}:{property}"
        self.set_property = [p for p in self.set_property if p.name != name]
        self.set_property.append(_PropertyValue(name, value))
        return self

    def add_queue_command(self, commands: list[str]) -> Self:
        """Runs commands on the entity.

        Args:
            commands (list[str]): The commands.
        """
        if not isinstance(commands, list):
            raise TypeError("Commands must be provided as a list of strings.")
        if self.queue_command is None:
            self.queue_command = _QueueCommand()
        self.queue_command.command.extend(str(c) for c in commands)
        return self

    def set_emit_vibration(self, vibration: Vibrations) -> Self:
        """Emits a vibration.

        Args:
            vibration (Vibrations): The vibration.
        """
        self.emit_vibration = _EmitVibration(vibration=vibration)
        return self

    def set_play_sound(self, sound: str) -> Self:
        """Plays a sound from the entity.

        Args:
            sound (str): The sound event.
        """
        self.play_sound = _PlaySound(sound=sound)
        return self

    def set_emit_particle(self, particle: str) -> Self:
        """Emits a particle from the entity.

        Args:
            particle (str): The particle.
        """
        self.emit_particle = _EmitParticle(particle=particle)
        return self

    def set_execute_event_on_home_block(self, event: str) -> Self:
        """Runs an event on the entity's home block.

        Args:
            event (str): The block event.
        """
        self.execute_event_on_home_block = _HomeBlockEvent(event=event)
        return self

    def set_unleash(
        self, unleash_self: bool = False, unleash_others: bool = False
    ) -> Self:
        """Unleashes the entity.

        Args:
            unleash_self (bool, optional): Unleashes the entity from what holds its leash.
                Defaults to False.
            unleash_others (bool, optional): Unleashes the entities the entity holds.
                Defaults to False.
        """
        self.unleash = _Unleash(
            unleash_self=unleash_self or None,
            unleash_others=unleash_others or None,
        )
        return self


class _SequenceEntry(_EventNode):
    """An entry of a sequence: every entry runs, in order, when its filters pass."""

    filters: Filter | None = None
    randomize: list[_RandomizeEntry] = json_field(
        default_factory=list, omit_default=True
    )
    parent: Any = json_field(default=None, exclude=True)

    def set_filters(self, filter: Filter) -> "_SequenceEntry":
        """Runs the entry only when the filter passes.

        Args:
            filter (Filter): The filter.
        """
        self.filters = filter
        return self

    def add_sequence(self) -> "_SequenceEntry":
        """Adds the next entry of the same sequence."""
        return self.parent.add_sequence()

    def add_randomize(self) -> "_RandomizeEntry":
        """Adds a random pick inside this entry, or its next option."""
        entry = _RandomizeEntry(parent=self)
        self.randomize.append(entry)
        return entry


class _RandomizeEntry(_EventNode):
    """An option of a random pick, picked by its weight."""

    weight: Annotated[int, NonNegative] = json_field(default=1)
    sequence: list[_SequenceEntry] = json_field(default_factory=list, omit_default=True)
    parent: Any = json_field(default=None, exclude=True)

    def set_weight(self, weight: int) -> "_RandomizeEntry":
        """Sets how likely the option is, against the other options' weights.

        Args:
            weight (int): The weight.
        """
        self.weight = weight
        return self

    def add_randomize(self) -> "_RandomizeEntry":
        """Adds the next option of the same random pick."""
        return self.parent.add_randomize()

    def add_sequence(self) -> _SequenceEntry:
        """Adds a sequence inside this option, or its next entry."""
        entry = _SequenceEntry(parent=self)
        self.sequence.append(entry)
        return entry


class _Event(_EventNode):
    """An entity event: component groups it adds and removes, and what else it runs. It
    has a sequence or a random pick, not both."""

    name: str = json_field(exclude=True, positional=True)
    sequence: list[_SequenceEntry] = json_field(default_factory=list, omit_default=True)
    randomize: list[_RandomizeEntry] = json_field(
        default_factory=list, omit_default=True
    )

    def add_sequence(self) -> _SequenceEntry:
        """Adds an entry to the event's sequence."""
        entry = _SequenceEntry(parent=self)
        self.sequence.append(entry)
        return entry

    def add_randomize(self) -> _RandomizeEntry:
        """Adds an option to the event's random pick."""
        entry = _RandomizeEntry(parent=self)
        self.randomize.append(entry)
        return entry

    def __validate__(self) -> None:
        if self.sequence and self.randomize:
            raise ValueError(
                "Sequences and Randomizes cannot coexist in the same event."
            )
