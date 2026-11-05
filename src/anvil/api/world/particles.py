"""Particle effects, loaded from the project's `assets/particles` into a typed document.

## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/particlesreference/particlecomponentlist)
"""

from pathlib import Path, PurePosixPath
from typing import ClassVar, Literal

import orjson

from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject, json_field
from anvil.lib.reports import ReportType

# region Description


class _ParticleRenderParameters(JsonObject):
    """`basic_render_parameters`: the particle's material and texture."""

    material: str = json_field()
    texture: str = json_field()

    def set_texture(self, texture: str) -> None:
        """Sets the texture path, from the resource pack root."""
        self.texture = texture


class _ParticleDescription(JsonObject):
    """The particle's `description`."""

    identifier: str = json_field()
    basic_render_parameters: _ParticleRenderParameters = json_field()

    def set_identifier(self, identifier: str) -> None:
        """Sets the identifier the game knows the particle by."""
        self.identifier = identifier


# endregion
# region Curves


class _ParticleCurveNode(JsonObject):
    """A node of a `bezier_chain` curve."""

    value: float | str | None = None
    left_value: float | str | None = None
    right_value: float | str | None = None
    slope: float | str | None = None
    left_slope: float | str | None = None
    right_slope: float | str | None = None


class _ParticleCurve(JsonObject):
    """A curve, evaluated into the Molang variable it is named after."""

    type: Literal["linear", "bezier", "bezier_chain", "catmull_rom"] = json_field()
    input: float | str | None = None
    horizontal_range: float | str | None = None
    nodes: list[float | str] | dict[str, _ParticleCurveNode] | None = None


# endregion
# region Events


class _ParticleEventEffect(JsonObject):
    """The particle effect an event spawns."""

    effect: str = json_field()
    type: Literal["emitter", "emitter_bound", "particle", "particle_with_velocity"] = (
        json_field()
    )
    pre_effect_expression: str | None = None

    def set_effect(self, effect: str) -> None:
        """Sets the identifier of the spawned particle."""
        self.effect = effect


class _ParticleEventSound(JsonObject):
    """The sound an event plays."""

    event_name: str = json_field()


class _ParticleEvent(JsonObject):
    """An event of the particle's `events`, fired by name from lifetime components."""

    sequence: list[_ParticleEvent] | None = None
    randomize: list[_ParticleEvent] | None = None
    weight: float | None = None
    particle_effect: _ParticleEventEffect | None = None
    sound_effect: _ParticleEventSound | None = None
    expression: str | None = None
    log: str | None = None


# endregion
# region Emitter components


class _EmitterLocalSpace(JsonObject):
    """`minecraft:emitter_local_space`: what the particles follow of the entity."""

    position: bool | None = None
    rotation: bool | None = None
    velocity: bool | None = None


class _EmitterInitialization(JsonObject):
    """`minecraft:emitter_initialization`: Molang run when the emitter starts and updates."""

    creation_expression: str | None = None
    per_update_expression: str | None = None


class _EmitterRateInstant(JsonObject):
    """`minecraft:emitter_rate_instant`: every particle at once."""

    num_particles: float | str | None = None


class _EmitterRateSteady(JsonObject):
    """`minecraft:emitter_rate_steady`: particles at a rate over time."""

    spawn_rate: float | str | None = None
    max_particles: float | str | None = None


class _EmitterRateManual(JsonObject):
    """`minecraft:emitter_rate_manual`: particles only when the game emits them."""

    max_particles: float | str | None = None


class _EmitterLifetimeLooping(JsonObject):
    """`minecraft:emitter_lifetime_looping`: emits, sleeps, and loops until removed."""

    active_time: float | str | None = None
    sleep_time: float | str | None = None


class _EmitterLifetimeOnce(JsonObject):
    """`minecraft:emitter_lifetime_once`: emits once, then expires."""

    active_time: float | str | None = None


class _EmitterLifetimeExpression(JsonObject):
    """`minecraft:emitter_lifetime_expression`: on and off through Molang."""

    activation_expression: float | str | None = None
    expiration_expression: float | str | None = None


