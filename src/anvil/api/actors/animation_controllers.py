"""The animation controllers of an actor: `animation_controllers/<actor>.bp_ac.json` in the
behavior pack and `animation_controllers/<actor>.rp_ac.json` in the resource pack. A
controller is a state machine; each state runs animations and Molang, and moves to another
state when a condition is true."""

from typing import TYPE_CHECKING, Annotated, Any, ClassVar, Self, overload

from anvil.api.actors.animations import _bp_command
from anvil.api.logic.molang import Molang
from anvil.lib.config import Pack
from anvil.lib.format_versions import ANIMATION_CONTROLLERS_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    JsonFile,
    JsonObject,
    JsonValue,
    Keyed,
    NonNegative,
    json_field,
)

if TYPE_CHECKING:
    from anvil.api.actors.client import _ActorClientDescription
    from anvil.api.actors.server import _EntityServerDescription

__all__ = ["BPAnimationControllers", "RPAnimationControllers"]


# region States


class _Named(JsonValue):
    """A name and an optional value, written as `name` or `{name: value}`."""

    name: str = json_field(positional=True)
    value: str | bool | None = json_field(default=None, exclude=True, positional=True)

    def __json__(self) -> Any:
        if self.value is None:
            return self.name
        return {self.name: self.value}

    @classmethod
    def __schema_body__(cls, definitions: dict[str, Any]) -> dict[str, Any]:
        return {
            "anyOf": [
                {"type": "string"},
                {
                    "type": "object",
                    "minProperties": 1,
                    "maxProperties": 1,
                    "additionalProperties": {"type": ["string", "boolean"]},
                },
            ]
        }


class _ActorScripts(JsonObject):
    """The `scripts` of an actor description: the animations and controllers it always
    runs. The client scripts add their own keys."""

    animate: list[_Named] = json_field(default_factory=list)

    def add_animate(self, name: str, condition: str | Molang | None = None) -> Self:
        """Runs an animation or controller all the time, or while a condition is true.
        The same name and condition are added once.

        Args:
            name (str): The short name in the description's `animations`.
            condition (str | Molang, optional): When it runs.
        """
        condition = None if condition is None else str(condition)
        if not any(e.name == name and e.value == condition for e in self.animate):
            self.animate.append(_Named(name, condition))
        return self


class _StateEffect(JsonObject):
    """A particle or sound effect a state plays, by its short name in the client
    description. Unset keys are left out."""

    effect: str = json_field()
    locator: str | None = None
    pre_effect_script: str | None = None
    bind_to_actor: bool | None = None


class _ControllerState(JsonObject, abstract=True):
    """The parts of a state shared by both packs. Unset keys are left out; a state with
    nothing set is not written."""

    name: str = json_field(exclude=True, positional=True)

    on_entry: list[str] | None = None
    on_exit: list[str] | None = None
    animations: list[_Named] | None = None
    transitions: list[_Named] | None = None

    def _is_empty(self) -> bool:
        return not self.__json__()

    def animation(
        self, animation: str, condition: str | None = None
    ) -> "_ControllerState":
        """Plays an animation or controller of the actor during this state.

        Args:
            animation (str): Its short name.
            condition (str, optional): When it plays, Molang. Its value blends the
                animation in the resource pack.
        """
        self.animations = (self.animations or []) + [
            _Named(animation, None if condition is None else str(condition))
        ]
        return self

    def transition(self, state: str, condition: str) -> "_ControllerState":
        """Moves to another state when a condition is true.

        Args:
            state (str): The state's name.
            condition (str): When to move, Molang.
        """
        self.transitions = (self.transitions or []) + [_Named(state, str(condition))]
        return self


class _BPControllerState(_ControllerState):
    """A state of a behavior pack animation controller."""

    def add_on_entry(self, *commands: str) -> "_BPControllerState":
        """Runs commands, events (`@s <event>`) or Molang when the state starts."""
        self.on_entry = (self.on_entry or []) + [_bp_command(str(c)) for c in commands]
        return self

    def add_on_exit(self, *commands: str) -> "_BPControllerState":
        """Runs commands, events (`@s <event>`) or Molang when the state ends."""
        self.on_exit = (self.on_exit or []) + [_bp_command(str(c)) for c in commands]
        return self


