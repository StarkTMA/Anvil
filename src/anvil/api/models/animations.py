"""Builders for Bedrock animation files (``*.animations.json``).

An :class:`Animations` is one animations file holding any number of
:class:`_Animation` objects. An animation hands out :class:`_AnimBone` objects
by bone name, and each keyframe call returns the same bone so keyframes chain.

Example:
    ```python
    anims = Animations("my_mob")

    walk = anims.animation("walk", length=1.0, loop=True)
    walk.bone("arm").add_rotation(0.0, [0, 0, 0]).add_rotation(
        0.5, [0, 30, 0]
    ).add_rotation(1.0, [0, 0, 0])
    walk.bone("body").add_position(0.5, [0, 1, 0], pre=[0, 0, 0])
    walk.particle(0.25, "minecraft:dust", locator="foot")
    walk.sound(0.25, "step")
    walk.add_timeline(0.5, "v.step = 1;")

    anims.queue()
    ```

## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/schemasreference/schemas/minecraftschema_actor_animation_1.8.0)
"""

from typing import Annotated, Any, ClassVar, Literal, Sequence

from anvil.api.core.types import JsonSchema
from anvil.api.models.geometry import Geometry
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import RP_ANIMATION_VERSION
from anvil.lib.jsonmodel import (
    Encoded,
    JsonFile,
    JsonObject,
    JsonValue,
    Keyed,
    NonNegative,
    json_field,
)


def _time(value: float | int | str) -> float:
    return round(float(value), 4)


def _script(value: str) -> str:
    return (value + ";").replace(";;", ";")


def _no_newline(value: str | None, what: str) -> None:
    if value is not None and "\n" in value:
        raise ValueError(f"Newline in {what}: {value!r}")


def _one_or_list(values: list[Any]) -> Any:
    return values[0] if len(values) == 1 else values


def _one_or_list_schema(inner: JsonSchema) -> JsonSchema:
    return {"anyOf": [inner["items"], inner]}


def _sorted_by_time(items: list[Any], item: Any) -> list[Any]:
    """`items` with `item` in time order, replacing the item at the same time."""
    kept = [existing for existing in items if existing.time != item.time]
    return sorted([*kept, item], key=lambda existing: existing.time)


# region Bones


class _AnimKeyframe(JsonObject):
    """A keyframe of a bone channel. Written as the vector alone when it only has `post`.

    Args:
        time (float): The time of the keyframe, in seconds.
        post (tuple[float | str, float | str, float | str]): The value from this keyframe on.
        pre (tuple[float | str, float | str, float | str], optional): The value up to this
            keyframe, which makes a step.
        lerp_mode (Literal["linear", "catmullrom"], optional): How the value moves to the
            next keyframe.
    """

    time: Annotated[float, NonNegative] = json_field(exclude=True)
    pre: tuple[float | str, float | str, float | str] | None = None
    post: tuple[float | str, float | str, float | str] = json_field()
    lerp_mode: Literal["linear", "catmullrom"] | None = None

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        return payload["post"] if list(payload) == ["post"] else payload

    @classmethod
    def __schema_body__(cls, definitions: dict[str, JsonSchema]) -> JsonSchema:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        return {"anyOf": [schema["properties"]["post"], schema]}


class _AnimRelativeTo(JsonObject):
    """What a bone's channels are relative to.

    Args:
        rotation (Literal["entity"]): Makes the bone rotation relative to the entity instead
            of the bone's parent.
    """

    rotation: Literal["entity"] = json_field()