class _LoopingTravelDistanceEvent(JsonObject):
    """Events fired every time the emitter travels `distance`."""

    distance: float = json_field()
    effects: list[str] = json_field()


class _EmitterLifetimeEvents(JsonObject):
    """`minecraft:emitter_lifetime_events`: events fired over the emitter's lifetime."""

    creation_event: str | list[str] | None = None
    expiration_event: str | list[str] | None = None
    timeline: dict[str, str | list[str]] | None = None
    travel_distance_events: dict[str, str | list[str]] | None = None
    looping_travel_distance_events: list[_LoopingTravelDistanceEvent] | None = None


class _EmitterShapePoint(JsonObject):
    """`minecraft:emitter_shape_point`: particles from one point."""

    offset: tuple[float | str, float | str, float | str] | None = None
    direction: tuple[float | str, float | str, float | str] | None = None


class _EmitterShapeSphere(JsonObject):
    """`minecraft:emitter_shape_sphere`: particles from a sphere."""

    offset: tuple[float | str, float | str, float | str] | None = None
    radius: float | str | None = None
    surface_only: bool | None = None
    direction: (
        Literal["inwards", "outwards"]
        | tuple[float | str, float | str, float | str]
        | None
    ) = None


class _EmitterShapeBox(JsonObject):
    """`minecraft:emitter_shape_box`: particles from a box."""

    offset: tuple[float | str, float | str, float | str] | None = None
    half_dimensions: tuple[float | str, float | str, float | str] | None = None
    surface_only: bool | None = None
    direction: (
        Literal["inwards", "outwards"]
        | tuple[float | str, float | str, float | str]
        | None
    ) = None


class _EmitterShapeCustom(JsonObject):
    """`minecraft:emitter_shape_custom`: particles placed by Molang."""

    offset: tuple[float | str, float | str, float | str] | None = None
    direction: tuple[float | str, float | str, float | str] | None = None


class _EmitterShapeEntityAabb(JsonObject):
    """`minecraft:emitter_shape_entity_aabb`: particles from the entity's bounding box."""

    surface_only: bool | None = None
    direction: (
        Literal["inwards", "outwards"]
        | tuple[float | str, float | str, float | str]
        | None
    ) = None


class _EmitterShapeDisc(JsonObject):
    """`minecraft:emitter_shape_disc`: particles from a disc."""

    plane_normal: (
        Literal["x", "y", "z"] | tuple[float | str, float | str, float | str] | None
    ) = None
    offset: tuple[float | str, float | str, float | str] | None = None
    radius: float | str | None = None
    surface_only: bool | None = None
    direction: (
        Literal["inwards", "outwards"]
        | tuple[float | str, float | str, float | str]
        | None
    ) = None


# endregion
# region Particle components


class _ParticleInitialSpin(JsonObject):
    """`minecraft:particle_initial_spin`: the starting rotation and spin rate, in degrees."""

    rotation: float | str | None = None
    rotation_rate: float | str | None = None


class _ParticleInitialization(JsonObject):
    """`minecraft:particle_initialization`: Molang run per particle update and render."""

    per_update_expression: str | None = None
    per_render_expression: str | None = None


class _ParticleMotionDynamic(JsonObject):
    """`minecraft:particle_motion_dynamic`: the forces on the particle."""

    linear_acceleration: tuple[float | str, float | str, float | str] | None = None
    linear_drag_coefficient: float | str | None = None
    rotation_acceleration: float | str | None = None
    rotation_drag_coefficient: float | str | None = None


class _ParticleMotionParametric(JsonObject):
    """`minecraft:particle_motion_parametric`: the particle's position set directly."""

    relative_position: tuple[float | str, float | str, float | str] | None = None
    direction: tuple[float | str, float | str, float | str] | None = None
    rotation: float | str | None = None


class _ParticleCollisionEvent(JsonObject):
    """An event fired when the particle collides."""

    event: str = json_field()
    min_speed: float | None = None


