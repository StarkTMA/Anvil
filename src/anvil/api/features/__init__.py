"""World generation features: what is placed in the world, such as a block, a scatter of
other features or a structure. A feature is only placed when a
:class:`~anvil.api.features.feature_rule.FeatureRule` attaches it to biomes, or when another
feature, a sapling or `/place feature` places it.

Each feature type writes one typed document. Its file class builds it with the same
methods as before: the constructor takes the options every feature of that type needs, and
methods set the rest. Values are checked when the file is exported.

Example:
    ```python
    flower = SingleBlockFeature("blue_flower").place_block("minecraft:cornflower")
    flower.may_replace(["minecraft:air"])

    patch = ScatterFeature("blue_flower_patch", flower)
    patch.distribution(8, None, CoordinateRange("uniform", (-4, 4)), 0, CoordinateRange("uniform", (-4, 4)))
    ```

## [Documentation reference](https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/featuresintroduction)
"""

from .aggregate import AggregateFeature
from .cave_carver import (
    CaveCarverFeature,
    NetherCaveCarverFeature,
    UnderwaterCaveCarverFeature,
)
from .feature import CoordinateRange, Feature
from .feature_rule import FeatureRule
from .fossil import FossilFeature
from .geode import GeodeFeature
from .growing_plant import GrowingPlantFeature
from .height_difference_filter import HeightDifferenceFilterFeature
from .multi_block import MultiBlockFeature
from .multiface import MultifaceFeature
from .ore import OreFeature
from .partially_exposed_blob import PartiallyExposedBlobFeature
from .scatter import ScatterFeature
from .sculk_patch import SculkPatchFeature
from .search import SearchFeature
from .sequence import SequenceFeature
from .single_block import SingleBlockFeature
from .snap_to_surface import SnapToSurfaceFeature
from .structure_template import StructureTemplateFeature
from .surface_relative_threshold import SurfaceRelativeThresholdFeature
from .tree import TreeFeature
from .vegetation_patch import VegetationPatchFeature
from .weighted_random import WeightedRandomFeature

__all__ = [
    "AggregateFeature",
    "CaveCarverFeature",
    "CoordinateRange",
    "Feature",
    "FeatureRule",
    "FossilFeature",
    "GeodeFeature",
    "GrowingPlantFeature",
    "HeightDifferenceFilterFeature",
    "MultiBlockFeature",
    "MultifaceFeature",
    "NetherCaveCarverFeature",
    "OreFeature",
    "PartiallyExposedBlobFeature",
    "ScatterFeature",
    "SculkPatchFeature",
    "SearchFeature",
    "SequenceFeature",
    "SingleBlockFeature",
    "SnapToSurfaceFeature",
    "StructureTemplateFeature",
    "SurfaceRelativeThresholdFeature",
    "TreeFeature",
    "UnderwaterCaveCarverFeature",
    "VegetationPatchFeature",
    "WeightedRandomFeature",
]
