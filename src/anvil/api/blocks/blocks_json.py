"""The resource pack's `blocks.json`: the sound group of each block."""

from typing import Annotated, Any, ClassVar

from anvil.lib.config import Pack
from anvil.lib.format_versions import BLOCK_JSON_FORMAT_VERSION
from anvil.lib.jsonmodel import JsonFile, JsonObject, Keyed, json_field
from anvil.lib.jsonmodel.enums import BlockSoundGroup


class _BlockEntry(JsonObject):
    """A block in `blocks.json`.

    Args:
        block (str): The block identifier.
        sound (str): The block's sound group.
    """

    block: str = json_field(exclude=True)
    sound: str = json_field()


class _BlocksJsonFile(JsonObject):
    """The content of `blocks.json`: the format version, and each block next to it."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version",)

    format_version: str = json_field(default=BLOCK_JSON_FORMAT_VERSION, init=False)
    blocks: Annotated[list[_BlockEntry], Keyed("block")] = json_field(
        default_factory=list
    )

    def add_block(self, block: _BlockEntry) -> None:
        """Adds a block, in place of an earlier entry for it."""
        self.blocks = [x for x in self.blocks if x.block != block.block] + [block]

    def __json__(self) -> Any:
        payload = JsonObject.__json__(self)
        payload.update(payload.pop("blocks", {}))
        return payload

    @classmethod
    def __schema_body__(cls, definitions: dict[str, dict[str, Any]]) -> dict[str, Any]:
        schema = JsonObject.__schema_body__.__func__(cls, definitions)
        blocks = schema["properties"].pop("blocks")
        schema["required"] = ["format_version"]
        schema["additionalProperties"] = blocks["additionalProperties"]
        return schema


class BlocksJSONObject(JsonFile):
    """The resource pack's `blocks.json`, which gives blocks their sound group. There is
    one per pack.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blocksjsonfilestructure)
    """

    _document = _BlocksJsonFile
    _instance = None
    _extension = ".json"
    _pack = Pack.RP
    _object_type = "Blocks JSON"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        super().__init__("blocks")
        self._initialized = True

    def add_block(
        self, block: str, sound_group: BlockSoundGroup | str | None = None
    ) -> "BlocksJSONObject":
        """Adds the block to `blocks.json`. Its `sound` is the block's own sound group, the
        one the custom block sound events define, unless `sound_group` names another (a
        vanilla one like `BlockSoundGroup.Wood`).

        Args:
            block (str): The block identifier.
            sound_group (BlockSoundGroup | str, optional): The sound group.
        """
        sound = str(block) if sound_group is None else str(sound_group)
        self._content.add_block(_BlockEntry(block=str(block), sound=sound))
        return self

    def queue(self) -> "BlocksJSONObject":
        """Queues `blocks.json` for export, when it has a block."""
        if not self._content.blocks:
            return self
        return super().queue()
