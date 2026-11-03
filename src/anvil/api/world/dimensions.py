import warnings
from typing import Annotated, ClassVar, Literal

from anvil.api.core.core import CONFIG
from anvil.api.core.enums import Dimension
from anvil.lib.config import ConfigPackageTarget, Pack
from anvil.lib.jsonmodel import (
    Identifier,
    InRange,
    JsonFile,
    JsonObject,
    Wrapped,
    json_field,
)

DIMENSION_FORMAT_VERSION = "1.18.0"

__all__ = ["DimensionConfiguration"]


class _DimensionBounds(JsonObject):
    """The `minecraft:dimension_bounds` component: the lowest and highest block heights.
    Both must be multiples of 16 from -512 to 512, the minimum lower than the maximum.
    """

    __required__: ClassVar[tuple[str, ...]] = ("min", "max")

    min: Annotated[int, InRange(-512, 512)] | None = None
    max: Annotated[int, InRange(-512, 512)] | None = None

    def set_min(self, min: int) -> None:
        """Sets the lowest block height, a multiple of 16 from -512 to 512."""
        self.min = min

    def set_max(self, max: int) -> None:
        """Sets the highest block height, a multiple of 16 from -512 to 512."""
        self.max = max

    def __validate__(self) -> None:
        if self.min is None or self.max is None:
            raise ValueError("Height bounds need both a minimum and a maximum.")
        if self.min % 16 != 0 or self.max % 16 != 0:
            raise ValueError("Height bounds must be multiples of 16.")
        if self.min >= self.max:
            raise ValueError("Minimum height must be less than maximum height.")


class _DimensionGeneration(JsonObject):
    """The `minecraft:generation` component."""

    __required__: ClassVar[tuple[str, ...]] = ("generator_type",)

    generator_type: Literal["void"] | None = None

    def set_generator_type(self, generator_type: Literal["void"]) -> None:
        """Sets how the dimension is generated."""
        self.generator_type = generator_type


class _DimensionComponents(JsonObject):
    """The `components` of a dimension. Unset components are left out."""

    dimension_bounds: _DimensionBounds | None = json_field(
        key="minecraft:dimension_bounds", default=None
    )
    generation: _DimensionGeneration | None = json_field(
        key="minecraft:generation", default=None
    )

    def set_dimension_bounds(self, min: int, max: int) -> None:
        """Sets the lowest and highest block heights."""
        self.dimension_bounds = _DimensionBounds()
        self.dimension_bounds.set_min(min)
        self.dimension_bounds.set_max(max)

    def set_generation(self, generator_type: Literal["void"]) -> None:
        """Sets how the dimension is generated."""
        self.generation = _DimensionGeneration()
        self.generation.set_generator_type(generator_type)


class _Dimension(JsonObject):
    """The `minecraft:dimension` object."""

    __required__: ClassVar[tuple[str, ...]] = ("description", "components")

    description: Annotated[Identifier, Wrapped("identifier")] | None = None
    components: _DimensionComponents = json_field(default_factory=_DimensionComponents)

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

    format_version: str = json_field(default=DIMENSION_FORMAT_VERSION, init=False)
    dimension: _Dimension = json_field(
        key="minecraft:dimension", default_factory=_Dimension
    )


class DimensionConfiguration(JsonFile):
    """Overrides a vanilla dimension's height bounds or generator.

    - The Overworld supports custom height bounds (``minecraft:dimension_bounds``) and void generation.
    - The Nether and the End support void generation only.

    Height bounds do not reshape terrain: already-generated terrain is cut off at the new
    minimum and maximum.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/datadrivenoverworldheight)
    """

    _document = _DimensionFile
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
            raise RuntimeError(
                "DimensionConfiguration cannot be used in an addon package."
            )
        if dimension not in (Dimension.Overworld, Dimension.Nether, Dimension.TheEnd):
            raise ValueError(f"Invalid dimension: {dimension}")

        super().__init__(dimension, is_vanilla=True)
        self._dimension = dimension
        self._content.dimension.set_description(self.identifier)

        if void or dimension != Dimension.Overworld:
            self.generator_type("void")

    def height_bounds(self, range: tuple[int, int]) -> "DimensionConfiguration":
        """Sets the height bounds of the Overworld.

        Args:
            range (tuple[int, int]): Minimum and maximum height. Both must be multiples of 16
                between -512 and 512, and the minimum must be lower than the maximum.

        Returns:
            DimensionConfiguration: The current DimensionConfiguration instance.
        """
        if self._dimension != Dimension.Overworld:
            raise ValueError("Only the Overworld supports custom height bounds.")
        minimum, maximum = range
        self._content.dimension.components.set_dimension_bounds(minimum, maximum)
        return self

    def generator_type(
        self, generator: Literal["void"] = "void"
    ) -> "DimensionConfiguration":
        """Sets the generator type for the dimension. Only 'void' is supported currently.

        Args:
            generator (Literal["void"]): The type of generator to set.
        Returns:
            DimensionConfiguration: The current DimensionConfiguration instance.
        """
        self._content.dimension.components.set_generation(generator)
        return self

    def queue(self) -> "DimensionConfiguration":
        return super().queue()