def _rp_molang(args: tuple, state: str) -> list[str]:
    if len(args) == 2:
        commands = [f"{args[0]}={args[1]}"]
    else:
        commands = [str(command) for command in args]
    for command in commands:
        if not any(command.startswith(prefix) for prefix in Molang.prefixes):
            raise ValueError(
                f"Invalid command '{command}'. Only Molang is allowed. Resource Pack "
                f"Controller State [{state}]"
            )
    return [f"{command};" for command in commands]


class _RPControllerState(_ControllerState):
    """A state of a resource pack animation controller."""

    particle_effects: list[_StateEffect] | None = None
    sound_effects: list[_StateEffect] | None = None
    blend_transition: Annotated[float, NonNegative] | None = None
    blend_via_shortest_path: bool | None = None

    @overload
    def add_on_entry(self, *commands: str | Molang) -> "_RPControllerState": ...

    @overload
    def add_on_entry(
        self, variable: Molang | str, value: Molang | str | int | float
    ) -> "_RPControllerState": ...

    def add_on_entry(self, *args) -> "_RPControllerState":
        """Runs Molang when the state starts: expressions, or a variable and its value."""
        self.on_entry = (self.on_entry or []) + _rp_molang(args, self.name)
        return self

    @overload
    def add_on_exit(self, *commands: str | Molang) -> "_RPControllerState": ...

    @overload
    def add_on_exit(
        self, variable: Molang | str, value: Molang | str | int | float
    ) -> "_RPControllerState": ...

    def add_on_exit(self, *args) -> "_RPControllerState":
        """Runs Molang when the state ends: expressions, or a variable and its value."""
        self.on_exit = (self.on_exit or []) + _rp_molang(args, self.name)
        return self

    def particle(
        self,
        effect: str,
        locator: str = "root",
        pre_anim_script: str | None = None,
        bind_to_actor: bool = True,
    ) -> "_RPControllerState":
        """Emits a particle effect during this state.

        Args:
            effect (str): The effect's short name in the client description.
            locator (str, optional): The locator it plays at. Defaults to `root`.
            pre_anim_script (str, optional): Molang run when the emitter starts.
            bind_to_actor (bool, optional): False leaves the effect in the world instead of
                following the actor. Defaults to True.
        """
        script = None
        if pre_anim_script is not None:
            script = f"{pre_anim_script};".replace(";;", ";")
        self.particle_effects = (self.particle_effects or []) + [
            _StateEffect(
                effect=effect,
                locator=locator,
                pre_effect_script=script,
                bind_to_actor=None if bind_to_actor else False,
            )
        ]
        return self

    def sound_effect(self, effect: str, locator: str = "root") -> "_RPControllerState":
        """Plays a sound effect when the state starts.

        Args:
            effect (str): The effect's short name in the client description.
            locator (str, optional): The locator it plays at. Defaults to `root`.
        """
        self.sound_effects = (self.sound_effects or []) + [
            _StateEffect(effect=effect, locator=locator)
        ]
        return self

    def set_blend_transition(self, blend_value: float) -> "_RPControllerState":
        """Sets how long, in seconds, the state's animations fade out when it moves on."""
        self.blend_transition = blend_value
        return self

    def set_blend_via_shortest_path(self, value: bool = True) -> "_RPControllerState":
        """Blends each rotation axis through the shortest way when moving on."""
        self.blend_via_shortest_path = value
        return self


# endregion


# region Controllers


class _AnimationController(JsonObject, abstract=True):
    """An animation controller, `controller.animation.<namespace>.<actor>.<name>`. The
    actor's description lists it by its short name; a controller whose states are all empty
    is not written.
    """

    _state: ClassVar[type[_ControllerState]]
    _side: ClassVar[str]

    name: str = json_field(exclude=True, positional=True)
    owner: Identifier = json_field(exclude=True)
    """The actor identifier."""
    animate: bool = json_field(default=False, exclude=True)
    """Runs all the time, or while `condition` is true."""
    condition: str | None = json_field(default=None, exclude=True)

    initial_state: str = "default"
    states: Annotated[list[_ControllerState], Keyed("name")] = json_field(
        default_factory=list
    )

    @property
    def identifier(self) -> str:
        """The controller's identifier, `controller.animation.<namespace>.<actor>.<name>`."""
        return f"controller.animation.{self.owner.replace(':', '.')}.{self.name}"

    def add_state(self, state_name: str) -> Any:
        """Returns the state with this name, added on first use.

        Args:
            state_name (str): The state's name.
        """
        for state in self.states:
            if state.name == state_name:
                return state
        state = self._state(state_name)
        self.states.append(state)
        return state

    def _is_empty(self) -> bool:
        return all(state._is_empty() for state in self.states)

    def _set_animate(self, condition: str | Molang | None = None) -> None:
        """Runs it all the time, or while the condition is true."""
        self.animate = True
        self.condition = None if condition is None else str(condition)

    def __validate__(self) -> None:
        names = {state.name for state in self.states}
        for state in self.states:
            for transition in state.transitions or []:
                if transition.name not in names:
                    raise ValueError(
                        f"State '{transition.name}' is referenced in transitions but not "
                        f"defined. {self._side} Animation Controller [{self.identifier}]."
                    )


