"""JSON UI animations: `_UIAnimationElement` and the animation file that holds them.

[Bedrock Wiki](https://wiki.bedrock.dev/json-ui/json-ui-documentation#animations)
"""

from pathlib import PurePosixPath
from typing import Annotated, Any, ClassVar, Self

from anvil.api.core.types import JsonSchema
from anvil.api.ui.elements import _REFERENCE, _keyed_schema, _merged_keys
from anvil.api.ui.enums import UIAnimType, UIEasing
from anvil.api.ui.files import _UIDefs
from anvil.lib.config import Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject, Keyed, json_field


class _UIAnimationElement(JsonObject):
    """A JSON UI animation, added with the animation file's `add_animation()`. Refer to it as
    `@namespace.name`.

    Args:
        name (str): The animation name.
    """

    name: str = json_field(exclude=True, positional=True)
    anim_type: UIAnimType | Annotated[str, _REFERENCE] | None = json_field(default=None)
    duration: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    next: str | None = json_field(default=None)
    destroy_at_end: str | None = json_field(default=None)
    play_event: str | None = json_field(default=None)
    end_event: str | None = json_field(default=None)
    start_event: str | None = json_field(default=None)
    reset_event: str | None = json_field(default=None)
    easing: UIEasing | Annotated[str, _REFERENCE] | None = json_field(default=None)
    from_: float | tuple[float | str, ...] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None, key="from")
    )
    to: float | tuple[float | str, ...] | Annotated[str, _REFERENCE] | None = (
        json_field(default=None)
    )
    initial_uv: tuple[float, float] | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    fps: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    frame_count: int | Annotated[str, _REFERENCE] | None = json_field(default=None)
    frame_step: float | Annotated[str, _REFERENCE] | None = json_field(default=None)
    reversible: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    resettable: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)
    scale_from_starting_alpha: bool | Annotated[str, _REFERENCE] | None = json_field(
        default=None
    )
    activated: bool | Annotated[str, _REFERENCE] | None = json_field(default=None)

    def __str__(self) -> str:
        return self.name

    def set_anim_type(self, anim_type: UIAnimType | str) -> Self:
        """Sets the property the animation changes.

        Args:
            anim_type (UIAnimType | str): The animation type, or a `$variable`.
        """
        self.anim_type = anim_type
        return self

    def set_duration(self, duration: float | str) -> Self:
        """Sets how many seconds the animation takes.

        Args:
            duration (float | str): The seconds, or a `$variable`.
        """
        self.duration = duration
        return self

    def set_next(self, next: str) -> Self:
        """Sets the animation that plays when this one ends.

        Args:
            next (str): The animation, as `@namespace.name`.
        """
        self.next = next
        return self

    def set_destroy_at_end(self, destroy_at_end: str) -> Self:
        """Sets the element destroyed when the animation ends.

        Args:
            destroy_at_end (str): The element name.
        """
        self.destroy_at_end = destroy_at_end
        return self

    def set_play_event(self, play_event: str) -> Self:
        """Sets the event that plays the animation.

        Args:
            play_event (str): The event.
        """
        self.play_event = play_event
        return self

    def set_end_event(self, end_event: str) -> Self:
        """Sets the event fired when the animation ends.

        Args:
            end_event (str): The event.
        """
        self.end_event = end_event
        return self

    def set_start_event(self, start_event: str) -> Self:
        """Sets the event fired when the animation starts.

        Args:
            start_event (str): The event.
        """
        self.start_event = start_event
        return self

    def set_reset_event(self, reset_event: str) -> Self:
        """Sets the event that resets the animation.

        Args:
            reset_event (str): The event.
        """
        self.reset_event = reset_event
        return self

    def set_easing(self, easing: UIEasing | str) -> Self:
        """Sets the easing of the animation.

        Args:
            easing (UIEasing | str): The easing, or a `$variable`.
        """
        self.easing = easing
        return self

    def set_from(self, from_: float | tuple[float | str, ...] | str) -> Self:
        """Sets the value the animation starts from, written as `from`.

        Args:
            from_ (float | tuple[float | str, ...] | str): A number, a vector, or a `$variable`.
        """
        self.from_ = from_
        return self

    def set_to(self, to: float | tuple[float | str, ...] | str) -> Self:
        """Sets the value the animation ends at.

        Args:
            to (float | tuple[float | str, ...] | str): A number, a vector, or a `$variable`.
        """
        self.to = to
        return self

    def set_initial_uv(self, initial_uv: tuple[float, float] | str = (0, 0)) -> Self:
        """Sets the first UV of a flip book.

        Args:
            initial_uv (tuple[float, float] | str): The UV, or a `$variable`.
        """
        self.initial_uv = initial_uv
        return self

    def set_fps(self, fps: int | str) -> Self:
        """Sets the frames per second of a flip book.

        Args:
            fps (int | str): The frames per second, or a `$variable`.
        """
        self.fps = fps
        return self

    def set_frame_count(self, frame_count: int | str) -> Self:
        """Sets the frames of a flip book.

        Args:
            frame_count (int | str): The frame count, or a `$variable`.
        """
        self.frame_count = frame_count
        return self

    def set_frame_step(self, frame_step: float | str) -> Self:
        """Sets the UV step between the frames of a flip book.

        Args:
            frame_step (float | str): The step, or a `$variable`.
        """
        self.frame_step = frame_step
        return self

    def set_reversible(self, reversible: bool | str = True) -> Self:
        """Sets whether the animation runs in reverse after it completes.

        Args:
            reversible (bool | str): The value, or a `$variable`.
        """
        self.reversible = reversible
        return self

    def set_resettable(self, resettable: bool | str = True) -> Self:
        """Sets whether the animation can be reset.

        Args:
            resettable (bool | str): The value, or a `$variable`.
        """
        self.resettable = resettable
        return self

    def set_scale_from_starting_alpha(
        self, scale_from_starting_alpha: bool | str = True
    ) -> Self:
        """Sets `scale_from_starting_alpha`.

        Args:
            scale_from_starting_alpha (bool | str): The value, or a `$variable`.
        """
        self.scale_from_starting_alpha = scale_from_starting_alpha
        return self

    def set_activated(self, activated: bool | str = True) -> Self:
        """Sets whether the animation starts activated.

        Args:
            activated (bool | str): The value, or a `$variable`.
        """
        self.activated = activated
        return self


