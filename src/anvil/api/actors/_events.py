from anvil.api.actors.components import Filter
from anvil.api.core.enums import Vibrations
from anvil.lib.config import CONFIG


class _BaseEvent:
    def __init__(self, event_name: str):
        self._event_name = event_name
        self._event = {}

    def add(self, component_groups: list[str]):
        if not isinstance(component_groups, list):
            raise TypeError("Component groups must be provided as a list of strings.")
        self._event.setdefault("add", {"component_groups": []})[
            "component_groups"
        ].extend(component_groups)
        return self

    def remove(self, component_groups: list[str]):
        if not isinstance(component_groups, list):
            raise TypeError("Component groups must be provided as a list of strings.")
        self._event.setdefault("remove", {"component_groups": []})[
            "component_groups"
        ].extend(component_groups)
        return self

    def trigger(self, event: str):
        if "trigger" in self._event:
            raise SyntaxError(
                "An event can only have one trigger. Use sequences instead."
            )
        self._event["trigger"] = event
        return self

    def set_property(self, property, value):
        self._event.setdefault("set_property", {})[
            f"{CONFIG.NAMESPACE}:{property}"
        ] = value
        return self

    def queue_command(self, commands: list[str]):
        if not isinstance(commands, list):
            raise TypeError("Commands must be provided as a list of strings.")
        self._event.setdefault("queue_command", {"command": []})["command"].extend(
            str(cmd) for cmd in commands
        )
        return self

    def emit_vibration(self, vibration: Vibrations):
        self._event["vibration"] = vibration
        return self

    def play_sound(self, sound: str):
        self._event["play_sound"] = {"sound": sound}
        return self

    def emit_particle(self, particle: str):
        self._event["emit_particle"] = {"particle": particle}
        return self

    def execute_event_on_home_block(self, event: str):
        self._event["execute_event_on_home_block"] = {"event": event}
        return self

    def unleash(self, unleash_self: bool = False, unleash_others: bool = False):
        """Unleashes the entity.

        Parameters:
            unleash_self (bool, optional): If true, unleashes the entity from the entity it is leashed to. Defaults to False.
            unleash_others (bool, optional): If true, unleashes all entities that are leashed to the entity. Defaults to False.
        """
        payload = {}
        if unleash_self:
            payload["unleash_self"] = unleash_self
        if unleash_others:
            payload["unleash_others"] = unleash_others
        self._event["unleash"] = payload
        return self

    def __export__(self):
        return {self._event_name: self._event}


class _Randomize(_BaseEvent):
    def __init__(self, parent):
        self._event = {"weight": 1}
        self._sequences: list["_Sequence"] = []
        self._parent_class: "_Event" = parent

    def weight(self, weight: int):
        self._event["weight"] = weight
        return self

    @property
    def randomize(self):
        return self._parent_class.randomize

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    def __export__(self):
        if self._sequences:
            self._event["sequence"] = [s.__export__() for s in self._sequences]
        return self._event


class _Sequence(_BaseEvent):
    def __init__(self, parent_event) -> None:
        self._event = {}
        self._randomizes: list[_Randomize] = []
        self._parent_class: "_Event" = parent_event

    def filters(self, filter: Filter):
        self._event["filters"] = filter
        return self

    @property
    def sequence(self):
        return self._parent_class.sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    def __export__(self):
        if self._randomizes:
            self._event["randomize"] = [r.__export__() for r in self._randomizes]
        return self._event


class _Event(_BaseEvent):
    def __init__(self, event_name: str):
        super().__init__(event_name)
        self._sequences: list[_Sequence] = []
        self._randomizes: list[_Randomize] = []

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    def __export__(self):
        if self._sequences and self._randomizes:
            raise SyntaxError(
                "Sequences and Randomizes cannot coexist in the same event."
            )
        if self._sequences:
            self._event["sequence"] = [s.__export__() for s in self._sequences]
        if self._randomizes:
            self._event["randomize"] = [r.__export__() for r in self._randomizes]
        return super().__export__()
