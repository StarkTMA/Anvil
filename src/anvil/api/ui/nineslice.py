"""`NinesliceJson`, the nineslice file of a UI texture."""

from pathlib import Path
from typing import ClassVar

from anvil.lib.config import Pack
from anvil.lib.jsonmodel import JsonFile, JsonObject


class _NinesliceFile(JsonObject):
    """The content of `textures/ui/<texture>.json`: how a UI texture stretches."""

    __required__: ClassVar[tuple[str, ...]] = ("base_size",)

    nineslice_size: int | tuple[int, int, int, int] | None = None
    base_size: tuple[int, int] | None = None

    def set_nineslice_size(
        self, nineslice_size: int | tuple[int, int, int, int]
    ) -> None:
        """Sets the border that does not stretch: one size for every side, or the left,
        top, right and bottom sizes in pixels."""
        self.nineslice_size = (
            nineslice_size if isinstance(nineslice_size, int) else tuple(nineslice_size)
        )

    def set_base_size(self, width: int, height: int) -> None:
        """Sets the size of the texture in pixels."""
        self.base_size = (width, height)

    def __validate__(self) -> None:
        if self.base_size is None:
            raise ValueError("A nineslice needs a base size.")


class NinesliceJson(JsonFile[_NinesliceFile]):
    """Makes a UI texture a nineslice: its border keeps its size and its center stretches.

    ```python
    NinesliceJson("button").nineslice_size(4).base_size(16, 16).queue()
    ```
    """

    _extension = ".json"
    _pack = Pack.RP
    _folder = Path("textures", "ui")
    _object_type = "Nineslice Json"

    def __init__(self, name: str) -> None:
        """Initializes the nineslice file of a UI texture.

        Args:
            name (str): The texture name, without `.png`.
        """
        super().__init__(name)

    def nineslice_size(
        self, nineslice_size: int | tuple[int, int, int, int]
    ) -> "NinesliceJson":
        """Sets the border that does not stretch: one size for every side, or the left,
        top, right and bottom sizes in pixels."""
        self._document.set_nineslice_size(nineslice_size)
        return self

    def base_size(self, width: int, height: int) -> "NinesliceJson":
        """Sets the size of the texture in pixels."""
        self._document.set_base_size(width, height)
        return self

    def queue(self) -> "NinesliceJson":
        """Queues the nineslice file for export."""
        return super().queue()