class _AnimBone(JsonObject):
    """Keyframes for one bone. Created through :meth:`_Animation.bone`."""

    name: str = json_field(exclude=True, positional=True)
    relative_to: _AnimRelativeTo | None = None
    position: Annotated[list[_AnimKeyframe], Keyed("time")] = json_field(
        default_factory=list, omit_default=True
    )
    rotation: Annotated[list[_AnimKeyframe], Keyed("time")] = json_field(
        default_factory=list, omit_default=True
    )
    scale: Annotated[list[_AnimKeyframe], Keyed("time")] = json_field(
        default_factory=list, omit_default=True
    )

    def set_relative_to(self, rotation: Literal["entity"]) -> "_AnimBone":
        """Makes the bone rotation relative to the entity instead of the bone's parent."""
        self.relative_to = _AnimRelativeTo(rotation=rotation)
        return self

    @staticmethod
    def _keyframe(
        time: float,
        value: Sequence[float | str],
        pre: Sequence[float | str] | None,
        lerp_mode: Literal["linear", "catmullrom"] | None,
    ) -> _AnimKeyframe:
        if pre is not None and lerp_mode is not None:
            raise ValueError("A keyframe cannot use both 'pre' and 'lerp_mode'.")
        return _AnimKeyframe(
            time=_time(time),
            post=tuple(value),
            pre=None if pre is None else tuple(pre),
            lerp_mode=lerp_mode,
        )

    def add_position(
        self,
        time: float,
        value: Sequence[float | str],
        *,
        pre: Sequence[float | str] | None = None,
        lerp_mode: Literal["linear", "catmullrom"] | None = None,
    ) -> "_AnimBone":
        """Adds a position keyframe, replacing the one at the same time. `pre` makes a step,
        `lerp_mode` e.g. 'catmullrom'."""
        keyframe = self._keyframe(time, value, pre, lerp_mode)
        self.position = _sorted_by_time(self.position, keyframe)
        return self

    def add_rotation(
        self,
        time: float,
        value: Sequence[float | str],
        *,
        pre: Sequence[float | str] | None = None,
        lerp_mode: Literal["linear", "catmullrom"] | None = None,
    ) -> "_AnimBone":
        """Adds a rotation keyframe, replacing the one at the same time. `pre` makes a step,
        `lerp_mode` e.g. 'catmullrom'."""
        keyframe = self._keyframe(time, value, pre, lerp_mode)
        self.rotation = _sorted_by_time(self.rotation, keyframe)
        return self

    def add_scale(
        self,
        time: float,
        value: Sequence[float | str],
        *,
        pre: Sequence[float | str] | None = None,
        lerp_mode: Literal["linear", "catmullrom"] | None = None,
    ) -> "_AnimBone":
        """Adds a scale keyframe, replacing the one at the same time. `pre` makes a step,
        `lerp_mode` e.g. 'catmullrom'."""
        keyframe = self._keyframe(time, value, pre, lerp_mode)
        self.scale = _sorted_by_time(self.scale, keyframe)
        return self

    def is_empty(self) -> bool:
        return not (self.position or self.rotation or self.scale)


# endregion

# region Events


class _AnimParticleEffect(JsonObject):
    """A particle effect an animation plays.

    Args:
        effect (str): The particle effect's short name, from the entity's description.
        locator (str, optional): The locator the effect plays at.
        pre_effect_script (str, optional): Molang run when the emitter starts.
        bind_to_actor (bool, optional): False plays the effect in the world instead of on
            the actor. Game default True.
    """

    effect: str = json_field()
    locator: str | None = None
    pre_effect_script: str | None = None
    bind_to_actor: bool | None = None

    def __validate__(self) -> None:
        _no_newline(self.effect, "particle effect")
        _no_newline(self.locator, "particle locator")
        _no_newline(self.pre_effect_script, "particle script")


class _AnimSoundEffect(JsonObject):
    """A sound effect an animation plays.

    Args:
        effect (str): The sound's short name, from the entity's description.
        locator (str, optional): The locator the sound plays at.
    """

    effect: str = json_field()
    locator: str | None = None

    def __validate__(self) -> None:
        _no_newline(self.effect, "sound effect")


class _AnimParticleEffects(JsonValue):
    """The particle effects at one time: one effect, or a list of them."""

    time: Annotated[float, NonNegative] = json_field(exclude=True)
    effects: Annotated[
        list[_AnimParticleEffect], Encoded(_one_or_list, _one_or_list_schema)
    ] = json_field(default_factory=list)

    def add_effect(self, effect: _AnimParticleEffect) -> None:
        self.effects.append(effect)


class _AnimSoundEffects(JsonValue):
    """The sound effects at one time, always as a list."""

    time: Annotated[float, NonNegative] = json_field(exclude=True)
    effects: list[_AnimSoundEffect] = json_field(default_factory=list)

    def add_effect(self, effect: _AnimSoundEffect) -> None:
        self.effects.append(effect)


class _AnimTimelineEntry(JsonValue):
    """The Molang run at one time: one script, or a list of them."""

    time: Annotated[float, NonNegative] = json_field(exclude=True)
    scripts: Annotated[list[str], Encoded(_one_or_list, _one_or_list_schema)] = (
        json_field(default_factory=list)
    )

    def add_script(self, script: str) -> None:
        self.scripts.append(script)

    def __validate__(self) -> None:
        for script in self.scripts:
            _no_newline(script, "timeline")


