import os
from typing import Literal

from anvil import ANVIL
from anvil.api.core.filters import Filter
from anvil.lib.config import CONFIG
from anvil.lib.lib import CopyFiles, FileExists, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import (
    ConstantIntProvider,
    Identifier,
    StructureProcessors,
    UniformIntProvider,
)


class Structure:
    """A class representing a Structure."""

    def __init__(self, structure_name: str):
        """Initializes a Structure instance.

        Parameters:
            structure_name (str): The name of the structure.
        """
        splits = structure_name.split("/")
        self._sub_path = splits[:-1]
        self._name = splits[-1]
        self._path = os.path.join(
            "structures",
            CONFIG.NAMESPACE,
            *self._sub_path,
            f"{self._name}.mcstructure",
        )
        if not FileExists(
            os.path.join(
                "world", "structures", *self._sub_path, f"{self._name}.mcstructure"
            )
        ):
            raise FileNotFoundError(
                f"{self._name}.mcstructure not found in {os.path.join('assets', 'world', 'structures')}. Please ensure the file exists."
            )

    def queue(self):
        """Queues the structure to be exported."""
        ANVIL._queue(self)

    @property
    def identifier(self) -> Identifier:
        """Returns the identifier of the structure."""
        return f"{CONFIG.NAMESPACE}:{self._name}"

    @property
    def reference(self) -> str:
        """Returns the reference path of the structure."""
        return self._path.removesuffix(".mcstructure").removeprefix("structures\\")

    def _export(self):
        """Exports the structure to the file system."""
        CopyFiles(
            os.path.join("world", "structures", *self._sub_path),
            os.path.join(
                CONFIG.BP_PATH,
                "structures",
                CONFIG.NAMESPACE,
                *self._sub_path,
            ),
            f"{self._name}.mcstructure",
        )


