import os
from pickle import FALSE
from typing import Any, Dict, List, Literal, Mapping

from anvil.api.blocks.components import (
    BlockDisplayName,
    BlockGeometry,
    BlockMaterialInstance,
)
from anvil.api.core.components import Component, _Components
from anvil.api.core.core import ANVIL, SoundEvent
from anvil.api.core.enums import (
    BlockInteractiveSoundEvent,
    BlockSoundEvent,
    ConnectionTrait,
    ItemCategory,
    ItemGroups,
    PlacementDirectionTrait,
    PlacementPositionTrait,
)
from anvil.api.logic.molang import Molang
from anvil.api.vanilla.blocks import MinecraftBlockTags
from anvil.lib.config import CONFIG
from anvil.lib.reports import ReportType
from anvil.lib.schemas import (
    AddonObject,
    JsonSchemes,
    MinecraftBlockDescriptor,
    MinecraftDescription,
)
from anvil.lib.translator import AnvilTranslator

__all__ = ["Block"]


class TagComponent(Component):
    """Represents a block tag component.

    Handles the creation and management of Minecraft block tags
    with associated dependencies and clashes.
    """

    _object_type = "Block Tag Component"
    _identifier = "minecraft:tag"

    def __init__(self, tag: MinecraftBlockTags):
        """Initializes the block tag component.

        Args:
            tag (MinecraftBlockTags): The block tag to be added as a component.
        """
        super().__init__(f"tag:{tag.value}", False)
        self._set_value({})


# Core
class _PermutationComponents(_Components):
    _count = 0

    def __init__(self, condition: str | Molang = None):
        """The permutation components.

        Args:
            condition (str | Molang, optional): The condition for the permutation.
        """
        super().__init__()
        _PermutationComponents._count += 1
        self._component_group_name = "components"
        self._condition = condition

    def tag(self, *tags: MinecraftBlockTags):
        """The tags for the block.

        Args:
            *tags (MinecraftBlockTags): The tags for the block.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktags
        """
        for tag in tags:
            self._set(TagComponent(tag))

        return self

    def __export__(self):
        cmp = super().__export__()
        if self._condition:
            cmp["condition"] = self._condition
        return cmp


class _BlockTraits:
    def __init__(self) -> None:
        self._traits = {}

    def placement_direction(
        self,
        *,
        y_rotation_offset: float = 0,
        blocks_to_corner_with: list[MinecraftBlockDescriptor] = None,
        traits: list[PlacementDirectionTrait] = None,
    ):
        """can add states containing information about the player's rotation when the block is placed.

        Parameters:
            y_rotation_offset (float, optional): The y rotation offset. Defaults to 0.
            blocks_to_corner_with (list[MinecraftBlockDescriptor], optional): A list of blocks that when placed next to this block, will cause the block to rotate to face the corner between them. Defaults to None.
            traits (list[PlacementDirectionTrait], optional): The traits for the block. Defaults to None.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_direction-example
        """

        if (
            blocks_to_corner_with
            and PlacementPositionTrait.CornerAndCardinal not in traits
        ):
            raise ValueError(
                "blocks_to_corner_with can only be used if PlacementPositionTrait.CornerAndCardinal is in traits."
            )

        self._traits["minecraft:placement_direction"] = {
            "enabled_states": traits,
            "y_rotation_offset": y_rotation_offset,
            "blocks_to_corner_with": blocks_to_corner_with,
        }

    def placement_position(self, traits: list[PlacementPositionTrait]):
        """Can add states containing information about the position of the block when it is placed.

        Parameters:
            traits (list[PlacementPositionTrait]): The traits for the block.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_position-example
        """
        self._traits["minecraft:placement_position"] = {"enabled_states": traits}

    def connection(self, traits: list[ConnectionTrait]):
        """Can add states containing information about the connection of the block to other blocks.

        Parameters:
            traits (list[ConnectionTrait]): The traits for the block.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#connection_trait_example
        """
        self._traits["minecraft:connection"] = {"enabled_states": traits}

    def multi_block(self, direction: Literal["up", "down"], part_count: int = 2):
        """Defines a block composed of multiple block parts.

        Multi blocks treat all parts as a single block, similar to doors. When the
        block uses ``minecraft:selection_box`` with a raw ``true`` value, Bedrock
        expands the selection outline by combining the AABBs of each part.

        Parameters:
            direction (Literal["up", "down"]): Direction the parts are placed from.
            part_count (int, optional): Number of parts in the multi block. Valid range is [2, 4]. Defaults to 2.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits
        """
        if direction not in ("up", "down"):
            raise ValueError("multi_block direction must be either 'up' or 'down'.")
        if not 2 <= part_count <= 4:
            raise ValueError("multi_block part_count must be between 2 and 4.")

        self._traits["minecraft:multi_block"] = {
            "enabled_states": ["minecraft:multi_block_part"],
            "parts": part_count,
            "direction": direction,
        }

        return self

    @property
    def export(self):
        return self._traits


