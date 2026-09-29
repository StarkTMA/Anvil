import os
import warnings
from typing import Literal

from anvil.api.core.core import CONFIG
from anvil.api.core.enums import Dimension
from anvil.lib.config import ConfigPackageTarget
from anvil.lib.schemas import AddonObject, JsonSchemes

DIMENSION_FORMAT_VERSION = "1.18.0"


class DimensionConfiguration(AddonObject):
    """Overrides a vanilla dimension's height bounds or generator.

    - The Overworld supports custom height bounds (``minecraft:dimension_bounds``) and void generation.
    - The Nether and the End support void generation only.

    Height bounds do not reshape terrain: already-generated terrain is cut off at the new
    minimum and maximum.

    ## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/documents/datadrivenoverworldheight)
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "dimensions")
    _object_type = "Dimension Configuration"

    def __init__(self, dimension: Dimension, void: bool = False) -> None:
        """Overrides a vanilla dimension.

        Parameters:
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

        super().__init__(str(dimension).removeprefix("minecraft:"))
        self._dimension = dimension
        self.content(JsonSchemes.dimension_configuration(str(dimension)))
        self._content["format_version"] = DIMENSION_FORMAT_VERSION

        if void or dimension != Dimension.Overworld:
            self.generator_type("void")

    @property
    def _components(self) -> dict:
        return self._content["minecraft:dimension"]["components"]

    def height_bounds(self, range: tuple[int, int]) -> "DimensionConfiguration":
        """Sets the height bounds of the Overworld.

        Parameters:
            range (tuple[int, int]): Minimum and maximum height. Both must be multiples of 16
                between -512 and 512, and the minimum must be lower than the maximum.

        Returns:
            DimensionConfiguration: The current DimensionConfiguration instance.
        """
        if self._dimension != Dimension.Overworld:
            raise ValueError("Only the Overworld supports custom height bounds.")

        if len(range) != 2:
            raise ValueError("Range must be a tuple of two integers (min, max).")

        minimum, maximum = range
        if minimum >= maximum:
            raise ValueError("Minimum height must be less than maximum height.")

        if minimum % 16 != 0 or maximum % 16 != 0:
            raise ValueError("Height bounds must be multiples of 16.")

        if minimum < -512 or maximum > 512:
            raise ValueError("Height bounds must be within -512 to 512.")

        self._components["minecraft:dimension_bounds"] = {
            "min": minimum,
            "max": maximum,
        }
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
        if generator != "void":
            raise ValueError("Currently, only 'void' generator is supported.")

        self._components["minecraft:generation"] = {"generator_type": "void"}
        return self

    def queue(self) -> "DimensionConfiguration":
        return super().queue()
