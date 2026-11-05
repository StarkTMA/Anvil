"""The behavior pack's `dimensions/<dimension>.json`: a vanilla dimension override and its
components."""

from typing import Annotated, Any, ClassVar

from anvil.api.core.components import ComponentGroup
from anvil.api.core.core import CONFIG
from anvil.api.dimension.components import DimensionComponent, DimensionGeneration
from anvil.lib.config import ConfigPackageTarget, Pack
from anvil.lib.format_versions import DIMENSION_VERSION
from anvil.lib.jsonmodel import (
    Encoded,
    Identifier,
    JsonFile,
    JsonObject,
    Wrapped,
    json_field,
    validate_components,
)
from anvil.lib.jsonmodel.enums import Dimension

__all__ = ["DimensionConfiguration"]


# region Parts


def _components(group: ComponentGroup) -> Any:
    return group.__payload__()


class _Dimension(JsonObject):
    """The `minecraft:dimension` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description", "components")

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    components: Annotated[ComponentGroup, Encoded(_components, {"type": "object"})] = (
        json_field(default_factory=lambda: ComponentGroup(name="components"))
    )

    def set_description(self, identifier: Identifier) -> None:
        """Sets the identifier written as `description.identifier`.

        Args:
            identifier (Identifier): The file's identifier, already parsed by the file.
        """
        self.description = identifier

    def __validate__(self) -> None:
        if self.description is None:
            raise ValueError("The dimension has no identifier.")


class _DimensionFile(JsonObject):
    """The content of `dimensions/<dimension>.json`."""

    __required__: ClassVar[tuple[str, ...]] = ("format_version", "minecraft:dimension")

    format_version: str = json_field(default=DIMENSION_VERSION, init=False)
    dimension: _Dimension = json_field(
        key="minecraft:dimension", default_factory=_Dimension
    )


# endregion


class DimensionConfiguration(JsonFile[_DimensionFile]):
    """Overrides a vanilla dimension. Add the dimension components from this module to
    `components`.

    The Nether and the End only support void generation, which is always set for them.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/datadrivenoverworldheight)
    """

    _extension = ".json"
    _pack = Pack.BP
    _folder = "dimensions"
    _object_type = "Dimension Configuration"

    def __init__(self, dimension: Dimension, void: bool = False) -> None:
        """Overrides a vanilla dimension.

        Args:
            dimension (Dimension): The dimension to configure.
            void (bool, optional): Generate the dimension as an empty void. Defaults to False.
                The Nether and the End only support void generation, so it is always set for them.
        """
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise ValueError(
                "DimensionConfiguration cannot be used in an addon package."
            )
        if dimension not in (Dimension.Overworld, Dimension.Nether, Dimension.TheEnd):
            raise ValueError(f"Invalid dimension: {dimension}")

        super().__init__(dimension, is_vanilla=True)
        self._dimension = dimension
        self._document.dimension.set_description(self.identifier)

        if void or dimension != Dimension.Overworld:
            self.components.add(DimensionGeneration(generator_type="void"))

    @property
    def components(self) -> ComponentGroup:
        """The dimension components."""
        return self._document.dimension.components

    def queue(self) -> "DimensionConfiguration":
        return super().queue()

    def __export__(self) -> None:
        """Checks the components before the file is written.

        Raises:
            ValueError: A component is not a dimension component.
        """
        for component in self.components:
            if not isinstance(component, DimensionComponent):
                raise ValueError(
                    f"{type(component).__name__} is not a dimension component. "
                    f"{self._object_type}[{self.identifier}]"
                )
        validate_components(self, self.components, [])
        return super().__export__()
