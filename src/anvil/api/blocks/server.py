"""The behavior pack's `blocks/<block>.block.json`: a server block, its description, traits,
components and permutations."""

from typing import Annotated, Any, ClassVar, Literal

from anvil.api.blocks.blocks import Block
from anvil.api.blocks.components import (
    BlockDisplayName,
    BlockGeometry,
    BlockMaterialInstance,
)
from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.core.components import ComponentGroup, Permutation
from anvil.api.logic.molang import Molang
from anvil.lib.config import CONFIG, Pack
from anvil.lib.format_versions import BLOCK_SERVER_VERSION
from anvil.lib.jsonmodel import (
    BlockId,
    Encoded,
    Identifier,
    JsonFile,
    JsonObject,
    json_field,
    validate_components,
)
from anvil.lib.jsonmodel.enums import (
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

__all__ = ["BlockServer"]


# region Parts


def _components(group: ComponentGroup) -> Any:
    return group.__payload__()


def _permutations(permutations: list[Permutation]) -> Any:
    return [
        {"condition": permutation.condition, "components": permutation.__payload__()}
        for permutation in permutations
    ]


class _PlacementDirectionTrait(JsonObject):
    """The `minecraft:placement_direction` trait: states about the player's rotation when
    the block is placed."""

    enabled_states: list[PlacementDirectionTrait] | None = None
    y_rotation_offset: float | None = None
    blocks_to_corner_with: (
        list[Annotated[str | Block | BlockDescriptor, BlockId]] | None
    ) = None


class _PlacementPositionTrait(JsonObject):
    """The `minecraft:placement_position` trait: states about where the block is placed."""

    enabled_states: list[PlacementPositionTrait] = json_field(default_factory=list)


class _ConnectionTrait(JsonObject):
    """The `minecraft:connection` trait: states about the blocks this one connects to."""

    enabled_states: list[ConnectionTrait] = json_field(default_factory=list)


class _MultiBlockTrait(JsonObject):
    """The `minecraft:multi_block` trait: a block made of several parts."""

    enabled_states: list[MultiblockPartState] = json_field(
        default_factory=lambda: [MultiblockPartState.Part], init=False
    )
    parts: int = json_field(default=2)
    direction: Literal["up", "down", "north", "south", "east", "west"] = json_field(
        default="up"
    )


class _BlockTraits(JsonObject):
    """The block traits, and the states each one adds.

    ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits)
    """

    placement_direction: _PlacementDirectionTrait | None = json_field(
        default=None, key="minecraft:placement_direction"
    )
    placement_position: _PlacementPositionTrait | None = json_field(
        default=None, key="minecraft:placement_position"
    )
    connection: _ConnectionTrait | None = json_field(
        default=None, key="minecraft:connection"
    )
    multi_block: _MultiBlockTrait | None = json_field(
        default=None, key="minecraft:multi_block"
    )

    def set_placement_direction(
        self,
        *,
        y_rotation_offset: float = 0,
        blocks_to_corner_with: list[str | Block | BlockDescriptor] | None = None,
        traits: list[PlacementDirectionTrait] | None = None,
    ) -> "_BlockTraits":
        """Adds states about the player's rotation when the block is placed.

        Args:
            y_rotation_offset (float, optional): The rotation offset, a multiple of 90 in
                [0, 360]. Defaults to 0.
            blocks_to_corner_with (list[Block | BlockDescriptor | str], optional): Blocks
                this one turns to face the corner with, when placed next to them. Needs the
                `CornerAndCardinalDirection` trait.
            traits (list[PlacementDirectionTrait], optional): The states to add.

        Raises:
            ValueError: When the offset or the traits are not valid, or the block is a
                multi block without the `CardinalDirection` trait only.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_direction-example)
        """
        if self.multi_block is not None and traits != [
            PlacementDirectionTrait.CardinalDirection
        ]:
            raise ValueError(
                "placement_direction can only be used with multi_block with the trait "
                "[PlacementDirectionTrait.CardinalDirection]."
            )
        if y_rotation_offset % 90 != 0:
            raise ValueError("y_rotation_offset must be a multiple of 90.")
        if not 360 >= y_rotation_offset >= 0:
            raise ValueError("y_rotation_offset must be between 0 and 360.")
        if blocks_to_corner_with and (
            not traits
            or PlacementDirectionTrait.CornerAndCardinalDirection not in traits
        ):
            raise ValueError(
                "blocks_to_corner_with requires "
                "PlacementDirectionTrait.CornerAndCardinalDirection to be in traits."
            )
        self.placement_direction = _PlacementDirectionTrait(
            enabled_states=list(traits) if traits else None,
            y_rotation_offset=y_rotation_offset if y_rotation_offset != 0 else None,
            blocks_to_corner_with=(
                list(blocks_to_corner_with) if blocks_to_corner_with else None
            ),
        )
        return self

    def set_placement_position(
        self, traits: list[PlacementPositionTrait]
    ) -> "_BlockTraits":
        """Adds states about the position the block is placed at.

        Args:
            traits (list[PlacementPositionTrait]): The states to add.

        Raises:
            ValueError: When the block is a multi block.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#placement_position-example)
        """
        if self.multi_block is not None:
            raise ValueError("placement_position cannot be used with multi_block.")
        self.placement_position = _PlacementPositionTrait(enabled_states=list(traits))
        return self

    def set_connection(self, traits: list[ConnectionTrait]) -> "_BlockTraits":
        """Adds states about the blocks this one connects to.

        Args:
            traits (list[ConnectionTrait]): The states to add.

        Raises:
            ValueError: When the block is a multi block.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits#connection_trait_example)
        """
        if self.multi_block is not None:
            raise ValueError("connection cannot be used with multi_block.")
        self.connection = _ConnectionTrait(enabled_states=list(traits))
        return self

    def set_multi_block(
        self,
        direction: Literal["up", "down", "north", "south", "east", "west"],
        part_count: int = 2,
    ) -> "_BlockTraits":
        """Makes the block one of several parts, treated as one block like a door. With a raw
        `true` selection box, the game outlines every part together.

        Args:
            direction (Literal["up", "down", "north", "south", "east", "west"]): Where the
                parts go from the first one. Horizontal directions need the experimental
                features.
            part_count (int, optional): The number of parts, in [2, 4]. Defaults to 2.

        Raises:
            ValueError: When the direction or the count is not valid, or another trait
                clashes with it.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blocktraits)
        """
        if self.placement_position is not None or self.connection is not None:
            raise ValueError(
                "multi_block cannot be used with placement_position, or connection traits."
            )
        if self.placement_direction is not None and (
            self.placement_direction.enabled_states
            != [PlacementDirectionTrait.CardinalDirection]
        ):
            raise ValueError(
                "multi_block can only be used with placement_direction with the trait "
                "[PlacementDirectionTrait.CardinalDirection]."
            )
        if direction not in ("up", "down", "north", "south", "east", "west"):
            raise ValueError(
                "multi_block direction must be one of 'up', 'down', 'north', 'south', "
                "'east', or 'west'."
            )
        if direction in ("north", "south", "east", "west") and not CONFIG._EXPERIMENTAL:
            raise ValueError(
                "Horizontal multi_block directions (north, south, east, west) require the "
                "experimental flag to be enabled in the config."
            )
        if not 2 <= part_count <= 4:
            raise ValueError("multi_block part_count must be between 2 and 4.")
        self.multi_block = _MultiBlockTrait(parts=part_count, direction=direction)
        return self

    @property
    def states(self) -> dict[str, list]:
        """The states the traits add to the block, with the values each can have."""
        states: dict[str, list] = {}
        enabled: list = []
        for trait in (
            self.placement_direction,
            self.placement_position,
            self.connection,
        ):
            if trait is not None and trait.enabled_states:
                enabled.extend(trait.enabled_states)
        if self.multi_block is not None:
            enabled.extend(self.multi_block.enabled_states)
        for state in enabled:
            match state:
                case PlacementDirectionTrait.CardinalDirection:
                    states[state] = list(CardinalDirectionsValues)
                case PlacementDirectionTrait.FacingDirection:
                    states[state] = list(FacingDirectionValues)
                case PlacementDirectionTrait.CornerAndCardinalDirection:
                    states[PlacementDirectionTrait.CardinalDirection] = list(
                        CardinalDirectionsValues
                    )
                    states[BlockCornerState.Corner] = list(BlockCornerValues)
                case PlacementPositionTrait.BlockFace:
                    states[state] = list(FacingDirectionValues)
                case PlacementPositionTrait.VerticalHalf:
                    states[state] = list(VerticalHalfValues)
                case ConnectionTrait.CardinalConnections:
                    for connection in CardinalConnectionStates:
                        states[connection] = [False, True]
                case MultiblockPartState.Part:
                    states[state] = list(range(self.multi_block.parts))
        return states


class _BlockMenuCategory(JsonObject):
    """Where the block is in the creative inventory."""

    category: ItemCategory = json_field()
    group: ItemGroups | str | None = None
    is_hidden_in_commands: bool | None = None


class _BlockServerDescription(JsonObject):
    """The `description` of a server block: its identifier, states, traits and menu
    category, with their builders.

    ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockdescription)
    """

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: Identifier | None = None
    states: dict[str, list[str | int | float | bool]] = json_field(default_factory=dict)
    menu_category: _BlockMenuCategory | None = None
    traits: _BlockTraits = json_field(default_factory=_BlockTraits)

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the identifier, already parsed by the file."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The description has no identifier.")

    def add_state(
        self, name: str, values: list[str | int | float | bool] | tuple
    ) -> "_BlockServerDescription":
        """Adds a state the block can be in. A name without a namespace gets the project's.

        Args:
            name (str): The state's name.
            values (list[str | int | float | bool] | tuple): The values it can have, at most 16.

        Raises:
            ValueError: When there are more than 16 values.
        """
        if len(values) > 16:
            raise ValueError(
                f"A block state can only have up to 16 values. {self.identifier}[{name}]."
            )
        state_name = name if ":" in name else f"{CONFIG.NAMESPACE}:{name}"
        self.states[state_name] = list(values)
        return self

    def set_menu_category(
        self,
        category: ItemCategory,
        group: ItemGroups | str | None = None,
        is_hidden_in_commands: bool = False,
    ) -> "_BlockServerDescription":
        """Puts the block in the creative inventory.

        Args:
            category (ItemCategory): The creative tab.
            group (ItemGroups | str, optional): The group inside the tab, a vanilla one or
                a `tag.<namespace>:<name>` key from the crafting item catalog.
            is_hidden_in_commands (bool, optional): Hides the block from commands. Defaults
                to False.

        ## [Documentation reference](https://learn.microsoft.com/en-gb/minecraft/creator/reference/content/blockreference/examples/blockdescription?view=minecraft-bedrock-stable#menu_category-parameters)
        """
        self.menu_category = _BlockMenuCategory(
            category=category,
            group=group,
            is_hidden_in_commands=True if is_hidden_in_commands else None,
        )
        return self


