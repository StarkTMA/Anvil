import os
from typing import Literal, TypedDict

from anvil import ANVIL, CONFIG
from anvil.api.actors.components import Filter
from anvil.lib.lib import CopyFiles, FileExists, clamp
from anvil.lib.schemas import AddonObject, JsonSchemes
from anvil.lib.types import (ConstantIntProvider, Identifier,
                             StructureProcessors, UniformIntProvider)


class Structure:
    """A class representing a Structure."""

    def __init__(self, structure_name: str):
        """Initializes a Structure instance.

        Parameters:
            structure_name (str): The name of the structure.
        """
        self._structure_name = structure_name
        self._path = os.path.join(CONFIG.BP_PATH, "structures", CONFIG.NAMESPACE, f"{self._structure_name}.mcstructure")
        if not FileExists(os.path.join("assets", "world", f"{self._structure_name}.mcstructure")):
            CONFIG.Logger.file_exist_error(f"{self._structure_name}.mcstructure", os.path.join("assets", "world"))

    def queue(self):
        """Queues the structure to be exported."""
        ANVIL._queue(self)

    @property
    def identifier(self) -> Identifier:
        """Returns the identifier of the structure."""
        return f"{CONFIG.NAMESPACE}:{self._structure_name}"

    @property
    def reference(self) -> str:
        """Returns the reference path of the structure."""
        return self._path.removesuffix(".mcstructure")

    def _export(self):
        """Exports the structure to the file system."""
        CopyFiles(
            os.path.join("assets", "world"),
            os.path.join(
                CONFIG.BP_PATH,
                "structures",
                CONFIG.NAMESPACE,
            ),
            f"{self._structure_name}.mcstructure",
        )