class _ParticleMotionCollision(JsonObject):
    """`minecraft:particle_motion_collision`: collision with the terrain."""

    enabled: bool | float | str | None = None
    collision_drag: float | None = None
    coefficient_of_restitution: float | None = None
    collision_radius: float | None = None
    expire_on_contact: bool | None = None
    events: list[_ParticleCollisionEvent] | _ParticleCollisionEvent | None = None


class _BillboardDirection(JsonObject):
    """How a billboard that faces a direction gets it."""

    mode: Literal["derive_from_velocity", "custom", "custom_direction"] = json_field()
    min_speed_threshold: float | None = None
    custom_direction: tuple[float | str, float | str, float | str] | None = None


class _BillboardFlipbook(JsonObject):
    """A flipbook animation over parts of the texture."""

    base_UV: tuple[float | str, float | str] | None = None
    size_UV: tuple[float | str, float | str] | None = None
    step_UV: tuple[float | str, float | str] | None = None
    frames_per_second: float | str | None = None
    max_frame: float | str | None = None
    stretch_to_lifetime: bool | None = None
    loop: bool | None = None


class _BillboardUV(JsonObject):
    """The part of the texture a billboard shows."""

    texture_width: int | None = None
    texture_height: int | None = None
    uv: tuple[float | str, float | str] | None = None
    uv_size: tuple[float | str, float | str] | None = None
    flipbook: _BillboardFlipbook | None = None


class _ParticleAppearanceBillboard(JsonObject):
    """`minecraft:particle_appearance_billboard`: the particle drawn as a rectangle."""

    size: tuple[float | str, float | str] | None = None
    facing_camera_mode: (
        Literal[
            "rotate_xyz",
            "rotate_y",
            "lookat_xyz",
            "lookat_y",
            "lookat_direction",
            "direction_x",
            "direction_y",
            "direction_z",
            "emitter_transform_xy",
            "emitter_transform_xz",
            "emitter_transform_yz",
        ]
        | None
    ) = None
    direction: _BillboardDirection | None = None
    uv: _BillboardUV | None = None


class _TintingGradient(JsonObject):
    """A color that moves through a gradient as `interpolant` goes from 0 to 1."""

    gradient: list[str | list[float | str]] | dict[str, str | list[float | str]] = (
        json_field()
    )
    interpolant: float | str | None = None


class _ParticleAppearanceTinting(JsonObject):
    """`minecraft:particle_appearance_tinting`: the particle's color."""

    color: str | list[float | str] | _TintingGradient = json_field()


class _ParticleAppearanceLighting(JsonObject):
    """`minecraft:particle_appearance_lighting`: the particle is lit by the world."""


class _ParticleLifetimeExpression(JsonObject):
    """`minecraft:particle_lifetime_expression`: when the particle expires."""

    expiration_expression: float | str | None = None
    max_lifetime: float | str | None = None


class _ParticleLifetimeEvents(JsonObject):
    """`minecraft:particle_lifetime_events`: events fired over the particle's lifetime."""

    creation_event: str | list[str] | None = None
    expiration_event: str | list[str] | None = None
    timeline: dict[str, str | list[str]] | None = None


