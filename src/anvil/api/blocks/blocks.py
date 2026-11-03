from typing import TYPE_CHECKING

from anvil.api.blocks.client import BlockClient
from anvil.api.blocks.server import BlockServer
from anvil.api.core.core import ANVIL
from anvil.api.pbr.texture_set import TextureComponents, TextureSet
from anvil.lib.config import CONFIG
from anvil.lib.jsonmodel import VANILLA_NAMESPACE, Identifier
from anvil.lib.reports import ReportType
from anvil.lib.schemas import MinecraftBlockDescriptor
from anvil.lib.translator import AnvilTranslator

if TYPE_CHECKING:
    from anvil.api.items.items import Item

__all__ = ["Block"]


class Block(MinecraftBlockDescriptor):
    _object_type = "Block"

    def __init__(self, name, is_vanilla=False) -> None:
        super().__init__(name, is_vanilla)

        self.server = BlockServer(name, is_vanilla)
        self.client = BlockClient(name, is_vanilla)

        self._item = None
        self._texture_only = False

    def descriptor(
        self, tags: list[str] = None, **state_values: str | int | float | bool
    ) -> Identifier | dict:
        """The block as a descriptor: its identifier, or the states and tags to match.

        States are keywords, `leaves.descriptor(natural=True)`. A name without a namespace is
        one of this block's states, `natural` is `<namespace>:natural`, or a state a trait
        adds, `cardinal_direction` is `minecraft:cardinal_direction`.

        Raises:
            ValueError: When the block has no such state, or the state cannot have the value.
        """
        identifier = Identifier.parse(
            self.identifier, vanilla=self._is_vanilla, object_type=self._object_type
        )
        vanilla_block = identifier.is_vanilla
        description = self.server.description
        registered = (
            description._description["description"]["states"]
            | description.traits.states
        )
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
        if not states and not tags:
            return identifier
        result: dict = {"name": identifier, "states": states}
        if tags:
            result["tags"] = tags
        return result

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

        ANVIL.__queue__(self)
        return self

    def __export__(self) -> None:

        from anvil.api.blocks.components import BlockDisplayName

        block_name_comp = self.server._server_block["minecraft:block"]["components"][
            BlockDisplayName.identifier
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
