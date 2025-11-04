import os

from anvil.lib.config import CONFIG
from anvil.lib.enums import AimAssistTargetMode, CameraPresets
from anvil.lib.lib import CopyFiles, FileExists, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes


class AimAssistPreset(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "Camera", "Presets")
    _object_type = "Aim Assist Preset"

    def __init__(self, name: str):
        super().__init__(name)
        self.content(JsonSchemes.aim_assist_preset(self.identifier))

    def item_settings(self, settings: dict):
        self._content["minecraft:aim_assist_preset"]["item_settings"] = settings
        return self

    def default_item_settings(self, setting: str):
        self._content["minecraft:aim_assist_preset"]["default_item_settings"] = setting
        return self

    def hand_settings(self, setting: str):
        self._content["minecraft:aim_assist_preset"]["hand_settings"] = setting
        return self

    def exclusion_list(self, exclusions: dict):
        self._content["minecraft:aim_assist_preset"]["exclusion_list"] = exclusions
        return self

    def liquid_targeting_list(self, targets: dict):
        self._content["minecraft:aim_assist_preset"]["liquid_targeting_list"] = targets
        return self

    def _export(self):
        return self._content

    def queue(self, directory: str = None):
        self.content(self._content)
        return super().queue(directory)


class AimAssistCategory:
    def __init__(self, name: str):
        self._category = {"name": name, "priorities": {}}

    def entity_default(self, value: int):
        self._category["entity_default"] = value
        return self

    def block_default(self, value: int):
        self._category["block_default"] = value
        return self

    def block_priority(self, block: str, priority: int):
        if "blocks" not in self._category["priorities"]:
            self._category["priorities"]["blocks"] = {}
        self._category["priorities"]["blocks"][block] = priority
        return self

    def entity_priority(self, entity: str, priority: int):
        if "entities" not in self._category["priorities"]:
            self._category["priorities"]["entities"] = {}
        self._category["priorities"]["entities"][entity] = priority
        return self

    def export(self):
        return self._category


class AimAssistCategories(AddonObject):
    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "Camera", "Presets")
    _object_type = "Aim Assist Categories"

    def __init__(self):
        super().__init__("categories")
        self.content(JsonSchemes.aim_assist_categories())
        self._categories: list[AimAssistCategory] = []

    def add_category(self, category_name: str):
        category = AimAssistCategory(category_name)
        self._categories.append(category)
        return category

    def _export(self):
        for category in self._categories:
            self._content["minecraft:aim_assist_categories"]["categories"].append(
                category.export()
            )
        return self._content

    def queue(self):
        return super().queue()


