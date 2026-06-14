from __future__ import annotations

import os
from typing import Literal

from anvil.api.core.enums import AimAssistTargetMode, CameraPresets, ControlSchemes
from anvil.lib.config import CONFIG
from anvil.lib.lib import Directory, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


class AimAssistPreset(AddonObject):
    """Represents an Aim Assist Preset in Minecraft Bedrock.

    Aim assist presets allow creators to customize targeting rules, such as
    excluding specific entities/blocks, setting item priorities, or defining
    liquid-targeting rules.

    Placed under the behavior pack folder: `cameras/presets/`.

    [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/documents/camerasystem/introtoaimassist)
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "cameras", "presets")
    _object_type = "Aim Assist Preset"

    def __init__(self, name: str):
        """Initializes the Aim Assist Preset.

        Parameters:
            name (str): Unique name of the preset.
        """
        super().__init__(name)
        self.content(JsonSchemes.aim_assist_preset(self.identifier))

    def item_settings(self, settings: dict):
        """Specifies which category of aim assist rules to use when specific items are held.

        Parameters:
            settings (dict): Key-value pairs of item names and category IDs.
        """
        self._content["minecraft:aim_assist_preset"]["item_settings"] = settings
        return self

    def default_item_settings(self, setting: str):
        """Sets the default aim assist category for items not listed in item_settings.

        Parameters:
            setting (str): The category name.
        """
        self._content["minecraft:aim_assist_preset"]["default_item_settings"] = setting
        return self

    def hand_settings(self, setting: str):
        """Sets the aim assist behavior applied when the player is not holding any items.

        Parameters:
            setting (str): The category name.
        """
        self._content["minecraft:aim_assist_preset"]["hand_settings"] = setting
        return self

    def exclusion_list(self, exclusions: dict):
        """Specifies entities or blocks that the aim assist will ignore.

        Parameters:
            exclusions (dict): Dictionary specifying blocks and/or entities to exclude.
        """
        self._content["minecraft:aim_assist_preset"]["exclusion_list"] = exclusions
        return self

    def liquid_targeting_list(self, targets: dict):
        """Lists the items that are allowed to target liquids.

        Parameters:
            targets (dict): Dictionary specifying liquid targeting items.
        """
        self._content["minecraft:aim_assist_preset"]["liquid_targeting_list"] = targets
        return self

    def __export__(self):
        return self._content

    def queue(self, directory: str = None):
        self.content(self._content)
        return super().queue(directory)


class AimAssistCategory:
    """Helper class representing a single Aim Assist Category.

    Categories define the evaluation priority between entities and blocks.
    Included in `AimAssistCategories`.
    """

    def __init__(self, name: str):
        """Initializes the Aim Assist Category.

        Parameters:
            name (str): Name of the category.
        """
        self._category = {"name": name, "priorities": {}}

    def entity_default(self, value: int):
        """Sets the default priority for entities in this category.

        Parameters:
            value (int): Default priority value.
        """
        self._category["entity_default"] = value
        return self

    def block_default(self, value: int):
        """Sets the default priority for blocks in this category.

        Parameters:
            value (int): Default priority value.
        """
        self._category["block_default"] = value
        return self

    def block_priority(self, block: str, priority: int):
        """Sets the priority for a specific block type.

        Parameters:
            block (str): Block identifier.
            priority (int): Priority value.
        """
        if "priorities" not in self._category:
            self._category["priorities"] = {}
        if "blocks" not in self._category["priorities"]:
            self._category["priorities"]["blocks"] = {}
        self._category["priorities"]["blocks"][block] = priority
        return self

    def entity_priority(self, entity: str, priority: int):
        """Sets the priority for a specific entity type.

        Parameters:
            entity (str): Entity identifier.
            priority (int): Priority value.
        """
        if "priorities" not in self._category:
            self._category["priorities"] = {}
        if "entities" not in self._category["priorities"]:
            self._category["priorities"]["entities"] = {}
        self._category["priorities"]["entities"][entity] = priority
        return self

    def __export__(self):
        return self._category

    def export(self):
        """Legacy alias for __export__ to prevent breaking potential callers."""
        return self.__export__()


class AimAssistCategories(AddonObject):
    """Represents a set of Aim Assist Categories.

    To define evaluation priority between blocks and entities, a categories.json
    file must be created in the same directory as aim assist presets.

    [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/documents/camerasystem/introtoaimassist)
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "cameras", "presets")
    _object_type = "Aim Assist Categories"

    def __init__(self):
        """Initializes the Aim Assist Categories container."""
        super().__init__("categories")
        self.content(JsonSchemes.aim_assist_categories())
        self._categories: list[AimAssistCategory] = []

    def add_category(self, category_name: str) -> AimAssistCategory:
        """Adds and returns a new Aim Assist Category.

        Parameters:
            category_name (str): Name of the category.
        """
        category = AimAssistCategory(category_name)
        self._categories.append(category)
        return category

    def __export__(self):
        self._content["minecraft:aim_assist_categories"]["categories"] = []
        for category in self._categories:
            self._content["minecraft:aim_assist_categories"]["categories"].append(
                category.__export__()
            )
        return self._content

    def queue(self):
        return super().queue()


