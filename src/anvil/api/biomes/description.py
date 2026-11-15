"""The `description` shared by the server and client biome files."""

from typing import ClassVar

from anvil.lib.jsonmodel import Identifier, JsonObject

__all__ = []


class _BiomeDescription(JsonObject):
    """The `description` of a biome: its identifier."""

    __required__: ClassVar[tuple[str, ...]] = ("identifier",)

    identifier: Identifier | None = None

    def set_identifier(self, identifier: Identifier) -> None:
        """Sets the identifier, already parsed by the file."""
        self.identifier = identifier

    def __validate__(self) -> None:
        if self.identifier is None:
            raise ValueError("The description has no identifier.")