class __JigsawStructureProcess(AddonObject):
    """A class representing a Structure Process in Minecraft."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "processors")

    class predicates(TypedDict):
        class input_predicate(TypedDict):
            def __init__(self):
                self._dict = {}

            def always_true(self):
                self.predicate_type = "minecraft:always_true"

            def block_match(self, identifier: str):
                self.predicate_type = "minecraft:block_match"
                self.block = identifier

            def random_block_match(self, identifier: str, probability: float):
                self.predicate_type = "minecraft:random_block_match"
                self.block = identifier
                self.probability = clamp(probability, 0.0, 1.0)

            def block_state_match(self, identifier: str, *states: dict[str, str | int | float | bool]):
                """Matches a block state based on its identifier and states.

                Parameters:
                    identifier (str): The block identifier.
                    states (dict[str, str | int]): The block states to match.
                """
                self.predicate_type = "minecraft:block_state_match"
                self.block_state = {"name": identifier, "states": {str(k): str(v) for k, v in states}}

            def random_block_state_match(self, identifier: str, probability: float, *states: dict[str, str | int | float | bool]):
                """Matches a random block state based on its identifier, states, and probability.

                Parameters:
                    identifier (str): The block identifier.
                    probability (float): The probability of matching the block state.
                    states (dict[str, str | int]): The block states to match.
                """
                self.predicate_type = "minecraft:random_block_state_match"
                self.block_state = {
                    "name": identifier,
                    "states": {str(k): str(v) for k, v in states},
                }
                self.probability = clamp(probability, 0.0, 1.0)

            def tag_match(self, tag: str):
                """Matches a block based on its tag.

                Parameters:
                    tag (str): The block tag to match.
                """
                self.predicate_type = "minecraft:tag_match"
                self.tag = tag

        class position_predicate(TypedDict):
            def axis_aligned_linear_pos(
                self, min_chance: float, max_chance: float, min_distance: int, max_distance: int, axis: Literal["x", "y", "z"]
            ):
                """Sets the position predicate to axis-aligned linear position.

                Parameters:
                    min_chance (float): The minimum chance of the position.
                    max_chance (float): The maximum chance of the position.
                    min_distance (int): The minimum distance from the structure.
                    max_distance (int): The maximum distance from the structure.
                """
                self.predicate_type = "minecraft:axis_aligned_linear_pos"
                self.min_chance = clamp(min_chance, 0.0, 1.0)
                self.max_chance = clamp(max_chance, 0.0, 1.0)
                self.min_dist = min_distance
                self.max_dist = max_distance
                self.axis = axis

        class location_predicate(TypedDict):
            pass

        def input(self):
            """Creates a new input predicate for the structure process.
            Returns:
                __JigsawStructureProcess.input_predicate: A new input predicate instance.
            """
            p = __JigsawStructureProcess.input_predicate()
            self.input_predicate = p
            return p

        def position(self):
            """Creates a new position predicate for the structure process.
            Returns:
                __JigsawStructureProcess.position_predicate: A new position predicate instance.
            """
            p = __JigsawStructureProcess.position_predicate()
            self.position_predicate = p
            return p

        def location(self):
            """Creates a new location predicate for the structure process.
            Returns:
                __JigsawStructureProcess.location_predicate: A new location predicate instance.
            """
            p = __JigsawStructureProcess.location_predicate()
            self.location_predicate = p
            return p

    def __init__(self, name: str):
        """Initializes a StructureProcess instance.

        Parameters:
            name (str): The name of the structure process.
        """
        super().__init__(name, "structure_process")
        self.content(JsonSchemes.jigsaw_structure_process(f"{CONFIG.NAMESPACE}:{name}"))

    def add_block_ignore_processor(self, blocks: list[str] | str):
        """Adds a block ignore processor to the structure process.

        Parameters:
            blocks (list[str] | str): The blocks to ignore in the structure.
        """
        if isinstance(blocks, str):
            blocks = [blocks]
        if not isinstance(blocks, list):
            raise TypeError("blocks must be a list or a string")

        self._content["minecraft:processor_list"]["processors"].append(
            {
                "processor_type": "minecraft:block_ignore",
                "blocks": [str(block) for block in blocks],
            }
        )

    def add_protected_blocks_processor(self, block_tag: str):
        """Specifies which blocks in the world cannot be overridden by this structure.

        Parameters:
            blocks (list[str] | str): The blocks to protect in the structure.
        """
        if not isinstance(block_tag, str):
            raise TypeError("block_tag must be a string")

        self._content["minecraft:processor_list"]["processors"].append(
            {
                "processor_type": "minecraft:protected_blocks",
                "value": block_tag,
            }
        )

    def add_capped_processor(
        self,
        delegate: StructureProcessors,
        limit: int | ConstantIntProvider | UniformIntProvider,
    ):
        """Applies a processor to some random blocks instead of applying it to all blocks, with a limit on the number of times it can be applied.

        Parameters:
            delegate (StructureProcessors): The type of processor to cap.
            limit (int | ConstantIntProvider | UniformIntProvider): The maximum number of blocks to cap.
        """
        if not isinstance(delegate, str):
            raise TypeError("delegate must be a string")
        if delegate not in ["minecraft:block_ignore", "minecraft:protected_blocks", "minecraft:capped"]:
            raise ValueError("delegate must be one of 'minecraft:block_ignore', 'minecraft:protected_blocks'")
        if delegate == "minecraft:capped":
            raise ValueError("delegate cannot be 'minecraft:capped' for a capped processor")
        if not isinstance(limit, (int, ConstantIntProvider, UniformIntProvider)):
            raise TypeError("limit must be an integer or a provider")

        self._content["minecraft:processor_list"]["processors"].append(
            {
                "processor_type": "minecraft:capped",
                "delegate": delegate,
                "limit": (
                    limit
                    if isinstance(limit, int)
                    else {
                        "type": "constant" if isinstance(limit, ConstantIntProvider) else "uniform",
                        "value": limit["value"] if "value" in limit else {},
                        "min_inclusive": limit["min"] if "min" in limit else {},
                        "max_inclusive": limit["max"] if "max" in limit else {},
                    }
                ),
            }
        )

    def add_block_rule(self, output_block: str, loot_table_path: str = None) -> predicates:
        """Adds a block rule to the structure.

        Parameters:
            output_block (str): The block to output.
            loot_table_path (str): The path to the loot table.
        """
        if not isinstance(output_block, str):
            raise TypeError("output_block must be a string")
        if not isinstance(loot_table_path, str):
            raise TypeError("loot_table_path must be a string")

        predicate = __JigsawStructureProcess.predicates()

        self._content["minecraft:processor_list"]["processors"].append(
            {
                "processor_type": "minecraft:rule",
                "output_state": {
                    "name": output_block,
                },
                "block_entity_modifier": (
                    {
                        "type": "minecraft:append_loot",
                        "loot_table": loot_table_path,
                    }
                    if loot_table_path
                    else {}
                ),
                **predicate,
            }
        )


class __JigsawStructure(AddonObject):
    """A class representing a Jigsaw structure in Minecraft."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "jigsaw_structures")

    class pool:
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

            pool = __JigsawStructure.direct_pool_alias(alias, target)
            self._pools.append(pool)
            return pool

        def random_pool_aliases(self, alias: str):
            """Creates a random pool alias.

            Parameters:
                alias (str): The alias for the random pool.
            """
            if not isinstance(alias, str):
                raise TypeError("alias must be a string")

            pool = __JigsawStructure.random_pool_alias(alias)
            self._pools.append(pool)
            return pool

        def random_pool_group(self, weight: int):
            """Creates a random pool group.

            Parameters:
                weight (int): The weight of the random pool group.
            """
            if not isinstance(weight, int):
                raise TypeError("weight must be an integer")

            pool = __JigsawStructure.group_pool_alias()
            self._pools.append(pool)
            return pool

        def _export(self):
            """Exports the pool aliases to the content."""
            return {
                "pool_aliases": [pool._export() for pool in self._pools],
            }

    class direct_pool_alias:
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

    class random_pool_alias:
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

    class group_pool_alias(pool):
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
        start_height: int,
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
        liquid_settings: Literal["apply_waterlogging", "ignore_waterlogging"] = "apply_waterlogging",
    ):
        """Initializes a Jigsaw instance.

        Parameters:
            name (str): The name of the jigsaw structure.
            placement_step (Literal["surface_structures", "underground_structures"]): The placement step for the jigsaw structure.
            terrain_adaptation (Literal['none', 'bury']): The terrain adaptation for the jigsaw structure.
            start_pool (JigsawStructureTemplatePool): The template pool for the jigsaw structure.
        """
        super().__init__(name, "jigsaw")
        if not isinstance(start_pool, JigsawStructureTemplatePool):
            raise TypeError("start_pool must be an instance of JigsawStructureTemplatePool")

        self.content(
            JsonSchemes.jigsaw_structures(
                f"{CONFIG.NAMESPACE}:{name}",
                placement_step,
                start_pool.identifier,
                start_jigsaw_name,
                clamp(max_depth, 0, 20),
                start_height,
                liquid_settings,
            )
        )
        self.pool_aliases = []

    def add_biome_filters(self, filter: Filter):
        """Adds biome filters to the jigsaw structure.

        Parameters:
            *filters (Filter): The biome filters to add.
        """
        if not isinstance(filter, Filter):
            raise TypeError("filter must be an instance of Filter")
        self._content["minecraft:jigsaw"]["biome_filters"].append(filter)

    def terrain_adaptation(self, terrain_adaptation: Literal["none", "bury", "beard_thin", "beard_box", "encapsulate"]):
        """Sets the terrain adaptation for the jigsaw structure.

        Parameters:
            terrain_adaptation (Literal['none', 'bury', 'beard_thin', 'beard_box', 'encapsulate']): The terrain adaptation to set.
        """
        if terrain_adaptation not in ["none", "bury", "beard_thin", "beard_box", "encapsulate"]:
            raise ValueError("Invalid terrain adaptation value")
        self._content["minecraft:jigsaw"]["terrain_adaptation"] = terrain_adaptation

    def heightmap_projection(self, heightmap_projection: Literal["none", "world_surface"]):
        """Sets the heightmap projection for the jigsaw structure.

        Parameters:
            heightmap_projection (Literal['none', 'world_surface']): The heightmap projection to set.
        """
        if heightmap_projection not in ["none", "world_surface"]:
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
    def pool_aliases(self) -> "__JigsawStructure.pool":
        """Returns the pool aliases for the jigsaw structure."""
        return self.pool()

    def _export(self):
        self._content["minecraft:jigsaw"]["pool_aliases"] = self.pool_aliases._export()
        return super()._export()


