import os
from typing import Literal

from anvil import CONFIG
from anvil.api.core.enums import Dimension
from anvil.lib.config import ConfigPackageTarget
from anvil.lib.schemas import AddonObject, JsonSchemes


class DimensionConfiguration(AddonObject):
    """A class representing a Fog."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "dimensions")
    _object_type = "Dimension Height"

    def __init__(self, dimension: Dimension):
        if CONFIG._TARGET == ConfigPackageTarget.ADDON:
            raise RuntimeError("DimensionHeight cannot be used in an addon package.")
        if dimension not in (Dimension.Overworld, Dimension.Nether, Dimension.TheEnd):
            raise ValueError(f"Invalid dimension: {dimension}")

        self.content(JsonSchemes.dimension_configuration(str(dimension)))
        self.generator_type("void")

        super().__init__(str(dimension.removeprefix("minecraft:")))

    def heigh_bounds(self, range: tuple[int, int]) -> "DimensionConfiguration":
        """Set the height bounds for the dimension.

        Args:
            range (tuple[int, int]): A tuple containing the minimum and maximum height.
        Returns:
            DimensionConfiguration: The current DimensionConfiguration instance.
        """
        if len(range) != 2:
            raise ValueError("Range must be a tuple of two integers (min, max).")

        if range[0] >= range[1]:
            raise ValueError("Minimum height must be less than maximum height.")

        if range[0] % 16 != 0 or range[1] % 16 != 0:
            raise ValueError("Height bounds must be multiples of 16.")

        if 512 < range[0] or range[1] < -512:
            raise ValueError("Height bounds must be within -512 to 512.")

        bounds = {"minecraft:dimension_bounds": {"min": range[0], "max": range[1]}}

        self._content["minecraft:dimension"]["components"].update(bounds)

    def generator_type(
        self, generator: Literal["void"] = "void"
    ) -> "DimensionConfiguration":
        """Set the generator type for the dimension. Only 'void' is supported currently.

        Args:
            generator (Literal["void"]): The type of generator to set.
        Returns:
            DimensionConfiguration: The current DimensionConfiguration instance.
        """
        if generator != "void":
            raise ValueError("Currently, only 'void' generator is supported.")

        gen = {"minecraft:generation": {"generator_type": "void"}}

        self._content.update(gen)
        return self
