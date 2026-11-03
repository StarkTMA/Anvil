"""Camera presets."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar, Literal

from anvil.api.camera.aim_assist import _PRESETS_FOLDER, AimAssistPreset
from anvil.api.core.enums import AimAssistTargetMode, CameraPresets, ControlSchemes
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import CAMERA_PRESET_VERSION
from anvil.lib.jsonmodel import (
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    NonNegative,
    json_field,
)
from anvil.lib.lib import Directory


class _CameraAimAssist(JsonObject):
    """The `aim_assist` of a camera preset.

    Args:
        preset (Identifier): The aim assist preset.
        target_mode (AimAssistTargetMode): What is evaluated first, the closest target or the
            one closest to the center of the targeting cone.
        angle (tuple[float, float]): The horizontal and vertical angles of the targeting
            cone, each from 10 to 90 degrees.
        distance (float): How far targets are searched, from 1 to 16 blocks.
    """

    preset: Identifier = json_field()
    target_mode: AimAssistTargetMode = json_field()
    angle: tuple[
        Annotated[float, InRange(10, 90)], Annotated[float, InRange(10, 90)]
    ] = json_field()
    distance: Annotated[float, InRange(1, 16)] = json_field()


class _CameraPreset(JsonObject):
    """The `minecraft:camera_preset` object. Unset keys are inherited from `inherit_from`."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier", "inherit_from")

    identifier: Identifier | None = None
    inherit_from: str | None = None
    pos_x: float | None = None
    pos_y: float | None = None
    pos_z: float | None = None
    rot_x: Annotated[float, InRange(-90, 90)] | None = None
    rot_y: float | None = None
    starting_rot_x: Annotated[float, InRange(-90, 90)] | None = None
    starting_rot_y: float | None = None
    player_effects: bool | None = None
    listener: Literal["player"] | None = None
    control_scheme: ControlSchemes | None = None
    extend_player_rendering: bool | None = None
    view_offset: tuple[float, float] | None = None
    entity_offset: tuple[float, float, float] | None = None
    radius: Annotated[float, InRange(0.1, 100)] | None = None
    aim_assist: _CameraAimAssist | None = None
    rotation_speed: Annotated[float, NonNegative] | None = None
    snap_to_target: bool | None = None
    horizontal_rotation_limit: (
        tuple[Annotated[float, NonNegative], Annotated[float, NonNegative]] | None
    ) = None
    vertical_rotation_limit: (
        tuple[Annotated[float, NonNegative], Annotated[float, NonNegative]] | None
    ) = None
    continue_targeting: bool | None = None
    tracking_radius: float | None = None

    def set_description(self, identifier: Identifier, inherit_from: str) -> None:
        """Sets the preset's identifier, already parsed by the file, and the preset it
        inherits from."""
        self.identifier = identifier
        self.inherit_from = inherit_from

    def set_position(
        self, x: float | None = None, y: float | None = None, z: float | None = None
    ) -> None:
        """Sets the coordinates given; the others are left as they are."""
        if x is not None:
            self.pos_x = x
        if y is not None:
            self.pos_y = y
        if z is not None:
            self.pos_z = z

    def set_rotation(self, x: float | None = None, y: float | None = None) -> None:
        """Sets the pitch (-90 to 90) and yaw given; the other is left as it is."""
        if x is not None:
            self.rot_x = x
        if y is not None:
            self.rot_y = y

    def set_starting_rotation(
        self, x: float | None = None, y: float | None = None
    ) -> None:
        """Sets the starting pitch (-90 to 90) and yaw given; the other is left as it is."""
        if x is not None:
            self.starting_rot_x = x
        if y is not None:
            self.starting_rot_y = y

    def set_player_effects(self, player_effects: bool) -> None:
        """Sets if player effects such as night vision render."""
        self.player_effects = player_effects

    def set_listener(self, listener: Literal["player"] | None) -> None:
        """Hears sounds from the player, or from the camera with None."""
        self.listener = listener

    def set_control_scheme(self, control_scheme: ControlSchemes) -> None:
        """Sets how input moves the player."""
        self.control_scheme = control_scheme

    def set_extend_player_rendering(self, extend_player_rendering: bool) -> None:
        """Sets if the player and leashed entities render further away."""
        self.extend_player_rendering = extend_player_rendering

    def set_view_offset(self, x: float, y: float) -> None:
        """Sets the view offset."""
        self.view_offset = (x, y)

    def set_entity_offset(self, x: float, y: float, z: float) -> None:
        """Sets the tracking offset from the target entity."""
        self.entity_offset = (x, y, z)

    def set_radius(self, radius: float) -> None:
        """Sets the distance from the target, from 0.1 to 100 blocks."""
        self.radius = radius

    def set_aim_assist(
        self,
        preset: Identifier,
        target_mode: AimAssistTargetMode,
        angle: tuple[float, float],
        distance: float,
    ) -> None:
        """Sets the aim assist used while the preset is active."""
        self.aim_assist = _CameraAimAssist(
            preset=preset, target_mode=target_mode, angle=angle, distance=distance
        )

    def set_focus_target(
        self,
        rotation_speed: float,
        snap_to_target: bool,
        horizontal_rotation_limit: tuple[float, float],
        vertical_rotation_limit: tuple[float, float],
        continue_targeting: bool,
        tracking_radius: float,
    ) -> None:
        """Sets how the camera tracks its target entity."""
        self.rotation_speed = rotation_speed
        self.snap_to_target = snap_to_target
        self.horizontal_rotation_limit = horizontal_rotation_limit
        self.vertical_rotation_limit = vertical_rotation_limit
        self.continue_targeting = continue_targeting
        self.tracking_radius = tracking_radius

    def __validate__(self) -> None:
        if self.identifier is None or self.inherit_from is None:
            raise ValueError(
                "A camera preset needs an identifier and a preset to inherit."
            )
        if (
            self.horizontal_rotation_limit is not None
            and sum(self.horizontal_rotation_limit) > 360
        ):
            raise ValueError(
                "The horizontal rotation limits cannot add up to more than 360 degrees."
            )
        if (
            self.vertical_rotation_limit is not None
            and sum(self.vertical_rotation_limit) > 180
        ):
            raise ValueError(
                "The vertical rotation limits cannot add up to more than 180 degrees."
            )