class _ParticleComponents(JsonObject):
    """The particle's `components`. Unset components are left out."""

    emitter_local_space: _EmitterLocalSpace | None = json_field(
        key="minecraft:emitter_local_space", default=None
    )
    emitter_initialization: _EmitterInitialization | None = json_field(
        key="minecraft:emitter_initialization", default=None
    )
    emitter_rate_instant: _EmitterRateInstant | None = json_field(
        key="minecraft:emitter_rate_instant", default=None
    )
    emitter_rate_steady: _EmitterRateSteady | None = json_field(
        key="minecraft:emitter_rate_steady", default=None
    )
    emitter_rate_manual: _EmitterRateManual | None = json_field(
        key="minecraft:emitter_rate_manual", default=None
    )
    emitter_lifetime_looping: _EmitterLifetimeLooping | None = json_field(
        key="minecraft:emitter_lifetime_looping", default=None
    )
    emitter_lifetime_once: _EmitterLifetimeOnce | None = json_field(
        key="minecraft:emitter_lifetime_once", default=None
    )
    emitter_lifetime_expression: _EmitterLifetimeExpression | None = json_field(
        key="minecraft:emitter_lifetime_expression", default=None
    )
    emitter_lifetime_events: _EmitterLifetimeEvents | None = json_field(
        key="minecraft:emitter_lifetime_events", default=None
    )
    emitter_shape_point: _EmitterShapePoint | None = json_field(
        key="minecraft:emitter_shape_point", default=None
    )
    emitter_shape_sphere: _EmitterShapeSphere | None = json_field(
        key="minecraft:emitter_shape_sphere", default=None
    )
    emitter_shape_box: _EmitterShapeBox | None = json_field(
        key="minecraft:emitter_shape_box", default=None
    )
    emitter_shape_custom: _EmitterShapeCustom | None = json_field(
        key="minecraft:emitter_shape_custom", default=None
    )
    emitter_shape_entity_aabb: _EmitterShapeEntityAabb | None = json_field(
        key="minecraft:emitter_shape_entity_aabb", default=None
    )
    emitter_shape_disc: _EmitterShapeDisc | None = json_field(
        key="minecraft:emitter_shape_disc", default=None
    )
    particle_initial_speed: (
        float | str | tuple[float | str, float | str, float | str] | None
    ) = json_field(key="minecraft:particle_initial_speed", default=None)
    particle_initial_spin: _ParticleInitialSpin | None = json_field(
        key="minecraft:particle_initial_spin", default=None
    )
    particle_initialization: _ParticleInitialization | None = json_field(
        key="minecraft:particle_initialization", default=None
    )
    particle_motion_dynamic: _ParticleMotionDynamic | None = json_field(
        key="minecraft:particle_motion_dynamic", default=None
    )
    particle_motion_parametric: _ParticleMotionParametric | None = json_field(
        key="minecraft:particle_motion_parametric", default=None
    )
    particle_motion_collision: _ParticleMotionCollision | None = json_field(
        key="minecraft:particle_motion_collision", default=None
    )
    particle_appearance_billboard: _ParticleAppearanceBillboard | None = json_field(
        key="minecraft:particle_appearance_billboard", default=None
    )
    particle_appearance_tinting: _ParticleAppearanceTinting | None = json_field(
        key="minecraft:particle_appearance_tinting", default=None
    )
    particle_appearance_lighting: _ParticleAppearanceLighting | None = json_field(
        key="minecraft:particle_appearance_lighting", default=None
    )
    particle_lifetime_expression: _ParticleLifetimeExpression | None = json_field(
        key="minecraft:particle_lifetime_expression", default=None
    )
    particle_lifetime_events: _ParticleLifetimeEvents | None = json_field(
        key="minecraft:particle_lifetime_events", default=None
    )
    particle_expire_if_in_blocks: list[str] | None = json_field(
        key="minecraft:particle_expire_if_in_blocks", default=None
    )
    particle_expire_if_not_in_blocks: list[str] | None = json_field(
        key="minecraft:particle_expire_if_not_in_blocks", default=None
    )
    particle_kill_plane: tuple[float, float, float, float] | None = json_field(
        key="minecraft:particle_kill_plane", default=None
    )


# endregion
# region Document


class _ParticleEffect(JsonObject):
    """The file's `particle_effect`."""

    description: _ParticleDescription = json_field()
    curves: dict[str, _ParticleCurve] | None = None
    events: dict[str, _ParticleEvent] | None = None
    components: _ParticleComponents = json_field(default_factory=_ParticleComponents)


class _ParticleDocument(JsonObject):
    """A `.particle.json` file. It starts empty and is read from the project's file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "particle_effect")

    format_version: str | None = None
    particle_effect: _ParticleEffect | None = None

    def __validate__(self) -> None:
        if self.format_version is None or self.particle_effect is None:
            raise ValueError("The particle has not been read from its file.")


# endregion


def _source_path(particle: str) -> Path:
    """The particle file in the project's assets."""
    return Path("assets", "particles", f"{particle}.particle.json")


class ParticlesNotRegisteredError(ValueError):
    pass