class JigsawStructureTemplatePool(AddonObject):
    """A class representing a Structure Template Pool in Minecraft."""

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "template_pools")

    def __init__(self, name: str, fallback: str = None):
        """Initializes a JigsawStructureTemplatePool instance.

        Parameters:
            name (str): The name of the template pool.
            fallback (str, optional): The fallback structure for the pool. Defaults to None.
        """
        super().__init__(name, "structure_template_pool")
        self.content(JsonSchemes.jigsaw_template_pools(f"{CONFIG.NAMESPACE}:{name}", fallback))
        self._structures: list[Structure] = []
        self._processors: list[__JigsawStructureProcess] = []

    def add_structure_element(
        self,
        structure: Structure | str | None,
        weight: int = 1,
        processors_name: str = None,
        projection: Literal["minecraft:rigid", "minecraft:terrain_matching"] = "minecraft:rigid",
    ) -> __JigsawStructureProcess | None:
        """Adds a structure to the template pool.

        Parameters:
            structure (str | Structure | None): The structure to add to the pool.
            weight (int, optional): The weight of the structure. Defaults to 1.
            processors_name (str, optional): The name of the processors for the structure. Defaults to None.
            projection (Literal["minecraft:rigid", "minecraft:terrain_matching"], optional): The projection type. Defaults to "minecraft:rigid".
        """
        if not isinstance(structure, (Structure, str, None)):
            raise TypeError("structure must be an instance of Structure or str")
        if not isinstance(processors_name, str):
            raise TypeError("processors_name must be an instance of str")

        if isinstance(structure, str):
            structure = Structure(structure)
            self._structures.append(structure)

        if isinstance(processors_name, str):
            processors_name: __JigsawStructureProcess = __JigsawStructureProcess(processors_name)
            self._processors.append(processors_name)

        self._content["minecraft:template_pool"]["elements"].append(
            {
                "element": {
                    "element_type": "minecraft:single_pool_element" if structure else "minecraft:empty_pool_element",
                    "location": structure.reference if structure else {},
                    "processors": processors_name.identifier if processors_name else {},
                    "projection": projection if projection else {},
                },
                "weight": weight,
            }
        )

        return processors_name

    def queue(self, directory=None):
        super().queue(directory)
        for structure in self._structures:
            structure.queue()