class _CameraPresetFile(JsonObject):
    """The content of a camera preset file."""

    __required__: ClassVar[tuple[str, ...]] = (
        "format_version",
        "minecraft:camera_preset",
    )

    format_version: str = json_field(default=CAMERA_PRESET_VERSION, init=False)
    preset: _CameraPreset = json_field(
        key="minecraft:camera_preset", default_factory=_CameraPreset
    )


class CameraPreset(JsonFile):
    """A custom camera preset, used with the `/camera` command or the Script API. Settings
    it does not set are inherited from the preset it is based on.

    Written to the behavior pack's `cameras/presets/` folder.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/camerasystem/cameracommandintroduction)
    """

    _document = _CameraPresetFile
    _extension = ".camera.json"
    _pack = Pack.BP
    _folder = _PRESETS_FOLDER
    _object_type = "Camera Preset"

    _RETICLES: ClassVar[tuple[str, ...]] = (
        "aimassist_block_highlight.png",
        "aimassist_entity_highlight.png",
    )

    def __init__(
        self, name: str, inherit_from: CameraPresets | CameraPreset | str
    ) -> None:
        """Initializes the CameraPreset instance.

        Args:
            name (str): The preset's name, also its file name. The identifier is
                `<namespace>:<name>`.
            inherit_from (CameraPresets | CameraPreset | str): The preset to inherit settings
                from: a vanilla `CameraPresets`, another `CameraPreset`, or its identifier.
        """
        super().__init__(name)
        if isinstance(inherit_from, CameraPreset):
            inherit_from = inherit_from.identifier
        elif not isinstance(inherit_from, str):
            raise TypeError(
                "inherit_from must be a CameraPresets, a CameraPreset or an identifier."
            )
        self._content.preset.set_description(self.identifier, str(inherit_from))
        self._replace_reticle = False

    def position(
        self, x: float | None = None, y: float | None = None, z: float | None = None
    ) -> "CameraPreset":
        """Sets the camera position. Coordinates left out keep the inherited value.

        Args:
            x (float, optional): The X position.
            y (float, optional): The Y position.
            z (float, optional): The Z position.
        """
        self._content.preset.set_position(x, y, z)
        return self

    def rotation(
        self, x: float | None = None, y: float | None = None
    ) -> "CameraPreset":
        """Sets the camera rotation. Angles left out keep the inherited value.

        Args:
            x (float, optional): The pitch, from -90 to 90 degrees. Positive looks down.
            y (float, optional): The yaw, in degrees.
        """
        self._content.preset.set_rotation(x, y)
        return self

    def starting_rotation(
        self, x: float | None = None, y: float | None = None
    ) -> "CameraPreset":
        """Sets the rotation the camera starts with. Angles left out keep the inherited value.

        Args:
            x (float, optional): The pitch, from -90 to 90 degrees.
            y (float, optional): The yaw, in degrees.
        """
        self._content.preset.set_starting_rotation(x, y)
        return self

    def player_effects(self, value: bool) -> "CameraPreset":
        """Sets if effects on the player, such as night vision or blindness, change how the
        game renders while the preset is active.

        Args:
            value (bool): If player effects render.
        """
        self._content.preset.set_player_effects(value)
        return self

    def listener(self, value: bool | Literal["player"]) -> "CameraPreset":
        """Sets where sounds are heard from.

        Args:
            value (bool | Literal["player"]): True or `"player"` hears from the player,
                False from the camera.
        """
        self._content.preset.set_listener("player" if value else None)
        return self

    def control_scheme(self, value: ControlSchemes) -> "CameraPreset":
        """Sets how player input moves the player while the preset is active.

        Args:
            value (ControlSchemes): The control scheme.
        """
        self._content.preset.set_control_scheme(value)
        return self

    def extend_player_rendering(self, value: bool = True) -> "CameraPreset":
        """Renders the player, their ride and leashed entities at further distances, so the
        camera can move far from the player.

        Args:
            value (bool, optional): If rendering is extended. Defaults to True.
        """
        self._content.preset.set_extend_player_rendering(value)
        return self

    def view_offset(self, x_offset: float, y_offset: float) -> "CameraPreset":
        """Sets the view offset from the camera position.

        Args:
            x_offset (float): The X offset.
            y_offset (float): The Y offset.
        """
        self._content.preset.set_view_offset(x_offset, y_offset)
        return self

    def entity_offset(
        self, x_offset: float, y_offset: float, z_offset: float
    ) -> "CameraPreset":
        """Sets the offset from the tracked entity.

        Args:
            x_offset (float): The X offset.
            y_offset (float): The Y offset.
            z_offset (float): The Z offset.
        """
        self._content.preset.set_entity_offset(x_offset, y_offset, z_offset)
        return self

    def radius(self, radius: float) -> "CameraPreset":
        """Sets the distance from the target of boom, follow and orbit cameras.

        Args:
            radius (float): The distance, from 0.1 to 100 blocks.
        """
        self._content.preset.set_radius(radius)
        return self

    def aim_assist(
        self,
        preset: AimAssistPreset,
        target_mode: AimAssistTargetMode = AimAssistTargetMode.Distance,
        angle: tuple[float, float] = (30.0, 30.0),
        distance: float = 8.0,
        replace_reticle: bool = False,
    ) -> "CameraPreset":
        """Uses an aim assist preset while the camera preset is active. It overrides the
        `/aimassist` command.

        Args:
            preset (AimAssistPreset): The aim assist preset.
            target_mode (AimAssistTargetMode, optional): What is evaluated first. Defaults to
                Distance.
            angle (tuple[float, float], optional): The horizontal and vertical angles of the
                targeting cone, each from 10 to 90 degrees. Defaults to (30, 30).
            distance (float, optional): How far targets are searched, from 1 to 16 blocks.
                Defaults to 8.
            replace_reticle (bool, optional): Copies `aimassist_block_highlight.png` and
                `aimassist_entity_highlight.png` from `assets/textures/ui` to replace the
                targeting reticles. Defaults to False.
        """
        self._content.preset.set_aim_assist(
            preset.identifier, target_mode, angle, distance
        )
        if replace_reticle:
            self._replace_reticle = True
        return self

    def focus_target(
        self,
        rotation_speed: float = 0.0,
        snap_to_target: bool = False,
        horizontal_rotation_limit: tuple[float, float] = (0.0, 360.0),
        vertical_rotation_limit: tuple[float, float] = (0.0, 180.0),
        continue_targeting: bool = False,
        tracking_radius: float = 50.0,
    ) -> "CameraPreset":
        """Tracks a target entity, set with `/camera @s target_entity`.

        Args:
            rotation_speed (float, optional): The tracking speed in degrees per second, 0 for
                perfect tracking. Defaults to 0.
            snap_to_target (bool, optional): Snaps to the target on the first frame, then
                tracks at `rotation_speed`. Defaults to False.
            horizontal_rotation_limit (tuple[float, float], optional): How far the camera
                turns left and right from where it first looked, adding up to 360 degrees at
                most. Defaults to (0, 360).
            vertical_rotation_limit (tuple[float, float], optional): The lowest and highest
                pitch, 0 straight down and 180 straight up, adding up to 180 degrees at most.
                Defaults to (0, 180).
            continue_targeting (bool, optional): Keeps tracking a target that leaves the
                limits or the radius. Defaults to False.
            tracking_radius (float, optional): The distance targets are tracked within, in
                blocks. Defaults to 50.
        """
        self._content.preset.set_focus_target(
            rotation_speed,
            snap_to_target,
            horizontal_rotation_limit,
            vertical_rotation_limit,
            continue_targeting,
            tracking_radius,
        )
        return self

    def queue(self) -> "CameraPreset":
        """Queues the camera preset for export."""
        return super().queue()

    def __export__(self) -> None:
        if self._replace_reticle:
            source = Path("assets", "textures", "ui")
            for reticle in self._RETICLES:
                if (source / reticle).exists():
                    Directory.copy_files(
                        source, CONFIG.RP_PATH / "textures" / "ui", reticle
                    )
        return super().__export__()