class _BlockServerDescription(MinecraftDescription):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block description.

        Parameters:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._traits = _BlockTraits()
        self._description["description"].update(
            {"states": {}, "traits": {}, "menu_category": {}}
        )

    def add_state(self, name: str, range: set[float | str | bool]):
        """Adds a state to the block.

        Parameters:
            name (str): The name of the state.
            range (float | str |bool): Values this state can have.

        """
        if len(range) > 16:
            raise ValueError(
                f"A block state can only have up to 16 values. {self._object_type}[{self.name}]."
            )

        state_name = name if ":" in name else f"{CONFIG.NAMESPACE}:{name}"
        self._description["description"]["states"][state_name] = range
        return self

    def menu_category(
        self,
        category: ItemCategory = ItemCategory.none,
        group: ItemGroups | str = ItemGroups.none,
        is_hidden_in_commands: bool = False,
    ):
        """Sets the menu category for the Block.

        Parameters:
            category (ItemCategory, optional): The category of the Block. Defaults to ItemCategory.none.
            group (str, optional): The group of the Block. Defaults to None.
            is_hidden_in_commands (bool, optional): Whether the Block is hidden in commands. Defaults to False.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockdescription?view=minecraft-bedrock-stable#menu_category-parameters

        """
        self._description["description"]["menu_category"]["category"] = (
            str(category) if category != ItemCategory.none else {}
        )
        self._description["description"]["menu_category"]["group"] = (
            str(group) if group != ItemGroups.none else {}
        )
        self._description["description"]["menu_category"]["is_hidden_in_commands"] = (
            is_hidden_in_commands if is_hidden_in_commands else {}
        )
        return self

    @property
    def traits(self):
        """Sets the traits for the block.

        ## Documentation reference:
            https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits
        """
        return self._traits

    def __export__(self):
        self._description["description"]["traits"] = self._traits.export
        return super().__export__()


class _BlockServer(AddonObject):
    """The block server object."""

    _extension = ".block.json"
    _path = os.path.join(CONFIG.BP_PATH, "blocks")
    _object_type = "Block Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block server object.

        Parameters:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name)
        self._server_block = JsonSchemes.server_block()
        self._description = _BlockServerDescription(name, is_vanilla)
        self._components = _PermutationComponents(None)
        self._permutations: list[_PermutationComponents] = []

    @property
    def description(self):
        """The block description."""
        return self._description

    @property
    def components(self):
        """The block components."""
        return self._components

    def permutation(self, condition: str | Molang):
        """Adds a permutation to the block.

        Parameters:
            condition (str | Molang): The condition for the permutation.
        """
        self._permutation = _PermutationComponents(condition)
        self._permutations.append(self._permutation)
        return self._permutation

    def __export__(self):
        """Queues the block to be exported."""
        self._server_block["minecraft:block"].update(self.description.__export__())
        self._server_block["minecraft:block"].update(self._components.__export__())
        comps: dict = self._server_block["minecraft:block"]["components"]
        self._server_block["minecraft:block"]["permutations"] = [
            permutation.__export__() for permutation in self._permutations
        ]

        if not BlockMaterialInstance._identifier in comps:
            raise RuntimeError(
                f"Block {self.identifier} missing default component. Block [{self.identifier}]"
            )
        if not BlockGeometry._identifier in comps:
            raise RuntimeError(
                f"Block {self.identifier} missing at least one geometry. Block [{self.identifier}]"
            )
        if (
            not BlockDisplayName._identifier
            in self._server_block["minecraft:block"]["components"]
        ):
            self._server_block["minecraft:block"]["components"][
                BlockDisplayName._identifier
            ] = self._display_name

        self.content(self._server_block)
        super().__export__()


class _BlockClient(AddonObject):
    def __init__(self, name: str, is_vanilla: bool = False):
        super().__init__(name, is_vanilla)

    def block_sound(
        self,
        sound_identifier: str,
        sound_event: BlockSoundEvent | BlockInteractiveSoundEvent,
        volume: float = 1.0,
        pitch: tuple[float, float] = (0.8, 1.2),
        max_distance: float = 0,
        min_distance: float = 9999,
    ):
        sound_event_obj = SoundEvent()
        if isinstance(sound_event, BlockSoundEvent):
            sound_def = sound_event_obj.add_block_event(
                self.identifier,
                sound_identifier,
                sound_event,
                volume,
                pitch,
                max_distance,
                min_distance,
            )
            return sound_def
        elif isinstance(sound_event, BlockInteractiveSoundEvent):
            sound_def = sound_event_obj.add_block_interactive_event(
                self.identifier,
                sound_identifier,
                sound_event,
                volume,
                pitch,
                max_distance,
                min_distance,
            )
            return sound_def
        else:
            raise TypeError("Invalid sound event type.")

    def queue(self):
        return


# ===========================================


class Block(MinecraftBlockDescriptor):
    _object_type = "Block"

    def __init__(self, name, is_vanilla=False):
        super().__init__(name, is_vanilla)

        self.server = _BlockServer(name, is_vanilla)
        self.client = _BlockClient(name, is_vanilla)

        self._item = None

    def descriptor(
        self,
        states: Mapping[str, str | int | float | bool] = None,
        tags: list[str] = None,
    ):
        if any([states, tags]):
            return {
                "name": self.identifier,
                "states": states if states else {},
                "tags": tags if tags else {},
            }
        return self.identifier

    @property
    def item(self):
        if not self._item:
            from anvil.api.items.items import Item

            self._item = Item(self.name)

        return self._item

    def queue(self):
        """Queues the block to be exported."""
        self.server.queue()
        self.client.queue()

        if self._item:
            self._item.queue()

        ANVIL.__queue__(self)

    def __export__(self):
        block_name_comp = self.server._server_block["minecraft:block"]["components"][
            BlockDisplayName._identifier
        ]
        if block_name_comp.startswith("tile."):
            display_name = AnvilTranslator().get_localization_value(block_name_comp)
        else:
            display_name = block_name_comp

        CONFIG.Report.add_report(
            ReportType.BLOCK,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
            col2=[
                f"{key}: {[', '.join(str(v) for v in value)]}"
                for key, value in self.server.description._description["description"][
                    "states"
                ].items()
            ],
        )