class JigsawStructureSet(AddonObject):
    """A class representing a Structure Set in Minecraft.
    A Structure Set contains a set of Jigsaw Structures and rules for how those
    structures should be placed in the world relative to other instances of structures
    from the same set. Each structure within a set is paired with a weight that
    influences how frequently it is chosen.
    """

    _extension = ".json"
    _path = os.path.join(CONFIG.BP_PATH, "worldgen", "structure_sets")
    _structures: list[__JigsawStructure] = []

    def __init__(self, name: str, separation: int = 10, spacing: int = 4, spread_type: Literal["linear", "triangle"] = "linear"):
        """Initializes a JigsawStructureSet instance.

        Parameters:
            name (str): The name of the structure set.
        """
        super().__init__(name, "structure_set")
        self.content(JsonSchemes.jigsaw_structure_set(f"{CONFIG.NAMESPACE}:{name}", separation, spacing, spread_type))

    def add_jigsaw_structure(self, structure_name: str, weight: int = 1):
        """Adds a jigsaw structure to the structure set.

        Parameters:
            structure_name (str): The name of the jigsaw structure to add.
            weight (int): The weight of the structure in the set. Defaults to 1.
        """

        structure = __JigsawStructure(structure_name)
        self._structures.append(structure)
        self._content["minecraft:structure_set"]["structures"].append({"structure": structure.identifier, "weight": weight})
        return structure
