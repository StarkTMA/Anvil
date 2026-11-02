from typing import Literal

from anvil.api.blocks.components import (
    BlockDisplayName,
    BlockGeometry,
    BlockMaterialInstance,
)
from anvil.api.core.components import ComponentGroup, Permutation
from anvil.api.core.enums import (
    BlockCornerState,
    BlockCornerValues,
    CardinalConnectionStates,
    CardinalDirectionsValues,
    ConnectionTrait,
    FacingDirectionValues,
    ItemCategory,
    ItemGroups,
    MultiblockPartState,
    PlacementDirectionTrait,
    PlacementPositionTrait,
    VerticalHalfValues,
)
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG, Pack
from anvil.lib.jsonmodel import validate_components
from anvil.lib.schemas import (
    AddonObject,
    JsonSchemes,
    MinecraftBlockDescriptor,
    MinecraftDescription,
)

__all__ = ["BlockServer"]


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

        Args:
            y_rotation_offset (float, optional): The y rotation offset. Defaults to 0.
            blocks_to_corner_with (list[MinecraftBlockDescriptor], optional): A list of blocks that when placed next to this block, will cause the block to rotate to face the corner between them. Defaults to None.
            traits (list[PlacementDirectionTrait], optional): The traits for the block. Defaults to None.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_direction-example)
        """

        if self._traits.get("minecraft:multi_block") and traits != [
            PlacementDirectionTrait.CardinalDirection
        ]:
            raise ValueError(
                "placement_direction can only be used with multi_block with the trait [PlacementDirectionTrait.CardinalDirection]."
            )

        if y_rotation_offset % 90 != 0:
            raise ValueError("y_rotation_offset must be a multiple of 90.")
        if not 360 >= y_rotation_offset >= 0:
            raise ValueError("y_rotation_offset must be between 0 and 360.")

        if blocks_to_corner_with:
            if PlacementDirectionTrait.CornerAndCardinalDirection not in traits:
                raise ValueError(
                    "blocks_to_corner_with requires PlacementDirectionTrait.CornerAndCardinalDirection to be in traits."
                )
        trait = {}
        if y_rotation_offset != 0:
            trait["y_rotation_offset"] = y_rotation_offset

        if blocks_to_corner_with:
            trait["blocks_to_corner_with"] = blocks_to_corner_with

        if traits:
            trait["enabled_states"] = traits

        self._traits["minecraft:placement_direction"] = trait

    def placement_position(self, traits: list[PlacementPositionTrait]):
        """Can add states containing information about the position of the block when it is placed.

        Args:
            traits (list[PlacementPositionTrait]): The traits for the block.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_position-example)
        """
        if self._traits.get("minecraft:multi_block"):
            raise ValueError("connection trait cannot be used with placement_position.")
        self._traits["minecraft:placement_position"] = {"enabled_states": traits}

    def connection(self, traits: list[ConnectionTrait]):
        """Can add states containing information about the connection of the block to other blocks.

        Args:
            traits (list[ConnectionTrait]): The traits for the block.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#connection_trait_example)
        """
        if self._traits.get("minecraft:multi_block"):
            raise ValueError("connection trait cannot be used with multi_block.")

        self._traits["minecraft:connection"] = {"enabled_states": traits}

    def multi_block(
        self,
        direction: Literal["up", "down", "north", "south", "east", "west"],
        part_count: int = 2,
    ):
        """Defines a block composed of multiple block parts.

        Multi blocks treat all parts as a single block, similar to doors. When the
        block uses ``minecraft:selection_box`` with a raw ``true`` value, Bedrock
        expands the selection outline by combining the AABBs of each part.

        Args:
            direction (Literal["up", "down", "north", "south", "east", "west"]): Direction the parts are placed from.
            part_count (int, optional): Number of parts in the multi block. Valid range is [2, 4]. Defaults to 2.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits)
        """
        if {
            "minecraft:placement_position",
            "minecraft:connection",
        } & self._traits.keys():
            raise ValueError(
                "multi_block cannot be used with placement_position, or connection traits."
            )

        if self._traits.get("minecraft:placement_direction"):
            if self._traits["minecraft:placement_direction"]["enabled_states"] != [
                PlacementDirectionTrait.CardinalDirection
            ]:
                raise ValueError(
                    "multi_block can only be used with placement_direction with the trait [PlacementDirectionTrait.CardinalDirection]."
                )

        if direction not in ("up", "down", "north", "south", "east", "west"):
            raise ValueError(
                "multi_block direction must be one of 'up', 'down', 'north', 'south', 'east', or 'west'."
            )
        if direction in ("north", "south", "east", "west") and not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "Horizontal multi_block directions (north, south, east, west) require the experimental flag to be enabled in the config."
            )

        if not 2 <= part_count <= 4:
            raise ValueError("multi_block part_count must be between 2 and 4.")

        self._traits["minecraft:multi_block"] = {
            "enabled_states": ["minecraft:multi_block_part"],
            "parts": part_count,
            "direction": direction,
        }

        return self

    @property
    def states(self) -> dict[str, list]:
        """The states the traits add to the block, with the values each can have."""
        states = {}
        for trait in self._traits.values():
            for enabled in trait.get("enabled_states", []):
                match enabled:
                    case PlacementDirectionTrait.CardinalDirection:
                        states[enabled] = list(CardinalDirectionsValues)
                    case PlacementDirectionTrait.FacingDirection:
                        states[enabled] = list(FacingDirectionValues)
                    case PlacementDirectionTrait.CornerAndCardinalDirection:
                        states[PlacementDirectionTrait.CardinalDirection] = list(
                            CardinalDirectionsValues
                        )
                        states[BlockCornerState.Corner] = list(BlockCornerValues)
                    case PlacementPositionTrait.BlockFace:
                        states[enabled] = list(FacingDirectionValues)
                    case PlacementPositionTrait.VerticalHalf:
                        states[enabled] = list(VerticalHalfValues)
                    case ConnectionTrait.CardinalConnections:
                        for state in CardinalConnectionStates:
                            states[state] = [False, True]
                    case MultiblockPartState.Part:
                        states[enabled] = list(range(trait["parts"]))
        return states

    @property
    def export(self):
        return self._traits


class _BlockServerDescription(MinecraftDescription):
    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block description.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self._traits = _BlockTraits()
        self._description["description"].update(
            {"states": {}, "traits": {}, "menu_category": {}}
        )

    def add_state(
        self, name: str, values: set[float | str | bool]
    ) -> "_BlockServerDescription":
        """Adds a state to the block.

        Args:
            name (str): The name of the state.
            values (float | str |bool): Values this state can have.

        """
        if len(values) > 16:
            raise ValueError(
                f"A block state can only have up to 16 values. {self._object_type}[{self.name}]."
            )

        state_name = name if ":" in name else f"{CONFIG.NAMESPACE}:{name}"
        self._description["description"]["states"][state_name] = values
        return self

    def menu_category(
        self,
        category: ItemCategory,
        group: ItemGroups | None = None,
        is_hidden_in_commands: bool = False,
    ) -> "_BlockServerDescription":
        """Sets the menu category for the Block.

        Args:
            category (ItemCategory): The category of the Block.
            group (ItemGroups | None, optional): The group of the Block. Defaults to None.
            is_hidden_in_commands (bool, optional): Whether the Block is hidden in commands. Defaults to False.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockdescription?view=minecraft-bedrock-stable#menu_category-parameters)

        """
        self._description["description"]["menu_category"]["category"] = str(category)
        self._description["description"]["menu_category"]["group"] = (
            group if group else None
        )
        self._description["description"]["menu_category"]["is_hidden_in_commands"] = (
            is_hidden_in_commands if is_hidden_in_commands else {}
        )
        return self

    @property
    def traits(self) -> "_BlockTraits":
        """Sets the traits for the block.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits)
        """
        return self._traits

    def __export__(self) -> dict:
        self._description["description"]["traits"] = self._traits.export
        return super().__export__()


class BlockServer(AddonObject):
    """The block server object."""

    _extension = ".block.json"
    _pack = Pack.BP
    _folder = "blocks"
    _object_type = "Block Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """The block server object.

        Args:
            name (str): The name of the block.
            is_vanilla (bool, optional): Whether or not the block is a vanilla block. Defaults to False.
        """
        super().__init__(name)
        self._server_block = JsonSchemes.server_block()
        self._description = _BlockServerDescription(name, is_vanilla)
        self._components = ComponentGroup(name="components")
        self._permutations: list[Permutation] = []

    @property
    def description(self) -> "_BlockServerDescription":
        """The block description."""
        return self._description

    @property
    def components(self) -> "ComponentGroup":
        """The block components."""
        return self._components

    def permutation(self, condition: str | Molang) -> Permutation:
        """Adds a permutation to the block.

        Args:
            condition (str | Molang): The condition for the permutation.
        """
        permutation = Permutation(condition=condition)
        self._permutations.append(permutation)
        return permutation

    def _before_export(self) -> None:
        """Gives every group a display name when it has none, then lets each component
        finish itself for export (its localized names, see `__prepare_export__`)."""
        for group, root in [
            (self._components, True),
            *((permutation, False) for permutation in self._permutations),
        ]:
            if root and not any(isinstance(c, BlockDisplayName) for c in group):
                group.add(BlockDisplayName(value=self._display_name))
            for component in group:
                component.__prepare_export__(self, root=root)

    def __export__(self) -> None:
        """Queues the block to be exported."""
        validate_components(self, self._components, self._permutations, is_block=True)
        if not self._components.has(BlockGeometry):
            raise RuntimeError(
                f"Block {self.identifier} missing at least one geometry in the root components."
            )
        if not self._components.has(BlockMaterialInstance):
            raise RuntimeError(
                f"Block {self.identifier} missing at least one material instance in the root "
                "components."
            )
        self._before_export()

        self._server_block["minecraft:block"].update(self.description.__export__())
        self._server_block["minecraft:block"][
            "components"
        ] = self._components.__payload__()
        self._server_block["minecraft:block"]["permutations"] = self._permutations

        self.content(self._server_block)
        super().__export__()