class _BPAnimationController(_AnimationController):
    """A behavior pack animation controller."""

    _state = _BPControllerState
    _side = "Behavior Pack"

    states: Annotated[list[_BPControllerState], Keyed("name")] = json_field(
        default_factory=list
    )

    def add_state(self, state_name: str) -> _BPControllerState:
        """Returns the state with this name, added on first use.

        Args:
            state_name (str): The state's name.
        """
        return super().add_state(state_name)


class _RPAnimationController(_AnimationController):
    """A resource pack animation controller."""

    _state = _RPControllerState
    _side = "Resource Pack"

    states: Annotated[list[_RPControllerState], Keyed("name")] = json_field(
        default_factory=list
    )

    def add_state(self, state_name: str) -> _RPControllerState:
        """Returns the state with this name, added on first use.

        Args:
            state_name (str): The state's name.
        """
        return super().add_state(state_name)


# endregion


# region Files


class _AnimationControllersFile(JsonObject, abstract=True):
    """The content of an animation controllers file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "animation_controllers",
    )

    format_version: str = json_field(default=ANIMATION_CONTROLLERS_VERSION, init=False)


class _BPAnimationControllersFile(_AnimationControllersFile):
    """The content of a `.bp_ac.json` file."""

    animation_controllers: Annotated[
        list[_BPAnimationController], Keyed("identifier")
    ] = json_field(default_factory=list)


class _RPAnimationControllersFile(_AnimationControllersFile):
    """The content of a `.rp_ac.json` file."""

    animation_controllers: Annotated[
        list[_RPAnimationController], Keyed("identifier")
    ] = json_field(default_factory=list)


class _AnimationControllers[D: JsonObject](JsonFile[D]):
    """The base of the animation controllers files of an actor, built at export from its
    description, which holds the controllers (`animation_controller()` adds them)."""

    _source: "_EntityServerDescription | _ActorClientDescription"

    def queue(self, directory: str | None = None):
        """Queues the controllers for export, when the actor has any."""
        self._document = self._document_type(
            animation_controllers=[
                e
                for e in self._source._animations
                if isinstance(e, _AnimationController)
            ]
        )
        if self._document.animation_controllers:
            return super().queue(directory=directory)
        return None


class BPAnimationControllers(_AnimationControllers[_BPAnimationControllersFile]):
    """The behavior pack animation controllers of an entity.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/animations/animationcontroller)
    """

    _extension = ".bp_ac.json"
    _pack = Pack.BP
    _folder = "animation_controllers"
    _object_type = "Behavior Pack Animation Controller"

    def __init__(self, source: "_EntityServerDescription") -> None:
        """Creates the behavior pack animation controllers file of an entity, at export.

        Args:
            source (_EntityServerDescription): The entity's description, which holds the
                controllers.
        """
        super().__init__(source.identifier, source.identifier.is_vanilla)
        self._source = source


class RPAnimationControllers(_AnimationControllers[_RPAnimationControllersFile]):
    """The resource pack animation controllers of an entity or attachable.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/animations/animationcontroller)
    """

    _extension = ".rp_ac.json"
    _pack = Pack.RP
    _folder = "animation_controllers"
    _object_type = "Resource Pack Animation Controller"

    def __init__(self, source: "_ActorClientDescription") -> None:
        """Creates the resource pack animation controllers file of an actor, at export.

        Args:
            source (_ActorClientDescription): The actor's client description, which holds the
                controllers.
        """
        super().__init__(source.name)
        self._source = source


# endregion
