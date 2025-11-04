from anvil.api.actors.components import Filter
from anvil.lib.config import CONFIG
from anvil.lib.enums import Vibrations
from anvil.lib.types import Event


class _BaseEvent:
    def __init__(self, event_name: Event):
        self._event_name = event_name
        self._event = {
            self._event_name: {
                "add": {"component_groups": []},
                "remove": {"component_groups": []},
                "queue_command": {"command": []},
                "set_property": {},
                "emit_vibration": {},
            }
        }

    def add(self, *component_groups: str):
        self._event[self._event_name]["add"]["component_groups"].extend(
            component_groups
        )
        return self

    def remove(self, *component_groups: str):
        self._event[self._event_name]["remove"]["component_groups"].extend(
            component_groups
        )
        return self

    def trigger(self, event: Event):
        self._event[self._event_name]["trigger"] = event
        return self

    def set_property(self, property, value):
        self._event[self._event_name]["set_property"].update(
            {f"{CONFIG.NAMESPACE}:{property}": value}
        )
        return self

    def queue_command(self, *commands: str):
        self._event[self._event_name]["queue_command"]["command"].extend(
            str(cmd) for cmd in commands
        )
        return self

    def emit_vibration(self, vibration: Vibrations):
        self._event[self._event_name]["vibration"] = vibration
        return self

    def play_sound(self, sound: str):
        self._event[self._event_name]["play_sound"] = {"sound": sound}
        return self

    def emit_particle(self, particle: str):
        self._event[self._event_name]["emit_particle"] = {"particle": particle}
        return self

    @property
    def _export(self):
        return self._event


class _Randomize(_BaseEvent):
    def __init__(self, parent):
        self._event = {"weight": 1, "set_property": {}}
        self._sequences: list[_Sequence] = []
        self._parent_class: _Event = parent

    def add(self, *component_groups):
        self._event.update({"add": {"component_groups": [*component_groups]}})
        return self

    def remove(self, *component_groups):
        self._event.update({"remove": {"component_groups": [*component_groups]}})
        return self

    def trigger(self, event: Event):
        self._event.update({"trigger": event})
        return self

    def weight(self, weight: int):
        self._event.update({"weight": weight})
        return self

    def set_property(self, property, value):
        self._event["set_property"].update({f"{CONFIG.NAMESPACE}:{property}": value})
        return self

    def queue_command(self, *commands: str):
        self._event.update(
            {"queue_command": {"command": [str(cmd) for cmd in commands]}}
        )
        return self

    def emit_vibration(self, vibration: Vibrations):
        self._event.update({"vibration": vibration})
        return self

    def play_sound(self, sound: str):
        self._event[self._event_name]["play_sound"] = {"sound": sound}
        return self

    def emit_particle(self, particle: str):
        self._event[self._event_name]["emit_particle"] = {"particle": particle}
        return self

    @property
    def randomize(self):
        return self._parent_class.randomize

    @property
    def sequence(self):
        sequence = _Sequence(self)
        self._sequences.append(sequence)
        return sequence

    @property
    def _export(self):
        if len(self._sequences) > 0:
            self._event.update({"sequence": []})
            for sequence in self._sequences:
                self._event["sequence"].append(sequence._export)
        return self._event


class _Sequence(_BaseEvent):
    def __init__(self, parent_event) -> None:
        self._randomizes: list[_Randomize] = []
        self._parent_class: _Event = parent_event
        self._event = {"set_property": {}}

    def add(self, *component_groups):
        self._event.update({"add": {"component_groups": [*component_groups]}})
        return self

    def remove(self, *component_groups):
        self._event.update({"remove": {"component_groups": [*component_groups]}})
        return self

    def trigger(self, event: Event):
        self._event.update({"trigger": event})
        return self

    def filters(self, filter: Filter):
        self._event.update({"filters": filter})
        return self

    def set_property(self, property, value):
        self._event["set_property"].update({f"{CONFIG.NAMESPACE}:{property}": value})
        return self

    def queue_command(self, *commands: str):
        self._event.update(
            {"queue_command": {"command": [str(cmd) for cmd in commands]}}
        )
        return self

    def emit_vibration(self, vibration: Vibrations):
        self._event.update({"vibration": vibration})
        return self

    def play_sound(self, sound: str):
        self._event[self._event_name]["play_sound"] = {"sound": sound}
        return self

    def emit_particle(self, particle: str):
        self._event[self._event_name]["emit_particle"] = {"particle": particle}
        return self

    @property
    def sequence(self):
        return self._parent_class.sequence

    @property
    def randomize(self):
        randomize = _Randomize(self)
        self._randomizes.append(randomize)
        return randomize

    @property
    def _export(self):
        if len(self._randomizes) > 0:
            self._event.update({"randomize": []})
            for randomize in self._randomizes:
                self._event["randomize"].append(randomize._export)
        return self._event


class _Event(_BaseEvent):
    def __init__(self, event_name: Event):
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

    @property
    def _export(self):
        if len(self._sequences) > 0 and len(self._randomizes) > 0:
            raise SyntaxError(
                "Sequences and Randomizes cannot coexist in the same event."
            )
        if len(self._sequences) > 0:
            self._event[self._event_name].update({"sequence": []})
            for sequence in self._sequences:
                self._event[self._event_name]["sequence"].append(sequence._export)
        if len(self._randomizes) > 0:
            self._event[self._event_name].update({"randomize": []})
            for randomize in self._randomizes:
                self._event[self._event_name]["randomize"].append(randomize._export)
        return super()._export