# endregion


class _Animation(JsonObject):
    """A single animation. Only create it through :meth:`Animations.animation`.

    Without `animation_length`, the game uses the time of the last keyframe or event.
    """

    name: str = json_field(exclude=True, positional=True)
    identifier: str = json_field(exclude=True)
    loop: bool | Literal["hold_on_last_frame"] = json_field(
        default=False, omit_default=True
    )
    start_delay: float | str | None = None
    loop_delay: float | str | None = None
    anim_time_update: float | str | None = None
    blend_weight: float | str | None = None
    override_previous_animation: bool = json_field(default=False, omit_default=True)
    bones: Annotated[list[_AnimBone], Keyed("name")] = json_field(
        default_factory=list, omit_default=True
    )
    particle_effects: Annotated[list[_AnimParticleEffects], Keyed("time")] = json_field(
        default_factory=list, omit_default=True
    )
    sound_effects: Annotated[list[_AnimSoundEffects], Keyed("time")] = json_field(
        default_factory=list, omit_default=True
    )
    timeline: Annotated[list[_AnimTimelineEntry], Keyed("time")] = json_field(
        default_factory=list, omit_default=True
    )
    animation_length: Annotated[float, NonNegative] | None = None
    _file: Any = json_field(default=None, init=False, exclude=True)

    @property
    def file(self) -> "Animations":
        """The animations file this animation belongs to."""
        if self._file is None:
            raise ValueError(
                f"Animation '{self.name}' does not belong to an animations file. Create it with Animations.animation()."
            )
        return self._file

    def _set_file(self, file: "Animations") -> None:
        self._file = file

    def set_loop(self, loop: bool | Literal["hold_on_last_frame"]) -> "_Animation":
        """Sets whether the animation stops, loops, or stays on its last frame when it ends."""
        self.loop = loop
        return self

    def set_start_delay(self, start_delay: float | str) -> "_Animation":
        """Sets how long to wait, in seconds or Molang, before playing the animation."""
        self.start_delay = start_delay
        return self

    def set_loop_delay(self, loop_delay: float | str) -> "_Animation":
        """Sets how long to wait, in seconds or Molang, before looping the animation."""
        self.loop_delay = loop_delay
        return self

    def set_anim_time_update(self, anim_time_update: float | str) -> "_Animation":
        """Sets how time passes while the animation plays. Game default
        `query.anim_time + query.delta_time`."""
        self.anim_time_update = anim_time_update
        return self

    def set_blend_weight(self, blend_weight: float | str) -> "_Animation":
        """Sets the weight of the animation when it blends with others."""
        self.blend_weight = blend_weight
        return self

    def set_override_previous_animation(
        self, override_previous_animation: bool = True
    ) -> "_Animation":
        """Resets the animated bones to their default pose before applying this animation."""
        self.override_previous_animation = override_previous_animation
        return self

    def set_animation_length(self, animation_length: float) -> "_Animation":
        """Sets the length in seconds, instead of the time of the last keyframe or event."""
        self.animation_length = animation_length
        return self

    def bone(
        self, name: str, *, relative_to_rotation: Literal["entity"] | None = None
    ) -> _AnimBone:
        """Returns the keyframes of `name`, creating them on first use."""
        bone = next((bone for bone in self.bones if bone.name == name), None)
        if bone is None:
            bone = _AnimBone(name)
            self.bones.append(bone)
        if relative_to_rotation is not None:
            bone.set_relative_to(relative_to_rotation)
        return bone

    def particle(
        self,
        time: float,
        effect: str,
        locator: str = "",
        script: str | None = None,
        bind_to_actor: bool | None = None,
    ) -> "_Animation":
        """Plays a particle effect at `time`.

        Args:
            time (float): The time, in seconds.
            effect (str): The particle effect's short name, from the entity's description.
            locator (str, optional): The locator the effect plays at.
            script (str, optional): Molang run when the emitter starts.
            bind_to_actor (bool, optional): False plays the effect in the world instead of
                on the actor.
        """
        entry = self._at(self.particle_effects, _AnimParticleEffects, time)
        entry.add_effect(
            _AnimParticleEffect(
                effect=effect,
                locator=locator or None,
                pre_effect_script=_script(script) if script else None,
                bind_to_actor=bind_to_actor,
            )
        )
        return self

    def sound(self, time: float, effect: str, locator: str = "") -> "_Animation":
        """Plays a sound effect at `time`.

        Args:
            time (float): The time, in seconds.
            effect (str): The sound's short name, from the entity's description.
            locator (str, optional): The locator the sound plays at.
        """
        entry = self._at(self.sound_effects, _AnimSoundEffects, time)
        entry.add_effect(_AnimSoundEffect(effect=effect, locator=locator or None))
        return self

    def add_timeline(self, time: float, script: str) -> "_Animation":
        """Runs Molang at `time`."""
        self._at(self.timeline, _AnimTimelineEntry, time).add_script(_script(script))
        return self

    def _at(self, entries: list[Any], kind: type, time: float) -> Any:
        """The entry of `entries` at `time`, created in time order on first use."""
        time = _time(time)
        entry = next((entry for entry in entries if entry.time == time), None)
        if entry is None:
            entry = kind(time=time)
            entries[:] = _sorted_by_time(entries, entry)
        return entry