class ParticleNotFoundError(FileNotFoundError):
    def __init__(self, particle_name: str):
        super().__init__(
            f"Could not find '{particle_name}.particle.json' in 'assets/particles'. {Particle._object_type}[{particle_name}]"
        )


class ParticleReferencedNotFoundError(FileNotFoundError):
    def __init__(self, source_name: str, reference_name: str):
        super().__init__(
            f"Could not find '{reference_name}.particle.json', referenced by {source_name}. {Particle._object_type}[{source_name}]"
        )


class ParticleNameMismatch(ParticlesNotRegisteredError):
    def __init__(self, particle_name: str, found_id: str):
        super().__init__(f"Expected '{particle_name}', found '{found_id}'")


class Particle(JsonFile[_ParticleDocument]):
    _non_queued_particles: set[str] = set()
    _queued_particles: set[str] = set()
    _extension = ".particle.json"
    _pack = Pack.RP
    _folder = "particles"
    _object_type = "Particle"

    def _check_event_particles(self):
        for event in (self._document.particle_effect.events or {}).values():
            component = event.particle_effect
            if component is None or component.effect.startswith("minecraft:"):
                continue

            name = component.effect.split(":")[-1]
            self._check_reference_file_exists(_source_path(name), name)

            if name not in Particle._queued_particles:
                Particle._non_queued_particles.add(name)

            component.set_effect(f"{CONFIG.NAMESPACE}:{name}")

    def _check_file_exists(self, source_path: Path, particle_name: str) -> None:
        if not source_path.exists():
            raise ParticleNotFoundError(particle_name)

    def _check_reference_file_exists(
        self, source_path: Path, reference_name: str
    ) -> None:
        if not source_path.exists():
            raise ParticleReferencedNotFoundError(self.identifier.name, reference_name)

    def _load_file_content(self, source_path: Path) -> None:
        try:
            self._document = _ParticleDocument.__from_json__(
                orjson.loads(source_path.read_bytes())
            )
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"{source_path.as_posix()} is not a valid particle file: {error} "
                f"{self._object_type}[{self.name}]"
            ) from error

    def _set_particle_id_texture(self, texture_name: str):
        texture_path = PurePosixPath(
            "textures",
            CONFIG.NAMESPACE,
            CONFIG.PROJECT_NAME,
            "particle",
            texture_name,
        )
        description = self._document.particle_effect.description
        description.basic_render_parameters.set_texture(texture_path.as_posix())
        description.set_identifier(f"{CONFIG.NAMESPACE}:{self.name}")

    def __init__(
        self,
        particle: str,
        component: TextureComponents,
    ) -> None:
        """Create a particle with optional PBR texture set support.

        Args:
            particle (str): Name of the particle.
            component (TextureComponents): Texture components configuration for PBR.
        """
        source_path = _source_path(particle)
        self._check_file_exists(source_path, particle)

        super().__init__(particle)
        self._load_file_content(source_path)

        source_id = self._document.particle_effect.description.identifier
        if source_id != particle:
            raise ParticleNameMismatch(particle, source_id)

        self._texture_set = TextureSet(component.color, "particle")
        self._texture_set.set_particle_textures(component)

        self._set_particle_id_texture(component.color)
        self._check_event_particles()

    def queue(self) -> "Particle":
        if self.name in Particle._non_queued_particles:
            Particle._non_queued_particles.remove(self.name)
        Particle._queued_particles.add(self.name)

        CONFIG.Report.add_report(
            ReportType.PARTICLE,
            vanilla=False,
            col0=self.identifier.name.replace("_", " ").title(),
            col1=f"{CONFIG.NAMESPACE}:{self.identifier.name}",
        )

        return super().queue()

    def __export__(self) -> None:
        if self._texture_set is not None:
            self._texture_set.queue()

        super().__export__()

    def __check_errors__():
        if len(Particle._non_queued_particles) == 0:
            return

        raise ParticlesNotRegisteredError(
            f"The following particles were referenced in particle events but were never queued. [{" ".join(Particle._non_queued_particles)}]"
        )