class _UIAnimationFile(JsonObject):
    """The content of a UI animation file: a namespace and its animations by name."""

    __required__: ClassVar[tuple[str, ...]] = ("namespace",)

    namespace: str | None = json_field(default=None)
    animations: Annotated[list[_UIAnimationElement], Keyed("name")] = json_field(
        default_factory=list, init=False, omit_default=True
    )

    def set_namespace(self, namespace: str) -> None:
        """Sets the namespace other files refer to this file's entries by."""
        self.namespace = namespace

    def __validate__(self) -> None:
        if self.namespace is None:
            raise ValueError("A UI file needs a namespace.")

    def __json__(self) -> Any:
        return _merged_keys(JsonObject.__json__(self), "animations")

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return _keyed_schema(
            schema,
            "animations",
            r"^(?!namespace$)",
            {"$ref": "#/$defs/_UIAnimationElement"},
        )


class _UIAnimation(JsonFile):
    """A UI animation file, whose animations elements refer to as `@namespace.name`.

    [Bedrock Wiki](https://wiki.bedrock.dev/json-ui/json-ui-documentation#animations)
    """

    _document = _UIAnimationFile
    _extension = ".json"
    _pack = Pack.RP
    _folder = "ui"
    _object_type = "UI Animation"

    def __init__(self, name: str, namespace: str, defs: _UIDefs) -> None:
        """Initialize the animation manager.

        Args:
            name (str): Name of the animation file
            namespace (str): Namespace for the animations
            defs (_UIDefs): UI definitions manager to register with
        """
        super().__init__(name)
        self._defs = defs
        self._content.set_namespace(namespace)

    def add_animation(self, animation_name: str) -> _UIAnimationElement:
        """Adds an animation and returns it.

        Args:
            animation_name (str): Name of the animation
        """
        animation = _UIAnimationElement(animation_name)
        self._content.animations.append(animation)
        return animation

    def queue(self, directory: str = "") -> "_UIAnimation":
        """Queues the animation file and adds it to the UI definitions.

        Args:
            directory (str, optional): Subdirectory for the file. Defaults to "".
        """
        self._defs.add_file(
            PurePosixPath("ui", directory, f"{self.name}{self._extension}").as_posix()
        )
        return super().queue(directory)


class _AnvilAnimations(_UIAnimation):
    def __init__(self, defs: _UIDefs) -> None:
        super().__init__("animations", "anvil_animations", defs)

    def queue(self) -> "_AnvilAnimations":
        return super().queue("anvil")