class _AnimationsFile(JsonObject):
    """The content of `animations/<name>.animations.json`."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "animations")

    format_version: str = json_field(default=RP_ANIMATION_VERSION, init=False)
    animations: Annotated[list[_Animation], Keyed("identifier")] = json_field(
        default_factory=list
    )

    def add_animation(self, animation: _Animation) -> None:
        self.animations.append(animation)


class Animations(JsonFile):
    """An animations file (``<name>.animations.json``) holding many animations.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/schemasreference/schemas/minecraftschema_actor_animation_1.8.0)
    """

    _document = _AnimationsFile
    _extension = ".animations.json"
    _pack = Pack.RP
    _folder = "animations"
    _object_type = "Animations"

    def animation(
        self,
        name: str,
        length: float | None = None,
        loop: bool | Literal["hold_on_last_frame"] = False,
        anim_time_update: float | str | None = None,
        override_previous_animation: bool = False,
    ) -> _Animation:
        """Creates an animation in this file and returns it.

        This is the only way to add an animation to a set.

        Args:
            name (str): The animation's name in this file.
            length (float, optional): The length in seconds. By default the game uses the
                time of the last keyframe or event.
            loop (bool | Literal["hold_on_last_frame"], optional): Whether the animation
                stops, loops, or stays on its last frame when it ends.
            anim_time_update (float | str, optional): How time passes while it plays.
            override_previous_animation (bool, optional): Resets the animated bones to their
                default pose first.
        """
        if self.get(name) is not None:
            raise ValueError(
                f"Duplicate animation '{name}' in '{self.identifier.name}'."
            )
        animation = _Animation(
            name,
            identifier=f"animation.{CONFIG.NAMESPACE}.{self.identifier.name}.{name}",
            loop=loop,
            anim_time_update=anim_time_update,
            override_previous_animation=override_previous_animation,
            animation_length=length,
        )
        animation._set_file(self)
        self._content.add_animation(animation)
        return animation

    @property
    def has_animations(self) -> bool:
        return bool(self._content.animations)

    def get(self, name: str) -> _Animation | None:
        return next(
            (
                animation
                for animation in self._content.animations
                if animation.name == name
            ),
            None,
        )

    def validate(self, geometry: Geometry) -> "Animations":
        """Checks that every animated bone and locator exists in `geometry`.

        Raises a single ValueError listing all problems.
        """
        locators = geometry.locator_names
        problems: list[str] = []
        for animation in self._content.animations:
            for bone in animation.bones:
                if not bone.is_empty() and geometry.find(bone.name) is None:
                    problems.append(f"'{animation.name}': bone '{bone.name}' not found")
            events = [
                *(e for entry in animation.particle_effects for e in entry.effects),
                *(e for entry in animation.sound_effects for e in entry.effects),
            ]
            for event in events:
                if event.locator and event.locator not in locators:
                    problems.append(
                        f"'{animation.name}': locator '{event.locator}' not found"
                    )
        if problems:
            details = "\n  - ".join(sorted(set(problems)))
            raise ValueError(
                f"Animations in '{self.identifier.name}' do not match geometry '{geometry.name}':\n  - {details}"
            )
        return self
