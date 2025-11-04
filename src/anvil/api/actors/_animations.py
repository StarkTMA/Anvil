import os

from anvil.api.logic.molang import Query
from anvil.lib.config import CONFIG
from anvil.lib.lib import MOLANG_PREFIXES
from anvil.lib.schemas import AddonObject, JsonSchemes


class _BPAnimation:
    def __init__(self, identifier, animation_short_name: str, loop: bool):
        self._identifier = identifier
        self._animation_key = (
            f"animation.{identifier.replace(':', '.')}.{animation_short_name}"
        )
        self._animation_length = 0.05
        self._animation = JsonSchemes.bp_animation(
            self._identifier, animation_short_name, loop
        )

    def timeline(self, timestamp: float, *commands: str):
        """Takes a timestamp and a list of events, command or molang to run at that time.

        Args:
            timestamp (float): The timestamp of the event.
            *commands (str): The Events, commands or molang to run on exit of this state.

        Returns:
            This animation.
        """
        if self._animation_length <= timestamp:
            self._animation_length = timestamp + 0.05

        self._animation[self._animation_key][
            "animation_length"
        ] = self._animation_length
        if timestamp not in self._animation[self._animation_key]["timeline"]:
            self._animation[self._animation_key]["timeline"][timestamp] = []
        for command in commands:
            if str(command).startswith("@s"):
                self._animation[self._animation_key]["timeline"][timestamp].append(
                    f"{command}"
                )
            elif any(str(command).startswith(v) for v in MOLANG_PREFIXES):
                self._animation[self._animation_key]["timeline"][timestamp].append(
                    f"{command};"
                )
            else:
                self._animation[self._animation_key]["timeline"][timestamp].append(
                    f"/{command}"
                )
        return self

    def animation_length(self, animation_length: float):
        """This function sets the length of the animation.

        Args:
            animation_length (float): The length of the animation in seconds.

        Returns:
            This animation.
        """
        self._animation[self._animation_key]["animation_length"] = animation_length
        return self

    def anim_time_update(self, anim_time_update: Query):
        """Sets the animation time update query.

        Args:
            anim_time_update (Query): The animation time update query.

        Returns:
            This animation.
        """
        self._animation[self._animation_key]["anim_time_update"] = anim_time_update
        return self

    @property
    def _export(self):
        """Exports the animation data.

        Returns:
            dict: The animation data.
        """
        return self._animation


class _BPAnimations(AddonObject):
    _extension = ".animation.json"
    _path = os.path.join(CONFIG.BP_PATH, "animations")
    _object_type = "behavior Pack Animation"

    def __init__(self, identifier) -> None:
        super().__init__(identifier)
        self._animations = JsonSchemes.animations_bp()
        self._animations_list: list[_BPAnimation] = []

    def add_animation(self, animation_short_name: str, loop: bool = False):
        """Adds a new animation to the current actor.

        Args:
            animation_short_name (str): The shortname of the animation you want to add.
            loop (bool, optional): If the animation should loop or not. Defaults to False.

        Returns:
            Animation.
        """
        self._animation = _BPAnimation(self.identifier, animation_short_name, loop)
        self._animations_list.append(self._animation)
        return self._animation

    def queue(self, directory: str = None):
        """Queues the animations for export.

        Args:
            directory (str, optional): The directory to export to. Defaults to None.
        """
        if len(self._animations_list) > 0:
            for animation in self._animations_list:
                self._animations["animations"].update(animation._export)
            self.content(self._animations)
            return super().queue(directory=directory)