class _JigsawStructureProcess(AddonObject):
    """A class representing a Structure Process in Minecraft."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "processors")
    _object_type = "Jigsaw Structure Process"

    class predicates:
        class _input_predicate:
            def __init__(self, processor: dict):
                self._dict = processor

            def always_true(self):
                self._dict["input_predicate"] = {
                    "predicate_type": "minecraft:always_true"
                }

            def block_match(self, identifier: str):
                self._dict["input_predicate"] = {
                    "predicate_type": "minecraft:block_match",
                    "block": identifier,
                }

            def random_block_match(self, identifier: str, probability: float):
                self._dict["input_predicate"] = {
                    "predicate_type": "minecraft:random_block_match",
                    "block": identifier,
                    "probability": clamp(probability, 0.0, 1.0),
                }

            def block_state_match(
                self, identifier: str, states: dict[str, str | int | float | bool]
            ):
                self._dict["input_predicate"] = {
                    "predicate_type": "minecraft:block_state_match",
                    "block_state": {
                        "name": identifier,
                        "states": {str(k): str(v) for k, v in states.items()},
                    },
                }

            def random_block_state_match(
                self,
                identifier: str,
                probability: float,
                states: dict[str, str | int | float | bool],
            ):
                self._dict["input_predicate"] = {
                    "predicate_type": "minecraft:random_block_state_match",
                    "block_state": {
                        "name": identifier,
                        "states": {str(k): str(v) for k, v in states.items()},
                    },
                    "probability": clamp(probability, 0.0, 1.0),
                }

            def tag_match(self, tag: str):
                self._dict["input_predicate"] = {
                    "predicate_type": "minecraft:tag_match",
                    "tag": tag,
                }

            def get(self):
                return self._dict

        class _position_predicate:
            def __init__(self, processor: dict):
                self._dict = processor

            def axis_aligned_linear_pos(
                self,
                min_chance: float,
                max_chance: float,
                min_distance: int,
                max_distance: int,
                axis: Literal["x", "y", "z"],
            ):
                self._dict["position_predicate"] = {
                    "predicate_type": "minecraft:axis_aligned_linear_pos",
                    "min_chance": clamp(min_chance, 0.0, 1.0),
                    "max_chance": clamp(max_chance, 0.0, 1.0),
                    "min_dist": min_distance,
                    "max_dist": max_distance,
                    "axis": axis,
                }

            def get(self):
                return self._dict

        class _location_predicate:
            def __init__(self, processor: dict):
                self._dict = processor

            def get(self):
                return self._dict

        def __init__(self, processor: dict):
            self.input_predicate = self._input_predicate(processor)
            self.position_predicate = self._position_predicate(processor)
            self.location_predicate = self._location_predicate(processor)

    def __init__(self, name: str):
        super().__init__(name)
        self.content(JsonSchemes.jigsaw_structure_process(self.identifier))

    def add_block_ignore_processor(self, blocks: list[str] | str):
        if isinstance(blocks, str):
            blocks = [blocks]
        if not isinstance(blocks, list):
            raise TypeError("blocks must be a list or a string")

        self._content["minecraft:processor_list"]["processors"].append(
            {"processor_type": "minecraft:block_ignore", "blocks": blocks}
        )

    def add_protected_blocks_processor(self, block_tag: str):
        if not isinstance(block_tag, str):
            raise TypeError("block_tag must be a string")

        self._content["minecraft:processor_list"]["processors"].append(
            {"processor_type": "minecraft:protected_blocks", "value": block_tag}
        )

    def add_capped_processor(
        self,
        delegate: StructureProcessors,
        limit: int | ConstantIntProvider | UniformIntProvider,
    ):
        if not isinstance(delegate, str):
            raise TypeError("delegate must be a string")
        if delegate not in ["minecraft:block_ignore", "minecraft:protected_blocks"]:
            raise ValueError(
                "delegate must be one of 'minecraft:block_ignore', 'minecraft:protected_blocks'"
            )
        if not isinstance(limit, (int, ConstantIntProvider, UniformIntProvider)):
            raise TypeError("limit must be an integer or a provider")

        if isinstance(limit, int):
            limit_data = limit
        elif isinstance(limit, ConstantIntProvider):
            limit_data = {"type": "constant", "value": limit["value"]}
        else:
            limit_data = {
                "type": "uniform",
                "min_inclusive": limit["min"],
                "max_inclusive": limit["max"],
            }

        self._content["minecraft:processor_list"]["processors"].append(
            {
                "processor_type": "minecraft:capped",
                "delegate": delegate,
                "limit": limit_data,
            }
        )

    def add_block_rule(
        self, output_block: str, loot_table_path: str = None
    ) -> predicates:
        if not isinstance(output_block, str):
            raise TypeError("output_block must be a string")
        if loot_table_path is not None and not isinstance(loot_table_path, str):
            raise TypeError("loot_table_path must be a string or None")

        processors: list[dict] = self._content["minecraft:processor_list"]["processors"]
        processor = next(
            (pr for pr in processors if pr.get("processor_type") == "minecraft:rule"),
            None,
        )
        if processor is None:
            processor = {"processor_type": "minecraft:rule", "rules": []}
            processors.append(processor)

        processor["rules"].append(
            {
                "input_predicate": {},
                "position_predicate": {},
                "location_predicate": {},
                "output_state": {"name": output_block},
            }
        )

        if loot_table_path:
            processor["block_entity_modifier"] = {
                "type": "minecraft:append_loot",
                "loot_table": loot_table_path,
            }

        predicate = _JigsawStructureProcess.predicates(processor["rules"][-1])
        return predicate

    def queue(
        self,
    ):
        return super().queue()


class _JigsawStructure(AddonObject):
    """A class representing a Jigsaw structure in Minecraft."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "jigsaw_structures")
    _object_type = "Jigsaw Structure"

    class _pool:
        def __init__(
            self,
        ):
            self._pools = []

        def direct_pool_alias(self, alias: str, target: str):
            """Creates a direct pool alias.

            Parameters:
                target (str): The target structure.
            """
            if not isinstance(target, str):
                raise TypeError("target must be a string")

            if not isinstance(alias, str):
                raise TypeError("alias must be a string")

            pool = _JigsawStructure._direct_pool_alias(alias, target)
            self._pools.append(pool)
            return pool

        def random_pool_aliases(self, alias: str):
            """Creates a random pool alias.

            Parameters:
                alias (str): The alias for the random pool.
            """
            if not isinstance(alias, str):
                raise TypeError("alias must be a string")

            pool = _JigsawStructure._random_pool_alias(alias)
            self._pools.append(pool)
            return pool

        def random_pool_group(self, weight: int):
            """Creates a random pool group.

            Parameters:
                weight (int): The weight of the random pool group.
            """
            if not isinstance(weight, int):
                raise TypeError("weight must be an integer")

            pool = _JigsawStructure._group_pool_alias()
            self._pools.append(pool)
            return pool

        def _export(self):
            """Exports the pool aliases to the content."""
            return {
                "pool_aliases": [pool._export() for pool in self._pools],
            }

    class _direct_pool_alias:
        def __init__(self, alias: str, target: str):
            """Initializes a direct pool alias.

            Parameters:
                alias (str): The alias for the direct pool.
                target (str): The target structure.
            """
            if not isinstance(alias, str):
                raise TypeError("alias must be a string")
            if not isinstance(target, str):
                raise TypeError("target must be a string")
            self._pool = {"type": "direct", "alias": alias, "target": target}

        def _export(self):
            """Exports the direct pool alias to the content."""
            return self._pool

    class _random_pool_alias:
        def __init__(self, alias: str):
            self._pool = {"type": "random", "alias": alias, "targets": []}

        def add_target(self, target: str, weight: int):
            """Adds a target to the random pool alias.

            Parameters:
                target (str): The target structure.
                weight (int): The weight of the target.
            """
            if not isinstance(target, str):
                raise TypeError("target must be a string")
            if not isinstance(weight, int):
                raise TypeError("weight must be an integer")
            self._pool["targets"].append({"data": target, "weight": weight})

        def _export(self):
            """Exports the random pool alias to the content."""
            return self._pool

    class _group_pool_alias(_pool):
        def __init__(self, weight: int):
            super().__init__()
            self._weight = weight

        def _export(self):
            return {
                "data": super()._export()["pool_aliases"],
                "weight": self._weight,
            }

    def __init__(
        self,
        name: str,
        start_pool: "JigsawStructureTemplatePool",
        max_depth: int,
        start_height: tuple[int, int] | int,
        placement_step: Literal[
            "raw_generation" "lakes",
            "local_modifications",
            "underground_structures",
            "surface_structures",
            "strongholds",
            "underground_ores",
            "underground_decoration",
            "fluid_springs",
            "vegetal_decoration",
            "top_layer_modification",
        ],
        start_jigsaw_name: str = None,
        liquid_settings: Literal[
            "apply_waterlogging", "ignore_waterlogging"
        ] = "apply_waterlogging",
        start_height_from_sea: bool = False,
    ):
        """Initializes a Jigsaw instance.

        Parameters:
            name (str): The name of the jigsaw structure.
            start_pool (JigsawStructureTemplatePool): The first Template Pool to use when generating the Jigsaw Structure.
            max_depth (int): The maximum recursion depth for Jigsaw Structure generation.
            start_height (tuple[int, int] | int): Height at which the Jigsaw Structure's start_pool should begin.
            placement_step (Literal[ 'raw_generation', 'lakes', 'local_modifications', 'underground_structures', 'surface_structures', 'strongholds', 'underground_ores', 'underground_decoration', 'fluid_springs', 'vegetal_decoration', 'top_layer_modification' ]): Specifies the world generation phase in which the Jigsaw Structure is generated.
            start_jigsaw_name (str, optional): The name of the Jigsaw Block from the start_pool to be placed first.
        """
        super().__init__(name)  # "jigsaw"

        if not isinstance(start_pool, JigsawStructureTemplatePool):
            raise TypeError(
                "start_pool must be an instance of JigsawStructureTemplatePool"
            )

        height = {}
        if isinstance(start_height, int):
            if start_height_from_sea:
                height = {"type": "constant", "value": {"from_sea": start_height}}
            else:
                height = {"type": "constant", "value": {"absolute": start_height}}

        elif isinstance(start_height, tuple) and len(start_height) == 2:
            height = {
                "type": "uniform",
                "min": {"above_bottom": min(start_height)},
                "max": {"below_top": max(start_height)},
            }
        else:
            raise TypeError("start_height must be an int or a tuple of two ints")

        self.content(
            JsonSchemes.jigsaw_structures(
                self.identifier,
                placement_step,
                start_pool.identifier,
                start_jigsaw_name,
                clamp(max_depth, 0, 20),
                height,
                liquid_settings,
            )
        )
        self._pool_aliases: _JigsawStructure._pool = None
        self._start_pool = start_pool

    def add_biome_filters(self, filter: Filter):
        """Adds biome filters to the jigsaw structure.

        Parameters:
            *filters (Filter): The biome filters to add.
        """
        self._content["minecraft:jigsaw"]["biome_filters"].append(filter)

    def terrain_adaptation(
        self,
        terrain_adaptation: Literal[
            "none", "bury", "beard_thin", "beard_box", "encapsulate"
        ],
    ):
        """Sets the terrain adaptation for the jigsaw structure.

        Parameters:
            terrain_adaptation (Literal['none', 'bury', 'beard_thin', 'beard_box', 'encapsulate']): The terrain adaptation to set.
            - "none" Do not adjust ambient block density.
            - "bury" Ambient block density will be added to all pieces of a structure, but only within the Y bounds of its starting piece. This is ideal for structures that need to bury themselves below the surface, but want another set of pieces to stick up through the terrain uncovered.
            - "beard_thin" Ambient block density will be added below the structure and block density will be reduced just above the ground.
            - "beard_box" Ambient block density will be added below the structure, and block density will be reduced within the entire box the structure occupies.
            - "encapsulate" Ambient block density will be added all around every piece of a structure.
        """
        if terrain_adaptation not in [
            "none",
            "bury",
            "beard_thin",
            "beard_box",
            "encapsulate",
        ]:
            raise ValueError("Invalid terrain adaptation value")
        self._content["minecraft:jigsaw"]["terrain_adaptation"] = terrain_adaptation

    def heightmap_projection(
        self, heightmap_projection: Literal["none", "world_surface", "ocean_floor"]
    ):
        """Sets the heightmap projection for the jigsaw structure.

        Parameters:
            heightmap_projection (Literal['none', 'world_surface', 'ocean_floor']): The heightmap projection to set.
        """
        if heightmap_projection not in ["none", "world_surface", "ocean_floor"]:
            raise ValueError("Invalid heightmap projection value")
        self._content["minecraft:jigsaw"]["heightmap_projection"] = heightmap_projection

    def dimension_padding(self, dimension_padding: tuple[int, int]):
        """Sets the dimension padding for the jigsaw structure.

        Parameters:
            dimension_padding (tuple[int, int]): The dimension padding to set.
        """
        if not isinstance(dimension_padding, tuple) or len(dimension_padding) != 2:
            raise TypeError("dimension_padding must be a tuple of two integers")
        self._content["minecraft:jigsaw"]["dimension_padding"] = dimension_padding

    def max_distance_from_center(self, horizontal: int, vertical: int):
        """Sets the maximum distance from center for the jigsaw structure.

        Parameters:
            horizontal (int): The maximum horizontal distance from center to set.
            vertical (int): The maximum vertical distance from center to set.
        """
        if not isinstance(horizontal, int):
            raise TypeError("horizontal must be an integer")
        if not isinstance(vertical, int):
            raise TypeError("vertical must be an integer")
        self._content["minecraft:jigsaw"]["max_distance_from_center"] = {
            "horizontal": horizontal,
            "vertical": vertical,
        }

    @property
    def pool_aliases(self) -> "_JigsawStructure._pool":
        """Returns the pool aliases for the jigsaw structure."""
        self._pool_aliases = self._pool()
        return self._pool_aliases

    def queue(self):
        return super().queue()

    def _export(self):
        self._content["minecraft:jigsaw"]["pool_aliases"] = self.pool_aliases._export()
        return super()._export()