class _BlockServer(JsonObject):
    """The `minecraft:block` body."""

    description: _BlockServerDescription = json_field(
        default_factory=_BlockServerDescription
    )
    components: Annotated[ComponentGroup, Encoded(_components, {"type": "object"})] = (
        json_field(default_factory=lambda: ComponentGroup(name="components"))
    )
    permutations: Annotated[
        list[Permutation], Encoded(_permutations, {"type": "array"})
    ] = json_field(default_factory=list)


class _BlockServerFile(JsonObject):
    """The content of a `.block.json` file."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:block")

    format_version: str = json_field(default=BLOCK_SERVER_VERSION, init=False)
    block: _BlockServer = json_field(
        default_factory=_BlockServer, key="minecraft:block"
    )


# endregion


class BlockServer(JsonFile):
    """A server block: its description, components and permutations.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/)
    """

    _document = _BlockServerFile
    _extension = ".block.json"
    _pack = Pack.BP
    _folder = "blocks"
    _object_type = "Block Server"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a server block. Add the block components from
        `anvil.api.blocks.components` to `components`.

        Args:
            name (str): The block's name.
            is_vanilla (bool, optional): If the block is a vanilla one. Defaults to False.
        """
        super().__init__(name, is_vanilla)
        self.description.set_identifier(self.identifier)

    @property
    def description(self) -> _BlockServerDescription:
        """The description builders, such as `add_state` and `set_menu_category`."""
        return self._content.block.description

    @property
    def components(self) -> ComponentGroup:
        """The block components."""
        return self._content.block.components

    @property
    def permutations(self) -> list[Permutation]:
        """The permutations, in the order they were added."""
        return self._content.block.permutations

    def permutation(self, condition: str | Molang) -> Permutation:
        """Adds a permutation, components that apply while a condition is true, and returns it.

        Args:
            condition (str | Molang): The Molang condition.
        """
        permutation = Permutation(condition=condition)
        self.permutations.append(permutation)
        return permutation

    def _before_export(self) -> None:
        """Gives the block a display name when it has none, then lets each component finish
        itself for export (its localized names, see `__prepare_export__`)."""
        for group, root in [
            (self.components, True),
            *((permutation, False) for permutation in self.permutations),
        ]:
            if root and not any(isinstance(c, BlockDisplayName) for c in group):
                group.add(BlockDisplayName(value=self.identifier.display_name))
            for component in group:
                component.__prepare_export__(self, root=root)

    def __export__(self) -> None:
        """Checks the components before the file is written.

        Raises:
            ValueError: When the root components have no geometry or no material instance.
            ValueError: A component is misplaced, misses one it requires, or clashes.
        """
        validate_components(self, self.components, self.permutations, is_block=True)
        if not self.components.has(BlockGeometry):
            raise ValueError(
                f"Block {self.identifier} missing at least one geometry in the root components."
            )
        if not self.components.has(BlockMaterialInstance):
            raise ValueError(
                f"Block {self.identifier} missing at least one material instance in the root "
                "components."
            )
        self._before_export()
        return super().__export__()