class CameraPreset(AddonObject):
    """Represents a custom Camera Preset in Minecraft Bedrock.

    Camera presets allow creators to customize how players view the game.
    These presets are stored in the behavior pack at `cameras/presets/`.

    [Documentation](https://learn.microsoft.com/en-us/minecraft/creator/documents/camerasystem/cameracommandintroduction)
    """

    _extension = ".camera.json"
    _path = os.path.join(CONFIG.BP_PATH, "cameras", "presets")
    _object_type = "Camera Preset"

    def __init__(self, name: str, inherit_from: CameraPresets | CameraPreset | str) -> None:
        """Initializes the CameraPreset instance.

        Parameters:
            name (str): Unique name identifier for the preset.
            inherit_from (CameraPresets | CameraPreset | str): The base preset to inherit settings from.
                Can be a vanilla `CameraPresets` enum, another custom `CameraPreset` instance, or its identifier string.
        """
        super().__init__(name)
        if isinstance(inherit_from, CameraPresets):
            self._inherit = inherit_from.value
        elif isinstance(inherit_from, CameraPreset):
            self._inherit = inherit_from.identifier
        elif isinstance(inherit_from, str):
            self._inherit = inherit_from
        else:
            raise ValueError(
                "inherit_from must be a CameraPresets enum, a CameraPreset instance, or a string identifier."
            )

        self._camera_preset = JsonSchemes.camera_preset(self.identifier, self._inherit)
        self._replace_reticle = False

    def position(self, x: float = None, y: float = None, z: float = None):
        """Sets the constant coordinate overrides for the camera.

        Parameters:
            x (float, optional): Override for target camera's X position.
            y (float, optional): Override for target camera's Y position.
            z (float, optional): Override for target camera's Z position.
        """
        if x is not None:
            self._camera_preset["minecraft:camera_preset"]["pos_x"] = x
        if y is not None:
            self._camera_preset["minecraft:camera_preset"]["pos_y"] = y
        if z is not None:
            self._camera_preset["minecraft:camera_preset"]["pos_z"] = z
        return self

    def rotation(self, x: float = None, y: float = None):
        """Sets the default rotation pitch and yaw overrides for the camera.

        Parameters:
            x (float, optional): The pitch (vertical rotation) of the camera in degrees. Clamped between -90 and 90.
            y (float, optional): The yaw (horizontal rotation) of the camera in degrees.
        """
        if x is not None:
            self._camera_preset["minecraft:camera_preset"]["rot_x"] = clamp(x, -90.0, 90.0)
        if y is not None:
            self._camera_preset["minecraft:camera_preset"]["rot_y"] = y
        return self

    def starting_rotation(self, x: float = None, y: float = None):
        """Sets the initial starting rotation pitch and yaw of the camera.

        Parameters:
            x (float, optional): The initial pitch in degrees. Clamped between -90 and 90.
            y (float, optional): The initial yaw in degrees.
        """
        if x is not None:
            self._camera_preset["minecraft:camera_preset"]["starting_rot_x"] = clamp(x, -90.0, 90.0)
        if y is not None:
            self._camera_preset["minecraft:camera_preset"]["starting_rot_y"] = y
        return self

    def player_effects(self, value: bool):
        """Enables or disables screen effects (like fire, night vision, blindness) for this camera preset.

        Parameters:
            value (bool): Whether the camera renders player effects.
        """
        self._camera_preset["minecraft:camera_preset"]["player_effects"] = value
        return self

    def listener(self, value: bool | str):
        """Specifies where the sound listener "ears" are positioned while using the camera.

        Parameters:
            value (bool | str): If True or 'player', uses the player's position.
                If False or 'camera', uses the camera's position.
        """
        if isinstance(value, bool):
            if value:
                self._camera_preset["minecraft:camera_preset"]["listener"] = "player"
            else:
                self._camera_preset["minecraft:camera_preset"].pop("listener", None)
        elif isinstance(value, str):
            self._camera_preset["minecraft:camera_preset"]["listener"] = value
        return self

    def control_scheme(self, value: ControlSchemes | str):
        """Overrides the default input response scheme for this camera.

        Parameters:
            value (ControlSchemes | str): The control scheme, such as 'camera_relative'.
        """
        if isinstance(value, ControlSchemes):
            self._camera_preset["minecraft:camera_preset"]["control_scheme"] = value.value
        else:
            self._camera_preset["minecraft:camera_preset"]["control_scheme"] = value
        return self

    def extend_player_rendering(self, value: bool = True):
        """Extends entity rendering distance so chunks and entities render at further distances.

        Optimized to render the player and leashed entities.

        Parameters:
            value (bool): Whether to extend rendering distance. Defaults to True.
        """
        self._camera_preset["minecraft:camera_preset"][
            "extend_player_rendering"
        ] = value
        return self

    def view_offset(self, x_offset: float, y_offset: float):
        """Sets the view offset relative to the camera position.

        Parameters:
            x_offset (float): X view offset.
            y_offset (float): Y view offset.
        """
        self._camera_preset["minecraft:camera_preset"]["view_offset"] = [
            x_offset,
            y_offset,
        ]
        return self

    def entity_offset(self, x_offset: float, y_offset: float, z_offset: float):
        """Sets the target entity tracking offset.

        Parameters:
            x_offset (float): X coordinate offset.
            y_offset (float): Y coordinate offset.
            z_offset (float): Z coordinate offset.
        """
        self._camera_preset["minecraft:camera_preset"]["entity_offset"] = [
            x_offset,
            y_offset,
            z_offset,
        ]
        return self

    def radius(self, radius: float):
        """Sets the orbital radius (distance from target) for boom/follow/orbit cameras.

        Parameters:
            radius (float): Radius in blocks. Clamped between 0.1 and 100.0.
        """
        self._camera_preset["minecraft:camera_preset"]["radius"] = clamp(
            radius, 0.1, 100
        )
        return self

    def aim_assist(
        self,
        preset: AimAssistPreset,
        target_mode: AimAssistTargetMode = AimAssistTargetMode.Distance,
        angle: list[float] = [30.0, 30.0],
        distance: float = 8.0,
        replace_reticle: bool = False,
    ):
        """Configures targeting aid/assist options for the camera.

        Parameters:
            preset (AimAssistPreset): Aim assist preset to apply.
            target_mode (AimAssistTargetMode): Evaluation mode (e.g. Distance, Angle).
            angle (list[float]): Horizontal/vertical angles defining target search cone.
            distance (float): Target search distance. Clamped between 1.0 and 16.0 blocks.
            replace_reticle (bool): Whether custom reticle UI textures should be copied.
        """
        self._camera_preset["minecraft:camera_preset"]["aim_assist"] = {
            "preset": preset.identifier,
            "target_mode": target_mode.value,
            "angle": [min(angle), max(angle)],
            "distance": clamp(distance, 1, 16),
        }

        if replace_reticle:
            self._replace_reticle = True
        return self

    def focus_target(
        self,
        rotation_speed: float = 0.0,
        snap_to_target: bool = False,
        horizontal_rotation_limit: list[float] = [0.0, 360.0],
        vertical_rotation_limit: list[float] = [0.0, 180.0],
        continue_targeting: bool = False,
        tracking_radius: float = 50.0,
    ):
        """Enables target tracking of a specific entity with custom boundaries.

        Parameters:
            rotation_speed (float): Degrees per second tracking rotation speed. Defaults to 0.0 (perfect tracking).
            snap_to_target (bool): If True, snaps tracking immediately on first frame.
            horizontal_rotation_limit (list[float]): Left and right rotation angle limit degrees. Max sum 360.0.
            vertical_rotation_limit (list[float]): Up and down rotation angle limit degrees. Max sum 180.0.
            continue_targeting (bool): Whether to continue tracking when target leaves rotation/radius boundaries.
            tracking_radius (float): Maximum block distance inside which target is tracked.
        """
        self._camera_preset["minecraft:camera_preset"]["rotation_speed"] = max(
            0.0, rotation_speed
        )
        self._camera_preset["minecraft:camera_preset"][
            "snap_to_target"
        ] = snap_to_target

        h_lim_0 = max(0.0, horizontal_rotation_limit[0])
        h_lim_1 = max(0.0, horizontal_rotation_limit[1])
        if h_lim_0 + h_lim_1 > 360.0:
            total = h_lim_0 + h_lim_1
            h_lim_0 = (h_lim_0 / total) * 360.0
            h_lim_1 = (h_lim_1 / total) * 360.0
        self._camera_preset["minecraft:camera_preset"]["horizontal_rotation_limit"] = [h_lim_0, h_lim_1]

        v_lim_0 = max(0.0, vertical_rotation_limit[0])
        v_lim_1 = max(0.0, vertical_rotation_limit[1])
        if v_lim_0 + v_lim_1 > 180.0:
            total = v_lim_0 + v_lim_1
            v_lim_0 = (v_lim_0 / total) * 180.0
            v_lim_1 = (v_lim_1 / total) * 180.0
        self._camera_preset["minecraft:camera_preset"]["vertical_rotation_limit"] = [v_lim_0, v_lim_1]

        self._camera_preset["minecraft:camera_preset"][
            "continue_targeting"
        ] = continue_targeting
        self._camera_preset["minecraft:camera_preset"][
            "tracking_radius"
        ] = tracking_radius
        return self

    def queue(self):
        """Queues the camera preset to be exported."""
        self.content(self._camera_preset)
        return super().queue()

    def __export__(self):
        if self._replace_reticle:
            if os.path.exists(
                os.path.join(
                    "assets", "textures", "ui", "aimassist_block_highlight.png"
                )
            ):
                Directory.copy_files(
                    os.path.join("assets", "textures", "ui"),
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "aimassist_block_highlight.png",
                )
            if os.path.exists(
                os.path.join(
                    "assets", "textures", "ui", "aimassist_entity_highlight.png"
                )
            ):
                Directory.copy_files(
                    os.path.join("assets", "textures", "ui"),
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "aimassist_entity_highlight.png",
                )

        return super().__export__()
