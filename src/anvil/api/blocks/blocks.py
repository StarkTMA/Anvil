import os
from typing import List, Dict, Any

from anvil import ANVIL, CONFIG
from anvil.api.actors.actors import _Components
from anvil.api.blocks.components import BlockDefault, BlockDisplayName, BlockGeometry, BlockMaterialInstance
from anvil.api.logic.molang import Molang
from anvil.lib.enums import BlockVanillaTags, ItemCategory, ItemGroups, PlacementDirectionTrait, PlacementPositionTrait
from anvil.lib.reports import ReportType
from anvil.lib.schemas import AddonObject, BlockDescriptor, JsonSchemes, MinecraftDescription, CustomComponent

__all__ = ["Block"]


class _tag:
    def __init__(self, tag: BlockVanillaTags):
        self._dependencies: List["_BaseComponent"] = []
        self._clashes: List["_BaseComponent"] = []
        self._component: Dict[str, Any] = {f"tag:{tag}": {"do_not_shorten": True}}

    def __iter__(self):
        return iter(self._component.items())

# Core
class _PermutationComponents(_Components):
    _count = 0

    def __init__(self, condition: str | Molang = None):
        """The permutation components.

        Parameters:
            condition (str | Molang): The condition for the permutation.
        """
        super().__init__()
        _PermutationComponents._count += 1
        self._component_group_name = "components"
        self._condition = condition

    def tag(self, *tags: BlockVanillaTags):
        """The tags for the block.

        Parameters:
            tags (BlockVanillaTags): The tags for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktags
        """
        for tag in tags:

            self._set(_tag(tag))

        return self

    def _export(self):
        cmp = super()._export()
        if self._condition:
            cmp["condition"] = self._condition
        return cmp


class _BlockTraits:
    def __init__(self) -> None:
        self._traits = {}

    def placement_direction(self, y_rotation_offset: float = 0, *traits: PlacementDirectionTrait):
        """can add states containing information about the player's rotation when the block is placed.

        Parameters:
            y_rotation_offset (float, optional): The y rotation offset. Defaults to 0.
            traits (PlacementDirectionTrait): The traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_direction-example
        """

        self._traits["minecraft:placement_direction"] = {
            "enabled_states": [t for t in traits if t],
            "y_rotation_offset": y_rotation_offset,
        }

    def placement_position(self, *traits: PlacementPositionTrait):
        """Can add states containing information about the position of the block when it is placed.

        Parameters:
            traits (PlacementPositionTrait): The traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_position-example
        """
        self._traits["minecraft:placement_position"] = {"enabled_states": traits}

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
            {
                "states": {},
                "traits": {},
            }
        )

    def add_state(self, name: str, range: set[float | str | bool]):
        """Adds a state to the block.

        Parameters:
            name (str): The name of the state.
            range (float | str |bool): Values this state can have.

        """
        if len(range) > 16:
            raise ValueError(f"A block state can only have up to 16 values. {self._object_type}[{self.name}].")

        self._description["description"]["states"][f"{CONFIG.NAMESPACE}:{name}"] = range
        return self

    def menu_category(
        self,
        category: ItemCategory = ItemCategory.none,
        group: ItemGroups | str = ItemGroups.none,
    ):
        """Sets the menu category for the block.

        Parameters:
            category (ItemCategory, optional): The category of the block. Defaults to ItemCategory.none.
            group (str, optional): The group of the block. Defaults to None.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockdescription?view=minecraft-bedrock-stable#menu_category-parameters

        """
        self._description["description"]["menu_category"] = {
            "category": category.value if not category == ItemCategory.none else {},
            "group": group.value if not group == ItemGroups.none else {},
        }
        return self

    @property
    def is_hidden_in_commands(self):
        """Sets the block to be hidden in commands.
        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockdescription?view=minecraft-bedrock-stable#menu_category-parameters
        """
        self._description["description"]["is_hidden_in_commands"] = True
        return self

    @property
    def traits(self):
        """Sets the traits for the block.

        [Documentation reference]: https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits
        """
        return self._traits

    def _export(self):
        self._description["description"]["traits"] = self._traits.export
        return super()._export()


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

    @property
    def queue(self):
        """Queues the block to be exported."""
        self._server_block["minecraft:block"].update(self.description._export())
        self._server_block["minecraft:block"].update(self._components._export())
        comps: dict = self._server_block["minecraft:block"]["components"]
        self._server_block["minecraft:block"]["permutations"] = [permutation._export() for permutation in self._permutations]

        if not BlockDefault._identifier in comps:
            if not BlockMaterialInstance._identifier in comps:
                raise RuntimeError(f"Block {self.identifier} missing default component. Block [{self.identifier}]")
            if not BlockGeometry._identifier in comps:
                raise RuntimeError(f"Block {self.identifier} missing at least one geometry. Block [{self.identifier}]")
        else:
            ANVIL.definitions.register_block(self.description.identifier, comps[BlockDefault._identifier])
            comps.pop(BlockDefault._identifier)

        if not BlockDisplayName._identifier in self._server_block["minecraft:block"]["components"]:
            self._server_block["minecraft:block"]["components"][BlockDisplayName._identifier] = self._display_name

        self.content(self._server_block)
        super().queue()


# ===========================================


class Block(BlockDescriptor):
    _object_type = "Block"

    def __init__(self, name, is_vanilla=False):
        super().__init__(name, is_vanilla)

        self.server = _BlockServer(name, is_vanilla)
        self._item = None

    @property
    def item(self):
        if not self._item:
            from anvil.api.items.items import Item

            self._item = Item(self.name)

        return self._item

    def queue(self):
        """Queues the block to be exported."""
        self.server.queue

        if self._item:
            self._item.queue()

        if self.server._server_block["minecraft:block"]["components"][BlockDisplayName._identifier].startswith("tile."):
            display_name = ANVIL.definitions._language[
                self.server._server_block["minecraft:block"]["components"][BlockDisplayName._identifier]
            ]
        else:
            display_name = self.server._server_block["minecraft:block"]["components"][BlockDisplayName._identifier]

        CONFIG.Report.add_report(
            ReportType.BLOCK,
            vanilla=self._is_vanilla,
            col0=display_name,
            col1=self.identifier,
            col2=[
                f"{key}: {[', '.join(str(v) for v in value)]}"
                for key, value in self.server.description._description["description"]["states"].items()
            ],
        )
