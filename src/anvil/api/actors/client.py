from anvil.api.actors.description import _ActorClientDescription
from anvil.api.core.textures import ItemTexturesObject
from anvil.api.logic.molang import Molang
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.lib.blockbench import _BlockBenchSource
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import JsonFile
from anvil.lib.schemas import (
    JsonSchemes,
)

__all__ = ["EntityClient"]


class _EntityClientDescription(_ActorClientDescription):
    """Base class for all client entity descriptions."""

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client entity descriptions.

        Args:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        self._spawn_egg_texture = None
        super().__init__(name, is_vanilla)

    def enable_attachables(self, value: bool = False) -> "_EntityClientDescription":
        """This determines if the entity should render attachables such as armor."""
        self._description["description"]["enable_attachables"] = value
        return self

    @property
    def HeldItemIgnoresLighting(self) -> "_EntityClientDescription":
        """This determines if the held item should ignore lighting."""
        self._description["description"]["held_item_ignores_lighting"] = True
        return self

    @property
    def HideArmor(self) -> "_EntityClientDescription":
        """This determines if the armor should be hidden."""
        self._description["description"]["hide_armor"] = True
        return self

    def spawn_egg(
        self, texture: TextureComponents, texture_index: int = 0
    ) -> "_EntityClientDescription":
        """This method adds a spawn egg texture to the entity.

        Args:
            item_sprite (str): The name of the item sprite.
        """
        if texture is None:
            raise ValueError("TextureComponents must be provided")

        ItemTexturesObject().add_item(texture.color, [texture.color])
        texture_set = TextureSet(texture.color, _BlockBenchSource.ITEM)
        texture_set.set_item_textures(texture)
        texture_set.queue()

        self._description["description"]["spawn_egg"] = {
            "texture": f"{CONFIG.NAMESPACE}:{texture.color}",
            "texture_index": texture_index if texture_index == 0 else {},
        }
        return self

    def spawn_egg_color(
        self, base_color: str, overlay_color: str
    ) -> "_EntityClientDescription":
        """This method adds a spawn egg color to the entity.

        Args:
            base_color (str): The base color of the spawn egg.
            overlay_color (str): The overlay color of the spawn egg.
        """
        self._description["description"]["spawn_egg"] = {
            "base_color": base_color,
            "overlay_color": overlay_color,
        }
        return self

    def held_item_scale(self, scale: Molang | str = 1) -> "_EntityClientDescription":
        """Sets the scale of the held item.

        Args:
            scale (str | Molang, optional): The scale of the held item. Defaults to "1".
        """
        if scale != 1:
            self._description["description"]["held_item_scale"] = scale
        return self

    def __export__(self, directory: str) -> dict:
        """Queues the entity for export.

        Args:
            directory (str): The directory to export the entity to.

        """
        super().__export__(directory)
        if "spawn_egg" not in self._description["description"] and not self._is_vanilla:
            self._description["description"]["spawn_egg"] = {
                "base_color": "#FFFFFF",
                "overlay_color": "#000000",
            }

        return self._description


class EntityClient(JsonFile):
    """Base class for all client entities."""

    _extension = ".entity.json"
    _pack = Pack.RP
    _folder = "entity"
    _object_type = "Client Entity"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Base class for all client entities.

        Args:
            name (str): The name of the entity.
            is_vanilla (bool, optional): Whether or not the entity is a vanilla entity. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._client_entity = JsonSchemes.entity_client()
        self._description = _EntityClientDescription(
            self.identifier, self.identifier.is_vanilla
        )

    @property
    def description(self) -> "_EntityClientDescription":
        """Returns the entity description."""
        return self._description

    def queue(self, directory: str = None) -> "EntityClient":
        """Queues the entity for export.

        Args:
            directory (str, optional): The directory to export the entity to. Defaults to None.
        """
        super().queue(directory=directory)

    def __export__(self) -> None:
        self._client_entity["minecraft:client_entity"].update(
            self._description.__export__(self._directory)
        )

        self.content(self._client_entity)
        return super().__export__()