class CameraPreset(AddonObject):
    """A class representing a CameraPreset."""

    _extension = ".camera.json"
    _path = os.path.join(CONFIG.BP_PATH, "cameras", "presets")
    _object_type = "Camera Preset"

    def __init__(self, name: str, inherit_from: CameraPresets) -> None:
        """Initializes a CameraPreset instance.

        Parameters:
            name (str): The name of the camera preset.
            is_vanilla (bool, optional): Whether the camera preset is a vanilla camera preset. Defaults to False.
        """
        super().__init__(name)
        if not isinstance(inherit_from, CameraPresets):
            raise ValueError("inherit_from must be an instance of CameraPresets enum.")

        self._inherit = inherit_from
        self._camera_preset = JsonSchemes.camera_preset(self.identifier, self._inherit)
        self._replace_reticle = False

    def position(self, x: float = 0, y: float = 0, z: float = 0):
        """Sets the position of the camera preset.

        Parameters:
            x (float): The x position of the camera preset.
            y (float): The y position of the camera preset.
            z (float): The z position of the camera preset.
        """
        if x != 0:
            self._camera_preset["minecraft:camera_preset"]["pos_x"] = x
        if y != 0:
            self._camera_preset["minecraft:camera_preset"]["pos_y"] = y
        if z != 0:
            self._camera_preset["minecraft:camera_preset"]["pos_z"] = z
        return self

    def rotation(self, x: float = 0, y: float = 0):
        """Sets the rotation of the camera preset.

        Parameters:
            x (float): The x rotation of the camera preset.
            y (float): The y rotation of the camera preset.
        """
        if x != 0:
            self._camera_preset["minecraft:camera_preset"]["rot_x"] = x
        if y != 0:
            self._camera_preset["minecraft:camera_preset"]["rot_y"] = y
        return self

    def player_effects(self, value: bool):
        """Sets whether the player effects are enabled.

        Parameters:
            value (bool): Whether the player effects are enabled.
        """
        self._camera_preset["minecraft:camera_preset"]["player_effects"] = value
        return self

    def listener(self, value: bool):
        """Sets whether the listener is enabled.

        Parameters:
            value (bool): Whether the listener is enabled.
        """
        if value:
            self._camera_preset["minecraft:camera_preset"]["listener"] = "player"
        return self

    def extend_player_rendering(self, value: bool = True):
        """Sets whether the player rendering is extended.

        Parameters:
            value (bool): Whether the player rendering is extended.
        """
        if self._inherit == CameraPresets.Free:
            if value == False:
                self._camera_preset["minecraft:camera_preset"][
                    "extend_player_rendering"
                ] = False
        else:
            raise ValueError(
                f"Extend player rendering can only be set for the Free camera preset, not {self._inherit}."
            )
        return self

    def view_offset(self, x_offset: float, y_offset: float):
        self._camera_preset["minecraft:camera_preset"]["view_offset"] = [
            x_offset,
            y_offset,
        ]
        return self

    def entity_offset(self, x_offset: float, y_offset: float, z_offset: float):
        self._camera_preset["minecraft:camera_preset"]["entity_offset"] = [
            x_offset,
            y_offset,
            z_offset,
        ]
        return self

    def radius(self, radius: float):
        self._camera_preset["minecraft:camera_preset"]["radius"] = clamp(
            radius, 0.1, 100
        )
        return self

    def aim_assist(
        self,
        preset: AimAssistPreset,
        target_mode: AimAssistTargetMode = AimAssistTargetMode.Distance,
        angle: list[float] = [30, 30],
        distance: float = 8,
        replace_reticle: bool = False,
    ):
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
        horizontal_rotation_limit: list[float] = [0, 360],
        vertical_rotation_limit: list[float] = [0, 180],
        continue_targeting: bool = False,
        tracking_radius: float = 50.0,
    ):
        self._camera_preset["minecraft:camera_preset"]["rotation_speed"] = max(
            0.0, rotation_speed
        )
        self._camera_preset["minecraft:camera_preset"][
            "snap_to_target"
        ] = snap_to_target

        self._camera_preset["minecraft:camera_preset"]["horizontal_rotation_limit"] = [
            max(horizontal_rotation_limit[0], 0),
            min(horizontal_rotation_limit[1], 360),
        ]
        self._camera_preset["minecraft:camera_preset"]["vertical_rotation_limit"] = [
            max(vertical_rotation_limit[0], 0),
            min(vertical_rotation_limit[1], 180),
        ]
        self._camera_preset["minecraft:camera_preset"][
            "continue_targeting"
        ] = continue_targeting
        self._camera_preset["minecraft:camera_preset"][
            "tracking_radius"
        ] = tracking_radius
        return self

    def starting_rotation(self, x: float = 0, y: float = 0):
        """Sets the starting rotation of the camera preset.

        Parameters:
            x (float): The x rotation of the camera preset.
            y (float): The y rotation of the camera preset.
        """
        if x != 0:
            self._camera_preset["minecraft:camera_preset"]["starting_rot_x"] = x
        if y != 0:
            self._camera_preset["minecraft:camera_preset"]["starting_rot_y"] = y
        return self

    def queue(self):
        """Queues the camera preset to be exported."""
        self.content(self._camera_preset)
        return super().queue()

    def _export(self):
        if self._replace_reticle:
            if FileExists(
                os.path.join(
                    "assets", "textures", "ui", "aimassist_block_highlight.png"
                )
            ):
                CopyFiles(
                    os.path.join("assets", "textures", "ui"),
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "aimassist_block_highlight.png",
                )
            if FileExists(
                os.path.join(
                    "assets", "textures", "ui", "aimassist_entity_highlight.png"
                )
            ):
                CopyFiles(
                    os.path.join("assets", "textures", "ui"),
                    os.path.join(CONFIG.RP_PATH, "textures", "ui"),
                    "aimassist_entity_highlight.png",
                )

        return super()._export()