class JigsawStructureTemplatePool(AddonObject):
    """A class representing a Structure Template Pool in Minecraft."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "template_pools")
    _object_type = "Jigsaw Structure Template Pool"

    def __init__(self, name: str, fallback: str = None):
        """Initializes a JigsawStructureTemplatePool instance.

        Parameters:
            name (str): The name of the template pool.
            fallback (str, optional): The fallback structure for the pool. Defaults to None.
        """
        super().__init__(name)  # "structure_template_pool"
        self.content(JsonSchemes.jigsaw_template_pools(self.identifier, fallback))
        self._structures: list[Structure] = []
        self._processors: list[_JigsawStructureProcess] = []

    def add_structure_element(
        self,
        structure: Structure | str | None,
        processors_name: str | _JigsawStructureProcess,
        weight: int = 1,
        projection: Literal[
            "minecraft:rigid", "minecraft:terrain_matching"
        ] = "minecraft:rigid",
    ) -> _JigsawStructureProcess | None:
        """Adds a structure to the template pool.

        Parameters:
            structure (str | Structure | None): The structure to add to the pool.
            weight (int, optional): The weight of the structure. Defaults to 1.
            processors_name (str, optional): The name of the processors for the structure. Defaults to None.
            projection (Literal["minecraft:rigid", "minecraft:terrain_matching"], optional): The projection type. Defaults to "minecraft:rigid".
        """
        if not isinstance(structure, (Structure, str, type(None))):
            raise TypeError("structure must be an instance of Structure or str")

        if not isinstance(processors_name, (str, _JigsawStructureProcess)):
            raise TypeError(
                "processors_name must be an instance of str or JigsawStructureProcess"
            )

        if isinstance(structure, str):
            structure = Structure(structure)
            self._structures.append(structure)

        if isinstance(processors_name, str):
            processors_name: _JigsawStructureProcess = _JigsawStructureProcess(
                processors_name
            )

        self._processors.append(processors_name)

        self._content["minecraft:template_pool"]["elements"].append(
            {
                "element": {
                    "element_type": (
                        "minecraft:single_pool_element"
                        if structure
                        else "minecraft:empty_pool_element"
                    ),
                    "location": structure.reference if structure else {},
                    "processors": processors_name.identifier if processors_name else {},
                    # "terrain_projection": projection if projection else {},
                },
                "weight": weight,
            }
        )

        return processors_name

    def queue(self):
        for processor in self._processors:
            processor.queue()
        for structure in self._structures:
            structure.queue()
        super().queue()


class JigsawStructureSet(AddonObject):
    """A class representing a Structure Set in Minecraft.
    A Structure Set contains a set of Jigsaw Structures and rules for how those
    structures should be placed in the world relative to other instances of structures
    from the same set. Each structure within a set is paired with a weight that
    influences how frequently it is chosen.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "structure_sets")
    _structures: list[_JigsawStructure] = []
    _object_type = "Jigsaw Structure Set"

    def __init__(
        self,
        name: str,
        separation: int = 4,
        spacing: int = 10,
        spread_type: Literal["linear", "triangle"] = "linear",
        placement_type: Literal["minecraft:random_spread"] = "minecraft:random_spread",
    ):
        """Initializes a JigsawStructureSet instance.

        Parameters:
            name (str): The name of the structure set.
            separation (int): Padding (in chunks) within each grid cell. Structures will not generate within the padded area.
            spacing (int): Grid cell size (in chunks) to use when generating the structure. Structures will attempt to generate at a random position within each cell.
            spread_type (Literal["linear", "triangle"]): Randomness algorithm used when placing structures.
            placement_type (Literal["minecraft:random_spread"]): Describes where structures in the set spawn relative to one another. Currently, the only placement type supported is random_spread, which scatters structures randomly with a given separation and spacing.
        """
        super().__init__(name)  # "structure_set"
        self.content(
            JsonSchemes.jigsaw_structure_set(
                self.identifier, separation, spacing, spread_type, placement_type
            )
        )

    def add_jigsaw_structure(
        self,
        structure_name: str,
        start_pool: "JigsawStructureTemplatePool",
        max_depth: int,
        start_height: tuple[int, int] | int,
        placement_step: Literal[
            "raw_generation" "lakes",
            "local_modifications",
            "underground_structures",
            "surface_structures",
            "strongholds",
            "underground_ores",
            "underground_decoration",
            "fluid_springs",
            "vegetal_decoration",
            "top_layer_modification",
        ],
        weight: int = 1,
        start_jigsaw_name: str = None,
        liquid_settings: Literal[
            "apply_waterlogging", "ignore_waterlogging"
        ] = "apply_waterlogging",
        start_height_from_sea: bool = False,
    ):
        """Adds a jigsaw structure to the structure set.

        Parameters:
            structure_name (str): The name of the jigsaw structure to add.
            weight (int): The weight of the structure in the set. Defaults to 1.
        """

        structure = _JigsawStructure(
            structure_name,
            start_pool,
            max_depth,
            start_height,
            placement_step,
            start_jigsaw_name,
            liquid_settings,
            start_height_from_sea,
        )
        self._structures.append(structure)
        self._content["minecraft:structure_set"]["structures"].append(
            {"structure": structure.identifier, "weight": weight}
        )
        return structure

    def queue(self):
        for structure in self._structures:
            structure.queue()

        return super().queue()
