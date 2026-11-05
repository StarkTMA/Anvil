from typing import TYPE_CHECKING

from anvil.api.blocks.descriptor import BlockDescriptor
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import VANILLA_NAMESPACE, Identifier
from anvil.lib.reports import ReportType
from anvil.lib.translator import AnvilTranslator

if TYPE_CHECKING:
    from anvil.api.items.items import Item

__all__ = ["Block"]


class Block:
    _object_type = "Block"

    def __init__(self, name: str, is_vanilla: bool = False) -> None:
        """Creates a block: its server and client files share one identifier.

        Args:
            name (str): The block's name, with or without its namespace.
            is_vanilla (bool, optional): If the block is a vanilla one. Defaults to False.

        Raises:
            ValueError: When the name is not valid (see `Identifier.parse`), or a vanilla
                block is not in `MinecraftBlockTypes`, or is an experimental one
                (`anvil.beta.vanilla`) without `features.experimental`.
        """
        from anvil.api.blocks.client import BlockClient
        from anvil.api.blocks.server import BlockServer
        from anvil.api.vanilla.blocks import vanilla_block_ids
        from anvil.beta.vanilla.blocks import (
            vanilla_block_ids as beta_vanilla_block_ids,
        )

        self.identifier = Identifier.parse(
            name, vanilla=is_vanilla, object_type=self._object_type
        )
        experimental = self.identifier in beta_vanilla_block_ids()
        if (
            self.identifier.is_vanilla
            and self.identifier not in vanilla_block_ids()
            and not (experimental and CONFIG._EXPERIMENTAL)
        ):
            if experimental:
                raise ValueError(
                    f"Vanilla block '{self.identifier}' is experimental: turn on "
                    f"features.experimental in anvilconfig.json. Block [{self.identifier}]"
                )
            raise ValueError(
                f"Invalid vanilla block '{self.identifier}'. Please use a valid vanilla "
                f"block from MinecraftBlockTypes. Block [{self.identifier}]"
            )
        self.server = BlockServer(self.identifier, self.identifier.is_vanilla)
        self.client = BlockClient(self.identifier, self.identifier.is_vanilla)

        self._item = None
        self._texture_only = False

    @property
    def name(self) -> str:
        """The block's name, without its namespace."""
        return self.identifier.name

    def __str__(self) -> str:
        return self.identifier

    def descriptor(
        self, tags: str | None = None, **state_values: str | int | float | bool
    ) -> Identifier | BlockDescriptor:
        """The block as a descriptor: its identifier, or a `BlockDescriptor` with the
        states and tags to match.

        States are keywords, `leaves.descriptor(natural=True)`. A name without a namespace is
        one of this block's states, `natural` is `<namespace>:natural`, or a state a trait
        adds, `cardinal_direction` is `minecraft:cardinal_direction`. `tags` is a Molang
        expression over block tags, such as `Query.AllTags(["stone"])`.

        Raises:
            ValueError: When the block has no such state, or the state cannot have the value.
        """
        identifier = self.identifier
        vanilla_block = identifier.is_vanilla
        description = self.server.description
        registered = description.states | description.traits.states
        states = {}
        for key, value in state_values.items():
            if ":" not in key and (
                vanilla_block or f"{VANILLA_NAMESPACE}:{key}" in registered
            ):
                key = f"{VANILLA_NAMESPACE}:{key}"
            state = Identifier.parse(
                key,
                vanilla=vanilla_block or key.startswith(f"{VANILLA_NAMESPACE}:"),
                object_type=f"{self._object_type}[{identifier}] state",
            )
            if not vanilla_block:
                if state not in registered:
                    raise ValueError(
                        f"Unknown state [{state}], the states are {[str(name) for name in registered]}. "
                        f"{self._object_type}[{identifier}]"
                    )
                if not any(
                    isinstance(allowed, bool) == isinstance(value, bool)
                    and allowed == value
                    for allowed in registered[state]
                ):
                    raise ValueError(
                        f"Invalid value {value!r} for state [{state}], the values are "
                        f"{[str(allowed) for allowed in registered[state]]}. {self._object_type}[{identifier}]"
                    )
            states[str(state)] = value
        if not states and tags is None:
            return identifier
        return BlockDescriptor(name=identifier, states=states, tags=tags)

    @property
    def item(self) -> "Item":
        if not self._item:
            from anvil.api.items.items import Item

            self._item = Item(self.name)

        return self._item

    def override_vanilla_texture(
        self, blockbench: str, component: TextureComponents, subfolder: str = ""
    ) -> None:
        """Extracts textures from a Blockbench model and exports them as the block's texture layout,
        bypassing the generation of block configuration files (server/client JSON files).
        Generates a .texture_set.json file under RP_PATH/textures/blocks/{subfolder}.

        Args:
            blockbench (str): The name of the Blockbench model (without extension).
            component (TextureComponents): A TextureComponents object containing color/normal/height/MER/MERS map names.
            subfolder (str, optional): Subfolder under RP_PATH/textures/blocks. Defaults to "".
        """
        self._texture_only = True
        texture_set = TextureSet(self.name, "blocks", overriding_vanilla=True)
        texture_set.set_vanilla_texture(blockbench, component, subfolder)
        texture_set.queue(subfolder)

    def queue(self) -> "Block":
        """Queues the block to be exported."""
        if self._texture_only:
            return self

        self.server.queue()
        self.client.queue()

        if self._item:
            self._item.queue()

        from anvil.api.core.core import ANVIL

        ANVIL.__queue__(self)
        return self

    def __export__(self) -> None:
        from anvil.api.blocks.components import BlockDisplayName

        display_name = next(
            component.value
            for component in self.server.components
            if isinstance(component, BlockDisplayName)
        )
        if display_name.startswith("tile."):
            display_name = AnvilTranslator().get_localization_value(display_name)

        CONFIG.Report.add_report(
            ReportType.BLOCK,
            vanilla=self.identifier.is_vanilla,
            col0=display_name,
            col1=self.identifier,
            col2=[
                f"{key}: {[', '.join(str(v) for v in value)]}"
                for key, value in self.server.description.states.items()
            ],
        )
